# 真人演员电影摄影、视效整合与低修图

## 目录

1. 真实感优先级
2. 角色身份继承
3. 镜头与摄影距离
4. 感知年龄与软组织状态
5. 主角选角与镜头存在感
6. 剧情布光与皮肤反光
7. 实景光与视效光
8. 环境介质与妆效
9. 数字中间片与低修图
10. 提示词模块
11. 自检

## 1. 真实感优先级

把人类角色呈现为在真实片场中被摄影机记录的演员，而不是经过 PBR 渲染的数字资产。真实感按以下顺序建立：

`身份与年龄 → 骨骼/软骨/肌肉/脂肪垫 → 表演和重力 → 光线与曝光 → 区域性皮肤纹理/反光 → 环境状态 → 克制后期`

不要颠倒成“高频毛孔、锐利虹膜、全脸高光、电影 LUT”。超写实来自人体、光学和环境之间的一致关系，不来自纹理数量。

真实感不要求人物显老。年轻、紧致、健康、具有主角魅力的脸同样可以保留毛孔、细毛、肤色差和真实光学；不要以皱纹、重眼袋、面颊下垂、赘肉或苦相替代电影真实性。

本参考的完整章节用于 Production Pass。Hero Concept Pass 只保留自然透视、真实演员表演、主角眼神和一到两句皮肤可信度，避免把完整低修图清单变成第一张图的生产规格。

人物正向描述优先使用：

- `photographed live-action human performance`
- `real actor captured in a narrative film frame`
- `biologically credible facial soft tissue`
- `region-specific skin texture and reflectance`
- `minimally retouched cinematic skin`

谨慎或禁止默认使用：

`digital human`, `PBR skin`, `3D character render`, `hyperreal skin shader`, `ultra-detailed pores`, `flawless skin`, `glass skin`, `glowing face`, `razor-sharp face`, `perfect symmetry`。

## 2. 角色身份继承

角色若来自 `$craft-production-design-prompts` 或参考图，先建立并重复以下锁定：

```text
LIVE-ACTION IDENTITY LOCK
age and current health state:
target perceived age range and forbidden aging cues:
bone structure and facial proportions:
age-specific elasticity, fat-pad support and healthy soft-tissue volume:
natural asymmetry:
skin undertone and regional color variation:
permanent marks: moles / freckles / sunspots / scars / acne marks:
hairline, hair and facial hair:
eye, sclera, lip and teeth characteristics:
costume and visible accessories:
current temporary state: sweat / rain / dust / blood / makeup / injury:
forbidden identity changes:
lead-performer casting anchors, gaze intention and posture:
```

电影镜头可以改变表情、姿态、光线、湿度、污染和损伤，但不得擅自改变年龄、骨相、脂肪位置、肤色底调、永久标志、发际线和天然不对称。

## 3. 镜头与摄影距离

- 面部特写优先采用 75–105 mm 等效的自然中长焦观感；头肩、中近景可使用 50–85 mm。
- 32–50 mm 可用于人物与环境共同叙事，但保持正常工作距离，让脸部远离边缘。
- 21–35 mm 贴近人物只用于主观压迫、混乱、危险或身体性；透视变形必须有叙事意义。
- 不通过镜头贴脸获得大特写；鼻子、远侧眼和耳朵不得无意夸张或缩小。
- 近景通常使用中等景深。焦点落在近侧眼、双眼平面、表情肌或关键伤痕；远侧耳朵和背景可自然软化。
- 动作镜头可以让肢体末端、发丝和近镜粒子产生方向性模糊，但眼神、决定性表情或接触点至少保留一个清晰锚点。
- 锐度必须随焦平面、运动速度、面部曲率和镜头距离衰减；禁止整张脸与背景同样锐利。

## 4. 感知年龄与软组织状态

