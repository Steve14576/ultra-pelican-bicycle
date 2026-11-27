"""把 renders/seq/ 的 PNG 序列合成 motion.gif（Pillow，不依赖 FFMPEG）。"""
import os, glob
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
seq = sorted(glob.glob(os.path.join(ROOT, "renders", "seq", "f_*.png")))
frames = []
for p in seq:
    im = Image.open(p).convert("RGB")
    im.thumbnail((480, 480))
    frames.append(im.convert("P", palette=Image.ADAPTIVE))
out = os.path.join(ROOT, "renders", "motion.gif")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
print("gif frames:", len(frames), "->", out, os.path.getsize(out), "bytes")