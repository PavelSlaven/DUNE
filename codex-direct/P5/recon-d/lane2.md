# Пункт 2: вызовы режима UiAudit из кода игры в FORK1

## Команда поиска и вывод

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'uiaudit::|UiAudit' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src ':!src/debug'
```

Вывод: 122 строк.

```text
9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.h:25:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame.h:313:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:12:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:771:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:772:            uiaudit::beginFrame(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:780:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp:781:            uiaudit::onFramePresented(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/controls/cMouse.h:99:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cBuildingListDrawer.h:16:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:9:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:100:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:101:        uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp:102:        UiAuditAccess::recordCommandBarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.h:16:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:5:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:73:    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:74:        uiaudit::recordClick("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:84:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cMiniMapDrawer.cpp:85:        uiaudit::recordArea("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cOrderDrawer.h:13:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:69:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:70:        UiAuditAccess::recordSidebarClicks(*this);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:81:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:82:        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:366:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp:367:        uiaudit::recordArea("build-list", layout.catalog.getX(), layout.catalog.getY(), layout.catalog.getWidth(), layout.catalog.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.h:17:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:7:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1031:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1032:        uiaudit::recordLabel("structure-health", iStructure, "STRUCTURE", draw_x, draw_y, width_x + 1, height_y + 1,
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cStructureDrawer.cpp:1033:                             uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:3:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:59:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:60:        uiaudit::recordText(msg, x, y, cacheEntry->width, cacheEntry->height);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:108:    std::optional<uiaudit::BoxScope> auditBox;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:109:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:140:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:141:        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:142:        uiaudit::recordText(msg, x, y, width, height, &box);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:169:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:170:        const uiaudit::Rect box{rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()};
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:171:        uiaudit::recordText(msg, origin.x, origin.y, width, height, &box);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:194:    std::optional<uiaudit::BoxScope> auditBox;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cTextDrawer.cpp:195:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:17:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:581:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:582:        uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:633:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:634:        uiaudit::recordUnitLabel("health", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:660:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:661:            uiaudit::beginLabelText();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:665:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:666:            uiaudit::endLabelText("group", iID, iType, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:720:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp:723:            uiaudit::recordUnitLabel("experience", iID, iType, drawx, drawy, (iStars - 1) * 9 + star->w, star->h, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:111:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:112:        uiaudit::recordClick("house-atreides", houseAtreides.getX(), houseAtreides.getY(), houseAtreides.getWidth(), houseAtreides.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:113:        uiaudit::recordClick("house-ordos", houseOrdos.getX(), houseOrdos.getY(), houseOrdos.getWidth(), houseOrdos.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:114:        uiaudit::recordClick("house-harkonnen", houseHarkonnen.getX(), houseHarkonnen.getY(), houseHarkonnen.getWidth(), houseHarkonnen.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cChooseHouseState.cpp:115:        uiaudit::recordClick("house-back", backButtonRect->getX(), backButtonRect->getY(), backButtonRect->getWidth(), backButtonRect->getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:405:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp:406:        uiaudit::recordCanvasClick("credits-speed-up");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.h:26:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cMainMenuState.h:32:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cOptionsState.h:26:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:316:    if (uiaudit::isEnabled() && state == eRegionState::REGSTATE_SELECT_NEXT_CONQUEST) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.cpp:318:        uiaudit::recordClick("campaign-region-map", mapRect.getX(), mapRect.getY(), mapRect.getWidth(), mapRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.h:85:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:452:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.cpp:454:            uiaudit::recordClick(name, r.getX(), r.getY(), r.getWidth(), r.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSetupSkirmishState.h:46:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiButton.cpp:1:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiButton.cpp:31:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiCheckBox.cpp:1:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiCheckBox.cpp:26:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiLabel.cpp:1:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiLabel.cpp:25:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiObject.cpp:4:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiObject.cpp:14:    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiObject.cpp:19:    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiSlider.cpp:1:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiSlider.cpp:20:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiWindow.cpp:1:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/gui/GuiWindow.cpp:25:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:25:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:86:    uiaudit::consumeArguments(argc, argv);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:88:    if (uiaudit::isEnabled() && uiaudit::handleEarlyExit(uiAuditExitCode)) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:114:            if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:115:                uiaudit::onSetupDone(game);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp:132:    if (uiaudit::isEnabled() && (uiAuditError || uiaudit::failed())) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:5:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:234:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:235:        uiaudit::recordArea("top-panel", 0, 0, game.m_screenW, cSideBar::TopBarHeight);
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:275:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:276:        uiaudit::recordClick("top-options", optionsRect.getX(), optionsRect.getY(), optionsRect.getWidth(), optionsRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:310:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:311:        uiaudit::recordClick("music-previous", layout.previous.getX(), layout.previous.getY(), layout.previous.getWidth(), layout.previous.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:312:        uiaudit::recordClick("music-next", layout.next.getX(), layout.next.getY(), layout.next.getWidth(), layout.next.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/managers/cDrawManager.cpp:313:        uiaudit::recordClick("music-speed-slider", layout.speedSlider.getX(), layout.speedSlider.getY(), layout.speedSlider.getWidth(), layout.speedSlider.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h:242:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:15:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:406:        if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp:407:            uiaudit::recordCanvasClick("mentat-skip");
9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.h:46:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:5:#include "debug/UiAudit.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:268:    if (uiaudit::isEnabled()) {
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:269:        uiaudit::dropClicksUnderModal();
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:272:            uiaudit::recordClick(("save-slot:" + std::to_string(index + 1)).c_str(), slot.getX(), slot.getY(), slot.getWidth(), slot.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:274:        uiaudit::recordClick("save-name", m_nameRect.getX(), m_nameRect.getY(), m_nameRect.getWidth(), m_nameRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:275:        uiaudit::recordClick("save-save", m_saveRect.getX(), m_saveRect.getY(), m_saveRect.getWidth(), m_saveRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:276:        uiaudit::recordClick("save-load", m_loadRect.getX(), m_loadRect.getY(), m_loadRect.getWidth(), m_loadRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.cpp:277:        uiaudit::recordClick("save-close", m_closeRect.getX(), m_closeRect.getY(), m_closeRect.getWidth(), m_closeRect.getHeight());
9208dcf5a358f40afd95c99480e4e09f781ed566:src/save/SaveSlotsDialog.hpp:36:    friend class UiAuditAccess;
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cPlatformLayerInit.cpp:1:#include "debug/UiAuditArguments.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cPlatformLayerInit.cpp:18:    const Uint32 initFlags = uiaudit::isEnabled()
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:1:#include "debug/UiAuditArguments.hpp"
9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cScreenInit.cpp:127:    if (uiaudit::isEnabled()) {
```

## Таблица

Полная таблица находится в hooks.tsv; строка таблицы соответствует одной строке команды git grep. Шаг вычислен по строке совпадения и сигнатуре с полным телом охватывающей функции; регистр учитывался.

### Число строк по шагам

| Шаг | Строк таблицы |
|---|---:|
| П5в | 14 |
| П7 | 0 |
| П8 | 7 |
| П9 | 4 |
| П10 | 5 |
| П5г | 94 |
| Всего | 122 |

Две строки относятся одновременно к П5в и П10; поэтому сумма чисел по шагам превышает общее число строк таблицы.

### Области функций FORK1 и сопоставление с PORT

| Область функции FORK1 | Функция | Подстроки словаря в строках функции | Место в PORT |
|---|---|---|---|
| src/cGame_logic.cpp@9208dcf:716-786 | cGame::run | нет | src/game/cGame_logic.cpp@7eb119b:570-636 |
| src/drawers/cCommandBarDrawer.cpp@9208dcf:97-124 | cCommandBarDrawer::draw | CommandBar, commandBar | нет |
| src/drawers/cMiniMapDrawer.cpp@9208dcf:71-101 | cMiniMapDrawer::draw | MiniMap | src/drawers/cMiniMapDrawer.cpp@7eb119b:108-133 |
| src/drawers/cSideBarDrawer.cpp@9208dcf:66-73 | cSideBarDrawer::draw | SideBar, Sidebar | src/drawers/cSideBarDrawer.cpp@7eb119b:80-91 |
| src/drawers/cSideBarDrawer.cpp@9208dcf:333-404 | cSideBarDrawer::drawHdBuildingLists | HudLayout, SideBar, BuildingList, OrderDrawer | нет функции |
| src/drawers/cSideBarDrawer.cpp@9208dcf:75-109 | cSideBarDrawer::drawHdSidebar | HudLayout, SideBar, Sidebar, BuildingList | нет функции |
| src/drawers/cStructureDrawer.cpp@9208dcf:1005-1042 | cStructureDrawer::drawStructureHealthBar | нет | src/drawers/cStructureDrawer.cpp@7eb119b:477-510 |
| src/drawers/cTextDrawer.cpp@9208dcf:54-66 | cTextDrawer::drawText | нет | src/drawers/cTextDrawer.cpp@7eb119b:43-53, src/drawers/cTextDrawer.cpp@7eb119b:55-58, src/drawers/cTextDrawer.cpp@7eb119b:60-63 |
| src/drawers/cTextDrawer.cpp@9208dcf:185-199 | cTextDrawer::drawTextCentered | нет | src/drawers/cTextDrawer.cpp@7eb119b:65-68, src/drawers/cTextDrawer.cpp@7eb119b:70-78, src/drawers/cTextDrawer.cpp@7eb119b:157-166 |
| src/drawers/cTextDrawer.cpp@9208dcf:94-113 | cTextDrawer::drawTextCenteredInBox | нет | src/drawers/cTextDrawer.cpp@7eb119b:80-93, src/drawers/cTextDrawer.cpp@7eb119b:95-98, src/drawers/cTextDrawer.cpp@7eb119b:100-103 |
| src/drawers/cTextDrawer.cpp@9208dcf:125-148 | cTextDrawer::drawTextScaledCenteredInBox | нет | src/drawers/cTextDrawer.cpp@7eb119b:105-124 |
| src/drawers/cTextDrawer.cpp@9208dcf:150-183 | cTextDrawer::drawTextScaledOpticallyCenteredInBox | нет | src/drawers/cTextDrawer.cpp@7eb119b:126-155 |
| src/gameobjects/units/cUnit.cpp@9208dcf:687-731 | cUnit::draw_experience | нет | нет функции |
| src/gameobjects/units/cUnit.cpp@9208dcf:647-669 | cUnit::draw_group | нет | нет функции |
| src/gameobjects/units/cUnit.cpp@9208dcf:614-645 | cUnit::draw_health | нет | нет функции |
| src/gameobjects/units/cUnit.cpp@9208dcf:570-593 | cUnit::draw_spice | нет | нет функции |
| src/gamestates/cChooseHouseState.cpp@9208dcf:107-172 | cChooseHouseState::draw | нет | src/gamestates/cChooseHouseState.cpp@7eb119b:111-142 |
| src/gamestates/cCreditsState.cpp@9208dcf:403-436 | cCreditsState::draw | нет | src/gamestates/cCreditsState.cpp@7eb119b:441-469 |
| src/gamestates/cSelectYourNextConquestState.cpp@9208dcf:307-353 | cSelectYourNextConquestState::draw | нет | src/gamestates/cSelectYourNextConquestState.cpp@7eb119b:341-376 |
| src/gamestates/cSetupSkirmishState.cpp@9208dcf:387-552 | cSetupSkirmishState::draw | нет | src/gamestates/cSetupSkirmishState.cpp@7eb119b:436-534 |
| src/gui/GuiButton.cpp@9208dcf:29-119 | GuiButton::draw | нет | src/gui/GuiButton.cpp@7eb119b:46-145 |
| src/gui/GuiCheckBox.cpp@9208dcf:24-53 | GuiCheckBox::draw | нет | src/gui/GuiCheckBox.cpp@7eb119b:39-63 |
| src/gui/GuiLabel.cpp@9208dcf:16-50 | GuiLabel::draw | нет | src/gui/GuiLabel.cpp@7eb119b:35-66 |
| src/gui/GuiObject.cpp@9208dcf:17-20 | GuiObject::auditClick | нет | нет функции |
| src/gui/GuiObject.cpp@9208dcf:12-15 | GuiObject::auditRecord | нет | нет функции |
| src/gui/GuiObject.cpp@9208dcf:2-10 | GuiObject::setTheme | нет | src/gui/GuiObject.cpp@7eb119b:29-32 |
| src/gui/GuiSlider.cpp@9208dcf:19-26 | GuiSlider::draw | нет | src/gui/GuiSlider.cpp@7eb119b:74-77 |
| src/gui/GuiWindow.cpp@9208dcf:23-36 | GuiWindow::draw | нет | src/gui/GuiWindow.cpp@7eb119b:36-47 |
| src/main.cpp@9208dcf:78-136 | main | нет | src/main.cpp@7eb119b:53-134 |
| src/managers/cDrawManager.cpp@9208dcf:296-422 | cDrawManager::drawMusicControls | MusicControls | нет функции |
| src/managers/cDrawManager.cpp@9208dcf:232-286 | cDrawManager::drawTopBarBackground | SideBar | src/managers/cDrawManager.cpp@7eb119b:301-315 |
| src/mentat/AbstractMentat.cpp@9208dcf:373-467 | AbstractMentat::draw | нет | 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/AbstractMentat.cpp:273:void AbstractMentat::draw()
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/AtreidesMentat.cpp:65:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/BeneMentat.cpp:91:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/HarkonnenMentat.cpp:64:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/OrdosMentat.cpp:63:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/SardaukarMentat.cpp:64:    AbstractMentat::draw(); |
| src/save/SaveSlotsDialog.cpp@9208dcf:263-409 | SaveSlotsDialog::draw | SaveSlot | нет |
| src/utils/cPlatformLayerInit.cpp@9208dcf:8-43 | cPlatformLayerInit::cPlatformLayerInit | нет | нет |
| src/utils/cScreenInit.cpp@9208dcf:125-147 | cScreenInit::getWindowedSize | нет | нет |

### Проверка путей PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src/audio/MusicController.h src/cGame.h src/cGame_logic.cpp src/controls/cMouse.h src/drawers/cBuildingListDrawer.h src/drawers/cCommandBarDrawer.cpp src/drawers/cCommandBarDrawer.h src/drawers/cMiniMapDrawer.cpp src/drawers/cOrderDrawer.h src/drawers/cSideBarDrawer.cpp src/drawers/cSideBarDrawer.h src/drawers/cStructureDrawer.cpp src/drawers/cTextDrawer.cpp src/gameobjects/units/cUnit.cpp src/gamestates/cChooseHouseState.cpp src/gamestates/cCreditsState.cpp src/gamestates/cCreditsState.h src/gamestates/cMainMenuState.h src/gamestates/cOptionsState.h src/gamestates/cSelectYourNextConquestState.cpp src/gamestates/cSelectYourNextConquestState.h src/gamestates/cSetupSkirmishState.cpp src/gamestates/cSetupSkirmishState.h src/gui/GuiButton.cpp src/gui/GuiCheckBox.cpp src/gui/GuiLabel.cpp src/gui/GuiObject.cpp src/gui/GuiSlider.cpp src/gui/GuiWindow.cpp src/main.cpp src/managers/cDrawManager.cpp src/map/cMapCamera.h src/mentat/AbstractMentat.cpp src/mentat/AbstractMentat.h src/save/SaveSlotsDialog.cpp src/save/SaveSlotsDialog.hpp src/utils/cPlatformLayerInit.cpp src/utils/cScreenInit.cpp
```

Вывод (список найденных путей; пути из входного списка, которых в выводе нет, отсутствуют в PORT):

```text
src/controls/cMouse.h
src/drawers/cBuildingListDrawer.h
src/drawers/cMiniMapDrawer.cpp
src/drawers/cOrderDrawer.h
src/drawers/cSideBarDrawer.cpp
src/drawers/cSideBarDrawer.h
src/drawers/cStructureDrawer.cpp
src/drawers/cTextDrawer.cpp
src/gameobjects/units/cUnit.cpp
src/gamestates/cChooseHouseState.cpp
src/gamestates/cCreditsState.cpp
src/gamestates/cCreditsState.h
src/gamestates/cMainMenuState.h
src/gamestates/cOptionsState.h
src/gamestates/cSelectYourNextConquestState.cpp
src/gamestates/cSelectYourNextConquestState.h
src/gamestates/cSetupSkirmishState.cpp
src/gamestates/cSetupSkirmishState.h
src/gui/GuiButton.cpp
src/gui/GuiCheckBox.cpp
src/gui/GuiLabel.cpp
src/gui/GuiObject.cpp
src/gui/GuiSlider.cpp
src/gui/GuiWindow.cpp
src/main.cpp
src/managers/cDrawManager.cpp
```

### Поиск функции для пути, отсутствующего в PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'cGame::run(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/game/cGame_logic.cpp:570:void cGame::run()
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/include/sGameServices.h:60:    Texture *screenTexture = nullptr; // set in cGame::run(), before any state transition
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'cCommandBarDrawer::draw(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
пустой вывод; код возврата 1
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'AbstractMentat::draw(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/AbstractMentat.cpp:273:void AbstractMentat::draw()
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/AtreidesMentat.cpp:65:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/BeneMentat.cpp:91:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/HarkonnenMentat.cpp:64:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/OrdosMentat.cpp:63:    AbstractMentat::draw();
7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gameobjects/mentat/SardaukarMentat.cpp:64:    AbstractMentat::draw();
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'SaveSlotsDialog::draw(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
пустой вывод; код возврата 1
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'cPlatformLayerInit::cPlatformLayerInit(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
пустой вывод; код возврата 1
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n 'cScreenInit::getWindowedSize(' 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- src
```

Вывод:

```text
пустой вывод; код возврата 1
```

### Сверка количества строк

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
python3 -c 'from pathlib import Path; import subprocess; rev='"'"'9208dcf5a358f40afd95c99480e4e09f781ed566'"'"'; r=subprocess.run(['"'"'git'"'"','"'"'grep'"'"','"'"'-n'"'"','"'"'-E'"'"','"'"'uiaudit::|UiAudit'"'"',rev,'"'"'--'"'"','"'"'src'"'"','"'"':!src/debug'"'"'],text=True,capture_output=True,check=True); g=len(r.stdout.splitlines()); t=len(Path('"'"'.tmp/p5dr/hooks.tsv'"'"').read_text(encoding='"'"'utf-8'"'"').splitlines())-1; print(f'"'"'git grep строк: {g}'"'"'); print(f'"'"'hooks.tsv строк данных: {t}'"'"'); print(f'"'"'совпадение: {g==t}'"'"')'
```

Вывод:

```text
git grep строк: 122
hooks.tsv строк данных: 122
совпадение: True
```
