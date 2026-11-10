# Доказательства: P5CR2, дорожка 1

Все чтения Git выполнялись с явными ревизиями. Для чтения и сверки использовались `BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566` и `PORT=832c953a94a632d57872349013f7ed1a37434715`.

## Наличие файлов в PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python - <<'PY'
import subprocess
rev='832c953a94a632d57872349013f7ed1a37434715'
files='src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h'.split()
for path in files:
 subprocess.run(['git','cat-file','-e',rev+':'+path],check=True)
 print(path+': файл присутствует в PORT')
PY
```

Вывод:

```text
src/drawers/CreditsDrawer.cpp: файл присутствует в PORT
src/drawers/CreditsDrawer.h: файл присутствует в PORT
src/drawers/cBuildingListDrawer.cpp: файл присутствует в PORT
src/drawers/cBuildingListDrawer.h: файл присутствует в PORT
src/drawers/cMessageDrawer.cpp: файл присутствует в PORT
src/drawers/cMessageDrawer.h: файл присутствует в PORT
src/drawers/cMiniMapDrawer.cpp: файл присутствует в PORT
src/drawers/cMiniMapDrawer.h: файл присутствует в PORT
src/drawers/cSideBarDrawer.cpp: файл присутствует в PORT
src/drawers/cSideBarDrawer.h: файл присутствует в PORT
```

## Построение таблицы и сверка

Таблица формируется скриптом `build_fork_hunks_1.py`. Он читает участки `git diff --unified=3 BASE FORK1 -- <путь>`, сопоставляет функции и диапазоны в `PORT` через `git show PORT:<путь>` и проверяет пересечения по участкам `git diff --unified=3 BASE PORT -- <путь>`. Строки словаря шагов проверяются на всех строках добавления, удаления и контекста каждого участка.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/build_fork_hunks_1.py
```

Вывод:

```text
Создана таблица: .tmp/p5cr2/fork-hunks-1.tsv (42 строк данных).
src/drawers/CreditsDrawer.cpp: таблица=4; @@=4; OK
src/drawers/CreditsDrawer.h: таблица=2; @@=2; OK
src/drawers/cBuildingListDrawer.cpp: таблица=17; @@=17; OK
src/drawers/cBuildingListDrawer.h: таблица=3; @@=3; OK
src/drawers/cMessageDrawer.cpp: таблица=3; @@=3; OK
src/drawers/cMessageDrawer.h: таблица=1; @@=1; OK
src/drawers/cMiniMapDrawer.cpp: таблица=6; @@=6; OK
src/drawers/cMiniMapDrawer.h: таблица=2; @@=2; OK
src/drawers/cSideBarDrawer.cpp: таблица=2; @@=2; OK
src/drawers/cSideBarDrawer.h: таблица=2; @@=2; OK
```

Отдельная команда сверки, которая пересчитывает строки таблицы по каждому файлу и число строк `@@` в соответствующем diff:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p5cr2/verify_fork_hunks_1.py
```

Её stdout:

```text
src/drawers/CreditsDrawer.cpp: строки таблицы=4; участки @@=4; OK
src/drawers/CreditsDrawer.h: строки таблицы=2; участки @@=2; OK
src/drawers/cBuildingListDrawer.cpp: строки таблицы=17; участки @@=17; OK
src/drawers/cBuildingListDrawer.h: строки таблицы=3; участки @@=3; OK
src/drawers/cMessageDrawer.cpp: строки таблицы=3; участки @@=3; OK
src/drawers/cMessageDrawer.h: строки таблицы=1; участки @@=1; OK
src/drawers/cMiniMapDrawer.cpp: строки таблицы=6; участки @@=6; OK
src/drawers/cMiniMapDrawer.h: строки таблицы=2; участки @@=2; OK
src/drawers/cSideBarDrawer.cpp: строки таблицы=2; участки @@=2; OK
src/drawers/cSideBarDrawer.h: строки таблицы=2; участки @@=2; OK
ИТОГО: 42 строк данных; число строк совпадает с числом @@ во всех 10 файлах.
```

В таблице находятся строки FORK1 по новой стороне заголовков `@@`; для участков без добавленных строк указана начальная строка и пометка «только удаление». Скрипты, таблица и этот отчёт находятся в `.tmp/p5cr2/`.

## Точность описания участка cBuildingListDrawer.cpp@9208dcf:354-360

Спот-проверка показала, что этот участок заменяет строку `Upgrading` локализованным вызовом с ключом `Upgrade` и русским текстом `Улучшение`. Описание соответствующей ячейки таблицы и запись в скрипте-генераторе уточнены; остальные ячейки таблицы не менялись.

Команда проверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp | rg -n -C 3 'localization::text\("Upgrade"'
```

Вывод:

```text
337- 
338-                     Color red = Color{255, 0, 0,255};
339--                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
340:+                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
341-                 }
342- 
343-                 // Pending building (ie: a build is progressing, blocking the upgrade)
```

Полный stdout исходной команды `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp` находится в разделе `src/drawers/cBuildingListDrawer.cpp: BASE → FORK1` файла `.tmp/p5cr2/track1-source-outputs.md`.
