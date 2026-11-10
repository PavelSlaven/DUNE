# Задание P5CT — приёмочные тесты боевого HUD (шаг П5в)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны сборки делает один субагент `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5c`, `HEAD` — `7eb119b007c05f063fe6dacf2e93ae31ac135b33` (вершина ветки порта после шага П5б). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5ct/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Написать приёмочные тесты шага П5в по контракту API ниже, получить красные прогоны A и B и зелёный прогон C по заявленным причинам и заморозить тесты хэшем. Код игры не менять, кроме временных файлов прогонов B и C (шаг 2), которые убираются сразу после каждого из них.

## Что уже решено

Шаг П5в переносит на боевой HUD порта геометрию форка `HudLayout`: боковую панель, список построек, мини-карту, строку сообщений, полосу кредитов, гербы Домов. Заголовок `src/sidebar/HudLayout.hpp` переносится дословной копией ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566`; приёмка раскладки — тест форка `tests/HudLayoutTests.cpp` той же ревизии, перенесённый на Catch2, и четыре новых теста ниже. Холст игры порта — не меньше 800 × 600; тесты проверяют холсты шириной 800–3840 и высотой 600–2160.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `tests/utils/test_OptionsMenu.cpp` — образец переноса теста форка на Catch2;
- `tests/CMakeLists.txt`;
- `src/utils/cRectangle.h`, `src/utils/cRectangle.cpp`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HudLayoutTests.cpp` — тест форка, который переносишь;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp` — заголовок форка.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт API

Этот раздел дословно входит и в задание исполнителя кода.

1. **Раскладка боевого HUD (новый файл).** `src/sidebar/HudLayout.hpp` — дословная копия одноимённого файла ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566` (команда `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp`). В нём структура `HudLayout`: константа `static constexpr int TopBarHeight = 42;`; поля `screenWidth`, `screenHeight`, `sidebarWidth`, `columns`, `cardGap`, `cardWidth`, `cardHeight` типа `int`; поля `topBar`, `battlefield`, `sidebar`, `credits`, `radarPanel`, `houseHeader`, `radarViewport`, `powerMeter`, `spiceMeter`, `tabs`, `catalog`, `cards`, `scrollbar` типа `cRectangle`; статический метод `create(int logicalWidth, int logicalHeight, bool reserveStarportOrderArea = false)`; методы `visibleRows()`, `totalRows(int itemCount)`, `maxScrollRow(int itemCount)`, `cardRect(int itemIndex, int scrollRow)`, `tabRect(int tabIndex, int tabCount = 6)`, `scrollbarThumb(int itemCount, int scrollRow)`. Заголовок не добавляется в `src/CMakeLists.txt` и в `TEST_SOURCES` файла `tests/CMakeLists.txt`: у него нет файла `.cpp`.

## Шаг 1. Тесты — корневая нить сама

Catch2 3, как остальные файлы `tests/`. У каждого `TEST_CASE` имя начинается с `P5C `, тег — `[P5C]`.

### Новый файл `tests/utils/test_HudLayout.cpp`

Файл состоит из частей ниже, по порядку.

1. Подключения — ровно эти строки:
   ```cpp
   #include <catch2/catch_test_macros.hpp>

   #include "sidebar/HudLayout.hpp"

   #include <algorithm>
   ```
2. Анонимное пространство имён: строка `namespace {`; затем строки 7–44 файла форка `tests/HudLayoutTests.cpp@9208dcf5a358f40afd95c99480e4e09f781ed566` (функция `verifyHdLayout`) дословно, кроме одного изменения: каждое из 13 вхождений `assert(` заменено на `CHECK(`; затем две функции ровно такого вида:
   ```cpp
   bool inside(const cRectangle &inner, const cRectangle &outer)
   {
       return inner.getX() >= outer.getX() && inner.getEndX() <= outer.getEndX() &&
              inner.getY() >= outer.getY() && inner.getEndY() <= outer.getEndY();
   }

   bool sameRect(const cRectangle &rect, int x, int y, int width, int height)
   {
       return rect.getX() == x && rect.getY() == y && rect.getWidth() == width && rect.getHeight() == height;
   }
   ```
   и строка `}`. Функции `main` форка в файле нет: её четыре вызова переходят в тест 1.
3. Пять тестов ровно такого вида, по порядку:

