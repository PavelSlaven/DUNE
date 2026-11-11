# Карта экранов рассказа и итогов (только факты из кода)

Рабочая копия: `C:/Users/Slaven/Projects/DUNE/.claude/worktrees/ui-redesign-360d77` (ветка `claude/ui-redesign-360d77`).
Пути в тексте относительны к корню рабочей копии `W`. Все числа и формулы даны как в коде.
Размеры картинок: «пиксели файла» взяты из заголовков PNG/пакетов; «логические» = пиксели / 4 (см. §0.4).

Легенда: «не найдено» = поиск выполнен, соответствия нет; «не проверено» = выходит за рамки чтения или требует запуска.

---

## 0. Общие факты (касаются всех шести экранов)

### 0.1 Таймеры и тики
- `thinkFast` — тик 5 мс, `thinkNormal` — 100 мс; по комментарию `src/game/cTimeManager.cpp:156` и `:167`. Сам таймер не проверялся (не проверено).
- Все счётчики ментата (`TIMER_*`) считаются в тиках `thinkFast`: `src/gameobjects/mentat/AbstractMentat.cpp:121-166`.

### 0.2 Шрифты и текст
- Основной шрифт экранов: `getBeneTextDrawer()` = `benegess.fon`, размер 12 (`src/context/ContextCreator.cpp:86`, `:124`; имя файла `resources/bin/settings.ini:91`).
- Мелкий шрифт (только отчёт о миссии): `getSmallTextDrawer()` = `small.ttf`, размер 12 (`src/context/ContextCreator.cpp:94`, `:123`; имя файла `resources/bin/settings.ini:92`).
- Текст рисуется через `TTF_RenderText_Solid` (без сглаживания); тень — тот же текст чёрным (`src/drawers/cTextTextureCache.cpp:95-110`, чёрный вариант `:99`).
- `cTextDrawer::drawText(x, y, color, msg, applyShadow = true)` — тень по умолчанию включена, сдвиг `+1,+1` (`src/drawers/cTextDrawer.h:35-39`, `src/drawers/cTextDrawer.cpp:45-58`). Для `drawTextScaledCenteredInBox` сдвиг тени `+2,+2` (`cTextDrawer.cpp:133-135`), по умолчанию `applyShadow = true` (`cTextDrawer.h:57`).
- `getFontHeight()` = `TTF_GetFontHeight` (`cTextDrawer.cpp:210-213`); `getTextLength` = ширина строки через `TTF_GetStringSize` (`cTextDrawer.cpp:224-230`). В таблицах ниже `F` = `getFontHeight()` bene-шрифта, `Fs` = `getFontHeight()` small-шрифта. Конкретные значения в пикселях не измерены (не проверено).
- Переноса строк в коде нет: каждая строка рисуется одним вызовом `drawText`.

### 0.3 Мышь и клавиши
- `MOUSE_LEFT_BUTTON_PRESSED` — нажатие (`src/controls/cMouse.cpp:165`); `MOUSE_LEFT_BUTTON_CLICKED` — отпускание (`cMouse.cpp:174`); при двойном щелчке вместо CLICKED шлётся DOUBLE_CLICKED (`cMouse.cpp:170-175`).
- `GuiButton::onMouseLeftButtonClicked` срабатывает только если `m_focus` (установлен по `MOUSE_MOVED_TO`) и точка внутри rect (`src/gui/GuiButton.cpp:321-330`).
- Клавиши действий: `MENU_BACK = Escape`, `MENU_CONFIRM = Return`, `MENU_CANCEL = Backspace` (`src/controls/cKeyBindings.cpp:117-119`; `resources/bin/settings.ini:143-145`).

### 0.4 Текстуры, density, рисование
- HD-пакеты читаются с `kHd4AssetDensity = 4` (`src/utils/Graphics.hpp:64`); для UI — `loadHdUiTexture` с той же плотностью (`src/utils/HdUiTextureLoader.cpp:13-21`).
- `Texture::w = pixelW / density`, `h = pixelH / density` (`src/include/Texture.hpp:41-43`). Логический размер = пиксели / 4.
- `renderSprite(tex, x, y)` рисует тексту логический размер `w x h` без растяжки (`src/drawers/SDLDrawer.cpp:37-47`).
- `renderStrechFullSprite(tex, dest)` растягивает текстуру на `dest` (`src/drawers/SDLDrawer.cpp:93-100`).
- `renderRectFillColor` / `renderRectColor` — заливка и рамка (`src/drawers/SDLDrawer.hpp:39-45`).
- Холст: `m_settings->getScreenW()` x `getScreenH()` (`src/game/cGameSettings.h`). Масштаб окна/презентации — не проверено (`src/utils/RenderScale.hpp` не смотрел).

### 0.5 Жизненный цикл состояний
- При каждом `setState` старые состояния-экраны удаляются и создаются заново: `deleteOldState = newState not in {GAME_REGION, GAME_PLAYING, GAME_EDITOR, GAME_OPTIONS}` (`src/game/cGame_logic.cpp:988-991`), удаление `destroyState(targetCreatorState)` (`cGame_logic.cpp:1047-1049`). Значит, снимок статистики `cScoringState` и ментат каждый раз строятся заново.
- Соответствие состояний и классов: `src/gamestates/cCreatorState.cpp:95-142` (MENU, CREDITS `:101-103`, WINNING `:113-115`, LOSING `:117-119`, SCORING `:121-123`, BRIEFING `:125-128`, WINBRIEF `:130-133`, LOSEBRIEF `:135-138`, TELLHOUSE `:140-142`); VIDEO создаётся в `createVideoState` (`cCreatorState.cpp:81-83`).
- Числовые коды `GAME_*`: `src/include/eGameState.h:51-68` (BRIEFING=3, TELLHOUSE=10, WINNING=11, WINBRIEF=12, LOSEBRIEF=13, LOSING=14, CREDITS=17, SCORING=20, VIDEO=21).

### 0.6 Переходы без затухания и с затуханием
- `setNextState(state)` — без fade (`src/game/GameStateTransition.hpp:34-36`); `setNextStateWithFade(state)` — с fade (`:38-40`); `fadeOut()` — запускает затухание (`:42-44`).

### 0.7 Ресурсы (сводка по паку, проверено декодированием заголовков)
- `resources/bin/data/sdl_mentat_hd4.dat` — реальный пакет (32 817 129 байт, заголовок `D2TM`, 52 записи). Индексы совпадают с `src/include/gfxmentat.h:24-75`.
- `resources/bin/data/sdl_inter_hd4.dat` — реальный пакет (146 записей). Используются индексы 10, 17, 21, 22.
- `resources/bin/data/hd4/*.png` — реальные PNG (outcome, credits).
- `resources/bin/data/scenes/hd4/sdl_*.dat` — ВСЕ файлы в рабочей копии это git-LFS-указатели (132 байта: `version https://git-lfs.github.com/spec/v1`, `oid sha256:...`, `size N`). Реальные пакеты не загружены. Размеры N приведены в §1.3. Проверено: `resources/bin/data/scenes/hd4/sdl_win01.dat` — 132 байта, атрибут `filter: lfs` в `git check-attr`.
- `intro.pak` — в рабочей копии не найден (`Glob **/intro*.pak` — пусто).

---

## 1. Ментат (брифинг, советы, вопрос «да / нет», «повторить / продолжить»)

Файлы: `src/gamestates/cMentatState.{h,cpp}`, `src/gameobjects/mentat/{AbstractMentat,AtreidesMentat,HarkonnenMentat,OrdosMentat,SardaukarMentat,BeneMentat}.{h,cpp}`.

### 1.1 Режимы и выбор подкласса
- Режимы `enum class MentatMode { Briefing, WinBrief, LoseBrief }` — `src/gamestates/cMentatState.h:34-38`.
- Конструктор `cMentatState(...)` сразу вызывает `prepareMentat(m_house)` — `cMentatState.cpp:38-65`, вызов `:64`.
- `prepareMentat(int house)` — `cMentatState.cpp:75-137`:
  - `m_allowMissionSelect = !m_settings->isSkirmish()` (`:78`).
  - `house = (m_house > GENERALHOUSE) ? m_house : humanPlayer->getHouse()` (`:80`).
  - Выбор подкласса по `house`: ATREIDES → `AtreidesMentat`, HARKONNEN → `HarkonnenMentat`, ORDOS → `OrdosMentat`, SARDAUKAR → `SardaukarMentat`, иначе → `BeneMentat` (`:83-92` для Briefing; аналогично `:99-108` и `:117-126`).
  - Briefing: `m_missionFlow->init()` (`:93`), `m_scenarioFlow->setupPlayers()` (`:94`), `m_cIni->loadScenario(...)` (`:95`), `m_cIni->loadBriefing(house, region, BRIEFING, ...)` (`:96`).
  - WinBrief: сцена `RNG::rnd(100) < 50 ? "win01" : "win02"` (`:110-113`), текст секции WIN (`:114`).
  - LoseBrief: сцена `"lose01"` / `"lose02"` (`:128-131`), текст секции LOSE (`:133`).
  - Во всех режимах в конце `m_mentat->speak()` (`:136`).
- Вызовы: `cGame::prepareMentatForPlayer` (`src/game/cGame_logic.cpp:1239-1255`) переподготавливает `BRIEFING`/`WINBRIEF`/`LOSEBRIEF` с `m_dataCampaign->housePlayer`.
- `cMentatState::draw()` — `cMentatState.cpp:144-149`: `m_mouse->setTile(MOUSE_NORMAL)`, затем `m_mentat->draw()`, затем `m_mouse->draw()`.
- `thinkFast` → `m_mentat->think()` (`:139-142`); мышь → `m_mentat->onNotifyMouseEvent` (`:151-154`); клавиатура → `m_mentat->onNotifyKeyboardEvent` (`:156-159`).

