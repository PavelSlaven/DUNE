# TESTS-OK-U9-T1

Сдача `## DONE-U9-T1 | 2026-11-02 09:32:00 UTC` по возврату `REVIEW-U9-T1-01` (`codex-direct/U9/REVIEW-tests-01.md`) принята ведущим. Приёмочные тесты кадра Осадного заморожены суммами ниже.

## Что проверено скриптами ведущего

- Пункты 1–7 возврата — по diff рабочей копии: определение `D2TM_CLANG=1` у библиотеки движка при `APPLE` и Clang; `SDL_MAIN_HANDLED` в проверке `renderStrechSpriteF` и `FATAL_ERROR`, когда заголовок содержит имя метода, а проверка ложна; `unit_sprite_layout_tests` линкуется с `d2tm_unit_frame_engine`; четыре пиксельные проверки выполняются при любом исходе проверки рамки и печатают свой результат; ожидание смещения `r0k1` = `[-458, -441]`, расчёт исполнителя совпал с аудитом; у каждой цели своя папка фикстур; `git diff --check e4e703d7` пуст.
- Суммы 16 файлов по рабочей копии совпали со сдачей; `sha256sum -c tools/units3d/tests/ACCEPTANCE.sha256` — все строки `OK` после обновления строки `test_siege_frame.py` ведущим.
- Python-прогон на коде `main`: `Ran 235 tests`, `FAILED (failures=12)` — те же числа, что в сдаче `reply-02.txt`.
- Пиксельный тест на коде `main`: рамка и проверки «метки краёв» и «цвет Дома» — `FAIL`, «метка соседа» и «утечка» — `PASS` при обоих масштабах. Это ожидаемо: код `main` рисует старый кадр.

## Отклонение, принятое ведущим

Проба с заглушками выполнена в `/srv/dune/worktrees/u9f/.tmp/probe-03`, а не в `/srv/dune/tasks/u9-t1/probe-03`: среда исполнителя разрешает запись только в рабочей копии и `/tmp`. Проба удалена. Строки пробы: проверка `D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER` — `Success`; сборка всех целей — код `0`; CTest — 25 тестов запущены, `Not Run` нет, 3 красных на заглушках; без объявления метода — `FATAL_ERROR` с именем проверки и путём заголовка.

## Ветка

`codex/u9-frame`, коммит `cf757ad72f04515c8d91bf384cd0af11001574a6` поверх `1ea03e0d`, переслан на GitHub.

## Суммы замороженных файлов

```text
b357a4bae1946bd14c5206eb4f717121632f23b4fc33e04e5d147e090c96937f  tests/UnitDrawRecorder.cpp
b16c95131ee89ead0b9d43ab41b786e9de0a991b9d7269219f9d5be2a994f4e9  tests/UnitDrawRecorder.hpp
ca7b23cb3da2d56452718b3a68f45e38d0d1167b617333dc8aefd5de88926feb  tests/UnitDrawRegressionTests.cpp
da4386944a8d41eaef3251b5d6e380f2d96bac4a565168db900d687e7bcb206e  tests/UnitFrameBaseline.hpp
aef3e5f973f4020ddb853a3387cf31a07b3b7337b31262781deb4c97ae3e409b  tests/UnitFrameFixture.cpp
f820bddf17144a4cf1a1d644a85551ac8a09bc1a6e7bbde104ef816c7b95001e  tests/UnitFrameFixture.hpp
59505fda3676e71edf178c8759db9fa244733d7a9c521d9ecd03a01f364e312b  tests/UnitFrameInteractionsTests.cpp
e9572796c1477684634966c4511950c6b9c9e68628728ce914d8505870cf940f  tests/UnitHdFrameDrawTests.cpp
ccd23ff046f8896baedeaf0d16c700888fd226e03230782fc5ab428b2d13a842  tests/UnitRenderFixture.cmake
49beba10a3cf822523c51795b5fa7a166674246251a83096cb92e4aedc98c2ee  tests/UnitRenderPixelsTests.cpp
e674e9d7380ab2329e1ac67f6713e5ba49f9a7716dc0cf05c068e60da1e29397  tests/UnitSpriteLayoutTests.cpp
74f560b244d8b27f445c4c55e0cb46fe39bfa916f9ccffdb2f663a5dceaf0e2d  tests/UnitTextRecorder.cpp
1688a7595afcaf9b8db11cc5d05956ddeda1b4db5d81a788a3301b59474a1d11  tools/units3d/tests/test_siege_frame.py
90442565812fc0a6bf2686e028f994908a1b47398d6e3be50d8f1530b06adbb3  tools/units3d/tests/test_install_geometry.py
c7f707e2fdad8b5833681c1f3bda896c03167fcfadd2920b22ef5a7aa5867115  tools/units3d/tests/test_siege_contract.py
a740cb1c6770353442c204c8784f120f5f8e891fd921ad12be71802543c01e86  tools/units3d/tests/test_unit_contract.py
```

## Дальше

Реализация кадра Осадного — новым заданием Codex `gpt-6.1-sol` по `codex-direct/U9/TASK-frame.md`, `PLAN-frame`, `PLAN-OK-frame` и договору поправки 6 `PLAN-OK-tests`, на этой ветке. Файлы выше исполнитель реализации не меняет; правка теста — блок `Q`. При PR в `main` — влить `main` в ветку; в `.github/workflows/build_pr.yml` оставить `-j 4` и шаг Test.
