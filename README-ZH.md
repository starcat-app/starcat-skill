# Starcat Skill

<!-- starcat-promo:start -->
<div align="center">
<a href="https://starcat.ink"><img src="https://raw.githubusercontent.com/starcat-app/starcat-pro/main/banner.webp" width="100%" alt="Starcat" /></a>

<p><strong>这是供 Codex、Claude Code 等 AI Agent 读取和整理 Starcat 数据的官方 Skill。</strong></p>
<p>Starcat 是一款原生 macOS 应用，可以把 GitHub Stars 变成可搜索、可整理、可用 AI 理解的知识库。它支持 README 渲染、标签与私有笔记、Release 追踪、仓库健康度、AI 摘要、语义搜索、浏览器插件工作流，并提供多个可自部署 API。</p>

<a href="https://github.com/starcat-app/homebrew-starcat"><img src="https://img.shields.io/badge/Install%20with-Homebrew-FBBF24?style=for-the-badge&logo=homebrew&logoColor=white" width="220" alt="Install with Homebrew"/></a>
<br/>
<sub><a href="./README.md">English</a></sub>
</div>

<div align="center">
<a href="https://starcat.ink"><img src="https://img.shields.io/badge/website-starcat.ink-38BDF8?style=flat&color=blue" alt="website"/></a>
<a href="https://github.com/starcat-app/starcat-pro"><img src="https://img.shields.io/badge/support-starcat--pro-lightgrey.svg?style=flat&color=blue" alt="support"/></a>
<a href="https://github.com/starcat-app/homebrew-starcat"><img src="https://img.shields.io/badge/install-homebrew-lightgrey.svg?style=flat&color=blue" alt="homebrew"/></a>
<a href="https://github.com/starcat-app/starcat-localization"><img src="https://img.shields.io/badge/localization-open-lightgrey.svg?style=flat&color=blue" alt="localization"/></a>
</div>

<div align="center">
<img width="900" src="https://raw.githubusercontent.com/starcat-app/starcat-pro/main/main.webp" alt="Starcat main window"/>
</div>

**首选 Homebrew 安装：**

```bash
brew tap starcat-app/starcat
brew trust starcat-app/starcat
brew install --cask starcat
```

**相关链接：**

- 官网与下载: https://starcat.ink
- 公开支持与发布说明: https://github.com/starcat-app/starcat-pro
- Starcat App Homebrew tap: https://github.com/starcat-app/homebrew-starcat
- CLI / MCP: [starcat-cli](https://github.com/starcat-app/starcat-cli) / [Homebrew tap](https://github.com/starcat-app/homebrew-starcat-cli)
- AI Agent Skill: https://github.com/starcat-app/starcat-skill
- 浏览器插件: [Chrome](https://github.com/starcat-app/starcat-chrome-plugin) / [Safari](https://github.com/starcat-app/starcat-safari-plugin)
- 本地化: https://github.com/starcat-app/starcat-localization

**可自部署支撑 API：**

- [starcat-sharing-api](https://github.com/starcat-app/starcat-sharing-api)
- [starcat-trending-api](https://github.com/starcat-app/starcat-trending-api)
- [starcat-weekly-api](https://github.com/starcat-app/starcat-weekly-api)
- [starcat-wiki-api](https://github.com/starcat-app/starcat-wiki-api)
- [starcat-recommend-api](https://github.com/starcat-app/starcat-recommend-api)
- [starcat-discovery-api](https://github.com/starcat-app/starcat-discovery-api)
<!-- starcat-promo:end -->

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
python3 scripts/validate_contract.py --cli "$(command -v starcat)"
```
