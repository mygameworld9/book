"""The Assembler Agent - Information integration and formatting."""

import logging

from src.agents.base import BaseAgent
from src.models.book import Book, BookCandidate, UserProfile
from src.models.recommendation import RecommendationCard

logger = logging.getLogger(__name__)


class AssemblerAgent(BaseAgent):
    """在线图书管理员 (The Assembler) - Integrates and formats recommendations."""

    async def process(
        self,
        user_profile: UserProfile,
        candidates: list[BookCandidate],
        summaries: dict[str, str],
        reasons: dict[str, str],
    ) -> RecommendationCard:
        """Assemble final recommendation card.

        Args:
            user_profile: User's reading profile
            candidates: List of book candidates
            summaries: Book summaries keyed by title
            reasons: Recommendation reasons keyed by title

        Returns:
            Complete recommendation card
        """
        logger.info(f"Assembler integrating data for {len(candidates)} books")

        # Verify completeness
        books: list[Book] = []
        for candidate in candidates:
            title = candidate.title

            if title not in summaries:
                logger.warning(f"Missing summary for {title}")
                summaries[title] = f"这是一本由{candidate.author}撰写的优秀作品。"

            if title not in reasons:
                logger.warning(f"Missing recommendation reason for {title}")
                reasons[title] = "这本书值得您阅读。"

            # Create complete Book object
            book = Book(
                title=candidate.title,
                author=candidate.author,
                isbn=candidate.isbn,
                book_id=candidate.book_id,
                summary=summaries[title],
                recommendation_reason=reasons[title],
            )
            books.append(book)

        # Generate friendly message
        message = self._generate_message(user_profile, len(books))

        recommendation_card = RecommendationCard(
            user_profile=user_profile,
            recommended_books=books,
            message=message,
        )

        logger.info("Assembler successfully created recommendation card")
        return recommendation_card

    def _generate_message(self, profile: UserProfile, book_count: int) -> str:
        """Generate a friendly message to the user.

        Args:
            profile: User's reading profile
            book_count: Number of recommended books

        Returns:
            Friendly message string
        """
        return f"""基于您对{profile.genre}类书籍的偏好，以及{profile.mood}的心情，
我们为您精选了 {book_count} 本书。这些书籍都符合您{profile.reading_goal}的阅读目标。
您更倾向于哪一本？我们随时可以为您提供更多延伸信息。"""
