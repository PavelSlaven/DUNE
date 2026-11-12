# Задание P7V-RETELL — пересказ задания P7V

## Цель

Перескажи своими словами задание P7V ниже, после строки «===== ЗАДАНИЕ P7V =====», так, как ты понял его при одном прочтении. Пересказ сверяет ведущий: расхождение с его замыслом показывает двусмысленное место задания, которое увело бы работу в цикл.

Метки `@@B@@` (ревизия основы) и `@@N@@` (число тестов CTest) ведущий заполнит перед запуском; их незаполненность — не двусмысленность.

## Прочитать до работы

Файлов читать не нужно: весь материал — текст задания P7V ниже и строки кода в этом разделе.

Нынешний текст семи мест (в `cSetupSkirmishState.cpp` — уже после части П7б):

| место | строка кода сейчас |
|---|---|
| `src/utils/ini.cpp`, `cIni::loadRegionfile` | `    auto filename = std::format("campaign/{}/mission{}.ini", getHouseDirectoryName(iHouse), iMission);` |
| `src/gameobjects/mentat/AbstractMentat.cpp`, время речи | `            int iLength = static_cast<int>(sentence[iMentatSentence].size());` и следующая `            iLength += static_cast<int>(sentence[iMentatSentence + 1].size());` |
| `src/gameobjects/mentat/AbstractMentat.cpp`, `draw()` | `        if (iMentatSentence >= 0) {`, затем `            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{0, 0, 0,255},sentence[iMentatSentence]);`, `            m_textDrawer->drawText(offsetX + 17, offsetY + 17,Color{255, 255, 255,255},sentence[iMentatSentence]);`, пустая строка, `            m_textDrawer->drawText(offsetX + 17, offsetY + 37,Color{0, 0, 0,255},sentence[iMentatSentence+1]);`, `            m_textDrawer->drawText(offsetX + 17, offsetY + 36,Color{255, 255, 255,255},sentence[iMentatSentence+1]);`, `        }` |
| `src/gamestates/cSetupSkirmishState.cpp`, сведения о карте | `        const std::string mapName = localization::format("Name: {}", "Название: {}", selectedMap->name);` |
| `src/gamestates/cSetupSkirmishState.cpp`, список карт | `        const std::string *nameToRender = &mapToRender->name;`, `        std::string truncatedName;`, `        if (m_textDrawer->getTextLength(mapToRender->name) > availableTextWidth) {`, `            truncatedName = mapToRender->name;`, `            while (!truncatedName.empty() && m_textDrawer->getTextLength(truncatedName + "...") > availableTextWidth) {`, `                truncatedName.pop_back();` |
| `resources/bin/skirmish/2PL_AncientDelta.ini`, строки 1–4 | `[SKIRMISH]`, `Title="Ancient Delta"`, `Author = Ripps`, `Description = -`; строка таблицы `TITLES-P7V.tsv`: `2PL_AncientDelta.ini`, `Ancient Delta`, `Старая дельта` |
| `tests/ui_audit/data/latin-ru-allowed.tsv`, строки 2 и 61–63 | строка 2: `Built at .*` + табуляция + `штамп времени сборки из CMakeLists.txt`; строка 61: `Your\ replacement\ has\ been\ selected,\ and\ we\ look\ forward\ to\ the` + табуляция + `текст кампании из файлов миссий и ментатов — переводит П7в`; строка 62: `replacing\ you\.` + табуляция + `текст кампании из файлов миссий и ментатов — переводит П7в`; строка 63: `Sietch\ Stefan` + табуляция + `название карты из файла карты — переводит П7в` |

## Правила

- Файлы и команды не открывай и не запускай: работа — только по тексту задания и таблице выше. Писать никуда нельзя. Весь результат — в последнем сообщении хода.
- Не исправляй задание. Где текст допускает два прочтения — запиши оба и какое выбрал бы.
- `create_goal` не вызывай, помощников не запускай.

## Сдача

Блок `## DONE-P7V-RETELL | <время UTC из date -u>`:
- цель задания одной фразой;
- что и в каком порядке ты делал бы, что делает каждый помощник и корневая нить;
- для каждого из семи мест таблицы выше — текст после правки целиком (для файла карты — строки 1–5; для списка исключений — какие из названных строк останутся) и пункт контракта, по которому он получился; какие строки `#include` появятся в этих файлах и после какой строки;
- что вернёт `layoutMentatPage` для страницы `"The Ordos broke through the Atreides."` и `""` при ширине 606, и для страницы из двух русских фраз шириной 632 и 120 точек — по какому правилу;
- что проверяют T7–T10 и как T9 находит номера сценариев и разделы; почему T6 краснеет на шаге 2 и какие строки лога это показывают;
- проверки 1–7: что ожидается и по каким строкам это видно;
- какие файлы ты тронул бы и какие запрещено трогать; что делает помощник B со скриптом `add_titles.py`, и когда он останавливается;
- где ты остановился бы и с каким блоком, в том числе если случай CTest упал из-за русского текста или скрипт проверки 4 упал из-за положения текста;
- места, которые можно прочитать двумя способами, — оба прочтения и выбранное;
- места, где план, по-твоему, расходится с фактами о коде, названными в самом задании или в таблице выше, — цитата и в чём расхождение.

## Организация работы

- **Порядок:** прочитать текст задания P7V → пересказ → сдача и стоп.
- **Параллельно:** нет, одна работа.
- **Помощники:** 0.
- **Остановки:** только на `## DONE-P7V-RETELL`.
- **Рамка правок:** ничего не меняй.

===== ЗАДАНИЕ P7V =====

