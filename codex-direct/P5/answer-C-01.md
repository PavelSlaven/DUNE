## Ответ на Q-P5C-01

Решение ведущего — дельта плана `PLAN-P5C-delta-01`.

1. В шаге 6 разрешено поле `cGameSettings* m_settings` в классе `CreditsDrawer` (`src/drawers/CreditsDrawer.h`). Поле инициализируется параметром конструктора `settings` в `src/drawers/CreditsDrawer.cpp`. `CreditsDrawer::draw` берёт размеры экрана через `m_settings->getScreenW()` и `m_settings->getScreenH()`. Это уже сделано в рабочей копии; оставь как есть.
2. Фраза шага 6 «Остальные функции и поля не меняются» действует с этим исключением: в классе `CreditsDrawer` добавляются только поля `m_settings` и `m_gameTextDrawer`, остальные поля не меняются.

Продолжай с шага C/7: перенос `src/drawers/cBuildingListDrawer.h` и `src/drawers/cBuildingListDrawer.cpp` по таблице `PLAN-P5C`, включая строку «Слияние `drawList`». Затем дорожка D: проверки 1–6 задания. Всё остальное — по плану без изменений. Не отступай от плана, не переусложняй.

Остановки прежние: блок `## DONE-P5C` или блок `## Q-P5C-NN`.
