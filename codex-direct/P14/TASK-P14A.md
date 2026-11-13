# Задание P14A — догоняющий merge апстрима в ветку порта (шаг П14, часть а)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p14`, ветка `codex/p14`, `HEAD` — `6967cc72fe80be6a800829d2e2268aca293e66c7` (вершина ветки порта `port/up-d06f2fcd` после слияния П13, PR #146). В этой рабочей копии ведущий уже выполнил `git merge --no-ff --no-commit d7869e710fc5a91e8e217a3d387767428d82e07d`: слияние не завершено, файл `.git/MERGE_HEAD` содержит этот SHA, в 27 файлах стоят маркеры конфликта. Файлы Git LFS в рабочей копии — настоящие данные. Временные файлы — в `.tmp/p14a/`. Папка `.git` в песочнице только для чтения: ты только правишь файлы рабочего дерева. Команды `git add`, `git commit`, `git merge` (любой вариант), `git checkout`, `git restore`, `git stash`, `git reset` не выполняй: слияние фиксирует ведущий. Файлы задания лежат в папке `/srv/dune/tasks/p14a/` (дальше — «папка задания»).

## Цель

Рабочее дерево готово к фиксации слияния: в нём нет маркеров конфликта; код порта работает на устройстве апстрима `UP2` — звуки и музыка ищутся по имени через `AudioContext` и `SoundPool`, состояния игры — `enum class eGameState` и `GameStateMachine`, паки читаются по заголовку и имени. Игрок видит игру так же, как на `B14` (вершине порта до шага П13), и дополнительно получает всё, что принесли 48 коммитов апстрима; ни одна функция, добавленная шагами П2–П13 и решениями владельца, не пропадает и не меняется. Готово, когда зелёные проверки раздела «Проверки»: сборка и CTest, состав тестов, каталог из 192 сцен, 31 эталонный снимок, скрипты `tests/ui_audit/`, Python-тесты. Файлы, которые апстрим и порт изменили без конфликта (приложение Б), не правятся: их ветка кода остаётся такой, какой её собрал Git.

## Что уже решено

Ревизии (все — полные SHA):

- `B14` = `0683500a829556942723703183692b29be39d539` — вершина ветки порта после шагов П1–П12 (`git rev-parse 0683500a`). Шаг П13 добавил в порт только файлы `tools/ui-audit/reference_shots.py`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv`, `tools/ui-audit/tests/test_reference_shots.py`; проверка 0 это подтверждает. Тестов форка этот шаг не переносит.
- `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489` — апстрим, на котором построен порт; `git merge-base 0683500a d7869e710` даёт `UP1`.
- `UP2` = `d7869e710fc5a91e8e217a3d387767428d82e07d` — свежий master апстрима, 48 коммитов после `UP1` (`git log --oneline UP1..UP2`), 129 изменённых файлов (`git diff --stat UP1 UP2`).

Факты слияния (команда ведущего: `git merge-tree --write-tree --name-only --messages 0683500a d7869e710`, дерево результата `22d47aa4d10d94b50badf661c3fc08bb5335c946`): 27 файлов с конфликтом содержимого, 38 участков (hunks) с маркерами; ещё 41 файл изменили обе стороны, и Git слил их без конфликта. Номера строк в этом задании — строки файлов дерева `22d47aa4…`; в твоей рабочей копии эти файлы совпадают с ним до первой правки (скрипт `.tmp/p14a/check_hunks.py`, шаг 1 плана, это проверяет). Слово «дерево слияния» ниже — это оно.

Правило разрешения (решение ведущего):

1. Устройство кода — апстрима: новые механизмы `UP2` остаются целиком. Исключения — только участки, которые таблицы К2 и К3 называют явно (музыка в `AudioContext` и `cPlayer`); вне них правило действует без исключений.
2. Поведение порта — сохраняется целиком: всё, что добавили шаги П2–П13 и решения владельца (Р63–Р83), игрок видит так же, как на `B14`.
3. Точного текста разрешения для каждого участка в задании нет там, где участок велик: по каждому из 27 файлов дана строка таблицы К2 — что меняет апстрим, что добавил порт, как разрешить, чем проверено. Для коротких участков точный текст приведён под таблицей.
4. Где поведение порта нельзя сохранить на устройстве апстрима — блок `## Q-P14A-NN` и стоп; выбор — не твой.

Что нового у апстрима (механизмы `UP2`, ты их читаешь в разделе «Прочитать до работы»):

- Звук по имени: `AudioContext::indexOf(std::string_view)` (`UP2:src/context/AudioContext.hpp`), `AudioContext::playVoice(const SoundPool&, int house)`, `cSoundPlayer::getIndexFromName` и `cSoundPlayer::playVoice(int)` (`UP2:src/utils/cSoundPlayer.h`), пулы `soundpools::*` и `soundpools::resolve` (`UP2:src/data/SoundPools.h`), класс `SoundPool` и `resolveSoundIds` (`UP2:src/utils/SoundPool.hpp`). Файл `src/data/gfxaudio.h` удалён. Файла `src/data/Sounds.h` нет ни в `UP1`, ни в `UP2` (его добавил коммит e5c58d045 и удалил 4d233b5ab); порт на него не ссылается (`git grep -n 'Sounds\.h' 0683500a -- src tests tools` — пусто).
- Пак звуков `resources/bin/data/sdl_audio.dat` изменён апстримом: 108 записей стали 107, записи `MIDI_LOSE1..3` переименованы в `MIDI_LOSE01..03`, `SOUND_TANKDIE` — в `SOUND_TANKDIE1`, запись `SOUND_TANK` удалена (коммиты 8a3468304 и 4ba66a16b). Порт файл не менял (sha256 в `B14` и `UP1` один: `13de1e8711860babe01a5d4923fa4342ab73bd2e69b5693917df6a99d58ec25d`); после слияния sha256 файла — `601d2d109844ea2f22a1094bea2296bae17596941e368ae3f0ecf0c351b3dc29` (проверка 9).
- Пак: заголовок (автор и версия), поиск индекса по имени через `std::map`, `ReaderPack::getNames`, `getExtension`, `getText`; `DataPack::getNames`, `getText`; `Graphics::getNames` (`UP2:src/utils/cPack.h`, `cDataPack.hpp`, `Graphics.hpp`).
- Состояния игры: `enum class eGameState` без целочисленных констант `GAME_*`; `GameStateMachine`, `IStateCallbacks`, `IStateCreator` (`UP2:src/game/GameStateMachine.hpp`, `IStateCallbacks.hpp`, `IStateCreator.hpp`); `cGame` наследует `IStateCallbacks`; `std::optional<eGameState> m_nextState`; полей `m_state` и `m_currentState` в `cGame` нет — `m_stateMachine->getState()` и `m_stateMachine->getCurrentState()`. Строка журнала перехода теперь `Setting state from INITIALIZE to MENU` (`UP2:src/game/GameStateMachine.cpp:51-52`).
- Заголовки `cInputObserver.h`, `cScenarioObserver.h`, `cPlayerBrain.h`, `GameContext.hpp`, `cInfoContext.h` больше не подключают определения типов, а только объявляют их вперёд; конструктор `cInfoContextCreator` получил второй параметр `const AudioContext*`.
- Новые тесты Catch2: 92 случая в 11 файлах (список в разделе «Тесты»).

Звуки и музыка порта (решение 4 ведущего): порт не добавлял записей в `sdl_audio.dat` и не вводил своих имён звуков; музыка форка (Р79, коммит 33f028f2c) — файлы папки `music/` рядом с игрой, проигрывает `MusicController` (`src/audio/MusicController.h`); запись пака `MIDI_*` — запасной вариант, когда папка категории пуста. После слияния запасные записи ищутся по имени через `AudioContext::indexOf` и пулы `soundpools::ids::*` (точный текст — подраздел К2.2).

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом; пути без `/srv/` — от корня рабочей копии:

- `src/game/GameStateMachine.hpp` целиком;
- `src/game/GameStateMachine.cpp` целиком;
- `src/game/IStateCallbacks.hpp` целиком;
- `src/include/eGameState.h` целиком;
- `src/data/SoundPools.h` целиком;
- `src/utils/SoundPool.hpp` целиком;
- `src/context/AudioContext.hpp` целиком (с маркерами);
- `src/context/AudioContext.cpp` целиком (с маркерами);
- `src/audio/MusicController.h` целиком;
- `src/gamestates/cOptionsState.h` целиком (с маркерами);
- `src/debug/UiAudit.hpp` целиком;
- `tools/upstream/build_upstream_linux.sh` целиком;
- `tools/ui-audit/check_screens.py` целиком;
- `tools/ui-audit/tests/test_check_screens.py` целиком;
- `tools/upstream/tests/test_port_packs_data.py` целиком;
- `tests/CMakeLists.txt` целиком (с маркерами);
- вывод `git log --oneline d06f2fcd2a347182c3774fb96e9a85570405c489..d7869e710fc5a91e8e217a3d387767428d82e07d`;
- вывод `git diff d06f2fcd2a347182c3774fb96e9a85570405c489 d7869e710fc5a91e8e217a3d387767428d82e07d -- src/game/cGame.h src/game/cGame_logic.cpp` (читай по частям до конца: вывод длинный; обрезанный вывод — не чтение).

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт

Четыре пункта: К1 — общие правила разрешения; К2 — разрешение 27 файлов с конфликтом; К3 — правки в 9 файлах без конфликта; К4 — новый тестовый файл. Больше в дереве ничего не меняется.

### К1. Общие правила разрешения

