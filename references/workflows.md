# Starcat Skill Workflows

## Add a private note to a repository

```bash
starcat capabilities
starcat repo context owner/repo
printf '%s' "$NOTE_CONTENT" | starcat repo note set owner/repo --stdin
printf '%s' "$NOTE_CONTENT" | starcat repo note set owner/repo --stdin --apply
starcat repo context owner/repo
```

Do not repurpose system variables such as `$HOME` for note content. Do not allow untrusted backticks or `$()` expressions to be expanded by the shell.

## Organize tags incrementally

```bash
starcat repo context owner/repo
starcat repo tags add owner/repo Swift macOS
starcat repo tags add owner/repo Swift macOS --apply
starcat repo context owner/repo
```

Prefer `add` and `remove`. Use `replace` only when the user explicitly provides the complete final tag set.

## Generate a summary

```bash
starcat capabilities
starcat repo summary owner/repo --generate
starcat repo context owner/repo
```

Use external context only when the user explicitly authorizes External Search:

```bash
starcat repo summary owner/repo --generate --allow-external-context
```

## Recover from connection failures

Check these conditions in order:

1. Run `starcat doctor --json` and inspect whether the CLI reports missing pairing, invalid credentials, protocol incompatibility, or an unavailable Starcat app.
2. Ask the user to confirm that Starcat is running and MCP Service is enabled.
3. If credentials are invalid, instruct the user to generate and copy a new complete single-use pairing command from Starcat. Execute the provided `starcat pair ...` command exactly as supplied. Never request a Local API Key or repeat the command in a response or log.
4. From a remote device, connect only to the HTTPS endpoint contained in the pairing invitation. Never downgrade the connection to LAN HTTP manually.
