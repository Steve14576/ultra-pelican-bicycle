"""轮组参数化建模：PETG 轮体（盘+轴承座+减重孔+互锁槽）+ TPU 胎（环+内舌）。
胎辋靠机械互锁（倒扣槽+舌）结合，不依赖化学粘合；舌留保守间隙（无打样，宁松不卡）。
导出 STL/STEP 到 cad/out/，打印质量属性。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Cylinder, Pos, export_stl, export_step
from params import WHEEL_R, WHEEL_W, TIRE_T, FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

rim_r = WHEEL_R - TIRE_T                 # 46 轮辋外半径
seat_r = FIT["bearing_seat_608"] / 2     # 11 轴承座孔半径

# PETG 轮体
body = Cylinder(rim_r, WHEEL_W)
body -= Cylinder(seat_r, WHEEL_W + 2)                 # 608 轴承通孔
for i in range(5):                                     # 5 个减重孔
    a = i * 2 * math.pi / 5
    body -= Pos(28 * math.cos(a), 28 * math.sin(a), 0) * Cylinder(8, WHEEL_W + 2)
groove = Cylinder(rim_r + 0.5, 4) - Cylinder(rim_r - 2, 4)   # 外缘互锁槽 R44->46 宽4
body -= groove

# TPU 胎：主环 + 内舌（舌留 0.2mm 保守间隙）
tire = Cylinder(WHEEL_R, WHEEL_W) - Cylinder(rim_r, WHEEL_W)
tongue = Cylinder(rim_r - 0.2, 3.8) - Cylinder(rim_r - 2 + 0.2, 3.8)
tire += tongue

for name, part, mat in [("wheel_rim_petg", body, "PETG"), ("wheel_tire_tpu", tire, "TPU")]:
    export_stl(part, os.path.join(OUT, name + ".stl"))
    export_step(part, os.path.join(OUT, name + ".step"))
    bb = part.bounding_box()
    print(f"{name:18s} {mat:5s} mass={mass_g(part.volume, mat):6.1f}g  "
          f"bbox=({bb.size.X:.1f},{bb.size.Y:.1f},{bb.size.Z:.1f})mm")
print("轮组导出完成 ->", OUT)