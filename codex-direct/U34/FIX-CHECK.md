## FIX-CHECK-U34 | 2026-11-04 23:53:29 UTC | HEAD d50c9bd46f5299b80ca0040dba86aa7ee489b319

**1. Состав — чисто.** Изменены только `tools/building_angle/angle.py` и `tools/building_angle/tests/test_angle.py`.

```text
2 files changed, 21 insertions(+), 3 deletions(-)
allowlist_exact= True changed_files= 2
```

**2. F6 — чисто.** На прежних входах с прозрачной рамкой шириной один и два пикселя и рамкой с альфой 127 каждый запуск дал:

```text
edge-to-edge: FAIL
EXIT_CODE 1
```

Прежний пример `root_soft_separable_output.png` также отклонён. Дополнительный поиск проверил отсутствие непрозрачных пикселей по каждому из четырёх краёв:

```text
missing_edge_search cases= 48 false_passes= 0
```

Контрпример не найден. Условие `touch` в [angle.py:148](/srv/dune/worktrees/u34/tools/building_angle/angle.py:148) непосредственно требует альфу больше 127 на каждом краю.

Извлечённые из пака HEAD `BUILD_RADAR` — все восемь кадров — и `BUILD_WINDTRAP` — один кадр — получили:

```text
edge-to-edge: pass
EXIT_CODE 0
```

[Лог проверки F6 и пака](/srv/dune/worktrees/u34/.tmp/fix-check-u34/item2.log).

**3. F5 — чисто по заданному сценарию.** Прозрачный непурпурный фон исключён; результат попиксельно совпал с растяжкой непрозрачной области исходника:

```text
fit_alpha input_bbox= (40, 40, 216, 216) output_bbox= (0, 0, 256, 256) output_corner= (90, 90, 90, 255) crop_reference_differing_pixels= 0
```

Вход W1a найден по `log-G1.tsv`; SHA-256 локальной копии совпал с журналом. Вход имеет режим RGB. Результат HEAD сравнен с `.tmp/u34-fit/BUILD_WINDTRAP_W1_a.png`:

```text
W1a differing_pixels= 0
```

[Лог проверки F5](/srv/dune/worktrees/u34/.tmp/fix-check-u34/item3.log).

**4. Тесты — чисто.** Полный прогон с `D2TM_PACK_DIR=$PWD/resources/bin/data`:

```text
test_current_outpost_leaves_margins ... skipped 'pack already holds an edge-to-edge Outpost'
Ran 14 tests in 0.845s
OK (skipped=1)
EXIT_CODE 0
```

Оба новых метода с извлечённым `angle.py` из `ee5e7211` выявили старые ошибки:

```text
test_transparent_rim_fails ... FAIL
test_transparent_background_stays_transparent ... FAIL
Ran 2 tests in 0.020s
FAILED (failures=2)
EXIT_CODE 1
```

Подмена модуля проверена через `angle.__file__`; извлечённый файл совпадает с Git-блобом. Логи: [HEAD](/srv/dune/worktrees/u34/.tmp/fix-check-u34/tests-head.log), [старый код](/srv/dune/worktrees/u34/.tmp/fix-check-u34/tests-old.log).

**5. Коммит — одна находка в формулировке.** Сообщение английское; абзац `Behavior changes:` расположен перед `Co-Authored-By`. Утверждения о неизменности пака и прохождении пилотных зданий подтверждены.

**FC1.** [Сообщение коммита, строка 1](/srv/dune/worktrees/u34/.tmp/fix-check-u34/item5-message.log:1): формулировка `keep source alpha in fit` шире фактического поведения. Исходная альфа учитывается при выборе области, но [angle.py:88](/srv/dune/worktrees/u34/tools/building_angle/angle.py:88) заменяет её бинарной маской 0/255. Контрольный вход с альфой здания 128 подтвердил потерю исходного значения:

```text
alpha_preservation input_alpha= 128 output_alpha_extrema= (255, 255)
```

Пример сохранён как [alpha128_input.png](/srv/dune/worktrees/u34/.tmp/fix-check-u34/alpha128_input.png). Точная формулировка заголовка должна говорить об учёте прозрачности при выделении здания.

### Итог

**Одна находка: FC1. Слияние не блокирует:** неточность касается заголовка сообщения; обязательные сценарии исправлений F5 и F6 проходят.

Код и данные ветки не изменены, коммитов нет. Финальный `git status --short` с отключённым фильтром LFS пуст. Все материалы проверки находятся в `.tmp/fix-check-u34/`.