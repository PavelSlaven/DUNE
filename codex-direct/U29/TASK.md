# Задание U29 — остатки классической графики

Режим: **«План у ревьюера»** (см. «Режимы задания» в правилах исполнителя ниже): до правок пришли `## PLAN-U29` и стой до `PLAN-OK-U29`. Исполнитель: Codex `gpt-6-luna` `xhigh`.

## Цель

Закрыть issue #55 репозитория PavelSlaven/DUNE в рабочей копии `/srv/dune/worktrees/u29` (ветка `codex/u29-classic-leftovers` от `aff7776d`, вершины ветки U26 `codex/u26-hd-screens`): мёртвые классические ветки, члены без вызовов и всегда истинные параметры из текста #55 удалены; папка `resources/bin/data/scenes/hd4/hd4/` и файл `resources/bin/CLASSIC_WORLD_TRIAL_RU.txt` удалены из репозитория (решение владельца Р36); `resources/bin/README_RU.txt` не описывает классическую графику; игра рисует всё так же, как на `aff7776d`; сборка и все тесты CTest проходят.

## Источник истины

- Что удалить — текст #55 в разделе «Тексты issue» в конце задания (снят с GitHub 2026-11-04) и пункты раздела «Что сделать»; где пункт уточняет issue, верен пункт. Сверка ведущего на main `90e44509`: числа вхождений `m_adaptiveHdLayout` — BeneMentat.cpp 14, AtreidesMentat.cpp 11, HarkonnenMentat.cpp 11, OrdosMentat.cpp 11, AbstractMentat.cpp 19, AbstractMentat.h 1; все четыре ментата передают в `AbstractMentat` значение `true`; `tools/ui-audit/check_completeness.py` уже содержит `GRAPHICS = ("hd",)`.
- Решение Р36 (владелец, 2026-11-04, дословно из `docs/decisions.md`): «Папка `resources/bin/data/scenes/hd4/hd4/` и файл `resources/bin/CLASSIC_WORLD_TRIAL_RU.txt` удаляются из репозитория; в истории git они остаются.»
- Код — рабочая копия u29 на `aff7776d`. Сборка игры и CTest на servak — рецепт `/srv/dune/deps/sdl2/README.txt`. Аудит U11 — `tools/ui-audit/`.

## Что сделать

1. **Ментаты.** В `src/mentat/AbstractMentat.cpp`, `AbstractMentat.h`, `BeneMentat.cpp`, `AtreidesMentat.cpp`, `HarkonnenMentat.cpp`, `OrdosMentat.cpp` остаётся только код ветки `m_adaptiveHdLayout == true`; член `m_adaptiveHdLayout` и параметр конструктора `AbstractMentat`, который его задаёт, удаляются вместе с аргументом `true` у всех вызовов.
2. **Члены без вызовов.** Удаляются объявления и определения: `CreditsDrawer::drawCurrentCredits`, `drawPreviousCredits`, `getXDrawingOffset`; `cBuildingListDrawer::getCardGap`; `cMiniMapDrawer::m_iTrans`; `cDrawManager::m_sidebarColor`. `CreditsDrawer::thinkAboutIndividualCreditOffsets` и `getCreditDrawId` удаляются вместе с вызовом и с членами, которые пишет только эта пара, если ни один код рисования их не читает; в PLAN — список этих членов с файлом:строкой каждого чтения на `aff7776d`. Член читается кодом рисования — `Q` до правки.
3. **Всегда истинные параметры.** Удаляются параметр `hd` у `HudLayout::create`, `hdLayout` у `OptionsMenuLayout::create`, первый параметр `bool` у `shouldUsePhysicalHdPresentation`, `hd` у `MusicControlsLayout::create`, и классические ветки внутри этих функций; все вызовы в `src/` и `tests/` обновляются. Тестовые случаи, которые проверяют только классическую ветку (параметр `false`), удаляются; ожидания остальных тестов не меняются. В DONE — каждое удалённое или изменённое утверждение тестов с файлом:строкой на `aff7776d`.
4. **Данные (Р36).** `git rm -r resources/bin/data/scenes/hd4/hd4` и `git rm resources/bin/CLASSIC_WORLD_TRIAL_RU.txt`. До удаления — `rg -n` по `src/`, `tools/`, `.github/`, `CMakeLists.txt`, `resources/bin/*.txt` и `resources/bin/*.ini` на `hd4/hd4` и `CLASSIC_WORLD_TRIAL`: найденная ссылка вне удаляемых путей — `Q` до удаления.
5. **README.** В `resources/bin/README_RU.txt` удаляются описание классической графики и ключа `GraphicsMode` (на main `3e9d8a70` это строки 19, 25, 60, 152, 162, 195, 213; на `aff7776d` номера могут отличаться — ищи `rg -n -i "классич|Classic|GraphicsMode"`). Фраза, где классика — часть предложения о HD, переписывается так, чтобы описывать только HD. Остальной текст не меняется. В DONE — `git diff` файла целиком.

