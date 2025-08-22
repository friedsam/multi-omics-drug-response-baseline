
from fastapi.testclient import TestClient
from src.app.main import app

def test_health():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict():
    c = TestClient(app)
    payload = {"features": {"g1": 1.0, "g2": -2.0, "g3": 0.5}, "masks": {"g1":1,"g2":1,"g3":0}}
    r = c.post("/predict", json=payload)
    assert r.status_code == 200
    js = r.json()
    assert "risk_score" in js and "top_features" in js
