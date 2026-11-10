# RECON-P11R

Рабочая копия и исходники не изменялись. Сборки, CTest и запуск игры не выполнялись. Табличные сведения с построчными ссылками приведены в пяти приложенных TSV; ниже зафиксированы основные команды, их фактические выводы и содержательные результаты.

## 1. Ментаты в FORK1

В `src/mentat/*.cpp@9208dcf` таблица содержит 28 подходящих функций. Для каждой указаны диапазон строк, краткое назначение, наличие одноимённой функции в BASE, передаваемые имена ресурсов и результаты поиска в паке: [fork-mentat.tsv](fork-mentat.tsv).

Функции извлекались командой `git grep -n -E '^(AbstractMentat::AbstractMentat|AbstractMentat::~AbstractMentat|void AbstractMentat::(think|thinkEyes|thinkMouth|draw\(|drawHdTextHeader|harmonizeHdButtonTextScale|clearHdMovieOpening|clearHdForegroundLayerRegion|loadScene|speak)|Texture \*AbstractMentat::(getBackgroundBitmap|getHdForegroundLayer)|AtreidesMentat::AtreidesMentat|void AtreidesMentat::(clearHdMovieOpening|draw_eyes|draw_mouth)|BeneMentat::BeneMentat|void BeneMentat::(draw_eyes|draw_mouth)|HarkonnenMentat::HarkonnenMentat|void HarkonnenMentat::(draw_eyes|draw_mouth)|OrdosMentat::OrdosMentat|void OrdosMentat::(clearHdMovieOpening|draw_eyes|draw_mouth))' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/mentat/AbstractMentat.cpp src/mentat/AtreidesMentat.cpp src/mentat/BeneMentat.cpp src/mentat/HarkonnenMentat.cpp src/mentat/OrdosMentat.cpp`.

Вывод содержит определения в `AbstractMentat.cpp` на строках 126, 209, 221, 284, 318, 373, 469, 479, 516, 538, 559, 581, 645 и 677; в `AtreidesMentat.cpp` — 15, 73, 120 и 125; в `BeneMentat.cpp` — 17, 102 и 111; в `HarkonnenMentat.cpp` — 11, 55 и 60; в `OrdosMentat.cpp` — 13, 57, 119 и 124. Определения, начинающиеся с этих строк, и их назначение указаны в TSV.

Вызовы сцен и их вывод получены командой `git grep -n 'loadScene(' 9208dcf5a358f40afd95c99480e4e09f781ed566 --`:

```text
src/cGame_logic.cpp:1535: m_mentat->loadScene("win01");
src/cGame_logic.cpp:1538: m_mentat->loadScene("win02");
src/cGame_logic.cpp:1544: m_mentat->loadScene("lose01");
src/cGame_logic.cpp:1547: m_mentat->loadScene("lose02");
src/cGame_logic.cpp:1582: m_mentat->loadScene("platr");
src/cGame_logic.cpp:1586: m_mentat->loadScene("plhar");
src/cGame_logic.cpp:1590: m_mentat->loadScene("plord");
src/ini.cpp:690: pMentat->loadScene(scene);
src/mentat/AbstractMentat.cpp:645: void AbstractMentat::loadScene(const std::string &scene)
src/mentat/AbstractMentat.h:61: loadScene declaration
```

`AbstractMentat::loadScene` строит формат `data/scenes/hd4/sdl_{}.dat` в `src/mentat/AbstractMentat.cpp@9208dcf:650`. Проверки по `tests/data/hd4_packs_expected.tsv@832c953` использовали `git show 832c953a94a632d57872349013f7ed1a37434715:tests/data/hd4_packs_expected.tsv | grep -c '<имя>'`. Для `win01`, `win02`, `lose01`, `lose02`, `platr`, `plhar`, `plord` фактический stdout по порядку был `1`, `1`, `1`, `1`, `33`, `33`, `33`; для буквального шаблона `data/scenes/hd4/sdl_{}.dat` — `0`. В `fork-mentat.tsv` указаны имена и результаты для каждой функции, включая динамическое значение `scene` из `src/ini.cpp@9208dcf:690`.

