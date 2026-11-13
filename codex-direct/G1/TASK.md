# Задание G1 — проба: перерисовка 3D-рендера Девастатора в стиле старого спрайта

Режим: «Ведёт sol». Плана на утверждение не нужно: первой частью сдачи запиши `## PLAN-G1` для записи. Исполнитель: Codex `gpt-6.1-sol` `high` со встроенной генерацией изображений.
Рабочая копия: `/srv/dune/worktrees/g1`, ветка `units3d/pilot`.

## Цель

Получить четыре картинки: 3D-рендер Девастатора под углом камеры 63°, перерисованный в стиле старого HD-спрайта игры. Форма, ракурс и положение танка берутся из рендера, а материалы, палитра и манера — из старого спрайта. По картинкам ведущий решит, годится ли этот путь для всех юнитов. Облик оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024×1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файл | Что это |
|---|---|
| `form_k1.png` | рендер 3D-модели, направление «северо-восток» |
| `form_k6.png` | рендер 3D-модели, направление «юг» |
| `style_k1.png` | старый спрайт игры, то же направление «северо-восток» |
| `style_k6.png` | старый спрайт игры, то же направление «юг» |

Перед работой сверь SHA-256 входов с этим списком. При расхождении — `Q-G1-01` и стоп.

```text
d4d8931638053bb6d93169f21237d954cf5a8f13b5890e038e78aeaaa15f303b  .tmp/input/form_k1.png
7b225989088472c6167a0b3fcfcb40c99462e43b8ca01f763786ee04020356ab  .tmp/input/form_k6.png
7ce5426bb1389c932ccf427438b5546e9f3795a72398f1651398921265b14dd4  .tmp/input/style_k1.png
5e3537fe661e22de5cd85b1e8a416d1ed1500593e853e2d5b03e1af301f4f8c8  .tmp/input/style_k6.png
```

## Что сделать

1. Для направления `k1` открой `form_k1.png` первой картинкой и `style_k1.png` второй и вызови генерацию изображения с промптом ниже. Размер выхода — 1024×1024. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`.
2. То же для направления `k6` с `form_k6.png` и `style_k6.png`.
3. Скопируй каждую полученную картинку в `.tmp/out/` под именем `g1_k<направление>_<попытка>.png`: `g1_k1_a.png`, `g1_k1_b.png`, `g1_k6_a.png`, `g1_k6_b.png`. Если скопировать файл генерации в рабочую копию невозможно, запиши в сдачу полный путь каждого файла и продолжай.
4. Запиши `.tmp/out/prompts.md`: по каждой картинке — имя, входные файлы в порядке подачи, промпт дословно, размер выхода, путь исходного файла генерации.

Промпт — дословно, без правок и дополнений:

```text
Repaint image 1 in the art style of image 2.
Image 1 is a 3D render of a heavy tank for a real-time strategy game, seen through an orthographic camera 63 degrees above the horizon. Keep its shape exactly: the silhouette, outline, proportions, camera angle, perspective, facing direction, position and size on the canvas, and every part with its placement. Do not move, add or remove parts. Do not change the view.
Image 2 is a sprite from the same game in the target art style. Take from it only the surface treatment: materials (dark graphite armour, aged steel and brass details, bright orange accent panels), palette, contrast, level of detail, crisp edge highlights and the painted game-sprite look. Place the orange accent panels the way image 2 does: on large flat armour plates. Tracks and the underside stay dark.
Keep the lighting direction of image 1. Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

**Повтор.** Попытку можно повторить один раз тем же промптом, только если выход нарушает жёсткое правило: фон не пурпурный; на картинке есть текст, буквы или цифры; танк обрезан краем; на картинке не один танк. Причину повтора запиши в `prompts.md`. Всего генераций — не больше 8.

## Сдача

Последнее сообщение — `## DONE-G1 | время UTC | база <sha HEAD>`:
- `## PLAN-G1` для записи: шаги и кто их делал;
- таблица: файл в `.tmp/out/` → направление → попытка → путь исходного файла генерации → повтор (нет или причина);
- SHA-256 четырёх итоговых файлов;
- **Не проверено** — раздел обязателен;
- `git status --short`.

Оценку облика, сравнение попыток и выбор лучшей не делай.

## Не трогать

Все файлы под git. Писать можно только в `.tmp/`.

## Организация работы

- Порядок: сверка SHA-256 входов → генерации `k1` и `k6` → копии и `prompts.md` → `DONE-G1`.
- Параллельно: генерации для `k1` и `k6` независимы.
- Помощники: генерацию изображений делаешь сам; помощнику `gpt-6-luna` `xhigh` можно отдать только сверку SHA-256 и подсчёт SHA-256 итоговых файлов.
- Остановки: SHA-256 входов не совпал или генерация изображений недоступна — `Q-G1-NN` и стоп.
- Рамка правок: только `.tmp/`.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка.
