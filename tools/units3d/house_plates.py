"""House-colour plates of a painted unit mesh (decision R18).

Pure numpy, so the selection is testable outside Blender: render_unit.py feeds it mesh arrays.
"""
import math

import numpy as np


def weld_ids(positions, tolerance):
    """Vertex ids that join copies of one position, so faces cut apart along UV seams stay neighbours."""
    _, ids = np.unique(np.round(positions / tolerance).astype(np.int64), axis=0, return_inverse=True)
    return ids.ravel()


def face_pairs(loop_vertices, loop_starts, loop_totals):
    """Pairs of faces that share an edge, by vertex id; an edge of n faces gives all n·(n − 1)/2 pairs."""
    face_of_loop = np.repeat(np.arange(len(loop_starts)), loop_totals)
    following = np.arange(len(loop_vertices)) + 1
    following[loop_starts + loop_totals - 1] = loop_starts
    a, b = loop_vertices, loop_vertices[following]
    key = np.minimum(a, b) * (int(loop_vertices.max()) + 1) + np.maximum(a, b)
    order = np.argsort(key, kind='stable')
    key, faces = key[order], face_of_loop[order]
    first, second = [faces[:0]], [faces[:0]]
    for step in range(1, len(key)):
        shared = key[step:] == key[:-step]
        if not shared.any():
            break
        first.append(faces[:-step][shared])
        second.append(faces[step:][shared])
    return np.concatenate(first), np.concatenate(second)


def face_paint(loop_uv, loop_starts, loop_totals, paint):
    """Paint class of the texel under each face's mean UV; paint is a (height, width) bool image, row 0 at v = 0."""
    height, width = paint.shape
    uv = np.add.reduceat(loop_uv, loop_starts) / loop_totals[:, None]
    x = np.floor(uv[:, 0] % 1.0 * width).astype(np.int64) % width
    y = np.floor(uv[:, 1] % 1.0 * height).astype(np.int64) % height
    return paint[y, x]


def select_plates(painted, pairs, normals, areas, rule):
    """Painted faces that keep the House colour: large smooth painted regions, then a few majority-vote passes."""
    first, second = pairs
    limit = math.cos(math.radians(rule['plate_angle_deg']))
    joined = painted[first] & painted[second] & ((normals[first] * normals[second]).sum(1) >= limit)
    parent = np.arange(len(painted))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, j in zip(first[joined].tolist(), second[joined].tolist()):
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            parent[root_i] = root_j
    roots = np.array([find(i) for i in range(len(painted))])
    painted_area = areas * painted
    region_area = np.bincount(roots, weights=painted_area, minlength=len(painted))
    plate = painted & (region_area[roots] >= rule['plate_min_share'] * painted_area.sum())
    for _ in range(rule['smooth_passes']):
        vote = np.where(plate, areas, -areas)
        score = vote.copy()
        np.add.at(score, first, vote[second] * painted[second])
        np.add.at(score, second, vote[first] * painted[first])
        plate = painted & (score > 0)
    return plate
