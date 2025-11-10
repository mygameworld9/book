"""Recommendation service coordinating multi-theme agent workflows."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from src.agents import (
    AssemblerAgent,
    EssenceExtractorAgent,
    InsightProviderAgent,
    SelectorAgent,
)
from src.models.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    ThemeLiteral,
)

logger = logging.getLogger(__name__)
SUPPORTED_THEMES: tuple[ThemeLiteral, ...] = ("books", "games", "movies", "anime")


@dataclass(slots=True)
class AgentBundle:
    """Container for all four agents assigned to a theme."""

    selector: SelectorAgent
    extractor: EssenceExtractorAgent
    insight: InsightProviderAgent
    assembler: AssemblerAgent


class RecommendationService:
    """Service coordinating the multi-agent recommendation workflow."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize the recommendation service with agents per theme."""
        self.agents: dict[ThemeLiteral, AgentBundle] = {}

        for theme in SUPPORTED_THEMES:
            self.agents[theme] = AgentBundle(
                selector=SelectorAgent(
                    theme=theme, api_key=api_key, api_base=api_base, model=model
                ),
                extractor=EssenceExtractorAgent(
                    theme=theme, api_key=api_key, api_base=api_base, model=model
                ),
                insight=InsightProviderAgent(
                    theme=theme, api_key=api_key, api_base=api_base, model=model
                ),
                assembler=AssemblerAgent(
                    theme=theme, api_key=api_key, api_base=api_base, model=model
                ),
            )

        logger.info(
            "RecommendationService initialized with themes: %s",
            ", ".join(SUPPORTED_THEMES),
        )

    async def get_recommendations(
        self, theme: ThemeLiteral, request: RecommendationRequest
    ) -> RecommendationResponse:
        """Process recommendation request through multi-agent workflow.

        Workflow:
        1. Selector: Understand user needs and select candidates
        2. EssenceExtractor & InsightProvider: Generate summaries and reasons (parallel)
        3. Assembler: Integrate all information into final recommendation

        Args:
            theme: Requested recommendation theme
            request: User's recommendation request

        Returns:
            Complete recommendation response
        """
        logger.info("Starting recommendation workflow for theme=%s", theme)
        agents = self.agents.get(theme)
        if not agents:
            raise ValueError(f"Unsupported theme: {theme}")

        user_profile, candidates, selector_message = await agents.selector.process(
            user_message=request.user_input,
            conversation_history=[
                msg.model_dump() for msg in request.conversation_history
            ],
        )

        logger.info(
            "Selector identified %s candidates for user profile", len(candidates)
        )

        summaries_task = agents.extractor.process(candidates)
        reasons_task = agents.insight.process(candidates, user_profile)

        summaries, reasons = await asyncio.gather(summaries_task, reasons_task)

        logger.info("EssenceExtractor and InsightProvider completed for theme=%s", theme)

        recommendation_response = await agents.assembler.process(
            user_profile=user_profile,
            candidates=candidates,
            summaries=summaries,
            reasons=reasons,
            intro_message=selector_message,
        )

        logger.info("Recommendation workflow completed successfully for theme=%s", theme)
        return recommendation_response
