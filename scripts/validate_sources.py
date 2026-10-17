from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DATASETS = {
    "acme_data_enrollment.txt": ("|", 11),
    "acme_data_medical_claims.txt": ("|", 15),
    "acme_data_pharmacy_claims.txt": (",", 10),
    "acme_data_providers.txt": ("|", 4),
}

for filename, (delimiter, expected_columns) in DATASETS.items():
    path = DATA_DIR / filename

    print(f"\nDataset: {filename}")

    if not path.is_file():
        print("ERROR: File not found")
        continue

    valid_rows = 0
    invalid_rows = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, delimiter=delimiter)

        header = next(reader, None)

        if header is None:
            print("ERROR: Empty file")
            continue

        print(f"Header columns: {len(header)}")

        if len(header) != expected_columns:
            print("ERROR: Unexpected header column count")

        for line_number, row in enumerate(reader, start=2):
            if len(row) == expected_columns:
                valid_rows += 1
            else:
                invalid_rows.append(line_number)

    print(f"Valid data rows: {valid_rows}")
    print(f"Invalid data rows: {len(invalid_rows)}")

    if invalid_rows:
        print(f"Invalid line numbers: {invalid_rows[:20]}")
