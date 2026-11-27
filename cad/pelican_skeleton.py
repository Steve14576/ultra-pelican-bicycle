"""鹈鹕碳纤骨架（PET-CF，承载）：脊柱板 + 髋横杆 + 翅根/颈根铰链座。
结构件规范：中面轮廓对称挤出 + 倒角。承载走骨架，软皮不承载。
坐标与车架一致（坐车座 S=(75,0,160)，髋在曲柄上方 ~90）。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import extrude, chamfer, Box, Axis, export_stl, export_step
from common import seg_face, ybore
from params import FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
pin_r = FIT["pivot_pin_M3"] / 2

spine = seg_face((75, 0, 150), (115, 0, 205), 20)
sk = extrude(spine, 6, both=True)

# 横杆/座用矩形_bar_（扁平面贴平面，非圆杆拼接），与脊柱板平齐连通
sk += Box(12, 40, 12).translate((75, 0, 150))     # 髋横杆（髋孔与脚踏踝销同平面 y=±16，防腿链锁死）
sk += Box(12, 56, 10).translate((95, 0, 185))     # 翅根横杆
sk += Box(10, 10, 10).translate((95, 28, 185))    # 翅根座
sk += Box(10, 10, 10).translate((95, -28, 185))
sk += Box(12, 16, 12).translate((115, 0, 205))    # 颈根座
try:
    sk = chamfer(sk.edges().filter_by(Axis.Y), 1.0)
except Exception:
    pass

sk -= ybore((75, 16, 150), pin_r, 14)             # 髋铰链孔（低阻，y=±16 与踝同平面）
sk -= ybore((75, -16, 150), pin_r, 14)
sk -= ybore((95, 28, 185), pin_r, 12)             # 翅自锁铰链孔
sk -= ybore((95, -28, 185), pin_r, 12)
sk -= ybore((115, 0, 205), pin_r, 18)             # 颈铰链孔

export_stl(sk, os.path.join(OUT, "pelican_skeleton_petcf.stl"))
export_step(sk, os.path.join(OUT, "pelican_skeleton_petcf.step"))
print(f"pelican_skeleton PET-CF mass={mass_g(sk.volume,'PET-CF'):.1f}g")