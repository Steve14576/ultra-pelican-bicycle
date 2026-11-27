"""M6 交付防漏交叉核对：BOM↔模型↔文档↔固件引脚。
打印件每个必须有 STL（文件名在 BOM"规格"列）；关键文档齐备；固件 GPIO 与接线表一致。
"""
import os, csv, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "cad", "out")
all_ok = True

# 1) BOM 打印件 -> STL 存在
sec = True
with open(os.path.join(ROOT, "manufacturing", "bom.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["类别"] == "打印":
            if not os.path.exists(os.path.join(OUT, row["规格"] + ".stl")):
                sec = False; print("缺STL:", row["规格"])
print("BOM打印件STL核对:", "OK" if sec else "FAIL"); all_ok &= sec

# 2) 关键文档齐备
sec = True
docs = ["manufacturing/bom.md", "manufacturing/cindy_manual.md", "manufacturing/slicing.md",
        "electronics/pinout.md", "electronics/pcb_carrier.md",
        "electronics/firmware/pelican_bike.ino", "docs/M2_design.md", "docs/cad_conventions.md"]
for d in docs:
    if not os.path.exists(os.path.join(ROOT, d)):
        sec = False; print("缺文档:", d)
print("文档齐备:", "OK" if sec else "FAIL"); all_ok &= sec

# 3) 固件 GPIO 与接线表一致
sec = True
ino = open(os.path.join(ROOT, "electronics/firmware/pelican_bike.ino"), encoding="utf-8").read()
pin = open(os.path.join(ROOT, "electronics/pinout.md"), encoding="utf-8").read()
gpio = re.findall(r"PIN_\w+\s*=\s*(\d+)", ino)
for g in gpio:
    if g not in pin:
        sec = False; print("接线表缺GPIO:", g)
print("固件GPIO:", gpio, "接线表一致:", "OK" if sec else "FAIL"); all_ok &= sec

print("M6 交叉核对:", "PASS" if all_ok else "FAIL")
sys.exit(0 if all_ok else 1)