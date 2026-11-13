# RECON P8R — разведка сохранений перед шагом П8

Ревизии: `BASE=e17379a`, `FORK1=9208dcf`, `UP1=d06f2fc`, `PORT=0a33444`, документы `MAIN=62e1ff6`. Строки исходников и сверки приведены в восьми TSV-таблицах рядом с этим отчётом.

## 1. Механизм сохранений в FORK1

Команда предварительного чтения карты:

```text
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '9,36p;530,563p;800,845p;915,931p'
```

Вывод описывает `save-slots` как десять именованных сохранений и F5/F9; перечисляет семь файлов `src/save/` как отсутствующие в UP1, две save-тестовые цели и риск нового API `src/game/cGame.h@d06f2fc:89` против старого `cGame.h`, подключаемого `SaveGameManager.cpp@9208dcf:9`. В карте также указано, что переносить нужно слоты, диалог выбора и F5/F9.

В `FORK1` кодек записывает заголовок вида `D2TM_SAVE <version> <checksum>\n<body>` (`src/save/SaveFileCodec.cpp@9208dcf:9,24-32`); `FormatVersion=2` объявлен в `src/save/SaveGameManager.hpp@9208dcf:22`, максимальный размер файла — 16 MiB (`src/save/SaveGameManager.cpp@9208dcf:43`). `decode()` отклоняет чрезмерный размер, отсутствующий или повреждённый заголовок, лишнее поле, несовпадающую версию и неверную контрольную сумму (`src/save/SaveFileCodec.cpp@9208dcf:39-67`). Разбор тела допускает отсутствие `INFO`, когда первым идёт `META` (`src/save/SaveGameManager.cpp@9208dcf:378-388`). Писатель тела — `serializeBody()` (`src/save/SaveGameManager.cpp@9208dcf:248-365`), читатель — `deserializeBody()` (`:367-692`). Порядок разделов: `INFO`, `META`, `MAP`, `PLAYERS`/`PLAYER`, `CELLS`/`CELL`, `STRUCTURES`/`STRUCTURE`, `UNITS`/`UNIT`, `REINFORCEMENTS`/`REINFORCEMENT`, `BUILD_QUEUE`/`BUILD`, `FACTORYPADS`/`FACTORYPAD`, `END`; функции записи и чтения каждого раздела указаны в `fork-save.tsv`.

В `FORK1` разрешено 10 слотов с номерами 1–10 (`src/save/SaveSlotName.hpp@9208dcf:12-18`). Имя ограничено 96 байтами; очистка удаляет ASCII-коды `0x00–0x1f` и `0x7f`, схлопывает и убирает крайние пробелы, а неполные многобайтные последовательности не добавляет (`SaveSlotName.hpp@9208dcf:13,33-92`). Имя сохраняется в тексте раздела `INFO`; в имя файла оно не входит. Каталог относительный `saves`; слот 1 — `saves/quicksave.d2s`, остальные — `saves/saveNN.d2s` (`SaveGameManager.cpp@9208dcf:1349-1359`).

`fork-save.tsv` содержит объявленные API/типы/константы заголовков и функции `.cpp`, работающие с разделами, с входами, выходами и строками. `save-fields.tsv` перечисляет все сериализуемые поля состояния и соответствия в PORT.

Подсчёт `save-fields.tsv` выполнен через `/srv/dune/venv/bin/python`, чтением столбцов типов и объявления PORT. Вывод:

```text
Поля всего: 147
С тем же типом в PORT: 102
С другим типом в PORT: 4
Без члена в PORT: 41
Проверка суммы категорий: 147
```

Команда выборочной сверки `git show` подтвердила поля направления юнитов: FORK1 объявляет их `int` (`src/gameobjects/units/cUnit.h@9208dcf:146-149`), PORT — `Facing` (`src/gameobjects/units/cUnit.h@0a33444:118-121`). `FactoryPad.hpp` в PORT отсутствует: `git ls-tree -r --name-only 0a33444e9032ef935dfe4cdde6bb622771484230 | grep '/FactoryPad.hpp$'` вывел пустую строку.

## 2. Состояние игры в сохранении

`save-fields.tsv` содержит 147 строк состояния с разделом, классом, членом, типом, объявлением FORK1, записью и чтением, объявлением и типом PORT. Подсчёт и вывод приведены в пункте 1. Например, `cGame::m_skirmish` записывается/читается в `META` (`SaveGameManager.cpp@9208dcf:253,390`), в PORT поле `bool m_skirmish` есть в `src/game/cGameSettings.h@0a33444:166`; четыре направления `cUnit` имеют смену `int` на `Facing`; 41 член отсутствует в PORT, включая девять полей `factory_pad::PadState`.

