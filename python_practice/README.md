# Python Practice: ETL Pipeline & Analytics

An ETL pipeline that extracts data from JSON files (students and rooms), loads it into a PostgreSQL database, performs analytical SQL queries, and exports the results in JSON or XML format.

---

## Tech Stack

* **Python 3.12+**
* **PostgreSQL 16** (via Docker)
* **psycopg 3** (PostgreSQL driver, no ORM)
* **Docker & Docker Compose**
* **uv** (Dependency manager)

---

## Features

* **Relational database schema** with a many-to-one relationship.
* **Pure SQL data ingestion** (no ORM).
* **Database-level processing:** All mathematical operations (aggregations, sorting) are handled at the database level.
* **Query optimization** using composite indexes.
* **OOP design** following SOLID principles.
* **CLI interface** supporting `--students`, `--rooms`, `--format`, and other configuration flags.

---

## Project Structure

* **`loaders.py`**: Abstract `BaseLoader` and `JsonLoader` streaming implementation.
* **`exporters.py`**: Abstract `BaseExporter`, `JsonExporter`/`XmlExporter`, and a factory function.
* **`db.py`**: Database connection management, schema initialization, and batch inserts.
* **`analytics.py`**: `AnalyticsService` executes SQL queries managed via the registry.
* **`cli.py`**: `CommandLineInterface` orchestrates the pipeline and parses arguments.
* **`sql/`**: Contains `schema.sql`, `queries.json` registry, and individual `.sql` files for queries.

---

## Installation & Setup

### 1. Prepare Data
Ensure `students.json` and `rooms.json` are in the project root. If they are missing, place them next to `pyproject.toml`.

### 2. Environment Variables
Create a `.env` file in the project root (or copy from `.env.example`) with the following content:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=python_practice_db
DB_USER=postgres
DB_PASSWORD=postgrespassword
```

### 3. Start the Database
Run the following command to start the PostgreSQL container:

```bash
docker compose up -d
```

### 4. Install Dependencies
Run the following command to install the required packages:

```bash
uv sync
```

### 5. Run the Pipeline
Run the main ETL script:

```bash
python -m python_practice.main --students students.json --rooms rooms.json --format json
```

---

## Usage Examples

### Screenshots

#### CLI Help Output
![CLI Help Output](docs/help_output.png)

#### Successful Pipeline Execution
![Successful Pipeline Execution](docs/pipeline_success.png)

### Available CLI Parameters

| Parameter | Short | Required | Default | Description |
| :--- | :---: | :---: | :---: | :--- |
| `--students` | `-s` | **Yes** | — | Path to students JSON file |
| `--rooms` | `-r` | **Yes** | — | Path to rooms JSON file |
| `--format` | `-f` | **Yes** | — | Export format (`json` or `xml`) |
| `--query` | `-q` | No | `all` | Specific query to run (`all`, `q1`, `q2`, `q3`, `q4`) |
| `--output-dir` | `-o` | No | `output/` | Output directory for saved reports |
| `--batch-size` | — | No | `1000` | Batch size for database inserts |
| `--verbose` | `-v` | No | `False` | Enable debug-level logging |

---

## Analytical Queries

All calculations are performed on the PostgreSQL side. Queries are stored in `src/python_practice/sql/` and managed via `queries.json`.

* **`q1`**: List of rooms and the number of students in each.
* **`q2`**: Top 5 rooms with the lowest average student age.
* **`q3`**: Top 5 rooms with the largest age difference among students (`max - min`).
* **`q4`**: List of rooms where students of different sexes live together.

---

## Optimization (Indexes)

To speed up analytical queries, the following indexes are added in `schema.sql`:

* **`idx_students_room_birthday`**: Designed for `q2` and `q3` (age aggregation and calculations).
* **`idx_students_room_sex`**: Designed for `q4` (mixed-sex rooms lookup).