## Доработка P4 — находки ревью

Ревью нашло два дефекта сдачи `DONE-P4` (коммиты ведущего `f3b41e2f` и `87efa64f`, `HEAD` — `87efa64f2035dcf84f62aaf59f605f5e4ca8796a`). Исправь их правками 1–4 ниже, дословно; план не нужен. Затем выполни проверки 1–5 раздела «Проверки» задания и сдай `## DONE-P4`. Остальные правила задания и `PLAN-OK-P4` действуют. Журнал хода — дописывай в `.tmp/p4/progress.md`, строка на законченную правку.

### Дефект 0 — висячий указатель на фон

`cGame::ensureFrameTargets()` при смене плотности удаляет `screenTexture`. `cOptionsState` и `cWinLoseState` при создании копируют указатель `services->screenTexture` в поле и рисуют копию. Клавиши `TOGGLE_FULLSCREEN` и `TOGGLE_SCALING_MODE` меняют плотность, пока эти состояния открыты, и копия указывает на удалённую текстуру.

1. **`src/gamestates/cOptionsState.h` и `src/gamestates/cOptionsState.cpp`.**
   - `cOptionsState.h:61`: `Texture *m_backgroundTexture = nullptr;` → `Texture *const *m_backgroundTexture = nullptr;`.
   - `cOptionsState.cpp:54`: `m_backgroundTexture = services->screenTexture;` → `m_backgroundTexture = &services->screenTexture;`.
   - `cOptionsState.cpp:341–343`, в `draw()`: условие `if (m_backgroundTexture) {` → `if (m_backgroundTexture && *m_backgroundTexture) {`, вызов `m_sdlDrawer->renderSprite(m_backgroundTexture,0,0);` → `m_sdlDrawer->renderSprite(*m_backgroundTexture,0,0);`.
   - `cOptionsState.cpp:378` (`m_backgroundTexture = nullptr;`) не меняется.
2. **`src/gamestates/cWinLoseState.h` и `src/gamestates/cWinLoseState.cpp`.**
   - `cWinLoseState.h:50`: `Texture *m_backgroundTexture = nullptr;` → `Texture *const *m_backgroundTexture = nullptr;`.
   - `cWinLoseState.cpp:53`: `m_backgroundTexture = services->screenTexture;` → `m_backgroundTexture = &services->screenTexture;`.
   - `cWinLoseState.cpp:72–73`, в `draw()`: условие `if (m_backgroundTexture)` → `if (m_backgroundTexture && *m_backgroundTexture)`, вызов `m_sdlDrawer->renderSprite(m_backgroundTexture,0,0);` → `m_sdlDrawer->renderSprite(*m_backgroundTexture,0,0);`.
3. **`src/game/cGame_logic.cpp`, `cGame::ensureFrameTargets()`.** Снимок кадра в `screenTexture` сохраняется при смене плотности: меню настроек и экран победы показывают тот же фон, а затемнение — тот же кадр. Тело функции после строки `if (actualRenderer != nullptr && actualRenderer->density == density) { return; }` заменяется на:

   ```cpp
   Texture *previousScreenTexture = screenTexture;
   delete actualRenderer;

   actualRenderer = m_sdlDrawer->createRenderTargetTexture(m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);
   screenTexture = m_sdlDrawer->createRenderTargetTexture(m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);
   if (previousScreenTexture != nullptr) {
       m_sdlDrawer->beginDrawingToTexture(screenTexture);
       m_sdlDrawer->renderClearToColor();
       m_sdlDrawer->renderSprite(previousScreenTexture, 0, 0);
       m_sdlDrawer->endDrawingToTexture();
       delete previousScreenTexture;
   }
   m_services->screenTexture = screenTexture;

   Logger::info(COMP_SDL2, "frame", "Frame targets {}x{} at density {}", m_gameSettings->m_screenW, m_gameSettings->m_screenH, density);
   ```

   Строки до проверки плотности (`const int density = m_Screen->frameDensity();` и `m_sdlDrawer->setFrameDensity(density);`) не меняются.

### Дефект 1 — панель не догоняет плотность кадра

Плотность `m_candiBarRenderer` сверяется только в `createPlayerCandyBar()`, а он вызывается при создании панели и при смене Дома. После повышения плотности кадра панель остаётся с прежней плотностью и теряет HD-детали.

4. **`src/drawers/cSideBarDrawer.cpp`, `cSideBarDrawer::drawCandybar()` (строка 232).** Первой строкой тела, перед `m_sdlDrawer->renderSprite(m_candiBarRenderer, …);`, вставь:

   ```cpp
   if (m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()) {
       createPlayerCandyBar();
   }
   ```

   Проверка в `createPlayerCandyBar()` (строки 113–116) остаётся.

### Проверки и сдача

- Перед сборкой — `df -m /srv`; при `Available` меньше 5000 — блок `## Q-P4-02` с выводом и стоп.
- Проверки 1–5 задания — как в задании, с одним дополнением к проверке 5: допустимые изменённые файлы — только `src/gamestates/cOptionsState.h`, `src/gamestates/cOptionsState.cpp`, `src/gamestates/cWinLoseState.h`, `src/gamestates/cWinLoseState.cpp`, `src/game/cGame_logic.cpp`, `src/drawers/cSideBarDrawer.cpp` и строки `__pycache__`.
- Дополнительный греп: `git grep -n "m_backgroundTexture = services->screenTexture" -- src` — пустой вывод, код выхода 1.
- В сдаче — один коммит: сообщение на английском о сохранении фона и плотности панели при смене плотности кадра, последняя строка `Behavior changes: …`, затем шесть файлов.
- Стоп только на `## DONE-P4` или `## Q-P4-NN`.
