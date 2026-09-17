import pandas as pd
from datetime import date
from pathlib import Path

today = date.today().isoformat()

df = pd.read_csv(f"bronze/weather_{today}.csv")

df["city"] = df["city"].astype("string")

df["latitude"] = df["latitude"].astype("float")
df["longitude"] = df["longitude"].astype("float")

df["date"] = pd.to_datetime(df["date"])
df["extraction_date"] = pd.to_datetime(df["extraction_date"])

df["temp_max"] = df["temp_max"].astype("float")
df["temp_min"] = df["temp_min"].astype("float")
df["precipitation"] = df["precipitation"].astype("float")
df["precip_probability"] = df["precip_probability"].astype("float")
df["wind_speed"] = df["wind_speed"].astype("float")
df["wind_gust"] = df["wind_gust"].astype("float")

df["weather_code"] = df["weather_code"].astype("int")

df = df.drop_duplicates(
    subset=["city", "date", "extraction_date"],
    keep="last"
)

df = df.sort_values(["city", "date"])

df["temp_max"] = (
    df.groupby("city")["temp_max"]
      .transform(lambda x: x.interpolate())
)

df["temp_min"] = (
    df.groupby("city")["temp_min"]
      .transform(lambda x: x.interpolate())
)

def find_nearest_probability(row):

    if pd.notna(row["precip_probability"]):
        return row["precip_probability"]

    candidates = df[
        (df["date"] == row["date"]) &
        (df["city"] != row["city"]) &
        (df["precip_probability"].notna())
    ].copy()

    if candidates.empty:
        return None

    candidates["distance"] = (
        (candidates["latitude"] - row["latitude"]) ** 2
        + (candidates["longitude"] - row["longitude"]) ** 2
    )

    nearest = candidates.loc[candidates["distance"].idxmin()]

    return nearest["precip_probability"]

df["precip_probability"] = df.apply(
    find_nearest_probability,
    axis=1
)

df = df.dropna(
    subset=[
        "city",
        "latitude",
        "longitude",
        "date",
        "extraction_date",
        "temp_max",
        "temp_min",
        "precipitation",
        "precip_probability",
        "wind_speed",
        "wind_gust",
        "weather_code"
    ]
)

output_dir = Path("silver")
output_dir.mkdir(exist_ok=True)

df.to_csv(
    output_dir / f"weather_{today}.csv",
    index=False
)