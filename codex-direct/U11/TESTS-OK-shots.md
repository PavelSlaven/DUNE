# TESTS-OK-U11-S — тесты этапа A приняты с двумя поправками

Тесты — блок `## TESTS-U11-S | 2026-11-02` исполнителя; суммы файлов в рабочей копии `/srv/dune/worktrees/u11` сверены ведущим и равны строкам блока. Принято: 43 теста проверки журнала по правилам 1–6, 11 тестов комплектности, три CTest, раскладка `png/<WxH>/<lang>/<gfx>/<scene>.png` и `logs/<WxH>/<lang>/<gfx>/<scene>.geometry.jsonl`, имена `src/debug/UiAuditArguments.hpp`, `uiaudit::consumeArguments(int&, char**)`, `isEnabled()`, `options()` с полями `list`, `scene`, `outDir`. Правило 2 флагует и текст, целиком накрывший элемент; правило 3 не флагует вложение и равные прямоугольники — принято.

## Поправки — сделать до этапа B, дословно

1. **CTest с запуском игры — только по опции CMake.** Задания CI в `.github/workflows/release.yml` (строки 143, 191, 251) берут репозиторий с `lfs: false` и запускают `ctest` на Windows, Linux и macOS: файлы `resources/` там — указатели Git LFS, а `make_runtime` в `tests/ui_audit_runtime_support.py` копирует игру под именем `d2tm` и делает символические ссылки. Тесты `ui_audit_unknown_scene` и `ui_audit_main_menu_png` в CI упали бы. В `CMakeLists.txt` блок регистрации этих двух тестов замени на:

   ```cmake
       option(D2TM_UI_AUDIT_RUNTIME_TESTS "Run the UI audit tests that start the game; they need the real resources/ files" OFF)
       if(D2TM_UI_AUDIT_RUNTIME_TESTS)
           find_package(Python3 REQUIRED COMPONENTS Interpreter)
           add_test(
               NAME ui_audit_unknown_scene
               COMMAND
                   ${Python3_EXECUTABLE}
                   ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_unknown_scene.py
                   --exe $<TARGET_FILE:${PROJECT_NAME}>
                   --resources ${CMAKE_CURRENT_SOURCE_DIR}/resources
           )
           add_test(
               NAME ui_audit_main_menu_png
               COMMAND
                   ${Python3_EXECUTABLE}
                   ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_main_menu_png.py
                   --exe $<TARGET_FILE:${PROJECT_NAME}>
                   --resources ${CMAKE_CURRENT_SOURCE_DIR}/resources
           )
       endif()
   ```

   Цель `ui_audit_arguments_tests` и тест `ui_audit_arguments` остаются без условия. Все сборки на servak на этапах B и C — с `-DD2TM_UI_AUDIT_RUNTIME_TESTS=ON`; в сдаче — строка `ctest -N` с 23 тестами.

2. **Правило 6 сравнивает только при одинаковой графике.** В класс `ResolutionDifferenceRule` файла `tools/ui-audit/tests/test_check_geometry.py` сразу после метода `test_different_language_is_not_compared` добавь:

   ```python
       def test_different_graphics_is_not_compared(self):
           flags = self.pair([text("Apply", 10, 10, 40, 12)],
                             [text("Apply", 99, 10, 40, 12)], graphics="classic")
           self.assertEqual(flags, [])
   ```

После правок: строки `sha256sum` файлов `tools/ui-audit/tests/test_check_geometry.py` и вывода `git diff CMakeLists.txt | sha256sum` — в журнал `.tmp/progress-u11s.md` и в сдачу; дальше тесты не меняются. Других изменений в тестах нет. Снова останавливаться не нужно: после правок сразу этап B.

## Дальше

Этап B по заданию `codex-direct/U11/TASK-shots.md`, затем этап C. Место на `/` до этапа C освобождает ведущий; остаток меньше 5 ГБ перед сочетанием — блок `## Q-U11-S-NN` и стоп, как в задании.
