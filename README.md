# 🌌 Multi-Theme Recommendation System

Multi-agent recommendation platform built with LangChain + FastAPI + React, covering **books, games, movies, and anime**.

## ✨ Features

- 🌗 **4 Themes, 1 Framework**: Books / Games / Movies / Anime share the same four-agent workflow
- 🤖 **Multi-Agent AI System**: Selector · Essence Extractor · Insight Provider · Assembler
- 💬 **Interactive Chat Interface**: Theme-aware prompts, history-aware chat, instant resets
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🎨 **Beautiful UI**: Modern, gradient-styled recommendation cards
- 🔀 **Instant Theme Switching**: Custom navigation without extra dependencies
- ⚡ **Fast Performance**: Optimized with Vite and React 18
- 🐳 **Docker Ready**: Complete Docker Compose setup for easy deployment

## 🏗️ Architecture

Each theme uses the same four collaborating agents with theme-specific prompts loaded from `src/prompts/<theme>/<role>.txt`:

1. **Selector (向导)** – Understands user intent, builds profiles, and picks candidates
2. **Essence Extractor (简介撰写者)** – Generates neutral summaries
3. **Insight Provider (推荐人)** – Creates concise, value-driven reasons
4. **Assembler (管理员)** – Validates completeness and assembles final cards

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

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

> Vite dev/build 过程中会自动读取仓库根目录 `.env` 里的 `VITE_` 变量，因此你只需维护一个 `.env` 文件即可让前后端共享 API 地址。如需前端单独覆盖，可在 `frontend/.env.local` 写入新的 `VITE_API_BASE_URL`。

## Development

### API Endpoints

```
POST /api/books/recommend
POST /api/games/recommend
POST /api/movies/recommend
POST /api/anime/recommend
```

All endpoints accept the unified payload:

```json
{
  "user_message": "...",
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

Response schema:

```json
{
  "theme": "books",
  "user_profile": {
    "theme": "books",
    "summary": "偏好描述",
    "attributes": { "类型": ["科幻"], "心情": "探索" }
  },
  "recommendations": [
    {
      "title": "沙丘",
      "creator": "弗兰克·赫伯特",
      "metadata": {"年份": "1965", "类型": "科幻"},
      "summary": "……",
      "reason": "……"
    }
  ],
  "message": "友好提示"
}
```

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
├── src/                          # Backend (FastAPI + LangChain)
│   ├── agents/                  # Theme-aware agents
│   ├── models/                  # Unified request/response models
│   ├── prompts/{theme}/{role}.txt
│   ├── services/                # Agent orchestration
│   └── main.py                  # FastAPI application + routes
├── frontend/                    # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/          # Theme selector, cards, chat
│   │   ├── hooks/               # useThemeRouting, useRecommendation
│   │   ├── constants/themes.js  # Theme metadata
│   │   └── test/                # RTL + Vitest
│   ├── Dockerfile               # Frontend build
│   └── nginx.conf
├── tests/                       # Backend tests (pytest + httpx)
├── docs/                        # Project documentation
└── docker-compose.yml           # Complete stack orchestration
```

## License

MIT
