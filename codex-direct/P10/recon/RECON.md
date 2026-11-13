# RECON-P10R

## Чтение

- Прочитан целиком `/srv/dune/tasks/load-check/PORT_PLAN.md` отдельным вызовом `cat`; вывод содержал разделы 1–8. В нём указан источник порядка шагов и приёмки `docs/PLAN_units_sega_upstream.md` §§3.2 и 5.3, а также карточка `codex-direct/launch-card-27.md`.
- Команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '9,36p;592,686p;800,845p;915,931p'` вывела таблицу функций, разделы четырёх функций, тестовый реестр и риски, требуемые заданием.
- Команда `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р63\.'` вывела одну строку решения Р63: «Новые возможности апстрима (туман войны с памятью, значок нехватки энергии, предел юнитов, вступительный ролик, `preferences.ini`, папки музыки) берутся как есть; где новинка спорит с функцией форка, ведущий спрашивает владельца на шаге этой функции».
- Прочитан целиком `docs/PLAN_units_sega_upstream.md@62e1ff6`: исходный план §3.2 требует переноса функций по одной с отдельными тестами; §5.3 содержит критерии проверки обновления. Первичный вывод был усечён, затем файл дочитан командами `git show ... | sed -n '1,100p'`, `'101,200p'`, `'201,294p'`.
- Прочитан целиком `codex-direct/launch-card-27.md@62e1ff6`: подтверждает волну переноса, роли, шаги П2–П15 и применение решений Р4/Р63.
- В задании не хватало приведённых выше контрактов этапа и проверок, на которые ссылается `PORT_PLAN.md`; они прочитаны до сбора фактов. Других необходимых правил, норм или контрактов из ссылок задания не обнаружено.

## 1. Клавиши и режимы приказов

### Вывод

В src/controls/CommandBindings.hpp@9208dcf:11 объявлен CommandBindingAction со значениями Attack, Repair, Unload, Deploy, Rally и Release. CommandBindings хранит одно поле SDL_Scancode на действие и сравнивает набор через operator== (src/controls/CommandBindings.hpp@9208dcf:20, :28). Клавиши по умолчанию:

| Команда | Клавиша | Отдельный модификатор | Что вызывает |
|---|---|---|---|
| Move | LMB | нет | Включает перемещение; строка управления не переназначается (src/gamestates/cOptionsState.cpp@9208dcf:460, src/drawers/cCommandBarDrawer.cpp@9208dcf:86, :279). |
| Attack | LCTRL | нет; одно назначение сканкода | В выбранном отряде включает состояние атаки (src/controls/CommandBindings.hpp@9208dcf:12, :21; src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:422). |
| Repair | R | нет | Переводит мышь в режим ремонта (src/controls/CommandBindings.hpp@9208dcf:13, :22; src/controls/mousestates/cMouseNormalState.cpp@9208dcf:254). |
| Unload | D | нет | Отправляет выбранных разгружаемых харвестеров к НПЗ (src/controls/CommandBindings.hpp@9208dcf:14, :23; src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:494). |
| Deploy | D | нет | Разворачивает MCV в CONSTYARD при допустимом размещении (src/controls/CommandBindings.hpp@9208dcf:15, :24; src/cGame_logic.cpp@9208dcf:2078). |
| Rally | LCTRL | нет | Для своей выбранной структуры, способной выпускать юниты, включает режим rally (src/controls/CommandBindings.hpp@9208dcf:16, :25; src/controls/mousestates/cMouseNormalState.cpp@9208dcf:221). |
| Release | D | нет | У выбранного ремонтного центра вызывает событие выпуска (src/controls/CommandBindings.hpp@9208dcf:17, :26; src/cGame_logic.cpp@9208dcf:2157). |

Поэтому LCTRL и D в таблице — самостоятельные значения одной клавиши, а не Ctrl-комбинации. Код bindings не хранит отдельный модификатор или сочетание.

В CommandBindings.hpp функции: commandBindingKeysMatch(first, second) возвращает признак совпадения сканкодов; commandBinding(bindings, action) возвращает код клавиши действия; setCommandBinding(bindings, action, scancode) меняет поле; trySetCommandBinding(bindings, action, scancode) проверяет прочие действия и либо возвращает первое конфликтующее, либо применяет назначение; commandBindingFromIni(value, fallback) разбирает имя SDL и возвращает fallback для UNKNOWN; commandBindingToIni(scancode) возвращает имя SDL или имя UNKNOWN; commandBindingDisplayName(scancode, english) формирует подпись, отдельно отображая CTRL/SHIFT/ALT/ENTER и локализуя SPACE. Ссылки: src/controls/CommandBindings.hpp@9208dcf:31, :46, :61, :76, :101, :109, :115. Сравнение объединяет L/R Shift и L/R Alt, но не объединяет L/R Ctrl (:35–44).

ActiveCommandMode содержит Normal, ForceAttack, Rally, Repair; PointerMoveCommandPolicy — Reevaluate и Preserve; RightClickCommandPolicy — DefaultAction и CancelCommand (src/controls/CommandModePolicy.hpp@9208dcf:3, :10, :15). pointerMoveCommandPolicy(mode) сохраняет состояние только в ForceAttack, остальные режимы требуют повторно вычислить действие (:20). rightClickCommandPolicy(mode) отменяет приказ в ForceAttack/Rally/Repair, а Normal возвращает действие по умолчанию (:28).

Назначения читаются из settings.ini, секции [SETTINGS], по ключам KeyAttack, KeyRepair, KeyUnload, KeyDeploy, KeyRally, KeyRelease (src/utils/common.cpp@9208dcf:52, :57, :110–127). saveSettingsToIni записывает те же ключи (src/utils/common.cpp@9208dcf:350, :380–385). Кнопка Apply сохраняет settings.ini, затем при успехе обновляет bindings активной игры (src/gamestates/cOptionsState.cpp@9208dcf:492–506).

### Команды и существенный вывод

- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/CommandBindings.hpp | nl -ba | sed -n '11,143p' вывел enum, структуру с шестью значениями по умолчанию, operator== и семь функций bindings, указанных выше.
- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/CommandModePolicy.hpp | nl -ba | sed -n '3,36p' вывел три перечисления и две политики: Preserve только для ForceAttack; отмена правым кликом для ForceAttack, Rally, Repair.
- Команды git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseNormalState.cpp | nl -ba | sed -n '219,257p', git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseUnitsSelectedState.cpp | nl -ba | sed -n '420,501p' и git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2078,2088p;2152,2170p' вывели runtime-обработчики Rally, Repair, Attack, Unload, Deploy и Release, перечисленные в таблице.
- Поисковая команда git grep -n -E 'CommandBinding|commandBindings|m_commandBindings|command_bar|controls-tab|Controls|control' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src | head -n 320 нашла точки использования в cGame_logic.cpp, cMouseNormalState.cpp, cMouseUnitsSelectedState.cpp, cOptionsState.cpp, common.cpp и command bar. Её вывод усекался; точные факты выше подтверждены адресными git show.

## 2. Панель приказов

### Вывод

CommandBarLayout содержит panel и массив из семи прямоугольников; ActionCount равен 7 (src/drawers/CommandBarLayout.hpp@9208dcf:8–12). create(screenWidth, screenHeight, sidebarWidth) возвращает layout панели, размещённой снизу доступной части экрана. Целевой размер 350×52, нижний зазор и внешний отступ — 8; границы семи кнопок — 0, 400, 800, 1200, 1600, 2000, 2400, 2800 (src/drawers/CommandBarLayout.hpp@9208dcf:14–42).

CommandBarPolicy.hpp содержит isMoveCommandEnabled(hasSelectedUnits) (:3), isAttackCommandEnabled(hasAttackCapableUnit) (:8), isRepairCommandEnabled() (:13), isUnloadCommandEnabled(hasUnloadableHarvester) (:18), isDeployCommandEnabled(hasSelectedMcv) (:23), isRallyCommandEnabled(ownsSelectedStructure, selectedStructureCanSpawnUnits) (:28) и isReleaseCommandEnabled(ownsSelectedStructure, selectedStructureIsRepairFacility) (:35). Вывод: соответствующие условия передаются напрямую, Repair всегда доступен.

