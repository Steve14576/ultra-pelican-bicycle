"""M2 机构方案秒级校验探针。
验证两件事：
1) 单电机驱动后轮的速度与扭矩余量是否够（N20 + 皮带减速）。
2) 鹈鹕腿（大腿+小腿两连杆）能否全程跟随脚踏曲柄圆，不发生死点/超程。
几何与质量为初值，M3 建模时精修；本探针只判可行性量级。
"""
import math

g = 9.81

# ---- 整车初值 ----
mass_kg = 1.2          # 打印件+电子+电池 保守估计
wheel_r = 0.05         # 后轮半径 m（轮径 10cm）
crr = 0.03             # TPU 小轮在平滑地面滚阻系数（量级估计）
motor_rpm_loaded = 120 # N20 6V 150rpm 档带载估计
belt_ratio = 2.0       # 电机->后轴 减速比（后轴转速 = 电机/2）

# ---- 驱动校验 ----
wheel_rpm = motor_rpm_loaded / belt_ratio
v = wheel_rpm / 60 * 2 * math.pi * wheel_r
F_roll = crr * mass_kg * g
T_wheel = F_roll * wheel_r                 # N·m 维持匀速所需
T_wheel_margin = T_wheel * 3               # 3x 余量（加速/小坡/损耗）
T_motor_need = T_wheel_margin / belt_ratio # 折算到电机轴
kgcm = lambda nm: nm / 0.0980665
n20_stall_kgcm = 1.8   # N20 6V 150rpm 档典型堵转扭矩量级（ datasheet 待核）
n20_cont_kgcm = 0.5    # 典型连续额定量级

print("=== 驱动校验 ===")
print(f"后轮转速      : {wheel_rpm:.0f} rpm")
print(f"车速          : {v:.2f} m/s  ({v*100:.0f} cm/s)")
print(f"匀速轮端扭矩  : {kgcm(T_wheel):.2f} kg·cm")
print(f"3x余量轮端    : {kgcm(T_wheel_margin):.2f} kg·cm")
print(f"折算电机需求  : {kgcm(T_motor_need):.2f} kg·cm")
print(f"N20连续额定   : ~{n20_cont_kgcm:.1f} kg·cm  -> {'够' if n20_cont_kgcm>=kgcm(T_motor_need) else '偏紧,建议更高减速比'}")
print(f"N20堵转       : ~{n20_stall_kgcm:.1f} kg·cm")

# ---- 踩踏传动 ----
crank_ratio = 1.8      # 后轴->曲柄 减速比（曲柄更慢,踩踏可读）
crank_rpm = wheel_rpm / crank_ratio
print("\n=== 踩踏传动 ===")
print(f"曲柄转速      : {crank_rpm:.0f} rpm  (踩踏节奏)")

# ---- 腿部连杆工作空间 ----
# 髋关节固定在身体; 脚踩在曲柄圆上。两连杆腿自然解算膝关节。
hip = (0.0, 0.09)         # 髋关节坐标 m（相对曲柄中心）
crank_center = (0.0, 0.0)
crank_r = 0.02            # 曲柄半径 m（脚踏圆半径 4cm 直径）
L_thigh = 0.06
L_shin = 0.06
d_hip_crank = math.dist(hip, crank_center)
reach_max = L_thigh + L_shin
reach_min = abs(L_thigh - L_shin)
foot_far = d_hip_crank + crank_r
foot_near = d_hip_crank - crank_r

print("\n=== 腿部连杆工作空间 ===")
print(f"髋->曲柄中心  : {d_hip_crank*100:.1f} cm")
print(f"脚->髋 范围   : [{foot_near*100:.1f}, {foot_far*100:.1f}] cm")
print(f"腿可达范围    : [{reach_min*100:.1f}, {reach_max*100:.1f}] cm")
ok = foot_far <= reach_max and foot_near >= reach_min
print(f"全程可达      : {'是' if ok else '否,需改杆长/髋位'}")
print(f"最大伸展余量  : {(reach_max-foot_far)*100:.1f} cm (避免膝死点)")

# 膝关节角度范围（余弦定理）
def knee_angle(foot_dist):
    c = (L_thigh**2 + L_shin**2 - foot_dist**2) / (2*L_thigh*L_shin)
    c = max(-1, min(1, c))
    return math.degrees(math.acos(c))
print(f"膝角范围      : {knee_angle(foot_far):.0f}° .. {knee_angle(foot_near):.0f}° (180°=完全伸直)")