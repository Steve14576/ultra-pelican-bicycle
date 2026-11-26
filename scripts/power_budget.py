"""M4 功率预算先验校核（无打样）。峰值电流 vs 器件额定，续航估算，保险丝选型。
数据为器件典型量级（datasheet BOM 阶段逐条核），结论留余量判定。
"""
# 负载电流（A）
N20_run, N20_stall = 0.3, 1.0      # 6V 减速电机
MG90S_run, MG90S_stall = 0.2, 0.7  # 5V 舵机
ESP_tx, ESP_avg = 0.35, 0.08       # ESP32-C3 WiFi

# 5V 轨（buck 输出）：舵机 + ESP32
v5_peak = MG90S_stall + ESP_tx
v5_avg = MG90S_run + ESP_avg
BUCK_RATED = 3.0
print(f"5V 轨峰值 {v5_peak:.2f}A / 额定 {BUCK_RATED}A -> {'OK' if v5_peak < BUCK_RATED*0.8 else '紧'}")

# 7.4V 电池轨：电机 + buck 输入(效率0.9)
buck_in_peak = v5_peak * 5 / 7.4 / 0.9
batt_peak = N20_stall + buck_in_peak
batt_avg = N20_run + v5_avg * 5 / 7.4 / 0.9
print(f"电池峰值 {batt_peak:.2f}A / 平均 {batt_avg:.2f}A")

# DRV8833：VM<=10.8V, 单通道连续1.2A/峰值2A
DRV_CONT, DRV_PEAK, DRV_VM_MAX = 1.2, 2.0, 10.8
print(f"DRV8833 电机电流 stall {N20_stall}A vs 连续{DRV_CONT}/峰值{DRV_PEAK} -> {'OK' if N20_stall <= DRV_CONT else '需限流'}")
print(f"DRV8833 VM 7.4V vs 上限{DRV_VM_MAX} -> OK")

# 电池 2S 18650 带保护板：典型持续放电 2-5A
BATT_CONT = 2.0
print(f"电池峰值 {batt_peak:.2f}A vs 持续{BATT_CONT}A -> {'OK' if batt_peak < BATT_CONT else '紧,选动力芯'}")

# 保险丝/PTC：hold > 平均, trip < 电池/导线安全
print(f"保险丝选型: hold 1.5A / trip 3A（平均{batt_avg:.2f}A < hold < 峰值{batt_peak:.2f}A 容忍瞬态）")

# 续航
CAP_mAh = 2500
runtime_h = CAP_mAh / 1000 / batt_avg
print(f"续航估算（平均负载）≈ {runtime_h:.1f} h；混合使用打 0.5 折 ≈ {runtime_h*0.5:.1f} h")