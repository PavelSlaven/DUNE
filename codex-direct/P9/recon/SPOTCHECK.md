| № | пункт | утверждение (кратко) | команда | вывод (до 2 строк) | совпало/не совпало |
|---|---|---|---|---|---|
| 1 | п.1 | категория BriefingAtreides, строка 16 enum | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.h \| sed -n '16p'` |     BriefingAtreides, | совпало |
| 2 | п.1 | клавиша [ (SDL_SCANCODE_LEFTBRACKET) в обработчике клавиш | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp \| sed -n '2105p'` |     if (event.hasKey(SDL_SCANCODE_LEFTBRACKET)) { | совпало |
| 3 | п.2 | Conquest: каталог music/conquest и MIDI_SCENARIO | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp \| sed -n '1148p'` |     m_musicController->configure(MusicCategory::Conquest, "music/conquest", {MIDI_SCENARIO}); | совпало |
| 4 | п.2 | каталог категории = m_gameDirectory / relativeDirectory | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.cpp \| sed -n '32p'` |     state.directory = m_gameDirectory / relativeDirectory; | совпало |
| 5 | п.3 | в cGame объявлен MusicController | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h \| sed -n '46p'` | class SaveGameManager; | не совпало |
| 6 | п.3 | вызов drawTopBarMusicControls в боевом состоянии | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp \| sed -n '89p'` |     drawTopBarMusicControls(); | совпало |
| 7 | п.4 | WIN → каталог win (repertoryDir) | `git -C C:/Users/Slaven/Projects/DUNE show 616280c8926ec642d86144a9fe2db105ceaf4061:src/context/MusicJukeBox.cpp \| sed -n '40p'` |     case eMusicType::WIN: return "win"; | совпало |
| 8 | п.4 | загрузка пользовательского аудио через MIX_LoadAudio_IO | `git -C C:/Users/Slaven/Projects/DUNE show 616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp \| sed -n '203p'` |     MIX_Audio *audio = MIX_LoadAudio_IO(m_mixer, io, false, true); | совпало |
| 9 | п.5 | CTest music_controls_layout_geometry | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt \| sed -n '431p'` |     add_test(NAME music_controls_layout_geometry COMMAND music_controls_layout_tests) | совпало |
| 10 | п.5 | assert(discovered.size() == 4U) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MusicPlaylistTests.cpp \| sed -n '58p'` |     assert(discovered.size() == 4U); | совпало |
| 11 | п.6 | playMusic по умолчанию true (GameSettings.hpp, 9208dcf) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/GameSettings.hpp \| sed -n '18p'` |     bool playMusic = true; | совпало |
| 12 | п.6 | customMusic по умолчанию false (InitialGameSettings.hpp, d06f2fc) | `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/utils/InitialGameSettings.hpp \| sed -n '34p'` |     bool customMusic = false; | совпало |
| 13 | п.2 | путей resources/bin с music-pools = 22 | `git show 62e1ff...:docs/upstream/port_inventory.json \| python -c '<подсчёт music-pools и resources/bin/>' \| wc -l` | 22 | совпало |
| 14 | п.4 | вызовов MIX_ в PORT (сумма git grep -c) = 33 | `git grep -c "MIX_" 616280c -- src \| сумма (отчёт: регулярка с '(' = 33)` | 60 | не совпало |
| 15 | п.5 | проверок в MusicPlaylistTests.cpp = 15 | `python count_checks.py (команда подсчёта из отчёта, локальный python), строка MusicPlaylistTests` | tests/MusicPlaylistTests.cpp: assertion_macro_calls=15; if_blocks=0; shouldAdvance_calls=0 | совпало |

Итог: 13 из 15 совпало.
