---
name: starcat-skill
description: Read and organize GitHub repository knowledge stored in Starcat through the cross-platform Starcat CLI. Use when an agent needs to search repositories; inspect tags, private notes, reading status, READMEs, or AI summaries; or, with user authorization, add or update notes, statuses, and tags. Trigger for requests involving Starcat data, organizing starred repositories, annotating a project, or generating a repository summary.
---

# Starcat Skill

## Use the CLI as the only integration surface

Use only the `starcat` CLI to operate Starcat. Do not read SQLite, CloudKit, encrypted credential files, or Local API Keys directly. Do not implement custom HTTP or MCP requests.

Before the first operation, run:

```bash
starcat doctor --json
```

If the command is unavailable, install the appropriate official release from `https://github.com/dong4j/starcat-cli`. If the CLI is not paired, ask the user to copy one-time pairing instructions from **Starcat > Settings > MCP Service**, run `starcat pair --stdin`, and provide the URI only through stdin. Never request a Local API Key, print the pairing URI, persist it, or place it in command arguments.

## Follow the operating rules

1. Run `starcat capabilities --json` before each workflow. Use its result to determine whether private notes, writes, destructive writes, and summary generation are available.
2. When `owner/name` is known, prefer `starcat repo context owner/name` to retrieve repository data, tags, the private note, and the summary in one call.
3. Treat stdout from every command as JSON. Parse the JSON before answering; do not infer state from human-readable messages.
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

See [references/commands.md](references/commands.md) for the command contract and [references/workflows.md](references/workflows.md) for reusable workflows and recovery steps.
