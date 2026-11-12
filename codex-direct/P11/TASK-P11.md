# Задание P11 — HD-ментаты: места глаз и рта, окно сцены и передний слой на картинах форка (шаг П11, issue #124)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и помощники `gpt-6-luna` `xhigh` (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p11`, ветка `codex/p11`, `HEAD` — `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (вершина ветки порта `port/up-d06f2fcd`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p11/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p11/` (дальше — «папка задания»).

## Цель

Ментаты Атрейдесов, Харконненов, Ордосов и Бене Гессерит рисуют глаза и рот в местах, которые заданы под HD-картины форка (`MENTATA`, `MENTATH`, `MENTATO`, `MENTATM`), а не под классические картины; кадр сцены ментата лежит в окне на картине, и картина рисуется поверх сцены с прозрачным окном по фигуре проёма, поэтому рама и плечо ментата остаются поверх краёв сцены. Ментат Сардаукаров не меняется. Готово, когда новые тесты Catch2 и сборка со всеми тестами зелёные, а PNG сцен ментатов лежат в `.tmp/p11/png/` для оценки вида ведущим.

## Что уже решено

Ревизия `B` = `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (дерево равно `a1e63b860482d7e7a82e502359965e2caefd6470`), ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`. Все факты о коде порта ниже — о файлах ревизии `B`; номера строк форка — ревизии `FORK1`.

- **Что переносится.** Только то, что привязано к HD-картинам форка: места глаз и рта каждого из четырёх ментатов (единицы кадра 640 × 480 от левого верхнего угла кадра; в порту кадр стоит в `offsetX`, `offsetY` с масштабом 1); окно сцены каждого ментата (кадр сцены и прозрачное окно проёма); передний слой форка (картина поверх сцены, в картине прорезано прозрачное окно по фигуре проёма) и `SDLDrawer::clearRectToTransparent`. Места и размеры — данными, общий механизм — в `AbstractMentat`, без ветвлений по Дому в общем коде.
- **Не переносится** (это делает переработка интерфейса после П11 или уже сделано): масштаб экрана ментата `m_uiScale` и функции `baseX`, `baseY`, `baseRect`; кнопки по гнёздам картины и кнопка «Missions» (остаются кнопки порта); HD-шрифт ментата `getMentatHdTextDrawer` и `wrapMentatText` (текст остаётся как в порту: `layoutMentatPage`); `HdPresentation.hpp`, `useHdPresentation`; `drawHdTextHeader`, `harmonizeHdButtonTextScale`; инструменты форка (`build_mentat_hd_screen.py` и остальные) и их картины `resources/hd/**`; титры (перенесены шагом П5а); вступительный ролик и кнопка «Вступление» (решение Р72 п. 2).
- **Сардаукары.** Глаз и рта Сардаукаров в паке нет, данных окна сцены у форка для их картины `MENTATS` нет. `SardaukarMentat` и его путь рисования остаются как в `B`: файл `src/gameobjects/mentat/SardaukarMentat.cpp` не меняется.
- **Бене Гессерит** показывает сцены (`cTellHouseState::prepareMentat` вызывает `m_mentat->loadScene("platr")`, `"plhar"`, `"plord"` у `BeneMentat`; `cMentatState` — `win01`, `win02`, `lose01`, `lose02` при чужом Доме), поэтому у него есть окно сцены. Его значения — значения форка по умолчанию из `FORK1:src/mentat/AbstractMentat.h` (`m_movieClipX = 215`, `m_movieClipY = 104`, `m_movieClipWidth = 398`, `m_movieClipHeight = 215`) и `FORK1:src/mentat/AbstractMentat.cpp` (`HD_STANDARD_MOVIE_X = 211`, `HD_STANDARD_MOVIE_Y = 93`, `HD_STANDARD_MOVIE_WIDTH = 400`, `HD_STANDARD_MOVIE_HEIGHT = 243`); у Харконненов те же значения, у Ордосов те же, кроме фигуры проёма.
- **Размеры спрайтов.** Все картины глаз в паке — 96 × 32 единиц кадра (384 × 128 px при плотности 4), все картины рта — 112 × 80 (448 × 320 px): `tests/data/hd4_packs_expected.tsv`, строки `ATR_EYES01 … ORD_MOUTH05`.
- **Форма данных** (выбрана по коду): заголовок без зависимостей `src/gameobjects/mentat/MentatHdLayout.hpp` с структурой `MentatHdLayout` и четырьмя `inline constexpr` значениями — по одному на ментата. Заголовки классов ментатов не годятся для теста: `AbstractMentat.h` подключает `SDL3_ttf`, а список `TEST_SOURCES` не содержит `GameContext`. Класс ментата получает свою раскладку указателем `m_hdLayout`; у Сардаукаров он остаётся `nullptr`, и в `AbstractMentat::draw` остаётся прежний путь.
- **Тесты форка.** По этому шагу тестов форка нет (`tests/HdPresentationTests.cpp` относится к другому шагу), таблицы «проверка форка → случай Catch2» нет. Новый файл — приёмочный тест значений.
- **Порт.** SDL3, `SDLDrawer` вместо глобального `renderDrawer`, `cRectangle::toSDLF()` вместо `toSDL()`, `Texture::w/h` — в единицах кадра, `Texture::pixelW/pixelH/density` — в пикселях; цель рисования `createRenderTargetTexture(width, height, density)` при плотности больше 1 сама ставит логическое представление на `width × height`, поэтому слой строится в единицах кадра 640 × 480.
- **Issue #124** закрывается этим шагом в части «рот на воротнике» (ведущий закрывает после приёмки вида); кнопки по гнёздам — не этого шага.

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл отдельным вызовом; вывод обрезан — дочитай частями до конца:

