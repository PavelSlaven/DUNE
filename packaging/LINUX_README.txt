DUNE II — The Maker RU/HD — Linux x64
=====================================

This binary targets Ubuntu 24.04 or a compatible distribution with glibc 2.39
or newer.

1. Install the SDL2 runtime dependencies. On Debian/Ubuntu:

   sudo apt-get update
   sudo apt-get install libsdl2-2.0-0 libsdl2-image-2.0-0 \
     libsdl2-ttf-2.0-0 libsdl2-mixer-2.0-0

2. Download the matching common-assets ZIP from the same GitHub Release.
3. Extract this archive and common-assets into the same empty directory.
4. Ensure the binary is executable and launch it:

   chmod +x d2tm
   ./d2tm

Back up settings.ini, music and saves before replacing an older installation.
