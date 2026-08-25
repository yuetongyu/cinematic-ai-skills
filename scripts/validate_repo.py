#!/usr/bin/env python3
"""Validate repository skill structure without third-party dependencies."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
PRIVATE_PATH = re.compile(r"(?:/Users/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+)")
REFERENCE_LINK = re.compile(r"\]\((references/[^)#]+)")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = unquote(value.strip())
    return fields


def validate_skill(skill_dir: Path) -> list[str]:
    issues: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    unexpected = sorted(set(fields) - ALLOWED_FRONTMATTER)
    if unexpected:
        issues.append(f"unexpected frontmatter fields: {', '.join(unexpected)}")
    if fields.get("name") != skill_dir.name:
        issues.append("frontmatter name does not match directory")
    name = fields.get("name", "")
    if not SKILL_NAME.fullmatch(name) or len(name) > 64:
        issues.append("frontmatter name must be hyphen-case and at most 64 characters")
    description = fields.get("description", "")
    if not description:
        issues.append("frontmatter description is missing")
    elif len(description) > 1024 or "<" in description or ">" in description:
        issues.append("frontmatter description exceeds limits or contains angle brackets")
    if "TODO" in text or "FIXME" in text:
        issues.append("contains TODO or FIXME")
    if text.count("```") % 2:
        issues.append("unbalanced Markdown fences")
    if len(text.splitlines()) > 500:
        issues.append("SKILL.md exceeds 500 lines")
    agent_file = skill_dir / "agents" / "openai.yaml"
    if not agent_file.is_file():
        issues.append("missing agents/openai.yaml")
    else:
        agent_text = agent_file.read_text(encoding="utf-8")
        interface: dict[str, str] = {}
        for line in agent_text.splitlines():
            if not line.startswith("  "):
                continue
            key, separator, value = line.strip().partition(":")
            if separator:
                interface[key] = unquote(value.strip())
        display_name = interface.get("display_name", "")
        short_description = interface.get("short_description", "")
        default_prompt = interface.get("default_prompt", "")
        if not display_name:
            issues.append("agents/openai.yaml missing display_name")
        if not 25 <= len(short_description) <= 100:
            issues.append("agents/openai.yaml short_description must be 25-100 characters")
        if f"${skill_dir.name}" not in default_prompt:
            issues.append("agents/openai.yaml default_prompt must mention the skill by $name")
    for relative in REFERENCE_LINK.findall(text):
        if not (skill_dir / relative).is_file():
            issues.append(f"missing referenced file: {relative}")
    for file in skill_dir.rglob("*"):
        if not file.is_file() or file.name == "world-mythology-dataset.md":
            continue
        content = file.read_text(encoding="utf-8", errors="ignore")
        if PRIVATE_PATH.search(content):
            issues.append(f"private absolute path in {file.relative_to(skill_dir)}")
    return issues


def main() -> int:
    report: dict[str, object] = {"skills": {}, "dataset": None, "workflow_example": None}
    failed = False
    for skill_dir in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        issues = validate_skill(skill_dir)
        report["skills"][skill_dir.name] = {"ok": not issues, "issues": issues}
        failed = failed or bool(issues)

    mythology_query = SKILLS_ROOT / "craft-world-mythology" / "scripts" / "query_mythology.py"
    result = subprocess.run(
        [sys.executable, str(mythology_query), "validate", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        report["dataset"] = json.loads(result.stdout)
        failed = failed or not report["dataset"].get("ok", False)
    else:
        report["dataset"] = {"ok": False, "error": result.stderr.strip()}
        failed = True

    project_validator = (
        SKILLS_ROOT
        / "orchestrate-ai-drama-production"
        / "scripts"
        / "validate_project.py"
    )
    workflow_example = ROOT / "examples" / "yaksha-90s-demo"
    if project_validator.is_file() and workflow_example.is_dir():
        result = subprocess.run(
            [sys.executable, str(project_validator), str(workflow_example), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            report["workflow_example"] = json.loads(result.stdout)
        else:
            report["workflow_example"] = {
                "ok": False,
                "error": result.stderr.strip() or result.stdout.strip(),
            }
            failed = True
    else:
        report["workflow_example"] = {
            "ok": False,
            "error": "missing production validator or workflow example",
        }
        failed = True

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
