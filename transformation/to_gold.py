import pandas as pd
from datetime import date
from pathlib import Path

today = date.today().isoformat()

df = pd.read_csv(f"silver/weather_{today}.csv")


df["temp_category"] = pd.cut(
    df["temp_max"],
    bins=[
        -float("inf"),
        25,
        32,
        37,
        float("inf")
    ],
    labels=[
        "Cool / Mild",
        "Normal / Pleasant",
        "Warm",
        "Very Warm / Heatwave"
    ],
    right=False
)

df["precip_category"] = pd.cut(
    df["precipitation"],
    bins=[
        -float("inf"),
        0.1,
        1,
        5,
        float("inf")
    ],
    labels=[
        "Dry",
        "Light",
        "Moderate",
        "Heavy"
    ],
    right=False
)



df["wind_category"] = pd.cut(
    df["wind_speed"],
    bins=[
        -float("inf"),
        15,
        25,
        35,
        float("inf")
    ],
    labels=[
        "Calm / Light",
        "Moderate",
        "Strong",
        "Very Strong / Stormy"
    ],
    right=False
)


df["temp_range"] = df["temp_max"] - df["temp_min"]

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.day_name()


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"


df["season"] = df["month"].apply(get_season)


def temperature_risk(temp):
    if temp <= 30:
        return 10
    elif temp <= 35:
        return 50
    elif temp <= 38:
        return 75
    else:
        return 100


df["temp_risk"] = df["temp_max"].apply(temperature_risk)


def wind_risk(gust):
    if gust <= 35:
        return 10
    elif gust <= 50:
        return 40
    elif gust <= 65:
        return 75
    else:
        return 100


df["wind_risk"] = df["wind_gust"].apply(wind_risk)


def precipitation_risk(precipitation):
    if precipitation == 0:
        return 0
    elif precipitation <= 1:
        return 30
    elif precipitation <= 5:
        return 60
    else:
        return 100


df["precip_risk"] = df["precipitation"].apply(precipitation_risk)


df["risk_score"] = (
    0.30 * df["temp_risk"]
    + 0.50 * df["wind_risk"]
    + 0.20 * df["precip_risk"]
).round(2)


df = df.drop(
    columns=[
        "temp_risk",
        "wind_risk",
        "precip_risk"
    ]
)

output_dir = Path("gold")
output_dir.mkdir(exist_ok=True)

df.to_csv(
    output_dir / f"weather_{today}.csv",
    index=False
)