### 1.2 Кадр ментата: геометрия и порядок
Константы (`src/gameobjects/mentat/AbstractMentat.cpp:40-43`):
- `MENTAT_SCREEN_W = 640`, `MENTAT_SCREEN_H = 480` (логический размер кадра, арт 640x480).
- Смещение кадра (`AbstractMentat.cpp:106-107`): `offsetX = (W - 640) / 2`, `offsetY = (H - 480) / 2` (целое деление, без clamp, для W < 640 смещение отрицательное).
- Сцена-ролик: `movieTopleftX = offsetX + 256`, `movieTopleftY = offsetY + 120` (`:108-109`).

Порядок рисования `AbstractMentat::draw()` (`src/gameobjects/mentat/AbstractMentat.cpp:273-314`):
1. Очистка экрана `renderClearToColor(Color{7,7,15,255})` (`:275`).
2. Рамка: `renderRectColor(offX-1, offY-1, 641, 481, {64,64,89})` (`:276`); `(offX-2, offY-2, 642, 482, {40,40,60})` (`:277`); `(offX-3, offY-3, 643, 483, {0,0,0})` (`:278`).
3. Сцена-ролик `draw_movie()` (`:281`, тело `:322-331`): текстура `gfxmovie->getTexture(iMovieFrame)`, dest `{movieTopleftX, movieTopleftY, tmp->w, tmp->h}` (`:329`), `renderStrechFullSprite` (`:330`).
4. Фон: `getBackgroundBitmap()` (`:283`, тело `:316-320`, индекс `iBackgroundFrame`), растянут на dest `{offX, offY, 640, 480}` (`:284-285`).
5. Глаза `draw_eyes()` (`:287`), рот `draw_mouth()` (`:288`), `draw_other()` (`:289`; во всех подклассах пусто).
6. Если `state == SPEAKING` и `iMentatSentence >= 0`: две строки текста (см. §1.5) (`:291-300`).
7. Если `state == AWAITING_RESPONSE`: левая и правая кнопки (`:302-309`).
8. Кнопка «Mission select», если создана (`:311-313`), рисуется во всех состояниях.

Исходный размер и растяжка картинок (проверено по заголовкам PNG в `sdl_mentat_hd4.dat`):

| Картинка | Константа / имя записи | Пиксели | Логический размер | Как рисуется | Позиция |
|---|---|---|---|---|---|
| Фон Atreides | `MENTATA` (индекс 37, `gfxmentat.h:61`) | 2560x1920 | 640x480 | растянут на 640x480 | (offX, offY) |
| Фон Harkonnen | `MENTATH` (38, `gfxmentat.h:62`) | 2560x1920 | 640x480 | растянут | (offX, offY) |
| Фон Bene | `MENTATM` (39, `gfxmentat.h:63`) | 2560x1920 | 640x480 | растянут | (offX, offY) |
| Фон Ordos | `MENTATO` (40, `gfxmentat.h:64`) | 2560x1920 | 640x480 | растянут | (offX, offY) |
| Фон Sardaukar | `MENTATS` (51, `gfxmentat.h:75`) | 2560x1920 | 640x480 | растянут | (offX, offY) |
| Глаза (5 кадров) | `ATR_EYES01..05` (0-4), `HAR_EYES01..05` (24-28), `ORD_EYES01..05` (41-45), `BEN_EYES01..05` (10-14) | 384x128 | 96x32 | без растяжки, `renderSprite` | см. таблицу подклассов |
| Рот (5 кадров) | `ATR_MOUTH01..05` (5-9), `HAR_MOUTH01..05` (29-33), `ORD_MOUTH01..05` (46-50), `BEN_MOUTH01..05` (15-19) | 448x320 | 112x80 | без растяжки | см. таблицу подклассов |
| Кнопка «Repeat» | `BTN_REPEAT` (22) | 616x184 | 154x46 | `renderSprite` (WITH_TEXTURE) | rect |
| Кнопка «Yes» | `BTN_YES` (23) | 616x184 | 154x46 | `renderSprite` | rect |
| Кнопка «Proceed» | `BTN_PROCEED` (21) | 616x184 | 154x46 | только для размера rect | rect |
| Кнопка «No» | `BTN_NO` (20) | 616x184 | 154x46 | `renderSprite` | rect |
| Сцена-ролик | файл `data/scenes/hd4/sdl_<scene>.dat` (`src/utils/Graphics.hpp:66-69`, `AbstractMentat.cpp:350`) | кадры не измерены: пакет LFS-указатель | не измерено | кадр за кадром, `renderStrechFullSprite` с размером самого кадра (`tmp->w/h`) | (offX+256, offY+120) |

Прочие ресурсы:
- `HEN_HARKONNEN` (34, 732x108), `MEN_WISH` (35, 1680x168), `MENTAT` (36, PAL, 1280x960 с альфой) — в коде ментата не используются (поиск `\bMENTAT\b` вне `gfxmentat.h`: совпадений нет).

Прозрачность фона (проверено декодированием PNG из пакета, скрипт в scratchpad, только чтение):
- Фоны 37, 38, 39, 40, 51 полностью непрозрачны: в каждом 0 пикселей с alpha < 128 и 0 полупрозрачных.
- Средний цвет фона в области сцены `[256,120)-[640,480)` (логические, пиксели/4): Atreides (11,16,27), Harkonnen (36,16,16), Bene (9,8,13), Ordos (16,23,18), Sardaukar (30,15,39); доля «тёмных» пикселей (все каналы < 16): 10.8%, 34.3%, 73.3%, 50.1%, 32.8% соответственно.
- Вывод по коду: сцена рисуется ДО фона (`AbstractMentat.cpp:281` и `:285`), фон непрозрачен, значит кадр сцены перекрыт полностью. Видимость сцены на экране не проверена (нужен визуальный запуск с загруженными hd4-пакетами).

Масштаб: кадр строится в логических координатах, арт 640x480 и `renderStrechFullSprite` растягивает фон на 640x480; проверка масштаба презентации окна — не проверено.

### 1.3 Сцены (ролики), используемые ментатом
Имена сцен и размер пакета по LFS-указателю (байт):

| Сцена (BriefPicture / загрузка) | Файл | Размер по указателю, байт | Где задаётся |
|---|---|---|---|
| harvest | `sdl_harvest.dat` | 31 827 681 | `cIniUtils::sceneFileMap` `src/utils/cIniUtils.cpp:65` (`HARVEST.WSA`) |
| headqrts | `sdl_headqrts.dat` | 9 932 263 | `cIniUtils.cpp:71` |
| hvyftry | `sdl_hvyftry.dat` | 16 561 538 | `cIniUtils.cpp:70` |
| ix | `sdl_ix.dat` | 2 618 749 | `cIniUtils.cpp:66` |
| palace | `sdl_palace.dat` | 3 056 416 | `cIniUtils.cpp:68` |
| quad | `sdl_quad.dat` | 1 977 715 | `cIniUtils.cpp:72` |
| repair | `sdl_repair.dat` | 2 864 051 | `cIniUtils.cpp:69` |
| ltank | `sdl_ltank.dat` | 2 107 267 | `cIniUtils.cpp:73` |
| sardukar | `sdl_sardukar.dat` | 2 802 116 | `cIniUtils.cpp:67` (`SARDUKAR.WSA`) |
| platr (Atreides, описание дома) | `sdl_platr.dat` | 85 570 649 | `src/gamestates/cTellHouseState.cpp:73` |
| plhar (Harkonnen) | `sdl_plhar.dat` | 90 668 738 | `cTellHouseState.cpp:77` |
| plord (Ordos) | `sdl_plord.dat` | 101 484 814 | `cTellHouseState.cpp:81` |
| win01 / win02 | `sdl_win01.dat` 2 546 254; `sdl_win02.dat` 2 435 570 | | `cMentatState.cpp:111,113` |
| lose01 / lose02 | `sdl_lose01.dat` 2 576 412; `sdl_lose02.dat` 2 417 014 | | `cMentatState.cpp:129,131` |

Для брифинга сцена берётся из `BriefPicture=` в ini миссии: `cIni::populateScenario` → `if (data.briefScene) pMentat->loadScene(*data.briefScene)` (`src/utils/ini.cpp:134-137`); разбор `BriefPicture`: `src/utils/IniParsing.cpp:544-551`; если карта не нашла имя, сцены нет (`cIniUtils.cpp:194-195`, `unknown`).

Используемые в `resources/bin/campaign` и `resources/bin/skirmish` значения `BriefPicture` (счёт по grep): HARVEST 4, HEADQRTS 12, HVYFTRY 12, IX 12, LTANK 12, PALACE 8, QUAD 12, REPAIR 12, SARDUKAR 5.

### 1.4 Подклассы пяти ментатов

Общее (`src/gameobjects/mentat/AbstractMentat.h:44-127`): все подклассы вызывают базовый конструктор с `allowMissionSelect`; кнопки строятся через `buildLeftButton(bmp, x, y)` / `buildRightButton(bmp, x, y)` (`AbstractMentat.cpp:374-384`): rect = `{offX + x, offY + y, bmp->w, bmp->h}`.

