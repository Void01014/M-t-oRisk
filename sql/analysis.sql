SELECT city, MAX(temp_max) AS max_temperature
FROM weather_forecasts
GROUP BY city
ORDER BY max_temperature DESC
LIMIT 10;

SELECT city, MAX(precipitation) AS max_precipitation
FROM weather_forecasts
GROUP BY city
ORDER BY max_precipitation DESC
LIMIT 10;

SELECT city, ROUND(AVG(risk_score), 2) AS avg_risk_score
FROM weather_forecasts
GROUP BY city
ORDER BY avg_risk_score DESC
LIMIT 10;

SELECT date, ROUND(AVG(risk_score), 2) AS avg_daily_risk, MAX(risk_score) AS max_daily_risk
FROM weather_forecasts
GROUP BY date
ORDER BY max_daily_risk DESC;

-- WITH RankedRisks AS (
--     SELECT 
--         city,
--         date,
--         risk_score,
--         temp_max,
--         precipitation,
--         wind_gust,
--         ROW_NUMBER() OVER (PARTITION BY city ORDER BY risk_score DESC, date ASC) as rank
--     FROM weather_forecasts
-- )
-- SELECT city, date, risk_score, temp_max, precipitation, wind_gust
-- FROM RankedRisks
-- WHERE rank = 1
-- ORDER BY risk_score DESC;

SELECT wf.city, date
FROM weather_forecasts wf
JOIN (
    SELECT city, MAX(risk_score) AS max_risk_score
    FROM weather_forecasts
    GROUP BY city
) max_risks
ON wf.city = max_risks.city AND wf.risk_score = max_risks.max_risk_score
GROUP BY wf.city