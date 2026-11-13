# Сверка пунктов 1–4

Ревизия для всех команд: `af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf`.

## Пункт 1 — ключи режима

### Строка grep 1

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp:23:        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp | nl -ba | sed -n '23p'
```

Полный вывод:

```text
    23	        if (std::strcmp(argv[i], "--ui-audit-list") == 0) {
```

### Строка grep 2

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp:26:        else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp | nl -ba | sed -n '26p'
```

Полный вывод:

```text
    26	        else if (std::strcmp(argv[i], "--ui-audit-scales") == 0 && i + 1 < argc) {
```

### Строка grep 3

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp:29:        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp | nl -ba | sed -n '29p'
```

Полный вывод:

```text
    29	        else if (std::strcmp(argv[i], "--ui-audit-scene") == 0 && i + 1 < argc) {
```

### Функция consumeArguments

Выбранный текст: `.tmp/p5g5/1.md`, строки 18–44; `B = 44`.

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/debug/UiAuditArguments.cpp | nl -ba | sed -n '44,47p'
```

Полный вывод:

```text
    44	}
    45	
    46	}
```

Итог: **совпало** — строка 44 закрывает тело `consumeArguments`.

## Пункт 2 — вызовы режима из игры

### Строка grep 1

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp:628:            uiaudit::beginFrame(*this);
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '628p'
```

Полный вывод:

```text
   628	            uiaudit::beginFrame(*this);
```

### Строка grep 2

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp:638:            uiaudit::onFramePresented(*this);
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '638p'
```

Полный вывод:

```text
   638	            uiaudit::onFramePresented(*this);
```

### Строка grep 3

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/main.cpp:124:                uiaudit::onSetupDone(game);
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/main.cpp | nl -ba | sed -n '124p'
```

Полный вывод:

```text
   124	                uiaudit::onSetupDone(game);
```

### Функция cGame::run

Выбранный текст: `.tmp/p5g5/2.md`, строки 571–643; `B = 643`.

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cGame_logic.cpp | nl -ba | sed -n '643,646p'
```

Полный вывод:

```text
   643	}
   644	
   645	void cGame::ensureFrameTargets()
   646	{
```

Итог: **совпало** — строка 643 закрывает тело `cGame::run`.

## Пункт 3 — таймеры и ожидание кадров

### Строка grep 1

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cSDLSystem.cpp:326:    SDL_SetRenderVSync(renderer, 1);
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cSDLSystem.cpp | nl -ba | sed -n '326p'
```

Полный вывод:

```text
   326	    SDL_SetRenderVSync(renderer, 1);
```

### Строка grep 2

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cTimeManager.cpp:237:        SDL_Delay(m_waitingTime);
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cTimeManager.cpp | nl -ba | sed -n '237p'
```

Полный вывод:

```text
   237	        SDL_Delay(m_waitingTime);
```

### Строка grep 3

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cTimeManager.cpp:200:    Uint64 now = SDL_GetTicks();
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cTimeManager.cpp | nl -ba | sed -n '200p'
```

Полный вывод:

```text
   200	    Uint64 now = SDL_GetTicks();
```

### Функция cTimeManager::waitForCPU

Выбранный текст: `.tmp/p5g5/3.md`, строки 234–240; `B = 240`.

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:src/game/cTimeManager.cpp | nl -ba | sed -n '240,243p'
```

Полный вывод:

```text
   240	}
   241	
   242	void cTimeManager::capFps()
   243	{
```

Итог: **совпало** — строка 240 закрывает тело `cTimeManager::waitForCPU`.

## Пункт 4 — ключи формата геометрии

### Строка grep 1

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tests/ui_audit/ui_audit_main_menu_png.py:12:    "k": "header",
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tests/ui_audit/ui_audit_main_menu_png.py | nl -ba | sed -n '12p'
```

Полный вывод:

```text
    12	    "k": "header",
```

### Строка grep 2

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tools/ui-audit/check_geometry.py:163:    if not lines or lines[0].get("k") != "header":
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tools/ui-audit/check_geometry.py | nl -ba | sed -n '163p'
```

Полный вывод:

```text
   163	    if not lines or lines[0].get("k") != "header":
```

### Строка grep 3

Вывод из полного результата `git grep`:

```text
af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tools/ui-audit/check_scenes.py:69:    viewport = header.get("map_viewport")
```

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tools/ui-audit/check_scenes.py | nl -ba | sed -n '69p'
```

Полный вывод:

```text
    69	    viewport = header.get("map_viewport")
```

### Функция check_structures

Выбранный текст: `.tmp/p5g5/4.md`, строки 76–87; `B = 87`.

Команда сверки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show af6a2e1e4f2baba4ff52e4812c7dc798cfd46aaf:tools/ui-audit/check_scenes.py | nl -ba | sed -n '87,90p'
```

Полный вывод:

```text
    87	    return None
    88	
    89	
    90	def check_scene(header, records):
```

Итог: **не совпало** — в пункте 4 выбран текст Python-функции, у которой нет закрывающей фигурной скобки; строка 87 содержит `return None`, а завершение функции обозначено отступом.

Итог по PLAN-P5G5-delta-1: совпало — строка 90 начинается без отступа.