| Подкласс | Фон (`iBackgroundFrame`) | Глаза: спрайт, позиция | Рот: спрайт, позиция | Левая кнопка (rect, текстура) | Правая кнопка (rect, текстура) | Действие левой | Действие правой | Файл:строки |
|---|---|---|---|---|---|---|---|---|
| Atreides | `MENTATA` | `ATR_EYES01+iMentatEyes` @ (80, 241) | `ATR_MOUTH01+iMentatMouth` @ (80, 273) | rect (293,423) размер BTN_REPEAT; текстура `BTN_REPEAT` | rect (466,423) размер BTN_PROCEED; текстура `BTN_YES` | `resetSpeak()` | `m_mentatFlow->leave()` | `AtreidesMentat.cpp:31-33, 36-54, 75, 80` |
| Harkonnen | `MENTATH` | `HAR_EYES01+iMentatEyes` @ (64, 256) | `HAR_MOUTH01+iMentatMouth` @ (64, 288) | то же | то же | `resetSpeak()` | `leave()` | `HarkonnenMentat.cpp:32-34, 35-53, 73, 78` |
| Ordos | `MENTATO` | `ORD_EYES01+iMentatEyes` @ (32, 240) | `ORD_MOUTH01+iMentatMouth` @ (31, 270) | то же | то же | `resetSpeak()` | `leave()` | `OrdosMentat.cpp:31-33, 34-52, 72, 77` |
| Sardaukar | `MENTATS` | не рисуются (закомментировано) `SardaukarMentat.cpp:73` | не рисуются (закомментировано) `:78` | то же | то же | `resetSpeak()` | `leave()` | `SardaukarMentat.cpp:32-34, 35-53` |
| Bene (BeneMentat) | `MENTATM` | `BEN_EYES01+iMentatEyes` @ (128, 240) | `BEN_MOUTH01+iMentatMouth` @ (112, 272) | rect (293,423) размер BTN_NO; текстура `BTN_NO`, подпись «No» | rect (466,423) размер BTN_YES; текстура `BTN_YES`, подпись «Yes» | `onNoButtonPressed()` | `onYesButtonPressed()` | `BeneMentat.cpp:39-41, 43-59, 108, 113` |

Примечания:
- Атрибут «Yes» у правой кнопки Atreides/Harkonnen/Ordos/Sardaukar: подпись `"Yes"`, текстура `BTN_YES`, размер rect от `BTN_PROCEED` (все три 616x184, отличий нет). Это факт кода, не ошибка размера.
- Подписи `withLabel(...)` («Repeat», «Yes», «No») в вид не выводятся: `WITH_TEXTURE` рисует только текстуру (`GuiButton.cpp:94-96`); подпись используется только в audit-записи (§1.9).
- Sardaukar: `loadScene` в `cTellHouseState` не вызывается и звук отключён (см. §2.2).

### 1.5 Текст: скорость, строки, пары
Данные: `cIni::loadBriefing` (`src/utils/ini.cpp:353-374`) очищает 10 строк, затем `setSentence(i, sentences[i])` для каждого элемента. Файлы: `resources/bin/campaign/briefings/mentata.ini`, `mentath.ini`, `mentato.ini`, `mentats.ini` (`src/utils/IniParsing.cpp:634-643`; `getBriefingFileName`). Для BENE имя пустое → файл `campaign/briefings/` не открывается (`ini.cpp:363-367`).
- Разбор: `parseBriefing` (`IniParsing.cpp:645-686`) берёт строки `Text="..."` из нужной секции (DESCRIPTION / BRIEFING / WIN / LOSE; `ScenarioIniWordType` `IniParsing.cpp:172-181`), не больше 10 (`:647`, `:681`).
- `setSentence(i, text)` обрезает текст до 254 символов: `AbstractMentat.cpp:340-344` (`text.substr(0, 254)`).
- Пары: строки выводятся парами `sentence[i]`, `sentence[i+1]` для `i = 0, 2, 4, 6, 8` (`AbstractMentat.cpp:134`: `iMentatSentence += 2`; последняя пара при `> 8` → `AWAITING_RESPONSE`, `:137-140`).
- Скорость: длительность пары `TIMER_Speaking = (len(s[i]) + len(s[i+1])) * 12` тиков (`AbstractMentat.cpp:143-152`); при 5 мс на тик — 60 мс на символ пары. Пример: пара 70 символов = 840 тиков = 4.2 с.
- Пустая пара (сумма длин < 2) сразу переводит в `AWAITING_RESPONSE` (`AbstractMentat.cpp:147-149`).
- Эффекта «печатания» по буквам нет: строки выводятся целиком (`:291-300`).
- Клик левой кнопкой в состоянии SPEAKING: если `TIMER_Speaking > 0`, ставится 1 — пара переключается на следующем тике (`AbstractMentat.cpp:411-415`).
- Позиции текста (`AbstractMentat.cpp:291-300`):
  - строка 1: `drawText(offX+17, offY+17, black, s[i])`, затем `drawText(offX+17, offY+17, white(255,255,255), s[i])`;
  - строка 2: `drawText(offX+17, offY+37, black, s[i+1])`, затем `drawText(offX+17, offY+36, white, s[i+1])`.
  - Каждый `drawText` дополнительно рисует тень `+1,+1` (см. §0.2).
- Переноса по ширине нет; обрезка по краю кадра/экрана в коде не реализована (не найдено; рисуется полная строка).
- В файлах текста есть подсказка о максимальной длине строки без точного числа (`mentata.ini:18-20`); код не проверяет длину строки относительно ширины кадра, кроме обрезки до 254 символов.

### 1.6 Мимика: глаза и рот
- Глаза (`AbstractMentat::thinkEyes`, `AbstractMentat.cpp:184-216`): таймер `TIMER_Eyes`; при истечении `rnd(100)`: `< 30` → кадр 3, `< 60` → кадр 0, иначе → 4; если совпало с предыдущим, кадр = `rnd(4)` (`:204-207`). Длительность: если кадр != 4 → `90 + rnd(160)` тиков; если кадр == 4 → 30 тиков (`:209-214`).
- Рот (`thinkMouth`, `AbstractMentat.cpp:218-271`): пока `TIMER_Speaking > 0` — кадры меняются `+ (1 + rnd(4))` по модулю 5; из закрытого состояния открывается с вероятностью 45%, иначе ждёт 25 тиков (`:229-237`); вне речи рот = 0 (`:262-264`). Таймер рта `13 + rnd(15)` тиков (`:267`).
- Моргание: `iMentatEyes` не меняется в `draw`, только в `think`.
- Фон и сцена: `thinkMovie` (`AbstractMentat.cpp:168-182`): `TIMER_movie` каждый тик +1; при `> 20` кадр +1, по достижении `getNumberOfFiles()` — возврат к 0. Т.е. ~21 тик (105 мс при 5 мс) на кадр сцены.

### 1.7 Кнопки: когда видны и что делают
- Левая/правая кнопки (Atreides..Sardaukar и Bene) рисуются только при `state == AWAITING_RESPONSE` (`AbstractMentat.cpp:302-309`).
- Кнопка «Mission select»: создаётся только если `canMissionSelect` (`AbstractMentat.cpp:80-102`). Для ментатов из `cMentatState` — `m_allowMissionSelect = !isSkirmish()`; для Bene и TellHouse — `false` (`BeneMentat.cpp:35`, `AbstractMentat(..., false)`).
  - Позиция: `x = settings.W - getTextLength("Mission select")`, `y = settings.H - getFontHeight()` (`AbstractMentat.cpp:82-85`).
  - Тип: `TRANSPARENT_WITHOUT_BORDER`, тема `cGuiThemeBuilder().light()`, подпись «Mission select» (`:87-93`).
  - Клик: `m_stateTransitions->setNextState(GAME_MISSIONSELECT)` — без fade (`:94-96`).
  - Рисуется в любом состоянии (`:311-313`), обрабатывает мышь в SPEAKING и AWAITING (`:407-428`).
- Repeat (`resetSpeak()` → `speak()`, `AbstractMentat.cpp:386-389`, `:366-372`): сбрасывает `TIMER_Speaking`, `iMentatSentence = -2`, состояние SPEAKING, т.е. текст повторяется с начала.

### 1.8 Вопрос «Do you wish to join house X ?» (только BeneMentat)
- `BeneMentat::draw()` (`src/gameobjects/mentat/BeneMentat.cpp:89-100`): после `AbstractMentat::draw()`; при `state == AWAITING_RESPONSE`:
  - `houseName = cPlayer::getHouseNameForId(house)` (`:95`);
  - `msg = std::format("Do you wish to join house {} ?", houseName)` (`:96`);
  - `drawText(offX+17, offY+17, Color{0,0,0,255}, msg)` (`:97`), затем `drawText(offX+16, offY+16, Color{255,214,137,255}, msg)` (`:98`).
- Имена домов (`src/gameobjects/players/cPlayer.cpp:822-...`): ATREIDES → "Atreides", HARKONNEN → "Harkonnen", ORDOS → "Ordos", SARDAUKAR → "Sardaukar", FREMEN → "Fremen", MERCENARY → "Mercenary", GENERALHOUSE → (см. ветку в `cPlayer.cpp` после строки 842; не открыто полностью).
- Дом: `BeneMentat::setHouse(house)` вызывается из `cTellHouseState::prepareMentat` (`src/gamestates/cTellHouseState.cpp:68`).
- Клавиатура Bene (`BeneMentat.cpp:116-125`, переопределяет базовый и НЕ вызывает базовый): `MENU_CONFIRM` (Return) → `onYesButtonPressed()`; `MENU_CANCEL` (Backspace) → `onNoButtonPressed()`.