- `src/gameobjects/mentat/AbstractMentat.h` целиком;
- `src/gameobjects/mentat/AbstractMentat.cpp` целиком;
- `src/gameobjects/mentat/AtreidesMentat.cpp`, `BeneMentat.cpp`, `HarkonnenMentat.cpp`, `OrdosMentat.cpp`, `SardaukarMentat.cpp` из той же папки — каждый целиком;
- `src/gameobjects/mentat/MentatTextLayout.hpp` целиком;
- `src/drawers/SDLDrawer.hpp` целиком;
- `src/drawers/SDLDrawer.cpp` целиком;
- `src/include/Texture.hpp` целиком;
- вывод `nl -ba src/gamestates/cMentatState.cpp | sed -n '80,140p'`;
- вывод `nl -ba src/gamestates/cTellHouseState.cpp | sed -n '60,95p'`;
- вывод `nl -ba tests/CMakeLists.txt | sed -n '1,60p'`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp` (732 строки, частями);
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.h`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AtreidesMentat.cpp`, `BeneMentat.cpp`, `HarkonnenMentat.cpp`, `OrdosMentat.cpp` — каждый отдельным вызовом;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/drawers/SDLDrawer.cpp | sed -n '165,190p'`;
- вывод `git grep -n -E 'ATR_EYES01|ORD_MOUTH05|MENTATA|MENTATS' 6ceb29d1604ad0a487436bb9f1a0c60a746deeb6 -- tests/data/hd4_packs_expected.tsv`.

Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

