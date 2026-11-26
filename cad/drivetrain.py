"""传动组：曲柄臂×2（180°相位）+ 脚踏×2（踝销孔）+ 曲柄带轮。
曲柄轴沿 Y；脚踏踝销孔沿 Y（低阻铰链，脚相对小腿自由转）。带轮 GT2 齿形金属保底。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import export_stl, export_step
from common import beam, ybore
from params import CRANK_R, FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

axle_r = FIT["axle_clear_8"] / 2
pin_r = FIT["pivot_pin_M3"] / 2

# 曲柄臂 + 轴套 + 脚踏（PEBA，韧耐磨）
crank = beam((0, 12, 0), (CRANK_R, 12, 0), 5)
crank += beam((0, -12, 0), (-CRANK_R, -12, 0), 5)
crank += ybore((0, 0, 0), 7, 26)
crank -= ybore((0, 0, 0), axle_r, 28)
crank += ybore((CRANK_R, 16, 0), 6, 14)     # 右脚踏
crank += ybore((-CRANK_R, -16, 0), 6, 14)   # 左脚踏
crank -= ybore((CRANK_R, 16, 0), pin_r, 16)  # 踝销孔
crank -= ybore((-CRANK_R, -16, 0), pin_r, 16)

# 曲柄带轮（PETG，GT2 金属保底）
pulley = ybore((0, 0, 0), 14, 6) - ybore((0, 0, 0), axle_r, 8)

for name, part, mat in [("crank_peba", crank, "PEBA"), ("crank_pulley_petg", pulley, "PETG")]:
    export_stl(part, os.path.join(OUT, name + ".stl"))
    export_step(part, os.path.join(OUT, name + ".step"))
    print(f"{name:20s} {mat:5s} mass={mass_g(part.volume, mat):6.1f}g")