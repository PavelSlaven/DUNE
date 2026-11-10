## RECON-P8AR1 | Tue Nov 10 18:09:49 UTC 2026

## Чтение

- Отдельным вызовом целиком прочитан файл /srv/dune/tasks/load-check/PORT_PLAN.md. Прочитаны строка П8а в разделе 4 и пункт «П8а — игровые правки зданий» в разделе «Содержание шагов».
- Отдельным вызовом прочитан фрагмент карты переноса командой:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '687,757p'
~~~
Вывод:
~~~text
### placement-rule — Единое правило размещения зданий

Перенести общее правило размещения зданий и подключить его к режиму установки, подсказке и проверке игрока. Коммиты FORK1: e7a1c04f, a8a7f49a, 9ea227d2.

Пути кода и тестов; судьба в UP1:

- `src/controls/mousestates/cMousePlaceState.cpp` — изменён
- `src/controls/mousestates/cMousePlaceState.h` — изменён
- `src/drawers/cPlaceItDrawer.cpp` — изменён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `tests/PlacementRuleTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: нет

### refinery-dock — Стыковка Харвестера в центре площадки НПЗ

Перенести стыковку Харвестера в центре площадки НПЗ. Коммиты FORK1: c655ceb6, b6c58b8c.

Пути кода и тестов; судьба в UP1:

- `src/utils/WorldObjectScale.hpp` — отсутствует
- `tests/WorldObjectScaleTests.cpp` — отсутствует

Остальные пути по каталогу второго уровня: codex-direct/U23: 4; resources/bin: 1; tools/units3d: 1

### factory-pads — Площадки заводов: выезд юнитов, очередь, перевозчик, мигание, раздел сохранения FACTORYPADS

Перенести площадки заводов: выезд, очередь, перевозчик, мигание и раздел FACTORYPADS. Коммиты FORK1: 223f24c5, e39f6279, ac3c6b7d, e632b5e3, 90da98c4, 7bed86fc, 46b71484, 9e8a65e3, 00d15658, 5c2cda10, 29b3ca76, f2b5811e.

Пути кода и тестов; судьба в UP1:

- `CMakeLists.txt` — изменён
- `src/building/cItemBuilder.cpp` — изменён
- `src/building/cItemBuilder.h` — изменён
- `src/drawers/cStructureDrawer.cpp` — изменён
- `src/gameobjects/structures/FactoryPad.hpp` — отсутствует
- `src/gameobjects/structures/cAbstractStructure.cpp` — изменён
- `src/gameobjects/structures/cAbstractStructure.h` — изменён
- `src/gameobjects/structures/cHeavyFactory.cpp` — изменён
- `src/gameobjects/structures/cHeavyFactory.h` — изменён
- `src/gameobjects/structures/cLightFactory.cpp` — изменён
- `src/gameobjects/structures/cLightFactory.h` — изменён
- `src/gameobjects/structures/cUnitFactory.cpp` — отсутствует
- `src/gameobjects/structures/cUnitFactory.h` — отсутствует
- `src/gameobjects/units/cUnit.cpp` — изменён
- `src/gameobjects/units/cUnit.h` — изменён
- `src/save/SaveGameManager.cpp` — отсутствует
- `src/save/SaveGameManager.hpp` — отсутствует
- `src/utils/cStructureUtils.cpp` — изменён
- `src/utils/cStructureUtils.h` — изменён
- `tests/FactoryPadEngineTests.cpp` — отсутствует
- `tests/FactoryPadSaveTests.cpp` — отсутствует
- `tests/FactoryPadTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: корень: 1

### radar-dish — Тарелка Командного поста на 32 кадрах

Перенести анимацию тарелки Командного поста на 32 кадрах и её ресурсы. Коммиты FORK1: 3d3ff49e, 849650d0.

Пути кода и тестов; судьба в UP1:

- `src/gameobjects/structures/cOutPost.cpp` — изменён
- `tests/OutpostFrameTests.cpp` — отсутствует
- `tests/UnitRenderFixture.cmake` — отсутствует

Остальные пути по каталогу второго уровня: корень: 1; resources/bin: 1; resources/hd: 2; tools/building_angle: 3
~~~

- Отдельным вызовом прочитан фрагмент рисков:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '928,931p'
~~~
Вывод:
~~~text
- placement-rule: UP1 изменил `src/controls/mousestates/cMousePlaceState.cpp`; актуальная проверка размещения — `src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:98` (**cMousePlaceState::mayPlaceIt**).
- factory-pads: UP1 изменил `src/gameobjects/structures/cLightFactory.cpp`; логику площадки и выезда юнита нужно встроить в текущий вывод фабрики `src/gameobjects/structures/cLightFactory.cpp@d06f2fc:76` (**cLightFactory::draw**).
- radar-dish: UP1 изменил `src/gameobjects/structures/cOutPost.cpp`; вращение следует согласовать с текущей анимацией `src/gameobjects/structures/cOutPost.cpp@d06f2fc:51` (**cOutPost::think_animation**).
- refinery-dock: FORK1 вызывает `refineryHarvesterLayout` из `src/drawers/cStructureDrawer.cpp@9208dcf:880`; кодовые пути этой функции не изменены в BASE..UP1. UP1 рисует REFINERY через `src/drawers/cStructureDrawer.cpp@d06f2fc:316` (**cStructureDrawer::drawStructureForLayer**), который направляет его в `src/drawers/cStructureDrawer.cpp@d06f2fc:280` (**cStructureDrawer::drawStructureAnimationRefinery**). Путь потребителя не входит в запись refinery-dock.
~~~

