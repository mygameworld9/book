"""Recommendation request and response models."""

from pydantic import BaseModel, Field

from src.models.book import Book, UserProfile


class RecommendationRequest(BaseModel):
    """Request for book recommendations."""

    user_message: str = Field(..., description="User's message describing their needs")
    conversation_history: list[dict[str, str]] = Field(
        default_factory=list,
        description="Previous conversation messages",
    )


class RecommendationCard(BaseModel):
    """Final recommendation card with all book information."""

    user_profile: UserProfile = Field(..., description="User's reading profile")
    recommended_books: list[Book] = Field(
        ..., min_length=2, max_length=3, description="2-3 recommended books"
    )
    message: str = Field(..., description="Friendly message to user")