cCommandBarDrawer объявлен в src/drawers/cCommandBarDrawer.h@9208dcf:15; вложенный Command перечисляет Move, Attack, Repair, Unload, Deploy, Rally, Release (:29–37), Button хранит команду, прямоугольник, подпись, hotkey, enabled и active (:39–46). Класс имеет конструктор/деструктор (:18–19), draw, onNotifyMouseEvent, setPlayer, isMouseOver, getTopY (:21–26), rebuildLayout, drawButton, drawIcon, execute, executeUnload, executeDeploy, executeRelease, hasAttackCapableUnit, hasUnloadableHarvester, hasSelectedMcv (:48–58).

В cCommandBarDrawer.cpp пять цветовых функций — panelColor, panelBorder, brass, disabledText, blueFilter (src/drawers/cCommandBarDrawer.cpp@9208dcf:22–26). Конструктор загружает HD-текстуры command_bar.png и command_bar_disabled.png и строит layout (:29–50); деструктор освобождает текстуры (:53–57). setPlayer меняет игрока (:59), getTopY возвращает верх панели (:64), isMouseOver проверяет точку в её прямоугольнике (:69). rebuildLayout вычисляет геометрию и семь кнопок (:74–95). draw обновляет layout и рисует панель/кнопки (:97–124); drawButton выводит сегмент текстуры, hotkey и запасную иконку (:126–196); drawIcon рисует векторный символ одной из команд (:198–250). onNotifyMouseEvent обновляет hover на движении и выполняет доступную кнопку по левому клику (:252–273). execute направляет команду обработчику (:275–303); исполнители Unload, Deploy, Release находятся на :305, :315, :329. Предикаты attack-capable, unloadable harvester и selected MCV — :342, :351, :358.

| Кнопка | Условие доступности | Изображение | Действие |
|---|---|---|---|
| Move | Есть выбранные юниты (src/drawers/cCommandBarDrawer.cpp@9208dcf:86; src/drawers/CommandBarPolicy.hpp@9208dcf:3). | Слот 0 command_bar.png; fallback — стрелка (cCommandBarDrawer.cpp@9208dcf:208). | Подпись LMB; включает Move (:86, :279–281). |
| Attack | Есть выбранный нехарвестер, способный атаковать юниты, авиацию или здания (:87, :342–349; CommandBarPolicy.hpp@9208dcf:8). | Слот 1; fallback — прицел (cCommandBarDrawer.cpp@9208dcf:214–220). | Активирует атаку (:282–284). |
| Repair | Всегда (:88; CommandBarPolicy.hpp@9208dcf:13–16). | Слот 2; fallback — крест (cCommandBarDrawer.cpp@9208dcf:221–224). | Включает состояние ремонта (cCommandBarDrawer.cpp@9208dcf:285–287). |
| Unload | Есть выбранный харвестер, который может разгрузиться (:89, :351–356; CommandBarPolicy.hpp@9208dcf:18). | Слот 3; fallback — стрелка вниз (cCommandBarDrawer.cpp@9208dcf:225–231). | Отправляет подходящих харвестеров к НПЗ (cCommandBarDrawer.cpp@9208dcf:305–313). |
| Deploy | Есть валидный выбранный MCV (:90, :358–363; CommandBarPolicy.hpp@9208dcf:23). | Слот 4; fallback — силуэт здания (cCommandBarDrawer.cpp@9208dcf:232–237). | Исполнение дополнительно проверяет владельца и возможность разместить CONSTYARD (cCommandBarDrawer.cpp@9208dcf:315–326). |
| Rally | Выбранная структура принадлежит игроку и выпускает юниты (:91; CommandBarPolicy.hpp@9208dcf:28–33). | Слот 5; fallback — флаг (cCommandBarDrawer.cpp@9208dcf:238–242). | Включает команду rally (cCommandBarDrawer.cpp@9208dcf:294–296). |
| Release | Выбранная структура принадлежит игроку и имеет тип REPAIR (:92; CommandBarPolicy.hpp@9208dcf:35–40). | Слот 6; fallback — бокс со стрелкой вверх (cCommandBarDrawer.cpp@9208dcf:243–248). | Посылает событие выпуска ремонтному центру (cCommandBarDrawer.cpp@9208dcf:329–340). |

При наличии command_bar.png код берёт соответствующую седьмую часть ширины текстуры (src/drawers/cCommandBarDrawer.cpp@9208dcf:130–142); при отсутствии текстуры рисует запасной значок. command_bar_disabled.png используется как фон панели, если загружен (:105–115).

### Ресурсы из карты переноса

Команда карты из задания:

    git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/port_inventory.json | /srv/dune/venv/bin/python -c "import json,sys; d=json.load(sys.stdin); [print(k) for k,v in d['paths'].items() if set(v.get('features',[])) & {'command-bar','controls-tab'} and k.startswith('resources/')]"

Вывод — шесть путей: resources/bin/data/hd4/command_bar.png, resources/bin/settings.ini, resources/hd/master4/command_bar.png, resources/hd/master4/command_bar_disabled.png, resources/hd/source_references/command_bar_bronze_reference.png, resources/hd/source_references/command_bar_color_reference.png. Все шесть помечены command-bar; у resources/bin/settings.ini дополнительно graphics-modes, hd-render, hd4-assets, localization. Ревизия карты и строки: docs/upstream/port_inventory.json@62e1ff6:14073, :14997, :25482, :25497, :38366, :38381.

Результат адресных git cat-file -s и разбора git cat-file -p для путей FORK1:

| Путь | Размер объекта Git | Тип и LFS-объект | Наличие в PORT / совпадение |
|---|---:|---|---|
| resources/bin/data/hd4/command_bar.png | 132 байта; blob 3b48b12cc9037998ec2abc719ca096d421605089 | LFS SHA-256 2194d72c6de3bd01193701b708da3001485d7c0e23d69d8eb7563d88115d2acf, 1 219 692 байта | Нет пути и нет другого пути с basename; сравнение невозможно. |
| resources/bin/settings.ini | 1 723 байта; blob 636898ad4ca47088d4374950f6e71ba802d5f431 | Обычный Git blob | Путь есть; blob PORT d3f475fc78e9416d32f6987633f5664c53f8e626, отличается. |
| resources/hd/master4/command_bar.png | 132 байта; blob 3b48b12cc9037998ec2abc719ca096d421605089 | Тот же LFS SHA-256 2194d72c6de3bd01193701b708da3001485d7c0e23d69d8eb7563d88115d2acf, 1 219 692 байта | Нет пути и нет другого пути с basename; сравнение невозможно. |
| resources/hd/master4/command_bar_disabled.png | 131 байт; blob 46603dfda1d47b6c57304517279c643d102e8490 | LFS SHA-256 4a763c285568a6dd860f882c0a3f249d19e45a5690aef7c6fa5a0f61f3e44f23, 952 143 байта | Нет пути и нет другого пути с basename; сравнение невозможно. |
| resources/hd/source_references/command_bar_bronze_reference.png | 132 байта; blob 60fce35166b925a3284ccfb1842ce7b03a2ad46b | LFS SHA-256 a915c92225411a2c1732b3ef7bd10c0a5483f5a9a3160da2e5e2e40dab5c03ed, 1 382 967 байт | Нет пути и нет другого пути с basename; сравнение невозможно. |
| resources/hd/source_references/command_bar_color_reference.png | 132 байта; blob de959fbf2884e321c21180a8a32f89539cf6025b | LFS SHA-256 f30f642cdbbc20528e2646a76c607b31b0af6936eb8fd153faa81981c1226117, 2 226 977 байт | Нет пути и нет другого пути с basename; сравнение невозможно. |

Команда git diff --raw 9208dcf5a358f40afd95c99480e4e09f781ed566 832c953a94a632d57872349013f7ed1a37434715 -- resources/bin/data/hd4/command_bar.png resources/bin/settings.ini resources/hd/master4/command_bar.png resources/hd/master4/command_bar_disabled.png resources/hd/source_references/command_bar_bronze_reference.png resources/hd/source_references/command_bar_color_reference.png вывела D для четырёх LFS-изображений и M для resources/bin/settings.ini; blob сокращённо 636898ad изменён на d3f475fc.

git diff --no-ext-diff 9208dcf5a358f40afd95c99480e4e09f781ed566 832c953a94a632d57872349013f7ed1a37434715 -- resources/bin/settings.ini вывела удаление из FORK1 Language=ru и KeyAttack, KeyRepair, KeyUnload, KeyDeploy, KeyRally, KeyRelease; в PORT вместо них есть секция [KEYS] с другими правилами назначений. Это инвентарный ресурс resources/bin/settings.ini; runtime-код FORK1 отдельно загружает файл с именем settings.ini.

