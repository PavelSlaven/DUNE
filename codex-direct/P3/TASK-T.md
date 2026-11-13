# Задание P3T — приёмочные тесты загрузки HD4 с плотностью 4

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогон сборки делает один субагент `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/p2`, ветка `codex/p3`, `HEAD` — `36a1c8d57341e137cf40737027e0a614e7d8f6b7` (вершина ветки порта `port/up-d06f2fcd` после слияния П2г). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p3t/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Написать приёмочные тесты шага П3 по контракту API ниже, получить красный прогон по заявленной причине и заморозить тесты хэшем. Код игры не менять.

## Что уже решено

Шаг П3 переводит игру на коде апстрима на HD4-паки форка. Четыре игровых графических пака (`GFXDATA`, `GFXINTER`, `GFXWORLD`, `GFXMENTAT`) и паки сцен грузятся из HD4 с плотностью 4: картинка HD4 в 4 раза больше классической по ширине и по высоте. `Texture` хранит физический размер и плотность, логический размер равен физическому, делённому на плотность. Функции рисования умножают исходный прямоугольник на плотность, прямоугольник назначения остаётся логическим. Пак значков редактора `sdl_gfxeditor.dat` остаётся классическим с плотностью 1. Цвет Дома на HD4-картинках в П3 не рисуется: функция перекраски по палитре для картинки без палитры возвращает картинку как есть. Маски цвета Дома переносит шаг П6.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет.

## Контракт API

Этот раздел дословно входит и в задание исполнителя кода.

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

## Шаг 1. Тесты — корневая нить сама

Создай файл `tests/utils/test_Hd4Loading.cpp` на Catch2 3, как остальные файлы `tests/`. У каждого `TEST_CASE` имя начинается с `P3 `, тег — `[P3]`. Путь к корню исходников — макрос `D2TM_SOURCE_DIR`, как в `tests/utils/test_Hd4Packs.cpp`.

Рендерер для тестов с SDL — программный, без окна. В начале такого теста: `SDL_SetHint(SDL_HINT_VIDEO_DRIVER, "dummy")`, затем `SDL_Init(SDL_INIT_VIDEO)` (результат `REQUIRE`); рендерер — `SDL_CreateSoftwareRenderer` на поверхности `SDL_CreateSurface(..., SDL_PIXELFORMAT_RGBA32)`. Объекты, которые владеют текстурами (`Texture`, `Graphics`, `SDLDrawer`), уничтожаются до `SDL_DestroyRenderer`; в конце теста — `SDL_DestroyRenderer`, `SDL_DestroySurface` цели, затем `SDL_Quit()`. Цвет пикселя назначения читай `SDL_RenderReadPixels` после рисования; перед рисованием очищай цель чёрным непрозрачным цветом `{0, 0, 0, 255}`. Текстурам, которые тест создаёт сам из своей поверхности, ставь `SDL_SCALEMODE_NEAREST`.

Тесты, по одному `TEST_CASE` на пункт:

1. **`P3 Texture keeps physical size and density`.** `Texture(nullptr, 2560, 832, false, 4)`: `w` = 640, `h` = 208, `pixelW` = 2560, `pixelH` = 832, `density` = 4. `Texture(nullptr, 64, 48)`: `w` = 64, `h` = 48, `pixelW` = 64, `pixelH` = 48, `density` = 1. `Texture(nullptr, 64, 48, false, 0)`: `density` = 1, `w` = 64.
2. **`P3 Graphics loads HD4 data pack with density 4`.** `Graphics gfx(renderer, <D2TM_SOURCE_DIR>/resources/bin/data/sdl_data_hd4.dat, 4)`:
   - `gfx.getDensity()` = 4;
   - для `UNIT_QUAD` из `data/gfxdata.h`: `Texture *t = gfx.getTexture(UNIT_QUAD)` не `nullptr`; `t->pixelW` = `gfx.getSurface(UNIT_QUAD)->w`; `t->pixelH` = `gfx.getSurface(UNIT_QUAD)->h`; `t->w` = `t->pixelW / 4`; `t->h` = `t->pixelH / 4`; `t->density` = 4; `SDL_GetTextureScaleMode` для `t->tex.get()` даёт `SDL_SCALEMODE_LINEAR`;
   - `gfx.getTexture("UNIT_QUAD")` возвращает тот же указатель, что `gfx.getTexture(UNIT_QUAD)`;
   - дополнительная запись форка по имени: `gfx.getTexture("HM_UNIT_HARVESTER")` не `nullptr`, `pixelW` = 2560, `pixelH` = 832, `w` = 640, `h` = 208, `density` = 4. Перед тем как записать эти числа в тест, сверь их с паком командой на Python (модуль `tools/hd_assets.py`, функция `read_pack`, аргумент — `pathlib.Path`; размер — по заголовку PNG записи). Другие числа в паке — блок `## Q-P3T-01` с выводом и стоп.