Таблицы проверены `/srv/dune/venv/bin/python`. Вывод:

```text
.tmp/p11r/fork-mentat.tsv: lines=29, expected_columns=6, actual_columns=[6], malformed_lines=[]
.tmp/p11r/port-mentat.tsv: lines=89, expected_columns=5, actual_columns=[5], malformed_lines=[]
```

## 2. Ментаты в PORT

В `port-mentat.tsv` приведены 24 функции из `src/gameobjects/mentat/*.cpp@832c953` с формулами кадров, прямоугольниками отрисовки и файлами/записями. Там же перечислены 64 участка diff BASE..UP1 с начальной строкой `@d06f2fc` и изменением участка.

Определения проверялись `git grep -n -E` по исходникам FORK1 и PORT. В PORT вывод дал определения `AbstractMentat` на строках 45, 121, 168, 184, 218, 273, 316, 322 и 346; производные классы: Atreides — 27, 73, 78; Bene — 35, 106, 111; Harkonnen — 28, 71, 76; Ordos — 27, 70, 75; Sardaukar — 28, 71, 76. Полные имена функций, ревизии, диапазоны строк и назначения находятся в таблице.

Число участков diff подсчитано командой:

```sh
git diff --unified=0 --no-color e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gameobjects/mentat src/mentat | awk '/^@@/{n++} END{print n}'
```

Вывод:

```text
64
```

Фрагмент `src/gameobjects/mentat/AbstractMentat.cpp@832c953:168-182` проверен отдельно:

```sh
git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/mentat/AbstractMentat.cpp | sed -n '168,182p'
```

Вывод показывает, что каждые 21 тика `iMovieFrame` увеличивается и сбрасывается в ноль по числу файлов сцены. Функция `AbstractMentat::draw_eyes` для Атрейдесов отрисовывает `ATR_EYES01 + iMentatEyes` в `(offsetX + 80, offsetY + 241)` (`AtreidesMentat.cpp@832c953:73-76`); команда и весь её stdout находятся в [spotcheck.md](spotcheck.md). Для Сардаукаров `draw_eyes` пустая, а вызов `renderSprite` закомментирован (`SardaukarMentat.cpp@832c953:71-74`); эта строка тоже выборочно сверена помощником 4.

В PORT `loadScene` использует `hd4SceneFile(scene)` и `kHd4AssetDensity` (`src/gameobjects/mentat/AbstractMentat.cpp@832c953:346-352`). Вызовы `win01`, `win02`, `lose01`, `lose02` находятся в `cMentatState.cpp@832c953:111-131`, вызовы `platr`, `plhar`, `plord` — в `cTellHouseState.cpp@832c953:73-81`; `briefScene` поступает через `src/utils/ini.cpp@832c953:137`. Полный вывод `git grep -n 'loadScene(' 832c953a94a632d57872349013f7ed1a37434715 --` приведён в дорожке помощника 1 и отражён в таблице.

## 3. Титры

Для каждого метода `cCreditsState` в `src/gamestates/cCreditsState.cpp/.h` таблица содержит строки начала и конца в обеих ревизиях и назначение: [credits.tsv](credits.tsv). В FORK1 и PORT найдены девять методов: конструктор, `prepareCrawlerLines`, `resetCrawler`, деструктор, `thinkFast`, `draw`, `onNotifyMouseEvent`, `getType`, `onNotifyKeyboardEvent`.

Конструктор загружает `resources/bin/data/hd4/credits_team.png` и `resources/bin/data/hd4/credits_title.png` через `loadHdUiTexture`, а при отсутствии HD-изображений — записи `CREDITS_DUNE2_CORE_TEAM` и `D2TM_TITLE`. Метод `draw` рисует две художественные картинки, прокручиваемый текст, кнопку Back и указатель мыши. Функции и ссылки на строки обеих ревизий перечислены в `credits.tsv`.

