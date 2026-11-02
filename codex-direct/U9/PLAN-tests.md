## PLAN-U9-T1

План составлен по полностью перечитанному `codex-direct/U9/TESTS-frame.md` на HEAD `aaf0c8ef8467f6bd782c1d43a9ff1ade2fc148d7`. Уточнение `ANSWER-Q-U9-T1-01` принято: проверяются все 16 пар выбранных настроек; действующий масштаб мира в классике равен `1,0`, в HD — выбранному `s`.

До `PLAN-OK-U9-T1` изменён только журнал `.tmp/progress-u9t1.md`. Тесты, конфигурация сборки и код продукта не изменены.

### 1. Источники и независимые ожидания

Приоритет требований: обновлённый `TESTS-frame.md` → `PLAN-OK-frame.md` → `PLAN-frame.md`. Поведение проверяется по пунктам 1–6 `TASK-frame.md`; эталон прежнего рисования — `bb2f1b37`.

В `tests/UnitFrameBaseline.hpp` запишу таблицу из `cIniGameRessouces.cpp` эталонного коммита:

| Типы | Логический кадр | `bmp_frames` |
|---|---:|---:|
| `CARRYALL` | 48 × 48 | 2 |
| `ORNITHOPTER` | 48 × 48 | 4 |
| `DEVASTATOR` | 38 × 46 | 1 |
| `HARVESTER` | 80 × 52 | 4 |
| `TANK` | 32 × 32 | 0 |
| `SIEGETANK` | 36 × 36 | 0 |
| `MCV` | 48 × 50 | 1 |
| `DEVIATOR`, `LAUNCHER`, `QUAD`, `SONICTANK` | 32 × 32 | 1 |
| `TRIKE`, `RAIDER` | 28 × 26 | 1 |
| `FRIGATE` | 64 × 64 | 2 |
| `SOLDIER`, `INFANTRY`, `TROOPER`, `TROOPERS`, `UNIT_FREMEN_ONE`, `UNIT_FREMEN_THREE`, `SABOTEUR` | 32 × 32 | 3 |
| `SANDWORM` | 48 × 48 | 0 — начальное значение, отдельного назначения нет |

Ожидания положения, `visual`, `src` и `dest` вычислю непосредственно по формулам задания из этой таблицы. Текущие `sUnitInfo`, `getVisualRectangle()` и новый helper будут проверяемыми результатами, а не источниками ожиданий.

Матрицы строк 1–4 охватят `z={0,8;1,0;1,3;2,0}`, выбранный `s={1,00;1,10;1,25;1,50}`, все 64 пары направлений корпуса и башни. Значения `iFrame`: `0`, а при положительном `bmp_frames` также `1` и `bmp_frames`, без повторов.

### 2. Предлагаемый интерфейс `UnitSpriteLayout.hpp`

Реализацию заголовка пишет следующий исполнитель. Приёмочные тесты будут требовать следующий интерфейс без зависимости от SDL:

```cpp
struct UnitSpriteFrame {
    int width;
    int height;
    bool usesHdFrame;
};

struct UnitSpriteRectangle {
    int x;
    int y;
    int width;
    int height;
};

struct UnitSpriteFloatRectangle {
    float x;
    float y;
    float width;
    float height;
};

UnitSpriteFrame resolveUnitSpriteFrame(
    int bmpWidth,
    int bmpHeight,
    int hdFrameWidth,
    int hdFrameHeight,
    int textureDensity
);

UnitSpriteRectangle unitSpriteSourceRectangle(
    UnitSpriteFrame frame,
    int facingIndex,
    int animationFrame
);

UnitSpriteFloatRectangle unitSpriteDestinationRectangle(
    UnitSpriteFrame frame,
    UnitSpriteRectangle visual,
    float cameraZoom,
    float worldScale
);
```

Семантика:

- При плотности больше единицы и заданных положительных HD-размерах `width/height` равны физическим размерам HD-кадра, делённым на плотность; `usesHdFrame=true`.
- Без переопределения или при плотности `1` возвращается логический кадр `bmpWidth × bmpHeight`, `usesHdFrame=false`.
- Источник равен `{facingIndex·width, animationFrame·height, width, height}`.
- При HD-переопределении назначение рассчитывается с двумя округлениями размера и дробным центрированием по правилу задания.
- Без переопределения назначение точно равно переданному `visual`.

Новый метод `SDLDrawer`, который должен добавить исполнитель продукта:

```cpp
void renderStrechSpriteF(
    Texture *src,
    cRectangle srcPos,
    SDL_FRect destPos,
    Uint8 opacity = 255,
    SDL_BlendMode blendMode = SDL_BLENDMODE_BLEND
);
```

Метод умножает исходный прямоугольник на плотность текстуры и передаёт дробное назначение в `SDL_RenderCopyF`. Прежний `renderStrechSprite` сохраняется для старого пути.