1. **Маркеры.** Участок начинается строкой `<<<<<<< 0683500a829556942723703183692b29be39d539`, затем идёт «сторона порта», строка `=======`, «сторона апстрима» и строка `>>>>>>> upstream/master`. Три строки маркеров удаляются всегда; что остаётся между ними — по таблице К2.
2. **Состояния.** В `src/` и `tests/` не остаётся слов `GAME_INITIALIZE`, `GAME_OVER`, `GAME_MENU`, `GAME_PLAYING`, `GAME_BRIEFING`, `GAME_EDITOR`, `GAME_NEW_MAP_EDITOR`, `GAME_OPTIONS`, `GAME_REGION`, `GAME_SELECT_HOUSE`, `GAME_INTRO`, `GAME_TELLHOUSE`, `GAME_WINNING`, `GAME_SCORING`, `GAME_WINBRIEF`, `GAME_LOSEBRIEF`, `GAME_LOSING`, `GAME_SKIRMISH`, `GAME_SETUPSKIRMISH`, `GAME_CREDITS`, `GAME_MISSIONSELECT`, `GAME_VIDEO`, кроме двух мест: слов в комментариях `src/gamestates/cGameState.h` (18 строк) и слов в двойных кавычках в таблицах `src/debug/UiAuditScenes.cpp` (41 строка: строки каталога сцен вывода `--ui-audit-list`, поле `state`, они не меняются). Каждое слово `GAME_<ИМЯ>` в коде заменяется на `eGameState::<ИМЯ>` (то же `<ИМЯ>`). Параметры и поля состояния игры имеют тип `eGameState`, не `int`.
3. **Звуки.** Целочисленных констант `SOUND_*` и `MIDI_*` в коде порта нет (файл `gfxaudio.h` удалён). Одиночный звук: `m_audioContext->indexOf("<имя записи пака>")` один раз, результат хранится в поле класса (образец — `m_placeSound` в `src/controls/mousestates/cMousePlaceState.cpp`); вариации звука — `soundpools::<имя пула>`; голос — `m_audioContext->playVoice(<пул голоса>, <дом>)`.
4. **Подключения (`#include`).** Участок из одних `#include` разрешается так: сначала строки порта, потом строки апстрима, каждая строка один раз; подключение `#include "data/gfxaudio.h"` удаляется везде; подключение `#include "game/eScalingMode.h"` не добавляется: файла нет в порту (`git ls-tree 0683500a src/game/eScalingMode.h` — пусто, его удалил коммит 3840d3c62).
5. **Лямбды.** В новых лямбдах не захватывай константы с константным инициализатором (CI на macOS собирает clang с `-Werror`, `-Wunused-lambda-capture`; на servak clang нет).
6. **Каталог сцен.** Строки в двойных кавычках таблицы `kGroupScreens` в `src/debug/UiAuditScenes.cpp` остаются как есть: вывод `--ui-audit-list` (поле `state`, например `"GAME_MENU"`) проверяют скрипты `tests/ui_audit/` и их менять запрещено.
7. **Ничего сверх таблиц.** Никаких переформатирований, переименований, переносов кода и новых комментариев, кроме названных в К2–К4. Файлы приложения Б не правятся.
8. **Конструктор `AudioContext`.** Объект создаётся в `cGame::setupGame` строкой `auto audioContext = std::make_unique<AudioContext>(std::move(soundPlayer), m_gameSettings.get());` сразу после `std::make_unique<cSoundPlayer>(...)` (оба в одной функции): к моменту выполнения конструктора пак `sdl_audio.dat` загружен, и `indexOf` работает. Эту последовательность не менять.

### К2. Разрешение 27 файлов с конфликтом

Столбец «Апстрим» — коммиты `UP1..UP2`, столбец «Порт» — коммиты `UP1..B14` по `git log --oneline d06f2fcd..0683500a -- <файл>` (шаг плана порта в скобках). Столбец «Участки» — номера строк `<<<<<<<` в дереве слияния; `.tmp/p14a/check_hunks.py` проверяет их все. Тесты, названные в столбце «Сохранить / проверено», — файлы в `tests/`; сцены — скрипты `tests/ui_audit/`.

