# Сверка помощником 4

Для каждого из отчётов выбрано по четыре факта со ссылками на строки PORT. Команды выполнялись отдельно; вывод ниже приведён дословно.

## Факты из `headers.md`

### 1. `src/context/AudioContext.hpp@acddd29:42`

Факт: объявлена функция `playMusicByType` с четырьмя параметрами.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/AudioContext.hpp | sed -n '42p'
```

Дословный вывод:

```text
    bool playMusicByType(eMusicType iType, bool triggerWithVoice, bool isCurrentlyPlayingMission, int humanHouse);
```

Итог: **совпало**.

### 2. `src/context/ContextCreator.hpp@acddd29:36`

Факт: объявлен метод `createGraphicsContext`, возвращающий `std::unique_ptr<GraphicsContext>`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/context/ContextCreator.hpp | sed -n '36p'
```

Дословный вывод:

```text
    std::unique_ptr<GraphicsContext> createGraphicsContext();
```

Итог: **совпало**.

### 3. `src/game/cGame.h@acddd29:141`

Факт: объявлен метод `setNextStateToTransitionTo(int newState)`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame.h | sed -n '141p'
```

Дословный вывод:

```text
    void setNextStateToTransitionTo(int newState);
```

Итог: **совпало**.

### 4. `src/gameobjects/map/cMapCamera.h@acddd29:214`

Факт: объявлен метод `setViewportPosition(int x, int y)`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMapCamera.h | sed -n '214p'
```

Дословный вывод:

```text
    void setViewportPosition(int x, int y);
```

Итог: **совпало**.

## Факты из `functions.md`

### 5. `src/drawers/cStructureDrawer.cpp@acddd29:479`

Факт: `drawStructureHealthBar` сразу выходит, если индекс структуры вне допустимого диапазона.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cStructureDrawer.cpp | sed -n '479p'
```

Дословный вывод:

```text
    if (iStructure < 0 || iStructure >= MAX_STRUCTURES) return;
```

Итог: **совпало**.

### 6. `src/game/cGame_logic.cpp@acddd29:575`

Факт: цикл `cGame::run` продолжается, пока `m_playing` истинно.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '575p'
```

Дословный вывод:

```text
    while (m_gameSettings->m_playing) {
```

Итог: **совпало**.

### 7. `src/game/cGame_logic.cpp@acddd29:1710`

Факт: `takeBackGroundScreen` начинает рисование в текстуру `screenTexture`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1710p'
```

Дословный вывод:

```text
    m_sdlDrawer->beginDrawingToTexture(screenTexture);
```

Итог: **совпало**.

### 8. `src/managers/cDrawManager.cpp@acddd29:421`

Факт: `cDrawManager::missionInit` вызывает `setCredits` у `m_creditsDrawer`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | sed -n '421p'
```

Дословный вывод:

```text
    m_creditsDrawer->setCredits();
```

Итог: **совпало**.

## Факты из `names.tsv`

### 9. `src/gameobjects/map/cMap.h@acddd29:69`

Факт: строка `names.tsv` для `canDeployUnitTypeAtCell` указывает объявление в `src/gameobjects/map/cMap.h:69).

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/map/cMap.h | sed -n '69p'
```

Дословный вывод:

```text
    bool canDeployUnitTypeAtCell(int iCell, int iUnitType);
```

Итог: **совпало**.

### 10. `src/gameobjects/units/cUnit.h@acddd29:155`

Факт: строка `names.tsv` для `fExperience` указывает поле в `src/gameobjects/units/cUnit.h:155).

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/units/cUnit.h | sed -n '155p'
```

Дословный вывод:

```text
    float fExperience;	// experience gained by unit
```

Итог: **совпало**.

### 11. `src/gameobjects/players/cPlayer.h@acddd29:147`

Факт: строка `names.tsv` для `setHouse` указывает объявление метода в `src/gameobjects/players/cPlayer.h:147).

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gameobjects/players/cPlayer.h | sed -n '147p'
```

Дословный вывод:

```text
    void setHouse(int iHouse);
```

Итог: **совпало**.

### 12. `src/game/cNotificationArea.h@acddd29:31`

Факт: строка `names.tsv` для `addNotification` указывает объявление метода в `src/game/cNotificationArea.h:31).

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cNotificationArea.h | sed -n '31p'
```

Дословный вывод:

```text
    void addNotification(const std::string &msg, eNotificationType type);
```

Итог: **совпало**.

## Пункт 4

Для каждого факта команда `git show` выполнена отдельно после установки PATH. Проверенные номера строк взяты из `.tmp/p5g3r/drawers.md`.

### 1. `src/drawers/cUnitDrawer.cpp@acddd29:56`

Факт: вызов `healthBar` принимает ширину, текущие кредиты юнита и `max`, а результат записывается в `w`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/drawers/cUnitDrawer.cpp | sed -n '56p'
```

Дословный вывод:

```text
    int w = healthBar(width_x, m_unit.iCredits, max);
```

Итог: **совпало**.

### 2. `src/gamestates/cWinLoseState.cpp@acddd29:95`

Факт: HD-текстура исхода отрисовывается как растянутый спрайт в области `layout.image`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cWinLoseState.cpp | sed -n '95p'
```

Дословный вывод:

```text
        m_sdlDrawer->renderStrechFullSprite(m_hdOutcomeTexture, layout.image);
```

Итог: **совпало**.

### 3. `src/managers/cDrawManager.cpp@acddd29:146`

Факт: `drawCombatState` вызывает отрисовку полос здоровья построек.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/managers/cDrawManager.cpp | sed -n '146p'
```

Дословный вывод:

```text
    m_structureDrawer->drawStructuresHealthBars();
```

Итог: **совпало**.

### 4. `src/gamestates/cGamePlaying.cpp@acddd29:302`

Факт: `cGamePlaying::draw` вызывает `drawCombatState` у менеджера отрисовки.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cGamePlaying.cpp | sed -n '302p'
```

Дословный вывод:

```text
    m_drawManager->drawCombatState();
```

Итог: **совпало**.
