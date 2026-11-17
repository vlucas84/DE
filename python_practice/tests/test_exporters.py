import json
from python_practice.exporters import JsonExporter, XmlExporter, get_exporter


def test_json_exporter(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": 1, "name": "Room 101"}]

    JsonExporter().export(data, file_path)

    assert file_path.exists()
    assert json.loads(file_path.read_text()) == data


def test_xml_exporter(tmp_path):
    file_path = tmp_path / "test.xml"
    data = [{"id": 1, "name": "Room 101"}]

    XmlExporter().export(data, file_path)

    assert file_path.exists()
    content = file_path.read_text()
    assert "<results>" in content
    assert "<name>Room 101</name>" in content


def test_get_exporter():
    assert isinstance(get_exporter("json"), JsonExporter)
    assert isinstance(get_exporter("xml"), XmlExporter)