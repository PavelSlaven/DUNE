# Задание P4 — HD-кадр, масштаб мира, HD-кадры юнитов и флаг ветряка на коде апстрима (шаг П4а)

Режим: **«План у ревьюера»** (см. «Режимы задания» в конце). Исполнитель: корневая нить Codex `gpt-6-luna` `xhigh`; правки и прогоны делают субагенты `gpt-6-luna` `xhigh` по разделу «Организация работы».

Рабочая копия: `/srv/dune/worktrees/p2`, ветка `codex/p4`, `HEAD` — `36a055ae9e488c4f8f79137a949696efab33f4b2` (коммит ведущего с приёмочными тестами P4T поверх вершины ветки порта `b07f5e10445e3b4f497d23878d49699cbfa5f245`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p4/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Игра на коде апстрима рисует кадр в текстуру-цель с плотностью кадра, поэтому HD-картинки сохраняют детали, когда окно показывает кадр крупнее логического размера; камера начинает миссию с зумом масштаба мира; осадный танк рисуется своими HD-кадрами; ветряк виден всегда и машет HD-флагом. Приёмочные тесты `[P4]` и `[P3]` проходят без изменений.

## Что уже решено

- Шаг П3 перевёл игру на HD4-паки: `Texture` хранит физический размер и плотность, функции рисования умножают исходный прямоугольник на плотность, прямоугольник назначения логический.
- **HD-кадр.** Логический размер игры (`renderResolution`, `m_screenW` × `m_screenH`) и логическое представление окна (`ScalingMode`) остаются как в апстриме. Кадр рисуется в текстуру-цель с плотностью кадра: масштаб показа кадра в окне, округлённый вверх, от 1 до 4 (`calculateFrameDensity`). У такой цели своё логическое представление SDL3 размером с логический кадр, поэтому все функции рисования работают в логических координатах. Сборка кадра в окне (`renderSprite(actualRenderer, …)`), затемнение и перевод координат мыши (`SDL_RenderCoordinatesFromWindow`, он берёт представление окна) не меняются.
- **Масштаб мира** — стартовый зум камеры (решение владельца Р33): `worldScaleZoom(настройка WorldScale, m_screenH)`. Сброс зума (начало миссии, клавиша сброса зума) возвращает этот же зум. Ограничения зума 0.25–4.0, шаг колёсика, `zoomOutToFit` и закладки камеры апстрима не меняются.
- **HD-кадры юнитов.** Юнит с заданным HD-размером кадра рисуется кадром этого размера по центру своего прямоугольника; сейчас HD-размер задан только у осадного танка (176×176 физических пикселей; запись пака `UNIT_SIEGEBASE` — 1408×176, 8 направлений).
- **Ветряк.** У HD-ветряка один кадр тела (256×256 физических пикселей) вместо семи классических, поэтому тело не анимируется; поверх тела рисуется HD-флаг `BUILD_WINDTRAP_FLAG` (8 кадров по 64×64 логических пикселя, смена каждые 125 мс), а классический флаг Дома у ветряка не рисуется. Цвет Дома на флаге — шаг П6.
- Приёмочные тесты уже написаны и заморожены: `tests/utils/test_HdRender.cpp` и одна строка в `tests/CMakeLists.txt`, хэши — в `.tmp/p4t/tests.sha256`. Эти два файла не меняются. Тест падает из-за ошибки в самом тесте (тест противоречит контракту ниже) — блок `## Q-P4-NN` с выводом и стоп.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `tests/utils/test_HdRender.cpp` — приёмочные тесты шага;
- `src/drawers/SDLDrawer.hpp`, `src/drawers/SDLDrawer.cpp`, `src/include/Texture.hpp`, `src/utils/Graphics.hpp`;
- `src/utils/InitialGameSettings.hpp`, `src/game/Preferences.cpp`, `src/game/cGameSettings.h`;
- `src/game/cGame.h`, `src/game/cGame_logic.cpp`, `src/game/cSDLSystem.h`, `src/game/cSDLSystem.cpp`;
- `src/gameobjects/map/cMapCamera.h`, `src/gameobjects/map/cMapCamera.cpp`;
- `src/gameobjects/units/cUnitInfos.h`, `src/drawers/cUnitDrawer.cpp`;
- `src/gameobjects/structures/cWindTrap.h`, `src/gameobjects/structures/cWindTrap.cpp`, `src/gameobjects/structures/cAbstractStructure.h`, `src/gameobjects/structures/cAbstractStructure.cpp`;
- `src/drawers/cStructureDrawer.h`, `src/drawers/cStructureDrawer.cpp`, `src/drawers/cSideBarDrawer.h`, `src/drawers/cSideBarDrawer.cpp`.

Субагент читает из этого списка файлы своей дорожки.

## Контракт API

1. **`src/utils/WorldScale.hpp` (новый файл, только встроенные определения).** Подключает `<algorithm>` и `<array>`.
   - `inline constexpr int AutomaticWorldScale = 0;`
   - `inline constexpr std::array<int, 4> ManualWorldScales{100, 110, 125, 150};`
   - `inline bool isWorldScaleSupported(int worldScalePercent)` — `true` для `AutomaticWorldScale` и для каждого значения `ManualWorldScales`, иначе `false`.
   - `inline int calculateAutomaticWorldScalePercent(int outputHeight)` — `100` при `outputHeight <= 768`; иначе `110` при `outputHeight <= 1080`; иначе `125` при `outputHeight <= 1600`; иначе `150`.
   - `inline int resolveWorldScalePercent(int selectedWorldScalePercent, int outputHeight)` — при `selectedWorldScalePercent == AutomaticWorldScale` или `isWorldScaleSupported(selectedWorldScalePercent) == false` возвращает `calculateAutomaticWorldScalePercent(outputHeight)`, иначе `selectedWorldScalePercent`.
   - `inline float worldScaleZoom(int selectedWorldScalePercent, int outputHeight)` — `static_cast<float>(resolveWorldScalePercent(selectedWorldScalePercent, outputHeight)) / 100.0f`.
2. **Настройка `WorldScale`.** `src/utils/InitialGameSettings.hpp`, структура `InitialGameSettings`: новое поле `int worldScalePercent = 0;` сразу после поля `scalingMode`. `src/game/Preferences.cpp`, `readSettings`: если `section.hasValue("WorldScale")`, то `settings.worldScalePercent = section.getInt("WorldScale");`. `Preferences::save` не меняется. `resources/bin/settings.ini` не меняется.
3. **`src/utils/UnitSpriteLayout.hpp` (новый файл).** Дословная копия `src/utils/UnitSpriteLayout.hpp` ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566` (получить командой `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/UnitSpriteLayout.hpp`): структуры `UnitSpriteFrame {int width; int height; bool usesHdFrame;}`, `UnitSpriteRectangle {int x; int y; int width; int height;}`, `UnitSpriteFloatRectangle {float x; float y; float width; float height;}` и встроенные функции:
   - `resolveUnitSpriteFrame(int bmpWidth, int bmpHeight, int hdFrameWidth, int hdFrameHeight, int textureDensity)` — при `textureDensity > 1 && hdFrameWidth > 0 && hdFrameHeight > 0` возвращает `{hdFrameWidth / textureDensity, hdFrameHeight / textureDensity, true}`, иначе `{bmpWidth, bmpHeight, false}`;
   - `unitSpriteSourceRectangle(UnitSpriteFrame frame, int facingIndex, int animationFrame)` — `{facingIndex * frame.width, animationFrame * frame.height, frame.width, frame.height}`;
   - `unitSpriteDestinationRectangle(UnitSpriteFrame frame, UnitSpriteRectangle visual, float cameraZoom)` — при `frame.usesHdFrame == false` возвращает прямоугольник `visual` в `float`; иначе `zoomedWidth = static_cast<int>(std::lround(frame.width * cameraZoom))`, `zoomedHeight` так же по высоте, результат `{visual.x + (visual.width - zoomedWidth) / 2.0F, visual.y + (visual.height - zoomedHeight) / 2.0F, zoomedWidth, zoomedHeight}`.
4. **`src/utils/WindTrapFlag.hpp` (новый файл, только встроенные определения).** Подключает `<cstdint>`.
   - `inline constexpr int kWindTrapFlagFrames = 8;`
   - `inline constexpr int kWindTrapFlagFrameSize = 64;`
   - `inline int windTrapFlagFrame(std::uint64_t ticksMs)` — `static_cast<int>((ticksMs / 125U) % kWindTrapFlagFrames)`.
5. **`src/utils/Graphics.hpp`, свободное встроенное определение после `scaleToBitmap`.** `inline int calculateFrameDensity(float presentationWidth, float presentationHeight, int logicalWidth, int logicalHeight)`: при `logicalWidth <= 0` или `logicalHeight <= 0` возвращает `1`; иначе `scale = std::min(presentationWidth / logicalWidth, presentationHeight / logicalHeight)` и результат `std::clamp(static_cast<int>(std::ceil(scale - 0.01f)), 1, kHd4AssetDensity)`. Нужный заголовок `<algorithm>` подключается в `Graphics.hpp`.
6. **`src/drawers/SDLDrawer.hpp` и `SDLDrawer.cpp`, класс `SDLDrawer`.**
   - `Texture *createRenderTargetTexture(int width, int height, int density = 1)`: `d = std::max(1, density)`; текстура `SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, width * d, height * d)`; ошибка создания — исключение, как в `HEAD`; режим масштабирования `SDL_SCALEMODE_LINEAR` при `d > 1`, иначе `SDL_SCALEMODE_NEAREST`; при `d > 1` у новой текстуры задаётся своё логическое представление: запомнить `SDL_GetRenderTarget(renderer)`, сделать новую текстуру целью, вызвать `SDL_SetRenderLogicalPresentation(renderer, width, height, SDL_LOGICAL_PRESENTATION_STRETCH)`, вернуть запомненную цель; результат — `new Texture(texture, width * d, height * d, true, d)` (у неё `w` = `width`, `h` = `height`, `pixelW` = `width * d`, `density` = `d`). При `d == 1` логическое представление новой текстуры не задаётся.
   - `void setFrameDensity(int density)` сохраняет `std::max(1, density)`; `int getFrameDensity() const` возвращает сохранённое значение; до первого вызова `setFrameDensity` — `1`.
   - `beginDrawingToTexture`, `endDrawingToTexture`, функции рисования не меняются.

## Подключение

Номера строк — по `b07f5e10445e3b4f497d23878d49699cbfa5f245` до твоих правок; перед правкой найди строку по приведённому тексту.

1. **Настройка в игре.** `src/game/cGameSettings.h`: поле `int m_worldScalePercent = 0;` рядом с `m_screenH`, с тем же доступом, что у `m_screenH`; открытый метод `float getWorldScaleFactor() const`, возвращает `worldScaleZoom(m_worldScalePercent, m_screenH)`. В `src/game/cGame_logic.cpp` там, где поле `screenW` из `InitialGameSettings` переносится в `m_gameSettings->m_screenW`, так же перенеси `worldScalePercent` в `m_gameSettings->m_worldScalePercent`. В `cGame::currentSettings()` (строки 343–352) добавь `gs.worldScalePercent = m_gameSettings->m_worldScalePercent;`.
2. **Камера.** `src/gameobjects/map/cMapCamera.cpp`, конструктор, строка 45: `m_zoomLevel = std::clamp(m_gameSettings->getWorldScaleFactor(), 0.25f, 4.0f);`. `src/gameobjects/map/cMapCamera.h`, `resetZoom()` (строки 53–57): тело — `setZoomLevel(m_gameSettings->getWorldScaleFactor());`. Если в `cMapCamera.h` тип `cGameSettings` неполный и встроенное тело не компилируется, объяви `void resetZoom();` в заголовке и перенеси это тело в `cMapCamera.cpp`. Другие методы камеры не меняются.
3. **HD-размер кадра юнита.** `src/gameobjects/units/cUnitInfos.h`, `struct s_UnitInfo`: поля `int hd_frame_width = 0;` и `int hd_frame_height = 0;` сразу после поля `bmp_height`. `src/context/cInfoContextCreator.cpp`, сразу после строки 286 `unitInfos[SIEGETANK].bmp_height = 18 * 2;`: `unitInfos[SIEGETANK].hd_frame_width = 176;` и `unitInfos[SIEGETANK].hd_frame_height = 176;`. Других присвоений `hd_frame_*` нет.
4. **Рисование юнита.** `src/drawers/cUnitDrawer.cpp`, `cUnitDrawer::draw()`, строки 229–271 (тень, тело, верх). Введи `const UnitSpriteRectangle visual{ux, uy, roundedScaledWidth, roundedScaledHeight};` и `const float cameraZoom = m_unit.getMapCamera()->factorZoomLevel(1.0f);`. Для каждой из трёх текстур (`shadow` с направлением `bmp_body`, `bitmap` с направлением `bmp_body`, `top` с направлением `bmp_head`):
   - `frame = resolveUnitSpriteFrame(bmp_width, bmp_height, unitType.hd_frame_width, unitType.hd_frame_height, <текстура>->density)`;
   - `s = unitSpriteSourceRectangle(frame, <направление>, m_unit.rendering.iFrame)`, исходный прямоугольник `cRectangle{s.x, s.y, s.width, s.height}`;
   - `d = unitSpriteDestinationRectangle(frame, visual, cameraZoom)`, прямоугольник назначения `cRectangle{static_cast<int>(std::lround(d.x)), static_cast<int>(std::lround(d.y)), static_cast<int>(d.width), static_cast<int>(d.height)}`;
   - у тени `CARRYALL` к `y` назначения прибавляется 24, как в `HEAD`;
   - вызовы `renderStrechSprite` с теми же текстурами и прозрачностью, что в `HEAD`; условие рисования верха (`top && m_unit.getHitPoints() > -1`) не меняется.
   Для юнита без HD-размера получаются ровно прямоугольники `HEAD`. Код после строки 271 не меняется.
5. **Тело ветряка.** `src/gameobjects/structures/cWindTrap.cpp`: в конструкторе строка 31 — `iFrame = 0;`, строка 30 (`m_flagDir = true;`) удаляется; `cWindTrap::thinkFast()` содержит только вызов `cAbstractStructure::thinkFast();`. Поле `m_flagDir` удаляется из `src/gameobjects/structures/cWindTrap.h`. `think_animation` не меняется.
6. **Прямоугольник постройки.** `src/gameobjects/structures/cAbstractStructure.h` и `.cpp`: новый открытый метод `cRectangle getDrawRectangle()`, возвращает `{iDrawX(), iDrawY(), scaledWidth, scaledHeight}`, где `scaledWidth` и `scaledHeight` вычисляются так же, как в `drawWithShadow` (строки 934–935: `int scaledWidth = m_mapCamera->factorZoomLevel(getWidthInPixels());` и то же по высоте). `drawWithShadow` берёт свой `dest` из `getDrawRectangle()`; остальное в `drawWithShadow` не меняется.
7. **Флаг ветряка.** `src/drawers/cStructureDrawer.h` и `.cpp`: новый закрытый метод `bool drawHdWindTrapFlag(cAbstractStructure *structure)`:
   - тип постройки не `WINDTRAP` — возврат `false`;
   - `Texture *flag = m_gfxdata->getTexture("BUILD_WINDTRAP_FLAG");` при `nullptr` — возврат `false`;
   - `const int frame = windTrapFlagFrame(SDL_GetTicks());`
   - рисование: тот же объект `SDLDrawer`, которым `cStructureDrawer` рисует постройки, метод `renderStrechSprite(flag, cRectangle{0, frame * kWindTrapFlagFrameSize, kWindTrapFlagFrameSize, kWindTrapFlagFrameSize}, structure->getDrawRectangle())`;
   - возврат `true`.
   В `drawStructureForLayer` строка 321 `structure->drawFlags();` заменяется на `if (!drawHdWindTrapFlag(structure)) { structure->drawFlags(); }`.
8. **Кадр с плотностью.**
   - `src/game/cSDLSystem.h` и `.cpp`: новый открытый метод `int frameDensity() const`: `SDL_FRect rect{};`; если `SDL_GetRenderLogicalPresentationRect(renderer, &rect)` вернул `false` — возврат `1`; иначе `calculateFrameDensity(rect.w, rect.h, renderResolution.width, renderResolution.height)`.
   - `src/game/cGame.h` и `src/game/cGame_logic.cpp`: новый закрытый метод `void cGame::ensureFrameTargets()`:
     1. `const int density = m_Screen->frameDensity();` и `m_sdlDrawer->setFrameDensity(density);`
     2. если `actualRenderer != nullptr` и `actualRenderer->density == density` — возврат;
     3. `delete actualRenderer;` и `delete screenTexture;`
     4. `actualRenderer` и `screenTexture` — `m_sdlDrawer->createRenderTargetTexture(m_gameSettings->m_screenW, m_gameSettings->m_screenH, density)`; `m_services->screenTexture = screenTexture;`
     5. `Logger::info(COMP_SDL2, "frame", "Frame targets {}x{} at density {}", m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);`
   - `cGame::run()`: строки 570–572 заменяются вызовом `ensureFrameTargets();`; в цикле вызов `ensureFrameTargets();` стоит сразу перед строкой 623 `m_sdlDrawer->beginDrawingToTexture(actualRenderer);`. Строки 624–632 не меняются.
   - `src/drawers/cSideBarDrawer.cpp`: строка 50 — третий аргумент `createRenderTargetTexture` равен `m_sdlDrawer->getFrameDensity()`. Сразу перед строкой 113 `m_sdlDrawer->beginDrawingToTexture(m_candiBarRenderer);`: если `m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()`, то `delete m_candiBarRenderer;` и `m_candiBarRenderer` создаётся заново тем же вызовом, что в строке 50. Строка 60 не меняется.
   - Остальные вызовы `createRenderTargetTexture` (`cMiniMapDrawer.cpp`, `cMainMenuState.cpp`) не меняются.

Заголовки (`utils/WorldScale.hpp`, `utils/UnitSpriteLayout.hpp`, `utils/WindTrapFlag.hpp`, `utils/Graphics.hpp`, `<algorithm>`, `<cmath>`) подключай только там, где без них файл не компилируется.

## Не делать в этом шаге

Эти отличия от форка остаются до своих шагов; не исправляй их и не добавляй для них обходов:

- «Масштаб игры» форка (`RenderScale`), выбор логического размера игры, `ScalingMode`, `ScreenWidth` и `ScreenHeight` — шаг П4б;
- строки «Масштаб игры» и «Размер объектов» в меню настроек — шаг П5; запись `WorldScale` в `preferences.ini` — шаг П8;
- HD-картинки интерфейса из папки `data/hd4/` (`loadHdUiTexture` форка) — шаги П5 и П10;
- HD-метки Дома на заводе, хранилище, строительной площадке и казарме, цвет Дома на флаге ветряка (`HM_BUILD_WINDTRAP_FLAG`) — шаг П6;
- харвестер на площадке завода (`WorldObjectScale` форка) — шаг П8а;
- цели рендера миникарты и отладочного фона меню, текстуры текста и шрифты, снимок экрана, флаги создания окна.

## Проверки

1. `sha256sum -c .tmp/p4t/tests.sha256` — `OK` для обоих файлов. Иначе — блок `## Q-P4-01` и стоп.
2. Сборка Linux. Перед сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P4-02` и стоп. Команда из корня рабочей копии:
   ```
   DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p4/build.log 2>&1
   ```
   Успех: код выхода 0; в `ctest.log` последней папки `.tmp/out/logs/` итоговая строка `100% tests passed`; десять строк тестов с именем, начинающимся на `P4 `, каждая `Passed`; десять строк тестов с именем, начинающимся на `P3 `, каждая `Passed`. Иначе — блок `## Q-P4-03` с последними 40 строками `.tmp/p4/build.log` и строками провалов из `ctest.log`, и стоп.
