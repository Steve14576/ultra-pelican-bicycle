"""共享几何助手：梁、Y 向孔、中面厚线轮廓面、扁平连杆（stadium 轮廓挤出）。"""
import math
from build123d import Cylinder, Rectangle, Circle, Pos, Axis, Align, extrude


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


def seg_face(p1, p2, t):
    """X-Z 中面上 p1->p2 的等宽厚线轮廓面（宽 t），供对称挤出成等厚板。"""
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    mid = [(p1[i] + p2[i]) / 2 for i in range(3)]
    r = Rectangle(L, t)
    r = r.rotate(Axis((0, 0, 0), (1, 0, 0)), 90)
    th = -math.degrees(math.atan2(v[2], v[0]))
    r = r.rotate(Axis((0, 0, 0), (0, 1, 0)), th)
    return r.translate(mid)


def link_solid(p1, p2, w, t):
    """扁平连杆：X-Z 中面 stadium 轮廓（矩形+两端圆）对称挤出厚 t。
    真 CAD 成型（非圆杆拼接），两端自带圆眼，适合铰链链接。"""
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    mid = [(p1[i] + p2[i]) / 2 for i in range(3)]
    f = Rectangle(L, w)
    f += Pos(-L / 2, 0, 0) * Circle(w / 2)
    f += Pos(L / 2, 0, 0) * Circle(w / 2)
    f = f.rotate(Axis((0, 0, 0), (1, 0, 0)), 90)
    th = -math.degrees(math.atan2(v[2], v[0]))
    f = f.rotate(Axis((0, 0, 0), (0, 1, 0)), th)
    f = f.translate(mid)
    return extrude(f, t / 2, both=True)