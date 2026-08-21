# 数据源与检索地图

## 源文件与分发

skill 默认内置：

`references/world-mythology-dataset.md`

它是 Markdown 说明 + 一个完整 JSON 代码块。读取时只解析 ` ```json ` 与结束围栏之间的对象，避免把说明文字误当成数据。源文件版本、更新时间和统计数字以 `_metadata` 为准；数据可能不全、混合不同版本或包含未经核验的叙述。

查询脚本也支持独立 JSON 文件、`--source PATH` 和 `MYTHOLOGY_SOURCE`。数据源优先级为：显式 `--source`、环境变量、skill 的 `references/` 或 `data/`、当前工作目录、用户 `Downloads` 目录。公开发布前检查内置数据的再分发许可；没有许可时删除内置数据，保留脚本和 schema 即可。

## 顶层结构

```text
_metadata
systems
  └─ 神话体系
       ├─ count / relation_count / weapon_count / spell_count
       └─ entities[]
            ├─ id / name / aliases / category / system
            ├─ relations[]: entity / relation / event
            ├─ abilities / appearance / personality
            ├─ residence / weapons[] / spells[]
            ├─ story_background / detailed_description
            └─ sources / notes
spell_systems
  └─ categories
       └─ 术法分类
            └─ spells[]: name / category / origin / description / abilities / sources / related_entities
```

## 查询命令

```bash
Q=/path/to/craft-world-mythology/scripts/query_mythology.py
python3 "$Q" stats
python3 "$Q" systems
python3 "$Q" validate
python3 "$Q" entity "后羿" --limit 3
python3 "$Q" entity "后羿" --full --json
python3 "$Q" search "复活" --limit 20
python3 "$Q" relations "黄帝" --json
python3 "$Q" weapons "金箍棒"
python3 "$Q" spells "占卜" --limit 20
```

`entity` 优先精确匹配名称或别名，再退回名称包含匹配；`search` 会检索实体的所有字段；`relations` 用于获取完整事件描述；`weapons` 和 `spells` 用于从能力之外寻找物质和仪式媒介。

## 研究时的字段优先级

1. **关系事件**：用于故事事实和人物之间的因果动作。
2. **故事背景/详细描述**：用于叙事语境，但要检查是否把多个版本合并。
3. **能力**：只当作候选权能，不直接当作可无限使用的技能表。
4. **武器/法宝/住所**：用于视觉资产和场景行动，仍需核对时代与版本。
5. **来源/备注**：作为网络核验入口，不等于已证实的原典引文。