### 1.9 Audit-записи (uiaudit) на ментате
- Явных вызовов `uiaudit::` в файлах ментата нет (поиск `uiaudit::` по `src/`: в `gameobjects/mentat` и `gamestates/cMentatState.cpp` совпадений нет).
- Косвенно: `GuiButton::draw` → `auditRecord("GuiButton")` и `auditClick("GuiButton:" + label)` (`src/gui/GuiButton.cpp:49-53`) → `GuiObject::auditRecord` / `auditClick` (`src/gui/GuiObject.cpp:35-43`: `uiaudit::recordGui(type, ...)`, `uiaudit::recordClick(name, ...)`).
  - Записи кликов для кнопок ментата: `GuiButton:Repeat`, `GuiButton:Yes`, `GuiButton:No`, `GuiButton:Mission select` (подписи из `withLabel`).
- Тексты: `cTextDrawer::drawText` → `uiaudit::recordText(msg, x, y, w, h)` (`src/drawers/cTextDrawer.cpp:51-52`). Все строки ментата записываются этим путём.

### 1.10 Элементы кадра ментата (таблица)

| Элемент | Вид | Текст (как в коде) | Геометрия (логика, холст W x H) | Шрифт | Цвета | Где |
|---|---|---|---|---|---|---|
| Очистка | `renderClearToColor` | — | весь холст | — | (7,7,15,255) | `AbstractMentat.cpp:275` |
| Рамка 1 | `renderRectColor` | — | (offX-1, offY-1, 641, 481) | — | (64,64,89,255) | `:276` |
| Рамка 2 | `renderRectColor` | — | (offX-2, offY-2, 642, 482) | — | (40,40,60,255) | `:277` |
| Рамка 3 | `renderRectColor` | — | (offX-3, offY-3, 643, 483) | — | (0,0,0,255) | `:278` |
| Сцена | `renderStrechFullSprite` | файл `sdl_<scene>` | (offX+256, offY+120), размер кадра | — | — | `:281`, `:329-330` |
| Фон | `renderStrechFullSprite` | `MENTATA/H/M/O/S` | (offX, offY, 640, 480) | — | — | `:283-285` |
| Глаза | `renderSprite` | `*_EYES0x` | (offX+80, offY+241) Atreides; и т.д. (§1.4) | — | — | `AtreidesMentat.cpp:75` и др. |
| Рот | `renderSprite` | `*_MOUTH0x` | (см. §1.4) | — | — | `:80` и др. |
| Строка 1 (чёрная) | `drawText` | строка `sentence[i]` | (offX+17, offY+17) | bene | black | `AbstractMentat.cpp:294` |
| Строка 1 (белая) | `drawText` | то же | (offX+17, offY+17) | bene | white | `:295` |
| Строка 2 (чёрная) | `drawText` | строка `sentence[i+1]` | (offX+17, offY+37) | bene | black | `:297` |
| Строка 2 (белая) | `drawText` | то же | (offX+17, offY+36) | bene | white | `:298` |
| Вопрос Bene | `drawText` x2 | `Do you wish to join house {} ?` | (offX+17, offY+17) чёрный; (offX+16, offY+16) | bene | (0,0,0); (255,214,137) | `BeneMentat.cpp:96-98` |
| Кнопка левая | `GuiButton` WITH_TEXTURE | «Repeat» / «No» (только audit) | rect (offX+293, offY+423, 154, 46) | — | текстура | `AtreidesMentat.cpp:32,36-43`; `BeneMentat.cpp:40,43-50` |
| Кнопка правая | `GuiButton` WITH_TEXTURE | «Yes» (только audit) | rect (offX+466, offY+423, 154, 46) | — | текстура | `AtreidesMentat.cpp:33,45-54`; `BeneMentat.cpp:41,52-59` |
| Mission select | `GuiButton` TRANSPARENT_WITHOUT_BORDER | «Mission select» | (W - L, H - F, L, F), L = getTextLength | bene | hover (255,0,0), иначе White (light-тема) | `AbstractMentat.cpp:82-102`, `:311-313` |

Текст «Mission select» в кнопке рисуется `drawTextScaledOpticallyCenteredInBox` с масштабом `fittedScale = clamp(min(1, (L-16)/L, (F-8)/F), 0.65, 1)` (`src/gui/GuiButton.cpp:199-219`; `m_textScale = 1.0F` по умолчанию, `GuiButton.h:79`). Т.е. `L` = ширина текста, `F` = высота шрифта.

### 1.11 Зоны нажатия вне виджетов (ментат)
- Не найдено: в `AbstractMentat::onNotifyMouseEvent` (`AbstractMentat.cpp:391-429`) и в `cMentatState::onNotifyMouseEvent` (`cMentatState.cpp:151-154`) кроме кнопок есть только клик левой в SPEAKING, который пропускает паузу (`:411-415`). Зона — весь экран, действие — пропуск паузы текущей пары.

### 1.12 Клавиши ментата
- Общая база (`AbstractMentat.cpp:431-436`): только пересылка в `m_guiBtnToMissionSelect->onNotifyKeyboardEvent` (обработка клавиш `GuiButton` не проверена).
- Атрейдес/Харконнен/Ордос/Сардаукар: нет собственной обработки (не найдено).
- Bene: `MENU_CONFIRM` → Yes, `MENU_CANCEL` → No (`BeneMentat.cpp:116-125`); база не вызывается.

### 1.13 Переходы ментата
- Briefing (BRIEFING), Atreides/Harkonnen/Ordos/Sardaukar, кнопка «Yes» → `m_mentatFlow->leave()` → `cGame::changeStateFromMentat` (`src/game/cGame_logic.cpp:1307-1321`): при `isState(GAME_BRIEFING)` → `setNextStateToTransitionTo(GAME_PLAYING)`, `drawManager->missionInit()`, мышь в центр, `initiateFadingOut()`, музыка PEACE.
- WinBrief, «Proceed» (правая) → `changeStateFromMentat` (`cGame_logic.cpp:1307-1373`):
  - SKIRMISH: если WINBRIEF или LOSEBRIEF → `GAME_SETUPSKIRMISH`, `missionInit()`, fade (`:1323-1334`).
  - Кампания, `isState(GAME_WINBRIEF)` и `m_dataCampaign->mission >= LAST_CAMPAIGN_MISSION` (=9, `src/include/sDataCampaign.h:18`) → `GAME_CREDITS`, fade (`:1340-1345`).
  - Кампания, WINBRIEF иначе → `GAME_REGION`, fade (`:1348-1353`).
- LoseBrief, «Proceed» → `changeStateFromMentat` (`:1356-1373`): `missionInit()`; если `mission > 1` → `GAME_REGION`, `mission--`; иначе → `GAME_BRIEFING` (`prepareMentatForPlayer`, музыка BRIEFING), fade.
- Bene (TELLHOUSE/Briefing через Bene): «Yes» → `onYesButtonPressed` (`BeneMentat.cpp:62-72`): `setNextState(GAME_BRIEFING)`, `mission = 1`, `region = 1`, `missionFlow->init()`, `m_humanPlayer->setHouse(house)`, `housePlayer = house`, `fadeOut()`.
- Bene: «No» → `onNoButtonPressed` (`:74-81`): `humanPlayer->setHouse(GENERALHOUSE)`, `housePlayer = GENERALHOUSE`, `setNextState(GAME_SELECT_HOUSE)`, `fadeOut()`.
- «Mission select» → `setNextState(GAME_MISSIONSELECT)` без fade (`AbstractMentat.cpp:94-96`).

### 1.14 Пороги раскладки (ментат)
- Порогов нет: единственная зависимость — центрирование `offsetX = (W-640)/2`, `offsetY = (H-480)/2` (`AbstractMentat.cpp:106-107`). При W < 640 или H < 480 смещение отрицательное, код не clamp-ит (не найдено ограничения).
- Mission select привязана к правому нижнему углу холста, не к кадру (`:82-85`).

### 1.15 Вызовы uiaudit (ментат)
- Явных `uiaudit::` в файлах ментата: не найдено (см. §1.9).
- Через `cTextDrawer::drawText` — `src/drawers/cTextDrawer.cpp:51-52` (`recordText`).
- Через `GuiButton::draw` — `src/gui/GuiButton.cpp:49-53` (`auditRecord("GuiButton")`, `auditClick("GuiButton:<label>")`).

---

## 2. Рассказ о Доме (`cTellHouseState`)

Файлы: `src/gamestates/cTellHouseState.{h,cpp}`. Использует `BeneMentat` (`cTellHouseState.cpp:17`, `:67`).

### 2.1 Инициализация и выбор текста/сцены
- Конструктор (`cTellHouseState.cpp:34-54`): `m_house = dataCampaign->housePlayer`, `prepareMentat(m_house)` (`:53`).
- `prepareMentat(house)` (`cTellHouseState.cpp:64-91`):
  - `m_mentat = std::make_unique<BeneMentat>(m_ctx, m_settings, m_stateTransitions, m_missionFlow, m_humanPlayer, m_dataCampaign)` (`:67`); `setHouse(house)` (`:68`).
  - ATREIDES: звук `SOUND_ATREIDES` (`:71`), `loadBriefing(ATREIDES, 0, DESCRIPTION)` (`:72`), сцена `"platr"` (`:73`).
  - HARKONNEN: звук `SOUND_HARKONNEN` (`:75`), `loadBriefing(HARKONNEN, 0, DESCRIPTION)` (`:76`), сцена `"plhar"` (`:77`).
  - ORDOS: звук `SOUND_ORDOS` (`:79`), `loadBriefing(ORDOS, 0, DESCRIPTION)` (`:80`), сцена `"plord"` (`:81`).
  - SARDAUKAR: звук закомментирован (`:83`), `loadBriefing(SARDAUKAR, 0, DESCRIPTION)` (`:84`), сцена закомментирована (`:85`) → без сцены.
  - Иначе: `Logger::warn` (`:87`) и `setSentence(0, "Looks like you choose an unknown house")` (`:88`).
  - `m_mentat->speak()` (`:90`).
