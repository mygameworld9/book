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
        assert "message" in data
        assert "docs" in data
        assert "health" in data


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
            "/api/v1/recommendations",
            json=sample_recommendation_request,
        )
        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "user_profile" in data
        assert "recommended_books" in data
        assert "message" in data

        # Verify user profile
        profile = data["user_profile"]
        assert "genre" in profile
        assert "style" in profile
        assert "mood" in profile
        assert "reading_goal" in profile

        # Verify books
        books = data["recommended_books"]
        assert len(books) >= 2
        assert len(books) <= 3

        for book in books:
            assert "title" in book
            assert "author" in book
            assert "summary" in book
            assert "recommendation_reason" in book

    def test_recommendation_endpoint_invalid_request(
        self, client: TestClient
    ) -> None:
        """Test recommendation endpoint with invalid request."""
        response = client.post(
            "/api/v1/recommendations",
            json={},  # Missing required fields
        )
        assert response.status_code == 422  # Validation error
