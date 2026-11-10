# Задание P5B — меню настроек (шаг П5б)

Исполнитель: корневая нить Codex `gpt-6-luna` `xhigh`; правки и прогоны делают субагенты `gpt-6-luna` `xhigh` по разделу «Организация работы». План работы — раздел `## PLAN-P5B` этого задания; он написан ведущим и выполняется дословно, свой план не пиши.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5b`, `HEAD` — коммит ведущего с приёмочными тестами P5BT поверх вершины ветки порта `832c953a94a632d57872349013f7ed1a37434715`. Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5b/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

Ревизия форка: `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`, релиз `v0.8.0-ru-hd.10`. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Цель

Меню настроек порта получает раскладку окна форка `OptionsMenuLayout` и две строки форка: «Масштаб игры» (`RenderScale`) и «Размер объектов» (`WorldScale`). Кнопка «Apply» записывает выбор в `preferences.ini`; выбор вступает в силу после перезапуска игры. Приёмочные тесты `[P5B]` и все остальные тесты проходят без изменений.

## Что уже решено

- **Строки окна.** Строка `n` окна стоит на высоте `contentTop + (n - 1) * (buttonHeight + contentGap)` раскладки `OptionsMenuLayout`, как в форке:

  | строка | содержимое |
  |---|---|
  | 1 | музыка: флажок и громкость |
  | 2 | звуки: флажок и громкость |
  | 3 | скорость игры |
  | 4 | туман войны (флажок порта) |
  | 5 | «Масштаб игры»: `<`, значение, `>` |
  | 6 | «Размер объектов»: `<`, значение, `>` |
  | 7 | значок нехватки энергии (флажок порта) |
  | 8 | пусто — строка языка шага П7 |
  | 9 | надпись режима читов порта (только в режиме читов) |

- **Кнопки внизу окна** — по прямоугольникам `OptionsMenuLayout`: «Main menu», «Quit game», «Back»; в бою (`m_prevState == GAME_PLAYING`) ещё ряд «Save game», «Load game», «Mission select». «Save game» и «Load game» неактивны до шага П8; «Mission select» показывается по условию порта. Кнопка «More settings» неактивна до шага П10. Неактивная кнопка — тема `GuiTheme::RemasterInactive()` и `withEnabled(false)`, как кнопки «Load» и «Hall of Fame» главного меню порта.
- **Тексты** — английские до шага П7.
- **Сохранение выбора.** «Apply» сразу записывает два ключа в `preferences.ini` функцией `Preferences::saveScales` и показывает «Saved. Restart the game.». Идущая игра работает с прежними масштабами до перезапуска. Запись всех настроек при выходе из игры (`src/main.cpp`) пишет выбранные в меню масштабы. При каждом запуске игра читает два ключа масштаба из `preferences.ini` функцией `Preferences::loadScales`, с ключом `-prefs` и без него; остальные ключи `preferences.ini` — как в порту, только с `-prefs` (решение владельца Р69).
- **Приёмочные тесты уже написаны и заморожены:** `tests/utils/test_OptionsMenu.cpp`, `tests/utils/test_Preferences.cpp` и `tests/CMakeLists.txt`, хэши — в `.tmp/p5bt/tests.sha256`. Эти три файла не меняются. Ведущий сверил девять тестов `[P5B]` с контрактом API ниже и противоречий не нашёл. Если при проверке 2 тест падает и причина — ошибка в самом тесте (тест противоречит контракту API), — блок `## Q-P5B-03` по проверке 2 и стоп.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `tests/utils/test_OptionsMenu.cpp` и `tests/utils/test_Preferences.cpp` — приёмочные тесты шага;
- `src/gamestates/cOptionsState.h`, `src/gamestates/cOptionsState.cpp`;
- `src/game/Preferences.hpp`, `src/game/Preferences.cpp`, `src/game/PreferencesPath.hpp`, `src/main.cpp`;
- `src/game/cGameSettings.h`, `src/game/cSDLSystem.h`;
- строки 295–360 и 755–780 файла `src/game/cGame_logic.cpp`;
- `src/utils/RenderScale.hpp`, `src/utils/WorldScale.hpp`;
- строки 100–200 файла `src/gamestates/cMainMenuState.cpp` — кнопки с темой `GuiTheme::Remaster()` и неактивные кнопки;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp | sed -n '760,1385p'` — окно настроек форка, геометрия строк.

## Контракт API

1. **Раскладка окна настроек (новый файл).** `src/gamestates/OptionsMenuLayout.hpp` — дословная копия одноимённого файла ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566` (команда `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp`). В нём структура `OptionsMenuLayout`: поля `window`, `speedLabel`, `apply`, `advanced`, `status`, `save`, `load`, `missionSelect`, `mainMenu`, `quit`, `back` типа `cRectangle`, поля `contentTop` и `contentGap` типа `int`, статический метод `create(int canvasWidth, int canvasHeight, int buttonHeight, bool playing, int titleFontHeight = -1)`.
2. **Списки масштабов (новые файлы).** `src/utils/ScaleChoices.hpp`:
   ```cpp
   #pragma once

   #include <cstddef>
   #include <string>
   #include <vector>

   [[nodiscard]] std::vector<int> renderScaleChoices(int outputWidth, int outputHeight);
   [[nodiscard]] std::vector<int> worldScaleChoices();
   [[nodiscard]] std::size_t scaleChoiceIndex(const std::vector<int> &choices, int scalePercent);
   [[nodiscard]] std::string scaleChoiceText(int scalePercent, int automaticScalePercent);
   ```
   - `renderScaleChoices`: первый элемент — `AutomaticRenderScale` (0); за ним значения массива `ManualRenderScales` из `src/utils/RenderScale.hpp` в порядке массива — только те, для которых `isManualRenderScaleAvailable(outputWidth, outputHeight, <значение>)` возвращает `true`.
   - `worldScaleChoices`: первый элемент — `AutomaticWorldScale` (0); за ним все значения массива `ManualWorldScales` из `src/utils/WorldScale.hpp` в порядке массива. Результат — `{0, 100, 110, 125, 150}`.
   - `scaleChoiceIndex`: индекс первого элемента `choices`, равного `scalePercent`; если равного нет — 0.
   - `scaleChoiceText`: при `scalePercent` = 0 — `std::format("Auto ({}%)", automaticScalePercent)`; при любом другом `scalePercent` — `std::format("{}%", scalePercent)`.
   - Реализация — `src/utils/ScaleChoices.cpp`. В `src/CMakeLists.txt` строка `utils/ScaleChoices.cpp` стоит сразу после строки `utils/RenderScale.cpp`.