```cpp
TEST_CASE("P5C hud layout keeps the fork examples", "[P5C]")
{
    verifyHdLayout(800, 600, 280, 2);
    verifyHdLayout(1067, 600, 360, 3);
    verifyHdLayout(1280, 720, 360, 3);
    verifyHdLayout(1920, 1080, 360, 3);
}

TEST_CASE("P5C hud layout fits every canvas", "[P5C]")
{
    int cases = 0;
    int sidebarFailures = 0;
    int topFailures = 0;
    int panelFailures = 0;
    int orderFailures = 0;
    int radarFailures = 0;
    int catalogFailures = 0;
    int cardSizeFailures = 0;
    for (int width = 800; width <= 3840; ++width) {
        for (int height = 600; height <= 2160; ++height) {
            ++cases;
            const HudLayout layout = HudLayout::create(width, height);
            const int expectedSidebar = width < 960 ? 280 : 360;
            const int expectedColumns = width < 960 ? 2 : 3;
            if (layout.sidebarWidth != expectedSidebar || layout.columns != expectedColumns ||
                !sameRect(layout.sidebar, width - expectedSidebar, 0, expectedSidebar, height)) {
                ++sidebarFailures;
            }
            if (!sameRect(layout.topBar, 0, 0, width, HudLayout::TopBarHeight) ||
                !sameRect(layout.battlefield, 0, HudLayout::TopBarHeight, width - expectedSidebar,
                          height - HudLayout::TopBarHeight)) {
                ++topFailures;
            }
            if (!inside(layout.credits, layout.sidebar) || !inside(layout.radarPanel, layout.sidebar) ||
                !inside(layout.tabs, layout.sidebar) || !inside(layout.catalog, layout.sidebar)) {
                ++panelFailures;
            }
            if (layout.credits.getEndY() > layout.radarPanel.getY() ||
                layout.radarPanel.getEndY() > layout.tabs.getY() ||
                layout.tabs.getEndY() > layout.catalog.getY()) {
                ++orderFailures;
            }
            if (!inside(layout.houseHeader, layout.radarPanel) || !inside(layout.radarViewport, layout.radarPanel) ||
                !inside(layout.powerMeter, layout.radarPanel) || !inside(layout.spiceMeter, layout.radarPanel) ||
                layout.houseHeader.getEndY() > layout.radarViewport.getY() ||
                layout.radarViewport.getEndY() > layout.powerMeter.getY() ||
                layout.powerMeter.getY() != layout.spiceMeter.getY() ||
                layout.powerMeter.getEndX() > layout.spiceMeter.getX()) {
                ++radarFailures;
            }
            if (!inside(layout.cards, layout.catalog) || !inside(layout.scrollbar, layout.catalog) ||
                layout.cards.getEndX() > layout.scrollbar.getX()) {
                ++catalogFailures;
            }
            if (layout.cardWidth < 99 || layout.cardHeight <= 100) {
                ++cardSizeFailures;
            }
        }
    }
    CHECK(cases == 4747001);
    CHECK(sidebarFailures == 0);
    CHECK(topFailures == 0);
    CHECK(panelFailures == 0);
    CHECK(orderFailures == 0);
    CHECK(radarFailures == 0);
    CHECK(catalogFailures == 0);
    CHECK(cardSizeFailures == 0);
}

TEST_CASE("P5C hud layout keeps visible cards and the scrollbar thumb inside the catalog", "[P5C]")
{
    int cases = 0;
    int cardFailures = 0;
    int columnOrderFailures = 0;
    int rowOrderFailures = 0;
    int thumbFailures = 0;
    int thumbEndFailures = 0;
    for (const int width : {800, 959, 960, 3840}) {
        for (int height = 600; height <= 2160; ++height) {
            const HudLayout layout = HudLayout::create(width, height);
            for (int itemCount = 0; itemCount <= 40; ++itemCount) {
                const int maxScroll = layout.maxScrollRow(itemCount);
                for (int scrollRow = 0; scrollRow <= maxScroll; ++scrollRow) {
                    ++cases;
                    const int first = scrollRow * layout.columns;
                    const int last = std::min(itemCount, (scrollRow + layout.visibleRows()) * layout.columns);
                    for (int item = first; item < last; ++item) {
                        const cRectangle card = layout.cardRect(item, scrollRow);
                        if (!inside(card, layout.cards)) {
                            ++cardFailures;
                        }
                        if (item + 1 < last && (item + 1) % layout.columns != 0 &&
                            card.getEndX() > layout.cardRect(item + 1, scrollRow).getX()) {
                            ++columnOrderFailures;
                        }
                        if (item + layout.columns < last &&
                            card.getEndY() > layout.cardRect(item + layout.columns, scrollRow).getY()) {
                            ++rowOrderFailures;
                        }
                    }
                    const cRectangle thumb = layout.scrollbarThumb(itemCount, scrollRow);
                    if (thumb.getX() != layout.scrollbar.getX() || thumb.getWidth() != layout.scrollbar.getWidth() ||
                        thumb.getY() < layout.scrollbar.getY() || thumb.getEndY() > layout.scrollbar.getEndY()) {
                        ++thumbFailures;
                    }
                    if (maxScroll == 0) {
                        if (!sameRect(thumb, layout.scrollbar.getX(), layout.scrollbar.getY(),
                                      layout.scrollbar.getWidth(), layout.scrollbar.getHeight())) {
                            ++thumbEndFailures;
                        }
                    } else if (thumb.getHeight() < 22 ||
                               (scrollRow == 0 && thumb.getY() != layout.scrollbar.getY()) ||
                               (scrollRow == maxScroll && thumb.getEndY() != layout.scrollbar.getEndY())) {
                        ++thumbEndFailures;
                    }
                }
            }
        }
    }
    CHECK(cases == 955624);
    CHECK(cardFailures == 0);
    CHECK(columnOrderFailures == 0);
    CHECK(rowOrderFailures == 0);
    CHECK(thumbFailures == 0);
    CHECK(thumbEndFailures == 0);
}

TEST_CASE("P5C hud layout splits the tab strip into six tabs", "[P5C]")
{
    for (const int width : {800, 960, 1920}) {
        const HudLayout layout = HudLayout::create(width, 720);
        CHECK(layout.tabRect(0).getX() == layout.tabs.getX());
        CHECK(layout.tabRect(5).getEndX() == layout.tabs.getEndX());
        for (int tab = 0; tab < 6; ++tab) {
            const cRectangle rect = layout.tabRect(tab);
            CHECK(rect.getY() == layout.tabs.getY());
            CHECK(rect.getHeight() == layout.tabs.getHeight());
            CHECK(rect.getWidth() > 0);
            if (tab < 5) {
                CHECK(rect.getEndX() == layout.tabRect(tab + 1).getX());
            }
        }
    }
}

TEST_CASE("P5C hud layout reserves the starport order area", "[P5C]")
{
    int cases = 0;
    int failures = 0;
    for (const int width : {800, 960}) {
        for (int height = 600; height <= 2160; ++height) {
            ++cases;
            if (HudLayout::create(width, height, true).catalog.getEndY() != height - 54 ||
                HudLayout::create(width, height, false).catalog.getEndY() != height - 6) {
                ++failures;
            }
        }
    }
    CHECK(cases == 3122);
    CHECK(failures == 0);
}
```

