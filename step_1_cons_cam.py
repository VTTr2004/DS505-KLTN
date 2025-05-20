from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import to_json, from_json, col

spark = SparkSession.builder\
    .master("local[*]")\
    .appName("KLTN")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

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

def process_batch(df, epoch_id):
    from pyspark.sql.functions import expr

    # Gom 5 ảnh mỗi lần
    batched_df = df.repartition(1)\
                   .withColumn("row_id", expr("monotonically_increasing_id()")) \
                   .withColumn("group_id", (col("row_id") / 5).cast("int")) \
                   .groupBy("group_id") \
                   .agg(f.collect_list("data").alias("batch_data")) \
                   .select(to_json(col("batch_data")).alias("value"))

    # Ghi vào Kafka
    batched_df.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "check_error") \
        .save()

query = parsed_df.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "./checkpoints/check_error") \
    .start()
query.awaitTermination()