- Отдельным вызовом целиком прочитаны решения владельца Р33, Р34 и Р63:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р(33|34|63)\.'
~~~
Вывод:
~~~text
- **Р33. Масштаб мира — это приближение камеры (#38).** Владелец 2026-11-02: «Масштаб = приближение». Масштаб мира (100, 110, 125, 150 % или авто) задаёт приближение камеры в начале миссии и после сброса клавишей Z; спрайты зданий, юнитов, частиц и снарядов на него больше не умножаются, поэтому земля, клетки и объекты увеличиваются вместе и здание стоит ровно на своих клетках. Спецификация — `codex-direct/U15/SPEC.md`.
- **Р34. Только HD-графика (#49).** Владелец 2026-11-02: «надо оставить только одну версию графики, максимальную. Остальные убрать просто». Игра всегда загружает паки HD4; режим «Классика», его выбор в окне настроек и откат на классические паки удалены; классические паки остаются в репозитории только как эталон для инструментов и в пакет игры не попадают.
- **Р63. Волна 4 — перенос форка на свежий апстрим.** Графика и перерисовка закончены; задача волны — перенести всё на новый код апстрима, сохранив наработки форка (Р4). Новая база UP1 — master апстрима в момент запуска первой задачи, d06f2fcd на 2026-11-09. Новые возможности апстрима (туман войны с памятью, значок нехватки энергии, предел юнитов, вступительный ролик, preferences.ini, папки музыки) берутся как есть; где новинка спорит с функцией форка, ведущий спрашивает владельца на шаге этой функции. Новых задач по графике нет; код и данные игры в main не меняются до перемотки на ветку порта, в main идут только документы процесса и карта переноса. Шаги П1–П15 — по карточке codex-direct/launch-card-27.md. Владелец, 2026-11-09, по карточке 27: «Свежий master», «Все как есть», «Мы закончили с графикой и перерисовкой. Теперь задача всё перенести на их новый код, сохранив наши наработки.»
~~~

Дополнительно прочитаны ссылки, на которые опирается PORT_PLAN.md: разделы 3.2 (перенос функций по одной, тесты функций форка как приёмочные) и 5.3 (сохранение тестов и числа проверок) файла docs/PLAN_units_sega_upstream.md; карточка запуска 27 codex-direct/launch-card-27.md прочитана целиком. Сначала полный вывод PLAN файла был помечен как усечённый, затем отдельным вызовом дочитаны требуемые разделы 3.2 и 5.3 целиком; карточка прочитана целиком отдельным вызовом. Эти ссылки прочитаны потому, что PORT_PLAN на них ссылается как на источник способа переноса и проверок. Других отсутствующих правил, норм или контрактов, от которых зависят действия разведки, не обнаружено.

## 1. Правило размещения в FORK1

### Коммиты и вывод `git show --stat`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat e7a1c04f
git show --stat a8a7f49a
git show --stat 9ea227d2
```

Вывод:

```text
commit e7a1c04f3cf11483db315cd977f313c4f21ca752
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 10:23:48 2026 +0300

    Use one placement rule for the preview, the click and the placement

    The placement preview, the click check and placeItem now ask the same
    rule: a regular building and SLAB1 need rock or slab under every cell,
    SLAB4 keeps its concrete exception, a structure blocks every type except
    SLAB4, and any unit blocks a regular building. A refused click keeps the
    item and the placement mode, plays no sound and shows the reason.

    Behavior changes: the preview, the click and the placement no longer
    disagree; a refused placement shows a message in Russian or English and
    the item stays ready to place.

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 src/controls/mousestates/cMousePlaceState.cpp | 160 +++++++++-------------
 src/controls/mousestates/cMousePlaceState.h   |   3 +-
 src/drawers/cPlaceItDrawer.cpp                | 112 +++-------------
 src/player/cPlayer.cpp                        |  91 ++++++++++++-
 src/player/cPlayer.h                          |   3 +
 tests/PlacementRuleTests.cpp                  | 184 ++++++++++++++++++++++++++
 tests/UnitRenderFixture.cmake                 |   2 +
 7 files changed, 360 insertions(+), 195 deletions(-)
commit a8a7f49aa96d123c732b36cb632d1b533395bb5a
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 10:58:37 2026 +0300

    Keep the AI's building placement as it was before the unified rule

    placeItem applied the player's placement rule to the AI as well, so the
    AI was refused on rock without a construction link and dropped the
    order. The AI again uses the check it had before; the player keeps the
    unified rule. The placement test now covers all 21 combinations of item
    and cell for the player and the AI case on unlinked rock.

    Behavior changes: the AI places buildings as before this branch.

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 src/player/cPlayer.cpp       |   8 ++-
 tests/PlacementRuleTests.cpp | 154 ++++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 157 insertions(+), 5 deletions(-)
commit 9ea227d20c77fb6d7d655f82c9b2877b36436266
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 10:58:37 2026 +0300

    Name the structure limit in the refused placement message

    Behavior changes: the message for a full structure list now says that
    the structure limit has been reached instead of "no free space".

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 src/controls/mousestates/cMousePlaceState.cpp | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

### Участки `src/` и добавленные/изменённые символы

Команды чтения: `git show --format=fuller e7a1c04f -- src/controls/mousestates/cMousePlaceState.cpp src/controls/mousestates/cMousePlaceState.h src/drawers/cPlaceItDrawer.cpp src/player/cPlayer.cpp src/player/cPlayer.h`, далее `git show --format=fuller a8a7f49a -- src/player/cPlayer.cpp` и `git show --format=fuller 9ea227d2 -- src/controls/mousestates/cMousePlaceState.cpp`; строки сверены командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> | nl -ba`.

| Коммит | Участок FORK1 | Изменение |
|---|---|---|
| `e7a1c04f` | `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:58` | Обработчик клика получает `s_PlaceResult`, вызывает общую проверку, показывает локализованную причину отказа; отказ сохраняет выбранный предмет и режим размещения, успешный вызов играет звук и возвращает состояние. |
| `e7a1c04f` | `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:114` | `mayPlaceIt` перестаёт повторять геометрические правила и делегирует `canPlaceBuildingListItemAt`, возвращая `placement.success`. |
| `e7a1c04f` | `src/controls/mousestates/cMousePlaceState.h@9208dcf:12` и `:40` | Добавлены forward declaration `s_PlaceResult` и необязательный выходной указатель в сигнатуру `mayPlaceIt`. |
| `e7a1c04f` | `src/drawers/cPlaceItDrawer.cpp@9208dcf:45` | Предпросмотр вызывает ту же `canPlaceBuildingListItemAt`; клетки пятна получают нейтральный/хороший цвет при успехе и плохой при отказе. |
| `e7a1c04f` | `src/player/cPlayer.cpp@9208dcf:1507` | `placeItem` добавляет защиту от null и использует новую общую проверку до создания постройки; после безуспешного создания обычной постройки не расходует предмет. |
| `e7a1c04f` | `src/player/cPlayer.cpp@9208dcf:2012` | Добавлен `canPlaceBuildingListItemAt`: проверяет корректность типа и клетки, габариты/границы, поверхность, занятость строениями и юнитами, а также якорь строительства в соседней области. |
| `e7a1c04f` | `src/player/cPlayer.h@9208dcf:63` | `s_PlaceResult` получает поле `outOfBuildDistance`. |
| `e7a1c04f` | `src/player/cPlayer.h@9208dcf:438` | В публичный API `cPlayer` добавлено объявление `canPlaceBuildingListItemAt(int iCell, int iStructureType)`. |
| `a8a7f49a` | `src/player/cPlayer.cpp@9208dcf:1516` | `placeItem` выбирает правило по `isHuman()`: для человека — новое `canPlaceBuildingListItemAt`, для ИИ — прежнее `canPlaceStructureAt`; отказ создания объекта защищает только человеческий путь. |
| `9ea227d2` | `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:64` | Текст причины при `result.success` заменён на сообщение о достигнутом лимите построек (английский и русский варианты). |

Точные начала diff-hunks из `git show --format= --unified=0`:

```text
e7a1c04f, src/controls/mousestates/cMousePlaceState.cpp: +7, +8, +58, +95, +101, +110, +120, +124
e7a1c04f, src/controls/mousestates/cMousePlaceState.h: +12, +40
e7a1c04f, src/drawers/cPlaceItDrawer.cpp: +45, +48, +51, +55, +62
e7a1c04f, src/player/cPlayer.cpp: +1509, +1516, +1539, +2008
e7a1c04f, src/player/cPlayer.h: +63, +438
a8a7f49a, src/player/cPlayer.cpp: +1516, +1543
9ea227d2, src/controls/mousestates/cMousePlaceState.cpp: +64
```

По одному смыслу на каждый hunk: `cMousePlaceState.cpp@9208dcf:7` добавляет Localization include; `:8` удаляет старые MapGeometry/algorithm include; `:58` добавляет классификацию причин и локализованное уведомление; `:95` связывает click с общей проверкой и результатом `placeItem`; `:101`, `:110`, `:120`, `:124` заменяют прежнюю геометрическую реализацию `mayPlaceIt` на передачу результата `canPlaceBuildingListItemAt`. В заголовке `cMousePlaceState.h@9208dcf:12` forward-declare-ится результат, `:40` меняется сигнатура helper-а. В `cPlaceItDrawer.cpp@9208dcf:45` вызывается общий validator, `:48`, `:51`, `:55` убирают прежние проверки соседства/footprint, `:62` рисует клетки по общей проверке. В `cPlayer.cpp@9208dcf:1509` добавляется null-item guard, `:1516` вызывается общая проверка, `:1539` добавляется возврат при неудачном создании обычного объекта, `:2008` начинается вставка новой функции (её определение находится на `:2012`). В `cPlayer.h@9208dcf:63` добавляется поле результата и на `:438` объявление функции. `a8a7f49a` на `cPlayer.cpp@9208dcf:1516` разводит человеческий и AI validator, на `:1543` делает null-return guard только для человека. `9ea227d2` меняет текст лимита на `cMousePlaceState.cpp@9208dcf:64`.

Команды для этих границ: `git show --format= --unified=0 e7a1c04f -- src/controls/mousestates/cMousePlaceState.cpp src/controls/mousestates/cMousePlaceState.h src/drawers/cPlaceItDrawer.cpp src/player/cPlayer.cpp src/player/cPlayer.h`, `git show --format= --unified=0 a8a7f49a -- src/player/cPlayer.cpp`, `git show --format= --unified=0 9ea227d2 -- src/controls/mousestates/cMousePlaceState.cpp`.

Определение/контракт правила:

- `s_PlaceResult` — `src/player/cPlayer.h@9208dcf:51`; поля: `success`, `badTerrain`, `outOfBounds`, `outOfBuildDistance`, блокирующие `unitIds` и `structureIds` (`:52-69`).
- `cPlayer::canPlaceBuildingListItemAt(int iCell, int iStructureType)` — `src/player/cPlayer.cpp@9208dcf:2012`; входы — клетка и тип; выход — `s_PlaceResult`. Успех требует отсутствия выходов за границы, неподходящего рельефа, блокирующих юнитов/строений и наличия строительной связи (`:2016-2089`). Исключения в коде: `SLAB4` пропускает проверку рельефа и занятости строением, `SLAB1` и `SLAB4` не блокируются юнитом (`:2041-2053`).
- `cMousePlaceState::mayPlaceIt(cBuildingListItem*, int, s_PlaceResult*)` — `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:114`; входы — предмет, клетка и необязательный указатель; выход — bool, при указателе также копирует `s_PlaceResult` (`:116-124`).
- Лямбда `notifyPlacementFailure(const s_PlaceResult&)` — `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:58`; вход — результат, выход — уведомление `BAD` с локализованной причиной (`:59-92`). Текст про лимит задаётся строками `Cannot place another structure: the structure limit has been reached.` и `Нельзя поставить ещё одну постройку: достигнут лимит построек.` — `src/controls/mousestates/cMousePlaceState.cpp@9208dcf:64-66`.
- `cPlayer::placeItem(int destinationCell, cBuildingListItem*)` — `src/player/cPlayer.cpp@9208dcf:1507`; входы — клетка и предмет списка; выход — указатель на структуру либо `nullptr`; применяет человеческое/ИИ правило после `a8a7f49a` (`:1516-1521`).

Команды/выводы поиска мест вызова: `git grep -n -E 'canPlaceBuildingListItemAt|mayPlaceIt|notifyPlacementFailure|s_PlaceResult|placeItem\(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src` и `git grep -n 'canPlaceBuildingListItemAt' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src`.

```text
src/controls/mousestates/cMousePlaceState.cpp:58:    const auto notifyPlacementFailure = [this](const s_PlaceResult &result) {
src/controls/mousestates/cMousePlaceState.cpp:95:    s_PlaceResult result;
src/controls/mousestates/cMousePlaceState.cpp:96:    if (!mayPlaceIt(itemToPlace, mouseCell, &result)) {
src/controls/mousestates/cMousePlaceState.cpp:97:        notifyPlacementFailure(result);
src/controls/mousestates/cMousePlaceState.cpp:102:    cAbstractStructure *placed = m_player->placeItem(mouseCell, itemToPlace);
src/controls/mousestates/cMousePlaceState.cpp:105:        result = m_player->canPlaceBuildingListItemAt(mouseCell, structureType);
src/controls/mousestates/cMousePlaceState.cpp:106:        notifyPlacementFailure(result);
src/controls/mousestates/cMousePlaceState.cpp:114:bool cMousePlaceState::mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result)
src/controls/mousestates/cMousePlaceState.cpp:120:    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, itemToPlace->getBuildId());
src/controls/mousestates/cMousePlaceState.h:12:struct s_PlaceResult;
src/controls/mousestates/cMousePlaceState.h:40:    bool mayPlaceIt(cBuildingListItem *itemToPlace, int mouseCell, s_PlaceResult *result = nullptr);
src/drawers/cPlaceItDrawer.cpp:45:    const s_PlaceResult placement = player->canPlaceBuildingListItemAt(mouseCell, structureId);
src/player/brains/cPlayerBrainCampaign.cpp:1685:                player->placeItem(iCll, pItem);
src/player/brains/cPlayerBrainSkirmish.cpp:1120:            const s_PlaceResult &placeResult = player->canPlaceStructureAt(iCll, pItem->getBuildId());
src/player/brains/cPlayerBrainSkirmish.cpp:1123:                player->placeItem(iCll, pItem);
src/player/cPlayer.cpp:1507:cAbstractStructure *cPlayer::placeItem(int destinationCell, cBuildingListItem *itemToPlace)
src/player/cPlayer.cpp:1518:                          ? canPlaceBuildingListItemAt(destinationCell, iStructureTypeId).success
src/player/cPlayer.cpp:2012:s_PlaceResult cPlayer::canPlaceBuildingListItemAt(int iCell, int iStructureType)
src/player/cPlayer.h:438:    s_PlaceResult canPlaceBuildingListItemAt(int iCell, int iStructureType);
```

## TSV: placement.tsv

```tsv
коммит_или_символ	путь@9208dcf:строка	что делает одной строкой	входы	выходы	места вызова
e7a1c04f	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:58	Объединяет click/preview/place вокруг общего результата и показывает причину отказа.	mouseCell, cBuildingListItem*, s_PlaceResult	размещение или отказ-уведомление	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:96,97,102,106; src/drawers/cPlaceItDrawer.cpp@9208dcf:45; src/player/cPlayer.cpp@9208dcf:1518
a8a7f49a	src/player/cPlayer.cpp@9208dcf:1516	Оставляет для AI прежнюю canPlaceStructureAt, а для человека использует общий validator.	isHuman, destinationCell, structure type	bool canPlace	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:102; src/player/brains/cPlayerBrainCampaign.cpp@9208dcf:1685; src/player/brains/cPlayerBrainSkirmish.cpp@9208dcf:1123
9ea227d2	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:64	Меняет причину отказа на явно названный достигнутый лимит построек.	result.success	локализованная строка	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:97,106
s_PlaceResult outOfBuildDistance	src/player/cPlayer.h@9208dcf:63	Добавлен флаг отсутствия строительной связи.	—	поле результата	читается в src/controls/mousestates/cMousePlaceState.cpp@9208dcf:87-90; выставляется в src/player/cPlayer.cpp@9208dcf:2085
cPlayer::canPlaceBuildingListItemAt	src/player/cPlayer.cpp@9208dcf:2012	Единая проверка типа клетки, terrain, границ, blockers и строительного якоря.	iCell, iStructureType	s_PlaceResult	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:105,120; src/drawers/cPlaceItDrawer.cpp@9208dcf:45; src/player/cPlayer.cpp@9208dcf:1518
cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:114	Адаптер click-check к общей функции размещения.	itemToPlace, mouseCell, необязательный s_PlaceResult*	bool и при указателе записанный результат	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:96
notifyPlacementFailure	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:58	Выбирает локализованную причину и отправляет BAD-уведомление.	s_PlaceResult	уведомление	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:97,106
cPlayer::placeItem	src/player/cPlayer.cpp@9208dcf:1507,1543	Применяет человеческое unified rule либо AI legacy rule; при null-результате создания сохраняет готовый item.	destinationCell, cBuildingListItem*	cAbstractStructure* или nullptr	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:102; src/player/brains/cPlayerBrainCampaign.cpp@9208dcf:1685; src/player/brains/cPlayerBrainSkirmish.cpp@9208dcf:1123
placement-limit message	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:64	Показывает английский/русский текст о достигнутом лимите построек.	result.success	локализованная строка	src/controls/mousestates/cMousePlaceState.cpp@9208dcf:97,106 через notifyPlacementFailure
```

## 2. Размещение в PORT

### Условия в указанных исходниках

Команды: `git show 832c953a94a632d57872349013f7ed1a37434715:<путь> | nl -ba` для четырёх заданных путей; `git grep -n -E 'canPlace|mayPlace|placeStructure' 832c953a94a632d57872349013f7ed1a37434715 -- src`.

- `cMousePlaceState::onMouseLeftButtonClicked` — `src/controls/mousestates/cMousePlaceState.cpp@832c953:72-96`: сначала требует `mayPlaceIt`; отдельно отказывает при достигнутом лимите, кроме действий, меняющих поверхность, показывает `Unable to create more.` и не закрывает режим (`:86-90`).
- `cMousePlaceState::mayPlaceIt` — `src/controls/mousestates/cMousePlaceState.cpp@832c953:98-203`:
  - `:101-103` — отрицательная клетка отклоняется.
  - `:108-162` — ищет строительный якорь в области размера footprint плюс `SCANWIDTH=1`; якорем служит своё строение либо `TERRAIN_WALL`/`TERRAIN_SLAB` (`:129-155`). Если встретилось чужое строение, его фундамент не считается якорем (`:135-148`).
  - `:164-165` — без якоря отклоняет размещение.
  - `:168-175` — каждая footprint-клетка должна быть внутри границ.
  - `:179-185` — занятое строением место блокирует всё, кроме `SLAB4`.
  - `:188-197` — занятый живым юнитом footprint блокируется для всех типов, кроме `SLAB4`; мёртвый юнит не препятствует (`:189-195`).
- `cPlaceItDrawer::drawStatusOfStructureAtCell` — `src/drawers/cPlaceItDrawer.cpp@832c953:70-185`: визуально повторяет проверку строительного якоря и footprint; без якоря рисует нейтральный цвет (`:99-136`); для клеток пятна неподходящая/непроходимая поверхность окрашивается в плохой цвет, slab — в хороший (`:139-158`); занятое строением и живым юнитом пятно окрашивается в плохой (`:160-172`). Это расчёт цвета предпросмотра.
- Перегрузка `cPlayer::canPlaceStructureAt(iCell, iStructureType)` — `src/gameobjects/players/cPlayer.cpp@832c953:1950-1957`: `SLAB4` направляется в `canPlaceConcreteAt`, остальные типы — в перегрузку с третьим параметром `-1`.
- `cPlayer::canPlaceStructureAt(iCell, iStructureType, iUnitIDToIgnore)` — `src/gameobjects/players/cPlayer.cpp@832c953:1986-2039`:
  - `:1990-1993` — начальная клетка должна быть допустимой.
  - `:1995-2010` — обходит габариты по `bmp_width/height`; непригодная поверхность помечает `badTerrain`.
  - `:2012-2016` — любое существующее строение в клетке добавляется в `structureIds`.
  - `:2018-2030` — проверяет unit layer; учитывает валидность/владельца при `foundUnitFromOtherPlayerThanMe` и исключает только `iUnitIDToIgnore` из `unitIds`.
  - `:2035-2036` — успех означает пригодный рельеф и пустые множества блокирующих юнитов/строений; отдельно задаётся `onlyMyUnitsBlock`.
- `cPlayer::canPlaceConcreteAt` — `src/gameobjects/players/cPlayer.cpp@832c953:2205-2218`: для slab4 проверяет валидность клетки и затем возвращает успех.
- `cPlayer::placeStructure` — `src/gameobjects/players/cPlayer.cpp@832c953:1573-1589`: повторно требует `canPlaceStructureAt(...).success` (`:1576-1579`) и свободный лимит построек, кроме изменения поверхности (`:1581-1583`).
- `cPlayer::canBuildStructure` — `src/gameobjects/players/cPlayer.cpp@832c953:1523-1566`: проверяет допустимость начала строительства; среди причин отказа — достигнутый лимит построек (`:1563-1565`), исключая SLAB1/SLAB4/WALL через `isModifyingTerrain`; это проверка очереди/допуска без конкретной клетки.
- `cPlayer::placeItem` — `src/gameobjects/players/cPlayer.cpp@832c953:1598-1635`: повторно требует `canPlaceStructureAt(...).success` (`:1603-1606`) и лимит строений, кроме изменения поверхности (`:1608-1611`); затем создаёт объект и расходует предмет списка (`:1627-1635`).


Построчная сверка предикатов выполнялась командами `git grep -n -E 'if \(|SCANWIDTH|TERRAIN_WALL|TERRAIN_SLAB|isStructureLimitReached|isModifyingTerrain|isWithinBoundaries|isDead' 832c953a94a632d57872349013f7ed1a37434715 -- src/controls/mousestates/cMousePlaceState.cpp`, та же команда с `src/drawers/cPlaceItDrawer.cpp`, и `git grep -n -E 'isStructureLimitReached|isModifyingTerrain|isValidCell|isValidTerrainForStructureAtCell|getCellIdStructuresLayer|getCellIdUnitLayer|result\.success|result\.onlyMyUnitsBlock|iStructureType != SLAB4' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/players/cPlayer.cpp`.

Ниже приведены релевантные строки выдачи (в исходном выводе перед каждой строкой стоит `832c953a94a632d57872349013f7ed1a37434715:`):

```text
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:87:        if (m_context->getObjects()->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(itemToPlace->getBuildId())) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:101:    if (mouseCell < 0) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:113:#define SCANWIDTH    1
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:139:                    if (m_context->getObjects()->getStructures()[iID]->getOwner() == m_player->getId()) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:151:                if (m_context->getObjects()->getMap()->getCellType(iCll) == TERRAIN_WALL ||
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:152:                        m_context->getObjects()->getMap()->getCellType(iCll) == TERRAIN_SLAB) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:164:    if (!bWithinBuildDistance) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:173:            if (!m_context->getObjects()->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:181:            if (idOfStructureAtCell > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:183:                if (structureIdToPlace != SLAB4) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:189:            if (structureIdToPlace != SLAB4) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:191:                if (unitIdOnMap > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMousePlaceState.cpp:193:                    if (!m_context->getObjects()->getUnit(unitIdOnMap)->isDead()) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:83:#define SCANWIDTH	1
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:109:                    if (m_objects->getStructures()[iID]->getOwner() == m_player->getId()) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:121:                if (m_objects->getMap()->getCellType(iCll) == TERRAIN_WALL ||
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:122:                        m_objects->getMap()->getCellType(iCll) == TERRAIN_SLAB) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:134:    if (!bWithinBuildDistance) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:146:                if (!m_objects->getMapGeometry()->isWithinBoundaries(cellX, cellY)) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:152:                if (!m_objects->getMap()->isCellPassable(iCll) || m_objects->getMap()->getCellType(iCll) != TERRAIN_ROCK) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:156:                if (m_objects->getMap()->getCellType(iCll) == TERRAIN_SLAB) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:162:                if (idOfStructureAtCell > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:167:                if (unitIdOnMap > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cPlaceItDrawer.cpp:169:                    if (!m_objects->getUnit(unitIdOnMap)->isDead()) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1563:    if (m_objects->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(iStructureType)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1576:    bool canPlace = canPlaceStructureAt(destinationCell, iStructureTypeId).success;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1581:    if (pStructureFactory->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(iStructureTypeId)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1603:    bool canPlace = canPlaceStructureAt(destinationCell, iStructureTypeId).success;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1609:    if (m_objects->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(iStructureTypeId)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1952:    if (iStructureType != SLAB4) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:1990:    if (!m_objects->getMapGeometry()->isValidCell(iCell)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2008:            if (!result.badTerrain && !m_objects->getMap()->isValidTerrainForStructureAtCell(cll)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2013:            int structureId = m_objects->getMap()->getCellIdStructuresLayer(cll);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2018:            int idOfUnitAtCell = m_objects->getMap()->getCellIdUnitLayer(cll);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2014:            if (structureId > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2019:            if (idOfUnitAtCell > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2021:                    foundUnitFromOtherPlayerThanMe = true;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2023:                if (iUnitIDToIgnore > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2024:                    if (idOfUnitAtCell != iUnitIDToIgnore) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2035:    result.success = (result.badTerrain == false && result.unitIds.empty() && result.structureIds.empty());
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2036:    result.onlyMyUnitsBlock = (result.badTerrain == false && !foundUnitFromOtherPlayerThanMe && result.structureIds.empty());
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2209:    if (!m_objects->getMapGeometry()->isValidCell(iCell)) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2214:    result.success = true;
```

`git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '1523,1566p'` подтверждает, что лимит в `:1563` находится в `cPlayer::canBuildStructure`; это допуск к началу строительства вместе с проверками денег, CONSTYARD, занятости строительства и доступности типа (`:1536-1565`), а проверки конкретной клетки выполняют перечисленные выше `canPlaceStructureAt`/`placeItem`.

`git grep -n -E 'if \(structureId > -1\)|if \(idOfUnitAtCell > -1\)|foundUnitFromOtherPlayerThanMe|iUnitIDToIgnore' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/players/cPlayer.cpp` выводит также точные условия occupancy:

```text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2014:            if (structureId > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2019:            if (idOfUnitAtCell > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2021:                    foundUnitFromOtherPlayerThanMe = true;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2023:                if (iUnitIDToIgnore > -1) {
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:2024:                    if (idOfUnitAtCell != iUnitIDToIgnore) {
```

Команда `git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp | nl -ba | sed -n '1523p;1563,1565p'` даёт:

```text
  1523 eCantBuildReason cPlayer::canBuildStructure(int iStructureType)
  1563     if (m_objects->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(iStructureType)) {
  1564         log("canBuildStructure: FALSE, reason STRUCTURE_LIMIT_REACHED");
  1565         return eCantBuildReason::STRUCTURE_LIMIT_REACHED;
```

### Вызовы размещения ИИ

Основной поиск, запрошенный в брифе, выполнен командой `git grep -n 'canPlace\|mayPlace\|placeStructure' 832c953a94a632d57872349013f7ed1a37434715 -- src`; отфильтрованное AI-совпадение в его выводе:

```text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1183:            const s_PlaceResult &placeResult = player->canPlaceStructureAt(iCll, pItem->getBuildId());
```

Это внутри `cPlayerBrainSkirmish::thinkState_ProcessBuildOrders`. Контекст из `git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp | nl -ba` показывает enclosing function `cPlayerBrainSkirmish::thinkState_ProcessBuildOrders` (начало строки 1071); после `placeResult.success` и проверки лимита выполняется `placeItem` (строки 1185-1189). Команда `git grep -n 'placeItem' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/players/brains` дала оба места размещения: `src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1739` и `src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1188`. Контекст первой строки — `cPlayerBrainCampaign::thinkState_ProcessBuildOrders` (начало строки 1682); перед вызовом лимит проверяется на строке 1737. В обоих случаях конечный метод `cPlayer::placeItem` снова вызывает `canPlaceStructureAt` и проверяет лимит.

Сверка функций/контекста через `git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp | nl -ba | sed -n '1071p;1183p;1185p;1187,1188p'` и `git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp | nl -ba | sed -n '1682p;1735p;1737p;1739p' дала:

```text
  1071 void cPlayerBrainSkirmish::thinkState_ProcessBuildOrders()
  1183             const s_PlaceResult &placeResult = player->canPlaceStructureAt(iCll, pItem->getBuildId());
  1185             if (placeResult.success) {
  1187                 if (!m_objects->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(pItem->getBuildId())) {
  1188                     player->placeItem(iCll, pItem);
  1682 void cPlayerBrainCampaign::thinkState_ProcessBuildOrders()
  1735                 cBuildingListItem *pItem = player->getStructureBuildingListItemBeingBuilt();
  1737                 if (m_objects->getStructureFactory()->isStructureLimitReached() && !cStructureFactory::isModifyingTerrain(structureType)) break;
  1739                 player->placeItem(iCll, pItem);
```

Поиск `placeItem` в brain-коде дал:

```text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1739:                player->placeItem(iCll, pItem);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1188:                    player->placeItem(iCll, pItem);
```

### Участки `BASE..UP1`

Команда и вывод hunks (`+N` — первая строка участка в `UP1`): `git diff e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/controls/mousestates/cMousePlaceState.cpp src/drawers/cPlaceItDrawer.cpp`.

```text
src/controls/mousestates/cMousePlaceState.cpp
@d06f2fc:1    добавлены заголовочный комментарий, новые include и проверки аргументов конструктора.
@d06f2fc:65   исправлено имя поля mouseTile на m_mouseTile.
@d06f2fc:84   в обработчик клика добавлена проверка лимита строений и сообщение; звук переведён на AudioContext.
@d06f2fc:103  assert и получение габаритов переведены на API порта.
@d06f2fc:123  координаты границ соседней области получают через MapGeometry контекста.
@d06f2fc:132  получение клетки в области переведено на MapGeometry контекста.
@d06f2fc:135  чтение occupancy слоя строений переведено на объект карты.
@d06f2fc:139  проверка якоря использует owner игрока через контекст, вместо HUMAN.
@d06f2fc:145  чужое строение пропускает проверку slab под ним как якоря.
@d06f2fc:151  проверка wall/slab якоря переведена на объект карты.
@d06f2fc:170  проверка границ footprint переведена на MapGeometry контекста.
@d06f2fc:177  генерация клетки footprint переведена на MapGeometry контекста.
@d06f2fc:180  чтение occupancy строений переведено на объект карты.
@d06f2fc:186  SLAB1 перестаёт обходить unit-check; SLAB4 остаётся исключением.
@d06f2fc:193  проверка живого юнита переведена с массива на контекст объектов.
@d06f2fc:225  имя mouseTile исправлено на m_mouseTile в установке состояния.
@d06f2fc:239  имя mouseTile исправлено на m_mouseTile при фокусе.

src/drawers/cPlaceItDrawer.cpp
@d06f2fc:1    добавлены заголовочный комментарий, include, зависимости контекста, проверки конструктора и serviceInit.
@d06f2fc:63   отрисовка передаёт mouseCell в функцию спрайта.
@d06f2fc:72   assert заменён на d2tm_assert.
@d06f2fc:77   assert идентификатора заменён на d2tm_assert.
@d06f2fc:80   размеры структуры берутся через m_structureUtils.
@d06f2fc:85   координаты клетки берутся из MapGeometry.
@d06f2fc:93   геометрия области сканирования берётся из MapGeometry контекста.
@d06f2fc:128  весь расчёт предпросмотра и отрисовка используют объекты/контекст вместо глобалов; чужое здание исключено из wall/slab якорей; изменены цвета предпросмотра; drawStructureIdAtMousePos получает mouseCell.
```

## TSV: port-placement.tsv

```tsv
ревизия	функция или участок	путь@ревизия:строка	что проверяет или меняет
832c953	cMousePlaceState::onMouseLeftButtonClicked	src/controls/mousestates/cMousePlaceState.cpp@832c953:72-96	mayPlaceIt и отдельный limit-check; при полном лимите сообщает Unable to create more и оставляет режим активным.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:101-103	Отклоняет отрицательную клетку.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:108-162	Ищет собственное строение или wall/slab как строительный якорь в пределах footprint + SCANWIDTH.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:135-148	Чужое строение не засчитывает как slab/wall якорь.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:164-165	Отклоняет placement без якоря.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:168-175	Отклоняет footprint за границами карты.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:179-185	Блокирует занятое строением место, кроме SLAB4.
832c953	cMousePlaceState::mayPlaceIt	src/controls/mousestates/cMousePlaceState.cpp@832c953:188-197	Блокирует живой юнит для всех типов, кроме SLAB4.
832c953	cPlaceItDrawer::drawStatusOfStructureAtCell	src/drawers/cPlaceItDrawer.cpp@832c953:99-136	Отображает якорь строительства: свой объект либо wall/slab, чужой объект пропускает.
832c953	cPlaceItDrawer::drawStatusOfStructureAtCell	src/drawers/cPlaceItDrawer.cpp@832c953:139-158	Предпросмотр красит неподходящий terrain/непроходимую клетку плохо, slab хорошо.
832c953	cPlaceItDrawer::drawStatusOfStructureAtCell	src/drawers/cPlaceItDrawer.cpp@832c953:160-172	Предпросмотр красит занятое строением или живым юнитом footprint плохо.
832c953	cPlayer::canPlaceStructureAt(iCell,type)	src/gameobjects/players/cPlayer.cpp@832c953:1950-1957	Направляет SLAB4 в canPlaceConcreteAt, прочие типы — в перегрузку с iUnitIDToIgnore=-1.
832c953	cPlayer::canPlaceStructureAt(iCell,type,ignore)	src/gameobjects/players/cPlayer.cpp@832c953:1990-1993	Проверяет валидность начальной клетки.
832c953	cPlayer::canPlaceStructureAt(iCell,type,ignore)	src/gameobjects/players/cPlayer.cpp@832c953:1995-2010	Проверяет terrain каждой footprint-клетки.
832c953	cPlayer::canPlaceStructureAt(iCell,type,ignore)	src/gameobjects/players/cPlayer.cpp@832c953:2012-2016	Считает любое существующее строение blocker-ом.
832c953	cPlayer::canPlaceStructureAt(iCell,type,ignore)	src/gameobjects/players/cPlayer.cpp@832c953:2018-2030	Собирает блокирующих юнитов с исключением iUnitIDToIgnore.
832c953	cPlayer::canPlaceStructureAt(iCell,type,ignore)	src/gameobjects/players/cPlayer.cpp@832c953:2035-2036	Составляет success и onlyMyUnitsBlock по terrain и blocker-множествам.
832c953	cPlayer::canPlaceConcreteAt	src/gameobjects/players/cPlayer.cpp@832c953:2205-2218	Проверяет только валидность клетки, затем возвращает success.
832c953	cPlayer::placeStructure	src/gameobjects/players/cPlayer.cpp@832c953:1573-1589	Проверяет canPlaceStructureAt и лимит строений, исключая изменение terrain.
832c953	cPlayer::canBuildStructure	src/gameobjects/players/cPlayer.cpp@832c953:1523-1566	Проверяет допуск к началу строительства и возвращает STRUCTURE_LIMIT_REACHED при достигнутом лимите (клетку не проверяет).
832c953	cPlayer::placeItem	src/gameobjects/players/cPlayer.cpp@832c953:1598-1611	Проверяет canPlaceStructureAt и лимит строений, исключая изменение terrain.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:1	Добавлены boilerplate/include, зависимости контекста и d2tm_assert конструктора.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:65	Переименование mouseTile в m_mouseTile.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:84	Добавлена проверка лимита перед звуком/размещением; sound берётся из AudioContext.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:103	assert и получение размеров переведены на API контекста.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:123	Границы scan area нормализуются через MapGeometry.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:132	Поиск клетки scan area переведён на MapGeometry.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:135	Чтение структуры из map layer переведено на cMap.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:139	Проверка собственного owner переведена с HUMAN на player id.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:145	Фундамент чужого строения не проходит как wall/slab якорь.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:151	Чтение terrain якоря переведено на cMap.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:170	Проверка границ footprint переведена на MapGeometry.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:177	Создание cell id footprint переведено на MapGeometry.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:180	Проверка структуры на footprint переведена на cMap.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:186	Условие меняет поведение: SLAB1 теперь тоже блокируется unit-check.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:193	Проверка мёртвого/живого юнита обращается через cGameObjectContext.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:225	Переименование mouseTile в m_mouseTile при смене состояния.
d06f2fc	mouse hunk	src/controls/mousestates/cMousePlaceState.cpp@d06f2fc:239	Переименование mouseTile в m_mouseTile при возврате фокуса.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:1	Добавлены boilerplate/include, зависимости контекста, проверки конструктора и serviceInit.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:63	draw передаёт mouseCell в drawStructureIdAtMousePos.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:72	assert itemToPlace заменён на d2tm_assert.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:77	assert structureId заменён на d2tm_assert.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:80	Габариты берутся из m_structureUtils.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:85	Координаты клетки берутся через MapGeometry контекста.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:93	Область scan вычисляется через MapGeometry контекста.
d06f2fc	drawer hunk	src/drawers/cPlaceItDrawer.cpp@d06f2fc:128	Расчёт предпросмотра, tint и отрисовка используют объекты/контекст вместо глобалов; чужое здание исключено из якоря; drawStructureIdAtMousePos получает mouseCell.
```

## 3. Стыковка у НПЗ

### Коммит `c655ceb6`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat c655ceb6
```

Вывод:

```text
commit c655ceb600abc910beef8c926f48839c5d1d2534
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 00:22:28 2026 +0300

    Redraw the Harvester from the owner's 3D model and centre it on the refinery pad
    
    All eight directions are painted over renders of one 3D model, so the
    vehicle keeps its shape when it turns. The House colour covers the rear
    roof, the cab with its hatch and, at 7 and 11 o'clock, the rear roof strip
    around its lamps. The docked Harvester is moved so its body sits in the
    middle of the refinery pad.
    
    Behavior changes: new Harvester body, shadow and House mask atlases in
    sdl_data_hd4.dat; a Harvester docked at a refinery is drawn 3.25 logical px
    further left and 2.375 logical px lower.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 codex-direct/U23/JOURNAL.md                    |  30 +++
 codex-direct/U23/fade.py                       | 175 ++++++++++++++++
 codex-direct/U23/gen/UNIT_HARVESTER.SHA256SUMS | 104 ++++++++++
 codex-direct/U23/shift.py                      |  46 +++++
 resources/bin/data/sdl_data_hd4.dat            |   4 +-
 src/utils/WorldObjectScale.hpp                 |   6 +-
 tests/WorldObjectScaleTests.cpp                |  16 +-
 tools/units3d/units/UNIT_HARVESTER/unit.json   | 268 +++++++++++++------------
 8 files changed, 506 insertions(+), 143 deletions(-)
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show c655ceb6 -- src/
```

Вывод:

```diff
commit c655ceb600abc910beef8c926f48839c5d1d2534
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 00:22:28 2026 +0300

    Redraw the Harvester from the owner's 3D model and centre it on the refinery pad
    
    All eight directions are painted over renders of one 3D model, so the
    vehicle keeps its shape when it turns. The House colour covers the rear
    roof, the cab with its hatch and, at 7 and 11 o'clock, the rear roof strip
    around its lamps. The docked Harvester is moved so its body sits in the
    middle of the refinery pad.
    
    Behavior changes: new Harvester body, shadow and House mask atlases in
    sdl_data_hd4.dat; a Harvester docked at a refinery is drawn 3.25 logical px
    further left and 2.375 logical px lower.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/src/utils/WorldObjectScale.hpp b/src/utils/WorldObjectScale.hpp
index 36d7f7fa..4b7ff5b7 100644
--- a/src/utils/WorldObjectScale.hpp
+++ b/src/utils/WorldObjectScale.hpp
@@ -13,7 +13,7 @@ struct WorldObjectLayout {
 /**
  * Keep the harvester on the refinery pad at exactly the same visual scale
  * as the unit uses on the map.  The transparent 80x52 unit frame extends
- * beyond the pad, while its visible south-facing body stays on the deck.
+ * beyond the pad, while its visible south-facing body is centred on the deck.
  */
 inline WorldObjectLayout refineryHarvesterLayout(
     int refineryX,
@@ -23,8 +23,8 @@ inline WorldObjectLayout refineryHarvesterLayout(
 {
     constexpr float logicalRefineryWidth = 96.0F;
     constexpr float logicalRefineryHeight = 64.0F;
-    constexpr float logicalOffsetX = 30.0F;
-    constexpr float logicalOffsetY = 15.0F;
+    constexpr float logicalOffsetX = 26.75F;
+    constexpr float logicalOffsetY = 17.375F;
     constexpr float logicalHarvesterWidth = 80.0F;
     constexpr float logicalHarvesterHeight = 52.0F;
     return {
```

### Коммит `b6c58b8c`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat b6c58b8c
```

Вывод:

```text
commit b6c58b8c7dad1a37a742b33facfab43c79f12c5a
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Thu Nov 5 23:45:16 2026 +0300

    Dock the Harvester in the middle of the redrawn refinery pad
    
    The refinery picture drawn at the Outpost angle moved its pad up and to
    the right, but the docked Harvester kept the offset measured on the old
    picture, so it stood left of the pad and over the front wall. Its body
    centre now sits on the centre of the new pad, at (290, 93) of the
    384x256 refinery frame.
    
    Behavior changes: a Harvester docked at a refinery is drawn 5.625
    logical px further right and 16.75 logical px higher.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 src/utils/WorldObjectScale.hpp  |  4 ++--
 tests/WorldObjectScaleTests.cpp | 16 ++++++++--------
 2 files changed, 10 insertions(+), 10 deletions(-)
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show b6c58b8c -- src/
```

Вывод:

```diff
commit b6c58b8c7dad1a37a742b33facfab43c79f12c5a
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Thu Nov 5 23:45:16 2026 +0300

    Dock the Harvester in the middle of the redrawn refinery pad
    
    The refinery picture drawn at the Outpost angle moved its pad up and to
    the right, but the docked Harvester kept the offset measured on the old
    picture, so it stood left of the pad and over the front wall. Its body
    centre now sits on the centre of the new pad, at (290, 93) of the
    384x256 refinery frame.
    
    Behavior changes: a Harvester docked at a refinery is drawn 5.625
    logical px further right and 16.75 logical px higher.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/src/utils/WorldObjectScale.hpp b/src/utils/WorldObjectScale.hpp
index 4b7ff5b7..e6cf5224 100644
--- a/src/utils/WorldObjectScale.hpp
+++ b/src/utils/WorldObjectScale.hpp
@@ -23,8 +23,8 @@ inline WorldObjectLayout refineryHarvesterLayout(
 {
     constexpr float logicalRefineryWidth = 96.0F;
     constexpr float logicalRefineryHeight = 64.0F;
-    constexpr float logicalOffsetX = 26.75F;
-    constexpr float logicalOffsetY = 17.375F;
+    constexpr float logicalOffsetX = 32.375F;
+    constexpr float logicalOffsetY = 0.625F;
     constexpr float logicalHarvesterWidth = 80.0F;
     constexpr float logicalHarvesterHeight = 52.0F;
     return {
```

### `WorldObjectScale.hpp` в FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp
```

Вывод:

```cpp
#pragma once

#include <algorithm>
#include <cmath>

struct WorldObjectLayout {
    int x;
    int y;
    int width;
    int height;
};

/**
 * Keep the harvester on the refinery pad at exactly the same visual scale
 * as the unit uses on the map.  The transparent 80x52 unit frame extends
 * beyond the pad, while its visible south-facing body is centred on the deck.
 */
inline WorldObjectLayout refineryHarvesterLayout(
    int refineryX,
    int refineryY,
    int refineryWidth,
    int refineryHeight)
{
    constexpr float logicalRefineryWidth = 96.0F;
    constexpr float logicalRefineryHeight = 64.0F;
    constexpr float logicalOffsetX = 32.375F;
    constexpr float logicalOffsetY = 0.625F;
    constexpr float logicalHarvesterWidth = 80.0F;
    constexpr float logicalHarvesterHeight = 52.0F;
    return {
        refineryX + static_cast<int>(std::lround(
            refineryWidth * logicalOffsetX / logicalRefineryWidth
        )),
        refineryY + static_cast<int>(std::lround(
            refineryHeight * logicalOffsetY / logicalRefineryHeight
        )),
        std::max(1, static_cast<int>(std::lround(
            refineryWidth * logicalHarvesterWidth /
                logicalRefineryWidth
        ))),
        std::max(1, static_cast<int>(std::lround(
            refineryHeight * logicalHarvesterHeight /
                logicalRefineryHeight
        )))
    };
}
```

Команда для строк и вывод:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'struct WorldObjectLayout|int x;|int y;|int width;|int height;|inline WorldObjectLayout refineryHarvesterLayout|int refineryX|int refineryY|int refineryWidth|int refineryHeight|constexpr float logical' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/utils/WorldObjectScale.hpp
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:6:struct WorldObjectLayout {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:7:    int x;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:8:    int y;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:9:    int width;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:10:    int height;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:18:inline WorldObjectLayout refineryHarvesterLayout(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:19:    int refineryX,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:20:    int refineryY,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:21:    int refineryWidth,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:22:    int refineryHeight)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:24:    constexpr float logicalRefineryWidth = 96.0F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:25:    constexpr float logicalRefineryHeight = 64.0F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:26:    constexpr float logicalOffsetX = 32.375F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:27:    constexpr float logicalOffsetY = 0.625F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:28:    constexpr float logicalHarvesterWidth = 80.0F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:29:    constexpr float logicalHarvesterHeight = 52.0F;
```

В `WorldObjectScale.hpp` объявлены одна функция и шесть локальных констант. `WorldObjectLayout` содержит четыре целых поля: x, y, width, height.

- `refineryHarvesterLayout` — `src/utils/WorldObjectScale.hpp@9208dcf:18-45`. Входы: `refineryX`, `refineryY`, `refineryWidth`, `refineryHeight` (целочисленный прямоугольник НПЗ). Выход: `WorldObjectLayout`; x/y — начало прямоугольника с логическим смещением, округлённым через `std::lround`; ширина/высота — размер Харвестера, округлённый тем же способом и ограниченный снизу единицей.
- `logicalRefineryWidth = 96.0F) — `src/utils/WorldObjectScale.hpp@9208dcf:24`: логическая ширина НПЗ, делитель для горизонтальных отношений.
- `logicalRefineryHeight = 64.0F) — `src/utils/WorldObjectScale.hpp@9208dcf:25`: логическая высота НПЗ, делитель для вертикальных отношений.
- `logicalOffsetX = 32.375F) — `src/utils/WorldObjectScale.hpp@9208dcf:26`: логическое смещение прямоугольника Харвестера по x внутри прямоугольника НПЗ.
- `logicalOffsetY = 0.625F) — `src/utils/WorldObjectScale.hpp@9208dcf:27`: логическое смещение прямоугольника Харвестера по y внутри прямоугольника НПЗ.
- `logicalHarvesterWidth = 80.0F) — `src/utils/WorldObjectScale.hpp@9208dcf:28`: логическая ширина кадра Харвестера.
- `logicalHarvesterHeight = 52.0F) — `src/utils/WorldObjectScale.hpp@9208dcf:29`: логическая высота кадра Харвестера.

В FORK1 есть вызов из отрисовки НПЗ и четыре вызова из теста.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -C 4 'refineryHarvesterLayout' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cStructureDrawer.cpp tests/WorldObjectScaleTests.cpp
```

Вывод:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-876-        frameHeight,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-877-    };
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-878-
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-879-    const cRectangle refineryVisual = structure->getVisualRectangle();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:880:    const WorldObjectLayout harvesterVisual = refineryHarvesterLayout(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-881-        refineryVisual.getX(),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-882-        refineryVisual.getY(),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-883-        refineryVisual.getWidth(),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp-884-        refineryVisual.getHeight()
--
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-17-int main()
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-18-{
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-19-    bool passed = true;
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-20-    const WorldObjectLayout scale100 =
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:21:        refineryHarvesterLayout(0, 0, 96, 64);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-22-    passed &= expectEqual("100% x", scale100.x, 32);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-23-    passed &= expectEqual("100% y", scale100.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-24-    passed &= expectEqual("100% width", scale100.width, 80);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-25-    passed &= expectEqual("100% height", scale100.height, 52);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-26-
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-27-    const WorldObjectLayout scale110 =
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:28:        refineryHarvesterLayout(10, 20, 106, 70);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-29-    passed &= expectEqual("110% x", scale110.x, 46);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-30-    passed &= expectEqual("110% y", scale110.y, 21);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-31-    passed &= expectEqual("110% width", scale110.width, 88);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-32-    passed &= expectEqual("110% height", scale110.height, 57);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-33-
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-34-    const WorldObjectLayout scale125 =
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:35:        refineryHarvesterLayout(0, 0, 120, 80);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-36-    passed &= expectEqual("125% x", scale125.x, 40);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-37-    passed &= expectEqual("125% y", scale125.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-38-    passed &= expectEqual("125% width", scale125.width, 100);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-39-    passed &= expectEqual("125% height", scale125.height, 65);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-40-
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-41-    const WorldObjectLayout scale150 =
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:42:        refineryHarvesterLayout(0, 0, 144, 96);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-43-    passed &= expectEqual("150% x", scale150.x, 49);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-44-    passed &= expectEqual("150% y", scale150.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-45-    passed &= expectEqual("150% width", scale150.width, 120);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp-46-    passed &= expectEqual("150% height", scale150.height, 78);
```

В FORK1 `refineryHarvesterLayout` вызывается в `src/drawers/cStructureDrawer.cpp@9208dcf:880-885` из `drawHarvesterOnRefineryPad`; вход — визуальный прямоугольник здания, выход — `harvesterVisual`, который становится destination-прямоугольником кадра Харвестера. Сама отрисовка находится в `src/drawers/cStructureDrawer.cpp@9208dcf:846-897`; `drawStructureAnimationRefinery` вызывает overlay при `hasUnitWithin()` в строках 201-210.

### Отрисовка и положение Харвестера в PORT

В PORT `drawStructureAnimationRefinery` по строкам 283-289 проверяет указатель и тип REFINERY и вызывает только `drawStructureAnimation(structure)`. В этом теле нет координат или прямоугольника Харвестера. В выводе целевого поиска по `cStructureDrawer.cpp` есть только само имя функции, её вызов из диспетчера и проверка `hasUnitWithin()` для REPAIR; `drawHarvesterOnRefineryPad` и `refineryHarvesterLayout` в этом файле отсутствуют.

Команда и вывод функции отрисовки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -C 8 'void cStructureDrawer::drawStructureAnimationRefinery' 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cStructureDrawer.cpp
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-275-            }
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-276-
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-277-        }
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-278-    }
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-279-
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-280-    drawStructureAnimation(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-281-}
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-282-
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp:283:void cStructureDrawer::drawStructureAnimationRefinery(cAbstractStructure *structure)
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-284-{
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-285-    d2tm_assert(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-286-    d2tm_assert(structure->getType() == REFINERY);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-287-
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-288-    drawStructureAnimation(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-289-}
```

Команда, показывающая совпадения, связанные с overlay в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'drawStructureAnimationRefinery|drawHarvesterOnRefineryPad|refineryHarvesterLayout|hasUnitWithin\\(\\)' 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cStructureDrawer.cpp
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp:283:void cStructureDrawer::drawStructureAnimationRefinery(cAbstractStructure *structure)
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp:339:                drawStructureAnimationRefinery(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp:355:        if (structure->getType() == REPAIR && structure->hasUnitWithin()) {
```

Вход на НПЗ обрабатывается `cUnit.cpp@832c953:2730` вызовом `pStructure->enterStructure(iID)`. В `cAbstractStructure::enterStructure` `src/gameobjects/structures/cAbstractStructure.cpp@832c953:792-807` юнит скрывается, получает cell здания через `pUnit->setCell(getCell())`, обновляет cell X/Y и удаляется со слоя MAPID_UNITS. Формула абсолютной позиции задаётся `cUnit::setCell` в `src/gameobjects/units/cUnit.cpp@832c953:3146-3151`: `posX = mapGeometry.getAbsoluteXPositionFromCell(cell); posY = mapGeometry.getAbsoluteYPositionFromCell(cell)`. Поэтому при входе `cell = refinery.getCell()`.

При окончании разгрузки `cRefinery::think_unit_occupation` вызывает `unitLeavesStructure()` в `src/gameobjects/structures/cRefinery.cpp@832c953:93`. В `cAbstractStructure::unitLeavesStructure` `src/gameobjects/structures/cAbstractStructure.cpp@832c953:809-843` выбирается свободная клетка около здания; если её индекс больше -1, юниту присваивается эта клетка через `setCell(iNewCell)`. Выходная позиция: `posX = mapGeometry.getAbsoluteXPositionFromCell(iNewCell); posY = mapGeometry.getAbsoluteYPositionFromCell(iNewCell)`. Ветка без свободной клетки пишет предупреждение, но новую позицию не задаёт.

Для входа и выхода координаты игрового юнита заданы в терминах карты; в PORT отдельного прямоугольника рисования Харвестера на площадке НПЗ в этих функциях отрисовки нет.

## `refinery.tsv`

```tsv
ревизия	символ или участок	путь@ревизия:строка	что делает	входы	выходы
c655ceb6	смещения в коммите	src/utils/WorldObjectScale.hpp@c655ceb6:26-27	Сдвигает логический offset с 30,15 на 26.75,17.375; commit message указывает на 3.25 logical px влево и 2.375 logical px вниз	Смещения предыдущей версии 30.0F и 15.0F	Смещения 26.75F и 17.375F
b6c58b8c	смещения в коммите	src/utils/WorldObjectScale.hpp@b6c58b8c:26-27	Сдвигает offset с 26.75,17.375 на 32.375,0.625; commit message указывает на 5.625 logical px вправо и 16.75 logical px вверх	Смещения предыдущей версии 26.75F и 17.375F	Смещения 32.375F и 0.625F
9208dcf	WorldObjectLayout	src/utils/WorldObjectScale.hpp@9208dcf:6-10	Хранит координаты и размеры прямоугольника	Нет	x, y, width, height типа int
9208dcf	refineryHarvesterLayout	src/utils/WorldObjectScale.hpp@9208dcf:18-45	Строит прямоугольник кадра Харвестера в масштабе фактического прямоугольника НПЗ	Целые refineryX, refineryY, refineryWidth, refineryHeight	WorldObjectLayout: x/y со смещением и width/height кадра; округление lround, размеры минимум 1
9208dcf	logicalRefineryWidth	src/utils/WorldObjectScale.hpp@9208dcf:24	Задаёт базовую логическую ширину НПЗ	Нет	96.0F, делитель ширины
9208dcf	logicalRefineryHeight	src/utils/WorldObjectScale.hpp@9208dcf:25	Задаёт базовую логическую высоту НПЗ	Нет	64.0F, делитель высоты
9208dcf	logicalOffsetX	src/utils/WorldObjectScale.hpp@9208dcf:26	Задаёт логический x-offset кадра Харвестера относительно НПЗ	Нет	32.375F
9208dcf	logicalOffsetY	src/utils/WorldObjectScale.hpp@9208dcf:27	Задаёт логический y-offset кадра Харвестера относительно НПЗ	Нет	0.625F
9208dcf	logicalHarvesterWidth	src/utils/WorldObjectScale.hpp@9208dcf:28	Задаёт логическую ширину кадра Харвестера	Нет	80.0F
9208dcf	logicalHarvesterHeight	src/utils/WorldObjectScale.hpp@9208dcf:29	Задаёт логическую высоту кадра Харвестера	Нет	52.0F
9208dcf	drawHarvesterOnRefineryPad	src/drawers/cStructureDrawer.cpp@9208dcf:846-897	Рисует кадр Харвестера, проверив, что юнит внутри — валиден и имеет тип HARVESTER; source берёт нижний кадр, destination вычисляет через refineryHarvesterLayout	Здание с занятым юнитом, валидный Харвестер, bitmap владельца, размеры кадра	Source rectangle и destination rectangle; renderStrechSprite
9208dcf	drawStructureAnimationRefinery	src/drawers/cStructureDrawer.cpp@9208dcf:201-210	Рисует НПЗ, затем overlay Харвестера при hasUnitWithin()	Указатель на НПЗ, состояние занятости	Анимация НПЗ и кадр Харвестера на площадке
9208dcf	вызов refineryHarvesterLayout	src/drawers/cStructureDrawer.cpp@9208dcf:880-885	Передаёт визуальный прямоугольник НПЗ в функцию раскладки	visual rect: x,y,width,height	WorldObjectLayout harvesterVisual
9208dcf	вызов refineryHarvesterLayout, тест 100%	tests/WorldObjectScaleTests.cpp@9208dcf:21	Считает раскладку для прямоугольника НПЗ 96x64	0,0,96,64	WorldObjectLayout scale100
9208dcf	вызов refineryHarvesterLayout, тест 110%	tests/WorldObjectScaleTests.cpp@9208dcf:28	Считает раскладку для прямоугольника НПЗ 106x70 с началом 10,20	10,20,106,70	WorldObjectLayout scale110
9208dcf	вызов refineryHarvesterLayout, тест 125%	tests/WorldObjectScaleTests.cpp@9208dcf:35	Считает раскладку для прямоугольника НПЗ 120x80	0,0,120,80	WorldObjectLayout scale125
9208dcf	вызов refineryHarvesterLayout, тест 150%	tests/WorldObjectScaleTests.cpp@9208dcf:42	Считает раскладку для прямоугольника НПЗ 144x96	0,0,144,96	WorldObjectLayout scale150
832c953	drawStructureAnimationRefinery	src/drawers/cStructureDrawer.cpp@832c953:283-289	Проверяет структуру и её тип REFINERY, затем вызывает только drawStructureAnimation; overlay Харвестера в теле не задаётся	cAbstractStructure* structure	Анимация здания; координат Харвестера нет
832c953	enterStructure	src/gameobjects/structures/cAbstractStructure.cpp@832c953:792-807	Скрывает юнит и ставит его cell на cell здания; удаляет со слоя MAPID_UNITS	unitId, refinery.getCell()	Позиция через cUnit::setCell(refinery.getCell()); posX/Y из абсолютных координат cell
832c953	cUnit::setCell	src/gameobjects/units/cUnit.cpp@832c953:3146-3151	Обновляет cell и мировые координаты юнита	Индекс cell	 posX = mapGeometry.getAbsoluteXPositionFromCell(cell); posY = mapGeometry.getAbsoluteYPositionFromCell(cell)
832c953	cRefinery::think_unit_occupation	src/gameobjects/structures/cRefinery.cpp@832c953:49-105	После окончания сброса credits вызывает unitLeavesStructure	Юнит внутри НПЗ, таймер и состояние credits	Вызов выхода; свободная клетка выбирается в unitLeavesStructure
832c953	unitLeavesStructure	src/gameobjects/structures/cAbstractStructure.cpp@832c953:809-843	Выбирает свободную клетку вокруг здания и передаёт её в setCell	iUnitIDWithinStructure; результат getNonOccupiedCellAroundStructure()	Если cell найден: абсолютные posX/Y из iNewCell; если не найден: координаты не обновляются
```

## 4. Тарелка радара

## Коммиты форка: статистика и diff

### 3d3ff49e

Команда:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show --stat 3d3ff49e

Вывод:

    commit 3d3ff49e1a5b35a29d860a99e8f175f0dc52e567
    Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
    Date:   Fri Nov 6 23:48:29 2026 +0300

        Turn the Outpost radar dish at half speed

        The owner asked for the dish to turn half as fast. BUILD_RADAR now holds
        16 frames of 22.5 degrees instead of 8 frames of 45 degrees; the even
        frames are the previous 8. cOutPost::thinkFast keeps the frame time of
        55 calls and cycles frames 0-15, so a full turn takes about 4.4 s
        instead of 2.2 s. BUILD_RADAR_SHADOW repeats the old frame 0 sixteen
        times; the transparent flag overlay keeps its own 8-frame timer and is
        unchanged.

        A new CTest target outpost_frame_tests checks the frame order 1-15, 0, 1
        and 55 calls between changes. The pack tests now expect 16 Outpost
        frames.

        Behavior changes: the Outpost dish turns half as fast in 16 smoother
        steps.

        Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

     README_AI.md                                       |  1 +
     resources/bin/data/sdl_data_hd4.dat                |  4 +-
     resources/hd/master4/sdl_data/0026_BUILD_RADAR.png |  4 +-
     .../master4/sdl_data/0027_BUILD_RADAR_SHADOW.png   |  4 +-
     src/gameobjects/structures/cOutPost.cpp            |  3 +-
     tests/OutpostFrameTests.cpp                        | 64 ++++++++++++++++++++++
     tests/UnitRenderFixture.cmake                      |  1 +
     tools/building_angle/tests/test_angle.py           |  4 +-
     tools/building_angle/tests/test_pilot_pack.py      |  2 +-
     tools/building_angle/tests/test_rollout_pack.py    | 10 ++--
     10 files changed, 81 insertions(+), 16 deletions(-)

### 849650d0

Команда:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show --stat 849650d0

Вывод:

    commit 849650d06d6c7a2e9bd568a72ebeb7d97fb86382
    Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
    Date:   Sat Nov 7 11:11:24 2026 +0300

        Turn the Outpost radar dish in 32 frames

        The owner asked for the dish to turn slower again and chose the smooth
        option. BUILD_RADAR now holds 32 frames of 11.25 degrees (256x8192);
        the even frames are the previous 16. cOutPost::thinkFast keeps the
        frame time of 55 calls and cycles frames 0-31, so a full turn takes
        about 8.8 s instead of 4.4 s. BUILD_RADAR_SHADOW repeats the old frame
        0 thirty-two times; the transparent flag overlay keeps its own 8-frame
        timer and is unchanged.

        outpost_frame_tests now expects the frame order 1-31, 0, 1 with 55
        calls between changes, and the pack tests expect 32 Outpost frames.

        Behavior changes: the Outpost dish turns half as fast again, in 32
        steps.

        Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

     resources/bin/data/sdl_data_hd4.dat                       |  4 ++--
     resources/hd/master4/sdl_data/0026_BUILD_RADAR.png        |  4 ++--
     resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png |  4 ++--
     src/gameobjects/structures/cOutPost.cpp                   |  2 +-
     tests/OutpostFrameTests.cpp                               | 12 ++++++------
     tools/building_angle/tests/test_angle.py                  |  4 ++--
     tools/building_angle/tests/test_pilot_pack.py             |  2 +-
     tools/building_angle/tests/test_rollout_pack.py            | 10 +++++-----

Команда для patch-вывода обоих коммитов:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show --format= 3d3ff49e
    git show --format= 849650d0

Вывод, diff 3d3ff49e (включая все файлы вне src/):

    diff --git a/README_AI.md b/README_AI.md
    index 53d0666f..4aa4b810 100644
    --- a/README_AI.md
    +++ b/README_AI.md
    @@ -131,6 +131,7 @@ cmake --build build-ru --parallel
     | Шрифты | `font_coverage_tests` |
     | Цвета фракций | `faction_tint_tests` |
     | Площадка завода: появление юнита, съезд, очередь, Карриер, мерцание, сохранение | `factory_pad_tests` (логика без SDL, `FactoryPad.hpp`), `factory_pad_engine_tests` (движок), `factory_pad_save_tests` (раздел `FACTORYPADS` сохранения) |
    +| Командный пост: кадры поворота тарелки | `outpost_frame_tests` |
     
     Обычный запуск:
     
    diff --git a/resources/bin/data/sdl_data_hd4.dat b/resources/bin/data/sdl_data_hd4.dat
    index 2f8da0b1..0cc50937 100644
    --- a/resources/bin/data/sdl_data_hd4.dat
    +++ b/resources/bin/data/sdl_data_hd4.dat
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:f2aa2f2f68161f525e4d93197214527439e358b0ba7424f8cfd4d6ae933f0102
    -size 36661882
    +oid sha256:6277281be14d5f33f8cfee04492ec0a22deb803123a1ad824a9dac4998e1a4dd
    +size 37437362
    diff --git a/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png b/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    index 90acec64..0d6cf814 100644
    --- a/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    +++ b/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:998508bb9df387be9450f6f30ec000baf3a0e29b8d70521516554aafa99088de
    -size 768632
    +oid sha256:4a4002136e36d6d9536e2eea6d04975a6ddc3bfc49b02723a91eb29cd4656361
    +size 1537603
    diff --git a/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png b/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    index 831d49b1..c2b73096 100644
    --- a/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    +++ b/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:2d74a1d1839790f04a93bae3b132b8d77db1e7df6d7252d4f424621d8875dd03
    -size 6614
    +oid sha256:8dc22d52cb637264ecd6dd0c5b5abe7254e9db360d0fc7c571f48d9df992cf7d
    +size 13123
    diff --git a/src/gameobjects/structures/cOutPost.cpp b/src/gameobjects/structures/cOutPost.cpp
    index 6de0f82f..220178be 100644
    --- a/src/gameobjects/structures/cOutPost.cpp
    +++ b/src/gameobjects/structures/cOutPost.cpp
    @@ -24,8 +24,7 @@ void cOutPost::thinkFast()
         if (TIMER_flag > 54) {
             iFrame++;
     
    -        // switch between 0 and 7.
    -        if (iFrame > 7) {
    +        if (iFrame > 15) {
                 iFrame=0;
             }
     
    diff --git a/tests/OutpostFrameTests.cpp b/tests/OutpostFrameTests.cpp
    new file mode 100644
    index 00000000..4046dadb
    --- /dev/null
    +++ b/tests/OutpostFrameTests.cpp
    @@ -0,0 +1,64 @@
    +#include "d2tmc.h"
    +#include "definitions.h"
    +#include "gameobjects/structures/cOutPost.h"
    +
    +#include <iostream>
    +#include <memory>
    +#include <sstream>
    +#include <vector>
    +
    +int main()
    +{
    +    sStructureInfo[RADAR].flags = {s_FlagInfo{false, 25, 3}};
    +    auto outpost = std::make_unique<cOutPost>();
    +    outpost->setWidth(2);
    +    outpost->setHeight(2);
    +    outpost->setFrame(0);
    +
    +    std::vector<int> frames;
    +    std::vector<int> callsBetweenChanges;
    +    int previousFrame = outpost->getFrame();
    +    int callsSinceChange = 0;
    +    for (int calls = 0; calls < 2000 && frames.size() < 17; ++calls) {
    +        outpost->thinkFast();
    +        ++callsSinceChange;
    +        const int frame = outpost->getFrame();
    +        if (frame != previousFrame) {
    +            frames.push_back(frame);
    +            if (frames.size() > 1) {
    +                callsBetweenChanges.push_back(callsSinceChange);
    +            }
    +            previousFrame = frame;
    +            callsSinceChange = 0;
    +        }
    +    }
    +
    +    std::vector<int> expectedFrames;
    +    for (int frame = 1; frame <= 15; ++frame) {
    +        expectedFrames.push_back(frame);
    +    }
    +    expectedFrames.push_back(0);
    +    expectedFrames.push_back(1);
    +    if (frames != expectedFrames) {
    +        std::ostringstream message;
    +        message << "expected frames 1..15,0,1; got";
    +        for (const int frame : frames) {
    +            message << ' ' << frame;
    +        }
    +        std::cerr << "outpost_frame: " << message.str() << '\n';
    +        return 1;
    +    }
    +    if (callsBetweenChanges.size() != 16) {
    +        std::cerr << "outpost_frame: expected 16 intervals, got " << callsBetweenChanges.size() << '\n';
    +        return 1;
    +    }
    +    for (size_t interval = 0; interval < callsBetweenChanges.size(); ++interval) {
    +        if (callsBetweenChanges[interval] != 55) {
    +            std::cerr << "outpost_frame: interval " << interval + 1 << " used "
    +                      << callsBetweenChanges[interval] << " thinkFast calls, expected 55\n";
    +            return 1;
    +        }
    +    }
    +    std::cout << "outpost_frame: 17 frame changes with 55 calls between them: ok\n";
    +    return 0;
    +}
    diff --git a/tests/UnitRenderFixture.cmake b/tests/UnitRenderFixture.cmake
    index 4a7e82a2..f136ca20 100644
    --- a/tests/UnitRenderFixture.cmake
    +++ b/tests/UnitRenderFixture.cmake
    @@ -130,4 +130,5 @@ add_unit_frame_test(mouse_cell_refresh_tests mouse_cell_refresh MouseCellRefresh
     add_unit_frame_test(mouse_click_init_tests mouse_click_init MouseClickInitTests.cpp recorded)
     add_unit_frame_test(placement_rule_tests placement_rule PlacementRuleTests.cpp recorded)
     add_unit_frame_test(factory_pad_engine_tests factory_pad_engine FactoryPadEngineTests.cpp recorded)
    +add_unit_frame_test(outpost_frame_tests outpost_frame OutpostFrameTests.cpp recorded)
     add_unit_frame_test(factory_pad_save_tests factory_pad_save FactoryPadSaveTests.cpp recorded)
    diff --git a/tools/building_angle/tests/test_angle.py b/tools/building_angle/tests/test_angle.py
    index 0807d3d6..e2cb5101 100644
    --- a/tools/building_angle/tests/test_angle.py
    +++ b/tools/building_angle/tests/test_angle.py
    @@ -107,13 +107,13 @@ class OutpostPackTests(unittest.TestCase):
             self.radar = decode_image(entries["BUILD_RADAR"].payload).convert("RGBA")
     
         def test_current_outpost_leaves_margins(self):
    -        ok, rows = angle.check(self.radar, (2, 2), 8)
    +        ok, rows = angle.check(self.radar, (2, 2), 16)
             if ok:
                 self.skipTest("pack already holds an edge-to-edge Outpost")
             self.assertLess(rows[0]["left"], angle.MIN_EDGE_COVERAGE)
     
         def test_stretched_outpost_reaches_every_edge(self):
    -        ok, rows = angle.check(angle.stretch(self.radar, (2, 2), 8), (2, 2), 8)
    +        ok, rows = angle.check(angle.stretch(self.radar, (2, 2), 16), (2, 2), 16)
             self.assertTrue(ok, rows)
    diff --git a/tools/building_angle/tests/test_pilot_pack.py b/tools/building_angle/tests/test_pilot_pack.py
    index bdd30de2..c38ff5c3 100644
    --- a/tools/building_angle/tests/test_pilot_pack.py
    +++ b/tools/building_angle/tests/test_pilot_pack.py
    @@ -24,7 +24,7 @@ class PilotPackTests(unittest.TestCase):
             return image.convert("RGBA")
     
         def test_build_radar_reaches_every_edge(self):
    -        ok, rows = angle.check(self.image("BUILD_RADAR"), (2, 2), 8)
    +        ok, rows = angle.check(self.image("BUILD_RADAR"), (2, 2), 16)
             self.assertTrue(ok, rows)
     
         def test_build_windtrap_reaches_every_edge(self):
    diff --git a/tools/building_angle/tests/test_rollout_pack.py b/tools/building_angle/tests/test_rollout_pack.py
    index c6789d73..8cb332fc 100644
    --- a/tools/building_angle/tests/test_rollout_pack.py
    +++ b/tools/building_angle/tests/test_rollout_pack.py
    @@ -42,7 +42,7 @@ class RolloutPackTests(unittest.TestCase):
                 ("BUILD_CONSTYARD", (2, 2), 1),
                 ("BUILD_IX", (2, 2), 1),
                 ("BUILD_LIGHTFACTORY", (2, 2), 8),
    -            ("BUILD_RADAR", (2, 2), 8),
    +            ("BUILD_RADAR", (2, 2), 16),
                 ("BUILD_SILO", (2, 2), 1),
                 ("BUILD_WOR", (2, 2), 1),
                 ("BUILD_PALACE", (3, 3), 1),
    @@ -56,20 +56,20 @@ class RolloutPackTests(unittest.TestCase):
                 self.assertTrue(ok, rows)
     
         def test_radar_dish_turns_inside_its_circle(self):
    -        frames = angle.frames_of(self.image("BUILD_RADAR"), (2, 2), 8)
    +        frames = angle.frames_of(self.image("BUILD_RADAR"), (2, 2), 16)
             baseline = np.asarray(frames[0])
             y, x = np.ogrid[:256, :256]
             allowed = (x - 130) ** 2 + (y - 114) ** 2 <= 128 ** 2
             arrays = [baseline]
    -        for frame_index in range(1, 8):
    +        for frame_index in range(1, 16):
                 current = np.asarray(frames[frame_index])
                 arrays.append(current)
                 changed = np.any(current != baseline, axis=2)
                 with self.subTest(frame=frame_index):
                     self.assertFalse(np.any(changed & ~allowed), "pixels changed outside the dish circle")
                     self.assertGreaterEqual(int(changed.sum()), 5000, "too few pixels changed")
    -        for left in range(8):
    -            for right in range(left + 1, 8):
    +        for left in range(16):
    +            for right in range(left + 1, 16):
                     with self.subTest(frame_pair=(left, right)):
                         self.assertFalse(np.array_equal(arrays[left], arrays[right]), "frames are identical")

Вывод, diff 849650d0:

    diff --git a/resources/bin/data/sdl_data_hd4.dat b/resources/bin/data/sdl_data_hd4.dat
    index 0cc50937..9c09db22 100644
    --- a/resources/bin/data/sdl_data_hd4.dat
    +++ b/resources/bin/data/sdl_data_hd4.dat
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:6277281be14d5f33f8cfee04492ec0a22deb803123a1ad824a9dac4998e1a4dd
    -size 37437362
    +oid sha256:bb2729debefd4ff2034e9a4f9681b4dbb693d6ffba84d8319b1574ef40b418aa
    +size 38987582
    diff --git a/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png b/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    index 0d6cf814..e16019f4 100644
    --- a/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    +++ b/resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:4a4002136e36d6d9536e2eea6d04975a6ddc3bfc49b02723a91eb29cd4656361
    -size 1537603
    +oid sha256:6aebca32a6e74d6d0a901f78eb6c8853ff630b5c796f16e847a0c8046ea9d3ce
    +size 3074765
    diff --git a/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png b/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    index c2b73096..799b80b1 100644
    --- a/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    +++ b/resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    @@ -1,3 +1,3 @@
     version https://git-lfs.github.com/spec/v1
    -oid sha256:8dc22d52cb637264ecd6dd0c5b5abe7254e9db360d0fc7c571f48d9df992cf7d
    -size 13123
    +oid sha256:5fb41322572a85e6068ec829a26a76399c1b03125780e6ed6d64d345b13e7b0d
    +size 26181
    diff --git a/src/gameobjects/structures/cOutPost.cpp b/src/gameobjects/structures/cOutPost.cpp
    index 220178be..8c6bc6c5 100644
    --- a/src/gameobjects/structures/cOutPost.cpp
    +++ b/src/gameobjects/structures/cOutPost.cpp
    @@ -24,7 +24,7 @@ void cOutPost::thinkFast()
             if (TIMER_flag > 54) {
                 iFrame++;
     
    -        if (iFrame > 15) {
    +        if (iFrame > 31) {
                 iFrame=0;
             }
     
    diff --git a/tests/OutpostFrameTests.cpp b/tests/OutpostFrameTests.cpp
    index 4046dadb..84c3856a 100644
    --- a/tests/OutpostFrameTests.cpp
    +++ b/tests/OutpostFrameTests.cpp
    @@ -19,7 +19,7 @@ int main()
         std::vector<int> callsBetweenChanges;
         int previousFrame = outpost->getFrame();
         int callsSinceChange = 0;
    -    for (int calls = 0; calls < 2000 && frames.size() < 17; ++calls) {
    +    for (int calls = 0; calls < 4000 && frames.size() < 33; ++calls) {
             outpost->thinkFast();
             ++callsSinceChange;
             const int frame = outpost->getFrame();
    @@ -34,22 +34,22 @@ int main()
     
         std::vector<int> expectedFrames;
    -    for (int frame = 1; frame <= 15; ++frame) {
    +    for (int frame = 1; frame <= 31; ++frame) {
             expectedFrames.push_back(frame);
         }
         expectedFrames.push_back(0);
         expectedFrames.push_back(1);
         if (frames != expectedFrames) {
             std::ostringstream message;
    -        message << "expected frames 1..15,0,1; got";
    +        message << "expected frames 1..31,0,1; got";
             for (const int frame : frames) {
                 message << ' ' << frame;
             }
             std::cerr << "outpost_frame: " << message.str() << '\n';
             return 1;
         }
    -    if (callsBetweenChanges.size() != 16) {
    -        std::cerr << "outpost_frame: expected 16 intervals, got " << callsBetweenChanges.size() << '\n';
    +    if (callsBetweenChanges.size() != 32) {
    +        std::cerr << "outpost_frame: expected 32 intervals, got " << callsBetweenChanges.size() << '\n';
             return 1;
         }
         for (size_t interval = 0; interval < callsBetweenChanges.size(); ++interval) {
             if (callsBetweenChanges[interval] != 55) {
                 std::cerr << "outpost_frame: interval " << interval + 1 << " used "
                           << callsBetweenChanges[interval] << " thinkFast calls, expected 55\n";
                 return 1;
             }
         }
    -    std::cout << "outpost_frame: 17 frame changes with 55 calls between them: ok\n";
    +    std::cout << "outpost_frame: 33 frame changes with 55 calls between them: ok\n";
         return 0;
     }
    diff --git a/tools/building_angle/tests/test_angle.py b/tools/building_angle/tests/test_angle.py
    index e2cb5101..7ec62ce9 100644
    --- a/tools/building_angle/tests/test_angle.py
    +++ b/tools/building_angle/tests/test_angle.py
    @@ -107,13 +107,13 @@ class OutpostPackTests(unittest.TestCase):
             self.radar = decode_image(entries["BUILD_RADAR"].payload).convert("RGBA")
     
         def test_current_outpost_leaves_margins(self):
    -        ok, rows = angle.check(self.radar, (2, 2), 16)
    +        ok, rows = angle.check(self.radar, (2, 2), 32)
             if ok:
                 self.skipTest("pack already holds an edge-to-edge Outpost")
             self.assertLess(rows[0]["left"], angle.MIN_EDGE_COVERAGE)
     
         def test_stretched_outpost_reaches_every_edge(self):
    -        ok, rows = angle.check(angle.stretch(self.radar, (2, 2), 16), (2, 2), 16)
    +        ok, rows = angle.check(angle.stretch(self.radar, (2, 2), 32), (2, 2), 32)
             self.assertTrue(ok, rows)
    diff --git a/tools/building_angle/tests/test_pilot_pack.py b/tools/building_angle/tests/test_pilot_pack.py
    index c38ff5c3..ccd6c2a6 100644
    --- a/tools/building_angle/tests/test_pilot_pack.py
    +++ b/tools/building_angle/tests/test_pilot_pack.py
    @@ -24,7 +24,7 @@ class PilotPackTests(unittest.TestCase):
             return image.convert("RGBA")
     
         def test_build_radar_reaches_every_edge(self):
    -        ok, rows = angle.check(self.image("BUILD_RADAR"), (2, 2), 16)
    +        ok, rows = angle.check(self.image("BUILD_RADAR"), (2, 2), 32)
             self.assertTrue(ok, rows)
     
         def test_build_windtrap_reaches_every_edge(self):
    diff --git a/tools/building_angle/tests/test_rollout_pack.py b/tools/building_angle/tests/test_rollout_pack.py
    index 8cb332fc..835a6821 100644
    --- a/tools/building_angle/tests/test_rollout_pack.py
    +++ b/tools/building_angle/tests/test_rollout_pack.py
    @@ -42,7 +42,7 @@ class RolloutPackTests(unittest.TestCase):
                 ("BUILD_CONSTYARD", (2, 2), 1),
                 ("BUILD_IX", (2, 2), 1),
                 ("BUILD_LIGHTFACTORY", (2, 2), 8),
    -            ("BUILD_RADAR", (2, 2), 16),
    +            ("BUILD_RADAR", (2, 2), 32),
                 ("BUILD_SILO", (2, 2), 1),
                 ("BUILD_WOR", (2, 2), 1),
                 ("BUILD_PALACE", (3, 3), 1),
    @@ -56,20 +56,20 @@ class RolloutPackTests(unittest.TestCase):
             self.assertTrue(ok, rows)
     
         def test_radar_dish_turns_inside_its_circle(self):
    -        frames = angle.frames_of(self.image("BUILD_RADAR"), (2, 2), 16)
    +        frames = angle.frames_of(self.image("BUILD_RADAR"), (2, 2), 32)
             baseline = np.asarray(frames[0])
             y, x = np.ogrid[:256, :256]
             allowed = (x - 130) ** 2 + (y - 114) ** 2 <= 128 ** 2
             arrays = [baseline]
    -        for frame_index in range(1, 16):
    +        for frame_index in range(1, 32):
                 current = np.asarray(frames[frame_index])
                 arrays.append(current)
                 changed = np.any(current != baseline, axis=2)
                 with self.subTest(frame=frame_index):
                     self.assertFalse(np.any(changed & ~allowed), "pixels changed outside the dish circle")
                     self.assertGreaterEqual(int(changed.sum()), 5000, "too few pixels changed")
    -        for left in range(16):
    -            for right in range(left + 1, 16):
    +        for left in range(32):
    +            for right in range(left + 1, 32):
                     with self.subTest(frame_pair=(left, right)):
                         self.assertFalse(np.array_equal(arrays[left], arrays[right]), "frames are identical")

## Файлы вне src/: объекты FORK1 и наличие в PORT

Пути вне src/, объединение затронутых файлов обоих коммитов: README_AI.md, resources/bin/data/sdl_data_hd4.dat, два PNG в resources/hd/master4/sdl_data, tests/OutpostFrameTests.cpp, tests/UnitRenderFixture.cmake, и три файла tools/building_angle/tests/.

Команда для размеров и первой строки объекта в FORK1, а также для идентификаторов объектов FORK1 и PORT:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    for p in README_AI.md resources/bin/data/sdl_data_hd4.dat resources/hd/master4/sdl_data/0026_BUILD_RADAR.png resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png tests/OutpostFrameTests.cpp tests/UnitRenderFixture.cmake tools/building_angle/tests/test_angle.py tools/building_angle/tests/test_pilot_pack.py tools/building_angle/tests/test_rollout_pack.py; do
      printf 'PATH %s\n' "$p"
      printf 'SIZE '; git cat-file -s "9208dcf5a358f40afd95c99480e4e09f781ed566:$p"
      printf 'FIRST '; git cat-file -p "9208dcf5a358f40afd95c99480e4e09f781ed566:$p" | head -n 1
      printf 'FORK '; git rev-parse "9208dcf5a358f40afd95c99480e4e09f781ed566:$p"
      printf 'PORT '; git rev-parse "832c953a94a632d57872349013f7ed1a37434715:$p" 2>&1 || true
    done

Вывод:

    PATH README_AI.md
    SIZE 38013
    FIRST # D2TM v0.8.0 RU/HD — точка входа для AI-агента
    FORK 4aa4b81062b3ab682964907d13c089297352a842
    PORT fatal: path 'README_AI.md' exists on disk, but not in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:README_AI.md
    PATH resources/bin/data/sdl_data_hd4.dat
    SIZE 133
    FIRST version https://git-lfs.github.com/spec/v1
    FORK d90d6698e4c5e5fd9d2993000e15032a2241aa1a
    PORT 0924b6df5bf7db800d425ff52c80c55e3386c927
    PATH resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    SIZE 132
    FIRST version https://git-lfs.github.com/spec/v1
    FORK e16019f477f470b640dd1fa773482c2e3c338ac6
    PORT fatal: path 'resources/hd/master4/sdl_data/0026_BUILD_RADAR.png' exists on disk, but not in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:resources/hd/master4/sdl_data/0026_BUILD_RADAR.png
    PATH resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    SIZE 130
    FIRST version https://git-lfs.github.com/spec/v1
    FORK 799b80b1f631f0ad24b492a4ee400ad8a7107a36
    PORT fatal: path 'resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png' exists on disk, but not in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png
    PATH tests/OutpostFrameTests.cpp
    SIZE 2088
    FIRST #include "d2tmc.h"
    FORK 84c3856a5207c75a0ee138e0588566169f13e4fb
    PORT fatal: path 'tests/OutpostFrameTests.cpp' does not exist in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:tests/OutpostFrameTests.cpp
    PATH tests/UnitRenderFixture.cmake
    SIZE 6530
    FIRST include(CheckCXXSourceCompiles)
    FORK f136ca207ee2969f9881d839a566bc00365ffdee
    PORT fatal: path 'tests/UnitRenderFixture.cmake' exists on disk, but not in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:tests/UnitRenderFixture.cmake
    PATH tools/building_angle/tests/test_angle.py
    SIZE 4812
    FIRST import os
    FORK 7ec62ce943838f0cae96b6016167576e2433f8ad
    PORT fatal: path 'tools/building_angle/tests/test_angle.py' does not exist in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:tools/building_angle/tests/test_angle.py
    PATH tools/building_angle/tests/test_pilot_pack.py
    SIZE 1130
    FIRST import os
    FORK 1ec89eea61293455fca2d8c6bcc8c5c05447c2ed
    PORT fatal: path 'tools/building_angle/tests/test_pilot_pack.py' does not exist in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:tools/building_angle/tests/test_pilot_pack.py
    PATH tools/building_angle/tests/test_rollout_pack.py
    SIZE 8033
    FIRST import os
    FORK 808fa3f6d80316abbd051b192d673b06fc9363dd
    PORT fatal: path 'tools/building_angle/tests/test_rollout_pack.py' does not exist in '832c953a94a632d57872349013f7ed1a37434715'
    832c953a94a632d57872349013f7ed1a37434715:tools/building_angle/tests/test_rollout_pack.py

Проверка путей PORT командой:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 -- README_AI.md resources/bin/data/sdl_data_hd4.dat resources/hd/master4/sdl_data/0026_BUILD_RADAR.png resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png tests/OutpostFrameTests.cpp tests/UnitRenderFixture.cmake tools/building_angle/tests/test_angle.py tools/building_angle/tests/test_pilot_pack.py tools/building_angle/tests/test_rollout_pack.py

Вывод:
    resources/bin/data/sdl_data_hd4.dat

Только sdl_data_hd4.dat из перечисленных путей есть в дереве PORT. Для него размер объекта PORT — 133 байта, первая строка cat-file -p — version https://git-lfs.github.com/spec/v1, объект FORK1 d90d6698e4c5e5fd9d2993000e15032a2241aa1a, объект PORT 0924b6df5bf7db800d425ff52c80c55e3386c927; объекты не совпадают. PNG и остальные перечисленные пути в PORT отсутствуют. Вывод rev-parse для отсутствующих путей в таблице выше сопровождается fatal и не является хешем blob-объекта.

## Выбор кадра и запись пака в PORT

Команда:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOutPost.cpp | /srv/dune/venv/bin/python -c 'import sys; print("".join(f"{i}: {line}" for i, line in enumerate(sys.stdin, 1) if 1 <= i <= 48), end="")'
    git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp | /srv/dune/venv/bin/python -c 'import sys; print("".join(f"{i}: {line}" for i, line in enumerate(sys.stdin, 1) if 1 <= i <= 58), end="")'

Результаты по анимации (строки файла):
    cOutPost::thinkFast — src/gameobjects/structures/cOutPost.cpp@9208dcf:15-32; после TIMER_flag > 54 увеличивает iFrame, при iFrame > 31 устанавливает 0, затем обнуляет TIMER_flag. Формула: iFrame=(iFrame+1) mod 32 раз в 55 вызовов thinkFast; 32 кадра.
    cOutPost::thinkFast — src/gameobjects/structures/cOutPost.cpp@832c953:30-48; после TIMER_flag > 54 увеличивает iFrame, при iFrame > 7 устанавливает 0, затем обнуляет TIMER_flag. Формула: iFrame=(iFrame+1) mod 8 раз в 55 вызовов thinkFast; 8 кадров.

Команда для сверки записи пака:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -i 'radar\|outpost' 832c953a94a632d57872349013f7ed1a37434715 -- src

Вывод:

    832c953a94a632d57872349013f7ed1a37434715:src/CMakeLists.txt:99:    gameobjects/structures/cOutPost.cpp
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:613:    // Description : Special infantry unit, moves like trike, deadly as hell, not detectable on radar!
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1180:    upgradeInfos[UPGRADE_TYPE_CONSTYARD_RTURRET].needsStructureType = RADAR;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1542:    // Structure    : Radar
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1544:    structureInfos[RADAR].bmp_width = 32 * 2;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1545:    structureInfos[RADAR].bmp_height = 32 * 2;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1546:    structureInfos[RADAR].bmp = m_gfxdata->getSurface(BUILD_RADAR);
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1547:    structureInfos[RADAR].shadow = m_gfxdata->getTexture(BUILD_RADAR_SHADOW); // shadow
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1548:    structureInfos[RADAR].sight = 12;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1549:    structureInfos[RADAR].fadecol = -1;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1550:    structureInfos[RADAR].icon = ICON_STR_RADAR;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1551:    structureInfos[RADAR].configured = true;
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1552:    // outpost has 2 flags
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1553:    structureInfos[RADAR].flags.push_back(s_FlagInfo{
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1558:    structureInfos[RADAR].flags.push_back(s_FlagInfo{
    832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1563:    structureInfos[RADAR].name = "Outpost";
    832c953a94a632d57872349013f7ed1a37434715:src/data/gfxaudio.h:90:constexpr int SOUND_RADAR                      = 66;       /* SAMP */
    832c953a94a632d57872349013f7ed1a37434715:src/data/gfxdata.h:50:constexpr int BUILD_RADAR = 26; /* BMP  */
    832c953a94a632d57872349013f7ed1a37434715:src/data/gfxdata.h:51:constexpr int BUILD_RADAR_SHADOW = 27; /* BMP  */
    832c953a94a632d57872349013f7ed1a37434715:src/data/gfxinter.h:65:constexpr int ICON_STR_RADAR = 41; /* BMP  */
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:171:    if (m_player->hasAtleastOneStructure(RADAR)) {
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:174:            // power check below (which plays SOUND_RADAR) always gets a chance to run,
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:175:            // even when power is already sufficient the instant the radar completes.
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:185:    bool hasRadarAndEnoughPower = (m_player->getAmountOfStructuresForType(RADAR) > 0) && m_player->bEnoughPower();
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:189:        if (!hasRadarAndEnoughPower) {
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:192:            // "Radar de-activated""
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:199:        if (hasRadarAndEnoughPower) {
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:202:            m_audioContext->playSound(SOUND_RADAR);
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.cpp:203:            // "Radar activated"
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.h:49:    NOTAVAILABLE, // show logo / no radar available
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.h:50:    POWERUP,      // powering up (radar available & enough power)
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.h:51:    RENDERMAP,    // map is rendering (radar available & enough power)
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.h:52:    POWERDOWN,    // powering down (radar available & not enough power)
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cMiniMapDrawer.h:53:    LOWPOWER,     // map is not rendered (radar available & not enough power)
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cSideBarDrawer.cpp:255:    bool hasRadarAndEnoughPower = m_player->hasRadarAndEnoughPower();
    832c953a94a632d57872349013f7ed1a37434715:src/drawers/cSideBarDrawer.cpp:257:    if (hasRadarAndEnoughPower) {
    832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp:1083:                // resuming the mission from the options menu: keep the drawers (radar), mission stats
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/cUpgradeInfo.h:48:    // above, so if you require CONSTYARD *and* RADAR you set structureType=CONSTYARD and needsStructure=RADAR, keep -1
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1516:    if (!player->hasAtleastOneStructure(RADAR) && !player->hasAtleastOneStructure(HEAVYFACTORY)) {
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1518:            return RADAR;
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1525:        if (!player->hasAtleastOneStructure(RADAR)) return RADAR;
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:375:bool cPlayer::hasRadarAndEnoughPower() const
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.cpp:377:    return getAmountOfStructuresForType(RADAR) > 0 && bEnoughPower();
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/cPlayer.h:247:    bool hasRadarAndEnoughPower() const;
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:2: * @file cOutPost.cpp
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:16:#include "cOutPost.h"
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:20:cOutPost::cOutPost()
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:25:int cOutPost::getType() const
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:27:    return RADAR;
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:30:void cOutPost::thinkFast()
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:36:    // dish on outpost)
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:51:void cOutPost::think_animation()
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.cpp:58:void cOutPost::think_guard()
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.h:2: * @file cOutPost.h
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.h:20:class cOutPost : public cAbstractStructure {
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cOutPost.h:22:    cOutPost();
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cStructureFactory.cpp:36:#include "cOutPost.h"
    832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/structures/cStructureFactory.cpp:85:    if (type == RADAR)\t\t\treturn std::make_unique<cOutPost>();
    832c953a94a632d57872349013f7ed1a37434715:src/include/definitions.h:121:inline constexpr int RADAR = 9; // = OUTPOST (cOutPost)
    832c953a94a632d57872349013f7ed1a37434715:src/sidebar/cBuildingListUpdater.cpp:109:    listConstYard->addStructureToList(RADAR, 0);
    832c953a94a632d57872349013f7ed1a37434715:src/sidebar/cBuildingListUpdater.cpp:328:            listConstYard->addStructureToList(RADAR, 0);
    832c953a94a632d57872349013f7ed1a37434715:src/sidebar/cBuildingListUpdater.cpp:354:    if (structureType == RADAR) {
    832c953a94a632d57872349013f7ed1a37434715:src/utils/HdHouseFlag.hpp:17:        {RADAR, "BUILD_RADAR_FLAG", 64, 64},
    832c953a94a632d57872349013f7ed1a37434715:src/utils/cIniUtils.cpp:86:    {"RADAR", RADAR},
    832c953a94a632d57872349013f7ed1a37434715:src/utils/cIniUtils.cpp:108:    {"Outpost", RADAR},

Идентификаторы/загрузка записи тарелки: src/data/gfxdata.h@832c953:50 — BUILD_RADAR=26; src/context/cInfoContextCreator.cpp@832c953:1546 — surface загружается через getSurface(BUILD_RADAR). Число кадров выбирается циклом cOutPost::thinkFast — 8 кадров (iFrame 0..7), см. src/gameobjects/structures/cOutPost.cpp@832c953:39-47. Тень — BUILD_RADAR_SHADOW=27 и getTexture на строке 1547. Дополнительно HD-описание флага Outpost находится в src/utils/HdHouseFlag.hpp@832c953:17; две записи s_FlagInfo для RADAR — строки 1553 и 1558.

## Diff BASE → UP1 по cOutPost.cpp

Команда:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git diff --unified=5 e17379ad660fca46859b403a6c3d33ec8d831a40 d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gameobjects/structures/cOutPost.cpp

Вывод:

    diff --git a/src/gameobjects/structures/cOutPost.cpp b/src/gameobjects/structures/cOutPost.cpp
    index 6de0f82f..4ba0614b 100644
    --- a/src/gameobjects/structures/cOutPost.cpp
    +++ b/src/gameobjects/structures/cOutPost.cpp
    @@ -1,5 +1,20 @@
    +/**
    + * @file cOutPost.cpp
    + *
    + * Dune 2 - The Maker
    + *
    + * @author Stefan Hendriks & the D2TM Team
    + * @www http://www.dune2themaker.com
    + * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
    + * @license This software is released under the MIT License. See LICENSE.md.
    + *
    + * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    + *
    + * This is a non-commercial educational project.
    + */
    +
     #include "cOutPost.h"
     
     #include "definitions.h"

Новый участок в UP1: src/gameobjects/structures/cOutPost.cpp@d06f2fc:1 — добавлен файловый заголовок; логика thinkFast и выбор кадра в этом diff не меняются.

## Содержимое radar.tsv

Таблица содержит те же строки, что и отдельный файл .tmp/p8ar1/radar.tsv:

    ревизия	символ	файл или участок	путь@ревизия:строка	что делает
    FORK1	cOutPost::thinkFast	выбор кадра тарелки	src/gameobjects/structures/cOutPost.cpp@9208dcf:15-32	При TIMER_flag > 54 увеличивает iFrame, циклически выбирает 0…31; 32 кадра и 55 вызовов между сменами
    PORT	cOutPost::thinkFast	выбор кадра тарелки	src/gameobjects/structures/cOutPost.cpp@832c953:30-48	При TIMER_flag > 54 увеличивает iFrame, циклически выбирает 0…7; 8 кадров и 55 вызовов между сменами
    3d3ff49e	iFrame > 15	diff	src/gameobjects/structures/cOutPost.cpp@3d3ff49e:27	Расширяет цикл кадров с 8 до 16
    849650d0	iFrame > 31	diff	src/gameobjects/structures/cOutPost.cpp@849650d0:27	Расширяет цикл кадров с 16 до 32
    UP1	файловый заголовок	diff	src/gameobjects/structures/cOutPost.cpp@d06f2fc:1	Добавляет заголовок файла; выбор кадра не меняется
    PORT	BUILD_RADAR	идентификатор записи	src/data/gfxdata.h@832c953:50	Запись 26 типа BMP для изображения тарелки
    PORT	BUILD_RADAR	getSurface	src/context/cInfoContextCreator.cpp@832c953:1546	Загружает изображение тарелки из записи пака
    PORT	BUILD_RADAR_SHADOW	getTexture	src/context/cInfoContextCreator.cpp@832c953:1547	Загружает тень записи 27
    PORT	RADAR flag 1	src/context/cInfoContextCreator.cpp@832c953:1553	Первый флаг записи структуры Outpost
    PORT	RADAR flag 2	src/context/cInfoContextCreator.cpp@832c953:1558	Второй флаг записи структуры Outpost
    PORT	BUILD_RADAR_FLAG	HD House Flag	src/utils/HdHouseFlag.hpp@832c953:17	Связывает RADAR с HD-изображением BUILD_RADAR_FLAG размером 64 на 64
    FORK1	порядок кадров	OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:42	Сравнивает полученные кадры с ожидаемыми 1…31,0,1
    FORK1	число интервалов	OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:51	Проверяет 32 интервала между сменами кадра
    FORK1	длина интервала	OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:56	Проверяет по 55 вызовов thinkFast в каждом интервале

## 5. Тесты

### PlacementRuleTests.cpp и PlacementFrameTests.cpp

Тесты прочитаны командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/PlacementRuleTests.cpp | nl -ba` и `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/PlacementFrameTests.cpp | nl -ba`.

### Подсчёт проверок

Команды подсчитывали статические места вызова проверочных функций регулярным выражением по stdout `git show` (это подсчёт call-sites, не запуск тестов):

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/PlacementRuleTests.cpp | /srv/dune/venv/bin/python -c 'import sys,re,collections; s=sys.stdin.read(); p=re.compile(r"(?m)^\s*(assert|requirePlacement|requireRect|require)\s*\("); c=collections.Counter(m.group(1) for m in p.finditer(s)); print("static_check_call_sites="+str(sum(c.values()))); print("by_name="+repr(dict(sorted(c.items()))))'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/PlacementFrameTests.cpp | /srv/dune/venv/bin/python -c 'import sys,re,collections; s=sys.stdin.read(); p=re.compile(r"(?m)^\s*(assert|requirePlacement|requireRect|require)\s*\("); c=collections.Counter(m.group(1) for m in p.finditer(s)); print("static_check_call_sites="+str(sum(c.values()))); print("by_name="+repr(dict(sorted(c.items()))))'
```

Вывод:

```text
static_check_call_sites=17
by_name={'require': 1, 'requirePlacement': 16}
static_check_call_sites=3
by_name={'require': 1, 'requireRect': 2}
```

В `PlacementRuleTests.cpp` 16 мест вызова `requirePlacement` и одно место вызова внутреннего `require` (само тело обёртки на строках 25-28); матрица порождает 21 комбинацию «5 видов поверхности × 3 предмета» и «2 вида блокировщика × 3 предмета» (`:195-243`). Список условий/проверок, по одному на call-site:

- `tests/PlacementRuleTests.cpp@9208dcf:33` — тестовая клетка существует перед записью terrain.
- `tests/PlacementRuleTests.cpp@9208dcf:91` — общая функция игрока возвращает ожидаемый результат.
- `tests/PlacementRuleTests.cpp@9208dcf:94` — проверка клика совпадает с общей функцией.
- `tests/PlacementRuleTests.cpp@9208dcf:104` — цвет каждой footprint-клетки согласован с ожидаемым разрешением/запретом.
- `tests/PlacementRuleTests.cpp@9208dcf:107` — у предпросмотра есть окрашенные footprint-клетки.
- `tests/PlacementRuleTests.cpp@9208dcf:111` — разрешённое обычное здание создаёт структуру.
- `tests/PlacementRuleTests.cpp@9208dcf:112` — успешное размещение здания уменьшает количество предметов и сбрасывает place-mode.
- `tests/PlacementRuleTests.cpp@9208dcf:116` — размещение плиты не создаёт объект структуры.
- `tests/PlacementRuleTests.cpp@9208dcf:117` — успешное размещение плиты расходует готовый предмет.
- `tests/PlacementRuleTests.cpp@9208dcf:121` — заблокированное здание не создаётся.
- `tests/PlacementRuleTests.cpp@9208dcf:122` — отказ не меняет количество предметов и готовность.
- `tests/PlacementRuleTests.cpp@9208dcf:189` — изменение terrain после размещения соответствует ожидаемому по каждой клетке footprint.
- `tests/PlacementRuleTests.cpp@9208dcf:285` — человеческому игроку запрещено здание на rock без строительной связи.
- `tests/PlacementRuleTests.cpp@9208dcf:287` — отказ для человека не создаёт здание.
- `tests/PlacementRuleTests.cpp@9208dcf:289` — отказ человеку оставляет предмет готовым.
- `tests/PlacementRuleTests.cpp@9208dcf:300` — ИИ строит на rock без строительной связи.
- `tests/PlacementRuleTests.cpp@9208dcf:27` — реализация `requirePlacement` передаёт false в `require`, который бросает ошибку с сообщением.

В `PlacementFrameTests.cpp`:

- `tests/PlacementFrameTests.cpp@9208dcf:59` — записан ровно один кадр рамки предпросмотра.
- `tests/PlacementFrameTests.cpp@9208dcf:82` — рамка предпросмотра совпадает с рассчитанным прямоугольником камеры/масштаба.
- `tests/PlacementFrameTests.cpp@9208dcf:86` — при 100% рамка совпадает с visual rectangle созданного здания.

Статически в `PlacementFrameTests` тело циклов вызывает проверку строки `:59` и `:82` для 2 зданий × 4 процентов × 7 zoom × 3 позиций (по 168 раз); `:86` вызывается для 2 зданий × 1 случая 100% × 7 zoom × 3 позиции (42 раза). Это подсчёт по циклам исходника, не результат исполнения.

### Полный список include тестовых файлов

Сверено выводом `git show FORK1:tests/PlacementRuleTests.cpp | nl -ba` и `git show FORK1:tests/PlacementFrameTests.cpp | nl -ba`:

```text
PlacementRuleTests.cpp:
  1 #include "ZoomTestSupport.hpp"
  3 #include "UnitDrawRecorder.hpp"
  5 #include "controls/mousestates/cMousePlaceState.h"
  6 #include "data/gfxdata.h"
  7 #include "drawers/cPlaceItDrawer.h"
  8 #include "building/cItemBuilder.h"
  9 #include "gameobjects/structures/cWindTrap.h"
 10 #include "player/cPlayer.h"
11 #include "sidebar/cBuildingList.h"
12 #include "sidebar/cBuildingListUpdater.h"
13 #include "sidebar/cSideBar.h"
15 #include <array>
16 #include <iostream>
17 #include <string>

PlacementFrameTests.cpp:
 1 #include "ZoomTestSupport.hpp"
 3 #include "UnitDrawRecorder.hpp"
 5 #include "drawers/cPlaceItDrawer.h"
 6 #include "gameobjects/structures/cRefinery.h"
 7 #include "gameobjects/structures/cWindTrap.h"
 8 #include "sidebar/cBuildingListItem.h"
10 #include <iostream>
11 #include <memory>
13 #include <vector>
```

### Используемые заголовки и символы; наличие в PORT

Наличие сверено через `git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 -- src tests`, `git grep -n` по PORT и чтение найденных заголовков через `git show`. Обе тестовые единицы и их fixture/helper-файлы отсутствуют в дереве `tests/` PORT.

| FORK1-тест | Заголовок | В PORT |
|---|---|---|
| `PlacementRuleTests` | `tests/ZoomTestSupport.hpp@9208dcf:1` | нет |
| `PlacementRuleTests` | `tests/UnitDrawRecorder.hpp@9208dcf:3` | нет |
| `PlacementRuleTests` | `controls/mousestates/cMousePlaceState.h@9208dcf:5` | `src/controls/mousestates/cMousePlaceState.h@832c953:1` |
| `PlacementRuleTests` | `data/gfxdata.h@9208dcf:6` | `src/data/gfxdata.h@832c953:1` |
| `PlacementRuleTests` | `drawers/cPlaceItDrawer.h@9208dcf:7` | `src/drawers/cPlaceItDrawer.h@832c953:1` |
| `PlacementRuleTests` | `building/cItemBuilder.h@9208dcf:8` | `src/building/cItemBuilder.h@832c953:1` |
| `PlacementRuleTests` | `gameobjects/structures/cWindTrap.h@9208dcf:9` | `src/gameobjects/structures/cWindTrap.h@832c953:1` |
| `PlacementRuleTests` | `player/cPlayer.h@9208dcf:10` | нет по этому пути; новый путь `src/gameobjects/players/cPlayer.h@832c953:1` |
| `PlacementRuleTests` | `sidebar/cBuildingList.h@9208dcf:11` | `src/sidebar/cBuildingList.h@832c953:1` |
| `PlacementRuleTests` | `sidebar/cBuildingListUpdater.h@9208dcf:12` | `src/sidebar/cBuildingListUpdater.h@832c953:1` |
| `PlacementRuleTests` | `sidebar/cSideBar.h@9208dcf:13` | `src/sidebar/cSideBar.h@832c953:1` |
| `PlacementFrameTests` | `tests/ZoomTestSupport.hpp@9208dcf:1` | нет |
| `PlacementFrameTests` | `tests/UnitDrawRecorder.hpp@9208dcf:3` | нет |
| `PlacementFrameTests` | `drawers/cPlaceItDrawer.h@9208dcf:5` | `src/drawers/cPlaceItDrawer.h@832c953:1` |
| `PlacementFrameTests` | `gameobjects/structures/cRefinery.h@9208dcf:6` | `src/gameobjects/structures/cRefinery.h@832c953:1` |
| `PlacementFrameTests` | `gameobjects/structures/cWindTrap.h@9208dcf:7` | `src/gameobjects/structures/cWindTrap.h@832c953:1` |
| `PlacementFrameTests` | `sidebar/cBuildingListItem.h@9208dcf:8` | `src/sidebar/cBuildingListItem.h@832c953:1` |

Ключевые используемые символы и наличие соответствующего API в PORT:

| Символ в тесте | Место использования в FORK1 | В PORT |
|---|---|---|
| `InputRig`, `UnitFrameFixture`, `MapCells`, `CellSize`, `useCamera`, `ScreenWidth`, `ScreenHeight` | `tests/ZoomTestSupport.hpp@9208dcf:26-31,55,121`; `UnitFrameFixture` в `tests/UnitFrameFixture.hpp@9208dcf:11` | нет: helper/fixture отсутствуют в `tests/` PORT |
| `UnitDrawCall`, `unitDrawCalls`, `clearUnitDrawCalls` | `tests/UnitDrawRecorder.hpp@9208dcf:12,35-36` | нет: recorder отсутствует в `tests/` PORT |
| `s_PlaceResult` | `tests/PlacementRuleTests.cpp@9208dcf:90` | есть: `src/gameobjects/players/cPlayer.h@832c953:60` |
| `cPlayer::canPlaceBuildingListItemAt` | `tests/PlacementRuleTests.cpp@9208dcf:90,285` | нет; в PORT есть `canPlaceStructureAt`: `src/gameobjects/players/cPlayer.h@832c953:514-515` и определения в `src/gameobjects/players/cPlayer.cpp@832c953:1950,1986` |
| `cPlayer::placeItem` | `tests/PlacementRuleTests.cpp@9208dcf:109,287,300` | есть: `src/gameobjects/players/cPlayer.h@832c953:487`, реализация `src/gameobjects/players/cPlayer.cpp@832c953:1598` |
| `cMousePlaceState::mayPlaceIt` | `tests/PlacementRuleTests.cpp@9208dcf:94` | есть: `src/controls/mousestates/cMousePlaceState.h@832c953:54`, реализация `:98` |
| `cPlaceItDrawer::drawStatusOfStructureAtCell` | `tests/PlacementRuleTests.cpp@9208dcf:99` | есть: `src/drawers/cPlaceItDrawer.h@832c953:44`, реализация `.cpp@832c953:70` |
| `cPlaceItDrawer::drawStructureIdAtMousePos` | `tests/PlacementFrameTests.cpp@9208dcf:51` (один аргумент) | есть с двумя аргументами `itemToPlace, mouseCell`: `src/drawers/cPlaceItDrawer.h@832c953:42`; ctor также требует `GameContext*, cPlayer*, cStructureUtils*` (`:32`) |
| `global_map`, глобальный массив `players`, `sStructureInfo` | например, `tests/PlacementRuleTests.cpp@9208dcf:32,85,66-75` | нет в коде PORT под этими именами; тестовый `UnitFrameFixture.cpp` FORK1 определяет их (`@9208dcf:25-43`) |
| `cBuildingListItem`, `cItemBuilder`, `cBuildingListUpdater`, `cSideBar`, `cBuildingList` | `tests/PlacementRuleTests.cpp@9208dcf:46-64,86`; `PlacementFrameTests.cpp@9208dcf:48` | есть: `src/sidebar/cBuildingListItem.h@832c953:38`, `src/building/cItemBuilder.h@832c953:33`, `src/sidebar/cBuildingListUpdater.h@832c953:25`, `src/sidebar/cSideBar.h@832c953:70`, `src/sidebar/cBuildingList.h@832c953:44` |
| `WINDTRAP`, `SLAB1`, `SLAB4`, `HUMAN`, `AI_CPU1`, `TANK` | например, `tests/PlacementRuleTests.cpp@9208dcf:202,272,281,292` | есть: `src/include/definitions.h@832c953:71-72,113,131-132,176` |
| `TERRAIN_ROCK`, `TERRAIN_SLAB`, `TERRAIN_SAND`, `TERRAIN_MOUNTAIN`, `TERRAIN_SPICE` | `tests/PlacementRuleTests.cpp@9208dcf:41-44,205-209` | есть как идентификаторы terrain/gfx: `src/data/gfxdata.h@832c953:143-147` |
| `cWindTrap`, `cRefinery` | `tests/PlacementRuleTests.cpp@9208dcf:154`; `PlacementFrameTests.cpp@9208dcf:35-38` | есть: `src/gameobjects/structures/cWindTrap.h@832c953:20`, `cRefinery.h@832c953:20` |

### Файлы, используемые тестами

Сами `PlacementRuleTests.cpp` и `PlacementFrameTests.cpp` не содержат вызовов чтения внешних игровых файлов: проверки используют тестовые объекты, карту, камеру и recorder. Оба создают `UnitFrameFixture` (`PlacementRuleTests.cpp@9208dcf:306`, `PlacementFrameTests.cpp@9208dcf:92`). Fixture под `D2TM_UNIT_FRAME_FIXTURE_ROOT` создаёт `placeholder-<suffix>.png`, `siege-atlas-<suffix>.png`, `siege-shadow-<suffix>.png`, `siege-top-<suffix>.png`, `tank-hd-<suffix>.png`, `tank-hd-shadow-<suffix>.png`, `harvester-hd-<suffix>.png`, `harvester-hd-shadow-<suffix>.png`, `siege-mask-<suffix>.png`, `siege-top-mask-<suffix>.png` и `unit-frame-<suffix>.dat`, где `<suffix>` — `SDL_GetTicks()` (`tests/UnitFrameFixture.cpp@9208dcf:216-229`). `Graphics` загружает созданный `.dat` pack (`:153-156`); промежуточные PNG удаляются после pack-записи (`:281-286`), pack — в деструкторе (`:202-205`).

### WorldObjectScaleTests.cpp

Подсчёт вызовов проверочной функции:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -c 'passed &= expectEqual' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests/WorldObjectScaleTests.cpp
```

Вывод:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:16
```

Файл делает 16 сравнений через `expectEqual`; вызовов `assert` в результатах поиска нет. Общая проверка находится в `expectEqual`: `actual == expected` — `tests/WorldObjectScaleTests.cpp@9208dcf:8`; при несовпадении функция пишет ожидаемое и фактическое значения через `std::cerr` (строки 11-13). `main` возвращает 0 при успешных проверках и 1 иначе, строка 47.

Команда, выводящая строку с каждой проверкой:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'assert|expectEqual|passed \? ' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests/WorldObjectScaleTests.cpp
```

Вывод:

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:6:bool expectEqual(const char *name, int actual, int expected)
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:22:    passed &= expectEqual("100% x", scale100.x, 32);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:23:    passed &= expectEqual("100% y", scale100.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:24:    passed &= expectEqual("100% width", scale100.width, 80);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:25:    passed &= expectEqual("100% height", scale100.height, 52);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:29:    passed &= expectEqual("110% x", scale110.x, 46);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:30:    passed &= expectEqual("110% y", scale110.y, 21);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:31:    passed &= expectEqual("110% width", scale110.width, 88);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:32:    passed &= expectEqual("110% height", scale110.height, 57);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:36:    passed &= expectEqual("125% x", scale125.x, 40);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:37:    passed &= expectEqual("125% y", scale125.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:38:    passed &= expectEqual("125% width", scale125.width, 100);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:39:    passed &= expectEqual("125% height", scale125.height, 65);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:43:    passed &= expectEqual("150% x", scale150.x, 49);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:44:    passed &= expectEqual("150% y", scale150.y, 1);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:45:    passed &= expectEqual("150% width", scale150.width, 120);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:46:    passed &= expectEqual("150% height", scale150.height, 78);
9208dcf5a358f40afd95c99480e4e09f781ed566:tests/WorldObjectScaleTests.cpp:47:    return passed ? 0 : 1;
```

### Полные построчные данные проверок для `tests.tsv`

```tsv
ревизия	символ или проверка	путь@ревизия:строка	что проверяет	входы	ожидаемый выход
9208dcf	100% x	tests/WorldObjectScaleTests.cpp@9208dcf:22	Координату x для базового прямоугольника НПЗ	Вызов строки 21: (0,0,96,64); scale100.x	32
9208dcf	100% y	tests/WorldObjectScaleTests.cpp@9208dcf:23	Координату y для базового прямоугольника НПЗ	Вызов строки 21: (0,0,96,64); scale100.y	1
9208dcf	100% width	tests/WorldObjectScaleTests.cpp@9208dcf:24	Ширину кадра Харвестера при базовом размере	Вызов строки 21: (0,0,96,64); scale100.width	80
9208dcf	100% height	tests/WorldObjectScaleTests.cpp@9208dcf:25	Высоту кадра Харвестера при базовом размере	Вызов строки 21: (0,0,96,64); scale100.height	52
9208dcf	110% x	tests/WorldObjectScaleTests.cpp@9208dcf:29	Координату x для прямоугольника НПЗ 106x70, начинающегося в (10,20)	Вызов строки 28: (10,20,106,70); scale110.x	46
9208dcf	110% y	tests/WorldObjectScaleTests.cpp@9208dcf:30	Координату y для прямоугольника НПЗ 106x70, начинающегося в (10,20)	Вызов строки 28: (10,20,106,70); scale110.y	21
9208dcf	110% width	tests/WorldObjectScaleTests.cpp@9208dcf:31	Ширину кадра Харвестера при прямоугольнике НПЗ 106x70	Вызов строки 28: (10,20,106,70); scale110.width	88
9208dcf	110% height	tests/WorldObjectScaleTests.cpp@9208dcf:32	Высоту кадра Харвестера при прямоугольнике НПЗ 106x70	Вызов строки 28: (10,20,106,70); scale110.height	57
9208dcf	125% x	tests/WorldObjectScaleTests.cpp@9208dcf:36	Координату x для прямоугольника НПЗ 120x80	Вызов строки 35: (0,0,120,80); scale125.x	40
9208dcf	125% y	tests/WorldObjectScaleTests.cpp@9208dcf:37	Координату y для прямоугольника НПЗ 120x80	Вызов строки 35: (0,0,120,80); scale125.y	1
9208dcf	125% width	tests/WorldObjectScaleTests.cpp@9208dcf:38	Ширину кадра Харвестера при прямоугольнике НПЗ 120x80	Вызов строки 35: (0,0,120,80); scale125.width	100
9208dcf	125% height	tests/WorldObjectScaleTests.cpp@9208dcf:39	Высоту кадра Харвестера при прямоугольнике НПЗ 120x80	Вызов строки 35: (0,0,120,80); scale125.height	65
9208dcf	150% x	tests/WorldObjectScaleTests.cpp@9208dcf:43	Координату x для прямоугольника НПЗ 144x96	Вызов строки 42: (0,0,144,96); scale150.x	49
9208dcf	150% y	tests/WorldObjectScaleTests.cpp@9208dcf:44	Координату y для прямоугольника НПЗ 144x96	Вызов строки 42: (0,0,144,96); scale150.y	1
9208dcf	150% width	tests/WorldObjectScaleTests.cpp@9208dcf:45	Ширину кадра Харвестера при прямоугольнике НПЗ 144x96	Вызов строки 42: (0,0,144,96); scale150.width	120
9208dcf	150% height	tests/WorldObjectScaleTests.cpp@9208dcf:46	Высоту кадра Харвестера при прямоугольнике НПЗ 144x96	Вызов строки 42: (0,0,144,96); scale150.height	78
```

Используемые заголовки и символы:

| Элемент | FORK1 | Наличие в PORT |
|---|---|---|
| `"utils/WorldObjectScale.hpp"` | `tests/WorldObjectScaleTests.cpp@9208dcf:1` | `нет`: путь `src/utils/WorldObjectScale.hpp` не возвращён `git ls-tree PORT -- ...`; `WorldObjectScale`/тип в PORT не находятся `git grep` |
| `<iostream>` | `tests/WorldObjectScaleTests.cpp@9208dcf:3` | `src/drawers/SDLDrawer.cpp@832c953:19` |
| `WorldObjectLayout` | Определение `src/utils/WorldObjectScale.hpp@9208dcf:6`, употребление в тесте с 20-й строки | `нет`: совпадений `git grep` в `src tests` PORT нет |
| `refineryHarvesterLayout` | Определение `src/utils/WorldObjectScale.hpp@9208dcf:18`, вызовы `tests/WorldObjectScaleTests.cpp@9208dcf:21,28,35,42` | `нет`: совпадений `git grep` в `src tests` PORT нет |
| `expectEqual` | Локальная функция `tests/WorldObjectScaleTests.cpp@9208dcf:6` | `нет`: совпадений `git grep` в `src tests` PORT нет |
| `main()` | `tests/WorldObjectScaleTests.cpp@9208dcf:17` | `нет`: тестовый файл в дереве PORT отсутствует |
| `std::cerr` | `tests/WorldObjectScaleTests.cpp@9208dcf:11` | Есть как стандартный поток в `src/drawers/SDLDrawer.cpp@832c953:44`; это не проверочная функция теста |

Команды, проверяющие присутствие заголовка и проектных символов в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree 832c953a94a632d57872349013f7ed1a37434715 -- tests/WorldObjectScaleTests.cpp src/utils/WorldObjectScale.hpp
git grep -n -E 'WorldObjectLayout|refineryHarvesterLayout|WorldObjectScale' 832c953a94a632d57872349013f7ed1a37434715 -- src tests
git grep -n -F 'expectEqual' 832c953a94a632d57872349013f7ed1a37434715 -- src tests
```

Вывод `git ls-tree`: пусто для обоих указанных путей (код возврата 0). Выводы обеих `git grep`: пусто (код возврата 1).

Тест включает `src/utils/WorldObjectScale.hpp` и `<iostream>). По исходнику он не читает файлы во время выполнения: входные прямоугольники и эталоны заданы литералами, результат выводится только в `std::cerr` при ошибке.

### OutpostFrameTests.cpp и регистрация CTest

Команда подсчёта проверок:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/OutpostFrameTests.cpp | /srv/dune/venv/bin/python -c 'import sys; lines=sys.stdin.readlines(); checks=("if (frames != expectedFrames)", "if (callsBetweenChanges.size() != 32)", "if (callsBetweenChanges[interval] != 55)"); interval_count=int(next(line for line in lines if "callsBetweenChanges.size() !=" in line).split("!=")[1].split(")")[0].strip()); print("assert_calls", sum(line.count("assert(") for line in lines)); print("if_conditions", sum(line.lstrip().startswith("if (") for line in lines)); print("validation_sites", sum(any(check in line for check in checks) for line in lines)); print("comparisons_if_expected_path_reaches_all_intervals", 2 + interval_count)'

Вывод:

    assert_calls 0
    if_conditions 5
    validation_sites 3
    comparisons_if_expected_path_reaches_all_intervals 34

Счёт: assert-вызовов нет; в файле пять if-условий, из них три места сравнивают результат с ожиданием и являются проверками теста. При полном ожидаемом цикле эти три места выполняют 34 проверочных сравнения: один вектор кадров, одно количество интервалов и 32 сравнения длины каждого интервала.

Что проверяет каждая проверка:
    tests/OutpostFrameTests.cpp@9208dcf:42 — собранный вектор равен ожидаемому порядку кадров 1…31, 0, 1.
    tests/OutpostFrameTests.cpp@9208dcf:51 — число интервалов между сменами кадра равно 32.
    tests/OutpostFrameTests.cpp@9208dcf:56 — каждый интервал содержит ровно 55 вызовов thinkFast.

Проверка строки 26 фиксирует смену кадра для накопления последовательности; строка 28 пропускает начальный неполный интервал. Они не сравнивают результат теста с ожиданием.

Подготовка теста: строка 12 задаёт RADAR-флаги; строки 13–16 создают cOutPost и задают ширину, высоту, начальный кадр; строки 22–34 собирают наблюдаемые смены кадра. Файлов, которые тест читает с диска, нет: тест не открывает файлы, он работает с объектом cOutPost и данными в памяти.

Заголовки теста (строки в FORK1): d2tmc.h (1), definitions.h (2), gameobjects/structures/cOutPost.h (3), стандартные <iostream> (5), <memory> (6), <sstream> (7), <vector> (8).
Символы, используемые тестом, и наличие в PORT:
    sStructureInfo — нет в PORT; тест обращается к глобальному массиву в строке tests/OutpostFrameTests.cpp@9208dcf:12.
    RADAR — есть: src/include/definitions.h@832c953:121.
    s_FlagInfo — есть: src/gameobjects/structures/cStructureInfo.h@832c953:31.
    cOutPost — есть: src/gameobjects/structures/cOutPost.h@832c953:20; конструктор — строка 22.
    thinkFast — есть: src/gameobjects/structures/cOutPost.h@832c953:24 и реализация src/gameobjects/structures/cOutPost.cpp@832c953:30.
    setWidth, setHeight, setFrame, getFrame — есть в базовом типе: src/gameobjects/structures/cAbstractStructure.h@832c953:269, :268, :277 и :203 соответственно. cOutPost наследует cAbstractStructure в src/gameobjects/structures/cOutPost.h@832c953:20.
    Заголовок d2tmc.h — нет среди путей дерева PORT.
    Заголовок definitions.h — есть как src/include/definitions.h; определение RADAR — строка 121.
    Заголовок gameobjects/structures/cOutPost.h — есть как src/gameobjects/structures/cOutPost.h.
    <iostream>, <memory>, <sstream>, <vector> — стандартные заголовки C++; они не являются файлами дерева PORT.
    Из стандартных библиотечных символов тест использует std::make_unique (строка 13), std::vector (18–19), std::ostringstream (43), std::cerr (48, 52, 57), std::cout (62) и size_t (55); их предоставляет стандартная библиотека C++.

Команда поиска символов и файлов-заголовков в PORT:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -e sStructureInfo -e structureInfos -e s_FlagInfo -e 'inline constexpr int RADAR' -e 'class cOutPost' -e 'void cOutPost::thinkFast' -e 'void setWidth' -e 'void setHeight' -e 'void setFrame' -e 'getFrame()' 832c953a94a632d57872349013f7ed1a37434715
    git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | /srv/dune/venv/bin/python -c 'import sys; terms=("d2tmc.h", "definitions.h", "cOutPost.h", "cStructureInfo.h", "cAbstractStructure.h"); print("".join(line for line in sys.stdin if any(line.rstrip().endswith(t) for t in terms)), end="")'

Ключевые строки вывода git grep:
    src/gameobjects/structures/cStructureInfo.h:31:struct s_FlagInfo {
    src/gameobjects/structures/cAbstractStructure.h:203:    int getFrame() {
    src/gameobjects/structures/cAbstractStructure.h:268:    void setHeight(int height);
    src/gameobjects/structures/cAbstractStructure.h:269:    void setWidth(int width);
    src/gameobjects/structures/cAbstractStructure.h:277:    void setFrame(int frame);
    src/gameobjects/structures/cOutPost.cpp:30:void cOutPost::thinkFast()
    src/gameobjects/structures/cOutPost.h:20:class cOutPost : public cAbstractStructure {
    src/gameobjects/structures/cOutPost.h:24:    void thinkFast() override;
    src/include/definitions.h:121:inline constexpr int RADAR = 9; // = OUTPOST (cOutPost)

Дополнительная сверка отсутствующего глобала и заголовков выполнена командами ниже. Пустой результат sStructureInfo подтверждает отсутствие этого имени в PORT; structureInfos — объект другой системы, применённый в cInfoContextCreator.
Дополнительная команда и вывод для проектных символов:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n sStructureInfo 832c953a94a632d57872349013f7ed1a37434715 -- src; printf 'grep_exit=%s\n' "$?"
    git grep -n -e s_FlagInfo -e 'inline constexpr int RADAR' -e 'class cOutPost' -e 'void cOutPost::thinkFast' -e 'getFrame()' -e 'setWidth(' -e 'setHeight(' -e 'setFrame(' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/structures src/include/definitions.h
    git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | /srv/dune/venv/bin/python -c 'import sys; terms=("d2tmc.h", "definitions.h", "cOutPost.h", "cStructureInfo.h", "cAbstractStructure.h"); print("".join(line for line in sys.stdin if any(line.rstrip().endswith(t) for t in terms)), end="")'

    grep_exit=1
     src/gameobjects/structures/cAbstractStructure.cpp:445:void cAbstractStructure::setWidth(int width)
     src/gameobjects/structures/cAbstractStructure.cpp:452:void cAbstractStructure::setHeight(int height)
     src/gameobjects/structures/cAbstractStructure.cpp:472:void cAbstractStructure::setFrame(int frame)
     src/gameobjects/structures/cAbstractStructure.cpp:798:    setFrame(0);
     src/gameobjects/structures/cAbstractStructure.h:203:    int getFrame() {
     src/gameobjects/structures/cAbstractStructure.h:268:    void setHeight(int height);
     src/gameobjects/structures/cAbstractStructure.h:269:    void setWidth(int width);
     src/gameobjects/structures/cAbstractStructure.h:277:    void setFrame(int frame);
     src/gameobjects/structures/cOutPost.cpp:30:void cOutPost::thinkFast()
     src/gameobjects/structures/cOutPost.h:20:class cOutPost : public cAbstractStructure {
     src/gameobjects/structures/cOutPost.h:22:    cOutPost();
     src/gameobjects/structures/cOutPost.h:24:    void thinkFast() override;
     src/gameobjects/structures/cStructureInfo.h:31:struct s_FlagInfo {
     src/gameobjects/structures/cStructureInfo.h:45:    std::vector<s_FlagInfo> flags;
     src/include/definitions.h:121:inline constexpr int RADAR = 9; // = OUTPOST (cOutPost)
    src/gameobjects/structures/cAbstractStructure.h
    src/gameobjects/structures/cOutPost.h
    src/gameobjects/structures/cStructureInfo.h
    src/include/definitions.h


## Регистрация CTest и исходники четырёх тестов в FORK1

Команды:
    export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
    git grep -n -e world_object_scale -e placement_rule_tests -e placement_frame_tests -e outpost_frame_tests 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt tests/UnitRenderFixture.cmake
    git grep -n -e WorldObjectScaleTests.cpp -e PlacementRuleTests.cpp -e PlacementFrameTests.cpp -e OutpostFrameTests.cpp 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt tests/UnitRenderFixture.cmake

Вывод первой команды (имена/вызовы регистрации):

    9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:299:        world_object_scale_tests
    9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:303:        world_object_scale_tests
    9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:307:    add_test(NAME world_object_scale_selection COMMAND world_object_scale_tests)
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:127:add_unit_frame_test(placement_frame_tests placement_frame PlacementFrameTests.cpp recorded)
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:131:add_unit_frame_test(placement_rule_tests placement_rule PlacementRuleTests.cpp recorded)
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:133:add_unit_frame_test(outpost_frame_tests outpost_frame OutpostFrameTests.cpp recorded)

Вывод второй команды (пути исходников):

    9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt:300:        tests/WorldObjectScaleTests.cpp
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:56:    "${CMAKE_CURRENT_SOURCE_DIR}/tests/PlacementFrameTests.cpp"
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:59:    "${CMAKE_CURRENT_SOURCE_DIR}/tests/PlacementRuleTests.cpp"
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:127:add_unit_frame_test(placement_frame_tests placement_frame PlacementFrameTests.cpp recorded)
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:131:add_unit_frame_test(placement_rule_tests placement_rule PlacementRuleTests.cpp recorded)
    9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake:133:add_unit_frame_test(outpost_frame_tests outpost_frame OutpostFrameTests.cpp recorded)

Матрица строк:
    PlacementRuleTests.cpp — CMakeLists.txt: регистрация CTest нет, строка исходника нет. UnitRenderFixture.cmake: CTest-вызов add_unit_frame_test на строке 131; отдельная строка исходника на строке 59.
    PlacementFrameTests.cpp — CMakeLists.txt: регистрация CTest нет, строка исходника нет. UnitRenderFixture.cmake: CTest-вызов add_unit_frame_test на строке 127; отдельная строка исходника на строке 56.
    WorldObjectScaleTests.cpp — CMakeLists.txt: регистрация CTest на строке 307, точное имя теста world_object_scale_selection (команда world_object_scale_tests); отдельная строка исходника на строке 300. UnitRenderFixture.cmake: регистрация нет, строка исходника нет.
    OutpostFrameTests.cpp — CMakeLists.txt: регистрация CTest нет, строка исходника нет. UnitRenderFixture.cmake: CTest-вызов add_unit_frame_test на строке 133; путь OutpostFrameTests.cpp указан в том же вызове, отдельной строки списка исходников нет.

### Сводная таблица tests.tsv

Отдельная строка таблицы соответствует каждому проверочному месту. Для PlacementRuleTests указаны 16 проверок-потребителей; helper require вынесен дополнительной строкой. Для WorldObjectScaleTests — 16 сравнений, для PlacementFrameTests — 3 места, для OutpostFrameTests — 3 места.

~~~tsv
файл	проверка и путь@FORK1:строка	что проверяет	символы и заголовки	есть ли каждый в PORT	читаемые файлы
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:33	Тестовая клетка существует перед записью terrain.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:91	Общая функция игрока возвращает ожидаемый результат.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:94	Проверка клика возвращает ожидаемый результат общей функции.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:104	Цвет каждой footprint-клетки согласован с ожидаемым разрешением или запретом.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:107	У предпросмотра есть окрашенные footprint-клетки.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:111	Разрешённое обычное здание создаёт структуру.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:112	Успешное размещение здания уменьшает число предметов и сбрасывает place-mode.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:116	Размещение плиты не создаёт объект структуры.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:117	Успешное размещение плиты расходует готовый предмет.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:121	Заблокированное здание не создаётся.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:122	Отказ не меняет количество предметов и готовность.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:189	Изменение terrain после размещения совпадает с ожидаемым на каждой клетке footprint.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:285	Человеческому игроку запрещено здание на rock без строительной связи.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:287	Отказ для человека не создаёт здание.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:289	Отказ человеку оставляет предмет готовым.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:300	ИИ строит на rock без строительной связи.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementRuleTests.cpp	tests/PlacementRuleTests.cpp@9208dcf:27	Внутренний requirePlacement передаёт условие в require, который сообщает ошибку при false; это вспомогательная проверка общего тестового helper.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; controls/mousestates/cMousePlaceState.h@9208dcf:5; data/gfxdata.h@9208dcf:6; drawers/cPlaceItDrawer.h@9208dcf:7; building/cItemBuilder.h@9208dcf:8; gameobjects/structures/cWindTrap.h@9208dcf:9; player/cPlayer.h@9208dcf:10; sidebar/cBuildingList.h@9208dcf:11; sidebar/cBuildingListUpdater.h@9208dcf:12; sidebar/cSideBar.h@9208dcf:13; <array>@15; <iostream>@16; <string>@17. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; s_PlaceResult, canPlaceBuildingListItemAt, placeItem, mayPlaceIt, drawStatusOfStructureAtCell; global_map, players, sStructureInfo; cBuildingListItem, cItemBuilder, cBuildingListUpdater, cSideBar, cBuildingList; WINDTRAP, SLAB1, SLAB4, HUMAN, AI_CPU1, TANK; TERRAIN_ROCK, TERRAIN_SLAB, TERRAIN_SAND, TERRAIN_MOUNTAIN, TERRAIN_SPICE.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp, InputRig/UnitFrameFixture helpers and canPlaceBuildingListItemAt absent; PORT has canPlaceStructureAt@src/gameobjects/players/cPlayer.h@832c953:514-515. s_PlaceResult@src/gameobjects/players/cPlayer.h@832c953:60. placeItem, mayPlaceIt, drawStatusOfStructureAtCell, building/sidebar/structure API, types and terrain identifiers present at lines in RECON.md, §5. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementFrameTests.cpp	tests/PlacementFrameTests.cpp@9208dcf:59	Записан ровно один кадр рамки предпросмотра; повторяется по матрице циклов 168 раз.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; drawers/cPlaceItDrawer.h@9208dcf:5; gameobjects/structures/cRefinery.h@9208dcf:6; gameobjects/structures/cWindTrap.h@9208dcf:7; sidebar/cBuildingListItem.h@9208dcf:8; <iostream>@10; <memory>@11; <vector>@13. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; drawStructureIdAtMousePos, cRefinery, cWindTrap, cBuildingListItem.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp and fixture/helpers absent; drawStructureIdAtMousePos has two arguments and a context constructor@src/drawers/cPlaceItDrawer.h@832c953:32,42; cRefinery@src/gameobjects/structures/cRefinery.h@832c953:20; cWindTrap@src/gameobjects/structures/cWindTrap.h@832c953:20; cBuildingListItem@src/sidebar/cBuildingListItem.h@832c953:38. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementFrameTests.cpp	tests/PlacementFrameTests.cpp@9208dcf:82	Рамка предпросмотра совпадает с рассчитанным прямоугольником камеры и масштаба; повторяется 168 раз.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; drawers/cPlaceItDrawer.h@9208dcf:5; gameobjects/structures/cRefinery.h@9208dcf:6; gameobjects/structures/cWindTrap.h@9208dcf:7; sidebar/cBuildingListItem.h@9208dcf:8; <iostream>@10; <memory>@11; <vector>@13. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; drawStructureIdAtMousePos, cRefinery, cWindTrap, cBuildingListItem.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp and fixture/helpers absent; drawStructureIdAtMousePos has two arguments and a context constructor@src/drawers/cPlaceItDrawer.h@832c953:32,42; cRefinery@src/gameobjects/structures/cRefinery.h@832c953:20; cWindTrap@src/gameobjects/structures/cWindTrap.h@832c953:20; cBuildingListItem@src/sidebar/cBuildingListItem.h@832c953:38. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/PlacementFrameTests.cpp	tests/PlacementFrameTests.cpp@9208dcf:86	При 100% рамка совпадает с visual rectangle здания; повторяется 42 раза.	ZoomTestSupport.hpp@9208dcf:1; UnitDrawRecorder.hpp@9208dcf:3; drawers/cPlaceItDrawer.h@9208dcf:5; gameobjects/structures/cRefinery.h@9208dcf:6; gameobjects/structures/cWindTrap.h@9208dcf:7; sidebar/cBuildingListItem.h@9208dcf:8; <iostream>@10; <memory>@11; <vector>@13. Symbols: InputRig, UnitFrameFixture, MapCells, CellSize, useCamera, ScreenWidth, ScreenHeight; UnitDrawCall, unitDrawCalls, clearUnitDrawCalls; drawStructureIdAtMousePos, cRefinery, cWindTrap, cBuildingListItem.	ZoomTestSupport.hpp, UnitDrawRecorder.hpp and fixture/helpers absent; drawStructureIdAtMousePos has two arguments and a context constructor@src/drawers/cPlaceItDrawer.h@832c953:32,42; cRefinery@src/gameobjects/structures/cRefinery.h@832c953:20; cWindTrap@src/gameobjects/structures/cWindTrap.h@832c953:20; cBuildingListItem@src/sidebar/cBuildingListItem.h@832c953:38. Standard headers come from toolchain.	External game files are not read. UnitFrameFixture creates placeholder-<suffix>.png, siege-atlas-<suffix>.png, siege-shadow-<suffix>.png, siege-top-<suffix>.png, tank-hd-<suffix>.png, tank-hd-shadow-<suffix>.png, harvester-hd-<suffix>.png, harvester-hd-shadow-<suffix>.png, siege-mask-<suffix>.png, siege-top-mask-<suffix>.png, and unit-frame-<suffix>.dat; Graphics loads this synthetic pack; suffix = SDL_GetTicks().
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:22	100%: x ожидается 32.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:23	100%: y ожидается 1.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:24	100%: width ожидается 80.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:25	100%: height ожидается 52.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:29	110%: x ожидается 46.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:30	110%: y ожидается 21.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:31	110%: width ожидается 88.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:32	110%: height ожидается 57.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:36	125%: x ожидается 40.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:37	125%: y ожидается 1.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:38	125%: width ожидается 100.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:39	125%: height ожидается 65.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:43	150%: x ожидается 49.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:44	150%: y ожидается 1.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:45	150%: width ожидается 120.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/WorldObjectScaleTests.cpp	tests/WorldObjectScaleTests.cpp@9208dcf:46	150%: height ожидается 78.	utils/WorldObjectScale.hpp@9208dcf:1; <iostream>@3. Symbols: WorldObjectLayout@src/utils/WorldObjectScale.hpp@9208dcf:6; refineryHarvesterLayout@src/utils/WorldObjectScale.hpp@9208dcf:18; expectEqual@tests/WorldObjectScaleTests.cpp@9208dcf:6; std::cerr@tests/WorldObjectScaleTests.cpp@9208dcf:11.	WorldObjectScale.hpp, WorldObjectLayout, refineryHarvesterLayout and expectEqual absent in PORT; <iostream> and std::cerr are standard library/toolchain items; std::cerr is also used in SDLDrawer.cpp@832c953:44.	Файлов при выполнении нет: прямоугольники и ожидания заданы литералами.
tests/OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:42	Собранный вектор кадров равен ожидаемой последовательности 1…31, 0, 1.	d2tmc.h@9208dcf:1; definitions.h@9208dcf:2; gameobjects/structures/cOutPost.h@9208dcf:3; <iostream>@5; <memory>@6; <sstream>@7; <vector>@8. Symbols: sStructureInfo, RADAR, s_FlagInfo, cOutPost, thinkFast, setWidth, setHeight, setFrame, getFrame.	d2tmc.h and sStructureInfo absent; RADAR@src/include/definitions.h@832c953:121; s_FlagInfo@src/gameobjects/structures/cStructureInfo.h@832c953:31; cOutPost and thinkFast@src/gameobjects/structures/cOutPost.h@832c953:20,24; setWidth/setHeight/setFrame/getFrame@src/gameobjects/structures/cAbstractStructure.h@832c953:268-269,277,203. Standard headers come from toolchain.	Файлов с диска нет: объект и данные создаются в памяти.
tests/OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:51	Число интервалов между сменами кадра равно 32.	d2tmc.h@9208dcf:1; definitions.h@9208dcf:2; gameobjects/structures/cOutPost.h@9208dcf:3; <iostream>@5; <memory>@6; <sstream>@7; <vector>@8. Symbols: sStructureInfo, RADAR, s_FlagInfo, cOutPost, thinkFast, setWidth, setHeight, setFrame, getFrame.	d2tmc.h and sStructureInfo absent; RADAR@src/include/definitions.h@832c953:121; s_FlagInfo@src/gameobjects/structures/cStructureInfo.h@832c953:31; cOutPost and thinkFast@src/gameobjects/structures/cOutPost.h@832c953:20,24; setWidth/setHeight/setFrame/getFrame@src/gameobjects/structures/cAbstractStructure.h@832c953:268-269,277,203. Standard headers come from toolchain.	Файлов с диска нет: объект и данные создаются в памяти.
tests/OutpostFrameTests.cpp	tests/OutpostFrameTests.cpp@9208dcf:56	Каждый интервал содержит ровно 55 вызовов thinkFast; один call-site выполняет до 32 сравнений.	d2tmc.h@9208dcf:1; definitions.h@9208dcf:2; gameobjects/structures/cOutPost.h@9208dcf:3; <iostream>@5; <memory>@6; <sstream>@7; <vector>@8. Symbols: sStructureInfo, RADAR, s_FlagInfo, cOutPost, thinkFast, setWidth, setHeight, setFrame, getFrame.	d2tmc.h and sStructureInfo absent; RADAR@src/include/definitions.h@832c953:121; s_FlagInfo@src/gameobjects/structures/cStructureInfo.h@832c953:31; cOutPost and thinkFast@src/gameobjects/structures/cOutPost.h@832c953:20,24; setWidth/setHeight/setFrame/getFrame@src/gameobjects/structures/cAbstractStructure.h@832c953:268-269,277,203. Standard headers come from toolchain.	Файлов с диска нет: объект и данные создаются в памяти.
~~~

### Выборочная сверка корневой нитью

Команды и выводы:

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat e7a1c04f
~~~
~~~text
commit e7a1c04f3cf11483db315cd977f313c4f21ca752
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 10:23:48 2026 +0300

    Use one placement rule for the preview, the click and the placement

    The placement preview, the click check and placeItem now ask the same
    rule: a regular building and SLAB1 need rock or slab under every cell,
    SLAB4 keeps its concrete exception, a structure blocks every type except
    SLAB4, and any unit blocks a regular building. A refused click keeps the
    item and the placement mode, plays no sound and shows the reason.

    Behavior changes: the preview, the click and the placement no longer
    disagree; a refused placement shows a message in Russian or English and
    the item stays ready to place.

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 src/controls/mousestates/cMousePlaceState.cpp | 160 +++++++++-------------
 src/controls/mousestates/cMousePlaceState.h   |   3 +-
 src/drawers/cPlaceItDrawer.cpp                | 112 +++-------------
 src/player/cPlayer.cpp                        |  91 ++++++++++++-
 src/player/cPlayer.h                          |   3 +
 tests/PlacementRuleTests.cpp                  | 184 ++++++++++++++++++++++++++
 tests/UnitRenderFixture.cmake                 |   2 +
 7 files changed, 360 insertions(+), 195 deletions(-)
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'canPlaceBuildingListItemAt' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
~~~
~~~text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMousePlaceState.cpp:105:        result = m_player->canPlaceBuildingListItemAt(mouseCell, structureType);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMousePlaceState.cpp:120:    const s_PlaceResult placement = m_player->canPlaceBuildingListItemAt(mouseCell, itemToPlace->getBuildId());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cPlaceItDrawer.cpp:45:    const s_PlaceResult placement = player->canPlaceBuildingListItemAt(mouseCell, structureId);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.cpp:1518:                          ? canPlaceBuildingListItemAt(destinationCell, iStructureTypeId).success
9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.cpp:2012:s_PlaceResult cPlayer::canPlaceBuildingListItemAt(int iCell, int iStructureType)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/player/cPlayer.h:438:    s_PlaceResult canPlaceBuildingListItemAt(int iCell, int iStructureType);
~~~

### Выборочная сверка корневой нитью для пункта 2

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'canPlace|mayPlace|placeStructure|placeItem' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/players/brains
~~~
~~~text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainCampaign.cpp:1739:                player->placeItem(iCll, pItem);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1183:            const s_PlaceResult &placeResult = player->canPlaceStructureAt(iCll, pItem->getBuildId());
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp:1188:                    player->placeItem(iCll, pItem);
~~~

### Выборочная сверка корневой нитью для пункта 3

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat c655ceb6
~~~
~~~text
commit c655ceb600abc910beef8c926f48839c5d1d2534
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Wed Nov 4 00:22:28 2026 +0300

    Redraw the Harvester from the owner's 3D model and centre it on the refinery pad

    All eight directions are painted over renders of one 3D model, so the
    vehicle keeps its shape when it turns. The House colour covers the rear
    roof, the cab with its hatch and, at 7 and 11 o'clock, the rear roof strip
    around its lamps. The docked Harvester is moved so its body sits in the
    middle of the refinery pad.

    Behavior changes: new Harvester body, shadow and House mask atlases in
    sdl_data_hd4.dat; a Harvester docked at a refinery is drawn 3.25 logical px
    further left and 2.375 logical px lower.

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 codex-direct/U23/JOURNAL.md                    |  30 +++
 codex-direct/U23/fade.py                       | 175 ++++++++++++++++
 codex-direct/U23/gen/UNIT_HARVESTER.SHA256SUMS | 104 ++++++++++
 codex-direct/U23/shift.py                      |  46 +++++
 resources/bin/data/sdl_data_hd4.dat            |   4 +-
 src/utils/WorldObjectScale.hpp                 |   6 +-
 tests/WorldObjectScaleTests.cpp                |  16 +-
 tools/units3d/units/UNIT_HARVESTER/unit.json   | 268 +++++++++++++------------
 8 files changed, 506 insertions(+), 143 deletions(-)
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'logicalOffsetX|logicalOffsetY' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/utils/WorldObjectScale.hpp
~~~
~~~text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:26:    constexpr float logicalOffsetX = 32.375F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:27:    constexpr float logicalOffsetY = 0.625F;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:32:            refineryWidth * logicalOffsetX / logicalRefineryWidth
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/WorldObjectScale.hpp:35:            refineryHeight * logicalOffsetY / logicalRefineryHeight
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -A 7 'void cStructureDrawer::drawStructureAnimationRefinery' 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cStructureDrawer.cpp
~~~
~~~text
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp:283:void cStructureDrawer::drawStructureAnimationRefinery(cAbstractStructure *structure)
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-284-{
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-285-    d2tm_assert(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-286-    d2tm_assert(structure->getType() == REFINERY);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-287-
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-288-    drawStructureAnimation(structure);
832c953a94a632d57872349013f7ed1a37434715:src/drawers/cStructureDrawer.cpp-289-}
~~~

### Выборочная сверка корневой нитью для пункта 4

~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show --stat 849650d0
~~~
~~~text
commit 849650d06d6c7a2e9bd568a72ebeb7d97fb86382
Author: PavelSlaven <55245062+PavelSlaven@users.noreply.github.com>
Date:   Sat Nov 7 11:11:24 2026 +0300

    Turn the Outpost radar dish in 32 frames

    The owner asked for the dish to turn slower again and chose the smooth
    option. BUILD_RADAR now holds 32 frames of 11.25 degrees (256x8192);
    the even frames are the previous 16. cOutPost::thinkFast keeps the
    frame time of 55 calls and cycles frames 0-31, so a full turn takes
    about 8.8 s instead of 4.4 s. BUILD_RADAR_SHADOW repeats the old frame
    0 thirty-two times; the transparent flag overlay keeps its own 8-frame
    timer and is unchanged.

    outpost_frame_tests now expects the frame order 1-31, 0, 1 with 55
    calls between changes, and the pack tests expect 32 Outpost frames.

    Behavior changes: the Outpost dish turns half as fast again, in 32
    steps.

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 resources/bin/data/sdl_data_hd4.dat                       |  4 ++--
 resources/hd/master4/sdl_data/0026_BUILD_RADAR.png        |  4 ++--
 resources/hd/master4/sdl_data/0027_BUILD_RADAR_SHADOW.png |  4 ++--
 src/gameobjects/structures/cOutPost.cpp                   |  2 +-
 tests/OutpostFrameTests.cpp                               | 12 ++++++------
 tools/building_angle/tests/test_angle.py                  |  4 ++--
 tools/building_angle/tests/test_pilot_pack.py             |  2 +-
 tools/building_angle/tests/test_rollout_pack.py           | 10 +++++-----
 8 files changed, 21 insertions(+), 21 deletions(-)
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'TIMER_flag > 54|iFrame > 31' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/gameobjects/structures/cOutPost.cpp
~~~
~~~text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOutPost.cpp:24:    if (TIMER_flag > 54) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/cOutPost.cpp:27:        if (iFrame > 31) {
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'BUILD_RADAR =|getSurface\(BUILD_RADAR\)|getTexture\(BUILD_RADAR_SHADOW\)' 832c953a94a632d57872349013f7ed1a37434715 -- src/data/gfxdata.h src/context/cInfoContextCreator.cpp
~~~
~~~text
832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1546:    structureInfos[RADAR].bmp = m_gfxdata->getSurface(BUILD_RADAR);
832c953a94a632d57872349013f7ed1a37434715:src/context/cInfoContextCreator.cpp:1547:    structureInfos[RADAR].shadow = m_gfxdata->getTexture(BUILD_RADAR_SHADOW); // shadow
832c953a94a632d57872349013f7ed1a37434715:src/data/gfxdata.h:50:constexpr int BUILD_RADAR = 26; /* BMP  */
~~~
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/sdl_data_hd4.dat
~~~
~~~text
133
~~~
