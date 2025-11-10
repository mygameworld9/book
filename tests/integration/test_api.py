"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Multi-Theme Recommendation API"
        assert "themes" in data and "books" in data["themes"]
        assert "/api/books/recommend" in data["endpoints"].values()


@pytest.mark.skip(reason="Requires OpenAI API key")
class TestRecommendationEndpoint:
    """Tests for recommendation endpoint (requires API key)."""

    def test_recommendation_endpoint(
        self,
        client: TestClient,
        sample_recommendation_request: dict[str, object],
    ) -> None:
        """Test recommendation endpoint returns valid response."""
        response = client.post(
            "/api/books/recommend",
            json=sample_recommendation_request,
        )
        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert data["theme"] == "books"
        assert "user_profile" in data
        assert "recommendations" in data
        assert "message" in data

        # Verify user profile
        profile = data["user_profile"]
        assert profile["theme"] == "books"
        assert isinstance(profile["attributes"], dict)

        # Verify books
        items = data["recommendations"]
        assert len(items) >= 2
        assert len(items) <= 3

        for item in items:
            assert "title" in item
            assert "creator" in item
            assert "summary" in item
            assert "reason" in item

    def test_recommendation_endpoint_invalid_request(
        self, client: TestClient
    ) -> None:
        """Test recommendation endpoint with invalid request."""
        response = client.post(
            "/api/books/recommend",
            json={},  # Missing required fields
        )
        assert response.status_code == 422  # Validation error
