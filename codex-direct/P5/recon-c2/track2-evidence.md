# Дорожка 2, пункт 1 задания P5CR2

Таблица находится в `fork-hunks-2.tsv`. Скрипт `assemble.py` собрал участки командами `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- <путь>`, определил шаг по строкам hunk и проверил места в `PORT`. Исходные diff-фрагменты, выгруженные через `git show`, вспомогательные скрипты и результаты работы сохранены только в `.tmp/p5cr2/`.

Для трёх файлов с фильтром применялись буквальные подстроки `HudLayout`, `sidebarWidth`, `TopBarHeight`, `battlefield`, `Battlefield` к добавленным, удалённым и контекстным строкам hunk. В `src/cGame_logic.cpp`, `src/controls/cGameControlsContext.cpp` и `src/controls/cMouse.cpp` совпадений нет; поэтому в таблице по ним 0 строк.

Для файлов камеры, отсутствующих по исходному пути в `PORT`, выполнены `git grep -n -F '<Класс>::<функция>(' 832c953a94a632d57872349013f7ed1a37434715 -- src`; полные команды и вывод лежат в `git-grep-port.txt`. Методы камеры нашлись в перемещённом `src/gameobjects/map/cMapCamera.cpp`; отсутствующие совпадения отмечены в таблице. Пересечения рассчитаны по новым сторонам hunks вывода `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- <путь в PORT>`.

## Проверка количества строк

Команда:

```text
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/verify_counts.py
```

Вывод:

```text
src/managers/cDrawManager.cpp	TSV=10	diff=10	OK
src/managers/cDrawManager.h	TSV=6	diff=6	OK
src/map/cMapCamera.cpp	TSV=8	diff=8	OK
src/map/cMapCamera.h	TSV=5	diff=5	OK
src/sidebar/cBuildingList.cpp	TSV=2	diff=2	OK
src/sidebar/cBuildingList.h	TSV=1	diff=1	OK
src/sidebar/cBuildingListFactory.cpp	TSV=3	diff=3	OK
src/sidebar/cBuildingListItem.cpp	TSV=3	diff=3	OK
src/sidebar/cBuildingListItem.h	TSV=2	diff=2	OK
src/sidebar/cBuildingListUpdater.cpp	TSV=2	diff=2	OK
src/sidebar/cSideBar.cpp	TSV=3	diff=3	OK
src/sidebar/cSideBar.h	TSV=2	diff=2	OK
src/cGame_logic.cpp	TSV=0	diff=0	OK
src/controls/cGameControlsContext.cpp	TSV=0	diff=0	OK
src/controls/cMouse.cpp	TSV=0	diff=0	OK
Всего строк данных TSV: 47
Итог: OK
```

Полный stdout также сохранён в `verify-output.txt`. Сборки, CTest и запуск игры не выполнялись.

## Дополнительная проверка hunk `cDrawManager.cpp@9208dcf:77-82`

Команда:

```text
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/managers/cDrawManager.cpp
```

В её stdout есть hunk:

```diff
@@ -76,8 +77,6 @@ void cDrawManager::drawCombatState()
     // GUI
     drawSidebar();
 
-    drawOptionBar();
-
     renderDrawer->setClippingFor(0, cSideBar::TopBarHeight, mapCamera->getWindowWidth(), mapCamera->getWindowHeight() + cSideBar::TopBarHeight);
     drawStructurePlacing();
     renderDrawer->resetClippingFor();
```

Удаление `drawOptionBar()` подтверждает описание в таблице. Диапазон `77-82` относится к новой стороне hunk; удалённая строка поэтому показана со знаком `-` в выводе diff. Ячейку TSV не менял. Полный stdout команды находится в `track2-source-outputs.txt` и `source-outputs/fork__src__managers__cDrawManager.cpp.diff`.

Полные stdout 15 команд `git diff BASE FORK1`, результаты фильтра по трём файлам и 17 команд `git diff BASE PORT` сохранены в `track2-source-outputs.txt`; отдельные raw diff находятся в `source-outputs/`. Результаты поиска перенесённых методов камеры сохранены в `git-grep-port.txt`.
