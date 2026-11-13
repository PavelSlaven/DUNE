## DONE-P7V | Thu Nov 12 11:11:43 UTC 2026 | HEAD c106b54a21af3577ce98c38330455be8c0b15d89

Русские тексты кампаний и названия карт подключены. Перенос страниц ментата и операции с UTF-8 реализованы. Все проверки 1–7 прошли по условиям задания. Коммитов нет.

**Чтение**

Полностью прочитаны все файлы раздела «Прочитать до работы» и оба требуемых вывода команд. Дополнительно прочитаны `/srv/dune/tasks/p7v/task.md` как источник брифов и `/srv/dune/tasks/codex-watch.py` для проверки доступного инструмента учёта. Недостающих норм не обнаружено.

**Журнал хода**

[.tmp/p7v/progress.md](/srv/dune/worktrees/u34/.tmp/p7v/progress.md):

```text
1. Шаг 1 завершён: добавлены T7–T9 и случаи T10, тесты подключены в CMake, из T6 удалены 64 исключения; очистка вывела removed=64 remaining=41. Решено исполнителем: проверка текстовых строк переиспользует isTextLine, набор campaign_ru сравнивается по всем обычным файлам, textValue снимает пробелы и кавычки с обоих краёв → tests/utils/test_CampaignTextRu.cpp:61,82,67; было: дублированный regex, только .ini, внешняя пара кавычек → общие помощники, все файлы и повторное удаление краевых символов; основание: тестовый контракт T9. Ожидаемое время: помощник A — 15 минут.
2. Шаг 2 завершён: красный T6 на имеющейся сборке вернул exit=1; лог содержит untranslated text 'replacing you.' (строки 25–26) и 'Ancient Delta' (строки 85, 90), итог: translation: 172 scenes, 110 failures. Ожидаемое время: помощник A — 15 минут.
3. Шаг 3 завершён: скопированы 36 файлов campaign_ru, в 37 файлах карт вставлен TitleRu, сборка копирует resources/bin/campaign_ru; diff -r — пусто, exit=0; add_titles.py — Проверка Title: файлов 37, совпадений 37, вставлено TitleRu: 37, exit=0. Ожидание: помощник B — 10 минут.
4. Шаг 4 завершён: русская игра выбирает campaign_ru, страницы ментата переносятся по ширине и таймер считает буквы UTF-8, названия карт показывают TitleRu с обрезкой по буквам; git diff --check по файлам шага 4 — пусто, exit=0; сборка ещё не запускалась. Решений исполнителя у C нет. Ожидание: помощник C — 15 минут.
5. Шаг 5 завершён: проверка 1 — df Available 6809, сборка exit=0, CTest 100% из 345; 2 — предупреждений по changed-paths нет (пустой grep, exit=1); 3 — Imminent crash отсутствует (пустой grep, exit=1); 4 — все 15 скриптов UI-аудита exit=0; 5 — unittest exit=0, OK, 199 tests, новых __pycache__ нет; 6 — diff -r exit=0, 37 карт по 1/0, T6: 64 удалено/0 добавлено; 7 — status содержит только ожидаемые пути шагов 1, 3, 4. Ожидаемое время: помощник A — 60 минут. Решено исполнителем: расположение инструмента учёта → использован /srv/dune/tasks/codex-watch.py; .tmp/p7v/progress.md:5, было: tools/codex-watch.py без доступного файла → найденный скрипт; основание: поиск rg и вывод --help
```

**Красный T6**

`exit=1`. Последние 30 строк [.tmp/p7v/red-t6.log](/srv/dune/worktrees/u34/.tmp/p7v/red-t6.log):

