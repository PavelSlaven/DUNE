import json
import re

FULL_RESOLUTIONS = ("1024x768", "1920x1080")
LANGUAGES = ("en",)
GRAPHICS = ("hd",)


def parse_scales(text):
    data = json.loads(text)
    return data["resolution"], list(data["render"]), list(data["world"])


def generate(scales):
    combos = []
    for resolution, available in scales.items():
        renders = [0] + list(available["render"])
        for language in LANGUAGES:
            for graphics in GRAPHICS:
                for render in renders:
                    combos.append(_combo(resolution, language, graphics, render, 0, "all"))
                if graphics == "hd":
                    for render in renders:
                        for world in available["world"]:
                            combos.append(_combo(resolution, language, graphics, render, world, "game"))
    return combos


def _combo(resolution, language, graphics, render, world, scope):
    return {"resolution": resolution, "language": language, "graphics": graphics,
            "render": render, "world": world, "scope": scope,
            "legacy": render == 0 and world == 0}


def combo_id(combo):
    base = f"{combo['resolution']}/{combo['language']}/{combo['graphics']}"
    if combo["legacy"]:
        return base
    return f"{base}/r{combo['render']}w{combo['world']}"


def legacy_combo(identifier):
    resolution, language, graphics = identifier.split("/")
    return _combo(resolution, language, graphics, 0, 0, "all")


def parse_id(identifier):
    parts = identifier.split("/")
    if len(parts) == 3:
        return legacy_combo(identifier)
    match = re.fullmatch(r"r(\d+)w(\d+)", parts[3])
    if len(parts) != 4 or not match:
        raise ValueError(f"bad combination id: {identifier}")
    render, world = int(match.group(1)), int(match.group(2))
    return _combo(parts[0], parts[1], parts[2], render, world, "game" if world else "all")


def scenes_for(combo, scenes):
    if combo["scope"] == "game":
        return [scene for scene in scenes if scene.get("game_screen")]
    return list(scenes)


def resolution_of(identifier):
    return identifier.split("/")[0]


def flag_key(flag):
    return (flag["scene"], flag["rule"], tuple(sorted(flag.get("names", []))))


def earlier_ids(ordered_ids, identifier):
    same = [item for item in ordered_ids if resolution_of(item) == resolution_of(identifier)]
    return same[:same.index(identifier)]


def first_combo_by_key(flags, ordered_ids):
    position = {item: number for number, item in enumerate(ordered_ids)}
    first = {}
    for flag in flags:
        key = (resolution_of(flag["combo"]), flag_key(flag))
        if key not in first or position[flag["combo"]] < position[first[key]]:
            first[key] = flag["combo"]
    return first


def png_required(flags, ordered_ids):
    first = first_combo_by_key(flags, ordered_ids)
    required = set()
    for flag in flags:
        legacy = flag["combo"].count("/") == 2
        if legacy or first[(resolution_of(flag["combo"]), flag_key(flag))] == flag["combo"]:
            required.add((flag["combo"], flag["scene"]))
    return required


def keep_png(combo, scene, flagged):
    if (combo_id(combo), scene["id"]) in flagged:
        return True
    return combo["legacy"] and (combo["resolution"] in FULL_RESOLUTIONS or bool(scene.get("hud")))
