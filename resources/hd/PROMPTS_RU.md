# Журнал генерации эталонного набора ru3-preview1

Генератор: встроенный OpenAI ImageGen. Исходные ответы сохранены в
`C:\Users\Slaven\.codex\generated_images\019f9f8c-95c9-72a0-b768-fe6851c9788b`.
Рабочие копии находятся в `resources/hd/style_reference`.

Общий контракт каждого запроса:

- faithful modern RTS remaster;
- сохранить силуэт, камеру, композицию и цвета Домов;
- graphite / aged brass / ochre / restrained cobalt;
- никаких надписей, псевдобукв, цифр, логотипов и водяных знаков;
- исходник используется как точный композиционный референс;
- `gameplay_ui_wide_v1.png` используется как общий референс материалов.

| Ресурс | Ответ ImageGen | Исходные референсы | Специальные условия |
|---|---|---|---|
| `gameplay_ui_wide_v1.png` | `call_UxS30nqev6Rxl9lvpXqX7Yvm.png` | снимок исходного HUD, карточки харвестера и ветряной ловушки | 16:9, sidebar 28%, три карточки, пустые полосы названий |
| `gameplay_ui_4x3_v1.png` | `call_PcbLvi6jP0ofxRQbLwB2na6w.png` | широкий эталон и исходный HUD | узкий режим, две карточки |
| `mentat_atreides_v1.png` | `call_KJDhhwGle8cxVWRP8sZNzwh5.png` | исходный ментат и широкий эталон | сохранить лицо, позу, книгу, зоны глаз/рта; монитор пустой |
| `campaign_map_v1.png` | `call_z2C6JColSdk4jLuILzRJTb79.png` | `0033_WORLD_DUNE.png` и широкий эталон | сохранить рельеф и сверхширокую композицию, без меток |
| `story_victory_v1.png` | `call_VIXPBZyls0kshXimxLIHgDQ4.png` | `sdl_win01/0000_WIN01.png` и широкий эталон | сохранить движение справа налево и число основных фигур |
| `card_harvester_v1.png` | `call_fhtypEWJJ0mVgtgl4xTQYZKl.png` | `0055_ICON_UNIT_HARVESTER.png` и широкий эталон | точный 4:3, нижняя полоса пустая, широкий гусеничный харвестер |
| `card_windtrap_v1.png` | `call_BXwQot7kyqJpVCWZPNLdOknt.png` | `0049_ICON_STR_WINDTRAP.png` и широкий эталон | две синие воздухозаборные башни, нижняя полоса пустая |
| `card_refinery_v1.png` | `call_8fW3PocIGA7KEmYaoIaBKBMd.png` | `0042_ICON_STR_REFINERY.png` и широкий эталон | широкий завод с группой узких колонн, нижняя полоса пустая |
| `card_tank_v1.png` | `call_o8dPdkgynxNdgeXdf4r9nwOV.png` | `0068_ICON_UNIT_TANK.png` и широкий эталон | низкий корпус, округлая башня, длинная пушка, нижняя полоса пустая |
| `terrain_board_v1.png` | `call_n122wG9uc3WZ7aL8Lpauklek.png` | `TERRAIN_SAND`, `TERRAIN_ROCK`, `TERRAIN_SPICE` и широкий эталон | четыре ортографических образца, спокойная игровая детализация |
| `explosion_sheet_v1.png` | `call_kv5NkODcOEVWxKmprcUHSG51.png` | `0065_EXPLOSION_FIRE.png` и широкий эталон | шесть последовательных фаз, фон RGB 255/0/255 |
| `main_menu_background_v1.png` | `call_vYNsZrEV2Mqv935Qly7fwHNo.png` | широкий эталон и неизменяемый логотип | 16:9, центральная безопасная зона, логотип не генерировать |
| `card_constyard_v1.png` | `call_lDGAgk7Yp0UF38HCXxtpp3ba.png` | `0035_ICON_STR_CONSTYARD.png` и широкий эталон | квадратная промышленная платформа, центральный сборочный механизм, без подписи |
| `card_heavyfactory_v1.png` | `call_NJ50a26daWDBdKyJPYQzrZVs.png` | `0036_ICON_STR_HEAVYFACTORY.png` и широкий эталон | широкий тяжёлый завод, въездная рампа и группа вытяжных башен, без подписи |
| `card_siegetank_v1.png` | `call_UfL53pcIAMbAtKG01fHD6zSL.png` | `0065_ICON_UNIT_SIEGETANK.png` и широкий эталон | массивное шасси, две параллельные длинные пушки, без подписи |
| `card_ornithopter_v1.png` | `call_2TFBBKrd01YXBya8Ldd6zzdE.png` | `0059_ICON_UNIT_ORNITHOPTER.png` и широкий эталон | компактный корпус и высокие маховые крылья целиком в кадре, без подписи |
| `hud_house_atreides.png` | `exec-e6e93b54-695a-4f6b-a9f0-5da657e2a5fb.png` | `0011_BMP_SELECT_HOUSE_ATREIDES.png` | круглый герб с синим ястребом, фон RGB 255/0/255, без рамки экрана и текста |
| `hud_house_harkonnen.png` | `exec-31539a57-c7bf-434e-837f-b5c759222c5f.png` | `0012_BMP_SELECT_HOUSE_HARKONNEN.png` | круглый герб с рогатым черепом, чёрный металл и багряная эмаль, без текста |
| `hud_house_ordos.png` | `exec-881bad4f-df24-4bbe-b763-4de540f7a698.png` | `0013_BMP_SELECT_HOUSE_ORDOS.png` | круглый герб со змеёй, изумрудная эмаль, без текста |

