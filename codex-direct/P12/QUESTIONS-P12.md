# Вопросы ведущему к заданию P12

Ревизии: `B` = `0d186e8b1894d37091b31c362cecffa95ffadb4e`, `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`, `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489`. В `TASK-P12.md` записан выбор по умолчанию (первый вариант каждого вопроса); ответ меняет названные пункты контракта.

## Q-P12-01. Как Linux-пакет получает SDL3

Не решено: платформенный архив Linux содержит только `d2tm` и `INSTALL.txt` (как у форка), но SDL3 в Ubuntu 24.04 нет в репозиториях.

Факты:
- `install_dependencies_ubuntu.sh@B:5` — «SDL3 is not in Ubuntu 24.04 standard repos, so we build it from source»; теги `release-3.4.10`, `release-3.4.4`, `release-3.2.2`, `release-3.2.4` (строки 42, 48, 54, 60).
- `CMakeLists.txt@B:81-88` — SDL3 подключается как `find_package`, `link_libraries(SDL3 SDL3_ttf SDL3_mixer SDL3_image)`; `git grep -i rpath B -- CMakeLists.txt src/CMakeLists.txt` — ноль строк, значит бинарник ищет `libSDL3.so` по обычным путям.
- `packaging/LINUX_README.txt@FORK1:7-11` — форк требовал `apt-get install libsdl2-*` (у SDL2 пакеты в Ubuntu есть).
- `release.yml@FORK1:226-229` ставит `libsdl2-dev` из репозитория; для порта такого пакета нет, SDL3 в задании собирается скриптом `install_dependencies_ubuntu.sh` в `/usr/local`.

Варианты:
- A (по умолчанию в задании). Игрок сам собирает SDL3 по тегам из `INSTALL.txt`. Следствие: Linux-архив крошечный, но запустить его может только тот, кто умеет собрать четыре библиотеки; `release.yml` не меняется.
- B. В архив кладутся `libSDL3*.so*`, `libSDL3_image*.so*`, `libSDL3_ttf*.so*`, `libSDL3_mixer*.so*` из `/usr/local/lib` (список из `ldd build/d2tm`) в папку `lib/`, а `RUNPATH` бинарника ставится `patchelf --set-rpath '$ORIGIN/lib'` (в задание `linux` добавляются шаги `sudo apt-get install -y patchelf` и копирование; `LINUX_README.txt` теряет шаг 1). Следствие: игрок ничего не ставит; растёт архив и шаги задания; нужна проверка в сухом прогоне (`ldd` после `patchelf`).
- C. Статическая сборка SDL3 или AppImage. Следствие: правки `CMakeLists.txt` и скриптов, вне объёма П12.

## Q-P12-02. Обновлять ли снимки галереи

Не решено: пять PNG форка показывают вид форка, порт после П5–П11 выглядит иначе (адаптивные меню, настройки, панель музыки).

Факты:
- `gallery.tsv` и `RECON.md` §4: 5 PNG, 2 049 636–4 450 212 байт, ссылки `README.md@FORK1:10,15,16,23,24`; в `B` снимков нет.
- Задание брифа: «переносятся как есть»; обновление — вопрос владельцу.
- Снимки делает только Claude (Р70, «Визуал делает только Claude»).

Варианты:
- A (по умолчанию). Перенос как есть; снимки обновляются позже. Следствие: галерея в `README.md` до обновления показывает вид форка, не порта.
- B. Новые пять снимков делает ведущий на сборке порта до PR П12 (те же имена файлов, те же подписи). Следствие: шаг П12 ждёт снимков; `sha256` в пункте 12 контракта и в C12 заменяются на новые.
- C. Новые снимки на шаге П13 (эталонные снимки старой и новой сборки), `README.md` правится там. Следствие: П12 сливается с прежними снимками.

## Q-P12-03. Абзац о шрифтах и `README_AI.md` («паспорт форка»)

Не решено: что в `README.md` вместо абзаца о Sangyo и что делать с паспортом форка.

