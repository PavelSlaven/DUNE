## PLAN-OK-P4

План принят. Выполняй его шаги 1–10 в заявленном порядке и с заявленными исполнителями.

Решения по развилкам:

1. Развилка 1 принята: в `src/gameobjects/map/cMapCamera.h` остаётся объявление `void resetZoom();`, тело определяется в `src/gameobjects/map/cMapCamera.cpp` и состоит из одного вызова `setZoomLevel(m_gameSettings->getWorldScaleFactor());`. Конструктор камеры, строка 45: `m_zoomLevel = std::clamp(m_gameSettings->getWorldScaleFactor(), 0.25f, 4.0f);`.
2. Развилка 2 принята: `src/gameobjects/structures/cAbstractStructure.h` подключает `utils/cRectangle.h`.
3. Развилка 3: проверка места перед сборкой — как в задании; загрузка зависимостей не нужна.

Дополнительно к плану:

- После каждого законченного шага плана — одна строка в `.tmp/p4/progress.md`: номер шага, что сделано, файлы. Лимит Codex основного аккаунта близок к исчерпанию; если нить оборвётся, работу продолжат по этому журналу.
- Стоп только на `## DONE-P4` или `## Q-P4-NN`.