Числа `cases` посчитаны ведущим моделью заголовка форка: 4747001 = 3041 ширина × 1561 высота; 955624 — сумма `maxScrollRow(itemCount) + 1` по четырём ширинам, 1561 высоте и 41 значению `itemCount`; 3122 = 2 ширины × 1561 высота. Все счётчики сбоев на заголовке форка равны 0.

### Правка `tests/CMakeLists.txt`

В список `TEST_FILES` строка `${CMAKE_CURRENT_SOURCE_DIR}/utils/test_HudLayout.cpp` сразу после строки `${CMAKE_CURRENT_SOURCE_DIR}/utils/test_OptionsMenu.cpp`. Других правок в `tests/CMakeLists.txt` нет.

Другие файлы `tests/` и весь код вне `tests/` не меняются.

## Шаг 2. Прогоны — субагент `gpt-6-luna` `xhigh`

Перед каждой сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P5CT-01` и стоп. Команда сборки из корня рабочей копии (в `<лог>` — имя файла ниже):

```
DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5ct/<лог> 2>&1
```

Субагент сдаёт корневой нити код выхода каждого прогона, все строки лога прогона и `.tmp/out/logs/<последняя папка>/full.log`, содержащие `error:`, вывод `grep -A3 "CMake Error"` по тем же двум файлам и, если есть `ctest.log` последней папки логов, его строки с `P5C `, `Failed`, `failed` и итоговую строку `tests passed`.

- **Прогон A** — лог `build-red-a.log`, рабочая копия как после шага 1. Ожидается: код выхода не 0; блоков `CMake Error` нет; строки `error:` есть, и каждая содержит `sidebar/HudLayout.hpp: No such file or directory`.
- **Прогон B** — лог `build-red-b.log`. Перед ним субагент создаёт временный файл `src/sidebar/HudLayout.hpp` ровно такого вида:
  ```cpp
  #pragma once

  #include "utils/cRectangle.h"

  struct HudLayout {
      static constexpr int TopBarHeight = 0;

      int screenWidth = 0;
      int screenHeight = 0;
      int sidebarWidth = 0;
      int columns = 1;
      int cardGap = 0;
      int cardWidth = 0;
      int cardHeight = 0;

      cRectangle topBar;
      cRectangle battlefield;
      cRectangle sidebar;
      cRectangle credits;
      cRectangle radarPanel;
      cRectangle houseHeader;
      cRectangle radarViewport;
      cRectangle powerMeter;
      cRectangle spiceMeter;
      cRectangle tabs;
      cRectangle catalog;
      cRectangle cards;
      cRectangle scrollbar;

      static HudLayout create(int, int, bool = false)
      {
          return HudLayout{};
      }

      [[nodiscard]] int visibleRows() const
      {
          return 1;
      }

      [[nodiscard]] int totalRows(int) const
      {
          return 0;
      }

      [[nodiscard]] int maxScrollRow(int) const
      {
          return 0;
      }

      [[nodiscard]] cRectangle cardRect(int, int) const
      {
          return cRectangle();
      }

      [[nodiscard]] cRectangle tabRect(int, int = 6) const
      {
          return cRectangle();
      }

      [[nodiscard]] cRectangle scrollbarThumb(int, int) const
      {
          return cRectangle();
      }
  };
  ```
  Сразу после прогона B — `rm src/sidebar/HudLayout.hpp`. Ожидается: строк `error:` нет; код выхода не 0; в `ctest.log` провалены ровно пять тестов — все пять тестов `P5C ` из шага 1; остальные тесты — `Passed`.
- **Прогон C** — лог `build-green-c.log`. Перед ним субагент создаёт временный файл заголовка форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/HudLayout.hpp > src/sidebar/HudLayout.hpp`. Сразу после прогона C — `rm src/sidebar/HudLayout.hpp`. Ожидается: код выхода 0; строк `error:` нет; все пять тестов `P5C ` — `Passed`; итоговая строка `ctest.log` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` на 5 больше числа тестов в итоговой строке `ctest.log` последней сборки шага П5б (307).

Проверка уборки после прогонов B и C: `test ! -e src/sidebar/HudLayout.hpp` с кодом выхода 0, иначе блок `## Q-P5CT-05` и стоп.

