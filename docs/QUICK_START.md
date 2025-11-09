# 5分钟快速开始

这是一份超快速入门指南，让你在5分钟内运行起图书推荐系统。

## 前置要求

- ✅ Python 3.11+
- ✅ uv (Python包管理器)
- ✅ OpenAI API Key 或兼容的API

## 步骤 1: 克隆项目

```bash
git clone https://github.com/mygameworld9/book.git
cd book
```

## 步骤 2: 安装依赖

```bash
# 安装uv (如果还没安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync --all-extras
```

## 步骤 3: 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的API Key
# 使用任何文本编辑器打开 .env
# 修改这一行：
# OPENAI_API_KEY=your_api_key_here
```

**最小配置示例** (.env):
```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

## 步骤 4: 运行服务

```bash
uv run uvicorn src.main:app --reload
```

看到以下输出表示成功：
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 步骤 5: 测试API

### 方法 1: 浏览器 (推荐)

访问 http://localhost:8000/docs

在Swagger UI中：
1. 找到 `POST /api/v1/recommendations`
2. 点击 "Try it out"
3. 输入请求体：
```json
{
    "user_message": "我想读一些科幻小说",
    "conversation_history": []
}
```
4. 点击 "Execute"
5. 查看响应结果

### 方法 2: cURL

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "我想读一些科幻小说",
    "conversation_history": []
  }'
```

### 方法 3: Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/recommendations",
    json={
        "user_message": "我想读一些科幻小说",
        "conversation_history": []
    }
)

print(response.json())
```

## ✅ 成功！

如果你看到了推荐结果，恭喜！系统已经成功运行。

## 下一步

- 📖 阅读 [完整项目指南](./PROJECT_OVERVIEW.md)
- 🔌 查看 [API使用手册](./API_MANUAL.md)
- 🤖 了解 [Agent工作原理](./AGENT_DETAILS.md)

## 常见问题

### Q: `uv: command not found`

安装uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 重新打开终端
```

### Q: `ValidationError: openai_api_key field required`

确保 `.env` 文件中配置了 `OPENAI_API_KEY`

### Q: API返回 500 错误

检查：
1. API Key是否有效
2. 是否有足够的配额
3. 网络连接是否正常
4. 查看终端日志获取详细错误

### Q: 端口 8000 被占用

使用其他端口：
```bash
uv run uvicorn src.main:app --reload --port 8001
```

---

**遇到其他问题?** 查看 [完整故障排查指南](./PROJECT_OVERVIEW.md#故障排查)
