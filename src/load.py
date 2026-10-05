from pymongo import MongoClient
from src.config import MONGO_URI, MONGO_DATABASE
from datetime import date, datetime


def save_to_mongodb(df, collection_name):
    if df is None or df.empty:
        print(f"{collection_name}: no data to save")
        return

    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DATABASE][collection_name]

    collection.delete_many({})

    records = df.to_dict("records")

    # Convert unsupported date values to datetime
    for record in records:
        for key, value in record.items():
            if isinstance(value, date) and not isinstance(value, datetime):
                record[key] = datetime.combine(value, datetime.min.time())

    collection.insert_many(records)

    client.close()

    print(f"{collection_name}: saved {len(records)} records to MongoDB")