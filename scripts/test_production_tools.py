#!/usr/bin/env python3
"""Smoke-test project initialization and production validation failures."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = (
    ROOT
    / "skills"
    / "orchestrate-ai-drama-production"
    / "scripts"
    / "init_project.py"
)
VALIDATE = INIT.with_name("validate_project.py")
EXAMPLE = ROOT / "examples" / "yaksha-90s-demo"


def run(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        text=True,
        capture_output=True,
        check=False,
    )


def assert_result(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cinematic-ai-skills-test-") as temporary:
        temp = Path(temporary)

        initialized = run(INIT, "夜叉测试", "--output", temp, "--duration", 12)
        assert_result(initialized.returncode == 0, initialized.stderr)
        project = temp / "夜叉测试"
        assert_result(project.is_dir(), "Unicode project folder was not created")
        valid_empty = run(VALIDATE, project, "--json")
        assert_result(valid_empty.returncode == 0, valid_empty.stdout + valid_empty.stderr)

        valid_copy = temp / "valid-copy"
        shutil.copytree(EXAMPLE, valid_copy)
        valid = run(VALIDATE, valid_copy, "--json")
        assert_result(valid.returncode == 0, valid.stdout + valid.stderr)

        broken_dependency = temp / "broken-dependency"
        shutil.copytree(EXAMPLE, broken_dependency)
        shot_path = broken_dependency / "07-shots" / "shots.json"
        shot_packet = json.loads(shot_path.read_text(encoding="utf-8"))
        shot_packet["depends_on"].append("MISSING001@1")
        write_json(shot_path, shot_packet)
        invalid = run(VALIDATE, broken_dependency, "--json")
        assert_result(invalid.returncode == 1, "Unresolved dependency was not rejected")
        assert_result("unresolved dependency" in invalid.stdout, invalid.stdout)

        broken_timing = temp / "broken-timing"
        shutil.copytree(EXAMPLE, broken_timing)
        timing_path = broken_timing / "03-timing" / "timing.json"
        timing_packet = json.loads(timing_path.read_text(encoding="utf-8"))
        timing_packet["payload"]["segments"][1]["start"] = 19.0
        write_json(timing_path, timing_packet)
        invalid = run(VALIDATE, broken_timing, "--json")
        assert_result(invalid.returncode == 1, "Timeline gap was not rejected")
        assert_result("visual timeline has gap" in invalid.stdout, invalid.stdout)

        broken_shot_time = temp / "broken-shot-time"
        shutil.copytree(EXAMPLE, broken_shot_time)
        shot_path = broken_shot_time / "07-shots" / "shots.json"
        shot_packet = json.loads(shot_path.read_text(encoding="utf-8"))
        shot_packet["payload"]["shots"][0]["time_range"][1] = 45.0
        write_json(shot_path, shot_packet)
        invalid = run(VALIDATE, broken_shot_time, "--json")
        assert_result(invalid.returncode == 1, "Shot/storyboard time mismatch was not rejected")
        assert_result("time_range differs from storyboard" in invalid.stdout, invalid.stdout)

        broken_four_grid = temp / "broken-four-grid"
        shutil.copytree(EXAMPLE, broken_four_grid)
        action_path = broken_four_grid / "05-action" / "action.json"
        action_packet = json.loads(action_path.read_text(encoding="utf-8"))
        action_packet["payload"]["four_grid"]["output_count"] = 4
        write_json(action_path, action_packet)
        invalid = run(VALIDATE, broken_four_grid, "--json")
        assert_result(invalid.returncode == 1, "Four separate grid outputs were not rejected")
        assert_result("four_grid output_count must be 1" in invalid.stdout, invalid.stdout)

        cyclic = temp / "cyclic"
        shutil.copytree(EXAMPLE, cyclic)
        research_path = cyclic / "01-research" / "research.json"
        research_packet = json.loads(research_path.read_text(encoding="utf-8"))
        research_packet["depends_on"] = ["CON001@2"]
        write_json(research_path, research_packet)
        invalid = run(VALIDATE, cyclic, "--json")
        assert_result(invalid.returncode == 1, "Dependency cycle was not rejected")
        assert_result("dependency cycle" in invalid.stdout, invalid.stdout)

        malformed = temp / "malformed"
        shutil.copytree(EXAMPLE, malformed)
        action_path = malformed / "05-action" / "action.json"
        action_packet = json.loads(action_path.read_text(encoding="utf-8"))
        action_packet.pop("revision")
        write_json(action_path, action_packet)
        shot_path = malformed / "07-shots" / "shots.json"
        shot_packet = json.loads(shot_path.read_text(encoding="utf-8"))
        shot_packet["depends_on"] = {"not": "a list"}
        write_json(shot_path, shot_packet)
        manifest_path = malformed / "project.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["packet_index"].append({"not": "a string"})
        write_json(manifest_path, manifest)
        invalid = run(VALIDATE, malformed, "--json")
        assert_result(invalid.returncode == 1, "Malformed packet fields were not rejected")
        assert_result("missing fields: revision" in invalid.stdout, invalid.stdout)
        assert_result("depends_on must be a list" in invalid.stdout, invalid.stdout)
        assert_result("packet_index entries must be strings" in invalid.stdout, invalid.stdout)
        assert_result("Traceback" not in invalid.stderr, invalid.stderr)

    print("production tool tests: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
