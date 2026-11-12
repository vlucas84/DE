-- Query 002: Top 5 rooms with the lowest average student age
SELECT
    r.id AS room_id,
    r.name AS room_name,
    ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM s.birthday)), 2) AS avg_age
FROM rooms r
INNER JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY avg_age ASC, r.id ASC
LIMIT 5;