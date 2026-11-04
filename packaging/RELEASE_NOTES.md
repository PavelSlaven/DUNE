# DUNE RU/HD cross-platform release

This release contains the Dune II — The Maker RU/HD remaster for Windows,
Linux and macOS.

## Highlights in v0.8.0-ru-hd.8

- redrawn vehicles and infantry for the 63 degree camera, with even sizes
  across all eight directions: Devastator, Tank, Siege tank, Launcher,
  infantry and squads;
- the Harvester redrawn from a 3D model and centred on the refinery pad;
- track marks under tanks, siege tanks and harvesters, dead infantry and
  squish sprites in HD, right-handed infantry in west-facing frames;
- concrete slabs drawn as thick plates at the building angle;
- the classic graphics mode is removed: the game always uses the HD4 pack;
- the world scale setting is now the starting camera zoom;
- reworked settings window, key rebinding that refuses occupied keys and
  tells Left Ctrl from Right Ctrl;
- HD layout fixes: the outcome screen prompt is centred on the image, the
  skirmish map size no longer overlaps the map name, top bar music controls
  make room for long messages, and two-line build list labels are aligned.

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