1. **Раскладка (новый файл).** `src/gameobjects/mentat/MentatHdLayout.hpp` — создаётся с этим содержимым дословно:
   ```cpp
   #pragma once

   #include <algorithm>
   #include <array>
   #include <cmath>
   #include <cstddef>
   #include <span>

   struct MentatHdPoint {
       int x;
       int y;
   };

   struct MentatHdRect {
       int x;
       int y;
       int width;
       int height;
   };

   struct MentatSceneEdgePoint {
       int y;
       int rightX;
   };

   struct MentatHdRowSpan {
       int left;
       int right;
   };

   struct MentatHdLayout {
       MentatHdPoint eyes;
       MentatHdPoint mouth;
       MentatHdRect sceneFrame;
       MentatHdRect sceneOpening;
       int openingCornerHeight;
       std::span<const MentatSceneEdgePoint> shoulderEdge;
   };

   inline constexpr int MENTAT_HD_FRAME_WIDTH = 640;
   inline constexpr int MENTAT_HD_FRAME_HEIGHT = 480;
   inline constexpr int MENTAT_EYES_WIDTH = 96;
   inline constexpr int MENTAT_EYES_HEIGHT = 32;
   inline constexpr int MENTAT_MOUTH_WIDTH = 112;
   inline constexpr int MENTAT_MOUTH_HEIGHT = 80;

   inline constexpr std::array<MentatSceneEdgePoint, 10> kAtreidesShoulderEdge = {{
       {270, 273}, {290, 273}, {294, 275}, {296, 285}, {300, 289},
       {306, 293}, {314, 297}, {320, 303}, {326, 308}, {334, 314}
   }};

   inline constexpr std::array<MentatSceneEdgePoint, 11> kOrdosShoulderEdge = {{
       {273, 213}, {276, 218}, {280, 225}, {285, 232}, {290, 239}, {295, 243},
       {300, 247}, {305, 250}, {310, 254}, {315, 257}, {319, 261}
   }};

   inline constexpr MentatHdLayout kAtreidesMentatHdLayout = {
       {96, 180}, {100, 210}, {234, 95, 400, 243}, {276, 115, 322, 219}, 0, kAtreidesShoulderEdge
   };

   inline constexpr MentatHdLayout kBeneMentatHdLayout = {
       {96, 180}, {100, 210}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, {}
   };

   inline constexpr MentatHdLayout kHarkonnenMentatHdLayout = {
       {96, 180}, {100, 210}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, {}
   };

   inline constexpr MentatHdLayout kOrdosMentatHdLayout = {
       {48, 174}, {52, 207}, {211, 93, 400, 243}, {215, 104, 398, 215}, 14, kOrdosShoulderEdge
   };

   inline MentatHdRowSpan sceneOpeningSpan(const MentatHdLayout &layout, int y)
   {
       const MentatHdRect &opening = layout.sceneOpening;
       const int bottom = opening.y + opening.height;
       if (y < opening.y || y >= bottom) {
           return {0, 0};
       }

       int inset = 0;
       if (y < opening.y + layout.openingCornerHeight) {
           inset = opening.y + layout.openingCornerHeight - y;
       }
       else if (y >= bottom - layout.openingCornerHeight) {
           inset = y - (bottom - layout.openingCornerHeight) + 1;
       }

       int left = opening.x + inset;
       const int right = opening.x + opening.width - inset;
       for (std::size_t segment = 0; segment + 1 < layout.shoulderEdge.size(); ++segment) {
           const MentatSceneEdgePoint from = layout.shoulderEdge[segment];
           const MentatSceneEdgePoint to = layout.shoulderEdge[segment + 1];
           if (y < from.y || y >= to.y) {
               continue;
           }
           const double progress = static_cast<double>(y - from.y) / (to.y - from.y);
           const int portraitRight = static_cast<int>(std::lround(from.rightX + (to.rightX - from.rightX) * progress));
           left = std::max(left, portraitRight + 1);
           break;
       }
       return {left, right};
   }
   ```
   Источники значений: глаза и рот — `FORK1:src/mentat/AtreidesMentat.cpp` строки 120–128, `BeneMentat.cpp` (функции `draw_eyes`, `draw_mouth`), `HarkonnenMentat.cpp` строки 55–63, `OrdosMentat.cpp` строки 119–127; окно и кадр Атрейдесов — `AtreidesMentat.cpp` строки 21–28; ломаная Атрейдесов — строки 83–93; ломаная Ордосов — `OrdosMentat.cpp` строки 68–79; закругление углов 14 — `clearHdMovieOpening` в `AbstractMentat.cpp` форка (`cornerHeight = 14`) и в `OrdosMentat.cpp`. Функция `sceneOpeningSpan` — построчная форма трёх функций форка `AbstractMentat::clearHdMovieOpening`, `AtreidesMentat::clearHdMovieOpening`, `OrdosMentat::clearHdMovieOpening`: у Атрейдесов закруглений нет (`openingCornerHeight` 0), у остальных — 14; `right` — исключающая граница. Файл не правится сверх этого текста.

