-- Query 004: List of rooms where students of different sexes live together
SELECT
    r.id AS room_id,
    r.name AS room_name
FROM rooms r
INNER JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) > 1
ORDER BY r.id;