- Текст: секция `[DESCRIPTION]` в `resources/bin/campaign/briefings/mentat{a,h,o,s}.ini` (`mentata.ini:32-40` — первая строка `"House Atreides"`, затем описание Caladan). Номер сценария = 0 (параметр `0`), парсер ищет `iScenario == 0` (DESCRIPTION идёт до первого `[SCEN]`, `mentata.ini:32`, `:46`).
- Сцена-ролик — ТОЙ ЖЕ геометрией, что у ментата (см. §1.2), но фон и глаза/рот — Bene (`BeneMentat`), т.е. `MENTATM`, `BEN_EYES`, `BEN_MOUTH`, не дома.

### 2.2 Порядок рисования
Тот же `AbstractMentat::draw` (§1.2): очистка, рамка, сцена `sdl_platr/plhar/plord` (для Sardaukar сцены нет), фон `MENTATM` (640x480), глаза Bene (128,240), рот Bene (112,272), текст (SPEAKING), вопрос Bene (AWAITING), кнопки Bene (AWAITING), «Mission select» — НЕ создаётся (`false`, `BeneMentat.cpp:35`).

Звук: `SOUND_ATREIDES` / `SOUND_HARKONNEN` / `SOUND_ORDOS` (`cTellHouseState.cpp:71,75,79`); для SARDAUKAR звука нет.

### 2.3 Элементы
Совпадают с ментатом Bene (§1.10), плюс: текст из `[DESCRIPTION]` (строки парами, §1.5). Вопрос «Do you wish to join house {} ?» и кнопки «No» (слева, `BTN_NO`) / «Yes» (справа, `BTN_YES`) появляются после речи (§1.8).

### 2.4 Зоны нажатия вне виджетов
- Не найдено (`cTellHouseState::onNotifyMouseEvent`, `cTellHouseState.cpp:105-108`, только пересылает в `m_mentat`).

### 2.5 Клавиши
- `cTellHouseState::onNotifyKeyboardEvent` (`:110-113`) пересылает в `m_mentat`, т.е. Bene: Return = Yes, Backspace = No (`BeneMentat.cpp:116-125`).

### 2.6 Переходы
- «Yes» (Bene) → `GAME_BRIEFING` (`BeneMentat.cpp:65`), `mission = 1`, `region = 1`, `missionFlow->init()`, `fadeOut()`.
- «No» (Bene) → `GAME_SELECT_HOUSE` (`BeneMentat.cpp:79`), `fadeOut()`.
- Вход в состояние: `cGame::prepareMentatToTellAboutHouse(house)` (`src/game/cGame_logic.cpp:1257-1285`) ← `MentatFlow::prepareToTellAboutHouse` ← выбор дома в `cChooseHouseState` (`src/gamestates/cChooseHouseState.cpp:249-258`):
  - `nextMission >= FIRST_MISSION+1` → `GAME_MISSIONSELECT` (`cGame_logic.cpp:1264-1267`);
  - `nextMission == FIRST_MISSION` → `mission = FIRST_MISSION`, `region = 1`, `GAME_BRIEFING` (`:1269-1274`);
  - иначе → `prepareMentat(house)` и `GAME_TELLHOUSE` (`:1277-1284`).
- `nextMission` берётся из `CampaignProgress::nextMission(house)` при `supportsHouse(house)` (`:1261-1263`).

### 2.7 Пороги раскладки
- Как у ментата (§1.14): порогов нет.

### 2.8 Вызовы uiaudit
- Явных `uiaudit::` нет; косвенно — см. §1.9, §1.15 (`cTextDrawer`, `GuiButton`).

---

## 3. Экран исхода миссии (победа / поражение) — `cWinLoseState`

Файлы: `src/gamestates/cWinLoseState.{h,cpp}`, `src/utils/OutcomeScreenLayout.hpp`.

### 3.1 Загрузка и выбор картинки
- `Outcome::Lose` → файл `outcome_defeat_en.png`; `Outcome::Win` → `outcome_victory_en.png` (`src/gamestates/cWinLoseState.cpp:57-59`). Суффикс `_en` жёстко задан; версии `_ru` в файлах есть (`resources/bin/data/hd4/outcome_*_ru.png`), в коде не используются.
- `loadHdUiTexture(renderer, file, label)` (`cWinLoseState.cpp:60-64`) → `data/hd4/<file>` (`HdUiTextureLoader.cpp:13`).
- Фон-резерв: `m_backgroundTexture = &services->screenTexture` (`:66`).
- Резерв картинок (если HD не загрузился): `gfxinter->getTexture(BMP_LOSING)` для Lose, `BMP_WINNING` для Win (`:68-72`).

### 3.2 Порядок рисования `draw()` (`cWinLoseState.cpp:84-114`)
1. Если `m_hdOutcomeTexture` есть (`:86`):
   - `prompt = "Click to continue"` (`:87`);
   - `layout = calculateOutcomeScreenLayout(W, H, pixelW, pixelH, getTextLength(prompt))` (`:88-94`);
   - `renderStrechFullSprite(m_hdOutcomeTexture, layout.image)` (`:95`);
   - `drawTextScaledCenteredInBox(prompt, layout.prompt, layout.promptTextScale, Color{255,224,164,255})` (`:96-100`).
2. Иначе резерв (`:103-111`): `renderSprite(screenTexture, 0, 0)` если есть (`:104-106`); `posW = (W - tex.w)/2`, `posH = (H - tex.h)/2` (`:108-109`); `renderSprite(m_tex, posW, posH)` (`:110`).
3. `m_mouse->draw()` (`:113`).

Исходные размеры (проверено по PNG):
- `outcome_defeat_en.png` — 2752 x 1536 px (файл 6 403 321 байт); логически в загрузчике 688 x 384 (`HdUiTextureLoader.cpp:21`), для раскладки используется `pixelW/pixelH` = 2752x1536.
- `outcome_victory_en.png` — 2752 x 1536 px (файл 7 431 127 байт).
- Резерв `BMP_LOSING` (индекс 10) и `BMP_WINNING` (17) в `sdl_inter_hd4.dat`: 1280x480 px → логически 320x120 (`gfxinter.h:34`, `:41`).
- Растяжка: до `layout.image` (см. §3.4), т.е. пропорции сохраняются через расчёт.

### 3.3 Элементы
| Элемент | Вид | Текст | Геометрия | Шрифт | Цвет | Где |
|---|---|---|---|---|---|---|
| Картинка исхода | `renderStrechFullSprite` | файл `outcome_*_en.png` | `layout.image` | — | — | `cWinLoseState.cpp:95` |
| Подсказка | `drawTextScaledCenteredInBox` (тень `+2,+2`) | `Click to continue` | `layout.prompt`, масштаб `layout.promptTextScale` | bene | (255,224,164) | `:96-100` |
| Резерв фон | `renderSprite` | — | (0,0) | — | — | `:104-106` |
| Резерв картинка | `renderSprite` | — | ((W-w)/2, (H-h)/2) | — | — | `:108-110` |

### 3.4 Раскладка (`src/utils/OutcomeScreenLayout.hpp:14-77`)
- `margin = max(12, min(W, H) / 32)` (`:26-29`).
- `availW = max(1, W - 2*margin)`, `availH = max(1, H - 2*margin)` (`:30-31`).
- `drawWidth = availW`, `drawHeight = availW * imageH / imageW` (целочисленно, int64) (`:33-36`). Если `drawHeight > availH`: `drawHeight = availH`, `drawWidth = availH * imageW / imageH` (`:37-42`). Далее `max(1, ...)` (`:43-44`).
- `image = {(W - drawWidth)/2, (H - drawHeight)/2, drawWidth, drawHeight}` (`:46-51`).
- Подсказка: `promptW = max(1, drawWidth/3)` (`:53`); `promptH = max(1, drawHeight*5/100)` (`:54`); `bottomInset = max(1, drawHeight*10/100)` (`:55`); `promptX = image.x + (drawWidth - promptW)/2` (`:56`); `promptY = image.endY - bottomInset - promptH` (`:57-62`).
- Масштаб текста: `basePromptScale = 50/18 ≈ 2.7778` (`:63`); `imageTextInset = 12` (`:64`); `availTextW = max(1, drawWidth - 24)` (`:65-68`); `promptTextScale = textW > 0 ? min(basePromptScale, availTextW / textW) : basePromptScale` (`:69-74`).
- Пример (W=800, H=600, исход 2752x1536): margin = max(12, 18) = 18; availW = 764, availH = 564; drawHeight = 764*1536/2752 = 426 (≤ 564), drawWidth = 764; image = (18, 87, 764, 426).

### 3.5 Зоны нажатия вне виджетов
- Всё окно: любой `MOUSE_LEFT_BUTTON_CLICKED` (`cWinLoseState.cpp:116-125`, `:136-145`).

### 3.6 Клавиши
- Не найдено: `onNotifyKeyboardEvent` пустой (`cWinLoseState.cpp:132-134`).

### 3.7 Переходы
- Lose (`cWinLoseState.cpp:138-139`): `m_missionFlow->goingToWinLoseBrief(GAME_LOSEBRIEF)` → `cGame::goingToWinLoseBrief` (`src/game/cGame_logic.cpp:1300-1305`): `setState(GAME_LOSEBRIEF)` + `prepareMentatForPlayer()`; затем `m_stateTransitions->fadeOut()` (`cWinLoseState.cpp:144`).
- Win (`:141`): `setNextState(GAME_SCORING)`; затем `fadeOut()` (`:144`).
- Вход: `setMissionWon()` (`cGame_logic.cpp:472-498`) → `setState(GAME_WINNING)` (`:480`), звук `SOUND_VOICE_07_ATR` (`:485`), музыка WIN (`:487`), `takeBackGroundScreen()` (`:497`). `setMissionLost()` (`:500-513`) → `GAME_LOSING` (`:503`), звук `SOUND_VOICE_08_ATR` (`:508`), музыка LOSE (`:510`).