- 将感知年龄锁定在设定年龄约 ±3 岁内；妆效、重病、极端疲劳或超自然衰老必须由剧情明确授权。
- 疲劳优先通过眼神聚焦、眼周色差、眨眼张力、呼吸和姿态表现，不自动增加永久眼袋、深皱纹、法令沟和松弛。
- 肉感表示健康皮下体积、弹性、含水量、面颊支撑与肌肉覆盖，不表示浮肿、下垂、嘴角赘肉、双下巴或松颈。
- 18–29 岁角色静止时通常只有极少静态纹；30–39 岁可有少量动态纹或浅变化；40–55 岁只选择少数年龄信号，不把全部皱纹、眼袋、法令纹和松弛同时叠加。
- 只有设定年龄、体脂、健康或剧情明确要求时，才加入明显眼袋、面颊下垂、jowls、双下巴、深颈纹和松弛皮肤。

先建立活体组织的重量和连续性：

- 眼睑有厚度并包覆眼球；眼下由眼轮匝肌、泪沟、脂肪支撑和当前疲劳共同形成。
- 面颊由骨性突出、皮下脂肪、弹性、肌肉牵拉和重力组成连续曲面；年轻与壮年主角保持清楚的向上支撑，不是硬雕刻切面，也不是下垂赘肉。
- 鼻翼、鼻尖和耳廓具有软骨厚度与柔度，不像塑料组件。
- 鼻唇沟、嘴角和下颌随表情、年龄、体脂、头部朝向与重力变化，不是固定深槽。
- 奔跑、呼喊、受击、哭泣或屏息会改变面颊压缩、颈部肌腱、鼻翼张力、唇部含水状态和血色；这些变化必须服从动作。
- 风、加速度和冲击主要影响头发、细毛、皮肤松弛处、衣领和配饰；不让整张脸像橡胶面具同步变形。

毛孔和皱纹必须附着于上述体积，并随伸展、压缩、焦平面、汗水和入射光改变可见度。

## 5. 主角选角与镜头存在感

主角感来自“观众相信摄影机会持续追随这个人”，而不是传统美型评分。

- 为主角选择一至三个稳定选角锚点：眉眼关系、眼形、鼻梁轮廓、唇线、疤痕、发际线、脸型节奏或独特轻微不对称。
- 使用 `distinctive live-action lead casting`, `lead-performer screen presence`, `clear intentional gaze`, `controlled head-and-neck posture`, `quiet confidence` 等可执行语言。
- 主角眼神必须清醒并指向目标；中性、克制或悲伤不等于无神、呆滞或背景演员状态。
- 头颈舒展、下巴自然回收、肩线稳定、重心明确；除非镜头表达失败或崩溃，不默认塌肩、缩颈、耷拉嘴角和被动站姿。
- 通过焦点、局部对比、眼神光、轮廓、色彩锚点、负空间和其他人物视线形成第一视觉层级。主角不必居中或最亮，但不得被背景、烟雾、配角和特效吞没。
- 主角可以自然、粗粝、普通、苍白或带伤；仍保持辨识度、意志与镜头控制力。不要依靠削尖下颌、大眼、完美对称和无瑕皮肤制造主角感。

## 6. 剧情布光与皮肤反光

先用主光建立真实面部体积，再决定是否让剧情隐藏或破坏部分信息。

- 主光必须来自太阳、天空、窗口、门、灯具、火焰、屏幕或已定义视效源之一。
- 使用负补光或受控环境填充，让暗侧比受光侧更低，同时保留叙事需要的眼神和轮廓。
- 额头：以漫反射为主，只保留不连续皮脂微光。
- 鼻梁/鼻尖：可有较明确但被毛孔与曲率打断的高光。
- 上颧骨：允许弱扩散光泽；下颊、咬肌区、下颌和颈部通常更哑光。
- 眼睑边缘、泪线和内唇：只允许小范围含水反光。
- 皮肤高光内部保留肤色、纹理和细毛，不无条件剪切为白色。
- 眼神光只来自已定义光源；数量、形状和方向与摄影机和演员位置一致。

除非用户明确要求美容广告，禁止环灯、clamshell、正面 beauty dish、轴线 butterfly light、左右对称柔光箱、无方向包围光、全脸辉光和多重矛盾眼神光。