2. **`SDLDrawer::clearRectToTransparent`.**
   - `src/drawers/SDLDrawer.hpp`: сразу после строки `    void renderRectColor(const cRectangle &rect, Color color, unsigned char opacity=255);` добавляется строка `    void clearRectToTransparent(const cRectangle &rect);`.
   - `src/drawers/SDLDrawer.cpp`: сразу перед строкой `void SDLDrawer::resetClippingFor()` вставляется функция и одна пустая строка после неё:
     ```cpp
     void SDLDrawer::clearRectToTransparent(const cRectangle &rect)
     {
         Uint8 previousR = 0;
         Uint8 previousG = 0;
         Uint8 previousB = 0;
         Uint8 previousA = 0;
         SDL_BlendMode previousBlendMode = SDL_BLENDMODE_BLEND;
         SDL_GetRenderDrawColor(renderer, &previousR, &previousG, &previousB, &previousA);
         SDL_GetRenderDrawBlendMode(renderer, &previousBlendMode);

         SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_NONE);
         SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
         const SDL_FRect destination = rect.toSDLF();
         SDL_RenderFillRect(renderer, &destination);

         SDL_SetRenderDrawColor(renderer, previousR, previousG, previousB, previousA);
         SDL_SetRenderDrawBlendMode(renderer, previousBlendMode);
     }
     ```
     Это тело `FORK1:src/drawers/SDLDrawer.cpp` строки 171–185 с единственной заменой `SDL_Rect destination = rect.toSDL();` → `const SDL_FRect destination = rect.toSDLF();`.

3. **`AbstractMentat.h`.**
   - После строки `#include "observers/cInputObserver.h"` добавляется строка `#include "gameobjects/mentat/MentatHdLayout.hpp"`.
   - В защищённой части после строки `    void draw_movie();` добавляются строки:
     ```cpp
         void drawMentatTexture(Texture *texture, const MentatHdPoint &position);
         Texture *getHdForegroundLayer(Texture *background);
     ```
   - После строки `    int movieTopleftY;` добавляются строки:
     ```cpp
         const MentatHdLayout *m_hdLayout = nullptr;
         std::unique_ptr<Texture> m_hdForegroundLayer;
     ```

4. **`AbstractMentat.cpp`.**
   - **Отрисовка.** В `AbstractMentat::draw` строки
     ```cpp
         Texture *tmp = getBackgroundBitmap();
         cRectangle dest = {offsetX, offsetY, MENTAT_SCREEN_W, MENTAT_SCREEN_H};
         m_sdlDrawer->renderStrechFullSprite(tmp, dest);
     ```
     заменяются строками:
     ```cpp
         Texture *tmp = getBackgroundBitmap();
         cRectangle dest = {offsetX, offsetY, MENTAT_SCREEN_W, MENTAT_SCREEN_H};
         const bool hasMovie = gfxmovie != nullptr && iMovieFrame >= 0;
         if (m_hdLayout != nullptr && hasMovie) {
             m_sdlDrawer->renderStrechFullSprite(getHdForegroundLayer(tmp), dest);
         }
         else {
             m_sdlDrawer->renderStrechFullSprite(tmp, dest);
         }
     ```
     Строка `draw_movie();` перед ними, рамки, текст, глаза, рот и кнопки остаются на своих местах.
   - **Кадр сцены.** В `AbstractMentat::draw_movie` после строки `    cRectangle dest = {movieTopleftX, movieTopleftY,tmp->w, tmp->h};` добавляются строки:
     ```cpp
         if (m_hdLayout != nullptr) {
             const MentatHdRect &frame = m_hdLayout->sceneFrame;
             dest = cRectangle(offsetX + frame.x, offsetY + frame.y, frame.width, frame.height);
         }
     ```
   - **Новые функции** — сразу после функции `AbstractMentat::draw_movie` и перед `void AbstractMentat::initSentences()`, с одной пустой строкой между функциями:
     ```cpp
     void AbstractMentat::drawMentatTexture(Texture *texture, const MentatHdPoint &position)
     {
         m_sdlDrawer->renderSprite(texture, offsetX + position.x, offsetY + position.y);
     }

     Texture *AbstractMentat::getHdForegroundLayer(Texture *background)
     {
         if (background == nullptr) return nullptr;
         if (m_hdForegroundLayer) return m_hdForegroundLayer.get();

         m_hdForegroundLayer.reset(m_sdlDrawer->createRenderTargetTexture(background->w, background->h, background->density));
         m_sdlDrawer->beginDrawingToTexture(m_hdForegroundLayer.get());
         m_sdlDrawer->renderClearToColor(Color{0, 0, 0, 0});
         m_sdlDrawer->renderStrechFullSprite(background, cRectangle(0, 0, background->w, background->h));
         const MentatHdRect &opening = m_hdLayout->sceneOpening;
         for (int y = opening.y; y < opening.y + opening.height; ++y) {
             const MentatHdRowSpan span = sceneOpeningSpan(*m_hdLayout, y);
             if (span.right > span.left) {
                 m_sdlDrawer->clearRectToTransparent(cRectangle(span.left, y, span.right - span.left, 1));
             }
         }
         m_sdlDrawer->endDrawingToTexture();
         SDL_SetTextureBlendMode(m_hdForegroundLayer->tex.get(), SDL_BLENDMODE_BLEND);
         return m_hdForegroundLayer.get();
     }
     ```
     Это функции `FORK1:src/mentat/AbstractMentat.cpp` `getHdForegroundLayer` (строки 538–557), `clearHdMovieOpening` (559–579) и `clearHdForegroundLayerRegion` (581–605) по правилам переноса пункта 7; перевод единиц кадра в пиксели отсутствует, потому что цель рисования создаётся с плотностью картины.
   - Других правок в файле нет.

