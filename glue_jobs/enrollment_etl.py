
import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

# Get Glue job parameters
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "OUTPUT_PATH"]
)

# Initialize Spark and Glue
sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)

# Read enrollment data from Glue Catalog
enrollment_df = glue_context.create_dynamic_frame.from_catalog(
    database="healthcare_raw_catalog",
    table_name="enrollment_enrollment"
).toDF()

# Preserve member identifiers as strings
enrollment_df = enrollment_df.withColumn(
    "member_id",
    col("member_id").cast("string")
)

# Write data as Parquet
enrollment_df.write.mode("overwrite").parquet(
    args["OUTPUT_PATH"]
)

print("Enrollment ETL completed successfully.")
