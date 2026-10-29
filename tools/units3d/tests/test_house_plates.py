from __future__ import annotations

import math
import unittest

import numpy as np

from tools.units3d import house_plates


def strip(count):
    """Unit quads in a row along x; neighbours share an edge by vertex id."""
    loops = []
    for i in range(count):
        loops += [2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1]
    starts = np.arange(count, dtype=np.int64) * 4
    totals = np.full(count, 4, dtype=np.int64)
    return np.array(loops, dtype=np.int64), starts, totals


def tilted(degrees):
    return [math.sin(math.radians(degrees)), 0.0, math.cos(math.radians(degrees))]


def rule(angle, share, passes=0):
    return {'plate_angle_deg': angle, 'plate_min_share': share, 'smooth_passes': passes}


def plates(normals, painted=None, areas=None, **kwargs):
    loops, starts, totals = strip(len(normals))
    painted = np.ones(len(normals), bool) if painted is None else np.array(painted)
    areas = np.ones(len(normals)) if areas is None else np.array(areas, float)
    pairs = house_plates.face_pairs(loops, starts, totals)
    return house_plates.select_plates(painted, pairs, np.array(normals, float), areas, rule(**kwargs)).tolist()


class FacePairsTest(unittest.TestCase):
    def test_neighbours_in_a_strip(self):
        first, second = house_plates.face_pairs(*strip(3))
        self.assertEqual(sorted(map(sorted, zip(first.tolist(), second.tolist()))), [[0, 1], [1, 2]])

    def test_uv_seam_copies_are_welded(self):
        positions = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [1, 0, 0], [2, 0, 0], [2, 1, 0], [1, 1, 0]], float)
        loops = np.arange(8, dtype=np.int64)
        starts, totals = np.array([0, 4]), np.array([4, 4])
        self.assertEqual(len(house_plates.face_pairs(loops, starts, totals)[0]), 0)
        welded = house_plates.weld_ids(positions, 1e-5)
        first, second = house_plates.face_pairs(welded[loops], starts, totals)
        self.assertEqual(sorted([first.tolist()[0], second.tolist()[0]]), [0, 1])

    def test_weld_joins_one_rounding_cell_only(self):
        ids = house_plates.weld_ids(np.array([[0, 0, 0], [0.0002, 0, 0], [0.002, 0, 0]], float), 1e-3).tolist()
        self.assertEqual(ids[0], ids[1])
        self.assertNotEqual(ids[0], ids[2])

    def test_pairs_are_distinct_and_never_one_face(self):
        loops = np.array([0, 1, 0, 1, 1, 0, 2], dtype=np.int64)
        first, second = house_plates.face_pairs(loops, np.array([0, 4]), np.array([4, 3]))
        self.assertEqual(list(zip(first.tolist(), second.tolist())), [(0, 1)])

    def test_edge_of_three_faces_gives_all_pairs(self):
        loops = np.array([0, 1, 2, 1, 0, 3, 0, 1, 4], dtype=np.int64)
        first, second = house_plates.face_pairs(loops, np.array([0, 3, 6]), np.array([3, 3, 3]))
        self.assertEqual(sorted(map(sorted, zip(first.tolist(), second.tolist()))), [[0, 1], [0, 2], [1, 2]])


class FacePaintTest(unittest.TestCase):
    def test_mean_uv_picks_texel_with_row_zero_at_v_zero(self):
        paint = np.array([[True, False], [False, False]])
        uv = np.array([[0.2, 0.2], [0.3, 0.3], [0.7, 0.2], [0.8, 0.3], [0.2, 0.7], [0.3, 0.8], [1.2, 0.2], [1.3, 0.3]])
        starts, totals = np.array([0, 2, 4, 6]), np.array([2, 2, 2, 2])
        self.assertEqual(house_plates.face_paint(uv, starts, totals, paint).tolist(), [True, False, False, True])


class SelectPlatesTest(unittest.TestCase):
    def test_bend_sharper_than_plate_angle_splits_a_plate(self):
        normals = [tilted(0)] * 4 + [tilted(60)] * 2
        self.assertEqual(plates(normals, angle=35, share=0.4), [True] * 4 + [False] * 2)
        self.assertEqual(plates(normals, angle=70, share=0.4), [True] * 6)

    def test_small_painted_region_is_not_a_plate(self):
        normals = [tilted(0)] * 7
        painted = [True] * 5 + [False, True]
        self.assertEqual(plates(normals, painted, angle=35, share=0.2), [True] * 5 + [False, False])
        self.assertEqual(plates(normals, painted, angle=35, share=0.1), [True] * 5 + [False, True])

    def test_region_size_is_area_not_face_count(self):
        normals = [tilted(0)] * 2 + [tilted(60)] * 4
        areas = [5, 5, 1, 1, 1, 1]
        self.assertEqual(plates(normals, areas=areas, angle=35, share=0.5), [True] * 2 + [False] * 4)

    def test_smoothing_fills_a_detail_hole_inside_a_plate(self):
        normals = [tilted(0)] * 3 + [tilted(60)] + [tilted(0)] * 3
        self.assertEqual(plates(normals, angle=35, share=0.3, passes=0), [True] * 3 + [False] + [True] * 3)
        self.assertEqual(plates(normals, angle=35, share=0.3, passes=1), [True] * 7)

    def test_smoothing_votes_by_area(self):
        normals = [tilted(0)] * 3 + [tilted(60)] + [tilted(0)] * 3
        areas = [1, 1, 1, 2.5, 1, 1, 1]
        self.assertEqual(plates(normals, areas=areas, angle=35, share=0.3, passes=1), [True, True, False, False, False, True, True])

    def test_unpainted_face_never_becomes_a_plate(self):
        normals = [tilted(0)] * 5
        painted = [True, True, False, True, True]
        self.assertEqual(plates(normals, painted, angle=35, share=0.1, passes=3), [True, True, False, True, True])


if __name__ == '__main__':
    unittest.main()
