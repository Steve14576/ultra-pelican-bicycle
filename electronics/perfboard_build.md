# 洞洞板电控装配（可制造交付，评审#4 整改）

定制 PCB 无 Gerber/EDA 工程、Cindy 无法从说明落板 → **主路径改洞洞板飞线**（brief 允许"PCB打板或洞洞板飞线"）。
本文给逐孔布局 + 网络接线表，Cindy 照表插模块、焊跨线即可。[pcb_carrier.md](pcb_carrier.md) 降为**可选参考（非 fab-ready）**。

板：24×18 孔洞洞板，2.54mm。坐标 (行,列)，行1在上。

## 布局
```
行1   : BAT+ JST(1,2-3)  SW(1,5-6)  FUSE(1,8-9)
行3   : SuperMini 排A (3,4..11)   [5V,GPIO4,5,6,7,10,GND...]
行12  : SuperMini 排B (12,4..11)
行13  : 5V  rail (13,4..15)
行14  : VM  rail (14,4..9)
行15  : DRV8833 (15,4..9)[VM,GND,AOUT1,AOUT2,AIN1,AIN2,PWMA,nSLEEP]  buck(15,12..15)[IN+,IN-,OUT+,OUT-]
行17  : GND rail (17,2..15)
行18  : MOTOR JST(18,4-5)  SERVO(18,8-10)[S,V,G]  LED+R(18,12-13)
```
模块用母排座插接（不直焊模块），跨线焊在孔间。

## 网络接线表（照此焊跨线）
| 网络 | 从 | 到 |
| --- | --- | --- |
| BAT+ | JST(1,2) | SW(1,5) |
| SW出 | SW(1,6) | FUSE(1,8) |
| VM | FUSE(1,9) | DRV VM(15,4) + buck IN+(15,12) + VM rail(14,4) |
| GND | JST(1,3) | GND rail(17,2)；DRV GND(15,5)、buck IN-(15,13)、SuperMini GND、SERVO G(18,10) 共接 |
| 5V | buck OUT+(15,14) | 5V rail(13,4)；SuperMini 5V、SERVO V(18,9)、DRV nSLEEP(15,9) |
| AIN1 | SuperMini GPIO4 | DRV(15,7) |
| AIN2 | SuperMini GPIO5 | DRV(15,8) |
| PWMA | SuperMini GPIO6 | DRV(15,9)? 按模块丝印 PWMA |
| AOUT1 | DRV(15,6) | MOTOR(18,4) |
| AOUT2 | DRV(15,6+1) | MOTOR(18,5) |
| SERVO_S | SuperMini GPIO7 | SERVO(18,8) |
| LED | SuperMini GPIO10 | LED+R(18,12) |

（DRV/buck 引脚序以模块丝印为准；表给网络名，孔位为布局参考。）

## 步骤
1. 焊母排座/ JST /开关/保险丝/LED 到布局位。
2. 按网络表焊跨线；功率线（VM/GND/5V）用 ≥0.5mm 线或加锡拖焊。
3. 插 SuperMini/DRV8833/buck（对丝印方向）。
4. 万用表蜂鸣测 BAT+↔GND 不响；上电测 5V rail=5V、VM=电池压。
5. VM 加 ≥100µF 电容跨 VM-GND（防舵机堵转拉垮）。