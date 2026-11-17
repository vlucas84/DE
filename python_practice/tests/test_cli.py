import json
from unittest.mock import MagicMock
import pytest
from python_practice.cli import CommandLineInterface


def test_cli_parses_arguments():
    db = MagicMock()
    analytics = MagicMock()
    analytics.get_available_commands.return_value = ["all", "q1"]

    cli = CommandLineInterface(
        db, analytics, argv=["-s", "students.json", "-r", "rooms.json", "-f", "json", "-q", "q1"]
    )

    assert cli.args.format == "json"
    assert cli.args.query == "q1"


def test_cli_missing_required_args():
    db = MagicMock()
    analytics = MagicMock()
    analytics.get_available_commands.return_value = ["all"]

    with pytest.raises(SystemExit):
        CommandLineInterface(db, analytics, argv=[])


def test_cli_run_pipeline(tmp_path):
    rooms_file = tmp_path / "rooms.json"
    students_file = tmp_path / "students.json"
    rooms_file.write_text(json.dumps([{"id": 1, "name": "Room 1"}]))
    students_file.write_text(json.dumps([{"id": 10, "name": "Alice", "room": 1}]))

    db = MagicMock()
    analytics = MagicMock()
    analytics.get_available_commands.return_value = ["all"]
    analytics.run_all_queries.return_value = {"report_1": [{"count": 1}]}

    out_dir = tmp_path / "out"
    cli = CommandLineInterface(
        db,
        analytics,
        argv=["-s", str(students_file), "-r", str(rooms_file), "-f", "json", "-o", str(out_dir)],
    )
    cli.run()

    db.init_schema.assert_called_once()
    db.insert_rooms_batch.assert_called_once()
    db.insert_students_batch.assert_called_once()
    assert (out_dir / "report_1.json").exists()