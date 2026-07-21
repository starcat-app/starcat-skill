# Starcat Skill

<!-- starcat-promo:start -->
<div align="center">
<a href="https://starcat.ink"><img src="https://raw.githubusercontent.com/starcat-app/starcat-pro/main/banner.webp" width="100%" alt="Starcat" /></a>

<p><strong>Official skill for AI agents such as Codex and Claude Code to read and organize Starcat data.</strong></p>
<p>Starcat is a native macOS app that turns GitHub Stars into a searchable, organized and AI-assisted knowledge base. It supports README rendering, tags, private notes, release tracking, repository health signals, AI summaries, semantic search, browser plugin workflows and self-hostable support APIs.</p>

<a href="https://github.com/starcat-app/homebrew-starcat"><img src="https://img.shields.io/badge/Install%20with-Homebrew-FBBF24?style=for-the-badge&logo=homebrew&logoColor=white" width="220" alt="Install with Homebrew"/></a>
<br/>
<sub><a href="./README-ZH.md">中文说明</a></sub>
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

**Preferred install method:**

```bash
brew tap starcat-app/starcat
brew trust starcat-app/starcat
brew install --cask starcat
```

**Useful links:**

- Home and downloads: https://starcat.ink
- Public support and release notes: https://github.com/starcat-app/starcat-pro
- Starcat App Homebrew tap: https://github.com/starcat-app/homebrew-starcat
- CLI / MCP: [starcat-cli](https://github.com/starcat-app/starcat-cli) / [Homebrew tap](https://github.com/starcat-app/homebrew-starcat-cli)
- AI Agent Skill: https://github.com/starcat-app/starcat-skill
- Browser plugins: [Chrome](https://github.com/starcat-app/starcat-chrome-plugin) / [Safari](https://github.com/starcat-app/starcat-safari-plugin)
- Localization: https://github.com/starcat-app/starcat-localization

**Self-hostable support APIs:**

- [starcat-sharing-api](https://github.com/starcat-app/starcat-sharing-api)
- [starcat-trending-api](https://github.com/starcat-app/starcat-trending-api)
- [starcat-weekly-api](https://github.com/starcat-app/starcat-weekly-api)
- [starcat-wiki-api](https://github.com/starcat-app/starcat-wiki-api)
- [starcat-recommend-api](https://github.com/starcat-app/starcat-recommend-api)
- [starcat-discovery-api](https://github.com/starcat-app/starcat-discovery-api)
<!-- starcat-promo:end -->

Official AI agent skill for reading and organizing repository knowledge stored in [Starcat](https://starcat.ink) through the cross-platform [Starcat CLI](https://github.com/starcat-app/starcat-cli) MCP bridge.

[简体中文](./README-ZH.md)

## What It Supports

- Inspect Star, AI token, knowledge-base, and RAG index statistics.
- Search repositories with keyword or semantic search.
- Read repository context, tags, private notes, status, READMEs, and cached AI summaries.
- Generate repository summaries through the user's configured Starcat AI provider.
- Add or update private notes, reading status, and tags after an explicit dry run and user authorization.

The skill does not access Starcat's SQLite database, CloudKit data, credential files, or Local API Keys directly. All business operations use the `starcat mcp` bridge and Starcat's capability model.

## Install

Clone the repository into the user-level skill directory for your agent:

```bash
# Codex
git clone https://github.com/starcat-app/starcat-skill "$HOME/.codex/skills/starcat-skill"

# Claude Code
git clone https://github.com/starcat-app/starcat-skill "$HOME/.claude/skills/starcat-skill"
```

Then install the Starcat CLI, restart or reload the agent, and verify the local bridge:

```bash
starcat doctor
```

If the CLI is not paired, open **Starcat → Settings → MCP Service**, copy the complete single-use pairing command, and execute it exactly as shown.

## Agent Workflow

1. Connect the agent's user-level MCP configuration to the absolute `starcat` executable with the single argument `mcp`.
2. Call `starcat.get_capabilities` before each workflow.
3. Use read-only tools for search, statistics, context, READMEs, and summaries.
4. For a write, call the relevant tool with `dry_run = true` first.
5. Apply the exact proposed change with `dry_run = false` only when the user has explicitly authorized it.
6. Read the repository context again to verify the result.

## Repository Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions, safety rules, and common workflows. |
| `agents/openai.yaml` | OpenAI agent display metadata and default prompt. |
| `references/commands.md` | Starcat MCP and CLI contract. |
| `references/workflows.md` | Reusable read, write, generation, and recovery workflows. |
| `scripts/validate_contract.py` | Contract consistency validation. |

## Validate

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contract.py --cli "$(command -v starcat)"
```
