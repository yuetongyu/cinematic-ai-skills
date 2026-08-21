#!/usr/bin/env python3
"""Install one or more skills from this repository into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
AVAILABLE = tuple(sorted(path.name for path in SKILLS_ROOT.iterdir() if (path / "SKILL.md").is_file()))


def default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home).expanduser() if codex_home else Path.home() / ".codex") / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Cinematic AI Skills for Codex")
    parser.add_argument("--all", action="store_true", help="install every bundled skill")
    parser.add_argument("--skill", action="append", default=[], choices=AVAILABLE, help="skill to install; repeatable")
    parser.add_argument("--target", type=Path, default=default_target(), help="Codex skills directory")
    parser.add_argument("--force", action="store_true", help="replace an existing skill after backing it up")
    parser.add_argument("--dry-run", action="store_true", help="show planned operations without writing")
    parser.add_argument("--list", action="store_true", help="list bundled skills and exit")
    return parser.parse_args()


def unique_backup(destination: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = destination.with_name(f"{destination.name}.backup-{timestamp}")
    suffix = 1
    while candidate.exists():
        candidate = destination.with_name(f"{destination.name}.backup-{timestamp}-{suffix}")
        suffix += 1
    return candidate


def install_skill(name: str, target: Path, force: bool, dry_run: bool) -> tuple[bool, str]:
    source = SKILLS_ROOT / name
    destination = target / name
    if destination.exists() and not force:
        return False, f"exists: {destination} (use --force to update)"

    if dry_run:
        action = "replace" if destination.exists() else "install"
        return True, f"would {action}: {name} -> {destination}"

    target.mkdir(parents=True, exist_ok=True)
    staging = target / f".{name}.installing-{uuid.uuid4().hex}"
    backup: Path | None = None
    try:
        shutil.copytree(source, staging)
        if destination.exists():
            backup = unique_backup(destination)
            destination.rename(backup)
        staging.rename(destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if backup is not None and backup.exists() and not destination.exists():
            backup.rename(destination)
        raise

    message = f"installed: {name} -> {destination}"
    if backup is not None:
        message += f"; previous version backed up to {backup}"
    return True, message


def main() -> int:
    args = parse_args()
    if args.list:
        print("\n".join(AVAILABLE))
        return 0

    selected = list(AVAILABLE if args.all else dict.fromkeys(args.skill))
    if not selected:
        print("error: choose --all or at least one --skill", file=sys.stderr)
        return 2

    failed = False
    for name in selected:
        try:
            ok, message = install_skill(name, args.target.expanduser(), args.force, args.dry_run)
        except OSError as exc:
            ok, message = False, f"failed: {name}: {exc}"
        print(message, file=sys.stdout if ok else sys.stderr)
        failed = failed or not ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
