# Starcat Skill

Starcat 官方 AI Agent Skill，通过跨平台 [Starcat CLI](https://github.com/starcat-app/starcat-cli) MCP bridge 读取和整理 [Starcat](https://starcat.ink) 中保存的仓库知识。

[English](./README.md)

## 支持能力

- 查看 Star、AI Token、知识库与 RAG 索引统计。
- 使用关键词或语义搜索查找仓库。
- 读取仓库上下文、标签、私人笔记、阅读状态、README 与缓存的 AI 摘要。
- 通过用户在 Starcat 中配置的 AI Provider 生成仓库摘要。
- 在完成 dry-run 并获得用户明确授权后，新增或更新私人笔记、阅读状态和标签。

本 Skill 不直接访问 Starcat 的 SQLite 数据库、CloudKit 数据、凭据文件或 Local API Key。所有业务操作都通过 `starcat mcp` bridge 与 Starcat capability 模型完成。

## 安装

将仓库克隆到当前 Agent 的用户级 Skill 目录：

```bash
# Codex
git clone https://github.com/starcat-app/starcat-skill "$HOME/.codex/skills/starcat-skill"

# Claude Code
git clone https://github.com/starcat-app/starcat-skill "$HOME/.claude/skills/starcat-skill"
```

随后安装 Starcat CLI，重启或重新加载 Agent，并验证本机 bridge：

```bash
starcat doctor
```

如果 CLI 尚未配对，请打开 **Starcat → Settings → MCP Service**，复制完整的一次性配对命令，并按原样执行。

## Agent 工作流

1. 在 Agent 的用户级 MCP 配置中，将 server command 指向 `starcat` 可执行文件的绝对路径，并只传入参数 `mcp`。
2. 每个工作流开始前调用 `starcat.get_capabilities`。
3. 搜索、统计、仓库上下文、README 与摘要使用只读工具。
4. 写操作先以 `dry_run = true` 调用对应工具。
5. 只有用户明确授权且预览结果完全匹配请求时，才以 `dry_run = false` 应用修改。
6. 写入后再次读取仓库上下文，确认结果已经生效。

## 仓库结构

| 路径 | 用途 |
|------|------|
| `SKILL.md` | Agent 使用说明、安全规则与常用工作流。 |
| `agents/openai.yaml` | OpenAI Agent 展示元数据与默认提示词。 |
| `references/commands.md` | Starcat MCP 与 CLI 契约。 |
| `references/workflows.md` | 可复用的读取、写入、生成与故障恢复流程。 |
| `scripts/validate_contract.py` | 契约一致性校验。 |

## 验证

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contract.py
```
