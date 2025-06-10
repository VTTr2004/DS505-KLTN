from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import to_json, from_json, col, pandas_udf

spark = SparkSession.builder\
    .master("local[*]")\
    .appName("KLTN")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

spark_reader = spark.readStream\
    .format('kafka')\
    .option('kafka.bootstrap.servers', '192.168.1.240:9092')\
    .option('subscribe', 'cam')\
    .option('startingOffsets', 'latest')\
    .load()

schema = StructType([
    StructField("cam", StringType(), True),
    StructField("img", StringType(), True)
])

parsed_df = spark_reader.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select(col("data.cam").alias("cam"), col("data.img").alias("img"))
parsed_df = parsed_df.withColumn("json", f.to_json(f.struct("cam", "img")))

#---------------------------------------------------------#
from ultralytics import YOLO
import pandas as pd
import numpy as np
import cv2
import json
import base64

_model = None
def load_model():
    global _model
    if _model is None:
        _model = YOLO('./model/model_ver4.pt')
    return _model

@pandas_udf(StringType())
def Run(json_series: pd.Series) -> pd.Series:
    cam_list = []
    img_list = []
    result_list = []

    for json_str in json_series:
        try:
            data = json.loads(json_str)
            cam = data['cam']
            img_data = base64.b64decode(data['img'])
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is not None:
                cam_list.append(cam)
                img_list.append(img)
            else:
                result_list.append(json.dumps({'cam': cam, 'error': False}))
        except Exception as e:
            result_list.append(json.dumps({'cam': None, 'error': False}))

    # Predict 1 lần nếu có ảnh hợp lệ
    if img_list:
        model = load_model()
        preds = model.predict(img_list)

        for cam, img, pred in zip(cam_list, img_list, preds):
            success, enc_img = cv2.imencode('.jpg', img)
            if success:
                img_b64 = base64.b64encode(enc_img).decode('utf-8')
                result_list.append(json.dumps({
                    'cam': cam,
                    'img': img_b64,
                    'result': pred.names  # hoặc pred.tojson()
                }))
            else:
                result_list.append(json.dumps({
                    'cam': cam,
                    'error': False
                }))

    return pd.Series(result_list)
#---------------------------------------------------------#

parsed_df = parsed_df.withColumn('out_put', Run(col('json'))) \
    .selectExpr("CAST(out_put AS STRING) as value")
query = parsed_df.select(col('value')).writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.1.240:9092") \
    .option("topic", "check_error") \
    .option("checkpointLocation", "./checkpoints/check_error") \
    .outputMode("append") \
    .trigger(processingTime="2 seconds") \
    .start()
query.awaitTermination()

# def process_batch(df, epoch_id):
#     from pyspark.sql.functions import expr

#     # Gom 5 ảnh mỗi lần
#     batched_df = df.repartition(1)\
#                    .withColumn("row_id", expr("monotonically_increasing_id()")) \
#                    .withColumn("group_id", (col("row_id") / 5).cast("int")) \
#                    .groupBy("group_id") \
#                    .agg(f.collect_list("data").alias("batch_data")) \
#                    .select(to_json(col("batch_data")).alias("value"))

#     # Ghi vào Kafka
#     batched_df.write \
#         .format("kafka") \
#         .option("kafka.bootstrap.servers", "localhost:9092") \
#         .option("topic", "check_error") \
#         .save()

# query = parsed_df.writeStream \
#     .foreachBatch(process_batch) \
#     .option("checkpointLocation", "./checkpoints/check_error") \
#     .start()
# query.awaitTermination()