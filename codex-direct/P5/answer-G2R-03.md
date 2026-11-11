## Дополнение к P5G2R — пункт 5

В порту ментат, рассказ о Доме и карта кампании живут в состояниях игры, которые создаёт `cCreatorState`. Нужен ещё один пункт той же разведки по тем же правилам раздела «Рабочая копия и ревизии» и ответа `answer-G2R-01.md` (правило «функция дословно» с шаблоном `^(.*[ *&])?<Класс>::<имя>\(`).

5. **Состояния ментата и кампании.**
   - «Файл дословно» для `src/gamestates/cMentatState.h`, `src/gamestates/cTellHouseState.h`, `src/gamestates/cCreatorState.h`, `src/gamestates/cGameState.h`, `src/gameobjects/mentat/AbstractMentat.cpp`, `src/include/sDataCampaign.h`, `src/include/sGameServices.h`, `src/game/CampaignProgress.hpp`, `src/game/MentatFlow.hpp`, `src/game/MissionFlow.hpp`.
   - Вывод `git grep -n -E '^(.*[ *&])?(cMentatState|cTellHouseState)::[A-Za-z_~]+\(' <PORT> -- src` и «функция дословно» для каждой найденной строки без `;` в конце.
   - «Функция дословно» для `cCreatorState::getOrCreateState`, `cCreatorState::getState`, `cCreatorState::hasState`, `cSelectYourNextConquestState::calculateOffset`, `cSelectYourNextConquestState::installWorld`, `cSelectYourNextConquestState::fastForwardUntilMission`, `cSelectYourNextConquestState::regionSetupNextMission`.
   - Вывод `git grep -n -w -E 'm_dataCampaign|m_campaignProgress|m_creatorState|m_mentatFlow|m_missionFlow' <PORT> -- src/game/cGame.h src/gamestates/cChooseHouseState.h src/gamestates/cSelectMissionState.h`.
   Отчёт — `.tmp/p5g2r/states.md`: для каждого файла заголовок `### <путь>@acddd29`, для каждой функции заголовок `### <Класс>::<имя> — <путь>@acddd29:<начало>-<конец>`, команды и выводы в блоках кода.

**Организация.** Помощник 1 (`gpt-6-luna` `xhigh`) делает пункт 5; затем помощник 2 сверяет четыре факта из `states.md` так же, как помощник 4 сверял отчёты, и дописывает итог в конец `.tmp/p5g2r/spotcheck.md` под заголовком `## Пункт 5`. В бриф помощника дословно входят раздел «Рабочая копия и ревизии» задания, правило из `answer-G2R-01.md`, этот пункт 5, абзац «Комментарии в коде» задания и запрет писать вне `.tmp/p5g2r/`. Остальные отчёты не меняй. Корневая нить дописывает `states.md` с числом строк в `RECON.md`.

**Сдача.** Блок `## RECON-P5G2R | <время UTC из date -u>`: число строк `states.md`, список файлов пункта 5 с числом строк каждого (последний номер `nl`), список функций с `путь@acddd29:<начало>-<конец>` или «нет определения», итог сверки пункта 5.

Не отступай от плана, не переусложняй.
