# Разведка P4B-R: масштаб игры

Ревизии: FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566, PORT = ce0cacfb3ba425c8c831b52b64769186a835bdbb, MAIN = ac3244d12bed5b4b25c24605c162a33938cfa982. Все чтения Git ниже выполнены с явной ревизией; дерево рабочей копии не переключалось.

## Чтение

До разведки прочитаны отдельными вызовами:

- git show MAIN:docs/upstream/PORT_PLAN.md — вывод целиком. План говорит, что П4б переносит RenderScale вместо фиксированного ScreenWidth × ScreenHeight и ScalingMode; строки настройки «Масштаб игры» и «Размер объектов» перенесены в П5, запись WorldScale в preferences.ini — в П8 (PORT_PLAN.md@MAIN:88–90).
- git show MAIN:codex-direct/P4/TASK.md — первый вывод был обрезан, после чего весь файл дочитан тремя отдельными вызовами: git show ... | sed -n '1,64p', '65,145p' и '146,231p'. Задание П4а оставляет ScreenWidth/ScreenHeight и ScalingMode как в апстриме, добавляет density frame targets и задаёт вызов worldScaleZoom(WorldScale, m_screenH); в списке «Не делать» RenderScale и экранные настройки отнесены к П4б, строки меню — к П5 (TASK.md@MAIN:11–15, 96–104).
- git show MAIN:docs/decisions.md | grep -E '^- \*\*Р(33|34|63|66)\.' — вывод полностью:
  ~~~text
  - **Р33. Масштаб мира — это приближение камеры (#38).** Владелец 2026-11-02: «Масштаб = приближение». Масштаб мира (100, 110, 125, 150 % или авто) задаёт приближение камеры в начале миссии и после сброса клавишей Z; спрайты зданий, юнитов, частиц и снарядов на него больше не умножаются, поэтому земля, клетки и объекты увеличиваются вместе и здание стоит ровно на своих клетках. Спецификация — codex-direct/U15/SPEC.md.
  - **Р34. Только HD-графика (#49).** Владелец 2026-11-02: «надо оставить только одну версию графики, максимальную. Остальные убрать просто». Игра всегда загружает паки HD4; режим «Классика», его выбор в окне настроек и откат на классические паки удалены; классические паки остаются в репозитории только как эталон для инструментов и в пакет игры не попадают.
  - **Р63. Волна 4 — перенос форка на свежий апстрим.** Графика и перерисовка закончены; задача волны — перенести всё на новый код апстрима, сохранив наработки форка (Р4). Новая база UP1 — master апстрима в момент запуска первой задачи, d06f2fcd на 2026-11-09. Новые возможности апстрима (туман войны с памятью, значок нехватки энергии, предел юнитов, вступительный ролик, preferences.ini, папки музыки) берутся как есть; где новинка спорит с функцией форка, ведущий спрашивает владельца на шаге этой функции. Новых задач по графике нет; код и данные игры в main не меняются до перемотки на ветку порта, в main идут только документы процесса и карта переноса. Шаги П1–П15 — по карточке codex-direct/launch-card-27.md. Владелец, 2026-11-09, по карточке 27: «Свежий master», «Все как есть», «Мы закончили с графикой и перерисовкой. Теперь задача всё перенести на их новый код, сохранив наши наработки.»
  - **Р66. П4б: «Масштаб игры» форка вместо фиксированного размера и ScalingMode апстрима.** Логический холст игры = размер экрана / процент масштаба (RenderScale форка): ручные значения 100–200 % и «Авто» по высоте экрана. Фиксированный логический размер ScreenWidth × ScreenHeight и режимы ScalingMode (IntegerScale / Letterbox) апстрима UP1 не переносятся как способ масштабирования: с одними HD4-паками (Р34) целочисленное увеличение кадра смысла не имеет, а адаптивным меню П5 нужен холст переменного размера. Шаг П4б делается после приёмки П4а. Владелец, 2026-11-10, на вопрос «П4б: берём «Масштаб игры» форка (холст = экран / процент, 100–200 % и «Авто») или фиксированный размер апстрима с ScalingMode? Рекомендую форк.»: «Да. По рекомендациям».
  ~~~
  Печатные строки решений в файле: decisions.md@MAIN:41–42, 92, 95. Решение Р33 прямо ссылается на U15/SPEC.md.
- Дополнительно прочитаны ссылки плана, которые задают путь переноса и проверок: docs/PLAN_units_sega_upstream.md §3.2 и §5.3 (команда git show MAIN:docs/PLAN_units_sega_upstream.md | sed -n '90,109p;201,215p'); docs/upstream/PORT_MAP.md, разделы hd-render и world-scale (git show MAIN:docs/upstream/PORT_MAP.md | sed -n '152,310p'); codex-direct/launch-card-27.md целиком (план П2–П15 выполняется без новой карточки, если не меняются рамка и подход); codex-direct/U15/SPEC.md целиком (спецификация Р33 считает AutoWorldScale от outputHeight и описывает масштаб мира как зум камеры). Эти документы не перечислены в обязательном чтении задания, но на них прямо ссылаются PORT_PLAN.md и Р33.

## 1. Логический размер и представление окна в PORT

### Источники и хранение значений

Команда:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'ScreenWidth|ScreenHeight|FullScreen|ScalingMode|screenW =|screenH =|windowed =|scalingMode =|SCREENX|SCREENY' ce0cacfb3ba425c8c831b52b64769186a835bdbb -- src resources/bin/settings.ini
~~~

Фрагмент фактического вывода:
~~~text
resources/bin/settings.ini:3:ScreenWidth=1024
resources/bin/settings.ini:4:ScreenHeight=768
resources/bin/settings.ini:10:FullScreen=false
resources/bin/settings.ini:13:ScalingMode=IntegerScale
src/utils/InitialGameSettings.hpp:22:    int screenW = 800;
src/utils/InitialGameSettings.hpp:23:    int screenH = 600;
src/utils/InitialGameSettings.hpp:27:    bool windowed = false;
src/utils/InitialGameSettings.hpp:28:    eScalingMode scalingMode = eScalingMode::INTEGER_SCALE;
src/utils/cHandleArgument.cpp:116:                    settings->screenW = std::stoi(argv[i]);
src/utils/cHandleArgument.cpp:124:                    settings->screenH = std::stoi(argv[i]);
src/game/cGame_logic.cpp:771:    m_gameSettings->m_screenW = m_Screen->Width();
src/game/cGame_logic.cpp:772:    m_gameSettings->m_screenH = m_Screen->Height();
~~~

Preferences::readSettings читает ScreenWidth, ScreenHeight, FullScreen и ScalingMode при наличии ключей (src/game/Preferences.cpp@ce0cacfb:47–68); FullScreen сохраняется в поле windowed как инвертированный флаг. Значения по умолчанию screenW=800, screenH=600, windowed=false, ScalingMode=INTEGER_SCALE заданы в InitialGameSettings (src/utils/InitialGameSettings.hpp@ce0cacfb:22–28). CLI переопределяет начальные значения: -screenWidth/-screenHeight в cHandleArgument.cpp:113–124, -windowed/-fullscreen и -integerscale/-letterbox в :74–83. main.cpp сначала читает settings.ini, только с флагом -prefs подмешивает пользовательский preferences.ini, затем разбирает CLI (src/main.cpp@ce0cacfb:74–90).

Поля m_screenW и m_screenH находятся в cGameSettings; они получают начальные параметры и затем итоговый размер SDL (src/game/cGameSettings.h@ce0cacfb:28–32, 144–145; src/game/cGame_logic.cpp@ce0cacfb:303, 306, 771–772). cSDLSystem хранит renderResolution, windowResolution и usableResolution (src/game/cSDLSystem.h@ce0cacfb:71–73). m_screenW/H и getScreenW/H сейчас являются логическим размером renderResolution: Width()/Height() возвращают его компоненты (cSDLSystem.h@ce0cacfb:48–53), а SDL_SetRenderLogicalPresentation получает renderResolution.width/height.

### Создание окна и логическое представление

Команда:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'SDL_CreateWindow|SDL_SetRenderLogicalPresentation' ce0cacfb3ba425c8c831b52b64769186a835bdbb -- src
~~~

Фактический вывод:
~~~text
src/game/cSDLSystem.cpp:53:        SDL_SetRenderLogicalPresentation(renderer, renderResolution.width, renderResolution.height, SDL_LOGICAL_PRESENTATION_INTEGER_SCALE);
src/game/cSDLSystem.cpp:65:        SDL_SetRenderLogicalPresentation(renderer, renderResolution.width, renderResolution.height, SDL_LOGICAL_PRESENTATION_LETTERBOX);
src/game/cSDLSystem.cpp:110:    SDL_SetRenderLogicalPresentation(renderer, renderResolution.width, renderResolution.height, SDL_LOGICAL_PRESENTATION_LETTERBOX);
src/game/cSDLSystem.cpp:301:    window = SDL_CreateWindow(title.c_str(), renderResolution.width, renderResolution.height, 0);
src/game/cSDLSystem.cpp:340:    SDL_SetRenderLogicalPresentation(renderer, renderResolution.width, renderResolution.height, SDL_LOGICAL_PRESENTATION_LETTERBOX);
src/drawers/SDLDrawer.cpp:324:        SDL_SetRenderLogicalPresentation(renderer, width, height, SDL_LOGICAL_PRESENTATION_STRETCH);
~~~

Вызовы в cSDLSystem.cpp:53 и :65 относятся к fullscreen-представлению по выбранному ScalingMode (IntegerScale либо Letterbox); :110 — оконный режим, всегда Letterbox; :340 — начальное представление, Letterbox. При высокой density SDLDrawer задаёт целевой текстуре своё STRETCH-представление (:324). SDL_CreateWindow передаёт флаги 0 (:301), SDL_WINDOW_HIGH_PIXEL_DENSITY не включён.

До создания окна cSDLSystem вычисляет renderResolution из желаемого размера, минимумов 800×600 и границ дисплея (cSDLSystem.cpp@ce0cacfb:35–36, 145–165, 200–232). Оконный размер подгоняется к usable bounds; после создания берётся SDL_GetRenderOutputSize и обновляется renderResolution, если физический output не меньше минимумов (:174–198). В fullscreen presentation использует renderResolution; фактический fullscreen output берётся из renderer. При переключении fullscreen событие SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED повторно применяет presentation, но не меняет renderResolution или m_screenW/H (cGame_logic.cpp@ce0cacfb:595–596; cSDLSystem.cpp@ce0cacfb:98–103). Создание окна в :301 получает размеры renderResolution и флаги 0.

### Клавиши, меню и сохранение

Команда и вывод для обработчиков:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show ce0cacfb3ba425c8c831b52b64769186a835bdbb:src/game/cGame_logic.cpp | nl -ba | sed -n '1548,1563p'
~~~
~~~text
1548    if (event.isAction(eKeyAction::TOGGLE_FULLSCREEN)) {
1549        if (m_windowed) {
1550            m_Screen->setFullScreenMode();
1551            m_windowed = false;
1552        } else {
1553            m_Screen->setWindowMode();
1554            m_windowed = true;
1555        }
1556    }
1558    if (event.isAction(eKeyAction::TOGGLE_SCALING_MODE)) {
1559        m_Screen->toggleScalingMode();
1560        m_scalingMode = m_Screen->getScalingMode();
1561        auto message = std::format("Scaling mode: {}", m_scalingMode == eScalingMode::INTEGER_SCALE ? "Integer scale" : "Letterbox");
1562        m_notificationArea->addNotification(message, eNotificationType::NEUTRAL);
~~~

Клавиша TOGGLE_FULLSCREEN (Alt+Return) переключает оконный/fullscreen режим сразу. TOGGLE_SCALING_MODE (Alt+L) меняет между IntegerScale и Letterbox и выводит сообщение (cKeyBindings.cpp@ce0cacfb:34–35; cGame_logic.cpp@ce0cacfb:1548–1562; settings.ini@ce0cacfb:105–106). В меню cOptionsState нет строк resolution, ScreenWidth/Height, FullScreen или ScalingMode; команда git grep -n -i -E 'ScreenWidth|ScreenHeight|FullScreen|ScalingMode|IntegerScale|Letterbox|resolution' PORT -- src/gamestates/cOptionsState.cpp совпадений не дала. Функция Preferences::save при обычном завершении записывает ScreenWidth, ScreenHeight, FullScreen и ScalingMode в пользовательский preferences.ini (Preferences.cpp@ce0cacfb:149–165; main.cpp@ce0cacfb:110–118). resources/bin/settings.ini остаётся исходным файлом настроек.

### Преобразование мыши

Команда:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'SDL_RenderCoordinatesFromWindow|SDL_RenderCoordinatesToWindow|SDL_ConvertEventToRenderCoordinates|SDL_ConvertEventToRender' ce0cacfb3ba425c8c831b52b64769186a835bdbb -- src
~~~

Фактический вывод по активным SDL преобразованиям:
~~~text
src/controls/cMouse.cpp:83  SDL_RenderCoordinatesFromWindow(renderer, event.button.x, event.button.y, &px, &py)
src/controls/cMouse.cpp:98  SDL_RenderCoordinatesFromWindow(renderer, event.button.x, event.button.y, &px, &py)
src/controls/cMouse.cpp:125 SDL_RenderCoordinatesFromWindow(renderer, event.motion.x, event.motion.y, &px, &py)
src/controls/cMouse.cpp:213 SDL_RenderCoordinatesToWindow(..., &wx, &wy)
src/controls/cMouse.cpp:214 SDL_WarpMouseInWindow(_windows, wx, wy)
~~~

Нажатие, отпускание и движение мыши преобразуются в renderer coordinates; при центрировании курсора используется обратное преобразование до SDL_WarpMouseInWindow (cMouse.cpp@ce0cacfb:77–130, 210–219). В PORT не найден вызов SDL_ConvertEventToRenderCoordinates. Дальше логические координаты переводятся в области игры/карты: проверка sidebar/topbar и cells — cGameControlsContext.cpp@ce0cacfb:86–123; камера вычитает topbar, делит на zoom и учитывает viewport — cMapCamera.h@ce0cacfb:111–118; minimap переводит координаты относительно рамки в координаты карты — cMiniMapDrawer.cpp@ce0cacfb:510–521; редактор и региональная карта имеют собственные преобразования — cEditorCam.cpp@ce0cacfb:100–108 и cSelectYourNextConquestState.cpp@ce0cacfb:577–586.

### Density targets и изменение размера

cSDLSystem::frameDensity читает SDL_GetRenderLogicalPresentationRect и сравнивает rect.w/rect.h с renderResolution (cSDLSystem.cpp@ce0cacfb:250–258). calculateFrameDensity берёт минимум отношений presentation/logical и округляет scale−0.01 вверх, ограничивая density диапазоном 1–4 (Graphics.hpp@ce0cacfb:70–78). ensureFrameTargets вызывается до цикла и перед каждым кадром; при изменении density пересоздаёт actualRenderer и screenTexture размером m_screenW × m_screenH (cGame_logic.cpp@ce0cacfb:572, 623, 638–661). Target texture физически имеет width*density × height*density; при density>1 SDLDrawer устанавливает STRETCH logical presentation (SDLDrawer.cpp@ce0cacfb:309–327). При изменении только логической ширины/высоты и сохранении density текущий ensureFrameTargets не пересоздаёт текстуры, потому что ранний возврат проверяет только actualRenderer->density (:642–648).

## 2. Потребители и места хранения логического размера в PORT

Полный список чтений m_screenW/m_screenH, getScreenW()/getScreenH() и известных мест хранения/кэширования находится в .tmp/p4br/screen-size-uses.tsv. Команда поиска прямых потребителей: git grep -n -E 'm_screenW|m_screenH|getScreenW\\(|getScreenH\\(' ce0cacfb3ba425c8c831b52b64769186a835bdbb -- src. Результат после разбора содержит 249 строк данных, 234 уникальные ссылки на 67 файлов; файл проверен по каждой ссылке командой git show PORT:<path>. Из 249 строк 69 вызовов getScreenW(), 51 getScreenH(), 12 прямых чтений m_screenW/H, 2 чтения через getWorldScaleFactor(); остальные строки фиксируют поля и кэши размеров/viewport/render targets/layout.

Примеры вывода TSV:
~~~text
src/game/cGame_logic.cpp@ce0cacfb:650 m_screenW/H -> создание actualRenderer размерами логического холста с density; при запуске/изменении density
src/game/cGame_logic.cpp@ce0cacfb:651 m_screenW/H -> создание screenTexture размерами логического холста с density; при запуске/изменении density
src/game/cGame.h@ce0cacfb:101 m_mapViewport -> хранит игровой логический viewport; создаётся из screenW/H
src/gameobjects/map/cMapCamera.h@ce0cacfb:236–237 m_windowWidth/m_windowHeight -> кэширует размер карты после вычета sidebar/topbar
src/gamestates/cSetupSkirmishState.cpp@ce0cacfb:148–149 screen_x/screen_y -> сохраняет размеры для раскладки skirmish
src/gamestates/cOptionsState.cpp@ce0cacfb:70 m_guiWindow -> GUI раскладка, созданная с учётом screenW/H
src/gamestates/cCreditsState.cpp@ce0cacfb:68–70 backButtonRect -> прямоугольник кнопки действительно передаётся в GuiButtonBuilder::withRect
src/include/Texture.hpp@ce0cacfb:34–38 w/h/pixelW/pixelH/density -> хранит логический и backing размер текстуры
src/game/cSDLSystem.h@ce0cacfb:71 renderResolution -> хранит итоговый логический размер renderer
~~~

Числовые кандидаты из src/ помещены в .tmp/p4br/screen-size-literals.tsv. Таблица содержит 20 строк: defaults 800×600, минимумы рендера 800×600, холсты/фиксированные рамки Mentat и меню, размер регионального ресурса, целевой прямоугольник cutscene и пороги WorldScale. Для каждого отдельно указано, является ли число размером всего экрана. Пороги 768/1080/1600 — пороги логической высоты, переданной WorldScale, а не физическая высота дисплея.

Примеры получения вывода:
~~~sh
head -n 8 .tmp/p4br/screen-size-uses.tsv
head -n 8 .tmp/p4br/screen-size-literals.tsv
wc -l .tmp/p4br/screen-size-uses.tsv .tmp/p4br/screen-size-literals.tsv
~~~

## 3. Реализация RenderScale в FORK1

RenderScale.hpp задаёт RenderCanvasSize (defaulted operator==), MinimumRenderWidth=800, MinimumRenderHeight=600, AutomaticRenderScale=0 и ManualRenderScales={100,125,150,175,200} (src/utils/RenderScale.hpp@9208dcf:5–27). RenderScale.cpp содержит normalizedOutputWidth/Height (std::max к минимумам), automaticRenderScale (min(normalizedWidth/800, normalizedHeight/600)), calculateAutomaticRenderScalePercent (std::lround(scale*100)), isManualRenderScaleAvailable и calculateRenderCanvasSize (src/utils/RenderScale.cpp@9208dcf:7–73). Ручное значение доступно, только если оно перечислено и при делении обеих сторон выходного размера на процент холст не станет меньше 800×600; сравнение целочисленное с расширением до long long (:32–49). При Auto и допустимом ручном значении ширина и высота холста делятся на scale, округляются std::lround и ограничиваются минимумами (:51–73). Недопустимое ручное значение ведёт к автоматическому масштабу. Положительные полуцелые значения lround округляет от нуля.

Команда и фактический вывод вызовов RenderScale:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'calculateRenderCanvasSize|calculateAutomaticRenderScalePercent|isManualRenderScaleAvailable|RenderScale|SDL_RenderSetLogicalSize|SDL_SetWindowFullscreen' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src
~~~
Основные места: cScreenInit::adaptResolution рассчитывает outputResolution и renderResolution; SDL_SetRenderLogicalSize получает canvas width/height при создании и смене оконного режима (src/utils/cScreenInit.cpp@9208dcf:59–95, 149–198, 13–46). ScreenWidth/ScreenHeight в settings.ini — желаемый output size. В оконном режиме окно подгоняется к usable bounds и не превышает output size; fullscreen использует SDL_WINDOW_FULLSCREEN_DESKTOP, то есть режим рабочего стола, а не выбранное разрешение ScreenWidth/Height (cScreenInit.cpp@9208dcf:13–46, 125–147, 149–198). В игре cGame::applySettings передаёт выбранную высоту выходного разрешения в WorldScale, затем cGame_logic сохраняет cScreenInit::Width/Height как m_screenW/H; при RenderScale это логический холст, а не размер окна (cGame_logic.cpp@9208dcf:185–195, 1075–1087; cScreenInit.h@9208dcf:33–38).

В настройках FORK1 есть строки «Разрешение», «Масштаб игры» и «Полноэкранный режим» (cOptionsState.cpp@9208dcf:1066–1068, 1134–1137, 1272–1275). Стрелки разрешения меняют выбранный output size; после смены списка масштабов доступные ручные значения пересобираются (cOptionsState.cpp@9208dcf:227–255, 257–275). Строка «Масштаб игры» показывает Auto как фактический процент либо выбранное ручное значение (cOptionsState.cpp@9208dcf:576–599). Checkbox полноэкранного режима меняет выбранный флаг; сохранение записывает ScreenWidth/Height, FullScreen, RenderScale и WorldScale в settings.ini и показывает сообщение о необходимости перезапуска (cOptionsState.cpp@9208dcf:707–758).

Фактический вывод строк меню:
~~~text
1067 .withLabel(optionText(m_selectedSettings, "Resolution", "Разрешение"))
1135 .withLabel(optionText(m_selectedSettings, "Game scale", "Масштаб игры"))
1273 .withLabel(optionText(m_selectedSettings, "Fullscreen", "Полноэкранный режим"))
737 .setText(optionText(m_selectedSettings, "Saved. Restart the game.", "Сохранено. Перезапустите игру."))
~~~

Options menu строит список ручных значений по текущей паре разрешения/масштаба; недоступные значения не показываются и при загрузке заменяются Auto (cOptionsState.cpp@9208dcf:227–255; cScreenInit.cpp@9208dcf:70–95). Изменение экранных параметров в меню сохраняет settings.ini и показывает «Сохранено. Перезапустите игру»; окно, renderer и screen-sized targets пересоздаются при следующем запуске, а камера читает выбранный world scale при создании/сбросе (cOptionsState.cpp@9208dcf:707–758; cGame_logic.cpp@9208dcf:1075–1101, 721–722; cMapCamera.cpp@9208dcf:44, 72). Alt+Enter переключает fullscreen без перезапуска (cGame_logic.cpp@9208dcf:2142–2149).

Команда требуемого журнала коммитов и вывод:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git log --format='%h %s' e17379ad660fca46859b403a6c3d33ec8d831a40..9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/utils/RenderScale.cpp src/utils/RenderScale.hpp tests/RenderScaleTests.cpp
~~~
~~~text
f1b8ea26 Publish RU/HD remaster source and assets
~~~

## 4. WorldScale и HD-рендер при переменном холсте

В FORK1 нет worldScaleZoom. applySettings один раз вызывает resolveWorldScalePercent(..., gs->screenH), где gs->screenH на этом этапе — высота выбранного output-разрешения; камера использует полученный масштаб при создании и сбросе (src/cGame_logic.cpp@9208dcf:185–195; src/map/cMapCamera.cpp@9208dcf:44,72). Auto пороги 768, 1080, 1600 заданы в WorldScale.cpp@9208dcf:13–37. Р33 спецификация также описывает outputHeight как высоту для AutoWorldScale (codex-direct/U15/SPEC.md@MAIN:14–18).

В PORT worldScaleZoom вызывается из cGameSettings::getWorldScaleFactor с m_screenH (src/game/cGameSettings.h@ce0cacfb:34–35); m_screenH получает m_Screen->Height() (cGame_logic.cpp@ce0cacfb:771–772), а Height() возвращает renderResolution.height (cSDLSystem.h@ce0cacfb:48–53). Сейчас это фиксированный логический размер PORT. После RenderScale этот вызов продолжит видеть переменный логический холст, если не изменить аргумент. В PORT WorldScale отсутствует в settings.ini; default 0 (Auto) задаётся InitialGameSettings (resources/bin/settings.ini@ce0cacfb; InitialGameSettings.hpp@ce0cacfb:21–29).

В FORK1 физическая цель HD-рендера берёт renderer output size, тогда как RenderScale отдельно задаёт логический SDL2 холст. HD presentation включён для сцен кроме Legacy (HdPresentation.hpp@9208dcf:42–46); цель выбирается игровым циклом и размеры получает через SDL_GetRendererOutputSize (cGame_logic.cpp@9208dcf:764–779, 808–849). Поэтому RenderScale меняет логический размер/геометрию, но не размер физической цели.

Canvas-формулы скрипта повторяют RenderScale.cpp@9208dcf:7–73, WorldScale.hpp@ce0cacfb:9–40 и calculateFrameDensity@PORT Graphics.hpp:70–78. Скрипт .tmp/p4br/canvas.py содержит ссылки на строки рядом с каждой формулой; таблица — .tmp/p4br/canvas.tsv.

Команда запуска и фактический вывод:
~~~sh
/srv/dune/venv/bin/python .tmp/p4br/canvas.py
~~~
~~~text
Разрешение	Масштаб	Холст FORK1	Ручной масштаб доступен	Зум мира PORT (WorldScale=0, высота холста)	Плотность кадра PORT
1366×768	Авто	1067×600	—	1	2
1366×768	100	1366×768	да	1	1
1366×768	125	1093×614	да	1	2
1366×768	150	1067×600	нет	1	2
1366×768	175	1067×600	нет	1	2
1366×768	200	1067×600	нет	1	2
1920×1080	Авто	1067×600	—	1	2
1920×1080	100	1920×1080	да	1.1	1
1920×1080	125	1536×864	да	1.1	2
1920×1080	150	1280×720	да	1	2
1920×1080	175	1097×617	да	1	2
1920×1080	200	1067×600	нет	1	2
2560×1440	Авто	1067×600	—	1	3
2560×1440	100	2560×1440	да	1.25	1
2560×1440	125	2048×1152	да	1.25	2
2560×1440	150	1707×960	да	1.1	2
2560×1440	175	1463×823	да	1.1	2
2560×1440	200	1280×720	да	1	2
3840×2160	Авто	1067×600	—	1	4
3840×2160	100	3840×2160	да	1.5	1
3840×2160	125	3072×1728	да	1.5	2
3840×2160	150	2560×1440	да	1.25	2
3840×2160	175	2194×1234	да	1.25	2
3840×2160	200	1920×1080	да	1.1	2
~~~

## 5. Тесты

RenderScaleTests.cpp@9208dcf:36–43 проверяет canvas:
~~~text
800×600 Auto -> 800×600
1024×768 Auto -> 800×600
1280×720 Auto -> 1067×600
1920×1080 Auto -> 1067×600
1920×1080 100% -> 1920×1080
1920×1080 175% -> 1097×617
2560×1440 Auto -> 1067×600
5120×1440 Auto -> 2133×600
~~~
В RenderScaleTests.cpp:45–56 ожидаются AutoPercent=180 при 1920×1080, доступность 175% и недоступность 200% при том же выходе. CMakeLists.txt@9208dcf:199–209 создаёт CMake target render_scale_tests из RenderScaleTests.cpp и RenderScale.cpp; CTest-имя render_scale_calculations. Тест включает utils/RenderScale.hpp, <format>, <iostream>, <string_view>; использует RenderCanvasSize, calculateRenderCanvasSize, calculateAutomaticRenderScalePercent и isManualRenderScaleAvailable; в PORT нет RenderScale.hpp и этих проектных символов. <format>, <iostream> и <string_view> — стандартные заголовки C++, не файлы проекта.

Другой форк-тест с RenderScale.hpp: OptionsMenuLayoutTests.cpp, target options_menu_layout_tests / CTest options_menu_layout_geometry (CMakeLists.txt@9208dcf:224–236). Проверяет геометрию, границы, отступы и пересечения меню на стандартных, нестандартных и ручных холстах (OptionsMenuLayoutTests.cpp@9208dcf:295–365).

PORT:
- tests/utils/test_HdRender.cpp — P4 frame density rounds the presentation scale up (строки 206–216) проверяет отношения с фиксированным логическим размером 1024×768.
- P4 render target with density keeps logical size and physical pixels (:218–268) проверяет логический холст 8×4, backing 16×8 при density 2, STRETCH 8×4; при density 1 — DISABLED.
- P4 HD frame target keeps detail finer than a logical pixel и P4 nested render target keeps the frame target state (:270–345) опираются на холсты 8×8, проверяют детализацию density 2/1 и восстановление вложенной цели/presentation.
- tests/utils/test_Preferences.cpp, Preferences - saved settings load back identical (:25–66) сохраняет/загружает LETTERBOX.
- tests/utils/test_cHandleArgument.cpp:53–60 ожидает INTEGER_SCALE по умолчанию; :171–176 проверяет разбор -windowed/-fullscreen (последний аргумент побеждает); :178–185 проверяет -letterbox/-integerscale. Игровой переход в fullscreen не проверяется.
- Тест PORT на SDL_RenderCoordinatesFromWindow или преобразование мыши не найден.

Команды/вывод для P4-проверок:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show ce0cacfb3ba425c8c831b52b64769186a835bdbb:tests/utils/test_HdRender.cpp | nl -ba | sed -n '206,268p'
~~~
Вывод содержит перечисленные TEST_CASE и CHECK с фиксированными аргументами. Сборки, тесты и CTest не запускались.

## 6. Файлы настроек

Печать ресурсов обоих деревьев:
~~~sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/settings.ini | nl -ba | sed -n '1,13p'
git show ce0cacfb3ba425c8c831b52b64769186a835bdbb:resources/bin/settings.ini | nl -ba | sed -n '1,13p'
~~~
FORK1: [SETTINGS], ScreenWidth=1024, ScreenHeight=768, FullScreen=false, RenderScale=0; WorldScale в файле отсутствует. PORT: ScreenWidth=1024, ScreenHeight=768, FullScreen=false, ScalingMode=IntegerScale; RenderScale и WorldScale в файле отсутствуют. Фактический построчный вывод этих двух команд: пункты соответствуют resources/bin/settings.ini@9208dcf:1–10 и @ce0cacfb:1–13.

В FORK1 чтение идёт в common.cpp@9208dcf:59–66, 73–74; начальный вызов — main.cpp:92. common.cpp читает RenderScale и WorldScale при наличии ключа (:63–66); WorldScale в settings.ini отсутствует, его значение по умолчанию — 0 (GameSettings.hpp@9208dcf:6–10). Options menu сохраняет в settings.ini через saveSettingsToIni (cOptionsState.cpp@9208dcf:715–738); common.cpp записывает ScreenWidth, ScreenHeight, FullScreen, RenderScale и WorldScale (:350–360) во временный settings.ini.tmp, затем подменяет файл (:279–323).

В PORT readSettings читает ScreenWidth, ScreenHeight, FullScreen, ScalingMode и опциональный WorldScale (Preferences.cpp@ce0cacfb:47–71). InitialGameSettings задаёт WorldScale=0, RenderScale отсутствует в InitialGameSettings и коде. При завершении Preferences::save записывает ScreenWidth/Height, FullScreen и ScalingMode в preferences.ini (Preferences.cpp@ce0cacfb:149–165, 186–198); resources/bin/settings.ini не меняется. Путь пользовательского файла строится SDL_GetPrefPath (PreferencesPath.cpp@ce0cacfb:28–46). По умолчанию main загружает settings.ini, а preferences.ini подмешивается только при -prefs (main.cpp@ce0cacfb:74–85); сохранение preferences.ini выполняется после game.run() при обычном завершении (:110–118).

## 7. SDL3 logical presentation и DPI

Источник — SDL3 3.4.10 в /srv/dune/worktrees/p2/.tmp/deps/src/SDL/src/render/ и src/video/. Каждый фрагмент ниже получен через nl -ba <путь> | sed -n <диапазон>; сборку не выполняли.

В SDL_render.c:2868–2909 DISABLED задаёт rect всего renderer output, отключая logical scale; STRETCH тоже задаёт полный output. LETTERBOX при совпадающем aspect ratio использует ту же ветку STRETCH; при несовпадающих пропорциях рассчитывает rect с полосами (SDL_render.c:2911–2937). INTEGER_SCALE делит размеры выхода целочисленно, затем центрирует результат (SDL_render.c:2888–2903). SDL_GetRenderLogicalPresentationRect копирует logical_dst_rect (SDL_render.c:3011–3022).

Для холста 1536×864 и renderer output 1920×1080:
| Режим | rect выхода | Показ |
| DISABLED | {0,0,1920,1080} | logical size выключен, координаты не переводятся к 1536×864 |
| STRETCH | {0,0,1920,1080} | по 1,25 по X/Y |
| LETTERBOX | {0,0,1920,1080} | пропорции совпадают, полос нет |
| INTEGER_SCALE | {192,108,1536,864} | масштаб 1, поля по 192 и 108 |

SDL_RenderCoordinatesFromWindow сначала умножает window coordinates на dpi_scale; при включённой logical presentation вычитает начало destination rect и умножает на отношение logical src / destination rect; затем учитывает viewport и render scale (SDL_render.c:3048–3077). При обычном DPI и точке в окне (960,540) получаются (960,540) для DISABLED, (768,432) для STRETCH/LETTERBOX, (768,432) для INTEGER_SCALE; для INTEGER_SCALE координаты на полях могут быть вне холста. В PORT mouse events реально проходят через SDL_RenderCoordinatesFromWindow (cMouse.cpp@ce0cacfb:77–127; cGame_logic.cpp@ce0cacfb:604–608).

SDL_GetWindowSize возвращает window->w/h, то есть оконные логические точки (SDL_video.c:3228–3237). SDL_GetWindowSizeInPixels вызывает платформенную функцию либо умножает размер окна на pixel_density дисплея (SDL_video.c:3299–3332). SDL_GetRenderOutputSize берёт renderer output либо GetWindowSizeInPixels (SDL_render.c:1367–1384). При масштабе DPI 2 окно 1920×1080 точек может иметь backing 3840×2160 пикселей; фактический коэффициент зависит от платформы. DPI renderer вычисляется как output pixels / window points и применяется к мыши (SDL_render.c:824–841, 3054–3065).

PORT сейчас не задаёт SDL_WINDOW_HIGH_PIXEL_DENSITY (окно создаётся с флагами 0: cSDLSystem.cpp@ce0cacfb:301), не вызывает SDL_GetWindowSizeInPixels напрямую, а логическое представление получает размеры renderResolution и реальный output — через SDL_GetRenderOutputSize (cSDLSystem.cpp@ce0cacfb:114–125, 174–198, 250–258, 340). При смене оконного renderer output renderResolution синхронизируется из SDL_GetRenderOutputSize; логические bounds берутся через SDL_GetDisplayBounds. Если П4б добавляет HIGH_PIXEL_DENSITY, расчёт RenderScale должен использовать output pixels, а события мыши оставаться в оконных координатах до SDL_RenderCoordinatesFromWindow.

## 8. Развилки и рекомендации

| Вопрос | Варианты и последствия | Рекомендация |
|---|---|---|
| Значение ScreenWidth/ScreenHeight | Считать настройками физического/желаемого размера вывода, как в форке; либо оставить фиксированным размером логического холста, как в PORT. Если сохранить второй смысл, выбор RenderScale не повлияет на холст отдельно. В полноэкранном режиме FORK1 использует режим рабочего стола; PORT создаёт окно по renderResolution и отдельно получает фактический размер вывода рендерера. | Сохранить ScreenWidth/ScreenHeight как желаемый размер окна/вывода. m_screenW/H сделать вычисленным логическим холстом = размер пиксельного вывода / RenderScale. В полноэкранном режиме брать актуальный размер вывода у рендерера, не переключать монитор на ScreenWidth×ScreenHeight. Это согласуется с Р66 и устройством FORK1, где пользовательский размер вывода и renderResolution разделены (cScreenInit.cpp@9208dcf:65–95, 125–147, 149–198). |
| ScalingMode, TOGGLE_SCALING_MODE и строки настроек | Оставить IntegerScale/Letterbox и Alt+L — получится второй способ масштабирования; сохранить только enum/key ради совместимости — останется неиспользуемое состояние; убрать режим, его клавишу и сохранение — исчезнет выбор пиксельного/letterbox-представления. В PORT строк меню разрешения/ScalingMode сейчас нет, что подтвердил пустой git grep по cOptionsState. | Убрать ScalingMode, TOGGLE_SCALING_MODE/Alt+L и строки/ключи IntegerScale/Letterbox из настроек. Оставить одну RenderScale-настройку; пункт «Масштаб игры» показать на П5, как предписывает план. |
| Режим SDL logical presentation | DISABLED не переводит координаты в холст; INTEGER_SCALE создаёт поля и не подходит к HD4; LETTERBOX может оставить поля при расхождении пропорций; STRETCH заполняет весь вывод и подходит, когда холст рассчитывается из пропорций того же вывода. | Применять SDL_LOGICAL_PRESENTATION_STRETCH. При целых размерах холст сохранит отношение сторон выхода с точностью до округления; если важнее сохранить пропорции при расхождении размеров, LETTERBOX оставит узкие полосы. |
| WorldScale Auto: физический выход или логический холст | Сейчас PORT передаёт m_screenH, который станет переменным вместе с RenderScale. Тогда масштаб мира зависит также от RenderScale: на 3840×2160 холст 100% даёт WorldScale zoom 1.5, а холст 200% (1920×1080) — 1.1 (canvas.tsv). Р33/SPEC определяет Auto по высоте экрана/outputHeight. | Передавать в AutoWorldScale физическую высоту вывода рендерера, чтобы RenderScale менял детализацию холста, но не менял отдельно выбранное приближение камеры. Ручной WorldScale оставить явным переопределением. Это устраняет конфликт между Р33 и текущим вызовом m_screenH (cGameSettings.h@ce0cacfb:34–35; cSDLSystem.cpp@ce0cacfb:250–258; U15/SPEC.md@MAIN:14–18). |
| Смена размера окна/fullscreen и кэшированные размеры | Оставить холст и раскладку до перезапуска проще, но процент перестаёт относиться к актуальному размеру вывода. Пересчитать холст, логическое представление и цели рендеринга при изменении окна/fullscreen сохраняет смысл настройки, но требует обновить размеры и раскладки, запомненные при создании. ensureFrameTargets сейчас сравнивает только плотность; при изменении холста с той же плотностью цель останется старого размера. | При SDL size/display event повторно получить размер вывода, пересчитать холст и STRETCH logical presentation; пересоздать actualRenderer/screenTexture при изменении ширины/высоты холста или плотности. Обновить viewport камеры и кэшированные UI-раскладки из screen-size-uses.tsv; меню расположить через адаптивный слой П5. |
| RenderScale: файл, default и строка меню | FORK1 хранит RenderScale в settings.ini, default 0=Auto; PORT пишет экранные настройки в preferences.ini, загружая его только с -prefs. Переносить только ini-ключ без переноса пути записи/чтения означает, что выбор может не примениться при следующем обычном запуске. | Рекомендую перенести RenderScale вместе с его settings.ini-путём из FORK1: при обычном запуске PORT читает settings.ini, а preferences.ini сохраняется отдельно и применяется только с -prefs. Default — AutomaticRenderScale=0; ручные значения — 100,125,150,175,200, если холст не меньше 800×600. Не дублировать ключ в обоих файлах. П4б даёт поле/парсер/расчёт/применение и постоянное хранение, а UI-строку «Масштаб игры» и список доступных значений добавляет П5 (PORT_PLAN.md@MAIN:88–90; FORK1 settings.ini@9208dcf:3–9; main.cpp@ce0cacfb:74–85, 110–118). |
| Применение выбранного RenderScale | Применить изменение немедленно — требует перестроить screen targets, camera viewport и cached layout; применить после перезапуска — совпадает с FORK1 и не оставляет созданные с прежним размером текстуры/окна. | До UI П5 оставить изменение RenderScale настройкой запуска, как в FORK1: P4b должен делать корректный холст при старте. Размер окна/fullscreen, который SDL меняет в ходе игры, всё равно обрабатывать live по предыдущей строке таблицы. |
| Retina/High Pixel Density | У PORT нет HIGH_PIXEL_DENSITY флага; GetWindowSize возвращает оконные координаты, renderer output — физические пиксели. Если использовать оконные координаты в формуле, плотность и холст будут занижены при DPI>1. | Если П4б включает окна высокой плотности, рассчитывать RenderScale от SDL_GetRenderOutputSize в пикселях; оставить SDL-преобразование мыши между оконными и логическими координатами. Сейчас не добавлять новый флаг без отдельного требования. |

## Не проверено

- Не прослежены все дальнейшие потребители алиасов sGameServices::screenTexture и общего mapViewport; таблица содержит места создания/передачи этих алиасов, но не каждый последующий вызов.
- Не сверены временные локальные геометрические значения и параметры GUI builders за пределами найденных строк таблицы.
- Не проведена полная инвентаризация всех кэшей текстур и ресурсов вне screen-sized targets и полей Texture.
- Сборки, тесты/CTest и запуск игры не выполнялись по запрету задания.