Проверка LFS-хранилища: git rev-parse --git-common-dir вывела /srv/dune/worktrees/u63/.git; файлы всех четырёх LFS-объектов найдены в lfs/objects/<первые 2>/<следующие 2>/<oid> с размерами 1 219 692, 952 143, 1 382 967 и 2 226 977 байт соответственно.

Команда git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -E '/(command_bar\.png|command_bar_disabled\.png|command_bar_bronze_reference\.png|command_bar_color_reference\.png|settings\.ini)$' вывела только resources/bin/settings.ini. Поэтому четыре изображения отсутствуют в PORT и по basename; у settings.ini путь есть, но объект отличается.

### Команды и существенный вывод

- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CommandBarLayout.hpp | nl -ba | sed -n '8,43p' вывела layout, ActionCount, размеры и границы ячеек; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CommandBarPolicy.hpp | nl -ba | sed -n '3,40p' вывела все семь предикатов.
- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.h | nl -ba | sed -n '15,67p' вывела class, перечисление команд, структуру Button и объявления методов. Команда git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | nl -ba | sed -n '21,95p;97,124p;126,166p;198,250p;252,363p' вывела цвета, построение и отрисовку семи кнопок, значки, обработку клика и исполнители.
- Проверка объектов через git cat-file -s и git cat-file -p показала: resources/bin/data/hd4/command_bar.png — 132 байта и LFS size 1219692; resources/bin/settings.ini — 1723 байта и regular Git blob; resources/hd/master4/command_bar.png — 132 и тот же LFS size 1219692; command_bar_disabled.png — 131 и LFS size 952143; bronze reference — 132 и LFS size 1382967; color reference — 132 и LFS size 2226977.

## 3. Правки форка вне новых файлов
### Сбор символов и выбор участков

Команда для просмотра новых исходников FORK1 и существенный результат:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 | awk '$1 == "A" && $2 ~ /^src\// { print $2 }'
```

Среди добавленных исходников найдены `src/controls/CommandBindings.hpp`, `src/controls/CommandModePolicy.hpp`, `src/drawers/CommandBarLayout.hpp`, `src/drawers/CommandBarPolicy.hpp`, `src/drawers/cCommandBarDrawer.cpp` и `.h`.

Символы новых файлов искались командой:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'class |struct |enum|constexpr|inline|Command|Binding|Mode' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/CommandBindings.hpp src/controls/CommandModePolicy.hpp src/drawers/CommandBarLayout.hpp src/drawers/CommandBarPolicy.hpp src/drawers/OrderButtonPolicy.hpp src/drawers/cCommandBarDrawer.cpp src/drawers/cCommandBarDrawer.h src/gameobjects/structures/StarportOrderQueue.hpp src/gamestates/OptionsMenuLayout.hpp src/gamestates/AdvancedOptionsHeaderLayout.hpp src/gamestates/CampaignMapLayout.hpp
```

Существенный вывод: `CommandBindingAction`, `CommandBindings`, `commandBindingKeysMatch`, `setCommandBinding`, `trySetCommandBinding`, `commandBindingFromIni`, `ActiveCommandMode`, `PointerMoveCommandPolicy`, `RightClickCommandPolicy`, `pointerMoveCommandPolicy`, `rightClickCommandPolicy`, `CommandBarLayout` и `isRepairCommandEnabled`.

По заданным 20 путям diff читался с обычным контекстом, а участок включался, если в нём встречались `Command`, `Binding`, `CommandBar`, `Mode` или найденное имя символа. Команда подсчёта совпавших участков:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt src/cGame.h src/cGame_logic.cpp src/context/TextContext.cpp src/context/TextContext.hpp src/controls/cGameControlsContext.cpp src/controls/cGameControlsContext.h src/controls/cKeyboardEvent.h src/controls/cMouse.h src/controls/mousestates/cMouseNormalState.cpp src/controls/mousestates/cMouseNormalState.h src/controls/mousestates/cMouseRepairState.cpp src/controls/mousestates/cMouseUnitsSelectedState.cpp src/controls/mousestates/cMouseUnitsSelectedState.h src/include/definitions.h src/managers/cDrawManager.cpp src/managers/cDrawManager.h src/managers/cInteractionManager.cpp src/utils/GameSettings.hpp src/utils/common.cpp | awk 'function emit(){if(have && found) n++} /^diff --git / {emit(); file=$4; sub("b/", "", file); have=0; next} /^@@/ {emit(); hdr=$0; found=0; have=1; next} have {if ($0 ~ /(Command|Binding|CommandBar|Mode|ActiveCommandMode|CommandBinding)/) found=1} END {emit(); print n}'
```

Вывод — `41`. В `hooks.tsv` ниже сохранены все 41 участка и соответствие каждого участка в PORT; заголовок таблицы даёт итоговые 42 строки.

### Пути и соответствия в PORT

Пути проверялись чтением дерева PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | rg '^(CMakeLists\.txt|src/(cGame|context/TextContext|controls/cGameControlsContext|controls/cKeyboardEvent|controls/cMouse|controls/mousestates/cMouseNormalState|controls/mousestates/cMouseRepairState|controls/mousestates/cMouseUnitsSelectedState|include/definitions|managers/cDrawManager|managers/cInteractionManager|utils/GameSettings|utils/common))'
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | rg '(^src/game/cGame|^src/utils/InitialGameSettings|^src/managers/cInteractionManager|^src/controls/Command|^src/drawers/cCommandBar|^src/gamestates/cOptionsState|^src/gamestates/cMainMenuState)'
```

Существенный вывод: `src/cGame.h` и `src/cGame_logic.cpp` находятся в PORT как `src/game/cGame.h` и `src/game/cGame_logic.cpp`; `GameSettings.hpp` перенесён в `src/utils/InitialGameSettings.hpp`. `src/managers/cInteractionManager.cpp` и command bar файлы в PORT не найдены.

