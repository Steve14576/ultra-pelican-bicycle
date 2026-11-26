"""腿部连杆：大腿/小腿（两端低阻铰链孔）+ 脚（踝孔+踏面）。
B 类低阻自由铰链：M3 销 + 轴套，clearance 配合不抱死（蹬车驱动链要求）。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Box, export_stl, export_step
from common import beam, ybore
from params import THIGH, SHIN, FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
pin_r = FIT["pivot_pin_M3"] / 2


def link(L):
    b = beam((0, 0, 0), (L, 0, 0), 5)
    b -= ybore((0, 0, 0), pin_r, 12)
    b -= ybore((L, 0, 0), pin_r, 12)
    return b


thigh = link(THIGH)
shin = link(SHIN)
foot = Box(18, 12, 5).translate((0, 0, 0))
foot -= ybore((0, 0, 0), pin_r, 14)   # 踝孔

for name, part, mat in [("thigh_peba", thigh, "PEBA"), ("shin_peba", shin, "PEBA"),
                        ("foot_petg", foot, "PETG")]:
    export_stl(part, os.path.join(OUT, name + ".stl"))
    export_step(part, os.path.join(OUT, name + ".step"))
    print(f"{name:16s} {mat:5s} mass={mass_g(part.volume, mat):6.1f}g")