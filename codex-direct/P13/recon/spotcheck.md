# Сверка фактов помощников 1 и 2

## Помощник 1: четыре факта из `scenes.tsv` и `screens.tsv`

1. Факт из `scenes.tsv`: регистрация сцены `FORK1 main-menu`, `src/debug/UiAuditScenes.cpp@9208dcf:363`.

   Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '363p'`

   Вывод:

   ```text
       scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
   ```

   Итог: совпало.

2. Факт из `scenes.tsv`: регистрация сцены `FORK1 options-menu-main`, `src/debug/UiAuditScenes.cpp@9208dcf:469`.

   Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditScenes.cpp | sed -n '469p'`

   Вывод:

   ```text
       scene("options-menu-main", "options-menu", "", "FixedFrames(14, no readiness flag)", prepareOptionsMenu<0>,
   ```

   Итог: совпало.

3. Факт из `scenes.tsv`: регистрация сцены `PORT main-menu`, `src/debug/UiAuditScenes.cpp@010a6eb:378`.

   Команда: `git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '378p'`

   Вывод:

   ```text
       scene("main-menu", "main-menu", "", "StateSettled", prepareMainMenu),
   ```

   Итог: совпало.

4. Факт из `scenes.tsv`: регистрация сцены `PORT credits-title`, `src/debug/UiAuditScenes.cpp@010a6eb:481`.

   Команда: `git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditScenes.cpp | sed -n '481p'`

   Вывод:

   ```text
       scene("credits-title", "credits", "", "CreditsScrollPosition", prepareCredits, readyCredits<0>),
   ```

   Итог: совпало.

## Помощник 2: четыре факта из `screen-size.tsv` и `output.tsv`

5. Факт из `screen-size.tsv`: значение `-screenWidth` записывается в `settings->screenW`, `src/utils/cHandleArgument.cpp@9208dcf:86`.

   Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/utils/cHandleArgument.cpp | sed -n '86p'`

   Вывод:

   ```text
                       settings->screenW = std::stoi(argv[i]);
   ```

   Итог: совпало.

6. Факт из `screen-size.tsv`: окно SDL создаётся с `renderResolution.width` и `renderResolution.height`, `src/game/cSDLSystem.cpp@010a6eb:306`.

   Команда: `git show 010a6eb134661660a077279bb94a36f063b97d7a:src/game/cSDLSystem.cpp | sed -n '306p'`

   Вывод:

   ```text
       window = SDL_CreateWindow(title.c_str(), renderResolution.width, renderResolution.height, 0);
   ```

   Итог: совпало.

7. Факт из `output.tsv`: PNG сохраняется вызовом `IMG_SavePNG`, `src/debug/UiAuditCapture.cpp@9208dcf:227`.

   Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '227p'`

   Вывод:

   ```text
               ok = IMG_SavePNG(surface, path.string().c_str()) == 0;
   ```

   Итог: совпало.

8. Факт из `output.tsv`: первая запись geometry JSONL является заголовком с именем сцены и разрешением, `src/debug/UiAuditCapture.cpp@010a6eb:175`.

   Команда: `git show 010a6eb134661660a077279bb94a36f063b97d7a:src/debug/UiAuditCapture.cpp | sed -n '175p'`

   Вывод:

   ```text
       file << "{\"k\":\"header\",\"scene\":\"" << escapeJson(g_scene->id) << "\",\"resolution\":\"" << outputW << 'x'
   ```

   Итог: совпало.
