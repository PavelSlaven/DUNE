# Кандидаты шрифтов для русской версии D2TM (разведка)

Дата: 2026-11-12. Метод: WebSearch и WebFetch страниц авторов (itch.io, GitHub, fontlibrary), файлы шрифтов не скачивались. Для Google Fonts читались METADATA.pb из репозитория google/fonts (поля license и subsets). Названия лицензий даны как на странице; полные тексты лицензий и цитаты не переношу, кириллица описана пересказом со ссылкой на страницу.

Важно: поле «Кириллица» означает заявление автора или subset Google Fonts. Наличие всех 66 букв, включая Ё и ё, по глифам не проверено.

## Корректировки к исходным предположениям

- RunttiSP: автор не GGBotNet. По онлайн-каталогу Runtti SP Cyrillic — Sasha Pavljenko, в авторских правах также Juuso Haimilahti; исходный проект Runtti — github.com/juusohai/Runtti (автор juusohai). Лицензия SIL OFL 1.1.
- Профильная таблица itch.io ggbot (шрифты) дала неверные лицензии: у Sangyo, Cairopixel, Pixeloid, Pixelbasel на самих страницах SIL OFL 1.1, в таблице «не указана». Лицензии брались со страниц шрифтов.

## 1. arrak.ttf (пиксельный засечковый, только заглавные)

| № | Название | Автор | Лицензия | Страница | Google Fonts | Кириллица (где сказано) | Сходство с arrak |
|---|---|---|---|---|---|---|---|
| 1 | Northrup Serif (семейство Northrup, 8 вариантов) | mirnovov | OFL-1.1 (раздел «OFL-1.1 license»; текст LICENSE.txt не открыт) | https://github.com/mirnovov/northrup | не проверял | страница: Latin, Greek, Cyrillic | Пиксельное семейство, есть serif-варианты; сетка и высота не указаны |
| 2 | Obelisk - Pixel Font | Nikoichu | SIL OFL 1.1 | https://nikoichu.itch.io/obelisk-font | нет | «support for Cyrillics»; в демо только заглавные кириллические | «bold 10-pixel serif» — ближе всего по засечкам и пиксельности. Условие: полный файл открывается при оплате от $3 (name your own price) |
| 3 | Cairopixel | GGBotNet | SIL OFL 1.1 | https://ggbot.itch.io/cairopixel-font | нет | кириллица не названа; в списке 93 языков русский, украинский, болгарский, сербский | Тег «Pixel Font», 16 px. Засечки на странице не указаны (в профильной таблице «брусковый serif» — не подтверждено) |
| 4 | Pixellari Cyrillic (форк zedseven/Pixellari, 2017) | YuRaNnNzZZ | бейдж «Open Font-1.1» (OFL 1.1); текст LICENSE не открыт | https://www.github.com/YuRaNnNzZZ/PixellariCyrillic | нет | кириллица добавлена в 2021; автор просит указывать авторство | «A simple pixel font»; засечек не описано |
| 5 | Vyaz Pixel Font | GGBotNet | CC0 1.0 | https://ggbot.itch.io/vyaz-pixel-font | нет | тег cyrillic; 45 языков, в списке русский | Стиль спорный: одни источники — blackletter-inspired, другие — декоративный пиксель с орнаментом. Слабое совпадение |
| 6 | Kapel | jeti / Font End Dev | CC BY 4.0 (страница автора) | https://fontenddev.com/fonts/kapel/ | нет | «featuring Cyrillic characters» | Блочный геометричный, не засечковый; слабое совпадение. DaFont относит к «Public domain / GPL / OFL» — расхождение с автором |

## 2. benegess.ttf (пиксельный blackletter, строчные и заглавные)

| № | Название | Автор | Лицензия | Страница | Google Fonts | Кириллица | Сходство с benegess |
|---|---|---|---|---|---|---|---|
| 1 | Fantasy Warrior | Douglas Vautour (Burpy Fresh) | CC BY 4.0 (атрибуция обязательна) | https://burpyfresh.itch.io/fantasy-warrior | нет | страница: Latin, Cyrillic, Korean | «Blackletter inspired» (автор оговаривает «very loosely»), сетка 11x11 px |
| 2 | Vyaz Pixel Font | GGBotNet | CC0 1.0 | https://ggbot.itch.io/vyaz-pixel-font | нет | тег cyrillic; 45 языков | Blackletter-подобный по одному источнику (pixelbuddha), по другим — нет; размеры 11/22/44 px |