Все карточки нормализованы в точные мастера 256×192 детерминированным
Lanczos-уменьшением. Исходные ответы ImageGen не удаляются.

Гербы очищены штатным `remove_chroma_key.py`, нормализованы в прозрачные
мастера 384×384 и уменьшены до HD2 192×192.

## Завершение набора карточек ru3-preview3

Оставшиеся 35 карточек созданы встроенным OpenAI ImageGen отдельными
запросами для каждого ID. Рабочие ответы сохранены в
`resources/hd/style_reference/card_NNNN_ru3.png`, принятые мастера — в
`resources/hd/master4/sdl_inter`. Полный словарь ID и русских названий
находится в `resources/hd/CARD_NAMES_RU.json`.

Общий контракт запросов:

- Image 1 — соответствующая классическая карточка как точный референс
  объекта, силуэта и композиции;
- Image 2 — утверждённый `card_siegetank_v1.png` как референс качества,
  материалов, света Арракиса и цветовых акцентов Домов;
- современная высокодетализированная графика RTS-ремастера;
- весь объект находится в кадре и читается в уменьшенном размере;
- запрещены текст, буквы, цифры, псевдосимволы, логотипы и водяные знаки;
- ответы с резервной нижней зоной нормализуются в чистую иллюстрацию 256×192;
- HD2 получается только детерминированным Lanczos-уменьшением мастера HD4.

Сгенерированные ID:

`29–34, 37–41, 43–48, 50–54, 56–58, 60–64, 66–67, 69–71`.

Ранее утверждённые художественные мастера сохранены для ID:

`35, 36, 42, 49, 55, 59, 65, 68`.

## Красный логотип главного меню ru4

По пользовательскому изображению главного меню подготовлен отдельный
прозрачный логотип `DUNE II` без строки `The Maker`.

- первичная правка: `call_vz1kf5OJUjVVuKKWcUnPR4oL.png`;
- версия на ключевом фоне: `call_IVAGd44ICDuBrn3a7ncJLGba.png`;
- итог после штатного `remove_chroma_key.py`:
  `source_references/ru4/main_menu_logo_red_alpha.png`.

Контракт правки:

- сохранить написание, пропорции и засечки `DUNE II`;
- заменить синюю гамму на насыщенный металлический красный;
- полностью убрать `The Maker`;
- сохранить красную горизонтальную линию;
- не добавлять другие слова, символы или водяные знаки.