История изменений `cCreditsState.cpp` получена командой `git log --format=%h --name-only e17379ad660fca46859b403a6c3d33ec8d831a40..9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/gamestates/cCreditsState.cpp`. Вывод содержит коммиты `d7b927d4`, `ea6bfc4a`, `5c77e8f9`, `ecfd4990`, `f1b8ea26`; в каждом изменён `src/gamestates/cCreditsState.cpp`.

Для каждого коммита выполнена команда `git show --stat <коммит> | tail -n 1`. Фактический stdout по порядку коммитов:

```text
d7b927d4: 122 files changed, 9611 insertions(+), 1420 deletions(-)
ea6bfc4a: 51 files changed, 970 insertions(+), 2494 deletions(-)
5c77e8f9: 47 files changed, 2582 insertions(+), 1 deletion(-)
ecfd4990: 261 files changed, 3951 insertions(+), 1020 deletions(-)
f1b8ea26: 2326 files changed, 92910 insertions(+), 2235 deletions(-)
```

Суммарно таблица `credits.tsv` содержит 2 237 уникальных путей вне `src/` из этих коммитов. Для каждого указаны размер объекта, первая строка `git cat-file -p`, наличие Git LFS, наличие пути в PORT и сравнение OID. Шестьдесят девять путей из списка отсутствуют в FORK1; таблица содержит для них исторический объект, если он доступен в затрагивающем коммите или его родителе. Команды `git show --stat <коммит> -- src/gamestates/cCreditsState.cpp` дают строки изменений файла по порядку: `4 ++++`; `48 ++++++++++++++++-------------------------`; `4 ++++`; `27 +++++++++++++++++++++++++++--------`; `45 +++++++++++++++++++++++++++++++++++++++++++++---------`.

Для `resources/bin/data/hd4/credits_team.png` команды `git cat-file -s`, `git cat-file -p | head -n 1` и `git rev-parse` для FORK1 и PORT вывели соответственно `131`, `version https://git-lfs.github.com/spec/v1` и один и тот же OID `82d4fa87a45b181cd9943b2c14ff58c7cb8d346c` в обеих ревизиях. Для `credits_title.png` выводы: `131`, та же строка LFS и OID `3d48dea79ad7e153c1364e7a66c579590b45de46` в обеих ревизиях. Исторические HD2-файлы оба удалены коммитом `ecfd4990`; в родительском коммите team имеет размер `131` и OID `fd6d962505f80658e3439f016b6c97e4c6c22c1c`, title — размер `130` и OID `c8e7df126c1986882d19f1369d30b1c723a1455b`.

## 4. Вступительный ролик апстрима

В задании указан путь `src/VideoFlow.hpp`, но такой путь в UP1 отсутствует. Команда

```sh
git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/VideoFlow.hpp
```

вывела `fatal: path 'src/VideoFlow.hpp' does not exist in 'd06f2fcd2a347182c3774fb96e9a85570405c489'`. Фактический заголовок находится в `src/game/VideoFlow.hpp@d06f2fc`. API включает класс `VideoFlow` (строка 26), алиас `PlayCallback` (28), конструктор (30), `play` (34) и поле `m_play` (39); структуры и константы в этом заголовке отсутствуют. Все эти позиции присутствуют в PORT по тем же строкам. Список API приведён в [intro.tsv](intro.tsv).

Команды `git grep -n -i 'VideoFlow\|intro\|video' d06f2fcd2a347182c3774fb96e9a85570405c489 -- src` и та же команда для PORT выполнили поиск по всему `src`. Поиск включает также совпадения слов “introduced”, видеоподсистемы SDL и отдельного вступительного экрана кампании. Вывод UP1 по файлам и номерам строк:

