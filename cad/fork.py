"""前叉 + 转向管 + 舵机臂（补件：前轮此前悬空无持握）。
转向管沿头管轴（HB->HT）插入头管孔；双叉片持前轴；舵机臂接 MG90S 连杆。
结构件规范：叉片扁平连杆 + 矩形冠部连通，转向管为旋转体管。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Box, chamfer, Axis, export_stl, export_step
from common import beam, ybore, link_solid
from params import FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

HB = (222, 0, 95); HT = (210, 0, 150); F = (260, 0, 50)
axle_r = FIT["axle_clear_8"] / 2

fork = beam((225.3, 0, 79.7), (206.7, 0, 165.3), 5)   # 转向管与头管孔严格同轴（孔r6/管r5留1mm）
fork += Box(10, 26, 10).translate((222, 0, 80))      # 冠部（头管底以下，避免与头管实体干涉）
fork += link_solid((222, 10, 80), (260, 10, 50), 8, 6)   # 右叉片
fork += link_solid((222, -10, 80), (260, -10, 50), 8, 6)  # 左叉片
fork += ybore(F, 6, 26)                              # 前轴座
fork -= ybore(F, axle_r, 28)                         # 前轴孔
fork += link_solid((206, 10, 166), (200, 10, 172), 6, 4)   # 转向臂（上衣管上方、y=10侧置避干涉）
fork -= ybore((200, 10, 172), FIT["pivot_pin_M3"] / 2, 8)
try:
    fork = chamfer(fork.edges().filter_by(Axis.Y), 0.8)
except Exception:
    pass

export_stl(fork, os.path.join(OUT, "fork_petg.stl"))
export_step(fork, os.path.join(OUT, "fork_petg.step"))
print(f"fork PETG mass={mass_g(fork.volume,'PETG'):.1f}g")