## Чем проверить

- Сборка игры и всех тестов на servak по `/srv/dune/deps/sdl2/README.txt`, папка сборки — `/srv/dune/worktrees/u29/.tmp/build`; CTest — все тесты, итоговая строка в DONE.
- **Тот же облик.** Аудит U11 сцен ментатов, окна настроек и игрового экрана на `1920x1080/ru/hd` и `1024x768/ru/hd` бинарником `aff7776d` и бинарником HEAD: записи геометрии текста (журналы аудита) совпадают. До сравнения — два прогона `aff7776d`: записи двух прогонов одной версии различаются — сравнивай только сцены, где они совпали, и перечисли остальные в DONE. Список сцен — в PLAN.
- `rg -n "m_adaptiveHdLayout|drawCurrentCredits|drawPreviousCredits|getXDrawingOffset|getCardGap|m_iTrans|m_sidebarColor" src tests` — пусто.
- `git diff --stat aff7776d` — только файлы из рамки правок.
- Диск: перед каждым прогоном аудита свободного места на `/srv` не меньше 5 ГБ; меньше — удали PNG своих прошлых прогонов во `.tmp/`, оставив журналы; не хватает и после этого — блок `Q` со строкой `df -h /srv` и стоп. Пакеты на servak не скачивать и не ставить.

## Что не трогать

Поведение и раскладку HD, пак и атласы, `tools/units3d/`, остальные файлы `resources/`, другие рабочие копии (только чтение).

## Организация работы

- Порядок: `PLAN-U29` (со списком членов пункта 2 и сценами проверки облика) → `PLAN-OK-U29` → пункты 1, 2, 3, 4–5 → сборка, CTest, проверка облика → сдача `DONE-U29`.
- Параллельно: пункты 1, 2, 3 и 4–5 правят разные файлы и идут одновременно; два прогона аудита `aff7776d` идут одновременно с правками.
- Помощники: до 4 одновременно, `gpt-6-luna` `xhigh`: первый — пункт 1, второй — пункт 2, третий — пункт 3, четвёртый — сборка `aff7776d` и её прогоны аудита, затем прогон HEAD и сравнение. Пункты 4–5, сборку HEAD, CTest и сверку делаешь сам.
- Остановки: `Q` по пунктам 2 и 4; правка вне рамки — `Q` до правки; после всех пунктов — сдача `DONE-U29`.
- Рамка правок: `src/mentat/`; `src/drawers/CreditsDrawer.*`, `cBuildingListDrawer.*`, `cMiniMapDrawer.*`; `src/managers/cDrawManager.*`; `src/sidebar/HudLayout.hpp`, `MusicControlsLayout.hpp`; `src/gamestates/OptionsMenuLayout.hpp`; файл с `shouldUsePhysicalHdPresentation`; вызовы этих четырёх функций в `src/` и `tests/`; удаление двух путей пункта 4; `resources/bin/README_RU.txt`; `.tmp/`.

## Сдача

Блок `## DONE-U29` по формату сдачи из правил ниже. Дополнительно: строка «#55: что сделано, пункт списка коммитов, проверка»; список удалённых и изменённых утверждений тестов; `git diff` README; вывод сравнения облика.
