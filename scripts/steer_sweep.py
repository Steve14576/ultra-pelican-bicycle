"""转向扫掠干涉检查（3D 布尔，评审#5 承诺兑现）。
前叉+前轮绕头管轴(HB->HT) ±15° 旋转，与车架求交体积；>0 即干涉。
此前 2D 扫掠旋转轴错误，弃；本探针用真实几何布尔。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad"))
from build123d import import_step, Axis, Pos

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad", "out")
frame = import_step(os.path.join(OUT, "frame_petg.step"))
fork = import_step(os.path.join(OUT, "fork_petg.step"))
wheel = import_step(os.path.join(OUT, "wheel_rim_petg.step"))
wheel = wheel.rotate(Axis((0, 0, 0), (1, 0, 0)), 90).translate((260, 0, 50))
front = fork + wheel

HB = (222, 0, 95); HT = (210, 0, 150)
d = (HT[0] - HB[0], HT[1] - HB[1], HT[2] - HB[2])
axis = Axis(HB, d)
worst = 0.0
for ang in range(-15, 16, 5):
    moved = front.rotate(axis, ang)
    inter = frame.intersect(moved)
    v = 0.0 if inter is None else sum(s.volume for s in inter)
    worst = max(worst, v)
    print(f"steer {ang:+3d} deg  intersect volume = {v:8.1f} mm^3")
print("转向扫掠(3D布尔):", "PASS(无干涉)" if worst < 1.0 else f"FAIL(干涉 {worst:.0f} mm^3)")