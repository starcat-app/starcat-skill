# Starcat CLI Command Contract

## Pairing and MCP

| Command | Purpose |
|---|---|
| `starcat pair --stdin` | Redeem a one-time invitation provided through stdin and wait for approval in Starcat |
| `starcat unpair` | Delete the current device profile and its operating-system credential |
| `starcat doctor --json` | Check pairing, connectivity, protocol compatibility, available tools, and capabilities |
| `starcat capabilities --json` | Read the current Starcat permission snapshot |
| `starcat mcp` | Bridge stdio JSON-RPC to Starcat MCP Streamable HTTP |

Never place a `starcat-pair://...` URI in command arguments. Run `starcat pair --stdin` and provide the URI only through stdin.

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
