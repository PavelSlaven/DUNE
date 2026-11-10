# P5CR2, дорожка 3: журнал проверки пунктов 2–4


### Пункт 2 — инвентарь условий if / else if / ?: по полным файлам

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'if[[:space:]]*\(|else[[:space:]]+if|\?' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:68:    if (hasDrawnCurrentCredits() || initial) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:75:        // TODO: make it 'roll' instead of 'jump' to the newest credits?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:79:        if (newCurrentCredits != previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:83:            if (diff > 200) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:86:            else if (diff > 20) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:95:        if (currentCredits > previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:98:        else if (currentCredits < previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:106:        if (TIMER_money > 20) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:107:            if (rollSpeed > 0.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:110:            if (rollSpeed < 0.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:120:        if (rollSpeed < 3.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:142:        if (offset_direction[i] == 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:143:            if (currentId == CREDITS_NONE || previousId == CREDITS_NONE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:151:            if (currentCredits > previousCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:154:            else if (previousCredits > currentCredits) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:159:            if (currentId == previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:166:        if (offset_credit[i] > 18.0F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:169:            if (soundsMade < 7) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:250:    if (c == '0') return CREDITS_0;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:251:    if (c == '1') return CREDITS_1;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:252:    if (c == '2') return CREDITS_2;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:253:    if (c == '3') return CREDITS_3;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:254:    if (c == '4') return CREDITS_4;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:255:    if (c == '5') return CREDITS_5;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:256:    if (c == '6') return CREDITS_6;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:257:    if (c == '7') return CREDITS_7;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:258:    if (c == '8') return CREDITS_8;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:259:    if (c == '9') return CREDITS_9;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:278://			if (currentId > previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.cpp:280://			} else if (currentId < previousId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/CreditsDrawer.h:56:    int rolled; // how many credits did get rolled over?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:22:    if (text.empty()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:38:    if (drawer->getTextLength(text) <= maximumWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:53:    if (name == localization::text("Hi-Tech", "Авиазавод")) return localization::text("Hi-Tech", "Авиазавод");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:54:    if (name == localization::text("Spice Refinery", "Переработчик пряности")) return localization::text("Refinery", "Переработчик");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:55:    if (name == localization::text("MCV", "Мобильная база")) return localization::text("MCV", "Мобильная база");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:56:    if (name == localization::text("Light Infantry", "Отряд пехоты")) return localization::text("Infantry", "Пехота");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:57:    if (name == localization::text("Troopers", "Отряд ракетчиков")) return localization::text("Troopers", "Ракетчики");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:74:    if (listIDToDraw == eListTypeAsInt(eListType::LIST_CONSTYARD)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:117:    if (pressed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:121:    if (id < 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:123:        logbook("ERROR UNABLE TO DRAW LIST BECAUSE ID IS NOT VALID!?");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:154:        list->isAvailable() ? 255 : 96
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:156:    if (!list->isAvailable()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:168:        pressed ? active : border
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:170:    if (pressed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:180:    else if (list->isFlashing()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:219:    // is building an item in the list?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:238:        if (item == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:243:        if (card.getEndY() <= layout.cards.getY() ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:261:        if (shouldDrawStructureSize) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:266:        if (item->isBuilding()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:269:            if (!item->isDoneBuilding() || iFrame < 31) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:295:                if (item->shouldPlaceIt()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:298:                    ) ? Color{225, 48, 42, 255} : Color::white();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:306:                else if (item->shouldDeployIt()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:309:                    ) ? Color{225, 48, 42, 255} : Color::white();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:330:                if (isBuildingItemInList[i2] < 0) continue;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:331:                if (i2 == item->getSubList()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:337:            if (!item->isAvailable() || isBuildingSameSubListItem) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:350:                if (item->isPendingUpgrading()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:361:                if (item->isPendingBuilding()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:379:            if (list->getType() == eListType::LIST_STARPORT) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:382:                if (cannotPayIt) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:401:            if (list->getLastClickedId() == i) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:413:        if (listIsStarport) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:418:        if (showAmount) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:423:            if (amountToShow < 10) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:442:        if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:443:            if (m_renderListIds) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:453:        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:459:            if (item->isFlashing()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:485:    if (iW == 2 && iH == 2) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:489:    if (iW == 3 && iH == 2) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:493:    if (iW == 3 && iH == 3) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:506:    if (x >= drawX &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:520:    if (!layout.cards.isPointWithin(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:526:        if (item == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:530:        if (card.getY() < layout.cards.getY() ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:534:        if (card.isPointWithin(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:612:    if (m_smallTextDrawer->getTextLength(name) <= textWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:634:                ? candidateWord
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:636:            if (secondLine.empty() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:642:                    ? candidateWord
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:649:            firstLine.empty() ? name : firstLine,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:658:        if (secondLine.empty()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:687:    if (item->getBuildCost() > 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:737:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:741:    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:753:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:757:    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:769:    if (m_player == nullptr || m_player->getSideBar() == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:774:    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:803:    if (layout.maxScrollRow(list->getItemCount()) <= 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:821:    if (m_player == nullptr ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:828:    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:832:    if (list == nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:837:    if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:841:    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_UP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:845:    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:849:    if (event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED ||
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:858:    if (event.coords.y < thumb.getY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:861:    else if (event.coords.y > thumb.getEndY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:882:    if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:889:    if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:41:    if (m_state == messages::eMessageDrawerState::COMBAT) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:49:            ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:57:            ? music.panel.getEndX() + 8
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:80:            ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:83:        if (m_alpha > -1 && messageTextWidth > 0 && messageContentWidth > 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:85:            if (messageTextWidth <= messageContentWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:96:                if (scale >= 0.5F) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:115:    if (m_alpha > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:130:    if (m_fadeState == messages::eMessageDrawerFadingState::FADE_IN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:133:        if (m_TIMER_message > m_timeMessageIsVisible) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:134:            if (!m_keepMessage) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:141:        if (m_alpha > 254) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:149:    if (m_alpha < 0) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:154:    if (m_alpha < 1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:175:    if (m_bmpBar != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMessageDrawer.cpp:232:    if (m_bmpBar) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:73:    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:76:    if (!m_map) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:80:    if (m_status == eMinimapStatus::NOTAVAILABLE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:84:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:89:    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:94:    if (m_status == eMinimapStatus::LOWPOWER) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:113:    if (m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:114:        if (m_status == eMinimapStatus::NOTAVAILABLE) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:122:    if (m_status == eMinimapStatus::NOTAVAILABLE) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:127:    if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:128:        if (!hasRadarAndEnoughPower) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:137:    if (m_status == eMinimapStatus::POWERDOWN || m_status == eMinimapStatus::LOWPOWER) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:138:        if (hasRadarAndEnoughPower) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:149:    if (m_status == eMinimapStatus::POWERDOWN) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:150:        if (m_iStaticFrame < STAT21) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:157:    else if (m_status == eMinimapStatus::POWERUP) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:158:        if (m_iStaticFrame > STAT01) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:204:            //@mira where is map ?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:207:            if (m_map->isVisible(iCll, m_player->getId())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:213:            if (!m_map->isWithinBoundaries(x, y)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:240:    if (startX < m_RectFullMinimap.getX()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:244:    if (startY < m_RectFullMinimap.getY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:248:    if (startX + minimapWidth > m_RectFullMinimap.getEndX()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:251:    if (startY + minimapHeight > m_RectFullMinimap.getEndY()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:268:            if (!m_map->isWithinBoundaries(x, y)) continue;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:272:            if (!m_map->isVisible(iCll, m_player->getId())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:281:            if (idOfStructureAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:283:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:284:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:290:            if (idOfUnitAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:292:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:293:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:299:            if (idOfAirUnitAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:301:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:302:                    if (iPlr != m_player->getId()) continue; // skip non player units
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:308:            if (idOfWormAtCell > -1) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:309:                if (playerOnly) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:316:            if (iColor.r == black.r && iColor.g == black.g && iColor.b == black.b) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:369:    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:373:        if (m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.h:67:    //@mira : where is map ? Where is this initialisation ?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:69:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:81:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:113:    if (m_player->isHouse(ATREIDES)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:116:    if (m_player->isHouse(HARKONNEN)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:119:    if (m_player->isHouse(ORDOS)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:127:    if (m_player->isHouse(ATREIDES)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:130:    if (m_player->isHouse(HARKONNEN)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:133:    if (m_player->isHouse(ORDOS)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:182:    if (crest != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:216:    if (!m_player->hasRadarAndEnoughPower() && crest != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:253:        ? m_player->getErrorFadingColor()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:316:        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:325:        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:338:    if (selectedListId >= 0 && selectedListId < cSideBar::LIST_MAX) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:366:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:384:    if (selectedList != nullptr) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:390:        if (listId == selectedListId) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:394:        if (list->isAvailable() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:400:    if (selectedList != nullptr &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:97:    if (game.m_drawUsages) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:107:        if (unit[i].isValid()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:115:        if (pStructure) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:123:        if (pBullet.bAlive) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:131:        if (pParticle.isValid()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:155:    if (humanPlayer.selected_structure < 0) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:157:    if (!theStructure) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:159:    if (rallyPointCell < 0) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:198:    // TODO: move drawing this into mouse state draw function ??
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:199:    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:200:    if (!m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:203:    if (itemToPlace == nullptr) return;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:212:    // TODO: replace messageDrawer with drawMessageBar?
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:222:    if (context->shouldDrawToolTip()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:234:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:275:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:278:    if (game.getMouse()->isLeftButtonClicked() &&
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:300:        ? 0
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:307:    if (!layout.visible) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:310:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:328:    if (layout.showsLabel()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:333:               m_smallTextDrawer->getTextLength(name + (truncated ? ellipsis : std::string{})) > layout.label.getWidth() - 10) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:351:        if (!name.empty() && truncated) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:383:    if ((mouse->isLeftButtonPressed() || mouse->isLeftButtonClicked()) && mouseOverSlider) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:386:    if (!mouse->isLeftButtonPressed() && !mouse->isLeftButtonClicked()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:389:    if (m_speedSliderDragging) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:399:        if (requestedGlobalSpeed != globalSpeed) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:412:    if (mouse->isLeftButtonClicked()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:413:        if (mouse->isOverRectangle(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:417:        else if (mouse->isOverRectangle(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:480:    if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:481:        if (event.hasKeys(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:484:        if (event.hasKey(SDL_SCANCODE_G)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:492:    if (game.isDebugMode()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:495:        if (event.hasEitherKey(SDL_SCANCODE_TAB, SDL_SCANCODE_D)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:498:        if (event.hasKey(SDL_SCANCODE_G)) {
```

Exit code: 0.

### Пункт 2 — все упоминания функций drawHd по полным файлам

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'drawHd[A-Za-z0-9_]*' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:259:        drawHdCard(item, iDrawX, iDrawY);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:467:    drawHdScrollbar(list, layout);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:551:void cBuildingListDrawer::drawHdCard(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp:781:void cBuildingListDrawer::drawHdScrollbar(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.h:57:    void drawHdCard(cBuildingListItem *item, int x, int y);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.h:58:    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:72:    drawHdSidebar();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:75:void cSideBarDrawer::drawHdSidebar()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:106:    drawHdRadarPanel();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:107:    drawHdCapacities();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:108:    drawHdBuildingLists();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:139:void cSideBarDrawer::drawHdRadarPanel()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:236:void cSideBarDrawer::drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:306:void cSideBarDrawer::drawHdCapacities()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:314:    drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:323:    drawHdMeter(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:333:void cSideBarDrawer::drawHdBuildingLists()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:41:    void drawHdSidebar();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:42:    void drawHdBuildingLists();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:43:    void drawHdRadarPanel();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:44:    void drawHdCapacities();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:45:    void drawHdMeter(
```

Exit code: 0.

### Пункт 2 — cSideBarDrawer::draw и вызов drawHdSidebar

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '64,76p'
```

```text
    64	}
    65	
    66	// draws the sidebar on screen
    67	void cSideBarDrawer::draw()
    68	{
    69	    if (uiaudit::isEnabled()) {
    70	        UiAuditAccess::recordSidebarClicks(*this);
    71	    }
    72	    drawHdSidebar();
    73	}
    74	
    75	void cSideBarDrawer::drawHdSidebar()
    76	{
```

Exit code: 0.

### Пункт 2 — вызов drawHdCard внутри полного draw-list участка

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '225,266p'
```

```text
   225	
   226	    renderDrawer->setClippingFor(
   227	        layout.cards.getX(),
   228	        layout.cards.getY(),
   229	        layout.cards.getEndX(),
   230	        layout.cards.getEndY()
   231	    );
   232	
   233	    // Draw the visible icon rows. HD positions come from HudLayout so drawing
   234	    // and hit testing cannot drift apart.
   235	    for (int i = 0; i < end; i++) {
   236	        cBuildingListItem *item = list->getItem(i);
   237	
   238	        if (item == nullptr) {
   239	            continue; // allow gaps in the list data structure (just not with rendering)
   240	        }
   241	
   242	        const cRectangle card = layout.cardRect(i, scrollRow);
   243	        if (card.getEndY() <= layout.cards.getY() ||
   244	            card.getY() >= layout.cards.getEndY()) {
   245	            continue;
   246	        }
   247	        iDrawX = card.getX();
   248	        iDrawY = card.getY();
   249	
   250	        int iDrawXEnd = iDrawX + withOfIcon;
   251	        int iDrawYEnd = iDrawY + heightOfIcon;
   252	
   253	        // asumes drawing for human player
   254	        bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());
   255	
   256	        // icon id must be set , assert it.
   257	        assert(item->getIconId() > -1);
   258	
   259	        drawHdCard(item, iDrawX, iDrawY);
   260	
   261	        if (shouldDrawStructureSize) {
   262	            drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
   263	        }
   264	
   265	        // when this item is being built.
   266	        if (item->isBuilding()) {
```

Exit code: 0.

### Пункт 2 — безусловный вызов drawHdScrollbar после отрисовки карточек

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '450,472p'
```

```text
   450	
   451	        // draw rectangle when mouse hovers over icon
   452	        auto m_mouse = game.getMouse();
   453	        if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
   454	            renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
   455	            renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
   456	        }
   457	        else {
   458	            Color color = list->getFlashingColor();
   459	            if (item->isFlashing()) {
   460	                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
   461	                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
   462	            }
   463	        }
   464	    }
   465	
   466	    renderDrawer->resetClippingFor();
   467	    drawHdScrollbar(list, layout);
   468	}
   469	
   470	/**
   471	 * Draw the amount of squares a structure would take. The X and Y coordinates are the top
   472	 * left coordinates of an icon.
```

Exit code: 0.

### Пункт 2 — безусловные вызовы HD-подфункций боковой панели

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | nl -ba | sed -n '101,111p'
```

```text
   101	        layout.sidebar.getX() + 5,
   102	        game.m_screenH,
   103	        Color{166, 124, 44, 255}
   104	    );
   105	
   106	    drawHdRadarPanel();
   107	    drawHdCapacities();
   108	    drawHdBuildingLists();
   109	}
   110	
   111	Texture *cSideBarDrawer::getHouseCrest() const
```

Exit code: 0.

### Пункт 3 — строки с литералами .png/.bmp и вызовами loadHdUiTexture во всех 25 файлах

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E '"[^"]+\.(png|bmp)"|loadHdUiTexture' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp src/drawers/CreditsDrawer.h src/drawers/cBuildingListDrawer.cpp src/drawers/cBuildingListDrawer.h src/drawers/cMessageDrawer.cpp src/drawers/cMessageDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cMiniMapDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/managers/cDrawManager.cpp src/managers/cDrawManager.h src/map/cMapCamera.cpp src/map/cMapCamera.h src/sidebar/cBuildingList.cpp src/sidebar/cBuildingList.h src/sidebar/cBuildingListFactory.cpp src/sidebar/cBuildingListItem.cpp src/sidebar/cBuildingListItem.h src/sidebar/cBuildingListUpdater.cpp src/sidebar/cSideBar.cpp src/sidebar/cSideBar.h src/cGame_logic.cpp src/controls/cGameControlsContext.cpp src/controls/cMouse.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1944:    std::string filename = std::format("{}x{}_{:0>4}.bmp", m_screenW, m_screenH, m_screenshot);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1956:    std::string name = std::format("screenshot{}.bmp",m_screenshot);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2542:                "outcome_victory_en.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2543:                "outcome_victory_ru.png"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2546:                "outcome_defeat_en.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2547:                "outcome_defeat_ru.png"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:2549:        texture = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:31:    m_houseCrests[0] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:32:        "hud_house_atreides.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:36:    m_houseCrests[1] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:37:        "hud_house_harkonnen.png",
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:41:    m_houseCrests[2] = loadHdUiTexture(
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:42:        "hud_house_ordos.png",
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_victory_en.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_victory_en.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_victory_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_victory_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_victory_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_defeat_en.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_defeat_en.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_en.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'outcome_defeat_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'outcome_defeat_ru.png' || true
```

```text
resources/bin/data/hd4/outcome_defeat_ru.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_atreides.png' || true
```

```text
resources/bin/data/hd4/hud_house_atreides.png
resources/hd/master4/ui/hud_house_atreides.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_atreides.png' || true
```

```text
resources/bin/data/hd4/hud_house_atreides.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_harkonnen.png' || true
```

```text
resources/bin/data/hd4/hud_house_harkonnen.png
resources/hd/master4/ui/hud_house_harkonnen.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_harkonnen.png' || true
```

```text
resources/bin/data/hd4/hud_house_harkonnen.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'hud_house_ordos.png' || true
```

```text
resources/bin/data/hd4/hud_house_ordos.png
resources/hd/master4/ui/hud_house_ordos.png
```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'hud_house_ordos.png' || true
```

```text
resources/bin/data/hd4/hud_house_ordos.png
```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F {}x{}_{:0>4}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F '{}x{}_{:0>4}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F {}x{}_{:0>4}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F '{}x{}_{:0>4}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree FORK1: grep -F screenshot{}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -F 'screenshot{}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — ls-tree PORT: grep -F screenshot{}.bmp

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -F 'screenshot{}.bmp' || true
```

```text

```

Exit code: 0.

### Пункт 3 — sardaukar-пути с тематикой HUD/герба FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 | grep -i -E 'sardaukar' | grep -i -E 'hud|crest|house|emblem|logo' || true
```

```text

```

Exit code: 0.

### Пункт 3 — sardaukar-пути с тематикой HUD/герба PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 832c953a94a632d57872349013f7ed1a37434715 | grep -i -E 'sardaukar' | grep -i -E 'hud|crest|house|emblem|logo' || true
```

```text

```

Exit code: 0.

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_victory_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_en.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_victory_en.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_en.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_victory_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_ru.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_victory_ru.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_victory_ru.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_defeat_en.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_en.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_defeat_en.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_en.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/outcome_defeat_ru.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_ru.png
```

```text
132
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/outcome_defeat_ru.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/outcome_defeat_ru.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_atreides.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_atreides.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_atreides.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_atreides.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_atreides.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_atreides.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_atreides.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_harkonnen.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_harkonnen.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_harkonnen.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_harkonnen.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_harkonnen.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_harkonnen.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_harkonnen.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/bin/data/hd4/hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_ordos.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/bin/data/hd4/hud_house_ordos.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/hd4/hud_house_ordos.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 3 — размер blob FORK1 resources/hd/master4/ui/hud_house_ordos.png

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_ordos.png
```

```text
131
```

Exit code: 0.

### Пункт 3 — проверка первой строки blob FORK1 resources/hd/master4/ui/hud_house_ordos.png

```sh
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/ui/hud_house_ordos.png
```

```text
version https://git-lfs.github.com/spec/v1
```

### Пункт 4 — присваивания размеров видимой области камеры FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cMapCamera::cMapCamera|m_window(Width|Height)[[:space:]]*=|m_viewport(Width|Height)[[:space:]]*=' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/map/cMapCamera.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:37:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:49:    m_windowWidth= game.m_screenW - widthOfSidebar;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:50:    m_windowHeight= game.m_screenH - m_heightOfTopBar;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:52:    m_viewportWidth=m_windowWidth;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:53:    m_viewportHeight=m_windowHeight;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:122:    m_viewportWidth = divideByZoomLevel(m_windowWidth);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:123:    m_viewportHeight = divideByZoomLevel(m_windowHeight);
```

Exit code: 0.

### Пункт 4 — все результаты заданного поиска мест создания cMapCamera FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'make_unique<cMapCamera>|new cMapCamera\(|cMapCamera\(' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:1219:    mapCamera = new cMapCamera(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:37:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp:66:cMapCamera::~cMapCamera()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h:23:    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h:25:    ~cMapCamera();
```

Exit code: 0.

### Пункт 4 — проверки регионов указателя в cMouse/cGameControlsContext FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cGameControlsContext::updateMouseCell|cMouse::boxSelectLogic|SidebarWidth|TopBarHeight|getMiniMapDrawer\(\)->isMouseOver' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/controls/cMouse.cpp src/controls/cGameControlsContext.cpp || true
```

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:46:void cGameControlsContext::updateMouseCell(const cPoint &coords)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:48:    if (coords.y < cSideBar::TopBarHeight) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:60:    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp:66:    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:241:void cMouse::boxSelectLogic(int mouseCell)
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:250:            if (coords.x > game.m_screenW - cSideBar::SidebarWidth) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:251:                mouse_co_x2 = game.m_screenW - cSideBar::SidebarWidth - 1;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:255:            if (mouse_co_y2 < cSideBar::TopBarHeight) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:256:                mouse_co_y2 = cSideBar::TopBarHeight;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp:353:                m_textDrawer->drawText(0, cSideBar::TopBarHeight + 1, std::format("MouseCell {}", mouseCell));
```

Exit code: 0.

### Пункт 4 — присваивания размеров видимой области камеры PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cMapCamera::cMapCamera|m_window(Width|Height)[[:space:]]*=|m_viewport(Width|Height)[[:space:]]*=' 832c953a94a632d57872349013f7ed1a37434715 -- src/gameobjects/map/cMapCamera.cpp || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:32:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:50:    m_windowWidth= m_gameSettings->getScreenW() - widthOfSidebar;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:51:    m_windowHeight= m_gameSettings->getScreenH() - m_heightOfTopBar;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:53:    m_viewportWidth=m_windowWidth;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:54:    m_viewportHeight=m_windowHeight;
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:143:    m_viewportWidth = divideByZoomLevel(m_windowWidth);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:144:    m_viewportHeight = divideByZoomLevel(m_windowHeight);
```

Exit code: 0.

### Пункт 4 — все результаты заданного поиска мест создания cMapCamera PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'make_unique<cMapCamera>|new cMapCamera\(|cMapCamera\(' 832c953a94a632d57872349013f7ed1a37434715 -- src || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp:850:    m_mapCamera = std::make_unique<cMapCamera>(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get());
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:32:cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp:67:cMapCamera::~cMapCamera()
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.h:44:    cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse);
832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.h:46:    ~cMapCamera();
```

Exit code: 0.

### Пункт 4 — проверки регионов указателя в cMouse/cGameControlsContext PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'cGameControlsContext::updateMouseCell|cMouse::boxSelectLogic|SidebarWidth|TopBarHeight|getMiniMapDrawer\(\)->isMouseOver' 832c953a94a632d57872349013f7ed1a37434715 -- src/controls/cMouse.cpp src/controls/cGameControlsContext.cpp || true
```

```text
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:86:void cGameControlsContext::updateMouseCell(const cPoint &coords)
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:88:    if (coords.y < cSideBar::TopBarHeight) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:94:    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp:100:    if (coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth)) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:279:void cMouse::boxSelectLogic(int mouseCell)
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:288:            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:289:                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:293:            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp:294:                m_mouseCoY2 = cSideBar::TopBarHeight;
```

Exit code: 0.

### Пункт 4 — код конструктора камеры 9208dcf

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | nl -ba | sed -n '37,64p'
```

```text
    37	cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove) :
    38	    m_moveSpeedDrag(moveSpeedDrag),
    39	    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    40	    m_cameraEdgeMove(cameraEdgeMove),
    41	    m_pMap(theMap)
    42	{
    43	    m_viewportStartX = m_viewportStartY = 32;
    44	    m_zoomLevel = game.getWorldScaleFactor();
    45	
    46	    int widthOfSidebar = cSideBar::SidebarWidth;
    47	    m_heightOfTopBar = cSideBar::TopBarHeight;
    48	
    49	    m_windowWidth= game.m_screenW - widthOfSidebar;
    50	    m_windowHeight= game.m_screenH - m_heightOfTopBar;
    51	
    52	    m_viewportWidth=m_windowWidth;
    53	    m_viewportHeight=m_windowHeight;
    54	
    55	    m_moveX = 0.0f;
    56	    m_moveY = 0.0f;
    57	
    58	    m_keyPressedDown = false;
    59	    m_keyPressedUp = false;
    60	    m_keyPressedLeft = false;
    61	    m_keyPressedRight = false;
    62	
    63	    calibrate();
    64	}
```

Exit code: 0.

### Пункт 4 — код calibrate камеры 9208dcf

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.cpp | nl -ba | sed -n '117,124p'
```

```text
   117	void cMapCamera::calibrate()
   118	{
   119	    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
   120	    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
   121	
   122	    m_viewportWidth = divideByZoomLevel(m_windowWidth);
   123	    m_viewportHeight = divideByZoomLevel(m_windowHeight);
   124	}
```

Exit code: 0.

### Пункт 4 — код конструктора камеры 832c953

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '32,65p'
```

```text
    32	cMapCamera::cMapCamera(cMap *theMap, float moveSpeedDrag, float moveSpeedBorderOrKeys, bool cameraEdgeMove, cGameSettings* gameSettings, cMouse* mouse) :
    33	    m_moveSpeedDrag(moveSpeedDrag),
    34	    m_moveSpeedBorderOrKeys(moveSpeedBorderOrKeys),
    35	    m_cameraEdgeMove(cameraEdgeMove),
    36	    m_pMap(theMap),
    37	    m_mapGeometry(theMap->getGeometry()),
    38	    m_gameSettings(gameSettings),
    39	    m_mouse(mouse)
    40	{
    41	    d2tm_assert(theMap != nullptr);
    42	    d2tm_assert(gameSettings != nullptr);
    43	    d2tm_assert(mouse != nullptr);
    44	    m_viewportStartX = m_viewportStartY = 32;
    45	    m_zoomLevel = std::clamp(m_gameSettings->getWorldScaleFactor(), 0.25f, 4.0f);
    46	
    47	    int widthOfSidebar = cSideBar::SidebarWidth;
    48	    m_heightOfTopBar = cSideBar::TopBarHeight;
    49	
    50	    m_windowWidth= m_gameSettings->getScreenW() - widthOfSidebar;
    51	    m_windowHeight= m_gameSettings->getScreenH() - m_heightOfTopBar;
    52	
    53	    m_viewportWidth=m_windowWidth;
    54	    m_viewportHeight=m_windowHeight;
    55	
    56	    m_moveX = 0.0f;
    57	    m_moveY = 0.0f;
    58	
    59	    m_keyPressedDown = false;
    60	    m_keyPressedUp = false;
    61	    m_keyPressedLeft = false;
    62	    m_keyPressedRight = false;
    63	
    64	    calibrate();
    65	}
```

Exit code: 0.

### Пункт 4 — код calibrate камеры 832c953

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/map/cMapCamera.cpp | nl -ba | sed -n '138,145p'
```

```text
   138	void cMapCamera::calibrate()
   139	{
   140	    m_tileHeight = factorZoomLevel(TILESIZE_WIDTH_PIXELS);
   141	    m_tileWidth = factorZoomLevel(TILESIZE_HEIGHT_PIXELS);
   142	
   143	    m_viewportWidth = divideByZoomLevel(m_windowWidth);
   144	    m_viewportHeight = divideByZoomLevel(m_windowHeight);
   145	}
```

Exit code: 0.

### Пункт 4 — cGame::setupGame и создание камеры FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '1000,1012p;1216,1222p'
```

```text
  1000	/**
  1001		Setup the game
  1002	
  1003		Should not be called twice.
  1004	*/
  1005	bool cGame::setupGame()
  1006	{
  1007	    cLogger *logger = cLogger::getInstance();
  1008	    logger->setDebugMode(m_debugMode);
  1009	    logger->logHeader("Dune II - The Maker");
  1010	    logger->logCommentLine(""); // whitespace
  1011	
  1012	    logger->logHeader("Version information");
  1216	    IniGameRessources::install_terrain(m_TerrainInfo);
  1217	
  1218	    delete mapCamera;
  1219	    mapCamera = new cMapCamera(&global_map, game.m_cameraDragMoveSpeed, game.m_cameraBorderOrKeyMoveSpeed, game.m_cameraEdgeMove);
  1220	
  1221	    cIni::installGame(m_gameFilename);
  1222	    // Now we are ready for the menu state
```

Exit code: 0.

### Пункт 4 — cGame::setupGame и создание камеры PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/game/cGame_logic.cpp | nl -ba | sed -n '696,704p;846,854p'
```

```text
   696	/**
   697		Setup the game
   698	
   699		Should not be called twice.
   700	*/
   701	bool cGame::setupGame()
   702	{
   703	    Logger::g_loggerInstance->setDebug(m_gameSettings->m_debugMode);
   704	
   846	    infoCreator.installInfos(*m_infoContext);
   847	
   848	    m_mapCamera.reset();
   849	
   850	    m_mapCamera = std::make_unique<cMapCamera>(m_gameObjectsContext->getMap(), m_cameraDragMoveSpeed, m_cameraBorderOrKeyMoveSpeed, m_cameraEdgeMove, m_gameSettings.get(), m_mouse.get());
   851	    m_services->mapCamera = m_mapCamera.get();
   852	    m_structureUtils->serviceInit(m_services.get());
   853	
   854	    m_cIni->installGame(m_gameFilename);
```

Exit code: 0.

### Пункт 4 — updateMouseCell FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '46,73p'
```

```text
    46	void cGameControlsContext::updateMouseCell(const cPoint &coords)
    47	{
    48	    if (coords.y < cSideBar::TopBarHeight) {
    49	        m_mouseCell = MOUSECELL_TOPBAR; // at the top bar or higher, so no mouse cell id.
    50	        m_mouseOnBattleField = false;
    51	        return;
    52	    }
    53	
    54	    if (drawManager->getCommandBarDrawer()->isMouseOver(coords)) {
    55	        m_mouseCell = MOUSECELL_COMMAND_BAR;
    56	        m_mouseOnBattleField = false;
    57	        return;
    58	    }
    59	
    60	    if (drawManager->getMiniMapDrawer()->isMouseOver()) {
    61	        m_mouseCell = MOUSECELL_MINIMAP; // on minimap
    62	        m_mouseOnBattleField = false;
    63	        return;
    64	    }
    65	
    66	    if (coords.x > (game.m_screenW - cSideBar::SidebarWidth)) {
    67	        m_mouseCell = MOUSECELL_SIDEBAR; // on sidebar
    68	        m_mouseOnBattleField = false;
    69	        return;
    70	    }
    71	    m_mouseOnBattleField = true;
    72	    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
    73	}
```

Exit code: 0.

### Пункт 4 — updateMouseCell PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cGameControlsContext.cpp | nl -ba | sed -n '86,110p'
```

```text
    86	void cGameControlsContext::updateMouseCell(const cPoint &coords)
    87	{
    88	    if (coords.y < cSideBar::TopBarHeight) {
    89	        m_mouseCell = MOUSE_CELL_HOVER_TOPBAR; // at the top bar or higher, so no mouse cell id.
    90	        m_mouseOnBattleField = false;
    91	        return;
    92	    }
    93	
    94	    if (m_drawManager->getMiniMapDrawer()->isMouseOver()) {
    95	        m_mouseCell = MOUSE_CELL_HOVER_MINIMAP; // on minimap
    96	        m_mouseOnBattleField = false;
    97	        return;
    98	    }
    99	
   100	    if (coords.x > (m_settings->getScreenW() - cSideBar::SidebarWidth)) {
   101	        m_mouseCell = MOUSE_CELL_HOVER_SIDEBAR; // on sidebar
   102	        m_mouseOnBattleField = false;
   103	        return;
   104	    }
   105	    m_mouseOnBattleField = true;
   106	    m_mouseCell = getMouseCellFromScreen(coords.x, coords.y);
   107	    if (m_mouseCell < 0) { // clamp mouse cell to map
   108	        m_mouseCellClamped = getMouseCellFromScreenClamped(coords.x, coords.y);
   109	    }
   110	}
```

Exit code: 0.

### Пункт 4 — boxSelectLogic FORK1

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.cpp | nl -ba | sed -n '241,272p'
```

```text
   241	void cMouse::boxSelectLogic(int mouseCell)
   242	{
   243	// When the mouse is pressed, we will check if the first coordinates are filled in
   244	    // if so, we will update the second coordinates. If the player holds his mouse we
   245	    // keep updating the second coordinates and create a rectangle to select units with.
   246	    if (mouse_co_x1 > -1 && mouse_co_y1 > -1) {
   247	        if (abs(coords.x - mouse_co_x1) > 4 && abs(coords.y - mouse_co_y1) > 4) {
   248	            // assign 2nd coordinates
   249	            mouse_co_x2 = coords.x;
   250	            if (coords.x > game.m_screenW - cSideBar::SidebarWidth) {
   251	                mouse_co_x2 = game.m_screenW - cSideBar::SidebarWidth - 1;
   252	            }
   253	
   254	            mouse_co_y2 = coords.y;
   255	            if (mouse_co_y2 < cSideBar::TopBarHeight) {
   256	                mouse_co_y2 = cSideBar::TopBarHeight;
   257	            }
   258	
   259	            // and draw the selection box
   260	            //_rect(bmp_screen, mouse_co_x1, mouse_co_y1, mouse_co_x2, mouse_co_y2, game.getColorFadeSelected(255, 255, 255));
   261	            renderDrawer->renderRectColor(mouse_co_x1, mouse_co_y1, mouse_co_x2-mouse_co_x1, mouse_co_y2-mouse_co_y1, game.getColorFadeSelected(255, 255, 255));
   262	        }
   263	
   264	        // Note that we have to fix up the coordinates when checking 'within border'
   265	        // for units (when X2 < X1 for example!)
   266	    }
   267	    else if (mouseCell > -1) {
   268	        // no first coordinates set, so do that here.
   269	        mouse_co_x1 = coords.x;
   270	        mouse_co_y1 = coords.y;
   271	    }
   272	}
```

Exit code: 0.

### Пункт 4 — boxSelectLogic PORT

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 832c953a94a632d57872349013f7ed1a37434715:src/controls/cMouse.cpp | nl -ba | sed -n '279,306p'
```

```text
   279	void cMouse::boxSelectLogic(int mouseCell)
   280	{
   281	// When the mouse is pressed, we will check if the first coordinates are filled in
   282	    // if so, we will update the second coordinates. If the player holds his mouse we
   283	    // keep updating the second coordinates and create a rectangle to select units with.
   284	    if (m_mouseCoX1 > -1 && m_mouseCoY1 > -1) {
   285	        if (abs(m_coords.x - m_mouseCoX1) > 4 && abs(m_coords.y - m_mouseCoY1) > 4) {
   286	            // assign 2nd coordinates
   287	            m_mouseCoX2 = m_coords.x;
   288	            if (m_coords.x > m_settings->getScreenW() - cSideBar::SidebarWidth) {
   289	                m_mouseCoX2 = m_settings->getScreenW() - cSideBar::SidebarWidth - 1;
   290	            }
   291	
   292	            m_mouseCoY2 = m_coords.y;
   293	            if (m_mouseCoY2 < cSideBar::TopBarHeight) {
   294	                m_mouseCoY2 = cSideBar::TopBarHeight;
   295	            }
   296	        }
   297	
   298	        // Note that we have to fix up the coordinates when checking 'within border'
   299	        // for units (when X2 < X1 for example!)
   300	    }
   301	    else if (mouseCell > -1) {
   302	        // no first coordinates set, so do that here.
   303	        m_mouseCoX1 = m_coords.x;
   304	        m_mouseCoY1 = m_coords.y;
   305	    }
   306	}
```

Exit code: 0.

## Итоги


- Пункт 2: `drawHd-branches.tsv` содержит заголовок без строк. Во всех заданных полных файлах `drawHd`-вызовы не стоят в ветви `if`, `else if` или `?:`, где противоположная ветвь вызывает другую функцию рисования или ничего не рисует. `drawHdSidebar`, `drawHdCard` и `drawHdScrollbar` вызываются без такого переключающего условия.

- Пункт 3: в 25 перечисленных файлах найдены семь изображений HUD, передаваемых в `loadHdUiTexture`, и два строковых шаблона с суффиксом `.bmp` для скриншотов. Для каждого имени сохранены результаты `ls-tree` по обеим ревизиям; для существующих путей в FORK1 сохранены размеры `cat-file -s` и проверка признака LFS.

- Пункт 4: `updateMouseCell` классифицирует верхнюю панель, мини-карту, боковую панель и поле боя; `boxSelectLogic` ограничивает прямоугольник выделения границами поля. В каждой ревизии записаны конструктор и `calibrate`, фактический вызов создания камеры и обе функции мыши.

- По фильтру sardaukar: FORK1 — 0 путей; PORT — 0 путей.