```text
ru region-sardaukar-select-7: untranslated text 'The Sardaukar crushed most of the Ordos.'
ru region-sardaukar-select-8: untranslated text 'The Sardaukar devastated the Atreides.'
ru region-sardaukar-select-9: untranslated text 'Only House Sardaukar will prevail.'
ru skirmish-setup-random: untranslated text 'Ancient Delta'
ru skirmish-setup-random: untranslated text 'Broken Mountains'
ru skirmish-setup-random: untranslated text 'Division'
ru skirmish-setup-random: untranslated text 'Golek Crossing'
ru skirmish-setup-random: untranslated text 'Sietch Stefan'
ru skirmish-setup-ready-map: untranslated text 'Ancient Delta'
ru skirmish-setup-ready-map: untranslated text 'Broken Mountains'
ru skirmish-setup-ready-map: untranslated text 'Division'
ru skirmish-setup-ready-map: untranslated text 'Golek Crossing'
ru skirmish-setup-ready-map: untranslated text 'Sietch Stefan'
ru tellhouse-atreides-speak: untranslated text 'In recent centuries industrial and technological development has added'
ru tellhouse-atreides-speak: untranslated text 'In recent centuries industrial and technological development has added'
ru tellhouse-atreides-speak: untranslated text 'to the prosperity of the Caladanian peoples.'
ru tellhouse-atreides-speak: untranslated text 'to the prosperity of the Caladanian peoples.'
ru tellhouse-harkonnen-speak: untranslated text 'A cruel people, the Harkonnen are ruthless towards both friend and foe in'
ru tellhouse-harkonnen-speak: untranslated text 'A cruel people, the Harkonnen are ruthless towards both friend and foe in'
ru tellhouse-harkonnen-speak: untranslated text 'their fanatical persuit of power.'
ru tellhouse-harkonnen-speak: untranslated text 'their fanatical persuit of power.'
ru tellhouse-ordos-speak: untranslated text 'Acting as traders and brokers, the Ordos produce no physical products but'
ru tellhouse-ordos-speak: untranslated text 'Acting as traders and brokers, the Ordos produce no physical products but'
ru tellhouse-ordos-speak: untranslated text 'instead rely upon their mercantile skills to make their profits.'
ru tellhouse-ordos-speak: untranslated text 'instead rely upon their mercantile skills to make their profits.'
ru tellhouse-sardaukar-speak: untranslated text 'Kaitain is the second capital of the Corrino Empire'
ru tellhouse-sardaukar-speak: untranslated text 'Kaitain is the second capital of the Corrino Empire'
ru tellhouse-sardaukar-speak: untranslated text 'The seat of the empire was moved from Salusa Secundus, which became'
ru tellhouse-sardaukar-speak: untranslated text 'The seat of the empire was moved from Salusa Secundus, which became'
translation: 172 scenes, 110 failures
```

Вне хвоста присутствуют обе требуемые строки:

```text
25:ru mentat-lose-sardaukar-speak: untranslated text 'replacing you.'
85:ru skirmish-setup-random: untranslated text 'Ancient Delta'
```

**Проверки 1–7**

1. Место и сборка. Лог: [build.log](/srv/dune/worktrees/u34/.tmp/p7v/build.log), каталог сборочных логов — `.tmp/out/logs/20261112T104225-4/`.

   ```text
   df -m /srv: Available=6809; exit=0
   Сборка с CCACHE_DISABLE=1: exit=0
   100% tests passed, 0 tests failed out of 345
   Total Test time (real) = 12.70 sec
   ```

2. Предупреждения изменённых файлов:

   ```text
   grep: пустой вывод
   exit=1
   ```

   Код `1` означает отсутствие совпадений.

3. Проверка `Imminent crash` в `game-dummy.log` и `stdout-dummy.log`:

   ```text
   grep: пустой вывод
   exit=1
   ```

4. Скрипты интерфейса:

   ```text
   ui_audit_list_and_scales.py exit=0
   ui_audit_unknown_scene.py exit=0
   ui_audit_main_menu_png.py exit=0
   ui_audit_tools_run_combo.py exit=0
   ui_audit_part2_catalog.py exit=0
   ui_audit_part2_scenes.py exit=0
   ui_audit_part3a_catalog.py exit=0
   ui_audit_part3a_scenes.py exit=0
   ui_audit_part3b_catalog.py exit=0
   ui_audit_part3b_scenes.py exit=0
   ui_audit_frames.py exit=0
   ui_audit_part3c_catalog.py exit=0
   ui_audit_part3c_scenes.py exit=0
   ui_audit_language.py exit=0
   ui_audit_translation.py exit=0
   translation: 172 scenes, 0 failures
   ```

   Логи сохранены в `.tmp/p7v/run-<скрипт>.log`. Команды не прерывались.

