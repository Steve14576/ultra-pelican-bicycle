# 里程碑计划

长程 agent 自主任务。人 = Cindy（11 岁智力设定，极低主观能动性），按手册做物理操作与采购。
详细基线见 [PROJECT_BRIEF.md](PROJECT_BRIEF.md)；工程完整性滚动自查见 [docs/completeness_checklist.md](docs/completeness_checklist.md)。

| 里程碑 | 内容 | 交付 | 状态 |
| --- | --- | --- | --- |
| M0 基线 | brief 落档，参数拍板 | PROJECT_BRIEF.md | ✓ 完成 |
| M1 调研核实 | 打印机/材料/元件可得性，技术选型冻结 | docs/M1_research.md | ✓ 完成 |
| M2 方案设计 | 机构+电控+关节+本体+仿真决策+拆件+强度 | docs/M2_design.md | ✓ 已冻结 |
| M3 全车建模 | 车架/轮组/传动/腿/鹈鹕骨架软体/电控盒 | cad/ 源文件+STL/3MF | ✓ 完成 |
| M4 电控工程 | 原理图/载体PCB/固件/接线表 | electronics/ | 进行中 |
| M5 制造包 | 切片工程+BOM冻结+Cindy操作手册 | manufacturing/ | ✓ 主体完成 |
| M6 交付自查 | BOM↔模型↔手册↔固件交叉核对，打包 | 交付包 | 进行中 |

## 已定参数

- 功能：电动真骑行（遥控，踩踏动作，助学轮平衡）
- 尺寸：整车 ~40cm
- 硬件预算：≤ ¥300（嘉立创+淘宝，不含打印机/耗材）
- 打印机：拓竹 H3C（主），P3C（备）
- 建模：build123d + Blender；切片：BambuStudio；PCB：嘉立创EDA专业版

## 关键决策

- 单电机后驱 + 后轮反带曲柄连杆踩踏（车跑即蹬）。
- 助学轮平衡；否决动量轮 / 转向自平衡。
- 关节分类：翅颈自锁可摆（G-Flex）；腿/曲柄/轮低阻自由。
- 鹈鹕：碳纤骨架 + TPU 软皮 + 棉花填充。
- 电控：定制载体 PCB（模块插座 + 端子），2S 带保护板电池组。
- 仿真：轻量校核（运动学/质心稳定/功率预算），不做 FEA/SPICE。
- 支撑：易拆支撑独立工具头；胎辋机械互锁混打。

## 仓库维护

agent 用 git 维护本仓库（用户授权）；README / 计划 / 提交日志 / 仓库简介由 agent 撰写；交付物最终打包。
远程：https://github.com/Steve14576/ultra-pelican-bicycle