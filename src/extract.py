import pandas as pd
import requests
from pymongo import MongoClient
import psycopg2

from src.config import (
    API_URL,
    MONGO_URI,
    MONGO_DATABASE,
    MONGO_SOURCE_COLLECTION,
    CSV_PATH,
    POSTGRES_CONFIG,
    POSTGRES_TABLE,
)


def read_api():
    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()

        data = response.json()

        df = pd.json_normalize(data)

        return df

    except Exception as e:
        print(f"API read error: {e}")
        return None

def read_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DATABASE][MONGO_SOURCE_COLLECTION]
        data = list(collection.find())
        client.close()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        if "_id" in df.columns:
            df["_id"] = df["_id"].astype(str)

        return df
    except Exception as e:
        print(f"MongoDB read error: {e}")
        return None


def read_csv():
    try:
        return pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"CSV read error: {e}")
        return None


def read_postgresql():
    conn = None
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        query = f"SELECT * FROM {POSTGRES_TABLE}"
        return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"PostgreSQL read error: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()