| № | Файл, участки | Апстрим | Порт | Разрешение | Сохранить / проверено |
|---|---|---|---|---|---|
| 1 | `src/building/cItemBuilder.cpp` (48) | f7eb85450: голос «Construction Complete» из `soundpools::voice01`; 0062ec059: `#include "controls/cKeyboardEvent.h"` | 0afcf180e (П8а: очереди площадок заводов); c106b54a2 (П7: локализация) | Участок 48: обе стороны подряд; итог — 3 строки `#include "utils/Localization.hpp"`, `#include "gameobjects/structures/cUnitFactory.h"`, `#include "controls/cKeyboardEvent.h"` | Очереди площадок заводов и локализация: `tests/structures/test_FactoryPad.cpp`, `test_FactoryPadEngine.cpp`, `tests/save/test_FactoryPadSave.cpp`, `tests/utils/test_Localization.cpp` |
| 2 | `src/context/AudioContext.cpp` (50, 172) | 1a8c335dd, e5c58d045, 47f19db51, 3d7b58437, 66d1564b9, f7eb85450, b2745a7b2, cc7d6c305, 4d233b5ab: идентификаторы по именам, `soundpools::resolve`, `indexOf`, `playVoice(const SoundPool&, house)`; выбор трека пулами и `MusicJukeBox` | 33f028f2c (П9, Р79): `MusicController`, 8 категорий музыки папок, запасные записи пака; `playMusicByType` вызывает `m_musicController->activate`; боевой темы нет | Участок 50: текст из подраздела К2.2. Участок 172: оставить сторону порта (одна строка `m_musicController->activate(...)`), сторону апстрима (выбор пула, `m_jukeBox`, `m_newMusic`, обратный отсчёт) удалить целиком | Те же 8 категорий и те же записи пака, что на `B14`: `tests/utils/test_MusicPlaylist.cpp`, `test_MusicTransitionPolicy.cpp`, `test_MusicControlsLayout.cpp`, `tests/controls/test_MusicKeyBindings.cpp`; сцена `game-music` |
| 3 | `src/context/AudioContext.hpp` (19, 71) | 1a8c335dd, f7eb85450: `indexOf`, `playVoice(const SoundPool&, int)`, поля `m_menuMusic` и им подобные, `m_jukeBox`, `m_newMusic` | 33f028f2c: поле `std::unique_ptr<MusicController> m_musicController;`, заголовки `<filesystem>`, `<optional>` | Участок 19: текст из К2.3. Участок 71: оставить сторону порта (1 строка), сторону апстрима (8 полей `m_jukeBox`…`m_newMusicCountdown`) удалить: класс порта их не использует | Сборка; тесты музыки из строки 2 |
| 4 | `src/controls/mousestates/cMousePlaceState.cpp` (93) | 85fbaf7a4: `resolveSounds`, `m_placeSound = indexOf("SOUND_PLACE")`; 4d233b5ab, 295e82f7e, 66d1564b9, faf5c9a7b | 25e0c7a02 (П8а: единое решение о постановке `s_PlaceResult`, `notifyPlacementFailure`); c106b54a2 (сообщение «Unable to create more.» на двух языках) | Участок 93: оставить сторону порта целиком, сторону апстрима удалить. Вне участка строку `m_context->getAudioContext()->playSound(SOUND_PLACE);` (дерево слияния, строка 123) заменить на `m_context->getAudioContext()->playSound(m_placeSound);` | `tests/players/test_PlacementRule.cpp`; причина отказа постановки видна игроку как на `B14` |
| 5 | `src/controls/mousestates/cMouseRepairState.cpp` (31) | 0062ec059: `#include "controls/sMouseEvent.h"`, `#include "controls/cKeyboardEvent.h"` | d820d85e4 (П10а: панель приказов): `#include "controls/CommandModePolicy.hpp"` | Участок 31: обе стороны подряд (3 строки `#include`) | `tests/controls/test_CommandPolicies.cpp`, `test_CommandKeys.cpp` |
| 6 | `src/controls/mousestates/cMouseUnitsSelectedState.cpp` (39) | 66d1564b9, 3d7b58437: пулы `soundpools::infantryAcknowledge.pick()`, `soundpools::vehicleAcknowledge.pick()`; 0062ec059: `#include "controls/cKeyboardEvent.h"` | d820d85e4 (П10а): `#include "controls/CommandModePolicy.hpp"` | Участок 39: обе стороны подряд (2 строки `#include`) | `tests/controls/test_CommandPolicies.cpp`, `test_MouseClickInit.cpp` |
| 7 | `src/drawers/CreditsDrawer.cpp` (32) | 295e82f7e, 66d1564b9, faf5c9a7b, 4d233b5ab: `indexOf("SOUND_CREDIT_UP")` и `indexOf("SOUND_CREDIT_DOWN")`; удалено `#include "data/gfxaudio.h"` | c106b54a2 (П7); 4aa980e36 (П5в: HD-панель кредитов); 81ccd38c1 (П3) | Участок 32: оставить две строки порта `#include "context/TextContext.hpp"` и `#include "sidebar/HudLayout.hpp"`; строку `#include "data/gfxaudio.h"` и маркеры удалить | `tests/drawers/test_CreditsMath.cpp`, `tests/utils/test_HudLayout.cpp`; анимация счёта и звук кредитов как на `B14` |
| 8 | `src/drawers/cBuildingListDrawer.cpp` (46) | 0062ec059: `#include "controls/cKeyboardEvent.h"` | 4aa980e36 (П5в: карточки списка построек); a1e63b860 (П7); c106b54a2 (П7); c5834615f (П5г); 81ccd38c1 (П3): `#include "utils/Localization.hpp"`, `#include "utils/Utf8.hpp"`, анонимное пространство имён с `fitWithEllipsis` и `compactCardName` | Участок 46: сторона порта целиком (строки 47–76 дерева слияния), затем строка апстрима `#include "controls/cKeyboardEvent.h"` | `tests/utils/test_HudLayout.cpp`, `test_Utf8.cpp`, `test_Localization.cpp`; сцены `game-*` |
| 9 | `src/game/cGame.h` (23, 96, 243) | 846a0750a, 94b54034c, eb43655ac: `IStateCallbacks`, `eGameState`, `GameStateMachine`, `m_nextState` как `std::optional` | 1dd771d7f (П8: `friend class SaveGameManager`, `SaveGameFlow`); acddd297b (П5г: `friend class UiAuditAccess`); 3840d3c62 (П4б: удалены `eScalingMode.h` и поле `m_scalingMode`); 87efa64f2 (П4: `ensureFrameTargets()`) | Участки 23, 96, 243: текст из К2.4 | Доступ `SaveGameManager` и `UiAuditAccess` к полям `cGame`; `ensureFrameTargets` вызывается как на `B14`; `tests/game/test_GameStateMachine.cpp` |
| 10 | `src/game/cGame_logic.cpp` (23, 121, 601) | 846a0750a (`GameStateMachine`, колбэки `onTransition*`), 94b54034c, 4fc37408f, f7eb85450, af9410978 | 13 коммитов: cf55f164f (П10в: клавиши игрока), 1dd771d7f (П8: `m_saveGameFlow`), d820d85e4 (П10а), 33f028f2c (П9), c106b54a2 (П7), f932e90c0 (П7: язык), dc6e5ffd7 (П5г: `setTerrainInfo` после `installInfos`), acddd297b (П5г), 4aa980e36 (П5в: `cSideBar::configureLayout`), bf929f742 (П5б), 3840d3c62, ce0cacfb3, 87efa64f2 (П4) | Участок 23: обе стороны подряд (`#include "debug/UiAudit.hpp"`, затем `#include "game/GameStateMachine.hpp"`). Участок 121: обе стороны подряд (6 строк). Участок 601: текст из К2.5. Вне участков (дерево слияния): строки 1459 и 1463 `isState(GAME_PLAYING)` → `isState(eGameState::PLAYING)` | Остаются как на `B14` (`0683500a:src/game/cGame_logic.cpp`): `ensureFrameTargets` (строки 606, 657, 678), `notificationY` над панелью приказов (593–597), `cSideBar::configureLayout` (824), `setTerrainInfo` после `installInfos` (899), чтение клавиш `Preferences::loadKeyBindings` (795), клавиши музыки только в бою (1593); `tests/controls/test_MusicKeyBindings.cpp`, `test_KeyRebinding.cpp`, `tests/utils/test_Preferences.cpp`; сохранения — `tests/save/*` |
| 11 | `src/gameobjects/mentat/AbstractMentat.cpp` (39) | 94b54034c; 0062ec059: `#include "controls/sMouseEvent.h"` | 91a9274b6 (П11: глаза и рот ментатов на HD-картинах); a1e63b860, c106b54a2 (П7); 389f01e17 (П5г); 81ccd38c1 (П3) | Участок 39: обе стороны подряд (4 строки порта, затем 1 строка апстрима) | `tests/utils/test_MentatHdLayout.cpp`, `test_MentatTextLayout.cpp`, `test_CampaignTextRu.cpp` |
| 12 | `src/gameobjects/mentat/BeneMentat.cpp` (33) | 94b54034c; 0062ec059: `#include "controls/cKeyboardEvent.h"` | 91a9274b6 (П11); c106b54a2 (П7): `#include "utils/Localization.hpp"` | Участок 33: обе стороны подряд (2 строки) | `tests/utils/test_MentatHdLayout.cpp`, `test_Localization.cpp` |
| 13 | `src/gameobjects/players/cPlayer.cpp` (2086) | 295e82f7e, faf5c9a7b, f7eb85450, 4d233b5ab: голоса из `soundpools::voice09`, `soundpools::voice10`, `m_reportingSound`, `m_yesSirSound` (в конструкторе, вне участка) | 33f028f2c (П9, Р79): при виде врага только голосовое предупреждение не чаще раза в 30 000 мс (`m_lastEnemyWarningMs`, `m_hasPlayedEnemyWarning`), боевой темы нет; 25e0c7a02 (П8а), c106b54a2 (П7), 78c3d3634 (П6), 81ccd38c1 (П3) | Участок 2086: оставить сторону порта целиком, сторону апстрима (запуск боевой музыки и выбор `voice`) удалить. Вне участка (дерево слияния, строка 2164) строку `m_audioContext->playVoice(pUnit->iType == SANDWORM ? SOUND_VOICE_10_ATR : SOUND_VOICE_09_ATR, getHouse());` заменить на `m_audioContext->playVoice(pUnit->iType == SANDWORM ? soundpools::voice10 : soundpools::voice09, getHouse());` | Предупреждение об обнаружении врага и его период — как на `B14` (`0683500a:src/gameobjects/players/cPlayer.cpp:2089-2096`); `tests/utils/test_MusicTransitionPolicy.cpp` |
| 14 | `src/gameobjects/players/cPlayer.h` (634) | 295e82f7e: `int m_reportingSound = -1;`, `int m_yesSirSound = -1;` | 33f028f2c (П9): `m_lastEnemyWarningMs`, `m_hasPlayedEnemyWarning`; 25e0c7a02, 1dd771d7f | Участок 634: обе стороны подряд (4 поля) | Сборка |
| 15 | `src/gamestates/cChooseHouseState.cpp` (34) | 94b54034c; 0062ec059: `#include "controls/cKeyboardEvent.h"`, `#include "controls/sMouseEvent.h"` | c106b54a2 (П7); 389f01e17 (П5г); e1d52ac10 (П5а: четыре карточки Домов): `debug/UiAudit.hpp`, `utils/HdUiTextureLoader.hpp`, `utils/Localization.hpp`, `<algorithm>`, `<string>` | Участок 34: обе стороны подряд (порт 5 строк `#include` с пустыми строками как в стороне порта, затем 2 строки апстрима) | `tests/utils/test_AdaptiveMenus.cpp`; сцены `choose-house-*` |
| 16 | `src/gamestates/cCreditsState.cpp` (36) | 94b54034c; 0062ec059: те же 2 строки | c106b54a2, 389f01e17, e1d52ac10: `debug/UiAudit.hpp`, `utils/Localization.hpp`, `<algorithm>` | Участок 36: обе стороны подряд | Сцены `credits-*`; `tests/utils/test_AdaptiveMenus.cpp` |
| 17 | `src/gamestates/cMainMenuState.cpp` (71) | 94b54034c: в старом теле конструктора `GAME_*` → `eGameState::*` | 1dd771d7f (П8: диалог сохранений `SaveSlotsDialog`); c106b54a2; 4b7743a36 (П5а); e1d52ac10 (П5а: `buildHdMenu()`) | Участок 71: оставить сторону порта (9 строк: `buildHdMenu();` и создание `m_saveDialog`), сторону апстрима (старое тело меню, 176 строк) удалить. Вне участка слова `GAME_SELECT_HOUSE`, `GAME_SETUPSKIRMISH`, `GAME_NEW_MAP_EDITOR`, `GAME_OPTIONS`, `GAME_CREDITS` (дерево слияния, строки 346, 350, 356, 359, 381) → `eGameState::<ИМЯ>` | Меню как на `B14`: `tests/utils/test_AdaptiveMenus.cpp`; сцены `main-menu`, `save-dialog-menu` |
| 18 | `src/gamestates/cOptionsState.cpp` (206) | 94b54034c: `eGameState` в конструкторе и в `constructWindow`, `setPrevState(eGameState)` | 4486bb741, cf55f164f (П10в: страницы настроек); 1dd771d7f (П8: кнопки «Сохранить/Загрузить игру»); c106b54a2, f932e90c0 (П7); bf929f742 (П5б); ce0cacfb3 (П4) | Участок 206: оставить сторону порта целиком, сторону апстрима (старая кнопка «Mission select») удалить. Все `GAME_PLAYING` и `GAME_MISSIONSELECT` в файле (дерево слияния, строки 121, 207, 240, 250) → `eGameState::PLAYING`, `eGameState::MISSIONSELECT` | Кнопки «Сохранить игру», «Загрузить игру», «Выбор миссии» и условие `m_prevState == eGameState::PLAYING && !m_settings->isSkirmish()` как на `B14`: `tests/utils/test_OptionsMenu.cpp`, `test_OptionPages.cpp`; сцены `options-menu-*`, `options-game-*` |
| 19 | `src/gamestates/cOptionsState.h` (49, 110) | 94b54034c: конструктор и `constructWindow` принимают `eGameState` | 4486bb741, f932e90c0, bf929f742, ce0cacfb3 (П10в, П7, П5б, П4): `enum class OptionsPage`, функции страниц, `Texture *const *m_backgroundTexture`; 389f01e17 (П5г) | Участки 49 и 110: текст из К2.6 | Страницы настроек: `tests/utils/test_OptionPages.cpp`; сборка |
| 20 | `src/gamestates/cScoringState.cpp` (19) | 94b54034c; 0062ec059: `#include "controls/sMouseEvent.h"` | c106b54a2 (П7): `#include "utils/Localization.hpp"` | Участок 19: обе стороны подряд (2 строки) | `tests/utils/test_Localization.cpp`; сцены `scoring-*` |
| 21 | `src/gamestates/cSelectYourNextConquestState.cpp` (348) | 94b54034c; 0062ec059: в комментарии `GAME_BRIEFING` → `eGameState::BRIEFING` | c106b54a2, 389f01e17 (П5г: запись клика `campaign-region-map`), e1d52ac10 (П5а), 81ccd38c1 | Участок 348: обе стороны подряд (4 строки блока `if (uiaudit::isEnabled() …)` порта, затем 5 строк комментария апстрима) | Сцены `region-*`; `tests/utils/test_AdaptiveMenus.cpp` |
| 22 | `src/managers/cDrawManager.cpp` (59, 403) | 94b54034c, 0062ec059 | d820d85e4 (П10а), 2ab045066 (П9: кнопки музыки и регулятор скорости), c106b54a2, c5834615f, af6a2e1e4 (П5г), 4aa980e36 (П5в: `drawTopBarBackground`, кнопка «OPTIONS»), e1d52ac10, 81ccd38c1 | Участок 59: обе стороны подряд (7 строк порта, затем `#include "controls/cKeyboardEvent.h"`). Участок 403: оставить сторону порта целиком (кнопки «<» «>», название трека, регулятор скорости), сторону апстрима (4 строки «HACK HACK» с `optionsRect`) удалить. Вне участка строку `m_stateTransitions->setNextState(GAME_OPTIONS);` (дерево слияния, строка 365) → `m_stateTransitions->setNextState(eGameState::OPTIONS);` | Кнопка «OPTIONS» в прямоугольнике `(7, 4, 126, 33)`, музыкальные кнопки и регулятор: сцены `game-music`, `game-*`; `tests/utils/test_HudLayout.cpp`, `tests/utils/test_MusicControlsLayout.cpp` |
| 23 | `src/utils/Graphics.cpp` (136) | b1e4c78e5: функция `Graphics::getNames()` | 78c3d3634 (П6), afe836b01 (П3) | Участок 136: сторона порта пустая, оставить сторону апстрима (функция `getNames`) | `tests/utils/test_Hd4Loading.cpp`, `test_FactionTintTerrain.cpp` |
| 24 | `src/utils/Graphics.hpp` (26, 57) | b1e4c78e5: `#include <vector>`, объявление `getNames()` | 78c3d3634, f3b41e2f5 (П4), afe836b01: `#include <utility>`, `getDensity()` | Участки 26 и 57: обе стороны подряд | `tests/utils/test_Hd4Loading.cpp`, `test_HdRender.cpp` |
| 25 | `src/utils/cDataPack.hpp` (64) | d7869e710, c40688519, b1e4c78e5: `int getIndexFromName(const std::string &name) const;`, `getText`, `getNames` (вне участка) | 78c3d3634 (П6): `getIndexFromSurface`, `getNameFromIndex` | Участок 64: текст из К2.7 | `tests/utils/test_Hd4Loading.cpp`, `test_FactionTintTerrain.cpp`, `test_cPack.cpp` |
| 26 | `src/utils/cPack.h` (52) | d7869e710, c5e2b3c4c, 06049c5e9, 409e13562, 7d4db36e8, aa4fb2ac0: `getNames`, `getExtension`, `getText`, заголовок пака | 78c3d3634 (П6): `std::string getNameFromIndex(int index) const;` | Участок 52: обе стороны подряд | `tests/utils/test_cPack.cpp`, `test_Hd4Loading.cpp` |
| 27 | `tests/CMakeLists.txt` (6, 49, 117) | 63dcfed47, 62fe57b3b, 8624c6271, 846a0750a: новые файлы тестов и источники | 20 коммитов порта (П2–П10в): перечни своих тестов и источников | Участки 6, 49 и 117: текст из К2.8 | Сборка; число тестов (раздел «Тесты») |

