### git grep -n -i -E 'editor|scoring|video' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src/main.cpp src/game src/utils

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -i -E 'editor|scoring|video' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src/main.cpp src/game src/utils
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/ScenarioFlow.hpp:33:    ScenarioFlow(Callback setupPlayers, Callback loadScenario, IntCallback loadMapFromEditor, PlayerCallback setPlayerToInteractFor)
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/ScenarioFlow.hpp:36:          m_loadMapFromEditor(std::move(loadMapFromEditor)),
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/ScenarioFlow.hpp:48:    void loadMapFromEditor(int iSkirmishMap) const {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/ScenarioFlow.hpp:49:        m_loadMapFromEditor(iSkirmishMap);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/ScenarioFlow.hpp:59:    IntCallback m_loadMapFromEditor;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/VideoFlow.hpp:2: * @file VideoFlow.hpp
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/VideoFlow.hpp:23: * Narrow entry point to playing a video (a .pak file with frames), from anywhere in the game.
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/VideoFlow.hpp:26:class VideoFlow {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/VideoFlow.hpp:30:    explicit VideoFlow(PlayCallback play)
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame.h:72:class VideoFlow;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame.h:175:    void loadMapFromEditor(int map);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame.h:263:    std::unique_ptr<VideoFlow> m_videoFlow;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:28:#include "game/VideoFlow.hpp"
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:54:#include "gamestates/cEditorState.h"
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:58:#include "gamestates/cNewMapEditorState.h"
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:65:#include "gamestates/cVideoState.h"
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:235:    m_videoFlow = std::make_unique<VideoFlow>(
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:237:            m_creatorState->createVideoState(filename);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:238:            setNextStateToTransitionTo(GAME_VIDEO);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:269:            loadMapFromEditor(iSkirmishMap);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:291:    m_services->videoFlow = m_videoFlow.get();
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:736:        m_transfertMap[eGameDirFileName::GFXEDITOR] = settings->getStringValue("DATAFILE", "GFXEDITOR");
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:961:            case GAME_EDITOR: mapped = eGameState::EDITOR; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:967:            case GAME_SCORING: mapped = eGameState::SCORING; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:974:            case GAME_NEW_MAP_EDITOR: mapped = eGameState::NEW_MAP_EDITOR; return true;
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:990:                               newState != GAME_EDITOR &&
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1144:            else if (newState == GAME_EDITOR) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1145:                newStatePtr = m_creatorState->getState(eGameState::EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1147:            else if (newState == GAME_VIDEO) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1148:                newStatePtr = m_creatorState->getState(eGameState::VIDEO);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1155:            else if (newState == GAME_NEW_MAP_EDITOR) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1156:                newStatePtr = m_creatorState->getState(eGameState::NEW_MAP_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1204:            else if (newState == GAME_SCORING) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1205:                newStatePtr = m_creatorState->getState(eGameState::SCORING);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1733:void cGame::loadMapFromEditor(int map)
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1735:    setState(GAME_EDITOR);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cGame_logic.cpp:1736:    auto *pState = dynamic_cast<cEditorState*>(m_creatorState->getState(eGameState::EDITOR));
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cMissionStatsCollector.cpp:56:        // reading it live at scoring time would hide anyone the player actually beat.
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cSDLSystem.cpp:269:    if (!SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_EVENTS)) {
91416fb0c6aae877242d55e08559c32ec80de3e0:src/game/cSDLSystem.cpp:303:    SDL_SetHint(SDL_HINT_VIDEO_MAC_FULLSCREEN_SPACES, "0");
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/cFileValidator.h:31:    GFXEDITOR
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/cFileValidator.h:53:        case eGameDirFileName::GFXEDITOR:
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/cFileValidator.h:54:            return "GFXEDITOR";
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:31:#include "gameobjects/map/cMapEditor.h"
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:150:    auto mapEditor = cMapEditor(m_objects->getMap());
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:239:    mapEditor.smoothMap();
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:250:                mapEditor.createCell(cell, TERRAIN_BLOOM, 0);
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:260:                mapEditor.createRandomField(cell, TERRAIN_SPICE, 25 + (RNG::rnd(50)));
91416fb0c6aae877242d55e08559c32ec80de3e0:src/utils/ini.cpp:267:    mapEditor.smoothMap();
```
### git grep -n -E '\.(ogv|ogg|mp4|webm|avi|mkv|wsa|vqa)"' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git grep -n -E '\.(ogv|ogg|mp4|webm|avi|mkv|wsa|vqa)"' 91416fb0c6aae877242d55e08559c32ec80de3e0 -- src
91416fb0c6aae877242d55e08559c32ec80de3e0:src/context/MusicJukeBox.cpp:33:    return ext == ".ogg" || ext == ".mp3" || ext == ".wav" || ext == ".flac";
```
### git ls-tree -r --name-only 91416fb0c6aae877242d55e08559c32ec80de3e0 -- data | grep -i -E 'video|movie|scor|editor|\.(ogv|mp4|webm|wsa|vqa)$'

```text
$ export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
$ git ls-tree -r --name-only 91416fb0c6aae877242d55e08559c32ec80de3e0 -- data | grep -i -E 'video|movie|scor|editor|\.(ogv|mp4|webm|wsa|vqa)$'
пусто
```
