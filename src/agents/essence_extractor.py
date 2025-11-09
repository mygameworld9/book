"""The Essence Extractor Agent - Book summary generation."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.book import BookCandidate

logger = logging.getLogger(__name__)


class EssenceExtractorAgent(BaseAgent):
    """摘要撰写者 (The Essence Extractor) - Generates concise book summaries."""

    SYSTEM_PROMPT = """你是一位专业的摘要撰写者，擅长提炼书籍的核心精髓。

你的职责：
1. 接收候选书目列表
2. 为每本书生成简洁、客观、清晰的摘要
3. 识别书的核心主题、主要冲突和重要人物
4. 避免过度剧透

摘要要求：
- 长度：约50-80字
- 风格：客观、精练
- 重点：核心主题和价值
- 避免：剧透关键情节

输出格式：
返回JSON数组，每本书包含：
{
    "title": "书名",
    "summary": "精髓摘要（50-80字）"
}

使用中文输出。"""

    async def process(
        self, candidates: list[BookCandidate]
    ) -> dict[str, str]:
        """Generate summaries for book candidates.

        Args:
            candidates: List of book candidates

        Returns:
            Dictionary mapping book title to summary
        """
        logger.info(f"EssenceExtractor processing {len(candidates)} candidates")

        # Prepare book list
        book_list = "\n".join(
            [f"- {c.title} by {c.author}" for c in candidates]
        )

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(
                content=f"""请为以下书籍生成摘要：

{book_list}

以JSON数组格式返回，每个元素包含 title 和 summary 字段。"""
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

            # Create dictionary mapping title to summary
            summaries = {item["title"]: item["summary"] for item in data}

            logger.info(f"EssenceExtractor generated {len(summaries)} summaries")
            return summaries

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse EssenceExtractor response: {e}")
            # Fallback to default summaries
            return {
                c.title: f"这是一本由{c.author}撰写的优秀作品，值得一读。"
                for c in candidates
            }
