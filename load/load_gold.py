from datetime import date

import pandas as pd

from sqlalchemy.dialects.postgresql import insert

from models import Base, WeatherForecast
from database import engine


Base.metadata.create_all(engine)


today = date.today().isoformat()

gold_file = f"gold/weather_{today}.csv"

df = pd.read_csv(gold_file)

print(f"Loading {len(df)} rows from {gold_file}...")

records = df.to_dict(orient="records")

with engine.begin() as connection:

    statement = insert(WeatherForecast).values(records)

    statement = statement.on_conflict_do_update(
        constraint="unique_forecast",
        set_={
            column.name: getattr(statement.excluded, column.name)
            for column in WeatherForecast.__table__.columns
            if column.name != "id"
        }
    )

    connection.execute(statement)


print("Gold data loaded successfully.")