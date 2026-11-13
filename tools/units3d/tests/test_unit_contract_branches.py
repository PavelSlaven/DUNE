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
    markdown_document,
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

    def _changed_unit_source_literals(self, hd_literal, non_hd_literal):
        original = (ROOT / 'src/gameobjects/units/cUnit.cpp').read_text(encoding='utf-8')
        hd_marker = 'destination.y += 24.0F;'
        non_hd_marker = 'visualY + 24,'
        self.assertEqual(original.count(hd_marker), 1)
        self.assertEqual(original.count(non_hd_marker), 1)
        changed = original.replace(hd_marker, f'destination.y += {hd_literal};')
        changed = changed.replace(non_hd_marker, f'visualY + {non_hd_literal},')
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

    def test_carryall_rejects_lower_hd_offset(self):
        source = self._changed_unit_source_literals(hd_literal='23', non_hd_literal='24')

        with self.assertRaisesRegex(ValueError, 'offsets differ'):
            parse_carryall_offset(source)

    def test_carryall_rejects_fractional_hd_offset(self):
        source = self._changed_unit_source_literals(hd_literal='24.5F', non_hd_literal='24')

        with self.assertRaisesRegex(ValueError, 'offsets differ'):
            parse_carryall_offset(source)

    def test_carryall_integral_float_literals_return_int(self):
        source = self._changed_unit_source_literals(hd_literal='24.0F', non_hd_literal='24.0F')

        offset, _ = parse_carryall_offset(source)

        self.assertEqual(offset, 24)
        self.assertIs(type(offset), int)

    def test_carryall_rejects_equal_fractional_offsets(self):
        source = self._changed_unit_source_literals(hd_literal='24.5F', non_hd_literal='24.5F')

        with self.assertRaisesRegex(ValueError, 'CARRYALL visualY offset'):
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

    def test_markdown_draw_order_keeps_all_unique_sources(self):
        source_lines = (20, 10, 30, 40, 50, 60)
        unique_references = [
            {'ref': f'src/gameobjects/units/cUnit.cpp:{line}', 'identifier': 'draw_order'}
            for line in source_lines
        ]
        sources = [
            unique_references[0], unique_references[1], unique_references[0],
            *unique_references[2:], unique_references[1],
        ]
        contract = {
            'entries': [],
            'draw_rules': {
                'draw_order': {'value': 'shadow, bitmap, top', 'sources': sources},
            },
            'light': {'buildings': [], 'excluded': []},
        }

        markdown = markdown_document(contract)
        row = next(line for line in markdown.splitlines() if line.startswith('| `draw_order` |'))
        expected_links = [
            f'[src/gameobjects/units/cUnit.cpp:{line}](../../src/gameobjects/units/cUnit.cpp#L{line})'
            for line in source_lines
        ]
        links = row.split(' | ')[-1].removesuffix(' |').split(', ')

        self.assertTrue(
            len(links) == len(set(links)),
            'Повторные ссылки должны быть исключены',
        )
        self.assertEqual(len(links), 6)
        self.assertEqual(links, expected_links)
        self.assertEqual(
            row,
            f'| `draw_order` | shadow, bitmap, top | {", ".join(expected_links)} |',
        )


if __name__ == '__main__':
    unittest.main()
