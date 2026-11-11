# Точечная сверка

Для каждого выбранного факта выполнена отдельная команда `git show` с указанной ревизией.

## Из `names.md`

### 1. `src/sidebar/cSideBar.cpp@dc6e5ff:446-460`

Факт: `setSelectedListId` обновляет выбранный ID и снимает/устанавливает выделение у старого и нового списка, если их ID допустимы.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cSideBar.cpp | nl -ba | sed -n '446,460p'
```

Вывод:

```text
   446	void cSideBar::setSelectedListId(eListType value)
   447	{
   448	    Logger::info(COMP_SIDEBAR, "cSideBar::setSelectedListId", "m_PlayerId = [{}] - old value [{}], new [{}]",
   449	                 m_player->getId(), m_selectedListID, eListTypeAsInt(value));
   450	
   451	    int oldListId = m_selectedListID;
   452	    m_selectedListID = eListTypeAsInt(value);
   453	    if (oldListId > -1 && oldListId < LIST_MAX) {
   454	        m_lists[oldListId]->setSelected(false);
   455	    }
   456	
   457	    if (m_selectedListID > -1 && m_selectedListID < LIST_MAX) {
   458	        m_lists[m_selectedListID]->setSelected(true);
   459	    }
   460	}
```

Вердикт: **совпало**.

### 2. `src/sidebar/cBuildingListUpdater.cpp@dc6e5ff:42-68`

Факт: для человека и ИИ в skirmish выполняются строгая обработка создания здания и `evaluateUpgrades`; для ИИ в кампании вызывается обработчик кампании.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/sidebar/cBuildingListUpdater.cpp | nl -ba | sed -n '42,68p'
```

Вывод:

```text
    42	void cBuildingListUpdater::onStructureCreated(int structureType)
    43	{
    44	    m_player->log("onStructureCreated - begin");
    45	
    46	    if (m_player->isHuman()) {
    47	        // always strict (skirmish) mode. Which means, do not cheat...
    48	        onStructureCreatedSkirmishMode(structureType);
    49	        evaluateUpgrades();
    50	    }
    51	    else {
    52	        // AI m_players...
    53	
    54	        if (m_settings->isSkirmish()) {
    55	            // on skirmish mode use the 'strict' / no cheating mode (same as human m_players)
    56	            onStructureCreatedSkirmishMode(structureType);
    57	            evaluateUpgrades();
    58	        }
    59	        else {
    60	            // but on campaign missions, the AI has to cheat in order to be more fun...
    61	            onStructureCreatedCampaignMode(structureType);
    62	            // AI does use upgrades at all...
    63	        }
    64	    }
    65	
    66	    m_player->logStructures();
    67	    m_player->log("onStructureCreated - end");
    68	}
```

Вердикт: **совпало**.

### 3. `src/game/cNotificationArea.cpp@dc6e5ff:35-41`

Факт: `addNotification` добавляет уведомление, затем сортирует их по таймеру в порядке убывания.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cNotificationArea.cpp | nl -ba | sed -n '35,41p'
```

Вывод:

```text
    35	void cNotificationArea::addNotification(const std::string &msg, eNotificationType type)
    36	{
    37	    m_notifications.push_back(cPlayerNotification(msg, type));
    38	    std::sort(m_notifications.begin(), m_notifications.end(), [](const cPlayerNotification &lhs, const cPlayerNotification &rhs) {
    39	        return lhs.getTimer() > rhs.getTimer();
    40	    });
    41	}
```

Вердикт: **совпало**.

### 4. `src/utils/cStructureUtils.cpp@dc6e5ff:282-293`

Факт: `isMouseOverStructure` возвращает `false` для пустого указателя, масштабирует размеры структуры с учётом zoom и проверяет попадание мыши в полученный прямоугольник.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/utils/cStructureUtils.cpp | nl -ba | sed -n '282,293p'
```

Вывод:

```text
   282	bool cStructureUtils::isMouseOverStructure(cAbstractStructure *structure, int screenX, int screenY)
   283	{
   284	    if (!structure) return false;
   285	
   286	    // translate the structure coordinates to screen coordinates
   287	    int drawX = structure->iDrawX();
   288	    int drawY = structure->iDrawY();
   289	    int width = m_mapCamera->factorZoomLevel(structure->getWidthInPixels());
   290	    int height = m_mapCamera->factorZoomLevel(structure->getHeightInPixels());
   291	
   292	    return cRectangle::isWithin(screenX, screenY, drawX, drawY, width, height);
   293	}
```

Вердикт: **совпало**.

## Из `missing.md`

### 5. `src/debug/UiAuditAccess.cpp@9208dcf:828`

Факт: в коде форка указатель `MusicController` берётся из `game.m_musicController`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '828p'
```

Вывод:

```text
   828	            MusicController *music = game.m_musicController.get();
