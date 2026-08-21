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
            fields[key.strip()] = value.strip()
    return fields


def validate_skill(skill_dir: Path) -> list[str]:
    issues: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if fields.get("name") != skill_dir.name:
        issues.append("frontmatter name does not match directory")
    if not fields.get("description"):
        issues.append("frontmatter description is missing")
    if "TODO" in text or "FIXME" in text:
        issues.append("contains TODO or FIXME")
    if text.count("```") % 2:
        issues.append("unbalanced Markdown fences")
    if len(text.splitlines()) > 500:
        issues.append("SKILL.md exceeds 500 lines")
    if not (skill_dir / "agents" / "openai.yaml").is_file():
        issues.append("missing agents/openai.yaml")
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
    report: dict[str, object] = {"skills": {}, "dataset": None}
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

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
