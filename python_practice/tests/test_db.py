from unittest.mock import MagicMock, patch
import pytest
from python_practice import config
from python_practice.db import DatabaseManager


def test_init_missing_password(monkeypatch):
    monkeypatch.setattr(config, "db_password", "")
    with pytest.raises(ValueError):
        DatabaseManager()


def test_get_connection_commit_and_rollback(monkeypatch):
    monkeypatch.setattr(config, "db_password", "pass")
    db = DatabaseManager()

    mock_conn = MagicMock()
    with patch("python_practice.db.psycopg.connect", return_value=mock_conn):
        # 1. Успешный сценарий -> commit
        with db.get_connection():
            pass
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # 2. Сценарий с ошибкой -> rollback
        mock_conn.reset_mock()
        with pytest.raises(RuntimeError):
            with db.get_connection():
                raise RuntimeError("boom")
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()


def test_init_schema(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "db_password", "pass")
    db = DatabaseManager()

    schema_file = tmp_path / "schema.sql"
    schema_file.write_text("CREATE TABLE test (id INT);", encoding="utf-8")

    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

    with patch("python_practice.db.psycopg.connect", return_value=mock_conn):
        db.init_schema(schema_file)

    mock_cursor.execute.assert_called_once_with("CREATE TABLE test (id INT);")


def test_insert_rooms_batch(monkeypatch):
    monkeypatch.setattr(config, "db_password", "pass")
    db = DatabaseManager()

    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

    with patch("python_practice.db.psycopg.connect", return_value=mock_conn) as mock_connect:
        # Пустой список не должен открывать соединение
        db.insert_rooms_batch([])
        mock_connect.assert_not_called()

        # Непустой список вызывает executemany
        rooms = [{"id": 1, "name": "Room 1"}]
        db.insert_rooms_batch(rooms)
        mock_cursor.executemany.assert_called_once()


def test_execute_query(monkeypatch):
    monkeypatch.setattr(config, "db_password", "pass")
    db = DatabaseManager()

    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [{"id": 1, "count": 5}]

    with patch("python_practice.db.psycopg.connect", return_value=mock_conn):
        result = db.execute_query("SELECT 1;")

    assert result == [{"id": 1, "count": 5}]