### 3.8 Пороги раскладки
- Порог `margin`: `min(W,H)/32` с полом 12 (`OutcomeScreenLayout.hpp:26-29`).
- Выбор ширина/высота: если высота по ширине > доступной высоты — вписывание по высоте (`:37-42`).
- Масштаб подсказки ограничен сверху 50/18 и уменьшается, если текст шире `drawWidth-24` (`:63-74`).
- `drawTextScaledCenteredInBox` clamp масштаба снизу 0.5 (`cTextDrawer.cpp:122`).

### 3.9 Вызовы uiaudit
- Явных `uiaudit::` в `cWinLoseState` нет (поиск по `src/`).
- Косвенно: `cTextDrawer::drawTextScaledCenteredInBox` → `uiaudit::recordText(msg, x, y, w, h, &box)` (`src/drawers/cTextDrawer.cpp:129-131`).

---

## 4. Отчёт о миссии (очки, статистика) — `cScoringState`

Файлы: `src/gamestates/cScoringState.{h,cpp}`; сбор: `src/game/cMissionStatsCollector.{h,cpp}`, `src/game/MissionStats.h`.

### 4.1 Порядок рисования `draw()` (`src/gamestates/cScoringState.cpp:56-111`)
1. `renderClearToColor()` — чёрный фон, картинок нет (`:58`).
2. Заголовок `MISSION REPORT` (`:64`, Color::Yellow).
3. Время миссии (`:67-70`).
4. Блоки игроков по `playerId = 0..4` (`:73-107`), фильтр `playerId == HUMAN || house != GENERALHOUSE` (`:78-81`).
5. Подсказка `Click to continue` (`:109`).
6. Курсор `m_mouse->draw()` (`:110`).

### 4.2 Строки отчёта (как в коде)
| № | Строка | Функция / шрифт | Формула / источник | Где |
|---|---|---|---|---|
| 1 | `MISSION REPORT` | `drawTextCentered(msg, y, Color::Yellow)`, bene | `y = 40` | `cScoringState.cpp:62,64` |
| 2 | `Mission time: {:02}:{:02}` | bene, White | `minutes = elapsedSeconds / 60`, `seconds = elapsedSeconds % 60`; `elapsedSeconds` = `m_stats.elapsedSeconds` (из `cTimeManager::getElapsedSeconds()` при создании состояния, `cScoringState.cpp:39`) | `:67-69` |
| 3 | `YOU - {house}` или `ENEMY - {house}` | bene, цвет миникарты через `getColorFadeSelected(r,g,b)` | `label = (playerId == HUMAN) ? "YOU" : "ENEMY"`; `house = cPlayer::getHouseNameForId(playerStats.house)` | `:83-87` |
| 4 | `Units built: {}   lost: {}   destroyed: {}` | small, White | `unitsBuilt`, `unitsLost`, `unitsDestroyed` | `:90-92` |
| 5 | `Structures built: {}   lost: {}   destroyed: {}` | small, White | `structuresBuilt`, `structuresLost`, `structuresDestroyed` | `:95-97` |
| 6 | `Damage dealt: {}   received: {}` | small, White | `damageDealt`, `damageReceived` | `:100` |
| 7 | `Spice harvested: {}` | small, White | `spiceHarvested` | `:104` |
| 8 | `Click to continue` | bene, White, `y = H - lineHeight - 8` | `lineHeight = F + 4` | `:109` |

Игроки, которые не выводятся: `AI_CPU5` (Fremen) и `AI_WORM` исключены циклом `playerId < AI_WORM - 1` = `< 5` (`:72-73`); `AI_WORM = AI_CPU6 = 6` (`src/include/definitions.h:78`). Остаются 0..4: HUMAN, AI_CPU1..AI_CPU4.

### 4.3 Вертикальная раскладка
- `lineHeight = F + 4` (`cScoringState.cpp:60`); `statLineHeight = Fs + 2` (`:61`); `y0 = 40` (`:62`).
- Заголовок в `y0`, затем `y += 2*lineHeight` (`:65`).
- Время в текущем `y`, затем `y += 2*lineHeight` (`:69-70`).
- Блок игрока: строка имени в `y`, затем `y += lineHeight` (`:88`); строка 4 в `y`, `+= statLineHeight` (`:93`); строка 5, `+= statLineHeight` (`:98`); строка 6, `+= statLineHeight` (`:102`); строка 7 в `y`, затем `y += 2*lineHeight` (`:106`).
- Нижняя подсказка всегда в `H - lineHeight - 8`; при переполнении (много игроков) ничего не обрезается и не сдвигается (не найдено ограничения).

### 4.4 Источники чисел (`src/game/cMissionStatsCollector.cpp`)
- Снимок `snapshot(elapsedSeconds)` (`:157-163`): копирует `m_playerStats` и `elapsedSeconds`.
- `GAME_EVENT_ABOUT_TO_BEGIN` (`:50-64`): сброс `m_playerStats = {}` (`:53`); фиксируются `house` и `minimapColor` каждого игрока (`:57-62`).
- `GAME_EVENT_DAMAGED` (`:67-84`): атакующий (`resolveOriginPlayer`) — `damageDealt += damage` (`:73-76`); жертва — `damageReceived += damage` (`:77-82`).
- `GAME_EVENT_SPICE_HARVESTED` (`:86-97`): `spiceHarvested += amount` (`:92-95`).
- `GAME_EVENT_DESTROYED` (`:110-122`): убийца — `damageDealt += damage` (`:114`); `unitsDestroyed++` при `entityType == UNIT` (`:115-117`), `structuresDestroyed++` при `STRUCTURE` (`:118-120`).
- `GAME_EVENT_CREATED` (`:135-145`): `isReinforce` — не учитывается (`:136-138`); `unitsBuilt++` / `structuresBuilt++` (`:139-144`).
- `GAME_EVENT_DESTROYED` для владельца (`:146-154`): `damageReceived += damage` (`:147`); `unitsLost++` / `structuresLost++` (`:148-153`).
- Замечание: `damageDealt` и `damageReceived` увеличиваются и из `DAMAGED`, и из `DESTROYED` (`:75`, `:114`, `:80`, `:147`). Является ли это двойным учётом последнего удара — не проверено.

### 4.5 Зоны нажатия вне виджетов
- Всё окно: `MOUSE_LEFT_BUTTON_CLICKED` → `continueToWinBrief()` (`cScoringState.cpp:113-120`).

### 4.6 Клавиши
- Не найдено: `onNotifyKeyboardEvent` пустой (`:122-124`).

### 4.7 Переходы
- `continueToWinBrief()` (`:42-46`): `m_missionFlow->goingToWinLoseBrief(GAME_WINBRIEF)` → `cGame::goingToWinLoseBrief` → `setState(GAME_WINBRIEF)`, `prepareMentatForPlayer()` (`cGame_logic.cpp:1247-1250`, `:1300-1305`); затем `m_stateTransitions->fadeOut()`.
- Дальше: ментат WinBrief (§1.13).

### 4.8 Пороги раскладки
- Не найдено: нет порогов по размеру холста, кроме `H - lineHeight - 8` для подсказки.

### 4.9 Вызовы uiaudit
- Явных `uiaudit::` в `cScoringState` нет; косвенно через `cTextDrawer::drawTextCentered` (`cTextDrawer.cpp:75-83` → `drawText` → `recordText`) и `drawTextCentered(x, width, y, color)` (`:174-187`, `BoxScope`).

---

## 5. Титры — `cCreditsState` (+ что такое `CreditsDrawer`)

Файлы: `src/gamestates/cCreditsState.{h,cpp}`.

### 5.0 Уточнение по `CreditsDrawer`
- `src/drawers/CreditsDrawer.{h,cpp}` и `src/drawers/CreditsMath.hpp` НЕ относятся к экрану титров. Это HUD-счётчик кредитов в сайдбаре: `CreditsDrawer::draw()` рисует панель `CREDITS` и сумму (`src/drawers/CreditsDrawer.cpp:215-275`); создаётся в `cDrawManager` (`src/managers/cDrawManager.cpp:93`). `cCreditsState` его не использует (поиск `CreditsDrawer` по `src/`: только `cDrawManager` и сам класс).
- `CreditsMath` — чистая логика счётчика (`CreditsMath.hpp:24-52`): цифры кредитов, выравнивание, шаг `nextDisplayedCredits`. К титрам не относится.

### 5.1 Порядок рисования `draw()` (`src/gamestates/cCreditsState.cpp:441-469`)
1. Фото команды `m_teamBmp` в `m_teamCoordinates` (`:443`).
2. Заголовок `m_titleBmp` в `(m_titleX, m_crawlerY)` (`:448`).
3. Строки титров, начиная с `textCrawlY = m_crawlerY + m_titleHeight` (`:449-465`).
4. Кнопка «Back» (`:467`).
5. Курсор (`:468`).

