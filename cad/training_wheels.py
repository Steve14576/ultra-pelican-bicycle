"""助学轮（略小于主轮，倾斜接地）：PETG 轮毂盘 + TPU 胎，轴沿 Y。
结构件规范：等厚盘 + 孔。本地坐标原点，装配时移到助学轮臂端 (0,±55,38)。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import export_stl, export_step
from common import ybore
from params import TRAIN_R, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

rim_r = TRAIN_R - 3
rim = ybore((0, 0, 0), rim_r, 8) - ybore((0, 0, 0), 2.6, 10)   # 5mm 轴滑配
tire = ybore((0, 0, 0), TRAIN_R, 8) - ybore((0, 0, 0), rim_r, 8)

for name, part, mat in [("train_rim_petg", rim, "PETG"), ("train_tire_tpu", tire, "TPU")]:
    export_stl(part, os.path.join(OUT, name + ".stl"))
    export_step(part, os.path.join(OUT, name + ".step"))
    print(f"{name:16s} {mat:5s} mass={mass_g(part.volume, mat):5.1f}g")