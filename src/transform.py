import pandas as pd


def _convert_common_numeric_columns(df):
    numeric_columns = [
        "student_id", "id", "age", "gpa",
        "price", "rating", "stock", "discountPercentage"
    ]

    for column in numeric_columns:
        if column in df.columns:
            converted = pd.to_numeric(df[column], errors="coerce")
            if converted.notna().any():
                df[column] = converted

    return df


def _fill_numeric_missing(df):
    for column in df.select_dtypes(include=["number"]).columns:
        median = df[column].median()
        if pd.isna(median):
            median = 0
        df[column] = df[column].fillna(median)
    return df


def _fill_text_missing(df):
    for column in df.select_dtypes(include=["object"]).columns:

        # Ignore columns containing complex values
        has_complex_values = df[column].apply(
            lambda value: isinstance(value, (list, dict))
        ).any()

        if has_complex_values:
            continue

        # Remove spaces from normal text
        df[column] = df[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

        df[column] = df[column].replace("", pd.NA)

        valid_values = df[column].dropna()

        if valid_values.empty:
            fill_value = "Unknown"
        else:
            mode = valid_values.mode()

            if mode.empty:
                fill_value = "Unknown"
            else:
                fill_value = mode.iloc[0]

        df[column] = df[column].fillna(fill_value)

    return df


def clean_data(df):
    if df is None:
        return None

    df = df.copy()
def clean_data(df):
    if df is None:
        return None

    df = df.copy()

    # Remove duplicates
    if "id" in df.columns:
        df = df.drop_duplicates(subset="id")

    elif "student_id" in df.columns:
        df = df.drop_duplicates(subset="student_id")

    # Convert known numeric columns.
    df = _convert_common_numeric_columns(df)

    # Convert known numeric columns.
    df = _convert_common_numeric_columns(df)

    # Infinity is treated as missing.
    df = df.replace([float("inf"), float("-inf")], pd.NA)

    # Repair numeric missing/invalid values with median.
    df = _fill_numeric_missing(df)

    # Repair text missing values with mode.
    df = _fill_text_missing(df)

    # Student data rules.
    if "gpa" in df.columns:
        valid_gpa = df["gpa"].between(0, 4)
        median_gpa = df.loc[valid_gpa, "gpa"].median()

        if pd.isna(median_gpa):
            median_gpa = 0

        df.loc[~valid_gpa, "gpa"] = median_gpa

        def get_status(gpa):
            if gpa >= 3.5:
                return "Excellent"
            elif gpa >= 2.5:
                return "Good"
            else:
                return "Pass"

        df["status"] = df["gpa"].apply(get_status)

    if "age" in df.columns:
        valid_age = df["age"].between(16, 80)
        median_age = df.loc[valid_age, "age"].median()

        if pd.isna(median_age):
            median_age = 18

        df.loc[~valid_age, "age"] = median_age

    # Product data rules.
    if "price" in df.columns:
        valid_price = df["price"] >= 0
        median_price = df.loc[valid_price, "price"].median()

        if pd.isna(median_price):
            median_price = 0

        df.loc[~valid_price, "price"] = median_price

    if "rating" in df.columns:
        valid_rating = df["rating"].between(0, 5)
        median_rating = df.loc[valid_rating, "rating"].median()

        if pd.isna(median_rating):
            median_rating = 0

        df.loc[~valid_rating, "rating"] = median_rating

    # Delete only rows that still contain unusable values after repair.
    df = df.dropna(how="any")

    return df
