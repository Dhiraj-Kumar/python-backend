from fastapi.testclient import TestClient
from app import app, init_db, get_db

import os
import sqlite3
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: create a fresh test database
    if os.path.exists("transactions.db"):
        os.remove("transactions.db")
    init_db()
    yield
    # Teardown: remove the test database
    if os.path.exists("transactions.db"):
        os.remove("transactions.db")


def test_add_transaction():
    data = {
        "amount": 100.0,
        "description": "Test expense",
        "type": "expense",
        "date": "2023-01-01"
    }
    response = client.post("/transactions/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["amount"] == 100.0
    assert result["description"] == "Test expense"
    assert result["type"] == "expense"
    assert result["date"] == "2023-01-01"
    assert "id" in result


def test_get_transactions():
    # Add a transaction first
    data = {
        "amount": 50.0,
        "description": "Test income",
        "type": "income",
        "date": "2023-01-02"
    }
    client.post("/transactions/", json=data)
    response = client.get("/transactions/")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["description"] == "Test income"


def test_delete_transaction():
    # Add a transaction first
    data = {
        "amount": 20.0,
        "description": "To be deleted",
        "type": "expense",
        "date": "2023-01-03"
    }
    post_resp = client.post("/transactions/", json=data)
    transaction_id = post_resp.json()["id"]
    # Delete the transaction
    del_resp = client.delete(f"/transactions/{transaction_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Transaction deleted"
    # Try deleting again (should 404)
    del_resp2 = client.delete(f"/transactions/{transaction_id}")
    assert del_resp2.status_code == 404
