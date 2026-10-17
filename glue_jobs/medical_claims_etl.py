
import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ["JOB_NAME", "OUTPUT_PATH"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)

# Read Medical Claims from Glue Data Catalog
medical_claims_df = glue_context.create_dynamic_frame.from_catalog(
    database="healthcare_raw_catalog",
    table_name="medical_claims_medical_claims",
).toDF()

# Preserve identifiers as strings
for column_name in ["member_id", "claim_id"]:
    if column_name in medical_claims_df.columns:
        medical_claims_df = medical_claims_df.withColumn(
            column_name,
            col(column_name).cast("string"),
        )

# Write the processed dataset as Parquet
medical_claims_df.write.mode("overwrite").parquet(args["OUTPUT_PATH"])

print("Medical Claims ETL completed successfully.")
