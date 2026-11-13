# Дополнение к RECON по пунктам 2–4

В `track3-evidence.md` уже сохранены выводы команд для каждой строки трёх TSV. Здесь зафиксирована классификация полного списка `drawHd` и указаны соответствующие секции исходного журнала.

## Пункт 2: классификация всех `drawHd`-упоминаний

Полный вывод `git grep -n -E 'drawHd[A-Za-z0-9_]*'` по десяти файлам дорожки 1 и `src/managers/cDrawManager.cpp` находится в секции «Пункт 2 — все упоминания функций drawHd по полным файлам» файла `track3-evidence.md`. Полный инвентарь `if`, `else if` и `?` находится в секции перед ним. Проверенные места вызова классифицируются так:

| Место | Вызов | Классификация |
| --- | --- | --- |
| `src/drawers/cSideBarDrawer.cpp:72` | `drawHdSidebar()` | Вызов идёт после закрытого условия `uiaudit::isEnabled()`; условие вызывает только запись кликов. Сам HD-вызов безусловный. Вывод исходника сохранён в секции «cSideBarDrawer::draw и вызов drawHdSidebar». |
| `src/drawers/cSideBarDrawer.cpp:106–108` | `drawHdRadarPanel()`, `drawHdCapacities()`, `drawHdBuildingLists()` | Безусловные вызовы внутри `drawHdSidebar()`. Их исходник сохранён в секции «безусловные вызовы HD-подфункций боковой панели». |
| `src/drawers/cSideBarDrawer.cpp:314, 323` | `drawHdMeter()` | Оба вызова идут подряд в `drawHdCapacities()` и не разделяются условием. Точный вывод команды приведён ниже. |
| `src/drawers/cBuildingListDrawer.cpp:259` | `drawHdCard(...)` | Прямой вызов внутри цикла; перед ним есть проверки пропуска пустого и невидимого элемента, но в их ветках нет вызова другой функции рисования. Вызов и окружение сохранены в секции «вызов drawHdCard внутри полного draw-list участка». |
| `src/drawers/cBuildingListDrawer.cpp:467` | `drawHdScrollbar(...)` | Безусловный вызов после цикла и сброса clipping. Вывод сохранён в секции «безусловный вызов drawHdScrollbar после отрисовки карточек». |

Остальные совпадения полного поиска — объявления и определения функций в `.h`/`.cpp`, а не вызовы в ветвлениях. Поэтому `hd-branches.tsv` содержит только заголовок: ни одна ветка `if`, `else if` или `?:` не содержит вызова `drawHd...` как альтернативу иной функции рисования или пустой ветке.

### Точный вывод для вызовов `drawHdMeter`

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '306,336p'
```

```text
   306	void cSideBarDrawer::drawHdCapacities()
   307	{
   308	    const HudLayout layout = HudLayout::create(
   309	        game.m_screenW,
   310	        game.m_screenH
   311	    );
   312	    const int produced = std::max(0, m_player->getPowerProduced());
   313	    const int used = std::max(0, m_player->getPowerUsage());
   314	    drawHdMeter(
   315	        layout.powerMeter,
   316	        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
   317	        used,
   318	        produced,
   319	        Color{72, 202, 103, 255},
   320	        !m_player->bEnoughPower()
   321	    );
   322	
   323	    drawHdMeter(
   324	        layout.spiceMeter,
   325	        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
   326	        std::max(0, m_player->getCredits()),
   327	        std::max(1, static_cast<int>(m_player->getMaxCredits())),
   328	        Color{218, 139, 47, 255},
   329	        !m_player->bEnoughSpiceCapacityToStoreCredits()
   330	    );
   331	}
   332	
   333	void cSideBarDrawer::drawHdBuildingLists()
   334	{
   335	    m_sidebar = m_player->getSideBar();
   336	    const int selectedListId = m_sidebar->getSelectedListID();
```

## Пункт 3: покрытие команд

В `track3-evidence.md` раздел «строки с литералами .png/.bmp и вызовами loadHdUiTexture» содержит вывод поиска по всем 25 путям. Для всех девяти имён есть отдельные блоки `git ls-tree -r --name-only REV | grep -F '<имя>'` для FORK1 и PORT; для семи имён с найденными ресурсами есть `git cat-file -s FORK1:<путь>` и отдельная проверка первого содержимого через `git cat-file -p`. Первая строка LFS-пойнтера приведена для каждого из десяти найденных путей; у двух шаблонов BMP пути отсутствуют, поэтому blob для них не существует. Фильтры sardaukar сохранены отдельно для обеих ревизий и возвращают пустой вывод.

## Пункт 4: покрытие команд и формул

В `track3-evidence.md` для обеих ревизий есть:

- `git grep` результатов присваивания `m_windowWidth`, `m_windowHeight`, `m_viewportWidth` и `m_viewportHeight`, а также строки конструктора;
- `git show` исходника конструктора и `calibrate`, откуда взяты формулы ширины/высоты окна и viewport;
- полный stdout заданного поиска мест создания `cMapCamera`, включая вызов в `cGame::setupGame`; непосредственно строки с аргументами дополнительно показаны командами `git show`;
- `git grep` по проверкам областей мыши и вывод `git show` для полных тел `updateMouseCell` и `boxSelectLogic` в FORK1 и PORT.

Таким образом, фактические команды и исходный вывод к каждой строке `camera-mouse.tsv` уже присутствуют в `track3-evidence.md`; таблицы не менялись.
