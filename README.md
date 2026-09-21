# BODY2-fluke-leg — 两栖四足机器人 BODY2 的划水腿：尾鳍脚设计、水动力分析与电控轨迹

TUM MRBE Semesterarbeit（Lu Xiaotian，2026 WS）。仓库只放**当前有效**的代码、数据和笔记；CFD 算例、动画帧、Office 报告不进仓库。

## 目录

| 目录 | 内容 | 入口 |
|---|---|---|
| `cad/` | 直排一体件尾鳍脚 **A2**（PETG 单件：安装片 → 支杆 → 耗材销铰 + 叶簧 → 月牙尾鳍），STL/STEP 成品、尺寸核算、船体截面 | `fluke_straight_cad.py` 生成零件；`直排一体件A2_说明.md` 打印/装配说明 |
| `firmware/` | 给电控的摇橹式游泳轨迹：`scull_gait_patch.c`（替换 `swim_leg_pose()`）、100 点/周期 CSV、舵机角核对 | `README_scull.md` |
| `hydro/` | 尾鳍水动力：UVLM 拍动翼求解器、被动俯仰 FSI（相量法）、摇橹式 FSI、E 点铰铲桨、面积/展弦比扫描 | `uvlm_foil.py`（求解器）→ `passive_pitch.py` / `sculling_fsi.py` |
| `cfd/` | OpenFOAM overset 单腿/整机非定常 CFD 的生成与后处理（`overPimpleDyMFoam` + `tabulated6DoFMotion`） | `README_cfd.md`、`make_leg_cfd.py`、`paddle_forces.py`、`run_cloud.sh` |
| `gait/` | 阻力型划水的最优行程理论、开合时机扫描、结构无关目标轨迹、CFD 矩阵后处理 | `optimal_trajectory.py`、`fold_timing_sweep.py`、`gait_to_firmware.py` |
| `docs/` | 研究笔记 00–14（按时间顺序，含设计决策）、文献清单 `.bib`、关键图 | `docs/notes/00_阅读顺序.md` |

## 当前设计状态（2026-09-20）
- **机构**：腿悬垂、长杆竖直、杆绕髋轴摆 **−18° ± 18°**（顶端水平），尾鳍在杆端销铰上被动俯仰（叶簧回位 k ≈ 2.5 mN·m/rad）。
- **尾鳍**：月牙 AR 3.1，展 60 mm，11.5 cm²，NACA 0021；整件 98 × 11 × 60 mm，PETG 6.9 g。展 86 的 A1 会在冲程顶端顶到船底，已弃用（`docs/figures/fig_size_check.png`）。
- **推力估计**（UVLM 上限 ×0.7）：1.5 Hz ≈ 20 mN/桨，2 Hz ≈ 35 mN/桨。待水槽实测。
- **压载**：水线到船顶；水深 ≥ 15 cm。

## 环境
```bash
pip install -r requirements.txt
# CFD 需要 OpenFOAM v2606（WSL2/Ubuntu），见 cfd/README_cfd.md
# gait/ 的后处理脚本读本地 CFD 结果：export BODY2_CFD_RESULTS=/path/to/leg_dynamics
```

## 复现主要结果
```bash
python cad/fluke_straight_cad.py          # → cad/fluke_straight_A2.stl/.step + 刚度/应变 JSON
python firmware/scull_trajectory.py       # → 轨迹 CSV + C 补丁 + 舵机角范围
python hydro/sculling_fsi.py              # 摇橹式 FSI 扫描（f, θs0, k），几十分钟
python cad/fig_size_check.py              # 船体截面 vs 尾鳍包络（需要 hull_only.step，从总装 STEP 提取，不入库）
```

## 不入库的东西
CFD 算例与结果（`results_leg/`、`results_verify/`，数 GB）、动画帧、`.docx/.pdf` 报告、SolidWorks 源文件与整机总装 STEP。