3. **Файл настроек игрока.** `src/game/Preferences.hpp` и `src/game/Preferences.cpp`, пространство имён `Preferences`:
   - константа `inline constexpr const char *FILE_NAME = "preferences.ini";` в `Preferences.hpp`;
   - функция `save` дополнительно записывает ключ `WorldScale` со значением `std::to_string(settings.worldScalePercent)`; строка записи стоит сразу после строки записи ключа `RenderScale`; остальное в `save` не меняется;
   - поведение функции `load` не меняется: она уже читает ключи `RenderScale` и `WorldScale` (`readSettings`, `src/game/Preferences.cpp`, строки 65–70 ревизии `832c953a94a632d57872349013f7ed1a37434715`), поле, ключа которого в секции `SETTINGS` нет, не меняет и файл, в секции `SETTINGS` которого только два ключа масштаба, загружает с результатом `true`;
   - новая функция `bool saveScales(const std::filesystem::path &file, int renderScalePercent, int worldScalePercent, std::string &error);` Записывает в секцию `SETTINGS` файла `file` ключ `RenderScale` со значением `std::to_string(renderScalePercent)` и ключ `WorldScale` со значением `std::to_string(worldScalePercent)`. Если файл `file` существует, `cIniFile` его загружает и в нём есть секция `SETTINGS`, все остальные ключи секции `SETTINGS` сохраняют свои значения. Иначе после записи в секции `SETTINGS` только эти два ключа. Каталог файла создаётся; запись — через временный файл `<file>.tmp` и переименование, как в `save`. При ошибке — `false` и текст ошибки в `error`; иначе `true`;
   - новая функция `bool loadScales(const std::filesystem::path &file, InitialGameSettings &settings, std::string &error);` Если файла `file` нет, `cIniFile` его не загружает или в нём нет секции `SETTINGS` — `false`, текст ошибки в `error`, `settings` не меняется. Иначе: есть ключ `RenderScale` — `settings.renderScalePercent` получает его целое значение; есть ключ `WorldScale` — `settings.worldScalePercent` получает его целое значение; другие поля `settings` не меняются; результат `true`.

## PLAN-P5B

План ведущего. Шаги 1–3 — дорожка A, шаги 4–7 — дорожка B, шаги 8–9 — дорожка C, шаг 10 — дорожка D (раздел «Организация работы»). Пути — от корня рабочей копии. Номера строк — файлов ревизии `832c953a94a632d57872349013f7ed1a37434715`.

