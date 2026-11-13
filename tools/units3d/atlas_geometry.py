from __future__ import annotations


SIEGE_ATLAS_NAMES = frozenset({
    "UNIT_SIEGEBASE",
    "UNIT_SIEGEBASE_SHADOW",
    "UNIT_SIEGETOP",
    "HM_UNIT_SIEGEBASE",
    "HM_UNIT_SIEGETOP",
})
SIEGE_SOURCE_SIZE = (1152, 152)
SIEGE_HD_SIZE = (1408, 176)


def _dimensions(size, label: str) -> tuple[int, int]:
    if (
        not isinstance(size, (tuple, list))
        or len(size) != 2
        or any(type(value) is not int or value <= 0 for value in size)
    ):
        raise ValueError(f"{label}: expected two positive integer dimensions")
    return size[0], size[1]


def validate_atlas_size(name: str, replacement_size, source_size) -> None:
    replacement = _dimensions(replacement_size, f"{name}: replacement size")
    source = _dimensions(source_size, f"{name}: source size")
    if replacement == source:
        return
    if (
        name in SIEGE_ATLAS_NAMES
        and replacement == SIEGE_HD_SIZE
        and source in {SIEGE_SOURCE_SIZE, SIEGE_HD_SIZE}
    ):
        return
    raise ValueError(
        f"{name}: atlas size {replacement[0]}x{replacement[1]} is not allowed "
        f"for source size {source[0]}x{source[1]}"
    )
