## Ответ на Q-P5G-02

Решение ведущего — дельта плана `PLAN-P5G-delta-02`. Код игры вне `src/debug/` не меняется; твоё предложение про `drawState` не принято.

Причина. В порту `cGame::drawState` (`src/game/cGame_logic.cpp:545-565`) запускает `FadeIn` в каждом кадре, где затемнение в состоянии `None`, поэтому `None` на границе кадра устойчиво не держится. Картинку при этом меняет только `FadeOut`: в этом состоянии `drawState` рисует сохранённый кадр с прозрачностью и выходит (строки 547–552). При `FadeIn` `drawState` рисует текущее состояние вызовом `m_currentState->draw()` (строка 562), а прозрачность `FadeIn` нигде не используется. Значит, в порту кадр готов к снимку, когда затемнение не в состоянии `FadeOut`.

1. Функция `UiAuditAccess::fadeIsNone` из дельты 01 заменяется функцией `notFadingOut` с тем же местом в классе:
   - `src/debug/UiAudit.hpp`: строка `static bool fadeIsNone(const cGame &game);` заменяется строкой `static bool notFadingOut(const cGame &game);`.
   - `src/debug/UiAuditAccess.cpp`: определение `fadeIsNone` заменяется определением `notFadingOut`, которое возвращает `game.m_cScreenFader->getAction() != eFadeAction::FadeOut`. Над определением — ровно одна строка комментария: `// drawState restarts the fade-in every idle frame and the fade-in does not change the picture; only a fade-out does.`
   - `src/debug/UiAuditCapture.cpp`: в `beginFrame` — `g_fadeAtBegin = UiAuditAccess::notFadingOut(game);`, в `onFramePresented` — `g_fadeAtBegin && UiAuditAccess::notFadingOut(game)`.
2. Сверка из пункта 5 дельты 01 заменяется: `grep -c 'notFadingOut' src/debug/UiAudit.hpp src/debug/UiAuditAccess.cpp src/debug/UiAuditCapture.cpp` — `1`, `1`, `2`; `grep -rc 'fadeIsNone' src/debug` — `0` у каждого файла; `grep -c 'm_cScreenFader' src/debug/UiAuditCapture.cpp` — `0`.

После правки снова пройди проверки 3–7 задания по порядку: сборка и 319 тестов, проверка 4, три скрипта Python, сверки `grep` с пунктом 2 этого ответа, `git status`. Если `ui_audit_main_menu_png.py` снова не пройдёт, остановись блоком `## Q-P5G-03`: приложи файл `.tmp/p5g/run-ui_audit_main_menu_png.py.log` целиком и код не меняй.

Чтение исходников, прогоны и сверки поручай помощнику D; корневая нить сводит итоги их сдач и сама команды проверок не повторяет. Всё остальное — по плану без изменений. Не отступай от плана, не переусложняй.

Остановки прежние: блок `## DONE-P5G` или блок `## Q-P5G-NN`.