| № | Файл | Что сделать | Кто делает |
|---|---|---|---|
| 1 | `src/gamestates/OptionsMenuLayout.hpp` (новый) | `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp > src/gamestates/OptionsMenuLayout.hpp`. Файл не правится. | субагент A |
| 2 | `src/utils/ScaleChoices.hpp`, `src/utils/ScaleChoices.cpp` (новые), `src/CMakeLists.txt` | Заголовок — текст пункта 2 контракта дословно. В `.cpp` подключения `utils/ScaleChoices.hpp`, `utils/RenderScale.hpp`, `utils/WorldScale.hpp`, `<format>`; четыре функции — по пункту 2 контракта. В `src/CMakeLists.txt` строка `utils/ScaleChoices.cpp` с тем же отступом — сразу после строки `utils/RenderScale.cpp`. | субагент A |
| 3 | `src/game/Preferences.hpp`, `src/game/Preferences.cpp` | В `Preferences.hpp` внутри пространства имён `Preferences`: константа `FILE_NAME` пункта 3 контракта — первой строкой пространства имён; объявления `saveScales` и `loadScales` с однострочным комментарием каждое, по образцу соседних объявлений, — сразу после объявления `save`. В `Preferences.cpp`, в анонимном пространстве имён после функции `set`, две функции: `bool loadIni(const std::filesystem::path &file, cIniFile &ini, std::string &error)` — строки 132–136 и 139–142 функции `load` (проверка существования, загрузка в параметр `ini`, проверка секции, те же тексты ошибок), затем `return true;`; `bool writeIni(const cIniFile &ini, const std::filesystem::path &file, std::string &error)` — строки 149–154 функции `save` (создание каталога) и строки 184–196 (комментарий, временный файл, переименование, `return true`). `load`: `cIniFile ini; if (!loadIni(file, ini, error)) { return false; } readSettings(ini.getSection(SECTION), settings); return true;`. `save`: строки создания каталога убираются; после строки записи `RenderScale` строка `set(ini, "WorldScale", std::to_string(settings.worldScalePercent));`; вместо строк 184–196 — `return writeIni(ini, file, error);`. `saveScales`: `cIniFile loaded; std::string loadError; cIniFile fresh; cIniFile &ini = loadIni(file, loaded, loadError) ? loaded : fresh;`, затем `set(ini, "RenderScale", std::to_string(renderScalePercent));`, `set(ini, "WorldScale", std::to_string(worldScalePercent));`, `return writeIni(ini, file, error);`. `loadScales`: `cIniFile ini; if (!loadIni(file, ini, error)) { return false; }`, `const cSection section = ini.getSection(SECTION);`, по ключу `RenderScale` и ключу `WorldScale` — `if (section.hasValue(<ключ>)) { <поле> = section.getInt(<ключ>); }` как в `readSettings`, `return true;`. | субагент A |
| 4 | `src/main.cpp` | Строка 54 (`constexpr const char *PREFERENCES_FILE = "preferences.ini";`) удаляется; два вызова `PreferencesPath::file(PREFERENCES_FILE)` получают аргумент `Preferences::FILE_NAME`. Сразу перед строкой 76 (комментарий `// -prefs: …`) блок:<br>`// the scales chosen in the options menu apply on every start, the other preferences only with -prefs`<br>`if (const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME)) {`<br>`    std::string scalesError;`<br>`    Preferences::loadScales(*prefsFile, *settings, scalesError);`<br>`}`<br>с отступом окружающего кода. | субагент B |
| 5 | `src/game/cSDLSystem.h` | Сразу перед методом `OutputHeight()` метод `int OutputWidth() const { return outputResolution.width; }` в том же оформлении, что `OutputHeight()`. | субагент B |
| 6 | `src/game/cGameSettings.h` | Открытые методы сразу после метода `getScreenH()`, в оформлении соседних методов: `int getOutputW() const` — `m_outputW`; `int getOutputH() const` — `m_outputH`; `int getSavedRenderScalePercent() const` — `m_savedRenderScalePercent`; `int getSavedWorldScalePercent() const` — `m_savedWorldScalePercent`; `void setSavedScalePercents(int renderScalePercent, int worldScalePercent)` — присваивает два поля. Закрытые поля сразу после поля `int m_outputH = 0;`: `int m_outputW = 0;`, затем строка комментария `// written to preferences.ini; the running game keeps m_renderScalePercent and m_worldScalePercent until restart`, затем `int m_savedRenderScalePercent = 0;` и `int m_savedWorldScalePercent = 0;`. | субагент B |
| 7 | `src/game/cGame_logic.cpp` | `cGame::applySettings`: сразу после строки `m_gameSettings->m_renderScalePercent = gs->renderScalePercent;` строка `m_gameSettings->setSavedScalePercents(gs->renderScalePercent, gs->worldScalePercent);`. `cGame::currentSettings`: `gs.renderScalePercent = m_gameSettings->getSavedRenderScalePercent();` и `gs.worldScalePercent = m_gameSettings->getSavedWorldScalePercent();` вместо строк 352–353. Сразу перед строкой `m_gameSettings->m_outputH = m_Screen->OutputHeight();` строка `m_gameSettings->m_outputW = m_Screen->OutputWidth();`. | субагент B |
| 8 | `src/gamestates/cOptionsState.h` | Подключения `<cstddef>` и `<vector>` сразу после `#include <memory>`; объявления `class GuiButton;` и `class GuiLabel;` сразу после `class GuiWindow;`. Закрытые поля сразу после `int m_prevState;`: `std::vector<int> m_renderScaleChoices;`, `std::vector<int> m_worldScaleChoices;`, `std::size_t m_selectedRenderScaleIndex = 0;`, `std::size_t m_selectedWorldScaleIndex = 0;`, `GuiLabel *m_renderScaleValueLabel = nullptr;`, `GuiLabel *m_worldScaleValueLabel = nullptr;`, `GuiLabel *m_statusLabel = nullptr;`, `GuiButton *m_applyButton = nullptr;`. Закрытые методы сразу после `void constructWindow(int prevState);`: `void selectRenderScale(int step);`, `void selectWorldScale(int step);`, `void updateScaleControls();`, `void applyScaleSettings();`. | субагент C |
| 9 | `src/gamestates/cOptionsState.cpp` | По пунктам 9а–9д ниже. | субагент C |
| 10 | — | Проверки 1–5 раздела «Проверки» дословно. | субагент D |

