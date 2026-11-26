"""把 renders/ 的效果图/QA图打包成自包含 HTML 画廊（base64 内嵌），供对话呈现。
用法: python make_gallery.py <输出目录>
"""
import base64, os, sys, io
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

items = [
    ("assembly_full.png", "整车效果图：鹈鹕骑辅助轮自行车（招牌画面）"),
    ("pelican_skin.png", "鹈鹕软皮：白身 + 橙长嘴 + 喉囊"),
    ("frame_petg.png", "车架 v2：中面轮廓对称挤出等厚板 + 倒角"),
    ("fork_petg.png", "前叉：转向管 + 双叉片 + 前轴座 + 舵机臂"),
    ("pelican_skeleton_petcf.png", "碳纤骨架：扁平 bar 贴平面连通"),
    ("crank_peba.png", "曲柄：扁平 stadium 连杆 + 脚踏踝销孔"),
    ("thigh_peba.png", "腿连杆：扁平 stadium 带圆眼（低阻铰链）"),
    ("wheel_rim_petg.png", "轮辋：减重孔 + 608 轴承座 + 互锁槽"),
    ("train_rim_petg.png", "助学轮：带轴孔实心盘"),
]

cards = []
for f, cap in items:
    p = os.path.join(ROOT, "renders", f)
    if not os.path.exists(p):
        continue
    b = base64.b64encode(open(p, "rb").read()).decode()
    im = Image.open(p).convert("RGB")
    im.thumbnail((480, 480))
    buf = io.BytesIO(); im.save(buf, format="PNG", optimize=True)
    b = base64.b64encode(buf.getvalue()).decode()
    cards.append(
        f'<figure style="margin:0;background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:10px">'
        f'<img src="data:image/png;base64,{b}" style="width:100%;display:block;background:#f5f7fa;border-radius:6px"/>'
        f'<figcaption style="font:13px/1.5 system-ui;color:#333;margin-top:8px">{cap}</figcaption></figure>'
    )

html = (
    '<div style="font:14px/1.6 system-ui;color:#222;max-width:960px;margin:0 auto">'
    '<h2 style="margin:0 0 4px">Ultra Pelican Bicycle — 效果图与 QA 图</h2>'
    '<p style="margin:0 0 16px;color:#666">无打样条件下以渲染目视 + 定量校核验证；全部结构件为轮廓挤出/扁平 bar 成型。</p>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">' + "".join(cards) + '</div></div>'
)
open(os.path.join(OUT, "gallery.html"), "w", encoding="utf-8").write(html)
print("gallery written:", os.path.join(OUT, "gallery.html"), len(cards), "images")