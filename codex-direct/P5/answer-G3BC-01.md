## Ответ на Q-P5G3BC-01 — PLAN-P5G3BC-delta-1

Конфликт подтверждён: поле `cGame::m_eventEmitter` закрыто (`src/game/cGame.h:267`, после строки `private:` 185), а функции анонимного пространства имён в `src/debug/UiAuditAccess.cpp` не друзья `cGame`. Предложенное исправление принято — так же, как `createLabelUnit` части 3а получает `cEventEmitter *events` аргументом (`src/debug/UiAuditAccess.cpp:444`). Изменения шага 3 (б, в):

1. **`spawnUnit`.** Параметры — `cGame &currentGame, cEventEmitter *events, int type, int column, int row, float hpFraction`. Третий аргумент вызова `cUnits::unitCreate` — `events` вместо `currentGame.m_eventEmitter.get()`.
2. **`buildBase`.** Параметры — `cGame &currentGame, cEventEmitter *events, bool withRadar, BaseResult &result`. Каждый вызов `spawnUnit` в её теле передаёт `events` вторым аргументом, сразу после `currentGame`; строка 735 `FORK1` теперь — `result.tankId = spawnUnit(currentGame, events, TANK, 25, kStreetRow, 1.0f);`.
3. **`prepareGameScreen`.** Строка 788 `FORK1` теперь — `if (!buildBase(currentGame, currentGame.m_eventEmitter.get(), withRadar, base)) {`.

Других изменений шага 3 нет: остальные вспомогательные функции обращаются только к открытым полям `cGame` (`m_gameObjectsContext`, `m_infoContext`, `m_mapCamera`, `m_drawManager` объявлены после строки `public:` 91), а закрытые `m_mouse` и `m_notificationArea` читает только `UiAuditAccess::prepareGameScreen`.

Шаги 4–8 помощника B приняты: дифф пяти файлов совпал с планом. Дальше — по плану: шаги 1–3 (помощник A) с этой дельтой, затем шаг 9 (помощник D) и сдача. Остальные шаги, проверки и правила задания не меняются.
