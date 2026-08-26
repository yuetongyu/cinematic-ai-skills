# Production Packet Contracts

## 目录

- 设计目标
- 通用包头
- 稳定 ID
- 专业 Packet
- 锁定与变更
- 连续性
- 验证规则

## 设计目标

Packet 是专业 skill 之间的最小可靠交接，不是把全部创作写成 JSON。适合人类阅读的剧本、提示词和设计说明仍保留为 Markdown；Packet 只存储引用、决定、锁定项、状态变化和依赖关系。

下游必须能回答：

- 这个结论来自哪个上游版本？
- 哪些字段不能改？
- 哪些字段可以在范围内变化？
- 哪些内容只是暂时假设？
- 本区块改变了哪些连续性状态？
- 上游变更后，哪些下游需要失效或复核？

## 通用包头

每个 JSON Packet 使用：

```json
{
  "schema_version": "1.0.0",
  "packet_type": "SCRIPT_PACKET",
  "block_id": "SCR001",
  "revision": 1,
  "project_id": "YAKSHA-001",
  "episode_id": "EP001",
  "source_revision": "research:RSH001@1",
  "depends_on": ["RSH001@1"],
  "status": "draft",
  "locked_fields": [],
  "controlled_fields": {},
  "open_fields": [],
  "assumptions": [],
  "continuity_in": {},
  "continuity_out": {},
  "change_log": [
    {"revision": 1, "summary": "initial draft"}
  ],
  "payload": {}
}
```

### 字段规则

- `schema_version`：契约版本，不等于内容版本。
- `packet_type`：只使用已定义的大写类型。
- `block_id`：项目内稳定唯一，返工时不换 ID。
- `revision`：正整数；内容发生有意义变化时递增。
- `source_revision`：便于人类扫描的主要来源。
- `depends_on`：所有直接依赖，格式 `BLOCK_ID@revision`。
- `status`：`draft | review | locked | superseded`。
- `locked_fields`：下游不得静默修改的 JSON path 或语义字段。
- `controlled_fields`：允许变化及范围。
- `open_fields`：上游主动留白，下游可创作。
- `assumptions`：未获确认但为了推进采用的可撤回判断。
- `continuity_in/out`：区块前后的可追踪状态。
- `change_log`：每次 revision 的原因和影响。
- `payload`：专业内容索引与结构数据。

## 稳定 ID

| 前缀 | 对象 | 示例 |
|---|---|---|
| `RSH` | 研究包 | `RSH001` |
| `SCR` | 剧本包 | `SCR001` |
| `SC` | 场景 | `SC001` |
| `B` | 剧情节拍 | `B001` |
| `T` | 时间段 | `T001` |
| `CHR` | 人类/角色 | `CHR001` |
| `ENT` | 非人实体 | `ENT001` |
| `ENV` | 环境/场景资产 | `ENV001` |
| `PRP` | 道具/物品 | `PRP001` |
| `VFX` | 视效源/规则 | `VFX001` |
| `ACT` | 动作包 | `ACT001` |
| `SEQ` | 分镜序列 | `SEQ001` |
| `SH` | 镜头 | `SH001` |

删除对象时保留 tombstone，不复用 ID。名称变化不改变 ID；身份发生根本替换时创建新 ID。

## 专业 Packet

### RESEARCH_PACKET

`payload` 至少包含：

- `subject`
- `research_domain`
- `source_versions`
- `evidence_layers`
- `semantic_core`
- `adaptation_boundaries`
- `visual_motifs`
- `action_motifs`
- `disputes`
- `unknowns`

### SCRIPT_PACKET

- `premise`
- `theme_question`
- `character_pressure`
- `scenes[]`：`scene_id`、目标、阻力、转折、余波
- `beats[]`：`beat_id`、`scene_id`、行动、信息、情绪、声音
- `ending_state`

### TIMING_MAP

- `total_duration_seconds`
- `fps`
- `segments[]`：`timing_id`、`beat_refs`、`start`、`end`、`function`、`dialogue`、`sound`、`action_phase`

时间采用秒数或 `HH:MM:SS.mmm`，项目内统一。相邻段允许重叠声音，不允许未声明的画面重叠。

### ASSET_REGISTRY

- `assets[]`：ID、类型、名称、叙事功能、状态、不可变/受控/自由 DNA、尺度、材料、配饰/组件、引用场景
- `relationships[]`
- `style_profile`

### ACTION_PACKET

- 参照动作 skill 的 `ACTION_PACKET`。
- 必须引用 scene、beat、timing、participant 和 asset。
- `four_grid` 必须声明 `canvas_aspect_ratio: 16:9`、`layout: 2x2`、`output_count: 1`，并把四个动作相位合成为一条整图提示词。

### STORYBOARD_PACKET

- 参照分镜 skill 的 `STORYBOARD_PACKET`。
- 必须引用 scene、beat、timing、上游动作和资产版本。
- `four_grid` 必须是一张 16:9 图片中的 2×2 四镜，不得包含四条独立生图提示词。超过四镜时建立新的 `SEQ` Packet。

### SHOT_PACKET

- `shot_id`、`time_range`、`story_function`
- `asset_refs`、`action_refs`、`storyboard_ref`
- `first_frame`、`key_action_frame`、`last_frame`
- `video_motion_prompt`
- `camera_lighting`、`performance`、`vfx`、`sound`
- `positive_prompt`、`negative_prompt`
- `continuity_in/out`

### CONTINUITY_LEDGER

按镜头记录身份、配饰、道具、损伤、污染、环境破坏、天气、风、光源、色彩、VFX 阶段、屏幕方向、情绪策略和观众信息权限。

## 锁定与变更

优先级：

`事实/授权素材锁定 > 已确认剧本因果 > 资产身份 > 动作结果 > 分镜结构 > 摄影解释 > 表面细节`

下游发现锁定字段不可执行时：

1. 不静默修改。
2. 标记冲突和受影响 block。
3. 给出最小上游修订建议。
4. 用户或总控接受后递增上游 revision。
5. 只重新验证依赖该 revision 的下游。

## 连续性

`continuity_out` 默认成为直接下一块的 `continuity_in`。状态不是散文气氛，而是可比较字段，例如：

```json
{
  "CHR001.injury": "left_forearm_cut_stage_2",
  "PRP003.owner": "CHR002",
  "ENV001.rain": "heavy_wind_from_screen_right",
  "VFX001.phase": "post_impact_dissipation",
  "screen_direction.CHR001": "left_to_right"
}
```

## 验证规则

- block ID 在项目内唯一。
- revision 为正整数。
- depends_on 引用必须存在且版本匹配。
- locked/controlled/open 字段不得互相冲突。
- Packet 的 project/episode 与项目清单一致。
- 时间段 start < end，整体时长符合项目目标。
- 下游引用的 asset/action/shot ID 必须存在。
- 动作与分镜引用的 scene/beat/timing ID 必须存在；最终镜头时间必须与分镜镜头一致。
- ACTION/STORYBOARD 的四宫格必须是单张 16:9、2×2、`output_count: 1`，四格阅读顺序固定。
- 连续性输入与上游输出冲突时必须声明 override 和剧情理由。
