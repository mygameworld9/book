"""Base agent class for all recommendation agents."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.config import settings
from src.models.recommendation import ThemeLiteral

logger = logging.getLogger(__name__)
PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class BaseAgent:
    """Abstract base class for all agents in the system."""

    # Class-level prompt cache: (theme, role) -> prompt content
    _prompt_cache: dict[tuple[str, str], str] = {}

    def __init__(
        self,
        *,
        theme: ThemeLiteral,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        """Initialize the agent with LLM configuration.

        Args:
            theme: Current recommendation theme
            api_key: OpenAI API key (defaults to settings)
            api_base: OpenAI API base URL (defaults to settings)
            model: Model name (defaults to settings)
            temperature: Temperature for generation (defaults to settings)
        """
        self.theme = theme
        self.api_key = api_key or settings.openai_api_key
        self.api_base = api_base or settings.openai_api_base
        self.model_name = model or settings.openai_model
        self.temperature = temperature or settings.openai_temperature

        self.llm = self._create_llm()
        logger.info(
            "Initialized %s for theme=%s with model=%s",
            self.__class__.__name__,
            self.theme,
            self.model_name,
        )

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

    def load_prompt(self, role: str) -> str:
        """Load the system prompt for the given role and theme.

        Uses class-level cache to avoid repeated file I/O.

        Args:
            role: Agent role name, e.g., selector, extractor

        Returns:
            Prompt content as string
        """
        cache_key = (self.theme, role)

        # Check cache first
        if cache_key in self._prompt_cache:
            logger.debug("Loading prompt from cache: theme=%s, role=%s", self.theme, role)
            return self._prompt_cache[cache_key]

        # Load from file and cache
        prompt_path = PROMPTS_DIR / self.theme / f"{role}.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt file not found for theme={self.theme}, role={role}"
            )

        prompt_content = prompt_path.read_text(encoding="utf-8")
        self._prompt_cache[cache_key] = prompt_content
        logger.info("Loaded and cached prompt: theme=%s, role=%s", self.theme, role)

        return prompt_content

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