### Шаг 9 — `src/gamestates/cOptionsState.cpp`

**9а. Подключения** — после имеющихся: `gamestates/OptionsMenuLayout.hpp`, `gui/GuiTheme.hpp`, `game/Preferences.hpp`, `game/PreferencesPath.hpp`, `utils/Log.h`, `utils/RenderScale.hpp`, `utils/WorldScale.hpp`, `utils/ScaleChoices.hpp`, `<algorithm>`.

**9б. Конструктор.** Сразу перед строкой `refresh();` четыре строки:
```cpp
    m_renderScaleChoices = renderScaleChoices(m_settings->getOutputW(), m_settings->getOutputH());
    m_worldScaleChoices = worldScaleChoices();
    m_selectedRenderScaleIndex = scaleChoiceIndex(m_renderScaleChoices, m_settings->getSavedRenderScalePercent());
    m_selectedWorldScaleIndex = scaleChoiceIndex(m_worldScaleChoices, m_settings->getSavedWorldScalePercent());
```

**9в. `refresh`.** Сразу после строки `m_guiWindow.reset();` строки `m_renderScaleValueLabel = nullptr;`, `m_worldScaleValueLabel = nullptr;`, `m_statusLabel = nullptr;`, `m_applyButton = nullptr;`.

**9г. `constructWindow`.** Тело функции (строки 59–327) заменяется. Начало тела:
```cpp
    const int margin = 8;
    const int buttonHeight = std::max(32, m_textDrawer->getFontHeight() + 10);
    const OptionsMenuLayout menuLayout = OptionsMenuLayout::create(
        m_settings->getScreenW(),
        m_settings->getScreenH(),
        buttonHeight,
        m_prevState == GAME_PLAYING,
        m_textDrawer->getFontHeight()
    );
    const GuiTheme controlTheme = GuiTheme::Remaster();
    const GuiRenderKind buttonKind = GuiRenderKind::REMASTER_BUTTON;
    const int contentX = 24;
    const int audioLabelWidth = 110;
    const int audioCheckX = 138;
    const int volumeLabelX = 218;
    const int volumeLabelWidth = 110;
    const int audioSliderX = 350;
    const int audioSliderWidth = 250;
    const int checkLabelWidth = 220;
    const int checkX = 252;
    const int displayLabelWidth = 160;
    const int arrowWidth = 46;
    const int selectorX = 198;
    const int scaleValueWidth = 200;
```
затем строки 784–795 окна форка дословно (`contentRowStride`, лямбды `contentRowY` и `relativeRect`); затем `m_guiWindow = std::make_unique<GuiWindow>(m_sdlDrawer, menuLayout.window, m_textDrawer);`, `m_guiWindow->setTheme(controlTheme);`, строки 72–73 порта (`audioContext`, `soundPlayer`) и строка 76 порта (заголовок окна). Затем объекты по таблице, в порядке её строк; `rowY(n)` в таблице — `contentRowY(n)`, `bh` — `buttonHeight`, `rect(x, y, w, h)` — `m_guiWindow->getRelativeRect(x, y, w, h)`.

Объект, у которого в столбце «код порта» указаны строки, переносится строками порта из этого диапазона с такими изменениями и только с ними:
- строка объявления прямоугольника `const cRectangle &<имя> = m_guiWindow->getRelativeRect(…);` (у объекта 6 — строки 144–145) становится `const cRectangle &<то же имя> = <значение столбца «прямоугольник»>;`;
- в цепочке построителя аргумент `withLabel` — значение столбца «надпись», если оно задано;
- аргумент `withTheme` — значение столбца «тема», если оно задано; если вызова `withTheme` в цепочке нет, он добавляется;
- аргумент `withKind` — значение столбца «вид», если оно задано; если вызова `withKind` в цепочке нет, он добавляется;
- вызов `withTextAlign` из столбца «прочее» добавляется, если его в цепочке нет;
- строки, которые столбец «прочее» называет непереносимыми, не переносятся.

