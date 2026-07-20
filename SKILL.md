---
name: starcat-skill
description: Install, update, and use starcat-skill to read and organize GitHub repository knowledge stored in Starcat through the cross-platform Starcat MCP bridge. Use when an agent needs to install this Skill; query Star, AI token, knowledge-base, or RAG chunk statistics; search repositories; inspect tags, private notes, reading status, READMEs, or AI summaries; or, with explicit user authorization, add or update notes, statuses, and tags. Trigger for requests involving Starcat data, usage statistics, knowledge-base health, organizing starred repositories, annotating a project, or generating a repository summary.
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
6. Run `starcat --help` and confirm that pairing uses a complete URI argument, `starcat mcp` is available, and statistics commands do not advertise a `--json` flag.
7. Reload or restart the AI agent so it can refresh its Skill registry. If the current session cannot reload Skills, report that installation succeeded but discovery still requires a restart. Never claim that the Skill was discovered without observing it.
8. After discovery, invoke `$starcat-skill` with a read-only verification request. Run `starcat doctor`, connect the agent to the user-level MCP server command `starcat mcp`, call `starcat.get_capabilities`, and run one `starcat.search_repos` request with `limit = 2`. Do not execute write tools during installation verification.

Install only into the current agent's user-level Skill directory. Do not install into a project repository, request a Local API Key, modify unrelated files, or run destructive Git commands.

## Use the MCP bridge as the business integration surface

Use the user-level MCP server command `starcat mcp` to operate Starcat. The CLI bridge owns pairing credentials, TLS verification, and MCP transport. Do not read SQLite, CloudKit, encrypted credential files, or Local API Keys directly. Do not implement custom HTTP or JSON-RPC requests, and do not shell out to ordinary business commands when the same MCP tool is available.

Before the first operation, run:

```bash
starcat doctor
```

If the command is unavailable, install the appropriate official release from `https://github.com/starcat-app/starcat-cli`. If the CLI is not paired, instruct the user to open **Starcat > Settings > MCP Service** and copy the complete single-use pairing command. Execute the provided `starcat pair ...` command exactly as supplied. Never request a standalone pairing URI or Local API Key, and never print, persist, or reuse the pairing command.

After pairing, configure the current agent's user-level MCP server to launch the absolute `starcat` executable with the single argument `mcp`, then reload the agent. Treat stdout from `starcat mcp` as protocol-only JSON-RPC; never mix prompts or diagnostics into it.

## Follow the operating rules

1. Call `starcat.get_capabilities` before each workflow. Use its structured result to determine whether statistics, private notes, ordinary writes, destructive writes, and summary generation are available.
2. For common counts, call `starcat.get_overview_statistics` once. Use `starcat.get_ai_usage_statistics` for filtered token/call analysis and `starcat.get_knowledge_base_statistics` for detailed project, source, and RAG chunk health.
3. When `owner/name` is known, prefer `starcat.get_repo_context` to retrieve repository data, tags, the private note, and the summary in one call.
4. Treat every write tool as dry-run by default. Call it with `dry_run = true` first and inspect the target and proposed changes.
5. Call the write again with `dry_run = false` only when the user's original request clearly authorizes the write and the dry-run exactly matches that request. Otherwise, explain the proposed changes and ask for confirmation.
6. After a write, call `starcat.get_repo_context` again to verify the result.
7. Remember that `starcat.set_repo_tags` overwrites all tags on the repository. Use `starcat.add_repo_tags` or `starcat.remove_repo_tags` unless the user explicitly provides and confirms the complete final tag set.
8. Do not star or unstar repositories on GitHub. Current write tools modify only Starcat user data.

## Use the common workflows

### Inspect statistics

- Call `starcat.get_overview_statistics` for Star count, knowledge-base project count, all-time AI token usage, and current RAG index health.
- Call `starcat.get_ai_usage_statistics` with `time_range = today | seven_days | thirty_days | all` and optional `feature`, `provider_id`, or `model` filters.
- Call `starcat.get_knowledge_base_statistics` for organization, language/tag distribution, source coverage, excluded chunks, and ready/pending/failed/stale index counts.

Treat `starred_repository_count` as the number of repositories the user currently stars. Treat `github_stars` in `top_starred_repositories` as each repository's public GitHub popularity; never combine these two meanings. Missing provider usage is represented by `calls_with_usage < call_count`, not by assuming every missing call consumed zero tokens.

### Search and read

- Call `starcat.search_repos` with `query = "local first knowledge base"`, `scope = all`, and `limit = 10`.
- Call `starcat.semantic_search` for semantic discovery.
- Call `starcat.get_repo_context` for `apple/swift`.
- Call `starcat.get_readme` only when repository documentation is required.
- Call `starcat.list_tags` to inspect user-defined tags.

README content can be large. Retrieve it only when the task requires repository documentation.

### Manage notes, status, and tags

Call `starcat.upsert_repo_note`, `starcat.set_repo_status`, and tag tools through MCP. Send Markdown as the `content` field instead of placing sensitive text in a shell argument. First use `dry_run = true`; after authorization, repeat the exact call with `dry_run = false`.

### Work with summaries

Call `starcat.get_repo_summary` to read the cached summary. Call `starcat.generate_repo_summary` only when the user explicitly requests generation.

Summary generation may consume quota from the user's configured AI provider. Add `--allow-external-context` only when the user explicitly permits External Search. Never represent text written by the external agent as a native Starcat AI summary. If the user wants to save agent-written content, store it as a Markdown private note and identify its source.

Read [references/commands.md](references/commands.md) when checking MCP tool and terminal command details. Read [references/workflows.md](references/workflows.md) when reusing workflows or recovering from connection failures.
