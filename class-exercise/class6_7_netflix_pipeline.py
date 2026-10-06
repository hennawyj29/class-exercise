import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # Load the CSV file
    path = Path(args.input)

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error(f"Input file not found: {path}")
        sys.exit(1)

    logger.info(
        f"Loaded {df.shape[0]} rows and {df.shape[1]} columns"
    )

    # Save original data
    df_original = df.copy()

    # Display overview
    show_overview(df)
    logger.info("Displayed DataFrame overview")

    # Remove duplicates
    before = len(df)
    df = remove_duplicates(df)
    logger.info(
        f"Removed {before - len(df)} duplicate row(s)"
    )

    # Remove rows with missing values
    before = len(df)
    df = drop_missing_rows(df)
    logger.info(
        f"Dropped {before - len(df)} rows with missing values"
    )

    # Remove runtime_minutes outliers
    before = len(df)

    try:
        df = remove_iqr_outliers(
            df,
            "runtime_minutes",
            1.5
        )
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    logger.info(
        f"Removed {before - len(df)} runtime_minutes outlier(s)"
    )

    # Clean text columns
    for column in ["title", "type", "country"]:
        df[column] = df[column].apply(clean_text)
        logger.info(f"Cleaned text column: {column}")

    # Cleaning report
    report = {
        "rows_before": len(df_original),
        "rows_after": len(df),
        "rows_removed": len(df_original) - len(df),
        "columns": len(df.columns)
    }

    logger.info(f"Cleaning complete: {report}")


if __name__ == "__main__":
    main()