**К2.2. `src/context/AudioContext.cpp`, участок 50 (текст между маркерами заменяется ровно этим):**

```cpp
    m_settings(settings)
{
    d2tm_assert(m_soundPlayer != nullptr);
    d2tm_assert(m_settings != nullptr);
    const auto lookup = [this](std::string_view name) { return indexOf(name); };
    const int missing = soundpools::resolve(lookup);
    if (missing > 0) {
        Logger::error(COMP_SOUND, "AudioContext", "{} sound names not found in the audio pack", missing);
    }
    const std::filesystem::path gameDirectory = std::filesystem::current_path();
    struct MusicPool {
        MusicCategory category;
        const char *directory;
        std::vector<int> fallbackIds;
    };
    const std::array<MusicPool, 8> pools{{
        {MusicCategory::Gameplay, "music/gameplay",
         std::vector<int>(soundpools::ids::musicPeace.begin(), soundpools::ids::musicPeace.end())},
        {MusicCategory::Menu, "music/menu", {indexOf("MIDI_MENU")}},
        {MusicCategory::Conquest, "music/conquest", {indexOf("MIDI_SCENARIO")}},
        {MusicCategory::BriefingAtreides, "music/briefing/atreides", {indexOf("MIDI_MENTAT_ATR")}},
        {MusicCategory::BriefingHarkonnen, "music/briefing/harkonnen", {indexOf("MIDI_MENTAT_HAR")}},
        {MusicCategory::BriefingOrdos, "music/briefing/ordos", {indexOf("MIDI_MENTAT_ORD")}},
        {MusicCategory::Victory, "music/victory",
         std::vector<int>(soundpools::ids::musicWin.begin(), soundpools::ids::musicWin.end())},
        {MusicCategory::Defeat, "music/defeat",
         std::vector<int>(soundpools::ids::musicLose.begin(), soundpools::ids::musicLose.end())},
    }};
    for (const MusicPool &pool : pools) {
        std::error_code createError;
        std::filesystem::create_directories(gameDirectory / pool.directory, createError);
        if (createError) {
            Logger::warn(COMP_SOUND, "Music directory", "Could not create {}: {}",
                         (gameDirectory / pool.directory).string(), createError.message());
        }
    }
    m_musicController = std::make_unique<MusicController>(m_soundPlayer.get(), gameDirectory);
    for (const MusicPool &pool : pools) {
        m_musicController->configure(pool.category, pool.directory, pool.fallbackIds);
    }
```

(Строка `}` закрытия конструктора идёт после участка и остаётся.) Запасные записи категорий — те же мелодии, что на `B14`, под именами записей пака `UP2` (`0683500a:src/context/AudioContext.cpp:62-71`): музыка игры — `MIDI_BUILDING01..09`, победа — `MIDI_WIN01..03`, поражение — `MIDI_LOSE01..03`, меню `MIDI_MENU`, карта завоевания `MIDI_SCENARIO`, три записи брифингов `MIDI_MENTAT_ATR/HAR/ORD`; пулы `soundpools::ids::musicPeace`, `musicWin`, `musicLose` апстрима перечисляют именно эти имена (`UP2:src/data/SoundPools.h:25-32`).

**К2.3. `src/context/AudioContext.hpp`, участок 19 (заменяется ровно этим):**

```cpp
#include "utils/SoundPool.hpp"
#include <filesystem>
#include <optional>

#include <memory>
#include <string>
#include <string_view>
```

**К2.4. `src/game/cGame.h`.** Участок 23 заменяется двумя строками:

```cpp
#include "game/IStateCallbacks.hpp"
#include "include/eGameState.h"
```

Участок 96 заменяется тремя строками:

```cpp
class cGame : public cScenarioObserver, cInputObserver, IStateCallbacks {
    friend class UiAuditAccess;
    friend class SaveGameManager;
```

Участок 243 заменяется ровно этим:

```cpp
    void setState(eGameState newState);
    void ensureFrameTargets();

    // IStateCallbacks: the side effects of a state transition
    void onTransitionStarting(eGameState from, eGameState to) override;
    void playMusic(eMusicType musicType) override;
    void setCheatMode(bool enabled) override;
    void setMouseNormal() override;
    void takeBackgroundScreen() override;
    void onTransitionToPlaying(cGameState *state, bool isNew) override;
    void onTransitionToPlayingFromOptions() override;
    void onTransitionToOptions(bool fromPlaying) override;
    void onTransitionToOptionsExisting(cGameState *state, eGameState from) override;
    void onTransitionToRegionNew(cGameState *state) override;
    void onTransitionToRegionExisting(cGameState *state, bool fromWinLoseBrief) override;
    void onTransitionToSkirmish() override;
    void onEnteringTellHouse() override;
    void onEnteringLoseBrief() override;
```

**К2.5. `src/game/cGame_logic.cpp`, участок 601 (заменяется ровно этим):**

```cpp
    m_stateMachine->getCurrentState()->draw();
    int notificationY = m_gameSettings->getScreenH() - 64;
    if (isState(eGameState::PLAYING)) {
        notificationY = CommandBarLayout::create(m_gameSettings->getScreenW(), m_gameSettings->getScreenH(), cSideBar::SidebarWidth).panel.getY() - 18;
    }
    m_notificationArea->draw(m_textDrawer, 14, notificationY);
```

**К2.6. `src/gamestates/cOptionsState.h`.** Участок 49 заменяется ровно этим:

```cpp
    enum class OptionsPage { Main, Gameplay, Controls, Diagnostics };

    explicit cOptionsState(sGameServices* services, eGameState prevState);
```

Участок 110 заменяется ровно этим:

```cpp
    void constructWindow(eGameState prevState);
    void selectRenderScale(int step);
    void selectWorldScale(int step);
    void selectLanguage();
    void updateScaleControls();
    void applyScaleSettings();
    void selectResolution(int step);
    void loadSelectedOptions();
    void switchOptionsPage(OptionsPage page);
    void requestOptionsPage(OptionsPage page);
    void constructAdvancedWindow(eGameState prevState);
    void applyAdvancedPage();
    Texture *const *m_backgroundTexture = nullptr;
```

