"""Render the parametrized 63-degree block guide under Blender."""

import math
import os
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

arguments = sys.argv[sys.argv.index('--') + 1:]
OUT = Path(arguments[0])
ORTHO_SCALE = float(arguments[1])
LENGTH, WIDTH, HEIGHT = map(float, arguments[2:5])
A0, A1, A2 = map(float, arguments[5:8])
DIRECTIONS = [int(value) for value in arguments[8:]]
THETA, CANVAS = 63.0, 1024
DIRECTION_YAW = [0, 45, 90, 135, 180, 225, 270, 315]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'
scene.render.resolution_x = scene.render.resolution_y = CANVAS
scene.render.image_settings.color_mode = 'RGBA'

world = bpy.data.worlds.new('world')
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6

sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
sun.data.energy = 2.0
az, el = math.radians(130), math.radians(76)
sun.rotation_euler = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))).to_track_quat('Z', 'Y').to_euler()
scene.collection.objects.link(sun)


def material(name, grey):
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    result.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (grey, grey, grey, 1.0)
    result.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
    return result


mesh = bpy.data.meshes.new('block')
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
bmesh.ops.scale(bm, vec=(LENGTH, WIDTH, HEIGHT), verts=bm.verts)
bmesh.ops.translate(bm, vec=(0.0, 0.0, HEIGHT / 2), verts=bm.verts)
bm.to_mesh(mesh)
bm.free()
block = bpy.data.objects.new('block', mesh)
mesh.materials.append(material('side', 0.45))
mesh.materials.append(material('front', 0.08))
for poly in mesh.polygons:
    poly.material_index = 1 if poly.normal.x > 0.9 else 0
scene.collection.objects.link(block)

arrow_mesh = bpy.data.meshes.new('arrow')
top = HEIGHT + 0.5
arrow_mesh.from_pydata([
    (LENGTH / 2 - A0, 0.0, top),
    (LENGTH / 2 - A1, A2, top),
    (LENGTH / 2 - A1, -A2, top),
], [], [(0, 1, 2)])
arrow = bpy.data.objects.new('arrow', arrow_mesh)
arrow_mesh.materials.append(material('arrow', 0.03))
arrow.parent = block
scene.collection.objects.link(arrow)

theta = math.radians(THETA)
cam = bpy.data.objects.new('camera', bpy.data.cameras.new('camera'))
cam.data.type = 'ORTHO'
cam.data.ortho_scale = ORTHO_SCALE
target = Vector((0.0, 0.0, HEIGHT / 2))
cam.location = target + Vector((0.0, -math.cos(theta), math.sin(theta))) * 1000.0
cam.rotation_euler = (math.pi / 2 - theta, 0.0, 0.0)
cam.data.clip_end = 4000.0
scene.collection.objects.link(cam)
scene.camera = cam

OUT.mkdir(parents=True, exist_ok=True)
for direction in DIRECTIONS:
    block.rotation_euler = (0.0, 0.0, math.radians(DIRECTION_YAW[direction]))
    scene.render.filepath = str(OUT / f'guide_raw_k{direction}.png')
    bpy.ops.render.render(write_still=True)

# The sandboxed PulseAudio finalizer hangs after the PNGs have been written.
sys.stdout.flush()
sys.stderr.flush()
os._exit(0)
