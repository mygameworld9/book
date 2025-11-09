"""Base agent class for all recommendation agents."""

import logging
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.config import settings

logger = logging.getLogger(__name__)


class BaseAgent:
    """Abstract base class for all agents in the system."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        """Initialize the agent with LLM configuration.

        Args:
            api_key: OpenAI API key (defaults to settings)
            api_base: OpenAI API base URL (defaults to settings)
            model: Model name (defaults to settings)
            temperature: Temperature for generation (defaults to settings)
        """
        self.api_key = api_key or settings.openai_api_key
        self.api_base = api_base or settings.openai_api_base
        self.model_name = model or settings.openai_model
        self.temperature = temperature or settings.openai_temperature

        self.llm = self._create_llm()
        logger.info(f"Initialized {self.__class__.__name__} with model {self.model_name}")

    def _create_llm(self) -> BaseChatModel:
        """Create and configure the LLM instance.

        Returns:
            Configured ChatOpenAI instance
        """
        return ChatOpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
            model=self.model_name,
            temperature=self.temperature,
        )

    async def process(self, *args: Any, **kwargs: Any) -> Any:
        """Process the agent's task.

        This method should be implemented by all concrete agent classes.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Agent-specific output
        """
        raise NotImplementedError("Subclasses must implement process()")