5. Тесты инструмента, [run-j.log](/srv/dune/worktrees/u34/.tmp/p7v/run-j.log):

   ```text
   exit=0
   Ran 199 tests in 0.470s

   OK
   ```

   Новых папок `__pycache__` после проверок нет.

6. Данные:

   ```text
   diff -r campaign_ru: пустой вывод; exit=0
   git diff --numstat -- resources/bin/skirmish: 37 строк, каждая 1/0; exit=0
   Удалённые строки исключений T6: 64; grep exit=0
   Добавленные строки исключений T6: 0; grep exit=1
   ```

7. Рамка изменений соблюдена:

   ```text
   git status --short: exit=0
   Изменены только пути шагов 1, 3 и 4.
   Новые пути соответствуют разрешённому списку.
   ```

**`git diff --stat`**

Вывод не включает новые, ещё не отслеживаемые файлы.

```text
 resources/bin/skirmish/2PL_AncientDelta.ini        |  1 +
 resources/bin/skirmish/2PL_BottleNeck2022.ini      |  1 +
 resources/bin/skirmish/2PL_BrokenMountains2022.ini |  1 +
 resources/bin/skirmish/2PL_CliffsRene2022.ini      |  1 +
 resources/bin/skirmish/2PL_DavidsPass2022.ini      |  1 +
 resources/bin/skirmish/2PL_Division.ini            |  1 +
 resources/bin/skirmish/2PL_DriftingPlains.ini      |  1 +
 resources/bin/skirmish/2PL_Duality2022.ini         |  1 +
 resources/bin/skirmish/2PL_Durancut.ini            |  1 +
 resources/bin/skirmish/2PL_Edge2Edge.ini           |  1 +
 resources/bin/skirmish/2PL_KigYar.ini              |  1 +
 resources/bin/skirmish/2PL_KynesValley.ini         |  1 +
 resources/bin/skirmish/2PL_MRelCanyon.ini          |  1 +
 resources/bin/skirmish/2PL_MarlandCove.ini         |  1 +
 resources/bin/skirmish/2PL_MarthasRock.ini         |  1 +
 resources/bin/skirmish/2PL_Mayberry.ini            |  1 +
 resources/bin/skirmish/2PL_OgelleBasin.ini         |  1 +
 resources/bin/skirmish/2PL_Rabban.ini              |  1 +
 resources/bin/skirmish/2PL_SIlverstoneChannel.ini  |  1 +
 resources/bin/skirmish/2PL_Sanctuarys2022.ini      |  1 +
 resources/bin/skirmish/2PL_TwinFists2022.ini       |  1 +
 resources/bin/skirmish/2PL_TwoStacks.ini           |  1 +
 resources/bin/skirmish/3PL_FocalPoint.ini          |  1 +
 resources/bin/skirmish/3PL_Gankyil.ini             |  1 +
 resources/bin/skirmish/3PL_GuillermoGorge.ini      |  1 +
 resources/bin/skirmish/3PL_Middle_Man.ini          |  1 +
 resources/bin/skirmish/3PL_Uvavu.ini               |  1 +
 resources/bin/skirmish/4PL_FelisCathedra.ini       |  1 +
 resources/bin/skirmish/4PL_GolekCrossing.ini       |  1 +
 resources/bin/skirmish/4PL_GuillermoGorge.ini      |  1 +
 resources/bin/skirmish/4PL_HuelsbeckRing.ini       |  1 +
 resources/bin/skirmish/4PL_Isis_Fields.ini         |  1 +
 resources/bin/skirmish/4PL_Neighbours.ini          |  1 +
 resources/bin/skirmish/4PL_SietchStefan2022.ini    |  1 +
 .../bin/skirmish/4PL_Sin\303\251adPlains.ini"      |  1 +
 resources/bin/skirmish/4PL_Warm Place.ini          |  1 +
 resources/bin/skirmish/4PL_WormsHole.ini           |  1 +
 src/CMakeLists.txt                                 |  1 +
 src/drawers/cBuildingListDrawer.cpp                | 14 +----
 src/gameobjects/map/PreviewMap.hpp                 |  8 +++
 src/gameobjects/map/cPreviewMaps.cpp               |  3 +
 src/gameobjects/mentat/AbstractMentat.cpp          | 16 ++++--
 src/gamestates/cSetupSkirmishState.cpp             | 11 ++--
 src/utils/IniParsing.cpp                           |  6 ++
 src/utils/IniParsing.hpp                           |  1 +
 src/utils/ini.cpp                                  |  4 +-
 tests/CMakeLists.txt                               |  4 ++
 tests/map/test_cPreviewMapsSave.cpp                | 67 ++++++++++++++++++++++
 tests/ui_audit/data/latin-ru-allowed.tsv           | 64 ---------------------
 tools/upstream/build_upstream_linux.sh             |  2 +-
 50 files changed, 147 insertions(+), 91 deletions(-)
```

