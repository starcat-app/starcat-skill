# 贡献指南

此仓库维护 Starcat 官方 AI Agent Skill。说明文本使用中文；命令、路径、工具名、参数和 YAML key 保持技术字面量。

修改契约、工作流或工具说明后运行：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contract.py
```

- `SKILL.md`、`references/` 和 `agents/openai.yaml` 必须与当前 Starcat CLI/MCP 契约一致。
- 写操作示例必须保留 dry-run 优先和用户明确授权边界。
- 不提交配对 URI、设备 token、私人笔记、仓库数据或其它 Starcat 用户信息。
