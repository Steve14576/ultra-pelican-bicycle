"""固件单源化：src/main.cpp 为唯一源；生成 pelican_bike.ino（去掉 #include <Arduino.h>，
因 Arduino IDE 自动注入）。消除评审#6 双源漂移。用法: python sync_firmware.py
"""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "electronics", "firmware")
src = open(os.path.join(ROOT, "src", "main.cpp"), encoding="utf-8").read()
ino = src.replace("#include <Arduino.h>\n", "", 1)
open(os.path.join(ROOT, "pelican_bike.ino"), "w", encoding="utf-8").write(ino)
print("ino regenerated from main.cpp")