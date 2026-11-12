-- Query 001: List of rooms and count of students living in each
SELECT
    r.id AS room_id,
    r.name AS room_name,
    COUNT(s.id) AS students_count
FROM rooms r
LEFT JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY r.id;