5. **Ментаты Атрейдесов, Бене, Харконненов, Ордосов.** Каждый `.cpp` меняется тремя правками; заголовки `.h` не меняются.
   - После строки `    iBackgroundFrame = <фон>;` (фон `MENTATA`, `MENTATM`, `MENTATH`, `MENTATO`) добавляется строка `    m_hdLayout = &<раскладка>;`.
   - Тело `draw_eyes` — ровно `    drawMentatTexture(gfxmentat->getTexture(<ГЛАЗА>01 + iMentatEyes), <раскладка>.eyes);`.
   - Тело `draw_mouth` — ровно `    drawMentatTexture(gfxmentat->getTexture(<РОТ>01 + iMentatMouth), <раскладка>.mouth);`.

   | Файл | `<фон>` | `<раскладка>` | `<ГЛАЗА>` | `<РОТ>` |
   |---|---|---|---|---|
   | `AtreidesMentat.cpp` | `MENTATA` | `kAtreidesMentatHdLayout` | `ATR_EYES` | `ATR_MOUTH` |
   | `BeneMentat.cpp` | `MENTATM` | `kBeneMentatHdLayout` | `BEN_EYES` | `BEN_MOUTH` |
   | `HarkonnenMentat.cpp` | `MENTATH` | `kHarkonnenMentatHdLayout` | `HAR_EYES` | `HAR_MOUTH` |
   | `OrdosMentat.cpp` | `MENTATO` | `kOrdosMentatHdLayout` | `ORD_EYES` | `ORD_MOUTH` |

   Строки с `buildLeftButton`, `buildRightButton`, `GuiButtonBuilder`, тексты и обработчики кнопок не меняются. `SardaukarMentat.cpp` не меняется.

6. **Что не меняется.** Не меняются: `cMentatState.cpp`, `cTellHouseState.cpp`, `cGame_logic.cpp`, `ini.cpp`, `TextContext.*`, `ContextCreator.*`, `src/CMakeLists.txt` (новых `.cpp` нет), `TEST_SOURCES` в `tests/CMakeLists.txt`, кнопки и тексты ментатов, `loadScene`, ожидания существующих тестов.

7. **Правила переноса** (для функций форка в пункте 4):
   1. `renderDrawer->` → `m_sdlDrawer->` (тот же метод, те же аргументы).
   2. `SDL_Rect`/`toSDL()` → `SDL_FRect`/`toSDLF()`.
   3. `logbook(...)` → `Logger::info(COMP_GAME, "<функция>", ...)` по образцу соседних строк `AbstractMentat.cpp`; в пункте 4 таких строк нет.
   4. Строки с `uiaudit::`, `UiAuditAccess`, `localization::` и подключения `<SDL2/...>` не переносятся.
   5. Вызов функции форка без пары в порту, не названной в задании, — блок `## Q-P11-NN` и стоп.

8. **Подключение.** Новых `#include` в `.cpp` нет: `MentatHdLayout.hpp` приходит через `AbstractMentat.h`; `Color`, `Texture`, `cRectangle`, `SDLDrawer` в `AbstractMentat.cpp` уже подключены (`drawers/SDLDrawer.hpp`, `include/Texture.hpp`, `utils/cRectangle.h`). Если сборка требует другого заголовка — он добавляется сразу после последней строки вида `#include "…"` в начале файла, и это строка в раздел «Решено исполнителем».

9. **Ничего сверх контракта.** Других изменений нет: ни переформатирования, ни новых комментариев, ни переноса строк сверх нужного для правки.

## Тесты

