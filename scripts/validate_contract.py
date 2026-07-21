#!/usr/bin/env python3
"""Validate starcat-skill structure and its contract with the current CLI."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

import yaml


REQUIRED_HELP_TEXT = (
    "pair [one-time-pairing-URI]",
    "doctor                       Check pairing, connection, tools, and capabilities",
    "capabilities                  Print Starcat capabilities as JSON",
    "stats                         Show Starcat repository, AI usage, and RAG statistics",
    "repo note set <owner/name> [--apply]",
)


def parse_arguments() -> argparse.Namespace:
    """Accept a CLI path so CI can test releases and local runs can test builds."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True, help="path to the starcat executable")
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

def main() -> None:
    """Run all Skill structure and CLI contract checks."""
    arguments = parse_arguments()
    root = Path(__file__).resolve().parent.parent
    validate_frontmatter(root)
    validate_cli_contract(Path(arguments.cli).expanduser().resolve())
    print("starcat-skill validation passed")


if __name__ == "__main__":
    main()
