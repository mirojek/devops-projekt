import os
import pytest

from app.src import create_app, db
from app.src.app import User

@pytest.fixture()
def app():
    os.environ["DB_HOST"] = "db"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "devdb"
    os.environ["DB_USER"] = "devuser"
    os.environ["DB_PASSWORD"] = "devpass"

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture()
def client(app):
    return app.test_client()

def test_user_to_dict():
    user = User(id=1, name="Test", email="test@email.com")
    d = user.to_dict()
    assert d["id"] == 1
    assert d["name"] == "Test"
    assert d["email"] == "test@email.com"

def test_business_logic_add_user(app):
    with app.app_context():
        u = User(name="Ala", email="ala@email.com")
        db.session.add(u)
        db.session.commit()

        found = User.query.filter_by(email="ala@email.com").first()
        assert found is not None
        assert found.name == "Ala"

def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] in ("ok", "error")