Тесты пишутся в шаге 1 плана. В шаге 2 они собираются и краснеют до правок шага 3: без файла `MentatHdLayout.hpp` новый файл не компилируется.

**T1 — новый файл `tests/utils/test_MentatHdLayout.cpp`**, тег `[P11]`. Подключает `catch2/catch_test_macros.hpp` и `gameobjects/mentat/MentatHdLayout.hpp`; никаких других заголовков проекта. В файле две вспомогательные функции:
- `bool insideFrame(int x, int y, int width, int height)` — `x >= 0 && y >= 0 && x + width <= MENTAT_HD_FRAME_WIDTH && y + height <= MENTAT_HD_FRAME_HEIGHT`;
- `bool intersects(const MentatHdRect &a, const MentatHdRect &b)` — полуоткрытые прямоугольники: `a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height`.

Случаи (в каждом пробег по четырём раскладкам — `kAtreidesMentatHdLayout`, `kBeneMentatHdLayout`, `kHarkonnenMentatHdLayout`, `kOrdosMentatHdLayout` — с `INFO("<имя Дома>")` перед проверками):

1. **`mentat HD layouts keep the fork values`** — `CHECK` на каждое поле, значения — литералы:

   | Раскладка | `eyes` | `mouth` | `sceneFrame` | `sceneOpening` | `openingCornerHeight` | `shoulderEdge.size()` |
   |---|---|---|---|---|---|---|
   | Атрейдесы | 96, 180 | 100, 210 | 234, 95, 400, 243 | 276, 115, 322, 219 | 0 | 10 |
   | Бене | 96, 180 | 100, 210 | 211, 93, 400, 243 | 215, 104, 398, 215 | 14 | 0 |
   | Харконнены | 96, 180 | 100, 210 | 211, 93, 400, 243 | 215, 104, 398, 215 | 14 | 0 |
   | Ордосы | 48, 174 | 52, 207 | 211, 93, 400, 243 | 215, 104, 398, 215 | 14 | 11 |

   Плюс `CHECK` на все пары (`y`, `rightX`) обеих ломаных, значения — из `kAtreidesShoulderEdge` и `kOrdosShoulderEdge` пункта 1 контракта, записанные литералами; плюс константы: `MENTAT_HD_FRAME_WIDTH == 640`, `MENTAT_HD_FRAME_HEIGHT == 480`, `MENTAT_EYES_WIDTH == 96`, `MENTAT_EYES_HEIGHT == 32`, `MENTAT_MOUTH_WIDTH == 112`, `MENTAT_MOUTH_HEIGHT == 80`.
2. **`mentat HD layouts stay inside the 640x480 frame`** — для каждой раскладки пять `CHECK(insideFrame(...))`: глаза (`eyes.x`, `eyes.y`, `MENTAT_EYES_WIDTH`, `MENTAT_EYES_HEIGHT`), рот (`mouth.x`, `mouth.y`, `MENTAT_MOUTH_WIDTH`, `MENTAT_MOUTH_HEIGHT`), `sceneFrame`, `sceneOpening`.
3. **`mentat HD scene opening does not cover eyes and mouth`** — для каждой раскладки: `CHECK_FALSE(intersects(sceneOpening, <рамка глаз>))` и `CHECK_FALSE(intersects(sceneOpening, <рамка рта>))`, где рамка глаз — `{eyes.x, eyes.y, MENTAT_EYES_WIDTH, MENTAT_EYES_HEIGHT}`, рамка рта — `{mouth.x, mouth.y, MENTAT_MOUTH_WIDTH, MENTAT_MOUTH_HEIGHT}`.
4. **`mentat HD shoulder edges are monotonic and inside the opening`** — для Атрейдесов и Ордосов: для каждой соседней пары точек ломаной `CHECK(next.y > previous.y)` и `CHECK(next.rightX >= previous.rightX)`; `CHECK(first.y >= sceneOpening.y)` и `CHECK(last.y <= sceneOpening.y + sceneOpening.height)`.
5. **`mentat HD scene opening rows follow the fork`** — `sceneOpeningSpan(<раскладка>, <y>)`, `CHECK` на `left` и `right`, значения посчитаны по формулам форка (`round` как `std::lround`):

   | Раскладка | `y` → (`left`, `right`) |
   |---|---|
   | Атрейдесы | 114 → (0, 0); 115 → (276, 598); 200 → (276, 598); 290 → (276, 598); 296 → (286, 598); 300 → (290, 598); 333 → (314, 598); 334 → (0, 0) |
   | Ордосы | 103 → (0, 0); 104 → (229, 599); 117 → (216, 612); 118 → (215, 613); 200 → (215, 613); 290 → (240, 613); 300 → (248, 613); 305 → (251, 612); 318 → (261, 599); 319 → (0, 0) |
   | Харконнены | 103 → (0, 0); 104 → (229, 599); 118 → (215, 613); 200 → (215, 613); 305 → (216, 612); 318 → (229, 599); 319 → (0, 0) |
   | Бене | 104 → (229, 599); 118 → (215, 613); 305 → (216, 612); 318 → (229, 599) |

   Числа проверены скриптом по формулам форка; расхождение со значением из функции — не правка теста, а блок `## Q-P11-NN` и стоп.

