"""整车装配效果图（Blender）：导入各零件 STL 按装配位姿放置，彩色渲染。
招牌画面：鹈鹕骑在辅助轮自行车上。供目视核对总体比例/干涉/可辨识。
用法: blender --background --python assemble_render.py -- <cad_out> <renders>
"""
import bpy, math, os, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, REND = argv[0], argv[1]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def mat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.5
    return m
M_petg = mat("petg", (0.75, 0.75, 0.78)); M_tpu = mat("tpu", (0.2, 0.2, 0.22))
M_white = mat("white", (0.9, 0.9, 0.88)); M_orange = mat("orange", (0.9, 0.45, 0.1))
M_cf = mat("cf", (0.25, 0.25, 0.28)); M_peba = mat("peba", (0.5, 0.5, 0.55))

def add(name, m, loc=(0, 0, 0), rot=None, mirror=False):
    bpy.ops.wm.stl_import(filepath=os.path.join(OUT, name + ".stl"))
    o = bpy.context.selected_objects[0]
    o.scale = (0.001, -0.001 if mirror else 0.001, 0.001)
    bpy.ops.object.transform_apply(scale=True)
    if rot: o.rotation_euler = rot
    o.location = loc
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o

X90 = (math.radians(90), 0, 0)
add("frame_petg", M_petg)
for x in (0, 0.24):
    add("wheel_rim_petg", M_petg, (x, 0, 0.05), X90)
    add("wheel_tire_tpu", M_tpu, (x, 0, 0.05), X90)
for y in (0.055, -0.055):
    add("train_rim_petg", M_petg, (0, y, 0.038))
    add("train_tire_tpu", M_tpu, (0, y, 0.038))
add("crank_peba", M_peba, (0.095, 0, 0.06))
add("crank_pulley_petg", M_petg, (0.095, 0, 0.06))
add("motor_pulley_petg", M_petg, (-0.022, 0, 0.058))
add("rear_pulley_petg", M_petg, (0, 0, 0.05))
add("fork_petg", M_petg)
add("pelican_skeleton_petcf", M_cf)
add("electronics_tray_petg", M_petg)
add("pelican_body_tpu", M_white, (0.075, 0, 0.185))   # 翅已融合进身体
add("pelican_beak_tpu", M_orange, (0.075, 0, 0.185))

def limb(name, m, p1, p2):
    v = Vector(p2) - Vector(p1)
    o = add(name, m, p1)
    o.rotation_euler = v.to_track_quat('X', 'Z').to_euler()
    return o
hipR, kneeR, footR = (0.075, 0.03, 0.15), (0.095, 0.03, 0.10), (0.115, 0.016, 0.06)
hipL, kneeL, footL = (0.075, -0.03, 0.15), (0.095, -0.03, 0.10), (0.075, -0.016, 0.06)
limb("thigh_peba", M_peba, hipR, kneeR); limb("shin_peba", M_peba, kneeR, footR)
limb("thigh_peba", M_peba, hipL, kneeL); limb("shin_peba", M_peba, kneeL, footL)
add("foot_petg", M_peba, footR); add("foot_petg", M_peba, footL)

objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
corners = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
center = sum(corners, Vector()) / len(corners)
d = max((max(c[i] for c in corners) - min(c[i] for c in corners)) for i in range(3))
cd = bpy.data.cameras.new("cam"); cd.clip_start = 0.001
cam = bpy.data.objects.new("cam", cd); bpy.context.collection.objects.link(cam)
cam.location = center + Vector((d * 1.6, -d * 1.6, d * 0.9))
tgt = bpy.data.objects.new("tgt", None); bpy.context.collection.objects.link(tgt); tgt.location = center
con = cam.constraints.new('TRACK_TO'); con.target = tgt; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'
bpy.context.scene.camera = cam
for nm, en, loc in [("key", 700 * d * d, center + Vector((d, -d * 0.6, d * 1.2))),
                    ("fill", 250 * d * d, center + Vector((-d, d * 0.8, d * 0.6)))]:
    ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en; ld.size = d * 1.5
    lo = bpy.data.objects.new(nm, ld); bpy.context.collection.objects.link(lo); lo.location = loc
w = bpy.data.worlds.new("w"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.4
bpy.context.scene.world = w
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 32
sc.render.resolution_x = 850; sc.render.resolution_y = 850
sc.render.film_transparent = True
sc.render.filepath = os.path.join(REND, "assembly_full.png")
bpy.ops.render.render(write_still=True)
print("ASSEMBLY_RENDER_OK")