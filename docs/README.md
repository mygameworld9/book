# 图书推荐系统文档中心

欢迎来到多Agent图书推荐系统的文档中心！这里提供了完整的项目文档，帮助你快速了解和使用本系统。

## 📚 文档导航

### 1. [项目全面指南](./PROJECT_OVERVIEW.md)
**适合人群**: 新手、开发者、运维人员

**内容概览**:
- 📖 项目概述和技术栈介绍
- 🏗️ 系统架构和目录结构详解
- 💡 核心概念和数据模型
- 🚀 快速开始和环境配置
- 👨‍💻 完整的开发指南
- 🐳 Docker部署和生产环境配置
- 🔧 故障排查和常见问题

**推荐阅读顺序**: 第一篇 - 建议所有人先阅读此文档

---

### 2. [API 使用手册](./API_MANUAL.md)
**适合人群**: 前端开发者、API集成人员、测试人员

**内容概览**:
- 🌐 API端点完整说明
- 📝 详细的请求响应示例
- 💻 多语言客户端示例代码
  - Python 客户端
  - JavaScript/TypeScript 客户端
  - cURL 命令行示例
- ⚠️ 错误处理和状态码说明
- ⚡ 性能优化和最佳实践
- 📎 Postman Collection

**推荐阅读顺序**: 第二篇 - 需要调用API时阅读

---

### 3. [Agent 工作原理详解](./AGENT_DETAILS.md)
**适合人群**: 核心开发者、架构师、AI工程师

**内容概览**:
- 🤖 多Agent架构设计理念
- 🔍 每个Agent的实现细节
  - Selector (文学向导)
  - EssenceExtractor (摘要撰写者)
  - InsightProvider (图书推荐人)
  - Assembler (在线图书管理员)
- 🎨 Prompt Engineering 技巧
- 🔄 Agent协作流程分析
- 🛠️ 扩展和自定义指南
- 📊 性能优化建议

**推荐阅读顺序**: 第三篇 - 深入理解系统时阅读

---

## 🎯 快速入口

### 我是新手，第一次接触这个项目
👉 开始阅读: [项目全面指南](./PROJECT_OVERVIEW.md) → 快速开始章节

### 我需要调用API
👉 开始阅读: [API 使用手册](./API_MANUAL.md) → API 端点详解

### 我想了解Agent是如何工作的
👉 开始阅读: [Agent 工作原理详解](./AGENT_DETAILS.md) → 多Agent架构概述

### 我想添加新功能或修改Agent
👉 开始阅读: [Agent 工作原理详解](./AGENT_DETAILS.md) → 扩展和自定义

### 我遇到了问题
👉 开始阅读: [项目全面指南](./PROJECT_OVERVIEW.md) → 故障排查

---

## 📖 完整学习路径

### 路径 1: 快速上手（20分钟）
1. 阅读 [项目全面指南](./PROJECT_OVERVIEW.md) - 项目概述
2. 阅读 [项目全面指南](./PROJECT_OVERVIEW.md) - 快速开始
3. 运行项目并访问 http://localhost:8000/docs
4. 在Swagger UI中测试API

### 路径 2: API集成（30分钟）
1. 阅读 [API 使用手册](./API_MANUAL.md) - API概述
2. 阅读 [API 使用手册](./API_MANUAL.md) - API端点详解
3. 选择你的语言查看客户端示例
4. 运行示例代码进行测试

### 路径 3: 深入理解（60分钟）
1. 阅读 [项目全面指南](./PROJECT_OVERVIEW.md) - 系统架构
2. 阅读 [Agent 工作原理详解](./AGENT_DETAILS.md) - 完整文档
3. 查看源代码验证理解
4. 尝试修改Prompt或添加新Agent

### 路径 4: 生产部署（45分钟）
1. 阅读 [项目全面指南](./PROJECT_OVERVIEW.md) - 部署指南
2. 配置生产环境变量
3. 构建Docker镜像
4. 部署并进行健康检查

---

## 🔗 相关链接

- **项目仓库**: [https://github.com/mygameworld9/book](https://github.com/mygameworld9/book)
- **在线API文档**: http://localhost:8000/docs (本地运行时)
- **问题反馈**: [GitHub Issues](https://github.com/mygameworld9/book/issues)

---

## 📊 文档统计

| 文档 | 章节数 | 预计阅读时间 |
|------|--------|--------------|
| [项目全面指南](./PROJECT_OVERVIEW.md) | 7 | 25分钟 |
| [API 使用手册](./API_MANUAL.md) | 7 | 20分钟 |
| [Agent 工作原理详解](./AGENT_DETAILS.md) | 9 | 30分钟 |
| **总计** | **23** | **75分钟** |

---

## 🤝 贡献文档

发现文档有误或需要改进？

1. Fork 项目仓库
2. 编辑 `docs/` 目录下的Markdown文件
3. 提交 Pull Request

---

## 📝 文档版本

- **当前版本**: 1.0.0
- **最后更新**: 2025-11-10
- **兼容系统版本**: 0.1.0

---

## ❓ 常见问题快速索引

### 安装和配置
- [如何安装依赖？](./PROJECT_OVERVIEW.md#安装步骤)
- [如何配置环境变量？](./PROJECT_OVERVIEW.md#配置环境变量)
- [如何启动开发服务器？](./PROJECT_OVERVIEW.md#运行开发服务器)

### API使用
- [如何调用推荐API？](./API_MANUAL.md#获取图书推荐核心-api)
- [支持哪些编程语言？](./API_MANUAL.md#客户端集成示例)
- [如何处理错误？](./API_MANUAL.md#错误处理)

### 开发相关
- [如何添加新的Agent？](./AGENT_DETAILS.md#添加新的agent)
- [如何运行测试？](./PROJECT_OVERVIEW.md#测试指南)
- [如何调试Agent？](./PROJECT_OVERVIEW.md#调试技巧)

### 部署相关
- [如何Docker部署？](./PROJECT_OVERVIEW.md#docker-部署)
- [生产环境配置？](./PROJECT_OVERVIEW.md#生产环境配置)
- [如何监控健康状态？](./API_MANUAL.md#健康检查)

---

**享受使用本系统吧！如有任何问题，请随时查阅文档或提交Issue。**

**Made with ❤️ by Book Recommendation Team**
