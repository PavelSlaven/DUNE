## A-P10C-01 — ответ на Q-P10C-02

Да. Правило 7 пункта 11 меняется: из него убирается `SDL_SCANCODE_UNKNOWN`. Строка `if (key == SDL_SCANCODE_UNKNOWN) {` в `onNotifyKeyboardEvent` файла `src/gamestates/cOptionsState.cpp` размечается в `keys.tsv` по правилу 5 пункта 11: `state` = `-`, `action` = `-`, `reason` = `сравнение с отсутствием клавиши`. Строка с `SDL_SCANCODE_ESCAPE` в `onNotifyKeyboardEvent` размечается по правилу 7, как записано: `state` = `options: key capture`, `action` = `cancel-capture`. Других отступлений от текста задания нет.

Продолжай с шага 7 плана и дальше по порядку до сдачи `## DONE-P10C`. Запись «Решено исполнителем» об этой разметке не нужна: она — ответ ведущего.
