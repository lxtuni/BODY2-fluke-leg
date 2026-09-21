#!/usr/bin/env python3
"""
把 leg_dynamics.py 的步态（摇臂角 ψ(τ) + 平行四边形张角 φ(τ)）换算成固件 swim_leg_pose() 用的足端 M 轨迹。
固件坐标：原点 O2（摇臂轴 / 电机 2 轴），+x 朝机身前方，+y 朝上，单位 mm；连杆按 geom_v3 图：
    O1 = (−21.8, 22)  曲柄 O1A = 30  连杆 AC = 35  摇臂 O2C = 30（连杆端）/ O2B = 25（平行四边形端，C–O2–B 一条直线）
    平行四边形 O2–B–D–E：O2E = 60（电机 2 驱动，角 γ）、ED = 25 ∥ O2B、BD = 60 ∥ O2E；足端 M = E + 35·(D→E 方向) = E + 35·rot(q2 + 180°)
关节量：q2 = O2→B 的方向角（= 桨方向 − 180°，本模型的 ψ），γ = O2→E 的方向角，φ' = γ − q2（伸展 ≈ −105°，蜷缩 ≈ −40°，
        与 leg_dynamics.py 的 φ 大小相同、符号相反：图上平行四边形在摇臂的另一侧）
    T=0.81 DUTY=0.45 SWEEP=50 PSI_START=120 SWITCH_FRAC=0.5 python3 gait_to_firmware.py --name V3 [--phi-ext -105 --phi-ret -40] [--ncp 20]
输出 results_verify/firmware/<name>_M_trajectory.csv（τ, t, stage, q2, γ, q1, xM, yM, |O2M|, 传动角）、<name>_swim_cp.h（控制点数组草案）、fig_<name>_firmware.png
"""
import os, sys, json, argparse, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("--name", default="V3"); ap.add_argument("--out", default=os.path.join(HERE, "results_verify", "firmware"))
ap.add_argument("--phi-ext", type=float, default=-105.0, help="伸展时 φ' = γ − q2 [°]"); ap.add_argument("--phi-ret", type=float, default=-40.0, help="蜷缩时 φ' [°]")
ap.add_argument("--ncp", type=int, default=20, help="控制点数（相位等分，最后一点 = 第一点闭合）")
ap.add_argument("--O1", type=float, nargs=2, default=[-21.8, 22.0]); ap.add_argument("--r1", type=float, default=30.0); ap.add_argument("--rod", type=float, default=35.0)
ap.add_argument("--rockC", type=float, default=30.0); ap.add_argument("--rockB", type=float, default=25.0); ap.add_argument("--LE", type=float, default=60.0); ap.add_argument("--LM", type=float, default=35.0)
ap.add_argument("--wl", type=float, default=-14.0, help="水线在此坐标系里的高度 [mm]（O2 在水线上 14 mm，按 BODY2 船体安装位置）")
ap.add_argument("--q2-mode", choices=["direct", "mirror"], default="direct", help="direct：q2 = ψ（图中 +x 确为机身前方）；mirror：q2 = 180° − ψ（若图的机构其实与 STEP 同向，即 +x 朝后）")
ap.add_argument("--seq", type=float, nargs=2, default=[0.15, 0.15], metavar=("FOLD", "EXT"), help="顺序式回收方案（LOCK_Q1 蜷缩 / 蜷着摆回 / 伸展）的蜷缩、伸展时长占周期比")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
sp = importlib.util.spec_from_file_location("ld", os.path.join(HERE, "leg_dynamics.py")); ld = importlib.util.module_from_spec(sp); sp.loader.exec_module(ld)
T, DUTY = ld.T_PER, ld.DUTY; SF = min(max(ld.SWITCH_FRAC, 0.05), 0.5)
N = 2000; tau = np.linspace(0, 1, N, endpoint=False); t = tau * T
psi, phi, power = ld.gait(t)                                    # ψ [rad]：摇臂角；φ：本模型张角（0..π）
q2 = np.degrees(psi) if a.q2_mode == "direct" else 180.0 - np.degrees(psi)   # 固件的 q2 = O2→B 方向角
blend = (np.degrees(phi) - ld.PHI_EXT) / (ld.PHI_RET - ld.PHI_EXT)   # 0 = 伸展, 1 = 蜷缩（与 leg_dynamics 的时序完全相同）
phi_p = a.phi_ext + (a.phi_ret - a.phi_ext) * blend             # 固件侧张角 φ'
gam = q2 + phi_p                                                # γ = O2→E 方向角（电机 2）
rot = lambda d: np.stack([np.cos(np.radians(d)), np.sin(np.radians(d))], -1)
E = a.LE * rot(gam); B = a.rockB * rot(q2); D = B + E; M = E + a.LM * rot(q2 + 180.0); C = a.rockC * rot(q2 + 180.0)
# 四杆逆解：|A−O1| = r1, |A−C| = rod → 两解，取与图中位姿（q2=26.6°, A=(−50,12)）同支的解
O1 = np.array(a.O1)
def crank_solutions(Cp):
    d = np.linalg.norm(Cp - O1); u = (Cp - O1) / d; h2 = a.r1 ** 2 - ((a.r1 ** 2 - a.rod ** 2 + d ** 2) / (2 * d)) ** 2
    if h2 < 0: return None
    p = O1 + u * (a.r1 ** 2 - a.rod ** 2 + d ** 2) / (2 * d); h = np.sqrt(h2); n = np.array([-u[1], u[0]])
    return [p + h * n, p - h * n]
