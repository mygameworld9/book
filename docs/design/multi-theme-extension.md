# 多主题推荐系统扩展方案

## 📋 概述

基于现有的书籍推荐四步协同模型，扩展为支持**书籍、游戏、电影、动漫**四个主题的多主题推荐系统。

## 🏗️ 系统架构

### 前端架构
- **主题选择器（Theme Selector）**：顶部导航栏，支持在四个主题之间切换
- **推荐界面（Recommendation Interface）**：根据选中主题动态渲染对应的推荐流程
- **路由设计**：
  - `/books` - 书籍推荐
  - `/games` - 游戏推荐
  - `/movies` - 电影推荐
  - `/anime` - 动漫推荐

### 后端架构
- **独立 API 端点**：每个主题使用独立的 API 路由
  - `POST /api/books/recommend`
  - `POST /api/games/recommend`
  - `POST /api/movies/recommend`
  - `POST /api/anime/recommend`
- **共享 Agent 框架**：四个主题复用相同的四步协同推荐模型
- **主题配置文件**：每个主题有独立的提示词配置文件

---

## 🎮 游戏推荐四步协同模型

### 第一步：🕹️ 游戏向导 (The Game Selector)

**角色定位：** 游戏推荐专家，负责与玩家对话，理解游戏偏好，并做出初级推荐决策。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**1.1 玩家对话与需求理解**|通过提问了解玩家的游戏类型偏好、平台、游玩时长、难度偏好、游戏目的（休闲/竞技/剧情）。|内部输出**玩家画像标签**（例如：`[类型: RPG, 平台: PC/PS5, 风格: 开放世界, 难度: 中等, 已玩:《艾尔登法环》]`）。|
|**1.2 初步推荐筛选**|基于玩家画像和游戏数据库，筛选出 2-3 款最匹配的**候选游戏**。|输出：**候选游戏列表**（包含游戏名、开发商、平台）。|
|**1.3 任务分配**|将候选游戏列表分发给其他三个 Agent。|**分发指令：** "针对以下游戏，请生成你的专业内容。"|

### 第二步：📝 游戏简介撰写者 (The Game Essence Extractor)

**角色定位：** 游戏核心玩法和特色的提炼专家。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**2.1 接收任务与检索**|接收候选游戏，从游戏数据库中检索相关信息。|动作：识别游戏的核心玩法、世界观、主要特色。|
|**2.2 撰写简洁摘要**|将游戏的**精髓**提炼成一段简洁、客观的描述，突出核心玩法机制。|输出：每款游戏的**《游戏精髓摘要》**（约 50-80 字）。|
|**2.3 传递结果**|将生成的摘要回传给**游戏管理员**。|传递内容：`[游戏名 A, 摘要 A]`，`[游戏名 B, 摘要 B]`。|

### 第三步：💡 游戏推荐人 (The Game Insight Provider)

**角色定位：** 游戏体验的评论家，专注于"为什么你应该玩它"。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**3.1 接收任务与情境化**|接收候选游戏和玩家画像标签。|动作：将游戏特点与玩家需求进行**关联匹配**。|
|**3.2 撰写推荐理由**|撰写具有"极简价值"的推荐理由，说明这款游戏如何满足玩家的**特定需求**。|输出：每款游戏的**《极简价值推荐理由》**（约 30-50 字）。|
|**3.3 传递结果**|将生成的推荐理由回传给**游戏管理员**。|传递内容：`[游戏名 A, 推荐理由 A]`，`[游戏名 B, 推荐理由 B]`。|

### 第四步：🗂️ 游戏管理员 (The Game Assembler)

**角色定位：** 信息的整合者和交付者。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**4.1 接收与核对**|接收摘要和推荐理由。|动作：验证每款游戏的完整性。|
|**4.2 内容整合与排版**|将所有信息整合到标准化推荐模板中。|输出：**《最终推荐卡片》**（游戏名、开发商、平台、摘要、推荐理由）。|
|**4.3 返回给游戏向导**|将完整的推荐卡片返回。|传递内容：完整的推荐结果。|

---

## 🎬 电影推荐四步协同模型

### 第一步：🎥 电影向导 (The Movie Selector)

**角色定位：** 电影推荐专家，负责与观众对话，理解观影偏好。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**1.1 观众对话与需求理解**|通过提问了解观众的类型偏好、导演/演员偏好、观影场景（独自/情侣/家庭）、情绪需求。|内部输出**观众画像标签**（例如：`[类型: 科幻/悬疑, 风格: 烧脑, 情绪: 思考, 已看:《盗梦空间》]`）。|
|**1.2 初步推荐筛选**|基于观众画像和电影数据库，筛选出 2-3 部最匹配的**候选电影**。|输出：**候选电影列表**（包含片名、导演、年份）。|
|**1.3 任务分配**|将候选电影列表分发给其他三个 Agent。|**分发指令：** "针对以下电影，请生成你的专业内容。"|

### 第二步：📝 电影简介撰写者 (The Movie Essence Extractor)

