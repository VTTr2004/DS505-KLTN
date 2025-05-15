from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json, col

spark = SparkSession.builder\
    .master("local[*]")\
    .appName("KLTN")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")
spark.conf.set("spark.driver.memory", "4g")
spark.conf.set("spark.executor.memory", "4g")
sc = spark.sparkContext

spark_reader = spark.readStream\
    .format('kafka')\
    .option('kafka.bootstrap.servers', 'localhost:9092')\
    .option('subscribe', 'cam')\
    .option('startingOffsets', 'latest')\
    .load()

schema = StructType([
    StructField("cam", StringType(), True),
    StructField("img", StringType(), True)
])

parsed_df = spark_reader.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select(col('data.cam').alias('cam'))
    # .groupBy()\
    # .agg(
    #     f.collect_list("data").alias("batch_data"),
    # )
#-------------------------------------------------------------#

from ultralytics import YOLO

def load_yolo_model():
    model = YOLO("./model/final.pt")
    return model
broadcasted_model = sc.broadcast(load_yolo_model())

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import ArrayType, FloatType
from pyspark.sql.functions import to_json, struct
import pandas as pd
import numpy as np
import json
import base64 
import cv2

@pandas_udf(ArrayType(StringType()))
def detect_yolo(json_list: pd.Series) -> pd.Series:
    results = []
    try:
        for js in json_list:
            results.append('da doc duoc')
        return results
    except:
        return json_list





    try:
        model = broadcasted_model.value
    except:
        # results.append("Lỗi model")
        return json_list
        # return pd.Series([json.dumps({"error": "load_model", "detail": str(e)})])

    img_list = []
    cam_list = []

    temp = []
    for js in json_list:
        try:
            js = json.load(js)
            cam_list.append(js['cam'])
            img_list.append(js['img'])

            # Decode image
            img = base64.b64decode(js['img'])
            img = np.frombuffer(img, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            temp.append(img)
        except Exception as e:
            results.append("Lỗi xử lý ảnh ở index:")
            # return pd.Series([json.dumps({"error": "decode_image", "index": "kjdsf", "detail": str(e)})])

    try:
        results = model.predict(temp)
        results = [{'class': r.cls, 'bbox': r.xyxy} for r in results]
    except Exception as e:
        results.append("Lỗi khi chạy model.predict:")
        # return pd.Series([json.dumps({"error": "model_predict", "detail": str(e)})])
    return pd.Series(results)
    # try:
    #     data = [{
    #         "cam_list": cam_list,
    #         "img_list": img_list,
    #         'results': results
    #     }]
    #     return pd.Series([json.dumps(data)])
    # except Exception as e:
    #     print("Lỗi khi trả về kết quả:", e)
    #     return pd.Series([json.dumps({"error": "return_output", "detail": str(e)})])

#-------------------------------------------------------------# 
# parsed_df = parsed_df.withColumn("batch_result", detect_yolo(col('cam')))\
#     .select("batch_result")
writer = parsed_df.writeStream \
    .outputMode("append") \
    .format("console")

# writer = parsed_df.writeStream \
#     .outputMode("append") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("topic", "check_error") \
#     .option("checkpointLocation", "./checkpoints/check_error") \
#     .format("kafka")
print("Arrow status:", spark.conf.get("spark.sql.execution.arrow.pyspark.enabled"))
query = writer.start()
query.awaitTermination()