**К2.7. `src/utils/cDataPack.hpp`, участок 64 заменяется ровно этим:**

```cpp
    int getIndexFromName(const std::string &name) const;
    int getIndexFromSurface(const SDL_Surface *surface) const;
    std::string getNameFromIndex(int index) const;
```

**К2.8. `tests/CMakeLists.txt`.** Участок 6 заменяется десятью строками:

```cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_CommandKeys.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_CommandPolicies.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_MouseClickInit.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_cKeyboardEvent.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/drawers/test_CommandBarLayout.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/drawers/test_CreditsMath.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/game/test_GameStateMachine.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/game/test_cTimeCounter.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/gameobjects/test_cPlayerNotification.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/structures/test_StarportOrders.cpp
```

Участок 49: обе стороны подряд (23 строки порта, затем 6 строк апстрима). Участок 117 заменяется десятью строками:

```cmake
    ${CMAKE_SOURCE_DIR}/src/audio/MusicPlaylist.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/cDataPack.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/cFileValidator.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/cPack.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/Graphics.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/HouseMaskTint.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/RenderScale.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/ScaleChoices.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/HdUiTextureLoader.cpp
    ${CMAKE_SOURCE_DIR}/src/debug/UiAuditArguments.cpp
```

Строка `src/utils/cPack.cpp` в итоге ровно одна.

### К3. Правки в 9 файлах без конфликта

Эти девять файлов Git слил без маркеров, но после слияния они ссылаются на то, чего в `UP2` нет, или проверяют старый текст. Номера строк — дерево слияния.

| № | Файл | Что сделать |
|---|---|---|
| К3.1 | `src/debug/UiAudit.hpp` | После строки 3 `#include "debug/UiAuditArguments.hpp"` — строка `#include "include/eGameState.h"`. В строке 87 `static void setState(cGame &game, int state);` → `static void setState(cGame &game, eGameState state);` |
| К3.2 | `src/debug/UiAuditAccess.cpp` | После строки 3 `#include "game/cGame.h"` — строка `#include "game/GameStateMachine.hpp"`. Строка 93 `void UiAuditAccess::setState(cGame &currentGame, int state)` → `void UiAuditAccess::setState(cGame &currentGame, eGameState state)`. Каждое `currentGame.m_currentState` (строки 70, 75, 132, 139, 142, 170, 185, 195, 205, 216, 264, 288, 294, 300, 998, 1008, 1033) → `currentGame.m_stateMachine->getCurrentState()`. Каждое `currentGame.m_state ==` (строки 539, 551, 1044) → `currentGame.m_stateMachine->getState() ==`. Каждое `GAME_<ИМЯ>` (строки 126, 130, 169, 283, 344, 525, 527, 539, 551, 1044) → `eGameState::<ИМЯ>` |
| К3.3 | `src/debug/UiAuditScenes.cpp` | В вызовах `UiAuditAccess::setState(game, GAME_<ИМЯ>)` (строки 137, 146, 158, 164, 172, 181, 203, 212, 233, 255, 322, 356) `GAME_<ИМЯ>` → `eGameState::<ИМЯ>`. Строки в двойных кавычках таблицы `kGroupScreens` не меняются (К1.6) |
| К3.4 | `src/save/SaveGameManager.cpp` | Удалить строку 6 `#include "data/gfxaudio.h"`. Строки 779 и 782: `game.isState(GAME_PLAYING)`, `game.setNextStateToTransitionTo(GAME_PLAYING)` → `eGameState::PLAYING`. Строки 906–907: `!game.isState(GAME_PLAYING) && !game.isState(GAME_OPTIONS) && game.m_nextState != GAME_PLAYING` → те же выражения с `eGameState::PLAYING` и `eGameState::OPTIONS` (`m_nextState` теперь `std::optional<eGameState>`; сравнение `!= eGameState::PLAYING` корректно) |
| К3.5 | `src/gamestates/cOptionsPages.cpp` | Строка 27 `void cOptionsState::constructAdvancedWindow(int)` → `void cOptionsState::constructAdvancedWindow(eGameState)` |
| К3.6 | `src/gamestates/cWinLoseState.cpp` | После строки 35 `#include "context/GraphicsContext.hpp"` — строка `#include "context/TextContext.hpp"`: `GameContext.hpp` апстрима больше не подключает `TextContext.hpp` (`UP2:src/context/GameContext.hpp:20-21` — только объявления вперёд), а строка 42 `m_textDrawer(m_ctx->getTextContext()->getBeneTextDrawer()),` требует полного типа |
| К3.7 | `tools/ui-audit/check_screens.py` | Скрипт `tools/ui-audit/check_screens.py` читает имена состояний регулярным выражением `STATE_DEFINE` по целочисленным константам `GAME_*` в `src/include/eGameState.h`; их больше нет, а каталог сцен и `tools/ui-audit/exclusions.tsv` называют состояния прежними именами `GAME_*`. Правка (три вставки, `code_states` не меняется): после строки 7 `STATE_DEFINE = …` — строка `ENUM_STATES = re.compile(r"enum\s+class\s+eGameState\b[^{]*\{([^}]*)\}")`; перед строкой 17 `def code_classes(sources):` — функция из блока ниже с двумя пустыми строками после неё; строка 59 `states = code_states((root / "src/include/eGameState.h").read_text(encoding="utf-8", errors="replace"))` заменяется двумя строками из блока ниже |
| К3.8 | `tools/upstream/build_upstream_linux.sh` | Строка 13 `menu_text='Setting state from -1(=INITIALIZE) to 1(=MENU)'` → `menu_text='Setting state from INITIALIZE to MENU'` (так пишет `GameStateMachine::transitionTo`, `UP2:src/game/GameStateMachine.cpp:51-52`). Строка 261: `Источник: src/game/cGame_logic.cpp:945–946` → `Источник: src/game/GameStateMachine.cpp:51–52`. Аргумент скрипта остаётся `d06f2fcd2a347182c3774fb96e9a85570405c489`: проверка в строке 183 (`merge-base --is-ancestor`) требует предка `HEAD`, а `d7869e710…` предком `HEAD` станет только после коммита слияния |
| К3.9 | `tests/data/classic_packs_expected.tsv` | Строки пака `sdl_audio.dat` (в файле 108 строк подряд после заголовка) заменяются 107 строками из `resources/bin/data/sdl_audio.dat` скриптом приложения А (`.tmp/p14a/regen_audio_rows.py`); строки остальных пяти паков (436 строк) остаются байт в байт; окончания строк не меняются. Ожидаемый вывод скрипта: `audio_rows=107 other_rows=436` |

К3.7, функция и две строки:

```python
def code_enum_states(text):
    block = ENUM_STATES.search(re.sub(r"//[^\n]*", "", text))
    names = re.findall(r"\b([A-Z][A-Z0-9_]*)\b", block.group(1)) if block else []
    return ["GAME_MAX_STATES" if name == "COUNT" else "GAME_" + name for name in names]
```

```python
    header = (root / "src/include/eGameState.h").read_text(encoding="utf-8", errors="replace")
    states = code_states(header) + code_enum_states(header)
```

Имена `GAME_<ИМЯ>` из перечисления — те же 23 имени, что были константами (22 состояния и `GAME_MAX_STATES` для `COUNT`).

### К4. Новый тестовый файл

`tools/ui-audit/tests/test_check_screens_enum.py` — точный текст в приложении А (три теста). Существующие файлы `tools/ui-audit/tests/test_check_screens.py` и `test_port_changes.py`, `tools/ui-audit/exclusions.tsv`, `tools/ui-audit/keys.tsv` и скрипты `tests/ui_audit/` не меняются.

### Что не меняется

Файлы приложения Б (40 файлов, слитых без конфликта) не правятся. `docs/`, `README.md`, `.github/`, `packaging/`, `resources/` (кроме того, что слил Git) не трогаются. Файл `src/game/eScalingMode.h` не возвращается. Связывание истории (`merge -s ours`) и перемотка `main` — шаг П14б, не этот.

## Тесты

Тестов форка шаг не переносит. Новые тесты — три теста Python (К4); тесты C++ апстрима (92 случая) и порта приходят через слияние.

**Новые тесты `tools/ui-audit/tests/test_check_screens_enum.py` (класс `EnumStates`, тег — имя файла):**

1. `test_enumerators_get_the_old_constant_names`: `check_screens.code_enum_states` для текста перечисления из приложения А возвращает `["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES"]`; слова в комментарии `// GAME OVER` в результат не попадают.
2. `test_text_without_the_enum_gives_no_states`: для текста `enum class Other { A, B };` результат — пустой список.
3. `test_collect_code_names_reads_the_enum`: `collect_code_names` для временной папки с заголовком из приложения А, `cA.h`, `M.h` и `SaveSlotsDialog.hpp` возвращает `["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES", "M", "cA", "SaveSlotsDialog"]`.

**Красный прогон (шаг 2 плана) до правок кода; ожидаемые результаты измерены на дереве слияния `22d47aa4…`:**

- `grep` маркеров (проверка 2) выводит 114 строк (по 38 строк `<<<<<<< `, `=======`, `>>>>>>> `);
- `cd tools/ui-audit/tests && python3 -B -m unittest test_check_screens_enum` — `FAILED (failures=1, errors=2)`;
- `cd tools/ui-audit/tests && python3 -B -m unittest test_port_changes.PortChanges.test_g_exclusions_exist_in_port_code` — `FAILED (failures=6)` (имена `GAME_INTRO`, `GAME_OVER`, `GAME_INITIALIZE`, `GAME_MAX_STATES`, `GAME_SKIRMISH`, `GAME_VIDEO` отсутствуют в именах кода);
- `/srv/dune/venv/bin/python -B -m unittest tools.upstream.tests.test_port_packs_data.PortPacksDataTests.test_classic_pack_entries` из корня рабочей копии — `FAILED (failures=1)` (пак `sdl_audio.dat` из `UP2`, строки из `B14`);
- сборка с маркерами (первая команда проверки 1 с логом `.tmp/p14a/red-build.log`) — `exit` не `0`.

