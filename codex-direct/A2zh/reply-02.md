## DONE-A2zh | 2026-10-29 11:51:31 UTC | ветка codex/a2zh

ХОД: [x] Разведка и план; [x] Приёмочные тесты и красный прогон; [x] Код движка и генератор; [x] Ссылки draw и мутации; [x] Контракт и сверка подключения; [x] Итоговые проверки и сдача

Добавлен HD-кадр Осадного 176×176 для корпуса, тени и башни с центрированием относительно прежнего `visual`. Контракт пересоздан. Классическая геометрия и интерфейс сохранены.

База: `d5cd7407445bfd0f05349f8acecefe0532a70b1c`. Коммиты не создавались.

### Журнал хода

Содержимое [.tmp/progress.md](/srv/dune/worktrees/a2zh/.tmp/progress.md):

```text
1. План принят сообщением PLAN-OK-A2zh. Рабочая копия чистая, ветка codex/a2zh; постоянные файлы не изменены. Проверка: git status --short без вывода.
2. Приёмочные тесты подготовлены и заморожены: tests/UnitFrameLayoutTests.cpp, CMakeLists.txt, tools/units3d/tests/test_unit_contract.py, codex-direct/A2zh/ACCEPTANCE.sha256. Независимый расчёт: .tmp/u2_check.log — PASS. Красный прогон: .tmp/red.log — движок checks=312 failures=72, EXIT=1, FAIL только U1/U2/U10; Python Ran 134 tests in 1223.829s, FAILED (failures=12, errors=6), EXIT=1, пропусков нет; все падения соответствуют заданию. Обе строки нового манифеста: OK.
3. Помощники A и B параллельно реализовали поля и кадр движка, состояния и выбор кадра генератора: src/include/structs.h, src/utils/cIniGameRessouces.cpp, src/gameobjects/units/cUnit.cpp, src/utils/UnitFrameLayout.hpp, tools/units3d/unit_contract.py. Проверки: .tmp/a-engine.log — compile_status=0, checks=312 failures=0, test_status=0; .tmp/b-phase3.log — Ran 6 tests, OK, test_status=0. Дифф движка проверен: остальные функции не изменены.
4. Помощники B и C параллельно завершили ссылки draw и мутации: tools/units3d/unit_contract.py. Проверки: .tmp/b-phase4.log — Ran 6 tests, OK, frame_tests_status=0, draw_parse_status=0, CARRYALL=24; .tmp/mut/mutations.log — MU1:72 FAIL U1/U2/U10, MU2:3 FAIL U2 (0.3/1.1, 0.3/1.25, 1.3/1.25), MU3:48 FAIL U3/U4/U5, MU4:72 FAIL U1/U2/U10, MU5:16 FAIL U6 hd176x0, MU6:32 FAIL U10, все коды мутаций 1; настоящий заголовок status=0, checks=312 failures=0. Обязательные случаи проверены по логу и C++-копиям.
5. Пересозданы docs/units/unit_contract.json и docs/units/UNIT_CONTRACT.md: .tmp/generate.log — generate_status=0, entries=59, size_exceptions=7. Сверка: .tmp/contract-semantic.log — UNEXPECTED_CHANGES 0; .tmp/contract-diff.log — (а)+65/-25, (б)+18/-322, (в)+226/-108, (г)+1092/-1093, (д)+152/-153, итого +1553/-1701, unclassified=0. Шесть пунктов подключения draw проверены по новому cUnit.cpp. Проверки: .tmp/engine-test.log — checks=312 failures=0, engine_status=0; .tmp/contract-tests.log — Ran 15 tests in 2.647s, OK, contract_status=0.
6. Полный прогон и заключительная сверка завершены; постоянные файлы на этом шаге не менялись. .tmp/green.log — Ran 134 tests in 1223.201s, OK, GREEN_PYTHON_EXIT=0, пропусков и ошибок нет. .tmp/acceptance-checks.log — четыре строки OK, acceptance_status=0. .tmp/diff-check.log — diff_check_status=0. .tmp/scope-check.log — CHANGED_FILES 11, OUTSIDE_SCOPE [], MISSING_EXPECTED_FILES [], SCOPE_CHECK_PASS. Итоговый git status --short записан в .tmp/status.log; коммиты не создавались.
```

### Красный прогон до реализации

Полный вывод — [.tmp/red.log](/srv/dune/worktrees/a2zh/.tmp/red.log).

```text
UnitFrameLayout checks=312 failures=72
RED_ENGINE_EXIT=1
Ran 134 tests in 1223.829s
FAILED (failures=12, errors=6)
RED_PYTHON_EXIT=1
```

Падения соответствовали заданию. У движка `FAIL` были только в У1, У2 и У10; У3–У9 прошли. Примеры:

```text
FAIL U1 input classic=36x36 hd=176x176 pixelW=1408 density=4 column=0 row=0 visual={100,200,36,36} zoom=1 visualScale=1 got src={0,0,36,36} dest={100,200,36,36} expected src={0,0,44,44} dest={96,196,44,44}
FAIL U2 input classic=36x36 hd=176x176 pixelW=1408 density=4 column=3 row=0 visual={100,200,9,9} zoom=0.25 visualScale=1 got src={108,0,36,36} dest={100,200,9,9} expected src={132,0,44,44} dest={99,199,11,11}
FAIL U10 input classic=38x46 hd=160x192 pixelW=1280 density=4 column=0 row=0 visual={100,200,38,46} zoom=1 visualScale=1 got src={0,0,38,46} dest={100,200,38,46} expected src={0,0,40,48} dest={99,199,40,48}
```

