# %%
# ! pip install -U pyspark==3.5.1
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 stream.py

# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# %%
kafka_bootstrap_servers = "localhost:9092"
source_topic = "service-requests-events"
destination_topic = "cleaned-service-requests-events"

# %%
spark = (
    SparkSession.builder.appName("Streaming from Kafka")
    .config("spark.streaming.stopGracefullyOnShutdown", True)
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1")
    .config("spark.sql.shuffle.partitions", 4)
    .master("local[*]")
    .getOrCreate()
)

# %%
schema = StructType(
    [
        StructField("created_date", TimestampType(), True),
        StructField("resolution_action_updated_date", TimestampType(), True),
        StructField("closed_date", TimestampType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("x_coordinate_state_plane", IntegerType(), True),
        StructField("y_coordinate_state_plane", IntegerType(), True),
        StructField("unique_key", StringType(), True),
        StructField("agency", StringType(), True),
        StructField("agency_name", StringType(), True),
        StructField("complaint_type", StringType(), True),
        StructField("descriptor", StringType(), True),
        StructField("location_type", StringType(), True),
        StructField("incident_zip", StringType(), True),
        StructField("incident_address", StringType(), True),
        StructField("street_name", StringType(), True),
        StructField("cross_street_1", StringType(), True),
        StructField("cross_street_2", StringType(), True),
        StructField("intersection_street_1", StringType(), True),
        StructField("intersection_street_2", StringType(), True),
        StructField("address_type", StringType(), True),
        StructField("city", StringType(), True),
        StructField("landmark", StringType(), True),
        StructField("status", StringType(), True),
        StructField("community_board", StringType(), True),
        StructField("bbl", StringType(), True),
        StructField("borough", StringType(), True),
        StructField("open_data_channel_type", StringType(), True),
        StructField("park_facility_name", StringType(), True),
        StructField("park_borough", StringType(), True),
        StructField(
            "location",
            StructType(
                [
                    StructField("latitude", FloatType(), True),
                    StructField("longitude", FloatType(), True),
                    StructField(
                        "human_address", MapType(StringType(), StringType()), True
                    ),
                ]
            ),
            True,
        ),
        StructField(":@computed_region_efsh_h5xi", StringType(), True),
        StructField(":@computed_region_f5dn_yrer", StringType(), True),
        StructField(":@computed_region_yeji_bk3q", StringType(), True),
        StructField(":@computed_region_92fq_4b7q", StringType(), True),
        StructField(":@computed_region_sbqj_enih", StringType(), True),
        StructField(":@computed_region_7mpf_4k6g", StringType(), True),
        StructField("resolution_description", StringType(), True),
    ]
)

# %%
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("subscribe", source_topic)
    .load()
)

# %%
df = df.selectExpr("CAST(value AS STRING)").select(
    from_json(col("value"), schema).alias("data")
)

# %%
# Calculating the age of a complaint by subtracting the created date from the closed date
df = df.withColumn("complaint_age_days", datediff(col("data.closed_date"), col("data.created_date")))

# %%
# Adding is_active based on status
df = df.withColumn("is_active", col("data.status") == "true")

# %%
query = (
    df.selectExpr("to_json(struct(*)) AS value")
    .writeStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("topic", destination_topic)
    .option("checkpointLocation", "checkpoint_dir")
    .outputMode("update")
    .start()
)

# %%
query.awaitTermination()


