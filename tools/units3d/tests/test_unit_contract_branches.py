import tempfile
import unittest
from pathlib import Path

from tools.units3d.unit_contract import (
    ROOT,
    SourceIndex,
    parse_angle_mapping,
    parse_carryall_offset,
    parse_density,
    parse_draw_geometry,
    parse_tile_dimensions,
)


class UnitContractBranchTests(unittest.TestCase):
    def _changed_unit_source(self, hd_offset, non_hd_offset):
        original = (ROOT / 'src/gameobjects/units/cUnit.cpp').read_text(encoding='utf-8')
        hd_marker = 'destination.y += 24.0F;'
        non_hd_marker = 'visualY + 24,'
        self.assertEqual(original.count(hd_marker), 1)
        self.assertEqual(original.count(non_hd_marker), 1)
        changed = original.replace(hd_marker, f'destination.y += {hd_offset}.0F;')
        changed = changed.replace(non_hd_marker, f'visualY + {non_hd_offset},')
        (ROOT / '.tmp').mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        unit_path = root / 'src/gameobjects/units/cUnit.cpp'
        unit_path.parent.mkdir(parents=True)
        unit_path.write_text(changed, encoding='utf-8')
        return SourceIndex(root)

    def test_carryall_offset_uses_non_hd_branch(self):
        source = self._changed_unit_source(hd_offset=31, non_hd_offset=31)
        offset, reference = parse_carryall_offset(source)

        self.assertEqual(offset, 31)
        self.assertEqual(reference['ref'].split(':')[0], 'src/gameobjects/units/cUnit.cpp')
        self.assertIn('visualY + 31', reference['identifier'])

    def test_carryall_offset_rejects_different_branches(self):
        source = self._changed_unit_source(hd_offset=31, non_hd_offset=24)

        with self.assertRaisesRegex(ValueError, 'offsets differ'):
            parse_carryall_offset(source)

    def test_draw_order_sources_cover_both_render_branches(self):
        source = SourceIndex(ROOT)
        density, density_rule = parse_density(source)
        tile, tile_refs = parse_tile_dimensions(source)
        _, direction_rule, _ = parse_angle_mapping(source)
        draw_geometry = parse_draw_geometry(
            source,
            density,
            density_rule,
            tile,
            tile_refs,
            direction_rule,
        )

        references = draw_geometry['draw_order']['sources']
        identifiers = [reference['identifier'] for reference in references]
        line_numbers = [int(reference['ref'].rsplit(':', 1)[1]) for reference in references]
        source_lines = source.search_lines('src/gameobjects/units/cUnit.cpp')
        self.assertEqual(len(identifiers), 6)
        self.assertEqual(
            identifiers,
            [
                'renderStrechSpriteF(', 'renderStrechSprite(',
                'renderStrechSpriteF(', 'renderStrechSprite(',
                'renderStrechSpriteF(', 'renderStrechSprite(',
            ],
        )
        self.assertEqual(line_numbers, sorted(line_numbers))
        self.assertEqual(
            [source_lines[line_number].strip() for line_number in line_numbers],
            ['shadow,', 'shadow,', 'bitmap,', 'bitmap,', 'top,', 'top,'],
        )


if __name__ == '__main__':
    unittest.main()
