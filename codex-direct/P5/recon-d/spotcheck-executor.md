# Выборочная сверка таблиц

## Таблицы `api.tsv` и `entry.tsv` — 4 факта

1. `api.tsv`: строка `recordText` указывает объявление `void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);` в `src/debug/UiAudit.hpp@9208dcf:47`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAudit.hpp | sed -n '47p'
   ```
   Вывод:
   ```text
   void recordText(const std::string &text, int x, int y, int w, int h, const Rect *box = nullptr);
   ```
   Вердикт: совпало.

2. `api.tsv`: строка `consumeArguments` указывает объявление `void consumeArguments(int &argc, char **argv);` в `src/debug/UiAuditArguments.hpp@9208dcf:16`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.hpp | sed -n '16p'
   ```
   Вывод:
   ```text
   void consumeArguments(int &argc, char **argv);
   ```
   Вердикт: совпало.

3. `api.tsv`: строка `recordArea` указывает определение в `src/debug/UiAuditCapture.cpp@9208dcf:306`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '306p'
   ```
   Вывод:
   ```text
   void recordArea(const char *name, int x, int y, int w, int h)
   ```
   Вердикт: совпало.

4. `entry.tsv`: строка `PORT / файл разбора аргументов` указывает начало `cHandleArgument::handleArguments` в `src/utils/cHandleArgument.cpp@7eb119b:45`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/utils/cHandleArgument.cpp | sed -n '45p'
   ```
   Вывод:
   ```text
   int cHandleArgument::handleArguments(int argc, char *argv[], InitialGameSettings *settings)
   ```
   Вердикт: совпало.

## Таблица `hooks.tsv` — 4 факта

5. Строка `src/cGame_logic.cpp@9208dcf:772` указывает вызов `uiaudit::beginFrame(*this)` в `cGame::run`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | sed -n '772p'
   ```
   Вывод:
   ```text
               uiaudit::beginFrame(*this);
   ```
   Вердикт: совпало.

6. Строка `src/drawers/cMiniMapDrawer.cpp@9208dcf:73` указывает функцию `cMiniMapDrawer::draw`; поле PORT в этой строке таблицы задаёт её место в `src/drawers/cMiniMapDrawer.cpp@7eb119b:108-133`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/drawers/cMiniMapDrawer.cpp | sed -n '108p'
   ```
   Вывод:
   ```text
   void cMiniMapDrawer::draw()
   ```
   Вердикт: совпало.

7. Строка `src/drawers/cSideBarDrawer.cpp@9208dcf:70` указывает вызов `UiAuditAccess::recordSidebarClicks(*this)` в `cSideBarDrawer::draw`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cSideBarDrawer.cpp | sed -n '70p'
   ```
   Вывод:
   ```text
           UiAuditAccess::recordSidebarClicks(*this);
   ```
   Вердикт: совпало.

8. Строка `src/drawers/cCommandBarDrawer.cpp@9208dcf:101` указывает вызов `uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight())` в `cCommandBarDrawer::draw`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/cCommandBarDrawer.cpp | sed -n '101p'
   ```
   Вывод:
   ```text
           uiaudit::recordArea("command-bar", m_panelRect.getX(), m_panelRect.getY(), m_panelRect.getWidth(), m_panelRect.getHeight());
   ```
   Вердикт: совпало.

## Таблицы `scenes.tsv` и `tools.tsv` — 4 факта

9. `scenes.tsv`: строка сцены `main-menu` указывает запись сцены в `src/debug/UiAuditScenes.cpp@9208dcf:363`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '363p'
   ```
   Вывод:
   ```text
       scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
   ```
   Вердикт: совпало.

10. `scenes.tsv`: строка `region-atreides-intro-1` указывает наличие класса `cSelectYourNextConquestState` в PORT, `src/gamestates/cSelectYourNextConquestState.h@7eb119b:77`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:src/gamestates/cSelectYourNextConquestState.h | sed -n '77p'
   ```
   Вывод:
   ```text
   class cSelectYourNextConquestState : public cGameState {
   ```
   Вердикт: совпало.

11. `tools.tsv`: строка `tools/ui-audit/check_options_geometry.py@9208dcf:1` указывает первую строку `#!/usr/bin/env python3`.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_options_geometry.py | sed -n '1p'
   ```
   Вывод:
   ```text
   #!/usr/bin/env python3
   ```
   Вердикт: совпало.

12. `tools.tsv`: строка `tools/ui-audit/check_geometry.py@9208dcf:1` указывает чтение файла в строке 162.

   Команда:
   ```sh
   export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/ui-audit/check_geometry.py | sed -n '162p'
   ```
   Вывод:
   ```text
       lines = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
   ```
   Вердикт: совпало.