```

Вердикт: **совпало**.

### 6. `src/debug/UiAuditAccess.cpp@9208dcf:836`

Факт: код форка получает состояние категории музыки `Gameplay` из `music->m_categories`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '836p'
```

Вывод:

```text
   836	            auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
```

Вердикт: **совпало**.

### 7. `src/debug/UiAuditAccess.cpp@9208dcf:403`

Факт: код форка перебирает кнопки из `drawer.m_buttons`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '403p'
```

Вывод:

```text
   403	    for (const auto &button : drawer.m_buttons) {
```

Вердикт: **совпало**.

### 8. `src/debug/UiAuditAccess.cpp@9208dcf:885`

Факт: код форка присваивает `mouse_co_x1` экранную X-координату первой ячейки через `mapCamera`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '885p'
```

Вывод:

```text
   885	            mouse->mouse_co_x1 = mapCamera->getWindowXPositionFromCell(cell1);
```

Вердикт: **совпало**.

## Из `fork.md`

### 9. `src/debug/UiAuditAccess.cpp@9208dcf:682-693`

Факт: `buildStructure` проверяет свободность места, создаёт здание фабрикой, прекращает работу при ошибке создания, устанавливает фазу 10 и возвращает ID.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | nl -ba | sed -n '682,693p'
```

Вывод:

```text
   682	int buildStructure(int type, int column, int row)
   683	{
   684	    if (!footprintFree(type, column, row)) {
   685	        return -1;
   686	    }
   687	    cAbstractStructure *created = cStructureFactory::getInstance()->createStructure(cellAt(column, row), type, HUMAN, 100);
   688	    if (created == nullptr) {
   689	        return -1;
   690	    }
   691	    created->setBuildingFase(10);
   692	    return created->getStructureId();
   693	}
```

Вердикт: **совпало**.

### 10. `src/drawers/cCommandBarDrawer.cpp@9208dcf:97-104`

Факт: `draw` перестраивает раскладку, а при включённом UI-аудите записывает область командной панели и её кнопки.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | nl -ba | sed -n '97,104p'
```

Вывод:

```text
    97	void cCommandBarDrawer::draw()
    98	{
    99	    rebuildLayout();
   100	    if (uiaudit::isEnabled()) {
   101	        uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
   102	        UiAuditAccess::recordCommandBarClicks(*this);
   103	    }
   104	```

Вердикт: **совпало**.

### 11. `src/managers/cDrawManager.cpp@9208dcf:296-307`

Факт: `drawMusicControls` резервирует ноль пикселей без сообщения, иначе длину его текста плюс 16, и передаёт ширину в `MusicControlsLayout::create`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp | nl -ba | sed -n '296,307p'
```

Вывод:

```text
   296	void cDrawManager::drawMusicControls(int left, int right)
   297	{
   298	    const std::string message = m_messageDrawer.getMessage();
   299	    const int reservedMessageWidth = message.empty()
   300	        ? 0
   301	        : m_textDrawer->getTextLength(message) + 16;
   302	    const MusicControlsLayout layout = MusicControlsLayout::create(
   303	        left,
   304	        right,
   305	        reservedMessageWidth
   306	    );
   307	    if (!layout.visible) {
```

Вердикт: **совпало**.

### 12. `src/save/SaveSlotsDialog.cpp@9208dcf:263-280`

Факт: открытый диалог сохранений при включённом UI-аудите убирает клики под модальным окном и записывает зоны слотов, поля имени и кнопок; затем задаёт цвет overlay.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp | nl -ba | sed -n '263,280p'
```

Вывод:

```text
   263	void SaveSlotsDialog::draw() const
   264	{
   265	    if (!m_open) {
   266	        return;
   267	    }
   268	    if (uiaudit::isEnabled()) {
   269	        uiaudit::dropClicksUnderModal();
   270	        for (std::size_t index = 0; index < m_slotRects.size(); ++index) {
   271	            const cRectangle &slot = m_slotRects[index];
   272	            uiaudit::recordClick(("save-slot:" + std::to_string(index + 1)).c_str(), slot.getX(), slot.getY(), slot.getWidth(), slot.getHeight());
   273	        }
   274	        uiaudit::recordClick("save-name", m_nameRect.getX(), m_nameRect.getY(), m_nameRect.getWidth(), m_nameRect.getHeight());
   275	        uiaudit::recordClick("save-save", m_saveRect.getX(), m_saveRect.getY(), m_saveRect.getWidth(), m_saveRect.getHeight());
   276	        uiaudit::recordClick("save-load", m_loadRect.getX(), m_loadRect.getY(), m_loadRect.getWidth(), m_loadRect.getHeight());
   277	        uiaudit::recordClick("save-close", m_closeRect.getX(), m_closeRect.getY(), m_closeRect.getWidth(), m_closeRect.getHeight());
   278	    }
   279	
   280	    const Color overlay{0, 0, 0, 190};
```

Вердикт: **совпало**.

## Итог

Совпало: 12. Не совпало: 0.