**Список для коммитов**

1. Тесты — `tests/utils/test_Utf8.cpp`, `tests/utils/test_MentatTextLayout.cpp`, `tests/utils/test_CampaignTextRu.cpp`, `tests/map/test_cPreviewMapsSave.cpp`, `tests/CMakeLists.txt`, `tests/ui_audit/data/latin-ru-allowed.tsv`.

   ```text
   Test Russian campaign text, mentat layout and skirmish titles

   Behavior changes: translation audit no longer exempts campaign text or skirmish titles.
   ```

2. Данные — `resources/bin/campaign_ru/`, все изменённые `resources/bin/skirmish/*.ini`, `tools/upstream/build_upstream_linux.sh`.

   ```text
   Add Russian campaign resources and skirmish titles

   Behavior changes: Russian campaign resources and map titles are available in Linux run resources.
   ```

3. Код — `src/utils/IniParsing.hpp`, `src/utils/IniParsing.cpp`, `src/utils/ini.cpp`, `src/utils/Utf8.hpp`, `src/gameobjects/mentat/MentatTextLayout.hpp`, `src/gameobjects/mentat/MentatTextLayout.cpp`, `src/CMakeLists.txt`, `src/gameobjects/mentat/AbstractMentat.cpp`, `src/drawers/cBuildingListDrawer.cpp`, `src/gameobjects/map/PreviewMap.hpp`, `src/gameobjects/map/cPreviewMaps.cpp`, `src/gamestates/cSetupSkirmishState.cpp`.

   ```text
   Display localized campaign text and skirmish titles

   Behavior changes: Russian games read campaign_ru and TitleRu with an English title fallback; mentat pages wrap to two lines; speech timing and title truncation use UTF-8 code points; English text remains unchanged.
   ```

**Решено исполнителем**

- Решено исполнителем: проверка текстовых строк переиспользует `isTextLine`, набор `campaign_ru` сравнивается по всем обычным файлам, `textValue` снимает пробелы и кавычки с обоих краёв → `tests/utils/test_CampaignTextRu.cpp:61,82,67`; было: дублированный regex, только `.ini`, внешняя пара кавычек → общие помощники, все файлы и повторное удаление краевых символов; основание: тестовый контракт T9.
- Решено исполнителем: расположение инструмента учёта → использован `/srv/dune/tasks/codex-watch.py`; `.tmp/p7v/progress.md:5`, было: `tools/codex-watch.py` без доступного файла → найденный скрипт; основание: поиск `rg` и вывод `--help`.

**Учёт вызовов и не проверено**

Фактический вывод `codex-watch.py`:

```text
window 10:09-11:09 UTC

worktree: 57 changed paths; touched in window: 90
  resources/bin/skirmish/2PL_AncientDelta.ini
  resources/bin/skirmish/2PL_BottleNeck2022.ini
  resources/bin/skirmish/2PL_BrokenMountains2022.ini
  resources/bin/skirmish/2PL_CliffsRene2022.ini
  resources/bin/skirmish/2PL_DavidsPass2022.ini
  resources/bin/skirmish/2PL_Division.ini
  resources/bin/skirmish/2PL_DriftingPlains.ini
  resources/bin/skirmish/2PL_Duality2022.ini
```

Числа вызовов корневой нити и помощников не проверены: скрипт не вывел метрик нити и помощников по доступным транскриптам. CI будущих коммитов не запускался, поскольку коммиты по заданию создаёт ведущий. Все обязательные проверки 1–7 выполнены.

Находок вне задачи не зафиксировано.

