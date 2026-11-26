"""Blender 视觉 QA：加载 STL 渲染 PNG（无打样下的目视校验手段）。
用法: blender.exe --background --python render_stl.py -- <stl路径> <png路径> [r,g,b]
"""
import bpy, sys, os, math

argv = sys.argv[sys.argv.index("--") + 1:]
stl_path, png_path = os.path.abspath(argv[0]), os.path.abspath(argv[1])
os.makedirs(os.path.dirname(png_path), exist_ok=True)
color = tuple(float(c) for c in argv[2].split(",")) if len(argv) > 2 else (0.7, 0.7, 0.72)

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

# 相机 + 注视原点
cam_data = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (0.16, -0.16, 0.12)
target = bpy.data.objects.new("target", None)
bpy.context.collection.objects.link(target)
con = cam.constraints.new('TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
bpy.context.scene.camera = cam

# 面光（主光 + 补光）+ 环境光，保证 QA 图可读
light_data = bpy.data.lights.new("key", 'AREA')
light_data.energy = 18
light_data.size = 0.15
light = bpy.data.objects.new("key", light_data)
bpy.context.collection.objects.link(light)
light.location = (0.12, -0.08, 0.18)

fill_data = bpy.data.lights.new("fill", 'AREA')
fill_data.energy = 7
fill_data.size = 0.2
fill = bpy.data.objects.new("fill", fill_data)
bpy.context.collection.objects.link(fill)
fill.location = (-0.15, 0.12, 0.09)

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