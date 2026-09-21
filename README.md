# BODY2-fluke-leg — Paddling leg for the amphibious quadruped BODY2: fluke-foot design, hydrodynamics and servo trajectory

TUM MRBE Semesterarbeit (Lu Xiaotian, winter 2026). The repository contains only the **currently valid** code, data and notes. CFD cases, animation frames and Office reports are not tracked.

## Layout

| Folder | Content | Entry point |
|---|---|---|
| `cad/` | One-piece straight fluke foot **A2** (single PETG print: mounting tab → strut → filament-pin hinge + leaf springs → lunate fluke); STL/STEP output, size check, hull cross-section | `fluke_straight_cad.py` generates the part; `直排一体件A2_说明.md` print/assembly notes |
| `firmware/` | Sculling swim trajectory for the motion-control team: `scull_gait_patch.c` (replaces `swim_leg_pose()`), 100-points-per-cycle CSV, servo-angle check | `README_scull.md` |
| `hydro/` | Fluke hydrodynamics: UVLM flapping-foil solver, passive-pitch FSI (phasor method), sculling FSI, E-pivot spade paddle, area/aspect-ratio sweeps | `uvlm_foil.py` (solver) → `passive_pitch.py` / `sculling_fsi.py` |
| `cfd/` | Case generation and post-processing for OpenFOAM overset single-leg / full-robot unsteady CFD (`overPimpleDyMFoam` + `tabulated6DoFMotion`) | `README_cfd.md`, `make_leg_cfd.py`, `paddle_forces.py`, `run_cloud.sh` |
| `gait/` | Optimal-stroke theory for drag-based paddling, fold-timing sweep, structure-independent target trajectory, CFD-matrix post-processing | `optimal_trajectory.py`, `fold_timing_sweep.py`, `gait_to_firmware.py` |
| `docs/` | Research notes 00–14 (chronological, with design decisions), reference list `.bib`, key figures | `docs/notes/00_阅读顺序.md` |

## Current design status (2026-09-20)
- **Mechanism**: leg hangs down, long link stays vertical, the stem swings about the hip axis through **−18° ± 18°** (horizontal at the top of the stroke); the fluke pitches passively on a pin hinge at the stem tip (leaf-spring restoring stiffness k ≈ 2.5 mN·m/rad).
- **Fluke**: lunate planform, AR 3.1, span 60 mm, 11.5 cm², NACA 0021; whole part 98 × 11 × 60 mm, 6.9 g PETG. The 86 mm-span A1 hit the hull bottom at the top of the stroke and was dropped (`docs/figures/fig_size_check.png`).
- **Thrust estimate** (UVLM upper bound × 0.7): ≈ 20 mN per paddle at 1.5 Hz, ≈ 35 mN at 2 Hz. To be measured in the tank.
- **Ballast**: waterline at the hull top; water depth ≥ 15 cm.

## Environment
```bash
pip install -r requirements.txt
# CFD needs OpenFOAM v2606 (WSL2/Ubuntu), see cfd/README_cfd.md
# gait/ post-processing reads local CFD results: export BODY2_CFD_RESULTS=/path/to/leg_dynamics
```

## Reproducing the main results
```bash
python cad/fluke_straight_cad.py          # → cad/fluke_straight_A2.stl/.step + stiffness/strain JSON
python firmware/scull_trajectory.py       # → trajectory CSV + C patch + servo-angle ranges
python hydro/sculling_fsi.py              # sculling FSI sweep (f, θs0, k); takes tens of minutes
python cad/fig_size_check.py              # hull cross-section vs fluke envelope (needs hull_only.step, extracted from the assembly STEP, not tracked)
```

## Not tracked
CFD cases and results (`results_leg/`, `results_verify/`, several GB), animation frames, `.docx/.pdf` reports, SolidWorks sources and the full-robot assembly STEP.
