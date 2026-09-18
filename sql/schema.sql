-- Schema creation script for MétéoRisk
CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude NUMERIC(8, 4) NOT NULL,
    longitude NUMERIC(8, 4) NOT NULL,
    date DATE NOT NULL,
    extraction_date DATE NOT NULL,
    temp_max NUMERIC(4, 1) NOT NULL,
    temp_min NUMERIC(4, 1) NOT NULL,
    temp_range NUMERIC(4, 1) NOT NULL,
    precipitation NUMERIC(5, 2) NOT NULL,
    precip_probability NUMERIC(5, 2) NOT NULL,
    wind_speed NUMERIC(5, 2) NOT NULL,
    wind_gust NUMERIC(5, 2) NOT NULL,
    weather_code INTEGER NOT NULL,
    temp_category VARCHAR(30) NOT NULL,
    precip_category VARCHAR(30) NOT NULL,
    wind_category VARCHAR(30) NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    season VARCHAR(10) NOT NULL,
    risk_score NUMERIC(5, 2) NOT NULL,
    CONSTRAINT unique_forecast UNIQUE (city, date, extraction_date)
);

CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_forecasts(date);
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_forecasts(city);
CREATE INDEX IF NOT EXISTS idx_weather_risk ON weather_forecasts(risk_score);
