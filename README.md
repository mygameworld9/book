# Book Recommendation System

Multi-agent book recommendation system built with LangChain and FastAPI.

## Overview

This system uses four specialized AI agents working collaboratively to provide personalized book recommendations:

1. **The Selector (文学向导)** - User interaction and coordination
2. **The Essence Extractor (摘要撰写者)** - Book summary generation
3. **The Insight Provider (图书推荐人)** - Personalized recommendation reasoning
4. **The Assembler (在线图书管理员)** - Information integration and formatting

## Setup

### Prerequisites

- Python 3.11+
- uv (Python package manager)
- Docker & Docker Compose (for Redis)

### Installation

```bash
# Install dependencies
uv sync --all-extras

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
```

### Configuration

Create a `.env` file with the following:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Development

### Run locally

```bash
# Start Redis
docker-compose up -d redis

# Run API server
uv run uvicorn src.main:app --reload
```

### Run tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Type checking
uv run mypy src

# Linting
uv run ruff check src
```

### Docker

```bash
# Start all services
docker-compose up

# Build production image
docker build -t book-recommendation .
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── src/
│   ├── agents/          # LangChain agent implementations
│   ├── models/          # Pydantic data models
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   └── main.py          # FastAPI application
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── frontend/            # React frontend (future)
├── scripts/             # Utility scripts
└── docker-compose.yml   # Development environment
```

## License

MIT