Отсутствие новых command bar и command binding API проверялось поиском:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'command_bindings|CommandBindings|CommandBinding|CommandBar|m_commandBindings|m_renderScalePercent|m_effectiveWorldScalePercent|useHdPresentation|presentFrame|saveSettingsToIni|saveDisplaySettingsToIni|getCommandKeyTextDrawer' 832c953a94a632d57872349013f7ed1a37434715 -- CMakeLists.txt src
```

Существенный вывод: совпадения в PORT есть для `m_renderScalePercent` (`src/game/cGame_logic.cpp@832c953:304,352,756`), но для `CommandBindings`, `CommandBar`, `m_commandBindings`, `useHdPresentation`, `getCommandKeyTextDrawer` и новых writer-функций совпадений нет. Таблица отмечает частичные аналоги и отсутствующие места отдельно.

`src/managers/cInteractionManager.cpp` в PORT удалён. Приём mouse event в игре теперь виден в `src/game/cGame_logic.cpp@832c953:1416`; маршрутизация события в mouse state игрового поля — `src/controls/cGameControlsContext.cpp@832c953:239`. Это подтверждено командами `git show 832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp | nl -ba | sed -n '1416,1433p'` и `git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '219,257p'`: первая передаёт `event` текущему state, вторая передаёт его обработчику текущего боевого mouse state.

### Таблица участков

```tsv
путь в FORK1	путь@9208dcf:строка	что добавляет участок	путь в PORT	соответствие
CMakeLists.txt	CMakeLists.txt@9208dcf:175	Регистрирует тестовые цели для CommandBindings, конфликтов привязок и CommandBarLayout.	CMakeLists.txt	нет: в CMake PORT этих целей нет
src/cGame.h	src/cGame.h@9208dcf:16	Подключает новый заголовок CommandBindings.	src/game/cGame.h	нет: привязки команд не перенесены
src/cGame.h	src/cGame.h@9208dcf:85	Добавляет m_commandBindings в состояние игры.	src/game/cGame.h	нет: поля CommandBindings нет
src/cGame.h	src/cGame.h@9208dcf:284	Добавляет плотность HD-ресурсов и методы доступа к масштабу мира; hunk содержит getDebugMode.	src/game/cGame.h	нет: API getGraphicsDensity/getWorldScaleFactor отсутствует
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:190	Применяет настройки масштаба и копирует commandBindings в игру.	src/game/cGame_logic.cpp	частично: масштаб берётся из настроек на src/game/cGame_logic.cpp@832c953:304, commandBindings нет
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:788	Добавляет HD-рендер-цель, настройку logical size, presentation/fade capture; hunk содержит SDL_ScaleModeLinear.	src/game/cGame_logic.cpp	нет: этой HD presentation/fade-capture последовательности нет
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:1072	Передаёт render scale в создание окна и задаёт HD-плотность графическому контексту; hunk содержит setFullScreenMode.	src/game/cGame_logic.cpp	частично: масштаб окна настраивается на src/game/cGame_logic.cpp@832c953:756, HD-плотность контекста не совпадает
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2078	Заменяет D на настраиваемую клавишу deploy.	src/game/cGame_logic.cpp	нет в этом месте: игровой обработчик перемещён; общая привязка DEPLOY_UNIT есть на src/controls/cKeyBindings.cpp@832c953:60
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2157	Заменяет D на настраиваемую клавишу выпуска юнита из Repair Yard.	src/game/cGame_logic.cpp	нет: привязки release в PORT нет
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2192	Учитывает world scale при вычислении дальности звука и громкости; hunk содержит контекст game.isDebugMode().	src/game/cGame_logic.cpp	нет: soundMaxDistance/soundVolumeFactor с world scale отсутствуют
src/context/TextContext.cpp	src/context/TextContext.cpp@9208dcf:32	Создаёт отдельный текстовый drawer для клавиш command bar.	src/context/TextContext.cpp	нет: getCommandKeyTextDrawer отсутствует
src/context/TextContext.hpp	src/context/TextContext.hpp@9208dcf:22	Объявляет getCommandKeyTextDrawer.	src/context/TextContext.hpp	нет: getCommandKeyTextDrawer отсутствует
src/controls/cGameControlsContext.cpp	src/controls/cGameControlsContext.cpp@9208dcf:54	При расчёте клетки мыши распознаёт область command bar.	src/controls/cGameControlsContext.cpp	нет: области command bar нет
src/controls/cGameControlsContext.cpp	src/controls/cGameControlsContext.cpp@9208dcf:75	Добавляет обработчики Move, Attack и Rally для перевода mouse state в соответствующий режим.	src/controls/cGameControlsContext.cpp	нет: этих обработчиков нет
src/controls/cGameControlsContext.h	src/controls/cGameControlsContext.h@9208dcf:57	Добавляет проверку попадания курсора в command bar; hunk также меняет проверку sidebar/top bar.	src/controls/cGameControlsContext.h	нет: command bar отсутствует
src/controls/cGameControlsContext.h	src/controls/cGameControlsContext.h@9208dcf:93	Объявляет activateMoveCommand, activateAttackCommand и activateRallyPointCommand.	src/controls/cGameControlsContext.h	нет: этих объявлений нет
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:3	Подключает CommandModePolicy для правил отмены режимов.	src/controls/mousestates/cMouseNormalState.cpp	нет: CommandModePolicy отсутствует
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:157	При правом щелчке отменяет rally mode и сбрасывает курсор; hunk включает обработчик кнопки мыши.	src/controls/mousestates/cMouseNormalState.cpp	частично: обычное поведение правого щелчка в src/controls/mousestates/cMouseNormalState.cpp@832c953:178, отдельного rally-policy нет
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:221	Использует назначенную клавишу Rally вместо жёстко заданного сочетания.	src/controls/mousestates/cMouseNormalState.cpp	нет: настраиваемой command binding нет
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:234	Сбрасывает rally mode при отпускании назначенной клавиши.	src/controls/mousestates/cMouseNormalState.cpp	нет: такая привязка не поддерживается
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:254	Переводит мышь в Repair state по назначенной клавише Repair.	src/controls/mousestates/cMouseNormalState.cpp	частично: Repair action в PORT запускает Repair state на src/controls/mousestates/cMouseNormalState.cpp@832c953:365, но назначение через commandBindings отсутствует
src/controls/mousestates/cMouseNormalState.cpp	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:278	Добавляет setRallyPointCommandMode, устанавливающий SELECT_STATE_RALLY и курсор Rally.	src/controls/mousestates/cMouseNormalState.cpp	нет: метода нет
src/controls/mousestates/cMouseNormalState.h	src/controls/mousestates/cMouseNormalState.h@9208dcf:48	Объявляет setRallyPointCommandMode.	src/controls/mousestates/cMouseNormalState.h	нет: метода нет
src/controls/mousestates/cMouseRepairState.cpp	src/controls/mousestates/cMouseRepairState.cpp@9208dcf:5	Подключает CommandModePolicy.	src/controls/mousestates/cMouseRepairState.cpp	нет: CommandModePolicy отсутствует
src/controls/mousestates/cMouseRepairState.cpp	src/controls/mousestates/cMouseRepairState.cpp@9208dcf:69	При правом щелчке закрывает Repair command mode через rightClickCommandPolicy.	src/controls/mousestates/cMouseRepairState.cpp	частично: правый щелчок выходит из Repair state на src/controls/mousestates/cMouseRepairState.cpp@832c953:89, без policy
src/controls/mousestates/cMouseRepairState.cpp	src/controls/mousestates/cMouseRepairState.cpp@9208dcf:92	Выходит из Repair state по назначенной клавише Repair.	src/controls/mousestates/cMouseRepairState.cpp	частично: Repair action обрабатывается на src/controls/mousestates/cMouseRepairState.cpp@832c953:112, но не из commandBindings
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:5	Подключает CommandModePolicy.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	нет: CommandModePolicy отсутствует
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:229	При правом щелчке в ForceAttack отменяет приказ и возвращает Move; hunk включает обработчик кнопки мыши.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	частично: обычная отмена/снятие выделения обработана на src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:258, отдельного ForceAttack-policy нет
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:262	При движении указателя сохраняет ForceAttack mode вместо переоценки Move/Attack.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	нет: pointerMoveCommandPolicy отсутствует
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:422	Переводит выделенные юниты в Attack state по назначенной клавише.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	частично: старое действие ATTACK_MODE обрабатывается на src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:445, но не commandBindings
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:478	Повторно запускает Attack state при срабатывании назначенной клавиши.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	частично: старое действие ATTACK_MODE обрабатывается на src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:476, но не commandBindings
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:489	Запускает Repair state и команду разгрузки по назначенным клавишам Repair и Unload.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	частично: старые действия REPAIR_UNIT и SEND_TO_REFINERY есть на src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:591; src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:610, без commandBindings
src/controls/mousestates/cMouseUnitsSelectedState.cpp	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:530	Добавляет setCommandState и getCommandState для управления режимом через command bar.	src/controls/mousestates/cMouseUnitsSelectedState.cpp	нет: этих методов нет
src/controls/mousestates/cMouseUnitsSelectedState.h	src/controls/mousestates/cMouseUnitsSelectedState.h@9208dcf:49	Объявляет чтение и запись command state.	src/controls/mousestates/cMouseUnitsSelectedState.h	нет: этих методов нет
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:5	Подключает cCommandBarDrawer.	src/managers/cDrawManager.h	нет: drawer отсутствует
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:50	Добавляет getter command bar drawer.	src/managers/cDrawManager.h	нет: getter отсутствует
src/managers/cDrawManager.h	src/managers/cDrawManager.h@115	Добавляет экземпляр command bar drawer в DrawManager.	src/managers/cDrawManager.h	нет: экземпляра нет
src/managers/cInteractionManager.cpp	src/managers/cInteractionManager.cpp@9208dcf:87	Передаёт mouse event в command bar и блокирует карту от прокрутки над UI.	нет в PORT	файл удалён; мышиное событие маршрутизирует src/game/cGame_logic.cpp@832c953:1416, игровое mouse-state событие получает src/controls/cGameControlsContext.cpp@832c953:239
src/utils/GameSettings.hpp	src/utils/GameSettings.hpp@9208dcf:2	Включает типы CommandBindings в настройки.	src/utils/InitialGameSettings.hpp	нет: CommandBindings в настройках PORT нет
src/utils/GameSettings.hpp	src/utils/GameSettings.hpp@9208dcf:32	Добавляет commandBindings как сохраняемое поле GameSettings.	src/utils/InitialGameSettings.hpp	нет: поля commandBindings нет
src/utils/common.cpp	src/utils/common.cpp@9208dcf:111; src/utils/common.cpp@9208dcf:380	Читает шесть command bindings из ini и добавляет сохранение полного набора настроек через общий writer settings.ini, включая эти привязки.	src/utils/common.cpp	нет: эти ключи не читаются
```

## 4. Вкладка управления

### Вывод

bindingKeyName(scancode, english) возвращает LCTRL/RCTRL раздельно, остальные подписи передаёт commandBindingDisplayName; commandBindingActionName(settings, action) возвращает локализованное имя одного из шести действий (src/gamestates/cOptionsState.cpp@9208dcf:43, :55). При переключении страницы switchOptionsPage сбрасывает захват и сообщение (:658–664).

На вкладке Controls лямбда addBinding(label, optional action) показывает подпись и значение назначения; кнопка с действием ждёт ввода, Move с std::nullopt отображается как LMB и отключена (src/gamestates/cOptionsState.cpp@9208dcf:418–458, :460–466). Состояния захвата и сообщения — m_bindingCapture и m_bindingMessage (src/gamestates/cOptionsState.h@9208dcf:76, :78).

cOptionsState::onNotifyKeyboardEvent(event) работает при открытой вкладке Controls, активном захвате и событии PRESSED. Берёт event.firstKey(), игнорирует ESCAPE и UNKNOWN, вызывает trySetCommandBinding; при конфликте собирает сообщение, иначе очищает его. Затем в обоих случаях сбрасывает захват и вызывает refresh (src/gamestates/cOptionsState.cpp@9208dcf:1439–1475).

Правило конфликта задаёт commandBindingKeysMatch(first, second): одинаковые сканкоды, L/R Shift и L/R Alt конфликтуют; L/R Ctrl остаются разными (src/controls/CommandBindings.hpp@9208dcf:31–44). trySetCommandBinding сравнивает новую клавишу с текущими назначениями остальных действий и возвращает первое совпадение, иначе меняет назначение (src/controls/CommandBindings.hpp@9208dcf:76–99). Сообщение конфликта: английский Key <key> is already assigned to <action>.; русский Клавиша <key> уже назначена команде «<action>». Текст ожидания: Press key... / Нажмите клавишу… (src/gamestates/cOptionsState.cpp@9208dcf:436–440, :1457–1463).

### Команды и существенный вывод

- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '43,74p;415,478p;492,506p;658,664p;1439,1475p' вывела функции подписей, строку захвата Controls, список Move плюс шесть назначаемых действий, обработчик клавиатуры, сообщения и callback Apply.
- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.h | nl -ba | sed -n '73,79p' вывела поля m_bindingCapture и m_bindingMessage.
- git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/common.cpp | nl -ba | sed -n '47,57p;110,128p;350,386p' вывела загрузку [SETTINGS], шесть ключей и их запись в settings INI. git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/common.cpp | nl -ba | sed -n '188,265p' подтвердило, что helper заменяет или вставляет ключи внутри [SETTINGS].
- Поисковая команда git grep -n -E 'save.*Settings|saveGame|write.*Settings|writeSettings|saveSettings|m_selectedSettings|m_bindingCapture|KeyAttack|KeyRepair|KeyUnload|KeyDeploy|KeyRally|KeyRelease' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/gamestates/cOptionsState.cpp src/utils/common.cpp src/utils/common.h src вывела вызов сохранения settings.ini на cOptionsState.cpp:500, применение bindings на :504, обработчик захвата на :1445–1473, чтение ключей на common.cpp:110–127 и запись на :380–385.

## 5. Обновление взаимодействия
### Повторный вход в меню настроек

Команды чтения FORK1 и существенный вывод:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '1311,1452p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '77,115p;658,669p;1484,1510p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cMainMenuState.cpp | nl -ba | sed -n '155,182p'
```

