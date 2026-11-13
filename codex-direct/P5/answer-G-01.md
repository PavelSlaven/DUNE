## Ответ на Q-P5G-01

Решение ведущего — дельта плана `PLAN-P5G-delta-01`. Твоё предложение принято.

1. Шаг 2, `src/debug/UiAudit.hpp`: в классе `UiAuditAccess` девять статических функций — восемь из шага 2 и после `static void resumeClock(cGame &game);` девятая строка `static bool fadeIsNone(const cGame &game);`. Других функций в классе нет.
2. Шаг 5, `src/debug/UiAuditAccess.cpp`: девять функций. `fadeIsNone` возвращает `game.m_cScreenFader->getAction() == eFadeAction::None`. В файл добавляется строка `#include "game/cScreenFader.h"`. Слова «восемь функций» в шаге 5 читай как «девять функций».
3. Шаг 6, `src/debug/UiAuditCapture.cpp`:
   - переменная объявлена как `bool g_fadeAtBegin = false;`;
   - в `beginFrame` строка 468 форка переносится как `g_fadeAtBegin = UiAuditAccess::fadeIsNone(game);`;
   - в `onFramePresented` условие строк 485–486 форка `g_fadeAtBegin == FADE_NONE && game.m_fadeAction == FADE_NONE` переносится как `g_fadeAtBegin && UiAuditAccess::fadeIsNone(game)`.
4. Правило переноса 2 для `game.m_fadeAction == FADE_NONE` в файле `src/debug/UiAuditCapture.cpp` заменено пунктом 3: прямого обращения к `m_cScreenFader` в этом файле нет.
5. Новая сверка к проверке 6: `grep -c 'fadeIsNone' src/debug/UiAudit.hpp src/debug/UiAuditAccess.cpp src/debug/UiAuditCapture.cpp` — `1`, `1`, `2`; `grep -c 'm_cScreenFader' src/debug/UiAuditCapture.cpp` — `0`.

Ведущий сверил остальные обращения кода захвата форка к объекту игры. `game.m_screenW`, `game.m_screenH` и `game.m_playing` переносятся по правилу 2 через поле `m_gameSettings`: оно открыто, `src/game/cGame.h:116`. Строки 440–442 и 443–446 форка в шаге 6 удалены. Других закрытых полей код захвата не трогает.

По `.tmp/p5g/progress.md` сделаны шаги 1–5 и 7–12. Сначала приведи шаги 2 и 5 к пунктам 1 и 2. Потом шаг 6 по пункту 3 и шаги 13–14. Затем дорожка D: проверки 1–7 задания. Всё остальное — по плану без изменений. Не отступай от плана, не переусложняй.

Остановки прежние: блок `## DONE-P5G` или блок `## Q-P5G-NN`.
