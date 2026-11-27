# CAD 建模规范（M3）

来源：用户 2026-11-27 对车架 v1（圆杆逐根 union）的纠正——交接重叠小、毛刺、不平齐 = 脆弱点。

## 结构件（车架 / 鹈鹕骨架 / 电控托盘等承力件）
0. **规范适用于所有结构件**（车架/骨架/曲柄/腿/助学轮臂），不得只改被批评的那一个。圆杆/圆柱 union 一律禁止作为承力成型（实物造不出来/脆弱）。
1. **中面描中心线轮廓**：把各管描成等宽厚线，union 成连通面；沿厚度方向**对称挤出**成等厚板。连杆用 stadium 轮廓挤出（common.link_solid）； out-of-plane 横杆用矩形 bar 贴平面。禁止圆杆逐根 union。
2. **棱边倒角/圆角**加强：chamfer 比 fillet 稳健；fillet 整体失败时用 max_fillet 逐边细化。
3. 轴承孔 / 销孔在挤出后减去；配合按 [cad/params.py](../cad/params.py) FIT 保守表（无打样，宁松不卡）。
4. 等厚保证两侧平齐；交接为整块连通材料，非相切点。
5. 每零件出 STL/STEP + 渲染 QA（renders/ 纳管）+ 质量属性。

## 外观 / 非结构件
鹈鹕软皮等有机造型走 Blender 轨：**重叠 primitive join → 体素 remesh 融合 → 平滑 = 单一连续有机曲面**（plush 软体必须无缝）。禁止 primitive 直接拼接（有缝/雪人感）；metaball 需调阈值否则散球，弃用默认。骨架仍按结构件规范。导出 STL 统一毫米（global_scale=1000）。

## 渲染 QA
scripts/render_stl.py：包围盒自动取景 + 曝光随尺寸缩放 + 近裁剪 1mm；平面件用 top 视。