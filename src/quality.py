def check_quality(df, source_name):
    if df is None:
        raise ValueError(f"{source_name}: no data received")

    if df.empty:
        raise ValueError(f"{source_name}: dataset is empty")

    if df.isnull().sum().sum() > 0:
        raise ValueError(f"{source_name}: missing values still exist")

    if "gpa" in df.columns:
        if ((df["gpa"] < 0) | (df["gpa"] > 4)).any():
            raise ValueError(f"{source_name}: GPA must be between 0 and 4")

    if "age" in df.columns:
        if ((df["age"] < 16) | (df["age"] > 80)).any():
            raise ValueError(f"{source_name}: age must be between 16 and 80")

    if "price" in df.columns:
        if (df["price"] < 0).any():
            raise ValueError(f"{source_name}: price cannot be negative")

    if "rating" in df.columns:
        if ((df["rating"] < 0) | (df["rating"] > 5)).any():
            raise ValueError(f"{source_name}: rating must be between 0 and 5")

    print(f"{source_name}: data quality checks passed")
    return True
