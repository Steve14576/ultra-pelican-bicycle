"""M6 交付防漏交叉核对：BOM↔模型↔文档↔固件引脚。
打印件每个必须有 STL；关键文档齐备；固件 GPIO 与接线表一致。
"""
import os, csv, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "cad", "out")
ok = True

# 1) BOM 打印件 -> STL 存在
with open(os.path.join(ROOT, "manufacturing", "bom.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["类别"] == "打印":
            p = os.path.join(OUT, row["名称"] + ".stl")
            if not os.path.exists(p):
                ok = False; print("缺STL:", row["名称"])
print("BOM打印件STL核对:", "OK" if ok else "FAIL")

# 2) 关键文档齐备
docs = ["manufacturing/bom.md", "manufacturing/cindy_manual.md", "manufacturing/slicing.md",
        "electronics/pinout.md", "electronics/pcb_carrier.md",
        "electronics/firmware/pelican_bike.ino", "docs/M2_design.md", "docs/cad_conventions.md"]
for d in docs:
    if not os.path.exists(os.path.join(ROOT, d)):
        ok = False; print("缺文档:", d)
print("文档齐备:", "OK" if ok else "FAIL")

# 3) 固件 GPIO 与接线表一致
ino = open(os.path.join(ROOT, "electronics/firmware/pelican_bike.ino"), encoding="utf-8").read()
pin = open(os.path.join(ROOT, "electronics/pinout.md"), encoding="utf-8").read()
for g in ["4", "5", "6", "7", "10"]:
    if f"PIN_" not in ino or g not in pin:
        ok = False; print("引脚不一致:", g)
m = re.findall(r"const int PIN_\w+ = (\d+)", ino)
print("固件GPIO:", m, "接线表含:", all(g in pin for g in m))

print("M6 交叉核对:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)