**Состав тестов C++ (`UP2` против `UP1`, скрипт `.tmp/p14a/check_tests.py`, подсчёт по `TEST_CASE` и `REQUIRE`/`CHECK`):**

| Файл (новый в апстриме) | Случаев | `REQUIRE`/`CHECK` |
|---|---|---|
| `tests/controls/test_cKeyboardEvent.cpp` | 10 | 40 |
| `tests/game/test_GameStateMachine.cpp` | 15 | 41 |
| `tests/game/test_cTimeCounter.cpp` | 5 | 6 |
| `tests/gameobjects/test_cPlayerNotification.cpp` | 4 | 14 |
| `tests/utils/test_Color.cpp` | 6 | 31 |
| `tests/utils/test_RNG.cpp` | 7 | 16 |
| `tests/utils/test_SoundPool.cpp` | 7 | 18 |
| `tests/utils/test_cEnumArray.cpp` | 5 | 10 |
| `tests/utils/test_cFileValidator.cpp` | 11 | 22 |
| `tests/utils/test_cMatrix.cpp` | 7 | 18 |
| `tests/utils/test_cPack.cpp` | 15 | 69 |
| Итого | 92 | 285 |

В `B14`: 474 случая и 2201 проверка (`REQUIRE`/`CHECK`) по скрипту, 476 тестов в `ctest.log` `B14`. Эти три числа считают разное: 474 — имена `TEST_CASE` в исходниках (скрипт `check_tests.py`), 471 — случаи, которые перечисляет собранный `d2tm_tests --list-tests`, 476 — тесты `ctest`; каждую проверку сравнивай только с её числом. Ожидание после слияния: `ctest` — `100% tests passed, 0 tests failed out of N`, `N` не меньше 568 (476 + 92); в `d2tm_tests --list-tests` последняя строка `563 test cases` (471 случай `B14` + 92). Случай `cHandleArgument - scaling mode flags` есть в `UP1` и `UP2`, но порт удалил его коммитом 867948487 (П4б: `ScalingMode` заменён настройкой масштаба); он не возвращается; скрипт `check_tests.py` требует от `UP2` только случаи, которых не было в `UP1`.

## PLAN-P14A

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 0 | — | Проверка 0 (состояние слияния и `HEAD`), место на диске (проверка 1, первая строка). Записать в журнал хода `.tmp/p14a/progress.md` | корневая нить (чтение) и помощник C |
| 1 | `.tmp/p14a/check_hunks.py`, `check_tests.py`, `check_scenes.py`, `regen_audio_rows.py`, `tools/ui-audit/tests/test_check_screens_enum.py` | Создать пять файлов точным текстом приложения А; запустить `check_hunks.py` — `files=27 hunks=38 mismatches=0` | помощник C |
| 2 | — | Красный прогон: раздел «Тесты», пять пунктов; результаты в журнал хода строкой `красный прогон закончен`. Помощники A и B начинают шаги 3 и 4 только после этой строки | помощник C |
| 3 | `src/context/AudioContext.cpp`, `src/context/AudioContext.hpp`, `src/controls/mousestates/cMousePlaceState.cpp`, `cMouseRepairState.cpp`, `cMouseUnitsSelectedState.cpp`, `src/building/cItemBuilder.cpp`, `src/drawers/CreditsDrawer.cpp`, `src/drawers/cBuildingListDrawer.cpp`, `src/gameobjects/players/cPlayer.cpp`, `cPlayer.h` | К2, строки 1–8, 13, 14 (дорожка «звук») | помощник A |
| 4 | `src/game/cGame.h`, `src/game/cGame_logic.cpp`, `src/gameobjects/mentat/AbstractMentat.cpp`, `BeneMentat.cpp`, `src/gamestates/cChooseHouseState.cpp`, `cCreditsState.cpp`, `cMainMenuState.cpp`, `cOptionsState.cpp`, `cOptionsState.h`, `cScoringState.cpp`, `cSelectYourNextConquestState.cpp`, `src/managers/cDrawManager.cpp`, `src/debug/UiAudit.hpp`, `UiAuditAccess.cpp`, `UiAuditScenes.cpp`, `src/save/SaveGameManager.cpp`, `src/gamestates/cOptionsPages.cpp`, `cWinLoseState.cpp` | К2, строки 9–12, 15–22; К3.1–К3.6 (дорожка «состояния игры») | помощник B |
| 5 | `src/utils/Graphics.cpp`, `Graphics.hpp`, `cDataPack.hpp`, `cPack.h`, `tests/CMakeLists.txt`, `tools/ui-audit/check_screens.py`, `tools/upstream/build_upstream_linux.sh`, `tests/data/classic_packs_expected.tsv` | К2, строки 23–27; К3.7–К3.9 (дорожка «паки, инструменты, тесты») | помощник C |
| 6 | — | Проверки 1–12 раздела «Проверки» по порядку | помощник C (проверки), корневая нить (разбор провалов) |
| 7 | — | Сверка корневой нитью `git diff` с таблицей К2 и К3 по каждой строке, сдача | корневая нить |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p14`.

0. **Состояние слияния.**
   - `git rev-parse -q --verify MERGE_HEAD` — `d7869e710fc5a91e8e217a3d387767428d82e07d`.
   - `git diff --name-only 0683500a829556942723703183692b29be39d539 HEAD | sort` — ровно четыре строки: `tools/ui-audit/reference_gallery.tsv`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_shots.py`, `tools/ui-audit/tests/test_reference_shots.py`.
   - `git ls-files -u | cut -f2 | sort -u | wc -l` — `27`.
1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P14A-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p14a && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p14a/build.log 2>&1; echo exit=$?` — `exit=0`. Красный прогон шага 2 — та же команда с логом `.tmp/p14a/red-build.log`.
   - В `.tmp/p14a/build.log` есть строка `Строка MENU:` и в ней текст `Setting state from INITIALIZE to MENU`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` не меньше 568.
   - `LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib "$(find .tmp/out/build -name d2tm_tests -type f | head -1)" --list-tests | tail -1` — `563 test cases`.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает.
2. **Маркеры конфликта.** `git grep --untracked -n -e '^<<<<<<< ' -e '^>>>>>>> ' -e '^=======$' -- src tests tools` — пустой вывод (до правок — 114 строк).
3. **Предупреждения и падения.** `grep 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p14a/changed-paths.txt` — пустой вывод; файл `.tmp/p14a/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из таблиц К2 и К3, по одному на строку. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Состав тестов.** `python3 -B .tmp/p14a/check_tests.py > .tmp/p14a/check-tests.log 2>&1; echo exit=$?` — `exit=0`; в логе строки `B14: cases=474 checks=2201`, `UP2: cases=352 checks=1260`, `problems=0`.
5. **Тесты Python.**
   - `cd tools/ui-audit && python3 -B -m unittest discover -s tests > ../../.tmp/p14a/py-ui.log 2>&1; echo exit=$?` — `exit=0`, последняя строка `OK`, число в `Ran N tests` записать в сдачу (`N` не меньше 236: 233 теста `B14` плюс 3 новых; тесты шага П13 добавляют свои).
   - `/srv/dune/venv/bin/python -B -m unittest discover -s tools/upstream/tests -v > .tmp/p14a/py-up.log 2>&1; echo exit=$?` — `exit=0`, `OK` без пропусков.
   - После — `rm -r tools/ui-audit/tests/__pycache__ tools/ui-audit/__pycache__ tools/upstream/tests/__pycache__ tools/__pycache__` для тех из этих папок, что появились.
6. **Каталог сцен.** `mkdir -p .tmp/p14a/xdg && LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib python3 -B .tmp/p14a/check_scenes.py .tmp/out/run/bin .tmp/p14a/xdg > .tmp/p14a/check-scenes.log 2>&1; echo exit=$?` — `exit=0`, в логе `scenes_b14=192 scenes_new=192 missing=0 extra=0 duplicates=0`.
7. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_frames.py`, `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`, `ui_audit_part3a_catalog.py`, `ui_audit_part3a_scenes.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`, `ui_audit_part3c_catalog.py`, `ui_audit_part3c_scenes.py`, `ui_audit_saves.py`, `ui_audit_language.py`, `ui_audit_translation.py`, `ui_audit_tools_run_combo.py` (16 скриптов).
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p14a/tmp && TMPDIR=$PWD/.tmp/p14a/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p14a/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. Скрипты `*_scenes.py` и `ui_audit_translation.py` идут по несколько минут — это норма.
   - Скрипты `ui_audit_part3a_catalog.py` и `ui_audit_part3c_catalog.py` вызывают `tools/ui-audit/check_screens.py`; их `exit=0` подтверждает правку К3.7.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