```text
src/CMakeLists.txt:130
src/game/VideoFlow.hpp:2,23,26,30
src/game/cGame.h:73,263
src/game/cGame_logic.cpp:27,64,235,237,238,291,981,1108,1109
src/game/cSDLSystem.cpp:254,288
src/gameobjects/units/cUnit.cpp:200
src/gamestates/cCreatorState.cpp:28,81,82
src/gamestates/cCreatorState.h:43,44
src/gamestates/cGameState.cpp:47
src/gamestates/cGameState.h:46,55
src/gamestates/cMainMenuState.cpp:32,51,58,73,207,208,209,210,211,212,213,214,217,219,221,222,225
src/gamestates/cMainMenuState.h:28,52
src/gamestates/cSelectYourNextConquestState.cpp:109,160,164,203,305,306,355
src/gamestates/cSelectYourNextConquestState.h:48,161
src/gamestates/cVideoState.cpp:2,16,32,35,36,37,38,39,40,43,58,60,61,63,67,70,72,76,80,82,91,95,101,108
src/gamestates/cVideoState.h:2,28,30,31
src/include/Texture.hpp:23,25
src/definitions.h:35
src/eGameState.cpp:62,63,85,96
src/eGameState.h:29,40,56,68
src/include/sGameServices.h:40,65
```

Вывод PORT содержит соответствующие места в тех же 21 исходных файлах: `src/CMakeLists.txt@832c953:130`, `src/game/VideoFlow.hpp:2,23,26,30`, `src/game/cGame.h:72,262`, `src/game/cGame_logic.cpp:27,64,234,236,237,290,1010,1137,1138`, `src/game/cSDLSystem.cpp:261,295`, `src/gameobjects/units/cUnit.cpp:200`, `src/gamestates/cCreatorState.cpp:28,81,82`, `cCreatorState.h:43,44`, `cGameState.cpp:47`, `cGameState.h:46,55`, `cMainMenuState.cpp:33,56,63,171,172,173,174`, `cMainMenuState.h:28,55`, `cSelectYourNextConquestState.cpp:111,206,210,249,353,354,675`, `cSelectYourNextConquestState.h:50,163`, `cVideoState.cpp:2,16,32,35,36,37,38,39,40,43,58,60,61,63,67,70,72,76,80,82,91,95,101,108`, `cVideoState.h:2,28,30,31`, `src/include/Texture.hpp:24,26`, `src/definitions.h:35`, `src/eGameState.cpp:62,63,85,96`, `src/eGameState.h:29,40,56,68`, `src/include/sGameServices.h:40,65`. Полные пути с ревизией и назначением совпадений приведены в `intro.tsv`. `src/game/cSDLSystem.cpp` описывает видеоподсистему SDL, `cUnit.cpp:200` совпадает только по `introduced`, а строки `cSelectYourNextConquestState` относятся к вступительному экрану кампании, не к файлу ролика.

Кнопка Introduction показывается в главном меню (`cMainMenuState::getType`, `src/gamestates/cMainMenuState.cpp@d06f2fc:295,297`). В `src/gamestates/cMainMenuState.cpp@d06f2fc:210-211` задаётся `intro.pak` и проверяется его наличие через `std::filesystem::exists`; клик вызывает `videoFlow->play` (`:214,219,221`). Callback создаёт `cVideoState` и переход `GAME_VIDEO` (`src/game/cGame_logic.cpp@d06f2fc:235-238`), обработчик перехода выбирает VIDEO (`:1108-1109`). `cVideoState` возвращает `GAMESTATE_VIDEO` (`cVideoState.cpp@d06f2fc:70-72`), выдаёт по кадру за вызов `thinkNormal` и после последнего кадра переходит в `GAME_MENU` с затемнением (`:80-88`). Нажатие левой кнопки мыши (`:101-105`) или любой клавиши (`:108-112`) также пропускает ролик и переводит в меню. Пустой пакет оставляет состояние без кадров; следующий `thinkNormal` переводит его в меню (`:56-64,80-88`).

Имя файла передаётся в `Graphics` (`src/gamestates/cVideoState.cpp@d06f2fc:54`), затем `DataPack` создаёт `ReaderPack`, который открывает путь через `SDL_IOFromFile` (`src/utils/Graphics.cpp:25`, `src/utils/cDataPack.cpp:28`, `src/utils/cPack.cpp:103-107`). `git ls-tree -r d06f2fcd2a347182c3774fb96e9a85570405c489 -- intro.pak` и такая же команда для PORT вывели пустую строку. Поиск имени `intro.pak` по всему дереву также не нашёл файла ни в UP1, ни в PORT.

