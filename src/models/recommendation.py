"""Recommendation models with multi-theme support."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ThemeLiteral = Literal["books", "games", "movies", "anime"]
ProfileValue = str | list[str] | dict[str, str]


class ConversationMessage(BaseModel):
    """Represents a single message exchanged in the conversation."""

    role: Literal["user", "assistant"] = Field(..., description="Message sender role")
    content: str = Field(..., description="Message content")


class RecommendationRequest(BaseModel):
    """Request payload for recommendation endpoints."""

    user_input: str = Field(
        ...,
        alias="user_message",
        description="User's latest message describing their needs",
    )
    conversation_history: list[ConversationMessage] = Field(
        default_factory=list,
        description="Previous conversation messages for additional context",
    )

    model_config = ConfigDict(populate_by_name=True)


class UserProfile(BaseModel):
    """Structured profile extracted from the selector agent."""

    theme: ThemeLiteral = Field(..., description="Theme these preferences belong to")
    summary: str | None = Field(
        default=None,
        description="Optional natural language summary of the profile",
    )
    attributes: dict[str, ProfileValue] = Field(
        default_factory=dict,
        description="Structured preference attributes captured during the conversation",
    )


class RecommendationCandidate(BaseModel):
    """Intermediate candidate item surfaced by the selector agent."""

    title: str = Field(..., description="Content title")
    creator: str = Field(
        ...,
        description="Primary creator such as author, director, developer, or studio",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Additional metadata fields (platform, year, genre, etc.)",
    )


class RecommendationCard(RecommendationCandidate):
    """Final recommendation card with summary and personalized reason."""

    summary: str = Field(
        ...,
        min_length=10,
        description="Concise summary highlighting the item's essence",
    )
    reason: str = Field(
        ...,
        min_length=10,
        description="Personalized reason aligning the item to the user profile",
    )


class RecommendationResponse(BaseModel):
    """Unified response model for multi-theme recommendations."""

    theme: ThemeLiteral = Field(..., description="Theme identifier")
    user_profile: UserProfile = Field(..., description="Structured user profile")
    recommendations: list[RecommendationCard] = Field(
        ...,
        min_length=2,
        max_length=3,
        description="List of 2-3 recommendation cards",
    )
    message: str = Field(..., description="Friendly assistant message to the user")
