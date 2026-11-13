## RECON-P5BR | 2026-11-10 16:44:07 UTC

Ревизии: `BASE= e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `PORT=616280c8926ec642d86144a9fe2db105ceaf4061`, `MAIN=62e1ff6585d8f1f047a3f983c63d990662e6afb6`. Перед командами Git задавался `PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## 1. Функции `cOptionsState` в FORK1

Полная таблица `.tmp/p5br/fork-functions.tsv` содержит 72 строки данных: 35 функций и методов из `src/gamestates/cOptionsState.cpp@9208dcf`, члены и вложенные объявления из `src/gamestates/cOptionsState.h@9208dcf`, включая `operator==`, поля `cOptionsState`, `width` и `height` вложенного `ResolutionOption`, типы `ResolutionOption` и `OptionsPage`, значения `Main`, `Gameplay`, `Controls`, `Diagnostics`. В таблице указаны диапазоны объявлений/определений, наличие одноимённой функции в BASE, метки и все совпадения запроса `git grep -n '<имя>(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src`. Диапазоны определений идут от `optionText` (`src/gamestates/cOptionsState.cpp@9208dcf:31-36`) до `refresh` (`src/gamestates/cOptionsState.cpp@9208dcf:1494-1510`); `operator==` объявлен в `src/gamestates/cOptionsState.h@9208dcf:47`.

Команда проверки функций BASE и вывод:

```text
git grep -n 'cOptionsState::' e17379ad660fca46859b403a6c3d33ec8d831a40 -- src/gamestates/cOptionsState.cpp
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:16:cOptionsState::cOptionsState(cGame &theGame, GameContext *ctx, int prevState)
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:26:void cOptionsState::constructWindow(int prevState)
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:218:cOptionsState::~cOptionsState()
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:223:void cOptionsState::thinkFast()
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:228:void cOptionsState::draw() const
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:239:void cOptionsState::onNotifyMouseEvent(const s_MouseEvent &event)
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:244:eGameStateType cOptionsState::getType()
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:249:void cOptionsState::onNotifyKeyboardEvent(const cKeyboardEvent &)
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:257:void cOptionsState::setPrevState(int prevState)
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:263:void cOptionsState::refresh()
```

Команда подсчёта и её вывод:

```text
/srv/dune/venv/bin/python -c 'import csv,collections,sys; rows=list(csv.DictReader(open(sys.argv[1],encoding="utf-8"),delimiter="\t")); funcs=[r for r in rows if "src/gamestates/cOptionsState.cpp@" in r["строки"] or r["функция"]=="operator=="]; counts=collections.Counter(t for r in funcs if r["метки"]!="-" for t in r["метки"].split(",")); print("функций/методов:",len(funcs)); print("с метками:",sum(r["метки"]!="-" for r in funcs)); print("без меток:",sum(r["метки"]=="-" for r in funcs)); print("метки:", ", ".join(f"{k}={counts[k]}" for k in ["lang","save","music","keys","render","world","layout","audit","hdui","theme"])); print("строк данных:",len(rows))' .tmp/p5br/fork-functions.tsv
функций/методов: 35
с метками: 27
без меток: 8
метки: lang=16, save=4, music=3, keys=14, render=12, world=9, layout=2, audit=0, hdui=0, theme=3
строк данных: 72
```

Корневая сверка выборки:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '31,36p'
31  std::string optionText(const GameSettings &settings,
32                         std::string_view english,
33                         std::string_view russian)
34  {
35      return std::string(settings.language == "en" ? english : russian);
36  }

git grep -n 'constructAdvancedWindow(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp:278:void cOptionsState::constructAdvancedWindow(int /*prevState*/)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp:763:        constructAdvancedWindow(prevState);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.h:89:    void constructAdvancedWindow(int prevState);

