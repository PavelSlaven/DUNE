Port step P12 (`codex-direct/P12/TASK-P12.md`): release packaging, workflows and the author gallery of the fork on the port, owner decisions R82 and R83.

- `.github/workflows/claude-code-review.yml` is removed (R82); the other three upstream workflows are unchanged.
- New `release.yml` (the fork's workflow on the SDL3 build): a `v*` tag or a manual run with a tag creates a draft release, builds Windows, Linux, macOS arm64 and x64, uploads the archives and publishes the draft when all jobs pass.
- `packaging/make_common_assets.sh` builds the common asset archive: HD packs, HD scenes, both campaigns, skirmish maps, the 22 music tracks, settings and `game.ini`; no classic packs, no saves.
- The Linux archive carries its SDL3 libraries in `lib/` and starts through `d2tm.sh`, so a player needs nothing from the package manager (SDL3 is not in the Ubuntu 24.04 repositories).
- Installation notes for the three systems, release notes, `THIRD_PARTY_ASSETS_RU.txt` with the port fonts (R83), the fork's `windowed.bat`.
- README opens with the fork introduction and the five fork screenshots; new screenshots of the port come with step P13 (R83).

Checks on servak: build exit 0, CTest 443/443, `check_p12.py` 17/17 (YAML of the workflow, archive names, dry packaging of Linux and macOS, the full common asset list, `ldd` of the Linux package resolving SDL3 inside `lib/`, the main menu started through `d2tm.sh` from the unpacked packages). Lead review: read check (11 places, all READ), the package list and the publish flow of the workflow checked. The release workflow itself runs on GitHub only with a tag, at the release step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