Картинки:
| Картинка | Файл / константа | Пиксели | Логически | Растяжка | Позиция |
|---|---|---|---|---|---|
| Фото команды | `credits_team.png` (`loadHdUiTexture`, `cCreditsState.cpp:53-56`); резерв `CREDITS_DUNE2_CORE_TEAM` (индекс 21, `gfxinter.h:45`) | 948 x 624 (PNG; резерв тот же размер, `sdl_inter_hd4.dat` индекс 21) | 237 x 156 | нет (`renderSprite`) | x = trunc(W - 237*1.1), y = trunc(H - 156*1.1), см. §5.2 |
| Заголовок | `credits_title.png` (`cCreditsState.cpp:57-60`); резерв `D2TM_TITLE` (индекс 22, `gfxinter.h:46`) | 1280 x 800 (PNG; резерв 1280x800) | 320 x 200 | нет | x = `W/2 - 320/2`, y = `m_crawlerY` |

### 5.2 Геометрия
- `teamAtTheRight = W - (teamW * 1.1f)` → целое (`cCreditsState.cpp:69`): для team.w = 237 → `W - 260.7` с усечением.
- `teamAlmostAtBottom = H - (teamH * 1.1f)` → целое (`:70`): для team.h = 156 → `H - 171.6` с усечением.
- `m_teamCoordinates = (teamAtTheRight, teamAlmostAtBottom)` (`:71`).
- `titleWidth = m_titleBmp->w` (`:73`), `m_titleHeight = m_titleBmp->h` (`:74`), `centerOfScreen = W/2` (`:76`), `m_titleX = centerOfScreen - titleWidth/2` (`:78`).
- `m_crawlerY` начальное = `H + 1` (`resetCrawler`, `:410-413`).
- Сброс: в `thinkFast` (`:427-439`): `m_crawlerY -= m_moveSpeed` (`:429`); `textCrawlY = m_crawlerY + m_titleHeight + Σ line.height` (`:431-434`); если `< 0` → `resetCrawler()` (`:436-438`).

### 5.3 Скорость прокрутки
- `m_moveSpeed = 0.15f` (`cCreditsState.cpp:45`) → при тике 5 мс: 0.15 px/тик = 30 px/с (по `cTimeManager.cpp:156`).
- Нажатие левой (PRESSED) → `m_moveSpeed = 1.0f` (`:475-477`) → 200 px/с.
- Отпускание (CLICKED) → `m_moveSpeed = 0.15f` (`:478-480`).

### 5.4 Кнопка «Back»
- Ширина `max(140, getTextLength("Back") + 24)` (`cCreditsState.cpp:81`); высота `max(36, F + 10)` (`:82`); `x = 0` (`:84`), `y = H - height` (`:83`).
- `GuiButtonBuilder`: rect, подпись «Back», bene, тема `GuiTheme::Remaster()`, тип `REMASTER_BUTTON` (`:86-92`).
- Клик → `setNextStateWithFade(GAME_MENU)` (`:93-95`).
- Рамка Remaster: fill (24,29,33,238); borderLight (190,145,58); borderDark (71,50,24); text (236,229,202); hover (255,202,83); shadow (4,6,7,220) (`src/gui/GuiTheme.hpp:39-53`). `REMASTER_BUTTON` рисует тень `+3,+3` (`src/gui/GuiButton.cpp:100-130`).
- Текст внутри: `drawTextScaledOpticallyCenteredInBox` с `fittedScale` (см. §1.10).

### 5.5 Список строк (как в коде, порядок)
Строки `m_lines` (`cCreditsState.cpp:102-408`): 52 записи: 6 спейсеров (высота 40, объект `spacer` из `:108-113`), 16 с высотой `2F+4` (`spacerAfterHeadline`), 30 с высотой `F+4` (`fontHeightWithALittlePadding`).

Заголовки цвета `colorHeadlines = Color::Green` (`:104`).

| # | name | txt | цвет (`Color::`) | высота | строки кода |
|---|---|---|---|---|---|
| 1 | — | `Version {D2TM_VERSION}` | Yellow | 2F+4 | `:115-120` |
| 2 | — | `by Stefan Hendriks` | White | F+4 | `:121-126` |
| 3 | spacer | | Black | 40 | `:127` |
| 4 | — | `a remake of` | White | 2F+4 | `:128-133` |
| 5 | — | `Dune 2 - The Building of a Dynasty (by Westwood Studios)` | Red | 2F+4 | `:134-139` |
| 6 | spacer | | | 40 | `:141` |
| 7 | — | `--- CONTRIBUTORS ---` | Green | 2F+4 | `:143-148` |
| 8 | Paul | `Developer` | White | F+4 | `:149-154` |
| 9 | Arjen | `Developer & Sparring partner` | White | F+4 | `:155-160` |
| 10 | Mira | `Developer` | White | F+4 | `:161-166` |
| 11 | Matt Van Horn | `Bugfixes` | White | F+4 | `:167-172` |
| 12 | Rozmy | `Graphics` | White | F+4 | `:173-178` |
| 13 | Nema Fakei | `Graphics` | White | F+4 | `:179-184` |
| 14 | Vidiware | `Graphics` | White | F+4 | `:185-190` |
| 15 | Timenn | `Graphics` | White | F+4 | `:191-196` |
| 16 | MrFlibble | `Graphics` | White | F+4 | `:197-202` |
| 17 | Ravenborn | `Internal Editor UI graphics and miscellaneous assets` | White | F+4 | `:203-208` |
| 18 | Ripps | `Support at Discord, testing & Skirmish Maps` | White | F+4 | `:209-214` |
| 19 | Bruno | `For your lifelong support & valuable feedback` | White | F+4 | `:215-220` |
| 20 | spacer | | | 40 | `:222` |
| 21 | — | `--- ACKNOWLEDGEMENTS ---` | Green | 2F+4 | `:224-229` |
| 22 | Westwood Studios | `for producing Dune 2` | White | F+4 | `:230-235` |
| 23 | SDL3 | `by Sam Lantinga and contributors` | White | F+4 | `:236-241` |
| 24 | — | `with SDL_image, SDL_ttf and SDL_mixer` | White | F+4 | `:242-247` |
| 25 | — | `Dune Legacy, Dune Dynasty and Dune The Golden Path` | White | F+4 | `:248-253` |
| 26 | spacer | | | 40 | `:255` |
| 27 | — | `--- KO-FI SUPPORTERS ---` | Green | 2F+4 | `:257-262` |
| 28 | Fedaygin | `` (пусто) | White | F+4 | `:263-268` |
| 29 | Morto | `` | White | F+4 | `:269-274` |
| 30 | The General | `` | White | 2F+4 | `:275-280` |
| 31 | Bastian | `` | White | 2F+4 | `:281-286` |
| 32 | Florian | `` | White | 2F+4 | `:287-292` |
| 33 | Aleksandar | `` | White | 2F+4 | `:293-298` |
| 34 | Bruno | `` | White | 2F+4 | `:299-304` |
| 35 | Dan Greene | `` | White | 2F+4 | `:305-310` |
| 36 | Sergio Muad'Dib | `` | White | 2F+4 | `:311-316` |
| 37 | saif3r | `` | White | 2F+4 | `:317-322` |
| 38 | spacer | | | 40 | `:323` |
| 39 | — | `--- SPECIAL THANKS TO ---` | Green | 2F+4 | `:325-330` |
| 40 | Gobalopper | `for Dune2K, and hosting arrakis.dune2k.com` | White | F+4 | `:331-336` |
| 41 | Jpexs | `for help with the Dune 2 Seed Generator` | White | F+4 | `:337-342` |
| 42 | Rene | `for the D2TM Java Map Editor` | White | F+4 | `:343-348` |
| 43 | Mira | `for porting D2TM to SDL2` | White | F+4 | `:349-354` |
| 44 | Guillaume Lavoie | `` | White | F+4 | `:355-360` |
| 45 | Dennis Stansert | `` | White | F+4 | `:361-366` |
| 46 | Ash | `` | White | F+4 | `:367-372` |
| 47 | Ruurd Nijdam | `` | White | F+4 | `:373-378` |
| 48 | rphl | `` | White | F+4 | `:379-384` |
| 49 | Non sono Mandrake | `for nudging me to work on D2TM again in C++` | White | F+4 | `:385-390` |
| 50 | Dune2k.com | `For all the good times at the arrakis forums` | White | F+4 | `:391-396` |
| 51 | spacer | | | 40 | `:400` |
| 52 | — | `Thank you for playing` | White | 2F+4 | `:402-407` |

Строки 1-2 используют `D2TM_VERSION` из `config.h` (`cCreditsState.cpp:20`, `:117`); значение не открыто.

### 5.6 Вывод строки (`draw`, `cCreditsState.cpp:449-465`)
- Если `name` пуст: `drawTextCentered(txt, y, color)` (`:451-453`) — по центру экрана, цвет строки.
- Если `txt` пуст (name задан): `drawTextCentered(name, y, color)` (`:454-456`).
- Иначе (name и txt заданы): `drawText(halfScreen + 4, y, txt)` (`:458-460`) — цвет по умолчанию White, тень; `drawText(halfScreen - (widthName + 4), y, name)` (`:461-462`) — тоже White. Цвет строки (`line.color`) для строк с name+txt не используется (факт кода).
- Подпись `drawText` использует тень `+1,+1` (cTextDrawer.h:35-39).
- Шрифт для всех строк — bene (`m_textDrawer`, `cCreditsState.cpp:41`).

Сумма высот (для расчёта периода прокрутки): Σ = 16·(2F+4) + 30·(F+4) + 6·40 = 62F + 424 (логические px, F = getFontHeight bene). Полный путь от `m_crawlerY = H+1` до сброса: `titleH + Σ = 200 + 62F + 424 = 624 + 62F` (логические px). Точное F не измерено.

