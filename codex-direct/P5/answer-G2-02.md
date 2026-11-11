## PLAN-P5G2-delta — падение экрана настройки схватки

Сдача `DONE-P5G2` принята в части шагов 1–11. Повторный прогон ведущего нашёл падение игры: сцены `skirmish-setup-random` и `skirmish-setup-ready-map` при прямом запуске завершаются сигналом SIGSEGV (код 139) в 27 запусках из 27; у помощника D они прошли случайно.

Причина — ошибка игры, а не режима отладки. `cGame::setupGame` сначала вызывает `init()`, где карта получает указатель на правила местности (`map->setTerrainInfo(m_infoContext->getTerrainInfo())`, `src/game/cGame_logic.cpp@91416fb:383`); затем `infoCreator.installInfos(*m_infoContext)` (строка 856) заменяет правила местности новым объектом, и старый освобождается. Экран настройки схватки в конструкторе строит случайную карту, `cMap` берёт пределы пряности через освобождённый указатель (`RNG::genInt(m_terrainInfo->terrainSpiceMinSpice, m_terrainInfo->terrainSpiceMaxSpice)`, `src/gameobjects/map/cMap.cpp@91416fb:1088`), получает минимум больше максимума, и `std::uniform_int_distribution` уходит в бесконечную рекурсию. Указатель обновляет только `cGame::missionInit` — уже после экрана схватки.

**Шаг 12 (помощник B).** В `src/game/cGame_logic.cpp`, в `cGame::setupGame`, сразу после строки `    infoCreator.installInfos(*m_infoContext);` — ровно две строки:

```cpp
    // installInfos replaced the terrain info that init() handed to the map.
    m_gameObjectsContext->getMap()->setTerrainInfo(m_infoContext->getTerrainInfo());
```

Рамка правок расширяется только этим файлом и этими двумя строками.

**Шаг 13 (помощник D).** Сначала, до шага 12, красная проверка 8 на установленной игре текущей сборки, затем после шага 12 — сборка (проверка 2) и проверки 1–8 по порядку. Проверка 8, из корня рабочей копии; перед командой — `L=check-08-red.log` для красной проверки и `L=check-08-green.log` для зелёной:

```bash
R=$PWD/.tmp/p5g2; (cd .tmp/out/run/bin && for s in skirmish-setup-random skirmish-setup-ready-map; do for i in $(seq 1 20); do rm -rf $R/rep-xdg $R/rep-out; mkdir -p $R/rep-xdg $R/rep-out; LD_LIBRARY_PATH=/srv/dune/worktrees/u34/.tmp/deps/prefix/lib SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=$R/rep-xdg timeout 120 ./d2tm -windowed -screenWidth 1024 -screenHeight 768 --ui-audit-scene $s --ui-audit-out $R/rep-out > /dev/null 2>&1; echo "$s $i exit=$?"; done; done) > $R/$L 2>&1; grep -c 'exit=0' $R/$L
```

Ожидается: красная (до шага 12) — число меньше 40; зелёная (после шага 12 и сборки) — ровно `40`. После проверки 8 — `rm -r .tmp/p5g2/rep-xdg .tmp/p5g2/rep-out`.

**Сдача.** Новый блок `## DONE-P5G2 | <время UTC из date -u> | HEAD <sha>`: вывод красной проверки 8, сборки и проверок 1–8 после шага 12 (по разделу «Сдача» задания), `git diff -- src/game/cGame_logic.cpp`; список коммитов — второй пункт: файл `src/game/cGame_logic.cpp`, сообщение на английском о том, что карта получает правила местности, установленные при запуске, до экрана настройки схватки, последняя строка — `Behavior changes: …`. Первый пункт (файлы шагов 1–10) ведущий уже закоммитил: `389f01e1`.

Механику — правку, сборку, проверки — делают только помощники. Не отступай от плана, не переусложняй.
