#!/usr/bin/env python3
"""Validate AI drama project manifests and production packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"
PACKET_TYPES = {
    "RESEARCH_PACKET",
    "SCRIPT_PACKET",
    "TIMING_MAP",
    "ASSET_REGISTRY",
    "ACTION_PACKET",
    "STORYBOARD_PACKET",
    "SHOT_PACKET",
    "CONTINUITY_LEDGER",
}
STATUSES = {"draft", "review", "locked", "superseded"}
BLOCK_ID = re.compile(r"^[A-Z][A-Z0-9-]*\d{3}$")
DEPENDENCY = re.compile(r"^([A-Z][A-Z0-9-]*\d{3})@(\d+)$")
REQUIRED_PACKET_FIELDS = {
    "schema_version",
    "packet_type",
    "block_id",
    "revision",
    "project_id",
    "episode_id",
    "source_revision",
    "depends_on",
    "status",
    "locked_fields",
    "controlled_fields",
    "open_fields",
    "assumptions",
    "continuity_in",
    "continuity_out",
    "change_log",
    "payload",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an AI drama production project")
    parser.add_argument("project", type=Path, help="project directory")
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    return parser.parse_args()


def load_json(path: Path, issues: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        issues.append(f"{path}: root must be an object")
        return None
    return value


def field_overlap(packet: dict[str, Any]) -> set[str]:
    locked_value = packet.get("locked_fields", [])
    controlled_value = packet.get("controlled_fields", {})
    opened_value = packet.get("open_fields", [])
    locked = set(locked_value) if isinstance(locked_value, list) else set()
    controlled = set(controlled_value) if isinstance(controlled_value, dict) else set()
    opened = set(opened_value) if isinstance(opened_value, list) else set()
    return (locked & controlled) | (locked & opened) | (controlled & opened)


def list_items(value: Any) -> list[Any]:
    """Return list values while keeping malformed packets non-fatal."""
    return value if isinstance(value, list) else []


def numeric_range(value: Any) -> tuple[float, float] | None:
    if (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, (int, float)) for item in value)
        and value[0] < value[1]
    ):
        return float(value[0]), float(value[1])
    return None


def validate_timing(
    path: Path,
    packet: dict[str, Any],
    target_duration: float | None,
    issues: list[str],
) -> None:
    payload = packet.get("payload", {})
    if not isinstance(payload, dict):
        return
    total = payload.get("total_duration_seconds")
    segments = payload.get("segments", [])
    if not isinstance(total, (int, float)) or total <= 0:
        issues.append(f"{path}: TIMING_MAP needs positive total_duration_seconds")
    if not isinstance(segments, list):
        issues.append(f"{path}: TIMING_MAP segments must be a list")
        return
    valid_ranges: list[tuple[float, float, int]] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            issues.append(f"{path}: segment {index} must be an object")
            continue
        start, end = segment.get("start"), segment.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start >= end:
            issues.append(f"{path}: segment {index} must have numeric start < end")
        elif isinstance(total, (int, float)) and end > total:
            issues.append(f"{path}: segment {index} ends after total duration")
        else:
            valid_ranges.append((float(start), float(end), index))
    if isinstance(total, (int, float)) and isinstance(target_duration, (int, float)):
        if abs(float(total) - float(target_duration)) > 0.001:
            issues.append(f"{path}: total duration differs from project.json")
    if valid_ranges:
        ordered = sorted(valid_ranges)
        if abs(ordered[0][0]) > 0.001:
            issues.append(f"{path}: visual timeline must start at 0")
        for previous, current in zip(ordered, ordered[1:]):
            delta = current[0] - previous[1]
            if abs(delta) > 0.001:
                relation = "gap" if delta > 0 else "overlap"
                issues.append(
                    f"{path}: visual timeline has {relation} between "
                    f"segments {previous[2]} and {current[2]}"
                )
        if isinstance(total, (int, float)) and abs(ordered[-1][1] - float(total)) > 0.001:
            issues.append(f"{path}: visual timeline does not close at total duration")


def dependency_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in visiting:
            start = stack.index(node)
            cycles.append(stack[start:] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, set()):
            visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return cycles


def main() -> int:
    args = parse_args()
    root = args.project.expanduser().resolve()
    issues: list[str] = []
    manifest_path = root / "project.json"
    manifest = load_json(manifest_path, issues) if manifest_path.is_file() else None
    if manifest is None:
        if not manifest_path.is_file():
            issues.append(f"{manifest_path}: missing project manifest")
        project_id = episode_id = None
    else:
        project_id = manifest.get("project_id")
        episode_id = manifest.get("episode_id")
        target_duration = manifest.get("target_duration_seconds")
        if manifest.get("schema_version") != SCHEMA_VERSION:
            issues.append(f"{manifest_path}: unsupported schema_version")
        if not project_id or not episode_id:
            issues.append(f"{manifest_path}: project_id and episode_id are required")
        if not isinstance(target_duration, (int, float)) or target_duration <= 0:
            issues.append(f"{manifest_path}: target_duration_seconds must be positive")
    if manifest is None:
        target_duration = None

    packets: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.rglob("*.json")):
        if path.name in {"project.json", "packet.example.json"}:
            continue
        packet = load_json(path, issues)
        if packet is not None:
            packets.append((path, packet))

    block_versions: dict[str, int] = {}
    for path, packet in packets:
        missing = sorted(REQUIRED_PACKET_FIELDS - packet.keys())
        if missing:
            issues.append(f"{path}: missing fields: {', '.join(missing)}")
            continue
        packet_type = packet.get("packet_type")
        block_id = packet.get("block_id")
        revision = packet.get("revision")
        if packet.get("schema_version") != SCHEMA_VERSION:
            issues.append(f"{path}: unsupported schema_version")
        if packet_type not in PACKET_TYPES:
            issues.append(f"{path}: unknown packet_type {packet_type!r}")
        if not isinstance(block_id, str) or not BLOCK_ID.match(block_id):
            issues.append(f"{path}: invalid block_id {block_id!r}")
        elif block_id in block_versions:
            issues.append(f"{path}: duplicate block_id {block_id}")
        elif not isinstance(revision, int) or revision < 1:
            issues.append(f"{path}: revision must be a positive integer")
        else:
            block_versions[block_id] = revision
        if packet.get("project_id") != project_id or packet.get("episode_id") != episode_id:
            issues.append(f"{path}: project_id or episode_id differs from project.json")
        if packet.get("status") not in STATUSES:
            issues.append(f"{path}: invalid status")
        if not isinstance(packet.get("depends_on"), list):
            issues.append(f"{path}: depends_on must be a list")
        for field in ("locked_fields", "open_fields", "assumptions", "change_log"):
            if not isinstance(packet.get(field), list):
                issues.append(f"{path}: {field} must be a list")
        for field in ("controlled_fields", "continuity_in", "continuity_out", "payload"):
            if not isinstance(packet.get(field), dict):
                issues.append(f"{path}: {field} must be an object")
        overlap = field_overlap(packet)
        if overlap:
            issues.append(f"{path}: fields appear in multiple lock classes: {sorted(overlap)}")
        if packet_type == "TIMING_MAP":
            validate_timing(path, packet, target_duration, issues)

    dependency_graph: dict[str, set[str]] = {
        block_id: set() for block_id in block_versions
    }
    for path, packet in packets:
        owner = packet.get("block_id")
        for dependency in list_items(packet.get("depends_on")):
            match = DEPENDENCY.match(dependency) if isinstance(dependency, str) else None
            if not match:
                issues.append(f"{path}: invalid dependency {dependency!r}")
                continue
            block_id, revision_text = match.groups()
            actual = block_versions.get(block_id)
            if actual is None:
                issues.append(f"{path}: unresolved dependency {dependency}")
            elif actual != int(revision_text):
                issues.append(f"{path}: dependency {dependency} resolves to revision {actual}")
            elif isinstance(owner, str) and owner in dependency_graph:
                dependency_graph[owner].add(block_id)

    for cycle in dependency_cycles(dependency_graph):
        issues.append(f"dependency cycle: {' -> '.join(cycle)}")

    if manifest is not None:
        packet_index = manifest.get("packet_index")
        if not isinstance(packet_index, list):
            issues.append(f"{manifest_path}: packet_index must be a list")
        else:
            actual_index = {f"{block_id}@{revision}" for block_id, revision in block_versions.items()}
            malformed_entries = [entry for entry in packet_index if not isinstance(entry, str)]
            if malformed_entries:
                issues.append(f"{manifest_path}: packet_index entries must be strings")
            declared_index = {entry for entry in packet_index if isinstance(entry, str)}
            if actual_index != declared_index:
                missing = sorted(actual_index - declared_index)
                stale = sorted(declared_index - actual_index)
                if missing:
                    issues.append(f"{manifest_path}: packet_index missing {missing}")
                if stale:
                    issues.append(f"{manifest_path}: packet_index has stale entries {stale}")

    scene_ids: set[str] = set()
    beat_ids: set[str] = set()
    timing_ids: set[str] = set()
    timing_ranges: dict[str, tuple[float, float]] = {}
    asset_ids: set[str] = set()
    action_blocks: set[str] = set()
    storyboard_blocks: set[str] = set()
    storyboard_shots: dict[str, tuple[float, float] | None] = {}
    beat_scene_refs: list[tuple[Path, str, Any]] = []
    timing_beat_refs: list[tuple[Path, Any]] = []
    asset_scene_refs: list[tuple[Path, Any]] = []
    for path, packet in packets:
        payload = packet.get("payload", {})
        packet_type = packet.get("packet_type")
        if not isinstance(payload, dict):
            continue
        if packet_type == "SCRIPT_PACKET":
            for scene in list_items(payload.get("scenes")):
                scene_id = scene.get("scene_id") if isinstance(scene, dict) else None
                if not isinstance(scene_id, str):
                    issues.append(f"{path}: script scene needs scene_id")
                elif scene_id in scene_ids:
                    issues.append(f"{path}: duplicate scene_id {scene_id}")
                else:
                    scene_ids.add(scene_id)
            for beat in list_items(payload.get("beats")):
                beat_id = beat.get("beat_id") if isinstance(beat, dict) else None
                if not isinstance(beat_id, str):
                    issues.append(f"{path}: script beat needs beat_id")
                    continue
                if beat_id in beat_ids:
                    issues.append(f"{path}: duplicate beat_id {beat_id}")
                else:
                    beat_ids.add(beat_id)
                beat_scene_refs.append((path, beat_id, beat.get("scene_id")))
        elif packet_type == "TIMING_MAP":
            for segment in list_items(payload.get("segments")):
                timing_id = segment.get("timing_id") if isinstance(segment, dict) else None
                if not isinstance(timing_id, str):
                    issues.append(f"{path}: timing segment needs timing_id")
                    continue
                if timing_id in timing_ids:
                    issues.append(f"{path}: duplicate timing_id {timing_id}")
                else:
                    timing_ids.add(timing_id)
                time_range = numeric_range([segment.get("start"), segment.get("end")])
                if time_range is not None:
                    timing_ranges[timing_id] = time_range
                for beat_ref in list_items(segment.get("beat_refs")):
                    timing_beat_refs.append((path, beat_ref))
        elif packet_type == "ASSET_REGISTRY":
            for asset in list_items(payload.get("assets")):
                if isinstance(asset, dict) and isinstance(asset.get("asset_id"), str):
                    asset_ids.add(asset["asset_id"])
                    for scene_ref in list_items(asset.get("scene_refs")):
                        asset_scene_refs.append((path, scene_ref))
        elif (
            packet_type == "ACTION_PACKET"
            and isinstance(packet.get("block_id"), str)
            and isinstance(packet.get("revision"), int)
        ):
            action_blocks.add(f"{packet['block_id']}@{packet['revision']}")
        elif (
            packet_type == "STORYBOARD_PACKET"
            and isinstance(packet.get("block_id"), str)
            and isinstance(packet.get("revision"), int)
        ):
            storyboard_blocks.add(f"{packet['block_id']}@{packet['revision']}")
            for shot in list_items(payload.get("shots")):
                if isinstance(shot, dict) and isinstance(shot.get("shot_id"), str):
                    shot_id = shot["shot_id"]
                    if shot_id in storyboard_shots:
                        issues.append(f"duplicate storyboard shot_id {shot['shot_id']}")
                    storyboard_shots[shot_id] = numeric_range(
                        [shot.get("start"), shot.get("end")]
                    )

    for path, beat_id, scene_ref in beat_scene_refs:
        if scene_ref not in scene_ids:
            issues.append(f"{path}: beat {beat_id} has unresolved scene_id {scene_ref}")
    for path, beat_ref in timing_beat_refs:
        if beat_ref not in beat_ids:
            issues.append(f"{path}: unresolved timing beat_ref {beat_ref}")
    for path, scene_ref in asset_scene_refs:
        if scene_ref not in scene_ids:
            issues.append(f"{path}: unresolved asset scene_ref {scene_ref}")

    for path, packet in packets:
        payload = packet.get("payload", {})
        if not isinstance(payload, dict):
            continue
        if packet.get("packet_type") == "ACTION_PACKET":
            if payload.get("scene_id") not in scene_ids:
                issues.append(f"{path}: unresolved action scene_id {payload.get('scene_id')}")
            if payload.get("beat_id") not in beat_ids:
                issues.append(f"{path}: unresolved action beat_id {payload.get('beat_id')}")
            referenced_timing_ranges: list[tuple[float, float]] = []
            for timing_ref in list_items(payload.get("timing_refs")):
                if timing_ref not in timing_ids:
                    issues.append(f"{path}: unresolved action timing_ref {timing_ref}")
                elif timing_ref in timing_ranges:
                    referenced_timing_ranges.append(timing_ranges[timing_ref])
            if not list_items(payload.get("timing_refs")):
                issues.append(f"{path}: action timing_refs must not be empty")
            action_range = numeric_range(payload.get("time_range"))
            if action_range is None:
                issues.append(f"{path}: action time_range must be [start, end]")
            elif referenced_timing_ranges:
                allowed = (
                    min(value[0] for value in referenced_timing_ranges),
                    max(value[1] for value in referenced_timing_ranges),
                )
                if action_range[0] < allowed[0] - 0.001 or action_range[1] > allowed[1] + 0.001:
                    issues.append(f"{path}: action time_range falls outside timing_refs")
            participants = list_items(payload.get("participants"))
            asset_refs = list_items(payload.get("asset_refs"))
            for participant in participants:
                if participant not in asset_ids:
                    issues.append(f"{path}: unresolved action participant {participant}")
                if participant not in asset_refs:
                    issues.append(f"{path}: action participant missing from asset_refs {participant}")
            for asset_ref in list_items(payload.get("asset_refs")):
                if not isinstance(asset_ref, str) or asset_ref not in asset_ids:
                    issues.append(f"{path}: unresolved action asset_ref {asset_ref}")
        elif packet.get("packet_type") == "STORYBOARD_PACKET":
            if payload.get("scene_id") not in scene_ids:
                issues.append(f"{path}: unresolved storyboard scene_id {payload.get('scene_id')}")
            for beat_ref in list_items(payload.get("beat_refs")):
                if beat_ref not in beat_ids:
                    issues.append(f"{path}: unresolved storyboard beat_ref {beat_ref}")
            referenced_timing_ranges = []
            for timing_ref in list_items(payload.get("timing_refs")):
                if timing_ref not in timing_ids:
                    issues.append(f"{path}: unresolved storyboard timing_ref {timing_ref}")
                elif timing_ref in timing_ranges:
                    referenced_timing_ranges.append(timing_ranges[timing_ref])
            if not list_items(payload.get("timing_refs")):
                issues.append(f"{path}: storyboard timing_refs must not be empty")
            sequence_range = numeric_range(payload.get("time_range"))
            if sequence_range is None:
                issues.append(f"{path}: storyboard time_range must be [start, end]")
            elif referenced_timing_ranges:
                allowed = (
                    min(value[0] for value in referenced_timing_ranges),
                    max(value[1] for value in referenced_timing_ranges),
                )
                if sequence_range[0] < allowed[0] - 0.001 or sequence_range[1] > allowed[1] + 0.001:
                    issues.append(f"{path}: storyboard time_range falls outside timing_refs")
            shot_ranges: list[tuple[float, float]] = []
            for shot in list_items(payload.get("shots")):
                shot_range = (
                    numeric_range([shot.get("start"), shot.get("end")])
                    if isinstance(shot, dict)
                    else None
                )
                if shot_range is None:
                    issues.append(f"{path}: storyboard shot needs numeric start < end")
                else:
                    shot_ranges.append(shot_range)
            if sequence_range is not None and shot_ranges:
                ordered = sorted(shot_ranges)
                if abs(ordered[0][0] - sequence_range[0]) > 0.001:
                    issues.append(f"{path}: storyboard shots do not start at sequence start")
                for previous, current in zip(ordered, ordered[1:]):
                    if abs(current[0] - previous[1]) > 0.001:
                        issues.append(f"{path}: storyboard shots have a gap or overlap")
                if abs(ordered[-1][1] - sequence_range[1]) > 0.001:
                    issues.append(f"{path}: storyboard shots do not close at sequence end")
            for asset_ref in list_items(payload.get("asset_refs")):
                if not isinstance(asset_ref, str) or asset_ref not in asset_ids:
                    issues.append(f"{path}: unresolved storyboard asset_ref {asset_ref}")
            for action_ref in list_items(payload.get("action_refs")):
                if not isinstance(action_ref, str) or action_ref not in action_blocks:
                    issues.append(f"{path}: unresolved storyboard action_ref {action_ref}")
        elif packet.get("packet_type") == "SHOT_PACKET":
            for shot in list_items(payload.get("shots")):
                if not isinstance(shot, dict):
                    continue
                shot_id = shot.get("shot_id")
                if not isinstance(shot_id, str) or shot_id not in storyboard_shots:
                    issues.append(f"{path}: unresolved shot_id {shot_id}")
                shot_range = numeric_range(shot.get("time_range"))
                board_range = storyboard_shots.get(shot_id) if isinstance(shot_id, str) else None
                if shot_range is None:
                    issues.append(f"{path}: shot {shot_id} needs numeric time_range")
                elif board_range is not None and (
                    abs(shot_range[0] - board_range[0]) > 0.001
                    or abs(shot_range[1] - board_range[1]) > 0.001
                ):
                    issues.append(f"{path}: shot {shot_id} time_range differs from storyboard")
                for asset_ref in list_items(shot.get("asset_refs")):
                    if not isinstance(asset_ref, str) or asset_ref not in asset_ids:
                        issues.append(f"{path}: unresolved shot asset_ref {asset_ref}")
                action_ref = shot.get("action_ref")
                if not isinstance(action_ref, str) or action_ref not in action_blocks:
                    issues.append(f"{path}: unresolved shot action_ref {shot.get('action_ref')}")
                storyboard_ref = shot.get("storyboard_ref")
                if not isinstance(storyboard_ref, str) or storyboard_ref not in storyboard_blocks:
                    issues.append(
                        f"{path}: unresolved shot storyboard_ref {shot.get('storyboard_ref')}"
                    )

    report = {
        "ok": not issues,
        "project": str(root),
        "packets": len(packets),
        "blocks": block_versions,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("OK" if report["ok"] else "INVALID")
        print(f"packets: {len(packets)}")
        for issue in issues:
            print(f"- {issue}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
