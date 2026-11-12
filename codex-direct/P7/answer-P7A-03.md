## REVIEW-P7A-02

Сдача `DONE-P7A-R1` принята. Новое решение владельца меняет русский шрифт: Sangyo в порт не входит. Весь текст игры позже перейдёт на гладкие шрифты `RussoOne-Regular.ttf` и `PTSansNarrow-Regular.ttf` в обоих языках; это сделает отдельная часть шага. В этой части шрифты игры остаются как в апстриме в обоих языках, а кириллицу до той части рисует запасной `PTMono-Regular.ttf`. Исполняй пункты по порядку.

1. **Файлы.** Удали созданные этой задачей и не закоммиченные файлы `resources/bin/data/Sangyo-Regular.otf`, `resources/bin/data/licenses/Sangyo-LICENSE.txt`, `resources/bin/data/licenses/Sangyo-COPYRIGHT.txt` и пустую после этого папку `resources/bin/data/licenses/`. Это исключение из запрета на удаление: файлы — твоя работа в этой задаче.
2. **`src/context/ContextCreator.cpp`.** Убери выбор Sangyo:
   - игровой, диалоговый и мелкий шрифты в обоих языках открываются из `settings.ini` размером 12, как до задачи;
   - переменная `russianFontPath` и предупреждение о Sangyo удаляются;
   - лог: по строке `Hooked font: <имя файла>` на каждый шрифт;
   - запасной `PTMono-Regular.ttf` — без изменений: открывается и подключается `TTF_AddFallbackFont` к трём шрифтам в обоих языках, строка `Hooked fallback font: PTMono-Regular.ttf`.

   Включение `utils/Localization.hpp` в этом файле убери, если оно больше не используется.
3. **Тест T1 — `tests/utils/test_FontCoverage.cpp`.** Проверки переносятся на шрифты, которые будут рисовать текст; число проверок не уменьшается.
   - **Первый случай.** Шрифты `RussoOne-Regular.ttf` и `PTSansNarrow-Regular.ttf` размером 20 вместо Sangyo; запасной — `PTMono-Regular.ttf`. Для каждого из двух шрифтов:
     - 94 знака `russianRequired` есть у шрифта;
     - каждый из 5 знаков `serviceSymbols` есть у шрифта или у PTMono;
     - `ttfFontSupportsText(<шрифт>, "Повторить Миссии Далее")`;
     - `150%` есть у шрифта или у PTMono.

     Три проверки PTMono на `<`, `>` и `…` остаются. Итого 205 проверок.
   - **Второй случай** (стрелки). Вместо Sangyo проверяются `RussoOne-Regular.ttf` и `PTSansNarrow-Regular.ttf`: у них нет U+25C4 и U+25BA. Проверки PTMono, `arrakeen.fon`, `benegess.fon` и `small.ttf` остаются. Итого 12 проверок.
   - Название первого случая: `Russian text glyphs are covered by the UI fonts or the symbol fallback`.
4. **Тест T4 — `tests/ui_audit/ui_audit_language.py`.** В случае `--ui-audit-language ru` вместо строки `Hooked font: Sangyo-Regular.otf` требуется строка `Hooked fallback font: PTMono-Regular.ttf`; в выводе и логе обоих запусков нет подстроки `Sangyo`. Остальные проверки T4 не меняются.
5. **Проверки** раздела «Проверки» задания, логи с суффиксом `-r2`:
   - проверка 1: в итоговой строке `ctest.log` `<N>` не меньше 334;
   - проверки 2 и 3;
   - проверка 4 только для `ui_audit_part2_scenes.py`, `ui_audit_part3a_scenes.py` и `ui_audit_language.py`;
   - проверка 6 только для файлов, которые остались: `PTMono-Regular.ttf`, `OFL_RUSSO_ONE.txt`, `OFL_PT_FONTS.txt` и два файла Git LFS форка;
   - проверка 7 только для трёх оставшихся шрифтов;
   - проверка 8: в выводе нет `Sangyo` и нет `resources/bin/data/licenses/`.

   Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал.
6. **Сдача** — блок `## DONE-P7A-R2 | <время UTC из date -u> | HEAD <sha>`. В нём:
   - вывод проверок пункта 5 с кодами выхода;
   - строка Catch2 `All tests passed (<n> assertions in <m> test cases)` для тега `[font]`;
   - `git diff --no-index` трёх файлов `src/context/ContextCreator.cpp`, `tests/utils/test_FontCoverage.cpp` и `tests/ui_audit/ui_audit_language.py` относительно состояния `DONE-P7A-R1`;
   - новый список коммитов: «Шрифты и лицензии» без Sangyo, сообщение `Bundle the UI fonts, the symbol fallback font and their licenses`;
   - раздел «Решено исполнителем».

Помощники: один `gpt-6-luna` `xhigh` на проверки пункта 5. Правки пунктов 1–4 корневая нить делает сама: они дословные. Рамка правок: файлы пунктов 1–4 и `.tmp/p7a/`.

Не отступай от плана, не переусложняй.