Вывод: `setState` оставляет `GAME_OPTIONS` для повторного использования (`src/cGame_logic.cpp@9208dcf:1320-1329`). При входе в уже созданный state вызывается `setPrevState(m_state)` либо `refresh()` (`:1374-1386`). Конструктор `cOptionsState` вызывает `initializeDisplaySettings()`, которая читает `settings.ini` (`src/gamestates/cOptionsState.cpp@9208dcf:77-105`); повторный вход в тот же объект не загружает файл заново. `switchOptionsPage` сохраняет `m_optionsPage`, а `setPrevState` обновляет предыдущий state и пересобирает окно через `refresh()` (`:658-664, 1488-1509`). `refresh()` не сбрасывает страницу и не перечитывает настройки.

Поскольку для `src/gamestates/*` запрещены ссылки PORT, сравнение выполнено с UP1:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cOptionsState::cOptionsState|initializeDisplaySettings|refresh\(|m_optionsPage|switchOptionsPage|requestOptionsPage|setPrevState|m_game\.setNextStateToTransitionTo\(GAME_OPTIONS\)' d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/gamestates/cOptionsState.cpp src/gamestates/cMainMenuState.cpp src/gamestates/cGameMenuState.cpp src/game
git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/game/cGame_logic.cpp | nl -ba | sed -n '948,963p;1040,1052p'
git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cOptionsState.cpp | nl -ba | sed -n '39,55p;364,379p'
git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cMainMenuState.cpp | nl -ba | sed -n '182,193p'
```

Вывод: UP1 также переиспользует options state (`src/game/cGame_logic.cpp@d06f2fc:948-952`), при повторном входе обновляет предыдущий state либо вызывает `refresh()` (`:1040-1051`); окно пересобирается в `src/gamestates/cOptionsState.cpp@d06f2fc:368-379`. Вход из главного меню есть на `src/gamestates/cMainMenuState.cpp@d06f2fc:182-191`.

### Фиксация приказа и доступность ремонта

Command mode и dispatch в FORK1 проверялись командами:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/CommandModePolicy.hpp | nl -ba
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '75,97p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | nl -ba | sed -n '252,303p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseUnitsSelectedState.cpp | nl -ba | sed -n '138,168p;203,220p;227,269p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseNormalState.cpp | nl -ba | sed -n '124,130p;155,165p'
```

Вывод: command bar обрабатывает левый щелчок только по активной кнопке (`src/drawers/cCommandBarDrawer.cpp@9208dcf:265-270`). Move, Attack, Repair и Rally активируют соответствующие mouse state (`:279-296`; `src/controls/cGameControlsContext.cpp@9208dcf:75-95`). Attack переводит выделенные юниты в `SELECTED_STATE_FORCE_ATTACK`; после отправки приказа `attackAt(mouseCell)` state сохраняется, пока выделение не опустело (`src/controls/cMouseUnitsSelectedState.cpp@9208dcf:168-184, 215-218`). При движении мыши policy сохраняет ForceAttack, а правый щелчок отменяет его и возвращает Move (`src/controls/CommandModePolicy.hpp@9208dcf:20-35`; `src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:227-237, 262-267`). Rally click задаёт точку и не сбрасывает `SELECT_STATE_RALLY`; отмена происходит правым щелчком (`src/controls/mousestates/cMouseNormalState.cpp@9208dcf:124-130, 155-165`). Move остаётся в selected state после щелчка, если юниты остались выделены. Repair state также остаётся после левого щелчка.

Сверка соответствующих боевых handlers в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMouseUnitsSelectedState.cpp | nl -ba | sed -n '203,249p;271,286p;576,583p'
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMouseNormalState.cpp | nl -ba | sed -n '147,153p;178,187p'
```

Вывод: после Move/Attack PORT возвращается к выбору только при пустом выделении (`src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:203-249`), но pointer handler переоценивает режим на движении (`:271-286`), а отпускание клавиши ATTACK_MODE завершает временный режим (`:576-583`). Rally point ставится на `src/controls/mousestates/cMouseNormalState.cpp@832c953:147-153`; обычный правый щелчок снимает выделение (`:178-184`). У PORT отсутствует activation через command bar.

Доступность ремонта проверялась командами:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CommandBarPolicy.hpp | nl -ba
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | nl -ba | sed -n '80,94p;275,290p'
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/mousestates/cMouseRepairState.cpp | nl -ba | sed -n '43,60p;97,115p'
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/mousestates/cMouseRepairState.cpp | nl -ba | sed -n '66,82p;117,132p'
```

Вывод: `isRepairCommandEnabled()` безусловно возвращает `true` (`src/drawers/CommandBarPolicy.hpp@9208dcf:13-16`), и кнопка использует эту проверку (`src/drawers/cCommandBarDrawer.cpp@9208dcf:88`). Реальное действие ограничено: ремонт юнита требует владения и `isEligibleForRepair()`, а ремонт структуры — владения и повреждения (`src/controls/mousestates/cMouseRepairState.cpp@9208dcf:43-57`). Курсор показывает запрет на нецелевых объектах (`:97-114`); выделенные юниты получают ремонтный приказ только при `isEligibleForRepair()` (`src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:138-150`). В PORT проверки целей сохранены (`src/controls/mousestates/cMouseRepairState.cpp@832c953:66-82, 117-132`), но command bar и проверка доступности её кнопки отсутствуют.

### Таблица взаимодействия

```tsv
поведение	путь@9208dcf:строка	что делает	место в PORT
Повторный вход в меню настроек	src/gamestates/cMainMenuState.cpp@9208dcf:167; src/cGame_logic.cpp@9208dcf:1320; src/cGame_logic.cpp@9208dcf:1374	Кнопка меню выбирает GAME_OPTIONS. setState сохраняет объект настроек для повторного использования; при повторном входе обновляет prevState и вызывает setPrevState/refresh для уже существующего объекта.	src/gamestates/cMainMenuState.cpp@d06f2fc:182; src/game/cGame_logic.cpp@d06f2fc:952; src/game/cGame_logic.cpp@d06f2fc:1040
Повторный вход в меню настроек	src/gamestates/cOptionsState.cpp@9208dcf:77	initializeDisplaySettings вызывается только при создании объекта; повторный вход не перечитывает settings.ini.	src/gamestates/cOptionsState.cpp@d06f2fc:39
Повторный вход в меню настроек	src/gamestates/cOptionsState.cpp@9208dcf:658; src/gamestates/cOptionsState.cpp@9208dcf:1488	Смена страницы записывает m_optionsPage и делает refresh; при повторном входе setPrevState обновляет только предыдущий state, а refresh пересобирает окно текущей страницы. m_selectedSettings и m_optionsPage остаются в переиспользуемом объекте.	src/gamestates/cOptionsState.cpp@d06f2fc:368; src/gamestates/cOptionsState.cpp@d06f2fc:374
Фиксация приказа: Move	src/drawers/cCommandBarDrawer.cpp@9208dcf:279; src/controls/cGameControlsContext.cpp@9208dcf:75	Щелчок по кнопке Move переводит выделенные юниты в SELECTED_STATE_MOVE; левый щелчок отдаёт приказ перемещения, а state сбрасывается только если выделение опустело.	src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:173; src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:246
Фиксация приказа: Attack	src/drawers/cCommandBarDrawer.cpp@9208dcf:265; src/controls/cGameControlsContext.cpp@9208dcf:82	Щелчок по активной кнопке вызывает activateAttackCommand; тот переводит выбранные юниты в SELECTED_STATE_FORCE_ATTACK.	нет: command bar и activateAttackCommand отсутствуют; боевое событие обрабатывается через src/game/cGame_logic.cpp@832c953:1416 и src/controls/cGameControlsContext.cpp@832c953:239
Фиксация приказа: Attack	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:168; src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:215	Левый щелчок отправляет выбранные нехарвестеры атаковать клетку; state сбрасывается только если выделенных юнитов не осталось.	src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:203; src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:246
Фиксация приказа: Attack	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:251	PointerMoveCommandPolicy сохраняет ForceAttack при движении мыши, иначе пересчитывает Move/Attack cursor/state.	src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:273; src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:284
Фиксация приказа: Attack	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:227	Правый щелчок в ForceAttack сбрасывает режим к Move, не снимая выделение.	src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:258
Фиксация приказа: Rally	src/drawers/cCommandBarDrawer.cpp@9208dcf:294; src/controls/cGameControlsContext.cpp@9208dcf:89	Кнопка Rally переводит normal mouse state в SELECT_STATE_RALLY.	нет: command bar activation отсутствует; состояние мыши маршрутизируется через src/controls/cGameControlsContext.cpp@832c953:239
Фиксация приказа: Rally	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:124	Левый щелчок в SELECT_STATE_RALLY задаёт rally point выбранной структуре; обработчик не сбрасывает SELECT_STATE_RALLY, поэтому следующий щелчок тоже задаёт точку.	src/controls/mousestates/cMouseNormalState.cpp@832c953:147
Фиксация приказа: Rally	src/controls/mousestates/cMouseNormalState.cpp@9208dcf:155	Правый щелчок отменяет Rally mode и меняет курсор на обычный.	src/controls/mousestates/cMouseNormalState.cpp@832c953:178
Фиксация приказа: Repair	src/drawers/CommandBarPolicy.hpp@9208dcf:13; src/drawers/cCommandBarDrawer.cpp@9208dcf:88	Доступность кнопки Repair задаётся безусловным true, независимо от выбранного юнита или структуры.	нет: command bar и проверки доступности его кнопки отсутствуют
Фиксация приказа: Repair	src/drawers/cCommandBarDrawer.cpp@9208dcf:285; src/controls/mousestates/cMouseRepairState.cpp@9208dcf:43	Repair-кнопка переводит контекст в MOUSESTATE_REPAIR; левый щелчок отдаёт команду только своему eligible-for-repair юниту либо включает ремонт своей повреждённой структуры. После щелчка Repair state сохраняется.	src/controls/mousestates/cMouseRepairState.cpp@832c953:66
Фиксация приказа: Repair	src/controls/mousestates/cMouseRepairState.cpp@9208dcf:97	Курсор Repair показывается только над своим eligible-for-repair юнитом или своей повреждённой структурой; иначе рисуется запрещающий курсор.	src/controls/mousestates/cMouseRepairState.cpp@832c953:117
Фиксация приказа: Repair	src/controls/mousestates/cMouseUnitsSelectedState.cpp@9208dcf:138	При Repair order от выделенных юнитов move_to выполняется только для eligible-for-repair юнитов.	src/controls/mousestates/cMouseUnitsSelectedState.cpp@832c953:173
Фиксация приказа: Repair	src/controls/mousestates/cMouseRepairState.cpp@9208dcf:66	Правый щелчок выходит из Repair state, если мышь не прокручивает карту.	src/controls/mousestates/cMouseRepairState.cpp@832c953:89
```

## 6. Заказы Starport

### Очередь заказов FORK1

Исходник просмотрен командой `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/structures/StarportOrderQueue.hpp | nl -ba`. В нём объявлены `StarportOrder` (`src/gameobjects/structures/StarportOrderQueue.hpp@9208dcf:6`), поля `buildId` и `paidPrice` с начальным значением −1 (`@9208dcf:7`, `@9208dcf:8`), методы `getBuildId()` (`@9208dcf:10`) и `isValid()` (`@9208dcf:14`), шаблон `StarportOrderQueue<Capacity>` (`@9208dcf:19`) и его закрытый массив `orders` (`@9208dcf:73`).

`StarportOrder::getBuildId()` возвращает идентификатор сборки; `isValid()` считает запись занятой, если `buildId >= 0`. `StarportOrderQueue::add()` помещает пару build ID/цена в первый пустой слот и возвращает false при заполненной очереди (`StarportOrderQueue.hpp@9208dcf:22`). `hasFreeSlot()` и `empty()` проверяют наличие свободного слота и отсутствие заказов (`StarportOrderQueue.hpp@9208dcf:32`, `@9208dcf:41`). `takeNext()` извлекает и очищает первую по порядку занятую запись или возвращает `std::nullopt` (`StarportOrderQueue.hpp@9208dcf:50`); `removeFirst(buildId)` удаляет первую запись с заданным ID или возвращает `std::nullopt` (`StarportOrderQueue.hpp@9208dcf:61`). `isStarportCatalogAvailable(bool)` — constexpr-предикат, возвращающий аргумент без изменения (`StarportOrderQueue.hpp@9208dcf:76`). В заголовке нет именованных констант; размер задаёт параметр `Capacity`. Процессор передаёт очередь константу `kMaxItemsToOrder = 8` из `src/gameobjects/structures/cOrderProcesser.h@9208dcf:31`.

### Отличия четырёх файлов и соответствие PORT

Команда `git diff --unified=0 e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/gameobjects/structures/cOrderProcesser.cpp src/gameobjects/structures/cOrderProcesser.h src/gameobjects/structures/cStarPort.cpp src/sidebar/cBuildingListUpdater.cpp` показала следующие участки; полная таблица каждого hunкa, его строки FORK1 и соответствия в PORT записана в `starport.tsv`.

- `cOrderProcesser.cpp`: удалена ручная инициализация массива цен; pointer API `getItemToDeploy` и `markOrderAsDeployed` заменён извлечением значения `std::optional<StarportOrder>`; `hasOrderedAnything`/`acceptsOrders` используют проверки очереди; сообщения об обратном отсчёте и прибытии локализованы; `addOrder` хранит build ID и оплаченную цену, а `removeOrder` удаляет по ID и возвращает цену; `removeAllItems` извлекает заказы и возвращает цены. Старые поиск свободного слота, поиск указателя и очистка каждого массива слотов удалены. Существенные новые строки: `src/gameobjects/structures/cOrderProcesser.cpp@9208dcf:37`, `:42`, `:47`, `:91`, `:99`, `:131`, `:139`, `:149`.
- `cOrderProcesser.h`: подключена очередь (`src/gameobjects/structures/cOrderProcesser.h@9208dcf:4`), `hasFreeSlot` делегирует ей (`:48`), `takeNextOrderToDeploy` заменяет методы указателя (`:52`), а два массива заменены объектом очереди (`:66`). В PORT очередь отсутствует: команда `git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep '/StarportOrderQueue.hpp$'` вывела пустую строку. В PORT остаётся прежняя pointer-реализация: `src/gameobjects/structures/cOrderProcesser.h@832c953:71`, `:75`, `:77`, `:97-98`.
- `cStarPort.cpp`: `think_deploy` извлекает заказ как значение (`src/gameobjects/structures/cStarPort.cpp@9208dcf:76`), повторно ищет элемент каталога по build ID и уменьшает его счётчик, только если элемент и положительный счётчик существуют (`:79-84`), затем передаёт сохранённый ID в создание юнита и подкрепление (`:88`, `:106`). В PORT остаётся указатель на элемент каталога, его безусловное уменьшение и чтение build ID через этот указатель (`src/gameobjects/structures/cStarPort.cpp@832c953:94`, `:99`, `:104-105`, `:126`).
- `cBuildingListUpdater.cpp`: новый include очереди (`src/sidebar/cBuildingListUpdater.cpp@9208dcf:5`) даёт вызов предиката каталога при уничтожении последнего Starport (`:439`). Очистка каталога по одному элементу (`:444`) должна вызвать событие недоступности последнего списка и убрать выбор с вкладки. PORT делает то же отдельными действиями: вызывает `clearList()` и затем переключает выбор (`src/sidebar/cBuildingListUpdater.cpp@832c953:504`, `:509-511`); helper очереди не используется.
- В PORT в `cOrderProcesser.cpp` массив цен и старые методы сохранены; `std::fill` инициализирует цены (`src/gameobjects/structures/cOrderProcesser.cpp@832c953:51`), старые getter/helper/cleanup остаются на `:73`, `:83`, `:90`, `:201`, `:214`, `:221`, `:231`, `:241`. Вместо новых локализованных строк там английские сообщения (`:160`, `:164`).

## 7. Предел юнитов апстрима

### Значение, проверка и показ игроку

Для UP1 и PORT проверены команды `git grep -n -I -E 'isUnitLimitReached|unit.?limit|unitLimit|maxUnits|MAX_UNITS' d06f2fcd2a347182c3774fb96e9a85570405c489 --` и `git grep -n -I -E 'isUnitLimitReached|unit.?limit|unitLimit|maxUnits|MAX_UNITS' 832c953a94a632d57872349013f7ed1a37434715 --`. Результат содержит одну и ту же группу прямых вызовов, констант и значений MaxUnits в ресурсах карт; изменяется только строка вызова в `cPlayer.cpp`. Глобальный активный предел задаётся `cUnits::MAX_UNITS_CAPACITY = 300` (`src/gameobjects/units/cUnits.h@d06f2fc:70`, `src/gameobjects/units/cUnits.h@832c953:70`). `CARRYALL_RESERVE` равен 15 и `TOTAL_SLOTS` равен 315 (`src/gameobjects/units/cUnits.h@d06f2fc:76`, `:81`; `src/gameobjects/units/cUnits.h@832c953:76`, `:81`); при 90% занятой обычной ёмкости allocator может задействовать резерв для carry-all (`src/gameobjects/units/cUnits.cpp@d06f2fc:116`, `@832c953:116`). Сам `isUnitLimitReached()` вызывает `findAvailableSlot()`, который ищет только первые 300 обычных слотов (`src/gameobjects/units/cUnits.h@d06f2fc:105`, `@832c953:105`; `src/gameobjects/units/cUnits.cpp@d06f2fc:97`, `@832c953:97`).

Найденные прямые места вызова `isUnitLimitReached()` совпадают в UP1 и PORT, с изменением строк `cPlayer.cpp`:

- `src/building/cItemBuilder.cpp@d06f2fc:202` и `@832c953:202`: при завершённом производстве удерживает юнит в готовом состоянии и пробует снова на следующем такте; человеку один раз показывает «Unable to create more.» (`:203-209`).
- `src/sidebar/cSideBar.cpp@d06f2fc:111` и `@832c953:111`: не даёт начать производство и показывает то же сообщение; список Starport исключён из проверки.
- `src/gameobjects/players/cPlayer.cpp@d06f2fc:1395` и `@832c953:1402`: `canBuildUnit` возвращает `UNIT_LIMIT_REACHED` при исчерпании слотов; AI различает этот исход в `src/gameobjects/players/brains/cPlayerBrainSkirmish.cpp@d06f2fc:1476` и `@832c953:1476`.
- `src/drawers/cBuildingListDrawer.cpp@d06f2fc:182,241,264` и `@832c953:183,242,265`: проверяет лимит для списков пехоты и техники, блокирует недоступные юниты и рисует отметку для ожидающих заказов. `drawMaxBuilt` выводит красный крест и подписи «Max built» поверх иконки (`src/drawers/cBuildingListDrawer.cpp@d06f2fc:381-391`; `@832c953:382-392`).
- Отдельный путь доставки Starport вызывает `unitCreate`; если слот не выдан, он сохраняет заказ и повторяет доставку следующим тактом (`src/gameobjects/structures/cStarPort.cpp@d06f2fc:99-101`; `@832c953:99-101`).

Команды `git grep -n -i -E 'MaxUnits|MAXUNITS|MAX_UNITS' d06f2fcd2a347182c3774fb96e9a85570405c489 -- src` и такой же поиск по PORT не обнаружили чтения ini-ключа в коде. Команды `git grep -n -i 'maxunits' d06f2fcd2a347182c3774fb96e9a85570405c489 -- resources/bin/campaign/maps` и с ревизией PORT нашли `MaxUnits=20` в `scena005.ini` и `MaxUnits=25` в двенадцати картах уровней 17–19 для четырёх домов. Все 13 путей и строки перечислены в `unit-limit.tsv`. Эти ключи присутствуют в ini, но статический поиск по `src` не подтвердил, что они задают глобальный предел; глобальная константа в UP1 и PORT — 300.

### Кнопки command bar FORK1

Независимый просмотр `src/drawers/cCommandBarDrawer.cpp@9208dcf` показывает семь кнопок: Move, Attack, Repair, Unload, Deploy, Rally, Release (`:85-92`). Move/Attack/Repair меняют команду или состояние мыши (`:279-287`); Unload отправляет выбранный харвестер разгружаться (`:305-312`); Deploy превращает выбранный MCV в структуру CONSTYARD (`:315-327`); Rally назначает точку сбора (`:294-296`); Release посылает `GAME_EVENT_DEPLOY_UNIT` ремонтному зданию (`:329-340`), где `cRepairFacility` выводит уже находящийся внутри юнит через `unitLeavesStructure()` (`src/gameobjects/structures/cRepairFacility.cpp@9208dcf:127-134`). Ни одна кнопка не создаёт производственный заказ или новый юнит.

Команда поиска прямой проверки/создания в самом command bar:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'isUnitLimitReached|unitCreate|unitCreate\(|addItemToList|addOrder|UNIT_CREATE|queue' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cCommandBarDrawer.cpp
```

Вывод пустой. Следовательно, кнопки не вызывают код проверки лимита напрямую; выпуск через Release использует уже отремонтированный юнит. В `unit-limit.tsv` приведены все места лимита UP1/PORT, настройки MaxUnits и каждая кнопка панели.

## 8. Тесты

### CTest-регистрация и статический подсчёт

Регистрации просмотрены командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt | nl -ba | sed -n '162,205p;230,267p'` и `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UnitRenderFixture.cmake | nl -ba`. В корневом `CMakeLists.txt` зарегистрированы:

- `command_bindings` — `CMakeLists.txt@9208dcf:184`;
- `command_binding_conflicts` — `CMakeLists.txt@9208dcf:197`;
- `command_bar_layout_geometry` — `CMakeLists.txt@9208dcf:249`;
- `interaction_regressions` — `CMakeLists.txt@9208dcf:262`.

Mouse test добавлен вызовом `add_unit_frame_test(mouse_click_init_tests mouse_click_init MouseClickInitTests.cpp recorded)` (`tests/UnitRenderFixture.cmake@9208dcf:130`); helper вызывает `add_test(NAME ${test_name} COMMAND ${target})` на строке 99. CTest не запускался.

Одноразовый статический скрипт был сохранён в `.tmp/p10r/count_checks.py`, использовал только `git show` с ревизией FORK1, регулярное выражение для вызовов `assert`, `ASSERT_*`, `CHECK`, `EXPECT_*`, `REQUIRE`, `FAIL_*`, подсчёт `if (...)` и вызовов helper `require` без учёта объявления helper; после подсчёта скрипт удалён. Его основная логика:

```python
import re
import subprocess

revision = '9208dcf5a358f40afd95c99480e4e09f781ed566'
files = [
    'tests/CommandBarLayoutTests.cpp',
    'tests/CommandBindingConflictTests.cpp',
    'tests/CommandBindingsTests.cpp',
    'tests/InteractionRegressionTests.cpp',
    'tests/MouseClickInitTests.cpp',
]
for path in files:
    content = subprocess.run(['git', 'show', f'{revision}:{path}'], check=True,
                             text=True, capture_output=True).stdout
    macros = len(re.findall(r'\b(?:assert|ASSERT(?:_[A-Z]+)?|CHECK|EXPECT(?:_[A-Z]+)?|REQUIRE|FAIL(?:_[A-Z]+)?)\s*\(', content))
    if_guards = len(re.findall(r'\bif\s*\(', content))
    require_calls = len(re.findall(r'\brequire\s*\(', content))
    if 'bool require(' in content:
        require_calls -= 1
    checks = require_calls if require_calls else if_guards
    print(f'{path}: assert/check/fail macros={macros}; if-guards={if_guards}; require-calls={require_calls}; counted checks={checks}')
```

Команда запуска и существенный вывод:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python .tmp/p10r/count_checks.py
tests/CommandBarLayoutTests.cpp: assert/check/fail macros=0; if-guards=8; require-calls=0; counted checks=8
tests/CommandBindingConflictTests.cpp: assert/check/fail macros=0; if-guards=7; require-calls=0; counted checks=7
tests/CommandBindingsTests.cpp: assert/check/fail macros=0; if-guards=7; require-calls=0; counted checks=7
tests/InteractionRegressionTests.cpp: assert/check/fail macros=0; if-guards=1; require-calls=16; counted checks=16
tests/MouseClickInitTests.cpp: assert/check/fail macros=0; if-guards=2; require-calls=0; counted checks=2
```

Во всех пяти файлах — 0 вызовов assert/check/fail-макросов. Проверки выражены возвратом из `if`, а в InteractionRegressionTests — 16 вызовами helper `require` (без объявления helper); итог 40 статических проверок. Исходные строки тестов просмотрены командами `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/CommandBarLayoutTests.cpp | nl -ba`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/CommandBindingConflictTests.cpp | nl -ba`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/CommandBindingsTests.cpp | nl -ba`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/InteractionRegressionTests.cpp | nl -ba`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MouseClickInitTests.cpp | nl -ba`; каждая проверка и её результат записаны отдельно в `tests.tsv`:

- `CommandBarLayoutTests.cpp`: строка 12 — ширина панели; 13 — нижняя граница панели; 14 — точка внизу экрана вне панели; 17 — положительный размер кнопок; 18–19 — оба внутренних угла кнопки внутри панели; 23 — размер панели при 1920×1080; 25 — размер кнопок.
- `CommandBindingConflictTests.cpp`: 18 — занятой клавишей отклоняется переназначение Attack; 19–20 — обе исходные привязки сохраняются; 23–28 — Repair не переназначается на RCTRL при занятой LCTRL; 29 — Repair назначается на RCTRL после установки Attack на LCTRL; 33–34 — событие LCTRL распознаёт левую и не распознаёт правую клавишу.
- `CommandBindingsTests.cpp`: 10 — значение Attack по умолчанию LCTRL; 11 — английское имя CTRL; 12 — русское имя Space; 15 — назначение Repair=F; 16–17 — round-trip ini сохраняет F; 18 — неизвестный ключ возвращает резервную R; 21 — RCTRL не удовлетворяет проверке LCTRL.
- `InteractionRegressionTests.cpp`: 34 — заголовок вкладки не перекрывает вкладки; 38 — движение мыши сохраняет ForceAttack; 43, 48, 53 — правый щелчок отменяет ForceAttack, Rally и Repair; 58 — проверка доступности Repair; 62, 66, 70, 74 — доступность Move, Attack, Unload, Deploy зависит от соответствующего выбора; 78 и 84 — Rally требует принадлежащего игроку производителя, Release — Repair facility; 90 — отключена тень подписи заказа; 95 — очередь принимает свободный заказ; 101 — заказ хранит исходный ID после изменения каталога; 106 — доступность каталога соответствует наличию Starport.
- `MouseClickInitTests.cpp`: 23 и 24 — начальные состояния левого и правого click-флагов false.

Команда `git grep -n -E 'ifstream|fstream|fopen|SDL_RW|readFile|file\(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- tests/CommandBarLayoutTests.cpp tests/CommandBindingConflictTests.cpp tests/CommandBindingsTests.cpp tests/InteractionRegressionTests.cpp tests/MouseClickInitTests.cpp` вывела пустой результат: исходники тестов не читают файлы. На этапе конфигурации `UnitRenderFixture.cmake` отдельно вызывает `file(READ .../src/drawers/SDLDrawer.hpp ...)` (`tests/UnitRenderFixture.cmake@9208dcf:16`); это чтение CMake-конфигурации, не тестом при запуске. Ни сборка, ни CTest, ни тесты, ни игра не запускались.

Наличие пяти тестовых файлов проверялось командой `git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | rg 'tests/(CommandBarLayoutTests|CommandBindingConflictTests|CommandBindingsTests|InteractionRegressionTests|MouseClickInitTests)\.cpp$'`; вывод пустой. Специальные policy/header API проверены командой `git grep -n -E 'CommandBarLayout|CommandBindings|CommandBindingAction|setCommandBinding|trySetCommandBinding|commandBindingDisplayName|commandBindingToIni|commandBindingFromIni|hasAssignedKey|pointerMoveCommandPolicy|rightClickCommandPolicy|isRepairCommandEnabled|isMoveCommandEnabled|isAttackCommandEnabled|isUnloadCommandEnabled|isDeployCommandEnabled|isRallyCommandEnabled|isReleaseCommandEnabled|shouldDrawOrderLabelShadow|StarportOrderQueue|isStarportCatalogAvailable' 832c953a94a632d57872349013f7ed1a37434715 -- src`; вывод пустой. Исходники и тестовые API command bar/bindings/Starport queue не найдены. Совпадающие части Mouse test представлены, но интерфейс изменился: `cMouse` и click-методы есть (`src/controls/cMouse.h@832c953:32`, `:57`, `:61`), `GameContext::setTextContext` есть (`src/context/GameContext.hpp@832c953:44`), `TextContext` в PORT принимает три drawer (`src/context/TextContext.hpp@832c953:24`), а `cTextDrawer` требует три аргумента (`src/drawers/cTextDrawer.h@832c953:31`), тогда как FORK1 тест передаёт шесть drawer и вызывает `cTextDrawer(nullptr)`. В `cKeyboardEvent.h` файл есть, но тестовые конструктор с `std::set` и `hasAssignedKey` отсутствуют; сигнатура в PORT показана на `src/controls/cKeyboardEvent.h@832c953:30`. Для `src/gamestates/*` ссылки на PORT намеренно не собирались. Строковые включения, используемые API, их наличие в PORT и отсутствие чтения тестами собраны в `tests.tsv`.
