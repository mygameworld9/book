# API 使用手册

## 目录

1. [API 概述](#api-概述)
2. [认证和配置](#认证和配置)
3. [API 端点详解](#api-端点详解)
4. [请求和响应示例](#请求和响应示例)
5. [错误处理](#错误处理)
6. [客户端集成示例](#客户端集成示例)
7. [性能优化建议](#性能优化建议)

---

## API 概述

### 基础信息

- **Base URL**: `http://localhost:8000` (开发环境)
- **Protocol**: HTTP/HTTPS
- **Content-Type**: `application/json`
- **API Version**: v1

### 可用端点一览

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 根端点，返回API信息 |
| `/health` | GET | 健康检查 |
| `/docs` | GET | Swagger UI 交互式文档 |
| `/redoc` | GET | ReDoc API 文档 |
| `/api/books/recommend` | POST | 生成书籍推荐 |
| `/api/games/recommend` | POST | 生成游戏推荐 |
| `/api/movies/recommend` | POST | 生成电影推荐 |
| `/api/anime/recommend` | POST | 生成动漫推荐 |

---

## 认证和配置

### 环境变量配置

API 使用环境变量进行配置，无需客户端认证。服务端需要配置：

```bash
# .env 文件
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

### CORS 配置

API 默认允许所有来源的跨域请求（开发环境）。生产环境应该配置具体的允许来源：

```python
# src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # 生产环境配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## API 端点详解

### 1. 根端点

**端点**: `GET /`

**描述**: 返回 API 基本信息和文档链接

**请求**:
```bash
curl http://localhost:8000/
```

**响应**:
```json
{
    "message": "Multi-Theme Recommendation API",
    "docs": "/docs",
    "health": "/health",
    "themes": ["books", "games", "movies", "anime"],
    "endpoints": {
        "books": "/api/books/recommend",
        "games": "/api/games/recommend",
        "movies": "/api/movies/recommend",
        "anime": "/api/anime/recommend"
    }
}
```

**状态码**: `200 OK`

---

### 2. 健康检查

**端点**: `GET /health`

**描述**: 检查服务是否正常运行

**请求**:
```bash
curl http://localhost:8000/health
```

**响应**:
```json
{
    "status": "healthy"
}
```

**状态码**: `200 OK`

**用途**:
- 监控系统使用
- 容器健康检查
- 负载均衡器健康探测

---

### 3. 获取多主题推荐（核心 API）

**端点**: `POST /api/{theme}/recommend`

`{theme}` 可选值：`books`、`games`、`movies`、`anime`

**描述**: 根据用户需求生成对应主题的个性化推荐

#### 请求参数

**Content-Type**: `application/json`

**请求体结构**:

```json
{
    "user_message": "string (必填)",
    "conversation_history": [
        {
            "role": "string",
            "content": "string"
        }
    ]
}
```

**字段说明**:

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `user_message` | string | ✅ | 用户的当前消息，描述阅读需求 |
| `conversation_history` | array | ❌ | 对话历史记录（可选） |
| `conversation_history[].role` | string | - | 消息角色：`user` 或 `assistant` |
| `conversation_history[].content` | string | - | 消息内容 |

#### 响应结构

**成功响应** (200 OK):

```json
{
    "user_profile": {
        "genre": "string",
        "style": "string",
        "mood": "string",
        "previous_books": ["string"],
        "reading_goal": "string"
    },
    "recommended_books": [
        {
            "title": "string",
            "author": "string",
            "isbn": "string | null",
            "book_id": "string | null",
            "summary": "string (50-80字)",
            "recommendation_reason": "string (30-50字)"
        }
    ],
    "message": "string"
}
```

**字段说明**:

| 字段 | 类型 | 描述 |
|------|------|------|
| `user_profile` | object | 用户阅读画像 |
| `user_profile.genre` | string | 偏好类型（如：科幻、文学、历史） |
| `user_profile.style` | string | 阅读风格（如：硬核、轻松、深度） |
| `user_profile.mood` | string | 当前心情（如：渴望挑战、放松） |
| `user_profile.previous_books` | array | 已读书籍列表 |
| `user_profile.reading_goal` | string | 阅读目的 |
| `recommended_books` | array | 推荐书籍列表（2-3本） |
| `recommended_books[].title` | string | 书名 |
| `recommended_books[].author` | string | 作者 |
| `recommended_books[].isbn` | string\|null | ISBN 编号 |
| `recommended_books[].summary` | string | 书籍摘要（50-80字） |
| `recommended_books[].recommendation_reason` | string | 推荐理由（30-50字） |
| `message` | string | 给用户的友好消息 |

---

## 请求和响应示例

### 示例 1: 基础推荐请求

**场景**: 用户想读科幻小说

**请求**:
```bash
curl -X POST http://localhost:8000/api/books/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "我想读一些科幻小说，最近读完了《三体》，想找类似风格的作品",
    "conversation_history": []
  }'
```

**响应**:
```json
{
    "user_profile": {
        "genre": "科幻",
        "style": "硬核",
        "mood": "探索未知",
        "previous_books": ["三体"],
        "reading_goal": "寻找类似《三体》的硬核科幻作品"
    },
    "recommended_books": [
        {
            "title": "沙丘",
            "author": "弗兰克·赫伯特",
            "isbn": "978-7-5321-5614-4",
            "book_id": null,
            "summary": "宏大的星际史诗，讲述沙漠星球上的权力斗争、宗教预言与人类进化。香料是宇宙中最珍贵的资源，控制香料就控制了宇宙。",
            "recommendation_reason": "与《三体》一样具有深厚的科学基础和哲学思考，世界观构建宏大，是硬核科幻的经典之作。"
        },
        {
            "title": "基地",
            "author": "艾萨克·阿西莫夫",
            "isbn": "978-7-5366-8670-0",
            "book_id": null,
            "summary": "银河帝国衰落之际，心理史学家预见文明将陷入三万年黑暗。为缩短黑暗期，他建立两个基地以保存人类知识。",
            "recommendation_reason": "运用数学和心理学推演人类文明进程，思想深度不亚于《三体》，是科幻文学的里程碑。"
        },
        {
            "title": "神经漫游者",
            "author": "威廉·吉布森",
            "isbn": "978-7-5596-2642-3",
            "book_id": null,
            "summary": "赛博朋克开山之作，黑客凯斯在虚拟现实中执行危险任务，探索人工智能、意识上传和数字世界的边界。",
            "recommendation_reason": "开创赛博朋克流派，对未来科技的预见性堪比《三体》，融合哲学、技术与人性思考。"
        }
    ],
    "message": "基于您对科幻类书籍的偏好，以及探索未知的心情，我们为您精选了 3 本书。这些书籍都符合您寻找类似《三体》的硬核科幻作品的阅读目标。您更倾向于哪一本？我们随时可以为您提供更多延伸信息。"
}
```

---

### 示例 2: 带对话历史的请求

**场景**: 多轮对话，用户缩小范围

**请求**:
```bash
curl -X POST http://localhost:8000/api/books/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "我更喜欢轻松一点的，不要太硬核",
    "conversation_history": [
        {
            "role": "user",
            "content": "推荐一些科幻小说"
        },
        {
            "role": "assistant",
            "content": "您好！我可以为您推荐科幻小说。请问您更偏好哪种风格？硬核科幻还是软科幻？"
        }
    ]
  }'
```

**响应**:
```json
{
    "user_profile": {
        "genre": "科幻",
        "style": "轻松",
        "mood": "放松娱乐",
        "previous_books": [],
        "reading_goal": "轻松阅读，不要太烧脑"
    },
    "recommended_books": [
        {
            "title": "银河系漫游指南",
            "author": "道格拉斯·亚当斯",
            "isbn": "978-7-5442-5866-2",
            "book_id": null,
            "summary": "地球被毁前最后一刻，阿瑟搭上外星人的便车，开始荒诞搞笑的星际冒险。充满英式幽默和奇思妙想。",
            "recommendation_reason": "幽默轻松，不需要烧脑，却能让你捧腹大笑的同时思考宇宙的意义。完美的轻科幻入门作品。"
        },
        {
            "title": "火星救援",
            "author": "安迪·威尔",
            "isbn": "978-7-5596-0361-5",
            "book_id": null,
            "summary": "宇航员马克被困火星，运用科学知识和乐观精神自救。故事节奏明快，充满幽默和紧张感。",
            "recommendation_reason": "轻松幽默的语言，科学知识深入浅出，读起来像看美剧一样轻松愉快，不会感到负担。"
        }
    ],
    "message": "基于您对科幻类书籍的偏好，以及放松娱乐的心情，我们为您精选了 2 本书。这些书籍都符合您轻松阅读，不要太烧脑的阅读目标。您更倾向于哪一本？我们随时可以为您提供更多延伸信息。"
}
```

---

### 示例 3: Python 客户端

```python
import requests
import json

class BookRecommendationClient:
    """图书推荐API客户端"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def check_health(self) -> bool:
        """检查服务健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    def get_recommendations(
        self,
        user_message: str,
        conversation_history: list[dict] = None
    ) -> dict:
        """获取图书推荐

        Args:
            user_message: 用户消息
            conversation_history: 对话历史

        Returns:
            推荐结果

        Raises:
            requests.HTTPError: API请求失败
        """
        payload = {
            "user_message": user_message,
            "conversation_history": conversation_history or []
        }

        response = self.session.post(
            f"{self.base_url}/api/books/recommend",
            json=payload
        )
        response.raise_for_status()

        return response.json()


# 使用示例
if __name__ == "__main__":
    client = BookRecommendationClient()

    # 检查服务状态
    if not client.check_health():
        print("服务不可用")
        exit(1)

    # 获取推荐
    result = client.get_recommendations(
        user_message="我想读一些历史小说，喜欢明清时期的背景"
    )

    # 打印推荐
    print(f"\n用户画像: {result['user_profile']}")
    print(f"\n推荐书籍数量: {len(result['recommended_books'])}")

    for i, book in enumerate(result['recommended_books'], 1):
        print(f"\n{i}. {book['title']} - {book['author']}")
        print(f"   摘要: {book['summary']}")
        print(f"   推荐理由: {book['recommendation_reason']}")

    print(f"\n{result['message']}")
```

---

### 示例 4: JavaScript/TypeScript 客户端

```typescript
// bookRecommendationClient.ts
interface UserProfile {
    genre: string;
    style: string;
    mood: string;
    previous_books: string[];
    reading_goal: string;
}

interface Book {
    title: string;
    author: string;
    isbn: string | null;
    book_id: string | null;
    summary: string;
    recommendation_reason: string;
}

interface RecommendationCard {
    user_profile: UserProfile;
    recommended_books: Book[];
    message: string;
}

interface RecommendationRequest {
    user_message: string;
    conversation_history?: Array<{
        role: string;
        content: string;
    }>;
}

class BookRecommendationClient {
    private baseUrl: string;

    constructor(baseUrl: string = "http://localhost:8000") {
        this.baseUrl = baseUrl;
    }

    async checkHealth(): Promise<boolean> {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            return response.ok;
        } catch (error) {
            console.error("Health check failed:", error);
            return false;
        }
    }

    async getRecommendations(
        request: RecommendationRequest
    ): Promise<RecommendationCard> {
        const response = await fetch(
            `${this.baseUrl}/api/books/recommend`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_message: request.user_message,
                    conversation_history: request.conversation_history || [],
                }),
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`API Error: ${error.detail || response.statusText}`);
        }

        return await response.json();
    }
}

// 使用示例
async function main() {
    const client = new BookRecommendationClient();

    // 检查服务状态
    const isHealthy = await client.checkHealth();
    if (!isHealthy) {
        console.error("服务不可用");
        return;
    }

    // 获取推荐
    try {
        const result = await client.getRecommendations({
            user_message: "我想读一些悬疑推理小说，喜欢阿加莎·克里斯蒂的风格",
        });

        console.log("\n用户画像:", result.user_profile);
        console.log(`\n推荐书籍数量: ${result.recommended_books.length}`);

        result.recommended_books.forEach((book, index) => {
            console.log(`\n${index + 1}. ${book.title} - ${book.author}`);
            console.log(`   摘要: ${book.summary}`);
            console.log(`   推荐理由: ${book.recommendation_reason}`);
        });

        console.log(`\n${result.message}`);
    } catch (error) {
        console.error("获取推荐失败:", error);
    }
}

main();
```

---

### 示例 5: cURL 完整示例

```bash
#!/bin/bash
# test_api.sh

BASE_URL="http://localhost:8000"

echo "=== 1. 健康检查 ==="
curl -s "${BASE_URL}/health" | jq '.'

echo -e "\n=== 2. 获取推荐 ==="
curl -X POST "${BASE_URL}/api/books/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "我想读一些提升个人成长的书籍",
    "conversation_history": []
  }' | jq '.'

echo -e "\n=== 3. 多轮对话示例 ==="
curl -X POST "${BASE_URL}/api/books/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "有没有更偏向心理学方面的？",
    "conversation_history": [
      {
        "role": "user",
        "content": "我想读一些提升个人成长的书籍"
      },
      {
        "role": "assistant",
        "content": "为您推荐了几本个人成长类书籍"
      }
    ]
  }' | jq '.'
```

---

## 错误处理

### 错误响应格式

所有错误响应都遵循统一格式：

```json
{
    "detail": "错误描述信息"
}
```

### HTTP 状态码

| 状态码 | 含义 | 常见原因 |
|--------|------|----------|
| 200 | 成功 | 请求成功处理 |
| 422 | 验证错误 | 请求参数不符合要求 |
| 500 | 服务器错误 | 内部处理错误（如 API 调用失败） |

### 常见错误及解决方案

#### 1. 422 Validation Error

**错误示例**:
```json
{
    "detail": [
        {
            "loc": ["body", "user_message"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

**原因**: 缺少必填字段或字段类型错误

**解决方案**:
- 检查请求体是否包含所有必填字段
- 确认字段类型正确（string, array等）
- 参考 API 文档确认正确的请求格式

#### 2. 500 Internal Server Error

**错误示例**:
```json
{
    "detail": "Failed to generate recommendations: API call failed"
}
```

**可能原因**:
- OpenAI API Key 无效或过期
- API 配额不足
- 网络连接问题
- LLM 服务不可用

**解决方案**:
1. 检查服务器日志获取详细错误信息
2. 验证 OpenAI API Key 是否有效
3. 检查 API 配额和余额
4. 确认网络连接正常

#### 3. 连接超时

**原因**: LLM API 响应时间过长

**解决方案**:
- 增加客户端超时时间（推荐 60-120 秒）
- 检查网络连接质量
- 考虑使用更快的模型

**Python 示例**:
```python
response = requests.post(
    url,
    json=payload,
    timeout=120  # 120秒超时
)
```

---

## 性能优化建议

### 1. 客户端优化

#### 使用连接池
```python
import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20
)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

#### 异步请求
```python
import asyncio
import aiohttp

async def get_recommendations_async(user_message: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/books/recommend",
            json={"user_message": user_message}
        ) as response:
            return await response.json()

# 并发多个请求
results = await asyncio.gather(
    get_recommendations_async("推荐科幻小说"),
    get_recommendations_async("推荐历史书籍"),
)
```

### 2. 请求优化

#### 保持对话历史精简
```python
# 只保留最近 5 轮对话
conversation_history = conversation_history[-10:]  # 5轮 = 10条消息
```

#### 使用适当的超时
```python
# 根据场景设置合理的超时
timeout = 60  # 常规请求
timeout = 120  # 复杂查询
```

### 3. 错误重试策略

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def get_recommendations_with_retry(user_message: str):
    return client.get_recommendations(user_message)
```

### 4. 缓存推荐结果

```python
from functools import lru_cache
import hashlib

def cache_key(user_message: str) -> str:
    """生成缓存键"""
    return hashlib.md5(user_message.encode()).hexdigest()

# 简单内存缓存
recommendations_cache = {}

def get_cached_recommendations(user_message: str):
    key = cache_key(user_message)

    if key in recommendations_cache:
        return recommendations_cache[key]

    result = client.get_recommendations(user_message)
    recommendations_cache[key] = result

    return result
```

---

## 附录

### A. 完整的 OpenAPI Schema

访问 `http://localhost:8000/openapi.json` 获取完整的 OpenAPI 3.0 规范。

### B. Postman Collection

```json
{
    "info": {
        "name": "Multi-Theme Recommendation API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Health Check",
            "request": {
                "method": "GET",
                "url": "{{base_url}}/health"
            }
        },
        {
            "name": "Get Recommendations",
            "request": {
                "method": "POST",
                "url": "{{base_url}}/api/books/recommend",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n  \"user_message\": \"我想读一些科幻小说\",\n  \"conversation_history\": []\n}"
                }
            }
        }
    ],
    "variable": [
        {
            "key": "base_url",
            "value": "http://localhost:8000"
        }
    ]
}
```

### C. 速率限制说明

当前版本暂无速率限制。生产环境建议实现：
- 每 IP 限制：60 请求/分钟
- 每用户限制：100 请求/小时

---

**文档版本**: 1.0.0
**最后更新**: 2025-11-10
**维护者**: Book Recommendation Team
