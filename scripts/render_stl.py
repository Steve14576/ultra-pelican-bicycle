"""Blender 视觉 QA：加载 STL 渲染 PNG（无打样下的目视校验手段）。
用法: blender.exe --background --python render_stl.py -- <stl路径> <png路径> [r,g,b]
"""
import bpy, sys, os, math

argv = sys.argv[sys.argv.index("--") + 1:]
stl_path, png_path = os.path.abspath(argv[0]), os.path.abspath(argv[1])
os.makedirs(os.path.dirname(png_path), exist_ok=True)
color = tuple(float(c) for c in argv[2].split(",")) if len(argv) > 2 else (0.7, 0.7, 0.72)
view = argv[3] if len(argv) > 3 else "iso"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.wm.stl_import(filepath=stl_path)
obj = bpy.context.selected_objects[0]
obj.scale = (0.001, 0.001, 0.001)   # STL mm -> Blender m，光照距离才正常
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.shade_smooth()

mat = bpy.data.materials.new("plastic")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (*color, 1)
bsdf.inputs["Roughness"].default_value = 0.45
obj.data.materials.append(mat)

# 自动取景：以零件包围盒中心为目标，距离/光强随尺寸缩放（任意零件通用）
from mathutils import Vector
corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
center = sum(corners, Vector()) / 8
d = max(obj.dimensions)

cam_data = bpy.data.cameras.new("cam")
cam_data.clip_start = 0.001   # 小零件相机距离近，默认 0.1m 近裁剪会切掉模型
cam_data.clip_end = 100
cam = bpy.data.objects.new("cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = center + Vector((d * 1.1, -d * 1.1, d * 0.8))
if view == "top":
    cam.location = center + Vector((0, 0, d * 2.4))
elif view == "front":
    cam.location = center + Vector((0, -d * 1.6, d * 0.2))
target = bpy.data.objects.new("target", None)
bpy.context.collection.objects.link(target)
target.location = center
con = cam.constraints.new('TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
bpy.context.scene.camera = cam

# 面光（主光+补光）+ 环境光；能量随距离²缩放保证曝光一致
light_data = bpy.data.lights.new("key", 'AREA')
light_data.energy = 700 * d * d
light_data.size = d * 1.5
light = bpy.data.objects.new("key", light_data)
bpy.context.collection.objects.link(light)
light.location = center + Vector((d * 0.8, -d * 0.5, d * 1.2))

fill_data = bpy.data.lights.new("fill", 'AREA')
fill_data.energy = 250 * d * d
fill_data.size = d * 2
fill = bpy.data.objects.new("fill", fill_data)
bpy.context.collection.objects.link(fill)
fill.location = center + Vector((-d * 1.0, d * 0.8, d * 0.6))

world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.4
bpy.context.scene.world = world

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 24
scene.render.resolution_x = 720
scene.render.resolution_y = 540
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = png_path
bpy.ops.render.render(write_still=True)
print("RENDER_OK", png_path)