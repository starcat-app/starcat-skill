# Starcat 操作流程

## 选择入口

已连接 MCP 时调用同名工具；否则使用 `starcat tools call NAME --input FILE`。
两者都先读 capabilities 与目录，再按真实 Schema 准备参数，不自行发送 HTTP。

## 查询统计

读取 `starcat.get_capabilities`，概览用 `starcat.get_overview_statistics`；
AI 明细用 `starcat.get_ai_usage_statistics`，明确时间和筛选条件；
来源、项目与分片用 `starcat.get_knowledge_base_statistics`。
CLI 对应 `starcat stats --json`、`starcat stats ai --range 30d --json`、
`starcat stats knowledge --json`。回答注明范围，缺失 token 不按零处理。

## 整理仓库

1. 读取目标 `starcat.get_repo_context`。
2. 用笔记、状态、标签或 Star 工具预览，CLI 不加 `--apply`。
3. 原始指令已授权且目标一致时执行同一输入，CLI 加 `--apply`。
4. 回读实际状态，批量逐项核对。

标签优先增删，替换要有完整最终集合。GitHub Star / Unstar 需要远端写入权限。
笔记放 JSON 文件或 stdin，不把敏感正文放入 shell 参数。

## 知识库与 AI

读取 `starcat.knowledge_search` 的实际 Schema，输入 `query` 和明确 `repo_ids`。
只有 App 授权且用户需要才加 `include_private_notes=true`。
引用对应真实证据，检索不是生成答案。
用户要求索引时预览 `starcat.start_knowledge_index` 后再执行；
索引可能下载 README、上传内容到已配置后端并消耗 embedding 配额。

先读已有摘要，用户要求时才生成。目录有 `starcat.start_summary` /
`starcat.start_tag_suggestions` 时优先使用；预览后显式执行，不自动应用建议。
External Search 需要许可。

保存 `task_id`，查询 `starcat.get_task_status` 和 `starcat.get_task_result`。
超时先查状态；`TASK_NOT_FOUND` 可能是重启、切号或过期，不表示可以安全重放。
仅在支持时取消；`cancelling` 不是已取消，不伪造进度或恢复。

## 缓存与文件

Trending、Weekly、Awesome、每日热点、推荐和健康按缓存契约读取。
空缓存如实报告；刷新与生成需要独立授权。
每日热点使用目录修订和正文修订，不跨语言替换内容。
`starcat.export_repositories` 检查 `count`、`total`、`truncated` 和文件归属；
CLI 所在设备保存内容，此导出不含私有笔记，也不是数据库备份。

## 连接失败

先运行 `starcat doctor`，区分未配对、服务关闭、Pro / 权限拒绝和版本不支持。
MCP 配置指向正确的 `starcat mcp`；CLI 工作流不依赖重载 MCP。
凭据失效时请用户复制新的完整配对命令，不索要 Local API Key。
远程保持 HTTPS 和证书绑定，不自动换 HTTP。
不安装浏览器宿主或更改系统权限来绕过 MCP 失败。
