## A-P10A-01 — ответ на Q-P10A-01

Нет, `src/game/cTimeCounter.cpp` и `src/context/AudioContext.cpp` в `TEST_SOURCES` не добавляются: `AudioContext` одновременно переписывает соседний шаг, и тесты не должны от него зависеть. Тест T3 меняется так:

1. Из `TEST_SOURCES` в `tests/CMakeLists.txt` убираются все строки, которые этот шаг добавил ради `test_MouseClickInit.cpp` (`src/controls/cMouse.cpp`, `src/context/GameContext.cpp`, `src/context/TextContext.cpp` и каждая строка, добавленная сверх них). Строки `TEST_FILES` не меняются.
2. `tests/controls/test_MouseClickInit.cpp` переписывается без `cMouse`, `GameContext` и `SDLDrawer`. Он подключает `<catch2/catch_test_macros.hpp>`, `<filesystem>`, `<fstream>`, `<string>` и читает файл `std::filesystem::path(D2TM_SOURCE_DIR) / "src/controls/cMouse.h"` построчно (`std::ifstream` от `std::filesystem::path`). «Строка без краёв» — строка файла без пробелов и табуляций в начале и в конце. Два случая с прежними именами:
   - `P10A left button is not clicked after creation` — `REQUIRE(<в файле есть строка без краёв, равная "bool m_leftButtonClicked = false;">)`;
   - `P10A right button is not clicked after creation` — `REQUIRE(<в файле есть строка без краёв, равная "bool m_rightButtonClicked = false;">)`.
   Перед поиском — `REQUIRE(<файл открыт>)` в каждом случае.
3. Пункт 4 контракта (`= false` у двух флагов в `cMouse.h`) не меняется.

Продолжай с проверки 1 раздела «Проверки» (сборка заново) и дальше по порядку до сдачи `## DONE-P10A`. Запись в «Решено исполнителем» об этой замене не нужна: она — ответ ведущего.
