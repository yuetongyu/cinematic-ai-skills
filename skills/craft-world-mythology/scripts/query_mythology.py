#!/usr/bin/env python3
"""Targeted lookup for the user's Markdown-wrapped world mythology dataset."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable


SOURCE_FILENAMES = (
    "world-mythology-dataset.md",
    "world-mythology-dataset.json",
    "世界神话体系书目深度调研.md",
    "世界神话体系书目深度调研.json",
)


def candidate_sources() -> list[Path]:
    """Return portable defaults; explicit --source remains the primary path."""
    skill_root = Path(__file__).resolve().parents[1]
    candidates: list[Path] = []
    configured = os.environ.get("MYTHOLOGY_SOURCE")
    if configured:
        candidates.append(Path(configured).expanduser())
    for base in (
        skill_root / "references",
        skill_root / "data",
        Path.cwd(),
        Path.home() / "Downloads",
    ):
        candidates.extend(base / filename for filename in SOURCE_FILENAMES)
    return candidates


def resolve_source(path: Path | None) -> Path:
    if path is not None:
        return path.expanduser()
    for candidate in candidate_sources():
        if candidate.is_file():
            return candidate
    names = ", ".join(SOURCE_FILENAMES[:2])
    raise FileNotFoundError(
        "no mythology dataset found; pass --source PATH, set MYTHOLOGY_SOURCE, "
        f"or place {names} in the skill references directory"
    )


def load_dataset(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"source file not found: {path}")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = text
    else:
        marker = "```json"
        start = text.find(marker)
        if start < 0:
            payload = text.strip()
        else:
            start += len(marker)
            if start < len(text) and text[start] == "\n":
                start += 1
            end = text.find("```", start)
            if end < 0:
                raise ValueError("could not find the end of the JSON code block")
            payload = text[start:end]
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in source: {exc}") from exc
    if not isinstance(data, dict) or "systems" not in data:
        raise ValueError("source JSON does not have the expected systems field")
    return data


def entities(data: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for system_name, system in data.get("systems", {}).items():
        for entity in system.get("entities", []):
            record = dict(entity)
            record["_system"] = system_name
            yield record


def recursive_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{k} {recursive_text(v)}" for k, v in value.items())
    if isinstance(value, list):
        return " ".join(recursive_text(item) for item in value)
    return str(value)


def compact_entity(entity: dict[str, Any], full: bool = False) -> dict[str, Any]:
    if full:
        return entity
    return {
        "id": entity.get("id"),
        "name": entity.get("name"),
        "aliases": entity.get("aliases", []),
        "system": entity.get("_system", entity.get("system")),
        "category": entity.get("category"),
        "abilities": entity.get("abilities", []),
        "appearance": entity.get("appearance"),
        "personality": entity.get("personality"),
        "residence": entity.get("residence"),
        "weapons": entity.get("weapons", []),
        "spells": entity.get("spells", []),
        "story_background": entity.get("story_background"),
        "relations": entity.get("relations", []),
        "sources": entity.get("sources", []),
        "notes": entity.get("notes"),
    }


def matches(entity: dict[str, Any], term: str) -> bool:
    return term.casefold() in recursive_text(entity).casefold()


def search_entities(
    data: dict[str, Any], term: str, limit: int, system: str | None = None
) -> list[dict[str, Any]]:
    found = [
        entity
        for entity in entities(data)
        if matches(entity, term)
        and (system is None or system.casefold() in entity.get("_system", "").casefold())
    ]
    return [compact_entity(entity) for entity in found[:limit]]


def find_entities(
    data: dict[str, Any], term: str, limit: int, system: str | None = None
) -> list[dict[str, Any]]:
    exact = []
    partial = []
    folded = term.casefold()
    for entity in entities(data):
        if system is not None and system.casefold() not in entity.get("_system", "").casefold():
            continue
        names = [entity.get("name", ""), *entity.get("aliases", [])]
        if any(str(name).casefold() == folded for name in names):
            exact.append(entity)
        elif any(folded in str(name).casefold() for name in names):
            partial.append(entity)
    selected = exact or partial
    return [compact_entity(entity) for entity in selected[:limit]]


def relation_results(
    data: dict[str, Any], term: str, limit: int, system: str | None = None
) -> list[dict[str, Any]]:
    folded = term.casefold()
    output = []
    for entity in entities(data):
        if system is not None and system.casefold() not in entity.get("_system", "").casefold():
            continue
        if folded not in str(entity.get("name", "")).casefold() and not any(
            folded == str(alias).casefold() for alias in entity.get("aliases", [])
        ):
            continue
        output.append(
            {
                "entity": entity.get("name"),
                "system": entity.get("_system"),
                "relations": entity.get("relations", []),
            }
        )
        if len(output) >= limit:
            break
    return output


def spell_results(data: dict[str, Any], term: str, limit: int) -> list[dict[str, Any]]:
    categories = data.get("spell_systems", {}).get("categories", {})
    folded = term.casefold()
    output = []
    for category, record in categories.items():
        for spell in record.get("spells", []):
            if folded not in recursive_text({"category": category, **spell}).casefold():
                continue
            output.append({"category": category, **spell})
            if len(output) >= limit:
                return output
    return output


def weapon_results(data: dict[str, Any], term: str, limit: int) -> list[dict[str, Any]]:
    folded = term.casefold()
    output = []
    for entity in entities(data):
        for weapon in entity.get("weapons", []):
            if folded in recursive_text(weapon).casefold():
                output.append(
                    {
                        "owner": entity.get("name"),
                        "system": entity.get("_system"),
                        **weapon,
                    }
                )
                if len(output) >= limit:
                    return output
    return output


def stats(data: dict[str, Any]) -> dict[str, Any]:
    metadata = data.get("_metadata", {})
    return {
        "source_version": metadata.get("version"),
        "last_updated": metadata.get("last_updated"),
        "systems": len(data.get("systems", {})),
        "entities": sum(len(s.get("entities", [])) for s in data.get("systems", {}).values()),
        "relations": metadata.get("total_relations"),
        "weapons": metadata.get("total_weapons"),
        "spell_systems": metadata.get(
            "total_spell_systems", len(data.get("spell_systems", {}).get("categories", {}))
        ),
        "spell_categories": len(data.get("spell_systems", {}).get("categories", {})),
    }


def systems(data: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for name, record in data.get("systems", {}).items():
        result.append(
            {
                "system": name,
                "entities": record.get("count", len(record.get("entities", []))),
                "relations": record.get("relation_count"),
                "weapons": record.get("weapon_count"),
                "spells": record.get("spell_count"),
            }
        )
    return result


def validate(data: dict[str, Any]) -> dict[str, Any]:
    metadata = data.get("_metadata", {})
    all_entities = list(entities(data))
    ids = [entity.get("id") for entity in all_entities]
    relation_count = sum(len(entity.get("relations", [])) for entity in all_entities)
    weapon_count = sum(len(entity.get("weapons", [])) for entity in all_entities)
    issues: list[str] = []
    if any(not entity.get("id") or not entity.get("name") for entity in all_entities):
        issues.append("some entities are missing id or name")
    if len(ids) != len(set(ids)):
        issues.append("entity IDs are not unique")
    for entity in all_entities:
        for relation in entity.get("relations", []):
            if not relation.get("entity") or not relation.get("event"):
                issues.append(f"relation missing entity/event: {entity.get('name')}")
                break
    expected_checks = {
        "entities": (len(all_entities), metadata.get("total_entities")),
        "relations": (relation_count, metadata.get("total_relations")),
        "weapons": (weapon_count, metadata.get("total_weapons")),
        "systems": (len(data.get("systems", {})), metadata.get("total_systems")),
    }
    mismatches = {
        key: {"actual": actual, "expected": expected}
        for key, (actual, expected) in expected_checks.items()
        if expected is not None and actual != expected
    }
    if mismatches:
        issues.append("metadata counts do not match parsed data")
    return {
        "ok": not issues,
        "source_version": metadata.get("version"),
        "checks": {
            "entities": len(all_entities),
            "unique_entity_ids": len(ids) == len(set(ids)),
            "relations_with_events": relation_count,
            "weapons": weapon_count,
            "systems": len(data.get("systems", {})),
            "spell_categories": len(data.get("spell_systems", {}).get("categories", {})),
        },
        "metadata_mismatches": mismatches,
        "issues": issues,
    }


def emit(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return
    if isinstance(value, list):
        for item in value:
            print(json.dumps(item, ensure_ascii=False, indent=2))
            print()
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Markdown-wrapped JSON or plain JSON dataset; otherwise auto-discover one",
    )
    parser.add_argument("--system", help="limit entity, search, or relation results to a system name")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", dest="as_json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query the world mythology Markdown/JSON dataset")
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in [
        ("stats", "show dataset statistics"),
        ("systems", "list mythology systems"),
        ("validate", "validate required fields, IDs, relations, and metadata counts"),
    ]:
        command = sub.add_parser(name, help=help_text)
        add_common(command)

    for name, help_text in [
        ("entity", "find an entity by name or alias"),
        ("search", "search all entity fields"),
        ("relations", "show relations and event descriptions for an entity"),
        ("spells", "search world spell systems"),
        ("weapons", "search weapons and ritual objects"),
    ]:
        command = sub.add_parser(name, help=help_text)
        command.add_argument("term")
        command.add_argument("--full", action="store_true", help="include every stored field for entity results")
        add_common(command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = resolve_source(args.source)
        data = load_dataset(source)
        if args.command == "stats":
            result = stats(data)
        elif args.command == "systems":
            result = systems(data)
        elif args.command == "validate":
            result = validate(data)
        elif args.command == "entity":
            result = find_entities(data, args.term, args.limit, args.system)
            if args.full:
                result = [
                    compact_entity(entity, full=True)
                    for entity in entities(data)
                    if entity.get("name") in {item.get("name") for item in result}
                ][: args.limit]
        elif args.command == "search":
            result = search_entities(data, args.term, args.limit, args.system)
        elif args.command == "relations":
            result = relation_results(data, args.term, args.limit, args.system)
        elif args.command == "spells":
            result = spell_results(data, args.term, args.limit)
        else:
            result = weapon_results(data, args.term, args.limit)
        emit(result, args.as_json)
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