git grep -n 'cOptionsState::draw' e17379ad660fca46859b403a6c3d33ec8d831a40 -- src/gamestates/cOptionsState.cpp
e17379ad660fca46859b403a6c3d33ec8d831a40:src/gamestates/cOptionsState.cpp:228:void cOptionsState::draw() const
```

## 2. Раскладка в FORK1

`.tmp/p5br/layout.tsv` содержит 65 строк данных: структуры, поля, локальные константы и функции в `OptionsMenuLayout.hpp@9208dcf` и `AdvancedOptionsHeaderLayout.hpp@9208dcf`, их входы/выходы и места использования функций. `OptionsMenuLayout` имеет 13 полей; `create` принимает `canvasWidth`, `canvasHeight`, `buttonHeight`, `playing`, `titleFontHeight=-1` и возвращает геометрию окна и его элементов (`src/gamestates/OptionsMenuLayout.hpp@9208dcf:7-27`). `AdvancedOptionsHeaderLayout` содержит `title` и четыре `tabs`; её `create` принимает ширину окна, отступ, высоту кнопки и шрифта и возвращает заголовок и четыре прямоугольника вкладок (`src/gamestates/AdvancedOptionsHeaderLayout.hpp@9208dcf:7-20`). Все промежуточные формулы и вызовы функций перечислены в TSV.

Команды и вывод выборочной проверки полей, использования и CTest:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp | nl -ba | sed -n '7,20p'
7   struct OptionsMenuLayout {
8       cRectangle window;
9       cRectangle speedLabel;
10      cRectangle apply;
11      cRectangle advanced;
12      cRectangle status;
13      cRectangle save;
14      cRectangle load;
15      cRectangle missionSelect;
16      cRectangle mainMenu;
17      cRectangle quit;
18      cRectangle back;
19      int contentTop = 0;
20      int contentGap = 0;

git grep -n 'OptionsMenuLayout::create' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp:768:    const OptionsMenuLayout menuLayout = OptionsMenuLayout::create(

git grep -n 'AdvancedOptionsHeaderLayout::create' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src tests
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp:313:        AdvancedOptionsHeaderLayout::create(
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/InteractionRegressionTests.cpp:32:        AdvancedOptionsHeaderLayout::create(760, 8, 34, 24);

git grep -n 'options_menu_layout_geometry' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt
9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:236:    add_test(NAME options_menu_layout_geometry COMMAND options_menu_layout_tests)
```