Все остальные строки диапазона (условие `if` и закрывающая скобка, `withTextDrawer`, `withRenderer`, `onClick`, `onCheck`, `onUnCheck`, `withMinValue`, `withMaxValue`, `withInitialValue`, `onValueChanged`, переменные `timeManager` и `convertedForSlider`, вызовы `setChecked`, `addGuiObject`) сохраняются без изменений. Объект без строк порта строится цепочкой `withRect`, `withLabel` (если надпись задана), `withTextDrawer(m_textDrawer)`, `withRenderer(m_sdlDrawer)`, `withTheme`, `withKind` и вызовами столбца «прочее» и добавляется `m_guiWindow->addGuiObject(std::move(<объект>))`; указатель для поля класса берётся `.get()` до этого вызова.

| № | объект | код порта | прямоугольник | надпись | тема | вид | прочее |
|---|---|---|---|---|---|---|---|
| 1 | `gui_btn_toMenu` | 81–92 | `relativeRect(menuLayout.mainMenu)` | `"Main menu"` | `controlTheme` | `buttonKind` | — |
| 2 | `gui_btn_Quit` | 110–122 | `relativeRect(menuLayout.quit)` | `"Quit game"` | `controlTheme` | `buttonKind` | — |
| 3 | `gui_btn_Back` | 126–138 | `relativeRect(menuLayout.back)` | `"Back"` | `controlTheme` | `buttonKind` | — |
| 4 | `saveButton` | — | `relativeRect(menuLayout.save)` | `"Save game"` | `GuiTheme::RemasterInactive()` | `buttonKind` | `withEnabled(false)`; объекты 4 и 5 — внутри `if (m_prevState == GAME_PLAYING)` |
| 5 | `loadButton` | — | `relativeRect(menuLayout.load)` | `"Load game"` | `GuiTheme::RemasterInactive()` | `buttonKind` | `withEnabled(false)` |
| 6 | `gui_btn_toMissionSelect` | 140–157 | `relativeRect(menuLayout.missionSelect)` | `"Mission select"` | `controlTheme` | `buttonKind` | строки 142–143 порта (`rows`, `toMissionSelect`) не переносятся |
| 7 | `gui_cheatLabel` | 94–105 | `rect(contentX, rowY(9), checkLabelWidth, bh)` | — | — | — | `withTextAlign(GuiTextAlignHorizontal::LEFT)` |
| 8 | `gui_MusicLabel` | 158–166 | `rect(contentX, rowY(1), audioLabelWidth, bh)` | — | `controlTheme` | — | — |
| 9 | `gui_MusicCheckLabel` | 168–180 | `rect(audioCheckX, rowY(1), bh, bh)` | — | `controlTheme` | — | — |
| 10 | `gui_MusicVolumeLabel` | 182–190 | `rect(volumeLabelX, rowY(1), volumeLabelWidth, bh)` | — | `controlTheme` | — | — |
| 11 | `gui_sld_musicVolumeRect` | 192–203 | `rect(audioSliderX, rowY(1), audioSliderWidth, bh)` | — | `controlTheme` | — | — |
| 12 | `gui_SoundLabel` | 205–213 | `rect(contentX, rowY(2), audioLabelWidth, bh)` | — | `controlTheme` | — | — |
| 13 | `gui_SoundCheckLabel` | 215–227 | `rect(audioCheckX, rowY(2), bh, bh)` | — | `controlTheme` | — | — |
| 14 | `gui_SoundVolumeLabel` | 229–237 | `rect(volumeLabelX, rowY(2), volumeLabelWidth, bh)` | — | `controlTheme` | — | — |
| 15 | `gui_sld_soundVolumeRect` | 239–250 | `rect(audioSliderX, rowY(2), audioSliderWidth, bh)` | — | `controlTheme` | — | — |
| 16 | `gui_DifficultyLabel` | 252–260 | `relativeRect(menuLayout.speedLabel)` | `"Game speed"` | `controlTheme` | — | — |
| 17 | `gui_sld_speedRect` | 262–277 | `rect(audioCheckX, rowY(3), 220, bh)` | — | `controlTheme` | — | — |
| 18 | `gui_FogOfWarLabel` | 279–288 | `rect(contentX, rowY(4), checkLabelWidth, bh)` | — | `controlTheme` | — | — |
| 19 | `gui_FogOfWarCheckLabel` | 290–302 | `rect(checkX, rowY(4), bh, bh)` | — | `controlTheme` | — | — |
| 20 | `renderScaleLabel` | — | `rect(contentX, rowY(5), displayLabelWidth, bh)` | `"Game scale"` | `controlTheme` | `GuiRenderKind::TRANSPARENT_WITHOUT_BORDER` | `withTextAlign(GuiTextAlignHorizontal::LEFT)` |
| 21 | `previousRenderScaleButton` | — | `rect(selectorX, rowY(5), arrowWidth, bh)` | `"<"` | `controlTheme` | `buttonKind` | `onClick([this]() { selectRenderScale(-1); })` |
| 22 | `renderScaleValueLabel` | — | `rect(selectorX + arrowWidth + margin, rowY(5), scaleValueWidth, bh)` | `""` | `controlTheme` | `GuiRenderKind::OPAQUE_WITH_BORDER` | указатель — в `m_renderScaleValueLabel` |
| 23 | `nextRenderScaleButton` | — | `rect(selectorX + arrowWidth + margin + scaleValueWidth + margin, rowY(5), arrowWidth, bh)` | `">"` | `controlTheme` | `buttonKind` | `onClick([this]() { selectRenderScale(1); })` |
| 24 | `worldScaleLabel` | — | `rect(contentX, rowY(6), displayLabelWidth, bh)` | `"Object size"` | `controlTheme` | `GuiRenderKind::TRANSPARENT_WITHOUT_BORDER` | `withTextAlign(GuiTextAlignHorizontal::LEFT)` |
| 25 | `previousWorldScaleButton` | — | `rect(selectorX, rowY(6), arrowWidth, bh)` | `"<"` | `controlTheme` | `buttonKind` | `onClick([this]() { selectWorldScale(-1); })` |
| 26 | `worldScaleValueLabel` | — | `rect(selectorX + arrowWidth + margin, rowY(6), scaleValueWidth, bh)` | `""` | `controlTheme` | `GuiRenderKind::OPAQUE_WITH_BORDER` | указатель — в `m_worldScaleValueLabel` |
| 27 | `nextWorldScaleButton` | — | `rect(selectorX + arrowWidth + margin + scaleValueWidth + margin, rowY(6), arrowWidth, bh)` | `">"` | `controlTheme` | `buttonKind` | `onClick([this]() { selectWorldScale(1); })` |
| 28 | `gui_LowPowerIconLabel` | 304–313 | `rect(contentX, rowY(7), checkLabelWidth, bh)` | — | `controlTheme` | — | — |
| 29 | `gui_LowPowerIconCheck` | 315–327 | `rect(checkX, rowY(7), bh, bh)` | — | `controlTheme` | — | — |
| 30 | `applyButton` | — | `relativeRect(menuLayout.apply)` | `"Apply"` | `controlTheme` | `buttonKind` | `onClick([this]() { applyScaleSettings(); })`; указатель — в `m_applyButton` |
| 31 | `statusLabel` | — | `relativeRect(menuLayout.status)` | `""` | `controlTheme` | `GuiRenderKind::TRANSPARENT_WITHOUT_BORDER` | `withTextAlign(GuiTextAlignHorizontal::LEFT)`; указатель — в `m_statusLabel` |
| 32 | `advancedButton` | — | `relativeRect(menuLayout.advanced)` | `"More settings"` | `GuiTheme::RemasterInactive()` | `buttonKind` | `withEnabled(false)` |

