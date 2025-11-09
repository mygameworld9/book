# 请务必遵守以下技术规范和工作流程。
这些是 **“技术选型约定”**。**如果**一个项目需要某个特定的功能（如 API、前端、缓存），**则必须**使用清单中对应的技术。如果过程中遇到不清楚的或者需求模糊的及时向我提问

## 1. 核心技术栈 (Tech Stack)

|**场景 / 需求**|**必须 使用的规范**|**备注**|
|---|---|---|
|**Python 环境**|**uv**|**所有** Python 项目，使用 `uv` 管理环境和依赖。|
|**Python 依赖**|**`pyproject.toml`**|**所有** Python 依赖、配置 (pytest, mypy, ruff) **必须** 统一在 `pyproject.toml` 中管理。|
|**后端 API 服务**|**FastAPI**|如果项目需要提供 REST API，**必须**使用 FastAPI。|
|**前端 UI**|**React**|如果项目需要图形用户界面 (GUI / Web)，**必须**使用 React。|
|**缓存 / 消息队列**|**Redis**|如果项目需要使用 Redis，**必须**通过 **Docker** 运行。|

## 2. 质量保证与 API 设计 (QA & API Design)

|**场景 / 需求**|**必须 使用的规范**|**备注**|
|---|---|---|
|**Python 日志**|**`logging` 模块**|**禁止**在非临时调试代码中使用 `print()`。应使用结构化日志。|
|**Python 测试**|**Pytest**|如果项目包含 Python 逻辑，**必须**使用 Pytest 编写测试。|
|**React 测试**|**RTL + (Jest / Vitest)**|如果项目包含 React 前端，**必须**使用 React Testing Library (RTL)。|
|**类型提示 (Py)**|**严格类型提示**|**所有** Python 函数**必须**包含类型提示 (参数与返回值)。|
|**类型检查 (Py)**|**`mypy`**|**必须** 在 CI 流程中加入 `mypy` 进行静态类型检查。|
|**数据模型 (Py)**|**Pydantic**|**所有** API 的请求体和响应体**必须**使用 Pydantic 模型定义。|
|**API 错误处理**|**标准化错误响应**|**必须** 使用 FastAPI 异常处理器 (`@app.exception_handler`) 来统一所有 4xx/5xx 错误响应的 JSON 结构。|

## 3. 安全与配置 (Security & Config)

|**场景 / 需求**|**必须 使用的规范**|**备注**|
|---|---|---|
|**密钥管理**|**`.env` 文件**|**所有** 密钥、密码、API Key **必须** 存储在 `.env` 文件中。|
|**版本控制**|**`.gitignore`**|`.env` 文件 **必须** 添加到 `.gitignore` 中，**严禁**提交到 Git。|
|**配置模板**|**`.env.example`**|项目中 **必须** 包含一个 `.env.example` 文件作为配置模板。|

## 4. 结构、部署与自动化 (Structure, Deployment & Automation)

|**领域**|**规范要求**|**备注**|
|---|---|---|
|**目录结构**|**标准化结构**|必须遵循 `/src` (Py), `/frontend` (React), `/tests` (Pytest), `/scripts` (Bash/Py) 的顶层目录结构。|
|**本地开发**|**Docker Compose**|**必须** 提供 `docker-compose.yml` 来一键启动所有后端服务 (如 `backend`, `redis`)。|
|**热重载**|**Volume 挂载**|`docker-compose.yml` 中的 `backend` 服务**必须**挂载本地 `src` 目录以实现代码热重载。|
|**生产构建 (Py)**|**多阶段 `Dockerfile`**|FastAPI 后端**必须**有 `Dockerfile`，使用 `gunicorn -k uvicorn.workers.UvicornWorker` 在生产中启动。|
|**生产构建 (FE)**|**多阶段 `Dockerfile`**|React 前端**必须**有 `Dockerfile`，构建静态文件并通过 `nginx:alpine` 伺服。|
|**自动化 CI**|**GitHub Actions**|**必须** 配置 GitHub Actions 工作流，在 PR 和 push 时自动运行测试 (pytest) 和类型检查 (mypy)。|
|**LLM 交互**|**OpenAI 兼容接口**|**如果**项目需要调用大模型，代码实现**必须**抽象为接受 `api_base`, `api_key`, `model` 三个参数。|

## 5. 工作流 (Workflow)

| **领域**    | **规范要求**              | **备注**                                                        |
| --------- | --------------------- | ------------------------------------------------------------- |
| **分支模型**  | **功能分支**              | **所有** 的新功能或修复**必须**在一个新的分支上开发且每个模块单独一个分支 。                   |
| **主分支**   | **保护分支**              | `main` 分支**必须**被设置为**保护分支**。                                  |
| **合并流程**  | **Pull Request (PR)** | **严禁**直接 Push 到 `main` 分支。**必须**通过创建 Pull Request (PR) 来合并代码。 |
| **CI 门禁** | **检查必须通过**            | PR **必须**通过所有 GitHub Actions 状态检查后，才允许被合并。                    |
| **提交信息**  | **遵循约定**              | 保持 commit message 简洁并有意义                                      |