Cd = a.rockC * rot(np.array([26.6]))[0] * -1 + 0  # 图中 C = 30·rot(206.6°)
Cd = a.rockC * np.array([np.cos(np.radians(206.6)), np.sin(np.radians(206.6))])
sols = crank_solutions(Cd); Adiag = np.array([-50.0, 12.0]); branch = int(np.argmin([np.linalg.norm(s - Adiag) for s in sols]))
q1 = np.full(N, np.nan); mu = np.full(N, np.nan); dOC = np.linalg.norm(C - O1, axis=1)
for i in range(N):
    s = crank_solutions(C[i])
    if s is None: continue
    A = s[branch]; q1[i] = np.degrees(np.arctan2(*(A - O1)[::-1]))
    v1, v2 = A - C[i], -C[i]                                    # 传动角：连杆 AC 与摇臂 C→O2 的夹角
    mu[i] = np.degrees(np.arccos(np.clip(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1)))
q1 = np.degrees(np.unwrap(np.radians(q1)))
rM = np.linalg.norm(M, axis=1); angOEM = np.degrees(np.arccos(np.clip(np.einsum("ij,ij->i", -E, M - E) / (a.LE * a.LM), -1, 1)))
stage = np.where(tau < DUTY, 1, np.where(tau < DUTY + SF * (1 - DUTY), 2, 3))    # 1 划水(伸展) 2 回收-蜷缩段 3 回收-伸展段
# ---- 汇总 ----
print(f"[{a.name}/{a.q2_mode}] T={T} s DUTY={DUTY} SWITCH_FRAC={SF}  q2 {q2[0]:.0f}→{q2[int(DUTY*N)-1]:.0f}°  φ' {a.phi_ext}→{a.phi_ret}°  γ 范围 {gam.min():.1f}…{gam.max():.1f}°  q1 范围 {np.nanmin(q1):.1f}…{np.nanmax(q1):.1f}°")
print(f"     |O2M| 划水 {rM[power].min():.1f}…{rM[power].max():.1f} mm，回收最小 {rM[~power].min():.1f}；∠O2EM 最小 {angOEM.min():.0f}°；四杆 |O1C| 最大 {dOC.max():.1f}（极限 {a.r1 + a.rod}）传动角最小 {np.nanmin(mu):.0f}°")
print(f"     M 划水相：x {M[power,0].min():.1f}…{M[power,0].max():.1f}，y {M[power,1].min():.1f}…{M[power,1].max():.1f}（水线 y={a.wl}）；蜷缩到位时 M=({M[stage==2][-1,0]:.1f},{M[stage==2][-1,1]:.1f})")
# ---- CSV ----
hdr = "tau,t_s,stage,q2_deg,gamma_deg,q1_deg,xM_mm,yM_mm,r_O2M_mm,ang_O2EM_deg,fourbar_mu_deg"
np.savetxt(os.path.join(a.out, f"{a.name}_{a.q2_mode}_M_trajectory.csv"), np.c_[tau, t, stage, q2, gam, q1, M, rM, angOEM, mu][::10], fmt="%.4f", delimiter=",", header=hdr, comments="")
# ---- 控制点数组草案：相位等分 ncp 段（最后一点回到第一点），段内直线插值、不用 smooth（密控制点时 smooth 会一段一段地加减速） ----
kn = np.linspace(0, 1, a.ncp + 1); idx = np.minimum((kn * N).astype(int), N - 1)
cx, cy = M[idx, 0], M[idx, 1]; cx[-1], cy[-1] = cx[0], cy[0]
seg_stage = [int(stage[min(int(((kn[i] + kn[i + 1]) / 2) * N), N - 1)]) for i in range(a.ncp)]
st_name = {1: "LEG_STAGE_BOTH_MOVE_1", 2: "LEG_STAGE_BOTH_MOVE_2", 3: "LEG_STAGE_BOTH_MOVE_3"}
lines = [f"/* {a.name} 步态足端轨迹（{a.q2_mode}）—— gait_to_firmware.py 生成（T = {T} s, DUTY = {DUTY}, q2 {q2[0]:.0f}→{q2[int(DUTY * N) - 1]:.0f}°, φ' {a.phi_ext:.0f}/{a.phi_ret:.0f}°）",
         f"   坐标：O2 原点，+x 前，+y 上，mm。段内直线（shape = 直线, bulge = 0），建议 swim_smooth_enable = 0（相位已含余弦时间律）。",
         f"   stage：1 = 划水（伸展，in_power=1）；2 = 回收-蜷缩（q2 与 γ 同时动）；3 = 回收-伸展。若固件回收必须用 LOCK_Q1（q1 锁定），见 CSV 里的 q2/γ 表另排。 */",
         f"#define SWIM_CP_COUNT_{a.name} {a.ncp + 1}",
         "static const float swim_knots_%s[SWIM_CP_COUNT_%s] = {%s};" % (a.name, a.name, ", ".join(f"{k:.4f}f" for k in kn)),
         "static const float swim_cx_%s[SWIM_CP_COUNT_%s]    = {%s};" % (a.name, a.name, ", ".join(f"{v:.2f}f" for v in cx)),
         "static const float swim_cy_%s[SWIM_CP_COUNT_%s]    = {%s};" % (a.name, a.name, ", ".join(f"{v:.2f}f" for v in cy)),
         "static const uint8_t swim_seg_stage_%s[SWIM_CP_COUNT_%s - 1] = {%s};" % (a.name, a.name, ", ".join(st_name[s] for s in seg_stage)),
         "static const uint8_t swim_seg_shape_%s[SWIM_CP_COUNT_%s - 1] = {0};   /* 全部直线 */" % (a.name, a.name),
         "static const float   swim_seg_bulge_%s[SWIM_CP_COUNT_%s - 1] = {0};" % (a.name, a.name),
         f"/* 周期 T = {T} s：phase 每秒加 {1/T:.4f}；划水相 knots[0..{int(round(DUTY*a.ncp))}] = 0…{DUTY} */",
         "/* 关节空间对照（开环/校验用）：τ, q2[°], γ[°], q1[°] */",
         "static const float swim_joint_%s[%d][4] = {" % (a.name, a.ncp + 1)]
