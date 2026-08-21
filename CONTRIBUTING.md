# Contributing

Contributions should improve reusable skill behavior rather than add generic
prompt adjectives or one-off project lore.

## Skill changes

1. Keep each `SKILL.md` focused and below 500 lines when practical.
2. Put detailed domain guidance in one-level `references/` files.
3. Preserve the distinction between Hero Concept and Production Lock/Pass.
4. Preserve handoff contracts: research evidence, screenplay causality, asset
   DNA, and cinematography rules must remain distinguishable.
5. Do not add private paths, credentials, generated caches, or model-specific
   parameters presented as universal rules.

Validate a skill with the current Codex `skill-creator` validator when it is
available. Also check that Markdown fences are balanced and that referenced
files exist.

Run the repository-level standard-library validation before opening a pull
request:

```bash
python3 scripts/validate_repo.py
```

## Mythology data changes

Run:

```bash
python3 skills/craft-world-mythology/scripts/query_mythology.py validate --json
```

Every factual addition should identify its source and distinguish original
text, scholarly interpretation, later popular tradition, and project
adaptation. Do not silently merge incompatible versions or treat living
religions as fantasy asset lists.

By contributing, you agree that skill text and code are provided under MIT,
and contributions to the bundled dataset are provided under CC BY 4.0.
