-- KNIME / PostgreSQL analysis query
-- Returns one analytical row per city for the KNIME DB Query Reader node.
SELECT
    city,
    ROUND(AVG(max_temp)::numeric, 2) AS avg_max_temp,
    ROUND(AVG(min_temp)::numeric, 2) AS avg_min_temp,
    ROUND(SUM(precipitation)::numeric, 2) AS total_precipitation,
    COUNT(*) AS observation_count
FROM weather_data
GROUP BY city
ORDER BY avg_max_temp DESC;