3. Логи запуска игры той же папки логов: `game-dummy.log` (журнал игры) и `stdout-dummy.log` (вывод и ошибки процесса). Сборочный скрипт запускает игру на 20 секунд.
   - В `game-dummy.log` есть четыре строки `Hooked datafile:` с именами `sdl_mentat_hd4.dat`, `sdl_world_hd4.dat`, `sdl_inter_hd4.dat`, `sdl_data_hd4.dat` и одна с `sdl_gfxeditor.dat`; ровно одна строка с `Frame targets`, и в ней `at density 1`.
   - В обоих файлах нет ни одной строки с `Could not hook/load datafile`, `Failed to load image`, `No palette in the original image`, `Imminent crash`, `Invalid index`, `Error changing render target`, `Error creating render texture`.
   Иначе — блок `## Q-P4-04` с найденными строками и стоп.
4. `git grep -n -E "RNG::rnd\(6\)|m_flagDir" -- src/gameobjects/structures` — пустой вывод. `git grep -n "createRenderTargetTexture(" -- src` — вывод содержит определение в `SDLDrawer.cpp`, объявление в `SDLDrawer.hpp`, два вызова в `cGame_logic.cpp`, два в `cSideBarDrawer.cpp` и вызовы в `cMiniMapDrawer.cpp` и `cMainMenuState.cpp` в том виде, как в `HEAD`.
5. `git -c lfs.storage=$PWD/.tmp/p4/lfs status --short` — только строки ` M ` для файлов из рамки правок и строки `?? ` для `src/utils/WorldScale.hpp`, `src/utils/UnitSpriteLayout.hpp`, `src/utils/WindTrapFlag.hpp`. Строки `__pycache__` допустимы. Другие строки — блок `## Q-P4-05` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P4 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода;
- вывод проверок 1, 3, 4, 5; из проверки 2 — код выхода, итоговая строка `ctest.log`, десять строк тестов `P4 ` и десять строк тестов `P3 `;
- `git diff --stat`;
- список коммитов: пункт 1 — файлы контракта (`WorldScale.hpp`, `UnitSpriteLayout.hpp`, `WindTrapFlag.hpp`, `InitialGameSettings.hpp`, `Preferences.cpp`, `Graphics.hpp`, `SDLDrawer.hpp`, `SDLDrawer.cpp`), сообщение на английском о помощниках масштаба мира, HD-кадров юнитов, флага ветряка и плотности кадра; пункт 2 — остальные файлы, сообщение на английском о подключении: зум камеры по масштабу мира, HD-кадры осадного танка, флаг ветряка, кадр с плотностью. Последняя строка каждого сообщения — `Behavior changes: …`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p4 --size`; у `.tmp/p4` пометка `оставить — логи сборки нужны ревью`. Папки `.tmp/out`, `.tmp/deps` и `.tmp/p4t` созданы до этой задачи и в раздел не входят. Ничего не удаляй.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** `## PLAN-P4` и стоп до `PLAN-OK-P4` → правки (дорожки A, B и C параллельно) → проверки 1–5 (дорожка D) → сверка корневой нитью → сдача.
- **Параллельно:** дорожки A, B и C не зависят друг от друга: B и C пишут вызовы по сигнатурам контракта и не ждут A. Дорожка D ждёт A, B и C.
- **Помощники:** не больше трёх субагентов `gpt-6-luna` `xhigh` одновременно, без вложенных.
  - Субагент A — пункты 1–6 контракта (файлы `WorldScale.hpp`, `UnitSpriteLayout.hpp`, `WindTrapFlag.hpp`, `InitialGameSettings.hpp`, `Preferences.cpp`, `Graphics.hpp`, `SDLDrawer.hpp`, `SDLDrawer.cpp`). Бриф дословно содержит разделы «Контракт API», «Не делать в этом шаге» и абзац «Комментарии в коде».
  - Субагент B — пункты 1–7 раздела «Подключение». Бриф дословно содержит разделы «Контракт API», «Подключение», «Не делать в этом шаге» и абзац «Комментарии в коде».
  - Субагент C — пункт 8 раздела «Подключение»; закончив его, делает дорожку D: проверки 1–5 дословно, сдаёт корневой нити коды выхода и строки логов, перечисленные в проверках. Бриф дословно содержит разделы «Контракт API», «Подключение», «Не делать в этом шаге», «Проверки» и абзац «Комментарии в коде».
  - Корневая нить: план, сверка `git diff` с контрактом и разделом «Подключение» по каждому пункту, разбор провалов, сдача. Ошибка компиляции или провал теста из-за кода — корневая нить даёт субагенту A, B или C точную правку и повторяет дорожку D; третий подряд провал той же проверки — блок `## Q-P4-06` и стоп.
- **Остановки:** только на `## PLAN-P4`, `## DONE-P4` и на блоках `## Q-P4-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P4-07` и стоп.
- **Рамка правок:** файлы из разделов «Контракт API» и «Подключение» и папка `.tmp/p4/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка. Другие файлы рабочей копии не меняй.

<!-- team-process:executor-rules sha256=e95ddebd0b5ba9c0a5c06419ace7002804fdf2e33d2a441ec571208e7de05ed7 -->
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
- План пишет ведущий (владелец); исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы, развилки с рекомендацией) без плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
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
