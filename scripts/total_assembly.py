"""Blender 总装 + 运动仿真 + 出图/动画。
装配全部车件+鹈鹕件+紧固件/外购件 -> 导出单文件总装(GLB+STL) -> 关键帧驱动链运动 -> 渲静帧(优先)+MP4。
用法: blender --background --python total_assembly.py -- <cad_out> <renders>
"""
import bpy, math, os, sys
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, REND = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True); os.makedirs(REND, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def mat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.5
    return m
C_petg = mat("petg", (0.75, 0.75, 0.78)); C_tpu = mat("tpu", (0.2, 0.2, 0.22))
C_white = mat("white", (0.9, 0.9, 0.88)); C_orange = mat("orange", (0.9, 0.45, 0.1))
C_cf = mat("cf", (0.25, 0.25, 0.28)); C_peba = mat("peba", (0.5, 0.5, 0.55))
C_steel = mat("steel", (0.6, 0.6, 0.65)); C_black = mat("black", (0.1, 0.1, 0.1))
C_pcb = mat("pcb", (0.1, 0.4, 0.2)); C_batt = mat("batt", (0.2, 0.3, 0.6))

def add_stl(name, loc=(0, 0, 0), rot=None, color=C_petg):
    bpy.ops.wm.stl_import(filepath=os.path.join(OUT, name + ".stl"))
    o = bpy.context.selected_objects[0]; o.name = name
    o.scale = (0.001, 0.001, 0.001); bpy.ops.object.transform_apply(scale=True)
    if rot: o.rotation_euler = rot
    o.location = loc
    o.data.materials.append(color); bpy.ops.object.shade_smooth()
    return o

def prim(kind, loc, scale=(1, 1, 1), rot=None, color=C_steel, name="p"):
    if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=1, location=loc)
    elif kind == 'box': bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    elif kind == 'ring': bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.2, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    if rot: o.rotation_euler = rot
    o.data.materials.append(color); return o

X90 = (math.radians(90), 0, 0)
Y = (0, 0, 1)  # axis helper
# ---- 车件 ----
frame = add_stl("frame_petg")
fork = add_stl("fork_petg")
add_stl("servo_bracket_petg")
add_stl("pushrod_peba", color=C_peba)
add_stl("handlebar_petg")
rw_r = add_stl("wheel_rim_petg", (0, 0, 0.05), X90); rw_t = add_stl("wheel_tire_tpu", (0, 0, 0.05), X90, C_tpu)
fw_r = add_stl("wheel_rim_petg", (0.26, 0, 0.05), X90); fw_t = add_stl("wheel_tire_tpu", (0.26, 0, 0.05), X90, C_tpu)
tr = [add_stl("train_rim_petg", (0, y, 0.031)) for y in (0.055, -0.055)]
tt = [add_stl("train_tire_tpu", (0, y, 0.031), None, C_tpu) for y in (0.055, -0.055)]
crank = add_stl("crank_peba", (0.095, 0, 0.06), None, C_peba)
cpul = add_stl("crank_pulley_petg", (0.095, 0, 0.06))
rpul = add_stl("rear_pulley_petg", (0, 0, 0.05))
mpul = add_stl("motor_pulley_petg", (-0.022, 0, 0.058))
# ---- 鹈鹕 ----
add_stl("pelican_skeleton_petcf", color=C_cf)
add_stl("electronics_tray_petg")
add_stl("pelican_body_tpu", (0.075, 0, 0.185), None, C_white)
add_stl("pelican_beak_tpu", (0.075, 0, 0.185), None, C_orange)
add_stl("pelican_belly_plug_tpu", (0.075, 0, 0.140), None, C_white)
for y in (0.016, -0.016):
    add_stl("bushing_peba", (0.075, y, 0.15), X90, C_peba)
# ---- 紧固件/外购件 ----
prim('cyl', (0, 0, 0.05), (0.004, 0.004, 0.12), X90, name="axle_rear")
prim('cyl', (0.095, 0, 0.06), (0.004, 0.004, 0.04), X90, name="axle_crank")
prim('cyl', (0.26, 0, 0.05), (0.004, 0.004, 0.04), X90, name="axle_front")
for x, z in [(0, 0.05), (0.095, 0.06), (0.26, 0.05)]:
    for y in (0.01, -0.01):
        prim('cyl', (x, y, z), (0.011, 0.0035, 0.011), X90, C_black, name="bearing608")
for y in (0.03, -0.03):
    prim('cyl', (0.075, y, 0.15), (0.0015, 0.0015, 0.012), X90, name="pin_hip")
prim('box', (-0.022, 0, 0.058), (0.024, 0.012, 0.012), None, C_black, name="motor_N20")
prim('box', (0.198, 0, 0.172), (0.023, 0.012, 0.022), None, C_black, name="servo_MG90S")
prim('box', (0.12, 0, 0.08), (0.065, 0.035, 0.018), None, C_batt, name="battery_2S")
prim('box', (0.12, 0, 0.092), (0.06, 0.035, 0.0016), None, C_pcb, name="pcb_carrier")
prim('box', (-0.011, 0, 0.054), (0.024, 0.004, 0.006), None, C_black, name="belt_motor_rear")
prim('box', (0.0475, 0, 0.055), (0.095, 0.004, 0.006), None, C_black, name="belt_rear_crank")

