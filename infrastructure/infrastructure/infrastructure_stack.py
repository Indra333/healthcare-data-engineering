
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct
from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam


class InfrastructureStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Secure S3 bucket for healthcare source files
        landing_bucket = s3.Bucket(
            self,
            "HealthcareLandingBucket",

            # Prevent public access
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,

            # Enable server-side encryption
            encryption=s3.BucketEncryption.S3_MANAGED,

            # Require HTTPS connections
            enforce_ssl=True,

            # Retain previous versions of files
            versioned=True,

            # Protect bucket from stack deletion
            removal_policy=RemovalPolicy.RETAIN,

            # Disable object ACLs
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
        )

        # Display the generated bucket name after deployment
        CfnOutput(
            self,
            "LandingBucketName",
            value=landing_bucket.bucket_name,
        )

        CfnOutput(
            self,
            "LandingBucketArn",
            value=landing_bucket.bucket_arn,
        )

        # AWS Glue Data Catalog database
        glue_database = glue.CfnDatabase(
            self,
            "HealthcareGlueDatabase",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name="healthcare_raw_catalog",
                description=(
                    "Metadata catalog for healthcare source datasets "
                    "stored in Amazon S3"
                ),
            ),
        )

        
        # Classifier for pipe-delimited healthcare TXT files
        pipe_classifier = glue.CfnClassifier(
            self,
            "HealthcarePipeClassifier",
            csv_classifier=glue.CfnClassifier.CsvClassifierProperty(
                name="healthcare_pipe_classifier",
                delimiter="|",
                quote_symbol='"',
                contains_header="PRESENT",
                allow_single_column=False,
            ),
        )

        # Classifier for comma-delimited pharmacy TXT files
        comma_classifier = glue.CfnClassifier(
            self,
            "HealthcareCommaClassifier",
            csv_classifier=glue.CfnClassifier.CsvClassifierProperty(
                name="healthcare_comma_classifier",
                delimiter=",",
                quote_symbol='"',
                contains_header="PRESENT",
                allow_single_column=False,
            ),
        )

        
        # IAM role assumed by AWS Glue crawlers
        glue_crawler_role = iam.Role(
            self,
            "HealthcareGlueCrawlerRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            description=(
                "IAM role for healthcare Glue crawlers "
                "to discover source data in S3"
            ),
        )

        # AWS-managed permissions for Glue crawler operations
        glue_crawler_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSGlueServiceRole"
            )
        )

        # Read-only access to our healthcare S3 landing bucket
        landing_bucket.grant_read(glue_crawler_role)

        
        # AWS Glue crawlers for healthcare datasets
        crawler_configs = [
            ("EnrollmentCrawler", "enrollment", "healthcare_pipe_classifier"),
            ("MedicalClaimsCrawler", "medical_claims", "healthcare_pipe_classifier"),
            ("PharmacyClaimsCrawler", "pharmacy_claims", "healthcare_comma_classifier"),
            ("ProvidersCrawler", "providers", "healthcare_pipe_classifier"),
        ]

        for crawler_id, prefix, classifier_name in crawler_configs:
            crawler = glue.CfnCrawler(
                self,
                crawler_id,
                name=f"healthcare_{prefix}_crawler",
                role=glue_crawler_role.role_arn,
                database_name="healthcare_raw_catalog",
                classifiers=[classifier_name],
                targets=glue.CfnCrawler.TargetsProperty(
                    s3_targets=[
                        glue.CfnCrawler.S3TargetProperty(
                            path=f"s3://{landing_bucket.bucket_name}/{prefix}/",
                        )
                    ]
                ),
                table_prefix=f"{prefix}_",
                recrawl_policy=glue.CfnCrawler.RecrawlPolicyProperty(
                    recrawl_behavior="CRAWL_EVERYTHING"
                ),
            )

            crawler.node.add_dependency(glue_database)

            if classifier_name == "healthcare_pipe_classifier":
                crawler.node.add_dependency(pipe_classifier)
            else:
                crawler.node.add_dependency(comma_classifier)

            
            
        # S3 bucket for processed Parquet datasets
        processed_bucket = s3.Bucket(
            self,
            "HealthcareProcessedBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
        )

        CfnOutput(
            self,
            "ProcessedBucketName",
            value=processed_bucket.bucket_name,
        )

        CfnOutput(
            self,
            "ProcessedBucketArn",
            value=processed_bucket.bucket_arn,
        )

        
        # IAM role for AWS Glue ETL jobs
        glue_etl_role = iam.Role(
            self,
            "HealthcareGlueETLRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            description="IAM role for healthcare Glue ETL jobs",
        )

        # AWS-managed permissions for Glue job execution and logging
        glue_etl_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSGlueServiceRole"
            )
        )

        # Read raw healthcare source files
        landing_bucket.grant_read(glue_etl_role)

        # Read the ETL script and write processed Parquet files
        processed_bucket.grant_read_write(glue_etl_role)

        CfnOutput(
            self,
            "GlueETLRoleArn",
            value=glue_etl_role.role_arn,
        )

        
        # AWS Glue ETL job for Enrollment dataset
        enrollment_glue_job = glue.CfnJob(
            self,
            "HealthcareEnrollmentETLJob",
            name="healthcare_enrollment_etl",
            role=glue_etl_role.role_arn,
            glue_version="5.0",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=(
                    f"s3://{processed_bucket.bucket_name}/"
                    "glue-scripts/enrollment_etl.py"
                ),
                python_version="3",
            ),
            worker_type="G.1X",
            number_of_workers=2,
            timeout=30,
            max_retries=0,
            default_arguments={
                "--job-language": "python",
                "--enable-continuous-cloudwatch-log": "true",
                "--OUTPUT_PATH": (
                    f"s3://{processed_bucket.bucket_name}/"
                    "enrollment/"
                ),
            },
        )

        CfnOutput(
            self,
            "EnrollmentGlueJobName",
            value=enrollment_glue_job.name,
        )

        
        # AWS Glue ETL job for Medical Claims
        medical_claims_glue_job = glue.CfnJob(
            self,
            "HealthcareMedicalClaimsETLJob",
            name="healthcare_medical_claims_etl",
            role=glue_etl_role.role_arn,
            glue_version="5.0",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=(
                    f"s3://{processed_bucket.bucket_name}/"
                    "glue-scripts/medical_claims_etl.py"
                ),
                python_version="3",
            ),
            worker_type="G.1X",
            number_of_workers=2,
            timeout=30,
            max_retries=0,
            default_arguments={
                "--job-language": "python",
                "--enable-continuous-cloudwatch-log": "true",
                "--OUTPUT_PATH": (
                    f"s3://{processed_bucket.bucket_name}/"
                    "medical_claims/"
                ),
            },
        )

        CfnOutput(
            self,
            "MedicalClaimsGlueJobName",
            value=medical_claims_glue_job.name,
        )

        
        # AWS Glue ETL job for Pharmacy Claims
        pharmacy_claims_glue_job = glue.CfnJob(
            self,
            "HealthcarePharmacyClaimsETLJob",
            name="healthcare_pharmacy_claims_etl",
            role=glue_etl_role.role_arn,
            glue_version="5.0",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=(
                    f"s3://{processed_bucket.bucket_name}/"
                    "glue-scripts/pharmacy_claims_etl.py"
                ),
                python_version="3",
            ),
            worker_type="G.1X",
            number_of_workers=2,
            timeout=30,
            max_retries=0,
            default_arguments={
                "--job-language": "python",
                "--enable-continuous-cloudwatch-log": "true",
                "--OUTPUT_PATH": (
                    f"s3://{processed_bucket.bucket_name}/"
                    "pharmacy_claims/"
                ),
            },
        )

        CfnOutput(
            self,
            "PharmacyClaimsGlueJobName",
            value=pharmacy_claims_glue_job.name,
        )

        
        # AWS Glue ETL job for Providers
        providers_glue_job = glue.CfnJob(
            self,
            "HealthcareProvidersETLJob",
            name="healthcare_providers_etl",
            role=glue_etl_role.role_arn,
            glue_version="5.0",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=(
                    f"s3://{processed_bucket.bucket_name}/"
                    "glue-scripts/providers_etl.py"
                ),
                python_version="3",
            ),
            worker_type="G.1X",
            number_of_workers=2,
            timeout=30,
            max_retries=0,
            default_arguments={
                "--job-language": "python",
                "--enable-continuous-cloudwatch-log": "true",
                "--OUTPUT_PATH": (
                    f"s3://{processed_bucket.bucket_name}/"
                    "providers/"
                ),
            },
        )

        CfnOutput(
            self,
            "ProvidersGlueJobName",
            value=providers_glue_job.name,
        )

        
        # Snowflake IAM role for reading processed healthcare data
        snowflake_role = iam.Role(
            self,
            "HealthcareSnowflakeS3Role",
            role_name="healthcare-snowflake-s3-role",
            assumed_by=iam.ArnPrincipal(
                "arn:aws:iam::128117030834:user/j36d2000-s"
            ).with_conditions({
                "StringEquals": {
                    "sts:ExternalId": (
                        "UN34505_SFCRole=4_p3wuEDiaSytHml2Fusai7jdocNU="
                    )
                }
            }),
            description="Read-only S3 access for Snowflake",
        )

        # Permit listing the processed dataset folders
        snowflake_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[processed_bucket.bucket_arn],
                conditions={
                    "StringLike": {
                        "s3:prefix": [
                            "enrollment/*",
                            "medical_claims/*",
                            "pharmacy_claims/*",
                            "providers/*",
                        ]
                    }
                },
            )
        )

        # Permit reading Parquet files in the four dataset folders
        snowflake_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[
                    processed_bucket.arn_for_objects("enrollment/*"),
                    processed_bucket.arn_for_objects("medical_claims/*"),
                    processed_bucket.arn_for_objects("pharmacy_claims/*"),
                    processed_bucket.arn_for_objects("providers/*"),
                ],
            )
        )

        CfnOutput(
            self,
            "SnowflakeS3RoleArn",
            value=snowflake_role.role_arn,
        )










