# Выборочная сверка

Для каждого вызова Git перед командой выполнялся `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Помощник 1 — `port-mentat.tsv`

### 1. `AbstractMentat::thinkMovie`

Факт из строки таблицы (`src/gameobjects/mentat/AbstractMentat.cpp@832c953:168-182`): каждые 21 тика задаётся `iMovieFrame=(iMovieFrame+1) mod` число файлов сцены.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/mentat/AbstractMentat.cpp | sed -n '168,182p'
```

Фактический вывод:

```text
void AbstractMentat::thinkMovie()
{
    if (gfxmovie != nullptr) {
        TIMER_movie++;

        if (TIMER_movie > 20) {
            iMovieFrame++;

            if (iMovieFrame == gfxmovie->getNumberOfFiles()) {
                iMovieFrame = 0;
            }
            TIMER_movie = 0;
        }
    }
}
```

Итог: **совпало**.

### 2. `AtreidesMentat::draw_eyes`

Факт из строки таблицы (`src/gameobjects/mentat/AtreidesMentat.cpp@832c953:73-76`): рисует кадр `ATR_EYES01+iMentatEyes` с левым верхним углом `(offsetX+80, offsetY+241)`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/mentat/AtreidesMentat.cpp | sed -n '73,76p'
```

Фактический вывод:

```text
void AtreidesMentat::draw_eyes()
{
    m_sdlDrawer->renderSprite(gfxmentat->getTexture(ATR_EYES01+ iMentatEyes),  offsetX + 80, offsetY + 241);
}
```

Итог: **совпало**.

### 3. `SardaukarMentat::draw_eyes`

Факт из строки таблицы (`src/gameobjects/mentat/SardaukarMentat.cpp@832c953:71-74`): реализация пустая, глаза не рисуются, вызов `renderSprite` закомментирован.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 832c953a94a632d57872349013f7ed1a37434715:src/gameobjects/mentat/SardaukarMentat.cpp | sed -n '71,74p'
```

Фактический вывод:

```text
void SardaukarMentat::draw_eyes()
{
    //m_sdlDrawer->renderSprite(gfxmentat->getTexture(ORD_EYES01+ iMentatEyes), offsetX + 32, offsetY + 240);
}
```

Итог: **совпало**.

## Помощник 2 — `tests.tsv`

### 4. HD-представление меню

Факт из строки таблицы (`tests/HdPresentationTests.cpp@9208dcf:26`): тест ожидает физическое HD-представление меню.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '24,28p'
```

Фактический вывод:

```text
    passed &= expectEqual(
        "HD menu uses physical presentation",
        shouldUsePhysicalHdPresentation(HdPresentationScene::Menu),
        true
    );
```

Итог: **совпало**.

### 5. HD-представление игрового процесса

Факт из строки таблицы (`tests/HdPresentationTests.cpp@9208dcf:31`): тест ожидает физическое HD-представление игрового процесса.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '29,33p'
```

Фактический вывод:

```text
    passed &= expectEqual(
        "HD gameplay uses physical presentation",
        shouldUsePhysicalHdPresentation(HdPresentationScene::Gameplay),
        true
    );
```

Итог: **совпало**.

### 6. HD-представление ментата после выбора Дома

Факт из строки таблицы (`tests/HdPresentationTests.cpp@9208dcf:36`): тест ожидает физическое HD-представление сцены Mentat после выбора Дома.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/HdPresentationTests.cpp | sed -n '34,38p'
```

Фактический вывод:

```text
    passed &= expectEqual(
        "HD post-House Mentat uses physical presentation",
        shouldUsePhysicalHdPresentation(HdPresentationScene::Mentat),
        true
    );
```

Итог: **совпало**.

## Помощник 3 — `intro.tsv`

### 7. Проверка файла `intro.pak`

Факт из строки таблицы (`src/gamestates/cMainMenuState.cpp@d06f2fc:210-211`): задаётся имя `intro.pak`, а наличие файла проверяется через файловую систему.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cMainMenuState.cpp | sed -n '210,211p'
```

Фактический вывод:

```text
    const std::string introMoviePack = "intro.pak";
    const bool hasIntroMoviePack = std::filesystem::exists(introMoviePack);
```

Итог: **совпало**.

### 8. Запуск ролика кнопкой Introduction

Факт из строки таблицы (`src/gamestates/cMainMenuState.cpp@d06f2fc:214,219,221`): клик вызывает `videoFlow->play("intro.pak")`, и кнопка доступна при наличии файла.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cMainMenuState.cpp | sed -n '214,221p'
```

Фактический вывод:

```text
            .withLabel("Introduction")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(hasIntroMoviePack ? cGuiThemeBuilder().light().build() : cGuiThemeBuilder().inactive().build())
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .onClick([this, introMoviePack](){m_videoFlow->play(introMoviePack);})
            .build();
        gui_btn_Intro->setEnabled(hasIntroMoviePack);
```

Итог: **совпало**.

### 9. Чтение кадров видеосостоянием

Факт из строки таблицы (`src/gamestates/cVideoState.cpp@d06f2fc:80-88`): `thinkNormal` выдаёт кадры по одному, затем ставит переход с затемнением в `GAME_MENU`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cVideoState.cpp | sed -n '80,88p'
```

Фактический вывод:

```text
void cVideoState::thinkNormal()
{
    // one frame per call: thinkNormal runs every ~100 ms, so the video plays at 10 fps
    if (m_movieFrame < m_gfxMovie->getNumberOfFiles()) {
        m_currentFrame = m_gfxMovie->getTexture(m_movieFrame);
        m_movieFrame++;
    } else {
        m_stateTransitions->setNextStateWithFade(GAME_MENU);
    }
```

Итог: **совпало**.
