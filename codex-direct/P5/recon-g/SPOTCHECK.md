# Выборочная сверка разведки P5GR (Haiku)

Источник фактов: `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\p5g\spot-rows.md` (15 фактов).
Ревизии: форк `9208dcf5a358f40afd95c99480e4e09f781ed566`, порт `4aa980e36ee7a8ff0e651ce10c4f55869d86f08d`.
Команды выполнялись только чтением: `ssh servak 'bash -s'`, в `/srv/dune/worktrees/u13g`, с `PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin`. Скрипт проверок: `C:\Users\Slaven\AppData\Local\Temp\claude\570e86ef5805dee8\ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea\scratchpad\p5g\spot-run.sh`.

Правило: диапазон длиннее 40 строк — первые 5 и последние 5; диапазон до 40 строк сверен целиком, в записи показано не больше 12 строк (сокращение отмечено).
Поля «класс в PORT» и «поиск имени функции в PORT» проверялись через `git grep -n -w <имя>` (и для классов, где нужен полный список, через `git grep -n 'class <имя>'`); поля «поиск имён ветки в PORT» не проверялись: у них нет поля «имя».

---

## Факт 1

Таблица: `access.tsv`, строка файла 229. Функция `prepareGameScreen`, имя `HUMAN`.

**1.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '780,784p;930,934p'` (диапазон 780-934, 155 строк)
```
bool UiAuditAccess::prepareGameScreen(cGame &game, int house, int kind)
{
    using uiaudit::GameKind;
    if (!enterPlaying(game, house, 22)) {
        return false;
        }
        default:
            return false;
    }
}
```
**1.2** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '793p'`
```
            cAbstractStructure *s = structure[i];
```
**1.3** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/include/definitions.h | sed -n '86p'`
```
#define HUMAN			0  // 0 = HUMAN			== ALLIES WITH FREMEN WHEN ATREIDES
```
**1.4** `git grep -n -w HUMAN 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cMapDrawer.cpp:362:    if (playerId < HUMAN || playerId >= MAX_PLAYERS) return -1;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cMouseDrawer.cpp:229:    if (theWindTrap->getOwner() == HUMAN) {
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cMouseDrawer.cpp:253:    if (theStructure->getOwner() == HUMAN) {
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cStructureDrawer.cpp:88:    if (!m_settings->isFogOfWarEnabled() || iPl != HUMAN) return;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cStructureDrawer.cpp:129:    cGameControlsContext *context = m_objects->getPlayer(HUMAN)->getGameControlsContext();
```
Дополнительная проверка (первое вхождение в 780-934): `git show ...UiAuditAccess.cpp | sed -n '780,934p' | grep -n 'HUMAN'` — первое совпадение на фрагменте 15, то есть строка 794.

**Итог: не совпало.** Строка 793 — `cAbstractStructure *s = structure[i];`, без `HUMAN`. Первое `HUMAN` в диапазоне 780-934 — строка 794. Остальные проверки (объявление на 86, поиск в PORT) совпали.

---

## Факт 2

Таблица: `access.tsv`, строка файла 139. Функция `recordSidebarClicks`, имя `getButtonHeight`.

**2.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '350,354p;395,399p'` (диапазон 350-399, 50 строк)
```
void UiAuditAccess::recordSidebarClicks(cSideBarDrawer &drawer)
{
    cSideBar *sidebar = drawer.m_sidebar;
    if (sidebar == nullptr) {
        return;
    if (starportOrdering && drawManager != nullptr && drawManager->getOrderDrawer() != nullptr) {
        const cRectangle &rect = drawManager->getOrderDrawer()->m_buttonRect;
        uiaudit::recordClick("order-button", rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight());
    }
}
```
**2.2** `... UiAuditAccess.cpp | sed -n '367p'`
```
                             list->getButtonWidth(), list->getButtonHeight());
```
Дополнительная проверка: `sed -n '350,399p' | grep -n 'getButtonHeight'` — первое совпадение на фрагменте 18, то есть строка 367.

**2.3** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/cBuildingList.h | sed -n '86p'`
```
    int getButtonHeight() const {
```
**2.4** `git grep -n -w getButtonHeight 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cBuildingListDrawer.cpp:136:    int height = list->getButtonHeight();
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cBuildingListDrawer.cpp:163:    int height = list->getButtonHeight();
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/sidebar/cBuildingList.h:106:    int getButtonHeight() const {
```
**Итог: совпало.**

---

## Факт 3

Таблица: `access.tsv`, строка файла 178. Функция `enterPlaying`, имя `global_map`.

**3.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '536,549p'` (14 строк; показаны первые 12, строки 548-549 не выводятся в запись, но сверены при проверке)
```
bool UiAuditAccess::enterPlaying(cGame &game, int house, int region)
{
    players[HUMAN].setHouse(house);
    game.m_region = region;
    game.setNextStateToTransitionTo(GAME_BRIEFING);
    game.transitionStateIfRequired();
    game.setNextStateToTransitionTo(GAME_PLAYING);
    game.transitionStateIfRequired();
    if (drawManager == nullptr || global_map.getWidth() <= 0 || mapCamera == nullptr) {
        return false;
    }
    drawManager->missionInit();
```
**3.2** `... UiAuditAccess.cpp | sed -n '544p'`
```
    if (drawManager == nullptr || global_map.getWidth() <= 0 || mapCamera == nullptr) {
```
**3.3** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/include/d2tmc.h | sed -n '59p'`
```
extern cMap       global_map;
```
**3.4** `git grep -n -w global_map 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5` (ожидалось пусто)
```
(пусто)
```
**Итог: совпало.** Поле «поиск в PORT: нет» подтверждено: вывод пустой.

---

## Факт 4

Таблица: `access.tsv`, строка файла 82. Функция `creditsScroll`, имя `m_titleHeight`.

**4.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '213,217p;255,259p'` (диапазон 213-259, 47 строк)
```
bool UiAuditAccess::creditsScroll(cGame &game, int frame)
{
    auto *credits = dynamic_cast<cCreditsState *>(game.m_currentState);
    if (credits == nullptr) {
        return false;
    }
    // A tall canvas holds fewer groups; the scene must still exist, so it shows the last group.
    credits->m_crawlerY = static_cast<float>(64 - offsets[lastStart]);
    return true;
}
```
**4.2** `... UiAuditAccess.cpp | sed -n '228p'`
```
    int offset = credits->m_titleHeight;
```
Дополнительная проверка: `sed -n '213,259p' | grep -n 'm_titleHeight'` — первое совпадение на фрагменте 16, то есть строка 228.

**4.3** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.h | sed -n '43p'`
```
    int m_titleHeight;
```
**4.4** `git grep -n -w m_titleHeight 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cCreditsState.cpp:74:    m_titleHeight = m_titleBmp->h;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cCreditsState.cpp:431:    int textCrawlY = m_crawlerY + m_titleHeight;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cCreditsState.cpp:449:    int textCrawlY = m_crawlerY + m_titleHeight;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cCreditsState.h:66:    int m_titleHeight;
```
**Итог: совпало.**

---

## Факт 5

Таблица: `access-helpers.tsv`, строка файла 119. Функция `listForKind`, имя `LIST_UNITS`.

**5.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '765,776p'` (12 строк, целиком)
```
eListType listForKind(int kind)
{
    switch (kind) {
        case uiaudit::GameKind::ListBuild: return eListType::LIST_CONSTYARD;
        case uiaudit::GameKind::ListInfantry: return eListType::LIST_FOOT_UNITS;
        case uiaudit::GameKind::ListVehicles: return eListType::LIST_UNITS;
        case uiaudit::GameKind::ListStarport: return eListType::LIST_STARPORT;
        case uiaudit::GameKind::ListPalace: return eListType::LIST_PALACE;
        case uiaudit::GameKind::ListUpgrades: return eListType::LIST_UPGRADES;
        default: return eListType::LIST_NONE;
    }
}
```
**5.2** `... UiAuditAccess.cpp | sed -n '769p'`
```
        case uiaudit::GameKind::ListInfantry: return eListType::LIST_FOOT_UNITS;
```
Дополнительная проверка: `sed -n '765,776p' | grep -n 'LIST_UNITS'` — совпадение на фрагменте 6, то есть строка 770: `case uiaudit::GameKind::ListVehicles: return eListType::LIST_UNITS;`.

**5.3** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/include/enums.h | sed -n '197p'`
```
    LIST_UNITS, // quad, trike, tanks, air units
```
**5.4** `git grep -n -w LIST_UNITS 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/cInfoContextCreator.cpp:195:    unitInfos[CARRYALL].listType = eListType::LIST_UNITS;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/cInfoContextCreator.cpp:214:    unitInfos[ORNITHOPTER].listType = eListType::LIST_UNITS;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/cInfoContextCreator.cpp:231:    unitInfos[DEVASTATOR].listType = eListType::LIST_UNITS;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/cInfoContextCreator.cpp:251:    unitInfos[HARVESTER].listType = eListType::LIST_UNITS;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/context/cInfoContextCreator.cpp:269:    unitInfos[TANK].listType = eListType::LIST_UNITS;
```
**Итог: не совпало.** Строка 769 — `case ...ListInfantry: return eListType::LIST_FOOT_UNITS;`, без `LIST_UNITS`. Первое вхождение `LIST_UNITS` в диапазоне — строка 770. Остальные проверки совпали.

---

## Факт 6

Таблица: `access-helpers.tsv`, строка файла 82. Функция `buildBase`, имя `kBaseSpots`.

**6.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditAccess.cpp | sed -n '704,708p;742,746p'` (диапазон 704-746, 43 строки)
```
bool buildBase(bool withRadar, float tankHp, BaseResult &result)
{
    players[HUMAN].setTechLevel(9);
    players[HUMAN].getBuildingListUpdater()->onStructureCreated(CONSTYARD);

        return false;
    }
    unit[result.harvesterId].iCredits = unit[result.harvesterId].getUnitInfo().credit_capacity;
    return true;
}
```
**6.2** `... UiAuditAccess.cpp | sed -n '711p'`
```
    for (const BaseSpot &spot : kBaseSpots) {
```
Дополнительная проверка: `sed -n '704,746p' | grep -n 'kBaseSpots'` — первое совпадение на фрагменте 8, то есть строка 711.

**6.3** `git grep -n -w kBaseSpots 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5` (ожидалось пусто, поле «поиск в PORT: нет»)
```
(пусто)
```
**Итог: совпало.** Поле «объявление в FORK1: нет» не проверялось отдельно: в записи нет строки для проверки.

---

## Факт 7

Таблица: `friends.tsv`, строка файла 14. Класс `cMapCamera`, ссылка `src/map/cMapCamera.h@9208dcf:242`.

**7.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h | sed -n '242p'`
```
    friend class UiAuditAccess;
```
**7.2** Контекст: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/map/cMapCamera.h | grep -n -E '^\s*(class|struct) |^\};'`
```
20:class cMapCamera : cInputObserver {
243:};
```
Строка 242 лежит внутри класса `cMapCamera` (строки 20-243).

**7.3** Поле «класс в PORT» перечисляет объявления `class cMapCamera;`. Полная проверка: `git grep -n 'class cMapCamera;' 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src` (всего 19 строк; первые 8, перечисленные в поле, совпали):
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/controls/cGameControlsContext.h:42:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/CreditsDrawer.h:33:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cMapDrawer.h:31:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cMiniMapDrawer.h:34:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cPlaceItDrawer.h:27:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cStructureDrawer.h:25:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/game/cGame.h:59:class cMapCamera;
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/game/cScreenShake.h:18:class cMapCamera;
```
Примечание: `git grep -n -w cMapCamera ... | head -5` дал другие строки (CMakeLists, `#include`), поэтому для поля «класс» использован шаблон `class cMapCamera;`.

**Итог: совпало.**

---

## Факт 8

Таблица: `friends.tsv`, строка файла 12. Класс `cSelectYourNextConquestState`, ссылка `src/gamestates/cSelectYourNextConquestState.h@9208dcf:85`.

**8.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.h | sed -n '85p'`
```
    friend class UiAuditAccess;
```
**8.2** Контекст: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cSelectYourNextConquestState.h | grep -n -E '^\s*(class|struct) |^\};'` (показаны строки 47 и 151)
```
47:class cSelectYourNextConquestState : public cGameState {
151:};
```
Строка 85 лежит внутри класса (47-151).

**8.3** Поле «класс в PORT»: `git grep -n 'class cSelectYourNextConquestState' 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src` (полный вывод, 2 строки):
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gamestates/cSelectYourNextConquestState.h:77:class cSelectYourNextConquestState : public cGameState {
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/utils/ini.h:25:class cSelectYourNextConquestState;
```
Примечание: `git grep -n -w cSelectYourNextConquestState ... | head -5` показал другие строки (CMakeLists, `cGame_logic.cpp`), поэтому для поля «класс» использован шаблон `class cSelectYourNextConquestState`.

**Итог: совпало.**

---

## Факт 9

Таблица: `missing-hooks.tsv`, строка файла 9. Функция `cUnit::draw_spice`, ссылка `src/gameobjects/units/cUnit.cpp@9208dcf:581`.

**9.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | sed -n '581p'`
```
    if (uiaudit::isEnabled()) {
```
**9.2** `... cUnit.cpp | sed -n '570,593p'` (диапазон 570-593, 24 строки; показаны первые 12)
```
void cUnit::draw_spice()
{
    const cRectangle visual = getVisualRectangle();
    float width_x = visual.getWidth();
    int height_y = std::max(1, static_cast<int>(std::lround(mapCamera->factorZoomLevel(4))));
    int drawx = visual.getX();
    int drawy = visual.getY() - ((height_y * 2) + 2);

    int max = getUnitInfo().credit_capacity;
    int w = healthBar(width_x, iCredits, max);

    if (uiaudit::isEnabled()) {
        uiaudit::recordUnitLabel("spice", iID, iType, drawx, drawy, static_cast<int>(width_x), height_y, uiaudit::Rect{visual.getX(), visual.getY(), visual.getWidth(), visual.getHeight()});
```
(строки 583-593 не выводятся в запись; сверены при проверке: 583 — `}`, 593 — `}`)

Строка 579 — `int w = healthBar(...)`, 580 — пустая, 581 — `if (uiaudit::isEnabled()) {`, 582 — `uiaudit::recordUnitLabel("spice", ...)`, 583 — `}`. Блок из поля «строки вызова» совпадает с 579-583.

**9.3** `git grep -n -w draw_spice 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.cpp:48:void cUnitDrawer::draw_spice()
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.h:31:    void draw_spice();
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gameobjects/map/cMap.cpp:904:            unitDrawer.draw_spice();
```
**Итог: совпало.** Замечания, не влияющие на итог: в факте строка `cUnitDrawer.cpp:48` записана как `void cUnitDrawer::draw_spice();` (с `;`), в PORT такой строки нет, там `void cUnitDrawer::draw_spice()`. Поле «поиск имён ветки в PORT» не проверялось: у факта нет поля «имя».

---

## Факт 10

Таблица: `missing-hooks.tsv`, строка файла 13. Функция `cUnit::draw_group`, ссылка `src/gameobjects/units/cUnit.cpp@9208dcf:660`.

**10.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gameobjects/units/cUnit.cpp | sed -n '660p'`
```
        if (uiaudit::isEnabled()) {
```
**10.2** `... cUnit.cpp | sed -n '647,669p'` (диапазон 647-669, 23 строки; показаны первые 12)
```
void cUnit::draw_group(cTextDrawer* textDrawer)
{
    if (iHitPoints < 0) return;

    const cRectangle visual = getVisualRectangle();
    int height_y = std::max(1, static_cast<int>(std::lround(mapCamera->factorZoomLevel(4))));
    int drawx = visual.getX();
    int drawy = visual.getY() - (height_y + 2);
    // draw group
    // TODO: make text smaller depending on zoom factor?
    if (iGroup > 0 && iPlayer == HUMAN) {
        // @mira I don't fix group name without acces to textDrawer: fixed on ctx branch
```
(строки 658-669 не выводятся в запись; сверены при проверке.)

Строка 658 — комментарий `// @mira ...`, 659 — `const int groupX = ...`, 660 — `if (uiaudit::isEnabled()) {`, 661 — `uiaudit::beginLabelText();`, 662 — `}`.

**10.3** `git grep -n -w draw_group 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.cpp:96:void cUnitDrawer::draw_group(cTextDrawer* textDrawer)
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cUnitDrawer.h:32:    void draw_group(cTextDrawer *textDrawer);
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/gameobjects/map/cMap.cpp:901:        unitDrawer.draw_group(m_textDrawer);
```
**Итог: совпало.** Замечание: как в факте 9, в факте `cUnitDrawer.cpp:96` записано с `;` на конце, в PORT такого `;` нет. Поле «поиск имён ветки в PORT» не проверялось.

---

## Факт 11

Таблица: `missing-hooks.tsv`, строка файла 6. Функция `cSideBarDrawer::drawHdSidebar`, ссылка `src/drawers/cSideBarDrawer.cpp@9208dcf:82`.

**11.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | sed -n '82p'`
```
        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
```
**11.2** `... cSideBarDrawer.cpp | sed -n '75,109p'` (диапазон 75-109, 35 строк; показаны первые 12)
```
void cSideBarDrawer::drawHdSidebar()
{
    const HudLayout layout = HudLayout::create(
        game.m_screenW,
        game.m_screenH
    );
    if (uiaudit::isEnabled()) {
        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
    }
    renderDrawer->renderRectFillColor(
```
(строки 85-109 не выводятся в запись; сверены при проверке; 109 — `}`.)

Строка 80 — `);`, 81 — `if (uiaudit::isEnabled()) {`, 82 — `uiaudit::recordArea(...)`, 83 — `}`, 84 — `renderDrawer->renderRectFillColor(`. Блок из поля «строки вызова» совпадает с 80-84.

**11.3** `git grep -n -w drawHdSidebar 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d -- src | head -5`
```
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cSideBarDrawer.cpp:100:    drawHdSidebar();
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cSideBarDrawer.cpp:109:void cSideBarDrawer::drawHdSidebar()
4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/drawers/cSideBarDrawer.h:68:    void drawHdSidebar();
```
**Итог: совпало.** Замечание: как в фактах 9-10, в факте `cSideBarDrawer.cpp:109` записано с `;`. Поле «поиск имён ветки в PORT» (`sidebar`, `getX`) не проверялось.

---

## Факт 12

Таблица: `scene-functions.tsv`, строка файла 4. Функция `onGameScreen(Scene value, bool hovering)`, ссылка `src/debug/UiAuditScenes.cpp@9208dcf:36-41`.

**12.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '36,41p'` (6 строк, целиком)
```
Scene onGameScreen(Scene value, bool hovering)
{
    value.gameScreen = true;
    value.hover = hovering;
    return value;
}
```
Вызовов `UiAuditAccess` в диапазоне нет (поле «вызовы UiAuditAccess: —» совпадает). Поля «имя» и «поиск в PORT» отсутствуют в таблице по значению «—», проверок не требуется.

**Итог: совпало.**

---

## Факт 13

Таблица: `scene-functions.tsv`, строка файла 32. Функция `readyCredits<int Frame>`, ссылка `src/debug/UiAuditScenes.cpp@9208dcf:292-304`.

**13.1** `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '292,304p'` (13 строк; показаны первые 12)
```
template <int Frame>
bool readyCredits(cGame &game)
{
    if (g_step == 0) {
        if (!UiAuditAccess::creditsScroll(game, Frame)) {
            return false;
        }
        g_step = 1;
        g_wait = 0;
        return false;
    }
```
(строка 304 — `}`, не выводится в запись; сверена при проверке.)

Вызов `UiAuditAccess::creditsScroll` — строка 296, как и указано в поле «вызовы UiAuditAccess: creditsScroll». Заголовок функции — с `template <int Frame>` на 292 и сигнатурой на 293.

**Итог: совпало.**

---

## Факт 14

Таблица: `runtime.tsv`, строка файла 19. Функция `cSDLSystem::adaptResolution`, ссылка `src/game/cSDLSystem.cpp@4aa980e:199`.

**14.1** `git show 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/game/cSDLSystem.cpp | sed -n '199p'`
```
    Logger::info(COMP_SDL2, "Resolution", "Desired : {}x{}", desiredWidth, desiredHeight);
```
**14.2** `... cSDLSystem.cpp | sed -n '197,230p'` (диапазон 197-230, 34 строки; показаны первые 12)
```
void cSDLSystem::adaptResolution(int desiredWidth, int desiredHeight, bool windowed)
{
    Logger::info(COMP_SDL2, "Resolution", "Desired : {}x{}", desiredWidth, desiredHeight);
    if (desiredWidth<MIN_RENDER_WIDTH)
        desiredWidth = MIN_RENDER_WIDTH;
    if (desiredHeight<MIN_RENDER_HEIGHT)
        desiredHeight = MIN_RENDER_HEIGHT;

    int tmpWidth =  windowResolution.width * desiredHeight / windowResolution.height;
    if (tmpWidth > desiredWidth) {
        renderResolution.height = desiredHeight;
        renderResolution.width = tmpWidth;
```
(строки 210-230 не выводятся в запись; сверены при проверке; 230 — `}`.)

**Итог: совпало.** Строка 199 содержит `Desired : {}x{}`, функция начинается на 197.

---

## Факт 15

Таблица: `runtime.tsv`, строка файла 11. Вызов из `main.cpp`, ссылка `src/main.cpp@4aa980e:119`.

**15.1** `git show 4aa980e36ee7a8ff0e651ce10c4f55869d86f08d:src/main.cpp | sed -n '119p'`
```
                if (!Preferences::save(*prefsFile, game.currentSettings(), prefsError)) {
```
**Итог: совпало.** Текст строки совпадает с фактом (с точностью до отступа).

---

Итог: 13 из 15 совпало.
Не совпали: факт 1 (строка 793 без `HUMAN`, первое вхождение — 794), факт 5 (строка 769 — `LIST_FOOT_UNITS`, `LIST_UNITS` — на 770).
