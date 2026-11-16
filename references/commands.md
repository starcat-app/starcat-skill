# Starcat CLI 与 MCP 契约

## 连接与动态入口

| 命令 | 用途 |
| --- | --- |
| `starcat pair "<starcat-pair://...>"` | 执行用户从 App 复制的完整单次命令 |
| `starcat unpair` | 删除当前 CLI profile 和系统凭据 |
| `starcat doctor` | 检查连接、配对、协议、工具和权限 |
| `starcat mcp` | stdio JSON-RPC 经 CLI 连接层转发给 App |
| `starcat tools list --json` | 读取实际工具 Schema |
| `starcat tools describe starcat.get_repo_context --json` | 查看单个工具 |
| `starcat tools call starcat.get_overview_statistics` | 通用 JSON 调用 |
| `starcat tools call starcat.knowledge_search --input query.json` | 读取 CLI 本机文件；`--input -` 使用 stdin |
| `starcat resources list --json` | 动态列出资源 |
| `starcat resources read starcat://capabilities` | 读取目录与业务契约 |

输入必须是单个 JSON 对象，最大 8 MiB；结果为 JSON，诊断在 stderr。
CLI 与 MCP 共用业务执行器，App 是账号、Pro、隐私和写入权限的最终边界。

## 便利命令

| 工具 | 普通 CLI 路径 |
| --- | --- |
| `starcat.get_capabilities` | `starcat capabilities` |
| `starcat.get_overview_statistics` | `starcat stats --json` |
| `starcat.get_ai_usage_statistics` | `starcat stats ai --range 30d --json` |
| `starcat.get_knowledge_base_statistics` | `starcat stats knowledge --json` |
| `starcat.get_repo` | `starcat repo get owner/name` |
| `starcat.get_repo_note` | `starcat repo note get owner/name` |
| `starcat.list_repos_by_tag` | `starcat repo by-tag TAG --limit 20` |
| `starcat.star_repo` / `starcat.unstar_repo` | `starcat repo star owner/name` / `starcat repo unstar owner/name`，执行须 `--apply` |
| 其它工具，包括 `starcat.batch_organize_repos` | `starcat tools call NAME --input FILE`，执行可传 `dry_run=false` 或 `--apply` |

读取 `starcat help repo`、`starcat help stats`、`starcat help tools`、`starcat help resources`。
专用子命令是便利入口，通用调用也是正式入口。

## 新能力与版本

`starcat.get_capability_catalog` 返回 `contract_version`、`server_version`、`write_default`、
`availability`、任务保留策略和工具。登记了工具不代表当前权限开启。
缓存健康 / 安全 / 洞察、Release / 通知、Trending / Weekly / Awesome / 每日热点、
知识库、Skill 证据、模型、任务和导出均通过实际目录发现，不在 Skill 复制固定完整名单。

读取来源、缓存和分页标记；`cache_hit=false` 不代表来源永久为空。
按 `has_more` / `next_offset` 或 `next_cursor` 分页，页长不是全量总数。
知识库证据限定范围，笔记属于默认读取；`include_private_notes` 选择内容。

server `0.7.0` 的业务契约 v3 只有 `read` / `write`；读取默认开放，写入在 App 设置中开启。
含预览的工具由 App 默认 `dry_run=true`，执行传 `false`；CLI 保留输入，不强制重写。
`--apply` 是 `false` 的便利映射，与明确的 `true` 冲突时报错。无预览工具遵循 App 契约；未知工具不静默替换动作。

已有 App 按钮对应的业务默认应开放；下载、限流、校验、取消和事务由 App 负责，不能成为不接入的理由。

业务错误退出非零，通用入口 stderr 带 `STARCAT_ERROR CODE: message`，stdout 不混入诊断。
既有 `starcat search` 保持 global-search schema v1。
任务由 App 持有，断开不取消，状态与结果分别查询；不伪造取消、恢复或百分比。