Последняя строка тела — `updateScaleControls();`.

**9д. Новые методы** — сразу после `constructWindow`, дословно:
```cpp
void cOptionsState::selectRenderScale(int step)
{
    const int count = static_cast<int>(m_renderScaleChoices.size());
    m_selectedRenderScaleIndex = static_cast<std::size_t>((static_cast<int>(m_selectedRenderScaleIndex) + step + count) % count);
    m_statusLabel->setText("");
    updateScaleControls();
}

void cOptionsState::selectWorldScale(int step)
{
    const int count = static_cast<int>(m_worldScaleChoices.size());
    m_selectedWorldScaleIndex = static_cast<std::size_t>((static_cast<int>(m_selectedWorldScaleIndex) + step + count) % count);
    m_statusLabel->setText("");
    updateScaleControls();
}

void cOptionsState::updateScaleControls()
{
    const int outputW = m_settings->getOutputW();
    const int outputH = m_settings->getOutputH();
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    m_renderScaleValueLabel->setText(scaleChoiceText(renderScale, calculateAutomaticRenderScalePercent(outputW, outputH)));
    m_worldScaleValueLabel->setText(scaleChoiceText(worldScale, calculateAutomaticWorldScalePercent(outputH)));
    m_applyButton->setEnabled(
        renderScale != m_settings->getSavedRenderScalePercent() ||
        worldScale != m_settings->getSavedWorldScalePercent()
    );
}

void cOptionsState::applyScaleSettings()
{
    const int renderScale = m_renderScaleChoices[m_selectedRenderScaleIndex];
    const int worldScale = m_worldScaleChoices[m_selectedWorldScaleIndex];
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    if (prefsFile && Preferences::saveScales(*prefsFile, renderScale, worldScale, error)) {
        m_settings->setSavedScalePercents(renderScale, worldScale);
        m_statusLabel->setText("Saved. Restart the game.");
    } else {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save the scales: {}", error);
        m_statusLabel->setText("Could not save preferences.ini");
    }
    updateScaleControls();
}
```

