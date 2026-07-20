---
name: starcat-skill
description: 通过跨平台 Starcat CLI 读取和整理 Starcat 中的 GitHub 仓库知识库。适用于查询项目、标签、私有笔记、阅读状态、README 与 AI 摘要，以及在用户授权时新增笔记、状态和标签；当用户提到 Starcat、整理收藏仓库、为项目添加笔记或标签、读取 Starcat 数据、生成仓库摘要时使用。
---

# Starcat Skill

## 唯一交互入口

只使用 `starcat` CLI 操作 Starcat。不要直接读取 SQLite、CloudKit、加密凭据文件或 Local API Key，也不要自行实现 HTTP/MCP 请求。

首次使用先运行：

```bash
starcat doctor --json
```

如果命令不存在，从 `https://github.com/dong4j/starcat-cli` 安装适合当前平台的已签名 Release；如果提示尚未配对，请用户在 Starcat「设置 → MCP 服务」中复制一次性配对命令。不要要求用户提供 Local API Key，不要输出或持久化 pairing URI。

## 工作规则

1. 每个工作流先运行 `starcat capabilities --json`，根据返回值判断私有笔记、写入、破坏性写入和摘要生成能力。
2. 已知 `owner/name` 时优先运行 `starcat repo context owner/name`，一次读取 repo、tags、note 和 summary。
3. 所有命令 stdout 都是 JSON；解析 JSON 再回答，不要根据人类文案猜测状态。
4. 写入命令默认 dry-run。先运行不带 `--apply` 的命令核对目标和变化，再决定是否正式执行。
5. 用户原请求已明确写入意图且 dry-run 与请求完全一致时，可以追加 `--apply`；否则先说明变化并征求确认。
6. 正式写入后重新运行 `starcat repo context owner/name` 验证结果。
7. `replace` 会替换仓库全部标签。除非用户明确要求并确认完整集合，否则使用 `add` 或 `remove`。
8. 不执行 GitHub 远端 star/unstar；当前写入只修改 Starcat 用户数据。

## 常用工作流

### 搜索与读取

```bash
starcat repo search "local first knowledge base" --scope all --limit 10
starcat repo search "适合 Swift 初学者的并发库" --semantic
starcat repo context apple/swift
starcat repo readme apple/swift
starcat tags list
```

README 可能很大，只在任务确实需要项目正文时读取。

### 笔记、状态和标签

笔记内容必须通过 stdin 传入，避免 Markdown、换行或敏感文本进入进程参数：

```bash
printf '%s' '## 使用场景

用于学习 Swift Concurrency。' | starcat repo note set apple/swift --stdin
```

确认 dry-run 后正式写入：

```bash
printf '%s' '## 使用场景

用于学习 Swift Concurrency。' | starcat repo note set apple/swift --stdin --apply
starcat repo status set apple/swift using --apply
starcat repo tags add apple/swift Swift 官方 --apply
```

### 摘要

读取缓存摘要：

```bash
starcat repo summary apple/swift
```

只有用户明确要求生成新摘要时才运行：

```bash
starcat repo summary apple/swift --generate
```

摘要生成可能消耗用户配置的 AI Provider 配额。只有用户明确允许 External Search 时才追加 `--allow-external-context`。外部 Agent 自己编写的文字不能冒充 Starcat 原生 AI 摘要；需要保存时应作为 Markdown 私有笔记并注明来源。

命令与边界详见 [references/commands.md](references/commands.md) 和 [references/workflows.md](references/workflows.md)。
