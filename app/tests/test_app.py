import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR.parent / "src"
sys.path.append(str(SRC_DIR))

from app import app

def test_health_status_code():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_body():
    client = app.test_client()
    resp = client.get("/health")
    data = resp.get_json()
    assert data["status"] == "ok"


def test_items_endpoint():
    client = app.test_client()
    resp = client.get("/items")
    data = resp.get_json()
    assert data["items"] == [1, 2, 3]