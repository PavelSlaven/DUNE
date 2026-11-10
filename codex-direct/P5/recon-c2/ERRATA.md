# Поправка ведущего ко второй разведке П5в

Выборочная сверка Haiku (`SPOTCHECK.md`) — 14 из 15. Сверка помощника 4 исполнителя (`spotcheck-executor.md`) — 10 из 12; оба несовпадения — описания участков, исполнитель уточнил их в таблицах до сдачи.

- `camera-mouse.tsv`, строки 5 и 10: проверка поля боя вызывает `getMouseCellFromScreen(coords.x, coords.y)` (`src/controls/cGameControlsContext.cpp@9208dcf:72`), а не `cellFromScreen(x,y)`; остальное в строках верно.
- Ноль участков в `src/cGame_logic.cpp`, `src/controls/cGameControlsContext.cpp` и `src/controls/cMouse.cpp` верен: строки с `sidebarWidth` и `SidebarWidth` в этих файлах есть уже в `BASE`, форк их не менял (`git diff BASE FORK1 -- <путь> | grep -c -E 'HudLayout|sidebarWidth|TopBarHeight|battlefield|Battlefield'` — 0 для каждого файла).
