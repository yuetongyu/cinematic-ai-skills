# 真人面部摄影与电影级低修图

## 目录

1. 目标与禁用方向
2. 光学与景深
3. 软组织肉感
4. 皮肤区域差异
5. 真人五官
6. 布光与反光控制
7. 低修图标准
8. 年龄校准、主角感与肤色
9. 提示词模块
10. 自检

## 1. 目标与禁用方向

把人物呈现为真实演员经过克制摄影和数字中间片处理后的角色参考，不呈现为游戏 CG、数字雕塑、3D 渲染、MetaHuman、蜡像、美容广告或高频精修时尚肖像。

人物正向提示词优先使用：

- `photographed live-action human subject`
- `live-action casting and wardrobe reference photograph`
- `minimally retouched cinematic portrait`
- `authentic human skin and biologically credible soft tissue`

谨慎或禁止默认使用：

`flawless skin`, `perfect skin`, `smooth skin`, `porcelain complexion`, `glass skin`, `radiant skin`, `glowing face`, `ultra-detailed pores`, `razor-sharp face`, `hyperreal skin texture`, `symmetrical face`, `digital human`, `PBR skin`, `3D render`。

“超写实”只能作为整体目标，不能用毛孔数量、锐化和全脸反光代替真实人体。

“反美颜”也不能被理解成主动增加年龄。真实皮肤可以年轻、紧致、健康并具有镜头吸引力；不要用皱纹、眼袋、法令纹、面颊下垂和赘肉证明真实。

本参考主要服务 Production Lock Pass。Hero Concept Pass 只取一到两句真人摄影可信度，不要把本文件的完整皮肤、年龄和负面模块直接塞进第一张英雄概念图。

## 2. 光学与景深

- 纯面部/身份参考使用全画幅等效 85–105 mm 的自然中长焦观感。
- 头肩或上半身使用 70–100 mm；避免 24–50 mm 近距离贴脸导致鼻部膨大和耳部缩小。
- 保持正常肖像工作距离，通过焦段和裁切获得特写，而不是把镜头逼近脸部。
- 面部参考使用约 f/5.6–f/8 的中等景深观感；头肩肖像使用约 f/4–f/5.6。
- 双眼、鼻翼、嘴唇和近侧耳部应可读；远侧耳朵可自然软化，但不能变成奶油虚化。
- 对焦落在近侧眼或双眼平面。锐度随焦平面和曲率自然衰减，不让虹膜、鼻尖、耳朵、发丝和背景同样锐利。

## 3. 软组织肉感

先建立头骨、软骨、肌肉、脂肪垫、皮肤厚度、弹性和重力，再添加毛孔与色斑。软组织肉感指活体组织的连续体积、含水量、回弹与支撑，不等于松弛、臃肿或赘肉。

- 面颊具有年龄相符的皮下脂肪、含水组织、弹性和向上支撑，不是硬质雕刻切面；年轻或壮年角色不默认面颊下垂、口角赘肉或下半脸沉重。
- 眼下表现眼轮匝肌、泪沟、年龄相符的脂肪支撑和眼睑厚度，不画成锐利黑线，也不完全磨平。
- 鼻翼、鼻尖和耳廓具有软骨厚度、组织柔度和轻微不对称，不像硬塑料零件。
- 鼻唇沟、嘴角和木偶纹由表情、重力和组织体积形成，不是等宽深槽。
- 下颌线服从体脂、年龄和姿态；可以清楚、利落而仍然真实，不使用持续发亮的刀削 CG 边缘，也不默认加入双下巴、下颌赘肉或松弛口角。
- 颈部按年龄和姿态呈现皮肤、肌腱与衣领接触；年轻角色不默认加入深颈纹、松皮或颈部脂肪堆积。
- 保留左右眼睑开合、面颊饱满度、嘴角高度、鼻翼宽度和耳位的轻微天然差异。

毛孔必须附着于真实软组织表面。禁止在光滑模型脸上覆盖均匀噪点或程序化孔洞。

## 4. 皮肤区域差异

脸部不是统一颜色、统一粗糙度和统一毛孔的材质贴图。

