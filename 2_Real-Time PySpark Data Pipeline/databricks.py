#15.4 LTS (includes Apache Spark 3.5.0, Scala 2.12)
#org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.5 > type maven library
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

spark.conf.set("fs.s3a.access.key", "xxx")
spark.conf.set("fs.s3a.secret.key", "xxx")
spark.conf.set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")
# df = spark.read.format("parquet").load("s3a://mlops-clean-data-bucket/path/customer_features/")
# df.show()
#-----------------------------

# Define schema
schema = StructType() \
    .add("customer_id", StringType()) \
    .add("event", StringType()) \
    .add("timestamp", StringType()) \
    .add("product_id", StringType()) \
    .add("amount", DoubleType())

# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "44.198.175.56:9092") \
    .option("subscribe", "customer_events") \
    .option("startingOffsets", "latest") \
    .load()

# Extract value (in JSON string format)
json_df = kafka_df.selectExpr("CAST(value AS STRING)")

# Parse JSON to columns
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

parsed_df.printSchema()

parsed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .option("checkpointLocation", "/tmp/spark_checkpoints") \
    .start()

parsed_df.writeStream \
    .format("parquet") \
    .option("path", "s3a://mlops-clean-data-bucket/customer_features/") \
    .option("checkpointLocation", "/tmp/checkpoints/feature-stream/") \
    .outputMode("append") \
    .trigger(processingTime='30 seconds') \
    .start()

query.awaitTermination()
