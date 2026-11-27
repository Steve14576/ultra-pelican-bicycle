# M1 调研核实与选型

状态：进行中（2026-11-27 开始）。来源分层：【给定】= 用户 brief 给定；【检索】= 当场网络检索；【探针】= 本机实测。未核实项如实标注，不写成定论。

## 1. 打印机【检索，多源交叉】

主目标 = 拓竹 H3C（现场已有【给定】）。核实事实：

- 幅面 330 × 320 × 325 mm。40cm 整车多数零件可单件打印，长件斜放或分件。
- SwapTek 9 工具头自动切换，切换 < 6 秒；硬化钢喷嘴 0.2 / 0.4 / 0.6 / 0.8 mm。
- 喷嘴 350°C，热床 120°C，主动加热腔体 65°C。
- FlexFeed 挤出机自动适配 1.75 / 2.85 mm；2.85mm TPU 75A 需专用热端，打印速度约为普通 TPU 三倍。
- AMS 3H：9 盘位，打印中 85°C 烘干，RFID 识别，CMYKW 混色；可并联旧款 AMS 扩到 24 料。
- 官方支持材料含 PLA、ABS、PC、PA-CF、PET-CF。

备选 = P3C：幅面 256 × 256 × 260 mm，标配 5 头（最多 7 头），能力同源、幅面小一号，分件更多。

来源：
- https://bambulab.com/en-us/h3c/specs （规格页，抓取 403，事实取自搜索摘要）
- https://blog.bambulab.com/tool-changer-game-changer-bambu-lab-presents-h3c-the-defining-new-generation-of-3d-printers/
- https://www.3dprintingjournal.com/p/bambu-lab-introduces-h3c-a-3d-printer
- https://blog.bambulab.com/bambu-lab-p3c-brings-home-its-h3c-technology-at-half-the-price/
- https://bambulab.cn/zh-cn/h3c

## 2. 建模工具【探针，已验证】

选型 = build123d（Python 参数化 CAD）。本机探针：uv 建 .venv（Python 3.12.13），安装 build123d 0.13.0 + cadquery-ocp-novtk 8.0.1，import 成功。

理由：机构件（轴承座、热熔螺母柱、齿轮、连杆）需要精确参数化与可程序化校验尺寸；导出 STEP/STL；纯 Python 与本机 uv 环境一致，不装全局 GUI 软件。鹈鹕有机壳体若参数化困难，再引入 Blender 便携版（尚未安装）。

本机现状：仅 uv；无 OpenSCAD / Blender / Bambu Studio。备选建模 = OpenSCAD 便携版（放项目内）。切片工具（BambuStudio 或 OrcaSlicer CLI）在 M5 阶段落实。

## 3. 材料【部分核实】

已确认 H3C 能力覆盖：TPU（含 75A 软料）、PETG（通用支持）、PET-CF / PA-CF（硬化钢喷嘴）。

功能分配（初步，M2 冻结）：轮胎 = TPU；车架 = PETG 或 PET-CF；齿轮 / 连杆 = PETG 或 PEBA（韧、低摩擦）；鹈鹕壳体 = PETG + TPU 多材料混打。

待核实（BOM 阶段核实商品可得性，不阻塞方案）：TPU-玻纤、PETG-TPU 共混、PEBA 的具体牌号与货源。用户 brief 的材料池是"推荐包括但不限于"，按功能选子集即可。

已知限制【检索摘要】：2.85mm 热端只可打 2.85mm 柔性线材；Bambu Studio 当前 2.85mm 预设仅 Bambu TPU 75A 与 Generic TPU 两种。官方 wiki 兼容性指南页为 JS 渲染，正文未能抓取，后续如需逐条核实可用浏览器渲染。

来源：https://wiki.bambulab.com/zh/h3c/manual/filament-compatibility-guide

## 4. 电控元件【检索，调研代理已返回 2026-11-27】

渠道结论：成品模块类（主控板、舵机、驱动模块、充电模块、2 节电池座、热熔螺母、GT2 传动、洞洞板）嘉立创基本无成品货，走淘宝；嘉立创可供散件（杜邦线、排针、单节 18650 座 ¥2.18、部分轴承、电芯）。下表价格为检索到的公开标价估算，BOM 阶段逐条核价冻结。

| 类别 | 选型 | 渠道 | 估价（¥） |
| --- | --- | --- | --- |
| 主控 | ESP32-C3 SuperMini | 淘宝（嘉立创 DEVKITM-1 ¥53.92 缺货） | 7–12 |
| 驱动电机 | N20 减速电机 6V 100–300rpm | 淘宝（嘉立创类目未核实） | 7–11 |
| 电机驱动 | DRV8833 / TB6612 模块 | 淘宝（嘉立创仅裸芯片） | 2.4–6.8 |
| 转向舵机 | MG90S（金属齿）/ SG90 | 淘宝（嘉立创无成品） | 7–11 / 3–6 |
| 电池 | 2S 7.4V 带保护板成品组 | 淘宝（嘉立创 3S 组 ¥40.25） | 24–48 |
| 充电 | 配套 7.4V 充电器 / TP4056 模块 | 淘宝 | 1–12 |
| 电池座 | 2 节 18650 座（如用散芯） | 淘宝（嘉立创单节座 ¥2.18） | 3.5–4 |
| 降压 | 5V/2A buck（mini360/MP1584） | 淘宝 | ~3 |
| 辅料 | 洞洞板、排针、杜邦/硅胶线、JST | 淘宝/嘉立创 | ~10 |
| 紧固 | M2/M3 螺丝盒装 + 热熔螺母套件 | 淘宝（嘉立创未核实套装） | 15–44 + ~14 |
| 轴承 | 608ZZ / 625ZZ | 淘宝（嘉立创 MRO 有轴承类目） | 0.8–3/个 |
| 传动 | GT2 闭口带 + 带轮 | 淘宝 | 带 1.8–2.5 + 轮 1.8–6.6 |

粗总价 ¥110–150（含运费余量），≤¥300 充裕。
安全结论：电池优先成品带保护板电池组 + 配套插头充电器，免裸芯焊接，Cindy 插拔即可。
未核实项（BOM 阶段核实）：嘉立创 N20 具体商品、M2/M3 套装、608ZZ、洞洞板现货。

来源（调研代理提供）：
- https://item.szlcsc.com/21789516.html （嘉立创 ESP32-C3-DEVKITM-1）
- https://www.szlcsc.com/mro.html （嘉立创 MRO 目录）
- https://item.szlcsc.com/mro/6029055.html / https://item.szlcsc.com/mro/51591317.html / https://item.szlcsc.com/mro/6030882.html
- https://mrunx.com/parts/n20-motor/ （N20 采购参考）

## 5. 选型冻结状态

- 已冻结：打印机 = H3C；建模 = build123d（本机探针通过）；电控骨架 = ESP32-C3 SuperMini + DRV8833 + N20 + MG90S + 2S 带保护板电池组（渠道与估价已核实，具体商品 BOM 阶段锁定）。
- 待冻结：材料具体牌号（等 BOM 阶段）；机构与电控详细方案在 M2 冻结（冻结前给用户过目）。