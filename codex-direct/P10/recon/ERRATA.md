# Поправка ведущего к RECON-P10R

Источник: выборочная сверка `SPOTCHECK.md` (13 из 15 фактов совпали) и прямое чтение кода ведущим.

1. **Повторный вход в меню настроек** (`interaction.tsv`, строка «Повторный вход в меню настроек»; `RECON.md`, строка 287). Место в апстриме указано как `src/gamestates/cOptionsState.cpp@d06f2fc:39` — это только сигнатура конструктора. Функции `initializeDisplaySettings` в `UP1` нет. Повторный вход в меню в `UP1` идёт через `cOptionsState::setPrevState` (`src/gamestates/cOptionsState.cpp@d06f2fc:368-372`), который вызывает `refresh` (`@d06f2fc:374`): окно строится заново, состояние объекта не сбрасывается.
2. **Ёмкость очереди Starport** (`RECON.md`, строка 310). Константа `kMaxItemsToOrder = 8` стоит в `src/gameobjects/structures/cOrderProcesser.h@9208dcf:10`, а не `:31`; очередь `StarportOrderQueue<kMaxItemsToOrder> orderedItems` — `@9208dcf:66`.

Итоговые числа отчёта подтверждены сверкой: 41 участок в `hooks.tsv`, 40 проверок в тестах пункта 8.