# ---- 单文件总装导出（静态装配姿态）----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "total_assembly.glb"), export_format='GLB', use_selection=True)
bpy.ops.wm.stl_export(filepath=os.path.join(OUT, "total_assembly.stl"), export_selected_objects=True, global_scale=1000)
bpy.ops.object.select_all(action='DESELECT')

# ---- 运动仿真 ----
steer = bpy.data.objects.new("steer_pivot", None); bpy.context.collection.objects.link(steer)
steer.location = (0.216, 0, 0.12)
bpy.context.view_layer.update()   # 刷新 matrix_world，否则 parent_inverse 用旧矩阵甩飞子物体
for o in (fork, fw_r, fw_t):
    o.parent = steer; o.matrix_parent_inverse = steer.matrix_world.inverted()

BB = Vector((0.095, 0, 0.06)); R = 0.02
HIPR = Vector((0.075, 0.016, 0.15)); HIPL = Vector((0.075, -0.016, 0.15))
L1 = L2 = 0.06
def ik(H, F):
    d = F - H; dist = min(d.length, L1 + L2 - 1e-4); dn = d.normalized()
    M = H + dn * (dist / 2)
    x = Vector((1, 0, 0)); u = x - dn * x.dot(dn)
    if u.length < 1e-6: u = Vector((0, 0, 1))
    u.normalize(); h = math.sqrt(max(L1 * L1 - (dist / 2) ** 2, 0))
    return M + u * h
def place_leg(thigh, shin, foot, H, F):
    K = ik(H, F)
    thigh.location = H; thigh.rotation_euler = (K - H).to_track_quat('X', 'Z').to_euler()
    shin.location = K; shin.rotation_euler = (F - K).to_track_quat('X', 'Z').to_euler()
    foot.location = F
thR = add_stl("thigh_peba", color=C_peba); shR = add_stl("shin_peba", color=C_peba); foR = add_stl("foot_petg", color=C_peba)
thL = add_stl("thigh_peba", color=C_peba); shL = add_stl("shin_peba", color=C_peba); foL = add_stl("foot_petg", color=C_peba)

sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = 48; sc.render.fps = 24
for f in range(1, 49):
    sc.frame_set(f)
    tw = (f - 1) / 48 * 2 * math.pi * 2
    tc = tw / 1.8
    spinY = lambda a: (Matrix.Rotation(a, 3, 'Y') @ Matrix.Rotation(math.radians(90), 3, 'X')).to_euler()
    for o in (rw_r, rw_t, rpul): o.rotation_euler = spinY(tw); o.keyframe_insert("rotation_euler", frame=f)
    for o in (fw_r, fw_t): o.rotation_euler = spinY(tw); o.keyframe_insert("rotation_euler", frame=f)
    crank.rotation_euler = (0, tc, 0); crank.keyframe_insert("rotation_euler", frame=f)
    cpul.rotation_euler = (0, tc, 0); cpul.keyframe_insert("rotation_euler", frame=f)
    mpul.rotation_euler = (0, tw * 2, 0); mpul.keyframe_insert("rotation_euler", frame=f)
    steer.rotation_euler = (0, 0, math.radians(15) * math.sin(f / 48 * 2 * math.pi)); steer.keyframe_insert("rotation_euler", frame=f)
    FR = BB + Vector((R * math.cos(tc), 0.016, R * math.sin(tc)))
    FL = BB + Vector((-R * math.cos(tc), -0.016, -R * math.sin(tc)))
    place_leg(thR, shR, foR, HIPR, FR); place_leg(thL, shL, foL, HIPL, FL)
    for o in (thR, shR, foR, thL, shL, foL):
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)

# ---- 相机/光 ----
objs = [o for o in sc.objects if o.type == 'MESH']
corners = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
center = sum(corners, Vector()) / len(corners)
d = max((max(c[i] for c in corners) - min(c[i] for c in corners)) for i in range(3))
cd = bpy.data.cameras.new("cam"); cd.clip_start = 0.001
cam = bpy.data.objects.new("cam", cd); bpy.context.collection.objects.link(cam)
cam.location = center + Vector((d * 1.5, -d * 1.5, d * 0.8))
tgt = bpy.data.objects.new("tgt", None); bpy.context.collection.objects.link(tgt); tgt.location = center
con = cam.constraints.new('TRACK_TO'); con.target = tgt; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'
sc.camera = cam
for nm, en, loc in [("key", 700 * d * d, center + Vector((d, -d * 0.6, d * 1.2))),
                    ("fill", 250 * d * d, center + Vector((-d, d * 0.8, d * 0.6)))]:
    ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en; ld.size = d * 1.5
    lo = bpy.data.objects.new(nm, ld); bpy.context.collection.objects.link(lo); lo.location = loc
w = bpy.data.worlds.new("w"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.4
sc.world = w
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 16
sc.render.resolution_x = 720; sc.render.resolution_y = 540
sc.render.film_transparent = True

# 静帧优先
for f in (1, 12, 24, 36):
    sc.frame_set(f)
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(REND, f"motion_{f:02d}.png")
    bpy.ops.render.render(write_still=True)
# 动画：渲 PNG 序列（外部 Pillow 合成 GIF，不依赖 FFMPEG）
seq = os.path.join(REND, "seq"); os.makedirs(seq, exist_ok=True)
sc.render.image_settings.file_format = 'PNG'
for f in range(1, 49):
    sc.frame_set(f)
    sc.render.filepath = os.path.join(seq, f"f_{f:03d}.png")
    bpy.ops.render.render(write_still=True)
print("TOTAL_ASSEMBLY_MOTION_OK")