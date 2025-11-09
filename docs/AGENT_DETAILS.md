# Agent 工作原理详解

## 目录

1. [多Agent架构概述](#多agent架构概述)
2. [BaseAgent 基类](#baseagent-基类)
3. [Selector Agent 详解](#selector-agent-详解)
4. [EssenceExtractor Agent 详解](#essenceextractor-agent-详解)
5. [InsightProvider Agent 详解](#insightprovider-agent-详解)
6. [Assembler Agent 详解](#assembler-agent-详解)
7. [Agent 协作流程](#agent-协作流程)
8. [Prompt Engineering 技巧](#prompt-engineering-技巧)
9. [扩展和自定义](#扩展和自定义)

---

## 多Agent架构概述

### 设计理念

本系统采用**职责分离**的多Agent架构，每个Agent专注于特定任务：

- **专业化**: 每个Agent只做一件事，并把它做好
- **可扩展**: 易于添加新Agent而不影响现有功能
- **可测试**: 每个Agent可以独立测试
- **可维护**: 清晰的职责边界，降低维护成本

### 为什么需要多个Agent？

相比单一Agent，多Agent架构有以下优势：

1. **提高准确性**: 专业化的Prompt能产生更好的结果
2. **并行处理**: EssenceExtractor和InsightProvider可以并行运行
3. **易于调试**: 问题定位更精确
4. **灵活扩展**: 可以轻松替换或升级单个Agent

### 工作流程总览

```
用户输入
    ↓
┌─────────────────────────────────────┐
│  Selector (文学向导)                 │
│  - 理解用户需求                      │
│  - 生成用户画像                      │
│  - 筛选候选书目                      │
└─────────────────────────────────────┘
    ↓ 候选书目 + 用户画像
    ├────────────────┬─────────────────┐
    ↓                ↓                 ↓
┌─────────────┐  ┌─────────────┐      │
│ Essence     │  │ Insight     │      │ 并行执行
│ Extractor   │  │ Provider    │      │
│ (摘要)      │  │ (推荐理由)   │      │
└──────┬──────┘  └──────┬──────┘      │
       │                │             │
       └────────┬───────┘             │
                ↓                     │
       ┌─────────────────┐            │
       │   Assembler     │            │
       │   (整合)        │            │
       └────────┬────────┘            │
                ↓                     │
          最终推荐卡片 ◄────────────────┘
```

---

## BaseAgent 基类

### 源码位置
`src/agents/base.py`

### 类定义

```python
class BaseAgent:
    """所有Agent的抽象基类"""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        """初始化Agent

        Args:
            api_key: OpenAI API key (默认从settings读取)
            api_base: API基础URL (默认从settings读取)
            model: 模型名称 (默认从settings读取)
            temperature: 生成温度 (默认从settings读取)
        """
```

### 核心功能

#### 1. LLM 初始化
```python
def _create_llm(self) -> BaseChatModel:
    """创建LangChain ChatOpenAI实例"""
    return ChatOpenAI(
        api_key=self.api_key,
        base_url=self.api_base,
        model=self.model_name,
        temperature=self.temperature,
    )
```

#### 2. 处理方法接口
```python
async def process(self, *args: Any, **kwargs: Any) -> Any:
    """处理Agent任务的抽象方法

    子类必须实现此方法
    """
    raise NotImplementedError("Subclasses must implement process()")
```

### 使用示例

```python
# 创建Agent实例时可以自定义配置
agent = MyAgent(
    api_key="custom-key",
    api_base="https://custom-api.com/v1",
    model="gpt-4-turbo",
    temperature=0.5
)
```

### 设计考虑

1. **配置灵活性**: 支持全局配置和实例级配置
2. **OpenAI兼容**: 支持任何兼容OpenAI API的服务
3. **类型安全**: 使用类型提示，配合mypy进行检查
4. **日志记录**: 自动记录Agent初始化信息

---

## Selector Agent 详解

### 源码位置
`src/agents/selector.py`

### 角色定位

**文学向导（The Selector）** - 用户交互的前端，负责：
1. 与用户对话，理解阅读需求
2. 生成结构化的用户画像
3. 筛选2-3本候选书目
4. 协调其他Agent的工作

### System Prompt 分析

```python
SYSTEM_PROMPT = """你是一位专业的文学向导，负责与读者对话并理解他们的阅读需求。

你的职责：
1. 通过提问深入了解用户的偏好、阅读历史、当前心情和阅读目的
2. 基于对话生成用户画像标签
3. 从内部数据库筛选出2-3本最匹配的候选书目

提问技巧：
- "您最近读过什么书？最喜欢哪本，为什么？"
- "您现在的心情如何？是想放松、挑战自己还是学习新知识？"
- "您喜欢什么类型的书？科幻、文学、历史还是其他？"
- "您偏好什么样的阅读风格？轻松的、深度的还是硬核的？"

输出格式要求：
返回JSON格式，包含：
1. user_profile: 用户画像对象
2. candidates: 2-3本候选书目列表
3. message: 给用户的友好回复

保持专业、友好的语气，用中文回应。"""
```

**Prompt 设计要点**：
- ✅ 明确角色定位
- ✅ 列出具体职责
- ✅ 提供提问示例
- ✅ 规定输出格式
- ✅ 强调语气和语言

### 处理流程

#### 输入
```python
async def process(
    self,
    user_message: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> tuple[UserProfile, list[BookCandidate], str]:
```

#### 流程步骤

**1. 构建消息列表**
```python
messages: list[SystemMessage | HumanMessage] = [
    SystemMessage(content=self.SYSTEM_PROMPT)
]

# 添加对话历史
if conversation_history:
    for msg in conversation_history:
        messages.append(HumanMessage(content=msg.get("content", "")))

# 添加当前消息
messages.append(HumanMessage(content=user_message))
```

**2. 请求结构化输出**
```python
messages.append(
    HumanMessage(
        content="""请以JSON格式回复，包含以下字段：
{
    "user_profile": {
        "genre": "类型",
        "style": "风格",
        "mood": "心情",
        "previous_books": ["书名1", "书名2"],
        "reading_goal": "阅读目的"
    },
    "candidates": [
        {"title": "书名", "author": "作者", "isbn": "ISBN或null"},
        {"title": "书名", "author": "作者", "isbn": "ISBN或null"}
    ],
    "message": "给用户的友好回复"
}"""
    )
)
```

**3. 调用LLM并解析响应**
```python
response = await self.llm.ainvoke(messages)
content = response.content

# 处理Markdown代码块
if "```json" in content:
    content = content.split("```json")[1].split("```")[0].strip()

data = json.loads(content)

# 创建Pydantic模型
user_profile = UserProfile(**data["user_profile"])
candidates = [BookCandidate(**c) for c in data["candidates"]]
message = data["message"]

return user_profile, candidates, message
```

**4. 错误处理**
```python
except (json.JSONDecodeError, KeyError, ValueError) as e:
    logger.error(f"Failed to parse Selector response: {e}")
    # 返回默认值
    return default_profile, default_candidates, default_message
```

### 工作示例

**输入**:
```python
user_message = "我想读一些科幻小说，最近读完了《三体》"
conversation_history = []
```

**LLM 输出**:
```json
{
    "user_profile": {
        "genre": "科幻",
        "style": "硬核",
        "mood": "渴望挑战",
        "previous_books": ["三体"],
        "reading_goal": "寻找类似三体的硬核科幻"
    },
    "candidates": [
        {
            "title": "沙丘",
            "author": "弗兰克·赫伯特",
            "isbn": "978-7-5321-5614-4"
        },
        {
            "title": "基地",
            "author": "艾萨克·阿西莫夫",
            "isbn": "978-7-5366-8670-0"
        }
    ],
    "message": "基于您对《三体》的喜爱，我为您筛选了两本同样具有宏大世界观和深刻思考的硬核科幻作品。"
}
```

### 优化建议

1. **提高候选书目质量**: 可以集成真实的图书数据库API
2. **记忆管理**: 对于长对话，实现对话摘要机制
3. **多语言支持**: 根据用户语言自动切换输出语言

---

## EssenceExtractor Agent 详解

### 源码位置
`src/agents/essence_extractor.py`

### 角色定位

**摘要撰写者（The Essence Extractor）** - 信息压缩专家，负责：
1. 为每本候选书目生成精炼摘要
2. 识别书籍的核心主题、冲突和人物
3. 保持客观，避免剧透

### System Prompt 分析

```python
SYSTEM_PROMPT = """你是一位专业的摘要撰写者，擅长提炼书籍的核心精髓。

你的职责：
1. 接收候选书目列表
2. 为每本书生成简洁、客观、清晰的摘要
3. 识别书的核心主题、主要冲突和重要人物
4. 避免过度剧透

摘要要求：
- 长度：约50-80字
- 风格：客观、精练
- 重点：核心主题和价值
- 避免：剧透关键情节

输出格式：
返回JSON数组，每本书包含：
{
    "title": "书名",
    "summary": "精髓摘要（50-80字）"
}

使用中文输出。"""
```

**Prompt 特点**：
- 明确字数限制（50-80字）
- 强调客观性
- 规避剧透
- JSON格式输出

### 处理流程

#### 输入
```python
async def process(
    self, candidates: list[BookCandidate]
) -> dict[str, str]:
```

#### 流程步骤

**1. 准备书目列表**
```python
book_list = "\n".join(
    [f"- {c.title} by {c.author}" for c in candidates]
)
```

**2. 构建提示**
```python
messages = [
    SystemMessage(content=self.SYSTEM_PROMPT),
    HumanMessage(
        content=f"""请为以下书籍生成摘要：

{book_list}

以JSON数组格式返回，每个元素包含 title 和 summary 字段。"""
    ),
]
```

**3. 调用LLM并解析**
```python
response = await self.llm.ainvoke(messages)
# 解析JSON
summaries = {item["title"]: item["summary"] for item in data}
return summaries
```

### 工作示例

**输入**:
```python
candidates = [
    BookCandidate(title="沙丘", author="弗兰克·赫伯特"),
    BookCandidate(title="基地", author="艾萨克·阿西莫夫")
]
```

**输出**:
```python
{
    "沙丘": "宏大的星际史诗，讲述沙漠星球上的权力斗争、宗教预言与人类进化。香料是宇宙中最珍贵的资源，控制香料就控制了宇宙。",
    "基地": "银河帝国衰落之际，心理史学家预见文明将陷入三万年黑暗。为缩短黑暗期，他建立两个基地以保存人类知识。"
}
```

### 关键设计

1. **并行执行**: 与InsightProvider并行调用
2. **字典返回**: 使用书名作为key，便于Assembler查找
3. **容错机制**: 解析失败时返回默认摘要

### 优化方向

1. **集成真实书评**: 从豆瓣、Goodreads等获取真实摘要
2. **缓存机制**: 相同书籍的摘要可以缓存
3. **多语言摘要**: 根据书籍原语言生成摘要

---

## InsightProvider Agent 详解

### 源码位置
`src/agents/insight_provider.py`

### 角色定位

**图书推荐人（The Insight Provider）** - 个性化推荐专家，负责：
1. 根据用户画像生成推荐理由
2. 将书籍特点与用户需求匹配
3. 创造具有说服力的"为什么你应该读它"

### System Prompt 分析

```python
SYSTEM_PROMPT = """你是一位见解独到的图书推荐人，专注于生成极具说服力的推荐理由。

你的职责：
1. 接收候选书目和用户画像
2. 将书目特点与用户需求进行关联匹配
3. 为每本书撰写"为什么你应该读它"的理由

推荐理由要求：
- 长度：约30-50字
- 风格：主观、有感染力
- 重点：如何满足用户特定需求
- 价值：解决用户的阅读目的

输出格式：
返回JSON数组，每本书包含：
{
    "title": "书名",
    "recommendation_reason": "推荐理由（30-50字）"
}

使用中文输出，语气要热情且专业。"""
```

**Prompt 特点**：
- 强调主观性和感染力
- 突出个性化匹配
- 较短的字数（30-50字）
- 热情的语气

### 处理流程

#### 输入
```python
async def process(
    self, candidates: list[BookCandidate], user_profile: UserProfile
) -> dict[str, str]:
```

#### 流程步骤

**1. 准备用户画像描述**
```python
profile_str = f"""用户画像：
- 偏好类型：{user_profile.genre}
- 阅读风格：{user_profile.style}
- 当前心情：{user_profile.mood}
- 阅读目的：{user_profile.reading_goal}
- 已读书籍：{', '.join(user_profile.previous_books) if user_profile.previous_books else '无'}"""
```

**2. 构建上下文**
```python
messages = [
    SystemMessage(content=self.SYSTEM_PROMPT),
    HumanMessage(
        content=f"""请根据用户画像，为以下书籍生成个性化推荐理由：

{profile_str}

书籍列表：
{book_list}

以JSON数组格式返回，每个元素包含 title 和 recommendation_reason 字段。"""
    ),
]
```

**3. 生成推荐理由**
```python
response = await self.llm.ainvoke(messages)
reasons = {
    item["title"]: item["recommendation_reason"] for item in data
}
return reasons
```

### 工作示例

**输入**:
```python
user_profile = UserProfile(
    genre="科幻",
    style="硬核",
    mood="渴望挑战",
    previous_books=["三体"],
    reading_goal="扩展科幻阅读视野"
)

candidates = [
    BookCandidate(title="沙丘", author="弗兰克·赫伯特")
]
```

**输出**:
```python
{
    "沙丘": "与《三体》一样具有深厚的科学基础和哲学思考，世界观构建宏大，是硬核科幻的经典之作，能充分满足您的挑战欲望。"
}
```

### 关键特性

1. **个性化**: 基于用户画像定制推荐理由
2. **情感化**: 使用有感染力的语言
3. **目标导向**: 明确说明如何满足用户需求

### 优化方向

1. **A/B测试**: 测试不同风格的推荐理由效果
2. **用户反馈学习**: 根据用户选择调整推荐策略
3. **情感分析**: 更精准地匹配用户情绪状态

---

## Assembler Agent 详解

### 源码位置
`src/agents/assembler.py`

### 角色定位

**在线图书管理员（The Assembler）** - 信息整合者，负责：
1. 验证数据完整性
2. 整合所有Agent的输出
3. 生成标准化的推荐卡片
4. 添加友好的交付消息

### 处理流程

#### 输入
```python
async def process(
    self,
    user_profile: UserProfile,
    candidates: list[BookCandidate],
    summaries: dict[str, str],
    reasons: dict[str, str],
) -> RecommendationCard:
```

#### 流程步骤

**1. 数据完整性检查**
```python
for candidate in candidates:
    title = candidate.title

    if title not in summaries:
        logger.warning(f"Missing summary for {title}")
        summaries[title] = f"这是一本由{candidate.author}撰写的优秀作品。"

    if title not in reasons:
        logger.warning(f"Missing recommendation reason for {title}")
        reasons[title] = "这本书值得您阅读。"
```

**2. 组装完整的Book对象**
```python
books: list[Book] = []
for candidate in candidates:
    book = Book(
        title=candidate.title,
        author=candidate.author,
        isbn=candidate.isbn,
        book_id=candidate.book_id,
        summary=summaries[title],
        recommendation_reason=reasons[title],
    )
    books.append(book)
```

**3. 生成友好消息**
```python
def _generate_message(self, profile: UserProfile, book_count: int) -> str:
    return f"""基于您对{profile.genre}类书籍的偏好，以及{profile.mood}的心情，
我们为您精选了 {book_count} 本书。这些书籍都符合您{profile.reading_goal}的阅读目标。
您更倾向于哪一本？我们随时可以为您提供更多延伸信息。"""
```

**4. 创建推荐卡片**
```python
recommendation_card = RecommendationCard(
    user_profile=user_profile,
    recommended_books=books,
    message=message,
)
return recommendation_card
```

### 关键职责

1. **数据验证**: 确保所有必需信息都存在
2. **格式统一**: 标准化输出格式
3. **错误恢复**: 提供默认值处理缺失数据
4. **用户体验**: 生成友好的交付消息

### 设计考虑

- **容错性**: 即使部分数据缺失也能返回结果
- **可追溯**: 记录警告日志便于调试
- **灵活性**: 易于扩展添加新字段

---

## Agent 协作流程

### 完整执行流程

```python
# src/services/recommendation_service.py

async def get_recommendations(
    self, request: RecommendationRequest
) -> RecommendationCard:
    """完整的推荐流程"""

    # Step 1: Selector 理解用户需求
    user_profile, candidates, _ = await self.selector.process(
        user_message=request.user_message,
        conversation_history=request.conversation_history,
    )

    # Step 2: 并行执行 EssenceExtractor 和 InsightProvider
    summaries_task = self.essence_extractor.process(candidates)
    reasons_task = self.insight_provider.process(candidates, user_profile)

    summaries, reasons = await asyncio.gather(
        summaries_task, reasons_task
    )

    # Step 3: Assembler 整合所有信息
    recommendation_card = await self.assembler.process(
        user_profile=user_profile,
        candidates=candidates,
        summaries=summaries,
        reasons=reasons,
    )

    return recommendation_card
```

### 并行执行优化

**为什么并行**:
- EssenceExtractor 和 InsightProvider 互不依赖
- 可以同时调用LLM API
- 减少总响应时间约50%

**实现方式**:
```python
import asyncio

# 并行执行两个独立任务
results = await asyncio.gather(
    task1,
    task2,
    return_exceptions=True  # 捕获异常而不中断其他任务
)
```

### 错误处理策略

**1. 单个Agent失败**:
```python
try:
    summaries = await self.essence_extractor.process(candidates)
except Exception as e:
    logger.error(f"EssenceExtractor failed: {e}")
    # 使用默认摘要
    summaries = {c.title: f"默认摘要" for c in candidates}
```

**2. 部分失败**:
- Assembler 负责填补缺失数据
- 记录警告日志
- 返回部分结果而不是完全失败

**3. 全局失败**:
- FastAPI 异常处理器捕获
- 返回500错误和友好错误消息

---

## Prompt Engineering 技巧

### 1. 角色定位清晰

**好的示例**:
```
你是一位专业的文学向导，负责与读者对话并理解他们的阅读需求。
```

**不好的示例**:
```
你是一个AI助手。
```

### 2. 具体的输出格式

**好的示例**:
```
输出格式：
返回JSON格式，包含以下字段：
{
    "field1": "description",
    "field2": "description"
}
```

**不好的示例**:
```
请返回结果。
```

### 3. 提供示例

**好的示例**:
```
提问技巧：
- "您最近读过什么书？最喜欢哪本，为什么？"
- "您现在的心情如何？"
```

### 4. 明确约束条件

**好的示例**:
```
摘要要求：
- 长度：约50-80字
- 风格：客观、精练
- 避免：剧透关键情节
```

### 5. 指定语气和风格

**好的示例**:
```
保持专业、友好的语气，用中文回应。
```

---

## 扩展和自定义

### 添加新的Agent

**示例：添加BookReviewer Agent**

```python
# src/agents/book_reviewer.py
from src.agents.base import BaseAgent

class BookReviewerAgent(BaseAgent):
    """书评生成Agent"""

    SYSTEM_PROMPT = """你是一位资深书评人，擅长写简短精悍的书评。

职责：
1. 接收书籍信息
2. 生成100-150字的专业书评
3. 包含优点、缺点和适合人群

输出格式：JSON
"""

    async def process(
        self, book: BookCandidate
    ) -> str:
        """生成书评

        Args:
            book: 书籍信息

        Returns:
            书评文本
        """
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"请为《{book.title}》撰写书评")
        ]

        response = await self.llm.ainvoke(messages)
        return response.content
```

**集成到Service**:
```python
# src/services/recommendation_service.py
class RecommendationService:
    def __init__(self, ...):
        ...
        self.book_reviewer = BookReviewerAgent(...)

    async def get_detailed_recommendations(self, ...):
        # 在原有流程基础上添加书评
        recommendation_card = await self.get_recommendations(...)

        # 为每本书生成书评
        for book in recommendation_card.recommended_books:
            review = await self.book_reviewer.process(
                BookCandidate(title=book.title, author=book.author)
            )
            # 将书评添加到响应中
            ...
```

### 自定义Agent行为

#### 1. 调整Temperature

```python
# 更保守的输出
selector = SelectorAgent(temperature=0.3)

# 更有创意的输出
insight_provider = InsightProviderAgent(temperature=0.9)
```

#### 2. 更换模型

```python
# 使用更快的模型
selector = SelectorAgent(model="gpt-3.5-turbo")

# 使用更强的模型
insight_provider = InsightProviderAgent(model="gpt-4-turbo")
```

#### 3. 自定义Prompt

```python
class CustomSelectorAgent(SelectorAgent):
    SYSTEM_PROMPT = """
    你的自定义Prompt...
    """
```

### 添加缓存层

```python
from functools import lru_cache
import hashlib

class CachedEssenceExtractor(EssenceExtractorAgent):
    """带缓存的摘要生成器"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}

    def _cache_key(self, candidates: list[BookCandidate]) -> str:
        """生成缓存键"""
        titles = sorted([c.title for c in candidates])
        return hashlib.md5(str(titles).encode()).hexdigest()

    async def process(
        self, candidates: list[BookCandidate]
    ) -> dict[str, str]:
        """带缓存的处理"""
        cache_key = self._cache_key(candidates)

        if cache_key in self._cache:
            logger.info("Cache hit for summaries")
            return self._cache[cache_key]

        result = await super().process(candidates)
        self._cache[cache_key] = result

        return result
```

---

## 总结

### Agent 设计最佳实践

1. ✅ **单一职责**: 每个Agent只做一件事
2. ✅ **清晰的Prompt**: 角色、职责、格式、约束
3. ✅ **类型安全**: 使用Pydantic进行数据验证
4. ✅ **错误处理**: 提供降级和默认值
5. ✅ **并行执行**: 利用asyncio提高性能
6. ✅ **日志记录**: 便于调试和监控

### 性能优化建议

1. **并行执行**: 独立Agent并行调用
2. **缓存**: 缓存常见书籍的摘要
3. **批量处理**: 一次调用处理多本书
4. **模型选择**: 根据任务选择合适的模型
5. **超时控制**: 设置合理的超时时间

### 测试建议

1. **单元测试**: 测试每个Agent的process方法
2. **Mock LLM**: 使用固定响应测试解析逻辑
3. **集成测试**: 测试完整的Agent协作流程
4. **边界测试**: 测试各种异常情况

---

**文档版本**: 1.0.0
**最后更新**: 2025-11-10
**维护者**: Book Recommendation Team
