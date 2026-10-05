from src import extract
from src import transform
from src import quality
from src import load
from src.config import OUTPUT_COLLECTIONS


def run_source(source_name, read_function):
    print(f"\n--- {source_name.upper()} ---")

    df = read_function()

    if df is None:
        print(f"{source_name}: extract failed")
        return

    if df.empty:
        print(f"{source_name}: no records found")
        return

    print(f"{source_name}: extracted {len(df)} records")

    df = transform.clean_data(df)

    if df is None or df.empty:
        print(f"{source_name}: no usable data after cleaning")
        return

    quality.check_quality(df, source_name)

    load.save_to_mongodb(
        df,
        OUTPUT_COLLECTIONS[source_name]
    )


def main():
    run_source("api", extract.read_api)
    run_source("mongodb", extract.read_mongodb)
    run_source("csv", extract.read_csv)
    run_source("postgresql", extract.read_postgresql)

    print("\nPipeline finished.")


if __name__ == "__main__":
    main()
