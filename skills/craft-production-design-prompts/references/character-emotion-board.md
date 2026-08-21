# 角色感情词典与情绪版资产提示词

## 目录

1. 情绪板的资产目标
2. 先锁中性身份基线
3. 角色专属感情词典
4. 单个情绪状态的定义格式
5. 生产表情板与电影情绪版的区别
6. 情绪板构图与摄影
7. 跨版本一致性
8. 真人年龄、皮肤与主角感保护
9. 提示词模板
10. 失败模式与负面提示词

## 1. 情绪板的资产目标

角色情绪板不是通用“喜怒哀乐表情包”，而是验证同一演员身份在不同关系压力下如何表演。它应帮助后续镜头回答：

- 这个角色平时如何控制感情。
- 哪些部位最先泄露真实状态。
- 面对不同对象时，表演策略如何变化。
- 情绪强度增大时，哪些特征可以变化，哪些身份特征绝不能变化。
- 角色在最脆弱或最危险的状态下，为什么仍然是同一个人。

情绪形容词可以富有魅力和文学精度，但必须被眼神、呼吸、手部、姿态和行动倾向证明。

## 2. 先锁中性身份基线

Production Lock Pass 在生成情绪版前，先确定一张中性或低强度状态的主参考：

- 同一设定年龄与感知年龄。
- 同一骨相、脸型、五官比例、耳形、发际线和体型。
- 同一健康软组织、脂肪垫支撑和下颌/颈部状态。
- 同一永久皮肤标志、肤色底调和区域纹理。
- 同一发型、妆容、服装、配饰数量、左右与固定点。
- 同一主角选角锚点和自然不对称。

中性基线不等于空洞无神。角色仍要有清醒眼神目标、职业习惯和专属的头颈/重心状态，只是不发生高强度情绪动作。

三视图与表情板默认分开制作。Front/Profile/Back 使用中性、可比对状态；不要把哭泣、咆哮或夸张低头混入三视图，破坏比例和身份校验。

## 3. 角色专属感情词典

不要为所有角色套同一组六种表情。先根据人物欲望、创伤、关系、阶层、职业和控制方式，选择 4–8 个真正会在故事里出现的状态。

形容词应使用精确短语，而不是单词堆叠。可参考但不得固定复用：

| 感情方向 | 精确形容词短语 | 资产设计要观察的差异 |
| --- | --- | --- |
| 亲近 | `guarded tenderness` 有戒心的温柔、`protective affection` 保护性的爱 | 眼神停留、身体是否挡在对方前面、手部是否接近但克制 |
| 丧失 | `contained grief` 压住的悲痛、`quietly devastated` 无声崩坏 | 呼吸、吞咽、眼部湿润、肩颈控制，而非新增衰老 |
| 对抗 | `restrained fury` 克制暴怒、`cold contempt` 冰冷轻蔑 | 下颌、眼睑、握力、身体占位，而非整脸扭曲 |
| 警戒 | `uneasy suspicion` 不安怀疑、`predatory focus` 捕食般专注 | 视线扫描、头部微转、重心与出口关系 |
| 恐惧 | `suppressed panic` 被压住的惊慌、`dread behind composure` 镇定后的恐惧 | 呼吸变浅、冻结或撤退倾向、手指微颤，而非通用尖叫 |
| 羞耻/内疚 | `dignified shame` 保持尊严的羞耻、`private guilt` 私密内疚 | 回避对象、脸部遮挡、身体缩小或自我辩护 |
| 希望/释放 | `fragile hope` 脆弱希望、`relief without trust` 尚未信任的轻松 | 肌肉释放的顺序、首次允许接近、呼吸恢复 |
| 魅力/危险 | `seductive self-possession` 自持魅力、`dangerously amused` 危险兴味 | 对视权、微笑不对称、空间支配，不依赖磨皮油光 |

为角色选词时优先使用：

`主情绪短语 + 反向次情绪 + 对象/关系`

例如 `guarded tenderness toward the younger partner, complicated by fear of attachment`。不要只写 `tender expression`。

## 4. 单个情绪状态的定义格式

每个情绪版本建立一张 `EMOTION PERFORMANCE CARD`：

```text
状态名称：
主情绪形容词：
反向次情绪：
情绪对象与触发：
公开 / 私下 / 伪装：
强度 1–5：
行动倾向：靠近、保护、控制、试探、对抗、逃离、冻结、顺从、掩饰
眼神与眼睑：
眉部：
嘴唇、下颌与吞咽：
呼吸与胸腔：
头颈、肩部与重心：
手部与道具接触：
允许变化：
绝对不可变化：
禁止的夸张表演：
```

形容词不是最后一层装饰，而是用来统一全部可变化字段。若某个字段与情绪无关，不要强行让它变化。

## 5. 生产表情板与电影情绪版的区别

### 生产表情板

目标是验证脸部身份和表演范围。使用一致的头部尺度、机位、焦段、光线、背景、发型和服装，只改变受控的表演变量。适合制作表情/情绪资产库。

### 电影情绪版

目标是验证情绪如何进入场景、关系和摄影。可以改变构图、人物距离、遮挡、动作、焦点和有来源的光线，但必须沿用同一角色 DNA 和影片摄影语法。需要将角色交给 `$craft-cinematic-image-prompts` 完成。