for i, k in enumerate(kn):
    j = idx[i] if i < a.ncp else 0
    lines.append(f"    {{{k:.4f}f, {q2[j]:8.2f}f, {gam[j]:8.2f}f, {q1[j]:8.2f}f}},")
lines.append("};")
# ---- 顺序式回收（用固件的 LOCK_Q1 段）：划水 → q1 锁住只转 γ 蜷缩 → 蜷着摆回 → 伸展；时长按 --seq（未经 CFD 验证，与 V3 的“边摆边蜷”等效近似） ----
fo, ex = a.seq; iD = int(DUTY * N) - 1; i0 = 0
q2e, q2s = q2[iD], q2[i0]; g_ext_e, g_ret_e = q2e + a.phi_ext, q2e + a.phi_ret; g_ret_s, g_ext_s = q2s + a.phi_ret, q2s + a.phi_ext
def Mof(q, g): return a.LE * rot(np.array([g]))[0] + a.LM * rot(np.array([q + 180.0]))[0]
Mk = [Mof(q2s, g_ext_s), Mof(q2e, g_ext_e), Mof(q2e, g_ret_e), Mof(q2s, g_ret_s), Mof(q2s, g_ext_s)]
kseq = [0.0, DUTY, DUTY + fo, 1.0 - ex, 1.0]
lock_c = a.LM * rot(np.array([q2e + 180.0]))[0]
lines += ["", f"/* 顺序式回收方案（若回收必须用 LOCK_Q1）：knots {kseq}",
          f"   段 0 划水 BOTH_MOVE_1：M 沿 O2 为圆心、R = {rM[0]:.1f} mm 的圆弧从 ({Mk[0][0]:.1f},{Mk[0][1]:.1f}) 到 ({Mk[1][0]:.1f},{Mk[1][1]:.1f})（q2 {q2s:.0f}→{q2e:.0f}°，建议 smooth 开）",
          f"   段 1 LOCK_Q1：q1 锁在 {q1[iD]:.2f}°（q2 = {q2e:.0f}°），γ 从 {g_ext_e:.1f}° 转到 {g_ret_e:.1f}°（dγ = {g_ret_e-g_ext_e:+.1f}°）；锁定圆 圆心 ({lock_c[0]:.1f},{lock_c[1]:.1f}) R = {a.LE:.0f}",
          f"   段 2 蜷着摆回 BOTH_MOVE_2：φ' = {a.phi_ret:.0f}° 不变，q2 {q2e:.0f}→{q2s:.0f}°，M 从 ({Mk[2][0]:.1f},{Mk[2][1]:.1f}) 到 ({Mk[3][0]:.1f},{Mk[3][1]:.1f})（圆弧，R = {np.linalg.norm(Mk[2]):.1f}）",
          f"   段 3 伸展 BOTH_MOVE_3：q2 = {q2s:.0f}° 不变，γ {g_ret_s:.1f}→{g_ext_s:.1f}°，M 回到 ({Mk[4][0]:.1f},{Mk[4][1]:.1f}) */",
          "static const float swim_knots_%s_seq[5] = {%s};" % (a.name, ", ".join(f"{k:.4f}f" for k in kseq)),
          "static const float swim_cx_%s_seq[5]    = {%s};" % (a.name, ", ".join(f"{m[0]:.2f}f" for m in Mk)),
          "static const float swim_cy_%s_seq[5]    = {%s};" % (a.name, ", ".join(f"{m[1]:.2f}f" for m in Mk)),
          "static const uint8_t swim_seg_stage_%s_seq[4] = {LEG_STAGE_BOTH_MOVE_1, LEG_STAGE_LOCK_Q1, LEG_STAGE_BOTH_MOVE_2, LEG_STAGE_BOTH_MOVE_3};" % a.name]