### 3. Запись настоящего рисования

В `tests/UnitRenderFixture.cmake` зарегистрирую общую статическую библиотеку `d2tm_unit_frame_engine` из исходников движка без `src/main.cpp`, `src/drawers/SDLDrawer.cpp` и `src/drawers/cTextDrawer.cpp`.

Цели записи вызовов добавят тестовые определения настоящих невиртуальных методов из:

- `tests/UnitDrawRecorder.cpp`;
- `tests/UnitTextRecorder.cpp`.

Подмена происходит при линковке. `cUnit::draw`, `getVisualRectangle`, вспомогательные методы рисования и алгоритмы выбора остаются настоящими.

Регистратор сохраняет метод, указатель текстуры, `src`, целое или дробное `dest`, прозрачность, режим смешивания и порядок вызовов. Текстовый регистратор сохраняет координаты, цвет и содержание номера группы.

Наличие `renderStrechSpriteF` определю при конфигурации через `check_cxx_source_compiles` с `decltype(&SDLDrawer::renderStrechSpriteF)`. Условное определение метода в регистраторе включается только при наличии объявления. Проверка не вызывает метод и не требует его реализации; перед повторной конфигурацией результат проверки в кеше очищается. Поэтому регрессионные цели не зависят от появления нового метода на `main`.

Общие файлы `UnitFrameFixture.hpp/.cpp` определят глобальное окружение из `main.cpp`: `game`, карту, игроков, юнитов, таблицы описаний, `mapCamera`, `renderDrawer`, `gfxdata` и связанные массивы. Тестовые единицы трансляции получат `-fno-access-control` для установки закрытых полей окружения; исходники продукта этот флаг не получают.

Фикстура выставляет:

- размеры экрана, положение камеры, верхнюю панель и точное значение зума;
- плотность графики `1` или `4`, выбранный масштаб и действующий масштаб;
- `game.m_drawUnitDebug=false`;
- состояние юнита, владельца, слои карты и видимость;
- синтетические текстуры слоёв, `FOCUS`, `SYMB_PICKMEUP` и звёзд опыта.

Синтетический пак содержит необходимые числовые слоты. Настоящий `IniGameRessources::install_units()` задаёт производственные метаданные. В пиксельном тесте благодаря этому не требуется обращаться к новым полям: исполняемый файл соберётся на `main` и упадёт по проверке картинки.

Правка продукта для записи вызовов по результатам чтения не требуется. Линковка предложенной фикстуры пока не проверена сборкой.

### 4. C++-покрытие строк 1–5

| Строка | Файл и CTest | Проверки |
|---|---|---|
| 1 | `UnitSpriteLayoutTests.cpp`, `unit_sprite_layout` | Все направления Осадного, строка 0, источник 44 × 44, независимая башня, размер и центр назначения во всех 16 парах, включая половину пикселя. |
| 2 | `UnitHdFrameDrawTests.cpp`, `unit_hd_frame_draw` | Полная запись настоящего `draw` для `SIEGETANK` 176 × 176, `TANK` 160 × 160 и `HARVESTER` 352 × 224. У Харвестера проверяются строки 0, 1 и 4; шаг строки — 56 логических пикселей. |
| 3 | `UnitFrameInteractionsTests.cpp`, `unit_frame_interactions` | Настоящий `visual`, полосы, группа, опыт, символы, выбор, путь и отсечение. |
| 4 | `UnitDrawRegressionTests.cpp`, `unit_draw_regression` | Все типы без HD-переопределения в обеих графиках и Осадный в классике; точная последовательность всех вызовов. |
| 5 | `UnitRenderPixelsTests.cpp`, `unit_render_pixels` | Настоящие `Graphics::getHouseTexture`, `cUnit::draw`, `SDLDrawer` и программный SDL-рендерер. |

Регрессионные цели строк 3–4 не включают `UnitSpriteLayout.hpp` и не обращаются к `hd_frame_width/height`. Цели строк 1–2 отделены от них.

Для строки 3 выпишу ожидания из функций эталона:

- высота полосы — `max(1, lround(4·z·s))`;
- позиции и заполнение здоровья и спайса — по прежним формулам, включая рамку при высоте больше двух;
- группа — от `visual.x + max(3, visual.w−8)` и прежних вертикальных смещений;
- опыт — от `visual.x+3`, `visual.y−19`, с шагом звезды 9;
- `FOCUS` — весь `visual`, значок перевозки — `(visual.x, visual.y−7)`.

Настоящий поиск по ячейке проверю через `determineHoveringOverUnitId`, рамочное выделение — через `getAllMyUnitsWithinViewportRect`. Добавлю положительные контрольные случаи выбора. Путь проверю вызовом `draw_path()` с ожидаемыми координатами клеток и цветами сегментов. Для отсечения вызову `thinkFast_position()` и `isWithinViewport()` с областью, пересекающей только выступ картинки.

