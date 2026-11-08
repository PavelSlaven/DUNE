# DUNE RU/HD cross-platform release

This release contains the Dune II — The Maker RU/HD remaster for Windows,
Linux and macOS.

## Highlights in v0.8.0-ru-hd.10

- new hand-drawn build-menu cards for buildings, units and Palace strikes;
  the Raider and the Trike share one card;
- the Barracks are redrawn as a military compound of flat-roofed blocks
  around an empty yard, and the WOR as a sandstone fortress with gate
  niches, round towers, a dome and a dish;
- every building flies the Spice Silo flag with the same pole, shadow,
  size and waving; the Command Post carries its flag at the lower right;
- the Spaceport and the High-Tech Factory reach every edge of their cells,
  and the High-Tech Factory's dark panels are now metal;
- the horizontal seam across concrete slabs is as thin as the vertical one;
- the Launcher hull is steel grey like the tanks instead of sand;
- the game engine is unchanged since v0.8.0-ru-hd.9, so its saved games
  still load; saves from older releases do not.

## Installation

1. Download `DUNE-<version>-common-assets.zip`.
2. Download exactly one platform archive:
   - `windows-x64.zip` for 64-bit Windows;
   - `linux-x64.tar.gz` for 64-bit Linux;
   - `macos-arm64.tar.gz` for Apple Silicon;
   - `macos-x64.tar.gz` for Intel Macs.
3. Extract both archives into the same empty directory.
4. Read `INSTALL.txt` from the platform archive and start `d2tm`/`d2tm.exe`.

The common archive includes the bilingual campaigns, HD4 graphics,
fonts and the refreshed music pools. Existing `settings.ini`, `music` and
`saves` directories should be backed up before updating an older installation.

Windows binaries are portable and include their runtime DLLs. Linux targets
Ubuntu 24.04 or compatible distributions and requires SDL2 packages from the
distribution. macOS targets macOS 15+, requires SDL2 from Homebrew, and is
currently unsigned and not notarized.

Source builds require Git LFS. See `README_AI.md` for architecture, build and
verification details.