open(os.path.join(a.out, f"{a.name}_{a.q2_mode}_swim_cp.h"), "w").write("\n".join(lines) + "\n")
json.dump(dict(name=a.name, T=T, DUTY=DUTY, SWITCH_FRAC=SF, q2_start=float(q2.max()), q2_end=float(q2.min()), phi_ext=a.phi_ext, phi_ret=a.phi_ret, geom=dict(O1=a.O1, r1=a.r1, rod=a.rod, rockC=a.rockC, rockB=a.rockB, LE=a.LE, LM=a.LM),
               knots=kn.tolist(), cx=cx.tolist(), cy=cy.tolist(), seg_stage=seg_stage), open(os.path.join(a.out, f"{a.name}_{a.q2_mode}_swim_cp.json"), "w"), indent=1)

# ---- 图 ----
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
import glob
for f in [f for f in font_manager.findSystemFonts() if "NotoSansCJK" in f and "Regular" in f] + glob.glob("/mnt/c/Windows/Fonts/msyh.ttc"):
    try: font_manager.fontManager.addfont(f); plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name(); break
    except Exception: pass
plt.rcParams["axes.unicode_minus"] = False
INK, INK2, SURF, BLUE, ORANGE, GRAY, GRID, RED = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6", "#eb6834", "#a8a7a1", "#e6e5e1", "#e34948"
fig, axs = plt.subplots(1, 2, figsize=(15, 7), facecolor=SURF, gridspec_kw=dict(width_ratios=[1.15, 1]))
ax = axs[0]; ax.set_facecolor(SURF); ax.set_aspect("equal"); ax.grid(color=GRID, lw=0.8)
ax.axhline(a.wl, color=BLUE, lw=1.1); ax.text(-95, a.wl + 1.5, f"水线 y = {a.wl:.0f}（O2 在水线上 {-a.wl:.0f} mm，按 BODY2 安装）", color=BLUE, fontsize=8.5)
ax.plot(M[power, 0], M[power, 1], color=BLUE, lw=2.2, label="M 划水相（伸展）"); ax.plot(M[~power, 0], M[~power, 1], color=ORANGE, lw=2.2, ls="--", label="M 回收相（蜷缩→伸展）")
ax.scatter(cx, cy, s=22, color=INK, zorder=5, label=f"控制点 ×{a.ncp}（相位等分）")
def draw(i, col, al=1.0, lab=None):
    Bi, Ei, Di, Mi, Ci = B[i], E[i], D[i], M[i], C[i]; s = crank_solutions(Ci); Ai = s[branch] if s else None
    for P1, P2 in ((Ci, Bi), (np.zeros(2), Ei), (Ei, Di), (Bi, Di)): ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color=INK2, lw=1.3, alpha=al)
    if Ai is not None:
        for P1, P2 in ((O1, Ai), (Ai, Ci)): ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color=GRAY, lw=1.1, alpha=al)
    ax.plot([Ei[0], Mi[0]], [Ei[1], Mi[1]], color=col, lw=3.5, alpha=al, solid_capstyle="round")
    if lab: ax.text(Mi[0], Mi[1] - 5, lab, color=col, fontsize=8.5, ha="center", va="top", alpha=min(1, al + 0.3))
