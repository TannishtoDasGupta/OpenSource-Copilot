from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "OpenSource Copilot" in response.text


def test_analysis_routes_fail_closed_without_app_key(monkeypatch):
    monkeypatch.setattr("app.security.get_settings", lambda: SimpleNamespace(app_api_key=""))
    response = client.post("/api/triage/text", json={"title": "A valid title", "body": ""})
    assert response.status_code == 503


def test_analysis_routes_reject_wrong_app_key(monkeypatch):
    monkeypatch.setattr("app.security.get_settings", lambda: SimpleNamespace(app_api_key="a" * 40))
    response = client.post("/api/triage/text", headers={"X-App-API-Key": "wrong"}, json={"title": "A valid title", "body": ""})
    assert response.status_code == 401


def test_analysis_routes_accept_app_key_then_report_missing_openai_key(monkeypatch):
    monkeypatch.setattr("app.security.get_settings", lambda: SimpleNamespace(app_api_key="a" * 40))
    monkeypatch.setattr("app.services.ai.get_settings", lambda: SimpleNamespace(openai_api_key="", openai_model="gpt-5.5"))
    response = client.post("/api/triage/text", headers={"X-App-API-Key": "a" * 40}, json={"title": "A valid title", "body": ""})
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]
