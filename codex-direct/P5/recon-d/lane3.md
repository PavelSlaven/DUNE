# Дорожка 3: сцены, инструменты и тесты

Ревизии исходных фактов: `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `PORT=7eb119b007c05f063fe6dacf2e93ae31ac135b33`. Готовые таблицы: `.tmp/p5dr/scenes.tsv` (157 строк сцен и заголовок) и `.tmp/p5dr/tools.tsv` (35 файлов и заголовок).

## 3. Сцены

Команда получения перечня всех мест, где каталог присваивает имя сцене:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | grep -n 'scene("'
```

Вывод сохранён ниже как `Список сцен`. Строки `UiAuditScenes.hpp` задают структуру записи `Scene` (поля `id`, `group`, `state`, `screen`, `house`, флаги показа/наведения и callbacks), а конкретные имена присваиваются в каталоге `UiAuditScenes.cpp:362-569`.

Сопоставление группы с состоянием и экраном берётся из `src/debug/UiAuditScenes.cpp@9208dcf:49-63`. Команда и вывод:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | nl -ba | sed -n '49,63p'
```

В таблице действие каждой сцены приведено по callback, назначенному в каталоге: переключения состояний и подготовка игры определены в `UiAuditScenes.cpp@9208dcf:97-334`; операции с картой, `SaveSlotsDialog`, страницами настроек и `cDrawManager` — в `UiAuditAccess.cpp@9208dcf:67-178`, `181-229`, `274-283`, `536-549`, `780-934`. Эти фрагменты получены командами:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | nl -ba | sed -n '97,160p;176,260p;284,334p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '67,178p;181,229p;274,283p;536,549p;780,934p'
```

Для колонки «шаг» проверялась строка каталога, где указано имя конкретной сцены. Ни одна из 157 строк `scene("…")` не содержит подстрок словаря; все строки таблицы помечены `П5г`. Вспомогательная таблица экранов содержит `SaveSlotsDialog` (`UiAuditScenes.cpp@9208dcf:57-58`), но это не строка присвоения имени конкретной сцены.

### Проверка классов в PORT

Выполнялись `git grep -n 'class <имя>' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src` для имён классов из `kGroupScreens` и ментатов. Вывод найденных определений:

```text
src/gamestates/cMainMenuState.h:35:class cMainMenuState : public cGameState {
src/gamestates/cSelectYourNextConquestState.h:77:class cSelectYourNextConquestState : public cGameState {
src/gamestates/cChooseHouseState.h:35:class cChooseHouseState : public cGameState {
src/gamestates/cSelectMissionState.h:35:class cSelectMissionState : public cGameState {
src/gameobjects/mentat/BeneMentat.h:28:class BeneMentat : public AbstractMentat {
src/gamestates/cOptionsState.h:38:class cOptionsState : public cGameState {
src/gamestates/cCreditsState.h:42:class cCreditsState : public cGameState {
src/gamestates/cSetupSkirmishState.h:59:class cSetupSkirmishState : public cGameState {
src/managers/cDrawManager.h:57:class cDrawManager : cInputObserver {
src/gameobjects/mentat/AtreidesMentat.h:20:class AtreidesMentat : public AbstractMentat {
src/gameobjects/mentat/HarkonnenMentat.h:20:class HarkonnenMentat : public AbstractMentat {
src/gameobjects/mentat/OrdosMentat.h:20:class OrdosMentat : public AbstractMentat {
```

Для `SaveSlotsDialog` команда `git grep -n 'class SaveSlotsDialog' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src` вывела пустую строку. Поле `cGame::drawOutcomeScreen` в каталоге — метод, а не имя класса; `git grep -n 'class cGame::drawOutcomeScreen' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src` также не вывел строк. Хост-класс `cGame` определён в `src/game/cGame.h@7eb119b:88` (`class cGame : …`).

Полные имена, исходные строки, действия, класс/экран, проверка наличия класса и шаг находятся в таблице ниже и отдельно в `.tmp/p5dr/scenes.tsv`.

## 5. Инструменты и тесты

Команда, заданная в условии, и её полный вывод:

```sh
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tools/ui-audit tests | grep -i -E 'audit'
```

Вывод — 35 путей; в нём также перечислены четыре runtime/C++ теста под `tests/` и Python unit-тесты в `tools/ui-audit/tests/`. Каждый путь проверен командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> | wc -l` и `git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- <путь>`. Ни один из 35 путей не найден в PORT. Числа строк и статусы по каждому пути приведены в таблице ниже.

Для каждого basename списка выполнены команды поиска регистрации и workflow:

```sh
git grep -n '<имя файла>' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt tests/CMakeLists.txt
git grep -n '<имя файла>' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- .github
```

Непустой вывод CTest:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:446:        tests/UiAuditArgumentsTests.cpp
9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:471:                ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_main_menu_png.py
9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:463:                ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_unknown_scene.py
```

Для остальных 32 basename CTest-команда вывела пустой результат с кодом 1. Все 35 поисков basename в `.github` вывели пустой результат с кодом 1. В CMake `ui_audit_arguments` добавлен как тест в `CMakeLists.txt@9208dcf:444-454`; два runtime-теста условно добавлены при `D2TM_UI_AUDIT_RUNTIME_TESTS` в `CMakeLists.txt@9208dcf:456-474`.

Имена функций верхнего уровня, первый комментарий/отсутствие описания, пути файлового ввода-вывода с `путь@ревизия:строка`, результаты поиска CTest/workflow/ссылок из других файлов списка и наличие в PORT указаны построчно в `tools.tsv`. Фактические CTest/workflow и import/caller ссылки сохранены в этих строках. Файлы `tools/ui-audit/` и тесты не запускались.

Данные TSV:

```text
tools/ui-audit/exclusions.tsv: header=name<TAB>reason; total=10; data=9
tools/ui-audit/keys.tsv: header=file<TAB>function<TAB>key<TAB>mods<TAB>line<TAB>state<TAB>action<TAB>reason; total=169; data=168
```

