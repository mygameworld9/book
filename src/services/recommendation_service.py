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
from src.config import settings
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
        """Initialize the recommendation service with lazy-loaded agents.

        Agents are created on-demand for better resource utilization.
        """
        self.agents: dict[ThemeLiteral, AgentBundle | None] = dict.fromkeys(SUPPORTED_THEMES)
        self._api_key = api_key
        self._api_base = api_base
        self._model = model

        logger.info(
            "RecommendationService initialized (lazy-load mode) for themes: %s",
            ", ".join(SUPPORTED_THEMES),
        )

    def _get_or_create_agents(self, theme: ThemeLiteral) -> AgentBundle:
        """Get existing agents or create new ones for the given theme.

        Args:
            theme: Theme to get/create agents for

        Returns:
            AgentBundle for the theme
        """
        if self.agents[theme] is None:
            logger.info("Creating agents for theme=%s (first use)", theme)
            self.agents[theme] = AgentBundle(
                selector=SelectorAgent(
                    theme=theme,
                    api_key=self._api_key,
                    api_base=self._api_base,
                    model=self._model,
                ),
                extractor=EssenceExtractorAgent(
                    theme=theme,
                    api_key=self._api_key,
                    api_base=self._api_base,
                    model=self._model,
                ),
                insight=InsightProviderAgent(
                    theme=theme,
                    api_key=self._api_key,
                    api_base=self._api_base,
                    model=self._model,
                ),
                assembler=AssemblerAgent(
                    theme=theme,
                    api_key=self._api_key,
                    api_base=self._api_base,
                    model=self._model,
                ),
            )
        return self.agents[theme]  # type: ignore[return-value]

    async def _process_workflow(
        self, theme: ThemeLiteral, request: RecommendationRequest
    ) -> RecommendationResponse:
        """Internal method to process the recommendation workflow.

        Args:
            theme: Requested recommendation theme
            request: User's recommendation request

        Returns:
            Complete recommendation response
        """
        if theme not in SUPPORTED_THEMES:
            raise ValueError(f"Unsupported theme: {theme}")

        agents = self._get_or_create_agents(theme)

        user_profile, candidates, selector_message = await agents.selector.process(
            user_message=request.user_input,
            conversation_history=[
                msg.model_dump() for msg in request.conversation_history
            ],
        )

        logger.info(
            "Selector completed: request_id=%s, candidates=%s",
            request.request_id,
            len(candidates),
        )

        summaries_task = agents.extractor.process(candidates)
        reasons_task = agents.insight.process(candidates, user_profile)

        summaries, reasons = await asyncio.gather(summaries_task, reasons_task)

        logger.info(
            "Extractor and Insight completed: request_id=%s, theme=%s",
            request.request_id,
            theme,
        )

        recommendation_response = await agents.assembler.process(
            user_profile=user_profile,
            candidates=candidates,
            summaries=summaries,
            reasons=reasons,
            intro_message=selector_message,
        )

        # Add request_id to response
        recommendation_response.request_id = request.request_id

        return recommendation_response

    async def get_recommendations(
        self, theme: ThemeLiteral, request: RecommendationRequest
    ) -> RecommendationResponse:
        """Process recommendation request through multi-agent workflow with timeout.

        Workflow:
        1. Selector: Understand user needs and select candidates
        2. EssenceExtractor & InsightProvider: Generate summaries and reasons (parallel)
        3. Assembler: Integrate all information into final recommendation

        Args:
            theme: Requested recommendation theme
            request: User's recommendation request

        Returns:
            Complete recommendation response

        Raises:
            asyncio.TimeoutError: If workflow exceeds configured timeout
            ValueError: If theme is not supported
        """
        logger.info(
            "Starting recommendation workflow: request_id=%s, theme=%s, timeout=%ss",
            request.request_id,
            theme,
            settings.workflow_timeout,
        )

        try:
            recommendation_response = await asyncio.wait_for(
                self._process_workflow(theme, request),
                timeout=settings.workflow_timeout,
            )

            logger.info(
                "Workflow completed: request_id=%s, theme=%s, recommendations=%s",
                request.request_id,
                theme,
                len(recommendation_response.recommendations),
            )
            return recommendation_response

        except TimeoutError:
            logger.error(
                "Workflow timeout: request_id=%s, theme=%s, timeout=%ss",
                request.request_id,
                theme,
                settings.workflow_timeout,
            )
            raise
