### git grep -n -E 'uiaudit::' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp src/gamestates/cScoringState.cpp src/gamestates/cWinLoseState.cpp src/gamestates/cVideoState.cpp

```text
git grep -n -E 'uiaudit::' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp src/gamestates/cScoringState.cpp src/gamestates/cWinLoseState.cpp src/gamestates/cVideoState.cpp
пусто
```

### git grep -n -E 'cScoringState|GAME_SCORING|GAME_EDITOR|GAME_NEW_MAP_EDITOR|cEditorState|cNewMapEditorState|outcome-win|outcome-lose' c5834615f8fc71789bba7108078a461018cc7d56 -- src/debug tools/ui-audit

```text
git grep -n -E 'cScoringState|GAME_SCORING|GAME_EDITOR|GAME_NEW_MAP_EDITOR|cEditorState|cNewMapEditorState|outcome-win|outcome-lose' c5834615f8fc71789bba7108078a461018cc7d56 -- src/debug tools/ui-audit
c5834615f8fc71789bba7108078a461018cc7d56:src/debug/UiAuditScenes.cpp:391:    withScreen(scene("outcome-win", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>,
c5834615f8fc71789bba7108078a461018cc7d56:src/debug/UiAuditScenes.cpp:393:    withScreen(scene("outcome-lose", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<false>,
```

