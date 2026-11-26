"""共享几何助手：梁（任意方向圆杆）与 Y 向孔/圆柱。所有零件模块复用。"""
import math
from build123d import Cylinder, Axis, Align


def beam(p1, p2, r):
    """p1->p2 的圆杆梁，半径 r。"""
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    vn = [c / L for c in v]
    b = Cylinder(r, L, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cross = (-vn[1], vn[0], 0.0)
    cl = math.sqrt(sum(c * c for c in cross))
    ang = math.degrees(math.acos(max(-1, min(1, vn[2]))))
    if cl > 1e-9:
        b = b.rotate(Axis((0, 0, 0), (cross[0] / cl, cross[1] / cl, cross[2] / cl)), ang)
    return b.translate(p1)


def ybore(center, r, w):
    """沿 Y 轴的圆柱（实心），用作孔时从主体减去。"""
    c = Cylinder(r, w, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    c = c.rotate(Axis((0, 0, 0), (1, 0, 0)), 90)
    return c.translate(center)