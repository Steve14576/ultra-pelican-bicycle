"""Blender 鹈鹕软皮 v3：重叠 primitive join → 体素 remesh 融合 → 平滑 = 单一连续有机曲面。
（v1 primitive 拼接有缝、v2 metaball 阈值散球，均弃；v3 remesh 保证无缝融合。）
白身一体 + 橙嘴囊一体。导出 STL(mm) + 效果图。
用法: blender --background --python pelican_skin.py -- <out> <renders>
"""
import bpy, math, os, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, REND = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True); os.makedirs(REND, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def sphere(loc, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=loc)
    o = bpy.context.active_object; o.scale = scale; return o

def cone(loc, r1, r2, depth, rot):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    return bpy.context.active_object

def fuse(objs, name, voxel=0.002):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.active_object; o.name = name
    bpy.ops.object.transform_apply(scale=True)
    rm = o.modifiers.new("remesh", 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = voxel
    bpy.ops.object.modifier_apply(modifier=rm.name)
    sm = o.modifiers.new("smooth", 'SMOOTH'); sm.factor = 0.6; sm.iterations = 8
    bpy.ops.object.modifier_apply(modifier=sm.name)
    bpy.ops.object.shade_smooth()
    return o

body = fuse([
    sphere((0, 0, 0), (0.06, 0.045, 0.05)),
    cone((0.055, 0, 0.065), 0.02, 0.013, 0.08, (0, math.radians(-23), 0)),
    sphere((0.07, 0, 0.10), (0.02, 0.018, 0.018)),
    cone((-0.06, 0, 0.01), 0.02, 0.005, 0.05, (0, math.radians(-100), 0)),
    sphere((0, 0.045, 0.01), (0.05, 0.008, 0.028)),
    sphere((0, -0.045, 0.01), (0.05, 0.008, 0.028)),
], "pelican_body")

beak = fuse([
    cone((0.12, 0, 0.10), 0.012, 0.002, 0.07, (0, math.radians(90), 0)),
    sphere((0.10, 0, 0.083), (0.03, 0.014, 0.018)),
], "pelican_beak")

def mat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.6
    return m
body.data.materials.append(mat("white", (0.9, 0.9, 0.88)))
beak.data.materials.append(mat("orange", (0.9, 0.45, 0.1)))

for o, name in [(body, "pelican_body_tpu"), (beak, "pelican_beak_tpu")]:
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.wm.stl_export(filepath=os.path.join(OUT, name + ".stl"), export_selected_objects=True, global_scale=1000)

objs = [body, beak]
corners = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
center = sum(corners, Vector()) / len(corners)
d = max((max(c[i] for c in corners) - min(c[i] for c in corners)) for i in range(3))
cd = bpy.data.cameras.new("cam"); cd.clip_start = 0.001
cam = bpy.data.objects.new("cam", cd); bpy.context.collection.objects.link(cam)
cam.location = center + Vector((d * 1.4, -d * 1.4, d * 0.8))
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
sc.render.resolution_x = 800; sc.render.resolution_y = 600
sc.render.film_transparent = True
sc.render.filepath = os.path.join(REND, "pelican_skin.png")
bpy.ops.render.render(write_still=True)
print("PELICAN_SKIN_V3_OK")