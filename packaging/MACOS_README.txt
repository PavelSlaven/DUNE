DUNE II — The Maker RU/HD — macOS
================================

This binary targets macOS 15 or newer.

1. Install Homebrew from https://brew.sh if it is not already installed.
2. Install the SDL2 runtime dependencies:

   brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer

3. Download the matching common-assets ZIP from the same GitHub Release.
4. Extract this archive and common-assets into the same empty directory.
5. Ensure the binary is executable and launch it from Terminal:

   chmod +x d2tm
   ./d2tm

Choose macos-arm64 for Apple Silicon or macos-x64 for an Intel Mac.

The application is not signed or notarized. If Gatekeeper blocks it, remove
the quarantine attribute only after verifying that it came from the official
PavelSlaven/DUNE release:

   xattr -d com.apple.quarantine d2tm

Back up settings.ini, music and saves before replacing an older installation.
