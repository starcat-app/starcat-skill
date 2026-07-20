# Starcat Skill

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
python3 scripts/validate_contract.py
```
