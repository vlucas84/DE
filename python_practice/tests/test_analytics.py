import json
from unittest.mock import MagicMock
import pytest
from python_practice.analytics import AnalyticsService


def test_init_missing_registry(tmp_path):
    mock_db = MagicMock()
    with pytest.raises(FileNotFoundError):
        AnalyticsService(db_manager=mock_db, sql_dir=tmp_path)


def test_get_available_commands(tmp_path):
    registry = [
        {"command": "q1", "id": "rooms", "file": "q1.sql"},
        {"command": "q2", "id": "age", "file": "q2.sql"},
    ]
    (tmp_path / "queries.json").write_text(json.dumps(registry), encoding="utf-8")

    service = AnalyticsService(db_manager=MagicMock(), sql_dir=tmp_path)

    assert service.get_available_commands() == ["all", "q1", "q2"]


def test_run_query_by_command_success_and_unknown(tmp_path):
    registry = [{"command": "q1", "id": "rooms_count", "file": "q1.sql"}]
    (tmp_path / "queries.json").write_text(json.dumps(registry), encoding="utf-8")
    (tmp_path / "q1.sql").write_text("SELECT * FROM rooms;", encoding="utf-8")

    mock_db = MagicMock()
    mock_db.execute_query.return_value = [{"room": 1, "count": 3}]

    service = AnalyticsService(db_manager=mock_db, sql_dir=tmp_path)

    # 1. Valid command executes query and returns results
    key, rows = service.run_query_by_command("q1")
    assert key == "q1_rooms_count"
    assert rows == [{"room": 1, "count": 3}]
    mock_db.execute_query.assert_called_once_with("SELECT * FROM rooms;")

    # 2. Unknown command raises ValueError
    with pytest.raises(ValueError, match="Unknown query command"):
        service.run_query_by_command("q99")


def test_run_all_queries(tmp_path):
    registry = [
        {"command": "q1", "id": "first", "file": "q1.sql"},
        {"command": "q2", "id": "second", "file": "q2.sql"},
    ]
    (tmp_path / "queries.json").write_text(json.dumps(registry), encoding="utf-8")
    (tmp_path / "q1.sql").write_text("SELECT 1;", encoding="utf-8")
    (tmp_path / "q2.sql").write_text("SELECT 2;", encoding="utf-8")

    mock_db = MagicMock()
    mock_db.execute_query.side_effect = [[{"res": 1}], [{"res": 2}]]

    service = AnalyticsService(db_manager=mock_db, sql_dir=tmp_path)
    results = service.run_all_queries()

    assert results == {
        "q1_first": [{"res": 1}],
        "q2_second": [{"res": 2}],
    }
    assert mock_db.execute_query.call_count == 2