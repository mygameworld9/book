# 图书推荐系统 - 前端

基于React + Vite构建的图书推荐系统前端界面。

## 功能特性

- 📱 响应式设计，支持移动端和桌面端
- 💬 对话式交互界面
- 📚 精美的推荐卡片展示
- 👤 用户画像可视化
- ⚡ 快速的开发体验 (Vite HMR)
- 🧪 完整的测试覆盖

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

### 运行测试

```bash
# 运行测试
npm test

# 运行测试（带UI）
npm run test:ui
```

## 环境变量

创建 `.env` 文件：

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## 项目结构

```
frontend/
├── src/
│   ├── components/         # React组件
│   │   ├── BookCard.jsx           # 书籍卡片
│   │   ├── ChatInterface.jsx      # 对话界面
│   │   ├── RecommendationCards.jsx # 推荐卡片容器
│   │   └── UserProfile.jsx        # 用户画像
│   ├── services/          # API服务
│   │   └── api.js
│   ├── test/              # 测试文件
│   ├── App.jsx            # 主应用组件
│   ├── main.jsx          # 入口文件
│   └── index.css         # 全局样式
├── public/               # 静态资源
├── Dockerfile           # Docker构建配置
├── nginx.conf          # Nginx配置
└── vite.config.js      # Vite配置
```

## Docker 部署

### 构建镜像

```bash
docker build -t book-recommendation-frontend .
```

### 运行容器

```bash
docker run -d -p 80:80 book-recommendation-frontend
```

## 技术栈

- **框架**: React 18.3
- **构建工具**: Vite 5
- **HTTP客户端**: Axios
- **测试**: Vitest + React Testing Library
- **样式**: 原生CSS（支持深色/浅色模式）

## 开发说明

### 代码风格

项目使用 ESLint 进行代码检查：

```bash
npm run lint
```

### 组件说明

#### BookCard
显示单本书籍的详细信息卡片，包括：
- 书名、作者、ISBN
- 内容简介
- 推荐理由
- 操作按钮

#### ChatInterface
对话界面组件，提供：
- 消息输入框
- 对话历史显示
- 示例提示
- 重置功能

#### RecommendationCards
推荐结果容器，包含：
- 用户画像展示
- 书籍卡片网格
- 系统消息

#### UserProfile
用户阅读画像展示，包括：
- 类型、风格、心情、目标标签
- 已读书籍列表

### API集成

所有API调用通过 `src/services/api.js` 统一管理：

```javascript
import { getRecommendations } from './services/api'

const data = await getRecommendations(message, history)
```

## 浏览器支持

- Chrome (最新版)
- Firefox (最新版)
- Safari (最新版)
- Edge (最新版)

## License

MIT
