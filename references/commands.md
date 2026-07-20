# Starcat MCP and CLI Contract

## Pairing and transport

| Command | Purpose |
|---|---|
| `starcat pair "<starcat-pair://...>"` | Execute the complete single-use pairing command copied from Starcat and wait for in-app approval |
| `starcat unpair` | Delete the current device profile and its operating-system credential |
| `starcat doctor` | Check pairing, connectivity, protocol compatibility, tools, and capabilities using terminal-friendly text |
| `starcat doctor --json` | Print the same diagnostic result as machine-readable JSON |
| `starcat mcp` | Bridge stdio JSON-RPC to Starcat MCP Streamable HTTP |

For pairing, instruct the user to copy the complete command from Starcat and execute it exactly as provided. Never request a standalone `starcat-pair://...` URI or Local API Key. Never print, persist, or reuse the pairing command.

The agent must use `starcat mcp` for business operations. Ordinary CLI business commands are human-facing shortcuts and are not the Skill's data transport.

## Statistics tools

| MCP tool | Purpose |
|---|---|
| `starcat.get_overview_statistics` | Read starred repository count, knowledge-base project count, all-time AI usage, and RAG index health |
| `starcat.get_ai_usage_statistics` | Read token/call statistics filtered by time range, feature, provider, or model |
| `starcat.get_knowledge_base_statistics` | Read knowledge-base organization, source coverage, exclusions, and chunk/index health |

`starcat.get_ai_usage_statistics` accepts:

- `time_range`: `today`, `seven_days`, `thirty_days`, or `all`; default `all`.
- `feature`: optional Starcat feature raw value.
- `provider_id`: optional provider profile identifier.
- `model`: optional model name.

Statistics are local, read-only aggregates. They never include prompts, responses, API keys, chunk bodies, or raw error text. Private-note counts are omitted unless `private_notes_read` is enabled.

## Repository read tools

| MCP tool | Purpose |
|---|---|
| `starcat.get_capabilities` | Read the current privacy, statistics, generation, and write permissions |
| `starcat.search_repos` | Run local keyword search with `scope` and `limit` |
| `starcat.semantic_search` | Run semantic repository search |
| `starcat.get_repo_context` | Retrieve repository data, tags, optional private note, and cached summary together |
| `starcat.get_readme` | Read the cached README |
| `starcat.get_repo_summary` | Read the cached summary |
| `starcat.list_tags` | List all tags |

## Generation and write tools

| MCP tool | Purpose and constraints |
|---|---|
| `starcat.generate_repo_summary` | Generate a summary with the user's Starcat AI provider; this may consume quota |
| `starcat.upsert_repo_note` | Set or clear a Markdown private note |
| `starcat.set_repo_status` | Set `status` to `unread`, `read`, or `using` |
| `starcat.add_repo_tags` | Add tags incrementally and create missing tags when permitted |
| `starcat.remove_repo_tags` | Remove tags incrementally |
| `starcat.set_repo_tags` | Replace all tags; require destructive-write permission |
| `starcat.create_tag` | Create a tag with optional color and icon values |

Every write tool must first be called with `dry_run = true`. After an authorized write with `dry_run = false`, retrieve the repository context again to verify the stored result.

## Human-facing statistics commands

These commands call the same MCP tools but render terminal-friendly text:

```bash
starcat stats
starcat stats ai --range 30d
starcat stats knowledge
```

They intentionally do not accept `--json`. Agents use the structured MCP tools instead.