Факты:
- `README.md@FORK1:38-40` — «Russian interface uses Sangyo Regular»; папка `resources/bin/data/licenses` (`Sangyo-COPYRIGHT.txt`, `Sangyo-LICENSE.txt`, `RunttiSP-ReadMe.pdf`) есть в `FORK1`, в `B` нет.
- `resources/bin/settings.ini@B` — `[FONT]` `ARRAKEEN=PTSansNarrow-Regular.ttf`, `BENEGESS=PTSansNarrow-Regular.ttf`, `SMALL=RussoOne-Regular.ttf`; запасной `PTMono-Regular.ttf` (`src/context/ContextCreator.cpp:102@B`); лицензии — `resources/bin/OFL_PT_FONTS.txt`, `resources/bin/data/OFL_RUSSO_ONE.txt` в `B`.
- `README_AI.md@FORK1` — 38 013 байт, описывает SDL2, `build-ru\`, пути на ПК владельца (`C:\Users\Slaven\Documents\Codex\...`), ссылается на `resources/bin/README_RU.txt`; в `B` его нет; `README.md@FORK1:48-50` ссылается на него; `PORT_MAP.md` (раздел `author-gallery`) называет его «паспорт FORK1».

Варианты:
- A (по умолчанию). Абзац о шрифтах переписан под шрифты порта (пункт 11 контракта); `README_AI.md` не переносится, ссылка на него в `README.md` не вносится. Следствие: паспорта в порту нет до отдельной задачи.
- B. Абзац пишет владелец (дать текст).
- C. `README_AI.md` переносится как есть. Следствие: паспорт описывает SDL2 и пути ПК владельца, то есть неверен для порта.
- D. Паспорт переписывается под порт отдельной задачей (кто и когда — решает ведущий).

## Q-P12-04. `README_RU.txt` и `THIRD_PARTY_ASSETS_RU.txt` в пакете

Не решено: два файла форка из `resources/bin` попадают в пакет форка (`cp -a resources/bin/.`, `release.yml@FORK1:106`), в `B` их нет; карта (`port_inventory.json`, `release-packaging`) относит их к функции.

Факты:
- `resources/bin/README_RU.txt@FORK1:1` — «Dune II — The Maker v0.8.0-ru4-preview4»; описывает секцию `[HD4_DATAFILE]` и ключ `WorldScale`, которых нет в `resources/bin/settings.ini@B` (там `[DATAFILE]`, масштаб — `RenderScale`).
- `resources/bin/THIRD_PARTY_ASSETS_RU.txt@FORK1:1-5` — «D2TM v0.8.0-ru4», «локальной, неопубликованной и некоммерческой»; перечисляет источники спрайтов (Spriters Resource, Sega Retro) и Russo One.
- В `B` есть только `resources/bin/OFL_PT_FONTS.txt` и `resources/bin/data/OFL_RUSSO_ONE.txt`.

Варианты:
- A (по умолчанию). Не переносятся; пакет без русского README и без списка источников графики. Следствие: игрок не видит ссылок на источники спрайтов.
- B. `THIRD_PARTY_ASSETS_RU.txt` переносится с правкой строки о «локальной, неопубликованной» сборке (текст пишет ведущий), `README_RU.txt` не переносится.
- C. Оба файла пишет владелец заново под порт (дать тексты; отдельная правка в `resources/bin`, пакет подхватит копией).

## Q-P12-05. `create_release.sh` и `create_release.bat`

Не решено: сценарии, которые вызывает `build_master.yml` (на пуш в `master`), собирают пакет, с которым порт не запустится; форк свой `create_release.sh` менял.

Факты:
- `create_release.sh@B:33` — `cp resources/bin/data/*.dat bin/data` (классические паки в пакете, Р34); `:37` — `cp resources/bin/data/scenes/*.* bin/data/scenes` (не копирует `scenes/hd4`); `music`, `data/hd4`, `campaign_ru`, `windowed.bat` не копируются; `create_release.bat@B:32,36` — то же.
- `create_release.sh@FORK1:30-38` — форк перешёл на `sdl_audio.dat`, `*_hd4.dat`, `scenes/hd4`, `data/hd4`; `music` и `sdl_gfxeditor.dat` форк-сценарий тоже не копирует.
- `build_master.yml@B:3-6` — триггер `push` в `master`; основная ветка репозитория — `main`, так что workflow не срабатывает.
- `release.yml@FORK1` эти сценарии не вызывает.

Варианты:
- A (по умолчанию). Сценарии и `build_master.yml` не меняются. Следствие: в репозитории остаются сценарии с неверным составом; на выпуски по тегу это не влияет.
- B. Оба сценария переписываются вызовом `packaging/make_common_assets.sh` плюс копирование исполняемого файла и DLL. Следствие: добавляются два файла в рамку П12; для `.bat` нужна проверка на Windows.
- C. Сценарии и `build_master.yml` удаляются как мёртвые. Следствие: правка вне решений Р63 и вне объёма карты.

## Q-P12-06. Текст `RELEASE_NOTES.md`

Не решено: формулировка заметок к выпуску порта; раздел `Highlights` и номер выпуска — на шаге «Релиз».

Факты:
- `packaging/RELEASE_NOTES.md@FORK1:6-20` — `Highlights in v0.8.0-ru-hd.10` про рисунки зданий, неприменимо к порту; строки 37–40 — SDL2; строки 42–43 — ссылка на `README_AI.md`.
- Р78: сохранения `v0.8.0-ru-hd.9` и `hd.10` несовместимы, старый файл помечен как повреждённый, папка `saves` рядом с игрой; Р79: 22 трека в `music`.
- Текст пункта 8 контракта (без раздела `Highlights`, с фразой о несовместимости сохранений) составлен по этим фактам; формулировку «releases that predate this SDL3 build» ведущий не согласовывал.

Варианты:
- A (по умолчанию). Текст пункта 8; `Highlights` и номер — на шаге «Релиз».
- B. Ведущий присылает готовый английский текст заметок до запуска; пункт 8 заменяется им дословно.

## Q-P12-07. DLL Windows-архива

Не решено: шаг `Package Windows binary and DLLs` копирует всю папку `resources/dll` и DLL из `ldd`; в папке есть лишнее.

Факты:
- `release.yml@FORK1:188-195` — `cp resources/dll/*.dll package/`, затем DLL из `/mingw64/bin/`, найденные `ldd` (копируются поверх одноимённых).
- `resources/dll@B` (19 файлов): `SDL3.dll`, `SDL3_image.dll`, `SDL3_mixer.dll`, `SDL3_ttf.dll`, `libavif-16.dll`, `libgme.dll`, `libogg-0.dll`, `libopus-0.dll`, `libopusfile-0.dll`, `libpng16-16.dll`, `libtiff-6.dll`, `libwavpack-1.dll`, `libwebp-7.dll`, `libwebpdemux-2.dll`, `libwebpmux-3.dll`, `libwinpthread-1.dll`, `libxmp.dll`, `msvcr70.dll`, `msvcr70d.dll`.
- Какие из них нужны собранному бинарнику, решает `ldd` в CI; `msvcr70*.dll` порту не нужны.

Варианты:
- A (по умолчанию). Как у форка: вся папка плюс DLL из `ldd`. Следствие: в архиве лишние DLL (в том числе `msvcr70d.dll`, отладочная библиотека), возможна несовместимость версий, если `ldd` не перекрывает файл.
- B. Только DLL из `ldd`. Следствие: из шага удаляется строка `cp resources/dll/*.dll package/`; сухой прогон Windows на сервере невозможен, результат виден только после запуска workflow.

## Заметка (не вопрос)

В брифе «четыре прочих workflow» — в `B` их четыре с `claude-code-review.yml`, после его удаления три; в задании записано три.