`tests/OptionsMenuLayoutTests.cpp@9208dcf` не использует вызовы `assert` или других распознанных макросов проверки. Команда статического подсчёта и вывод:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/OptionsMenuLayoutTests.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); p=r"\b(?:assert|ASSERT_[A-Z_]+|EXPECT_[A-Z_]+|CHECK(?:_FALSE|_NOTHROW|_THROWS)?|REQUIRE(?:_FALSE|_NOTHROW|_THROWS)?)\s*\("; m=re.findall(p,s); print(f"check-macro invocations: {len(m)}"); print("matches:", ", ".join(m) if m else "(none)")'
check-macro invocations: 0
matches: (none)
```

Файл использует собственные группы проверок: `exact` сравнивает поля и прямоугольники с ожиданиями (`tests/OptionsMenuLayoutTests.cpp@9208dcf:151-168`); `table` сверяет фиксированные примеры (`:169-208`); `inside` проверяет границы холста и окна (`:209-233`); `header-spacing` проверяет отступ содержимого от заголовка (`:234-250`); `overlap` проверяет пересечения кнопок и девяти строк настроек (`:252-282`); `bh44` проверяет границы и пересечения при высоте кнопки 44 (`:341-349`), также вызывает `headerSpacing`, чей результат учитывается отдельной группой.

Заголовки и символы теста, проверенные в PORT: `gamestates/OptionsMenuLayout.hpp` и `OptionsMenuLayout` / `OptionsMenuLayout::create` — нет; `utils/RenderScale.hpp` — `src/utils/RenderScale.hpp@616280c:1`; `RenderCanvasSize`, `calculateRenderCanvasSize`, `AutomaticRenderScale`, `ManualRenderScales`, `isManualRenderScaleAvailable` — присутствуют по строкам в `layout.tsv`; `cRectangle` и `getX/getY/getWidth/getHeight` — `src/utils/cRectangle.h@616280c:21,51,57,63,66`. Стандартные заголовки теста `<algorithm>`, `<array>`, `<cstddef>`, `<iostream>`, `<string>`, `<string_view>` подключены в `tests/OptionsMenuLayoutTests.cpp@9208dcf:4-9`; как заголовки стандартной библиотеки они не являются файлами проекта. Команда проверки соответствующих include в исходниках PORT и её вывод:

```text
git grep -n -E '#include <(algorithm|array|cstddef|iostream|string|string_view)>' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src/main.cpp src/utils/RenderScale.hpp src/utils/RenderScale.cpp src/context/cGameObjectContext.h
616280c8926ec642d86144a9fe2db105ceaf4061:src/context/cGameObjectContext.h:19:#include <cstddef>
616280c8926ec642d86144a9fe2db105ceaf4061:src/main.cpp:29:#include <algorithm>
616280c8926ec642d86144a9fe2db105ceaf4061:src/main.cpp:30:#include <string>
616280c8926ec642d86144a9fe2db105ceaf4061:src/main.cpp:31:#include <string_view>
616280c8926ec642d86144a9fe2db105ceaf4061:src/main.cpp:33:#include <iostream>
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/RenderScale.cpp:3:#include <algorithm>
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/RenderScale.hpp:3:#include <array>
```

## 3. Масштабы

`.tmp/p5br/scales.tsv` содержит 40 строк данных с функциями, константами, входами/выходами, допустимыми значениями и тестовыми символами для FORK1 и PORT. В обеих ревизиях `RenderScale.hpp` задаёт `MinimumRenderWidth=800`, `MinimumRenderHeight=600`, `AutomaticRenderScale=0`, `ManualRenderScales={100,125,150,175,200}` (`src/utils/RenderScale.hpp@9208dcf:12-15`, `src/utils/RenderScale.hpp@616280c:12-15`). Для `renderScalePercent` допустимы 0 (Auto) и ручные 100/125/150/175/200%; ручные значения доступны, если выход позволяет сохранить минимум 800×600. Функции RenderScale и строки их реализаций приведены для обеих ревизий в TSV.

В FORK1 `AutomaticWorldScale=0`, `ManualWorldScales={100,110,125,150}` (`src/utils/WorldScale.hpp@9208dcf:5-6`); автоматический процент выбирается по высоте: 100 при высоте ≤768, 110 при ≤1080, 125 при ≤1600, иначе 150 (`src/utils/WorldScale.cpp@9208dcf:6-37`). В PORT `WorldScale.cpp` отсутствует; функции встроены в `src/utils/WorldScale.hpp@616280c:9-40`, добавлена `worldScaleZoom`. Допустимые значения `worldScalePercent` остаются 0 (Auto) и 100/110/125/150% в обеих ревизиях.

Подсчёт проверок тестов, команды и вывод:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/RenderScaleTests.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); n=len(re.findall(r"passed\s*&=\s*expectCanvas\(", s))+len(re.findall(r"^\s*if\s*\((?:calculateAutomaticRenderScalePercent|!isManualRenderScaleAvailable|isManualRenderScaleAvailable)", s, re.M)); print(n)'
11

git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldScaleTests.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); print(len(re.findall(r"passed\s*&=\s*expectEqual\(", s)))'
7

git show 616280c8926ec642d86144a9fe2db105ceaf4061:tests/utils/test_RenderScale.cpp | /srv/dune/venv/bin/python -c 'import re,sys; s=sys.stdin.read(); print(len(re.findall(r"\b(?:CHECK(?:_FALSE)?|REQUIRE)\s*\(", s)))'
49
```

`RenderScaleTests.cpp@9208dcf:36-43` проверяет восемь размеров canvas; оставшиеся проверки задают Auto=180% при 1920×1080, доступность 175% и недоступность 200% при этом выходе. `WorldScaleTests.cpp@9208dcf:20-26` проверяет пять автоматических высот, ручные 110% и переход неподдерживаемых 133% к Auto. `test_RenderScale.cpp@616280c` распределяет 49 макропроверок по четырём `TEST_CASE`: 4 константы, 13 размеров canvas, 12 автоматических процентов/доступности ручных значений, 20 чтения RenderScale и INI. Проверяются `RenderCanvasSize`, `calculateRenderCanvasSize`, `calculateAutomaticRenderScalePercent`, `isManualRenderScaleAvailable`, `calculateAutomaticWorldScalePercent`, `resolveWorldScalePercent` и `worldScaleZoom`; строки объявлений/реализаций и наличие каждого символа в PORT перечислены в `scales.tsv`.

Корневая сверка констант FORK1:

