# RECON-P7R

Рабочая копия: `/srv/dune/worktrees/u34`. Ревизии: `BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `UP1=d06f2fcd2a347182c3774fb96e9a85570405c489`, `PORT=0a33444e9032ef935dfe4cdde6bb622771484230`, `MAIN=62e1ff6585d8f1f047a3f983c63d990662e6afb6`. Команды чтения Git запускались после `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH` и с явными ревизиями.

## 1. Механизм языка в FORK1

Подробная таблица функций, структур, констант и изменённых участков, их входов, выходов и поведения: `.tmp/p7r/fork-mechanism.tsv` (43 строки данных). Для выделения изменений использована команда `git diff --unified=0 e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <путь>` по каждому из десяти заданных файлов. Вывод по каждому затрагивающему язык, интерфейсный текст или шрифты участку представлен соответствующими строками таблицы.

Состояние английского языка — `english` в `src/utils/Localization.hpp@9208dcf:11`, по умолчанию `false`. `setLanguage(std::string_view)` меняет состояние (`src/utils/Localization.hpp@9208dcf:13`); `text(const char*, const char*)` выбирает английский или русский литерал (`src/utils/Localization.hpp@9208dcf:18`); `isEnglish()` возвращает состояние (`:25`); `campaignRoot()` выбирает каталог кампании (`:30`); `format(const char*, const char*, Args&&...)` форматирует локализованный шаблон (`:36`). Проверка шрифта `ttfFontSupportsText(TTF_Font*, std::string_view)` описана в `src/utils/FontSupport.hpp@9208dcf:8`.

Вывод выборочной проверки сигнатур:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/Localization.hpp | nl -ba | sed -n '1,45p'
11 inline bool english = false;
13 inline void setLanguage(const std::string_view language)
18 [[nodiscard]] inline const char *text(
25 [[nodiscard]] inline bool isEnglish()
30 [[nodiscard]] inline const char *campaignRoot()
36 [[nodiscard]] inline std::string format(
```

Настройка `GameSettings.language` по умолчанию равна `ru` (`src/utils/GameSettings.hpp@9208dcf:31`). Ключ `Language` читается из ini в `src/utils/common.cpp@9208dcf:108`, записывается в `:379`, меняется настройкой языка в `src/gamestates/cOptionsState.cpp@9208dcf:644` и применяется через `localization::setLanguage` в `src/cGame_logic.cpp@9208dcf:185`. Элементы переключателя языка находятся в `src/gamestates/cOptionsState.cpp@9208dcf:1326`. Имена стандартных шрифтов в ini заданы в `resources/bin/settings.ini@9208dcf:79`.

## 2. Вызовы перевода в FORK1

Объявления `localization::text` и `localization::format` находятся в `src/utils/Localization.hpp@9208dcf:18` и `:36`. Строки интерфейса задаются парами английского и русского литералов непосредственно в вызовах; например, `src/cGame_logic.cpp@9208dcf:1963` и `src/drawers/cMouseDrawer.cpp@9208dcf:175`. Файлы данных кампаний расположены отдельно в каталогах `campaign/` и `campaign_en/`; загрузчики см. в пунктах 3 и 8.

Команда, требуемая заданием:

```sh
git grep -c -E 'localization::(text|format)' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
```