### 同一节拍的表演方案

可以保持剧情动作不变，仅测试人物把情绪公开、藏住或利用它的不同策略。这类版本应说明策略差异，而不是简单替换笑脸、哭脸和怒脸。

## 6. 情绪板构图与摄影

### 独立情绪图

质量优先时，为每种状态输出独立提示词。推荐头肩或胸像、自然中长焦观感、正常工作距离、中等景深、同一眼平机位和同一有方向的柔光。保留耳、下颌和头颅透视，不使用极近广角。

### 一页式生产情绪板

用户明确要求联系表时，可在横向画布中设置 4–8 个等尺寸头肩格：

- 所有头部同尺寸、同裁切、同机位、同焦段、同背景、同光线。
- 按角色故事所需状态排列，不固定“喜怒哀乐”。
- 第一个格可设为中性身份基线，其他格展示受控变化。
- 图内标签只留后期标注区，不依赖生成模型准确书写文字。
- 不与 Front/Profile/Back 三视图强行挤在同一页，除非用户有明确制作版式。

### 摄影限制

- 表情板需要足够景深看清双眼、鼻口和下颌体积，但不做全脸毛孔锐化。
- 光线帮助比较软组织与表演，不使用环灯、clamshell、美容正面填充或戏剧性彩色轮廓光。
- 中性背景和衣领区域保持一致，防止模型用造型变化冒充情绪变化。

## 7. 跨版本一致性

每个情绪版本重复同一简短锁定块：

```text
IDENTITY LOCK
同一演员身份、设定年龄与感知年龄；
同一骨相、脸型、五官比例、耳形、发际线与自然不对称；
同一健康软组织、永久皮肤标志、发型、妆容、服装和配饰；
同一相机高度、工作距离、焦段观感、背景和基础布光；
仅改变本卡片声明的眼神、面部肌肉张力、呼吸、手部和姿态。
```

同一角色可以拥有不同的情绪强度，但不能随情绪切换脸型、年龄、种族特征、体脂、发型、妆容风格、配饰左右或服装设计。

## 8. 真人年龄、皮肤与主角感保护

- 悲伤不得通过深眼袋、法令纹、面颊下垂和松颈把人物突然做老。
- 疲惫与恐惧属于当前状态，不改写永久软组织；只表现有限眼部充血、呼吸、姿态和注意力变化。
- 愤怒不得让鼻、嘴、下颌比例变化或把面孔压成怪相。
- 微笑不得默认露出全部牙齿，也不得自动瘦脸、提亮眼白或消除天然纹理。
- 魅惑不得转成美容广告：不磨皮、不玻璃肌、不环灯、不撅嘴、不无对象地看镜头。
- 高强度情绪仍要保留一至三个主角选角锚点；失控不等于失去人物目标。
- 表情纹只随肌肉运动在合理区域暂时出现，放松后不应变成永久深皱纹。

## 9. 提示词模板

### 独立情绪资产图

```text
photographed live-action human subject, the exact same established character identity,
[age, casting anchors, hair, costume and accessory lock],
[primary emotion phrase] complicated by [counter-emotion], directed toward [specific target],
[public/private/concealment strategy], intensity [1–5],
visible through [eye and eyelid behavior], [mouth/jaw/breath behavior], [head-neck/shoulder/hand behavior],
[specific action tendency without changing identity],
consistent eye-level camera, natural medium-telephoto portrait perspective, normal working distance, medium depth of field,
the same motivated soft key and restrained negative fill, the same neutral background,
age-appropriate healthy soft-tissue support, regional skin texture and limited natural skin sheen,
temporary expression lines only where muscles are active, no identity or age drift
```

### 一页式情绪板

```text
horizontal production emotion reference sheet for one and the same live-action character,
[4–8] equal head-and-shoulder panels, identical head scale, crop, camera height, lens perspective, background, wardrobe, hair, makeup and lighting,
panel one: neutral identity baseline with alert character-specific presence,
remaining panels: [story-derived emotion states, each with a distinct target, concealment strategy and visible performance evidence],
same facial bone structure, age, healthy soft tissue, permanent skin marks, natural asymmetry and accessories in every panel,
only expression, gaze, breath, hand tension and posture may change,
clean gutters and blank caption areas for post-production labels, no generated typography
```

## 10. 失败模式与负面提示词

按需排除：

- generic expression sheet, fixed happy-sad-angry-surprised emoji set
- theatrical grimace, melodramatic crying, default screaming, open-mouth fear
- vacant stare, eye line without target, random tears without cause
- face identity drift, age drift, bone-structure drift, changing body type
- grief rendered as aging, anger rendered as facial deformation
- deep permanent wrinkles created by temporary emotion
- beauty-ad seduction, pout, glass skin, oily face, ring-light catchlights
- airbrushed skin, wax skin, game-CG face, over-sharpened iris and pores
- changing hairstyle, makeup, costume, accessories, left-right placement or permanent marks
- inconsistent head scale, camera height, focal perspective, crop, lighting or background
- duplicated stranger faces, contact-sheet layout errors, generated gibberish labels

不要用 `no emotion`、`expressionless` 等宽泛负面词修理夸张表演；它们会把角色压成证件照。应具体排除错误的表演方式，同时保留角色应有的魅力和情绪范围。