```text
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/RenderScale.hpp | nl -ba | sed -n '1,36p'
5   struct RenderCanvasSize {
9       bool operator==(const RenderCanvasSize &) const = default;
12  constexpr int MinimumRenderWidth = 800;
13  constexpr int MinimumRenderHeight = 600;
14  constexpr int AutomaticRenderScale = 0;
15  constexpr std::array<int, 5> ManualRenderScales{100, 125, 150, 175, 200};
17  [[nodiscard]] int calculateAutomaticRenderScalePercent(int outputWidth, int outputHeight);
18  [[nodiscard]] bool isManualRenderScaleAvailable(
23  [[nodiscard]] RenderCanvasSize calculateRenderCanvasSize(
```

## 4. Сохранение выбора

В FORK1 `saveDisplaySettings` находится в `src/gamestates/cOptionsState.cpp@9208dcf:707-758`; она обновляет выбранные значения, включая `RenderScale` и `WorldScale`, и вызывает `saveSettingsToIni("settings.ini", ...)` (`:728`). Запись выполняет `saveIniReplacements` (`src/utils/common.cpp@9208dcf:189-324`), меняя/добавляя ключи секции `[SETTINGS]`; `saveSettingsToIni` определена в `src/utils/common.cpp@9208dcf:350-387`. Цепочка записывает 30 ключей: `ScreenWidth`, `ScreenHeight`, `FullScreen`, `RenderScale`, `WorldScale`, `CameraDragMoveSpeed`, `CameraBorderOrKeyMoveSpeed`, `CameraEdgeMove`, `AllowRepeatingReinforcements`, `AllTurretsDownOnLowPower`, `RocketTurretsDownOnLowPower`, `GameRules`, `NoAI`, `Debug`, `playMusic`, `playSound`, `drawUnitDebug`, `oneAi`, `disableWormAi`, `disableReinforcements`, `noAiRest`, `drawUsages`, `pauseWhenLosingFocus`, `Language`, `KeyAttack`, `KeyRepair`, `KeyUnload`, `KeyDeploy`, `KeyRally`, `KeyRelease`. Для каждого чтения/записи, секции и ключа TSV указывает строку `src/utils/common.cpp@9208dcf`.

После успешной записи задаётся сообщение `Saved. Restart the game.` / `Сохранено. Перезапустите игру.` (`src/gamestates/cOptionsState.cpp@9208dcf:734-740`); оно добавляется в статус на `src/gamestates/cOptionsState.cpp@9208dcf:1362-1371` и рисуется окном вызовом `m_guiWindow->draw()` на `src/gamestates/cOptionsState.cpp@9208dcf:1416`. Таймер видимости отсутствует: сообщение остаётся до очистки обработчиком или пересоздания окна; явные очистки перечислены на `src/gamestates/cOptionsState.cpp@9208dcf:272-273, 531-532, 557-558, 570-571, 607-608, 620-621, 647-648, 1294-1295, 1301-1302`.

Основная кнопка «Применить» вызывает `saveDisplaySettings` (`src/gamestates/cOptionsState.cpp@9208dcf:1349-1360`). Кнопка «Применить» дополнительной страницы записывает `m_selectedSettings` и обновляет command bindings при успехе (`src/gamestates/cOptionsState.cpp@9208dcf:492-507`). Её «Назад» возвращает `OptionsPage::Main` (`src/gamestates/cOptionsState.cpp@9208dcf:508-517`). Кнопка «В главное меню» задаёт переход в `GAME_MENU` (`src/gamestates/cOptionsState.cpp@9208dcf:805-816`).

В PORT `src/game/Preferences.hpp@616280c:29,33,36` объявляет `readSettings`, `load`, `save`; `src/game/Preferences.cpp@616280c:25,45-128,147-197` использует секцию `SETTINGS`, читает и записывает ключи. Имя файла `preferences.ini` задаётся в `src/main.cpp@616280c:54`; загрузка с `-prefs` вызывается на `src/main.cpp@616280c:77-84`, сохранение после `game.run()` — на `src/main.cpp@616280c:113-117`. `Preferences::save` создаёт родительские каталоги, пишет временный `.tmp` и переименовывает файл (`src/game/Preferences.cpp@616280c:150-195`). `persistence.tsv` содержит строки чтения/записи всех 27 ключей чтения и 26 ключей записи. `RenderScale` читается и записывается; `WorldScale` читается (`src/game/Preferences.cpp@616280c:68-69`), но не записывается в `Preferences::save`. Поля `cGameSettings`: `m_worldScalePercent` и `m_renderScalePercent` (`src/game/cGameSettings.h@616280c:146-147`); `applySettings` записывает их из начальных настроек (`src/game/cGame_logic.cpp@616280c:303-304`), `currentSettings` читает обратно (`src/game/cGame_logic.cpp@616280c:352-353`). Действия `applyRenderScale` и `worldScaleZoom` также указаны в TSV.