### Зелёные проверки

Тест движка — [.tmp/engine-test.log](/srv/dune/worktrees/a2zh/.tmp/engine-test.log):

```text
UnitFrameLayout checks=312 failures=0
engine_status=0
```

Полный Python-прогон — [.tmp/green.log](/srv/dune/worktrees/a2zh/.tmp/green.log):

```text
Ran 134 tests in 1223.201s
OK
GREEN_PYTHON_EXIT=0
```

Пропусков нет. Оба манифеста — [.tmp/acceptance-checks.log](/srv/dune/worktrees/a2zh/.tmp/acceptance-checks.log):

```text
tools/units3d/check_unit.py: OK
tools/units3d/tests/test_check_unit.py: OK
tests/UnitFrameLayoutTests.cpp: OK
tools/units3d/tests/test_unit_contract.py: OK
acceptance_status=0
```

Независимый расчёт У2 и У10 — [.tmp/u2_check.log](/srv/dune/worktrees/a2zh/.tmp/u2_check.log): `U2/U10 independent check: PASS`.

### Мутации

Скрипт — [.tmp/mut/run.sh](/srv/dune/worktrees/a2zh/.tmp/mut/run.sh), вывод — [.tmp/mut/mutations.log](/srv/dune/worktrees/a2zh/.tmp/mut/mutations.log). Все мутации скомпилировались и завершились кодом `1`.

| Мутация | Строки FAIL | Покрасневшие случаи |
|---|---:|---|
| MU1 | 72 | У1, У2, У10 |
| MU2 | 3 | У2: 0,3/1,1; 0,3/1,25; 1,3/1,25 |
| MU3 | 48 | У3, У4, У5 |
| MU4 | 72 | У1, У2, У10 |
| MU5 | 16 | У6, вход 176×0 |
| MU6 | 32 | У10 |

Настоящий заголовок: `status=0`, `checks=312 failures=0`.

### Дифф контракта относительно ecffa2f5

Подсчёт — [.tmp/contract-diff.log](/srv/dune/worktrees/a2zh/.tmp/contract-diff.log), содержательная сверка — [.tmp/contract-semantic.log](/srv/dune/worktrees/a2zh/.tmp/contract-semantic.log).

| Пункт | Добавлено строк | Удалено строк |
|---|---:|---:|
| (а) Размеры пяти записей и HD-ссылки | 65 | 25 |
| (б) Изменения `size_exceptions` | 18 | 322 |
| (в) `draw_rules` и `draw_sites` | 226 | 108 |
| (г) Номера строк источников | 1092 | 1093 |
| (д) Замена ссылки передачи `iFrame` | 152 | 153 |
| Всего | 1553 | 1701 |

Неразобранных изменений нет. В пункте (б) учтены 90 строк сопоставления Git вокруг удаления двух HM-исключений; сохранность соответствующих источников Девастатора проверена.

Пять записей имеют кадр 176×176, атлас 1408×176, сетку 8×1 и нулевой остаток. Три исключения Осадного сохраняют только причину несовпадения с classic×4; два HM-исключения удалены. Других содержательных изменений нет.

### Подключение в draw()

1. Тень и корпус передают `bmp_body`, башня — `bmp_head`; все передают `iFrame`: [тень](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:798), [корпус](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:829), [башня](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:861).
2. Каждый вызов использует собственные `pixelW` и `density`: [shadow](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:803), [bitmap](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:834), [top](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:866).
3. `zoom` получен из камеры, `visualScale` вычислен с требуемыми аргументами: [cUnit.cpp:791](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:791).
4. `+24` применяется только в ветке тени керриола: [cUnit.cpp:808](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:808). `ShadowTrans` сохранён: [cUnit.cpp:823](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:823).
5. `SYMB_PICKMEUP` использует `visualX`, `visualY - 7`, а `FOCUS` — `visual`: [значок](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:889), [рамка](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:897).
6. Ранние выходы сохранены: [isHidden](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:761), [isSandworm](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:767). Сохранены проверки [shadow](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:797), [bitmap с логом](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:828), [top и iHitPoints](/srv/dune/worktrees/a2zh/src/gameobjects/units/cUnit.cpp:860), а также порядок тень → корпус → башня.

### Не проверено

На servak не компилировались `cUnit.cpp` и `cIniGameRessouces.cpp`, не выполнялись полная сборка, `ctest` и запуск игры: отсутствует SDL2. Эти проверки выполняет ведущий.

### git status --short

```text
 M CMakeLists.txt
 M docs/units/UNIT_CONTRACT.md
 M docs/units/unit_contract.json
 M src/gameobjects/units/cUnit.cpp
 M src/include/structs.h
 M src/utils/cIniGameRessouces.cpp
 M tools/units3d/tests/test_unit_contract.py
 M tools/units3d/unit_contract.py
?? codex-direct/A2zh/ACCEPTANCE.sha256
?? src/utils/UnitFrameLayout.hpp
?? tests/UnitFrameLayoutTests.cpp
```

Все 11 файлов входят в рамку правок; `.tmp/` в статусе отсутствует.

### Владельцу

1. Осадный получает увеличенную и центрированную HD-картинку при прежней геометрии интерфейса.
2. Паки, ресурсы и другие функции движка не менялись.
3. От ведущего нужны полная сборка с SDL2, `ctest` и проверка изображения в игре.