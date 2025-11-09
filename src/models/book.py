"""Book-related data models."""

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User reading profile and preferences."""

    genre: str = Field(..., description="Preferred book genre (e.g., 科幻, 文学, 历史)")
    style: str = Field(..., description="Reading style preference (e.g., 硬核, 轻松, 深度)")
    mood: str = Field(..., description="Current reading mood (e.g., 渴望挑战, 放松, 学习)")
    previous_books: list[str] = Field(
        default_factory=list, description="List of previously read books"
    )
    reading_goal: str = Field(..., description="Purpose of current reading session")


class BookCandidate(BaseModel):
    """A candidate book for recommendation."""

    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Book author")
    isbn: str | None = Field(None, description="ISBN identifier")
    book_id: str | None = Field(None, description="Internal book ID")


class Book(BookCandidate):
    """Complete book information with summary and recommendation."""

    summary: str = Field(..., description="Concise book summary (50-80 characters)")
    recommendation_reason: str = Field(
        ..., description="Personalized recommendation reason (30-50 characters)"
    )