Строка 4 проверит наличие и отсутствие слоёв, отрицательное здоровье для башни, флаги выбора и перевозки, скрытого юнита и червя. Для тени фиксируются `ShadowTrans`, `SDL_BLENDMODE_BLEND` и смещение Carryall на 24. Дополнительных вызовов быть не должно.

Пиксельный тест создаст атлас и маску 1408 × 176 с различимыми метками своего и соседнего кадров. При `z=1`, действующем `s=1` и `1,25` проверит рамку альфы ≥128 с допуском один пиксель по каждой стороне, размер 44 × 44 или 55 × 55, положение относительно `visual`, метки краёв и цвет Дома. Инициализация — только `SDL_INIT_VIDEO`; уничтожение текстур предшествует уничтожению рендерера.

### 5. Python-покрытие строк 6–9

Создам три файла с шестью новыми методами.

**`tools/units3d/tests/test_siege_frame.py`:**

1. `test_build_reference_geometry_and_anchor` — настоящий CLI `redraw.py build`, старые кадры 144 × 152, новый атлас 1408 × 176, независимая медиана с `M=152`, перенос центра альфы на `(16,16)`.
2. `test_build_protective_shift_keeps_layers_aligned` — отдельная фигура, требующая защитного сдвига; ненулевой сдвиг, отсутствие обрезки всей альфы и совпадение смещения корпуса, перекраски и маски.
3. `test_real_siege_descriptions` — точное равенство всех перечисленных полей двух настоящих JSON, восьми путей перекрасок, масштабов и коридоров; отсутствие значения `"fit"`.

Для точного переноса без ресемплирования использую попытку 1024 × 1024 с фигурой `[474,550)²` и старую рамку `[34,110)²`. Медиана `1024/152` даёт холст ровно 1024, выходную рамку `[50,126)²` и центр `(88,88)`. Отдельный защитный случай со старой рамкой `[0,10)²` даёт итог `[0,76)²` и защитное перемещение `(17,17)`. Контрольная метка следующего столбца выявит ошибочную нарезку по ширине 176.

Существующий `test_redraw.py::test_01_build_atlases` останется прежним и проверит совместимость описания без новых полей.

**`tools/units3d/tests/test_install_geometry.py`:**

4. `test_pack_cli_geometry_policy`.
5. `test_install_cli_geometry_policy`.

Каждый метод отдельно проверит все пять разрешённых имён, переход размера и повторную установку. Затем проверит отказы для чужого атласа 1408 × 176, чужого исходного размера плюс один пиксель ширины, Осадного 1408 × 177 и 1152 × 176, смешанного правильного и неправильного набора. При отказах сравнит байты входного пака и заранее существующего выхода; при успехе — неизменность чужих payload.

**`tools/units3d/tests/test_siege_contract.py`:**

6. `test_generator_and_checker_siege_geometry` — копия пака из `D2TM_PACK_DIR`, пять синтетических замен, настоящий генератор и проверка новой геометрии Осадного. Для остальных записей сравнит с JSON, прочитанным через `git show bb2f1b37:docs/units/unit_contract.json`, семь полей:

`classic_size`, `hd4_size`, `frame_classic`, `frame_hd4`, `columns`, `rows`, `remainder_px`.

Ссылки на строки исходников не сравниваются. В том же методе `check_unit.py` примет согласованный Осадный и отвергнет чужой профиль и PNG новой геометрии при прежней записи его контракта.

В старом `test_unit_contract.py` изменю только две разрешённые проверки: исключение пяти имён из правила `classic×4` и фиксированные ожидания новой геометрии пяти записей. Других старых ожиданий, неизбежно конфликтующих с верной реализацией, чтение не выявило.

### 6. Файлы и CI

Новые C++-файлы:

```text
tests/UnitSpriteLayoutTests.cpp
tests/UnitHdFrameDrawTests.cpp
tests/UnitFrameInteractionsTests.cpp
tests/UnitDrawRegressionTests.cpp
tests/UnitRenderPixelsTests.cpp
tests/UnitFrameBaseline.hpp
tests/UnitFrameFixture.hpp
tests/UnitFrameFixture.cpp
tests/UnitDrawRecorder.hpp
tests/UnitDrawRecorder.cpp
tests/UnitTextRecorder.cpp
tests/UnitRenderFixture.cmake
```

Новые Python-файлы перечислены в разделе 5. Изменяемые файлы:

```text
tools/units3d/tests/test_unit_contract.py
tools/units3d/tests/ACCEPTANCE.sha256
CMakeLists.txt
.github/workflows/build_pr.yml
```

