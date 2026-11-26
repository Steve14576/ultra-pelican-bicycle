"""车架 v2：中面轮廓 + 对称挤出 + 圆角（结构件建模规范）。
不再用圆杆逐根 union（交接重叠小/毛刺/不平齐=脆弱点）。
做法：X-Z 中面把各管描成等宽厚线轮廓并 union 成连通面，沿 Y 对称挤出成等厚板，
交接处为整块连通材料；再对 Y 向棱边圆角加强。轴承孔/转向孔事后减去。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import Rectangle, Box, Axis, extrude, fillet, chamfer, export_stl, export_step
from common import beam, ybore
from params import WHEELBASE, FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

PLATE_T = 14.0   # Y 向等厚


def seg_face(p1, p2, t):
    """X-Z 中面上 p1->p2 的等宽厚线轮廓面（宽 t）。"""
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    mid = [(p1[i] + p2[i]) / 2 for i in range(3)]
    r = Rectangle(L, t)
    r = r.rotate(Axis((0, 0, 0), (1, 0, 0)), 90)          # XY -> XZ
    th = -math.degrees(math.atan2(v[2], v[0]))
    r = r.rotate(Axis((0, 0, 0), (0, 1, 0)), th)          # 长度对准 v
    return r.translate(mid)


R = (0, 0, 50); BB = (95, 0, 60); S = (75, 0, 160)
HB = (222, 0, 95); HT = (210, 0, 150)
seat_r = FIT["bearing_seat_608"] / 2

profile = seg_face(HB, BB, 14)   # 下管
profile += seg_face(BB, S, 14)   # 座管
profile += seg_face(HT, S, 12)   # 上管
profile += seg_face(BB, R, 12)   # 链撑
profile += seg_face(S, R, 10)    # 座撑
profile += seg_face(HB, HT, 18)  # 头管

frame = extrude(profile, PLATE_T / 2, both=True)

# 棱边倒角/圆角加强，失败则保留挤出体（交接已为整块连通材料）
try:
    frame = chamfer(frame.edges().filter_by(Axis.Y), 1.0)
    print("chamfer OK")
except Exception:
    try:
        frame = fillet(frame.edges().filter_by(Axis.Y), 0.8)
        print("fillet OK")
    except Exception as e:
        print("edge-break skipped (refine with max_fillet):", e)

# 孔：后轴/五通轴承座（Y 向），头管转向孔（沿转向轴）
frame -= ybore(R, seat_r, PLATE_T + 4)
frame -= ybore(BB, seat_r, PLATE_T + 4)
frame -= beam((224, 0, 90), (208, 0, 155), 6)

# 助学轮臂 + 电机座
frame += beam(R, (0, 55, 38), 4)
frame += beam(R, (0, -55, 38), 4)
frame += Box(26, 18, 6).translate((-22, 0, 58))

export_stl(frame, os.path.join(OUT, "frame_petg.stl"))
export_step(frame, os.path.join(OUT, "frame_petg.step"))
bb = frame.bounding_box()
print(f"frame v2 PETG mass={mass_g(frame.volume,'PETG'):.1f}g bbox=({bb.size.X:.0f},{bb.size.Y:.0f},{bb.size.Z:.0f})mm")