draw(0, BLUE, 1.0, "τ=0 (q2=%.0f°)" % q2[0]); draw(int(DUTY / 2 * N), BLUE, 0.45); draw(int(DUTY * N) - 1, BLUE, 1.0, "τ=DUTY (q2=%.0f°)" % q2[int(DUTY * N) - 1])
draw(int((DUTY + SF * (1 - DUTY)) * N) - 1, ORANGE, 1.0, "蜷缩到位 τ=%.2f" % (DUTY + SF * (1 - DUTY)))
ax.plot(0, 0, "o", color=INK, ms=5); ax.text(3, 3, "O2", fontsize=9); ax.plot(*O1, "o", color=GRAY, ms=4); ax.text(O1[0] + 3, O1[1] + 2, "O1", fontsize=9, color=INK2)
ax.set_xlim(-100, 110); ax.set_ylim(-110, 60); ax.set_xlabel("x [mm]（+x = 机身前方）" if a.q2_mode == "direct" else "x [mm]（镜像假设：图中 +x 其实朝机身后方）"); ax.set_ylabel("y [mm]（+y = 上）")
ax.set_title(f"{a.name}（{'q2 = ψ，+x 前' if a.q2_mode == 'direct' else '镜像：q2 = 180° − ψ'}）：固件坐标里的足端 M 轨迹与机构位姿（geom_v3 尺寸；EM 粗线 = 桨方向）", loc="left", fontsize=10.5); ax.legend(frameon=False, fontsize=8.5, loc="lower left")
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
ax = axs[1]; ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.8)
ax.axvspan(0, DUTY, color=BLUE, alpha=0.07, lw=0); ax.axvspan(DUTY, 1, color=ORANGE, alpha=0.07, lw=0); ax.axvline(DUTY, color=INK2, lw=0.9, ls="--")
ax.plot(tau, q2, color=INK, lw=2, label="q2 = 摇臂 O2→B 方向角（桨方向 − 180°）"); ax.plot(tau, gam, color=BLUE, lw=2, label="γ = O2→E 方向角（电机 2）")
ax.plot(tau, q1, color=ORANGE, lw=2, label="q1 = 曲柄 O1→A 方向角（电机 1，四杆逆解）"); ax.plot(tau, phi_p, color=GRAY, lw=1.4, ls=":", label="φ' = γ − q2（张角）")
ax.set_xlabel("周期相位 τ = t / T"); ax.set_ylabel("角度 [°]（从 +x 逆时针）"); ax.set_xlim(0, 1); ax.legend(frameon=False, fontsize=8.5, loc="upper right")
ax.set_title(f"关节量随相位：T = {T} s，划水 0…{DUTY}（q2 {q2[0]:.0f}→{q2[int(DUTY * N) - 1]:.0f}° 余弦律），回收蜷缩 {DUTY}…{DUTY + SF*(1-DUTY):.3f}、再伸展", loc="left", fontsize=10.5)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
plt.tight_layout(); fn = os.path.join(a.out, f"fig_{a.name}_{a.q2_mode}_firmware.png"); plt.savefig(fn, dpi=115, facecolor=SURF); print("→", fn)
