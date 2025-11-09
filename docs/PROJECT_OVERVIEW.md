# 项目全面指南

## 目录

1. [项目概述](#项目概述)
2. [系统架构](#系统架构)
3. [核心概念](#核心概念)
4. [快速开始](#快速开始)
5. [开发指南](#开发指南)
6. [部署指南](#部署指南)
7. [故障排查](#故障排查)

---

## 项目概述

### 项目简介

这是一个基于 LangChain 的**多Agent图书推荐系统**，通过四个专业化的 AI Agent 协同工作，为用户提供个性化的图书推荐。

### 核心特性

- **多Agent协作**：四个专业化Agent分工明确，协同完成推荐任务
- **个性化推荐**：基于用户画像生成定制化的推荐理由
- **类型安全**：使用 Pydantic 进行严格的数据验证和类型检查
- **生产就绪**：包含完整的测试、CI/CD、Docker 部署方案
- **OpenAI兼容**：支持任何 OpenAI 兼容的 API 接口

### 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| **语言** | Python 3.11+ | 主要开发语言 |
| **包管理** | uv | 快速的 Python 包管理器 |
| **Web框架** | FastAPI | REST API 服务 |
| **AI框架** | LangChain | 多Agent编排 |
| **数据验证** | Pydantic | 数据模型和验证 |
| **缓存** | Redis | 会话缓存（可选） |
| **测试** | Pytest | 单元和集成测试 |
| **类型检查** | MyPy | 静态类型检查 |
| **代码质量** | Ruff | Linting 和格式化 |
| **容器化** | Docker & Docker Compose | 开发和部署 |
| **CI/CD** | GitHub Actions | 自动化测试和构建 |

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户请求                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                     (src/main.py)                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              RecommendationService                           │
│           (src/services/recommendation_service.py)           │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Selector   │  │  Essence    │  │  Insight    │         │
│  │   Agent     │  │  Extractor  │  │  Provider   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│                    ┌─────────────┐                           │
│                    │  Assembler  │                           │
│                    │    Agent    │                           │
│                    └─────────────┘                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangChain + OpenAI API                      │
└─────────────────────────────────────────────────────────────┘
```

### 目录结构详解

```
book/
├── src/                          # 源代码目录
│   ├── agents/                   # Agent 实现
│   │   ├── __init__.py          # Agent 导出
│   │   ├── base.py              # Agent 基类
│   │   ├── selector.py          # 文学向导（Selector）
│   │   ├── essence_extractor.py # 摘要撰写者（EssenceExtractor）
│   │   ├── insight_provider.py  # 图书推荐人（InsightProvider）
│   │   └── assembler.py         # 在线图书管理员（Assembler）
│   │
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   ├── book.py              # 书籍相关模型
│   │   └── recommendation.py    # 推荐请求/响应模型
│   │
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   └── recommendation_service.py  # 推荐服务编排
│   │
│   ├── utils/                    # 工具函数
│   │   └── __init__.py
│   │
│   ├── config.py                 # 配置管理
│   └── main.py                   # FastAPI 应用入口
│
├── tests/                        # 测试代码
│   ├── unit/                     # 单元测试
│   │   └── test_models.py       # 数据模型测试
│   ├── integration/              # 集成测试
│   │   └── test_api.py          # API 端点测试
│   └── conftest.py              # Pytest 配置和 fixtures
│
├── scripts/                      # 实用脚本
│   ├── setup.sh                 # 项目初始化脚本
│   ├── run_dev.sh               # 开发服务器启动脚本
│   └── run_tests.sh             # 测试运行脚本
│
├── .github/                      # GitHub 配置
│   └── workflows/
│       └── ci.yml               # CI/CD 工作流
│
├── docs/                         # 项目文档（本目录）
│
├── .env.example                  # 环境变量模板
├── .gitignore                   # Git 忽略配置
├── CLAUDE.md                    # Claude Code 指南
├── README.md                    # 项目README
├── pyproject.toml               # 项目配置和依赖
├── uv.lock                      # 依赖锁定文件
├── Dockerfile                   # Docker 镜像配置
└── docker-compose.yml           # Docker Compose 配置
```

---

## 核心概念

### 1. 四个Agent的角色

#### Selector (文学向导)
- **职责**：用户交互的入口，理解用户需求
- **输入**：用户消息、对话历史
- **输出**：用户画像 + 2-3本候选书籍
- **文件**：`src/agents/selector.py`

**工作流程**：
1. 通过提问深入了解用户偏好
2. 生成结构化的用户画像（类型、风格、心情、阅读目的）
3. 从"内部数据库"筛选候选书目
4. 分发任务给其他Agent

#### EssenceExtractor (摘要撰写者)
- **职责**：生成客观、精练的书籍摘要
- **输入**：候选书目列表
- **输出**：每本书的50-80字摘要
- **文件**：`src/agents/essence_extractor.py`

**特点**：
- 客观、不剧透
- 突出核心主题和价值
- 提炼书籍精髓

#### InsightProvider (图书推荐人)
- **职责**：生成个性化推荐理由
- **输入**：候选书目 + 用户画像
- **输出**：每本书的30-50字推荐理由
- **文件**：`src/agents/insight_provider.py`

**特点**：
- 主观、有感染力
- 将书籍特点与用户需求匹配
- 说明"为什么你应该读它"

#### Assembler (在线图书管理员)
- **职责**：整合所有信息，生成最终推荐
- **输入**：用户画像 + 候选书目 + 摘要 + 推荐理由
- **输出**：完整的推荐卡片
- **文件**：`src/agents/assembler.py`

**特点**：
- 验证数据完整性
- 标准化格式
- 生成友好的交付消息

### 2. 数据流程

```
用户请求
    │
    ▼
┌─────────────────────┐
│  Selector Agent     │  生成用户画像
│  (文学向导)          │  筛选候选书目
└──────────┬──────────┘
           │
           ├─────────────┬─────────────┐
           ▼             ▼             │
  ┌──────────────┐  ┌──────────────┐  │
  │ Essence      │  │ Insight      │  │ 并行执行
  │ Extractor    │  │ Provider     │  │
  └──────┬───────┘  └──────┬───────┘  │
         │                 │           │
         └────────┬────────┘           │
                  ▼                    │
         ┌──────────────┐              │
         │  Assembler   │  整合信息    │
         │  Agent       │  生成推荐卡片│
         └──────┬───────┘              │
                │                      │
                ▼                      │
          返回给用户  ◄─────────────────┘
```

### 3. 数据模型

#### UserProfile (用户画像)
```python
{
    "genre": "科幻",              # 偏好类型
    "style": "硬核",              # 阅读风格
    "mood": "渴望挑战",           # 当前心情
    "previous_books": ["三体"],   # 已读书籍
    "reading_goal": "扩展视野"    # 阅读目的
}
```

#### BookCandidate (候选书目)
```python
{
    "title": "沙丘",
    "author": "弗兰克·赫伯特",
    "isbn": "978-7-5321-5614-4",
    "book_id": "optional"
}
```

#### Book (完整书籍信息)
```python
{
    "title": "沙丘",
    "author": "弗兰克·赫伯特",
    "isbn": "978-7-5321-5614-4",
    "summary": "沙漠星球上的权力斗争与人类进化的史诗...",  # 50-80字
    "recommendation_reason": "复杂的世界观和深刻的哲学思考..."  # 30-50字
}
```

#### RecommendationCard (推荐卡片)
```python
{
    "user_profile": { ... },           # 用户画像
    "recommended_books": [ ... ],      # 2-3本推荐书籍
    "message": "为您精选了..."         # 友好消息
}
```

---

## 快速开始

### 前置要求

- Python 3.11 或更高版本
- uv (Python 包管理器)
- Docker 和 Docker Compose (可选，用于 Redis)
- OpenAI API Key 或兼容的 API

### 安装步骤

#### 1. 克隆仓库
```bash
git clone https://github.com/mygameworld9/book.git
cd book
```

#### 2. 安装依赖
```bash
# 安装 uv (如果还没安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync --all-extras
```

#### 3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# 必须配置：OPENAI_API_KEY
nano .env
```

**.env 配置说明**：
```bash
# OpenAI API 配置
OPENAI_API_KEY=sk-xxx              # 必填：你的 API Key
OPENAI_API_BASE=https://api.openai.com/v1  # API 基础URL
OPENAI_MODEL=gpt-4                 # 使用的模型
OPENAI_TEMPERATURE=0.7             # 生成温度 (0-1)

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API 配置
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

#### 4. 启动 Redis (可选)
```bash
docker-compose up -d redis
```

#### 5. 运行开发服务器
```bash
uv run uvicorn src.main:app --reload
```

服务器将在 `http://localhost:8000` 启动。

#### 6. 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 验证安装

```bash
# 健康检查
curl http://localhost:8000/health

# 运行测试
uv run pytest -v

# 类型检查
uv run mypy src

# 代码质量检查
uv run ruff check src
```

---

## 开发指南

### 开发环境设置

#### 推荐的 IDE 配置

**VS Code 扩展**：
- Python
- Pylance
- Ruff
- Even Better TOML

**.vscode/settings.json** (推荐配置):
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "ruff.path": ["${workspaceFolder}/.venv/bin/ruff"]
}
```

### 添加新功能

#### 1. 创建新的 Agent

如果需要添加新的 Agent，遵循以下步骤：

**步骤 1：创建 Agent 类**
```python
# src/agents/my_new_agent.py
from src.agents.base import BaseAgent

class MyNewAgent(BaseAgent):
    """新Agent的描述"""

    SYSTEM_PROMPT = """
    你是一个...
    """

    async def process(self, input_data: InputType) -> OutputType:
        """处理逻辑

        Args:
            input_data: 输入数据

        Returns:
            输出数据
        """
        # 实现你的逻辑
        messages = [...]
        response = await self.llm.ainvoke(messages)
        return processed_result
```

**步骤 2：在 `__init__.py` 中导出**
```python
# src/agents/__init__.py
from src.agents.my_new_agent import MyNewAgent

__all__ = [..., "MyNewAgent"]
```

**步骤 3：在 Service 中使用**
```python
# src/services/recommendation_service.py
class RecommendationService:
    def __init__(self, ...):
        ...
        self.my_new_agent = MyNewAgent(...)
```

#### 2. 添加新的数据模型

**步骤 1：定义 Pydantic 模型**
```python
# src/models/new_model.py
from pydantic import BaseModel, Field

class NewModel(BaseModel):
    """模型描述"""

    field_name: str = Field(..., description="字段描述")
    optional_field: int | None = Field(None, description="可选字段")
```

**步骤 2：编写测试**
```python
# tests/unit/test_new_model.py
from src.models.new_model import NewModel

def test_valid_model():
    model = NewModel(field_name="test")
    assert model.field_name == "test"
```

#### 3. 添加新的 API 端点

**在 `src/main.py` 中添加**：
```python
@app.post("/api/v1/new-endpoint", response_model=ResponseModel)
async def new_endpoint(request: RequestModel) -> ResponseModel:
    """端点描述

    Args:
        request: 请求数据

    Returns:
        响应数据

    Raises:
        HTTPException: 错误情况
    """
    try:
        result = await some_service.process(request)
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

### 测试指南

#### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/unit/test_models.py

# 运行特定测试函数
uv run pytest tests/unit/test_models.py::test_valid_user_profile

# 带覆盖率报告
uv run pytest --cov=src --cov-report=html

# 详细输出
uv run pytest -v -s
```

#### 编写测试

**单元测试示例**：
```python
# tests/unit/test_my_feature.py
import pytest
from src.models.book import Book

class TestBook:
    def test_valid_book(self):
        book = Book(
            title="测试书籍",
            author="测试作者",
            summary="摘要",
            recommendation_reason="推荐理由"
        )
        assert book.title == "测试书籍"

    def test_invalid_book(self):
        with pytest.raises(ValidationError):
            Book(title="测试")  # 缺少必填字段
```

**集成测试示例**：
```python
# tests/integration/test_my_api.py
from fastapi.testclient import TestClient

def test_my_endpoint(client: TestClient):
    response = client.post("/api/v1/endpoint", json={...})
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

### 代码质量

#### 类型检查
```bash
# 检查整个项目
uv run mypy src

# 检查特定文件
uv run mypy src/agents/selector.py
```

#### Linting 和格式化
```bash
# 检查代码问题
uv run ruff check src tests

# 自动修复可修复的问题
uv run ruff check src tests --fix

# 格式化代码
uv run ruff format src tests
```

### 调试技巧

#### 1. 启用详细日志
```python
# 在 .env 中设置
LOG_LEVEL=DEBUG
```

#### 2. 使用 Python 调试器
```python
import pdb; pdb.set_trace()  # 在代码中设置断点
```

#### 3. 查看 LangChain 调试信息
```python
import langchain
langchain.debug = True
```

---

## 部署指南

### Docker 部署

#### 1. 构建镜像
```bash
docker build -t book-recommendation:latest .
```

#### 2. 运行容器
```bash
docker run -d \
  --name book-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  book-recommendation:latest
```

#### 3. 使用 Docker Compose
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

### 生产环境配置

#### 1. 环境变量
```bash
# 生产环境 .env
OPENAI_API_KEY=<production_key>
OPENAI_API_BASE=<your_api_base>
OPENAI_MODEL=gpt-4
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
REDIS_HOST=redis
```

#### 2. 性能优化

**增加 Worker 数量**：
```dockerfile
# 在 Dockerfile 中
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**配置 Gunicorn**：
```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

#### 3. 监控和日志

**日志收集**：
- 使用结构化日志（已实现）
- 集成 ELK Stack 或类似工具
- 配置日志轮转

**健康检查**：
```bash
# 应用内置健康检查端点
curl http://localhost:8000/health
```

---

## 故障排查

### 常见问题

#### 1. OpenAI API 错误

**问题**：`openai.AuthenticationError`
```
Solution:
- 检查 OPENAI_API_KEY 是否正确
- 确认 API key 有足够的配额
- 检查 OPENAI_API_BASE 配置
```

#### 2. 依赖安装失败

**问题**：`uv sync` 失败
```bash
Solution:
# 清理缓存
rm -rf .venv
rm uv.lock

# 重新安装
uv sync --all-extras
```

#### 3. 测试失败

**问题**：测试无法通过
```bash
Solution:
# 检查环境变量
cat .env

# 运行单个测试查看详细错误
uv run pytest tests/unit/test_models.py -v -s

# 检查 Python 版本
python --version  # 需要 3.11+
```

#### 4. Docker 构建失败

**问题**：Docker 镜像构建失败
```bash
Solution:
# 清理 Docker 缓存
docker system prune -a

# 使用 --no-cache 重新构建
docker build --no-cache -t book-recommendation .
```

#### 5. Redis 连接失败

**问题**：无法连接到 Redis
```bash
Solution:
# 检查 Redis 是否运行
docker-compose ps

# 启动 Redis
docker-compose up -d redis

# 检查连接
redis-cli ping
```

### 获取帮助

- **GitHub Issues**: https://github.com/mygameworld9/book/issues
- **文档**: 查看 `docs/` 目录下的其他文档
- **日志**: 检查应用日志获取详细错误信息

```bash
# 查看应用日志
docker-compose logs -f backend

# 实时监控日志
tail -f logs/app.log
```

---

## 下一步

- 阅读 [API使用手册](./API_MANUAL.md) 了解详细的API使用方法
- 阅读 [Agent工作原理](./AGENT_DETAILS.md) 深入了解Agent实现
- 查看 [贡献指南](./CONTRIBUTING.md) 学习如何贡献代码

---

**最后更新**: 2025-11-10
**版本**: 0.1.0
