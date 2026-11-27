"""转向链补件（评审#2）：舵机座 + 推杆 + 车把。
MG90S(22.8宽) 不进头管φ12孔 -> 外置舵机座于头管后/上管前；推杆连舵机臂与前叉转向臂；
车把装转向管顶（鹈鹕翅搭握）。此前缺 CAD/BOM/手册，现补。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Box, Cylinder, Axis, Align, export_stl, export_step
from common import link_solid, ybore, beam
from params import FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
pin_r = FIT["pivot_pin_M3"] / 2

# 舵机座：上衣管上方，立柱接上衣管顶面；舵机输出臂 y=10 侧置
br = Box(26, 16, 4).translate((198, 0, 166))
br += Box(26, 3, 12).translate((198, 8, 172))
br += Box(26, 3, 12).translate((198, -8, 172))
br += Box(6, 16, 8).translate((198, 0, 162))
br -= Cylinder(FIT["heatset_M3"] / 2, 10).translate((198, 5, 160))
br -= Cylinder(FIT["heatset_M3"] / 2, 10).translate((198, -5, 160))

# 推杆：舵机臂(198,10,172) -> 前叉转向臂(206,10,166)，y=10 侧置避上衣管
rod = link_solid((198, 10, 172), (206, 10, 166), 6, 4)
rod -= ybore((198, 10, 172), pin_r, 8)
rod -= ybore((206, 10, 166), pin_r, 8)

# 车把：茎(转向管顶->把横) + 把横沿Y + 握把
hb = beam((208, 0, 155), (206, 0, 165), 5)
hb += ybore((206, 0, 165), 4, 120)
hb += ybore((206, 55, 165), 6, 12)
hb += ybore((206, -55, 165), 6, 12)

for name, part, mat in [("servo_bracket_petg", br, "PETG"), ("pushrod_peba", rod, "PEBA"),
                        ("handlebar_petg", hb, "PETG")]:
    export_stl(part, os.path.join(OUT, name + ".stl"))
    export_step(part, os.path.join(OUT, name + ".step"))
    print(f"{name:20s} {mat:5s} mass={mass_g(part.volume, mat):5.1f}g")