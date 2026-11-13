import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "resources/bin/data"
LFS_SIGNATURE = b"version https://git-lfs.github.com/spec/v1"
CLASSIC_WITHOUT_HD = {
    "sdl_data_hd4.dat": ["EXPLOSION_CARRYALL"],
    "sdl_inter_hd4.dat": ["BMP_SELECT_HOUSE_SARDAUKAR", "ICON_POWER_LOW"],
    "sdl_mentat_hd4.dat": ["MENTATS"],
    "sdl_gfxeditor.dat": [
        "BLOOM", "BUILDINGS", "FLIPHORZ", "FLIPVERT", "GRID", "LAYERS",
        "MOUNTAINS", "SANDLAYER", "SELECT", "SPICELAYER", "STONELAYER",
        "UNITS", "SOLDIERS", "TERRAN_HILL", "TERRAN_MOUNTAIN", "TERRAN_ROCK",
        "TERRAN_SAND", "TERRAN_SPICE", "TERRAN_SPICEHILL", "STARTPOSITION",
        "STARTPOSITION1", "STARTPOSITION2", "STARTPOSITION3", "STARTPOSITION4",
        "STARTPOSITION5", "FLIPHORZLR", "FLIPHORZRL", "FLIPVERTBT", "FLIPVERTTB",
        "FLIPDIAGBL", "FLIPDIAGBR", "FLIPDIAGTL", "FLIPDIAGTR", "SAVEICON",
    ],
}
HD_DRAWINGS = {
    "sdl_data_hd4.dat": ["EXPLOSION_CARRYALL"],
    "sdl_inter_hd4.dat": ["ICON_STR_LIGHTFACTORY", "ICON_STR_RADAR", "BMP_SELECT_HOUSE_SARDAUKAR", "ICON_POWER_LOW"],
    "sdl_mentat_hd4.dat": ["MENTATS"],
    "scenes/hd4/sdl_harvest.dat": ["01"],
    "scenes/hd4/sdl_headqrts.dat": ["01"],
    "scenes/hd4/sdl_hitcftry.dat": ["hitcftry 0001"],
    "scenes/hd4/sdl_hvyftry.dat": ["03"],
    "scenes/hd4/sdl_ix.dat": ["ix"],
    "scenes/hd4/sdl_liteftry.dat": ["11"],
    "scenes/hd4/sdl_lose01.dat": ["lose"],
    "scenes/hd4/sdl_lose02.dat": ["lose2"],
    "scenes/hd4/sdl_ltank.dat": ["mentat_tank"],
    "scenes/hd4/sdl_palace.dat": ["palace"],
    "scenes/hd4/sdl_platr.dat": ["01"],
    "scenes/hd4/sdl_plhar.dat": ["01"],
    "scenes/hd4/sdl_plord.dat": ["01"],
    "scenes/hd4/sdl_quad.dat": ["quad"],
    "scenes/hd4/sdl_repair.dat": ["repair_facillity"],
    "scenes/hd4/sdl_sardukar.dat": ["sardukar"],
    "scenes/hd4/sdl_win01.dat": ["WIN01"],
    "scenes/hd4/sdl_win02.dat": ["WIN02"],
}
HEADERS = {
    "sdl_data_hd4.dat": "src/data/gfxdata.h",
    "sdl_inter_hd4.dat": "src/data/gfxinter.h",
    "sdl_mentat_hd4.dat": "src/include/gfxmentat.h",
    "sdl_world_hd4.dat": "src/include/gfxworld.h",
}
TAG_COUNTS = {
    "sdl_data_hd4.dat": 241,
    "sdl_inter_hd4.dat": 142,
    "sdl_mentat_hd4.dat": 51,
    "sdl_world_hd4.dat": 36,
    "scenes/hd4/sdl_harvest.dat": 0,
    "scenes/hd4/sdl_headqrts.dat": 0,
    "scenes/hd4/sdl_hitcftry.dat": 0,
    "scenes/hd4/sdl_hvyftry.dat": 0,
    "scenes/hd4/sdl_ix.dat": 0,
    "scenes/hd4/sdl_liteftry.dat": 0,
    "scenes/hd4/sdl_lose01.dat": 0,
    "scenes/hd4/sdl_lose02.dat": 0,
    "scenes/hd4/sdl_ltank.dat": 0,
    "scenes/hd4/sdl_palace.dat": 0,
    "scenes/hd4/sdl_platr.dat": 0,
    "scenes/hd4/sdl_plhar.dat": 0,
    "scenes/hd4/sdl_plord.dat": 0,
    "scenes/hd4/sdl_quad.dat": 0,
    "scenes/hd4/sdl_repair.dat": 0,
    "scenes/hd4/sdl_sardukar.dat": 0,
    "scenes/hd4/sdl_win01.dat": 0,
    "scenes/hd4/sdl_win02.dat": 0,
}
UNCHANGED_SHA256 = {
    "sdl_world_hd4.dat": "94cf42fef1a755cc36b3b70f34900b15f76f28a540a38b73f69483f41b311d68",
    "scenes/hd4/sdl_harvest.dat": "0f589f76d1049f040fb8dc904bdaf56e61a436ad51706cb35d9695473df663e7",
    "scenes/hd4/sdl_headqrts.dat": "b2958f4002ff02fb1da7c123e25482fb3a94c411d247f3e8b3ba2bbca1af20e9",
    "scenes/hd4/sdl_hitcftry.dat": "2abba1a340b7858ecd013dc7ac79b3ca8cbf08e83461cc856056f6bfd9ad5f24",
    "scenes/hd4/sdl_hvyftry.dat": "d1961b32b7fe15db65e536ca1f36df6d3ada9c03490b8b3b725ef4042b52c108",
    "scenes/hd4/sdl_ix.dat": "d08d1553e470290bf236b5835a9ae170d0e9120161104547a015ca36d5c22a25",
    "scenes/hd4/sdl_liteftry.dat": "bb51d83003cf517095e1b64328c6371c65188cbf50925e167677c4b2684e62cf",
    "scenes/hd4/sdl_lose01.dat": "cc9aa0733c557d95bfd5b2875dbc200dd96de1ac8c03f8898973e60c1a443dda",
    "scenes/hd4/sdl_lose02.dat": "5bbeb3d3da82a5aac697ac43823261ff8637ea1b99e90c536331b81fde42a5f4",
    "scenes/hd4/sdl_ltank.dat": "8eb97e09592b638b2719284451ef6bdb27840755869dda96dcbded40ed0cf871",
    "scenes/hd4/sdl_palace.dat": "063a95756b14fbdc396add8520a55e5d30dc5685dc97306ac5d821e0e1a31053",
    "scenes/hd4/sdl_platr.dat": "51aa0d6f1f672413abeaceaf494b810ff28c5f13db54ac21d29bf0f5745e2e22",
    "scenes/hd4/sdl_plhar.dat": "e3f69d523fdec4d43cc41a3ed096733ef06d2056c7d900195d92fb7115322135",
    "scenes/hd4/sdl_plord.dat": "55e28f3979687ae9c6c0609237652713f349119aac1517596a5a0c040aed6e11",
    "scenes/hd4/sdl_quad.dat": "44ea8e832aac57f8b9425750a9b7383c5f6e2231968df2e0ae7e1dcbb549e2aa",
    "scenes/hd4/sdl_repair.dat": "6e048a8ae111b4f029c12aec6e86ca09d7d6f604dc09817e535e832ffaeaf352",
    "scenes/hd4/sdl_sardukar.dat": "3a496664f899c3ca2f577de1e5d0f72825667295dfacffe06c2fbf95e64e458d",
    "scenes/hd4/sdl_win01.dat": "faf84528681c93ae599335a92397751fc66ba64c58481c41523e0d5e3d24cc88",
    "scenes/hd4/sdl_win02.dat": "3c7f7e0c912305bef57ecea4c815d3508332983101e5b8a62d2ce84c9e02738e",
    "sdl_world.dat": "ebf869028eae8d477e03f368c8a4d5e7040c5b204a151386792fa61c9f77aaa3",
}


