# 英雄概念图与生产锁定的两阶段工作流

## 目录

1. 模式选择
2. 英雄概念图 Pass
3. 生产锁定 Pass
4. 概念到资产的交接

## 1. 模式选择

### 使用英雄概念图 Pass

当用户说“第一张角色图”“英雄概念图”“主视觉”“最有冲击力”“电影海报感”“先看看她/他长什么样”，或没有参考图、没有连续性要求时，优先使用英雄概念图 Pass。

目标是让观众一眼记住角色的视觉命题，不是完成制作登记。

### 使用生产锁定 Pass

当用户要求三视图、正侧背、一页式设定板、服装拆解、资产 DNA、配饰固定点、跨画面一致性、交给剧组或作为后续镜头母版时，才使用生产锁定 Pass。

如果用户只说“设计一个角色”，先按英雄概念图 Pass；不要自动输出配饰登记表、尺寸、左右方向和长负面词。

## 2. 英雄概念图 Pass

先锁定以下五件事：

1. **一句视觉命题**：角色以什么矛盾让观众记住，例如“轻盈柔媚的外表承载紫色、危险、流动的毒性”。
2. **3–5 个核心 DNA 锚点**：只选最能形成轮廓和气质的特征，例如黑色光环伞、极长直刀、轻紫毒雾、彩色左臂纹身、技术服装的曲线轮廓。
3. **一个动作或气氛瞬间**：伞刚打开、毒雾绕腿上升、刀立在身侧、人物回头收刀或踏入光池。
4. **一组主色**：主导色、支撑色、一个强调色；不同时塞入多个风格色系。
5. **一种摄影语言**：近距离中长焦肖像、低机位广角压迫、远距离长焦窥视或环境英雄全景，只选一种主导观感。

把所有其他元素降为辅助层。品牌、功能、工艺、配饰数量、尺寸、固定点、精确年龄、皮肤区域和三视图左右方向暂时不进入主提示词，除非它们正是视觉命题的一部分。

“真实演员”只需用一到两句保持摄影可信，例如 `live-action film still`, `striking real actor presence`, `natural skin with controlled cinematic lighting`。不要把整套真人皮肤和低修图负面模块复制进英雄图。

允许使用有审美作用的词：`seductive`, `alluring`, `dangerously elegant`, `striking`, `glamorous but ominous`, `cinematically beautiful`, `sensual silhouette`。这些词要被轮廓、动作、服装和光线证明，不要替换成空泛的“高级感”。

当服装有多个文化或品牌来源时，先选择一个母审美，再把其他来源降级为局部语汇。例如：`Parisian dark runway as the parent aesthetic, with restrained Japanese warrior and technical outdoor details`。不要并列堆叠十几个品牌、流派和职业标签。

### 英雄概念提示词骨架

```text
[one-sentence visual thesis],
[3–5 silhouette and identity anchors],
[one decisive action or atmospheric event],
[dominant / supporting / accent colors],
[single camera and lens language],
[motivated light and emotional contrast],
[one or two meaningful material or world cues],
[live-action cinematic finish without flattening the imagination]
```

英雄图负面提示词只排除真正破坏画面的风险，通常控制在 8–15 项：

```text
game CG, generic fashion catalog, bland character design, random costume mashup, cluttered accessories, weak silhouette, flat lighting, empty gaze, static passport pose, plastic skin, unreadable prop, text, watermark
```

## 3. 生产锁定 Pass

只有在英雄概念成立后，再锁定：

- 角色 5–7 个不可变 DNA 锚点。
- 设定年龄与感知年龄。
- 服装层级、材料、工艺、磨损和功能结构。
- 配饰数量、左右、固定点、穿戴层级、受力与视角可见性。
- 面部、身体、道具、三视图比例和跨图一致性。
- 生产级负面词、结构控制、参考图、姿态控制与后续镜头交接。

生产锁定不是重写英雄概念，而是把英雄概念中已经成立的视觉命题翻译成可重复资产。任何新加入的规格如果削弱了命题，应降为受控特征或移除。

## 4. 概念到资产的交接

交接时保留：

```text
HERO CONCEPT HANDOFF
visual thesis:
dominant silhouette:
3–5 immutable visual anchors:
hero action / atmospheric event:
dominant / supporting / accent colors:
camera and lighting language:
parent aesthetic:
details intentionally left open for production design:
```

生产 Skill 读取这段交接，只补充可重复性所需的规格，不改变核心命题、主色、轮廓和气氛。
