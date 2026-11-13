# DUNE RU/HD cross-platform release

This release contains the Dune II — The Maker RU/HD remaster for Windows,
Linux and macOS, built on SDL3.

## What's new in v0.8.0-ru-hd.11

- The remaster now runs on the current upstream engine (SDL3), with builds for
  Windows, Linux and macOS.
- The first start uses the monitor's native resolution in fullscreen. The
  Resolution setting opens a short list of sizes that fit the screen.
- The command bar matches the rest of the interface: icons drawn by the game
  (move, attack, repair wrench, unload, deploy, rally flag, release), hotkey
  letters and a tooltip with the name and key.
- Vehicles keep the same apparent size in all eight directions.
- New art for the Light Factory, the Radar and the mentat briefings.

## Installation

1. Download `DUNE-<version>-common-assets.zip`.
2. Download exactly one platform archive:
   - `windows-x64.zip` for 64-bit Windows;
   - `linux-x64.tar.gz` for 64-bit Linux;
   - `macos-arm64.tar.gz` for Apple Silicon;
   - `macos-x64.tar.gz` for Intel Macs.
3. Extract both archives into the same empty directory.
4. Read `INSTALL.txt` from the platform archive and start `d2tm`/`d2tm.exe`.

The common archive includes the bilingual campaigns, HD4 graphics, fonts and
the 22 music tracks in the `music` folder. Existing `settings.ini`, `music`
and `saves` directories should be backed up before updating an older
installation. The game creates the `saves` folder next to itself. Saved games
from releases that predate this SDL3 build are not compatible: the game
lists them as damaged slots.

Windows binaries are portable and include their runtime DLLs. Linux targets
Ubuntu 24.04 or compatible distributions and includes the SDL3 libraries it
needs, started through `d2tm.sh`. macOS targets macOS 15+, requires SDL3 from
Homebrew, and is currently unsigned and not notarized.

Source builds require Git LFS.