Развилки, решённые ведущим:

- Строки «Resolution» и «Fullscreen» форка не переносятся: размер окна и полноэкранный режим порт берёт из `settings.ini` и аргументов запуска. Их места в раскладке занимают флажки порта «FOW» (строка 4) и «Low power icon» (строка 7), с геометрией строки «Fullscreen» форка.
- Доступные значения «Масштаба игры» считаются по размеру вывода, который игра получила при запуске (`cSDLSystem::applyRenderScale`), — строки выбора разрешения в порту нет.
- Выбор, не применённый кнопкой «Apply», сохраняется в объекте окна, пока объект живёт, как в форке; поведение при повторном входе в меню — шаг П10.

## Не делать в этом шаге

Эти отличия от форка остаются до своих шагов; не исправляй их и не добавляй для них обходов:

- строка языка, русские тексты меню — шаг П7;
- окно сохранения и загрузки игры, работа кнопок «Save game» и «Load game» — шаг П8;
- страница дополнительных настроек, вкладка клавиш, работа кнопки «More settings», поведение при повторном входе в меню — шаг П10;
- музыкальные пулы и громкость по категориям — шаг П9;
- строки «Resolution» и «Fullscreen» форка.

## Проверки

1. `sha256sum -c .tmp/p5bt/tests.sha256` — `OK` для трёх файлов. Иначе — блок `## Q-P5B-01` и стоп.
2. Сборка Linux. Перед сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P5B-02` и стоп. Команда из корня рабочей копии:
   ```
   DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5b/build.log 2>&1
   ```
   Успех: код выхода 0; в `full.log` последней папки `.tmp/out/logs/` нет строк `warning:` из файлов рамки правок; в `ctest.log` той же папки итоговая строка `100% tests passed`; девять строк тестов с именем, начинающимся на `P5B `, каждая `Passed`. Иначе корневая нить разбирает провал: причина в коде рамки правок — точная правка субагенту и повтор дорожки D по разделу «Организация работы»; причина в самом тесте (тест противоречит контракту API) — блок `## Q-P5B-03` с последними 40 строками `.tmp/p5b/build.log` и строками провалов из `ctest.log`, и стоп.
3. Логи запуска игры той же папки логов: `game-dummy.log` и `stdout-dummy.log`. В обоих файлах нет ни одной строки с `Imminent crash`. Иначе — блок `## Q-P5B-04` с найденными строками и стоп.
4. Сверки, каждая своей командой:
   - `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/OptionsMenuLayout.hpp | cmp - src/gamestates/OptionsMenuLayout.hpp` — код выхода 0;
   - `grep -c "PREFERENCES_FILE" src/main.cpp` — `0`; `grep -c "Preferences::FILE_NAME" src/main.cpp` — `3`; `grep -c "Preferences::loadScales(" src/main.cpp` — `1`;
   - `grep -c "OptionsMenuLayout::create(" src/gamestates/cOptionsState.cpp` — `1`; `grep -c "Preferences::saveScales(" src/gamestates/cOptionsState.cpp` — `1`; `grep -c "cGuiThemeBuilder" src/gamestates/cOptionsState.cpp` — `1`; `grep -c "GuiTheme::RemasterInactive()" src/gamestates/cOptionsState.cpp` — `3`;
   - `grep -c "setSavedScalePercents(" src/game/cGame_logic.cpp` — `1`; `grep -c "getSavedRenderScalePercent()" src/game/cGame_logic.cpp` — `1`; `grep -c "getSavedWorldScalePercent()" src/game/cGame_logic.cpp` — `1`;
   - `grep -n -A1 "utils/RenderScale.cpp" src/CMakeLists.txt` — вторая строка вывода содержит `utils/ScaleChoices.cpp`.
   Иначе — блок `## Q-P5B-05` с выводом и стоп.
