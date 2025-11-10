# 🚀 5 分钟快速启动（多主题推荐系统）

这份速查表帮助你在 5 分钟内跑通 **书籍 / 游戏 / 电影 / 动漫** 四主题推荐服务，并附带常见脚本。

---

## 0. 前置环境

- ✅ Python 3.11+
- ✅ [uv](https://astral.sh/uv)（Python 依赖管理）
- ✅ Node.js 18+（前端）
- ✅ Docker & Docker Compose（可选，一键启动）
- ✅ 有效的 OpenAI 兼容 API Key

---

## 1. 克隆 & 安装依赖

```bash
git clone https://github.com/mygameworld9/book.git
cd book

# (可选) 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装后端依赖
uv sync --all-extras

# 安装前端依赖
cd frontend
npm install
cd ..
```

---

## 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 OpenAI / Redis / API 端口等配置
```

最小示例：
```env
OPENAI_API_KEY=sk-xxxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
VITE_API_BASE_URL=http://localhost:8001
```

> **提示**：现在 `frontend/vite.config.js` 会自动读取仓库根目录的 `.env` 中所有 `VITE_` 开头的变量，因此只需维护一个 `.env` 文件即可让前后端共享 `VITE_API_BASE_URL`。若仍需要覆盖，可在 `frontend/.env.local` 中重新定义。

---

## 3. 启动服务

### 方式 A：本地开发模式

```bash
# 1. 启动 Redis（后台）
docker-compose up -d redis

# 2. 启动 FastAPI
uv run uvicorn src.main:app --reload
# => http://localhost:8000

# 3. 启动 React 前端
cd frontend
npm run dev
# => http://localhost:3000
```

### 方式 B：Docker 一键启动

```bash
docker-compose up -d
# 前端: http://localhost
# 后端: http://localhost:8000
```

---

## 4. 快速验证

### Swagger

打开 `http://localhost:8000/docs`，针对以下四个端点任选一个：

```
POST /api/books/recommend
POST /api/games/recommend
POST /api/movies/recommend
POST /api/anime/recommend
```

示例请求体（书籍）：

```json
{
  "user_message": "我想读一些硬核科幻小说",
  "conversation_history": []
}
```

### cURL

```bash
curl -X POST http://localhost:8000/api/games/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "推荐 PS5 上剧情深度的动作游戏",
    "conversation_history": []
  }'
```

### 前端界面

访问 `http://localhost:3000`（或 Docker 模式下的 `http://localhost`），通过顶部主题导航切换书籍/游戏/电影/动漫的对话与卡片输出。

---

## 5. 常用脚本

| 操作 | 命令 |
| --- | --- |
| 后端测试 | `uv run pytest` |
| 前端测试 | `cd frontend && npm run test -- --run` |
| 静态检查 | `uv run mypy src` / `uv run ruff check src` |
| 关闭 Docker | `docker-compose down` |

---

## 6. 常见问题

1. **500 错误 / 推荐失败**  
   - 检查 OpenAI API Key / Base / Model 是否正确  
   - 确认网络可访问目标 LLM

2. **端口被占用**  
   - `uv run uvicorn src.main:app --reload --port 8001`

3. **前端请求失败**  
   - 检查 `VITE_API_BASE_URL` 是否指向后端

---

✅ 以上步骤全部执行成功后，你就拥有了一个完整运行的多主题推荐系统。若需了解更细节的 Agent 流程、CI/CD、部署方案，请继续阅读 `docs/PROJECT_OVERVIEW.md` 与 `docs/API_MANUAL.md`。***
