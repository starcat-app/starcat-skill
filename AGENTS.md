# AGENTS.md

本文档是 `starcat-skill` 的 AI 协作规则唯一维护源。

## 仓库边界

- 本目录是 Starcat 官方 AI Agent Skill 的独立 Git 仓库，只通过跨平台
  `starcat mcp` bridge 使用 Starcat 能力，不直接读取应用数据库、CloudKit 或凭据文件。
- 本仓库拥有独立分支、remote、提交和发布边界；不得把改动并入外层 Starcat 主仓库
  或顺带修改 `starcat-cli` 及相邻 `supports/*` 项目。
- 开工前核对 `git status --short` 与当前分支，保留用户已有改动；未经明确要求不
  commit、push、切分支、安装/更新 Skill 或修改 remote。

## 用途、技术栈与目录

- `SKILL.md` 是 Agent 发现、安装和安全操作入口；`references/commands.md` 与
  `references/workflows.md` 记录命令/MCP 契约和复用流程。
- `agents/openai.yaml` 保存 Agent 展示元数据；`scripts/validate_contract.py` 使用
  Python 3、PyYAML 与隔离 HOME 校验 Skill 结构和当前 `starcat` CLI help 契约。
- 本仓库内新增或维护的 Skill 内容必须使用中文，包括 `SKILL.md`、`references/`、
  示例、触发说明和操作步骤；代码、命令、工具名、参数、路径、YAML key 与错误日志
  保持原文。

## CLI 与 MCP 契约

- `starcat` CLI 的当前 help、`starcat.get_capabilities` 返回值和正式 MCP tool schema
  是运行时契约来源；Skill 不得臆造命令、工具、字段、默认值或 capability。
- 业务操作必须通过用户级 `starcat mcp` bridge；不得绕过 bridge 自行访问 SQLite、
  Local API、HTTP/JSON-RPC、配对凭据或 Local API Key。
- 每个工作流先调用 `starcat.get_capabilities`；README 等大内容只在任务需要时读取，
  不把用户私有笔记、标签、状态或检索结果写入日志和仓库。
- CLI 与 Skill 同步演进时必须更新契约说明与校验预期；不能用未经确认的旧 release
  行为冒充当前 contract。

## 写操作授权

- 所有写工具默认先以 `dry_run = true` 预览目标和变化；只有用户原始请求明确授权，
  且 dry-run 与请求完全一致时，才可用相同参数执行 `dry_run = false`。
- 写后必须调用 `starcat.get_repo_context` 验证。`starcat.set_repo_tags` 会覆盖全部标签，
  除非用户确认完整最终集合，否则使用增删工具。
- 不得 Star/Unstar GitHub 仓库。摘要生成可能消耗用户 AI 配额，External Search 还会
  发送外部上下文，两者都必须由用户明确请求。

## 验证命令

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contract.py --cli "$(command -v starcat)"
git diff --check
```

依赖已安装时不要重复安装；校验使用可执行的当前 `starcat` CLI，并确认隔离 HOME 不会
读取真实配对数据。

## 外部副作用禁令

- 未经明确授权，不得执行 Skill clone/pull、用户级安装、Agent 配置写入、CLI 配对、
  Starcat 数据写入、摘要生成、External Search、push 或 Release。
- 一次性配对命令和 URI 不得请求拆分、打印、持久化或复用；不得输出 Local API Key、
  私有笔记、Token 或 MCP transport 内容。
