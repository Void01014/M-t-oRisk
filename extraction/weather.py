import json
import pandas as pd
from pathlib import Path
import requests
from datetime import date

cities = pd.read_csv("extraction/ma.csv")

weather_results = []

for _, row in cities.iterrows():

    city_name = row["city"]
    latitude = row["lat"]
    longitude = row["lng"]

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "weather_code"
            ],
            "forecast_days": 7,
            "timezone": "auto"
        },
        timeout=10
    )

    response.raise_for_status()

    weather_results.append(response.json())


all_data = []

for i, weather in enumerate(weather_results):

    daily = weather["daily"]

    df = pd.DataFrame(daily)

    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "precipitation_sum": "precipitation",
        "precipitation_probability_max": "precip_probability",
        "wind_speed_10m_max": "wind_speed",
        "wind_gusts_10m_max": "wind_gust",
    })

    extraction_date = date.today().isoformat()

    df["city"] = cities.iloc[i]["city"]
    df["latitude"] = cities.iloc[i]["lat"]
    df["longitude"] = cities.iloc[i]["lng"]
    df["extraction_date"] = extraction_date

    all_data.append(df)

bronze_df = pd.concat(all_data, ignore_index=True)

today = date.today().isoformat()

output_dir = Path("bronze")
output_dir.mkdir(exist_ok=True)

bronze_df.to_csv(output_dir / f"weather_{today}.csv", index=False)