Команды выборочной проверки:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp | sed -n '248,258p;385,397p'
git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/game/cGameSettings.h | sed -n '162,168p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.h | nl -ba | sed -n '144,151p'
git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gameobjects/units/cUnit.h | nl -ba | sed -n '108,123p'
```

Выводы содержат `META` с полями `skirmish`, `region`, `mission`, флагами победы/поражения и ячейкой камеры; `m_skirmish` в PORT имеет тип `bool`. В `cUnit` четыре поля направления в FORK1 имеют тип `int`, а одноимённые поля PORT — `Facing`.

## 3. Правки FORK1 вне `src/save/`

Для каждого пути из задания выполнен `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <путь>`. `fork-hooks.tsv` содержит совпавшие участки, строку FORK1, краткое описание добавленного и путь/совпадение в PORT. Для `src/gamestates/*` соответствия приведены по UP1, поскольку путь PORT там сейчас меняет П5.

Дополнены три участка по членам из `save-fields.tsv`. Вывод `git diff --unified=3 ... -- src/gameobjects/units/cUnit.h src/player/cPlayer.h`:

```text
@@ -109,6 +113,8 @@
 bool bCarryMe;
+bool bRollingOffFactoryPad;
+int iRollingOffFactoryPadStructureId;
 int iCarryAll;
@@ -539,6 +543,7 @@
 int iPrimaryBuilding[MAX_STRUCTURETYPES];
 int iStructures[MAX_STRUCTURETYPES];
+bool m_hdTextureReferences = false;
@@ -561,6 +566,9 @@
 bool alive;
+Uint64 m_lastEnemyWarningMs = 0;
+bool m_hasPlayedEnemyWarning = false;
```

Соответствия PORT сверены командами `git show`: `bCarryMe` и `iCarryAll` — `src/gameobjects/units/cUnit.h@0a33444:165-166`; `iPrimaryBuilding` и `iStructures` — `src/gameobjects/players/cPlayer.h@0a33444:640-641`; `alive` — `:660`. Полный список участков находится в `fork-hooks.tsv`.

## 4. Входы в сохранение в FORK1

В `inputs.tsv` пять входов: F5 вызывает `cGame::saveQuickGame` и `SaveGameManager::saveQuickGame` (`src/cGame_logic.cpp@9208dcf:2042-2046,2635-2637`); F9 вызывает `cGame::loadQuickGame` и `SaveGameManager::loadQuickGame` (`:2057-2059,2640-2642`); кнопка «Сохранения» главного меню открывает диалог загрузки (`src/gamestates/cMainMenuState.cpp@9208dcf:164-165`); кнопки Load и Save меню настроек во время игры открывают диалог (`src/gamestates/cOptionsState.cpp@9208dcf:850-877`). Таблица также содержит соответствующие обработчики событий UP1 и отмечает отсутствие кнопок сохранения/загрузки в его меню настроек.

Команда проверки настроек F5/F9:

```text
git grep -n -E 'F5|F9' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
```

Вывод:

```text
src/cGame_logic.cpp:2042:    if (event.hasKey(SDL_SCANCODE_F5) &&
src/cGame_logic.cpp:2057:    if (event.hasKey(SDL_SCANCODE_F9)) {
src/cGame_logic.cpp:2424:    if (event.hasKeys(SDL_SCANCODE_F5, SDL_SCANCODE_LSHIFT)) {
```

Совпадений в таблице настраиваемых клавиш FORK1 эта команда не показала.

## 5. Сохранения и `preferences.ini` в UP1 и PORT

Команда `git grep -n -i -E 'savegame|save_game|loadgame|load_game|quicksave|quickload' d06f2fcd2a347182c3774fb96e9a85570405c489 -- src` вывела пустой результат. В UP1 кнопка `Load` главного меню и её callback находятся в `src/gamestates/cMainMenuState.cpp@d06f2fc:151-163`; callback вызывает `fadeOut()` на `:161`.

Имя файла задаёт `PREFERENCES_FILE = "preferences.ini"` в `src/main.cpp@d06f2fc:54` и `src/main.cpp@0a33444:54`. Путь строит `PreferencesPath::file()`; `PreferencesPath::directory()` вызывает `SDL_GetPrefPath("D2TM", "Dune II - The Maker")` (`src/game/PreferencesPath.cpp@d06f2fc:28-47`, тот же код в `@0a33444:28-47`). `main` загружает файл при `-prefs` (`src/main.cpp@ревизия:77-84`) и сохраняет после игры (`:113-118`). Ключи читает/пишет `Preferences::load/save` (`src/game/Preferences.cpp@ревизия:129-195`). Код использует путь SDL без отдельных ветвей для Windows, Linux и macOS.

`preferences.tsv` содержит 26 ключей UP1 и 27 ключей PORT. Проверка исходников дала:

```text
d06f2fc reads=26 writes=26 unique_source=26 table=26 missing=[] extra=[]
read_only=[] write_only=[]
0a33444 reads=27 writes=26 unique_source=27 table=27 missing=[] extra=[]
read_only=['WorldScale'] write_only=[]
```

В UP1 ключ `ScalingMode` имеет тип `eScalingMode`, текстовое значение по умолчанию `IntegerScale`, читается и записывается в `Preferences.cpp@d06f2fc:66,162`. В PORT вместо него используется `RenderScale` (целое, default 0; чтение/запись `Preferences.cpp@0a33444:66,163`); также PORT читает `WorldScale` (int, default 0, `InitialGameSettings.hpp@0a33444:27`, `Preferences.cpp@0a33444:68`), но не записывает этот ключ. Остальные значения и все построчные источники приведены в `preferences.tsv`.

## 6. Настройки форка

`FORK1` берёт каталог исполняемого файла вызовом `SDL_GetBasePath()` и назначает его текущим (`src/main.cpp@9208dcf:34-49,85`); поэтому относительные `settings.ini` и `saves/` находятся у каталога игры. `settings.ini` загружается при старте (`src/main.cpp@9208dcf:92`); функции чтения и записи параметров — `src/utils/common.cpp@9208dcf:47-82,360-367`, а меню вызывает чтение/запись при `src/gamestates/cOptionsState.cpp@9208dcf:104,500,728`. `game.ini` отдельно читается как файл правил игры (`src/cGame_logic.cpp@9208dcf:1017-1025`). Таблица `fork-settings.tsv` содержит 40 читаемых/записываемых ключей `settings.ini` FORK1 и сравнение с обоими файлами настроек PORT.

Команда, требуемая для проверки `settings.ini` PORT:

```text
git show 0a33444e9032ef935dfe4cdde6bb622771484230:resources/bin/settings.ini
```

Вывод:

```ini
[SETTINGS]
#Uncomment to hard set resolution, keep commented to use auto-detection
ScreenWidth=1024
ScreenHeight=768
CameraBorderOrKeyMoveSpeed=0.5
CameraDragMoveSpeed=0.5
#Move camera when the mouse reaches the screen edge. Defaults to false when
#windowed, true when fullscreen. Uncomment to override either way.
#CameraEdgeMove=true
FullScreen=false
#Game scale in percent: 0 = Auto, or 100, 125, 150, 175, 200. The game canvas is the screen size divided by it, at least 800x600
RenderScale=0
#Dune 2 scenario's have a hint to have reinforcements repeat
#this is broken in Dune 2; D2TM can fix this behavior; set this
#to 'true' to enable. It will increase the difficulty.
AllowRepeatingReinforcements=false

#Dune 2 allows for turrets to fire even when low power. If you want to have all kind of turrets
#shut down on low power, set this true.
AllTurretsDownOnLowPower=false

#true = When low power, rocket turrets will not fire rockets (but do fire normal bullets)
#       unless "AllTurretsDownOnLowPower" is true
RocketTurretsDownOnLowPower=true

#true = show a blinking lightning-bolt icon on structures that need power when you are low on power.
#Off by default.
ShowLowPowerIcon=false

# this is the base-dir for [datafile] and [font] entries
GameDir=data

# disable AI
#NoAI = true

# Fix OneAi
#oneAi = True

# activate NoAiRest
#noAiRest = True

# disable WormAI
#disableWormAi = True

# disable Reinforcements
#disableReinforcements = True

# activate DebugMode
#Debug = true

# activate UnitDebugMode
#drawUnitDebug = True

# activate drawUsages
#drawUsages = True

# pauses game when losing focus
#pauseWhenLosingFocus = True

# enable fog of war (experimental)
#fogOfWarEnabled = True

# disable Music
#playMusic = false

# play music files from the audio directory (next to settings.ini) instead of the built-in music,
# when the directory of a music type contains .ogg, .mp3, .wav or .flac files. Directories:
# audio/win, audio/lose, audio/attack, audio/peace, audio/menu, audio/conquest and
# audio/briefing/atreides, audio/briefing/harkonnen, audio/briefing/ordos, audio/briefing/sardaukar
#customMusic = true

# disable sound 
#playSound = false

# disable the credits counting sound (spice collected/spent)
#playCreditsSound = false

# this is the game rules file
GameRules=game.ini

[DATAFILE]
GFXDATA=sdl_data_hd4.dat
GFXINTER=sdl_inter_hd4.dat
GFXWORLD=sdl_world_hd4.dat
GFXMENTAT=sdl_mentat_hd4.dat
GFXAUDIO=sdl_audio.dat
GFXEDITOR=sdl_gfxeditor.dat

[FONT]
ARRAKEEN=arrakeen.fon
BENEGESS=benegess.fon
SMALL=small.ttf

[KEYS]
#Key names must match SDL scancode names (e.g. Left, Right, Up, Down, F11, Escape, Return, Backspace)
#Modifier keys can be included as tokens: Alt, Ctrl, Shift  (e.g. TOGGLE_FULLSCREEN=Alt,Return)
#Multiple physical keys act as alternatives: ATTACK_MODE=Left Ctrl,Right Ctrl
SCREENSHOT=F11
TOGGLE_MUSIC=M
MUSIC_VOLUME_DOWN=O
MUSIC_VOLUME_UP=P
GAME_SPEED_UP=Keypad +
GAME_SPEED_DOWN=Keypad -
TOGGLE_FULLSCREEN=Alt,Return
TOGGLE_CHEAT=Alt,C
SCROLL_LEFT=Left
SCROLL_RIGHT=Right
SCROLL_UP=Up
SCROLL_DOWN=Down
CENTER_ON_HOME=H
CENTER_ON_STRUCTURE=C
ZOOM_RESET=Z
SAVE_VIEWPORT_BOOKMARK_1=Alt,F1
SAVE_VIEWPORT_BOOKMARK_2=Alt,F2
SAVE_VIEWPORT_BOOKMARK_3=Alt,F3
SAVE_VIEWPORT_BOOKMARK_4=Alt,F4
SAVE_VIEWPORT_BOOKMARK_5=Alt,F5
JUMP_TO_VIEWPORT_BOOKMARK_1=F1
JUMP_TO_VIEWPORT_BOOKMARK_2=F2
JUMP_TO_VIEWPORT_BOOKMARK_3=F3
JUMP_TO_VIEWPORT_BOOKMARK_4=F4
JUMP_TO_VIEWPORT_BOOKMARK_5=F5
TOGGLE_FPS=F
TOGGLE_TIME_DISPLAY=\
OPEN_MENU=Escape
DEPLOY_UNIT=D
SET_PRIMARY=P
ATTACK_MODE=Left Ctrl,Right Ctrl
ADD_TO_SELECTION=Left Shift,Right Shift
REPAIR=R
RETURN_TO_BASE=F
SEND_TO_REFINERY=D
SELECT_SAME_TYPE_ON_SCREEN=Ctrl,Z
GROUP_1=1
GROUP_2=2
GROUP_3=3
GROUP_4=4
GROUP_5=5
TRACK_UNIT=T
EDITOR_SAVE=Ctrl,S
EDITOR_ZOOM_IN=Page Up
EDITOR_ZOOM_OUT=Page Down
MENU_BACK=Escape
MENU_CONFIRM=Return
MENU_CANCEL=Backspace
DEBUG_WIN=Shift,Tab,F2
DEBUG_LOSE=Shift,Tab,F3
DEBUG_GIVE_CREDITS=Shift,Tab,F4
DEBUG_DESTROY_AT_CURSOR=Shift,Tab,F7
DEBUG_REVEAL_MAP=Shift,Tab,F5
DEBUG_DAMAGE_AT_CURSOR=Shift,Tab,F10
DEBUG_KILL_CARRYALLS=Shift,Tab,F6
DEBUG_SPAWN_ORNITHOPTER=Shift,Tab,F8
DEBUG_SPAWN_WORM=Shift,Tab,F9
DEBUG_CLEAR_SHROUD_AT_CURSOR=Shift,Tab,F12
DEBUG_SWITCH_PLAYER_0=Tab,0
DEBUG_SWITCH_PLAYER_1=Tab,1
DEBUG_SWITCH_PLAYER_2=Tab,2
DEBUG_SWITCH_PLAYER_3=Tab,3
```

## 7. Тесты

Тесты FORK1 регистрируются как `save_file_codec_roundtrip` (`CMakeLists.txt@9208dcf:384`), `save_slot_name_handling` (`:395`) и `factory_pad_save` (`tests/UnitRenderFixture.cmake@9208dcf:99,134`). В PORT тесты Catch2 входят в общий `d2tm_tests` (`tests/CMakeLists.txt@0a33444:4-29,61-64`), линкуют Catch2 (`:75`) и регистрируются через `catch_discover_tests(d2tm_tests)` (`:95-98`).

Команда подсчёта вызовов функций-проверок по исходникам FORK1:

```text
/srv/dune/venv/bin/python - <<'PY'
import re, subprocess
rev='9208dcf5a358f40afd95c99480e4e09f781ed566'
files=['tests/SaveFileCodecTests.cpp','tests/SaveSlotNameTests.cpp','tests/FactoryPadSaveTests.cpp']
texts={p:subprocess.check_output(['git','show',f'{rev}:{p}'],text=True) for p in files}
codec_calls=len(re.findall(r'\bexpectFailure\s*\(', texts[files[0]]))
slot_calls=len(re.findall(r'\bexpect\s*\(', texts[files[1]]))
pad_calls=len(re.findall(r'\bcheck\s*\(', texts[files[2]]))
codec_checks=codec_calls-1+1
slot_checks=slot_calls-1
pad_checks=pad_calls-1
print(f'{files[0]}: {codec_checks} checks (1 round-trip condition + {codec_calls-1} expectFailure calls)')
print(f'{files[1]}: {slot_checks} checks ({slot_calls-1} expect calls)')
print(f'{files[2]}: {pad_checks} checks ({pad_calls-1} check calls)')
PY
```

Вывод:

```text
tests/SaveFileCodecTests.cpp: 5 checks (1 round-trip condition + 4 expectFailure calls)
tests/SaveSlotNameTests.cpp: 10 checks (10 expect calls)
tests/FactoryPadSaveTests.cpp: 23 checks (23 check calls)
```

`tests.tsv` содержит отдельную строку на каждую проверку, проверяемое поведение, символы/заголовки и наличие каждого в PORT, а также чтение/запись файлов. Все проверки используют память; файлы сохранений тесты не открывают и не создают. `FactoryPadSaveTests.cpp` подключает `SaveGameManager.cpp`, но вызывает сериализацию в памяти.

## 8. Версии формата и каталоги

В кодеке FORK1 менеджер передаёт ожидаемую `FormatVersion=2` (`src/save/SaveGameManager.hpp@9208dcf:22`; вызовы декодера `SaveGameManager.cpp@9208dcf:1384-1388,1504-1508`). `versions.tsv` показывает версию 1 для тегов `v0.8.0-ru-hd.3`–`.8` и версию 2 для `.9`, `.10` и FORK1.

Команда истории:

```text
git log --format='%h %ad %s' --date=short e17379ad660fca46859b403a6c3d33ec8d831a40..9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/save
```

Вывод:

```text
f2b5811e 2026-11-06 Protect factory pad references and keep every queued unit
9e8a65e3 2026-11-06 Save and load the factory pads, rolling units and waiting units
5c77e8f9 2026-11-02 U11: UI audit debug mode
d8bfe207 2026-08-05 Polish Russian localization
f1b8ea26 2026-08-04 Publish RU/HD remaster source and assets
```

Команда списка релизов вывела восемь тегов: `v0.8.0-ru-hd.10`, `.3`, `.4`, `.5`, `.6`, `.7`, `.8`, `.9`. Для каждого тега выполнено `git grep -n FormatVersion <тег> -- src/save`; строки константы и значения приведены в `versions.tsv`.

Команда файлов сохранений:

```text
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -i -E 'sav'
```

Вывод:

```text
src/save/SaveFileCodec.cpp
src/save/SaveFileCodec.hpp
src/save/SaveGameManager.cpp
src/save/SaveGameManager.hpp
src/save/SaveSlotName.hpp
src/save/SaveSlotsDialog.cpp
src/save/SaveSlotsDialog.hpp
tests/FactoryPadSaveTests.cpp
tests/SaveFileCodecTests.cpp
tests/SaveSlotNameTests.cpp
```

Каталог слотов FORK1 строится как относительный `saves/` (`SaveGameManager.cpp@9208dcf:1349-1359`); `main` берёт каталог EXE через `SDL_GetBasePath()` и устанавливает текущий каталог (`src/main.cpp@9208dcf:34-49,85`). Путь пользовательского `preferences.ini` в UP1 и PORT строится через `SDL_GetPrefPath("D2TM", "Dune II - The Maker")` (`src/game/PreferencesPath.cpp@d06f2fc:28-47`, `@0a33444:28-47`). Для Windows, Linux и macOS в этих местах нет отдельных ветвей путей: используются SDL-вызовы.

## Чтение

Полностью прочитан `/srv/dune/tasks/load-check/PORT_PLAN.md` отдельным вызовом `cat`; также выполнены обе заданные команды чтения `PORT_MAP.md` и `docs/decisions.md`. В плане прочитаны строка П8 раздела 4, содержание П8 и строка П8 раздела 6. Критериев чтения исходников, ограничений рамки или правил остановки для этой разведки в списке не недоставало: они заданы в тексте задания.

Дословная команда по решениям:

```text
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р(5|63)\.'
```

Она вывела строку Р63. Строка Р5 отдельно подтверждена командой `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | sed -n '13p'`: заголовок там `Р5 (В5).`, поэтому он не совпадает с шаблоном `Р5\.`.


Вывод команды чтения карты, относящийся к `save-slots`:

```text
| save-slots | Десять именованных сохранений и F5/F9 | README_AI §1 | rewrite | adaptive-layout, localization | Б8 | 25 |
### save-slots — Десять именованных сохранений и F5/F9
Перенести именованные слоты сохранений, диалог выбора и команды F5/F9.
Пути кода и тестов; судьба в UP1:
- src/save/SaveFileCodec.cpp — отсутствует
- src/save/SaveFileCodec.hpp — отсутствует
- src/save/SaveGameManager.cpp — отсутствует
- src/save/SaveGameManager.hpp — отсутствует
- src/save/SaveSlotName.hpp — отсутствует
- src/save/SaveSlotsDialog.cpp — отсутствует
- src/save/SaveSlotsDialog.hpp — отсутствует
- tests/SaveFileCodecTests.cpp — отсутствует
- tests/SaveSlotNameTests.cpp — отсутствует
```

Фрагмент реестра тестов из того же вывода: `tests/SaveFileCodecTests.cpp@9208dcf:23` → `save_file_codec_roundtrip` (`CMakeLists.txt:384`); `tests/SaveSlotNameTests.cpp@9208dcf:16` → `save_slot_name_handling` (`CMakeLists.txt:395`); `tests/FactoryPadSaveTests.cpp@9208dcf:219` → `factory_pad_save` (`tests/UnitRenderFixture.cmake:134`). Фрагмент риска: `SaveGameManager.cpp@9208dcf:9` включает старый `cGame.h`; API UP1 находится в `src/game/cGame.h@d06f2fc:89`.

Фактический вывод заданной команды `docs/decisions.md`:

```text
- **Р63. Волна 4 — перенос форка на свежий апстрим.** Графика и перерисовка закончены; задача волны — перенести всё на новый код апстрима, сохранив наработки форка (Р4). Новая база `UP1` — master апстрима в момент запуска первой задачи, `d06f2fcd` на 2026-11-09. Новые возможности апстрима (туман войны с памятью, значок нехватки энергии, предел юнитов, вступительный ролик, `preferences.ini`, папки музыки) берутся как есть; где новинка спорит с функцией форка, ведущий спрашивает владельца на шаге этой функции. Новых задач по графике нет; код и данные игры в `main` не меняются до перемотки на ветку порта, в `main` идут только документы процесса и карта переноса. Шаги П1–П15 — по карточке `codex-direct/launch-card-27.md`. Владелец, 2026-11-09, по карточке 27: «Свежий master», «Все как есть», «Мы закончили с графикой и перерисовкой. Теперь задача всё перенести на их новый код, сохранив наши наработки.»
```

Дополнительный вывод Р5 из строки 13 того же файла:

```text
- **Р5 (В5). Сохранения v0.8.0-ru-hd.7** после обновления объявляются несовместимыми; конвертер не пишем.
```

Команда списка тегов и полный вывод:

```text
git tag --list 'v0.8.0-ru-hd.*'
v0.8.0-ru-hd.10
v0.8.0-ru-hd.3
v0.8.0-ru-hd.4
v0.8.0-ru-hd.5
v0.8.0-ru-hd.6
v0.8.0-ru-hd.7
v0.8.0-ru-hd.8
v0.8.0-ru-hd.9
```
