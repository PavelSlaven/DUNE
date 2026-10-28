"""Render one unit from its 3D source into per-direction frames.

Run inside Blender:
  blender -b --factory-startup --python tools/units3d/render_unit.py -- --unit resources/hd/units3d/<key> --out <dir>

Behaviour is specified in docs/units/UNITS3D_SPEC.md.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

FORWARD_YAW = {'+X': 0.0, '-Y': 90.0, '-X': 180.0, '+Y': -90.0}
DIRECTION_YAW = [0, 45, 90, 135, 180, 225, 270, 315]
MARKER_COLORS = {'nose': (1.0, 0.0, 0.0), 'axis': (0.0, 1.0, 0.0), 'ring': (0.0, 0.0, 1.0)}
HOUSE_CAP = 2
# The barrel belongs to the turret but must not widen the hull cap, so the cap
# follows only turret vertices close to the ring height (model units).
RING_BAND = 0.03


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--elevation', type=float, help='overrides camera.json; for angle comparison sheets only')
    parser.add_argument('--directions', default='0,1,2,3,4,5,6,7')
    parser.add_argument('--passes', default='color,mask,markers,shadow')
    return parser.parse_args(sys.argv[sys.argv.index('--') + 1:])


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(point, selector):
    if selector['type'] == 'box':
        return all(selector['min'][i] <= point[i] <= selector['max'][i] for i in range(3))
    if selector['type'] == 'cylinder':
        dx = point.x - selector['center_xy'][0]
        dy = point.y - selector['center_xy'][1]
        return dx * dx + dy * dy <= selector['radius'] ** 2 and point.z >= selector['z_min']
    raise ValueError(f"unknown selector type {selector['type']}")


def load_model(path, forward, decimate):
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in bpy.context.scene.objects:
        o.select_set(o in meshes)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    world = obj.matrix_world.copy()
    obj.parent = None
    obj.data.transform(world)
    obj.matrix_world = Matrix()
    obj.data.transform(Matrix.Rotation(math.radians(FORWARD_YAW[forward]), 4, 'Z'))
    if decimate < 1.0:
        modifier = obj.modifiers.new('decimate', 'DECIMATE')
        modifier.ratio = decimate
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    for other in list(bpy.context.scene.objects):
        if other is not obj:
            bpy.data.objects.remove(other)
    return obj


def tag_faces(obj, unit):
    turret_selectors = unit.get('split', {}).get('turret', [])
    zones = unit.get('house_zones', [])
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    house = bm.faces.layers.int.new('house')
    turret = bm.faces.layers.int.new('turret')
    for face in bm.faces:
        center = face.calc_center_median()
        face[turret] = int(any(inside(center, s) for s in turret_selectors))
        face[house] = int(not zones or any(inside(center, s) for s in zones))
    bm.to_mesh(obj.data)
    bm.free()


def keep_faces(obj, turret_value):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    layer = bm.faces.layers.int['turret']
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f[layer] != turret_value], context='FACES')
    bm.to_mesh(obj.data)
    bm.free()


def convex_hull(points):
    pts = sorted(set(points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def srgb_to_linear(value):
    c = value / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def add_cap(obj, polygon, z, facing_up, color):
    material = bpy.data.materials.new('cap')
    material.use_nodes = True
    material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*map(srgb_to_linear, color), 1.0)
    material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
    obj.data.materials.append(material)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    ordered = polygon if facing_up else list(reversed(polygon))
    face = bm.faces.new([bm.verts.new((x, y, z)) for x, y in ordered])
    face.material_index = len(obj.data.materials) - 1
    # The cap shows wherever the turret turns away from the hull, so it carries the house colour like the paint around it.
    face[bm.faces.layers.int['house']] = HOUSE_CAP
    bm.to_mesh(obj.data)
    bm.free()


def split_turret(obj, cap_z, cap_color):
    turret = obj.copy()
    turret.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(turret)
    keep_faces(obj, 0)
    keep_faces(turret, 1)
    base_band = cap_z + RING_BAND
    footprint = convex_hull([(round(v.co.x, 4), round(v.co.y, 4)) for v in turret.data.vertices if v.co.z <= base_band])
    add_cap(obj, footprint, cap_z, True, cap_color)
    add_cap(turret, footprint, cap_z, False, cap_color)
    obj.name, turret.name = 'body', 'top'
    return turret


def vertices(objs):
    return np.array([v.co[:] for o in objs for v in o.data.vertices])


def screen_bbox(points, yaw_deg, theta_deg, pivot_height, frame, px_per_m):
    yaw, theta = math.radians(yaw_deg), math.radians(theta_deg)
    x = points[:, 0] * math.cos(yaw) - points[:, 1] * math.sin(yaw)
    y = points[:, 0] * math.sin(yaw) + points[:, 1] * math.cos(yaw)
    up = y * math.sin(theta) + (points[:, 2] - pivot_height) * math.cos(theta)
    px = frame[0] / 2 + x * px_per_m
    py = frame[1] / 2 - up * px_per_m
    return [round(float(v), 2) for v in (px.min(), py.min(), px.max(), py.max())]


def setup_scene(render_cfg, light_cfg, frame, supersample):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.seed = render_cfg['seed']
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.render.resolution_x = frame[0] * supersample
    scene.render.resolution_y = frame[1] * supersample
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'

    world = bpy.data.worlds.new('world')
    scene.world = world
    world.use_nodes = True
    background = world.node_tree.nodes['Background']
    background.inputs['Color'].default_value = (*light_cfg['ambient_color'], 1.0)
    background.inputs['Strength'].default_value = light_cfg['ambient_strength']

    azimuth = math.radians(light_cfg['sun_azimuth_deg'])
    elevation = math.radians(light_cfg['sun_elevation_deg'])
    toward_sun = Vector((math.cos(elevation) * math.cos(azimuth), math.cos(elevation) * math.sin(azimuth), math.sin(elevation)))
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
    sun.data.energy = light_cfg['sun_strength']
    sun.data.color = light_cfg['sun_color']
    sun.data.angle = math.radians(light_cfg.get('sun_angle_deg', 2.0))
    sun.rotation_euler = toward_sun.to_track_quat('Z', 'Y').to_euler()
    scene.collection.objects.link(sun)
    return scene


def setup_camera(scene, theta_deg, pivot_height, frame, px_per_m):
    theta = math.radians(theta_deg)
    cam = bpy.data.objects.new('camera', bpy.data.cameras.new('camera'))
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = max(frame) / px_per_m
    cam.data.sensor_fit = 'AUTO'
    target = Vector((0.0, 0.0, pivot_height))
    cam.location = target + Vector((0.0, -math.cos(theta), math.sin(theta))) * 100.0
    cam.rotation_euler = (math.pi / 2 - theta, 0.0, 0.0)
    cam.data.clip_end = 400.0
    scene.collection.objects.link(cam)
    scene.camera = cam


def emission_material(name, color):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = 1.0
    output = nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    return material


def holdout_material():
    material = bpy.data.materials.new('holdout')
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    holdout = nodes.new('ShaderNodeHoldout')
    output = nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(holdout.outputs['Holdout'], output.inputs['Surface'])
    return material


def paint_material(source, rule):
    bsdf = next(n for n in source.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    texture = bsdf.inputs['Base Color'].links[0].from_node
    # Thresholds are stated on the sRGB texels of the file, so sample them without the linear conversion.
    image = texture.image.copy()
    image.colorspace_settings.name = 'Non-Color'

    material = bpy.data.materials.new('mask_paint')
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()

    def node(kind, **inputs):
        n = tree.nodes.new(kind)
        for key, value in inputs.items():
            setattr(n, key, value)
        return n

    def math_node(operation, a, b):
        n = node('ShaderNodeMath', operation=operation)
        for socket, value in zip(n.inputs, (a, b)):
            if isinstance(value, float):
                socket.default_value = value
            else:
                tree.links.new(value, socket)
        return n.outputs[0]

    tex = node('ShaderNodeTexImage', image=image, interpolation=texture.interpolation)
    hsv = node('ShaderNodeSeparateColor', mode='HSV')
    tree.links.new(tex.outputs['Color'], hsv.inputs['Color'])
    offset = math_node('ABSOLUTE', math_node('SUBTRACT', hsv.outputs[0], rule['hue_deg'] / 360.0), 0.0)
    distance = math_node('MINIMUM', offset, math_node('SUBTRACT', 1.0, offset))
    in_hue = math_node('LESS_THAN', distance, rule['hue_width_deg'] / 360.0)
    saturated = math_node('GREATER_THAN', hsv.outputs[1], rule['min_saturation'])
    bright = math_node('GREATER_THAN', hsv.outputs[2], rule['min_value'])
    factor = math_node('MULTIPLY', math_node('MULTIPLY', in_hue, saturated), bright)

    emission = node('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    mix = node('ShaderNodeMixShader')
    tree.links.new(factor, mix.inputs['Fac'])
    tree.links.new(node('ShaderNodeHoldout').outputs['Holdout'], mix.inputs[1])
    tree.links.new(emission.outputs['Emission'], mix.inputs[2])
    tree.links.new(mix.outputs['Shader'], node('ShaderNodeOutputMaterial').inputs['Surface'])
    return material


def render_to(scene, path, samples, denoise):
    scene.cycles.samples = samples
    scene.cycles.use_denoising = denoise
    path.parent.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def load_pixels(path):
    image = bpy.data.images.load(str(path))
    w, h = image.size
    pixels = np.array(image.pixels[:], dtype=np.float32).reshape(h, w, 4)
    bpy.data.images.remove(image)
    return pixels


def save_pixels(pixels, path):
    h, w, _ = pixels.shape
    image = bpy.data.images.new(path.stem, w, h, alpha=True)
    image.pixels.foreach_set(pixels.ravel())
    image.filepath_raw = str(path)
    image.file_format = 'PNG'
    image.save()
    bpy.data.images.remove(image)


def main():
    args = parse_args()
    unit_dir = args.unit
    common = unit_dir.parent / 'common'
    unit = read_json(unit_dir / 'unit.json')
    camera_cfg = read_json(common / 'camera.json')
    light_cfg = read_json(common / 'light.json')
    render_cfg = read_json(common / 'render.json')
    if bpy.app.version_string.split()[0] != render_cfg['blender']:
        raise SystemExit(f"Blender {render_cfg['blender']} required, running {bpy.app.version_string}")
    theta = args.elevation if args.elevation is not None else camera_cfg['elevation_deg']
    px_per_m = camera_cfg['hd4_px_per_m']
    supersample = camera_cfg['supersample']
    frame = unit['frame_hd4']
    directions = [int(d) for d in args.directions.split(',')]
    passes = set(args.passes.split(','))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    model_path = unit_dir / unit['model']
    body = load_model(model_path, unit['forward'], unit.get('decimate', 1.0))
    tag_faces(body, unit)
    parts = {'body': body}
    cap_z = None
    if 'split' in unit:
        cap_z = unit['split']['cap_z']
        parts['top'] = split_turret(body, cap_z, unit['split']['cap_color'])

    pts = vertices(parts.values())
    scale = unit['length_m'] / (pts[:, 0].max() - pts[:, 0].min())
    pivot_x, pivot_y = unit['pivot_xy']
    to_world = Matrix.Scale(scale, 4) @ Matrix.Translation((-pivot_x, -pivot_y, -pts[:, 2].min()))
    for obj in parts.values():
        obj.data.transform(to_world)
    if cap_z is not None:
        cap_z = (cap_z - pts[:, 2].min()) * scale
    hull = vertices([body])
    pivot_height = unit['pivot_height_ratio'] * hull[:, 2].max()

    scene = setup_scene(render_cfg, light_cfg, frame, supersample)
    setup_camera(scene, theta, pivot_height, frame, px_per_m)

    marker_radius = 2.0 / (px_per_m * supersample)
    markers = {}
    for part_name, obj in parts.items():
        part_pts = vertices([obj])
        positions = {'nose': (part_pts[:, 0].max(), 0.0, pivot_height), 'axis': (0.0, 0.0, pivot_height)}
        if cap_z is not None:
            positions['ring'] = (0.0, 0.0, cap_z)
        for marker_name, location in positions.items():
            bpy.ops.mesh.primitive_uv_sphere_add(radius=marker_radius, location=location, segments=16, ring_count=8)
            sphere = bpy.context.active_object
            sphere.data.materials.append(emission_material(marker_name, MARKER_COLORS[marker_name]))
            sphere.hide_render = True
            markers[(part_name, marker_name)] = sphere

    turntable = bpy.data.objects.new('turntable', None)
    scene.collection.objects.link(turntable)
    for obj in list(parts.values()) + list(markers.values()):
        obj.parent = turntable

    catcher = None
    if 'shadow' in passes:
        bpy.ops.mesh.primitive_plane_add(size=200.0, location=(0.0, 0.0, 0.0))
        catcher = bpy.context.active_object
        catcher.is_shadow_catcher = True
        catcher.hide_render = True

    if 'house_paint' in unit:
        mask_white = paint_material(parts['body'].data.materials[0], unit['house_paint'])
    else:
        mask_white = emission_material('mask', (1.0, 1.0, 1.0))
    mask_holdout = holdout_material()
    mask_cap = emission_material('mask_cap', (1.0, 1.0, 1.0))
    out = args.out
    tmp = out / '_tmp'

    def show_only(visible):
        for obj in parts.values():
            obj.hide_render = obj not in visible
            obj.visible_camera = True
        for sphere in markers.values():
            sphere.hide_render = True
        if catcher is not None:
            catcher.hide_render = True

    for k in directions:
        turntable.rotation_euler = (0.0, 0.0, math.radians(DIRECTION_YAW[k]))
        for part_name, obj in parts.items():
            if 'color' in passes:
                show_only([obj])
                render_to(scene, out / part_name / f'color_{k}.png', render_cfg['samples'], render_cfg['denoise'])
            if 'mask' in passes and unit['parts'][part_name].get('mask'):
                show_only([obj])
                indices = np.zeros(len(obj.data.polygons), dtype=np.int32)
                obj.data.polygons.foreach_get('material_index', indices)
                house = np.zeros(len(obj.data.polygons), dtype=np.int32)
                obj.data.attributes['house'].data.foreach_get('value', house)
                base = len(obj.data.materials)
                obj.data.materials.append(mask_holdout)
                obj.data.materials.append(mask_white)
                obj.data.materials.append(mask_cap)
                obj.data.polygons.foreach_set('material_index', (base + house).astype(np.int32))
                obj.data.update()
                render_to(scene, out / part_name / f'mask_{k}.png', render_cfg['mask_samples'], False)
                obj.data.polygons.foreach_set('material_index', indices)
                obj.data.materials.pop()
                obj.data.materials.pop()
                obj.data.materials.pop()
                obj.data.update()
            if 'markers' in passes:
                show_only([])
                combined = None
                for channel, marker_name in enumerate(('nose', 'axis', 'ring')):
                    sphere = markers.get((part_name, marker_name))
                    if sphere is None:
                        continue
                    sphere.hide_render = False
                    render_to(scene, tmp / f'{part_name}_{marker_name}_{k}.png', render_cfg['mask_samples'], False)
                    sphere.hide_render = True
                    alpha = load_pixels(tmp / f'{part_name}_{marker_name}_{k}.png')[:, :, 3]
                    if combined is None:
                        combined = np.zeros(alpha.shape + (4,), dtype=np.float32)
                    combined[:, :, channel] = alpha
                combined[:, :, 3] = combined[:, :, :3].max(axis=2)
                save_pixels(combined, out / part_name / f'markers_{k}.png')
        if 'shadow' in passes and unit['parts']['body'].get('shadow'):
            show_only(list(parts.values()))
            for obj in parts.values():
                obj.visible_camera = False
            catcher.hide_render = False
            # Sky light would add an occlusion halo that spreads to the frame edges; the unit shadow is the sun's only.
            sky = scene.world.node_tree.nodes['Background'].inputs['Strength']
            sky_strength = sky.default_value
            sky.default_value = 0.0
            render_to(scene, out / 'body' / f'shadow_{k}.png', render_cfg['samples'], render_cfg['denoise'])
            sky.default_value = sky_strength

    model_files = {name: unit_dir.parent / 'common' / f'{name}.json' for name in ('camera', 'light', 'render')}
    manifest = {
        'blender': bpy.app.version_string,
        'elevation_deg': theta,
        'hd4_px_per_m': px_per_m,
        'supersample': supersample,
        'frame_hd4': frame,
        'model_scale': scale,
        'pivot_height_m': pivot_height,
        'cap_height_m': cap_z,
        'hull_screen_length_px': float((hull[:, 0].max() - hull[:, 0].min()) * px_per_m),
        'parts': sorted(parts),
        'directions': directions,
        'bbox_hd4': {
            name: {str(k): screen_bbox(vertices([obj]), DIRECTION_YAW[k], theta, pivot_height, frame, px_per_m) for k in directions}
            for name, obj in parts.items()
        },
        'hashes': {
            **{f'{name}.json': sha256(path) for name, path in model_files.items()},
            'unit.json': sha256(unit_dir / 'unit.json'),
            'model': sha256(model_path),
        },
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / 'render_manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')


main()
