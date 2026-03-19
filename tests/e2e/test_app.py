import os
import time
import httpx
import pytest

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8001")


@pytest.fixture(scope="session")
def client():
    # simple wait loop (container startup)
    for _ in range(30):
        try:
            r = httpx.get(f"{BASE_URL}/health", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    else:
        raise RuntimeError("API did not start")

    with httpx.Client(base_url=BASE_URL) as c:
        yield c


def test_create_account_record(client):
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


def test_list_account_records_page(client):
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
    assert "Petra Baum" in r.text
