# BODY2 相关文献清单（2026-09-10 检索）

按**对你当前工作的用处**分组，不按学科分。每条给了链接、是否开放获取（OA），以及"用在哪一步"。
已有的两篇（Fish 2020 *The dog paddle*、Cui 2026 arXiv 2603.04073 ACPPO-PID）不再重复列出。

---

## 一、必读：直接支撑你已经做完的结论

### 1. Fish (1984)《Mechanics, power output and efficiency of the swimming muskrat》
*Journal of Experimental Biology* 110: 183–201 · [作者主页免费 PDF](https://www.wcupa.edu/sciences-mathematics/biology/fFish/documents/1984JEBMuskratMechanics.pdf) · **OA**

**这是你仿生对象（muskrat 麝鼠 / 水老鼠）本身的定量测量，且数字和 V3 惊人吻合。**已核对原文页码：
- 划水相 0.18 ± 0.01 s，回收相 0.22 ± 0.01 s → **占空比 0.45**（p. 191）——与你 CFD 选出的 V3（DUTY = 0.45）完全相同，纯属独立佐证。
- 划频在 0.2–0.75 m/s 全速度段**恒定在 2.5 ± 0.06 Hz**，动物靠**加大摆幅**而不是提高频率来提速（p. 190）。这与你"提高速率"的路线相反，值得在报告里讨论。
- 回收相桨的阻力**只有划水相的 33 %**（p. 194），靠趾收拢 + 足旋后把迎流面积减少 **55.5 %**（p. 194）——你的扇形脚蹼开合比是 20.0/13.3 = 1.5×（面积减少 33 %），**比麝鼠弱不少**，说明收拢宽度 CLOSED_W 还有优化空间。
- 回收相耗功是划水相的 20–39 %（p. 194）；最大机械效率 0.33（p. 197–198）。

用途：写作时的生物学基准（Kap. 2 仿生依据）；论证 DUTY 0.45 的选择；论证 CLOSED_W 该做小。

### 2. Csillag & Ribak (2025)《Underwater paddling kinematics and hydrodynamics in a surface swimming duck versus a diving duck》
*J. Exp. Biol.* 228(9): jeb249274 · [DOI 10.1242/jeb.249274](https://doi.org/10.1242/jeb.249274) · **OA**

**直接支撑我们上周关于 F_z（垂向力，Vertikalkraft）的讨论。**水面型（鸳鸯）的蹼产生**向上**的力，与自身浮力对抗；潜水型（潜鸭）低头约 16°、行程弧更小，把足力指向**向下**，作者证明这才是水平游动的高效运动学。也就是说：垂向分量的方向和大小是被行程平面姿态决定的设计变量，不是副产品。
另注：两种鸭子的划水相都**短于**回收相，与你的"短回收更好"相反 —— 这个矛盾值得在报告里明说（动物在省代谢能和控浮，机器人不需要）。

用途：F_z 一节的文献支撑；V3 降中心角（把力矢量倾角从 20° 压到 8°）的生物学对照。

### 3. Ribak & Gurka (2023)《The hydrodynamic performance of duck feet for submerged swimming resembles oars rather than delta-wings》
*Scientific Reports* 13: 16217 · [DOI 10.1038/s41598-023-42784-w](https://doi.org/10.1038/s41598-023-42784-w) · **OA**

蹼足在水动力上是**桨（drag-based oar）而不是三角翼**，流场里没有前缘涡升力。C_D 从 10° 攻角的约 0.25 单调升到 75° 以上的约 1.5，法向力峰值在 55° 攻角附近，30°–140° 之间力都很稳定。

用途：**这是你准定常叶素模型（quasi-steady blade element）最直接的合法性依据**——用纯阻力式建模是对的；也说明攻角在很宽范围内力都差不多，所以桨的俯仰精度要求不高。

---

## 二、直接可比的机器人：你的 benchmark 和竞争工作

### 4. Qu, Cai, Fish, Li, Chen, Zhong 等 (2025)《Amphibious robotic dog: design, paddling gait planning, and experimental characterization》
*Bioinspiration & Biomimetics* 20(3): 036012 · [DOI 10.1088/1748-3190/adcd1b](https://doi.org/10.1088/1748-3190/adcd1b) · 需订阅（TUM 图书馆有）

**平台最接近、且 Frank Fish 是共同作者。**双关节腿四足，三种划水步态：两种狗式（**划水相占 25 % 与 33 %**，侧对角序列）和一种类小跑（**50 %**）。结论：侧序列步态推力/速度更好，类小跑更稳。水中最高 0.576 km/h（0.16 m/s），陆上 1.26 km/h。还专门设计了重心–浮心关系来保证浮态稳定。

用途：**你的 V1/V2/V3 占空比对比的直接对照组**；速度指标的 benchmark；浮态稳定性的论证方式。

### 5. Wang, Cai, Xie, Zhu, Li, Chen (2025)《A Computational Study on the Hydrodynamics of Bio-Inspired Quadrupedal Paddling》
*Biomimetics* 10(3): 148 · [DOI 10.3390/biomimetics10030148](https://doi.org/10.3390/biomimetics10030148) · **OA**

**参数扫描和你几乎一模一样**：初始摆角（60/70/80°）× 摆幅（20/30/40°）× 划水相占比（50 %/33 %/25 %）× 三种步态序列（小跑/对角/侧序列）。发现三种推力生成模式（Trotting / Hindering / Separate），其中 Hindering = 前一条腿刚离开划水相的阻力抵消后一条腿的推力。**对角与侧序列产生的水动力矩远大于小跑**；推力越大，力矩和能耗同步上升。

用途：（a）你整机 4 相 vs 2 相步态选择的直接依据；（b）方法学对照——它用**浸没边界法（immersed boundary）、无自由面**，而你用 overset + VOF **带自由面**，正好是你的差异化卖点；（c)"低中心角能不能白拿"这个问题它给了警告：推力上去，力矩也上去。

### 6. Han 等 (2025)《Learn to Swim: Data-Driven LSTM Hydrodynamic Model for Quadruped Robot Gait Optimization》
ICRA 2025 · [arXiv:2505.03146](https://arxiv.org/abs/2505.03146) · **OA**

西湖大学（与你已有的 Cui 2026 同组）。用约 300 万点水槽/拖曳水池测力数据训练 LSTM 代理模型（FED-LSTM），再用 **NSGA-II** 对髋最小角、膝最大角、频率、腿间相位做多目标步态优化。明确论证经验/准定常公式低估非定常力。

用途：**你"标定后的准定常模型 + 少量 CFD 验证"路线的对照方法**。你可以说：他们用 3 M 实测点换一个黑箱，你用 6 个 CFD 算例标定一个可解释模型，偏差 ±16 %。这是论文里很有力的一段。

### 7. Lin, Guo, Badri-Spröwitz (2024)《Bird-inspired tendon coupling improves paddling efficiency by shortening phase transition times》
[arXiv:2409.14707](https://arxiv.org/abs/2409.14707) · **OA**（已核对全文数据）

**和你的线驱动扇形脚蹼是同一个机构问题。**蹼由三块三角片经尼龙布 + Kevlar 绳连接、带硬限位，回收时**自折叠**，划水时由伸肌腱拉开。核心发现：效率提升**不是来自面积比，而是来自把折叠↔展开的过渡时间缩短 45–67 %**。带全套腱：净推力 1.72 ± 0.06 N、推进效率 2.86 ± 0.12 %；无伸肌腱：0.86 ± 0.09 N、1.45 ± 0.15 %；被动桨基线只有 0.84 ± 0.09 %。

用途：**你的 FAN_CLOSE / 8 % T 过渡时间可能比 FAN_DEG 更值得优化**——这是一个你还没做过的敏感性方向，而且不用改机构，只改线的预紧和松线相位。

---

## 三、脚蹼/桨的设计与建模（变面积、被动折叠）

### 8. Hu 等 (2024)《Design and Reality-Based Modeling Optimization of a Flexible Passive Joint Paddle for Swimming Robots》
*Biomimetics* 9(1): 56 · [DOI 10.3390/biomimetics9010056](https://doi.org/10.3390/biomimetics9010056) · **OA**

方法学上最贴近你的一篇：刚性 PA66 分片 + 硅胶铰链 + 机械限位，划水时限位顶住保持共面（最大投影面积），回收时自动屈曲卸阻力；**单舵机对称指令**，不对称完全来自铰链非线性。建模用**伪刚体模型 + 叶素理论**，再用高速相机实验标定水动力系数，力误差 0.51 %。

用途：你"准定常叶素 + CFD 标定"链条的可引用先例；如果以后要做柔性桨，这是模板。

### 9. Chen, Wang, Tu, Wang (2022)《Dynamic modeling and experiment of hind leg swimming of beaver-like underwater robot》
*Mechanical Sciences* 13: 831 · [DOI 10.5194/ms-13-831-2022](https://doi.org/10.5194/ms-13-831-2022) · **OA（全文免费 PDF）**

"刚–液融合"单腿模型：可弯曲蹼足上的积分水动力（叶素式）耦合大腿/小腿的 Newton–Euler 刚体动力学，输出推进力与升力；用 Fluent 仿真 + 单腿水下游动实验验证，比较仿生/加大幅度/减小幅度三条轨迹。

用途：**你单腿 CFD + 解析模型验证链条的现成模板**，而且全文免费，写方法章时可直接对标结构。同组的 Chen 等 (2021) *Ocean Engineering* 234: 109179（[DOI](https://doi.org/10.1016/j.oceaneng.2021.109179)，需订阅）给了可弯曲蹼足的诱导速度修正和"划水后停顿降阻"的做法。

### 10. Kim & Gharib (2011)《Characteristics of vortex formation and thrust performance in drag-based paddling propulsion》
*J. Exp. Biol.* 214(13): 2283–2291 · [DOI 10.1242/jeb.050716](https://doi.org/10.1242/jeb.050716) · 需订阅

阻力式划水的奠基性实验（旋转平板 + 3D PIV，Re ≈ 140–19 720）。三个对你有用的结论：涡强度的**时间变化率**而非幅值决定推力；**三角形（delta / 扇形）桨产生的展向流远强于矩形桨**——正好对应你 120° 扇形；**柔性桨在快速加速段削平推力峰值但不损失总冲量**。

用途：扇形几何的正当性；如果 V1/V3 的舵机峰值力矩（20 mN·m）成为瓶颈，柔性桨膜是一条"降峰不降冲量"的出路。

### 11. Herrera-Amaya & Byron (2024)《Propulsive efficiency of spatiotemporally asymmetric oscillating appendages at intermediate Reynolds numbers》
*Bioinspiration & Biomimetics* 19: 066004 · [DOI 10.1088/1748-3190/ad7abf](https://doi.org/10.1088/1748-3190/ad7abf) · 需订阅

**和你的核心变量最贴近的一篇**：用机器人桨分离"空间不对称（面积变化）"与"时间不对称（划水快/回收慢）"各自的贡献，并提出一个脱离整机动力学的"integrated efficiency"指标（正好适合你的单腿孤立算例）。还发现**弯曲柔性桨比直桨效率高，且不用复杂控制就能产生空间不对称**。
同组的 Herrera-Amaya 等 (2021) *ICB* 61(5): 1579（[DOI 10.1093/icb/icab179](https://doi.org/10.1093/icb/icab179)）给出理论骨架：**Re 越高，空间不对称越不重要、时间不对称越重要**——先算你桨的 Re（你的桨头 Re ≈ 1.1×10⁴），再决定该优化 CLOSED_W 还是占空比。

### 12. Blake (1981)《Influence of pectoral fin shape on thrust and drag in labriform locomotion》
*Journal of Zoology* 194(1): 53–66 · [DOI 10.1111/j.1469-7998.1981.tb04578.x](https://doi.org/10.1111/j.1469-7998.1981.tb04578.x) · 需订阅

阻力式划水的鱼倾向于**三角形（扇形）而非方形**胸鳍，尽管方形鳍的压差阻力实测低约 14 %。配合 Blake (1980) *JEB* 85: 337（[免费 PDF](https://journals.biologists.com/jeb/article-pdf/85/1/337/3193575/jexbio_85_1_337.pdf)）——最早明确指出划水式推进必须把**回收相算进效率**，不能只看划水相。

用途：扇形几何 + "整周期效率"这两个立论的经典出处。

---

## 四、CFD 方法学与船体（写方法章 / V&V 用）

### 13. Chen 等 (2019)《Application of an overset mesh based numerical wave tank for modelling realistic free-surface hydrodynamic problems》
*Ocean Engineering* 176: 97–117 · [DOI 10.1016/j.oceaneng.2019.02.001](https://doi.org/10.1016/j.oceaneng.2019.02.001) · 需订阅

OpenFOAM overset + VOF 的验证集合：波中浮体、**入水（water entry）**、WEC 升沉衰减。明确论证大幅运动下 overset 优于网格变形（mesh morphing）——正是你桨穿越水线时需要的论据。

### 14. Windt, Davidson, Chandar, Faedo, Ringwood (2020)《Evaluation of the overset grid method ... in OpenFOAM numerical wave tanks》
*J. Ocean Eng. Mar. Energy* 6(1): 55–70 · [DOI 10.1007/s40722-019-00156-5](https://doi.org/10.1007/s40722-019-00156-5)

五个难度递增的算例对比 overset 与 morphing：运动幅度大到一定程度**morphing 直接崩，overset 活下来**，代价是约 2× 运行时间。你被问"为什么用 overset、为什么这么慢"时的标准答案。

另可参考 Kozelkov 等 (2026) *Fluids* 11(6): 138（[DOI 10.3390/fluids11060138](https://doi.org/10.3390/fluids11060138)，**OA**）：两种方法在阻力系数上差约 0.5 %，3D 情形 overset 反而便宜约 10 %。

### 15. ITTC 推荐规程
- **7.5-03-02-04 Practical Guidelines for Ship CFD**（2024 修订）· [免费 PDF](https://www.ittc.info/media/11960/75-03-02-04.pdf)：网格、y⁺、自由面加密、计算域尺寸、时间离散阶数的可引用出处。
- **7.5-02-02-01 Resistance Test**（2011）· [免费 PDF](https://ittc.info/media/1217/75-02-02-01.pdf)：明确规程**预设了湍流激励**、模型"尽可能大"、修正就是为了**避免层流**。

用途：**这正是你需要的"ITTC-57 摩擦线在 Re ≈ 3×10⁴ 不适用"的正式依据**——不是你算错了，是那条线本来就不为这个雷诺数设计。配合 Terziev, Tezdogan, Incecik (2022)《Scale effects and full-scale ship hydrodynamics: a review》*Ocean Engineering* 245: 110496（[作者版 PDF](https://momchil-terziev.github.io/files/Draft_1.pdf)，**OA**）讲外推的不确定性。船体章里直接报 CFD 力、把 ITTC 对比降为"仅供参照"，是站得住的做法。

### 16. Eça & Hoekstra (2014)《A procedure for the estimation of the numerical uncertainty of CFD calculations based on grid refinement studies》
*J. Comput. Phys.* 262: 104–130 · [DOI 10.1016/j.jcp.2014.01.006](https://doi.org/10.1016/j.jcp.2014.01.006) · 需订阅

最小二乘 / 观测阶方法，专为**网格加密不均匀、观测阶不听话**的情况设计——snappyHexMesh + overset 就是这种情况，比裸用 GCI 合适。结构上配 Stern, Wilson, Coleman, Paterson (2001) *ASME JFE* 123(4): 793（[作者 PDF](http://servidor.demec.ufpr.br/CFD/bibliografia/erros_numericos/Stern_et_al_2001.pdf)）。

### 17. Picardi, Astolfi, Chatzievangelou, Aguzzi, Calisti (2023)《Underwater legged robotics: review and perspectives》
*Bioinspiration & Biomimetics* 18 · [DOI 10.1088/1748-3190/acc0bb](https://doi.org/10.1088/1748-3190/acc0bb) · OA (CC BY-NC-ND)

水下足式机器人的综述，把开放问题按环境交互/感知驱动/建模控制/自主性归类，并与螺旋桨式 ROV/AUV 对比。引言里"为什么用腿划水而不是螺旋桨"的标准出处。

---

## 五、值得知道但优先级较低

- **Baines 等 (2022)《Multi-environment robotic transitions through adaptive morphogenesis》** *Nature* 610: 283（[DOI](https://doi.org/10.1038/s41586-022-05188-w)）+ Baines 等 (2020) *Bioinsp. Biomim.* 15（[DOI](https://doi.org/10.1088/1748-3190/ab68e8)）：变形肢（海龟鳍↔陆龟腿），"一条腿两种水动力状态"的奠基工作。
- **Wang, Pancheri, Lueth, Sun (2025)《DuckyDog: An Erect Amphibious Robot with Variable-Stiffness Legs and Passive Fins》** *Advanced Intelligent Systems* 7（[DOI 10.1002/aisy.202500267](https://doi.org/10.1002/aisy.202500267)，**OA**）：**TUM MiMed（Lueth / Sun）自家工作**，腱驱动 + 被动鳍，水中 0.30 BL/s。校内引用，答辩时容易被问到。
- **Ding 等 (2025)《Diving-Beetle-Inspired Paddling Propulsion Robot》** *Biomimetics* 10(3): 182（[DOI](https://doi.org/10.3390/biomimetics10030182)，**OA**）：不完全齿轮 + 扭簧做出"快划慢回"，被动足在回收时折叠。纯机械实现不对称的思路。
- **Qi 等 (2021)《Observation and analysis of diving beetle movements while swimming》** *Sci. Rep.* 11: 16581（[DOI](https://doi.org/10.1038/s41598-021-96158-1)，**OA**）：龙虱划水相只占 30–47 %，回收时跗节旋转 + 刚毛折叠几乎消除阻力；后腿同步比交替更高效。
- **Walker & Westneat (2000)** *Proc. R. Soc. B* 267: 1875（[PMC1690750](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1690750/)，**OA**）与 **Fish (1996)** *Am. Zool.* 36(6): 628（[DOI](https://doi.org/10.1093/icb/36.6.628)）：划水（rowing）效率上限约 33 %，摆动翼（flapping）可超 80 %。诚实交代你这一类推进方式的天花板，然后说明增益只能从占空比、回收阻力、力方向对齐里挖——正是你做的三件事。
- **Ghazali, Abdul Satar, Rahiman (2024)《Unmanned surface vehicles: From a hull design perspective》** *Ocean Engineering* 312: 118977（[DOI](https://doi.org/10.1016/j.oceaneng.2024.118977)）：USV 船型综述，你船体比选课题的上位框架。

---

## 六、检索中发现的两个空白（可能是你的贡献点）

1. **反复穿越水线的附体（每周期入水 + 出水）的 overset 力验证**：Chen 2019 只覆盖一次性入水；没有找到对"附在运动船体上、周期性进出水的附体"做力验证的工作。你的单腿 + 整机算例正好填这个缝。
2. **ITTC 摩擦线在 Re ≈ 3×10⁴ 是否成立**：没有论文直接测过。文献只说明该线预设湍流激励、外推不确定性大。你的"层流 vs k-ω SST 对比"在这个雷诺数上是有正当动机的。

另外，第 4、5 两篇（Qu 2025、Wang 2025）都在做占空比扫描，但**都没有加垂向力约束**，而 Cui 2026 加了却没做形状/中心角。你的 "F̄_z/F̄_x = 0.28、两对腿叠加升沉激励最低" 是这三者之间的空隙。

---

*检索日期 2026-09-10。带 **OA** 的可直接下载；其余 TUM 图书馆（eaccess.ub.tum.de）有订阅。BibTeX 见同目录 `BODY2_refs.bib`。*
