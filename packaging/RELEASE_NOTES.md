# DUNE RU/HD cross-platform release

This release contains the Dune II — The Maker RU/HD remaster for Windows,
Linux and macOS.

## Highlights in v0.8.0-ru-hd.7

- refreshed HD4-only presentation, including the main-menu cover, outcome
  screens, Mentat briefings and the compact command panel;
- Sangyo Russian interface font with corrected sizing and alignment;
- revised skirmish layout and shorter localized map names;
- updated launcher artwork, classic wall textures and normalized faction
  colors;
- in-mission game-speed control and improved music controls;
- fixed Starport order rendering, a deployment crash, and the Starport tab
  remaining available after the final Starport was destroyed.

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
