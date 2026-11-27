"""全局参数与先验配合公差表。单位 mm。
硬约束：无打样/DFM 迭代 → 配合取保守值，宁略松不卡死；按 FDM 收缩 ~0.2–0.5mm 留隙。
所有零件模块共享本表，改一处全局生效。
"""

# 材料密度 g/cm^3（量级值，mass props 用）
DENSITY = {
    "PETG": 1.27, "PET-CF": 1.30, "TPU": 1.20,
    "G-Flex": 1.15, "PEBA": 1.05, "PA-CF": 1.15,
}

# 整车布置（M2 初值）
WHEELBASE = 240.0
WHEEL_R = 50.0        # 主轮半径（轮径 100）
WHEEL_W = 12.0        # 主轮宽
TIRE_T = 4.0          # 胎厚
TRAIN_R = 30.0        # 助学轮半径（略小，倾斜接地）
TRAIN_W = 8.0

# 轴承（标准件）
BEARING_608 = {"id": 8.0, "od": 22.0, "w": 7.0}   # 轮轴/曲柄轴
BEARING_625 = {"id": 5.0, "od": 16.0, "w": 5.0}   # 备选小轴承

# 先验配合公差表（保守，一次成型）
FIT = {
    "bearing_seat_608": 22.0,   # 608 座孔 = OD，线到线轻压入（PETG 柔，可压）
    "bearing_seat_625": 16.0,
    "axle_clear_8": 8.3,        # 8mm 轴滑配孔（+0.3）
    "axle_clear_5": 5.3,
    "heatset_M3": 4.0,          # M3 热熔螺母底孔
    "heatset_M2": 3.0,
    "screw_clear_M3": 3.3,      # M3 螺丝过孔
    "screw_clear_M2": 2.3,
    "pivot_pin_M3": 3.2,        # 腿铰链 M3 销间隙（低阻）
    "bushing_id_M3": 3.4,       # 轴套内径
}

# 曲柄 / 腿连杆（m2_sanity.py 校验过的几何）
CRANK_R = 20.0        # 曲柄半径（脚踏圆）
HIP_HEIGHT = 90.0     # 髋关节相对曲柄中心高度
THIGH = 60.0
SHIN = 60.0
CRANK_RATIO = 1.8     # 后轴->曲柄 减速
BELT_RATIO = 2.0      # 电机->后轴 减速

# 结构
WALL_MIN = 3.0        # PETG 最小壁厚
FILLET_R = 1.5        # 应力集中圆角

def mass_g(volume_mm3, material):
    return volume_mm3 / 1000.0 * DENSITY[material]