В проверенном наборе полностью подходят по лицензии и кириллице только 2 кандидата (до 4 не добрал). Остальные похожие шрифты отброшены, см. ниже.

## 3. small.ttf (мелкий жирный пиксельный sans)

| № | Название | Автор | Лицензия | Страница | Google Fonts | Кириллица | Сходство с small |
|---|---|---|---|---|---|---|---|
| 1 | Pixelify Sans | Stefie Justprince | OFL | https://github.com/google/fonts/tree/main/ofl/pixelifysans (GF: «Pixelify Sans») | да | subset cyrillic (GF) | Пиксельный sans с толстым штрихом; несколько весов по сводке поиска (в METADATA один файл, weight 400 — проверить) |
| 2 | Press Start 2P | CodeMan38 | OFL | GF: «Press Start 2P» | да | subsets cyrillic, cyrillic-ext (GF) | 8 px, жирный штрих, очень широкий; сильный пиксельный характер |
| 3 | Handjet | Rosetta, David Březina | OFL | GF: «Handjet» | да | subsets cyrillic, cyrillic-ext (GF) | Пиксельный, есть оси — весом по сравнению не проверял |
| 4 | Tiny5 | Stefan Schmidt | OFL | GF: «Tiny5» | да | subsets cyrillic, cyrillic-ext (GF) | 5 px, мелкий; по весу слабее small |
| 5 | Pixeloid Sans Bold | GGBotNet | SIL OFL 1.1 | https://ggbot.itch.io/pixeloid-font | нет | русский в списке языков и в образце | Есть Sans Bold; сетка 9 px — вывод автора, не прямое описание |
| 6 | Avenue Pixel (6x15) | JD Jiménez | SIL OFL (на странице «Avenue Pixel License (SIL Open Font License)») | https://jdjimenez.itch.io/avenue-pixel | нет | в обновлении «Added accented and Cyrillic characters» | Пропорциональный пиксель, варианты Regular, Soft-Stroke, Stroke |
| 7 | Public Pixel Font | GGBotNet | CC0 1.0 | https://ggbot.itch.io/public-pixel-font | нет | образец с кириллическим алфавитом; 98 языков, включая русский | 8x8 моно, без жирного варианта — слабое совпадение |
| 8 | Pixelzone Font | GGBotNet | CC0 1.0 | https://ggbot.itch.io/pixelzone-font | нет | письменность «Cyrillic» в списке | Пиксельный ретро, 16 px; вес не указан |

## Отброшенные (похожие, но по правилу не подходят)

Без кириллицы (проверено по subsets GF или по языкам на странице):
- Silkscreen (OFL, GF, subsets latin, latin-ext, menu) — кириллицы нет.
- Jersey 10, Micro 5, Bytesized, Jacquard 12, Sixtyfour (OFL, GF) — кириллицы нет.
- Pirata One (OFL, GF) — нет кириллицы; blackletter.
- Grenze Gotisch (OFL, GF) — нет кириллицы; blackletter.
- UnifrakturCook (OFL, GF) — нет кириллицы; blackletter.
- Uncial Antiqua (OFL, GF) — нет кириллицы; uncial.
- Texturina (OFL, GF, SERIF) — нет кириллицы.
- Fondamento (OFL, GF) — нет кириллицы; рукописный.
- Jacquarda Bastarda 9 (OFL, GF) — пиксельный готический стиль, но нет кириллицы.
- Gotfridus (GGBotNet, OFL) — готика по тегам, языки без кириллицы.
- Pixelbasel (GGBotNet, OFL) — на странице нет кириллицы (serbian в списке).
- DarkByte, Bitrimus, Pixelated Elegance, Raster Forge, Vaticanus (GGBotNet, CC0) — кириллица не заявлена.
- Pixtile (GGBotNet, CC0) — кириллица не заявлена, тег serif.
- Gothic Pixels (Akezhar, CC0) — стиль готический пиксель, но на странице только uppercase, lowercase, numbers, symbols; кириллица не заявлена.
- Turpis, Westhorn (GGBotNet, OFL) — 2D serif, кириллица не заявлена.

