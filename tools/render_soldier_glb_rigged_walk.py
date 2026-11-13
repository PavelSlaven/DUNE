#!/usr/bin/env python3
"""Create a minimal deterministic leg rig for the unrigged soldier GLB."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


DIRECTIONS = (
    ("E", 135.0), ("NE", 180.0), ("N", 225.0), ("NW", 270.0),
    ("W", 315.0), ("SW", 0.0), ("S", 45.0), ("SE", 90.0),
)
# thigh-left, shin-left, thigh-right, shin-right (degrees). The two passing
# poses deliberately differ so the four-frame loop never freezes or reverses.
PHASES = (
    (-11.0, 6.0, 11.0, 21.0),
    (-2.5, 21.0, 2.5, 5.0),
    (11.0, 21.0, -11.0, 6.0),
    (2.5, 5.0, -2.5, 21.0),
)


def parse_args() -> argparse.Namespace:
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(arguments)


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_light(name: str, location: tuple[float, float, float], energy: float, size: float, target: Vector) -> None:
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


def add_bone(armature: bpy.types.Armature, name: str, head: tuple[float, float, float], tail: tuple[float, float, float], parent=None):
    bone = armature.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    bone.parent = parent
    return bone


def build_leg_rig(meshes: list[bpy.types.Object], height: float) -> bpy.types.Object:
    armature_data = bpy.data.armatures.new("SoldierLegRig")
    armature = bpy.data.objects.new("SoldierLegRig", armature_data)
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    hip_z = height * 0.49
    knee_z = height * 0.27
    ankle_z = height * 0.075
    side_x = height * 0.075
    left_thigh = add_bone(armature_data, "Leg.L", (-side_x, 0, hip_z), (-side_x, 0, knee_z))
    add_bone(armature_data, "Shin.L", (-side_x, 0, knee_z), (-side_x, 0, ankle_z), left_thigh)
    right_thigh = add_bone(armature_data, "Leg.R", (side_x, 0, hip_z), (side_x, 0, knee_z))
    add_bone(armature_data, "Shin.R", (side_x, 0, knee_z), (side_x, 0, ankle_z), right_thigh)
    bpy.ops.object.mode_set(mode="OBJECT")

    for obj in meshes:
        modifier = obj.modifiers.new(name="SoldierLegRig", type="ARMATURE")
        modifier.object = armature
        groups = {name: obj.vertex_groups.new(name=name) for name in ("Leg.L", "Shin.L", "Leg.R", "Shin.R")}
        for vertex in obj.data.vertices:
            position = vertex.co
            if position.z >= hip_z or abs(position.x) < height * 0.018:
                continue
            prefix = "L" if position.x < 0 else "R"
            # Blend around the knee to avoid a rigid seam; the shin inherits
            # the thigh transform, so both segments form one continuous leg.
            blend = max(0.0, min(1.0, (position.z - height * 0.20) / (height * 0.12)))
            groups[f"Leg.{prefix}"].add([vertex.index], blend, "REPLACE")
            groups[f"Shin.{prefix}"].add([vertex.index], 1.0 - blend, "REPLACE")
    return armature


def pose(armature: bpy.types.Object, values: tuple[float, float, float, float]) -> None:
    for name, degrees in zip(("Leg.L", "Shin.L", "Leg.R", "Shin.R"), values):
        bone = armature.pose.bones[name]
        bone.rotation_mode = "XYZ"
        bone.rotation_euler = (math.radians(degrees), 0.0, 0.0)


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

    armature = build_leg_rig(meshes, height)
    root = bpy.data.objects.new("SoldierRoot", None)
    bpy.context.collection.objects.link(root)
    for obj in [*meshes, armature]:
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

    target = Vector((0, 0, height * 0.47))
    camera_data = bpy.data.cameras.new("WalkCamera")
    camera = bpy.data.objects.new("WalkCamera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = max(height * 1.23, width * 1.7)
    camera.location = (3.9, -6.2, 5.4)
    look_at(camera, target)
    add_light("Key", (-4.5, -5.5, 7.5), 900.0, 4.5, target)
    add_light("Fill", (4.0, -2.0, 4.0), 450.0, 5.0, target)
    add_light("Rim", (1.0, 5.0, 6.0), 650.0, 3.5, target)

    for row, values in enumerate(PHASES):
        pose(armature, values)
        for column, (direction, degrees) in enumerate(DIRECTIONS):
            root.rotation_euler[2] = math.radians(degrees)
            bpy.context.view_layer.update()
            scene.render.filepath = str((args.output / f"r{row}_c{column}_{direction}.png").resolve())
            bpy.ops.render.render(write_still=True)
    print(f"Rendered rigged 8x4 walk cycle to {args.output}")


if __name__ == "__main__":
    main()
