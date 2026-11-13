Port step P11b (`codex-direct/P11/TASK-P11B.md`): mentat buttons without labels, found by the P13 comparison with the fork release (`codex-direct/P13/COMPARE.md`).

- The port kept the upstream mentat buttons: `WITH_TEXTURE` buttons at the classic positions, whose textures are empty in the fork's HD packs and which never draw their label. On the HD pictures the buttons looked like empty recesses, and the "join the House" question had no visible "Yes"/"No".
- Now every mentat (Atreides, Harkonnen, Ordos, Sardaukar, Bene Gesserit) places its two buttons in the recesses painted on the HD picture, with the fork's rectangles (`MentatHdButtons` in `MentatHdLayout.hpp`; Sardaukar use the Harkonnen frame), and draws the labels as text: "Repeat"/"Next" ("Повторить"/"Далее"), "No"/"Yes" ("Нет"/"Да"). Click handlers are unchanged. The scale of the mentat screen stays as it is (interface rework).
- Test: `[P11B]` in `tests/utils/test_MentatHdLayout.cpp`, 68 checks (fork rectangles, buttons inside the 640×480 frame, no overlap).

Checks on servak: build exit 0, CTest 569/569, `[P11B]` 68 assertions, the six mentat scenes (`mentat-briefing-atreides/ordos/harkonnen/sardaukar`, `mentat-win-ordos`, `tellhouse-ordos`) captured at 1920×1080, all ok. Lead review: the six shots viewed — every button sits in its recess with a readable label.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
