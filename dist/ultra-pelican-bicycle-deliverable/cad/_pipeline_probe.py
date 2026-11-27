"""管线探针：验证 build123d 建模 -> 导出 STL/STEP -> 回读 STEP 全链路。
跑通后才在真实零件上复用此管线。输出到 scratch/（gitignore）。
"""
import os
from build123d import Cylinder, Box, Pos, export_stl, export_step, import_step
from params import mass_g

os.makedirs("scratch", exist_ok=True)

# 一个带孔的测试件（模拟轴承座圆盘）
part = Cylinder(25, 10) - Cylinder(11, 12) - Pos(15, 0, 0) * Cylinder(3, 12)

stl = "scratch/probe.stl"
stp = "scratch/probe.step"
export_stl(part, stl)
export_step(part, stp)

# 回读 STEP 校验体积一致
back = import_step(stp)
v0 = part.volume
v1 = back.volume
print(f"原始体积   : {v0:.1f} mm^3")
print(f"回读体积   : {v1:.1f} mm^3")
print(f"体积偏差   : {abs(v0-v1)/v0*100:.3f} %")
print(f"PETG 质量  : {mass_g(v0,'PETG'):.1f} g")
print(f"STL 存在   : {os.path.exists(stl)} ({os.path.getsize(stl)} bytes)")
print(f"STEP 存在  : {os.path.exists(stp)} ({os.path.getsize(stp)} bytes)")
print("管线 OK" if abs(v0 - v1) / v0 < 0.01 else "管线异常")