import os

from sqlalchemy import create_engine


password = os.getenv("METEORISK_DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}"
    "@meteorisK-db:5432/meteorisK"
)

engine = create_engine(DATABASE_URL)