3. **`P3 Graphics keeps the classic editor pack at density 1`.** `Graphics editor(renderer, <D2TM_SOURCE_DIR>/resources/bin/data/sdl_gfxeditor.dat)` без третьего аргумента: `getDensity()` = 1; `Texture *t = editor.getTexture(N)` не `nullptr`; `t->w` = `editor.getSurface(N)->w`; `t->h` = `editor.getSurface(N)->h`; `t->density` = 1; режим масштабирования `SDL_SCALEMODE_NEAREST`. `N` — индекс первой записи пака, которая декодируется как картинка: найди его Python-командой (модуль `tools/hd_assets.py`, функция `read_pack`, декодирование — Pillow) и запиши в тест числом.
4. **`P3 renderStrechSprite scales the source rectangle by density`.** Поверхность RGBA32 8×4: столбцы `x` 0–3 — `{255, 0, 0, 255}`, столбцы `x` 4–7 — `{0, 0, 255, 255}`. Текстура из неё, `Texture tex(texture, 8, 4, false, 4)`. Цель 8×8.
   - `drawer.renderStrechSprite(&tex, cRectangle{1, 0, 1, 1}, cRectangle{0, 0, 4, 4})`: пиксели `(0,0)` и `(3,3)` — `{0, 0, 255, 255}`; пиксель `(4,4)` — `{0, 0, 0, 255}`.
   - После новой очистки `drawer.renderSprite(&tex, 0, 0)`: пиксель `(0,0)` — `{255, 0, 0, 255}`; пиксель `(1,0)` — `{0, 0, 255, 255}`; пиксели `(2,0)` и `(0,1)` — `{0, 0, 0, 255}`.
5. **`P3 renderFromSurface divides the destination by density`.** Поверхность RGBA32 8×8, вся `{0, 255, 0, 255}`. Цель 16×16.
   - `drawer.renderFromSurface(surface, 0, 0, 255, 4)`: пиксель `(1,1)` — `{0, 255, 0, 255}`; пиксели `(2,2)` и `(2,0)` — `{0, 0, 0, 255}`.
   - После новой очистки `drawer.renderFromSurface(surface, 0, 0)`: пиксель `(7,7)` — `{0, 255, 0, 255}`; пиксель `(8,8)` — `{0, 0, 0, 255}`.
6. **`P3 palette recolor returns RGBA surfaces untinted with density`.** Поверхность RGBA32 8×4, вся `{40, 50, 60, 255}`. `HouseColors colors{}`, у всех семи элементов `{10, 200, 30}`. `Texture *t = drawer.createTextureFromIndexedSurfaceWithPalette(surface, 0, colors, 4)`: не `nullptr`; `w` = 2, `h` = 1, `pixelW` = 8, `pixelH` = 4, `density` = 4. Цель 8×8; `drawer.renderSprite(t, 0, 0)`: пиксель `(0,0)` — `{40, 50, 60, 255}`; пиксели `(2,0)` и `(0,1)` — `{0, 0, 0, 255}`. Тест удаляет `t` через `delete`.
7. **`P3 palette recolor still tints indexed surfaces`.** Поверхность `SDL_PIXELFORMAT_INDEX8` 8×4 с палитрой на 256 цветов (`SDL_CreateSurfacePalette`): все цвета палитры — `{0, 0, 0, 255}`, цвет 144 — `{255, 255, 255, 255}`; все пиксели — индекс 144. `HouseColors` с первым элементом `{10, 200, 30}`, остальные — `{0, 0, 0}`. Прозрачный индекс — 0. Вызов с `assetDensity` 1: `w` = 8, `h` = 4, `density` = 1; после `renderSprite(t, 0, 0)` на цели 8×8 пиксель `(0,0)` — `{10, 200, 30, 255}`. Вызов с той же поверхностью и `assetDensity` 4: `w` = 2, `h` = 1, `density` = 4.
8. **`P3 settings point the game packs at HD4`.** Файл `<D2TM_SOURCE_DIR>/resources/bin/settings.ini` читается классом из `utils/cIniFile.h`, как в `tests/utils/test_cIniFile.cpp`. В секции `DATAFILE` значения ключей равны строкам пункта 6 контракта. Для каждого из шести значений существует файл `<D2TM_SOURCE_DIR>/resources/bin/data/<значение>`.
9. **`P3 scenes load from the HD4 folder`.** `kHd4AssetDensity` = 4. Для каждого имени из списка `harvest`, `ix`, `sardukar`, `palace`, `repair`, `hvyftry`, `headqrts`, `quad`, `ltank`, `win01`, `win02`, `lose01`, `lose02`, `platr`, `plhar`, `plord`: `hd4SceneFile(имя)` = `"data/scenes/hd4/sdl_" + имя + ".dat"`, и существует файл `<D2TM_SOURCE_DIR>/resources/bin/` + `hd4SceneFile(имя)`.
10. **`P3 scaleToBitmap maps the campaign map onto the click bitmap`.** `scaleToBitmap(0, 608, 2432)` = 0; `scaleToBitmap(100, 608, 2432)` = 400; `scaleToBitmap(607, 608, 2432)` = 2428; `scaleToBitmap(239, 240, 960)` = 956; `scaleToBitmap(100, 608, 608)` = 100.

