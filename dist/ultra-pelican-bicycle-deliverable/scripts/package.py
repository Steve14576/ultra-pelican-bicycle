"""M6 交付打包：把工程文件/固件/制造包/文档/效果图 zip 成单一交付物。
用法: python package.py  -> dist/ultra-pelican-bicycle-deliverable.zip
"""
import os, zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)
target = os.path.join(DIST, "ultra-pelican-bicycle-deliverable.zip")

include_dirs = ["cad", "electronics", "manufacturing", "docs", "renders", "scripts"]
include_files = ["README.md", "PLAN.md", "PROJECT_BRIEF.md", ".gitignore"]
skip = {"__pycache__", ".venv", "scratch", "src", ".pio"}

n = 0
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for d in include_dirs:
        for base, dirs, files in os.walk(os.path.join(ROOT, d)):
            dirs[:] = [x for x in dirs if x not in skip]
            for f in files:
                if f.endswith((".pyc", ".tmp")):
                    continue
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, ROOT)); n += 1
    for f in include_files:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            z.write(p, f); n += 1
print("packaged", n, "files ->", target, os.path.getsize(target), "bytes")