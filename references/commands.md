# Starcat CLI Command Contract

## Pairing and MCP

| Command | Purpose |
|---|---|
| `starcat pair "<starcat-pair://...>"` | Execute the complete single-use pairing command copied from Starcat and wait for in-app approval |
| `starcat unpair` | Delete the current device profile and its operating-system credential |
| `starcat doctor` | Check pairing, connectivity, protocol compatibility, tools, and capabilities using terminal-friendly text |
| `starcat doctor --json` | Print the same diagnostic result as machine-readable JSON |
| `starcat capabilities` | Read the current Starcat permission snapshot as JSON |
| `starcat mcp` | Bridge stdio JSON-RPC to Starcat MCP Streamable HTTP |

For pairing, instruct the user to copy the complete command from Starcat and execute it exactly as provided. Never request a standalone `starcat-pair://...` URI or Local API Key. Never print, persist, or reuse the pairing command.

## Read operations

| Command | Purpose |
|---|---|
| `starcat repo search <query>` | Run keyword search with optional `--scope`, `--limit`, or `--semantic` flags |
| `starcat repo context <owner/name>` | Retrieve repository data, tags, the private note, and the summary together |
| `starcat repo readme <owner/name>` | Read the cached README |
| `starcat repo summary <owner/name>` | Read the cached summary |
| `starcat tags list` | List all tags |

## Generation and write operations

| Command | Purpose and constraints |
|---|---|
| `starcat repo summary <owner/name> --generate` | Generate a summary with the user's Starcat AI provider; this may consume quota |
| `starcat repo note set <owner/name> --stdin` | Set or clear a Markdown private note; read content only from stdin |
| `starcat repo status set <owner/name> <status>` | Set `status` to `unread`, `read`, or `using` |
| `starcat repo tags add <owner/name> <tag...>` | Add tags incrementally and create missing tags when permitted |
| `starcat repo tags remove <owner/name> <tag...>` | Remove tags incrementally |
| `starcat repo tags replace <owner/name> <tag...>` | Replace all tags; require destructive-write permission |
| `starcat tag create <name>` | Create a tag with optional `--color` and `--icon` values |

Every write command is a dry-run without `--apply`. After applying a write, retrieve the repository context again to verify the stored result.