8. **Эталонные снимки.**
   - `TMPDIR=$PWD/.tmp/p14a/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tools/ui-audit/reference_shots.py --out .tmp/p14a/ref --new-dir .tmp/out/run/bin --no-old --headless --language ru > .tmp/p14a/run-ref.log 2>&1; echo exit=$?` — `exit=0`. Команду не прерывай.
   - Помощник C пишет временный скрипт `.tmp/p14a/check_ref.py` и запускает его (`python3 -B .tmp/p14a/check_ref.py .tmp/p14a/ref/reference.tsv > .tmp/p14a/check-ref.log 2>&1; echo exit=$?`): в `reference.tsv` — заголовок и ровно 31 строка данных; у каждой строки `new_exit` равен `0`, `problems` равен `ok`, `new_png_size` равен разрешению из столбца `resolution`, `new_canvas` равен ожидаемому холсту (`800x600` → `800x600`, `1920x1080` → `1067x600`, `5120x1440` → `2133x600`); все 31 файл столбца `sheet` существуют; число строк с `old_scene` равным `-` равно 31; в `.tmp/p14a/ref/new/` на каждую строку есть `.png` и `.geometry.jsonl`. Скрипт печатает `rows=31 ok=31 sheets=31 canvas_ok=31`; `exit=0`.
9. **Данные.** `sha256sum resources/bin/data/sdl_audio.dat` — `601d2d109844ea2f22a1094bea2296bae17596941e368ae3f0ecf0c351b3dc29`. `grep -c '^sdl_audio.dat' tests/data/classic_packs_expected.tsv` — `107`.
10. **Опись клавиш.** `python3 -B tools/ui-audit/extract_keys.py --root . --out .tmp/p14a/keys-raw.tsv > .tmp/p14a/keys.log 2>&1; python3 -B tools/ui-audit/check_keys.py --keys tools/ui-audit/keys.tsv --raw .tmp/p14a/keys-raw.tsv >> .tmp/p14a/keys.log 2>&1; echo exit=$?` — `exit=0`, в логе строка `keys: freshness OK; rule 10 flags: 178` (на `B14` и на пробном разрешении — те же `309` строк `keys-raw` и `178` отметок).
11. **Остатки старых имён.** Пути поиска `CODE` — шаблоны Git `'src/*.cpp' 'src/*.h' 'src/*.hpp' 'tests/*.cpp' 'tests/*.h' 'tests/*.hpp'` (в шаблонах Git `*` включает `/`); команды — `git grep --untracked -n -E '<шаблон>' -- <пути>`, в скобках ожидаемое число строк вывода:
    - `'#include\s+"(data/)?(gfxaudio|Sounds)\.h"'` в `CODE` (0);
    - `'(^|[^"A-Za-z_])(SOUND|MIDI)_[A-Z0-9_]+'` в `CODE` и `':!src/data/SoundPools.h'` (1: закомментированная строка `src/gamestates/cTellHouseState.cpp:85`);
    - `'\bGAME_(INITIALIZE|OVER|MENU|PLAYING|BRIEFING|EDITOR|NEW_MAP_EDITOR|OPTIONS|REGION|SELECT_HOUSE|INTRO|TELLHOUSE|WINNING|SCORING|WINBRIEF|LOSEBRIEF|LOSING|SKIRMISH|SETUPSKIRMISH|CREDITS|MISSIONSELECT|VIDEO|MAX_STATES)\b'` в `CODE` (59: 41 в `src/debug/UiAuditScenes.cpp`, 18 в `src/gamestates/cGameState.h`);
    - `'currentGame\.m_(state|currentState)\b|isState\(GAME_|\(GAME_'` в `'src/*.cpp' 'src/*.h' 'src/*.hpp'` (0);
    - `'playVoice\((SOUND|[0-9])'` в `'src/*.cpp' 'src/*.h' 'src/*.hpp'` (0).
12. **Рамка правок.** `git -c lfs.storage=$PWD/.tmp/p14a/lfs diff --name-only | sort > .tmp/p14a/changed.txt` — файл совпадает построчно (`diff` без вывода) со списком приложения Б.1 (36 путей); `git -c lfs.storage=$PWD/.tmp/p14a/lfs ls-files --others --exclude-standard` — только `tools/ui-audit/tests/test_check_screens_enum.py`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P14A-NN` с выводом и стоп. Ожидания существующих тестов (кроме данных `tests/data/classic_packs_expected.tsv`, К3.9) и скрипты в `tests/ui_audit/` не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P14A | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p14a/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: вывод пяти пунктов раздела «Тесты» (строки `error` из `.tmp/p14a/red-build.log` — не больше 30);
- вывод каждой проверки 0–12 с кодами выхода (не больше 40 строк на проверку); число `<N>` из `ctest.log` и число `N` из `Ran N tests`;
- `git diff --stat` и список путей для коммита слияния: 36 путей приложения Б.1 и новый файл К4 (ведущий делает `git add` по этому списку и `git commit`); текст сообщения коммита слияния на английском, последняя строка — `Behavior changes: …` (что меняется для игрока: изменения апстрима из `git log --oneline UP1..UP2`, изменений порта нет);
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p14a --size`; у `.tmp/p14a` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаги 0–2 (помощник C).
  4. Шаги 3 (помощник A), 4 (помощник B) и 5 (помощник C) — одновременно, после строки `красный прогон закончен` в журнале хода.
  5. Шаг 6 (помощник C) — после шагов 3, 4 и 5.
  6. Шаг 7 (корневая нить), сдача и стоп.
- **Параллельно:** дорожки A, B и C правят непересекающиеся файлы (таблица плана); шаг 6 собирает их вместе.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник C — 30 минут на шаги 0–2, 40 минут на шаг 5 и 4 часа на шаг 6 (сборка около 30 минут, 16 скриптов сцен — остальное); помощник A — 40 минут; помощник B — 60 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено» и «Контракт» (К1 и строки его шагов К2–К4); его шаги плана; для помощника C — ещё разделы «Тесты», «Проверки» и приложение А; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p14a/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P14A` и на блоках `## Q-P14A-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P14A-NN` и стоп.
- **Рамка правок:** 36 файлов приложения Б.1 (27 файлов таблицы К2 и 9 файлов К3), новый файл `tools/ui-audit/tests/test_check_screens_enum.py` и папка `.tmp/p14a/`. Понадобился другой файл — блок `## Q-P14A-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и во временные папки скриптов; это не правка. Не пиши в `.git` и не выполняй команд из списка запрещённых в начале задания.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

## Приложение А — тексты файлов

Файлы создаются байт в байт, кодировка UTF-8, окончания строк `\n`.

**`.tmp/p14a/check_hunks.py`**

```python
import sys

EXPECTED = {
    "src/building/cItemBuilder.cpp": [48],
    "src/context/AudioContext.cpp": [50, 172],
    "src/context/AudioContext.hpp": [19, 71],
    "src/controls/mousestates/cMousePlaceState.cpp": [93],
    "src/controls/mousestates/cMouseRepairState.cpp": [31],
    "src/controls/mousestates/cMouseUnitsSelectedState.cpp": [39],
    "src/drawers/CreditsDrawer.cpp": [32],
    "src/drawers/cBuildingListDrawer.cpp": [46],
    "src/game/cGame.h": [23, 96, 243],
    "src/game/cGame_logic.cpp": [23, 121, 601],
    "src/gameobjects/mentat/AbstractMentat.cpp": [39],
    "src/gameobjects/mentat/BeneMentat.cpp": [33],
    "src/gameobjects/players/cPlayer.cpp": [2086],
    "src/gameobjects/players/cPlayer.h": [634],
    "src/gamestates/cChooseHouseState.cpp": [34],
    "src/gamestates/cCreditsState.cpp": [36],
    "src/gamestates/cMainMenuState.cpp": [71],
    "src/gamestates/cOptionsState.cpp": [206],
    "src/gamestates/cOptionsState.h": [49, 110],
    "src/gamestates/cScoringState.cpp": [19],
    "src/gamestates/cSelectYourNextConquestState.cpp": [348],
    "src/managers/cDrawManager.cpp": [59, 403],
    "src/utils/Graphics.cpp": [136],
    "src/utils/Graphics.hpp": [26, 57],
    "src/utils/cDataPack.hpp": [64],
    "src/utils/cPack.h": [52],
    "tests/CMakeLists.txt": [6, 49, 117],
}

found = {}
for path in sorted(EXPECTED):
    text = open(path, encoding="utf-8", errors="replace").read().splitlines()
    found[path] = [number for number, line in enumerate(text, 1) if line.startswith("<<<<<<< ")]
mismatches = [path for path in EXPECTED if found[path] != EXPECTED[path]]
for path in mismatches:
    print(path, "expected", EXPECTED[path], "found", found[path])
print("files=%d hunks=%d mismatches=%d" % (len(EXPECTED), sum(len(v) for v in found.values()), len(mismatches)))
sys.exit(1 if mismatches else 0)
```

Команда запуска (до правок): `python3 -B .tmp/p14a/check_hunks.py` — `files=27 hunks=38 mismatches=0`.

**`.tmp/p14a/check_tests.py`**

```python
import re
import subprocess
import sys
from pathlib import Path

UP1 = "d06f2fcd2a347182c3774fb96e9a85570405c489"
REVISIONS = {
    "B14": "0683500a829556942723703183692b29be39d539",
    "UP2": "d7869e710fc5a91e8e217a3d387767428d82e07d",
}
CASE = re.compile(
    r'\b(?:TEST_CASE|TEST_CASE_METHOD|TEMPLATE_TEST_CASE|TEMPLATE_TEST_CASE_METHOD|SCENARIO|TEMPLATE_LIST_TEST_CASE)'
    r'\s*\(\s*(?:[A-Za-z_][\w:<>]*\s*,\s*)?"((?:[^"\\]|\\.)*)"'
)
CHECK = re.compile(r"\b(?:REQUIRE|CHECK)(?:_[A-Z_]+)?\s*\(")


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout.decode("utf-8", "replace")


def scan(text):
    return CASE.findall(text), len(CHECK.findall(text))


