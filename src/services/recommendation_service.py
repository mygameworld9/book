"""Book recommendation service coordinating all agents."""

import asyncio
import logging

from src.agents import (
    AssemblerAgent,
    EssenceExtractorAgent,
    InsightProviderAgent,
    SelectorAgent,
)
from src.models.recommendation import RecommendationCard, RecommendationRequest

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service coordinating the multi-agent recommendation workflow."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize the recommendation service.

        Args:
            api_key: OpenAI API key
            api_base: OpenAI API base URL
            model: Model name
        """
        self.selector = SelectorAgent(api_key=api_key, api_base=api_base, model=model)
        self.essence_extractor = EssenceExtractorAgent(
            api_key=api_key, api_base=api_base, model=model
        )
        self.insight_provider = InsightProviderAgent(
            api_key=api_key, api_base=api_base, model=model
        )
        self.assembler = AssemblerAgent(
            api_key=api_key, api_base=api_base, model=model
        )

        logger.info("RecommendationService initialized with all agents")

    async def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationCard:
        """Process recommendation request through multi-agent workflow.

        Workflow:
        1. Selector: Understand user needs and select candidates
        2. EssenceExtractor & InsightProvider: Generate summaries and reasons (parallel)
        3. Assembler: Integrate all information into final recommendation

        Args:
            request: User's recommendation request

        Returns:
            Complete recommendation card
        """
        logger.info("Starting recommendation workflow")

        # Step 1: Selector - Understand user and select candidates
        user_profile, candidates, _ = await self.selector.process(
            user_message=request.user_message,
            conversation_history=request.conversation_history,
        )

        logger.info(
            f"Selector identified {len(candidates)} candidates for user profile"
        )

        # Step 2: Run EssenceExtractor and InsightProvider in parallel
        summaries_task = self.essence_extractor.process(candidates)
        reasons_task = self.insight_provider.process(candidates, user_profile)

        summaries, reasons = await asyncio.gather(summaries_task, reasons_task)

        logger.info("EssenceExtractor and InsightProvider completed")

        # Step 3: Assembler - Integrate all information
        recommendation_card = await self.assembler.process(
            user_profile=user_profile,
            candidates=candidates,
            summaries=summaries,
            reasons=reasons,
        )

        logger.info("Recommendation workflow completed successfully")
        return recommendation_card
