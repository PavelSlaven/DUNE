#!/usr/bin/env python3
"""Render a supplied GLB soldier from eight fixed D2TM directions.

Run through Blender:
    blender --background --factory-startup --python this_file.py -- \
        --model soldier.glb --output artifacts/soldier_3d_review_v1/turntable
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


DIRECTIONS = (
    ("E", 0.0),
    ("NE", 45.0),
    ("N", 90.0),
    ("NW", 135.0),
    ("W", 180.0),
    ("SW", 225.0),
    ("S", 270.0),
    ("SE", 315.0),
)


def parse_args() -> argparse.Namespace:
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(arguments)


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_area_light(
    name: str,
    location: tuple[float, float, float],
    energy: float,
    size: float,
    target: Vector,
) -> None:
    data = bpy.data.lights.new(name=name, type="AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    light = bpy.data.objects.new(name=name, object_data=data)
    bpy.context.collection.objects.link(light)
    light.location = location
    look_at(light, target)


def world_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    return (
        Vector(tuple(min(point[axis] for point in points) for axis in range(3))),
        Vector(tuple(max(point[axis] for point in points) for axis in range(3))),
    )


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(args.model.resolve()))

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not meshes:
        raise RuntimeError("GLB contains no mesh objects")

    for obj in meshes:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    minimum, maximum = world_bounds(meshes)
    offset = Vector((-(minimum.x + maximum.x) / 2, -(minimum.y + maximum.y) / 2, -minimum.z))
    for obj in meshes:
        obj.location += offset
    bpy.context.view_layer.update()

    minimum, maximum = world_bounds(meshes)
    height = maximum.z - minimum.z
    width = max(maximum.x - minimum.x, maximum.y - minimum.y)
    target = Vector((0.0, 0.0, height * 0.47))

    root = bpy.data.objects.new("SoldierTurntable", None)
    bpy.context.collection.objects.link(root)
    for obj in meshes:
        world = obj.matrix_world.copy()
        obj.parent = root
        obj.matrix_world = world

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.render.image_settings.color_depth = "8"
    scene.render.resolution_percentage = 100
    scene.render.use_file_extension = True
    scene.view_settings.look = "AgX - Medium High Contrast"

    world = bpy.data.worlds.new("NeutralWorld") if not scene.world else scene.world
    scene.world = world
    world.color = (0.035, 0.035, 0.035)

    camera_data = bpy.data.cameras.new("TurntableCamera")
    camera = bpy.data.objects.new("TurntableCamera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.lens = 55
    camera_data.ortho_scale = max(height * 1.23, width * 1.7)
    camera.location = (3.9, -6.2, 5.4)
    look_at(camera, target)

    add_area_light("Key", (-4.5, -5.5, 7.5), 900.0, 4.5, target)
    add_area_light("Fill", (4.0, -2.0, 4.0), 450.0, 5.0, target)
    add_area_light("Rim", (1.0, 5.0, 6.0), 650.0, 3.5, target)

    # The imported model's local forward axis is established by this full
    # turntable. Direction labels are finalized after visual comparison with
    # the classic D2TM atlas, not guessed from GLB metadata.
    for index, (direction, degrees) in enumerate(DIRECTIONS):
        root.rotation_euler[2] = math.radians(degrees)
        bpy.context.view_layer.update()
        scene.render.filepath = str((args.output / f"{index}_{direction}_{int(degrees):03d}.png").resolve())
        bpy.ops.render.render(write_still=True)

    print(f"Rendered {len(DIRECTIONS)} directions to {args.output}")


if __name__ == "__main__":
    main()
