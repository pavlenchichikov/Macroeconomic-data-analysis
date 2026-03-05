import argparse
import csv
import logging
import sys

from tabulate import tabulate

from reports import REPORTS_REGISTRY

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Macroeconomic data analyzer script")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to the input CSV files.",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=list(REPORTS_REGISTRY.keys()),
        help="The name of the report to generate.",
    )
    return parser.parse_args()


def read_csv_files(file_paths: list[str]) -> list[dict[str, str]]:
    all_data: list[dict[str, str]] = []
    for file_path in file_paths:
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_data.append(row)
        except FileNotFoundError:
            logger.error("Error: File not found - %s", file_path)
            sys.exit(1)
        except Exception as e:
            logger.error("Error reading file %s: %s", file_path, e)
            sys.exit(1)
    return all_data


def main() -> None:
    args = parse_arguments()
    data = read_csv_files(args.files)

    if not data:
        logger.warning("No data found in the provided files.")
        sys.exit(0)

    report_strategy = REPORTS_REGISTRY[args.report]
    report_data = report_strategy.generate(data)
    headers = report_strategy.get_headers()

    print(tabulate(report_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
