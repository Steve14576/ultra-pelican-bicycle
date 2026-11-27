"""轴套（M3 销低阻铰链用）+ 打印备件基件。PEBA/ PETG 光滑套，OD5 ID3.2 L6。
 leg 髋/膝/踝 + 翅/颈自锁铰链共用；BOM 含备件余量。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import export_stl, export_step
from common import ybore
from params import FIT, mass_g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

bush = ybore((0, 0, 0), 2.5, 6) - ybore((0, 0, 0), FIT["bushing_id_M3"] / 2, 8)
export_stl(bush, os.path.join(OUT, "bushing_peba.stl"))
export_step(bush, os.path.join(OUT, "bushing_peba.step"))
print(f"bushing PEBA mass={mass_g(bush.volume,'PEBA'):.2f}g")