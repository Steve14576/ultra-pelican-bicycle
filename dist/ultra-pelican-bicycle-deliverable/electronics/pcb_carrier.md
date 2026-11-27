# 载体 PCB 设计包（M4，嘉立创EDA专业版 + JLCPCB）

决策：定制载体板（through-hole 模块插座），不飞线。Cindy 只焊少数连接器、插模块。
本文件为可直接在嘉立创EDA专业版落板的完整设计输入：outline / 孔位 / 插座 / 网络 / 线宽。

## 板框与安装
- 外形 60 × 35 mm，厚 1.6mm，2 层，圆角 R2。
- 4× M3 安装孔 @ (±25, ±12)（与电控托盘 standoff 一致），孔径 3.2。
- 板面丝印位号 + 极性标记 + "PELICAN BIKE v1"。

## 模块插座（母排，直插）
- J4 SuperMini：2×8 母排 2.54，间距按 SuperMini 外形（两排相距 22.86mm? 按实物核）。
- J5 DRV8833 模块：1×6 母排（VM GND AOUT1 AOUT2 AIN1 AIN2 PWMA nSLEEP 按模块丝印核）。
- J6 buck 模块：1×4 母排（IN+ IN- OUT+ OUT-）。

## 连接器 / 开关 / 保护
J1 电池 JST-XH2（keyed）→ F1 PTC → VM/buck；J2 电机 JST-XH2；J3 舵机 3P；SW1 总开关串电池正；LED+220Ω 接 GPIO10。

## 网络表（核心）
```
BAT+ --SW1--F1-- VM, buckIN+
BAT- -- GND
buckOUT+ -- 5V -- SuperMini5V, J3.V, DRV8833.nSLEEP
buckOUT- -- GND
GPIO4 -- AIN1 ; GPIO5 -- AIN2 ; GPIO6 -- PWMA
GPIO7 -- J3.S ; GPIO10 -- LED -- 220 -- GND
AOUT1 -- J2.1 ; AOUT2 -- J2.2
VM -- 100µF -- GND
```

## 线宽 / 间距
- 电机/电池功率路径 ≥1.0mm（1.8A 峰值）。
- 5V 路径 ≥0.6mm；逻辑信号 0.3mm。
- 间距 ≥0.2mm；铺地 GND 底层。

## 制造
JLCPCB 2 层 1.6mm 1oz，5 片；SMT 不贴（全直插，Cindy 手焊连接器）。
Gerber 由嘉立创EDA专业版按本设计导出（M5 制造包收口）。