**`tests/CMakeLists.txt`:** в `TEST_FILES` строка `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MentatHdLayout.cpp` сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MentatTextLayout.cpp`. `TEST_SOURCES` не меняется (в тесте только заголовок без `.cpp`).

## PLAN-P11

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/utils/test_MentatHdLayout.cpp`, `tests/CMakeLists.txt` | Раздел «Тесты». | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p11/build.log` стоит `.tmp/p11/red-build.log`, — `exit` не `0`, в логе есть строка с `test_MentatHdLayout.cpp` и `MentatHdLayout.hpp`. Запускается до того, как шаг 3 записал `src/gameobjects/mentat/MentatHdLayout.hpp`. | помощник A |
| 3 | `src/gameobjects/mentat/MentatHdLayout.hpp`, `src/gameobjects/mentat/AbstractMentat.h`, `src/gameobjects/mentat/AbstractMentat.cpp`, `src/gameobjects/mentat/AtreidesMentat.cpp`, `src/gameobjects/mentat/BeneMentat.cpp`, `src/gameobjects/mentat/HarkonnenMentat.cpp`, `src/gameobjects/mentat/OrdosMentat.cpp`, `src/drawers/SDLDrawer.hpp`, `src/drawers/SDLDrawer.cpp` | Пункты 1–9 контракта. | помощник B |
| 4 | — | Проверки раздела «Проверки» по порядку. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p11`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P11-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p11 && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p11/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345; строка `[P11]` в списке `ctest.log` — все случаи `Passed`.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает; в неё ничего не пиши.
2. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p11/changed-paths.txt` — пустой вывод. Файл `.tmp/p11/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1 и 3 плана, по одному на строку.
3. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_part2_catalog.py`, `ui_audit_part2_scenes.py`, `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p11/tmp && TMPDIR=$PWD/.tmp/p11/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p11/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part2_scenes.py` идёт по несколько минут — это норма.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
5. **Снимки сцен ментатов** (оценку вида делает ведущий; ты проверяешь только коды выхода, размеры файлов и размеры PNG). Для каждого `<сцена>` из списка: `mentat-briefing-atreides-speak`, `mentat-briefing-atreides-await`, `mentat-briefing-harkonnen-speak`, `mentat-briefing-ordos-speak`, `tellhouse-atreides-speak`, `mentat-briefing-sardaukar-speak` — команда
   `mkdir -p .tmp/p11/png .tmp/p11/xdg && (cd .tmp/out/run/bin && SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=/srv/library/dune/worktrees/p11/.tmp/p11/xdg LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 120 ./d2tm -windowed -screenWidth 1024 -screenHeight 768 --ui-audit-scene <сцена> --ui-audit-out /srv/library/dune/worktrees/p11/.tmp/p11/png > /srv/library/dune/worktrees/p11/.tmp/p11/png/<сцена>.run.log 2>&1; echo exit=$?)` — `exit=0`, а `python3 -c` с `ui_audit_runtime_support.png_size` (`sys.path.insert(0, 'tests/ui_audit')`) для файла `.tmp/p11/png/<сцена>.png` печатает `(1024, 768)`. В сдачу — пути шести PNG и их размеры в байтах (`stat -c %s`). Четыре ментата — Атрейдесы, Харконнены, Ордосы (сцены `mentat-briefing-*`) и Бене Гессерит (`tellhouse-atreides-speak`); `mentat-briefing-sardaukar-speak` — контроль: ментат Сардаукаров не меняется. В задании нет ни одной проверки вида глазами исполнителя.
6. **Сверки `grep`** (в скобках — ожидаемое число строк):
   - `git diff 6ceb29d1604ad0a487436bb9f1a0c60a746deeb6 -- src | grep -E '^\+.*(renderDrawer|game\.m_screen|game\.|uiaudit|UiAudit|localization::|SDL2/|logbook)'` (0);
   - `grep -rn 'clearRectToTransparent(' src` (3: объявление, определение, один вызов);
   - `grep -n 'm_hdLayout = &' src/gameobjects/mentat/AtreidesMentat.cpp src/gameobjects/mentat/BeneMentat.cpp src/gameobjects/mentat/HarkonnenMentat.cpp src/gameobjects/mentat/OrdosMentat.cpp` (4);
   - `grep -c 'drawMentatTexture(' src/gameobjects/mentat/AtreidesMentat.cpp src/gameobjects/mentat/BeneMentat.cpp src/gameobjects/mentat/HarkonnenMentat.cpp src/gameobjects/mentat/OrdosMentat.cpp` (по 2 у каждого);
   - `grep -c 'renderSprite(' src/gameobjects/mentat/AtreidesMentat.cpp src/gameobjects/mentat/BeneMentat.cpp src/gameobjects/mentat/HarkonnenMentat.cpp src/gameobjects/mentat/OrdosMentat.cpp` (по 0 у каждого);
   - `grep -c 'm_hdLayout' src/gameobjects/mentat/SardaukarMentat.cpp` (0);
   - `git diff 6ceb29d1604ad0a487436bb9f1a0c60a746deeb6 --stat -- src/gameobjects/mentat/SardaukarMentat.cpp src/gamestates src/CMakeLists.txt` — пустой вывод.
7. `git -c lfs.storage=$PWD/.tmp/p11/lfs status --short` — изменённые (` M`) пути — только пути шагов 1 и 3 плана; новые (`??`) — только `src/gameobjects/mentat/MentatHdLayout.hpp` и `tests/utils/test_MentatHdLayout.cpp`.

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P11-NN` с выводом и стоп. Ожидания существующих тестов и скрипты в `tests/ui_audit/` не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P11 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p11/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: строки `.tmp/p11/red-build.log` с `error` (не больше 30);
- вывод каждой проверки 1–7 с кодами выхода (не больше 40 строк на проверку); для проверки 5 — шесть строк `<сцена>: exit=<код>, <размер PNG>, <байт>` и пути PNG;
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. код: файлы шага 3.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …` (для кода: места глаз и рта четырёх ментатов сдвинуты на значения под HD-картины форка; кадр сцены ментата рисуется в окне форка; картина с прозрачным окном рисуется поверх сцены у ментатов с раскладкой; добавлен `SDLDrawer::clearRectToTransparent`; Сардаукары без изменений);
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p11 --size`; у `.tmp/p11` пометка `оставить — логи проверок и снимки нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A) и шаг 3 (помощник B) — одновременно; помощник B не создаёт `MentatHdLayout.hpp`, пока помощник A не записал в журнал хода строку о конце шага 2.
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 4 (помощник A) — после шагов 2 и 3.
  6. Сдача и стоп.
- **Параллельно:** шаги 1 и 3 правят разные файлы и идут одновременно; общий у них только порядок записи нового заголовка (пункт 3 порядка). Собирает их вместе проверка 1 шага 4.
- **Помощники:** два, `gpt-6-luna` `xhigh`, без вложенных. Ожидаемое время: помощник A — 40 минут на шаги 1–2 и 60 минут на шаг 4, помощник B — 50 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено» и «Контракт поведения»; его шаги плана; раздел «Тесты» и раздел «Проверки» — помощнику A; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p11/`.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P11` и на блоках `## Q-P11-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P11-NN` и стоп.
- **Рамка правок:** файлы шагов 1 и 3 плана и папка `.tmp/p11/`. Понадобился другой файл — блок `## Q-P11-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` и временные папки скриптов, снимки — в `.tmp/p11/png/`; это не правка.
- Данных LFS шаг не добавляет и не меняет: пак `sdl_mentat_hd4.dat`, картины сцен и остальные данные в рабочей копии остаются как в `B`; проверка 7 не должна показать ни одного пути в `resources/`.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
