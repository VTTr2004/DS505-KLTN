from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, FloatType

# import os
# os.environ['PYSPARK_PYTHON'] = r'C:\Users\trung\AppData\Local\Programs\Python\Python310\python.exe'

spark = SparkSession.builder\
    .master("local[*]")\
    .appName("KLTN")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()
# spark.conf.set("spark.sql.adaptive.enabled", "true")

spark_reader = spark.readStream\
    .format('kafka')\
    .option('kafka.bootstrap.servers', 'localhost:9092')\
    .option('subscribe', 'cam')\
    .option('startingOffsets', 'latest')\
    .load()

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StringType
from ultralytics import YOLO
from kafka import KafkaProducer
from pyspark.sql.window import Window
from pyspark.sql import functions as F

import pandas as pd
import numpy as np
import base64
import pickle
import cv2

model = None
producer = None

schema = StructType([
    StructField("cam", StringType(), True),
    StructField("data", StringType(), True)
])

parsed_df = spark_reader.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .withColumn("batch_id", (F.row_number().over(Window.orderBy('some_column')) - 1) // 10) \
    .groupBy('batch_id') \
    .agg(F.collect_list('data').alias('batch_images')) 

@pandas_udf(StringType())
def detect_with_yolo_udf(image_data: pd.Series) -> pd.Series:
    results = []
    global model, producer
    if model is None:
        model = YOLO("./model/final.pt")
    if producer is None:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def Extract_Color(img_hsv: np.ndarray, box) -> list:
        h = np.mean(img_hsv[box[0]:box[2],box[1]:box[3],0])
        s = np.mean(img_hsv[box[0]:box[2],box[1]:box[3],1])
        v = np.mean(img_hsv[box[0]:box[2],box[1]:box[3],2])
        return [box[-1] * 1000] + [h,s,v] + box[:4]

    for data in image_data:
        try:
            img = base64.b64decode(data['data'])
            img = np.frombuffer(img, np.uint8)
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        except:
            print("khong doc duoc anh")

        try:
            img_array = np.array(img)
            pred = model.predict(img_array, verbose = False)[0]
            img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            temp = [Extract_Color(img_hsv, box) for box in pred.xyxy]
            results.extend([data, temp])
        except:
            print('Khong co anh')
    if results:
        producer.send("Chars", value = pickle.dumps(results))
        producer.flush()

    return image_data


from pyspark.sql.functions import from_json, col


parsed_df = spark_reader.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .withColumn("batch_id", (F.row_number().over(Window.orderBy('some_column')) - 1) // 10)\
    .groupBy('batch_id').agg(F.collect_list('data').alias('batch_images'))\
    .withColumn("batch_id", detect_with_yolo_udf(col("batch_id"))) \

writer = parsed_df.writeStream \
    .outputMode("append") \
    .format("noop")
    
query = writer.start()
query.awaitTermination()