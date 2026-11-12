-- Create rooms table if it does not exist
CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create students table if it does not exist
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room INT NOT NULL,
    CONSTRAINT fk_room FOREIGN KEY (room) REFERENCES rooms(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students (room, birthday);

CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students (room, sex);