## 7. 实景光与视效光

把火光、霓虹、屏幕、车灯、能量体和爆炸当成有位置、面积、方向和衰减的真实附加光源。

- 只照亮朝向光源的面部曲面；鼻梁、眉骨、眼窝、头发和手会产生遮挡。
- 光源越近，局部色染和亮度越强；沿面部和身体随距离自然衰减。
- 火光产生暖色、不稳定、低位或侧位的变化；不让整张脸固定橙化。
- 屏幕光可以在眼睛、鼻梁和上颧骨形成有限色染，但必须保留肤色底调和暗侧。
- 能量光可以比现实灯光更特殊，但仍必须定义传播方向、照亮范围、反作用和曝光上限。
- 爆炸或强能量可造成局部高光剪切和短暂曝光污染，但不能永久改写皮肤材质。
- 发光粒子只在靠近皮肤时形成小尺度移动反射；远处粒子不能逐粒照亮整张脸。
- 禁止皮肤整体自发光、无来源轮廓描边、金属反射、玻璃高光、荧光毛孔和均匀彩色遮罩。

## 8. 环境介质与妆效

- 汗液集中在额头局部、发际线、鼻部、上唇、颈部和衣领接触区，沿重力汇聚；不平均涂满全脸。
- 雨水形成不同尺度液滴、流痕和湿发贴合，并改变局部反光；仍保留皮肤纹理与体积。
- 灰尘、煤尘和灰烬附着于迎风面、湿润处、毛发、皱褶和皮脂区域；皮肤活动处可出现擦除和裂纹。
- 血液必须有伤口或接触来源、流动路径、干湿阶段和颜色变化；不作为随机红色装饰。
- 烧伤、冻伤、淤青、苍白、缺氧和发热需要明确生理位置与阶段；妆效叠加在身份之上，不替换整张脸。
- 烟雾可以遮挡、软化和色染人物，但其密度、方向和距离决定影响范围；禁止均匀雾化磨皮。

## 9. 数字中间片与低修图

电影调色可以改变整体色彩关系和曝光重心，但不能抹除真人皮肤的内部差异。

必须保留：

- 痣、雀斑、晒斑、浅疤、痘印、色素沉着和年龄纹理。
- 设定或参考图中真实存在且符合年龄的眼下轮廓、鼻唇过渡、颈部状态、细绒毛、胡茬、局部毛细血管和天然不对称；不主动增加眼袋、深沟、松弛和颈纹。
- 额头、鼻部、眼周、面颊、口周、下颌、耳朵与颈部之间不同的颜色、粗糙度和反光。

只允许局部清理：

- 生成纹理接缝、异常色块、传感器污点、妆效边缘和单个无意义死白油点。
- 确实遮住眼神或关键轮廓的少量偶发干扰；保留自然碎发、灰尘和汗水。

禁止：

- 全局磨皮、频率分离熨平、美白、瘦脸、祛眼袋、去痣斑、年龄消除和完美对称化。
- HDR 局部对比、阴影过度抬升、高光压平、全局降噪、清晰度/纹理拉满和高反差锐化。
- 眼白与牙齿漂白、虹膜锐化、嘴唇塑料化、只贴在皮肤上的假颗粒。

颗粒、锐度和色彩噪声应跨越皮肤、服装、环境和空气介质，服从同一个摄影系统。

## 10. 提示词模块

### 正向核心块

