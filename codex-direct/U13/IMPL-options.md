# Задание U13-I — раскладка главной страницы окна настроек без наложений

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже). Исполнитель: Codex `gpt-6.1-sol` `high`; помощник — субагент `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u13`, ветка `codex/u13-options`, HEAD — коммит `bd2187cd` с приёмочным тестом или новее. Коммитов не делай: ведущий коммитит по списку из сдачи.

## Цель

Issue #31: на главной странице окна настроек кнопки низа ложатся на строки настроек. Сделай раскладку по `codex-direct/U13/LAYOUT.md`: кнопки низа — рядами по три, окно растёт в высоту только там, где иначе не помещается, и остаётся внутри холста. Готово, когда замороженный приёмочный тест `options_menu_layout_geometry` проходит, игра собирается, остальные тесты CTest проходят, а в игре окно и кнопки стоят по `LAYOUT.md` (это проверяет ведущий после сдачи).

## Источник истины

- Поведение и формулы — `codex-direct/U13/LAYOUT.md`, разделы «Входы», «Величины», «Результат», «Строки содержимого», «Что меняется в `cOptionsState`».
- Приёмочный тест — `tests/OptionsMenuLayoutTests.cpp` и цель `options_menu_layout_tests` в `CMakeLists.txt`. Они заморожены: суммы — в `/srv/dune/tasks/u13/frozen.sha256` (`sha256sum -c /srv/dune/tasks/u13/frozen.sha256` из корня рабочей копии). Эти два файла не меняй. Если тест, по-твоему, требует не того, что написано в `LAYOUT.md`, — остановка `Q`, тест не ослабляй.

## Что сделать

1. **`src/gamestates/OptionsMenuLayout.hpp`.** Новое поле `cRectangle window`. Новая сигнатура `static OptionsMenuLayout create(int canvasWidth, int canvasHeight, int buttonHeight, bool hdLayout, bool playing)`; прямоугольники — по формулам `LAYOUT.md`, разделы «Величины» и «Результат». Прежняя сигнатура с восемью параметрами удаляется. Имена прежних полей не меняются.
2. **`src/gamestates/cOptionsState.cpp`, `cOptionsState::constructWindow`, ветка главной страницы** (строки 755–812 сейчас):
   - вызов `OptionsMenuLayout::create(m_game.m_screenW, m_game.m_screenH, buttonHeight, m_hdLayout, m_prevState == GAME_PLAYING)` — после расчёта `buttonHeight`;
   - `GuiWindow` создаётся с прямоугольником `menuLayout.window`; переменные `mainMenuHeight`, `mainMenuFrameX`, `mainMenuFrameY` и их формулы удаляются;
   - `mainMenuWidth` = `menuLayout.window.getWidth()`; все прочие расчёты, где стоит `mainMenuWidth` или `buttonWidth`, остаются как есть;
   - строки 1–9, надписи, темы, действия кнопок и способ передачи прямоугольников кнопок через `relativeRect(menuLayout.<поле>)` не меняются.
3. Больше ничего не меняй. `constructAdvancedWindow`, `src/gamestates/cOptionsState.h`, `src/gui/GuiWindow.cpp` не трогай: их правит другая задача.

## Чем проверить

- Сборка по рецепту `/srv/dune/deps/sdl2/README.txt` (прочитай его целиком), папка сборки — `.tmp/u13i-build/`. Собери все цели (`cmake --build .tmp/u13i-build -j 32`).
- До правок: `cmake --build .tmp/u13i-build --target options_menu_layout_tests` не собирается (ошибка компилятора про `window` или число аргументов `create`) — строка ошибки в сдаче как красный результат.
- После правок: сборка всех целей — код 0; `ctest --test-dir .tmp/u13i-build --output-on-failure` с переменными окружения из рецепта — все тесты `Passed`; строка `Проверено случаев матрицы А + Б: 140320` из прямого запуска `options_menu_layout_tests`.
- `sha256sum -c /srv/dune/tasks/u13/frozen.sha256` — оба файла `OK`.
- `git diff --stat` — ровно два файла: `src/gamestates/OptionsMenuLayout.hpp`, `src/gamestates/cOptionsState.cpp`; `git diff --check` — пустой вывод.

## Что не трогать

Замороженные `tests/OptionsMenuLayoutTests.cpp` и `CMakeLists.txt`; другие тесты в `tests/`; `src/gamestates/cOptionsState.h`; `src/gui/`; `constructAdvancedWindow`; `resources/`; `.github/`; задания в `codex-direct/`.

## Организация работы

- Порядок: чтение `LAYOUT.md`, теста, рецепта сборки и `constructWindow` → PLAN → `PLAN-OK-U13-I` → красный прогон до правок → правка `OptionsMenuLayout.hpp` → правка `constructWindow` → сборка всех целей и CTest → суммы замороженных файлов → сдача `## DONE-U13-I`.
- Параллельно: после `PLAN-OK` помощник настраивает папку сборки и делает красный прогон, пока ты пишешь правки.
- Помощники: один субагент `gpt-6-luna` `xhigh` — сборки, прогоны CTest, выжимки логов. Сам — PLAN, правки кода, сверка с `LAYOUT.md`, итоговая сверка с заданием.
- Перед командами `git` выполняй `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`. 46 двоичных файлов в рабочей копии помечены локальным флагом `assume-unchanged`: их содержимое побайтно совпадает с git, флаг не снимай.
- Остановки — блок `## Q-U13-I-NN` и стоп: замороженный тест падает на реализации по формулам `LAYOUT.md`; для правки нужно изменить файл из раздела «Что не трогать»; после правок падает любой тест CTest; свободного места на `/` меньше 5 ГБ (`df -B1 /` перед каждой сборкой); команда оболочки дважды подряд не завершилась и за 30 минут не дописала ни строки в журнал.
- Рамка правок: `src/gamestates/OptionsMenuLayout.hpp`, `src/gamestates/cOptionsState.cpp`, `.tmp/`.
- Журнал: `.tmp/progress-u13i.md`, строка после каждого шага порядка; это имя сильнее имени журнала в правилах исполнителя ниже.
- Коммитов не делай; раздел `### Коммиты` в сдаче: сообщение и список файлов.
- Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
