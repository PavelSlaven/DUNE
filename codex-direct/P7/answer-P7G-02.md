## ANSWER-Q-P7G-02

Да: `tests/CMakeLists.txt` и новый файл `tests/utils/UiAuditRecordStub.cpp` входят в рамку правок. Исполняй пункты по порядку.

1. **`tests/CMakeLists.txt`.** В список `TEST_SOURCES` после строки `${CMAKE_SOURCE_DIR}/src/drawers/SDLDrawer.cpp` добавь две строки: `${CMAKE_SOURCE_DIR}/src/drawers/cTextDrawer.cpp` и `${CMAKE_SOURCE_DIR}/src/drawers/cTextTextureCache.cpp`. Других правок в этом файле нет, кроме пункта 2.
2. **Заглушка записи режима снимков.** `cTextDrawer.cpp` вызывает `uiaudit::recordText` и создаёт `uiaudit::BoxScope` только при `uiaudit::isEnabled()`; их определения лежат в `src/debug/UiAuditCapture.cpp`, который тянет в тесты всю игру (`game/cGame.h`). В тестах режим снимков выключен, эти функции не вызываются.
   - Если после пункта 1 линковка `d2tm_tests` не находит `uiaudit::recordText`, `uiaudit::BoxScope::BoxScope` или `uiaudit::BoxScope::~BoxScope`, создай файл `tests/utils/UiAuditRecordStub.cpp` и добавь строку `${CMAKE_CURRENT_SOURCE_DIR}/utils/UiAuditRecordStub.cpp` в конец списка `TEST_FILES`.
   - Содержимое файла: `#include "debug/UiAudit.hpp"`, затем строка комментария `// The recorder lives with the game loop in UiAuditCapture.cpp; tests run with the UI audit off and never call it.`, затем в `namespace uiaudit` пустые определения: `void recordText(const std::string &, int, int, int, int, const Rect *) {}`, `BoxScope::BoxScope(int, int, int, int) {}`, `BoxScope::~BoxScope() {}`. Других определений в файле нет.
   - Если линковка находит все три без файла — файл не создавай.
3. **Другие ненайденные символы** после пунктов 1–2 — блок `## Q-P7G-03` с полным списком строк `undefined reference` и стоп.
4. **Дальше** — шаг 6 плана с проверки 1. В проверке 2 к фильтру путей добавь `tests/utils/UiAuditRecordStub`; в проверке 6 допустимы новый путь `?? tests/utils/UiAuditRecordStub.cpp` (если создан) и ` M tests/CMakeLists.txt`. В сдаче — `git diff` файла `tests/CMakeLists.txt` и содержимое заглушки; в списке коммитов эти два файла входят в коммит «тесты T5 и T4».

Помощники, остановки и остальная рамка правок — как в задании P7G.

Не отступай от плана, не переусложняй.
