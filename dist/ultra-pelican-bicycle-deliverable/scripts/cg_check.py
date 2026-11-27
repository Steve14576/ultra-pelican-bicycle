"""装配体质心 / 助学轮稳定先验校核（无打样）。
导入各零件 STL，按装配位姿放置，按材料密度质量加权求质心；
电池/电机/舵机以点质量计入。校核质心投影落在助学轮+主轮接地支撑多边形内。
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad"))
from build123d import import_step, Axis
from params import DENSITY

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad", "out")

def load(name, mat, rot=None, loc=(0, 0, 0)):
    s = import_step(os.path.join(OUT, name + ".step"))
    if rot: s = s.rotate(Axis((0, 0, 0), rot[0]), rot[1])
    s = s.translate(loc)
    m = s.volume / 1000.0 * DENSITY[mat]
    c = s.center()
    return m, (c.X, c.Y, c.Z)

parts = []
parts.append(load("frame_petg", "PETG"))
for x in (0, 240):  # 前后主轮
    parts.append(load("wheel_rim_petg", "PETG", ((1, 0, 0), 90), (x, 0, 50)))
    parts.append(load("wheel_tire_tpu", "TPU", ((1, 0, 0), 90), (x, 0, 50)))
for y in (55, -55):  # 助学轮
    parts.append(load("train_rim_petg", "PETG", None, (0, y, 38)))
    parts.append(load("train_tire_tpu", "TPU", None, (0, y, 38)))
parts.append(load("crank_peba", "PEBA", None, (95, 0, 60)))
parts.append(load("crank_pulley_petg", "PETG", None, (95, 0, 60)))
parts.append(load("pelican_skeleton_petcf", "PET-CF"))
parts.append(load("electronics_tray_petg", "PETG"))

# 点质量：电池/电机/舵机/腿/鹈鹕软皮+棉花/嘴/翅
points = [(100, (120, 0, 80)), (30, (-22, 0, 58)), (10, (215, 0, 120)),
          (5, (85, 30, 120)), (5, (85, -30, 120)),
          (90, (75, 0, 185)), (10, (195, 0, 285)),
          (8, (75, 45, 195)), (8, (75, -45, 195))]
M = sum(m for m, _ in parts) + sum(m for m, _ in points)
cx = sum(m * c[0] for m, c in parts) + sum(m * p[0] for m, p in points)
cy = sum(m * c[1] for m, c in parts) + sum(m * p[1] for m, p in points)
cz = sum(m * c[2] for m, c in parts) + sum(m * p[2] for m, p in points)
CG = (cx / M, cy / M, cz / M)
print(f"总质量 {M:.0f} g")
print(f"质心 CG = ({CG[0]:.0f}, {CG[1]:.0f}, {CG[2]:.0f}) mm")

# 支撑多边形：前轮接地点(240,0) + 助学轮(0,±55)（后轮(0,0)在边内）
def inside(px, py):
    # 三角形 (240,0),(0,55),(0,-55)
    A, B, C = (240, 0), (0, 55), (0, -55)
    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
    d1, d2, d3 = sign((px,py),A,B), sign((px,py),B,C), sign((px,py),C,A)
    neg = (d1<0) or (d2<0) or (d3<0); pos = (d1>0) or (d2>0) or (d3>0)
    return not (neg and pos)
ok = inside(CG[0], CG[1])
print(f"质心投影在支撑多边形内: {'是' if ok else '否'}")
print(f"质心高度 {CG[2]:.0f} mm（越低越稳）; 纵向位置 {CG[0]:.0f} mm（0=后轴,240=前轴）")
print("稳定校核", "OK" if ok and CG[2] < 150 else "需调整配重")