Корневая сверка чтения/записи масштабов в PORT:

```text
git grep -n -E 'RenderScale|WorldScale' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src/game/Preferences.hpp src/game/Preferences.cpp
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/Preferences.cpp:65:    if (section.hasValue("RenderScale")) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/Preferences.cpp:66:        settings.renderScalePercent = section.getInt("RenderScale");
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/Preferences.cpp:68:    if (section.hasValue("WorldScale")) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/Preferences.cpp:69:        settings.worldScalePercent = section.getInt("WorldScale");
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/Preferences.cpp:163:    set(ini, "RenderScale", std::to_string(settings.renderScalePercent));
```

## 5. Меню настроек порта

`.tmp/p5br/port-options.tsv` содержит 31 строку: каждую функцию `cOptionsState` с диапазоном начала/конца и каждый GUI-объект меню с типом, надписью, формулой прямоугольника, темой, действием и строками в PORT. Реализации функций расположены в `src/gamestates/cOptionsState.cpp@616280c:39-379`; `constructWindow` создаёт окно и объекты на `:57-328`. В меню есть основные кнопки, параметры музыки/звука, скорости, тумана войны и значка низкой энергии; объектам, где тема задана, таблица указывает её, а для остальных — что она явно не задана. В текущем списке GUI-объектов меню нет элементов `RenderScale` или `WorldScale`.

Команда `git grep -n 'GAME_OPTIONS' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src` и полный вывод:

```text
git grep -n 'GAME_OPTIONS' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h:213:            case GAME_OPTIONS:
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h:214:                return "GAME_OPTIONS";
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1323:                               newState != GAME_OPTIONS); // don't delete these m_states, but re-use!
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1327:            delete m_states[GAME_OPTIONS];
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1328:            m_states[GAME_OPTIONS] = nullptr;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1333:            delete m_states[GAME_OPTIONS];
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1334:            m_states[GAME_OPTIONS] = nullptr;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1374:            else if (newState == GAME_OPTIONS) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1429:            else if (newState == GAME_OPTIONS) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1445:                if (m_state == GAME_OPTIONS) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2030:        game.setNextStateToTransitionTo(GAME_OPTIONS);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp:55:    {"options-menu", "GAME_OPTIONS", "cOptionsState"},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp:56:    {"options-game", "GAME_OPTIONS", "cOptionsState"},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp:58:    {"save-dialog", "GAME_OPTIONS", "SaveSlotsDialog"},
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp:189:            UiAuditAccess::setState(game, GAME_OPTIONS);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp:266:            UiAuditAccess::setState(game, GAME_OPTIONS);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cGameState.h:16:    GAMESTATE_OPTIONS,                      // #define GAME_OPTIONS	  5     // options menu
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cMainMenuState.cpp:168:        m_game.setNextStateToTransitionTo(GAME_OPTIONS);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:983:            m_game.setNextStateToTransitionTo(GAME_OPTIONS);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/include/definitions.h:66:#define GAME_OPTIONS	  5		 // options menu
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:284:                game.setNextStateToTransitionTo(GAME_OPTIONS);
```

Экран входа игрока: главное меню — `src/gamestates/cMainMenuState.cpp@9208dcf:167-169`; бой — `src/managers/cDrawManager.cpp@9208dcf:284-285`; выбор следующего завоевания — `src/gamestates/cSelectYourNextConquestState.cpp@9208dcf:979-985`.

Команда `git grep -n 'GAME_OPTIONS' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src` и полный вывод:

