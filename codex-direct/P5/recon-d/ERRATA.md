# Поправка ведущего к разведке П5г

Выборочная сверка Haiku (`SPOTCHECK.md`) — 15 из 15; сверка помощника 4 исполнителя (`spotcheck-executor.md`) — 12 из 12.

В `scenes.tsv` второй столбец указывает строку регистрации сцены (`scene("<имя>", ...)`); состояния и списки из третьего столбца (`GAME_MENU`, `GAME_OPTIONS`, `LIST_UPGRADES`) стоят в строках, названных в нём после слов «Код действий»: например, `UiAuditAccess::setState(game, GAME_MENU);` — `src/debug/UiAuditScenes.cpp@9208dcf:133` (функция `prepareMainMenu`, строка 132).