### 5.7 Зоны нажатия вне виджетов
- Всё окно: `MOUSE_LEFT_BUTTON_PRESSED` → ускорение (`cCreditsState.cpp:475-477`); `MOUSE_LEFT_BUTTON_CLICKED` → возврат скорости (`:478-480`). Переход по клику вне кнопки не предусмотрен (не найдено).

### 5.8 Клавиши
- `PRESSED` + `MENU_BACK` (Escape) → `setNextStateWithFade(GAME_MENU)` (`cCreditsState.cpp:488-492`).

### 5.9 Переходы
- Из главного меню: `m_stateTransitions->setNextStateWithFade(GAME_CREDITS)` (`src/gamestates/cMainMenuState.cpp:189`).
- После победы в последней миссии: `GAME_CREDITS` с fade (`src/game/cGame_logic.cpp:1340-1345`, условие `mission >= 9`).
- Из титров: Back или Escape → `GAME_MENU` с fade (`cCreditsState.cpp:93-95`, `:491`).

### 5.10 Пороги раскладки
- Не найдено пороговых значений по размеру холста (всё вычисляется от `W`, `H`). Геометрия из §5.2.

### 5.11 Вызовы uiaudit
- Явных `uiaudit::` в `cCreditsState` нет.
- Косвенно: `cTextDrawer::drawTextCentered`, `drawText` (`cTextDrawer.cpp:51-52`), `GuiButton::draw` (`GuiButton.cpp:49-53`) для Back: записи `GuiButton` и `GuiButton:Back`.

---

## 6. Ролик — `cVideoState`

Файлы: `src/gamestates/cVideoState.{h,cpp}`.

### 6.1 Вход и источник
- Единственный пункт входа в коде: кнопка «Introduction» в главном меню (`src/gamestates/cMainMenuState.cpp:171-175`): `introMoviePack = "intro.pak"` (`:171`); кнопка доступна только если файл существует (`:172-173`); клик → `m_videoFlow->play("intro.pak")` (`:174`).
- `VideoFlow::play` → `m_creatorState->createVideoState(filename)` + `setNextStateToTransitionTo(GAME_VIDEO)` (`src/game/cGame_logic.cpp:235-240`); `GAME_VIDEO` → `getState(VIDEO)` (`:1147-1149`).
- `intro.pak` в рабочей копии не найден (§0.7). Размер и число кадров — не проверено.

### 6.2 Геометрия (`cVideoState.cpp:31-41`, `:43-65`, `:91-99`)
- Константы: `VIDEO_WIDTH = 640`, `VIDEO_MAX_HEIGHT = 480`, `VIDEO_CENTER_SHIFT = 75`, `VIDEO_DRAW_EXTRA = 150`.
- `m_offsetX = (W - 640)/2 - 75` (`:60`); `m_offsetY = (H - 480)/2 - 75` (`:61`).
- Размер вывода: `dest = {offX, offY, 640 + 150, 480 + 150}` = 790 x 630 (`:95`), растяжка `renderStrechFullSprite` (`:96`).
- Комментарий в коде: «the source frames are reportedly 320x288 (drawn scaled up)» (`:34`) — не проверено.

### 6.3 Порядок рисования `draw()` (`:91-99`)
1. `m_mouse->setTile(MOUSE_NORMAL)` (`:93`).
2. Если `m_currentFrame != nullptr`: кадр растянут на `dest` (`:94-97`).
3. `m_mouse->draw()` (`:98`).
- Фона и текста нет.

### 6.4 Элементы
- Единственный элемент — кадр видео (`Graphics(renderer, filename)` без density, т.е. density = 1, `cVideoState.cpp:54`, `Graphics.hpp:39`). Текст отсутствует.

### 6.5 Зоны нажатия вне виджетов
- Всё окно: `MOUSE_LEFT_BUTTON_PRESSED` → `setNextStateWithFade(GAME_MENU)` (`cVideoState.cpp:101-106`).

### 6.6 Клавиши
- Любая клавиша в состоянии PRESSED → `setNextStateWithFade(GAME_MENU)` (`:108-113`).

### 6.7 Переходы
- Кадры: `thinkNormal` (`:80-89`) — один кадр за вызов (~100 мс, `cTimeManager.cpp:167`): `m_currentFrame = getTexture(m_movieFrame)`, `m_movieFrame++` (`:83-85`). Конец (`m_movieFrame >= getNumberOfFiles()`) → `setNextStateWithFade(GAME_MENU)` (`:86-88`).
- Пустой пакет: `Logger::error` и возврат в меню (`:62-63`, комментарий `:56`).
- Клик (PRESSED) и любая клавиша → `GAME_MENU` с fade.

### 6.8 Пороги раскладки
- Не найдено: `m_offsetX/Y` зависят только от `W`, `H` (`:60-61`); порогов нет.

### 6.9 Вызовы uiaudit
- Явных и косвенных `uiaudit::` в `cVideoState` нет (кадр без текста и без GUI-кнопок).

---

## 7. Неопределённости и риски (сводка)

1. Сцены ментата и TellHouse в рабочей копии — LFS-указатели (§0.7, §1.3). Размеры кадров и их число не измерены.
2. Риск разыменования: `AbstractMentat::draw_movie` (`AbstractMentat.cpp:322-331`) не проверяет `tmp` на `nullptr`. `Graphics::getTexture(index)` возвращает `nullptr` при `index >= getNumberOfFiles()` (`src/utils/Graphics.cpp` `getTexture(int)`; `cDataPack::getSurface` при неверном индексе, `src/utils/cDataPack.cpp:77-81`). Для пакета-указателя `fileInPak = 0` (`src/utils/cPack.h:65`), значит `getTexture(0)` вернёт `nullptr` и `tmp->w` разыменуется. Не запускалось (не проверено).
3. Видимость сцены: по коду сцена рисуется до непрозрачного фона (§1.2, все пять фонов полностью непрозрачны по декодированию PNG). Видимость на экране не проверена.
4. Ментат с `BeneMentat` внутри `cMentatState` (ветка `else` в `cMentatState.cpp:92,108,126`) — для `house`, не являющегося ATREIDES/HARKONNEN/ORDOS/SARDAUKAR; для Briefing файл текста `""` (`IniParsing.cpp:641`) не открывается. Когда эта ветка реально возникает — не проверено.
5. Отчёт о миссии: `damageDealt` и `damageReceived` увеличиваются и из `DAMAGED`, и из `DESTROYED` (§4.4). Возможное двойное учёт — не проверено.
6. `elapsedSeconds` — из `cTimeManager::getElapsedSeconds()` (`cTimeManager.cpp:65-68`), источник `m_timeCounter` не открыт (не проверено).
7. Тики 5 мс и 100 мс — из комментариев `cTimeManager.cpp:156,167`; реальный таймер не проверялся.
8. Масштаб окна/презентации и `RenderScale` не проверялись.
9. Шрифты `benegess.fon`, `small.ttf` (`settings.ini:91-92`): метрики (F, Fs) не измерены; формулы даны через F и Fs.
10. Кнопки `GuiButton` — обработка клавиш (`onNotifyKeyboardEvent`) не открыта: поведение «Mission select» по клавишам не проверено.
11. `D2TM_VERSION` (`config.h`) не открыт.
12. `cPlayer::getHouseNameForId` для `GENERALHOUSE` и далее — не открыто полностью (`cPlayer.cpp:822-` до конца функции).
13. Sardaukar в TellHouse: звук и сцена закомментированы (`cTellHouseState.cpp:83,85`) — подтверждено кодом.
14. `intro.pak` отсутствует в рабочей копии; видео не проверено.
15. Скрипт декодирования PNG (`alphabox.js`, `boxcolor.js`) и `packscan.js` лежат в scratchpad и удаляются после задачи; в репозиторий ничего не записано, кроме этого файла.

## 8. Вызовы uiaudit — сводка по экранам

| Экран | Явные `uiaudit::` | Косвенно через | Записи |
|---|---|---|---|
| Ментат (`AbstractMentat`, `cMentatState`, подклассы) | нет | `cTextDrawer::drawText` (`cTextDrawer.cpp:51-52`); `GuiButton::draw` (`GuiButton.cpp:49-53`) | `recordText(msg, ...)`; `recordGui("GuiButton", ...)`; `recordClick("GuiButton:Repeat"/"Yes"/"No"/"Mission select")` |
| Рассказ о Доме (`cTellHouseState`, Bene) | нет | то же | то же, плюс `GuiButton:Yes`/`GuiButton:No` |
| Исход (`cWinLoseState`) | нет | `drawTextScaledCenteredInBox` (`cTextDrawer.cpp:129-131`) | `recordText("Click to continue", x, y, w, h, &box)` |
| Отчёт (`cScoringState`) | нет | `drawTextCentered` (`cTextDrawer.cpp:75-83`, `:174-187`) | `recordText(...)` |
| Титры (`cCreditsState`) | нет | `drawText`, `drawTextCentered`, `GuiButton::draw` | `recordText(...)`; `GuiButton:Back` |
| Ролик (`cVideoState`) | нет | — | — |

Вызовы `uiaudit::` в `src/` (поиск): `src/main.cpp:60-150`, `src/game/cGame_logic.cpp:576-638`, `src/game/cSDLSystem.cpp:206`, `src/gui/GuiCheckBox.cpp:42`, `src/gui/GuiButton.cpp:49`, `src/gui/GuiLabel.cpp:42`, `src/gui/GuiObject.cpp:37,42`, `src/gui/GuiSlider.cpp:76`, `src/gui/GuiWindow.cpp:39`, `src/drawers/cTextDrawer.cpp:51,52,97-101,129-131,158-160,182-186`. Экранов рассказа/итогов среди них, кроме косвенных путей выше, нет.
