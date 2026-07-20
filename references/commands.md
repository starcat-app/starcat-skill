# Starcat CLI 命令契约

## 连接与 MCP

| 命令 | 用途 |
|---|---|
| `starcat pair <starcat-pair://...>` | 兑换一次性邀请并等待 Starcat 确认设备 |
| `starcat unpair` | 删除当前设备 profile 和系统安全存储凭据 |
| `starcat doctor --json` | 检查配对、连接、协议版本、工具列表和能力 |
| `starcat capabilities --json` | 读取 Starcat 当前权限快照 |
| `starcat mcp` | 将 stdio JSON-RPC 桥接到 Starcat MCP Streamable HTTP |

## 读取

| 命令 | 用途 |
|---|---|
| `starcat repo search <query>` | 关键词搜索；支持 `--scope`、`--limit`、`--semantic` |
| `starcat repo context <owner/name>` | 聚合读取 repo、tags、note、summary |
| `starcat repo readme <owner/name>` | 读取缓存 README |
| `starcat repo summary <owner/name>` | 读取缓存摘要 |
| `starcat tags list` | 列出全部标签 |

## 生成与写入

| 命令 | 用途与约束 |
|---|---|
| `starcat repo summary <owner/name> --generate` | 使用 Starcat AI Provider 生成摘要；可能消耗配额 |
| `starcat repo note set <owner/name> --stdin` | 写入或清空 Markdown 笔记；内容只从 stdin 读取 |
| `starcat repo status set <owner/name> <status>` | `status` 为 `unread`、`read` 或 `using` |
| `starcat repo tags add <owner/name> <tag...>` | 增量添加标签，缺失标签自动创建 |
| `starcat repo tags remove <owner/name> <tag...>` | 增量移除标签 |
| `starcat repo tags replace <owner/name> <tag...>` | 替换全部标签，需要破坏性写入权限 |
| `starcat tag create <name>` | 创建标签；可传 `--color`、`--icon` |

所有写入命令不带 `--apply` 时都是 dry-run。正式写入后必须重新读取 context 验证。