Лицензия не подходит или не указана:
- Eternity (Neutronio Games) — blackletter пиксель, высота 25 px, кириллица заявлена; лицензия «not specified»; версии платные (от 4.49 евро).
- Straight Pixel Gothic Font (MedievalMore) — blackletter пиксель, сетка 48 px, кириллица «full Cyrillic»; лицензии нет, условия «commercial and private use for an unlimited number of projects» — не названная свободная лицензия; скачивание от $9.
- Simplified Gothic Pixel Font (MedievalMore) — то же: кириллица upper и lower, условия без названной лицензии, от $9.
- Kingdom Pixel Font (gleeson) — blackletter, кириллица с v1.3; платная, минимум $8 (по сводке поиска, страница не открывалась).
- Blackcraft (GGBotNet, OFL) — кириллица по языкам есть, но тема Halloween/horror, готики по странице нет.
- GNU Unifont (fontlibrary, по сводке) — пиксельный, кириллица упомянута; лицензия на странице не выписана, не проверено.

Не проверено (страница не отдала содержимое):
- KJV 1611 (fontlibrary.org/ru/font/kjv-1611) — по сводке поиска blackletter, OFL, с кириллицей. Страница вернула только заголовок дважды. Кандидатом не считаю.

## Sangyo и RunttiSP (шрифты игры)

- Sangyo — https://ggbot.itch.io/sangyo-font — автор GGBotNet; SIL OFL 1.1 (на странице, профильная таблица ошиблась); 2 стиля (Regular, Italic), 818 глифов; заявлена кириллица (тег cyrillic, русский в списке языков). Не пиксельный шрифт.
- RunttiSP — по онлайн-каталогу https://online-fonts.com/fonts/runtti-sp-cyrillic: Runtti SP Cyrillic, дизайнер Sasha Pavljenko, копирайт Juuso Haimilahti, Sasha Pavljenko; SIL OFL 1.1; 60 языков, в списке русский; «1 file», начертание и вес не указаны. Исходный проект https://github.com/juusohai/Runtti (README: curveless display, слегка наклонный; OFL 1.1). Совпадение имени файла игры RunttiSP-Bold.otf с этим релизом не подтверждено.

## Другие пиксельные шрифты GGBotNet с кириллицей (проверено по страницам)

| Шрифт | Лицензия | Кириллица | Страница |
|---|---|---|---|
| Public Pixel Font | CC0 1.0 | образец кириллицы, русский в списке (98 языков) | https://ggbot.itch.io/public-pixel-font |
| Vyaz Pixel Font | CC0 1.0 | тег cyrillic, 45 языков | https://ggbot.itch.io/vyaz-pixel-font |
| Pixelzone Font | CC0 1.0 | «Cyrillic» в списке письменностей | https://ggbot.itch.io/pixelzone-font |
| Pixeloid (Mono, Sans, Sans Bold) | SIL OFL 1.1 | русский в списке и в образце | https://ggbot.itch.io/pixeloid-font |
| Cairopixel | SIL OFL 1.1 | русский, украинский, болгарский в списке языков | https://ggbot.itch.io/cairopixel-font |

Без кириллицы (пиксельные): Pixelbasel (OFL 1.1), DarkByte, Bitrimus, Pixelated Elegance, Raster Forge, Vaticanus (CC0), Pixtile (CC0; кириллица не заявлена).
Непиксельные с кириллицей: Kaph (OFL 1.1, «Version 1.2 - Cyrillic»), Sangyo (OFL 1.1).

## Неопределённости

1. Кириллица во всех кандидатах заявлена (автор, GF subsets, список языков), глифы Ё/ё и полный набор 66 букв не проверены: файлы не скачивались.
2. Поиск не исчерпывающий. GF проверен выборочно; fontlibrary почти не разобран; страница KJV 1611 не открылась.
3. Northrup: текст LICENSE.txt, сетка и наличие пиксельного serif-варианта не открыты. Google Fonts для него не проверял.
4. Obelisk: полный файл с lowercase кириллицей — после оплаты от $3. Условие загрузки, не лицензии.
5. Vyaz Pixel: стиль (blackletter или нет) источники описывают по-разному.
6. RunttiSP: связь игрового файла с Runtti SP Cyrillic не подтверждена напрямую; автор установлен по агрегатору online-fonts.com и по README проекта juusohai.
7. Страница pixelbuddha (Vyaz) дала timeout; стиль Vyaz взят из сводки поиска.
8. Google Fonts specimen-страницы не читались, только METADATA.pb (зеркало на GitHub).
