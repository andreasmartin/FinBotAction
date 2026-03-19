import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base, get_db
from app.infrastructure.web.app import create_app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session):
    app = create_app(init_db=False)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}


def test_create_account_record_json(client):
    r = client.post(
        "/account-records",
        json={
            "KassierDate": "20.05.1980",
            "KassierName": "Monika Meier",
            "PraesidiumDate": "15.02.1980",
            "PraesidiumName": "Hans Muster",
            "VereinEmail": "info@shindokan.ch",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert "AntragsNr" in data
    assert len(data["AntragsNr"]) == 12


def test_create_account_record_form(client):
    r = client.post(
        "/account-records",
        data={
            "KassierDate": "21.05.1980",
            "KassierName": "Petra Baum",
            "PraesidiumDate": "16.02.1980",
            "PraesidiumName": "Paul Vogel",
            "VereinEmail": "verein@example.ch",
        },
    )
    assert r.status_code == 201
    assert "AntragsNr" in r.json()


def test_create_account_record_missing_required_field(client):
    r = client.post(
        "/account-records",
        json={
            "KassierDate": "20.05.1980",
            "KassierName": "Monika Meier",
            "PraesidiumDate": "15.02.1980",
            "PraesidiumName": "Hans Muster",
        },
    )
    assert r.status_code == 400


def test_root_html_lists_submitted_records(client):
    client.post(
        "/account-records",
        json={
            "KassierDate": "20.05.1980",
            "KassierName": "Monika Meier",
            "PraesidiumDate": "15.02.1980",
            "PraesidiumName": "Hans Muster",
            "VereinEmail": "info@shindokan.ch",
        },
    )
    client.post(
        "/account-records",
        data={
            "KassierDate": "21.05.1980",
            "KassierName": "Petra Baum",
            "PraesidiumDate": "16.02.1980",
            "PraesidiumName": "Paul Vogel",
            "VereinEmail": "verein@example.ch",
        },
    )

    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Monika Meier" in r.text
    assert "Petra Baum" in r.text
