# 工程完整性自查清单

定位：维护性自查工具（非交付物），跨里程碑滚动维护。来源 = Cindy 反馈 + 独立评审(docs/agent_reminder.md) + agent 自查。
**硬约束：无打样 / DFM 迭代，先验仿真驱动一次成型；凡"样件验证"一律改为先验校核 + 保守设计。**
状态记号：[x] 已做（附证据）；[ ] 真未做（标归属）。评审#5 整改：已做必销项，未做不混列。

## A. 机构与关节
- [x] 驱动扭矩/速度 — scripts/m2_sanity.py
- [x] 腿连杆工作空间/死点 — m2_sanity.py
- [x] 腿链共面（髋=踝 y=±16）+ 全周期平面扫掠 — scripts/leg_planar_check.py PASS（评审#1）
- [x] 关节分类 自锁/低阻 — M2 §4
- [x] 平衡=助学轮 — M2 §3
- [x] 结构件轮廓挤出+倒角 — cad_conventions.md
- [x] 脚踝铰链（踝销孔+脚孔）— cad/drivetrain.py / legs.py
- [x] 曲柄 180° 相位 — cad/drivetrain.py
- [x] 轴向限位 E 卡簧 — BOM + 手册§5
- [x] 转向链补件（舵机座/推杆/车把）— cad/steering.py（评审#2）
- [x] 转向限位 + 3D 布尔扫掠 ±15° 零干涉 — scripts/steer_sweep.py PASS（评审#5）
- [x] 头管孔同轴+贯穿底端帽；前叉冠部避头管 — frame.py/fork.py（评审#6）
- [x] 助学轮离地1mm近触；臂嵌入14mm — frame.py（评审#6）
- [x] 皮带张紧机构（电机座滑槽）— frame.py 滑槽（M8）
- [x] 轮胎胎纹抓地 — wheel.py 12 沟（M8）

## B. 鹈鹕本体
- [x] 软皮+棉花+CF 骨架方案 — M2 §5
- [x] 骨架承载路径 — cad/pelican_skeleton.py
- [x] 嘴囊可辨识 — renders/pelican_skin.png
- [x] 皮壳空心壁1.5+腹填棉口+腹盖 — pelican_skin.py solidify+boolean（M8）

## C. 电控与电气
- [x] 电控载体=洞洞板可制造交付 — electronics/perfboard_build.md（评审#4）
- [x] 功率预算 — scripts/power_budget.py
- [x] 反接保护 keyed+PTC — pinout.md / BOM
- [x] VM bulk 电容+舵机隔离 — perfboard_build.md 步骤5 / pinout.md
- [x] 电机软启/限幅/看门狗 — firmware
- [x] 固件按住走（300ms 心跳）— firmware PAGE（评审#3）
- [x] 导线 keyed 防错插 — pinout.md
- [x] 开关/充电口外部可达 — perfboard SW1 / 电池插头
- [x] 走线槽/应力释放（扎带槽+脊）— electronics_tray.py（M8）

## D. 仿真与校核（先验）
- [x] 轻量校核决策 — M2 §7
- [x] 质心/助学轮稳定 — cg_check.py
- [x] 运动学扫掠（腿平面+转向3D）— leg_planar_check.py / steer_sweep.py
- [x] 配合公差表 — cad/params.py FIT
- [x] 关键件手算应力 — scripts/stress_check.py PASS（评审#5）
- [x] 整车装配效果图核对 — renders/assembly_full.png

## E. 制造与装配
- [x] 拆件/支撑/强度原则 — M2 §9-11
- [x] 热熔胶枪入 BOM — bom.csv
- [x] 装配顺序+工具清单 — cindy_manual.md
- [x] 打印备件（轴套/销）— BOM 备件行（M8）

## F. 固件与操作
- [x] 刷固件路径（bin+esptool 0x0 / Arduino IDE）— firmware.bin + 手册§6
- [x] 固件单源（main.cpp→.ino）— scripts/sync_firmware.py（评审#6）
- [x] 手机 AP+控制页步骤 — 手册§7
- [x] 万用表验电/查短 — 手册§3/4
- [x] 焊接安全 — 手册§0

## G. 验收
- [x] BOM↔模型↔文档↔固件 交叉核对 — m6_check.py PASS
- [x] 续航估算 ≈2.4h — power_budget.py
- [ ] 功能验收（直行/踩踏/转向/不倒）— 实物后验，交付后

## H. 采购可得性
- [x] 渠道/估价、棉花、G-Flex — M1 §4
- [ ] N20 datasheet / 嘉立创现货逐条核 — 真未做，采购阶段
- [ ] TPU-玻纤 / PEBA 牌号 — 真未做，采购阶段

## M7 评审整改记录（2026-11-27）
评审#1 腿共面锁死→修+探针；#2 转向链补件；#3 固件按住走→修；#4 PCB→洞洞板可制造；#5 手算应力/转向扫掠落档+台账销项+WebSocket 漂移声明；#6 头管同轴/助学轮/臂咬合/单源。
剩余真未做：无（M8 已闭环：皮带张紧/胎纹/皮壳空心/走线槽/备件）。采购阶段核 N20 datasheet/牌号；实物路试交付后。