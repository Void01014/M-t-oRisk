-- Business Analysis SQL Queries for MétéoRisk

-- 1. Quelles villes auront les températures les plus élevées ?
SELECT city, MAX(temp_max) AS max_temperature
FROM weather_forecasts
GROUP BY city
ORDER BY max_temperature DESC
LIMIT 10;

-- 2. Quelles villes auront les plus fortes précipitations ?
SELECT city, MAX(precipitation) AS max_precipitation
FROM weather_forecasts
GROUP BY city
ORDER BY max_precipitation DESC
LIMIT 10;

-- 3. Quelles villes présentent le risque moyen le plus élevé ?
SELECT city, ROUND(AVG(risk_score), 2) AS avg_risk_score
FROM weather_forecasts
GROUP BY city
ORDER BY avg_risk_score DESC
LIMIT 10;

-- 4. Quelles périodes présentent le risque maximal ?
SELECT date, ROUND(AVG(risk_score), 2) AS avg_daily_risk, MAX(risk_score) AS max_daily_risk
FROM weather_forecasts
GROUP BY date
ORDER BY max_daily_risk DESC;

-- 5. Pour chaque ville, quelle période présente le plus grand risque ?
WITH RankedRisks AS (
    SELECT 
        city,
        date,
        risk_score,
        temp_max,
        precipitation,
        wind_gust,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY risk_score DESC, date ASC) as rank
    FROM weather_forecasts
)
SELECT city, date, risk_score, temp_max, precipitation, wind_gust
FROM RankedRisks
WHERE rank = 1
ORDER BY risk_score DESC;
