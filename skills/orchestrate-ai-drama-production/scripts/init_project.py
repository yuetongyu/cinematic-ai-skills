#!/usr/bin/env python3
"""Create a traceable AI drama production project."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_ROOT / "assets" / "project-template" / "project.json"
STAGES = (
    "01-research",
    "02-script",
    "03-timing",
    "04-assets",
    "05-action",
    "06-storyboard",
    "07-shots",
    "08-continuity",
)
VISUAL_PROFILES = ("live-action-photoreal", "cinematic-ai-comic", "custom")


def slugify(value: str) -> str:
    slug = re.sub(r"[\W_]+", "-", value.lower(), flags=re.UNICODE).strip("-")
    return slug or "ai-drama-project"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an AI drama production project")
    parser.add_argument("title", help="project title")
    parser.add_argument("--output", type=Path, default=Path.cwd(), help="parent output directory")
    parser.add_argument("--project-id", help="stable project ID; defaults to PROJECT-001")
    parser.add_argument("--episode-id", default="EP001")
    parser.add_argument("--duration", type=float, default=90.0, help="target duration in seconds")
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--research-domain", default="original")
    parser.add_argument("--visual-profile", choices=VISUAL_PROFILES, default="cinematic-ai-comic")
    parser.add_argument("--target-platform", default="platform-neutral")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.duration <= 0:
        print("error: --duration must be positive", file=sys.stderr)
        return 2
    if args.fps <= 0:
        print("error: --fps must be positive", file=sys.stderr)
        return 2

    slug = slugify(args.title)
    destination = args.output.expanduser().resolve() / slug
    if destination.exists():
        print(f"error: destination exists: {destination}", file=sys.stderr)
        return 1

    destination.mkdir(parents=True)
    for stage in STAGES:
        (destination / stage).mkdir()

    manifest = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    manifest.update(
        {
            "project_id": args.project_id or "PROJECT-001",
            "title": args.title,
            "episode_id": args.episode_id,
            "target_duration_seconds": args.duration,
            "aspect_ratio": args.aspect_ratio,
            "fps": args.fps,
            "language": args.language,
            "research_domain": args.research_domain,
            "visual_profile": args.visual_profile,
            "target_platform": args.target_platform,
        }
    )
    (destination / "project.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    shutil.copy2(
        SKILL_ROOT / "assets" / "project-template" / "packet.example.json",
        destination / "packet.example.json",
    )
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
