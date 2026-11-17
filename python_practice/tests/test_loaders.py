import json
import pytest
from python_practice.loaders import JsonLoader


def test_load_json(tmp_path):
    file_path = tmp_path / "rooms.json"
    data = [{"id": 1, "name": "Room 101"}]
    file_path.write_text(json.dumps(data))

    loader = JsonLoader()
    result = loader.load(file_path)

    assert result == data


def test_load_file_not_found(tmp_path):
    loader = JsonLoader()
    with pytest.raises(FileNotFoundError):
        loader.load(tmp_path / "no_file.json")


def test_load_batches(tmp_path):
    file_path = tmp_path / "students.json"
    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    file_path.write_text(json.dumps(data))

    loader = JsonLoader()
    batches = list(loader.load_batches(file_path, batch_size=2))

    assert len(batches) == 2
    assert batches[0] == [{"id": 1}, {"id": 2}]
    assert batches[1] == [{"id": 3}]