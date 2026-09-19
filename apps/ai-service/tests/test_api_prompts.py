from fastapi.testclient import TestClient
from app.main import app
from tests.fixtures.requirements import (
    REQ_AUTHN_ONLY,
    REQ_GENERIC_API,
    REQ_REST_API,
    REQ_THAI_CRUD,
    REQ_WHITESPACE,
)

client = TestClient(app)


def test_analyze_endpoint_success():
    payload = {
        "raw_text": REQ_THAI_CRUD,
    }
    response = client.post("/v1/prompts/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "request_id" in data
    assert "normalized" in data
    assert "analysis" in data
    assert "prompt" in data
    assert "validation" in data

    assert data["normalized"]["normalized_text"] == REQ_THAI_CRUD
    assert data["validation"]["is_valid"] is True
    assert "## REQUIREMENTS" in data["prompt"]["raw_markdown"]


def test_analyze_endpoint_authn_only_rule():
    payload = {
        "raw_text": REQ_AUTHN_ONLY,
    }
    response = client.post("/v1/prompts/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    concepts = [c["name"] for c in data["analysis"]["technical_concepts"]]
    assert "Authentication" in concepts
    assert "Authorization" not in concepts


def test_analyze_endpoint_generic_api_rule():
    payload = {
        "raw_text": REQ_GENERIC_API,
    }
    response = client.post("/v1/prompts/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    concepts = [c["name"] for c in data["analysis"]["technical_concepts"]]
    assert "API Interface" in concepts
    assert "RESTful API" not in concepts


def test_analyze_endpoint_rest_api_rule():
    payload = {
        "raw_text": REQ_REST_API,
    }
    response = client.post("/v1/prompts/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    concepts = [c["name"] for c in data["analysis"]["technical_concepts"]]
    assert "RESTful API" in concepts


def test_analyze_endpoint_whitespace_returns_400():
    payload = {
        "raw_text": REQ_WHITESPACE,
    }
    response = client.post("/v1/prompts/analyze", json=payload)
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]


def test_analyze_endpoint_missing_body_returns_422():
    response = client.post("/v1/prompts/analyze", json={})
    assert response.status_code == 422
