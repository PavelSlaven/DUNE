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
    "sdl_inter_hd4.dat": ["BMP_SELECT_HOUSE_SARDAUKAR", "ICON_POWER_LOW"],
    "sdl_mentat_hd4.dat": ["MENTATS"],
}
HEADERS = {
    "sdl_data_hd4.dat": "src/data/gfxdata.h",
    "sdl_inter_hd4.dat": "src/data/gfxinter.h",
    "sdl_mentat_hd4.dat": "src/include/gfxmentat.h",
    "sdl_world_hd4.dat": "src/include/gfxworld.h",
}
TAG_COUNTS = {
    "sdl_data_hd4.dat": 241,
    "sdl_inter_hd4.dat": 144,
    "sdl_mentat_hd4.dat": 51,
    "sdl_world_hd4.dat": 36,
    "scenes/hd4/sdl_harvest.dat": 12,
    "scenes/hd4/sdl_headqrts.dat": 4,
    "scenes/hd4/sdl_hitcftry.dat": 1,
    "scenes/hd4/sdl_hvyftry.dat": 6,
    "scenes/hd4/sdl_ix.dat": 1,
    "scenes/hd4/sdl_liteftry.dat": 13,
    "scenes/hd4/sdl_lose01.dat": 1,
    "scenes/hd4/sdl_lose02.dat": 1,
    "scenes/hd4/sdl_ltank.dat": 1,
    "scenes/hd4/sdl_palace.dat": 1,
    "scenes/hd4/sdl_platr.dat": 33,
    "scenes/hd4/sdl_plhar.dat": 33,
    "scenes/hd4/sdl_plord.dat": 33,
    "scenes/hd4/sdl_quad.dat": 1,
    "scenes/hd4/sdl_repair.dat": 1,
    "scenes/hd4/sdl_sardukar.dat": 1,
    "scenes/hd4/sdl_win01.dat": 1,
    "scenes/hd4/sdl_win02.dat": 1,
}
UNCHANGED_SHA256 = {
    "sdl_world_hd4.dat": "94cf42fef1a755cc36b3b70f34900b15f76f28a540a38b73f69483f41b311d68",
    "scenes/hd4/sdl_harvest.dat": "87398462d2e738f9343bebb0b2b69e98832dd4e4d9ca81bc87c0fcef6e7dbd19",
    "scenes/hd4/sdl_headqrts.dat": "f893d902ceb80952843ab43739a25e21f9789eb75a8ea354d0218102d1cd6e4d",
    "scenes/hd4/sdl_hitcftry.dat": "9b2ca9a432b1313d52d45dcd3de08852e8306905392304b4cd995cb806879c25",
    "scenes/hd4/sdl_hvyftry.dat": "b56005c4b3ed616305ae03a88e07a3eaa8ab93347676c54b954b229984d009e7",
    "scenes/hd4/sdl_ix.dat": "22ae115b4f82698918be5854746883ee1c37d34e5bb51d8c10a46e86fc6da6a6",
    "scenes/hd4/sdl_liteftry.dat": "c3890660336afd0682be8db93643335a21aef5400b469f7a4be9615a6bdc009a",
    "scenes/hd4/sdl_lose01.dat": "cbc146ec610a4223d3b16a5093dadc146697f2ad02035077afbc2affe3a126f2",
    "scenes/hd4/sdl_lose02.dat": "6c46803526ea53ce25aa726178e37022b23c6e86a1e1da3fa4680259b2d60b06",
    "scenes/hd4/sdl_ltank.dat": "9c060b4c305d22a3839c2ffa795fe7dd78c983467837fdbe3bcd6ab9e318cfac",
    "scenes/hd4/sdl_palace.dat": "e50eb56b354ea2642c4c5a3970ad6b2691202509c53e73725331e62b9158b219",
    "scenes/hd4/sdl_platr.dat": "4284d1f533fb903097d0f6d84b2b3ebb11731be88e52fe87cb30d58ebc281b27",
    "scenes/hd4/sdl_plhar.dat": "df80aac4f0baa69e0bbc600d0b6215a7a0f094de9affbd1138d5407fddb76f11",
    "scenes/hd4/sdl_plord.dat": "d4fac41206c0aefff0fabe56fe5a5526dc14c9e2f8d0acb1836cea4dd5491771",
    "scenes/hd4/sdl_quad.dat": "5c9adc9bc2f6e56cfb61e00652268fe829f307e627c704489eb91a3bddabfe0f",
    "scenes/hd4/sdl_repair.dat": "693ef09c89b194d20e6b9c10288e9b742f5fe784f9904230780692c93d9aa718",
    "scenes/hd4/sdl_sardukar.dat": "f0e7ca1cffa39dd8cdb4eb186d4887bb1685731ab133c6de83ff1b975d3a45e2",
    "scenes/hd4/sdl_win01.dat": "c00dda733ab180bd55204121a1ab00a0305fb2e333b5734db42671ee48818727",
    "scenes/hd4/sdl_win02.dat": "746c528816c599ee8f80b30d3b28111c6e343b442ab9d20e4f5e8dffd5b678e5",
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
