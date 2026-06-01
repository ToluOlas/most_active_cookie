"""Command-line tool to find the most active cookie(s) in a log file for a given UTC date."""

from datetime import datetime, timezone, date
from collections import Counter
import csv
import argparse
import logging
import sys

logger = logging.getLogger("most_active_cookie")

def parse_date(date_str: str) -> date:
    """Parse a YYYY-MM-DD string into a date.
    """
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        logger.error(f"{date_str} is not a valid date. Expected format: YYYY-MM-DD")
        sys.exit(1)

def load_rows(file_name: str) -> list[dict[str, str]]:
    """CSV file to dict conversion.

    Primarily for catching potential errors related to finding and
    accessing the log file.
    """
    try:
        with open(file_name, newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        logger.error(f"'{file_name}' not found.")
        sys.exit(1)
    except IsADirectoryError:
        logger.error(f"'{file_name}' is a directory, not a file.")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Insufficient permissions for '{file_name}'.")
        sys.exit(1)
    except UnicodeDecodeError:
        logger.error("Expected UTF-8 encoding.")
        sys.exit(1)
    except OSError as e:
        logger.error(f"{e}")
        sys.exit(1)

def find_most_active_cookies(rows: list[dict[str, str]], target_date: date) -> list[str]:
    """Find the most active cookie(s) on a given UTC date.

    Timezone differences are normalised before dates are compared.
    Rows with a missing or invalid timestamp are skipped with a warning.
    Every cookie tied for the highest count is returned, or an empty list
    if no rows match the target date.
    """
    counts: Counter[str] = Counter()

    for index, row in enumerate(rows, start=1):
        try:
            utc_datetime = datetime.fromisoformat(row["timestamp"]).astimezone(timezone.utc)
            row_date = utc_datetime.date()
        except (ValueError, KeyError):
            logger.warning(f"Skipping invalid row {index}: {row}")
            continue

        if row_date == target_date:
            counts[row["cookie"]] += 1

    if not counts:
        return []

    max_count = max(counts.values())
    return [cookie for cookie, count in counts.items() if count == max_count]

def main() -> None:
    """Parse CLI arguments and run the entire workflow."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", stream=sys.stderr)

    parser = argparse.ArgumentParser(description="Find the most active cookie for a specific date.")
    parser.add_argument("-f", required=True, help="Path to CSV file.")
    parser.add_argument("-d", required=True, help="Date to query, YYYY-MM-DD format.")
    args = parser.parse_args()

    target = parse_date(args.d)
    rows = load_rows(args.f)
    results = find_most_active_cookies(rows, target)

    for cookie in results:
        print(cookie)

if __name__ == "__main__":
    main()
