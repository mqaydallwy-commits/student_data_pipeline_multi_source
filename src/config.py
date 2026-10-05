API_URL = "https://jsonplaceholder.typicode.com/users"

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DATABASE = "university_ai"
MONGO_SOURCE_COLLECTION = "students"

CSV_PATH = "data/raw/tudents.csv"

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "university_training",
    "user": "postgres",
    "password": ""
}
POSTGRES_TABLE = "students"

OUTPUT_COLLECTIONS = {
    "api": "api_products_clean",
    "mongodb": "mongodb_students_clean",
    "csv": "csv_students_clean",
    "postgresql": "postgresql_students_clean"
}
