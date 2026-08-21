# 电影级英雄概念图 Pass 与生产交接

## 目录

1. 何时使用
2. 视觉信息预算
3. 镜头与气氛优先级
4. 提示词与负面控制
5. 交给生产资产 Skill

## 1. 何时使用

英雄概念图 Pass 适用于“第一张图”“主视觉”“角色海报”“最有冲击力的角色图”“先看她/他长什么样”等需求。它的任务是先让一个强烈、可想象、可被观众记住的画面成立。

生产锁定 Pass 适用于三视图、服装拆解、道具结构、连续镜头、资产 DNA 和剧组交接。不要在第一张英雄图里提前执行全部生产规格。

## 2. 视觉信息预算

英雄概念图只保留：

- 一句视觉命题。
- 3–5 个核心轮廓/身份锚点。
- 一个动作或气氛事件。
- 一组主色：主导色、支撑色、强调色。
- 一套相容的摄影机、镜头、机位和布光语言。

所有其他信息降级为背景或暂不确定：品牌型号、精确尺寸、配饰数量、左右固定点、材料工艺、三视图比例、长篇皮肤负面和资产登记字段。

允许明确表达角色的审美魅力与情绪，如 `alluring`, `seductive`, `dangerously elegant`, `striking`, `cinematically beautiful`, `glamorous but ominous`, `sensual silhouette`。这些词必须被可见的轮廓、动作、光线和空间关系支撑，不用抽象安全词把魅力抹平。

如果用户给出多个风格来源，先指定一个母审美，其他来源只作为局部影响。例如“巴黎暗黑秀场”可以统领日式武士、技术户外和运动品牌细节；不要让每个来源获得同等权重。

## 3. 镜头与气氛优先级

先让主体轮廓和视线成立，再决定皮肤和材质细节。英雄图可以使用戏剧化但有来源的逆光、毒雾、火花、风、薄纱、长刀、伞、雨水或色彩污染；只要它们共同服务同一个视觉命题。

真人感在英雄图中只需保留摄影可信度：自然透视、真实演员的表演重量、可读眼神、受光方向一致的皮肤反射。不要把完整低修图规则、所有年龄负面和配饰连续性表格塞入主提示词。

主角感通过焦点、眼神、轮廓、动作、空间比例、局部对比、主色锚点和环境反应建立，不通过完美脸、全脸磨皮或无意义的英雄低机位建立。

## 4. 提示词与负面控制

主提示词顺序：

```text
[visual thesis and protagonist mood]
[3–5 silhouette anchors]
[decisive pose / action / atmosphere]
[dominant color system]
[one camera and lens language]
[motivated lighting and emotional contrast]
[one or two material / world cues]
[live-action cinematic finish]
```

英雄图负面词控制在约 8–15 个，优先排除：`game CG`, `generic fashion catalog`, `bland silhouette`, `random costume mashup`, `flat lighting`, `empty gaze`, `static passport pose`, `plastic skin`, `unreadable signature prop`, `text`, `watermark`。

不要默认加入：`perfect facial symmetry`, `no wrinkles`, `no body fat`, `flawless skin`, `ultra-detailed pores`, 大段三视图对齐词、配饰连接词和制作规格词。它们会把英雄概念推向美容广告或生产图表。

## 5. 交给生产资产 Skill

英雄概念成立后，输出一段简短交接：

```text
HERO CONCEPT HANDOFF
visual thesis:
dominant silhouette:
3–5 immutable visual anchors:
hero action / atmospheric event:
dominant / supporting / accent colors:
camera and lighting language:
parent aesthetic:
details intentionally left open:
```

再交给 `$craft-production-design-prompts` 做面部、服装、配饰、三视图、材质和一致性锁定。生产 Skill 不得用新增规格改写英雄概念的第一视觉印象。
