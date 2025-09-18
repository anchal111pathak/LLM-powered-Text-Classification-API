from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_classify_and_feedback():
    r = client.post("/classify", json={"text": "I love this product"})
    assert r.status_code == 200
    data = r.json()
    assert "cls" in data

    fb = {"text": "I love this product", "predicted": data["cls"], "correct": "safe"}
    r2 = client.post("/feedback", json=fb)
    assert r2.status_code == 200