problems = []
totals = {}
for name, revision in REVISIONS.items():
    listed = git("ls-tree", "-r", "--name-only", revision, "tests").splitlines()
    case_count = 0
    check_count = 0
    for path in listed:
        if not path.endswith((".cpp", ".hpp", ".h")):
            continue
        cases, checks = scan(git("show", f"{revision}:{path}"))
        case_count += len(cases)
        if name == "UP2":
            try:
                inherited, _ = scan(git("show", f"{UP1}:{path}"))
            except subprocess.CalledProcessError:
                inherited = []
            cases = [case for case in cases if case not in inherited]
        check_count += checks
        if not cases and not checks:
            continue
        current = Path(path)
        if not current.is_file():
            problems.append(f"{name} {path}: file is missing")
            continue
        current_cases, current_checks = scan(current.read_text(encoding="utf-8", errors="replace"))
        for case in cases:
            if case not in current_cases:
                problems.append(f"{name} {path}: test case missing: {case}")
        if current_checks < checks:
            problems.append(f"{name} {path}: checks {current_checks} < {checks}")
    totals[name] = (case_count, check_count)

for name, (case_count, check_count) in totals.items():
    print(f"{name}: cases={case_count} checks={check_count}")
for problem in problems[:50]:
    print(problem)
print(f"problems={len(problems)}")
sys.exit(1 if problems else 0)
```

**`.tmp/p14a/check_scenes.py`**

```python
import json
import os
import re
import subprocess
import sys

B14 = "0683500a829556942723703183692b29be39d539"
run_dir = os.path.abspath(sys.argv[1])
xdg = os.path.abspath(sys.argv[2])
os.makedirs(xdg, exist_ok=True)

source = subprocess.run(["git", "show", f"{B14}:src/debug/UiAuditScenes.cpp"], check=True,
                        capture_output=True).stdout.decode("utf-8", "replace")
expected = re.findall(r'scene\("([^"]*)"', source)

environment = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_RENDER_DRIVER="software",
                   SDL_AUDIODRIVER="dummy", XDG_DATA_HOME=xdg)
result = subprocess.run(
    [os.path.join(run_dir, "d2tm"), "-windowed", "-screenWidth", "1024", "-screenHeight", "768", "--ui-audit-list"],
    cwd=run_dir, env=environment, capture_output=True, text=True, timeout=120)
if result.returncode != 0:
    print("d2tm exit", result.returncode, result.stderr[:500])
    sys.exit(1)
actual = [scene["id"] for scene in json.loads(result.stdout.strip())["scenes"]]

missing = sorted(set(expected) - set(actual))
extra = sorted(set(actual) - set(expected))
duplicates = len(actual) - len(set(actual))
print("scenes_b14=%d scenes_new=%d missing=%d extra=%d duplicates=%d"
      % (len(expected), len(actual), len(missing), len(extra), duplicates))
for name in missing + extra:
    print(name)
sys.exit(0 if (not missing and not extra and not duplicates and len(actual) == 192) else 1)
```

**`.tmp/p14a/regen_audio_rows.py`** (запуск из корня: `/srv/dune/venv/bin/python -B .tmp/p14a/regen_audio_rows.py .`)

```python
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root))
from tools import hd_assets

tsv = root / "tests/data/classic_packs_expected.tsv"
raw = tsv.read_bytes().decode("utf-8")
newline = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(newline)
assert lines[0] == "pack\tindex\tname\textension\tsha256"
assert lines[-1] == ""
assert lines[1].startswith("sdl_audio.dat\t")
audio = [
    "\t".join(("sdl_audio.dat", str(e.index), e.name, e.extension, hashlib.sha256(e.payload).hexdigest()))
    for e in hd_assets.read_pack(root / "resources/bin/data/sdl_audio.dat")
]
rest = [line for line in lines[1:-1] if not line.startswith("sdl_audio.dat\t")]
tsv.write_bytes(newline.join([lines[0]] + audio + rest + [""]).encode("utf-8"))
print("audio_rows=%d other_rows=%d" % (len(audio), len(rest)))
```

**`tools/ui-audit/tests/test_check_screens_enum.py`**

```python
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_screens  # noqa: E402

ENUM_HEADER = """\
#pragma once

enum class eGameState : char {
    INITIALIZE = 0,        // initialize game
    OVER,                  // GAME OVER
    MENU,
    COUNT
};

const char *gameStateToString(eGameState state);
"""


class EnumStates(unittest.TestCase):
    def test_enumerators_get_the_old_constant_names(self):
        self.assertEqual(check_screens.code_enum_states(ENUM_HEADER),
                         ["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES"])

    def test_text_without_the_enum_gives_no_states(self):
        self.assertEqual(check_screens.code_enum_states("enum class Other { A, B };\n"), [])

    def test_collect_code_names_reads_the_enum(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {
                "src/include/eGameState.h": ENUM_HEADER,
                "src/gamestates/cA.h": "class cA {\n",
                "src/gameobjects/mentat/M.h": "class M : public X {\n",
                "src/save/SaveSlotsDialog.hpp": "class SaveSlotsDialog {\n",
            }
            for name, text in sources.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertEqual(check_screens.collect_code_names(root),
                             ["GAME_INITIALIZE", "GAME_OVER", "GAME_MENU", "GAME_MAX_STATES", "M", "cA", "SaveSlotsDialog"])


if __name__ == "__main__":
    unittest.main()
```

## Приложение Б — списки файлов

**Б.1. Рамка правок — 36 путей** (вывод `git diff --name-only | sort` проверки 12 равен этому списку; помощник C кладёт его в `.tmp/p14a/frame.txt`):

```
src/building/cItemBuilder.cpp
src/context/AudioContext.cpp
src/context/AudioContext.hpp
src/controls/mousestates/cMousePlaceState.cpp
src/controls/mousestates/cMouseRepairState.cpp
src/controls/mousestates/cMouseUnitsSelectedState.cpp
src/debug/UiAudit.hpp
src/debug/UiAuditAccess.cpp
src/debug/UiAuditScenes.cpp
src/drawers/CreditsDrawer.cpp
src/drawers/cBuildingListDrawer.cpp
src/game/cGame.h
src/game/cGame_logic.cpp
src/gameobjects/mentat/AbstractMentat.cpp
src/gameobjects/mentat/BeneMentat.cpp
src/gameobjects/players/cPlayer.cpp
src/gameobjects/players/cPlayer.h
src/gamestates/cChooseHouseState.cpp
src/gamestates/cCreditsState.cpp
src/gamestates/cMainMenuState.cpp
src/gamestates/cOptionsPages.cpp
src/gamestates/cOptionsState.cpp
src/gamestates/cOptionsState.h
src/gamestates/cScoringState.cpp
src/gamestates/cSelectYourNextConquestState.cpp
src/gamestates/cWinLoseState.cpp
src/managers/cDrawManager.cpp
src/save/SaveGameManager.cpp
src/utils/Graphics.cpp
src/utils/Graphics.hpp
src/utils/cDataPack.hpp
src/utils/cPack.h
tests/CMakeLists.txt
tests/data/classic_packs_expected.tsv
tools/ui-audit/check_screens.py
tools/upstream/build_upstream_linux.sh
```

**Б.2. Файлы, которые изменили и апстрим, и порт и которые Git слил без конфликта, — 40 файлов; они не правятся** (ещё один такой файл, `src/gamestates/cWinLoseState.cpp`, входит в Б.1 — правка К3.6; команда списка: `comm -12 <(git diff --name-only d06f2fcd2a347182c3774fb96e9a85570405c489 d7869e710fc5a91e8e217a3d387767428d82e07d | sort) <(git diff --name-only d06f2fcd2a347182c3774fb96e9a85570405c489 0683500a829556942723703183692b29be39d539 | sort)`, 68 путей, из них 27 с конфликтом, 1 — `cWinLoseState.cpp`, остальные — этот список):

```
src/CMakeLists.txt
src/context/cInfoContextCreator.cpp
src/controls/cGameControlsContext.cpp
src/controls/cGameControlsContext.h
src/controls/mousestates/cMouseNormalState.cpp
src/controls/mousestates/cMouseNormalState.h
src/controls/mousestates/cMousePlaceState.h
src/drawers/CreditsDrawer.h
src/drawers/cMiniMapDrawer.cpp
src/drawers/cMiniMapDrawer.h
src/gameobjects/map/cMapCamera.cpp
src/gameobjects/structures/cAbstractStructure.cpp
src/gameobjects/structures/cOrderProcesser.cpp
src/gameobjects/structures/cStarPort.cpp
src/gameobjects/units/cUnit.cpp
src/gameobjects/units/cUnitInfos.h
src/gamestates/cEditorState.cpp
src/gamestates/cGamePlaying.cpp
src/gamestates/cGamePlaying.h
src/gamestates/cNewmapEditorState.cpp
src/gamestates/cSelectMissionState.cpp
src/gamestates/cSelectMissionState.h
src/gamestates/cSetupSkirmishState.cpp
src/gamestates/cTellHouseState.h
src/gui/GuiBar.cpp
src/gui/GuiButton.cpp
src/gui/GuiCheckBox.cpp
src/gui/GuiCycleButton.cpp
src/gui/GuiLabel.cpp
src/gui/GuiSlider.cpp
src/gui/GuiStateButton.cpp
src/gui/GuiTextInput.cpp
src/gui/GuiValueButton.cpp
src/gui/GuiWindow.cpp
src/sidebar/cSideBar.cpp
src/sidebar/cSideBar.h
src/utils/cDataPack.cpp
src/utils/cPack.cpp
src/utils/cSoundPlayer.cpp
src/utils/cSoundPlayer.h
```

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