- 额头：较平整，可有轻微、不连续的皮脂微光和细小横纹。
- 眉间/鼻翼：可有皮脂丝、毛细血管和局部泛红。
- 鼻梁/鼻尖：高光相对明确，但必须被毛孔和微小起伏打断，保留高光内部颜色与纹理。
- 上颧骨：允许柔和扩散光泽；下颊、咬肌区和下颌通常更哑光。
- 面颊：保留肤色渐变、毛囊、细绒毛、淡斑和不连续红润。
- 眼周：皮肤更薄、纹理更细，可出现青、紫、红褐、黄或橄榄色过渡。
- 口周/下巴：保留毛囊、唇周色沉、剃须痕迹或激素性色差。
- 嘴唇：保留纵向唇纹、干湿变化和不规则色泽；反光只出现在内唇和局部纹理凸起。
- 耳朵/颈部：与面部有连续但不完全相同的血色、日晒和阴影变化。

毛孔尺度、方向、密度和清晰度必须随区域改变。不要让整张脸的毛孔同样大小、同样锐利或形成规则点阵。

## 5. 真人五官

### 眼睛

- 眼球真实嵌入眼眶并由有厚度的上下眼睑包覆。
- 眼白为暖灰或微蓝灰，保留极轻微血丝、泪膜、眼角红润和眼睑投影，不使用纯白。
- 虹膜细节受光线、瞳孔和焦距限制，不做成宝石或游戏贴图。
- 角膜高光只来自已定义主光，通常保留一个主要眼神光；两眼反光可因角度略有不同。
- 泪线只形成细小局部反光，不让眼球变成玻璃球。

### 嘴唇与牙齿

- 嘴唇保留纵向纹理、自然不对称、边缘色素过渡、局部干燥和口角暗部。
- 湿润高光局限在内唇或少量纹理凸起，禁止整片镜面唇釉。
- 牙齿为带暖色的象牙白，保留轻微色差、透明边缘和自然排列，不做蓝白瓷贴面。

### 耳朵

- 保留耳轮、对耳轮、耳甲腔、耳屏、耳垂和耳后连接厚度。
- 耳甲腔和耳后有柔和遮蔽阴影；薄耳轮可轻微暖色透光，但不形成发光红边。
- 保留耳部毛孔、细毛、血色和左右轻微不对称，避免低模、橡胶或蜡质耳朵。

## 6. 布光与反光控制

- 使用一个可追溯的宽大方向性柔光作为主光，位于镜头轴线一侧约 30–50°、高于眼睛约 15–30°。
- 让主光形成额头、眼窝、鼻侧、面颊、唇下和下颌的连续柔软明暗转折。
- 在暗侧使用克制负补光，使暗侧低于受光面约 1.5–2.5 挡，同时仍保留眼睛、耳部和皮肤信息。
- 仅使用极弱环境回填，不用强轴线填充抹平鼻侧、眼袋、法令区和下颌体积。
- 高光必须细碎、局部、非均匀，并与光源方向、皮脂、水分、曲率和细毛一致。
- 允许额头局部、鼻梁鼻尖、颧骨上缘、泪线和下唇出现不同强度的有限反光；面颊下部、眼周、下颌和颈部更哑光。
- 眼神光只与主光一致，不叠加环灯、双条形灯或多个矛盾反射。

除非用户明确要求美容广告，禁止环形灯、clamshell、正面 beauty dish、轴线 butterfly beauty light、左右完全对称柔光箱、无方向包围光、纯白高键冲洗、强轮廓光、彩色美容边光和皮肤辉光滤镜。

## 7. 低修图标准

修图只能清理临时干扰，不能重建人物面貌、年龄、肤色或皮肤材质。

### 必须保留

- 痣、雀斑、晒斑、色素沉着、胎记、浅疤和痘印。
- 设定或参考图中真实存在、且符合年龄的泪沟、眼下轮廓、鼻唇过渡、表情纹与组织状态；不要把“保留”误解成主动新增眼袋、深沟和松弛。
- 细绒毛、皮脂丝、毛囊、局部泛红、毛细血管和左右轻微不对称。
- 不同区域与面部/耳朵/颈部/手部之间连续但真实的肤色差异。

### 只允许局部修复

- 偶发发炎痘、破皮、结痂、化妆残渣、灰尘、纤维和传感器污点。
- 单个刺眼油点、压缩/抠像/生成造成的纹理接缝和异常色块。
- 确实遮挡眼睛或破坏轮廓的单根杂乱发丝；保留自然碎发与绒毛。

