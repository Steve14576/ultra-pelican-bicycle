"""腿链平面约束探针（评审#1 整改验证）。
直连杆两端销孔平行 Y => 髋/膝/踝必须共面（同一 y）。
本探针：1) 断言髋孔 y == 踝销 y（共面）；2) 在该平面内做全曲柄周期 2-link IK 扫掠，
核可达/膝角/无锁死。此前 m2_sanity 只核距离未核共面，total_assembly 用四元数抹掉平面约束。
"""
import math, re, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sk = open(os.path.join(ROOT, "cad/pelican_skeleton.py"), encoding="utf-8").read()
dr = open(os.path.join(ROOT, "cad/drivetrain.py"), encoding="utf-8").read()
hip_y = set(abs(float(m)) for m in re.findall(r"ybore\(\(75, (-?[\d.]+), 150\), pin_r", sk))
ank_y = set(abs(float(m)) for m in re.findall(r"ybore\(\((?:-?CRANK_R|CRANK_R), (-?[\d.]+), 0\), pin_r", dr))
print("髋孔 |y|:", sorted(hip_y), " 踝销 |y|:", sorted(ank_y))
coplanar = hip_y == ank_y
print("共面约束:", "OK" if coplanar else "FAIL(锁死)")

H = (75.0, 150.0); BB = (95.0, 60.0); R = 20.0; L1 = L2 = 60.0
dmin, dmax = 1e9, -1e9; kmin, kmax = 1e9, -1e9; ok = True
for i in range(24):
    th = i / 24 * 2 * math.pi
    F = (BB[0] + R * math.cos(th), BB[1] + R * math.sin(th))
    d = math.dist(H, F)
    dmin, dmax = min(dmin, d), max(dmax, d)
    if d >= L1 + L2 or d <= abs(L1 - L2):
        ok = False
    c = (L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2)
    k = math.degrees(math.acos(max(-1, min(1, c))))
    kmin, kmax = min(kmin, k), max(kmax, k)
print(f"髋-脚距离扫掠: {dmin:.1f}..{dmax:.1f} mm (腿可达 0..{L1+L2:.0f})")
print(f"膝角扫掠: {kmin:.0f}..{kmax:.0f} deg (180=锁死)")
print("平面运动学:", "PASS" if (ok and coplanar) else "FAIL")