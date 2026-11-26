"""Blender 鹈鹕软皮造型（招牌：大嘴+喉囊）。风格化有机体，白身+橙嘴囊。
导出 body/beak/wing STL；渲染彩色效果图供目视核对可辨识性与比例。
软皮空心+塞棉花+分件闭合为制造细化（M3/M5），本步先立外形。
用法: blender --background --python pelican_skin.py -- <out_dir> <renders_dir>
"""
import bpy, math, os, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, REND = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True); os.makedirs(REND, exist_ok=True)

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def sphere(name, loc, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale; return o

def cone(name, loc, r1, r2, depth, rot):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; return o

body = sphere("body", (0, 0, 0), (0.06, 0.045, 0.05))
neck = cone("neck", (0.055, 0, 0.065), 0.02, 0.013, 0.08, (0, math.radians(-23), 0))
head = sphere("head", (0.07, 0, 0.10), (0.02, 0.018, 0.018))
tail = cone("tail", (-0.06, 0, 0.01), 0.02, 0.005, 0.05, (0, math.radians(-100), 0))
bpy.ops.object.select_all(action='DESELECT')
for o in [body, neck, head, tail]: o.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join(); body = bpy.context.active_object; body.name = "pelican_body"

beak = cone("beak", (0.12, 0, 0.10), 0.012, 0.002, 0.07, (0, math.radians(90), 0))
pouch = sphere("pouch", (0.10, 0, 0.083), (0.03, 0.014, 0.018))
bpy.ops.object.select_all(action='DESELECT')
beak.select_set(True); pouch.select_set(True); bpy.context.view_layer.objects.active = beak
bpy.ops.object.join(); beak = bpy.context.active_object; beak.name = "pelican_beak"

wingL = sphere("wingL", (0, 0.045, 0.01), (0.05, 0.008, 0.028))
wingR = sphere("wingR", (0, -0.045, 0.01), (0.05, 0.008, 0.028))

def mat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.6
    return m
white = mat("white", (0.9, 0.9, 0.88)); orange = mat("orange", (0.9, 0.45, 0.1))
body.data.materials.append(white); wingL.data.materials.append(white); wingR.data.materials.append(white)
beak.data.materials.append(orange)

for o in [body, beak, wingL, wingR]:
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.context.view_layer.objects.active = o; bpy.ops.object.shade_smooth()

for o, name in [(body, "pelican_body_tpu"), (beak, "pelican_beak_tpu"), (wingL, "pelican_wing_tpu")]:
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.wm.stl_export(filepath=os.path.join(OUT, name + ".stl"), export_selected_objects=True)

# 自动取景渲染
objs = [body, beak, wingL, wingR]
corners = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
center = sum(corners, Vector()) / len(corners)
d = max((max(c[i] for c in corners) - min(c[i] for c in corners)) for i in range(3))
cam_data = bpy.data.cameras.new("cam"); cam_data.clip_start = 0.001
cam = bpy.data.objects.new("cam", cam_data); bpy.context.collection.objects.link(cam)
cam.location = center + Vector((d * 1.2, -d * 1.2, d * 0.7))
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
print("PELICAN_SKIN_OK")