Затем в `tests/CMakeLists.txt`: в список `TEST_FILES` добавь строку `${CMAKE_CURRENT_SOURCE_DIR}/utils/test_Hd4Loading.cpp` сразу после строки с `test_Hd4Packs.cpp`; в список `TEST_SOURCES` добавь строку `${CMAKE_SOURCE_DIR}/src/utils/Graphics.cpp` сразу после строки с `src/utils/cPack.cpp`. Других правок в `tests/CMakeLists.txt` нет.

Исключение из правила «Существующие тесты и их ожидания не менять»: меняется только `tests/CMakeLists.txt`, ровно двумя строками выше. Другие файлы `tests/` и весь код вне `tests/` не меняются.

## Шаг 2. Красный прогон — субагент `gpt-6-luna` `xhigh`

Перед сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P3T-02` и стоп. Команда из корня рабочей копии:

```
DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p3t/build-red.log 2>&1
```

Субагент сдаёт корневой нити код выхода и все строки `.tmp/p3t/build-red.log` и `.tmp/out/logs/<последняя папка>/full.log`, содержащие `error:`.

Ожидается: код выхода не 0; сборка останавливается на компиляции `tests/utils/test_Hd4Loading.cpp`; каждая строка `error:` относится к этому файлу; каждая ошибка — отсутствующий символ или отсутствующая перегрузка из контракта: `pixelW`, `pixelH`, `density`, `getDensity`, `kHd4AssetDensity`, `hd4SceneFile`, `scaleToBitmap`, конструктор `Graphics` с тремя аргументами, `renderFromSurface` с пятью аргументами, `createTextureFromIndexedSurfaceWithPalette` с четырьмя аргументами, конструктор `Texture` с пятью аргументами. Ошибка другого рода (опечатка, неверный тип, неверный заголовок) — исправь тест и повтори шаг 2. Ошибки вне `tests/utils/test_Hd4Loading.cpp` — блок `## Q-P3T-03` с этими строками и стоп. Тесты 8, 9 и 10 до кода тоже не компилируются; другого красного для них нет.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/utils/test_Hd4Loading.cpp tests/CMakeLists.txt > .tmp/p3t/tests.sha256`. После этой команды файлы тестов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p3t/lfs status --short` выводит ровно две строки: ` M tests/CMakeLists.txt` и `?? tests/utils/test_Hd4Loading.cpp`. Строки `__pycache__` в выводе допустимы; другие строки — блок `## Q-P3T-04` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P3T | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- `## PLAN-P3T` для записи: шаги по порядку и кто их делал;
- вывод сверки размеров `HM_UNIT_HARVESTER` из шага 1;
- код выхода красной сборки и все строки `error:` (не больше 80; если больше — первые 80 и их число);
- содержимое `.tmp/p3t/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — `tests/utils/test_Hd4Loading.cpp` и `tests/CMakeLists.txt`, сообщение на английском о приёмочных тестах загрузки HD4 с плотностью 4; последняя строка сообщения — `Behavior changes: none`.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** шаг 1 → шаг 2 → шаг 3 → сдача.
- **Параллельно:** нет. Красный прогон зависит от тестов, заморозка — от красного прогона.
- **Помощники:** не больше одного субагента `gpt-6-luna` `xhigh`, без вложенных. Субагент делает только шаг 2; его бриф дословно содержит раздел «Шаг 2» целиком и абзац «Комментарии в коде». Тесты, разбор ошибок, исправления тестов, заморозку и сдачу делает корневая нить.
- **Остановки:** только на `## DONE-P3T` и на блоках `## Q-P3T-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P3T-05` и стоп.
- **Рамка правок:** `tests/utils/test_Hd4Loading.cpp` (новый), `tests/CMakeLists.txt` (две строки), папка `.tmp/p3t/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка. Другие файлы рабочей копии не меняй.