```text
git grep -n 'GAME_OPTIONS' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:952:            case GAME_OPTIONS: mapped = eGameState::OPTIONS; return true;
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:981:                               newState != GAME_OPTIONS); // don't delete these states, but re-use!
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:1024:        if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:1069:            else if (newState == GAME_OPTIONS) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:1082:            else if (newState == GAME_PLAYING && m_state == GAME_OPTIONS) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame_logic.cpp:1155:            else if (newState == GAME_OPTIONS) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/gamestates/cEditorState.cpp:513:            m_stateTransitions->setNextState(GAME_OPTIONS);
616280c8926ec642d86144a9fe2db105ceaf4061:src/gamestates/cGamePlaying.cpp:539:        m_stateTransitions->setNextState(GAME_OPTIONS);
616280c8926ec642d86144a9fe2db105ceaf4061:src/gamestates/cGameState.h:37:    GAMESTATE_OPTIONS,                      // #define GAME_OPTIONS	  5     // options menu
616280c8926ec642d86144a9fe2db105ceaf4061:src/gamestates/cMainMenuState.cpp:167:        m_stateTransitions->setNextState(GAME_OPTIONS);
616280c8926ec642d86144a9fe2db105ceaf4061:src/gamestates/cSelectYourNextConquestState.cpp:1044:            m_stateTransitions->setNextState(GAME_OPTIONS);
616280c8926ec642d86144a9fe2db105ceaf4061:src/include/eGameState.cpp:38:        case GAME_OPTIONS:
616280c8926ec642d86144a9fe2db105ceaf4061:src/include/eGameState.cpp:39:            return "GAME_OPTIONS";
616280c8926ec642d86144a9fe2db105ceaf4061:src/include/eGameState.h:53:inline constexpr int GAME_OPTIONS = 5;
616280c8926ec642d86144a9fe2db105ceaf4061:src/managers/cDrawManager.cpp:313:        m_stateTransitions->setNextState(GAME_OPTIONS);
```

В PORT переходы вызываются из главного меню (`src/gamestates/cMainMenuState.cpp@616280c:166-168`), боя (`src/gamestates/cGamePlaying.cpp@616280c:538-540` и `src/managers/cDrawManager.cpp@616280c:301-314`), редактора (`src/gamestates/cEditorState.cpp@616280c:506-514`) и экрана выбора следующего завоевания (`src/gamestates/cSelectYourNextConquestState.cpp@616280c:1040-1046`). Другие совпадения grep — диспетчеризация и обслуживание состояния.

## 6. Дополнительная страница форка

`constructAdvancedWindow` определена в `src/gamestates/cOptionsState.cpp@9208dcf:278-518`. `.tmp/p5br/advanced.tsv` содержит 53 созданных GUI-объекта: тип, надпись, действие нажатия, строки создания и маркеры из строк создания и обработчиков. В таблице отражены окно, четыре вкладки, условные страницы Gameplay/Controls/Diagnostics, нижние Apply/Back и сообщение захвата клавиши. Тексты кнопок локализуются; вкладки и Back запрашивают страницу, переключатели меняют настройку, ползунки задают значения, кнопки назначения запускают захват клавиши (Move отключена), Apply записывает настройки и обновляет command bindings при успехе. Строки создания и обработчиков проверяются по той же команде поиска функций `git grep -n '<имя>(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src`; конкретные строки и метки указаны в TSV. `AdvancedOptionsHeaderLayout::create` вызывается из `cOptionsState.cpp@9208dcf:313` и `InteractionRegressionTests.cpp@9208dcf:32`.

## Чтение

Прочитан целиком `/srv/dune/tasks/load-check/PORT_PLAN.md`; выполнена указанная команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '311,381p'`; выполнена указанная команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р(30|33|66)\.'` и получены три строки. По ссылкам самого плана прочитаны §3.2 и §5.3 `docs/PLAN_units_sega_upstream.md@62e1ff6`, а также целиком `codex-direct/launch-card-27.md@62e1ff6`, чтобы проверить описание этапа разведки, запрет проверок и правило запуска без новой карточки. Не хватало в задании: текста этих двух ссылочных источников; они прочитаны по причине прямой ссылки из PORT_PLAN. Других необходимых для разведки правил или контрактов, не указанных в задании, не выявлено.

## Не проверено

Сборки, CTest и запуск игры не выполнялись по запрету задания. Реальное применение сохранённых настроек после перезапуска не запускалось; сведения о чтении и записи установлены по коду и строкам, приведённым выше и в таблицах.
