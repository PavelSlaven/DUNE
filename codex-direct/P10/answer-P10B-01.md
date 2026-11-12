## A-P10B-01 — ответ на Q-P10B-01

Пункт 5 контракта не меняется. Ветка без свободной клетки у Starport (`cellToDeployTo < 0`, доставка вызовом `REINFORCE`) остаётся как в апстриме: заказ снимается вызовом `orderProcesser->takeNextOrderToDeploy();` перед вызовом `REINFORCE`, на том же месте, где в ревизии `B` стоит `orderProcesser->markOrderAsDeployed(item);`. `REINFORCE` и `src/gameobjects/units/cReinforcements.cpp` не меняются: потеря заказа при неудачном `REINFORCE` — поведение апстрима, ведущий заводит на неё отдельную задачу.

Слова цели «Заказ снимается с очереди только после того, как юнит создан» относятся к ветке, где юнит создаёт `cUnits::unitCreate` у Starport (`cellToDeployTo >= 0`): там при `id < 0` срабатывает `return` до `takeNextOrderToDeploy()`, и заказ остаётся. Цель нити не меняй.

Продолжай с пункта 3 порядка раздела «Организация работы» задания: шаги 1 и 3 одновременно, дальше по порядку до сдачи `## DONE-P10B`.
