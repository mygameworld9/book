"""FastAPI application for book recommendation service."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings, setup_logging
from src.models.recommendation import RecommendationCard, RecommendationRequest
from src.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


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
    logger.info("Starting Book Recommendation Service")
    logger.info(f"Using model: {settings.openai_model}")
    logger.info(f"API base: {settings.openai_api_base}")

    yield

    # Shutdown
    logger.info("Shutting down Book Recommendation Service")


app = FastAPI(
    title="Book Recommendation API",
    description="Multi-agent book recommendation system using LangChain",
    version="0.1.0",
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
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "Book Recommendation API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}


@app.post("/api/v1/recommendations", response_model=RecommendationCard)
async def get_recommendations(request: RecommendationRequest) -> RecommendationCard:
    """Get book recommendations based on user input.

    This endpoint coordinates multiple AI agents to provide personalized
    book recommendations:
    1. Selector: Understands user needs and selects candidates
    2. EssenceExtractor: Generates book summaries
    3. InsightProvider: Creates personalized recommendation reasons
    4. Assembler: Integrates all information

    Args:
        request: User's recommendation request

    Returns:
        Recommendation card with 2-3 books

    Raises:
        HTTPException: If recommendation generation fails
    """
    try:
        logger.info("Received recommendation request")
        recommendation = await recommendation_service.get_recommendations(request)
        logger.info("Successfully generated recommendations")
        return recommendation

    except Exception as e:
        logger.error(f"Failed to generate recommendations: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}",
        ) from e


@app.exception_handler(Exception)
async def global_exception_handler(request: object, exc: Exception) -> dict[str, str]:
    """Global exception handler for unhandled errors.

    Args:
        request: The request object
        exc: The exception that was raised

    Returns:
        Error response
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {"error": "Internal server error", "detail": str(exc)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
