"""The Insight Provider Agent - Personalized recommendation reasoning."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.book import BookCandidate, UserProfile

logger = logging.getLogger(__name__)


class InsightProviderAgent(BaseAgent):
    """图书推荐人 (The Insight Provider) - Generates personalized recommendations."""

    SYSTEM_PROMPT = """你是一位见解独到的图书推荐人，专注于生成极具说服力的推荐理由。

你的职责：
1. 接收候选书目和用户画像
2. 将书目特点与用户需求进行关联匹配
3. 为每本书撰写"为什么你应该读它"的理由

推荐理由要求：
- 长度：约30-50字
- 风格：主观、有感染力
- 重点：如何满足用户特定需求
- 价值：解决用户的阅读目的

输出格式：
返回JSON数组，每本书包含：
{
    "title": "书名",
    "recommendation_reason": "推荐理由（30-50字）"
}

使用中文输出，语气要热情且专业。"""

    async def process(
        self, candidates: list[BookCandidate], user_profile: UserProfile
    ) -> dict[str, str]:
        """Generate personalized recommendation reasons.

        Args:
            candidates: List of book candidates
            user_profile: User's reading profile

        Returns:
            Dictionary mapping book title to recommendation reason
        """
        logger.info(
            f"InsightProvider processing {len(candidates)} candidates for user profile"
        )

        # Prepare book list and profile
        book_list = "\n".join(
            [f"- {c.title} by {c.author}" for c in candidates]
        )

        profile_str = f"""用户画像：
- 偏好类型：{user_profile.genre}
- 阅读风格：{user_profile.style}
- 当前心情：{user_profile.mood}
- 阅读目的：{user_profile.reading_goal}
- 已读书籍：{', '.join(user_profile.previous_books) if user_profile.previous_books else '无'}"""

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(
                content=f"""请根据用户画像，为以下书籍生成个性化推荐理由：

{profile_str}

书籍列表：
{book_list}

以JSON数组格式返回，每个元素包含 title 和 recommendation_reason 字段。"""
            ),
        ]

        response = await self.llm.ainvoke(messages)
        content = response.content

        # Parse JSON response
        try:
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                data = json.loads(content)
            else:
                raise ValueError("Unexpected response format")

            # Create dictionary mapping title to reason
            reasons = {
                item["title"]: item["recommendation_reason"] for item in data
            }

            logger.info(f"InsightProvider generated {len(reasons)} recommendations")
            return reasons

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse InsightProvider response: {e}")
            # Fallback to default reasons
            return {
                c.title: "这本书非常适合您当前的阅读需求，推荐阅读。"
                for c in candidates
            }