**Рабочие места**

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p7v --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u34/.tmp/p7v	dir	-	-	168384	-	-	-	-	0	0
```

```text
192K	.tmp/p7v
```

`.tmp/p7v` — оставить — логи проверок нужны ревью; также содержит журнал, скрипт вставки названий и список проверяемых путей. Других рабочих мест задача не создавала. `previous-run` не удалён.

**Полный Git status**

```text
 M resources/bin/skirmish/2PL_AncientDelta.ini
 M resources/bin/skirmish/2PL_BottleNeck2022.ini
 M resources/bin/skirmish/2PL_BrokenMountains2022.ini
 M resources/bin/skirmish/2PL_CliffsRene2022.ini
 M resources/bin/skirmish/2PL_DavidsPass2022.ini
 M resources/bin/skirmish/2PL_Division.ini
 M resources/bin/skirmish/2PL_DriftingPlains.ini
 M resources/bin/skirmish/2PL_Duality2022.ini
 M resources/bin/skirmish/2PL_Durancut.ini
 M resources/bin/skirmish/2PL_Edge2Edge.ini
 M resources/bin/skirmish/2PL_KigYar.ini
 M resources/bin/skirmish/2PL_KynesValley.ini
 M resources/bin/skirmish/2PL_MRelCanyon.ini
 M resources/bin/skirmish/2PL_MarlandCove.ini
 M resources/bin/skirmish/2PL_MarthasRock.ini
 M resources/bin/skirmish/2PL_Mayberry.ini
 M resources/bin/skirmish/2PL_OgelleBasin.ini
 M resources/bin/skirmish/2PL_Rabban.ini
 M resources/bin/skirmish/2PL_SIlverstoneChannel.ini
 M resources/bin/skirmish/2PL_Sanctuarys2022.ini
 M resources/bin/skirmish/2PL_TwinFists2022.ini
 M resources/bin/skirmish/2PL_TwoStacks.ini
 M resources/bin/skirmish/3PL_FocalPoint.ini
 M resources/bin/skirmish/3PL_Gankyil.ini
 M resources/bin/skirmish/3PL_GuillermoGorge.ini
 M resources/bin/skirmish/3PL_Middle_Man.ini
 M resources/bin/skirmish/3PL_Uvavu.ini
 M resources/bin/skirmish/4PL_FelisCathedra.ini
 M resources/bin/skirmish/4PL_GolekCrossing.ini
 M resources/bin/skirmish/4PL_GuillermoGorge.ini
 M resources/bin/skirmish/4PL_HuelsbeckRing.ini
 M resources/bin/skirmish/4PL_Isis_Fields.ini
 M resources/bin/skirmish/4PL_Neighbours.ini
 M resources/bin/skirmish/4PL_SietchStefan2022.ini
 M "resources/bin/skirmish/4PL_Sin\303\251adPlains.ini"
 M "resources/bin/skirmish/4PL_Warm Place.ini"
 M resources/bin/skirmish/4PL_WormsHole.ini
 M src/CMakeLists.txt
 M src/drawers/cBuildingListDrawer.cpp
 M src/gameobjects/map/PreviewMap.hpp
 M src/gameobjects/map/cPreviewMaps.cpp
 M src/gameobjects/mentat/AbstractMentat.cpp
 M src/gamestates/cSetupSkirmishState.cpp
 M src/utils/IniParsing.cpp
 M src/utils/IniParsing.hpp
 M src/utils/ini.cpp
 M tests/CMakeLists.txt
 M tests/map/test_cPreviewMapsSave.cpp
 M tests/ui_audit/data/latin-ru-allowed.tsv
 M tools/upstream/build_upstream_linux.sh
?? resources/bin/campaign_ru/
?? src/gameobjects/mentat/MentatTextLayout.cpp
?? src/gameobjects/mentat/MentatTextLayout.hpp
?? src/utils/Utf8.hpp
?? tests/utils/test_CampaignTextRu.cpp
?? tests/utils/test_MentatTextLayout.cpp
?? tests/utils/test_Utf8.cpp
```

**Для владельца**

- Кампании и названия карт показываются по-русски; длинные страницы ментата помещаются в две строки.
- Коммиты не созданы по заданию.
- От ведущего нужны приёмка изменений и создание коммитов по приведённому списку.