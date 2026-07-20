---
name: starcat-skill
description: Install, update, and use starcat-skill to read and organize GitHub repository knowledge stored in Starcat through the cross-platform Starcat CLI. Use when an agent needs to install this Skill; search repositories; inspect tags, private notes, reading status, READMEs, or AI summaries; or, with explicit user authorization, add or update notes, statuses, and tags. Trigger for requests involving Starcat data, organizing starred repositories, annotating a project, or generating a repository summary.
---

# Starcat Skill

## Install or update this Skill

When the user asks to install or update `starcat-skill`, perform the following workflow before using Starcat:

1. Identify the current AI agent and choose exactly one user-level destination:
   - Codex: `$HOME/.codex/skills/starcat-skill`
   - Claude Code: `$HOME/.claude/skills/starcat-skill`
2. If the destination does not exist, create its parent directory and clone `https://github.com/starcat-app/starcat-skill` into the destination.
3. If the destination is already a clean checkout of that repository, run `git -C <skill-path> pull --ff-only`.
4. If the destination exists but is not that repository, or contains uncommitted changes, stop and report the conflict. Never delete, overwrite, reset, or force-update it.
5. Confirm that `SKILL.md`, `agents/openai.yaml`, `references/commands.md`, and `references/workflows.md` exist.
6. Run `starcat --help` and confirm that pairing uses a complete URI argument and `capabilities` is called without a `--json` flag.
7. Reload or restart the AI agent so it can refresh its Skill registry. If the current session cannot reload Skills, report that installation succeeded but discovery still requires a restart. Never claim that the Skill was discovered without observing it.
8. After discovery, invoke `$starcat-skill` with a read-only verification request. Run `starcat doctor --json`, `starcat capabilities`, and one repository search with `--limit 2`. Do not execute write commands during installation verification.

Install only into the current agent's user-level Skill directory. Do not install into a project repository, request a Local API Key, modify unrelated files, or run destructive Git commands.

## Use the CLI as the only integration surface

Use only the `starcat` CLI to operate Starcat. Do not read SQLite, CloudKit, encrypted credential files, or Local API Keys directly. Do not implement custom HTTP or MCP requests.

Before the first operation, run:

```bash
starcat doctor --json
```

If the command is unavailable, install the appropriate official release from `https://github.com/starcat-app/starcat-cli`. If the CLI is not paired, instruct the user to open **Starcat > Settings > MCP Service** and copy the complete single-use pairing command. Execute the provided `starcat pair ...` command exactly as supplied. Never request a standalone pairing URI or Local API Key, and never print, persist, or reuse the pairing command.

## Follow the operating rules

1. Run `starcat capabilities` before each workflow. Use its JSON result to determine whether private notes, ordinary writes, destructive writes, and summary generation are available.
2. When `owner/name` is known, prefer `starcat repo context owner/name` to retrieve repository data, tags, the private note, and the summary in one call.
3. `capabilities`, repository, tag, and write commands return JSON. Parse that JSON before answering. `doctor` defaults to terminal-friendly text; use `starcat doctor --json` only when machine-readable diagnostics are needed.
4. Treat every write command as dry-run by default. Run it without `--apply` first and inspect the target and proposed changes.
5. Add `--apply` only when the user's original request clearly authorizes the write and the dry-run exactly matches that request. Otherwise, explain the proposed changes and ask for confirmation.
6. After an applied write, run `starcat repo context owner/name` again to verify the result.
7. Remember that `replace` overwrites all tags on the repository. Use `add` or `remove` unless the user explicitly provides and confirms the complete final tag set.
8. Do not star or unstar repositories on GitHub. Current write commands modify only Starcat user data.

## Use the common workflows

### Search and read

```bash
starcat repo search "local first knowledge base" --scope all --limit 10
starcat repo search "concurrency libraries for Swift beginners" --semantic
starcat repo context apple/swift
starcat repo readme apple/swift
starcat tags list
```

README content can be large. Retrieve it only when the task requires repository documentation.

### Manage notes, status, and tags

Pass note content through stdin so Markdown, line breaks, and sensitive text do not enter process arguments:

```bash
printf '%s' '## Use case

Use this repository to learn Swift Concurrency.' | starcat repo note set apple/swift --stdin
```

After reviewing the dry-run, apply the write:

```bash
printf '%s' '## Use case

Use this repository to learn Swift Concurrency.' | starcat repo note set apple/swift --stdin --apply
starcat repo status set apple/swift using --apply
starcat repo tags add apple/swift Swift Official --apply
```

### Work with summaries

Read the cached summary:

```bash
starcat repo summary apple/swift
```

Generate a new summary only when the user explicitly requests it:

```bash
starcat repo summary apple/swift --generate
```

Summary generation may consume quota from the user's configured AI provider. Add `--allow-external-context` only when the user explicitly permits External Search. Never represent text written by the external agent as a native Starcat AI summary. If the user wants to save agent-written content, store it as a Markdown private note and identify its source.

Read [references/commands.md](references/commands.md) when checking command details. Read [references/workflows.md](references/workflows.md) when reusing workflows or recovering from connection failures.
