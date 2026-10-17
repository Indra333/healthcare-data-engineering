
from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "cleaned"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "acme_data_enrollment.txt": ("|", 11),
    "acme_data_medical_claims.txt": ("|", 15),
    "acme_data_pharmacy_claims.txt": (",", 10),
    "acme_data_providers.txt": ("|", 4),
}

for filename, (delimiter, expected_columns) in DATASETS.items():
    source = DATA_DIR / filename
    destination = OUTPUT_DIR / filename

    valid_rows = 0
    skipped_rows = 0

    with (
        source.open("r", encoding="utf-8-sig", newline="") as infile,
        destination.open("w", encoding="utf-8", newline="") as outfile,
    ):
        reader = csv.reader(infile, delimiter=delimiter)
        writer = csv.writer(
            outfile,
            delimiter=delimiter,
            lineterminator="\n",
        )

        header = next(reader)

        if len(header) != expected_columns:
            raise ValueError(f"Invalid header in {filename}")

        writer.writerow(header)

        for line_number, row in enumerate(reader, start=2):
            if len(row) == expected_columns:
                writer.writerow(row)
                valid_rows += 1

            elif (
                not row
                or len(row) == 1
                and (
                    not row[0].strip()
                    or (
                        row[0].startswith("(")
                        and row[0].endswith(" rows affected)")
                    )
                    or row[0].startswith("Completion time:")
                )
            ):
                skipped_rows += 1

            else:
                raise ValueError(
                    f"Unexpected malformed row in "
                    f"{filename}, line {line_number}: {row}"
                )

    print(f"\n{filename}")
    print(f"Valid records: {valid_rows}")
    print(f"Skipped export artifacts: {skipped_rows}")
    print(f"Cleaned file: {destination}")

print("\nCleaning completed successfully.")
