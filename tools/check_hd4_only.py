from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources" / "bin" / "data"
FORBIDDEN_PATHS = (
    DATA / "hd2",
    DATA / "scenes" / "hd2",
    DATA / "sdl_data_hd2.dat",
    DATA / "sdl_inter_hd2.dat",
    DATA / "sdl_world_hd2.dat",
    DATA / "sdl_mentat_hd2.dat",
)


def main() -> None:
    leftovers = [path for path in FORBIDDEN_PATHS if path.exists()]
    if leftovers:
        joined = "\n".join(str(path) for path in leftovers)
        raise AssertionError(f"HD2 shipping resources still exist:\n{joined}")

    settings = (DATA.parent / "settings.ini").read_text(encoding="utf-8")
    if "HD2_DATAFILE" in settings or "_hd2.dat" in settings:
        raise AssertionError("settings.ini still advertises HD2 resources")

    print("Shipping resources: HD4 only")


if __name__ == "__main__":
    main()
