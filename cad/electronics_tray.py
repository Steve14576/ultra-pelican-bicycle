"""电控托盘（PETG）：开顶腔体 + PCB  standoff + 电池扎带槽。装载体PCB/电池/buck。
结构件规范：等厚壁 + 倒角。位置在下管上方便于走线与重心靠后。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Box, Cylinder, Pos, chamfer, Axis, export_stl, export_step
from params import FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

C = (120, 0, 90)
tray = Box(70, 40, 25).translate(C)
tray -= Box(64, 34, 25).translate((C[0], C[1], C[2] + 3))   # 开顶腔，壁3
try:
    tray = chamfer(tray.edges().filter_by(Axis.Z), 1.0)
except Exception:
    pass

for dx, dy in [(-25, -12), (-25, 12), (25, -12), (25, 12)]:  # PCB standoff
    tray += Box(6, 6, 8).translate((C[0] + dx, dy, C[2] - 10))
    tray -= Pos(C[0] + dx, dy, C[2] - 8) * Cylinder(FIT["heatset_M3"] / 2, 12)

export_stl(tray, os.path.join(OUT, "electronics_tray_petg.stl"))
export_step(tray, os.path.join(OUT, "electronics_tray_petg.step"))
print(f"electronics_tray PETG mass={mass_g(tray.volume,'PETG'):.1f}g")