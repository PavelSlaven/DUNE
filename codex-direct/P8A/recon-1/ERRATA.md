# Поправка ведущего к первой разведке П8а

Выборочная сверка Haiku (`SPOTCHECK.md`) — 13 из 15. Оба несовпадения ведущий проверил командами `git show <ревизия>:<путь> | nl -ba | sed -n '<строки>p'`: строки таблиц указывают начало блока, утверждения верны для соседних строк.

- `placement.tsv`, строка 3: `src/player/cPlayer.cpp@9208dcf:1516` — начало выбора `isHumanPlayer`; вызов `canPlaceBuildingListItemAt` для человека — строка 1518, прежний `canPlaceStructureAt` для AI — строка 1519. Читать как `cPlayer.cpp@9208dcf:1516-1519`.
- `port-placement.tsv`, строка 47: `src/drawers/cPlaceItDrawer.cpp@d06f2fc:128` — начало участка diff `BASE..UP1`. Вызов `drawStructureIdAtMousePos(itemToPlace, mouseCell)` — `cPlaceItDrawer.cpp@d06f2fc:66`; `mouse_draw_x(mouseCell)` и `mouse_draw_y(mouseCell)` — строки 131–132.

Строки `port-placement.tsv` с пометкой `hunk` во втором столбце читать как начало участка diff.
