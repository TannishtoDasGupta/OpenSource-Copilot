from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_dashboard_is_served():
    response = client.get('/')
    assert response.status_code == 200
    assert 'OpenSource Copilot' in response.text

def test_issue_text_validates_title():
    assert client.post('/api/triage/text', json={'title': ''}).status_code == 422

def test_github_issue_validates_number():
    response = client.post('/api/triage/issue', json={'owner':'octocat','repo':'hello-world','issue_number':0})
    assert response.status_code == 422