Получено командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> | wc -l` (10 и 169 строк), `git show …:tools/ui-audit/exclusions.tsv | sed -n '1p'` и `git show …:tools/ui-audit/keys.tsv | sed -n '1p'`. Заголовки и первые записи проверялись `git show …:<путь> | nl -ba | sed -n '1,3p'`; вывод: `name<TAB>reason`, `GAME_EDITING<TAB>режим редактора карт, не экран игрока и не достижим из меню`; и `file<TAB>function<TAB>key<TAB>mods<TAB>line<TAB>state<TAB>action<TAB>reason`, `src/building/cItemBuilder.cpp<TAB>cItemBuilder::onKeyHold<TAB>SDL_SCANCODE_LSHIFT<TAB><пусто><TAB>826<TAB>game: nothing selected | game: structure selected | game: units selected | game: repair mode | game: debug mode<TAB>build-multiplier<TAB><пусто>`.

## Таблица сцен

Источник: `.tmp/p5dr/scenes.tsv`.

```tsv
сцена	путь@9208dcf:строка	действия сцены	класс состояния	класс в PORT	шаг
main-menu	src/debug/UiAuditScenes.cpp@9208dcf:363	GAME_MENU; переводит игру в главное меню; миссия и карта не загружаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:132.	cMainMenuState	есть: src/gamestates/cMainMenuState.h@7eb119b:35	П5г
region-atreides-intro-1	src/debug/UiAuditScenes.cpp@9208dcf:364	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 1; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-intro-2	src/debug/UiAuditScenes.cpp@9208dcf:365	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 2; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-intro-3	src/debug/UiAuditScenes.cpp@9208dcf:366	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 3; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-conquer-3	src/debug/UiAuditScenes.cpp@9208dcf:367	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-conquer-5	src/debug/UiAuditScenes.cpp@9208dcf:368	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-conquer-7	src/debug/UiAuditScenes.cpp@9208dcf:369	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-conquer-9	src/debug/UiAuditScenes.cpp@9208dcf:370	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-2	src/debug/UiAuditScenes.cpp@9208dcf:371	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=2, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-3	src/debug/UiAuditScenes.cpp@9208dcf:372	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-4	src/debug/UiAuditScenes.cpp@9208dcf:373	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=4, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-5	src/debug/UiAuditScenes.cpp@9208dcf:374	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-6	src/debug/UiAuditScenes.cpp@9208dcf:375	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=6, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-7	src/debug/UiAuditScenes.cpp@9208dcf:376	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-8	src/debug/UiAuditScenes.cpp@9208dcf:377	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=8, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-atreides-select-9	src/debug/UiAuditScenes.cpp@9208dcf:378	GAME_REGION; HUMAN House=ATREIDES; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-intro-1	src/debug/UiAuditScenes.cpp@9208dcf:379	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 1; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-intro-2	src/debug/UiAuditScenes.cpp@9208dcf:380	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 2; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-intro-3	src/debug/UiAuditScenes.cpp@9208dcf:381	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 3; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-conquer-3	src/debug/UiAuditScenes.cpp@9208dcf:382	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-conquer-5	src/debug/UiAuditScenes.cpp@9208dcf:383	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-conquer-7	src/debug/UiAuditScenes.cpp@9208dcf:384	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-conquer-9	src/debug/UiAuditScenes.cpp@9208dcf:385	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-2	src/debug/UiAuditScenes.cpp@9208dcf:386	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=2, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-3	src/debug/UiAuditScenes.cpp@9208dcf:387	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-4	src/debug/UiAuditScenes.cpp@9208dcf:388	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=4, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-5	src/debug/UiAuditScenes.cpp@9208dcf:389	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-6	src/debug/UiAuditScenes.cpp@9208dcf:390	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=6, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-7	src/debug/UiAuditScenes.cpp@9208dcf:391	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-8	src/debug/UiAuditScenes.cpp@9208dcf:392	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=8, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-harkonnen-select-9	src/debug/UiAuditScenes.cpp@9208dcf:393	GAME_REGION; HUMAN House=HARKONNEN; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-intro-1	src/debug/UiAuditScenes.cpp@9208dcf:394	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 1; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-intro-2	src/debug/UiAuditScenes.cpp@9208dcf:395	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 2; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-intro-3	src/debug/UiAuditScenes.cpp@9208dcf:396	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=1, jump=false); карта боя не загружается; ожидает сцену вступления 3; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-conquer-3	src/debug/UiAuditScenes.cpp@9208dcf:397	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-conquer-5	src/debug/UiAuditScenes.cpp@9208dcf:398	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-conquer-7	src/debug/UiAuditScenes.cpp@9208dcf:399	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-conquer-9	src/debug/UiAuditScenes.cpp@9208dcf:400	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает сообщение о завоевании; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-2	src/debug/UiAuditScenes.cpp@9208dcf:401	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=2, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-3	src/debug/UiAuditScenes.cpp@9208dcf:402	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=3, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-4	src/debug/UiAuditScenes.cpp@9208dcf:403	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=4, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-5	src/debug/UiAuditScenes.cpp@9208dcf:404	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=5, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-6	src/debug/UiAuditScenes.cpp@9208dcf:405	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=6, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-7	src/debug/UiAuditScenes.cpp@9208dcf:406	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=7, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-8	src/debug/UiAuditScenes.cpp@9208dcf:407	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=8, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
region-ordos-select-9	src/debug/UiAuditScenes.cpp@9208dcf:408	GAME_REGION; HUMAN House=ORDOS; regionOpen(mission=9, jump=true); карта боя не загружается; ожидает состояние выбора следующего завоевания; щелчков и клавиш нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:327; src/debug/UiAuditAccess.cpp@9208dcf:274.	cSelectYourNextConquestState	есть: src/gamestates/cSelectYourNextConquestState.h@7eb119b:77	П5г
choose-house	src/debug/UiAuditScenes.cpp@9208dcf:409	GAME_SELECT_HOUSE; открывает выбор Дома; миссия и карта не загружаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:138.	cChooseHouseState	есть: src/gamestates/cChooseHouseState.h@7eb119b:35	П5г
select-mission-atreides	src/debug/UiAuditScenes.cpp@9208dcf:410	GAME_MISSIONSELECT; HUMAN House=ATREIDES; открывает выбор миссии без загрузки миссии/карты; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:144.	cSelectMissionState	есть: src/gamestates/cSelectMissionState.h@7eb119b:35	П5г
select-mission-harkonnen	src/debug/UiAuditScenes.cpp@9208dcf:411	GAME_MISSIONSELECT; HUMAN House=HARKONNEN; открывает выбор миссии без загрузки миссии/карты; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:144.	cSelectMissionState	есть: src/gamestates/cSelectMissionState.h@7eb119b:35	П5г
select-mission-ordos	src/debug/UiAuditScenes.cpp@9208dcf:413	GAME_MISSIONSELECT; HUMAN House=ORDOS; открывает выбор миссии без загрузки миссии/карты; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:144.	cSelectMissionState	есть: src/gamestates/cSelectMissionState.h@7eb119b:35	П5г
tellhouse-atreides-speak	src/debug/UiAuditScenes.cpp@9208dcf:414	GAME_TELLHOUSE; HUMAN House=ATREIDES; prepareTellHouse; фиксирует Mentat в SPEAKING на выбранной фразе; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
tellhouse-atreides-await	src/debug/UiAuditScenes.cpp@9208dcf:416	GAME_TELLHOUSE; HUMAN House=ATREIDES; prepareTellHouse; ожидает ответ Mentat; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
tellhouse-harkonnen-speak	src/debug/UiAuditScenes.cpp@9208dcf:418	GAME_TELLHOUSE; HUMAN House=HARKONNEN; prepareTellHouse; фиксирует Mentat в SPEAKING на выбранной фразе; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
tellhouse-harkonnen-await	src/debug/UiAuditScenes.cpp@9208dcf:420	GAME_TELLHOUSE; HUMAN House=HARKONNEN; prepareTellHouse; ожидает ответ Mentat; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
tellhouse-ordos-speak	src/debug/UiAuditScenes.cpp@9208dcf:422	GAME_TELLHOUSE; HUMAN House=ORDOS; prepareTellHouse; фиксирует Mentat в SPEAKING на выбранной фразе; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
tellhouse-ordos-await	src/debug/UiAuditScenes.cpp@9208dcf:424	GAME_TELLHOUSE; HUMAN House=ORDOS; prepareTellHouse; ожидает ответ Mentat; миссия и карта не загружаются; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:152; src/debug/UiAuditAccess.cpp@9208dcf:67.	BeneMentat	есть: src/gameobjects/mentat/BeneMentat.h@7eb119b:28	П5г
mentat-briefing-atreides-speak	src/debug/UiAuditScenes.cpp@9208dcf:426	GAME_BRIEFING; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-briefing-atreides-await	src/debug/UiAuditScenes.cpp@9208dcf:428	GAME_BRIEFING; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-win-atreides-speak	src/debug/UiAuditScenes.cpp@9208dcf:430	GAME_WINBRIEF; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-win-atreides-await	src/debug/UiAuditScenes.cpp@9208dcf:432	GAME_WINBRIEF; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-lose-atreides-speak	src/debug/UiAuditScenes.cpp@9208dcf:434	GAME_LOSEBRIEF; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-lose-atreides-await	src/debug/UiAuditScenes.cpp@9208dcf:436	GAME_LOSEBRIEF; HUMAN House=ATREIDES; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	AtreidesMentat	есть: src/gameobjects/mentat/AtreidesMentat.h@7eb119b:20	П5г
mentat-briefing-harkonnen-speak	src/debug/UiAuditScenes.cpp@9208dcf:438	GAME_BRIEFING; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-briefing-harkonnen-await	src/debug/UiAuditScenes.cpp@9208dcf:440	GAME_BRIEFING; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-win-harkonnen-speak	src/debug/UiAuditScenes.cpp@9208dcf:442	GAME_WINBRIEF; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-win-harkonnen-await	src/debug/UiAuditScenes.cpp@9208dcf:444	GAME_WINBRIEF; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-lose-harkonnen-speak	src/debug/UiAuditScenes.cpp@9208dcf:446	GAME_LOSEBRIEF; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-lose-harkonnen-await	src/debug/UiAuditScenes.cpp@9208dcf:448	GAME_LOSEBRIEF; HUMAN House=HARKONNEN; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	HarkonnenMentat	есть: src/gameobjects/mentat/HarkonnenMentat.h@7eb119b:20	П5г
mentat-briefing-ordos-speak	src/debug/UiAuditScenes.cpp@9208dcf:450	GAME_BRIEFING; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
mentat-briefing-ordos-await	src/debug/UiAuditScenes.cpp@9208dcf:452	GAME_BRIEFING; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=0); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
mentat-win-ordos-speak	src/debug/UiAuditScenes.cpp@9208dcf:454	GAME_WINBRIEF; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
mentat-win-ordos-await	src/debug/UiAuditScenes.cpp@9208dcf:456	GAME_WINBRIEF; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=1); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
mentat-lose-ordos-speak	src/debug/UiAuditScenes.cpp@9208dcf:458	GAME_LOSEBRIEF; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в SPEAKING; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
mentat-lose-ordos-await	src/debug/UiAuditScenes.cpp@9208dcf:460	GAME_LOSEBRIEF; HUMAN House=ORDOS; регион 1; prepareMentatScene(kind=2); фиксирует Mentat в AWAITING_RESPONSE; карта боя не загружается; ввода мышью/клавишами нет. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:97; src/debug/UiAuditAccess.cpp@9208dcf:97.	OrdosMentat	есть: src/gameobjects/mentat/OrdosMentat.h@7eb119b:20	П5г
skirmish-setup-random	src/debug/UiAuditScenes.cpp@9208dcf:462	GAME_SETUPSKIRMISH; загружает список карт схватки и инициализирует схватку, вариант 0 (случайная карта); Дом не задан; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:104; src/debug/UiAuditAccess.cpp@9208dcf:112.	cSetupSkirmishState	есть: src/gamestates/cSetupSkirmishState.h@7eb119b:59	П5г
skirmish-setup-ready-map	src/debug/UiAuditScenes.cpp@9208dcf:463	GAME_SETUPSKIRMISH; загружает список карт схватки и инициализирует схватку, вариант 1 (карта с четырьмя стартовыми позициями, игроки 3 и 4 включены); Дом не задан; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:104; src/debug/UiAuditAccess.cpp@9208dcf:112.	cSetupSkirmishState	есть: src/gamestates/cSetupSkirmishState.h@7eb119b:59	П5г
outcome-win	src/debug/UiAuditScenes.cpp@9208dcf:465	сначала GAME_PLAYING, House=ATREIDES, миссия/регион 1; затем GAME_WINNING и экран исхода победы; файла карты явно не задаёт; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:111; src/debug/UiAuditAccess.cpp@9208dcf:131.	cGame::drawOutcomeScreen	есть хост-класс cGame: src/game/cGame.h@7eb119b:88; метод screen — drawOutcomeScreen	П5г
outcome-lose	src/debug/UiAuditScenes.cpp@9208dcf:467	сначала GAME_PLAYING, House=ATREIDES, миссия/регион 1; затем GAME_LOSING и экран исхода поражения; файла карты явно не задаёт; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:111; src/debug/UiAuditAccess.cpp@9208dcf:131.	cGame::drawOutcomeScreen	есть хост-класс cGame: src/game/cGame.h@7eb119b:88; метод screen — drawOutcomeScreen	П5г
options-menu-main	src/debug/UiAuditScenes.cpp@9208dcf:469	сначала GAME_MENU, затем GAME_OPTIONS; оставляет главную страницу; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-menu-applied	src/debug/UiAuditScenes.cpp@9208dcf:471	сначала GAME_MENU, затем GAME_OPTIONS; записывает статус Saved. Restart the game.; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-menu-game	src/debug/UiAuditScenes.cpp@9208dcf:473	сначала GAME_MENU, затем GAME_OPTIONS; открывает страницу Game; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-menu-controls	src/debug/UiAuditScenes.cpp@9208dcf:475	сначала GAME_MENU, затем GAME_OPTIONS; открывает страницу Controls; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-menu-diagnostics	src/debug/UiAuditScenes.cpp@9208dcf:477	сначала GAME_MENU, затем GAME_OPTIONS; открывает страницу Diagnostics; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-menu-keybind	src/debug/UiAuditScenes.cpp@9208dcf:479	сначала GAME_MENU, затем GAME_OPTIONS; открывает Controls и включает захват действия Attack; Дом, миссия и карта не задаются; действия выполняются прямыми вызовами состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:176; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
main-menu-saves	src/debug/UiAuditScenes.cpp@9208dcf:481	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт save slots 1, 2, 5, повреждённый slot 3 и каталог slot 6; возвращается в GAME_MENU; без мыши/клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:222; src/debug/UiAuditAccess.cpp@9208dcf:138.	cMainMenuState	есть: src/gamestates/cMainMenuState.h@7eb119b:35	П5г
save-dialog-menu	src/debug/UiAuditScenes.cpp@9208dcf:482	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт save slots 1, 2, 5, повреждённый slot 3 и каталог slot 6; открывает меню сохранения вызовом open(false,false); без мыши/клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:222; src/debug/UiAuditScenes.cpp@9208dcf:233; src/debug/UiAuditAccess.cpp@9208dcf:138; src/debug/UiAuditAccess.cpp@9208dcf:149.	SaveSlotsDialog	нет	П5г
options-game-main-saves	src/debug/UiAuditScenes.cpp@9208dcf:484	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; главная страница с созданными слотами; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-main-nosaves	src/debug/UiAuditScenes.cpp@9208dcf:486	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; затем GAME_OPTIONS; главная страница без созданных слотов; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-applied	src/debug/UiAuditScenes.cpp@9208dcf:488	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; статус Saved. Restart the game.; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-game	src/debug/UiAuditScenes.cpp@9208dcf:490	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; страница Game; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-controls	src/debug/UiAuditScenes.cpp@9208dcf:492	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; страница Controls; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-diagnostics	src/debug/UiAuditScenes.cpp@9208dcf:494	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; страница Diagnostics; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
options-game-keybind	src/debug/UiAuditScenes.cpp@9208dcf:496	входит в GAME_PLAYING для ATREIDES, миссия/регион 1; создаёт тестовые save slots; затем GAME_OPTIONS; страница Controls с захватом Attack; прямые вызовы состояния, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:248; src/debug/UiAuditScenes.cpp@9208dcf:185; src/debug/UiAuditAccess.cpp@9208dcf:181; src/debug/UiAuditAccess.cpp@9208dcf:191; src/debug/UiAuditAccess.cpp@9208dcf:202.	cOptionsState	есть: src/gamestates/cOptionsState.h@7eb119b:38	П5г
save-dialog-load	src/debug/UiAuditScenes.cpp@9208dcf:498	входит в GAME_PLAYING для ATREIDES, миссия/регион 1 и создаёт тестовые slots; затем GAME_OPTIONS и saveDialog(action=0): открывает диалог загрузки; прямые вызовы, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:261; src/debug/UiAuditAccess.cpp@9208dcf:159.	SaveSlotsDialog	нет	П5г
save-dialog-save-new	src/debug/UiAuditScenes.cpp@9208dcf:500	входит в GAME_PLAYING для ATREIDES, миссия/регион 1 и создаёт тестовые slots; затем GAME_OPTIONS и saveDialog(action=1): открывает диалог сохранения для новой записи; прямые вызовы, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:261; src/debug/UiAuditAccess.cpp@9208dcf:159.	SaveSlotsDialog	нет	П5г
save-dialog-overwrite	src/debug/UiAuditScenes.cpp@9208dcf:502	входит в GAME_PLAYING для ATREIDES, миссия/регион 1 и создаёт тестовые slots; затем GAME_OPTIONS и saveDialog(action=2): выбирает slot 2 для перезаписи; прямые вызовы, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:261; src/debug/UiAuditAccess.cpp@9208dcf:159.	SaveSlotsDialog	нет	П5г
save-dialog-load-error	src/debug/UiAuditScenes.cpp@9208dcf:504	входит в GAME_PLAYING для ATREIDES, миссия/регион 1 и создаёт тестовые slots; затем GAME_OPTIONS и saveDialog(action=3): выбирает slot 3 и вызывает загрузку повреждённого сохранения; прямые вызовы, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:261; src/debug/UiAuditAccess.cpp@9208dcf:159.	SaveSlotsDialog	нет	П5г
save-dialog-save-error	src/debug/UiAuditScenes.cpp@9208dcf:506	входит в GAME_PLAYING для ATREIDES, миссия/регион 1 и создаёт тестовые slots; затем GAME_OPTIONS и saveDialog(action=4): выбирает каталог slot 6 и вызывает сохранение; прямые вызовы, без мыши и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:261; src/debug/UiAuditAccess.cpp@9208dcf:159.	SaveSlotsDialog	нет	П5г
credits-title	src/debug/UiAuditScenes.cpp@9208dcf:508	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=0; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
credits-1	src/debug/UiAuditScenes.cpp@9208dcf:509	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=1; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
credits-2	src/debug/UiAuditScenes.cpp@9208dcf:510	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=2; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
credits-3	src/debug/UiAuditScenes.cpp@9208dcf:511	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=3; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
credits-4	src/debug/UiAuditScenes.cpp@9208dcf:512	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=4; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
credits-5	src/debug/UiAuditScenes.cpp@9208dcf:513	GAME_CREDITS; включает вертикальную обрезку текста и прокрутку титров до frame=5; Дом, миссия и карта не задаются; мышь и клавиатура не задействуются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:284; src/debug/UiAuditScenes.cpp@9208dcf:292; src/debug/UiAuditAccess.cpp@9208dcf:213.	cCreditsState	есть: src/gamestates/cCreditsState.h@7eb119b:42	П5г
structure-label-top	src/debug/UiAuditScenes.cpp@9208dcf:514	GAME_PLAYING; ATREIDES, миссия/регион 1; создаёт WINDTRAP у верхнем краю видимой карты; задаёт hover на здании; клик и клавиши не генерирует. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:320; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:591.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
structure-label-right	src/debug/UiAuditScenes.cpp@9208dcf:516	GAME_PLAYING; ATREIDES, миссия/регион 1; создаёт WINDTRAP у правом краю видимой карты; задаёт hover на здании; клик и клавиши не генерирует. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:320; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:591.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-trike	src/debug/UiAuditScenes.cpp@9208dcf:518	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита TRIKE на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-raider	src/debug/UiAuditScenes.cpp@9208dcf:519	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита RAIDER на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-quad	src/debug/UiAuditScenes.cpp@9208dcf:520	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита QUAD на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-tank	src/debug/UiAuditScenes.cpp@9208dcf:521	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита TANK на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-siegetank	src/debug/UiAuditScenes.cpp@9208dcf:522	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита SIEGETANK на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-launcher	src/debug/UiAuditScenes.cpp@9208dcf:523	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита LAUNCHER на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-deviator	src/debug/UiAuditScenes.cpp@9208dcf:524	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита DEVIATOR на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-sonictank	src/debug/UiAuditScenes.cpp@9208dcf:525	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита SONICTANK на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-devastator	src/debug/UiAuditScenes.cpp@9208dcf:526	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита DEVASTATOR на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-harvester	src/debug/UiAuditScenes.cpp@9208dcf:527	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита HARVESTER на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-mcv	src/debug/UiAuditScenes.cpp@9208dcf:528	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита MCV на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-soldier	src/debug/UiAuditScenes.cpp@9208dcf:529	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита SOLDIER на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-infantry	src/debug/UiAuditScenes.cpp@9208dcf:530	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита INFANTRY на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-trooper	src/debug/UiAuditScenes.cpp@9208dcf:531	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита TROOPER на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-troopers	src/debug/UiAuditScenes.cpp@9208dcf:532	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита TROOPERS на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-unit-fremen-one	src/debug/UiAuditScenes.cpp@9208dcf:533	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита UNIT_FREMEN_ONE на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-unit-fremen-three	src/debug/UiAuditScenes.cpp@9208dcf:534	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита UNIT_FREMEN_THREE на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
units-label-saboteur	src/debug/UiAuditScenes.cpp@9208dcf:535	GAME_PLAYING; ATREIDES, миссия/регион 1; размещает три выбранных юнита SABOTEUR на верхнем, правом и нижнем краях видимой карты; без наведения, кликов и клавиш. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:306; src/debug/UiAuditAccess.cpp@9208dcf:536; src/debug/UiAuditAccess.cpp@9208dcf:551.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-hud	src/debug/UiAuditScenes.cpp@9208dcf:536	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и HUD и базу ATREIDES; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-music	src/debug/UiAuditScenes.cpp@9208dcf:537	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и длинное имя игрового музыкального трека; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:827.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-command-damaged-unit	src/debug/UiAuditScenes.cpp@9208dcf:538	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает повреждённый танк; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:843.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-command-harvester	src/debug/UiAuditScenes.cpp@9208dcf:539	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает комбайн; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:846.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-command-mcv	src/debug/UiAuditScenes.cpp@9208dcf:540	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает MCV; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:849.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-structure-selected	src/debug/UiAuditScenes.cpp@9208dcf:541	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает завод; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:852.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-build	src/debug/UiAuditScenes.cpp@9208dcf:542	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список строительства; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-infantry	src/debug/UiAuditScenes.cpp@9208dcf:543	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список пехоты; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-vehicles	src/debug/UiAuditScenes.cpp@9208dcf:544	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список техники; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-starport	src/debug/UiAuditScenes.cpp@9208dcf:545	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список космопорта; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-palace	src/debug/UiAuditScenes.cpp@9208dcf:546	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список дворца; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-upgrades	src/debug/UiAuditScenes.cpp@9208dcf:547	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает список улучшений; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-radar-none	src/debug/UiAuditScenes.cpp@9208dcf:548	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и строит базу без радара; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:787.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-radar-nopower	src/debug/UiAuditScenes.cpp@9208dcf:549	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и строит базу без достаточного энергоснабжения; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:791.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-place-allowed	src/debug/UiAuditScenes.cpp@9208dcf:550	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и включает режим размещения ветряка, меняет четыре клетки на камень и наводит курсор на разрешённое место; сцена помечена hover=true; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:859.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-place-forbidden	src/debug/UiAuditScenes.cpp@9208dcf:551	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и включает режим размещения ветряка и наводит курсор на запрещённое место; сцена помечена hover=true; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:859.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-group-select	src/debug/UiAuditScenes.cpp@9208dcf:552	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и заполняет координаты прямоугольного выделения мыши; реальное нажатие не генерирует; сцена помечена hover=true; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:881.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-messages	src/debug/UiAuditScenes.cpp@9208dcf:553	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и создаёт сообщение о строительстве и уведомления трёх приоритетов; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:892.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-item-hover	src/debug/UiAuditScenes.cpp@9208dcf:554	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и наводит курсор на третью карточку списка строительства; сцена помечена hover=true; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:908.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-list-scroll-end	src/debug/UiAuditScenes.cpp@9208dcf:555	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и прокручивает список строительства к строке 1000; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:908.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-rally-point	src/debug/UiAuditScenes.cpp@9208dcf:556	GAME_PLAYING; Дом=ATREIDES, миссия/регион 22; подготавливает базу и выбирает завод и задаёт точку сбора на клетке (28,32); файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780; src/debug/UiAuditAccess.cpp@9208dcf:855.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-build	src/debug/UiAuditScenes.cpp@9208dcf:557	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_CONSTYARD; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-infantry	src/debug/UiAuditScenes.cpp@9208dcf:558	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_FOOT_UNITS; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-vehicles	src/debug/UiAuditScenes.cpp@9208dcf:559	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_UNITS; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-starport	src/debug/UiAuditScenes.cpp@9208dcf:560	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_STARPORT; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-palace	src/debug/UiAuditScenes.cpp@9208dcf:561	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_PALACE; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-harkonnen-list-upgrades	src/debug/UiAuditScenes.cpp@9208dcf:562	GAME_PLAYING; Дом=HARKONNEN, миссия/регион 22; подготавливает базу и открывает список LIST_UPGRADES; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-build	src/debug/UiAuditScenes.cpp@9208dcf:563	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_CONSTYARD; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-infantry	src/debug/UiAuditScenes.cpp@9208dcf:564	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_FOOT_UNITS; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-vehicles	src/debug/UiAuditScenes.cpp@9208dcf:565	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_UNITS; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-starport	src/debug/UiAuditScenes.cpp@9208dcf:566	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_STARPORT; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-palace	src/debug/UiAuditScenes.cpp@9208dcf:567	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_PALACE; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
game-ordos-list-upgrades	src/debug/UiAuditScenes.cpp@9208dcf:568	GAME_PLAYING; Дом=ORDOS, миссия/регион 22; подготавливает базу и открывает список LIST_UPGRADES; файл карты явно не задаёт; клавиши и щелчки не генерируются. Код действий: src/debug/UiAuditScenes.cpp@9208dcf:313; src/debug/UiAuditAccess.cpp@9208dcf:765; src/debug/UiAuditAccess.cpp@9208dcf:780.	cDrawManager	есть: src/managers/cDrawManager.h@7eb119b:57	П5г
```

## Таблица инструментов и тестов

Источник: `.tmp/p5dr/tools.tsv`.

```tsv
путь	строк	назначение	функции	читает и пишет	как вызывается	есть в PORT
tests/UiAuditArgumentsTests.cpp@9208dcf:1	103	нет описания	—	файловые операции в файле не обнаружены	CTest: 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:446:        tests/UiAuditArgumentsTests.cpp; workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tests/ui_audit_main_menu_png.py@9208dcf:8	63	# noqa: E402	main	"tests/ui_audit_main_menu_png.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parent)); tests/ui_audit_main_menu_png.py@9208dcf:41: records = [json.loads(line) for line in log.read_text(encoding=""utf-8"").splitlines()]"	CTest: 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:471:                ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_main_menu_png.py; workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tests/ui_audit_runtime_support.py@9208dcf:1	104	нет описания	apply_settings,make_runtime,run_game,png_size,read_catalog	"tests/ui_audit_runtime_support.py@9208dcf:32: runtime = Path(directory) / ""runtime""; tests/ui_audit_runtime_support.py@9208dcf:33: runtime.mkdir(); tests/ui_audit_runtime_support.py@9208dcf:34: shutil.copy2(executable, runtime / ""d2tm""); tests/ui_audit_runtime_support.py@9208dcf:35: bin_dir = Path(resources) / ""bin""; tests/ui_audit_runtime_support.py@9208dcf:38: shutil.copy2(Path(resources) / ""game.ini"", runtime / ""game.ini""); tests/ui_audit_runtime_support.py@9208dcf:39: settings = (bin_dir / ""settings.ini"").read_text(encoding=""utf-8""); tests/ui_audit_runtime_support.py@9208dcf:40: (runtime / ""settings.ini"").write_text(apply_settings(settings, SETTINGS), encoding=""utf-8""); tests/ui_audit_runtime_support.py@9208dcf:58: return subprocess.run(; tests/ui_audit_runtime_support.py@9208dcf:74: self.out = Path(self.directory.name) / ""out""; tests/ui_audit_runtime_support.py@9208dcf:75: self.out.mkdir(); tests/ui_audit_runtime_support.py@9208dcf:93: data = Path(path).read_bytes(); tests/ui_audit_runtime_support.py@9208dcf:102: catalog = json.loads(stdout)"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tests/ui_audit_main_menu_png.py@9208dcf:8, tests/ui_audit_unknown_scene.py@9208dcf:7	нет
tests/ui_audit_unknown_scene.py@9208dcf:7	48	# noqa: E402	main	"tests/ui_audit_unknown_scene.py@9208dcf:5: sys.path.insert(0, str(Path(__file__).resolve().parent)); tests/ui_audit_unknown_scene.py@9208dcf:40: leftovers = sorted(path.name for path in game.out.rglob(""*"") if path.is_file())"	CTest: 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:463:                ${CMAKE_CURRENT_SOURCE_DIR}/tests/ui_audit_unknown_scene.py; workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/build_sheets.py@9208dcf:1	261	#!/usr/bin/env python3	load_font,chunks,scale_text,caption_lines,combo_of_path,find_pngs,scaled_rect,render_cell,make_sheet,build_catalog_sheets,canvas_factor,flag_rects,flag_text,unique_flags,display_flags,build_flag_sheets,build_index,main	"tools/ui-audit/build_sheets.py@9208dcf:11: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/build_sheets.py@9208dcf:30: if Path(path).exists():; tools/ui-audit/build_sheets.py@9208dcf:54: parts = Path(os.path.relpath(path, png_root)).parts; tools/ui-audit/build_sheets.py@9208dcf:55: return combos.parse_id(""/"".join(parts[:-1])), Path(parts[-1]).stem; tools/ui-audit/build_sheets.py@9208dcf:59: return sorted(Path(png_root).rglob(""*.png"")); tools/ui-audit/build_sheets.py@9208dcf:68: image = Image.open(png_path).convert(""RGB""); tools/ui-audit/build_sheets.py@9208dcf:89: Path(path).parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/build_sheets.py@9208dcf:90: sheet.save(path, ""JPEG"", quality=85); tools/ui-audit/build_sheets.py@9208dcf:95: directory = Path(png_root) / combo_id; tools/ui-audit/build_sheets.py@9208dcf:96: by_scene = {path.stem: path for path in directory.glob(""*.png"")}; tools/ui-audit/build_sheets.py@9208dcf:102: path = Path(out_dir) / combo_id.replace(""/"", ""_"") / f""{number:03d}.jpg""; tools/ui-audit/build_sheets.py@9208dcf:109: log = Path(logs_root) / combo_id / f""{scene}.geometry.jsonl""; tools/ui-audit/build_sheets.py@9208dcf:112: header = json.loads(log.read_text(encoding=""utf-8"").splitlines()[0]); tools/ui-audit/build_sheets.py@9208dcf:113: return Image.open(png_path).width / header[""canvas""][""w""]; tools/ui-audit/build_sheets.py@9208dcf:150: if (Path(png_root) / flag[""combo""] / f""{flag['scene']}.png"").exists():; tools/ui-audit/build_sheets.py@9208dcf:167: png = Path(png_root) / flag[""combo""] / f""{flag['scene']}.png""; tools/ui-audit/build_sheets.py@9208dcf:180: path = Path(out_dir) / f""rule{rule}-{number:03d}.jpg""; tools/ui-audit/build_sheets.py@9208dcf:208: base = Path(index_path).parent; tools/ui-audit/build_sheets.py@9208dcf:223: f'{html.escape(Path(path).parent.name + ""/"" + Path(path).name)}</a> ' for path in sheets); tools/ui-audit/build_sheets.py@9208dcf:230: Path(index_path).write_text(page, encoding=""utf-8""); tools/ui-audit/build_sheets.py@9208dcf:244: meta = {scene[""id""]: scene for scene in json.loads(Path(args.catalog).read_text(encoding=""utf-8""))[""scenes""]}; tools/ui-audit/build_sheets.py@9208dcf:245: flags = json.loads(Path(args.flags).read_text(encoding=""utf-8"")) if args.flags else []; tools/ui-audit/build_sheets.py@9208dcf:246: out = Path(args.out); tools/ui-audit/build_sheets.py@9208dcf:250: order = json.loads(Path(args.order).read_text(encoding=""utf-8"")) if args.order else None"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_build_sheets.py@9208dcf:11, tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:11	нет
tools/ui-audit/check_completeness.py@9208dcf:1	73	нет описания	all_combos,check,check_combinations,main	"tools/ui-audit/check_completeness.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/check_completeness.py@9208dcf:23: root = Path(root); tools/ui-audit/check_completeness.py@9208dcf:39: for path in sorted(png_dir.glob(""*.png"")):; tools/ui-audit/check_completeness.py@9208dcf:57: scenes = json.loads(Path(args.catalog).read_text(encoding=""utf-8""))[""scenes""]; tools/ui-audit/check_completeness.py@9208dcf:58: flags = json.loads(Path(args.flags).read_text(encoding=""utf-8"")) if args.flags else []; tools/ui-audit/check_completeness.py@9208dcf:61: order = json.loads(Path(args.order).read_text(encoding=""utf-8"")); tools/ui-audit/check_completeness.py@9208dcf:62: problems = check_combinations(Path(args.root), scenes, flagged, [combos.parse_id(i) for i in order],; tools/ui-audit/check_completeness.py@9208dcf:65: problems = check(Path(args.root), scenes, flagged, all_combos())"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_completeness.py@9208dcf:8, tools/ui-audit/tests/test_combos.py@9208dcf:9, tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:12	нет
tools/ui-audit/check_credits.py@9208dcf:1	53	нет описания	load,line_covered,check_credits,main	"tools/ui-audit/check_credits.py@9208dcf:9: records = [json.loads(line) for line in Path(path).read_text(encoding=""utf-8"").splitlines() if line.strip()]; tools/ui-audit/check_credits.py@9208dcf:24: for path in sorted(Path(logs_root).rglob(""credits-*.geometry.jsonl"")):"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_credits.py@9208dcf:6	нет
tools/ui-audit/check_geometry.py@9208dcf:1	251	нет описания	rect_of,intersects,contains,has_area,combo_of,name_of,make_flag,check_records,check_extra_records,summarize_rule8,load_log,check_log,content_key,compare_resolutions,format_flag,check_tree,main	"tools/ui-audit/check_geometry.py@9208dcf:162: lines = [json.loads(line) for line in Path(path).read_text(encoding=""utf-8"").splitlines() if line.strip()]; tools/ui-audit/check_geometry.py@9208dcf:214: for path in sorted(Path(logs_root).rglob(""*.geometry.jsonl"")):; tools/ui-audit/check_geometry.py@9208dcf:234: Path(args.txt_out).write_text("""".join(line + ""\n"" for line in lines), encoding=""utf-8""); tools/ui-audit/check_geometry.py@9208dcf:239: Path(args.json_out).write_text(json.dumps(flags, ensure_ascii=False, indent=1), encoding=""utf-8""); tools/ui-audit/check_geometry.py@9208dcf:241: summary_logs = [load_log(path) for path in sorted(Path(args.logs_root).rglob(""*.geometry.jsonl""))]; tools/ui-audit/check_geometry.py@9208dcf:242: Path(args.summary8_out).write_text("	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/build_sheets.py@9208dcf:239, tools/ui-audit/check_completeness.py@9208dcf:54, tools/ui-audit/check_options_geometry.py@9208dcf:9, tools/ui-audit/check_scenes.py@9208dcf:7, tools/ui-audit/finalize_png.py@9208dcf:33, tools/ui-audit/run_combo.py@9208dcf:13, tools/ui-audit/tests/test_check_geometry.py@9208dcf:9, tools/ui-audit/tests/test_extra_rules.py@9208dcf:9	нет
tools/ui-audit/check_keys.py@9208dcf:1	126	нет описания	load_tsv,normalize,is_binding_marker,states_of,is_handled,conflicts,rebindable_from_rows,rebinding_flags,format_flag,freshness,main	"tools/ui-audit/check_keys.py@9208dcf:13: with open(path, encoding=""utf-8"", newline="""") as handle:; tools/ui-audit/check_keys.py@9208dcf:120: Path(args.out).write_text(""\n"".join(lines) + (""\n"" if lines else """"), encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_keys.py@9208dcf:8	нет
tools/ui-audit/check_options_geometry.py@9208dcf:1	120	#!/usr/bin/env python3	is_gui,is_button,is_window,check_rule3,check_log,planned_pairs,check_tree,main	"tools/ui-audit/check_options_geometry.py@9208dcf:8: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/check_options_geometry.py@9208dcf:65: combos = [line.strip() for line in Path(combos_path).read_text(encoding=""utf-8"").splitlines(); tools/ui-audit/check_options_geometry.py@9208dcf:68: entries = json.loads(Path(plan_path).read_text(encoding=""utf-8"")); tools/ui-audit/check_options_geometry.py@9208dcf:83: for path in sorted(Path(logs_root).rglob(""*.geometry.jsonl"")):"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:11	нет
tools/ui-audit/check_scenes.py@9208dcf:1	132	нет описания	at_top,at_right,at_bottom,objects_of,edges_reason,text_inside_group,check_units,check_structures,check_scene,format_line,check_file,main	"tools/ui-audit/check_scenes.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/check_scenes.py@9208dcf:118: for path in sorted(Path(root).rglob(""*.geometry.jsonl"")):; tools/ui-audit/check_scenes.py@9208dcf:125: Path(args.out).write_text(""\n"".join(lines) + ""\n"", encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_scenes.py@9208dcf:9	нет
tools/ui-audit/check_screens.py@9208dcf:1	86	нет описания	code_states,code_classes,load_exclusions,check_screens,collect_code_names,main	"tools/ui-audit/check_screens.py@9208dcf:58: root = Path(root); tools/ui-audit/check_screens.py@9208dcf:59: states = code_states((root / ""src/include/definitions.h"").read_text(encoding=""utf-8"", errors=""replace"")); tools/ui-audit/check_screens.py@9208dcf:62: for path in sorted((root / directory).glob(""*.h"")) + sorted((root / directory).glob(""*.hpp"")):; tools/ui-audit/check_screens.py@9208dcf:63: sources.append(path.read_text(encoding=""utf-8"", errors=""replace"")); tools/ui-audit/check_screens.py@9208dcf:65: dialog_classes = [name for name in code_classes([dialog.read_text(encoding=""utf-8"", errors=""replace"")]); tools/ui-audit/check_screens.py@9208dcf:76: scenes = json.loads(Path(args.catalog).read_text(encoding=""utf-8""))[""scenes""]; tools/ui-audit/check_screens.py@9208dcf:77: exclusions, problems = load_exclusions(Path(args.exclusions).read_text(encoding=""utf-8""))"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_check_screens.py@9208dcf:7	нет
tools/ui-audit/combos.py@9208dcf:1	100	нет описания	parse_scales,generate,_combo,combo_id,legacy_combo,parse_id,scenes_for,resolution_of,flag_key,earlier_ids,first_combo_by_key,png_required,keep_png	tools/ui-audit/combos.py@9208dcf:10: data = json.loads(text)	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/build_sheets.py@9208dcf:12, tools/ui-audit/check_completeness.py@9208dcf:7, tools/ui-audit/finalize_png.py@9208dcf:10, tools/ui-audit/run_all.py@9208dcf:12, tools/ui-audit/run_combo.py@9208dcf:14, tools/ui-audit/tests/test_build_sheets.py@9208dcf:12, tools/ui-audit/tests/test_combos.py@9208dcf:10, tools/ui-audit/tests/test_png_policy.py@9208dcf:9, tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:13, tools/ui-audit/tests/test_run_all.py@9208dcf:8	нет
tools/ui-audit/exclusions.tsv@9208dcf:1	10	нет описания	—	файловые операции в файле не обнаружены	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/extract_keys.py@9208dcf:1	92	нет описания	strip_comments,definition_name,extract,to_tsv,extract_tree,main	"tools/ui-audit/extract_keys.py@9208dcf:69: root = Path(root); tools/ui-audit/extract_keys.py@9208dcf:71: for path in sorted((root / ""src"").rglob(""*"")):; tools/ui-audit/extract_keys.py@9208dcf:74: rows += extract(path.read_text(encoding=""utf-8"", errors=""replace""), relative); tools/ui-audit/extract_keys.py@9208dcf:84: Path(args.out).parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/extract_keys.py@9208dcf:85: with open(args.out, ""w"", encoding=""utf-8"", newline="""") as handle:; tools/ui-audit/extract_keys.py@9208dcf:86: handle.write(to_tsv(rows))"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_extract_keys.py@9208dcf:7	нет
tools/ui-audit/finalize_png.py@9208dcf:1	59	#!/usr/bin/env python3	plan_actions,main	"tools/ui-audit/finalize_png.py@9208dcf:9: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/finalize_png.py@9208dcf:19: png_dir = Path(out_root) / ""png"" / identifier; tools/ui-audit/finalize_png.py@9208dcf:20: have = {path.stem for path in png_dir.glob(""*.png"")} if png_dir.is_dir() else set(); tools/ui-audit/finalize_png.py@9208dcf:36: out = Path(args.out); tools/ui-audit/finalize_png.py@9208dcf:37: order = json.loads((out / ""order.json"").read_text(encoding=""utf-8"")); tools/ui-audit/finalize_png.py@9208dcf:38: flags = json.loads(Path(args.flags).read_text(encoding=""utf-8"")); tools/ui-audit/finalize_png.py@9208dcf:44: (out / ""png"" / identifier / f""{scene}.png"").unlink(); tools/ui-audit/finalize_png.py@9208dcf:50: command = [sys.executable, str(Path(__file__).resolve().parent / ""run_combo.py""), ""--exe"", args.exe,; tools/ui-audit/finalize_png.py@9208dcf:54: code = max(code, subprocess.run(command, check=False).returncode)"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_png_policy.py@9208dcf:10	нет
tools/ui-audit/find_hit_tests.py@9208dcf:1	58	нет описания	enclosing_functions,scan_text,scan,main	"tools/ui-audit/find_hit_tests.py@9208dcf:36: root = Path(root); tools/ui-audit/find_hit_tests.py@9208dcf:39: for path in sorted((root / directory).rglob(""*.cpp"")):; tools/ui-audit/find_hit_tests.py@9208dcf:40: rows, records = scan_text(path.read_text(encoding=""utf-8"", errors=""replace""))"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:8	нет
tools/ui-audit/keys.tsv@9208dcf:1	169	нет описания	—	файловые операции в файле не обнаружены	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/check_keys.py@9208dcf:98, tools/ui-audit/tests/test_check_keys.py@9208dcf:166	нет
tools/ui-audit/run_all.py@9208dcf:1	152	#!/usr/bin/env python3	scales_for,interleave,plan,audit_log_plan,done_marker,combo_bytes,forecast_gb,run_one,main	"tools/ui-audit/run_all.py@9208dcf:11: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/run_all.py@9208dcf:22: result = subprocess.run([str(executable), ""--ui-audit-scales"", resolution], env=run_combo.game_environment(),; tools/ui-audit/run_all.py@9208dcf:54: return Path(out_root) / ""done"" / combos.combo_id(combo).replace(""/"", ""_""); tools/ui-audit/run_all.py@9208dcf:61: directory = Path(out_root) / kind / identifier; tools/ui-audit/run_all.py@9208dcf:76: journal.write(f""{time.strftime('%F %T')} free {free:.1f} GB before {identifier}\n""); tools/ui-audit/run_all.py@9208dcf:80: log_path = Path(args.out) / ""run"" / (identifier.replace(""/"", ""_"") + "".txt""); tools/ui-audit/run_all.py@9208dcf:81: log_path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/run_all.py@9208dcf:82: command = [sys.executable, str(Path(__file__).resolve().parent / ""run_combo.py""), ""--exe"", args.exe,; tools/ui-audit/run_all.py@9208dcf:85: with open(log_path, ""w"", encoding=""utf-8"") as log:; tools/ui-audit/run_all.py@9208dcf:86: code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False).returncode; tools/ui-audit/run_all.py@9208dcf:89: marker.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/run_all.py@9208dcf:90: marker.write_text(""ok\n"", encoding=""utf-8""); tools/ui-audit/run_all.py@9208dcf:107: args.exe = str(Path(args.exe).resolve()); tools/ui-audit/run_all.py@9208dcf:108: args.resources = str(Path(args.resources).resolve()); tools/ui-audit/run_all.py@9208dcf:109: args.out = str(Path(args.out).resolve()); tools/ui-audit/run_all.py@9208dcf:110: Path(args.out).mkdir(parents=True, exist_ok=True); tools/ui-audit/run_all.py@9208dcf:119: (Path(args.out) / ""order.json"").write_text(json.dumps([combos.combo_id(c) for c in generated]), encoding=""utf-8""); tools/ui-audit/run_all.py@9208dcf:120: scenes = json.loads(Path(args.catalog).read_text(encoding=""utf-8""))[""scenes""]; tools/ui-audit/run_all.py@9208dcf:122: (Path(args.out) / ""audit-plan.json"").write_text(; tools/ui-audit/run_all.py@9208dcf:130: with open(Path(args.out) / ""free-space.txt"", ""a"", encoding=""utf-8"") as journal:"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/build_sheets.py@9208dcf:241, tools/ui-audit/check_completeness.py@9208dcf:55, tools/ui-audit/check_options_geometry.py@9208dcf:101, tools/ui-audit/tests/test_run_all.py@9208dcf:9	нет
tools/ui-audit/run_combo.py@9208dcf:1	184	#!/usr/bin/env python3	free_gb,apply_settings,split_resolution,make_runtime,game_environment,run_scene,list_scenes,load_order,has_new_flag,run_combo,main	"tools/ui-audit/run_combo.py@9208dcf:12: sys.path.insert(0, str(Path(__file__).resolve().parent)); tools/ui-audit/run_combo.py@9208dcf:46: runtime = Path(directory); tools/ui-audit/run_combo.py@9208dcf:49: runtime.mkdir(parents=True); tools/ui-audit/run_combo.py@9208dcf:50: shutil.copy2(executable, runtime / ""d2tm""); tools/ui-audit/run_combo.py@9208dcf:51: bin_dir = Path(resources) / ""bin""; tools/ui-audit/run_combo.py@9208dcf:54: shutil.copy2(Path(resources) / ""game.ini"", runtime / ""game.ini""); tools/ui-audit/run_combo.py@9208dcf:55: settings = apply_settings((bin_dir / ""settings.ini"").read_text(encoding=""utf-8""), {; tools/ui-audit/run_combo.py@9208dcf:63: (runtime / ""settings.ini"").write_text(settings, encoding=""utf-8""); tools/ui-audit/run_combo.py@9208dcf:79: return subprocess.run(command, cwd=runtime, env=game_environment(), check=False,; tools/ui-audit/run_combo.py@9208dcf:84: result = subprocess.run([str(executable), ""--ui-audit-list""], env=game_environment(), check=True,; tools/ui-audit/run_combo.py@9208dcf:86: return json.loads(result.stdout)[""scenes""]; tools/ui-audit/run_combo.py@9208dcf:90: path = Path(out_root) / ""order.json""; tools/ui-audit/run_combo.py@9208dcf:91: return json.loads(path.read_text(encoding=""utf-8"")) if path.is_file() else []; tools/ui-audit/run_combo.py@9208dcf:101: earlier_log = Path(out_root) / ""logs"" / earlier / f""{scene_id}.geometry.jsonl""; tools/ui-audit/run_combo.py@9208dcf:109: out_root = Path(out_root); tools/ui-audit/run_combo.py@9208dcf:113: png_dir.mkdir(parents=True, exist_ok=True); tools/ui-audit/run_combo.py@9208dcf:114: log_dir.mkdir(parents=True, exist_ok=True); tools/ui-audit/run_combo.py@9208dcf:115: work = Path(work_root or out_root / ""work"") / identifier.replace(""/"", ""_""); tools/ui-audit/run_combo.py@9208dcf:124: scene_out.mkdir(parents=True); tools/ui-audit/run_combo.py@9208dcf:146: (png_dir / png.name).unlink(); tools/ui-audit/run_combo.py@9208dcf:162: args.exe = str(Path(args.exe).resolve()); tools/ui-audit/run_combo.py@9208dcf:163: args.resources = str(Path(args.resources).resolve()); tools/ui-audit/run_combo.py@9208dcf:164: args.out = str(Path(args.out).resolve()); tools/ui-audit/run_combo.py@9208dcf:165: Path(args.out).mkdir(parents=True, exist_ok=True); tools/ui-audit/run_combo.py@9208dcf:174: flagged = {f[""scene""] for f in json.loads(Path(args.flags).read_text(encoding=""utf-8""))"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: tools/ui-audit/finalize_png.py@9208dcf:50, tools/ui-audit/run_all.py@9208dcf:13, tools/ui-audit/run_all.py@9208dcf:82, tools/ui-audit/tests/test_png_policy.py@9208dcf:11	нет
tools/ui-audit/tests/test_build_sheets.py@9208dcf:11	117	# noqa: E402	make_png,make_log	"tools/ui-audit/tests/test_build_sheets.py@9208dcf:9: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_build_sheets.py@9208dcf:19: path = Path(root) / ""png"" / combo_id / f""{scene}.png""; tools/ui-audit/tests/test_build_sheets.py@9208dcf:20: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_build_sheets.py@9208dcf:21: Image.new(""RGB"", size, color).save(path); tools/ui-audit/tests/test_build_sheets.py@9208dcf:26: path = Path(root) / ""logs"" / combo_id / f""{scene}.geometry.jsonl""; tools/ui-audit/tests/test_build_sheets.py@9208dcf:27: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_build_sheets.py@9208dcf:28: path.write_text(json.dumps({""k"": ""header"", ""canvas"": {""w"": width, ""h"": 100}}) + ""\n"", encoding=""utf-8""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:60: written = build_sheets.build_catalog_sheets(Path(root) / ""png"", META, ""1024x768/ru/hd"", Path(root) / ""out""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:62: width, height = Image.open(written[0]).size; tools/ui-audit/tests/test_build_sheets.py@9208dcf:69: written = build_sheets.build_catalog_sheets(Path(root) / ""png"", META, ""1024x768/ru/hd"", Path(root) / ""out""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:78: self.assertEqual(build_sheets.canvas_factor(png, Path(root) / ""logs"", ""1024x768/ru/hd"", ""s1""), 2.0); tools/ui-audit/tests/test_build_sheets.py@9208dcf:80: Path(root) / ""png"", Path(root) / ""logs"", META, [flag], Path(root) / ""out""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:82: reddish = any(r > 180 and g < 80 and b < 80 for r, g, b in Image.open(written[0]).getdata()); tools/ui-audit/tests/test_build_sheets.py@9208dcf:89: Path(root) / ""png"", Path(root) / ""logs"", META, [flag], Path(root) / ""out""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:98: index = Path(root) / ""out"" / ""index.html""; tools/ui-audit/tests/test_build_sheets.py@9208dcf:99: index.parent.mkdir(); tools/ui-audit/tests/test_build_sheets.py@9208dcf:100: rows = build_sheets.build_index(Path(root) / ""png"", META, [], [], index); tools/ui-audit/tests/test_build_sheets.py@9208dcf:101: text = index.read_text(encoding=""utf-8""); tools/ui-audit/tests/test_build_sheets.py@9208dcf:111: index = Path(root) / ""index.html""; tools/ui-audit/tests/test_build_sheets.py@9208dcf:112: build_sheets.build_index(Path(root) / ""png"", META, [flag], [], index); tools/ui-audit/tests/test_build_sheets.py@9208dcf:113: self.assertIn(""<td>1</td></tr>"", index.read_text(encoding=""utf-8""))"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_completeness.py@9208dcf:8	139	# noqa: E402	png_path,log_path,expected_pngs,build_tree,touch,run_check	"tools/ui-audit/tests/test_check_completeness.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_check_completeness.py@9208dcf:53: path = Path(root) / relative; tools/ui-audit/tests/test_check_completeness.py@9208dcf:54: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_check_completeness.py@9208dcf:55: path.write_bytes(b""""); tools/ui-audit/tests/test_check_completeness.py@9208dcf:59: return sorted(check_completeness.check(Path(root), scenes, flagged, combos)); tools/ui-audit/tests/test_check_completeness.py@9208dcf:65: self.root = Path(self.directory.name); tools/ui-audit/tests/test_check_completeness.py@9208dcf:76: (self.root / relative).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:81: (self.root / relative).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:86: (self.root / relative).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:106: (self.root / relative).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:111: (self.root / relative).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:118: (self.root / missing_png).unlink(); tools/ui-audit/tests/test_check_completeness.py@9208dcf:119: (self.root / missing_log).unlink()"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_credits.py@9208dcf:1	53	нет описания	write_log	"tools/ui-audit/tests/test_check_credits.py@9208dcf:10: directory = Path(root) / ""logs"" / resolution / ""ru"" / ""hd""; tools/ui-audit/tests/test_check_credits.py@9208dcf:11: directory.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_check_credits.py@9208dcf:17: (directory / f""{scene}.geometry.jsonl"").write_text(""\n"".join(json.dumps(r) for r in records) + ""\n"","	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_geometry.py@9208dcf:9	326	# noqa: E402	header,text,gui,area,rect,rules,check	"tools/ui-audit/tests/test_check_geometry.py@9208dcf:7: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_check_geometry.py@9208dcf:299: path = Path(directory) / ""scene.geometry.jsonl""; tools/ui-audit/tests/test_check_geometry.py@9208dcf:301: path.write_text("""".join(json.dumps(line) + ""\n"" for line in lines), encoding=""utf-8""); tools/ui-audit/tests/test_check_geometry.py@9208dcf:319: path = Path(directory) / ""scene.geometry.jsonl""; tools/ui-audit/tests/test_check_geometry.py@9208dcf:320: path.write_text(json.dumps(text(""Back"", 10, 10, 40, 12)) + ""\n"", encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_keys.py@9208dcf:8	173	# noqa: E402	row,raw	"tools/ui-audit/tests/test_check_keys.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_check_keys.py@9208dcf:166: path = Path(directory) / ""keys.tsv""; tools/ui-audit/tests/test_check_keys.py@9208dcf:167: path.write_text(""file\tfunction\tkey\tline\nsrc/a.cpp\tA::f\tSDLK_A\t12\n"", encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:11	137	# noqa: E402	header,gui,click	"tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:9: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:62: path = Path(root) / f""{scene}-{combo.replace('/', '_')}.geometry.jsonl""; tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:63: path.write_text("""".join(json.dumps(row) + ""\n"" for row in [head] + records), encoding=""utf-8""); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:72: next(Path(directory).glob(""*.geometry.jsonl""))); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:77: root = Path(directory); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:79: combos.write_text(""1024x768/ru/hd\n"", encoding=""utf-8""); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:94: root = Path(directory); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:96: combos.write_text(""1024x768/ru/hd\n1280x720/en/hd\n"", encoding=""utf-8""); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:112: path = Path(directory) / ""audit-plan.json""; tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:113: path.write_text(json.dumps([; tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:122: root = Path(directory); tools/ui-audit/tests/test_check_options_geometry.py@9208dcf:124: combos.write_text(""1024x768/ru/hd\n"", encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_scenes.py@9208dcf:9	166	# noqa: E402	header,label,text,unit_records,scene_of	"tools/ui-audit/tests/test_check_scenes.py@9208dcf:7: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_check_scenes.py@9208dcf:151: path = Path(directory) / ""units-label-trike.geometry.jsonl""; tools/ui-audit/tests/test_check_scenes.py@9208dcf:153: path.write_text("""".join(json.dumps(line) + ""\n"" for line in lines), encoding=""utf-8""); tools/ui-audit/tests/test_check_scenes.py@9208dcf:160: path = Path(directory) / ""main-menu.geometry.jsonl""; tools/ui-audit/tests/test_check_scenes.py@9208dcf:161: path.write_text(json.dumps(header(""main-menu"")) + ""\n"", encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_check_screens.py@9208dcf:7	97	# noqa: E402	—	tools/ui-audit/tests/test_check_screens.py@9208dcf:5: sys.path.insert(0, str(Path(__file__).resolve().parents[1]))	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_combos.py@9208dcf:9	170	# noqa: E402	find	"tools/ui-audit/tests/test_combos.py@9208dcf:7: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_combos.py@9208dcf:132: def write(self, root, relative):; tools/ui-audit/tests/test_combos.py@9208dcf:133: path = Path(root) / relative; tools/ui-audit/tests/test_combos.py@9208dcf:134: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_combos.py@9208dcf:135: path.write_bytes(b""x""); tools/ui-audit/tests/test_combos.py@9208dcf:142: self.write(root, f""logs/{combo_id}/{scene['id']}.geometry.jsonl""); tools/ui-audit/tests/test_combos.py@9208dcf:143: self.write(root, f""png/{combo_id}/main-menu.png""); tools/ui-audit/tests/test_combos.py@9208dcf:152: self.write(root, f""logs/{combo_id}/main-menu.geometry.jsonl""); tools/ui-audit/tests/test_combos.py@9208dcf:163: self.write(root, f""logs/{combo_id}/{scene['id']}.geometry.jsonl""); tools/ui-audit/tests/test_combos.py@9208dcf:164: self.write(root, f""png/{combo_id}/game-screen.png"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_extra_rules.py@9208dcf:9	203	# noqa: E402	header,text,gui,area,label,click,rules,extra	"tools/ui-audit/tests/test_extra_rules.py@9208dcf:7: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_extra_rules.py@9208dcf:193: path = Path(directory) / f""{name}.geometry.jsonl""; tools/ui-audit/tests/test_extra_rules.py@9208dcf:194: path.write_text("""".join(json.dumps(line) + ""\n"" for line in lines), encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_extract_keys.py@9208dcf:7	74	# noqa: E402	—	tools/ui-audit/tests/test_extract_keys.py@9208dcf:5: sys.path.insert(0, str(Path(__file__).resolve().parents[1]))	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:8	70	# noqa: E402	—	"tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:62: path = Path(root) / directory; tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:63: path.mkdir(parents=True); tools/ui-audit/tests/test_find_hit_tests.py@9208dcf:64: (path / ""a.cpp"").write_text(SOURCE, encoding=""utf-8"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_png_policy.py@9208dcf:9	93	# noqa: E402	header,area,write_log,flagged,flag	"tools/ui-audit/tests/test_png_policy.py@9208dcf:7: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_png_policy.py@9208dcf:34: path = Path(root) / ""logs"" / identifier / f""{scene}.geometry.jsonl""; tools/ui-audit/tests/test_png_policy.py@9208dcf:35: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_png_policy.py@9208dcf:36: path.write_text(""\n"".join(json.dumps(r) for r in [header(identifier, scene)] + records) + ""\n"", encoding=""utf-8""); tools/ui-audit/tests/test_png_policy.py@9208dcf:41: path = Path(root) / ""logs"" / identifier / f""{scene}.geometry.jsonl""; tools/ui-audit/tests/test_png_policy.py@9208dcf:84: path = Path(root) / ""png"" / identifier / f""{scene}.png""; tools/ui-audit/tests/test_png_policy.py@9208dcf:85: path.parent.mkdir(parents=True); tools/ui-audit/tests/test_png_policy.py@9208dcf:86: path.write_bytes(b""x"")"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:11	97	# noqa: E402	touch,flag	"tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:9: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:23: path = Path(root) / relative; tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:24: path.parent.mkdir(parents=True, exist_ok=True); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:25: path.write_bytes(data); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:65: png_root = Path(root) / ""png""; tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:74: png_root = Path(root) / ""png""; tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:84: png_root = Path(root) / ""png""; tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:86: png.parent.mkdir(parents=True); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:87: Image.new(""RGB"", (320, 240)).save(png); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:88: logs = Path(root) / ""logs"" / LEGACY / ""s.geometry.jsonl""; tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:89: logs.parent.mkdir(parents=True); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:90: logs.write_text(json.dumps({""k"": ""header"", ""canvas"": {""w"": 320, ""h"": 240}}) + ""\n"", encoding=""utf-8""); tools/ui-audit/tests/test_png_policy_outputs.py@9208dcf:92: png_root, Path(root) / ""logs"", {""s"": {""id"": ""s""}}, flags, Path(root) / ""out"", ORDER)"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
tools/ui-audit/tests/test_run_all.py@9208dcf:8	70	# noqa: E402	—	"tools/ui-audit/tests/test_run_all.py@9208dcf:6: sys.path.insert(0, str(Path(__file__).resolve().parents[1])); tools/ui-audit/tests/test_run_all.py@9208dcf:59: directory = Path(root) / kind / ""1024x768"" / ""ru"" / ""hd""; tools/ui-audit/tests/test_run_all.py@9208dcf:60: directory.mkdir(parents=True); tools/ui-audit/tests/test_run_all.py@9208dcf:61: (directory / ""a"").write_bytes(b""x"" * size)"	CTest: пустой вывод (exit 1); workflow: пустой вывод (exit 1); ссылка/импорт из списка: не найдено	нет
```

### Список сцен: команда и вывод

```text
363:    scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
364:    scene("region-atreides-intro-1", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<1>),
365:    scene("region-atreides-intro-2", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<2>),
366:    scene("region-atreides-intro-3", "region", "atreides", "RegionIntroScene", prepareRegion<ATREIDES, 1, false>, readyRegionIntro<3>),
367:    scene("region-atreides-conquer-3", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 3, true>, readyRegionConquer, 1),
368:    scene("region-atreides-conquer-5", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 5, true>, readyRegionConquer, 1),
369:    scene("region-atreides-conquer-7", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 7, true>, readyRegionConquer, 1),
370:    scene("region-atreides-conquer-9", "region", "atreides", "RegionConquerMessage", prepareRegion<ATREIDES, 9, true>, readyRegionConquer, 1),
371:    scene("region-atreides-select-2", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 2, true>, readyRegionSelect),
372:    scene("region-atreides-select-3", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 3, true>, readyRegionSelect),
373:    scene("region-atreides-select-4", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 4, true>, readyRegionSelect),
374:    scene("region-atreides-select-5", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 5, true>, readyRegionSelect),
375:    scene("region-atreides-select-6", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 6, true>, readyRegionSelect),
376:    scene("region-atreides-select-7", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 7, true>, readyRegionSelect),
377:    scene("region-atreides-select-8", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 8, true>, readyRegionSelect),
378:    scene("region-atreides-select-9", "region", "atreides", "RegionStateSelect", prepareRegion<ATREIDES, 9, true>, readyRegionSelect),
379:    scene("region-harkonnen-intro-1", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<1>),
380:    scene("region-harkonnen-intro-2", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<2>),
381:    scene("region-harkonnen-intro-3", "region", "harkonnen", "RegionIntroScene", prepareRegion<HARKONNEN, 1, false>, readyRegionIntro<3>),
382:    scene("region-harkonnen-conquer-3", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 3, true>, readyRegionConquer, 1),
383:    scene("region-harkonnen-conquer-5", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 5, true>, readyRegionConquer, 1),
384:    scene("region-harkonnen-conquer-7", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 7, true>, readyRegionConquer, 1),
385:    scene("region-harkonnen-conquer-9", "region", "harkonnen", "RegionConquerMessage", prepareRegion<HARKONNEN, 9, true>, readyRegionConquer, 1),
386:    scene("region-harkonnen-select-2", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 2, true>, readyRegionSelect),
387:    scene("region-harkonnen-select-3", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 3, true>, readyRegionSelect),
388:    scene("region-harkonnen-select-4", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 4, true>, readyRegionSelect),
389:    scene("region-harkonnen-select-5", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 5, true>, readyRegionSelect),
390:    scene("region-harkonnen-select-6", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 6, true>, readyRegionSelect),
391:    scene("region-harkonnen-select-7", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 7, true>, readyRegionSelect),
392:    scene("region-harkonnen-select-8", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 8, true>, readyRegionSelect),
393:    scene("region-harkonnen-select-9", "region", "harkonnen", "RegionStateSelect", prepareRegion<HARKONNEN, 9, true>, readyRegionSelect),
394:    scene("region-ordos-intro-1", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<1>),
395:    scene("region-ordos-intro-2", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<2>),
396:    scene("region-ordos-intro-3", "region", "ordos", "RegionIntroScene", prepareRegion<ORDOS, 1, false>, readyRegionIntro<3>),
397:    scene("region-ordos-conquer-3", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 3, true>, readyRegionConquer, 1),
398:    scene("region-ordos-conquer-5", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 5, true>, readyRegionConquer, 1),
399:    scene("region-ordos-conquer-7", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 7, true>, readyRegionConquer, 1),
400:    scene("region-ordos-conquer-9", "region", "ordos", "RegionConquerMessage", prepareRegion<ORDOS, 9, true>, readyRegionConquer, 1),
401:    scene("region-ordos-select-2", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 2, true>, readyRegionSelect),
402:    scene("region-ordos-select-3", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 3, true>, readyRegionSelect),
403:    scene("region-ordos-select-4", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 4, true>, readyRegionSelect),
404:    scene("region-ordos-select-5", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 5, true>, readyRegionSelect),
405:    scene("region-ordos-select-6", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 6, true>, readyRegionSelect),
406:    scene("region-ordos-select-7", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 7, true>, readyRegionSelect),
407:    scene("region-ordos-select-8", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 8, true>, readyRegionSelect),
408:    scene("region-ordos-select-9", "region", "ordos", "RegionStateSelect", prepareRegion<ORDOS, 9, true>, readyRegionSelect),
409:    scene("choose-house", "choose-house", "", "StateSettled", prepareChooseHouse),
410:    scene("select-mission-atreides", "select-mission", "atreides", "StateSettled", prepareSelectMission<ATREIDES>),
411:    scene("select-mission-harkonnen", "select-mission", "harkonnen", "StateSettled",
413:    scene("select-mission-ordos", "select-mission", "ordos", "StateSettled", prepareSelectMission<ORDOS>),
414:    scene("tellhouse-atreides-speak", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, false>,
416:    scene("tellhouse-atreides-await", "tellhouse", "atreides", "MentatFrozen", prepareTellHouse<ATREIDES, true>,
418:    scene("tellhouse-harkonnen-speak", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, false>,
420:    scene("tellhouse-harkonnen-await", "tellhouse", "harkonnen", "MentatFrozen", prepareTellHouse<HARKONNEN, true>,
422:    scene("tellhouse-ordos-speak", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, false>,
424:    scene("tellhouse-ordos-await", "tellhouse", "ordos", "MentatFrozen", prepareTellHouse<ORDOS, true>,
426:    withScreen(scene("mentat-briefing-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>,
428:    withScreen(scene("mentat-briefing-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 0>,
430:    withScreen(scene("mentat-win-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>,
432:    withScreen(scene("mentat-win-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 1>,
434:    withScreen(scene("mentat-lose-atreides-speak", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>,
436:    withScreen(scene("mentat-lose-atreides-await", "mentat", "atreides", "MentatFrozen", prepareMentat<ATREIDES, 2>,
438:    withScreen(scene("mentat-briefing-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>,
440:    withScreen(scene("mentat-briefing-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 0>,
442:    withScreen(scene("mentat-win-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>,
444:    withScreen(scene("mentat-win-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 1>,
446:    withScreen(scene("mentat-lose-harkonnen-speak", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>,
448:    withScreen(scene("mentat-lose-harkonnen-await", "mentat", "harkonnen", "MentatFrozen", prepareMentat<HARKONNEN, 2>,
450:    withScreen(scene("mentat-briefing-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>,
452:    withScreen(scene("mentat-briefing-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 0>,
454:    withScreen(scene("mentat-win-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>,
456:    withScreen(scene("mentat-win-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 1>,
458:    withScreen(scene("mentat-lose-ordos-speak", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>,
460:    withScreen(scene("mentat-lose-ordos-await", "mentat", "ordos", "MentatFrozen", prepareMentat<ORDOS, 2>,
462:    scene("skirmish-setup-random", "skirmish-setup", "", "FixedFrames(2, no readiness flag)", prepareSkirmishSetup<0>),
463:    scene("skirmish-setup-ready-map", "skirmish-setup", "", "FixedFrames(2, no readiness flag)",
465:    withScreen(scene("outcome-win", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<true>,
467:    withScreen(scene("outcome-lose", "outcome", "atreides", "FixedFrames(8, no readiness flag)", prepareOutcome<false>,
469:    scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>,
471:    scene("options-menu-applied", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<1>,
473:    scene("options-menu-game", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<2>,
475:    scene("options-menu-controls", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<3>,
477:    scene("options-menu-diagnostics", "options-menu", "", "FixedFrames(14, no readiness flag)",
479:    scene("options-menu-keybind", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<5>,
481:    scene("main-menu-saves", "main-menu", "", "StateSettled", prepareMenuWithSaves),
482:    scene("save-dialog-menu", "save-dialog-menu", "", "FixedFrames(10, no readiness flag)", prepareMenuWithSaves,
484:    scene("options-game-main-saves", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
486:    scene("options-game-main-nosaves", "options-game", "", "FixedFrames(14, no readiness flag)",
488:    scene("options-game-applied", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
490:    scene("options-game-game", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
492:    scene("options-game-controls", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
494:    scene("options-game-diagnostics", "options-game", "", "FixedFrames(14, no readiness flag)",
496:    scene("options-game-keybind", "options-game", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
498:    scene("save-dialog-load", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
500:    scene("save-dialog-save-new", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
502:    scene("save-dialog-overwrite", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
504:    scene("save-dialog-load-error", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
506:    scene("save-dialog-save-error", "save-dialog", "", "FixedFrames(14, no readiness flag)", prepareGameOptions<true>,
508:    scene("credits-title", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<0>),
509:    scene("credits-1", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<1>),
510:    scene("credits-2", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<2>),
511:    scene("credits-3", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<3>),
512:    hdOnly(scene("credits-4", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<4>)),
513:    hdOnly(scene("credits-5", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<5>)),
514:    onGameScreen(scene("structure-label-top", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<0>,
516:    onGameScreen(scene("structure-label-right", "game-playing", "atreides", kFixedGameFrames, prepareStructureLabel<1>,
518:    onGameScreen(scene("units-label-trike", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TRIKE>), false),
519:    onGameScreen(scene("units-label-raider", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<RAIDER>), false),
520:    onGameScreen(scene("units-label-quad", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<QUAD>), false),
521:    onGameScreen(scene("units-label-tank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TANK>), false),
522:    onGameScreen(scene("units-label-siegetank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SIEGETANK>), false),
523:    onGameScreen(scene("units-label-launcher", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<LAUNCHER>), false),
524:    onGameScreen(scene("units-label-deviator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVIATOR>), false),
525:    onGameScreen(scene("units-label-sonictank", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SONICTANK>), false),
526:    onGameScreen(scene("units-label-devastator", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<DEVASTATOR>), false),
527:    onGameScreen(scene("units-label-harvester", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<HARVESTER>), false),
528:    onGameScreen(scene("units-label-mcv", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<MCV>), false),
529:    onGameScreen(scene("units-label-soldier", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SOLDIER>), false),
530:    onGameScreen(scene("units-label-infantry", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<INFANTRY>), false),
531:    onGameScreen(scene("units-label-trooper", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPER>), false),
532:    onGameScreen(scene("units-label-troopers", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<TROOPERS>), false),
533:    onGameScreen(scene("units-label-unit-fremen-one", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_ONE>), false),
534:    onGameScreen(scene("units-label-unit-fremen-three", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<UNIT_FREMEN_THREE>), false),
535:    onGameScreen(scene("units-label-saboteur", "game-playing", "atreides", kFixedGameFrames, prepareUnitLabels<SABOTEUR>), false),
536:    withHud(onGameScreen(scene("game-hud", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Hud>), false)),
537:    onGameScreen(scene("game-music", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Music>), false),
538:    onGameScreen(scene("game-command-damaged-unit", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::DamagedUnit>), false),
539:    onGameScreen(scene("game-command-harvester", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Harvester>), false),
540:    onGameScreen(scene("game-command-mcv", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Mcv>), false),
541:    onGameScreen(scene("game-structure-selected", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Structure>), false),
542:    onGameScreen(scene("game-list-build", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListBuild>), false),
543:    onGameScreen(scene("game-list-infantry", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListInfantry>), false),
544:    onGameScreen(scene("game-list-vehicles", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListVehicles>), false),
545:    onGameScreen(scene("game-list-starport", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListStarport>), false),
546:    onGameScreen(scene("game-list-palace", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListPalace>), false),
547:    onGameScreen(scene("game-list-upgrades", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ListUpgrades>), false),
548:    onGameScreen(scene("game-radar-none", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNone>), false),
549:    onGameScreen(scene("game-radar-nopower", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::RadarNoPower>), false),
550:    onGameScreen(scene("game-place-allowed", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceAllowed>), true),
551:    onGameScreen(scene("game-place-forbidden", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::PlaceForbidden>), true),
552:    onGameScreen(scene("game-group-select", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::GroupSelect>), true),
553:    onGameScreen(scene("game-messages", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Messages>), false),
554:    onGameScreen(scene("game-item-hover", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ItemHover>), true),
555:    hdOnly(onGameScreen(scene("game-list-scroll-end", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::ScrollEnd>), false)),
556:    onGameScreen(scene("game-rally-point", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Rally>), false),
557:    onGameScreen(scene("game-harkonnen-list-build", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListBuild>), false),
558:    onGameScreen(scene("game-harkonnen-list-infantry", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListInfantry>), false),
559:    onGameScreen(scene("game-harkonnen-list-vehicles", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListVehicles>), false),
560:    onGameScreen(scene("game-harkonnen-list-starport", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListStarport>), false),
561:    onGameScreen(scene("game-harkonnen-list-palace", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListPalace>), false),
562:    onGameScreen(scene("game-harkonnen-list-upgrades", "game-playing", "harkonnen", kFixedGameFrames, prepareGame<HARKONNEN, uiaudit::ListUpgrades>), false),
563:    onGameScreen(scene("game-ordos-list-build", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListBuild>), false),
564:    onGameScreen(scene("game-ordos-list-infantry", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListInfantry>), false),
565:    onGameScreen(scene("game-ordos-list-vehicles", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListVehicles>), false),
566:    onGameScreen(scene("game-ordos-list-starport", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListStarport>), false),
567:    onGameScreen(scene("game-ordos-list-palace", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListPalace>), false),
568:    onGameScreen(scene("game-ordos-list-upgrades", "game-playing", "ordos", kFixedGameFrames, prepareGame<ORDOS, uiaudit::ListUpgrades>), false),
```

### Перечень файлов: команда и вывод

```text
tests/UiAuditArgumentsTests.cpp
tests/ui_audit_main_menu_png.py
tests/ui_audit_runtime_support.py
tests/ui_audit_unknown_scene.py
tools/ui-audit/build_sheets.py
tools/ui-audit/check_completeness.py
tools/ui-audit/check_credits.py
tools/ui-audit/check_geometry.py
tools/ui-audit/check_keys.py
tools/ui-audit/check_options_geometry.py
tools/ui-audit/check_scenes.py
tools/ui-audit/check_screens.py
tools/ui-audit/combos.py
tools/ui-audit/exclusions.tsv
tools/ui-audit/extract_keys.py
tools/ui-audit/finalize_png.py
tools/ui-audit/find_hit_tests.py
tools/ui-audit/keys.tsv
tools/ui-audit/run_all.py
tools/ui-audit/run_combo.py
tools/ui-audit/tests/test_build_sheets.py
tools/ui-audit/tests/test_check_completeness.py
tools/ui-audit/tests/test_check_credits.py
tools/ui-audit/tests/test_check_geometry.py
tools/ui-audit/tests/test_check_keys.py
tools/ui-audit/tests/test_check_options_geometry.py
tools/ui-audit/tests/test_check_scenes.py
tools/ui-audit/tests/test_check_screens.py
tools/ui-audit/tests/test_combos.py
tools/ui-audit/tests/test_extra_rules.py
tools/ui-audit/tests/test_extract_keys.py
tools/ui-audit/tests/test_find_hit_tests.py
tools/ui-audit/tests/test_png_policy.py
tools/ui-audit/tests/test_png_policy_outputs.py
tools/ui-audit/tests/test_run_all.py
```

### Команды и вывод поиска класса для сцен

Команда: `git grep -n 'class cMainMenuState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cMainMenuState.h:35:class cMainMenuState : public cGameState {
```

Команда: `git grep -n 'class cSelectYourNextConquestState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cSelectYourNextConquestState.h:77:class cSelectYourNextConquestState : public cGameState {
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/utils/ini.h:25:class cSelectYourNextConquestState;
```

Команда: `git grep -n 'class cChooseHouseState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cChooseHouseState.h:35:class cChooseHouseState : public cGameState {
```

Команда: `git grep -n 'class cSelectMissionState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cSelectMissionState.h:35:class cSelectMissionState : public cGameState {
```

Команда: `git grep -n 'class BeneMentat' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/BeneMentat.h:28:class BeneMentat : public AbstractMentat {
```

Команда: `git grep -n 'class cOptionsState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cOptionsState.h:38:class cOptionsState : public cGameState {
```

Команда: `git grep -n 'class SaveSlotsDialog' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
<пустой вывод; exit 1>
```

Команда: `git grep -n 'class cCreditsState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cCreditsState.h:42:class cCreditsState : public cGameState {
```

Команда: `git grep -n 'class cSetupSkirmishState' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cSetupSkirmishState.h:59:class cSetupSkirmishState : public cGameState {
```

Команда: `git grep -n 'class cDrawManager' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/controls/cGameControlsContext.h:44:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/game/cGame.h:60:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/structures/cOrderProcesser.h:25:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cGamePlaying.h:36:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cSelectYourNextConquestState.h:45:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/include/sGameServices.h:26:class cDrawManager;
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/managers/cDrawManager.h:57:class cDrawManager : cInputObserver {
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/sidebar/cSideBar.h:37:class cDrawManager;
```

Команда: `git grep -n 'class AtreidesMentat' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/AtreidesMentat.h:20:class AtreidesMentat : public AbstractMentat {
```

Команда: `git grep -n 'class HarkonnenMentat' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/HarkonnenMentat.h:20:class HarkonnenMentat : public AbstractMentat {
```

Команда: `git grep -n 'class OrdosMentat' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/OrdosMentat.h:20:class OrdosMentat : public AbstractMentat {
```

Команда: `git grep -n 'class cGame::drawOutcomeScreen' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src`

Вывод:

```text
<пустой вывод; exit 1>
```

Команда: `git grep -n '^class cGame :' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src` (класс-хост для screen-метода `cGame::drawOutcomeScreen`)

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/game/cGame.h:88:class cGame : public cScenarioObserver, cInputObserver {
```

## Выводы кода подготовки сцен

Команда:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | nl -ba | sed -n '97,160p;176,260p;284,334p'
```

Вывод:

```text
    97	template <int House, int Kind>
    98	bool prepareMentat(cGame &game)
    99	{
   100	    resetSteps();
   101	    return UiAuditAccess::prepareMentatScene(game, House, Kind);
   102	}
   103	
   104	template <int Variant>
   105	bool prepareSkirmishSetup(cGame &game)
   106	{
   107	    resetSteps();
   108	    return UiAuditAccess::prepareSkirmish(game, Variant);
   109	}
   110	
   111	template <bool Victory>
   112	bool prepareOutcome(cGame &game)
   113	{
   114	    resetSteps();
   115	    return UiAuditAccess::enterPlaying(game, ATREIDES, 1);
   116	}
   117	
   118	template <bool Victory>
   119	bool readyOutcome(cGame &game)
   120	{
   121	    if (g_step == 0) {
   122	        if (!pause(3)) {
   123	            return false;
   124	        }
   125	        UiAuditAccess::missionOutcome(game, Victory);
   126	        g_step = 1;
   127	        return false;
   128	    }
   129	    return pause(3);
   130	}
   131	
   132	bool prepareMainMenu(cGame &game)
   133	{
   134	    UiAuditAccess::setState(game, GAME_MENU);
   135	    return true;
   136	}
   137	
   138	bool prepareChooseHouse(cGame &game)
   139	{
   140	    UiAuditAccess::setState(game, GAME_SELECT_HOUSE);
   141	    return true;
   142	}
   143	
   144	template <int House>
   145	bool prepareSelectMission(cGame &game)
   146	{
   147	    players[HUMAN].setHouse(House);
   148	    UiAuditAccess::setState(game, GAME_MISSIONSELECT);
   149	    return true;
   150	}
   151	
   152	template <int House, bool Awaiting>
   153	bool prepareTellHouse(cGame &game)
   154	{
   155	    resetSteps();
   156	    players[HUMAN].setHouse(House);
   157	    UiAuditAccess::prepareTellHouse(game, House);
   158	    UiAuditAccess::setState(game, GAME_TELLHOUSE);
   159	    return true;
   160	}
   176	template <int Variant>
   177	bool prepareOptionsMenu(cGame &game)
   178	{
   179	    resetSteps();
   180	    UiAuditAccess::setState(game, GAME_MENU);
   181	    return true;
   182	}
   183	
   184	template <int Variant>
   185	bool readyOptionsMenu(cGame &game)
   186	{
   187	    switch (g_step) {
   188	        case 0:
   189	            UiAuditAccess::setState(game, GAME_OPTIONS);
   190	            g_step = 1;
   191	            g_wait = 0;
   192	            return false;
   193	        case 1:
   194	            if (!pause(4)) {
   195	                return false;
   196	            }
   197	            if (Variant == 1) {
   198	                UiAuditAccess::optionsStatus(game);
   199	            }
   200	            else if (Variant >= 2 && Variant <= 4) {
   201	                UiAuditAccess::optionsPage(game, Variant - 1);
   202	            }
   203	            else if (Variant == 5) {
   204	                UiAuditAccess::optionsPage(game, 2);
   205	            }
   206	            g_step = 2;
   207	            return false;
   208	        case 2:
   209	            if (!pause(4)) {
   210	                return false;
   211	            }
   212	            if (Variant == 5) {
   213	                UiAuditAccess::optionsBinding(game);
   214	            }
   215	            g_step = 3;
   216	            return false;
   217	        default:
   218	            return pause(4);
   219	    }
   220	}
   221	
   222	bool prepareMenuWithSaves(cGame &game)
   223	{
   224	    resetSteps();
   225	    if (!UiAuditAccess::enterPlaying(game, ATREIDES, 1)) {
   226	        return false;
   227	    }
   228	    UiAuditAccess::writeSaves(game);
   229	    UiAuditAccess::setState(game, GAME_MENU);
   230	    return true;
   231	}
   232	
   233	bool readyMenuSaveDialog(cGame &game)
   234	{
   235	    if (g_step == 0) {
   236	        if (!pause(4)) {
   237	            return false;
   238	        }
   239	        if (!UiAuditAccess::openMenuSaveDialog(game)) {
   240	            return false;
   241	        }
   242	        g_step = 1;
   243	        return false;
   244	    }
   245	    return pause(4);
   246	}
   247	
   248	template <bool WithSaves>
   249	bool prepareGameOptions(cGame &game)
   250	{
   251	    resetSteps();
   252	    if (!UiAuditAccess::enterPlaying(game, ATREIDES, 1)) {
   253	        return false;
   254	    }
   255	    if (WithSaves) {
   256	        UiAuditAccess::writeSaves(game);
   257	    }
   258	    return true;
   259	}
   260	
   284	bool prepareCredits(cGame &game)
   285	{
   286	    resetSteps();
   287	    UiAuditAccess::setState(game, GAME_CREDITS);
   288	    setVerticalClipText(true);
   289	    return true;
   290	}
   291	
   292	template <int Frame>
   293	bool readyCredits(cGame &game)
   294	{
   295	    if (g_step == 0) {
   296	        if (!UiAuditAccess::creditsScroll(game, Frame)) {
   297	            return false;
   298	        }
   299	        g_step = 1;
   300	        g_wait = 0;
   301	        return false;
   302	    }
   303	    return pause(3);
   304	}
   305	
   306	template <int Type>
   307	bool prepareUnitLabels(cGame &game)
   308	{
   309	    resetSteps();
   310	    return UiAuditAccess::enterPlaying(game, ATREIDES, 1) && UiAuditAccess::placeLabelUnits(game, Type);
   311	}
   312	
   313	template <int House, int Kind>
   314	bool prepareGame(cGame &game)
   315	{
   316	    resetSteps();
   317	    return UiAuditAccess::prepareGameScreen(game, House, Kind);
   318	}
   319	
   320	template <int Edge>
   321	bool prepareStructureLabel(cGame &game)
   322	{
   323	    resetSteps();
   324	    return UiAuditAccess::enterPlaying(game, ATREIDES, 1) && UiAuditAccess::placeStructure(game, Edge);
   325	}
   326	
   327	template <int House, int Mission, bool Jump>
   328	bool prepareRegion(cGame &game)
   329	{
   330	    resetSteps();
   331	    players[HUMAN].setHouse(House);
   332	    UiAuditAccess::regionOpen(game, Mission, Jump);
   333	    return true;
   334	}
```

Команда:

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '67,178p;181,229p;274,283p;536,549p;780,934p'
```

Вывод:

```text
    67	void UiAuditAccess::prepareTellHouse(cGame &game, int house)
    68	{
    69	    game.prepareMentatToTellAboutHouse(house);
    70	}
    71	
    72	bool UiAuditAccess::mentatFreeze(cGame &game, bool awaiting)
    73	{
    74	    AbstractMentat *mentat = game.m_mentat;
    75	    if (mentat == nullptr) {
    76	        return false;
    77	    }
    78	    if (awaiting) {
    79	        mentat->state = AWAITING_RESPONSE;
    80	        return true;
    81	    }
    82	    int bestPair = 0;
    83	    size_t bestLength = 0;
    84	    for (int pair = 0; pair <= 8; pair += 2) {
    85	        const size_t length = std::strlen(mentat->sentence[pair]) + std::strlen(mentat->sentence[pair + 1]);
    86	        if (length > bestLength) {
    87	            bestLength = length;
    88	            bestPair = pair;
    89	        }
    90	    }
    91	    mentat->iMentatSentence = bestPair;
    92	    mentat->TIMER_Speaking = 1 << 20;
    93	    mentat->state = SPEAKING;
    94	    return bestLength > 0;
    95	}
    96	
    97	bool UiAuditAccess::prepareMentatScene(cGame &game, int house, int kind)
    98	{
    99	    players[HUMAN].setHouse(house);
   100	    game.m_region = 1;
   101	    if (kind == 0) {
   102	        game.setNextStateToTransitionTo(GAME_BRIEFING);
   103	        game.transitionStateIfRequired();
   104	    }
   105	    else {
   106	        game.setState(kind == 1 ? GAME_WINBRIEF : GAME_LOSEBRIEF);
   107	        game.createAndPrepareMentatForHumanPlayer(true);
   108	    }
   109	    return game.m_mentat != nullptr;
   110	}
   111	
   112	bool UiAuditAccess::prepareSkirmish(cGame &game, int variant)
   113	{
   114	    game.loadSkirmishMaps();
   115	    game.initSkirmish();
   116	    game.setNextStateToTransitionTo(GAME_SETUPSKIRMISH);
   117	    game.transitionStateIfRequired();
   118	    auto *setup = dynamic_cast<cSetupSkirmishState *>(game.m_currentState);
   119	    if (setup == nullptr) {
   120	        return false;
   121	    }
   122	    setup->iSkirmishMap = variant == 0 ? 0 : 1;
   123	    if (variant == 1) {
   124	        setup->startingPoints = 4;
   125	        setup->skirmishPlayer[2].bPlaying = true;
   126	        setup->skirmishPlayer[3].bPlaying = true;
   127	    }
   128	    return true;
   129	}
   130	
   131	void UiAuditAccess::missionOutcome(cGame &game, bool victory)
   132	{
   133	    game.m_missionWasWon = victory;
   134	    game.setState(victory ? GAME_WINNING : GAME_LOSING);
   135	    game.takeBackGroundScreen();
   136	}
   137	
   138	void UiAuditAccess::writeSaves(cGame &game)
   139	{
   140	    std::string error;
   141	    std::filesystem::create_directories("saves");
   142	    SaveGameManager::saveGame(game, 1, "", error);
   143	    SaveGameManager::saveGame(game, 2, "A very long save name used to check how the slot row fits", error);
   144	    SaveGameManager::saveGame(game, 5, "Before the final attack", error);
   145	    std::ofstream(SaveGameManager::slotPath(3), std::ios::binary) << "not a save file";
   146	    std::filesystem::create_directories(SaveGameManager::slotPath(6));
   147	}
   148	
   149	bool UiAuditAccess::openMenuSaveDialog(cGame &game)
   150	{
   151	    auto *menu = dynamic_cast<cMainMenuState *>(game.m_currentState);
   152	    if (menu == nullptr || menu->m_saveDialog == nullptr) {
   153	        return false;
   154	    }
   155	    menu->m_saveDialog->open(false, false);
   156	    return true;
   157	}
   158	
   159	bool UiAuditAccess::saveDialog(cGame &game, int action)
   160	{
   161	    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   162	    if (options == nullptr || options->m_saveDialog == nullptr) {
   163	        return false;
   164	    }
   165	    SaveSlotsDialog &dialog = *options->m_saveDialog;
   166	    dialog.open(true, action == 1 || action == 2 || action == 4);
   167	    if (action == 2) {
   168	        dialog.selectSlot(2);
   169	    }
   170	    else if (action == 3) {
   171	        dialog.selectSlot(3);
   172	        dialog.loadSelected();
   173	    }
   174	    else if (action == 4) {
   175	        dialog.selectSlot(6);
   176	        dialog.saveSelected();
   177	    }
   178	    return true;
   181	bool UiAuditAccess::optionsPage(cGame &game, int page)
   182	{
   183	    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   184	    if (options == nullptr) {
   185	        return false;
   186	    }
   187	    options->switchOptionsPage(static_cast<cOptionsState::OptionsPage>(page));
   188	    return true;
   189	}
   190	
   191	bool UiAuditAccess::optionsBinding(cGame &game)
   192	{
   193	    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   194	    if (options == nullptr) {
   195	        return false;
   196	    }
   197	    options->m_bindingCapture = CommandBindingAction::Attack;
   198	    options->refresh();
   199	    return true;
   200	}
   201	
   202	bool UiAuditAccess::optionsStatus(cGame &game)
   203	{
   204	    auto *options = dynamic_cast<cOptionsState *>(game.m_currentState);
   205	    if (options == nullptr || options->m_displayStatusLabel == nullptr) {
   206	        return false;
   207	    }
   208	    options->m_displayStatusLabel->setText(
   209	        localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
   210	    return true;
   211	}
   212	
   213	bool UiAuditAccess::creditsScroll(cGame &game, int frame)
   214	{
   215	    auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
   216	    if (credits == nullptr) {
   217	        return false;
   218	    }
   219	    credits->m_moveSpeed = 0;
   220	    if (frame == 0) {
   221	        credits->m_crawlerY = 64;
   222	        return true;
   223	    }
   224	    const int fontHeight = credits->m_textDrawer->getFontHeight();
   225	    const int limit = game.m_screenH - 128;
   226	    std::vector<int> offsets;
   227	    std::vector<bool> visible;
   228	    int offset = credits->m_titleHeight;
   229	    for (const s_CreditLine &line : credits->m_lines) {
   274	void UiAuditAccess::regionOpen(cGame &game, int mission, bool jump)
   275	{
   276	    if (jump) {
   277	        game.jumpToSelectYourNextConquestMission(mission);
   278	    }
   279	    else {
   280	        game.m_mission = mission;
   281	    }
   282	    game.setState(GAME_REGION);
   283	}
   536	bool UiAuditAccess::enterPlaying(cGame &game, int house, int region)
   537	{
   538	    players[HUMAN].setHouse(house);
   539	    game.m_region = region;
   540	    game.setNextStateToTransitionTo(GAME_BRIEFING);
   541	    game.transitionStateIfRequired();
   542	    game.setNextStateToTransitionTo(GAME_PLAYING);
   543	    game.transitionStateIfRequired();
   544	    if (drawManager == nullptr || global_map.getWidth() <= 0 || mapCamera == nullptr) {
   545	        return false;
   546	    }
   547	    drawManager->missionInit();
   548	    return game.m_state == GAME_PLAYING;
   549	}
   780	bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
   781	{
   782	    using uiaudit::GameKind;
   783	    if (!enterPlaying(game, house, 22)) {
   784	        return false;
   785	    }
   786	    BaseResult base;
   787	    const bool withRadar = kind != GameKind::RadarNone;
   788	    if (!buildBase(withRadar, kind == GameKind::DamagedUnit ? 0.4f : 1.0f, base)) {
   789	        return false;
   790	    }
   791	    if (kind == GameKind::RadarNoPower) {
   792	        for (int i = 0; i < MAX_STRUCTURES; i++) {
   793	            cAbstractStructure *s = structure[i];
   794	            if (s != nullptr && s->isValid() && s->getOwner() == HUMAN && s->getType() == WINDTRAP) {
   795	                s->setHitPoints(1);
   796	            }
   797	        }
   798	        players[HUMAN].update();
   799	        if (players[HUMAN].bEnoughPower()) {
   800	            return false;
   801	        }
   802	    }
   803	    for (int i = 0; i < 40; i++) {
   804	        drawManager->getMiniMapDrawer()->think();
   805	    }
   806	
   807	    const bool lists = listForKind(kind) != eListType::LIST_NONE;
   808	    const int centerColumn = (kind == GameKind::PlaceAllowed || kind == GameKind::PlaceForbidden) ? 28 : 30;
   809	    mapCamera->centerAndJumpViewPortToCell(cellAt(centerColumn, 26));
   810	    cSideBar *sidebar = players[HUMAN].getSideBar();
   811	    if (sidebar == nullptr) {
   812	        return false;
   813	    }
   814	    cBuildingListDrawer *items = drawManager->getBuildingListDrawer();
   815	
   816	    if (lists) {
   817	        sidebar->setSelectedListId(listForKind(kind));
   818	        cBuildingList *list = sidebar->getList(sidebar->getSelectedListID());
   819	        return list != nullptr && list->isAvailable() && list->getItemCount() > 0;
   820	    }
   821	
   822	    switch (kind) {
   823	        case GameKind::Hud:
   824	        case GameKind::RadarNone:
   825	        case GameKind::RadarNoPower:
   826	            return true;
   827	        case GameKind::Music: {
   828	            MusicController *music = game.m_musicController.get();
   829	            if (music == nullptr) {
   830	                return false;
   831	            }
   832	            MusicTrack track;
   833	            track.externalPath = std::filesystem::path(
   834	                localization::text("Gameplay_theme_with_an_extremely_long_track_title_for_the_layout_audit.ogg",
   835	                                   "Игровая_тема_с_очень_длинным_названием_трека_для_проверки_раскладки.ogg"));
   836	            auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
   837	            state.playlist.setTracks({track});
   838	            state.playlist.next();
   839	            music->m_activeCategory = MusicCategory::Gameplay;
   840	            music->m_hasActiveCategory = true;
   841	            return !music->currentDisplayName().empty();
   842	        }
   843	        case GameKind::DamagedUnit:
   844	            selectOnly(base.tankId);
   845	            return true;
   846	        case GameKind::Harvester:
   847	            selectOnly(base.harvesterId);
   848	            return true;
   849	        case GameKind::Mcv:
   850	            selectOnly(base.mcvId);
   851	            return true;
   852	        case GameKind::Structure:
   853	            players[HUMAN].selected_structure = base.factoryId;
   854	            return true;
   855	        case GameKind::Rally:
   856	            players[HUMAN].selected_structure = base.factoryId;
   857	            structure[base.factoryId]->setRallyPoint(cellAt(28, 32));
   858	            return structure[base.factoryId]->getRallyPoint() >= 0;
   859	        case GameKind::PlaceAllowed:
   860	        case GameKind::PlaceForbidden: {
   861	            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
   862	            cBuildingListItem *item = list == nullptr ? nullptr : list->getItemByBuildId(WINDTRAP);
   863	            if (item == nullptr) {
   864	                return false;
   865	            }
   866	            item->setPlaceIt(true);
   867	            players[HUMAN].setContextMouseState(eMouseState::MOUSESTATE_PLACE);
   868	            if (kind == GameKind::PlaceAllowed) {
   869	                for (int dy = 0; dy < 2; dy++) {
   870	                    for (int dx = 0; dx < 2; dx++) {
   871	                        global_map.cellChangeType(cellAt(22 + dx, 25 + dy), TERRAIN_ROCK);
   872	                    }
   873	                }
   874	                hoverOnCell(22, 25);
   875	            }
   876	            else {
   877	                hoverOnCell(29, 24);
   878	            }
   879	            return true;
   880	        }
   881	        case GameKind::GroupSelect: {
   882	            const int cell1 = cellAt(24, 26);
   883	            const int cell2 = cellAt(31, 29);
   884	            cMouse *mouse = game.getMouse();
   885	            mouse->mouse_co_x1 = mapCamera->getWindowXPositionFromCell(cell1);
   886	            mouse->mouse_co_y1 = mapCamera->getWindowYPositionFromCell(cell1);
   887	            mouse->mouse_co_x2 = mapCamera->getWindowXPositionFromCell(cell2);
   888	            mouse->mouse_co_y2 = mapCamera->getWindowYPositionFromCell(cell2);
   889	            uiaudit::setHover(mouse->mouse_co_x2, mouse->mouse_co_y2);
   890	            return mouse->isBoxSelecting();
   891	        }
   892	        case GameKind::Messages: {
   893	            drawManager->setMessage(localization::text("Construction complete: the Windtrap is ready to be placed",
   894	                                                       "Строительство завершено: ветряная электростанция готова к размещению"), true);
   895	            for (int i = 0; i < 90; i++) {
   896	                drawManager->thinkFast();
   897	            }
   898	            players[HUMAN].addNotification(localization::text("Neutral notification", "Обычное уведомление"),
   899	                                           eNotificationType::NEUTRAL);
   900	            players[HUMAN].addNotification(localization::text("Priority notification: Harvester is full",
   901	                                                              "Важное уведомление: комбайн заполнен"),
   902	                                           eNotificationType::PRIORITY);
   903	            players[HUMAN].addNotification(localization::text("Bad news: a structure is under attack",
   904	                                                              "Плохая новость: здание атаковано"),
   905	                                           eNotificationType::BAD);
   906	            return true;
   907	        }
   908	        case GameKind::ItemHover:
   909	        case GameKind::ScrollEnd: {
   910	            sidebar->setSelectedListId(eListType::LIST_CONSTYARD);
   911	            cBuildingList *list = sidebar->getList(eListType::LIST_CONSTYARD);
   912	            if (list == nullptr || list->getItemCount() < 3) {
   913	                return false;
   914	            }
   915	            if (kind == GameKind::ScrollEnd) {
   916	                items->setScrollRow(list, 1000);
   917	                return true;
   918	            }
   919	            const int index = 2;
   920	            const HudLayout layout = items->getLayout(list);
   921	            const cRectangle card = layout.cardRect(index, items->getScrollRow(list));
   922	            const int x = card.getX() + card.getWidth() / 2;
   923	            const int y = card.getY() + card.getHeight() / 2;
   924	            drawManager->setMessage(list->getItem(index)->getInfo(), true);
   925	            for (int i = 0; i < 90; i++) {
   926	                drawManager->thinkFast();
   927	            }
   928	            uiaudit::setHover(x, y);
   929	            return true;
   930	        }
   931	        default:
   932	            return false;
   933	    }
   934	}
```

## Числа строк и проверка наличия в PORT

Для каждого пути выполнялись команды `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> | wc -l` и `git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- <путь>`. Вывод (в последней колонке «нет» означает пустой stdout второй команды):

```text
tests/UiAuditArgumentsTests.cpp	103	<пустой вывод; нет в PORT>
tests/ui_audit_main_menu_png.py	63	<пустой вывод; нет в PORT>
tests/ui_audit_runtime_support.py	104	<пустой вывод; нет в PORT>
tests/ui_audit_unknown_scene.py	48	<пустой вывод; нет в PORT>
tools/ui-audit/build_sheets.py	261	<пустой вывод; нет в PORT>
tools/ui-audit/check_completeness.py	73	<пустой вывод; нет в PORT>
tools/ui-audit/check_credits.py	53	<пустой вывод; нет в PORT>
tools/ui-audit/check_geometry.py	251	<пустой вывод; нет в PORT>
tools/ui-audit/check_keys.py	126	<пустой вывод; нет в PORT>
tools/ui-audit/check_options_geometry.py	120	<пустой вывод; нет в PORT>
tools/ui-audit/check_scenes.py	132	<пустой вывод; нет в PORT>
tools/ui-audit/check_screens.py	86	<пустой вывод; нет в PORT>
tools/ui-audit/combos.py	100	<пустой вывод; нет в PORT>
tools/ui-audit/exclusions.tsv	10	<пустой вывод; нет в PORT>
tools/ui-audit/extract_keys.py	92	<пустой вывод; нет в PORT>
tools/ui-audit/finalize_png.py	59	<пустой вывод; нет в PORT>
tools/ui-audit/find_hit_tests.py	58	<пустой вывод; нет в PORT>
tools/ui-audit/keys.tsv	169	<пустой вывод; нет в PORT>
tools/ui-audit/run_all.py	152	<пустой вывод; нет в PORT>
tools/ui-audit/run_combo.py	184	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_build_sheets.py	117	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_completeness.py	139	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_credits.py	53	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_geometry.py	326	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_keys.py	173	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_options_geometry.py	137	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_scenes.py	166	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_check_screens.py	97	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_combos.py	170	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_extra_rules.py	203	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_extract_keys.py	74	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_find_hit_tests.py	70	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_png_policy.py	93	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_png_policy_outputs.py	97	<пустой вывод; нет в PORT>
tools/ui-audit/tests/test_run_all.py	70	<пустой вывод; нет в PORT>
```

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/exclusions.tsv | nl -ba | sed -n '1,3p'`

Вывод:

```text
     1	name	reason
     2	GAME_EDITING	режим редактора карт, не экран игрока и не достижим из меню
     3	GAME_INTRO	вступительный ролик без интерфейса игры
```

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/keys.tsv | nl -ba | sed -n '1,3p'`

Вывод:

```text
     1	file	function	key	mods	line	state	action	reason
     2	src/building/cItemBuilder.cpp	cItemBuilder::onKeyHold	SDL_SCANCODE_LSHIFT		826	game: nothing selected | game: structure selected | game: units selected | game: repair mode | game: debug mode	build-multiplier	
     3	src/building/cItemBuilder.cpp	cItemBuilder::onKeyHold	SDL_SCANCODE_RSHIFT		826	game: nothing selected | game: structure selected | game: units selected | game: repair mode | game: debug mode	build-multiplier
```

