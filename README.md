# Starcat Skill

Official AI agent skill for reading and organizing repository knowledge stored in [Starcat](https://starcat.ink) through the cross-platform [Starcat CLI](https://github.com/starcat-app/starcat-cli).

[简体中文](./README-ZH.md)

## What It Supports

- Search repositories with keyword or semantic search.
- Read repository context, tags, private notes, reading status, READMEs, and cached AI summaries.
- Generate repository summaries through the user's configured Starcat AI provider.
- Add or update private notes, reading status, and tags after an explicit dry run and user authorization.

The skill does not access Starcat's SQLite database, CloudKit data, credential files, or Local API Keys directly. All operations go through the official `starcat` CLI and Starcat's capability model.

## Install

Clone the repository into the user-level skill directory for your agent:

```bash
# Codex
git clone https://github.com/starcat-app/starcat-skill "$HOME/.codex/skills/starcat-skill"

# Claude Code
git clone https://github.com/starcat-app/starcat-skill "$HOME/.claude/skills/starcat-skill"
```

Then install the Starcat CLI, restart or reload the agent, and verify the connection:

```bash
starcat doctor --json
starcat capabilities
starcat repo search "local first knowledge base" --scope all --limit 2
```

If the CLI is not paired, open **Starcat → Settings → MCP Service**, copy the complete single-use pairing command, and execute it exactly as shown.

## Agent Workflow

1. Run `starcat capabilities` before each workflow.
2. Use read-only commands for search, repository context, READMEs, tags, and summaries.
3. Run write commands without `--apply` first and inspect the dry-run result.
4. Repeat the exact command with `--apply` only when the user has explicitly authorized the proposed change.
5. Read the repository context again to verify the stored result.

## Repository Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions, safety rules, and common workflows. |
| `agents/openai.yaml` | OpenAI agent display metadata and default prompt. |
| `references/commands.md` | Starcat CLI command contract. |
| `references/workflows.md` | Reusable read, write, generation, and recovery workflows. |
| `scripts/validate_contract.py` | Skill and CLI contract validation. |

## Validate

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contract.py --cli /absolute/path/to/starcat
```
