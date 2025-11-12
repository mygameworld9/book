"""The Essence Extractor Agent - summary generation for all themes."""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.recommendation import RecommendationCandidate, ThemeLiteral

logger = logging.getLogger(__name__)


class EssenceExtractorAgent(BaseAgent):
    """提炼候选项目精髓的 Agent。"""

    def __init__(self, *, theme: ThemeLiteral, **kwargs: Any) -> None:
        super().__init__(theme=theme, **kwargs)
        self.system_prompt = self.load_prompt("extractor")

    async def process(
        self, candidates: list[RecommendationCandidate]
    ) -> dict[str, str]:
        """Generate summaries for candidates.

        Args:
            candidates: List of candidates

        Returns:
            Dictionary mapping item title to summary
        """
        logger.info(
            "EssenceExtractor processing %s candidates for theme=%s",
            len(candidates),
            self.theme,
        )

        payload = {
            "theme": self.theme,
            "candidates": [c.model_dump() for c in candidates],
        }

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(
                content=(
                    "请为以下候选内容生成简洁摘要，长度保持在50-80字：\n"
                    f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
                    "只返回JSON数组或包含 summaries 字段的对象，每个元素包含 title 和 summary。"
                )
            ),
        ]

        response = await self.llm.ainvoke(messages)
        summaries = self._parse_summaries(response.content)

        if not summaries:
            logger.warning(
                "EssenceExtractor failed to parse output, using fallback summaries"
            )
            return {
                c.title: f"{c.title} 由 {c.creator} 创作，是值得一试的优质作品。"
                for c in candidates
            }

        logger.info("EssenceExtractor generated %s summaries", len(summaries))
        return summaries

    def _parse_summaries(self, content: Any) -> dict[str, str]:
        if not isinstance(content, str):
            return {}

        text = content.strip()
        if "```json" in text:
            text = text.split("```json", maxsplit=1)[1].split("```", maxsplit=1)[0]
        elif "```" in text:
            text = text.split("```", maxsplit=1)[1].split("```", maxsplit=1)[0]

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.error("Failed to decode extractor JSON: %s", exc)
            return {}

        entries: list[dict[str, Any]]
        if isinstance(data, dict) and "summaries" in data:
            entries = data["summaries"]
        elif isinstance(data, list):
            entries = data
        else:
            return {}

        result: dict[str, str] = {}
        for item in entries:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or "").strip()
            summary = str(item.get("summary") or "").strip()
            if title and summary:
                result[title] = summary

        return result