**角色定位：** 电影核心主题和情节的提炼专家。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**2.1 接收任务与检索**|接收候选电影，从电影数据库中检索相关信息。|动作：识别电影的核心主题、情节线、视觉风格。|
|**2.2 撰写简洁摘要**|将电影的**精髓**提炼成一段简洁描述，避免剧透关键情节。|输出：每部电影的**《电影精髓摘要》**（约 50-80 字）。|
|**2.3 传递结果**|将生成的摘要回传给**电影管理员**。|传递内容：`[片名 A, 摘要 A]`，`[片名 B, 摘要 B]`。|

### 第三步：💡 电影推荐人 (The Movie Insight Provider)

**角色定位：** 电影价值的评论家，专注于"为什么你应该看它"。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**3.1 接收任务与情境化**|接收候选电影和观众画像标签。|动作：将电影特点与观众需求进行**关联匹配**。|
|**3.2 撰写推荐理由**|撰写具有"极简价值"的推荐理由，说明这部电影如何满足观众的**特定情绪需求**。|输出：每部电影的**《极简价值推荐理由》**（约 30-50 字）。|
|**3.3 传递结果**|将生成的推荐理由回传给**电影管理员**。|传递内容：`[片名 A, 推荐理由 A]`，`[片名 B, 推荐理由 B]`。|

### 第四步：🗂️ 电影管理员 (The Movie Assembler)

**角色定位：** 信息的整合者和交付者。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**4.1 接收与核对**|接收摘要和推荐理由。|动作：验证每部电影的完整性。|
|**4.2 内容整合与排版**|将所有信息整合到标准化推荐模板中。|输出：**《最终推荐卡片》**（片名、导演、年份、摘要、推荐理由）。|
|**4.3 返回给电影向导**|将完整的推荐卡片返回。|传递内容：完整的推荐结果。|

---

## 🎨 动漫推荐四步协同模型

### 第一步：✨ 动漫向导 (The Anime Selector)

**角色定位：** 动漫推荐专家，负责与观众对话，理解动漫偏好。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**1.1 观众对话与需求理解**|通过提问了解观众的类型偏好（热血/治愈/日常/悬疑）、画风偏好、番剧长度要求、情绪需求。|内部输出**观众画像标签**（例如：`[类型: 战斗番, 风格: 热血, 长度: 12-24集, 已看:《鬼灭之刃》]`）。|
|**1.2 初步推荐筛选**|基于观众画像和动漫数据库，筛选出 2-3 部最匹配的**候选动漫**。|输出：**候选动漫列表**（包含名称、制作公司、集数）。|
|**1.3 任务分配**|将候选动漫列表分发给其他三个 Agent。|**分发指令：** "针对以下动漫，请生成你的专业内容。"|

### 第二步：📝 动漫简介撰写者 (The Anime Essence Extractor)

**角色定位：** 动漫核心设定和世界观的提炼专家。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**2.1 接收任务与检索**|接收候选动漫，从动漫数据库中检索相关信息。|动作：识别动漫的核心设定、世界观、角色关系。|
|**2.2 撰写简洁摘要**|将动漫的**精髓**提炼成一段简洁描述，突出核心设定和故事主线。|输出：每部动漫的**《动漫精髓摘要》**（约 50-80 字）。|
|**2.3 传递结果**|将生成的摘要回传给**动漫管理员**。|传递内容：`[动漫名 A, 摘要 A]`，`[动漫名 B, 摘要 B]`。|

### 第三步：💡 动漫推荐人 (The Anime Insight Provider)

**角色定位：** 动漫观看体验的评论家，专注于"为什么你应该看它"。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**3.1 接收任务与情境化**|接收候选动漫和观众画像标签。|动作：将动漫特点与观众需求进行**关联匹配**。|
|**3.2 撰写推荐理由**|撰写具有"极简价值"的推荐理由，说明这部动漫如何满足观众的**特定情感需求**。|输出：每部动漫的**《极简价值推荐理由》**（约 30-50 字）。|
|**3.3 传递结果**|将生成的推荐理由回传给**动漫管理员**。|传递内容：`[动漫名 A, 推荐理由 A]`，`[动漫名 B, 推荐理由 B]`。|

### 第四步：🗂️ 动漫管理员 (The Anime Assembler)

**角色定位：** 信息的整合者和交付者。

|**子步骤**|**目标**|**动作/输出**|
|---|---|---|
|**4.1 接收与核对**|接收摘要和推荐理由。|动作：验证每部动漫的完整性。|
|**4.2 内容整合与排版**|将所有信息整合到标准化推荐模板中。|输出：**《最终推荐卡片》**（动漫名、制作公司、集数、摘要、推荐理由）。|
|**4.3 返回给动漫向导**|将完整的推荐卡片返回。|传递内容：完整的推荐结果。|

---

## 🔧 技术实现要点

### 1. 提示词配置管理

创建独立的提示词配置文件：

```
/src/prompts/
  ├── books/
  │   ├── selector.txt
  │   ├── extractor.txt
  │   ├── insight.txt
  │   └── assembler.txt
  ├── games/
  │   ├── selector.txt
  │   ├── extractor.txt
  │   ├── insight.txt
  │   └── assembler.txt
  ├── movies/
  │   ├── selector.txt
  │   ├── extractor.txt
  │   ├── insight.txt
  │   └── assembler.txt
  └── anime/
      ├── selector.txt
      ├── extractor.txt
      ├── insight.txt
      └── assembler.txt
```

