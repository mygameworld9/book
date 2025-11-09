# 📚 Book Recommendation System

Multi-agent book recommendation system built with LangChain, FastAPI, and React.

## ✨ Features

- 🤖 **Multi-Agent AI System**: Four specialized agents working collaboratively
- 💬 **Interactive Chat Interface**: Conversational book recommendation experience
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🎨 **Beautiful UI**: Modern, gradient-styled recommendation cards
- ⚡ **Fast Performance**: Optimized with Vite and React 18
- 🐳 **Docker Ready**: Complete Docker Compose setup for easy deployment

## 🏗️ Architecture

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

### Run Backend

```bash
# Start Redis
docker-compose up -d redis

# Run API server
uv run uvicorn src.main:app --reload
```

Backend will be available at http://localhost:8000

### Run Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

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

### Docker (Recommended)

Start all services (backend, frontend, and Redis) with one command:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Documentation

Once the server is running, visit:
- **Frontend UI**: http://localhost (when using Docker) or http://localhost:3000 (dev mode)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Project Docs**: See `docs/` directory for detailed guides

## Project Structure

```
.
├── src/                 # Backend (FastAPI + LangChain)
│   ├── agents/          # LangChain agent implementations
│   ├── models/          # Pydantic data models
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   └── main.py          # FastAPI application
├── frontend/            # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── test/        # Frontend tests
│   ├── Dockerfile       # Frontend Docker image
│   └── nginx.conf       # Nginx configuration
├── tests/               # Backend tests
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── docs/                # Project documentation
├── scripts/             # Utility scripts
└── docker-compose.yml   # Complete stack orchestration
```

## License

MIT
