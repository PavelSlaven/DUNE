## Ответ на Q-P5G3BC-02 — PLAN-P5G3BC-delta-2

Конфликт подтверждён: в бою миссии 1 порт сам выделяет строительный двор игрока (`src/gameobjects/players/cPlayer.cpp:1732-1735`), поэтому во всех 20 сценах `units-label-*` и `structure-label-*` части 3а `drawRallyPoint` пишет метку `structure-selected` двора, который лежит вне области карты (после обрезки `w` = 0). Метка выделенного здания, которого нет на экране, не описывает экран. Предложенное исправление принято. Изменение шага 5 (а):

1. Строка `if (uiaudit::isEnabled()) { uiaudit::recordLabel("structure-selected", …); }` в `cDrawManager::drawRallyPoint` получает условие пересечения прямоугольника здания с областью карты — ровно такое: `if (uiaudit::isEnabled() && m_mapViewport->getX() < auditStructure.x + auditStructure.w && auditStructure.x < m_mapViewport->getX() + m_mapViewport->getWidth() && m_mapViewport->getY() < auditStructure.y + auditStructure.h && auditStructure.y < m_mapViewport->getY() + m_mapViewport->getHeight()) {`. Тело блока не меняется (`m_mapViewport` — поле `cDrawManager`, `src/managers/cDrawManager.h:155`).
2. Строка записи `rally-point` (шаг 5 (б)) и строка `const uiaudit::Rect auditStructure{…};` не меняются.

Других изменений плана нет. Дальше: правка строки 1 этого ответа (помощник B), затем шаг 9 (помощник D) — проверки 1–8 с начала: сборка заново, все десять скриптов, unittest, сверки `grep`, `git status`; затем сдача.