禁止全局磨皮、频率分离熨平、液化瘦脸、祛眼袋、去痣去斑、美白、统一红润、全局降噪、HDR 局部对比、去雾、清晰度、纹理拉满、高反差锐化、虹膜锐化、眼白/牙齿漂白和完全对称化。

锐化只服从焦平面，在睫毛、眉毛、虹膜边缘、嘴唇局部和关键服装细节中克制出现。轻微颗粒必须跨越皮肤、服装和背景，不能只贴在皮肤上伪造真实。

## 8. 年龄校准、主角感与肤色

### 感知年龄锁定

- 用户给出准确年龄时，让画面感知年龄通常落在该年龄约 ±3 岁内。剧情性重病、极端失眠、妆效或超自然衰老必须单独声明，不能自动发生。
- 用户只给年龄段时，先写清目标区间和禁止越界的老化特征。
- 用户未提供年龄时，根据职业、剧情与参考图合理补全，但不得用皱纹和下垂作为“有故事”的默认符号。
- 疲惫主要通过眼神聚焦程度、眼周色差、姿态和表情肌张力表现；不要自动转换成永久眼袋、深皱纹、松弛下颌和年长十岁的脸。
- 消瘦主要改变脂肪厚度和骨性可见度；不要自动增加皱纹。强壮或有肉感主要改变健康体积与肌肉支撑；不要自动增加浮肿、赘肉和双下巴。

年龄阶段只选择真正需要的少量信号，不把全部信号同时叠加：

- 青少年：高弹性、细纹极少、自然皮脂变化和可能的痘印；不使用成人静态纹或下垂。
- 18–29 岁：稳定而有弹性的脂肪垫、清楚但不刀削的下颌、静止时极少静态纹；允许细毛、毛孔、局部泛红和轻微眼下色差。
- 30–39 岁：整体支撑仍清楚，可有少量动态纹或非常浅的静态变化；不默认深法令纹、重眼袋、面颊下垂或颈部松弛。
- 40–55 岁：选择性加入少量真实年龄信号，例如眼周细纹、肤色变化或轻微组织变化；不要同时叠加深额纹、重眼袋、深法令沟、赘肉和松颈。
- 56–69 岁：允许更明确的皮肤厚度、色斑和组织支撑变化，但仍服从个人体脂、健康与护理状态。
- 70 岁以上：允许皱纹层级、皮肤变薄、松弛和血管变化；仍避免均匀皱纹贴图和“所有老人都相同”的模板脸。

### 主角选角感

主角可以自然、粗粝、普通甚至带伤，但必须具有镜头吸引力和可重复辨识度：

- 选择一至三个明确选角锚点，例如特别的眼形/眉眼关系、鼻梁轮廓、嘴角状态、发际线、疤痕或脸型节奏；不要把所有五官都平均化。
- 使用 `lead-performer screen presence`, `distinctive live-action casting`, `calm focused gaze`, `controlled head-and-neck posture`, `quiet confidence` 等表演与选角语言。
- 让双眼清醒、视线有目标、眼睑不过度沉重；中性表情不等于空洞、疲惫或无反应。
- 保持头颈舒展、下巴自然回收、肩线稳定；避免畏缩、塌颈、耸肩和无意识张嘴。
- 用发型轮廓、服装上半身、配饰和轻微不对称增强身份；不要依靠削脸、大眼、尖鼻或无瑕皮肤制造主角感。
- 设定板保持中性摄影，但允许主角面部获得最清楚的焦点、最完整的眼神光与最好的轮廓可读性。

- 深肤色保留丰富暖冷层次和高光中的肤色信息，不提亮成灰紫或压成无细节暗块。
- 浅肤色保留血管、红润、雀斑、晒斑和黄暖变化，不统一粉白。
- 橄榄肤色不自动校正成粉红或橙色。
- 东亚肤色不默认冷白玻璃肌，保留黄、橄榄、红润、日晒和局部色差。
- 棕色肤色不统一橙化，也不用过度青绿阴影制造电影感。

## 9. 提示词模块

### 正向核心块

