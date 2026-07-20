# Starcat Skill 工作流

## 为一个仓库新增笔记

```bash
starcat capabilities --json
starcat repo context owner/repo
printf '%s' "$NOTE_CONTENT" | starcat repo note set owner/repo --stdin
printf '%s' "$NOTE_CONTENT" | starcat repo note set owner/repo --stdin --apply
starcat repo context owner/repo
```

不要把 `$NOTE_CONTENT` 声明成 `$HOME` 等系统变量，也不要让 shell 展开来源不明的反引号或 `$()`。

## 增量整理标签

```bash
starcat repo context owner/repo
starcat repo tags add owner/repo Swift macOS
starcat repo tags add owner/repo Swift macOS --apply
starcat repo context owner/repo
```

优先 `add` / `remove`。只有用户明确给出“最终完整标签集合”时使用 `replace`。

## 生成摘要

```bash
starcat capabilities --json
starcat repo summary owner/repo --generate
starcat repo context owner/repo
```

只有用户明确授权外部检索时使用：

```bash
starcat repo summary owner/repo --generate --allow-external-context
```

## 无法连接时

按顺序检查：

1. `starcat doctor --json` 是否提示未配对、凭据失效、协议不兼容或 Starcat 不在线。
2. 让用户确认 Starcat 正在运行并开启 MCP Service。
3. 凭据失效时重新生成一次性配对命令，不要求用户复制 Local API Key。
4. 远程设备只连接 invitation 提供的 HTTPS endpoint；不要手动降级成局域网 HTTP。
