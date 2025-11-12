"""Unit tests for recommendation data models."""

import pytest
from pydantic import ValidationError

from src.models.recommendation import (
    ConversationMessage,
    RecommendationCard,
    RecommendationCandidate,
    RecommendationRequest,
    RecommendationResponse,
    UserProfile,
)


class TestRecommendationRequest:
    """Tests for the recommendation request model."""

    def test_alias_user_message(self) -> None:
        """Ensure user_message alias populates user_input."""
        request = RecommendationRequest(
            user_message="我想找硬核科幻小说",
            conversation_history=[{"role": "assistant", "content": "你好"}],
        )
        assert request.user_input == "我想找硬核科幻小说"
        assert isinstance(request.conversation_history[0], ConversationMessage)

    def test_empty_history_default(self) -> None:
        """Ensure conversation history defaults to empty list."""
        request = RecommendationRequest(user_message="推荐电影")
        assert request.conversation_history == []


class TestUserProfile:
    """Tests for the user profile model."""

    def test_accepts_mixed_attribute_types(self) -> None:
        """Attributes can contain str, list, and dict values."""
        profile = UserProfile(
            theme="games",
            summary="偏好开放世界的轻度探索体验",
            attributes={
                "类型": ["RPG", "动作"],
                "心情": "放松",
                "偏好": {"多人": "否", "时长": "中等"},
            },
        )
        assert profile.attributes["类型"] == ["RPG", "动作"]
        assert profile.attributes["偏好"]["多人"] == "否"  # type: ignore[index]


class TestRecommendationCandidate:
    """Tests for candidate items."""

    def test_metadata_defaults(self) -> None:
        """Metadata defaults to empty dict."""
        candidate = RecommendationCandidate(title="沙丘", creator="弗兰克·赫伯特")
        assert candidate.metadata == {}


class TestRecommendationCard:
    """Tests for final recommendation card."""

    def test_extends_candidate(self) -> None:
        """Card inherits title/creator metadata."""
        card = RecommendationCard(
            title="沙丘",
            creator="弗兰克·赫伯特",
            metadata={"年份": "1965"},
            summary="描绘厄拉科斯星球权力斗争与生态哲思的史诗级故事。",
            reason="其宏大的世界观与哲思契合您对硬核科幻的期待。",
        )
        assert card.metadata["年份"] == "1965"

    def test_requires_minimum_summary_length(self) -> None:
        """Summary shorter than 10 chars should raise validation error."""
        with pytest.raises(ValidationError):
            RecommendationCard(
                title="测试",
                creator="测试者",
                metadata={},
                summary="太短",
                reason="理由充足，符合需求。",
            )


class TestRecommendationResponse:
    """Tests for response envelope."""

    def test_requires_two_recommendations(self) -> None:
        """Response enforces min length of 2."""
        profile = UserProfile(theme="books", attributes={"类型": ["科幻"]})
        card = RecommendationCard(
            title="银河帝国",
            creator="阿西莫夫",
            metadata={},
            summary="描绘银河帝国兴衰与心理史学的硬核科幻经典叙事。",
            reason="其宏大的时间尺度与逻辑推演满足你的思辨需求。",
        )
        with pytest.raises(ValidationError):
            RecommendationResponse(
                theme="books",
                user_profile=profile,
                recommendations=[card],
                message="至少需要两条推荐。",
            )

    def test_valid_response(self) -> None:
        """Ensure valid payload passes."""
        profile = UserProfile(theme="movies", attributes={"风格": "烧脑"})
        cards = [
            RecommendationCard(
                title="盗梦空间",
                creator="克里斯托弗·诺兰",
                metadata={"年份": "2010"},
                summary="多层梦境交错推进，探讨现实与潜意识边界的科幻悬疑片。",
                reason="复杂叙事结构契合你对烧脑体验的偏好。",
            ),
            RecommendationCard(
                title="银翼杀手2049",
                creator="丹尼斯·维伦纽瓦",
                metadata={"年份": "2017"},
                summary="冷峻未来主义视觉语言延续人类与复制人的身份拷问。",
                reason="它的哲学思辨与视觉沉浸感满足你求知与审美双重需求。",
            ),
        ]
        response = RecommendationResponse(
            theme="movies",
            user_profile=profile,
            recommendations=cards,
            message="祝你观影愉快！",
            request_id="test-request-id-123",
        )
        assert len(response.recommendations) == 2
        assert response.request_id == "test-request-id-123"
