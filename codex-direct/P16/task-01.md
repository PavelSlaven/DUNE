# Ответ на Q-P16-01 — PLAN-P16-delta-01

Продолжай с шага 5 (проверки). Работа шагов 0–4 остаётся в рабочей копии, её не переделывать.

1. **`T4 HD4 packs can be read by DataPack`** — упал вне задачи: картинки владельца сделали сцены ментата однокадровыми, эталон исправлен PR #151 в ветке порта (`18be7f33e66c6636c48be74e38689e90eeb5dc01`). Ветку порта в `codex/p16` вливает ведущий перед PR. В проверке 2 вместо `100% tests passed, 0 tests failed` ожидается: в `ctest.log` упал ровно один тест — `T4 HD4 packs can be read by DataPack`; любой другой упавший тест — `Q` и стоп.
2. **Разрешённые изменения ожиданий существующих тестов** (размер по умолчанию теперь 0 — решение владельца Р85):
   - `tests/utils/test_Preferences.cpp`, случаи «P5B preferences saveScales creates a missing file» и «P5B preferences loadScales reads only the scale keys»: `CHECK(loaded.screenW == 800)` → `CHECK(loaded.screenW == 0)`; если в этих двух случаях есть `CHECK(loaded.screenH == 600)` — → `CHECK(loaded.screenH == 0)`;
   - `tests/utils/test_PreferencesPages.cpp`, случай с `valuesOf` (около строки 155): `{"ScreenWidth", "800"}` → `{"ScreenWidth", "0"}`.
   Других изменений ожиданий нет.
3. **Рамка правок дополнена:** `tests/utils/test_Preferences.cpp`, `tests/utils/test_PreferencesPages.cpp`, `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp` и три файла пункта 7 контракта (`tests/ui_audit/ui_audit_part3a_scenes.py`, `tools/ui-audit/reference_shots.py`, `tools/ui-audit/tests/test_reference_shots.py`). В проверке 6 эти файлы тоже допустимы.
4. Если `tools/ui-audit/tests/test_reference_shots.py` запускается не CTest, а отдельно — запусти его той командой, которой его запускает `.github/workflows` (найди `git grep -n "test_reference_shots" -- .github`); нет такой команды — `python3 -m pytest tools/ui-audit/tests/test_reference_shots.py -q`; вывод — в сдачу.

Дальше — проверки 1–6 по заданию и `## DONE-P16`.
