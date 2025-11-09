"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create FastAPI test client.

    Returns:
        TestClient instance
    """
    return TestClient(app)


@pytest.fixture
def sample_recommendation_request() -> dict[str, object]:
    """Create sample recommendation request.

    Returns:
        Sample request data
    """
    return {
        "user_message": "我想读一些科幻小说，最近读完了《三体》，想找类似的作品。",
        "conversation_history": [],
    }


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set mock environment variables for testing.

    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4")
