"""FastAPI application for the multi-theme recommendation service."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings, setup_logging
from src.models.recommendation import RecommendationRequest, RecommendationResponse
from src.services.recommendation_service import (
    SUPPORTED_THEMES,
    RecommendationService,
)

logger = logging.getLogger(__name__)


def _validate_configuration() -> None:
    """Validate configuration at startup.

    Raises:
        ValueError: If configuration is invalid
        FileNotFoundError: If required prompt files are missing
    """
    from pathlib import Path

    # Validate OpenAI API key
    if not settings.openai_api_key or settings.openai_api_key == "test-key-placeholder":
        raise ValueError(
            "OPENAI_API_KEY must be set in .env file. "
            "Please copy .env.example to .env and configure your API key."
        )

    logger.info("Configuration validated: API key is set")

    # Validate prompt files exist for all themes
    prompts_dir = Path(__file__).resolve().parent / "prompts"
    missing_prompts = []

    for theme in SUPPORTED_THEMES:
        for role in ["selector", "extractor", "insight", "assembler"]:
            prompt_path = prompts_dir / theme / f"{role}.txt"
            if not prompt_path.exists():
                missing_prompts.append(str(prompt_path))

    if missing_prompts:
        raise FileNotFoundError(
            "Missing prompt files:\n" + "\n".join(f"  - {p}" for p in missing_prompts)
        )

    logger.info("Prompt files validated: all %d files present", len(SUPPORTED_THEMES) * 4)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    setup_logging(settings.log_level)
    logger.info("Starting Multi-Theme Recommendation Service")

    # Validate configuration
    try:
        _validate_configuration()
    except (ValueError, FileNotFoundError) as exc:
        logger.error("Configuration validation failed: %s", exc)
        raise

    logger.info(f"Using model: {settings.openai_model}")
    logger.info(f"API base: {settings.openai_api_base}")
    logger.info(f"Workflow timeout: {settings.workflow_timeout}s")
    logger.info(f"Supported themes: {', '.join(SUPPORTED_THEMES)}")

    yield

    # Shutdown
    logger.info("Shutting down Multi-Theme Recommendation Service")


app = FastAPI(
    title="Multi-Theme Recommendation API",
    description="Multi-agent recommendation system using LangChain",
    version="0.2.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
recommendation_service = RecommendationService()


@app.get("/")
async def root() -> dict[str, object]:
    """Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "Multi-Theme Recommendation API",
        "docs": "/docs",
        "health": "/health",
        "themes": list(SUPPORTED_THEMES),
        "endpoints": {
            theme: f"/api/{theme}/recommend" for theme in SUPPORTED_THEMES
        },
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}


async def _generate_recommendation(
    theme: str, request: RecommendationRequest
) -> RecommendationResponse:

    if theme not in SUPPORTED_THEMES:
        raise HTTPException(status_code=404, detail=f"Unsupported theme: {theme}")

    try:
        return await recommendation_service.get_recommendations(
            theme,  # type: ignore[arg-type]
            request,
        )
    except TimeoutError as exc:
        logger.error(
            "Request timeout: request_id=%s, theme=%s", request.request_id, theme
        )
        raise HTTPException(
            status_code=504,
            detail=f"Request timeout after {settings.workflow_timeout}s",
        ) from exc
    except ValueError as exc:
        logger.error("Validation error while generating recommendations: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to generate recommendations: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Recommendation generation failed") from exc


@app.post("/api/books/recommend", response_model=RecommendationResponse)
async def recommend_books(request: RecommendationRequest) -> RecommendationResponse:
    """Recommendation endpoint for books theme."""
    return await _generate_recommendation("books", request)


@app.post("/api/games/recommend", response_model=RecommendationResponse)
async def recommend_games(request: RecommendationRequest) -> RecommendationResponse:
    """Recommendation endpoint for games theme."""
    return await _generate_recommendation("games", request)


@app.post("/api/movies/recommend", response_model=RecommendationResponse)
async def recommend_movies(request: RecommendationRequest) -> RecommendationResponse:
    """Recommendation endpoint for movies theme."""
    return await _generate_recommendation("movies", request)


@app.post("/api/anime/recommend", response_model=RecommendationResponse)
async def recommend_anime(request: RecommendationRequest) -> RecommendationResponse:
    """Recommendation endpoint for anime theme."""
    return await _generate_recommendation("anime", request)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Format HTTP exceptions into a standard JSON schema."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_error",
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": request.url.path,
            }
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "server_error",
                "message": "Internal server error",
                "status_code": 500,
                "path": request.url.path,
            }
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
