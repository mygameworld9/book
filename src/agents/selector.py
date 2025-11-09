"""The Selector Agent - User interaction and coordination."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.book import BookCandidate, UserProfile

logger = logging.getLogger(__name__)


class SelectorAgent(BaseAgent):
    """文学向导 (The Selector) - Handles user interaction and task coordination."""

    SYSTEM_PROMPT = """你是一位专业的文学向导，负责与读者对话并理解他们的阅读需求。

你的职责：
1. 通过提问深入了解用户的偏好、阅读历史、当前心情和阅读目的
2. 基于对话生成用户画像标签
3. 从内部数据库筛选出2-3本最匹配的候选书目

提问技巧：
- "您最近读过什么书？最喜欢哪本，为什么？"
- "您现在的心情如何？是想放松、挑战自己还是学习新知识？"
- "您喜欢什么类型的书？科幻、文学、历史还是其他？"
- "您偏好什么样的阅读风格？轻松的、深度的还是硬核的？"

输出格式要求：
返回JSON格式，包含：
1. user_profile: 用户画像对象
2. candidates: 2-3本候选书目列表
3. message: 给用户的友好回复

保持专业、友好的语气，用中文回应。"""

    async def process(
        self,
        user_message: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[UserProfile, list[BookCandidate], str]:
        """Process user message and generate profile with book candidates.

        Args:
            user_message: User's current message
            conversation_history: Previous conversation messages

        Returns:
            Tuple of (user_profile, candidates, message_to_user)
        """
        logger.info("Selector processing user message")

        messages: list[SystemMessage | HumanMessage] = [
            SystemMessage(content=self.SYSTEM_PROMPT)
        ]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append(HumanMessage(content=msg.get("content", "")))

        # Add current message
        messages.append(HumanMessage(content=user_message))

        # Request structured output
        messages.append(
            HumanMessage(
                content="""请以JSON格式回复，包含以下字段：
{
    "user_profile": {
        "genre": "类型",
        "style": "风格",
        "mood": "心情",
        "previous_books": ["书名1", "书名2"],
        "reading_goal": "阅读目的"
    },
    "candidates": [
        {"title": "书名", "author": "作者", "isbn": "ISBN或null"},
        {"title": "书名", "author": "作者", "isbn": "ISBN或null"}
    ],
    "message": "给用户的友好回复"
}"""
            )
        )

        response = await self.llm.ainvoke(messages)
        content = response.content

        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                data = json.loads(content)
            else:
                raise ValueError("Unexpected response format")

            # Create models
            user_profile = UserProfile(**data["user_profile"])
            candidates = [BookCandidate(**c) for c in data["candidates"]]
            message = data["message"]

            logger.info(
                f"Selector generated profile and {len(candidates)} candidates"
            )
            return user_profile, candidates, message

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse Selector response: {e}")
            # Fallback to default values
            default_profile = UserProfile(
                genre="综合",
                style="适中",
                mood="探索",
                previous_books=[],
                reading_goal="阅读推荐",
            )
            default_candidates = [
                BookCandidate(title="默认推荐1", author="作者A", isbn=None),
                BookCandidate(title="默认推荐2", author="作者B", isbn=None),
            ]
            default_message = "我理解您的需求了，让我为您推荐一些书籍。"

            return default_profile, default_candidates, default_message
