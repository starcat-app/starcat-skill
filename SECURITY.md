# Security Policy

## 报告安全问题

请通过 [GitHub Security Advisories](https://github.com/starcat-app/starcat-skill/security/advisories/new) 报告 prompt injection、越权写入、dry-run 绕过、MCP 工具契约误导或敏感数据泄漏。不要在公开 Issue 中粘贴配对 URI、设备 token、私人笔记、仓库数据或其它 Starcat 用户信息。

## 安全边界

- Skill 必须在调用工具前读取当前 capabilities。
- 写操作必须先 dry-run，且只有用户明确授权后才能应用。
- Starcat App 仍是认证、权限、Pro entitlement 和审计的最终边界。
- Skill 不得要求 Agent 直接读取 Starcat 数据库或绕过 Starcat CLI/MCP。
