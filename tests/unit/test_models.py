"""Unit tests for data models."""

import pytest
from pydantic import ValidationError

from src.models.book import Book, BookCandidate, UserProfile
from src.models.recommendation import RecommendationCard, RecommendationRequest


class TestUserProfile:
    """Tests for UserProfile model."""

    def test_valid_user_profile(self) -> None:
        """Test creating a valid user profile."""
        profile = UserProfile(
            genre="科幻",
            style="硬核",
            mood="渴望挑战",
            previous_books=["三体", "沙丘"],
            reading_goal="扩展科幻阅读视野",
        )
        assert profile.genre == "科幻"
        assert profile.style == "硬核"
        assert len(profile.previous_books) == 2

    def test_user_profile_empty_previous_books(self) -> None:
        """Test user profile with no previous books."""
        profile = UserProfile(
            genre="文学",
            style="轻松",
            mood="放松",
            reading_goal="休闲阅读",
        )
        assert profile.previous_books == []


class TestBookCandidate:
    """Tests for BookCandidate model."""

    def test_valid_book_candidate(self) -> None:
        """Test creating a valid book candidate."""
        book = BookCandidate(
            title="流浪地球",
            author="刘慈欣",
            isbn="978-7-5086-5305-4",
        )
        assert book.title == "流浪地球"
        assert book.author == "刘慈欣"

    def test_book_candidate_without_isbn(self) -> None:
        """Test book candidate without ISBN."""
        book = BookCandidate(
            title="基地",
            author="阿西莫夫",
        )
        assert book.isbn is None


class TestBook:
    """Tests for Book model."""

    def test_valid_book(self) -> None:
        """Test creating a valid complete book."""
        book = Book(
            title="银河帝国",
            author="阿西莫夫",
            isbn="978-7-5366-8670-0",
            summary="宏大的银河帝国兴衰史，展现人类文明的终极命运。",
            recommendation_reason="适合喜欢硬核科幻的读者，思想深度极高。",
        )
        assert book.title == "银河帝国"
        assert len(book.summary) > 0
        assert len(book.recommendation_reason) > 0


class TestRecommendationRequest:
    """Tests for RecommendationRequest model."""

    def test_valid_recommendation_request(self) -> None:
        """Test creating a valid recommendation request."""
        request = RecommendationRequest(
            user_message="我想读科幻小说",
            conversation_history=[
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "你好！我是图书推荐助手"},
            ],
        )
        assert request.user_message == "我想读科幻小说"
        assert len(request.conversation_history) == 2

    def test_recommendation_request_empty_history(self) -> None:
        """Test recommendation request with empty history."""
        request = RecommendationRequest(user_message="推荐一本书")
        assert request.conversation_history == []


class TestRecommendationCard:
    """Tests for RecommendationCard model."""

    def test_valid_recommendation_card(self) -> None:
        """Test creating a valid recommendation card."""
        profile = UserProfile(
            genre="科幻",
            style="硬核",
            mood="挑战",
            reading_goal="学习",
        )
        books = [
            Book(
                title="沙丘",
                author="弗兰克·赫伯特",
                summary="沙漠星球上的权力斗争与人类进化的史诗。",
                recommendation_reason="复杂的世界观和深刻的哲学思考。",
            ),
            Book(
                title="神经漫游者",
                author="威廉·吉布森",
                summary="赛博朋克的开山之作，虚拟现实的先驱。",
                recommendation_reason="开创性的科幻作品，影响深远。",
            ),
        ]
        card = RecommendationCard(
            user_profile=profile,
            recommended_books=books,
            message="为您精选了两本硬核科幻作品。",
        )
        assert len(card.recommended_books) == 2
        assert card.user_profile.genre == "科幻"

    def test_recommendation_card_min_books(self) -> None:
        """Test recommendation card requires at least 2 books."""
        profile = UserProfile(
            genre="文学",
            style="轻松",
            mood="放松",
            reading_goal="休闲",
        )
        books = [
            Book(
                title="活着",
                author="余华",
                summary="一个人一生的苦难与坚韧。",
                recommendation_reason="深刻的人性洞察。",
            ),
        ]

        with pytest.raises(ValidationError):
            RecommendationCard(
                user_profile=profile,
                recommended_books=books,
                message="推荐",
            )