Её вывод считает совпавшие строки в каждом файле, а не отдельные вызовы:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:8
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseNormalState.cpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMousePlaceState.cpp:7
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:8
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:7
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMouseDrawer.cpp:16
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cOrderDrawer.cpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cAbstractStructure.cpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOrderProcesser.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cWindTrap.cpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:5
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cMainMenuState.cpp:9
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectMissionState.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:8
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:25
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cPreviewMaps.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:4
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AtreidesMentat.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/BeneMentat.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/HarkonnenMentat.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/OrdosMentat.cpp:2
9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.cpp:17
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveFileCodec.cpp:6
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveGameManager.cpp:39
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotName.hpp:1
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:9
9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/cBuildingListItem.cpp:7
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cIniGameRessouces.cpp:56
```

Подсчёт вхождений скриптом `/srv/dune/venv/bin/python .tmp/p7r/count_pairs.py` вывел:

```text
localization::text/format calls parsed: 291
calls with two literal language strings: 291
calls without two literal language strings: 0
distinct English/Russian pairs: 252
```

Итого — 291 вызов на 34 файлах; 281 строка с совпадением в выводе `git grep` (в десяти строках находится больше одного вызова); 252 разные пары. Подробности и наличие каждого файла в PORT находятся в `.tmp/p7r/fork-calls.tsv`.

## 3. Ресурсы

Список путей получен заданной командой:

```sh
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/port_inventory.json | /srv/dune/venv/bin/python -c "import json,sys; d=json.load(sys.stdin); [print(k) for k,v in d['paths'].items() if 'localization' in v.get('features',[]) and k.startswith('resources/bin/')]"
```

Вывод: 136 путей `resources/bin/`; все имена и построчные статусы `BASE`→`FORK1`, размеры объектов, наличие LFS, существование и совпадение в PORT, язык приведены в `.tmp/p7r/resources.tsv`.

Сводка таблицы рассчитана командой `/srv/dune/venv/bin/python .tmp/p7r/count_resource_summary.py`. Вывод:

```text
rows 136
Git object bytes 705333
статус BASE→FORK1 {'A': 72, 'M': 63, 'D': 1}
Git LFS {'нет': 133, 'да': 2, 'нет объекта': 1}
размер содержимого Git LFS {'-': 134, '396212': 1, '39124': 1}
есть в PORT {'нет': 72, 'да': 64}
объект совпадает {'нет пути': 72, 'нет': 64}
язык {'по имени не определён': 8, 'ru': 65, 'en': 63}
```

Старый путь `resources/bin/skirmish/4PL_SinéadPlains.ini` удалён/переименован и отсутствует как объект FORK1; ASCII-путь `resources/bin/skirmish/4PL_SineadPlains.ini` отражён отдельно. Команда `git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- 'resources/bin/skirmish/4PL_Sin*'` вывела:

```text
R099 "resources/bin/skirmish/4PL_Sin\303\251adPlains.ini" resources/bin/skirmish/4PL_SineadPlains.ini
```

`git cat-file -e 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/skirmish/4PL_SinéadPlains.ini` вывела `fatal: path ... does not exist` (код 128). Каталог `skirmish/` загружается кодом `src/map/cPreviewMaps.cpp@9208dcf:201`; там же выбираются каталоги карт по языку и передаются ini-файлы в загрузчик. `campaign/` и `campaign_en/` выбираются через `src/utils/Localization.hpp@9208dcf:30` и читаются в `src/ini.cpp@9208dcf:420`; брифинги строятся/открываются в `src/ini.cpp@9208dcf:1271` и `:1282`. Параметры ресурсов и шрифтов читаются из `settings.ini` (`src/cGame_logic.cpp@9208dcf:1017`, `:1043`; `resources/bin/settings.ini@9208dcf:30`, `:79`). Загрузка TTF выполняется в `src/context/ContextCreator.cpp@9208dcf:73` и `:88`.

Для `PTSansNarrow-Regular.ttf` команда `git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/PTSansNarrow-Regular.ttf` вывела LFS-указатель с `size 396212`; для `RussoOne-Regular.ttf` такой же вывод указывает `size 39124`. Объекты содержимого присутствуют в локальном LFS-каталоге, их размеры совпадают с `size` указателей. Полные oid и все строки путей приведены в TSV.

Поиск кода, который ссылается на лицензионные файлы ресурсов, выполнен командой `git grep -n -i -E 'OFL_PT_FONTS|README_RU|OFL_RUSSO_ONE|Sangyo-LICENSE|Sangyo-COPYRIGHT' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src`; вывод пустой, код 1. Поиск `git grep -n -i 'RunttiSP' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src` также вывел пустой результат.

## 4. Сборка

Команда фильтрации каталога второго уровня для `tools/`:

```sh
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/port_inventory.json | /srv/dune/venv/bin/python -c "import json,sys; d=json.load(sys.stdin); [print(k) for k,v in d['paths'].items() if 'localization' in v.get('features',[]) and k.startswith('tools/')]"
```

Вывод: `tools/check_skirmish_and_mentat_ui.py`. Сопоставление CMake зависимостей SDL2_ttf с SDL3_ttf в PORT, цель `font_coverage_tests`, её define и отсутствие соответствия в PORT, а также этот tool приведены в `.tmp/p7r/build.tsv`. В FORK1 связывание SDL2_ttf находится в `CMakeLists.txt@9208dcf:43`, `:88`, `:92`; в PORT SDL3_ttf найдено в `CMakeLists.txt@0a33444:51`, `:142`. FORK1 регистрирует `russian_font_coverage` в `CMakeLists.txt@9208dcf:345`; соответствующей цели в PORT нет. `tools/check_skirmish_and_mentat_ui.py@9208dcf:9` и `:16` проверяет подписи меню карт; `:27` читает файлы skirmish; `:41` проверяет текст Ментата. В PORT инструмент отсутствует.

## 5. Текст и шрифты в PORT и изменения UP1

Таблица `.tmp/p7r/port-text.tsv` содержит 50 строк: публичные сигнатуры методов восьми заданных файлов PORT, загрузку шрифтов, вызовы SDL3_ttf и существенные участки diff `BASE`→`UP1`. Дифф получен командой:

```sh
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/context/TextContext.hpp src/context/TextContext.cpp src/context/ContextCreator.hpp src/context/ContextCreator.cpp src/drawers/cTextDrawer.h src/drawers/cTextDrawer.cpp src/drawers/cTextTextureCache.h src/drawers/cTextTextureCache.cpp
```

Выборочная проверка сигнатур `TextContext` в PORT:

```text
git show 0a33444e9032ef935dfe4cdde6bb622771484230:src/context/TextContext.hpp | nl -ba | sed -n '20,45p'
24 TextContext(std::unique_ptr<cTextDrawer> smallTextDrawer,
25     std::unique_ptr<cTextDrawer> beneTextDrawer,
26     std::unique_ptr<cTextDrawer> gameTextDrawer);
29 ~TextContext();
31 void resetCache() const;
33 cTextDrawer* getSmallTextDrawer() const;
34 cTextDrawer* getBeneTextDrawer() const;
35 cTextDrawer* getGameTextDrawer() const;
```

В PORT код получает `arrakeen.fon`, `benegess.fon` и `small.ttf` из `GameDir` (`resources/bin/settings.ini@0a33444:90`, `:91`, `:92`), загружает их через `TTF_OpenFont` (`src/context/ContextCreator.cpp@0a33444:78`, `:86`, `:94`) и закрывает через `TTF_CloseFont` (`:105`, `:106`, `:107`). `TTF_GetStringSize` вызывается в `src/drawers/cTextDrawer.cpp@0a33444:71`, `:81`, `:106`, `:127`, `:143`, `:151`; `TTF_GetFontHeight` — там же на строке `:136`; `TTF_RenderText_Solid` вызывается в `src/drawers/cTextTextureCache.cpp@0a33444:49`, `:58`. Подробности и сигнатуры указаны в `port-text.tsv`.

## 6. Файлы шрифтов и кириллица

Команды из задания:

```sh
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- resources/bin | grep -i -E '\.(ttf|otf)$'
```

Вывод FORK1:

```text
resources/bin/data/PTMono-Regular.ttf
resources/bin/data/PTSansNarrow-Regular.ttf
resources/bin/data/RunttiSP-Bold.otf
resources/bin/data/RussoOne-Regular.ttf
resources/bin/data/Sangyo-Regular.otf
resources/bin/data/arrak.ttf
resources/bin/data/benegess.ttf
resources/bin/data/small.ttf
```

```sh
git ls-tree -r --name-only 0a33444e9032ef935dfe4cdde6bb622771484230 -- resources/bin | grep -i -E '\.(ttf|otf)$'
```

Вывод PORT:

```text
resources/bin/data/arrak.ttf
resources/bin/data/benegess.ttf
resources/bin/data/small.ttf
```

Одноразовый скрипт стандартной библиотеки `.tmp/p7r/assets_recon.py` командой `/srv/dune/venv/bin/python .tmp/p7r/assets_recon.py --fonts` читает sfnt `cmap` каждого файла и проверяет U+0401, U+0410–U+044F и U+0451 (66 точек). Полный результат с Git-размером, LFS-размером, объектами и списком отсутствующих точек находится в `.tmp/p7r/fonts.tsv`. Пять шрифтов FORK1 содержат 66/66; `arrak.ttf`, `benegess.ttf` и `small.ttf` содержат 0/66. В PORT есть только эти три файла, у каждого 0/66; все три объекта совпадают с FORK1.

Команды корневой выборочной проверки `PTSansNarrow-Regular.ttf`:

```sh
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/PTSansNarrow-Regular.ttf
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/PTSansNarrow-Regular.ttf
/srv/dune/venv/bin/python -c "import sys; sys.path.insert(0,'.tmp/p7r'); import assets_recon as a; lfs,size,first,data=a.font_content(a.FORK,'resources/bin/data/PTSansNarrow-Regular.ttf'); found,missing=a.cmap_points(data); print('lfs',lfs,'size',size,'cmap_found',found,'missing',missing)"
```

Вывод: `131`; LFS-указатель содержит `size 396212`; анализ вывел `lfs да size 396212 cmap_found 66 missing []`. Проверка `git rev-parse` объекта `resources/bin/data/arrak.ttf` в FORK1 и PORT вывела одинаковый oid `5998e37f18dd7a093b8b5cb2294524b6821eafb9`.

## 7. Тесты

FORK1 регистрирует CTest-цель `font_coverage_tests` с именем `russian_font_coverage` (`CMakeLists.txt@9208dcf:331`, `:345`). Скрипт `.tmp/p7r/count_font_checks.py` был запущен так:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/FontCoverageTests.cpp | /srv/dune/venv/bin/python .tmp/p7r/count_font_checks.py
```

