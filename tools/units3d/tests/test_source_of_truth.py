import json
import unittest
from pathlib import Path

from tools.units3d.redraw_common import REPO_PACK, load_unit
from tools.units3d.redraw_rotation import _block


ROOT = Path(__file__).resolve().parents[3]
SOURCE_OF_TRUTH = (
    "Источник истины — записи этого юнита в паке "
    "resources/bin/data/sdl_data_hd4.dat, принятые в игре (Р39, #60); "
    "пересборка из этого описания их не воспроизводит."
)
UNITS = ("UNIT_SIEGEBASE", "UNIT_HARVESTER", "UNIT_TANKTOP", "UNIT_SIEGETOP")


class SourceOfTruthTests(unittest.TestCase):
    def test_real_unit_descriptions_preserve_source_and_block(self):
        for name in UNITS:
            with self.subTest(unit=name):
                unit_path = ROOT / "tools/units3d/units" / name / "unit.json"
                description = json.loads(unit_path.read_text(encoding="utf-8"))
                unit = load_unit(unit_path.parent, "pack", REPO_PACK)

                self.assertEqual(unit.data["source_of_truth"], SOURCE_OF_TRUTH)
                self.assertEqual(_block(name), description["block"])


if __name__ == "__main__":
    unittest.main()
