-- Query 003: Top 5 rooms with the largest age difference among students
SELECT
    r.id AS room_id,
    r.name AS room_name,
    MAX(s.birthday) - MIN(s.birthday) AS age_diff_days
FROM rooms r
INNER JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
HAVING COUNT(s.id) > 1
ORDER BY age_diff_days DESC, r.id ASC
LIMIT 5;