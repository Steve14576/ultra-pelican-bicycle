"""车架参数化建模（钻石梁 + 头管 + 五通 + 后叉 + 助学轮臂）。
坐标：X 向前，Y  lateral，Z  up；地面 z=0，轮径 100 → 轴心 z=50。
后轴/五通轴承座孔沿 Y；头管孔沿转向轴。承载接头后续按拆件方案加螺丝+热熔螺母。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Cylinder, Box, Axis, Align, Pos, export_stl, export_step
from params import WHEELBASE, WHEEL_R, FIT, BEARING_608, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

def beam(p1, p2, r):
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    vn = [c / L for c in v]
    b = Cylinder(r, L, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cross = (-vn[1], vn[0], 0.0)          # Z × vn
    cl = math.sqrt(sum(c * c for c in cross))
    ang = math.degrees(math.acos(max(-1, min(1, vn[2]))))
    if cl > 1e-9:
        b = b.rotate(Axis((0, 0, 0), (cross[0] / cl, cross[1] / cl, cross[2] / cl)), ang)
    return b.translate(p1)

def ybore(center, r, w):
    c = Cylinder(r, w, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    c = c.rotate(Axis((0, 0, 0), (1, 0, 0)), 90)
    return c.translate(center)

# 节点
R = (0, 0, 50)        # 后轴
F = (WHEELBASE, 0, 50)  # 前轴
BB = (95, 0, 60)      # 五通/曲柄轴
S = (75, 0, 160)      # 座顶
HB = (222, 0, 95)     # 头管下
HT = (210, 0, 150)    # 头管上

seat_r = FIT["bearing_seat_608"] / 2

frame = beam(HB, BB, 7)          # 下管
frame += beam(BB, S, 7)          # 座管
frame += beam(HT, S, 6)          # 上管
frame += beam(BB, R, 6)          # 链撑
frame += beam(S, R, 5)           # 座撑
frame += beam(HB, HT, 10)        # 头管
frame -= beam((224, 0, 90), (208, 0, 155), 6)   # 头管转向孔

# 五通壳（曲柄轴承座）
frame += ybore(BB, 16, 22)
frame -= ybore(BB, seat_r, 24)

# 后叉 dropout 板 + 轴承座 + 助学轮臂 + 电机座
frame += Box(34, 22, 44).translate(R)
frame -= ybore(R, seat_r, 26)
frame += beam(R, (0, 55, 38), 4)
frame += beam(R, (0, -55, 38), 4)
frame += Box(26, 18, 6).translate((-22, 0, 58))   # 电机座 tab

export_stl(frame, os.path.join(OUT, "frame_petg.stl"))
export_step(frame, os.path.join(OUT, "frame_petg.step"))
bb = frame.bounding_box()
print(f"frame PETG mass={mass_g(frame.volume,'PETG'):.1f}g bbox=({bb.size.X:.0f},{bb.size.Y:.0f},{bb.size.Z:.0f})mm")