## 5. Тесты

Таблица [tests.tsv](tests.tsv) содержит четыре проверки из `tests/HdPresentationTests.cpp@9208dcf:26,31,36,41`: меню, игровой процесс, ментат после выбора Дома и старые неперенесённые экраны. Каждая вызывает `shouldUsePhysicalHdPresentation` с одним из значений `HdPresentationScene::{Menu,Gameplay,Mentat,Legacy}`. Тесты используют локальный `expectEqual` (`tests/HdPresentationTests.cpp@9208dcf:10-18`) и заголовок `utils/HdPresentation.hpp` (строка 1; объявления в `src/utils/HdPresentation.hpp@9208dcf:3-8,42-46`). Все эти четыре проверки, helper и API отсутствуют в PORT.

Число проверок получено командой

```sh
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | grep -c 'shouldUsePhysicalHdPresentation'
```

Вывод:

```text
4
```

Регистрация найдена в `CMakeLists.txt@9208dcf:321-329`: `hd_presentation_tests` собирается из `tests/HdPresentationTests.cpp`, а строка 329 содержит `add_test(NAME hd_presentation_selection COMMAND hd_presentation_tests)`. `include(CTest)` находится на строке 7. Проверка наличия символов в PORT командой `git grep -n -e shouldUsePhysicalHdPresentation -e HdPresentationScene 832c953a94a632d57872349013f7ed1a37434715 --` вывела пустую строку (код 1).

## Сверка

Помощник 4 выбрал по три факта из таблицы помощников 1, 2 и 3 и проверил каждый отдельной командой `git show <ревизия>:<путь> | sed -n '<строки>p'`. В [spotcheck.md](spotcheck.md) сохранены команды и фактический stdout. Проверено 9 фактов; совпало 9.

## Чтение

До начала изменений прочитаны отдельными вызовами:

- `/srv/dune/tasks/load-check/PORT_PLAN.md` целиком. Для П11 в разделе 4 записано: приёмка — снимки П13; в «Содержании шагов» П11 назван ментатами HD, титрами и сценами; в разделе вопросов владельцу зафиксирован вступительный ролик апстрима.
- `docs/upstream/PORT_MAP.md@62e1ff6`, строки 111–151 (`hd4-assets`): список изменённых, перемещённых и удалённых путей и каталогов ресурсов.
- `docs/upstream/PORT_MAP.md@62e1ff6`, строки 758–768 (`credits-art`): изменяемые `cCreditsState.cpp/.h` и ресурсы по каталогам.
- `docs/decisions.md@62e1ff6`: строки Р34 и Р63; игра загружает HD4, а новые возможности апстрима, включая вступительный ролик, берутся как есть, кроме случаев конфликта с функцией форка.

Из плана прочитаны ссылки, необходимые для понимания основания и приёмки П11: `docs/PLAN_units_sega_upstream.md@62e1ff6`, раздел 3.2 и поток Б (перенос функций по одной; Б11 принимает снимки Б13), а также раздел 5.3 (проверки обновления); `codex-direct/launch-card-27.md@62e1ff6` целиком (шаги П2–П15 выполняются без новых карточек, смена рамки требует новой карточки). Этих материалов не было в списке «Прочитать до работы», но `PORT_PLAN.md` прямо ссылается на них.

В пути из задания для заголовка VideoFlow обнаружено расхождение: `src/VideoFlow.hpp` отсутствует, фактический заголовок — `src/game/VideoFlow.hpp`. Команда и вывод отсутствующего пути приведены в пункте 4; дальнейшие факты по заголовку даны с фактическим путём.

## Не проверено

- Реальное воспроизведение `intro.pak` в игре и содержимое внешнего пакета не проверялись. Сборки, CTest и запуск игры запрещены заданием и не выполнялись; в деревьях UP1 и PORT `intro.pak` отсутствует.
- Все строки источников сверх девяти выборочных проверок помощника 4 не проходили отдельную независимую сверку.
