# Healthcare Data Engineering Pipeline



## Project Overview



An end-to-end healthcare data engineering project that processes enrollment, medical claims, pharmacy claims, and provider datasets using AWS, Snowflake, dbt, and Power BI.



The project demonstrates cloud-based ETL processing, data warehousing, dimensional modeling, data quality validation, and business intelligence reporting.



## Technology Stack



- **Cloud Platform:** Amazon Web Services (AWS)

- **Data Storage:** Amazon S3

- **ETL Processing:** AWS Glue, PySpark

- **Workflow Orchestration:** AWS Glue Workflows

- **Data Warehouse:** Snowflake

- **Data Transformation:** dbt Core, SQL

- **Data Visualization:** Microsoft Power BI

- **Version Control:** Git and GitHub



## Data Pipeline Architecture



```text

Healthcare Source Files (CSV)

            |

            v

     Amazon S3 Landing

            |

            v

     AWS Glue Workflow

            |

    AWS Glue PySpark ETL

            |

            v

     Amazon S3 Processed

       (Parquet Files)

            |

            v

       Snowflake RAW

            |

            v

     dbt Transformations

       |           |

    Staging       Marts

                   |

             Dimensions

             Fact Tables

             Financial Summary

                   |

                   v

             Power BI Dashboard

```



## Data Sources



The pipeline processes four healthcare datasets:



1. **Enrollment:** Member demographics, health plan enrollment, and eligibility.

2. **Medical Claims:** Medical claim transactions, providers, and financial measures.

3. **Pharmacy Claims:** Prescription claim transactions and associated costs.

4. **Providers:** Healthcare provider information.



## ETL Processing



AWS Glue PySpark jobs read CSV data from Amazon S3, process the datasets, and write Parquet files to the processed S3 bucket.



An AWS Glue workflow coordinates the four ETL jobs.



## Snowflake Data Warehouse



Snowflake stores the processed healthcare datasets in the `HEALTHCARE_DB` database.



The `RAW` schema contains the source datasets:



- `ENROLLMENT`

- `MEDICAL_CLAIMS`

- `PHARMACY_CLAIMS`

- `PROVIDERS`



Processed Parquet files are loaded through a Snowflake external stage.



## dbt Transformations



dbt transforms raw data into analytics-ready models.



### Staging Models



- `STG_ENROLLMENT`

- `STG_MEDICAL_CLAIMS`

- `STG_PHARMACY_CLAIMS`

- `STG_PROVIDERS`



### Dimensional Models



- `DIM_MEMBER`

- `DIM_PROVIDER`

- `FCT_MEDICAL_CLAIMS`

- `FCT_PHARMACY_CLAIMS`



### Reporting Model



- `RPT_CLAIMS_FINANCIAL_SUMMARY`



Transformations include data standardization, duplicate handling, dimensional modeling, and financial aggregation.



## Data Quality



The project implements data quality checks using SQL and dbt, including:



- Null and uniqueness checks

- Referential integrity tests

- Duplicate detection

- Date validation

- Financial reconciliation



## Power BI Dashboard



The Power BI report provides healthcare claims analytics, including:



- Total allowed amount

- Total medical and pharmacy claim records

- Total copayment

- Total coinsurance

- Medical versus pharmacy financial comparison

- Claim category filtering



## Pipeline Execution



1. Upload healthcare source CSV files to the S3 landing bucket.

2. Execute the AWS Glue workflow.

3. Verify successful ETL processing and Parquet output.

4. Load processed data into Snowflake RAW tables.

5. Execute dbt transformations and tests.

6. Refresh the Power BI report to view updated analytics.



Current orchestration scope: AWS Glue ETL jobs are orchestrated through AWS Glue Workflows. Snowflake RAW ingestion, dbt execution, and Power BI refresh are performed separately. Full end-to-end Airflow orchestration is a planned enhancement.



## Future Enhancements



- Apache Airflow orchestration

- Automated Snowflake ingestion

- Scheduled dbt execution

- Pipeline monitoring and alerts

- Automated Power BI refresh



## Project Purpose



This project demonstrates practical data engineering skills in cloud ETL development, Snowflake data warehousing, SQL transformation, data quality validation, dimensional modeling, and healthcare analytics.