Ошибка другого рода в файле теста (опечатка, неверный тип, неверный заголовок проекта) — корневая нить исправляет тест так, чтобы его текст по-прежнему совпадал с шагом 1, и повторяет прогоны с A. Ошибки вне `tests/utils/test_HudLayout.cpp` и `tests/CMakeLists.txt`; провал другого теста в прогоне B или C; в прогоне B любой из пяти тестов `P5C ` со статусом `Passed` или `Skipped`; в прогоне C любой из пяти тестов `P5C ` со статусом, отличным от `Passed`, — блок `## Q-P5CT-02` с этими строками и стоп. Ожидание теста под заголовок не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5CT-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/utils/test_HudLayout.cpp tests/CMakeLists.txt > .tmp/p5ct/tests.sha256`. После этой команды файлы тестов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5ct/lfs status --short` выводит ровно две строки: ` M tests/CMakeLists.txt` и `?? tests/utils/test_HudLayout.cpp`. Строки `__pycache__` в выводе допустимы; другие строки — блок `## Q-P5CT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5CT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- коды выхода прогонов A, B и C, их строки `error:`, вывод `grep -A3 "CMake Error"` и строки `ctest.log` из шага 2 (не больше 80 строк на прогон; если больше — первые 80 и их число);
- число проверок `CHECK` в новом файле — вывод `grep -cE '\bCHECK\(' tests/utils/test_HudLayout.cpp`;
- вывод `diff <(git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HudLayoutTests.cpp | sed -n '7,44p' | sed 's/assert(/CHECK(/') <(sed -n '/^void verifyHdLayout/,/^}$/p' tests/utils/test_HudLayout.cpp)` и его код выхода (ожидается 0 и пустой вывод);
- содержимое `.tmp/p5ct/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — два файла шага 3, сообщение на английском о приёмочных тестах раскладки боевого HUD: перенос теста раскладки форка и проверки холстов, карточек, полосы прокрутки, вкладок и места панели заказов космопорта; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5ct --size`; у `.tmp/p5ct` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out` и `.tmp/deps` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме временных файлов прогонов B и C.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаг 1 → шаг 2 (прогон A, затем прогон B, затем прогон C) → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один субагент `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды сборки, временные файлы прогонов B и C и их уборка, выписка строк ошибок и строк `ctest.log`. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме временных файлов прогонов B и C и логов в `.tmp/p5ct/`. Шаги 1 и 3, разбор ошибок и сдачу делает корневая нить.
- **Остановки:** только на `## DONE-P5CT` и на блоках `## Q-P5CT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5CT-04` и стоп.
- **Рамка правок:** `tests/utils/test_HudLayout.cpp`, `tests/CMakeLists.txt`, временные файлы прогонов B и C и папка `.tmp/p5ct/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`; это не правка.

Не отступай от плана, не переусложняй.

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
