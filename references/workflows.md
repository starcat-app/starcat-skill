# Starcat Skill Workflows

## Answer a statistics question

1. Call `starcat.get_capabilities` and confirm `statistics_read` is true.
2. For a general question, call `starcat.get_overview_statistics` once.
3. For token analysis, call `starcat.get_ai_usage_statistics` with an explicit `time_range` and any requested filters.
4. For project, source, or chunk analysis, call `starcat.get_knowledge_base_statistics`.
5. State the scope in the answer: current Starred repositories, `in_library` knowledge-base projects, or the selected AI usage window.

Do not confuse `starred_repository_count` with a repository's public `github_stars`. Do not infer zero usage from calls where the provider did not return token metadata.

## Add a private note to a repository

1. Call `starcat.get_capabilities` and confirm private notes and local writes are enabled.
2. Call `starcat.get_repo_context` for the target.
3. Call `starcat.upsert_repo_note` with the Markdown `content` and `dry_run = true`.
4. If the user authorized the exact change, repeat with `dry_run = false`.
5. Call `starcat.get_repo_context` again and verify the stored note.

## Organize tags incrementally

1. Call `starcat.get_repo_context`.
2. Prefer `starcat.add_repo_tags` or `starcat.remove_repo_tags`, first with `dry_run = true`.
3. Apply the exact authorized change with `dry_run = false`.
4. Call `starcat.get_repo_context` again.

Use `starcat.set_repo_tags` only when the user explicitly provides the complete final tag set and destructive writes are enabled.

## Generate a summary

1. Call `starcat.get_capabilities` and confirm `ai_summary_generation` is enabled.
2. Call `starcat.get_repo_summary` first to check the cache.
3. Call `starcat.generate_repo_summary` only when the user explicitly requests generation.
4. Set `allow_external_context = true` only when the user explicitly authorizes External Search.

## Recover from connection failures

Check these conditions in order:

1. Run `starcat doctor` and inspect whether the CLI reports missing pairing, invalid credentials, protocol incompatibility, or an unavailable Starcat app.
2. Ask the user to confirm that Starcat is running and MCP Service is enabled.
3. Confirm the agent's user-level MCP configuration launches the absolute Starcat executable with the single argument `mcp`.
4. If credentials are invalid, instruct the user to generate and copy a new complete single-use pairing command from Starcat. Execute the provided `starcat pair ...` command exactly as supplied. Never request a Local API Key or repeat the command in a response or log.
5. From a remote device, connect only to the HTTPS endpoint contained in the pairing invitation. Never downgrade the connection to LAN HTTP manually.
