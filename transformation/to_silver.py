import json
import pandas as pd
from pathlib import Path
import requests

cities = pd.read_csv("bronze/ma.csv")

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

    df["city"] = cities.iloc[i]["city"]
    df["latitude"] = cities.iloc[i]["lat"]
    df["longitude"] = cities.iloc[i]["lng"]

    all_data.append(df)

silver_df = pd.concat(all_data, ignore_index=True)
print(silver_df)