def read_expected(filename):
    groups = {}
    with (ROOT / "tests/data" / filename).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            groups.setdefault(row["pack"], []).append(row)
    return groups


def read_constants(path):
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*#define\s+(\w+)\s+(\d+)\b", line)
        if not match:
            match = re.match(
                r"^\s*(?:(?:inline|static)\s+)?constexpr\s+int\s+(\w+)\s*=\s*(\d+)\s*;",
                line,
            )
        if match:
            found.append((int(match[2]), match[1]))
    return sorted(found)


class PortPacksDataTests(unittest.TestCase):
    def require_pack(self, relative):
        path = DATA / relative
        self.assertTrue(path.is_file(), f"Нет файла пака: {path}")
        with path.open("rb") as stream:
            if stream.readline().rstrip(b"\r\n") == LFS_SIGNATURE:
                self.skipTest(f"Пак {relative} является указателем LFS; нужны настоящие данные")
        return path

    def test_classic_pack_entries(self):
        from tools import hd_assets
        expected = read_expected("classic_packs_expected.tsv")
        self.assertEqual(set(expected), {
            "sdl_audio.dat", "sdl_data.dat", "sdl_gfxeditor.dat",
            "sdl_inter.dat", "sdl_mentat.dat", "sdl_world.dat",
        })
        for pack, rows in expected.items():
            with self.subTest(pack=pack):
                entries = hd_assets.read_pack(self.require_pack(pack))
                actual = [(pack, str(e.index), e.name, e.extension,
                           hashlib.sha256(e.payload).hexdigest()) for e in entries]
                self.assertEqual(actual, [tuple(r[k] for k in
                    ("pack", "index", "name", "extension", "sha256")) for r in rows])

    def test_hd4_pack_entries(self):
        from tools import hd_assets
        expected = read_expected("hd4_packs_expected.tsv")
        self.assertEqual(set(expected), set(TAG_COUNTS))
        for pack, rows in expected.items():
            with self.subTest(pack=pack):
                entries = hd_assets.read_pack(self.require_pack(pack))
                self.assertEqual(len(entries), len(rows))
                self.assertEqual(sum(r["source"] == "fork" for r in rows), TAG_COUNTS[pack])
                self.assertEqual([r["name"] for r in rows if r["source"] == "hd_drawing"],
                                 HD_DRAWINGS.get(pack, []))
                for index, (entry, row) in enumerate(zip(entries, rows)):
                    with self.subTest(index=index, name=row["name"]):
                        self.assertEqual((entry.index, entry.name, entry.extension),
                                         (int(row["index"]), row["name"], row["extension"]))
                        self.assertEqual(entry.index, index)
                        with Image.open(io.BytesIO(entry.payload)) as image:
                            image.load()
                            self.assertEqual(image.size, (int(row["width"]), int(row["height"])))
                            if row["source"] in ("fork", "hd_drawing"):
                                self.assertEqual(hashlib.sha256(entry.payload).hexdigest(), row["sha256"])
                            else:
                                self.fail(f"Неизвестный источник: {row['source']}")

    def test_unchanged_pack_file_hashes(self):
        for pack, digest in UNCHANGED_SHA256.items():
            path = self.require_pack(pack)
            with self.subTest(pack=pack):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_upstream_constants_and_classic_without_hd_list(self):
        from tools import hd_assets
        for pack, header in HEADERS.items():
            with self.subTest(pack=pack):
                entries = hd_assets.read_pack(self.require_pack(pack))
                constants = read_constants(ROOT / header)
                self.assertTrue(constants, header)
                self.assertEqual([index for index, _ in constants], list(range(len(constants))))
                for index, name in constants:
                    self.assertEqual(entries[index].name, name, f"{pack}: индекс {index}")
        with (ROOT / "tools/upstream/classic_without_hd.json").open(encoding="utf-8") as stream:
            actual = json.load(stream)
        self.assertEqual(actual, CLASSIC_WITHOUT_HD)
        self.assertEqual(list(actual), list(CLASSIC_WITHOUT_HD))
        editor = read_constants(ROOT / "src/include/gfxeditor.h")
        self.assertTrue(editor)
        self.assertEqual([name for _, name in editor], actual["sdl_gfxeditor.dat"])

    def test_lfs_filter_attributes(self):
        classic = read_expected("classic_packs_expected.tsv")
        scene_paths = {pack.replace("scenes/hd4/", "scenes/")
                       for pack in TAG_COUNTS if pack.startswith("scenes/hd4/")}
        scene_paths.update(p.relative_to(DATA).as_posix()
                           for p in (DATA / "scenes").glob("sdl_*.dat"))
        paths = {pack: "lfs" for pack in TAG_COUNTS}
        paths.update({pack: None for pack in classic})
        paths.update({pack: None for pack in sorted(scene_paths)})
        for pack, expected_filter in paths.items():
            with self.subTest(pack=pack):
                self.require_pack(pack)
                relative = (Path("resources/bin/data") / pack).as_posix()
                result = subprocess.run(["git", "check-attr", "-z", "filter", "--", relative],
                                        cwd=ROOT, capture_output=True, check=True)
                fields = result.stdout.decode().split("\0")
                self.assertEqual(fields[:2], [relative, "filter"])
                if expected_filter == "lfs":
                    self.assertEqual(fields[2], "lfs")
                else:
                    self.assertNotEqual(fields[2], "lfs")


if __name__ == "__main__":
    unittest.main()
