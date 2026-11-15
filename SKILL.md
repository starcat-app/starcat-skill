---
name: starcat-skill
description: 安装、更新并通过 Starcat CLI 或 MCP 查询和整理 Starcat 中的 GitHub 仓库知识。适用于收藏搜索、标签、笔记、状态、README、摘要、知识库证据、统计、Release、每日热点和可用公共工具；用户明确授权后可执行写入、同步、索引和 AI 生成。
---

# Starcat Skill

## 安装或更新本 Skill

用户要求安装或更新时，先识别当前 Agent，选择唯一用户级目录：
Codex 使用 `$HOME/.codex/skills/starcat-skill`，Claude Code 使用 `$HOME/.claude/skills/starcat-skill`。
目录不存在时从 `https://github.com/starcat-app/starcat-skill` 克隆；已有干净的同源仓库只执行 `git pull --ff-only`。
其它目录或未提交改动须报告冲突，不覆盖、删除、reset 或强制更新。

确认 `SKILL.md`、`agents/openai.yaml`、`references/commands.md` 和 `references/workflows.md` 存在。
运行 `starcat --help`，核对完整 URI 配对、`mcp`、`tools`、`resources` 和统计入口。
重载 Agent 后再确认 Skill 已被发现；未观察到结果就如实报告待重载。
安装验证只运行 `starcat doctor`、读取 capabilities 和 `limit=2` 的仓库搜索，不执行写入。

## 选择 MCP 或结构化 CLI

- 已配置 MCP 时，以绝对路径启动 `starcat`，唯一参数为 `mcp`，调用其工具与资源。
- 没有 MCP 或用户偏好 CLI 时，使用 `tools list / describe / call`、`resources list / read`，业务输出为 JSON。
- 高频专用命令也可使用；统计加 `--json`，不要解析终端展示文字。

先运行 `starcat doctor`。未安装时使用官方 CLI 发行版；未配对时请用户在
**Starcat > 设置 > MCP 服务**复制完整单次命令，并原样执行 `starcat pair ...`。
不单独索要 URI 或 Local API Key，不打印、持久化或复用配对命令。
远程连接保持邀请中的 HTTPS 与证书绑定，不降级为局域网 HTTP。
浏览器 token 与 CLI / MCP 凭据分开管理，不能混用。

禁止直接读取 SQLite、CloudKit、Keychain 或凭据文件；禁止自造 HTTP / JSON-RPC 绕过 CLI。
`starcat mcp` 的 stdout 仅承载协议，诊断写 stderr。

## 每个工作流先发现能力

1. 调用 `starcat.get_capabilities` 获取当前权限。
2. 从 `tools/list` 或 `starcat tools list --json` 获取真实工具；通过 `starcat.get_capability_catalog` 或 `starcat://capabilities` 确认业务版本、联网和任务语义。
3. 读取要使用的工具 Schema，不臆造参数，不根据文档列表推断运行中的 App 已支持。
4. 缺少工具时报告版本或模块不支持；权限关闭时引导设置，不绕过门禁。
5. 以后新增公共工具可直接通用调用，不必等待 Skill 增加专用命令。

App 公共契约 v2 从 server `0.6.0` 起，含 `dry_run` 的操作省略时默认预览。
旧 App 可能省略即执行，因此调用方始终显式预览；MCP 协议版本不能代替业务版本。

## 读取与查询

- 概览使用 `starcat.get_overview_statistics`；AI 筛选使用 `starcat.get_ai_usage_statistics`，知识库与索引使用 `starcat.get_knowledge_base_statistics`。
- 已知 `owner/name` 时优先 `starcat.get_repo_context`；需要大正文才读取 `starcat.get_readme`。
- `starcat.knowledge_search` 必须限定 `repo_ids`，返回证据与引用，不代表完成答案生成。
- 健康、安全、洞察、推荐、Release、通知、每日热点和 Skill 证据按目录的缓存语义读取，缺失不是零，不自动刷新或生成。
- 私有笔记须有 App 授权并按 Schema 显式请求；结果和内容不写入日志或仓库。

用户收藏数与仓库公众 Star 数不同；Provider 未报告 token 不代表消耗为零。
每日热点按 `catalog_revision` 分页，详情固定语言和 `revision`，不能用新版正文解释旧引用。

## 写入和生成

先预览核对目标；原始指令已授权且预览一致时直接执行，无需为相同授权重复询问。

```bash
starcat tools call starcat.set_repo_status --input status.json
starcat tools call starcat.set_repo_status --input status.json --apply
```

CLI 用 `--apply` 决定 `dry_run`，输入 JSON 的 `false` 不能绕过预览。
无预览的副作用工具同样须显式执行，不能伪造预览。
MCP 对含该参数的工具先传 `dry_run=true`，执行时传 `false`。
写后按对应读取入口核验，批量逐项检查，不假定跨 GitHub 和本地事务原子回滚。

- 标签优先增删；`starcat.set_repo_tags` 会替换完整集合，需要完整目标和破坏性写入权限。
- GitHub Star / Unstar 仅在用户明确要求且 `github_star_writes` 开启时执行。
- 摘要、标签建议、翻译和问答可能消耗配额，仅在用户要求时发起，建议不自动应用。
- External Search 须明确许可。外部 Agent 的文章不能冒称原生摘要，可按授权存入注明来源的笔记。

## 长任务与文件

同步、索引和生成优先使用可用的 `start_*`，保存 `task_id`，查询
`starcat.get_task_status` / `starcat.get_task_result`。
超时或断开后先查询，不能盲目重放写入。
只有 `supports_cancellation=true` 才请求 `starcat.cancel_task`；`cancelling` 不等于已取消。
完成结果保留一小时；App 重启、账号切换或过期后无效，不宣称能恢复。

文件由运行 CLI 的设备保存，远端配对也不能让 App 使用客户端传来的任意本机路径。
`export_repositories` 是有数量上限的 Markdown / HTML 导出，须检查 `truncated`；不是数据库备份。
导入、恢复、安装、公开分享和发布须运行时工具确实支持，并有用户授权。

详见 [命令与能力契约](references/commands.md) 和 [操作流程](references/workflows.md)。
