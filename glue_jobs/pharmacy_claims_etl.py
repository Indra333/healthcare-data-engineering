
import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ["JOB_NAME", "OUTPUT_PATH"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)

# Read Pharmacy Claims from the Glue Data Catalog
pharmacy_df = glue_context.create_dynamic_frame.from_catalog(
    database="healthcare_raw_catalog",
    table_name="pharmacy_claims_pharmacy_claims",
).toDF()

# Preserve identifiers as strings when present
for column_name in ["member_id", "claim_id", "ndc"]:
    if column_name in pharmacy_df.columns:
        pharmacy_df = pharmacy_df.withColumn(
            column_name,
            col(column_name).cast("string"),
        )

# Write Pharmacy Claims as Parquet
pharmacy_df.write.mode("overwrite").parquet(args["OUTPUT_PATH"])

print("Pharmacy Claims ETL completed successfully.")
