
from pathlib import Path
import boto3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

AWS_PROFILE = "healthcare-dev"
AWS_REGION = "us-east-1"

BUCKET_NAME = (
    "infrastructurestack-healthcarelandingbucket771542d-"
    "iqzkkzpdzdij"
)

DATASETS = {
    "acme_data_enrollment.txt": "enrollment",
    "acme_data_medical_claims.txt": "medical_claims",
    "acme_data_pharmacy_claims.txt": "pharmacy_claims",
    "acme_data_providers.txt": "providers",
}


def main():
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    s3 = session.client("s3")

    # Check all files before uploading anything.
    for filename in DATASETS:
        filepath = CLEANED_DIR / filename
        if not filepath.is_file():
            raise FileNotFoundError(
                f"Cleaned file not found: {filepath}"
            )

    for filename, prefix in DATASETS.items():
        filepath = CLEANED_DIR / filename
        s3_key = f"{prefix}/{filename}"

        print(f"Uploading {filename}...")

        s3.upload_file(
            Filename=str(filepath),
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs={
                "ServerSideEncryption": "AES256",
                "ContentType": "text/plain",
            },
        )

        print(f"Uploaded: s3://{BUCKET_NAME}/{s3_key}")

    print("\nAll four datasets uploaded successfully.")


if __name__ == "__main__":
    main()
