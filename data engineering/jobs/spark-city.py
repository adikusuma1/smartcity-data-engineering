from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import from_json, col
from config import configuration

def main():
    spark = SparkSession.builder.appName("SmartCityStreaming") \
    .config("spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
        "org.apache.kafka:kafka-clients:3.4.1,"
        "org.apache.hadoop:hadoop-aws:3.3.1,"
        "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY')) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY')) \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .getOrCreate()

    spark.sparkContext.setLogLevel('WARN')

    vehicleSchema = StructType([
        StructField("id", StringType(),True),
        StructField("deviceId", StringType(),True),
        StructField("timestamp", TimestampType(),True),
        StructField("location", ArrayType(DoubleType()),True),
        StructField("speed", DoubleType(),True),
        StructField("direction", StringType(),True),
        StructField("make", StringType(),True),
        StructField("model", StringType(),True),
        StructField("year", StringType(),True),
        StructField("fuelType", StringType(),True)
    ])

    gpsSchema = StructType([
        StructField("id", StringType(),True),
        StructField("deviceId", StringType(),True),
        StructField("timestamp", TimestampType(),True),
        StructField("speed", DoubleType(),True),
        StructField("direction", StringType(),True),
        StructField("vehicleType", StringType(),True)
    ])

    trafficSchema = StructType([
        StructField("id", StringType(),True),
        StructField("deviceId", StringType(),True),
        StructField("cameraId", StringType(),True),
        StructField("location", ArrayType(DoubleType()),True),
        StructField("timestamp", TimestampType(),True),
        StructField("snapshot", StringType(),True)
    ])

    weatherSchema = StructType([
        StructField("id", StringType(),True),
        StructField("deviceId", StringType(),True),
        StructField("location", ArrayType(DoubleType()),True),
        StructField("timestamp", TimestampType(),True),
        StructField("temperature", DoubleType(),True),
        StructField("weatherCondition", StringType(),True),
        StructField("precipitation", DoubleType(),True),
        StructField("windSpeed", DoubleType(),True),
        StructField("humidity", IntegerType(),True),
        StructField("airQuality", DoubleType(),True)
    ])

    emergencySchema = StructType([
        StructField("deviceId", StringType(),True),
        StructField("incidentId", StringType(),True),
        StructField("type", StringType(),True),
        StructField("timestamp", TimestampType(),True),
        StructField("location", ArrayType(DoubleType()),True),
        StructField("status", StringType(),True),
        StructField("description", StringType(),True)
    ])

    def read_kafka_topic(topic, schema):
        return (spark.readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'broker:29092')
            .option('subscribe', topic)
            .option('startingOffsets', 'earliest')
            .load()
            .selectExpr('CAST(value AS STRING)')
            .select(from_json(col('value'), schema).alias('data'))
            .select('data.*')
            .withWatermark('timestamp', '2 minutes'))

    def streamWriter(input: DataFrame, checkpointFolder, output):
        try:
            spark.sparkContext._jvm.org.apache.hadoop.fs.FileSystem.closeAll()
            
            return (input.writeStream
                .format('parquet')
                .option('checkpointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start())
        except Exception as e:
            print(f"Failed to start stream writer for {output}: {e}")
            raise

    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema).alias('vehicle')
    gpsDF = read_kafka_topic('gps_data', gpsSchema).alias('gps')
    trafficDF = read_kafka_topic('traffic_data', trafficSchema).alias('traffic')
    weatherDF = read_kafka_topic('weather_data', weatherSchema).alias('weather')
    emergencyDF = read_kafka_topic('emergency_data', emergencySchema).alias('emergency')

    query1 = streamWriter(vehicleDF, 's3a://data-smart-city/checkpoints/vehicle_data', 's3a://data-smart-city/data/vehicle_data')
    query2 = streamWriter(gpsDF, 's3a://data-smart-city/checkpoints/gps_data', 's3a://data-smart-city/data/gps_data')
    query3 = streamWriter(trafficDF, 's3a://data-smart-city/checkpoints/traffic_data', 's3a://data-smart-city/data/traffic_data')
    query4 = streamWriter(weatherDF, 's3a://data-smart-city/checkpoints/weather_data', 's3a://data-smart-city/data/weather_data')
    query5 = streamWriter(emergencyDF, 's3a://data-smart-city/checkpoints/emergency_data', 's3a://data-smart-city/data/emergency_data')

    query5.awaitTermination()

if __name__ == "__main__":
    main()