Вывод:

```text
russianRequired=94 serviceSymbols=5 textCriteria=2 logicalChecks=101 TTF_GlyphIsProvided32_calls=104 ttfFontSupportsText_calls=3
```

Тест проверяет 94 обязательных глифа Sangyo, 5 сервисных глифов в Sangyo или PTMono, поддержку русской метки и fallback для `150%`. Он читает `resources/bin/data/Sangyo-Regular.otf` и `resources/bin/data/PTMono-Regular.ttf` (`tests/FontCoverageTests.cpp@9208dcf:18`, `:21`); пак не открывает, LFS-указателей в этих объектах нет. Символы и заголовки, результат их наличия в PORT и места чтения файлов перечислены в `.tmp/p7r/tests.tsv`.

В PORT тесты Catch2 подключаются `catch_discover_tests(d2tm_tests PROPERTIES SKIP_RETURN_CODE 4)` (`tests/CMakeLists.txt@0a33444:95`). `git grep -n -i -E 'ttf|font' 0a33444e9032ef935dfe4cdde6bb622771484230 -- tests` вывела пустой результат (код 1). Команда `git grep -l -E 'localization::(setLanguage|text|isEnglish|campaignRoot|format)' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests` также вывела пустой результат (код 1). В FORK1 нет других тестовых файлов с вызовами функций перевода.