В `CMakeLists.txt` добавлю регистрацию тестов, подключение фикстуры и опцию `D2TM_UNIT_FRAME_RESOURCE_TESTS=OFF`. Под опцией будет регистрация существующего `russian_font_coverage`, читающего два настоящих шрифта. Новых ресурсных C++-тестов не будет. На servak опция включается.

В четырёх заданиях `build_pr.yml` после сборки добавлю только шаг CTest в соответствующей папке сборки:

```yaml
env:
  SDL_VIDEODRIVER: dummy
  SDL_RENDER_DRIVER: software
  SDL_AUDIODRIVER: dummy
```

Команда — `ctest --output-on-failure`. Пиксельный тест зарегистрирован в CI.

### 7. Прогоны, мутанты и сдача

После одобрения Python и C++ выполняются двумя субагентами `gpt-6-luna`, `xhigh`, одновременно. Субагент C++ отвечает также за CMake, workflow и C++-прогоны; субагент Python — за Python-прогон. Я отвечаю за интерфейс, сведение, таблицу мутантов и один итоговый аудит.

Python:

```sh
PYTHONDONTWRITEBYTECODE=1 \
TMPDIR="$PWD/.tmp/unittest-tmp" \
D2TM_PACK_DIR="$PWD/resources/bin/data" \
/srv/dune/venv/bin/python -m unittest discover \
  -s tools/units3d/tests -v
```

C++ собирается в копии `.tmp/u9t1-main-src`, без копирования `resources`, `.git` и `.tmp`; `resources` заменяется ссылкой на ресурсы рабочей копии. Сборка — `.tmp/u9t1-main-build`, по полностью прочитанному README:

```sh
u9t1_prefix=/srv/dune/deps/sdl2/root/usr
u9t1_lib="$u9t1_prefix/lib/x86_64-linux-gnu"

cmake -S .tmp/u9t1-main-src -B .tmp/u9t1-main-build \
  -DCMAKE_PREFIX_PATH="$u9t1_prefix" \
  -DCMAKE_BUILD_TYPE=Release \
  -DD2TM_UNIT_FRAME_RESOURCE_TESTS=ON \
  "-DCMAKE_CXX_FLAGS=-I$u9t1_prefix/include -I$u9t1_prefix/include/x86_64-linux-gnu" \
  "-DCMAKE_EXE_LINKER_FLAGS=-L$u9t1_lib -Wl,-rpath-link,$u9t1_lib"

cmake --build .tmp/u9t1-main-build -j 32 -- -k

SDL_VIDEODRIVER=dummy \
SDL_RENDER_DRIVER=software \
SDL_AUDIODRIVER=dummy \
LD_LIBRARY_PATH="$u9t1_lib" \
ctest --test-dir .tmp/u9t1-main-build --output-on-failure
```

На `main` ожидаются ошибки компиляции интерфейсных целей с именами отсутствующих заголовка или полей, красный пиксельный тест и зелёные регрессионные цели и прежние CTest. Для Python сохраню строки результатов и причины красных проверок. Пропуск новых Python-тестов или класса контракта вызывает `Q`.

После прогона удалю исходную копию командой с буквальным путём:

```sh
rm -rf /srv/dune/worktrees/u9f/.tmp/u9t1-main-src
```

Таблица мутантов в сдаче будет привязана к фактическому тексту тестов. Планируемые связи: геометрия — 4, 5, 12, 16; настоящий HD `draw` — 3, 6; регрессия — 2, 7, 13; сборка атласов — 8, 9, 15; установка — 10, 14; контракт — 11. Настоящие описания обнаруживают мутант 1. Для мутантов 2–16 укажу «не проверено прогоном»; реализацию продукта и мутанты создавать не буду.

Обновлю SHA-256 новых Python-тестов и изменённого теста в существующем формате `ACCEPTANCE.sha256`; C++-суммы приведу отдельным списком в сдаче. Коммитов не делаю. В `DONE-U9-T1` перечислю предлагаемые сообщения коммитов с последней строкой `Behavior changes: none`, точные файлы, результаты, ограничения и `git status --short`.

### 8. Развилки, ограничения и текущая проверка

Рекомендую линковочный регистратор с общей статической библиотекой: он проверяет настоящий код и не требует правки продукта. Пиксельную проверку рекомендую оставить полностью синтетической, чтобы она выполнялась в CI без LFS.

Объём — пять новых CTest, шесть Python-методов, общие фикстуры, две разрешённые правки старых ожиданий и четыре шага CI. Художественное качество настоящих атласов, реализация продукта, зелёный прогон будущей реализации и запуск CI этим заданием не выполняются.

Не проверены сборкой предложенная линковка и её переносимость между четырьмя платформами. Тестовые прогоны ещё не выполнялись. Свободное место при чтении — `8772186112` байт; отслеживаемых изменений нет. При условиях остановки из задания оформлю `Q`.

**Остановка до `PLAN-OK-U9-T1`.**