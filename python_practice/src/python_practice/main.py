# Import sys to handle command-line arguments manually
import sys

# Import Path for cross-platform file path management
from pathlib import Path

# Import Any for generic dictionary type annotations
from typing import Any

# Import analytics query functions returning statistics datasets
from python_practice.analytics import (
    get_rooms_with_mixed_sex,
    get_rooms_with_student_count,
    get_top_5_rooms_biggest_age_diff,
    get_top_5_youngest_rooms,
)

# Import the database connection check, schema init, and bulk insertion functions
from python_practice.db import (
    check_connection,
    db_init,
    insert_rooms,
    insert_students,
)

# Import serializers to export analytics data to JSON and XML
from python_practice.exporters import (
    export_to_json, 
    export_to_xml
)

# Import JSON file loader helper
from python_practice.loaders import load_json


def check_db_status() -> None:
    """Check database status."""
    print("Checking database connection...")

    # Execute health-check query and report status
    if check_connection():
        print("SUCCESS: Connection established!")
    else:
        print("ERROR: Could not connect to PostgreSQL.")


def check_db_init() -> None:
    """Check database initialization."""
    print("Checking database initialization...")

    # Execute DDL statements from the schema file
    if db_init():
        print("SUCCESS: Database initialized!")
    else:
        print("ERROR: Could not initialize database.")


def load_data() -> None:
    """Load rooms and students from JSON files into the database."""
    # Resolve absolute paths to source JSON files relative to project root
    project_root = Path(__file__).resolve().parent.parent.parent
    rooms_path = project_root / "rooms.json"
    students_path = project_root / "students.json"

    # Ensure required input files exist before proceeding
    if not rooms_path.is_file() or not students_path.is_file():
        print(f"ERROR: Missing JSON data files in {project_root}")
        return

    # Extract: parse JSON files from disk
    print("Loading JSON data files...")
    rooms = load_json(rooms_path)
    students = load_json(students_path)
    print(f"Loaded {len(rooms)} rooms and {len(students)} students from disk.")

    # Load: insert parent records first to satisfy foreign key constraints
    print("Inserting rooms into database...")
    if not insert_rooms(rooms):
        print("ERROR: Failed to insert rooms. Aborting migration.")
        return
    print(f"SUCCESS: Inserted {len(rooms)} rooms.")

    # Load: insert dependent child records referencing rooms
    print("Inserting students into database...")
    if not insert_students(students):
        print("ERROR: Failed to insert students. Aborting migration.")
        return
    print(f"SUCCESS: Inserted {len(students)} students.")

    print("SUCCESS: All data successfully loaded!")


def run_analytics() -> None:
    """Execute analytics queries and print sample results to terminal."""
    print("Running analytics queries...\n")

    # Collect analytical query results mapped to display titles
    queries: dict[str, list[dict[str, Any]]] = {
        "1. Rooms and student count": get_rooms_with_student_count(),
        "2. Top 5 youngest rooms": get_top_5_youngest_rooms(),
        "3. Top 5 biggest age difference": get_top_5_rooms_biggest_age_diff(),
        "4. Rooms with mixed sexes": get_rooms_with_mixed_sex(),
    }

    # Iterate over query datasets and print top records for quick inspection
    for title, rows in queries.items():
        print(f"=== {title} (Total rows: {len(rows)}) ===")
        for row in rows[:3]:
            print(" ", row)
        if len(rows) > 3:
            print("  ...")
        print()


def export_reports(export_format: str) -> None:
    """Execute queries and export them to output/ folder in JSON or XML."""
    # Normalize export format string and validate against supported choices
    export_format = export_format.lower()
    if export_format not in ("json", "xml"):
        print(f"ERROR: Unsupported format '{export_format}'.")
        print("Usage: python -m python_practice.main db-export <format> (choose 'json' or 'xml')")
        return

    # Ensure output destination directory exists in project root
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather data from all four analytical queries
    reports: dict[str, list[dict[str, Any]]] = {
        "rooms_student_count": get_rooms_with_student_count(),
        "top5_youngest_rooms": get_top_5_youngest_rooms(),
        "top5_biggest_age_diff": get_top_5_rooms_biggest_age_diff(),
        "rooms_different_sex": get_rooms_with_mixed_sex(),
    }

    # Choose serializer function based on selected format
    exporter = export_to_json if export_format == "json" else export_to_xml

    print(f"Exporting reports to '{output_dir}' as {export_format.upper()}...")

    # Iterate over datasets, serialize, and write files to disk
    for report_name, data in reports.items():
        destination = output_dir / f"{report_name}.{export_format}"
        exporter(data, destination)
        print(f"SUCCESS: Exported {len(data)} records -> {destination.name}")

    print("\nSUCCESS: All reports exported successfully!")


def main() -> None:
    """Main entry point for handling CLI command routing manually."""
    # Multi-line usage instructions displaying each command and its description
    usage_text = (
        "Usage: python -m python_practice.main <command>\n\n"
        "Available commands:\n"
        "  db-status            Check PostgreSQL connection\n"
        "  db-init              Apply schema.sql DDL migrations\n"
        "  db-load              Load rooms.json and students.json into database\n"
        "  db-analytics         Run SQL analytics and display preview in terminal\n"
        "  db-export <format>   Export reports to output/ folder ('json' or 'xml')"
    )

    # Verify if a CLI command was passed
    if len(sys.argv) < 2:
        print(usage_text)
        return

    command = sys.argv[1]

    # Route execution to corresponding handler function based on CLI input
    if command == "db-status":
        check_db_status()
    elif command == "db-init":
        check_db_init()
    elif command == "db-load":
        load_data()
    elif command == "db-analytics":
        run_analytics()
    elif command == "db-export":
        # Ensure export format argument is provided by user
        if len(sys.argv) < 3:
            print("ERROR: Missing export format.\n")
            print("Usage: python -m python_practice.main db-export <format> ('json' or 'xml')")
            return
        export_reports(sys.argv[2])
    else:
        print(f"Unknown command: '{command}'\n")
        print(usage_text)


if __name__ == "__main__":
    # Execute the manual routing function when script is run directly
    main()