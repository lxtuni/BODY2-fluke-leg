/* ===== 摇橹式（尾鳍脚）游泳轨迹：替换 gait_task.c 里的 swim_leg_pose() =====
 * 长杆 H–I 保持竖直，杆 A–H（= 脚 I–J 方向，q2）绕髋轴 A 正弦摆动 scull_theta_mean_deg ± scull_theta0_deg（−18° ± 18°：顶端杆水平，底端 −36°），
 * 这样冲程顶端尾鳍仍在船底以下（船底 y = −35，尾鳍顶端 ≈ −48）。
 * 足端 J 走以 (0, −HI) 为圆心、半径 AH+IJ 的圆弧，中点切线竖直 → 尾鳍铰轴上下沉浮 ±31 mm。
 * 频率仍由 swim_freq_hz / CH5 控制（建议 1.5 Hz，最高 2 Hz），相位偏移沿用 swim_phase_off_*（对角同相）。
 * 船的前进方向 = 尾鳍拖行的反方向（脚朝前时船向后游）。 */
volatile float scull_theta0_deg = 18.0f;     /* 杆摆幅；18° → 沉浮 ±31 mm，22° → ±38 mm（2 Hz 时舵机 q1 峰值 ~317 °/s，注意上限） */
volatile float scull_theta_mean_deg = -18.0f;  /* 杆平均角（负 = 向下）；改成 0 就回到对称摆动，但尾鳍会顶到船底 */
volatile float scull_center_z   = -52.0f;         /* 圆心高度 = −HI（长杆竖直） */
volatile float scull_radius     = 101.0f;           /* AH + IJ */

static void scull_leg_pose(float phase, float *yJ, float *zJ, int *in_power)
{
    float p  = phase - floorf(phase);
    float th = deg_to_rad(scull_theta_mean_deg) + deg_to_rad(scull_theta0_deg) * sinf(2.0f * LEG_PI * p);
    *yJ = scull_radius * cosf(th);
    *zJ = scull_center_z + scull_radius * sinf(th);
    if (in_power) *in_power = (th > deg_to_rad(scull_theta_mean_deg));           /* 仅用于调试灯，升力型没有“划水相” */
}
/* 在 MODE 5 的 walk_trot_select == 2 分支里，把四个 swim_leg_pose(...) 改成 scull_leg_pose(...) 即可。
 * IK、舵机映射、相位推进都不用改。 */
