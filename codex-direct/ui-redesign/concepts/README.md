# Образцы экранов

Картинки `<группа>-<ширина>x<высота>.png` — образцы экранов по `../SYSTEM-ui.md`. Одна точка картинки при холсте 800 × 600 — одна точка логического холста игры.

| Файл | Экран |
|---|---|
| `1-main-menu` | главное меню |
| `2-options` | меню настроек: 800 × 600 — из главного меню, 1920 × 1080 — из боя; `2-options-game-800x600` — из боя на холсте 800 × 600 (окно 768) |
| `3-choose-house`, `3b-campaign-map`, `3c-mission-select` | выбор Дома, карта кампании, выбор миссии |
| `4-mentat` | брифинг ментата (так же устроен рассказ о Доме) |
| `5-skirmish` | настройка схватки |
| `6-battle` | экран боя с открытым списком построек; ещё холсты 1067 × 600 и 2133 × 600; `6-battle-starport-1067x600` — вкладка космопорта с заказом и нехватка энергии |
| `7b-outcome`, `7-mission-report` | картина исхода и, отдельным экраном после неё, отчёт о миссии; `7-mission-report-five-800x600` — отчёт на пять сторон (таблица) |
| `8-credits` | титры |
| `9-components-1920x1080` | общие части и их состояния |
| `9b-save-dialog` | окно сохранения и загрузки (шаг П8) |
| `compare/*.jpg` | листы «сейчас / образец» |

Образцы меню при 1920 × 1080 — это раскладка опорного холста 1067 × 600, увеличенная в 1,8 раза (`SYSTEM-ui.md`, раздел 2.2). Экран боя и лист частей нарисованы в настоящих точках холста.

## Как пересобрать

Исходники — `src/*.html`, `src/ui.css`, `src/ui.js`. Они берут картинки и шрифты игры из папки `.cache/ui-redesign/` рабочей копии (в git её нет):

1. Картинки паков: `python -B ../tools/dump_pack.py --tool tools/hd_assets.py --pack resources/bin/data/<пак>_hd4.dat --out-dir .cache/ui-redesign/assets` для `sdl_inter`, `sdl_mentat`, `sdl_data`, `sdl_world`; файлы `resources/bin/data/hd4/*.png` — копией в `.cache/ui-redesign/assets/hd4/`.
2. Шрифты для образцов: `git show origin/main:resources/bin/data/RussoOne-Regular.ttf | git lfs smudge > .cache/ui-redesign/fonts/RussoOne-Regular.ttf`, так же `PTSansNarrow-Regular.ttf`. Это копии только для рисования образцов; в ветку порта шрифты приносит шаг П7.
3. Снимки нынешней игры: `.cache/ui-redesign/before/` (режим отладки интерфейса, `../recon/before-shots.md`) и `.cache/ui-redesign/battle-ref/` (`../recon/history.md`, раздел 6).
4. `python src/prep_assets.py` — вырезки поля боя, мини-карт и миниатюр карт.
5. `python src/render.py` — все образцы; `python src/render.py 6- --size 1067x600,2133x600` — экран боя на других холстах; `python src/render.py 6- --variant starport --size 1067x600` — вариант с космопортом; `python src/render.py 2- --variant game --size 800x600` — настройки из боя; `python src/render.py 7-mission --variant five --size 800x600` — отчёт на пять сторон; `python src/build_compare.py` — листы сравнения.

`render.py` запускает Chrome без окна со своей временной папкой профиля.
