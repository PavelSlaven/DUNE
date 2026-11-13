# Сверка разведки П11 (Haiku)

## Факт 1. fork-mentat.tsv, строка 2
- Утверждение таблицы: AbstractMentat::AbstractMentat — Инициализирует состояние ментата и параметры HD-композиции, стартовое окно сцены и кнопку выбора миссии.
- Ссылка в таблице: src/mentat/AbstractMentat.cpp@9208dcf:126-207
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AbstractMentat.cpp | sed -n '126,207p'`
- Вывод (первые до 12 строк; всего 82 строк):
```text
AbstractMentat::AbstractMentat(
    GameContext* ctx,
    bool canMissionSelect,
    int hdMissionSelectCenterX,
    float hdMissionTextOffsetY)
{
    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    m_hdMissionSelectCenterX = hdMissionSelectCenterX;
    m_textDrawer = ctx->getTextContext()->getMentatHdTextDrawer();
    iMentatSentence = -1;

    TIMER_Speaking = -1;
```
- Итог: совпало

## Факт 2. fork-mentat.tsv, строка 16
- Утверждение таблицы: AtreidesMentat::AtreidesMentat — Выбирает фон MENTATA, задаёт положение фильма и строит кнопки HD-консоли.
- Ссылка в таблице: src/mentat/AtreidesMentat.cpp@9208dcf:15-56
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/AtreidesMentat.cpp | sed -n '15,56p'`
- Вывод (первые до 12 строк; всего 42 строк):
```text
AtreidesMentat::AtreidesMentat(GameContext* ctx, bool allowMissionSelect)
    : AbstractMentat(ctx, allowMissionSelect, 537, 4.0F)
{
    iBackgroundFrame = MENTATA;
    // The movie is deliberately larger than the glass.  A cached alpha
    // foreground keeps the monitor frame and Cyril's shoulder above it.
    m_movieClipX = 276;
    m_movieClipY = 115;
    m_movieClipWidth = 322;
    m_movieClipHeight = 219;
    m_movieWidth = 400;
    m_movieHeight = 243;
```
- Итог: совпало

## Факт 3. fork-mentat.tsv, строка 29
- Утверждение таблицы: OrdosMentat::draw_mouth — Рисует рот по ID ORD_MOUTH01+iMentatMouth в точке (52,207) логического экрана.
- Ссылка в таблице: src/mentat/OrdosMentat.cpp@9208dcf:124-127
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/mentat/OrdosMentat.cpp | sed -n '124,127p'`
- Вывод (первые до 12 строк; всего 4 строк):
```text
void OrdosMentat::draw_mouth()
{
    drawMentatTexture(gfxmentat->getTexture(ORD_MOUTH01 + iMentatMouth), 52, 207);
}
```
- Итог: совпало

## Факт 4. port-mentat.tsv, строка 2
- Утверждение таблицы: AbstractMentat::AbstractMentat — Инициализирует состояние и начинается с iBackgroundFrame=-1; задаёт movieTopleftX=offsetX+256, movieTopleftY=offsetY+120.
- Ссылка в таблице: src/gameobjects/mentat/AbstractMentat.cpp@832c953:45-111
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/mentat/AbstractMentat.cpp | sed -n '45,111p'`
- Вывод (первые до 12 строк; всего 67 строк):
```text
AbstractMentat::AbstractMentat(GameContext* ctx, cGameSettings* settings, GameStateTransition* stateTransitions, MentatFlow* mentatFlow, bool canMissionSelect)
{
    d2tm_assert(ctx != nullptr);
    d2tm_assert(settings != nullptr);
    m_stateTransitions = stateTransitions;
    d2tm_assert(m_stateTransitions != nullptr);
    m_mentatFlow = mentatFlow;
    gfxmentat = ctx->getGraphicsContext()->gfxmentat.get();
    m_textDrawer = ctx->getTextContext()->getBeneTextDrawer();
    m_sdlDrawer = ctx->getSDLDrawer();
    iMentatSentence = -1;

```
- Примечание: Полный вывод 67 строк. Совпадения: строка вывода 23 — `iBackgroundFrame = -1;`; строки 64 и 65 — `movieTopleftX = offsetX + 256;`, `movieTopleftY = offsetY + 120;` (строки файла 67, 108, 109).
- Итог: совпало

## Факт 5. port-mentat.tsv, строка 46
- Утверждение таблицы: hunk: draw background rect — Использует MENTAT_SCREEN_W/H и m_sdlDrawer при рисовании фона.
- Ссылка в таблице: src/gameobjects/mentat/AbstractMentat.cpp@d06f2fc:284
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gameobjects/mentat/AbstractMentat.cpp | sed -n '284p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
    cRectangle dest = {offsetX, offsetY, MENTAT_SCREEN_W, MENTAT_SCREEN_H};
```
- Расхождение: таблица утверждает «MENTAT_SCREEN_W/H и m_sdlDrawer» для строки 284; в выводе строки 284 есть только `MENTAT_SCREEN_W`/`MENTAT_SCREEN_H`. `m_sdlDrawer` находится в строке 285 того же файла: `m_sdlDrawer->renderStrechFullSprite(tmp, dest);`.
- Итог: не совпало

## Факт 6. port-mentat.tsv, строка 79
- Утверждение таблицы: hunk: новый OrdosMentat.h — Добавляет декларацию наследника AbstractMentat.
- Ссылка в таблице: src/gameobjects/mentat/OrdosMentat.h@d06f2fc:1
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gameobjects/mentat/OrdosMentat.h | sed -n '1p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
/**
```
- Расхождение: таблица ссылается на строку 1 и утверждает декларацию наследника AbstractMentat; в строке 1 — комментарий шапки (`/**`). Класс `class OrdosMentat : public AbstractMentat {` находится в строке 20 того же файла. Предварительный прогон с диапазоном 1–14 тоже не содержал этой декларации.
- Итог: не совпало

## Факт 7. credits.tsv, строка 2
- Утверждение таблицы: cCreditsState::cCreditsState — Загружает resources/bin/data/hd4/credits_team.png@FORK1 и resources/bin/data/hd4/credits_title.png@FORK1 через loadHdUiTexture (src/gamestates/cCreditsState.cpp@FORK1:24-33); при отсутствии использует записи пака CREDITS_DUNE2_CORE_TEAM и D2TM_TITLE (src/gamestates/cCreditsState.cpp@FORK1:36-40).
- Ссылка в таблице: src/gamestates/cCreditsState.cpp@FORK1:18-74; src/gamestates/cCreditsState.h@FORK1:27
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/gamestates/cCreditsState.cpp | sed -n '18,74p'`
- Вывод (первые до 12 строк; всего 57 строк):
```text
cCreditsState::cCreditsState(cGame &theGame, GameContext* ctx) :
    cGameState(theGame, ctx),
    m_moveSpeed(0.15f),
    m_textDrawer(ctx->getTextContext()->getMenuTextDrawer())
{
    auto *gfxinter = ctx->getGraphicsContext()->gfxinter.get();
    m_teamBmp = loadHdUiTexture(
        "credits_team.png",
        m_game.getGraphicsDensity(),
        "HD credits team photo"
    );
    m_titleBmp = loadHdUiTexture(
```
- Итог: совпало

## Факт 8. credits.tsv, строка 19
- Утверждение таблицы: cCreditsState::onNotifyKeyboardEvent — Не рисует; MENU_BACK возвращает в меню.
- Ссылка в таблице: src/gamestates/cCreditsState.cpp@832c953:488-493; src/gamestates/cCreditsState.h@832c953:52
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 832c953a94a632d57872349013f7ed1a37434715:src/gamestates/cCreditsState.cpp | sed -n '488,493p'`
- Вывод (первые до 12 строк; всего 6 строк):
```text
void cCreditsState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (event.isType(eKeyEventType::PRESSED) && event.isAction(eKeyAction::MENU_BACK)) {
        m_stateTransitions->setNextStateWithFade(GAME_MENU);
    }
}
```
- Итог: совпало

## Факт 9. credits.tsv, строка 1137
- Утверждение таблицы: файл resources/hd/master4/sdl_data/0066_EXPLOSION_GAS.png — PNG-изображение; изменявшие коммиты=f1b8ea26; FORK1 git cat-file -s=131; FORK1 git cat-file -p, первая строка=version https://git-lfs.github.com/spec/v1; Git LFS pointer=да; FORK1 oid=ca8c2cb1ac96606fe7f4eecd1f8dc7ca62acf805; PORT oid=нет; объекты совпадают=не сравнить: объекта нет в одной из ревизий
- Ссылка в таблице: resources/hd/master4/sdl_data/0066_EXPLOSION_GAS.png@FORK1
- Команда: `git -C C:/Users/Slaven/Projects/DUNE cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/hd/master4/sdl_data/0066_EXPLOSION_GAS.png | head -3`
- Вывод (первые до 12 строк; всего 3 строк):
```text
version https://git-lfs.github.com/spec/v1
oid sha256:bdfd24f9542cae170b3cfaf6bd9925df28e29cf811527544bf36ae92061e3346
size 261027
```
- Примечание: строка таблицы — файл `resources/hd/master4/sdl_data/0066_EXPLOSION_GAS.png` (PNG, Git LFS); проверка по первой строке объекта.
- Итог: совпало

## Факт 10. intro.tsv, строка 2
- Утверждение таблицы: VideoFlow — Класс-обёртка для передачи запроса проигрывания в callback без зависимости от cGame.
- Ссылка в таблице: src/game/VideoFlow.hpp@d06f2fc:26
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/game/VideoFlow.hpp | sed -n '26p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
class VideoFlow {
```
- Итог: совпало

## Факт 11. intro.tsv, строка 14
- Утверждение таблицы: Кнопка Introduction проверяет intro.pak — Задаёт имя intro.pak и включает кнопку только если файл существует в рабочем каталоге игры.
- Ссылка в таблице: src/gamestates/cMainMenuState.cpp@d06f2fc:210-211
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cMainMenuState.cpp | sed -n '210,211p'`
- Вывод (первые до 12 строк; всего 2 строк):
```text
    const std::string introMoviePack = "intro.pak";
    const bool hasIntroMoviePack = std::filesystem::exists(introMoviePack);
```
- Итог: совпало

## Факт 12. intro.tsv, строка 25
- Утверждение таблицы: Файл данных intro.pak — Единственный явно указанный на диске файл ролика; в UP1 отсутствует по git ls-tree -r UP1 -- intro.pak.
- Ссылка в таблице: src/gamestates/cMainMenuState.cpp@d06f2fc:210
- Команда: `git -C C:/Users/Slaven/Projects/DUNE ls-tree -r d06f2fcd2a347182c3774fb96e9a85570405c489 -- intro.pak`
- Вывод (первые до 12 строк; всего 0 строк):
```text
(вывод пуст)
```
- Примечание: проверка отсутствия пути: пустой вывод `git ls-tree` соответствует утверждению таблицы «в UP1 отсутствует».
- Итог: совпало

## Факт 13. tests.tsv, строка 2
- Утверждение таблицы: Ожидает физическое HD-представление меню. — Ожидает физическое HD-представление меню.
- Ссылка в таблице: HD menu uses physical presentation; tests/HdPresentationTests.cpp@9208dcf:26
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '26p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
        shouldUsePhysicalHdPresentation(HdPresentationScene::Menu),
```
- Итог: совпало

## Факт 14. tests.tsv, строка 3
- Утверждение таблицы: Ожидает физическое HD-представление игрового процесса. — Ожидает физическое HD-представление игрового процесса.
- Ссылка в таблице: HD gameplay uses physical presentation; tests/HdPresentationTests.cpp@9208dcf:31
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '31p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
        shouldUsePhysicalHdPresentation(HdPresentationScene::Gameplay),
```
- Итог: совпало

## Факт 15. tests.tsv, строка 5
- Утверждение таблицы: Ожидает, что для старых неперенесённых экранов физическое HD-представление не используется. — Ожидает, что для старых неперенесённых экранов физическое HD-представление не используется.
- Ссылка в таблице: Unconverted legacy screens keep their current path; tests/HdPresentationTests.cpp@9208dcf:41
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '41p'`
- Вывод (первые до 12 строк; всего 1 строк):
```text
        shouldUsePhysicalHdPresentation(HdPresentationScene::Legacy),
```
- Итог: совпало

Итог: совпало 13 из 15
