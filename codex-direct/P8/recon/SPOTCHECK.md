# Выборочная сверка RECON.md (P8R)

Ревизии (полные SHA):
- FORK1 `9208dcf` = `9208dcf5a358f40afd95c99480e4e09f781ed566`
- PORT `0a33444` = `0a33444e9032ef935dfe4cdde6bb622771484230`
- UP1 `d06f2fc` = `d06f2fcd2a347182c3774fb96e9a85570405c489`

Все команды выполнены из `C:/Users/Slaven/Projects/DUNE` (`git -C C:/Users/Slaven/Projects/DUNE show <sha>:<путь> | sed -n '<строка>p'`). Репозиторий не изменён.

| № | пункт | утверждение (кратко) | команда | вывод (до 2 строк) | совпало/не совпало |
|---|---|---|---|---|---|
| 1 | 1 | `FormatVersion = 2` в SaveGameManager.hpp:22 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.hpp \| sed -n '22p'` | `static constexpr int FormatVersion = 2;` | совпало |
| 2 | 1 | максимум 16 MiB в SaveGameManager.cpp:43 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp \| sed -n '43p'` | `constexpr std::size_t MaximumSaveBytes = 16U * 1024U * 1024U;` | совпало |
| 3 | 2 | `bool m_skirmish` в PORT, cGameSettings.h:166 | `git -C C:/Users/Slaven/Projects/DUNE show 0a33444e9032ef935dfe4cdde6bb622771484230:src/game/cGameSettings.h \| sed -n '166p'` | `bool m_skirmish;` | совпало |
| 4 | 2 | четыре направления cUnit в FORK1 имеют тип `int` (146–149) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.h \| sed -n '146,149p'` | `int iBodyFacing;`, `int iHeadFacing;`, `int iBodyShouldFace;`, `int iHeadShouldFace;` | совпало |
| 5 | 3 | `bCarryMe` и `iCarryAll` в PORT, cUnit.h:165–166 | `git -C C:/Users/Slaven/Projects/DUNE show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gameobjects/units/cUnit.h \| sed -n '165,166p'` | `bool bCarryMe;` / `int  iCarryAll;` | совпало |
| 6 | 3 | `iPrimaryBuilding` и `iStructures` в PORT, cPlayer.h:640–641 | `git -C C:/Users/Slaven/Projects/DUNE show 0a33444e9032ef935dfe4cdde6bb622771484230:src/gameobjects/players/cPlayer.h \| sed -n '640,641p'` | `int iPrimaryBuilding[MAX_STRUCTURETYPES] = {};` / `int iStructures[MAX_STRUCTURETYPES] = {};` | совпало |
| 7 | 4 | F5 вызывает `hasKey(SDL_SCANCODE_F5)`, cGame_logic.cpp:2042 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp \| sed -n '2042p'` | `if (event.hasKey(SDL_SCANCODE_F5) &&` | совпало |
| 8 | 4 | F9 вызывает `hasKey(SDL_SCANCODE_F9)`, cGame_logic.cpp:2057 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp \| sed -n '2057p'` | `if (event.hasKey(SDL_SCANCODE_F9)) {` | совпало |
| 9 | 5 | `PREFERENCES_FILE = "preferences.ini"` в UP1, main.cpp:54 | `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/main.cpp \| sed -n '54p'` | `constexpr const char *PREFERENCES_FILE = "preferences.ini";` | совпало |
| 10 | 5 | ключ `ScalingMode` читается в UP1, Preferences.cpp:66 | `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/game/Preferences.cpp \| sed -n '66p'` | `settings.scalingMode = section.getStringValue("ScalingMode") == "Letterbox"` | совпало по ключу; тип `eScalingMode` и значение `IntegerScale` на этой строке не видны (строка сравнивает с `"Letterbox"`) |
| 11 | 6 | `settings.ini` загружается при старте, main.cpp:92 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp \| sed -n '92p'` | `std::unique_ptr<GameSettings> settings = loadSettingsFromIni("settings.ini");` | совпало |
| 12 | 6 | текущим каталогом становится каталог EXE, main.cpp:85 (и `SDL_GetBasePath` в 34–49) | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp \| sed -n '85p'` (и `sed -n '34,49p'`) | `useExecutableDirectoryAsWorkingDirectory();`; в 34–49: `char *basePath = SDL_GetBasePath();` | совпало |
| 13 | 7 | регистрация теста `save_file_codec_roundtrip`, CMakeLists.txt:384 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt \| sed -n '384p'` | `add_test(NAME save_file_codec_roundtrip COMMAND save_file_codec_tests)` | совпало |
| 14 | 7 | регистрация теста `save_slot_name_handling`, CMakeLists.txt:395 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt \| sed -n '395p'` | `add_test(NAME save_slot_name_handling COMMAND save_slot_name_tests)` | совпало |
| 15 | 8 | каталог `saves` относительный; слот 1 — `quicksave.d2s`, остальные `saveNN.d2s`, SaveGameManager.cpp:1349–1359 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp \| sed -n '1349,1359p'` | `return std::filesystem::path("saves") / "quicksave.d2s";` / `std::format("save{:02}.d2s", slot);` | совпало |
| 16 | 8 | вызов декодера с `FormatVersion`, SaveGameManager.cpp:1384–1388 | `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp \| sed -n '1384,1388p'` | `const save_file::DecodeResult decoded = save_file::decode(` / `contents, FormatVersion, MaximumSaveBytes` | совпало |
| N1 | 1 и 2 | «Поля всего: 147» | Команда отчёта — `/srv/dune/venv/bin/python` на servak, полного текста команды в отчёте нет. Локально для сверки: `awk 'NR>1 && NF>0' codex-direct/P8/recon/save-fields.tsv \| wc -l` (не команда отчёта) | Строк данных в save-fields.tsv: 147. Сумма категорий 102+4+41 = 147 | не проверено, нужна среда servak |
| N2 | 7 | `SaveFileCodecTests.cpp`: 5 checks | Скрипт из отчёта (python, `git show 9208dcf…:tests/…`), запущен локально (Python 3.13.3) | `tests/SaveFileCodecTests.cpp: 5 checks (1 round-trip condition + 4 expectFailure calls)`. Вызовы `expectFailure(`: строки 42, 48, 54, 60 (определение — строка 7). Round-trip: encode/decode/сравнение в строках 30–35. «+1» в скрипте — константа, не счётчик | совпало |
| N3 | 7 | `SaveSlotNameTests.cpp`: 10 checks | Скрипт из отчёта, локально | `tests/SaveSlotNameTests.cpp: 10 checks (10 expect calls)`. `grep -c` даёт 11 — включая определение `expect(` в строке 7; вызовы в строках 19–54 — 10 | совпало |
| N4 | 7 | `FactoryPadSaveTests.cpp`: 23 checks | Скрипт из отчёта, локально | `tests/FactoryPadSaveTests.cpp: 23 checks (23 check calls)`. `grep -c` даёт 24 — включая определение `check(` в строке 12 | совпало |

Итог: 19 из 19 совпало (16 фактов и 3 числа N2–N4). Не проверено: 1 (N1, «147», нужна среда servak).

Примечания:
- Пункт 12 — замена. Исходная выборка `resources/bin/settings.ini@0a33444:133` была моей ошибкой: в отчёте для `RenderScale` строки не приведено. По выводу `git show` строка 133 у этого файла — `SELECT_SAME_TYPE_ON_SCREEN=Ctrl,Z`, а `RenderScale=0` стоит на строке 12. Выборка заменена на `src/main.cpp@9208dcf:85`.
- Строка 10 подтверждает чтение ключа `ScalingMode`; тип и значение по умолчанию в отчёте относятся к другим строкам файла и этим проверкой не покрыты.
- Арифметика пункта 1: 102 + 4 + 41 = 147, что сходится с заявленной суммой категорий.