### 2. 后端 API 结构

```python
# 统一的请求/响应模型
class RecommendationRequest(BaseModel):
    user_input: str
    user_profile: dict[str, Any] | None = None

class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationCard]

class RecommendationCard(BaseModel):
    title: str
    creator: str  # 作者/导演/制作公司/开发商
    metadata: dict[str, str]  # 灵活的元数据字段
    summary: str
    reason: str

# 路由定义
@app.post("/api/books/recommend", response_model=RecommendationResponse)
async def recommend_books(request: RecommendationRequest):
    return await run_recommendation_flow("books", request)

@app.post("/api/games/recommend", response_model=RecommendationResponse)
async def recommend_games(request: RecommendationRequest):
    return await run_recommendation_flow("games", request)

@app.post("/api/movies/recommend", response_model=RecommendationResponse)
async def recommend_movies(request: RecommendationRequest):
    return await run_recommendation_flow("movies", request)

@app.post("/api/anime/recommend", response_model=RecommendationResponse)
async def recommend_anime(request: RecommendationRequest):
    return await run_recommendation_flow("anime", request)
```

### 3. 前端路由和组件结构

```
/frontend/src/
  ├── components/
  │   ├── ThemeSelector.tsx       # 主题切换导航
  │   ├── RecommendationChat.tsx  # 对话界面（通用）
  │   └── RecommendationCard.tsx  # 推荐卡片（通用）
  ├── pages/
  │   ├── BooksPage.tsx
  │   ├── GamesPage.tsx
  │   ├── MoviesPage.tsx
  │   └── AnimePage.tsx
  ├── hooks/
  │   └── useRecommendation.ts    # 通用推荐逻辑 Hook
  └── types/
      └── recommendation.ts       # TypeScript 类型定义
```

### 4. 共享 Agent 框架

```python
class RecommendationAgent:
    """通用推荐 Agent 基类"""
    def __init__(self, theme: str, role: str):
        self.theme = theme
        self.role = role
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        """从文件加载对应主题和角色的提示词"""
        path = f"src/prompts/{self.theme}/{self.role}.txt"
        with open(path) as f:
            return f.read()

    async def execute(self, input_data: dict) -> dict:
        """执行 Agent 任务"""
        # 调用 LLM API 的通用逻辑
        pass

# 四个 Agent 使用相同的类，只是加载不同的提示词
selector = RecommendationAgent(theme="books", role="selector")
extractor = RecommendationAgent(theme="books", role="extractor")
insight = RecommendationAgent(theme="books", role="insight")
assembler = RecommendationAgent(theme="books", role="assembler")
```

---

## 📝 数据库扩展

### 统一的推荐记录表

```sql
CREATE TABLE recommendations (
    id UUID PRIMARY KEY,
    theme VARCHAR(20) NOT NULL,  -- 'books', 'games', 'movies', 'anime'
    user_input TEXT NOT NULL,
    user_profile JSONB,
    recommendations JSONB NOT NULL,  -- 存储推荐结果
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_theme ON recommendations(theme);
```

---

## 🎯 核心优势

1. **代码复用率高**：四个主题共享同一套 Agent 框架和前端组件
2. **易于扩展**：添加新主题只需：
   - 创建新的提示词配置文件夹
   - 添加一个新的 API 路由
   - 添加一个新的前端页面组件
3. **独立维护**：每个主题的推荐逻辑完全独立，互不影响
4. **一致的用户体验**：四个主题使用相同的交互模式和视觉设计

---

## 📋 实施检查清单

### 后端开发
- [ ] 创建 `/src/prompts/{theme}/{role}.txt` 提示词配置文件（4主题 × 4角色 = 16个文件）
- [ ] 实现通用的 `RecommendationAgent` 基类
- [ ] 实现 `run_recommendation_flow()` 函数
- [ ] 添加四个主题的 API 路由
- [ ] 编写 Pydantic 数据模型
- [ ] 添加错误处理和日志记录
- [ ] 编写 Pytest 测试用例

### 前端开发
- [ ] 创建 `ThemeSelector` 组件（顶部导航）
- [ ] 创建通用的 `RecommendationChat` 和 `RecommendationCard` 组件
- [ ] 创建四个主题的页面组件
- [ ] 配置 React Router 路由
- [ ] 实现 `useRecommendation` Hook
- [ ] 添加主题切换动画和过渡效果
- [ ] 编写 RTL 测试用例

### 配置和部署
- [ ] 更新 `.env.example` 添加新的配置项
- [ ] 更新 `docker-compose.yml`
- [ ] 配置 GitHub Actions CI/CD
- [ ] 编写部署文档

---

## 🚀 未来扩展方向

1. **用户偏好记忆**：记录用户在不同主题下的历史偏好
2. **跨主题推荐**：基于用户在书籍主题的偏好，推荐相关的电影或动漫
3. **社交功能**：用户可以分享推荐结果
4. **更多主题**：音乐、播客、艺术展览等