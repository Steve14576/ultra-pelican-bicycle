"""关键件手算应力（评审#5 承诺兑现）。梁模型弯曲应力 vs 材料屈服，保守点载。
载荷量级小（整车~0.74kg），应力不主导；刚度/配合主导。本脚本落档承诺的手算校核。
"""
import math
g = 9.81
W = 0.735 * g          # 整车重 N
sigma_yield = {"PETG": 50.0, "PEBA": 30.0, "PET-CF": 60.0}  # MPa 量级

def beam_sigma(P, L, w, t):
    M = P * L / 4                      # 简支中点载
    I = w * t ** 3 / 12
    return M * (t / 2) / I             # MPa (N,mm)

cases = [
    ("车架下管", "PETG", W * 0.5, 131, 14, 14),
    ("曲柄臂", "PEBA", 1.0, 20, 10, 8),
    ("大腿连杆", "PEBA", 1.0, 60, 10, 6),
    ("头管", "PETG", W * 0.3, 56, 18, 14),
]
ok = True
for name, mat, P, L, w, t in cases:
    s = beam_sigma(P, L, w, t)
    sf = sigma_yield[mat] / s
    ok &= sf > 3
    print(f"{name:8s} {mat:7s} sigma={s:6.2f} MPa  屈服{sigma_yield[mat]:.0f}  安全系数={sf:7.1f}")
print("手算应力:", "PASS(余量充足)" if ok else "FAIL")