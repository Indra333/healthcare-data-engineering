
import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ["JOB_NAME", "OUTPUT_PATH"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)

# Read Providers data from the Glue Data Catalog
providers_df = glue_context.create_dynamic_frame.from_catalog(
    database="healthcare_raw_catalog",
    table_name="providers_providers",
).toDF()

# Preserve provider identifiers as strings
for column_name in ["provider_id", "npi"]:
    if column_name in providers_df.columns:
        providers_df = providers_df.withColumn(
            column_name,
            col(column_name).cast("string"),
        )

# Write Providers data in Parquet format
providers_df.write.mode("overwrite").parquet(args["OUTPUT_PATH"])

print("Providers ETL completed successfully.")