5. `git -c lfs.storage=$PWD/.tmp/p5b/lfs status --short` — только строки ` M ` для файлов рамки правок и строки `?? ` для `src/gamestates/OptionsMenuLayout.hpp`, `src/utils/ScaleChoices.hpp`, `src/utils/ScaleChoices.cpp`. Строки `__pycache__` допустимы. Другие строки — блок `## Q-P5B-06` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5B | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода;
- вывод проверок 1, 3, 4, 5; из проверки 2 — код выхода, итоговая строка `ctest.log` и девять строк тестов `P5B `;
- `git diff --stat`;
- список коммитов: один пункт — все файлы рамки правок, сообщение на английском о переносе раскладки меню настроек форка и строк масштаба игры и размера объектов на код порта: раскладка окна, две строки масштаба, запись выбора в `preferences.ini`, чтение двух масштабов при каждом запуске, неактивные кнопки до своих шагов. Последняя строка сообщения — `Behavior changes: …` со списком;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5b --size`; у `.tmp/p5b` пометка `оставить — логи сборки нужны ревью`. Папки `.tmp/out`, `.tmp/deps` и `.tmp/p5bt` созданы до этой задачи и в раздел не входят. Ничего не удаляй.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → правки (дорожки A, B и C параллельно) → проверки 1–5 (дорожка D) → сверка корневой нитью `git diff` с таблицей `PLAN-P5B` и таблицей шага 9г по каждой строке → сдача и стоп.
- **Параллельно:** дорожки A, B и C не зависят друг от друга: B и C пишут вызовы по именам контракта API и шага 6 и не ждут A и B. Дорожка D ждёт A, B и C.
- **Помощники:** не больше трёх субагентов `gpt-6-luna` `xhigh` одновременно, без вложенных.
  - Субагент A — шаги 1–3 `PLAN-P5B`.
  - Субагент B — шаги 4–7.
  - Субагент C — шаги 8–9.
  - Субагент D — шаг 10: проверки 1–5 дословно; сдаёт корневой нити коды выхода и строки логов, перечисленные в проверках.
  - Бриф субагентов A, B и C дословно содержит разделы «Что уже решено», «Контракт API», строки своих шагов таблицы `PLAN-P5B`, развилки под таблицей, раздел «Не делать в этом шаге» и абзац «Комментарии в коде»; бриф субагента C — ещё раздел «Шаг 9» целиком. Бриф субагента D дословно содержит раздел «Проверки» и абзац «Комментарии в коде».
  - Корневая нить: сверка, разбор провалов, сдача. Ошибка компиляции или провал теста из-за кода — корневая нить даёт субагенту A, B или C точную правку в рамке его шагов и повторяет дорожку D; третий подряд провал той же проверки — блок `## Q-P5B-07` и стоп.
- **Остановки:** только на `## DONE-P5B` и на блоках `## Q-P5B-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5B-08` и стоп.
- **Рамка правок:** три новых файла контракта, `src/CMakeLists.txt`, `src/game/Preferences.hpp`, `src/game/Preferences.cpp`, `src/main.cpp`, `src/game/cSDLSystem.h`, `src/game/cGameSettings.h`, `src/game/cGame_logic.cpp`, `src/gamestates/cOptionsState.h`, `src/gamestates/cOptionsState.cpp` и папка `.tmp/p5b/`. Понадобился другой файл — блок `## Q-P5B-NN` и стоп. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=2d86ef51aef14ab0cfe146d96e8768450f1161cc5c1f859bbf13ba4b7ae869e7 -->
## Обязательно: правила исполнителя

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Без фоновых команд: после остановки исполнителя никто его не разбудит. Длинные прогоны — в переднем плане, с таймаутом до 30 минут.
- Git по договорённости с ревьюером. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ревьюер после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ревьюера.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не трогать, секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Временные файлы — только в отведённой временной папке, в репозиторий и в корень рабочей копии ничего временного не класть. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Удалять что-либо вне своей временной папки — только по правилу «Уборка»; чужое, общее и постоянное — не удаляешь. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. В `DONE` — раздел «Рабочие места»: каждый созданный путь, его размер (`du -sh`) и что это — доказательство (на него ссылаются DONE, PR или журнал) или промежуточное. Объекты сборки, ненужные для повторной проверки, удаляешь только по правилу «Уборка»; до `CLEAN-OK` пути задачи не удаляешь.
- Уборка (владелец). В DONE — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер, назначение и пометка: `удалить` или `оставить — <почему>`; доказательства — только `оставить`. Удаляешь только после ответа ведущего-ревьюера `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; если в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`. Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- **Чтение (владелец).** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по журналу: обрезанный вывод — не чтение.
- Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; помощникам цель не ставить.

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
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в DONE;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса (владелец).** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи и журнала хода не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий (владелец); исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи — строго по порядку списка.
- Замечания ревьюера выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения; DONE — один на задачу, после REVIEW — новый DONE.
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
- Сливать в целевую ветку только ветку с зелёным CI на её последнем коммите; после слияния проверить CI целевой ветки и красной её не оставлять.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Отчёт владельцу

- Три пункта на языке владельца — простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Эти три пункта — часть DONE; отдельного отчёта владельцу не создавать.

<!-- /team-process:executor-rules -->
