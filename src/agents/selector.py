"""The Selector Agent - User interaction and coordination."""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.base import BaseAgent
from src.models.recommendation import RecommendationCandidate, ThemeLiteral, UserProfile

logger = logging.getLogger(__name__)

THEME_LABELS: dict[ThemeLiteral, str] = {
    "books": "书籍",
    "games": "游戏",
    "movies": "电影",
    "anime": "动漫",
}


class SelectorAgent(BaseAgent):
    """Theme-aware selector that orchestrates the first step."""

    def __init__(self, *, theme: ThemeLiteral, **kwargs: Any) -> None:
        super().__init__(theme=theme, **kwargs)
        self.system_prompt = self.load_prompt("selector")

    async def process(
        self,
        user_message: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[UserProfile, list[RecommendationCandidate], str]:
        """Process user message and generate profile with candidates.

        Args:
            user_message: User's current message
            conversation_history: Previous conversation messages

        Returns:
            Tuple of (user_profile, candidates, message_to_user)
        """
        logger.info("Selector processing user message for theme=%s", self.theme)

        messages: list[SystemMessage | HumanMessage] = [
            SystemMessage(content=self.system_prompt)
        ]

        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if not content:
                    continue
                messages.append(
                    HumanMessage(content=f"{role.upper()}:\n{content}")
                )

        messages.append(HumanMessage(content=user_message))
        messages.append(HumanMessage(content=self._structure_prompt()))

        response = await self.llm.ainvoke(messages)
        return self._parse_response(response.content)

    def _structure_prompt(self) -> str:
        label = THEME_LABELS.get(self.theme, "推荐")
        return f"""请针对 {label} 推荐以 JSON 格式回复，严格包含以下字段：
{{
  "user_profile": {{
    "summary": "一句话总结（可选）",
    "attributes": {{
      "标签1": ["值1", "值2"],
      "标签2": "值"
    }}
  }},
  "candidates": [
    {{
      "title": "作品名称",
      "creator": "主要创作者（作者/导演/开发商）",
      "metadata": {{
        "平台或年份等字段": "值"
      }}
    }}
  ],
  "message": "给用户的友好回复"
}}
请勿添加额外文本或解释。"""

    def _parse_response(
        self, content: Any
    ) -> tuple[UserProfile, list[RecommendationCandidate], str]:
        data = self._extract_json(content)
        if not data:
            return self._fallback()

        profile = self._build_user_profile(data.get("user_profile", {}))
        candidates = self._build_candidates(data.get("candidates", []))
        message = str(data.get("message") or self._default_message())

        if not candidates:
            logger.warning(
                "Selector returned no candidates for theme=%s, using fallback defaults",
                self.theme,
            )
            return self._fallback()

        logger.info(
            "Selector generated profile (%s attrs) and %s candidates",
            len(profile.attributes),
            len(candidates),
        )
        return profile, candidates, message

    def _build_user_profile(self, payload: Any) -> UserProfile:
        summary = None
        attributes: dict[str, Any] = {}

        if isinstance(payload, dict):
            summary = payload.get("summary")
            attr_values = payload.get("attributes")
            if isinstance(attr_values, dict):
                attributes = attr_values
            else:
                attributes = {
                    key: value
                    for key, value in payload.items()
                    if key != "summary"
                }

        normalized = {
            str(key): self._normalize_value(value)
            for key, value in attributes.items()
        }
        return UserProfile(theme=self.theme, summary=summary, attributes=normalized)

    def _build_candidates(self, payload: Any) -> list[RecommendationCandidate]:
        if not isinstance(payload, list):
            return []

        candidates: list[RecommendationCandidate] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or "").strip()
            if not title:
                continue

            creator = (
                item.get("creator")
                or item.get("author")
                or item.get("developer")
                or item.get("director")
                or item.get("studio")
                or item.get("producer")
            )
            creator_str = str(creator).strip() if creator else "未知创作者"

            metadata = item.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {
                    key: value
                    for key, value in item.items()
                    if key
                    not in {
                        "title",
                        "creator",
                        "author",
                        "developer",
                        "director",
                        "studio",
                        "producer",
                    }
                }

            normalized_metadata = {
                str(key): self._stringify_metadata_value(value)
                for key, value in metadata.items()
                if value is not None
            }

            candidates.append(
                RecommendationCandidate(
                    title=title,
                    creator=creator_str,
                    metadata=normalized_metadata,
                )
            )

        return candidates[:3]  # 最多返回3个推荐

    def _normalize_value(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self._stringify_metadata_value(v) for v in value if v is not None]
        if isinstance(value, dict):
            return {
                str(key): self._stringify_metadata_value(val)
                for key, val in value.items()
            }
        return self._stringify_metadata_value(value)

    def _stringify_metadata_value(self, value: Any) -> str:
        if isinstance(value, list):
            return "、".join(
                str(item).strip() for item in value if str(item).strip()
            )
        return str(value).strip()

    def _extract_json(self, content: Any) -> dict[str, Any]:
        if not isinstance(content, str):
            return {}

        text = content.strip()
        if "```json" in text:
            text = text.split("```json", maxsplit=1)[1].split("```", maxsplit=1)[0]
        elif "```" in text:
            text = text.split("```", maxsplit=1)[1].split("```", maxsplit=1)[0]

        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as exc:
            logger.error("Failed to decode selector JSON: %s", exc)
        return {}

    def _default_message(self) -> str:
        label = THEME_LABELS.get(self.theme, "内容")
        return f"我已经了解您的偏好，正在为您挑选合适的{label}。"

    def _fallback(self) -> tuple[UserProfile, list[RecommendationCandidate], str]:
        logger.warning("Selector falling back to default data for theme=%s", self.theme)
        profile = UserProfile(
            theme=self.theme,
            summary=self._default_message(),
            attributes={"偏好": ["多样化体验"], "心情": "探索新灵感"},
        )
        candidates = [
            RecommendationCandidate(
                title="默认推荐 A",
                creator="系统推荐",
                metadata={"备注": "等待真实数据"},
            ),
            RecommendationCandidate(
                title="默认推荐 B",
                creator="系统推荐",
                metadata={"备注": "等待真实数据"},
            ),
        ]
        return profile, candidates, self._default_message()
