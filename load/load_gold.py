import pandas as pd

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Date,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import declarative_base


import os

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:Darkavatar.31"
    "@localhost:5432/meteorisK"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class WeatherForecast(Base):

    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True)

    city = Column(String(100), nullable=False)
    latitude = Column(Numeric(8, 4), nullable=False)
    longitude = Column(Numeric(8, 4), nullable=False)

    date = Column(Date, nullable=False)
    extraction_date = Column(Date, nullable=False)

    temp_max = Column(Numeric(4, 1), nullable=False)
    temp_min = Column(Numeric(4, 1), nullable=False)
    temp_range = Column(Numeric(4, 1), nullable=False)

    precipitation = Column(Numeric(5, 2), nullable=False)
    precip_probability = Column(Numeric(5, 2), nullable=False)

    wind_speed = Column(Numeric(5, 2), nullable=False)
    wind_gust = Column(Numeric(5, 2), nullable=False)

    weather_code = Column(Integer, nullable=False)

    temp_category = Column(String(30), nullable=False)
    precip_category = Column(String(30), nullable=False)
    wind_category = Column(String(30), nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)

    day_of_week = Column(String(10), nullable=False)
    season = Column(String(10), nullable=False)

    risk_score = Column(Numeric(5, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "city",
            "date",
            "extraction_date",
            name="unique_forecast"
        ),

        Index("idx_weather_date", "date"),
        Index("idx_weather_city", "city"),
        Index("idx_weather_risk", "risk_score"),
    )



Base.metadata.create_all(engine)


from datetime import date

today = date.today().isoformat()

gold_file = f"gold/weather_{today}.csv"

df = pd.read_csv(gold_file)

print(f"Loading {len(df)} rows from {gold_file}...")

df.to_sql(
    "weather_forecasts",
    engine,
    if_exists="append",
    index=False
)

print("Gold data loaded successfully.")