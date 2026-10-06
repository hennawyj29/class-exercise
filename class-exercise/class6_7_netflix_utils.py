import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug(f"DataFrame shape: {df.shape}")

    print(f"Shape: {df.shape}")
    print("First five rows:")
    print(df.head())
    print(f"Columns: {list(df.columns)}")
    print("Data types:")
    print(df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)

    df = df.drop_duplicates()

    after = len(df)
    logger.debug(
        f"Removed duplicates: before={before}, after={after}"
    )

    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)

    df = df.dropna()

    after = len(df)
    logger.debug(
        f"Dropped missing rows: before={before}, after={after}"
    )

    return df


def clean_text(value):
    """Normalize one text value."""
    value = value.strip()
    value = value.lower()
    value = re.sub(r"\s+", " ", value)

    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    if column not in df.columns:
        logger.error(f"Column not found: {column}")
        raise ValueError(f"Column not found: {column}")

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr

    before = len(df)

    df = df[
        (df[column] >= lower) &
        (df[column] <= upper)
    ]

    logger.debug(
        f"IQR bounds for {column}: {lower} to {upper}; "
        f"removed {before - len(df)} row(s)"
    )

    return df