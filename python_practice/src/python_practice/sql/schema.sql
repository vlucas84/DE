-- Create rooms table if it does not exist
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    room_name VARCHAR(20) NOT NULL
);


-- Create students table if it does not exist
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL,
    sex CHAR(1) NOT NULL,
    birthday TIMESTAMP,
    room_id INTEGER NOT NULL,

    CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES rooms(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);