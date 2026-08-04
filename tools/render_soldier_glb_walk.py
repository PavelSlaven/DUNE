#!/usr/bin/env python3
"""Synthesize a stable four-phase D2TM walk cycle from an unrigged GLB.

Only vertices below the hips are moved. The torso, hands and weapon therefore
remain bit-for-bit identical (apart from object rotation) in every phase.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


# D2TM's atlas order. The GLB faces the camera at +45 degrees, so these root
# rotations map its actual facing to the engine directions without mirroring.
DIRECTIONS = (
    ("E", 135.0),
    ("NE", 180.0),
    ("N", 225.0),
    ("NW", 270.0),
    ("W", 315.0),
    ("SW", 0.0),
    ("S", 45.0),
    ("SE", 90.0),
)
PHASES = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)


def parse_args() -> argparse.Namespace:
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(arguments)


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


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


def bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    return (
        Vector(tuple(min(point[axis] for point in points) for axis in range(3))),
        Vector(tuple(max(point[axis] for point in points) for axis in range(3))),
    )


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def deform_walk(
    meshes: list[bpy.types.Object],
    originals: dict[str, list[Vector]],
    phase: float,
    height: float,
) -> None:
    hip = height * 0.50
    full_weight = height * 0.33
    stride = height * 0.052
    lift = height * 0.024
    left_forward = math.sin(phase)
    right_forward = -left_forward
    left_lift = max(0.0, math.cos(phase))
    right_lift = max(0.0, -math.cos(phase))

    for obj in meshes:
        source = originals[obj.name]
        for vertex, base in zip(obj.data.vertices, source):
            result = base.copy()
            if base.z < hip:
                weight = smoothstep((hip - base.z) / max(0.001, hip - full_weight))
                if base.x <= 0.0:
                    result.y += stride * left_forward * weight
                    result.z += lift * left_lift * weight
                else:
                    result.y += stride * right_forward * weight
                    result.z += lift * right_lift * weight
            vertex.co = result
        obj.data.update()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(args.model.resolve()))
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not meshes:
        raise RuntimeError("GLB contains no mesh objects")

    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    minimum, maximum = bounds(meshes)
    offset = Vector((-(minimum.x + maximum.x) / 2, -(minimum.y + maximum.y) / 2, -minimum.z))
    for obj in meshes:
        obj.location += offset
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    bpy.context.view_layer.update()

    minimum, maximum = bounds(meshes)
    height = maximum.z - minimum.z
    width = max(maximum.x - minimum.x, maximum.y - minimum.y)
    target = Vector((0.0, 0.0, height * 0.47))
    originals = {
        obj.name: [vertex.co.copy() for vertex in obj.data.vertices]
        for obj in meshes
    }

    root = bpy.data.objects.new("SoldierWalkRoot", None)
    bpy.context.collection.objects.link(root)
    for obj in meshes:
        obj.parent = root

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = True
    scene.view_settings.look = "AgX - Medium High Contrast"
    world = bpy.data.worlds.new("NeutralWorld") if not scene.world else scene.world
    scene.world = world
    world.color = (0.035, 0.035, 0.035)

    camera_data = bpy.data.cameras.new("WalkCamera")
    camera = bpy.data.objects.new("WalkCamera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = max(height * 1.23, width * 1.7)
    camera.location = (3.9, -6.2, 5.4)
    look_at(camera, target)

    add_area_light("Key", (-4.5, -5.5, 7.5), 900.0, 4.5, target)
    add_area_light("Fill", (4.0, -2.0, 4.0), 450.0, 5.0, target)
    add_area_light("Rim", (1.0, 5.0, 6.0), 650.0, 3.5, target)

    for row, phase in enumerate(PHASES):
        deform_walk(meshes, originals, phase, height)
        for column, (direction, degrees) in enumerate(DIRECTIONS):
            root.rotation_euler[2] = math.radians(degrees)
            bpy.context.view_layer.update()
            scene.render.filepath = str(
                (args.output / f"r{row}_c{column}_{direction}.png").resolve()
            )
            bpy.ops.render.render(write_still=True)

    print(f"Rendered 8x4 walk cycle to {args.output}")


if __name__ == "__main__":
    main()