## 8. Тексты кампаний

Полная таблица `.tmp/p7r/campaign-texts.tsv` содержит 72 строки данных: 54 файла текстов кампаний Атрейдес, Харконнен и Ордос в FORK1 (RU и EN) и по 9 файлов кампании Сардаукаров в UP1 и PORT. Искались непустые player-facing значения `Text=`. Команды поиска в UP1 и PORT:

```sh
git grep -l -E '^Text=' d06f2fcd2a347182c3774fb96e9a85570405c489 -- resources/bin/campaign/briefings/mentats.ini resources/bin/campaign/sardaukar
git grep -l -E '^Text=' 0a33444e9032ef935dfe4cdde6bb622771484230 -- resources/bin/campaign/briefings/mentats.ini resources/bin/campaign/sardaukar
```

Вывод команды поиска в UP1:

```text
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/briefings/mentats.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission1.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission2.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission3.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission4.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission5.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission6.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission7.ini
d06f2fcd2a347182c3774fb96e9a85570405c489:resources/bin/campaign/sardaukar/mission8.ini
```

Вывод команды поиска в PORT содержит те же девять путей с префиксом `0a33444e9032ef935dfe4cdde6bb622771484230:`. `git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- resources/bin/campaign/briefings/mentats.ini resources/bin/campaign/sardaukar` вывела статус `A` для всех девяти файлов; `git diff --name-status d06f2fcd2a347182c3774fb96e9a85570405c489 0a33444e9032ef935dfe4cdde6bb622771484230 -- resources/bin/campaign/briefings/mentats.ini resources/bin/campaign/sardaukar` вывела пустой результат (код 0). Текст английский. В `mentats.ini` 310 строк; в миссиях 1–8 соответственно 3, 3, 2, 2, 1, 1, 1, 1 строки. Числа и выводы подсчёта для каждого файла записаны в TSV.

