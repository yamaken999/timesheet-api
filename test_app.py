import io
import os
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_holidays_ui(client):
    res = client.get("/holidays-ui")
    assert res.status_code == 200
    assert b"html" in res.data or b"HTML" in res.data

def test_holidays_download_not_found(client):
    pytest.skip("holidays.csv を削除しないためスキップ")

def test_holidays_upload_and_download(client):
    data = {
        "file": (io.BytesIO("2024-01-01,元日\n".encode("utf-8")), "holidays.csv")
    }
    res = client.post("/holidays/upload", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    assert "アップロード完了" in res.get_data(as_text=True)
    res = client.get("/holidays/download")
    assert res.status_code == 200
    assert "元日" in res.data.decode("utf-8")

def test_holidays_upload_invalid_file(client):
    data = {
        "file": (io.BytesIO(b"dummy"), "not_csv.txt")
    }
    res = client.post("/holidays/upload", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    assert "CSVファイルのみアップロード可能です" in res.get_data(as_text=True)

def test_upload_invalid_file_count(client):
    data = {
        "files": [
            (io.BytesIO(b"dummy1"), "a.csv"),
            (io.BytesIO(b"dummy2"), "b.csv"),
        ],
        "name": "test",
        "eid": "E001",
        "organization": "org",
        "year": "2024",
        "month": "1",
        "task": "task",
    }
    res = client.post("/upload", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    assert "ファイル数が不正" in res.get_data(as_text=True)