```text
Photographed as a real live-action human subject with natural medium-telephoto perspective, normal portrait working distance and medium depth of field. One large directional diffused key light placed 30–50 degrees off camera axis and slightly above eye level, gentle falloff across the face, restrained negative fill on the shadow side, one coherent catchlight, no frontal beauty fill.

Perceived age precisely matches the specified age range, with no age inflation. Biologically credible facial soft tissue over bone and cartilage, elastic age-appropriate fat-pad support, healthy natural subcutaneous volume, clear eyelid support, continuous cheek volume and a clean but non-sculpted jaw transition; no unintended jowls, sagging cheeks, puffiness or double chin. Authentic human skin with region-specific texture: irregular pores, fine vellus hair, subtle capillary and pigmentation variation, preserved identity marks and natural left-right asymmetry. Localized broken sebum highlights on the forehead and nose, faint diffuse sheen on upper cheekbones, more matte lower cheeks and jaw, localized moisture on eyelid margins and inner lips, no uniform facial gloss.

Distinctive live-action lead casting with one to three memorable facial anchors, calm focused eyes, a clear intentional gaze, controlled head-and-neck posture and quiet protagonist presence. Cinematically attractive through identity, intelligence and composure rather than facial perfection or beauty-filter reconstruction.

Minimally retouched cinematic portrait; retouching is limited to temporary distractions, preserving age-specific folds, moles, freckles, faint scars, under-eye chromatic variation, expression lines and nonuniform skin tone. Gentle optical softness, focus-plane-appropriate sharpness and subtle grain across the entire image.
```

### 负向核心块

以下年龄和体型词是条件模块，只在它们与设定年龄、体脂、参考图或剧情冲突时使用。老年、肥胖、疾病、疲劳妆效或明确具有眼袋/皱纹/松弛特征的角色，应保留相符特征，只排除进一步的年龄膨胀和身份漂移。

```text
game CG face, video game character render, digital human look, MetaHuman look, digital sculpture, uncanny digital double, wax figure, silicone skin, plastic skin, rubber skin, porcelain skin, glass skin, doll-like face, mannequin face, beauty filter, beauty retouching, airbrushed skin, over-retouched face, skin smoothing, poreless skin, flawless perfect skin, uniform pore field, procedural pores, pore stamp, repeated circular pores, hyper-detailed pores everywhere, synthetic microdetail, orange-peel texture, excessive subsurface scattering, glowing skin, full-face oily sheen, mirror-like skin, wet plastic highlights, uniform facial reflectance, clipped white highlights, metallic skin, hard glossy jawline, excessive clarity, over-sharpening, halo sharpening, HDR face, aggressive denoising, frequency-separation look, fake film grain applied only to skin, de-aged face, age inflation, older-than-specified appearance, prematurely aged face, excessive age-inappropriate wrinkles, deep static forehead lines, heavy under-eye bags, deeply carved nasolabial folds, sagging cheeks, jowls, drooping mouth corners, loose neck skin, puffy lower face, unintended double chin, bloated face, gaunt prematurely aged face, liquified jaw, enlarged eyes, pure white sclera, glowing eye whites, over-sharpened iris, neon iris, multiple catchlights, ring-light catchlight, Hollywood-white teeth, uniform porcelain veneers, painted lips, plastic glossy lips, perfect facial symmetry, empty unfocused gaze, passive background-character presence, collapsed neck posture, slumped shoulders, ring light, clamshell lighting, frontal beauty dish, butterfly beauty lighting, symmetrical twin softboxes, shadowless face, high-key cosmetic advertising, excessive rim light, colored beauty rim, glamour diffusion, dreamy skin glow
```

## 10. 自检

- 面部是否先有真实软组织体积，再有微观纹理？
- 毛孔是否按区域变化，而不是均匀毛孔贴图？
- 额头、鼻部、颧骨、面颊、眼周、下颌和颈部是否具有不同光泽？
- 高光中是否保留肤色和纹理，且没有大面积死白？
- 眼白、牙齿和嘴唇是否保留自然颜色与局部纹理？
- 是否保留年龄、永久标志、肤色底调和轻微不对称？
- 感知年龄是否与设定年龄接近，且没有因“真实感”被无故老化？
- 面颊、下颌和颈部是否具有年龄相符的支撑与弹性，而不是赘肉、松弛或双下巴？
- 主角是否拥有清醒眼神、明确视线、稳定头颈和一至三个可重复选角锚点？
- 主光是否有明确方向，负补光是否恢复面部体积？
- 是否只有一个与主光一致的主要眼神光？
- 修图是否只清理临时干扰，而没有重塑年龄、脸型和皮肤？
- 是否仍存在任何游戏 CG、蜡像、美容广告、磨皮、玻璃肌、全脸反光或程序化毛孔感？
