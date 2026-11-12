## A-P10A-02 — ответ на Q-P10A-02

Да. В конструкторе `cCommandBarDrawer` (пункт 7.3 контракта) строка `    rebuildLayout();` заменяется строкой:

```cpp
    m_panelRect = CommandBarLayout::create(m_settings->getScreenW(), m_settings->getScreenH(), cSideBar::SidebarWidth).panel;
```

Других правок пункта 7.3 нет. `rebuildLayout()` остаётся в `draw()` и `onNotifyMouseEvent()`, как в форке; `isMouseOver` работает по `m_panelRect` с первого кадра. Причина: панель создаётся в `cDrawManager::reset` раньше `serviceInit` игроков, и `getSelectedUnits()` в конструкторе обращается к ещё не заданному `cPlayer::m_objects`.

Продолжай с проверки 1 раздела «Проверки» (сборка заново) и дальше по порядку до сдачи `## DONE-P10A`. Запись «Решено исполнителем» об этой замене не нужна: она — ответ ведущего.
