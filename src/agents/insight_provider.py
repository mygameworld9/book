"""The Insight Provider Agent - Personalized recommendation reasoning."""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.recommendation import (
    RecommendationCandidate,
    ThemeLiteral,
    UserProfile,
)

logger = logging.getLogger(__name__)


class InsightProviderAgent(BaseAgent):
    """Theme-aware recommendation reason generator."""

    def __init__(self, *, theme: ThemeLiteral, **kwargs: Any) -> None:
        super().__init__(theme=theme, **kwargs)
        self.system_prompt = self.load_prompt("insight")

    async def process(
        self,
        candidates: list[RecommendationCandidate],
        user_profile: UserProfile,
    ) -> dict[str, str]:
        """Generate personalized recommendation reasons.

        Args:
            candidates: Candidate items
            user_profile: Structured user profile

        Returns:
            Mapping of item title to recommendation reason
        """
        logger.info(
            "InsightProvider processing %s candidates for theme=%s",
            len(candidates),
            self.theme,
        )

        profile_payload = user_profile.model_dump()
        payload = {
            "theme": self.theme,
            "user_profile": profile_payload,
            "candidates": [c.model_dump() for c in candidates],
        }

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(
                content=(
                    "请基于以下用户画像与候选内容，生成30-50字的个性化推荐理由：\n"
                    f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
                    "仅返回JSON数组或包含 reasons 字段的对象，字段名为 "
                    'title 与 recommendation_reason。'
                )
            ),
        ]

        response = await self.llm.ainvoke(messages)
        reasons = self._parse_reasons(response.content)

        if not reasons:
            logger.warning("InsightProvider response empty, using fallback reasons")
            return {
                c.title: "这项推荐与您的偏好高度契合，值得体验。"
                for c in candidates
            }

        logger.info("InsightProvider generated %s recommendation reasons", len(reasons))
        return reasons

    def _parse_reasons(self, content: Any) -> dict[str, str]:
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
            logger.error("Failed to decode insight JSON: %s", exc)
            return {}

        entries: list[dict[str, Any]]
        if isinstance(data, dict) and "reasons" in data:
            entries = data["reasons"]
        elif isinstance(data, list):
            entries = data
        else:
            return {}

        result: dict[str, str] = {}
        for item in entries:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or "").strip()
            reason = (
                item.get("recommendation_reason")
                or item.get("reason")
                or item.get("insight")
            )
            reason_str = str(reason).strip() if reason else ""
            if title and reason_str:
                result[title] = reason_str

        return result
