#!/usr/bin/env python3
"""隔离真实凭据，校验 Skill 文档、CLI help 与可选的 App 工具登记。"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

import yaml


REQUIRED_HELP_TEXT = (
    "pair [one-time-pairing-URI]",
    "doctor                       Check pairing, connection, tools, and capabilities",
    "capabilities                  Print Starcat capabilities as JSON",
    "stats                         Show Starcat repository, AI usage, and RAG statistics",
    "repo note set <owner/name> [--apply]",
    "tools list [--json]",
    "tools describe <name> [--json]",
    "tools call <name> [--input FILE|-] [--apply]",
    "resources list [--json]",
    "resources read <uri>",
)


def parse_arguments() -> argparse.Namespace:
    """Accept a CLI path so CI can test releases and local runs can test builds."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True, help="path to the starcat executable")
    parser.add_argument("--app-root", type=Path, help="可选：App 源码根目录，核对文档使用的工具名称")
    return parser.parse_args()


def validate_frontmatter(root: Path) -> None:
    """Validate discovery metadata so agents can load the Skill reliably."""
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        raise ValueError("SKILL.md must contain complete YAML frontmatter")

    frontmatter_text = content.split("\n---\n", maxsplit=1)[0][4:]
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    if set(frontmatter) != {"name", "description"}:
        raise ValueError("SKILL.md frontmatter may contain only name and description")
    if frontmatter["name"] != "starcat-skill":
        raise ValueError("SKILL.md name must be starcat-skill")
    if not isinstance(frontmatter["description"], str) or not frontmatter["description"].strip():
        raise ValueError("SKILL.md description must not be empty")


def run_cli(cli: Path, arguments: list[str], home: str) -> subprocess.CompletedProcess[str]:
    """Run CLI checks in an isolated HOME to protect real pairing data."""
    environment = os.environ.copy()
    environment["HOME"] = home
    environment["STARCAT_NO_UPDATE_CHECK"] = "1"
    return subprocess.run(
        [str(cli), *arguments],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


def validate_cli_contract(cli: Path) -> None:
    """Treat CLI help and argument parsing as the command contract source of truth."""
    if not cli.is_file() or not os.access(cli, os.X_OK):
        raise ValueError(f"starcat CLI does not exist or is not executable: {cli}")

    with tempfile.TemporaryDirectory(prefix="starcat-skill-contract-") as home:
        help_result = run_cli(cli, ["--help"], home)
        if help_result.returncode != 0:
            raise ValueError(f"starcat --help failed: {help_result.stderr.strip()}")
        for required in REQUIRED_HELP_TEXT:
            if required not in help_result.stdout:
                raise ValueError(f"starcat --help is missing expected contract: {required}")
        for topic, required in {
            "tools": ("list", "describe", "call", "--input", "--apply"),
            "resources": ("list", "read"),
            "repo": ("get", "by-tag", "star", "unstar"),
            "stats": ("--json",),
        }.items():
            result = run_cli(cli, ["help", topic], home)
            if result.returncode != 0 or any(text not in result.stdout for text in required):
                raise ValueError(f"starcat help {topic} does not match the Skill contract")


def validate_app_tools(root: Path, app_root: Path | None) -> None:
    """源码登记检查不冒充真实 App 连接；运行时权限与模块仍须通过目录发现。"""
    documents = [
        root / "SKILL.md", root / "references/commands.md", root / "references/workflows.md"
    ]
    for document in documents:
        content = document.read_text(encoding="utf-8")
        if "Ordinary CLI business commands" in content or "must use `starcat mcp` for business" in content:
            raise ValueError(f"{document.name} contains an obsolete MCP-only restriction")
    if app_root is None:
        return
    directory = app_root / "Starcat/Features/MCP"
    registry = (directory / "StarcatMCPToolRegistry.swift").read_text(encoding="utf-8")
    catalog = (directory / "StarcatMCPPublicCatalog.swift").read_text(encoding="utf-8")
    registered = set(re.findall(r'name:\s*"starcat\.([a-z][a-z0-9_]*)"', registry))
    registered.update(re.findall(r'\.init\(name:\s*"([a-z][a-z0-9_]*)"', catalog))
    used = set()
    for document in documents:
        used.update(re.findall(r'\bstarcat\.([a-z][a-z0-9_]*)', document.read_text(encoding="utf-8")))
    missing = used - registered
    if missing:
        raise ValueError(f"Skill references unregistered App tools: {', '.join(sorted(missing))}")

def main() -> None:
    """Run all Skill structure and CLI contract checks."""
    arguments = parse_arguments()
    root = Path(__file__).resolve().parent.parent
    validate_frontmatter(root)
    validate_cli_contract(Path(arguments.cli).expanduser().resolve())
    validate_app_tools(root, arguments.app_root)
    print("starcat-skill validation passed")


if __name__ == "__main__":
    main()