```text
Photographed as a real live-action lead performance inside a narrative film frame. Perceived age precisely matches the specified range, with no age inflation. Preserve the locked bone structure, elastic age-appropriate fat-pad support, healthy natural facial volume, clear eyelid support, continuous cheeks, a clean non-sculpted jaw transition, permanent skin marks and natural left-right asymmetry; no unintended wrinkles, heavy eye bags, sagging cheeks, jowls, puffiness or double chin. Biologically credible living soft tissue before surface detail; authentic region-specific skin texture, pigmentation and reflectance rather than a digital skin shader.

Distinctive live-action lead casting with one to three memorable facial anchors, calm focused eyes, a clear intentional gaze, controlled head-and-neck posture and quiet protagonist authority. The character holds first visual priority through focus, local contrast, eye light, silhouette and spatial relationships, never through beauty-filter perfection.

The motivated key light establishes continuous facial volume, while practical and VFX light affect only the facial planes oriented toward their defined sources, with anatomical occlusion and distance falloff. Broken localized sebum highlights remain on the forehead and nose, faint diffuse sheen on upper cheekbones, more matte lower cheeks, jaw and neck, and limited moisture on eyelid margins and inner lips. VFX color spill remains local and translucent, preserving skin undertone, pores, vellus hair, age lines and scars; no self-emissive skin or uniform facial glow.

Minimally retouched cinematic skin, preserving identity-bearing marks, age, under-eye structure, facial hair, regional color variation and environmental state. Focus-plane-appropriate sharpness, natural optical detail falloff, protected skin-toned highlights and restrained grain shared by subject and environment.
```

### 负向核心块

把年龄和体型相关词视为条件模块。只有特征超过角色的设定年龄、体脂、健康、参考图或妆效锁定时才加入；老年、肥胖、疾病或明确松弛角色应保留其真实身份，只禁止进一步年龄膨胀和无授权重塑。

```text
game CG face, video-game character render, digital human, MetaHuman look, digital sculpture, 3D render, PBR skin, wax figure, silicone skin, rubber skin, plastic skin, porcelain skin, glass skin, mannequin face, beauty-filter face, airbrushed skin, beauty retouching, skin smoothing, flawless perfect skin, poreless skin, uniform procedural pores, pore stamp, hyper-detailed pores everywhere, texture without soft-tissue volume, excessive subsurface scattering, full-face oily sheen, mirror-like skin, metallic skin, uniform facial reflectance, self-emissive skin, glowing facial texture, fluorescent pores, uniform VFX color wash, glowing head outline, no-falloff light spill, multiple contradictory catchlights, ring-light catchlight, clamshell beauty lighting, frontal beauty dish, shadowless face, de-aged face, age inflation, older-than-specified appearance, prematurely aged face, excessive age-inappropriate wrinkles, deep static forehead lines, heavy under-eye bags, deeply carved nasolabial folds, sagging cheeks, jowls, drooping mouth corners, loose neck skin, puffy lower face, unintended double chin, bloated face, passive background-character presence, empty unfocused gaze, collapsed neck posture, slumped shoulders, protagonist out of focus, protagonist underexposed, supporting character stealing visual priority, removed moles and scars, perfect facial symmetry, enlarged eyes, pure white sclera, glowing iris, plastic glossy lips, blue-white teeth, HDR face, aggressive denoising, excessive clarity, over-sharpened skin, fake grain only on skin, wide-angle facial distortion, shallow-focus beauty portrait
```

## 11. 自检

- 人物是否首先像真实演员，其次才像“高质量图像”？
- 年龄、骨相、脂肪垫、眼睑、面颊和下颌软组织是否在剧情光下仍然成立？
- 感知年龄是否与设定年龄接近，且没有因“真实感、疲惫或有故事”被无故老化？
- 肉感是否表现为弹性、健康体积和支撑，而不是赘肉、松弛、浮肿或双下巴？
- 主角是否拥有清醒眼神、明确目标、稳定头颈、一至三个选角锚点和第一视觉层级？
- 毛孔、色差和反光是否按面部区域变化，而不是统一材质贴图？
- 主光、实景光和视效光是否各有来源、方向、遮挡和距离衰减？
- 视效色染是否只影响朝向光源的曲面，并保留暗侧与肤色底调？
- 汗、雨、灰尘、血液和妆效是否有来源、路径、阶段和局部附着？
- 是否保留痣斑、浅疤、眼袋、胡茬、颈纹、细毛和天然不对称？
- 调色、降噪、锐化和颗粒是否服从整个摄影系统，而不是只重建皮肤？
- 是否仍存在任何游戏 CG、数字人、蜡像、美容广告、玻璃肌、全脸油光或自发光皮肤感？