UP1 вызывает загрузку описания Дома в `src/gamestates/cTellHouseState.cpp@d06f2fc:84`, брифинга/победы/поражения в `src/gamestates/cMentatState.cpp@d06f2fc:96`, `:114`, `:133`, а региональных файлов миссий — в `src/gamestates/cSelectYourNextConquestState.cpp@d06f2fc:514`. Фактическое открытие файлов в PORT: `src/utils/ini.cpp@0a33444:83`, `:353`, `:358` и `src/utils/IniParsing.cpp@0a33444:360`, `:640`.

В FORK1 тексты кампаний Атрейдес, Харконнен и Ордос лежат в `resources/bin/campaign/` и `resources/bin/campaign_en/`: по восемь `mission*.ini` и файл брифинга для каждого Дома. Загрузка миссий/брифингов задаётся `src/ini.cpp@9208dcf:420`, `:1276`, `:1282`, корень языка — `src/utils/Localization.hpp@9208dcf:30`. Скрипт `/srv/dune/venv/bin/python .tmp/p7r/emit_campaign_tsv.py` вывел `rows=72 fork1_files=54 sardaukar_files=18`. Команда `/srv/dune/venv/bin/python -c "import csv; rows=list(csv.DictReader(open('.tmp/p7r/campaign-texts.tsv',encoding='utf-8'),delimiter='\\t')); a=[r for r in rows if r['revision']=='FORK1' and r['house']=='Atreides']; print('Atreides RU',sum(int(r['text_rows']) for r in a if r['language']=='RU')); print('Atreides EN',sum(int(r['text_rows']) for r in a if r['language']=='EN'))"` вывела `Atreides RU 262` и `Atreides EN 346`. Построчный вывод подсчёта по каждому файлу находится в `campaign-texts.tsv`.

## Чтение

До начала работы отдельными командами прочитаны:

- `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_PLAN.md` — в строке 62 план связывает П7 с localization, зависимостью от П5 и вопросом о переводе кампании Сардаукаров; строка 92 задаёт RU/EN и приёмку `font_coverage_tests` плюс скриптовую проверку строк; строка 124 задаёт вопрос владельцу о переводе.
- Заданная команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '9,36p;467,529p'` — строка 21 описывает функцию localization и её зависимость/шаг; строки 467–528 перечисляют кодовые пути и 136 путей ресурсов и один tool.
- Заданная команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р63\.'` — одна строка Р63 закрепляет перенос на UP1 и принятие новых возможностей апстрима как есть.
- По ссылкам плана прочитаны `docs/PLAN_units_sega_upstream.md` целиком (команда `git show ...:docs/PLAN_units_sega_upstream.md`, дочитана частями после предупреждения об обрезанном выводе) и `codex-direct/launch-card-27.md` целиком. Причина: план ссылается на §3.2/§5.3 для процесса переноса и приёмки, а карточка 27 фиксирует UP1 и порядок П1–П15. Дополнительной нормы или контракта, на которые опирается эта разведка и которых не хватало бы после чтения этих ссылок, не обнаружено.

## Ограничения выполнения

Файлы рабочей копии вне `.tmp/p7r/` не менялись. Коммитов нет. Сборки, CTest и запуск игры не выполнялись по прямому запрету задания.
