# Задание P3 — загрузка HD4 с плотностью 4 на коде апстрима

Режим: **«План у ревьюера»** (см. «Режимы задания» в конце). Исполнитель: корневая нить Codex `gpt-6-luna` `xhigh`; правки и прогоны делают субагенты `gpt-6-luna` `xhigh` по разделу «Организация работы».

Рабочая копия: `/srv/dune/worktrees/p2`, ветка `codex/p3`, `HEAD` — `395250920ec210d6798e329dd95adeaa34e15bbd` (коммит ведущего с приёмочными тестами P3T поверх вершины ветки порта `36a1c8d57341e137cf40737027e0a614e7d8f6b7`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p3/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Игра на коде апстрима грузит четыре игровых графических пака и паки сцен из HD4 с плотностью 4, рисует их в логическом размере классики и не падает на HD4-картинках без палитры; приёмочные тесты `[P3]` проходят без изменений.

## Что уже решено

- Четыре игровых графических пака (`GFXDATA`, `GFXINTER`, `GFXWORLD`, `GFXMENTAT`) и паки сцен грузятся из HD4 с плотностью 4. Картинка HD4 в 4 раза больше классической по ширине и по высоте. `Texture` хранит физический размер и плотность; логический размер равен физическому, делённому на плотность. Функции рисования умножают исходный прямоугольник на плотность; прямоугольник назначения остаётся логическим.
- Пак значков редактора `sdl_gfxeditor.dat` остаётся классическим с плотностью 1. Пак звука `sdl_audio.dat` не меняется. Классические паки остаются в репозитории.
- Цвет Дома на HD4-картинках в этом шаге не рисуется: функция перекраски по палитре для картинки без палитры возвращает её как есть. Маски цвета Дома переносит шаг П6.
- Приёмочные тесты уже написаны и заморожены: `tests/utils/test_Hd4Loading.cpp` и две строки в `tests/CMakeLists.txt`, хэши — в `.tmp/p3t/tests.sha256`. Эти два файла не меняются. Тест падает из-за ошибки в самом тесте (тест противоречит контракту ниже) — блок `## Q-P3-NN` с выводом и стоп.

## Контракт API

1. **`src/include/Texture.hpp`, класс `Texture`.** Новые открытые поля после `h`: `int pixelW=0;`, `int pixelH=0;`, `int density=1;`. Конструктор: `explicit Texture(SDL_Texture *texture, int width, int height, bool isTarget = false, int assetDensity = 1)`. Значения: `density` = `std::max(1, assetDensity)`; `w` = `width / density`; `h` = `height / density` (целочисленное деление); `pixelW` = `width`; `pixelH` = `height`; `isRenderTarget` = `isTarget`.
2. **`src/utils/Graphics.hpp`, свободные определения после класса `Graphics`.** Только встроенные определения в заголовке; нужные стандартные заголовки (`<cmath>`, `<string>`) подключаются в `Graphics.hpp`:
   - `inline constexpr int kHd4AssetDensity = 4;`
   - `inline std::string hd4SceneFile(const std::string &scene)` возвращает `"data/scenes/hd4/sdl_" + scene + ".dat"`;
   - `inline int scaleToBitmap(int logical, int logicalExtent, int bitmapExtent)` возвращает `static_cast<int>(std::round(logical * static_cast<double>(bitmapExtent) / logicalExtent))`.
3. **`src/utils/Graphics.hpp` и `Graphics.cpp`, класс `Graphics`.** Конструктор: `explicit Graphics(SDL_Renderer *_renderer, const std::string &filePackName, int assetDensity = 1)`. Новый метод `int getDensity() const`, возвращает `std::max(1, assetDensity)`. `getTexture(int index)` создаёт `Texture(outTexture, outSurface->w, outSurface->h, false, getDensity())` и ставит текстуре режим масштабирования `SDL_SCALEMODE_LINEAR`, если `getDensity() > 1`, иначе `SDL_SCALEMODE_NEAREST`. `getTexture(const std::string &name)` и кэш текстур по индексу работают как в `HEAD`.
4. **`src/drawers/SDLDrawer.hpp` и `SDLDrawer.cpp`, класс `SDLDrawer`.**
   - `void renderFromSurface(SDL_Surface *src, int x, int y, Uint8 opacity = 255, int density = 1)`: ширина назначения `src->w / std::max(1, density)`, высота `src->h / std::max(1, density)`; режим масштабирования временной текстуры `SDL_SCALEMODE_LINEAR` при `density > 1`, иначе `SDL_SCALEMODE_NEAREST`. Остальное поведение — как в `HEAD`.
   - `renderStrechSprite`: поля `x`, `y`, `w`, `h` исходного прямоугольника умножаются на `src->density` перед `SDL_RenderTexture`; прямоугольник назначения не меняется.
   - `renderSprite`, `renderStrechFullSprite`, `renderTexture` не меняются.
   - `Texture *createTextureFromIndexedSurfaceWithPalette(SDL_Surface *referenceSurface, int paletteIndexForTransparency, const HouseColors& houseColors, int assetDensity = 1)`:
     - если `isSurface8BitPaletted(referenceSurface)` равно `false`: текстура создаётся `SDL_CreateTextureFromSurface(renderer, referenceSurface)` без перекраски и без цветового ключа; режим масштабирования — по правилу пункта 3 для `assetDensity`; результат — `new Texture(texture, referenceSurface->w, referenceSurface->h, false, assetDensity)`; если SDL вернул `nullptr` — `SDL_Log` с `SDL_GetError()` и возврат `nullptr`; строка «No palette in the original image!» в этой ветке не пишется;
     - если `true`: путь `HEAD` без изменений, кроме двух: режим масштабирования итоговой текстуры — по правилу пункта 3 для `assetDensity`; результат — `new Texture(texture, rgbaSurface->w, rgbaSurface->h, false, assetDensity)`.
5. **`src/utils/texture_utils.h` и `texture_utils.cpp`.** `Texture* createPlayerTextureFromIndexedSurfaceWithPalette(SDLDrawer *renderer, cPlayer* player, SDL_Surface* referenceSurface, int paletteIndexForTransparency, int assetDensity = 1)` передаёт `assetDensity` четвёртым аргументом в `SDLDrawer::createTextureFromIndexedSurfaceWithPalette`.
6. **`resources/bin/settings.ini`, секция `[DATAFILE]`.** `GFXDATA=sdl_data_hd4.dat`, `GFXINTER=sdl_inter_hd4.dat`, `GFXWORLD=sdl_world_hd4.dat`, `GFXMENTAT=sdl_mentat_hd4.dat`, `GFXAUDIO=sdl_audio.dat`, `GFXEDITOR=sdl_gfxeditor.dat`.

## Подключение

Номера строк — по `HEAD` до твоих правок; перед правкой найди строку по приведённому тексту.

1. **`src/context/ContextCreator.cpp`.** Строки 35, 43, 51, 59 (`gfxmentat`, `gfxworld`, `gfxinter`, `gfxdata`): третий аргумент конструктора `Graphics` — `kHd4AssetDensity`. Строка 67 (`gfxeditor`) не меняется.
2. **`src/gameobjects/mentat/AbstractMentat.cpp`, `AbstractMentat::loadScene`.** Строка 350: `const std::string filename = hd4SceneFile(scene);`. Строка 352: третий аргумент конструктора `Graphics` — `kHd4AssetDensity`.
3. **Вызовы `createPlayerTextureFromIndexedSurfaceWithPalette`.** Пятый аргумент — плотность пака, из которого взята поверхность:
   - `src/gameobjects/players/cPlayer.cpp`, строки 277, 278, 286, 298, 310, 316 — `m_gfxdata->getDensity()`;
   - `src/drawers/cOrderDrawer.cpp`, строки 41 и 121 — `getDensity()` того же объекта `Graphics`, у которого в этой строке вызван `getSurface(BTN_ORDER)`;
   - `src/drawers/cSideBarDrawer.cpp`, три вызова в строках 106–111 — `m_gfxinter->getDensity()`;
   - `src/managers/cDrawManager.cpp`, строки 101 и 322 — `m_gfxinter->getDensity()`;
   - `src/gamestates/cSelectYourNextConquestState.cpp`, строки 542 и 553 — `m_gfxworld->getDensity()`.
   Проверка: `git grep -n "createPlayerTextureFromIndexedSurfaceWithPalette(" -- src` выводит ровно 15 вызовов вне `src/utils/texture_utils.*`, и в каждом из них есть `getDensity()`.
4. **`src/drawers/cMapDrawer.cpp`, `cMapDrawer::createFogTexture`.** Строка 94: режим масштабирования `SDL_SCALEMODE_LINEAR`, если `m_gfxdata->getDensity() > 1`, иначе `SDL_SCALEMODE_NEAREST`. Строка 95: `std::make_unique<Texture>(fogTexture, width, height, false, m_gfxdata->getDensity())`.
5. **`src/drawers/cMessageDrawer.cpp`.** В `createMessageBarBmp` введи `const int density = m_gfxinter->getDensity();` и сделай полосу физической:
   - строка 179: `SDL_CreateSurface(desiredWidth * density, 30 * density, SDL_PIXELFORMAT_RGBA32)`;
   - строка 184: цикл `for (int drawX = 11 * density; drawX < m_bmpBar->w; drawX += 55 * density)`;
   - строка 191: `cRectangle{m_bmpBar->w - 11 * density, 0, src->w, src->h}`.
   В `draw` строки 61 и 65: `renderFromSurface(m_bmpBar, m_position.x, m_position.y, 255, m_gfxinter->getDensity())` и `renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha, m_gfxinter->getDensity())`.
6. **Размеры из поверхности пака — заменить логическим размером текстуры.**
   - `src/drawers/CreditsDrawer.cpp:73`: `m_gfxinter->getTexture(CREDITS_BAR)->w`.
   - `src/drawers/cBuildingListDrawer.cpp:91` и `:119`: `m_gfxinter->getTexture(id)->h`.
   - `src/drawers/cStructureDrawer.cpp:364–365`: `m_gfxdata->getTexture(MOUSE_REPAIR)->w` и `->h`; `:386–387`: `m_gfxinter->getTexture(iconId)->w` и `->h`.
   - `src/drawers/cUnitDrawer.cpp:278`: `Texture *focusBitmap = m_gfxdata->getTexture(FOCUS);` (строки 279–280 без изменений).
   - `src/managers/cDrawManager.cpp:236`: `Texture *mouseMoveBitmap = m_gfxdata->getTexture(MOUSE_MOVE);` (строки 238, 239, 246 без изменений).
7. **`src/gamestates/cSelectYourNextConquestState.cpp`, `regionOver`.** Строка 584: `int wCalc = scaleToBitmap(mouseX - offsetX - 16, 608, regionClickMapBmp->w);`. Строка 585: `int hCalc = scaleToBitmap(mouseY - offsetY - 73, 240, regionClickMapBmp->h);`.
8. **`resources/bin/settings.ini`.** Строки 83–86 — по пункту 6 контракта.

Заголовки (`include/Texture.hpp`, `utils/Graphics.hpp`) подключай только там, где без них файл не компилируется.

## Не делать в этом шаге

Эти отличия от форка остаются до своих шагов; не исправляй их и не добавляй для них обходов:

- цвет Дома у юнитов, зданий, флагов, кнопок приказов и настроек, полос кредитов и областей карты кампании — шаг П6 и шаги интерфейса;
- HD-картинки интерфейса из папки `data/hd4/` (`loadHdUiTexture` форка) — шаги П4 и П5;
- ветряк (у HD-картинки один кадр вместо семи), тарелка Командного поста (32 HD-кадра против 8 классических), осадный танк и тень перевозчика (другая раскладка HD-кадров), глаза и рты ментатов (другие размеры) — шаги П4, П8а и П11;
- поверхность в `cPlayer.cpp:294`, сборка релиза `create_release.sh`, шрифты, `ScalingMode` и камера.

## Проверки

1. `sha256sum -c .tmp/p3t/tests.sha256` — `OK` для обоих файлов. Иначе — блок `## Q-P3-01` и стоп.
2. Сборка Linux. Перед сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P3-02` и стоп. Команда из корня рабочей копии:
   ```
   DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p3/build.log 2>&1
   ```
   Успех: код выхода 0; в `ctest.log` последней папки `.tmp/out/logs/` итоговая строка `100% tests passed`; десять строк тестов с именем, начинающимся на `P3 `, каждая `Passed`; строка теста чтения HD4-паков `Passed`. Иначе — блок `## Q-P3-03` с последними 40 строками `.tmp/p3/build.log` и строками провалов из `ctest.log`, и стоп.
3. Логи запуска игры той же папки логов: `game-dummy.log` (журнал игры) и `stdout-dummy.log` (вывод и ошибки процесса). Сборочный скрипт запускает игру на 20 секунд.
   - В `game-dummy.log` есть четыре строки `Hooked datafile:` с именами `sdl_mentat_hd4.dat`, `sdl_world_hd4.dat`, `sdl_inter_hd4.dat`, `sdl_data_hd4.dat` и одна с `sdl_gfxeditor.dat`.
   - В обоих файлах нет ни одной строки с `Could not hook/load datafile`, `Failed to load image`, `No palette in the original image`, `Imminent crash`, `Invalid index`.
   Иначе — блок `## Q-P3-04` с найденными строками и стоп.
4. `git grep -n "data/scenes/sdl_" -- src` — пустой вывод.
5. `git -c lfs.storage=$PWD/.tmp/p3/lfs status --short` — только строки ` M ` для файлов из рамки правок. Другие строки — блок `## Q-P3-05` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P3 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода;
- вывод проверок 1, 3, 4, 5; из проверки 2 — код выхода, итоговая строка `ctest.log`, десять строк тестов `P3 ` и строка теста чтения HD4-паков;
- `git diff --stat`;
- список коммитов: пункт 1 — файлы контракта (`Texture.hpp`, `Graphics.hpp`, `Graphics.cpp`, `SDLDrawer.hpp`, `SDLDrawer.cpp`, `texture_utils.h`, `texture_utils.cpp`), сообщение на английском о плотности текстур и запасном пути без палитры; пункт 2 — остальные файлы, сообщение на английском о загрузке игровых паков и сцен из HD4. Последняя строка каждого сообщения — `Behavior changes: …`.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** `## PLAN-P3` и стоп до `PLAN-OK-P3` → правки (дорожки A и B параллельно) → проверки 1–5 (дорожка C) → сверка корневой нитью → сдача.
- **Параллельно:** дорожки A и B не зависят друг от друга: B пишет вызовы по сигнатурам контракта и не ждёт A. Дорожка C ждёт A и B.
- **Помощники:** не больше трёх субагентов `gpt-6-luna` `xhigh`, без вложенных.
  - Субагент A — пункты 1, 3, 4, 5 контракта (файлы `Texture.hpp`, `Graphics.hpp`, `Graphics.cpp`, `SDLDrawer.hpp`, `SDLDrawer.cpp`, `texture_utils.h`, `texture_utils.cpp`). Бриф дословно содержит разделы «Контракт API», «Не делать в этом шаге» и абзац «Комментарии в коде».
  - Субагент B — раздел «Подключение» целиком. Бриф дословно содержит разделы «Контракт API», «Подключение», «Не делать в этом шаге» и абзац «Комментарии в коде».
  - Субагент C — проверки 1–5 дословно; сдаёт корневой нити коды выхода и строки логов, перечисленные в проверках. Бриф дословно содержит раздел «Проверки» и абзац «Комментарии в коде».
  - Корневая нить: план, сверка `git diff` с контрактом и разделом «Подключение» по каждому пункту, разбор провалов, сдача. Ошибка компиляции или провал теста из-за кода — корневая нить даёт субагенту A или B точную правку и повторяет дорожку C; третий подряд провал той же проверки — блок `## Q-P3-06` и стоп.
- **Остановки:** только на `## PLAN-P3`, `## DONE-P3` и на блоках `## Q-P3-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P3-07` и стоп.
- **Рамка правок:** файлы из разделов «Контракт API» и «Подключение» и папка `.tmp/p3/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка. Другие файлы рабочей копии не меняй.
