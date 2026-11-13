# Задание U5-gen — генерации группы C под 63°: Харвестер, ряд 0

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u5`, ветка `codex/u5`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U5.

## Цель

Получить 16 картинок: Харвестер без песка, перерисованный под камеру 63° в восьми направлениях, по две попытки на направление. Облик и выбор попыток оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255). `harvester_old_k<k>.png` — старый спрайт Харвестера из игры, камера 36°; `harvester_guide_k<k>.png` — брусок-ориентир под 63°, стрелка на крыше — направление носа; направления k0…k7: восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U5-gen-01` и стоп.

```text
a6558b8051ed53e915de75e2a8b6a5c91a4db91d66c4b4ec38e4b14d6b51e4e7  .tmp/input/harvester_guide_k0.png
4b75f0ea3a1a2b99d35e192391b6076300546506a96391777a1cedee38518187  .tmp/input/harvester_guide_k1.png
3ea7813f05b228f4c50375edde444c4005941b7b2517638631ada1dcf6a144a2  .tmp/input/harvester_guide_k2.png
32d28ab87ccabff522db4f592ba5871409ca2d7abd10378e43efa1d842b1b730  .tmp/input/harvester_guide_k3.png
1bf174c6295ded108e926b1eec3c957336989f3d00390b6903ffb4d2cb13f576  .tmp/input/harvester_guide_k4.png
ed73460919e235efe4c866c87d7a8091d9597020f70c56e80bdcc171dfe1de62  .tmp/input/harvester_guide_k5.png
85c76e0340c8bda8df6272167fe50fcee10ecf1a7c9b97fc5f610f8e588242f4  .tmp/input/harvester_guide_k6.png
59629cdaeb0721f857de5d3c6fd021be1c04b6655c3a14de53d643f1c94368e4  .tmp/input/harvester_guide_k7.png
2dd1fe02a93d0388846cb1e8491ba3203ff6f1a2e797d296f2f73da585434cd3  .tmp/input/harvester_old_k0.png
5ebf1d51295337d49425133602e412e19dedb3bcbf118c642305755047d78f41  .tmp/input/harvester_old_k1.png
cef8ffdb14ce90d79ac45a2c3147d5982a59ae69952a3f117433c270f348378d  .tmp/input/harvester_old_k2.png
1e948582a3d945640116a3902ff1073c6570a4668354790301d0347b3f0ff2ee  .tmp/input/harvester_old_k3.png
19946b205215a507fdaf61e09953bcdbc1656200037bc7bb3edfc71463a7a33c  .tmp/input/harvester_old_k4.png
6a4bd3ad9a88c3b0d7abc18c56229e3c02b450cd8e77ccfae56c45caca0be8e9  .tmp/input/harvester_old_k5.png
86222f0e3a09a7cd4b606686ef0748ee77b163c45009c6eb2051a7294ac5065b  .tmp/input/harvester_old_k6.png
b2199cf9be71aca08d9e92e37a97be4fc18a48c71b4fe486f2c0670f40f1916e  .tmp/input/harvester_old_k7.png
```

## Что сделать

8 случаев — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out/` под именем `<случай>_<попытка>.png`, например `harvester_k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт | Юнит и направление |
|---|---|---|---|---|
| `harvester_k0` | `harvester_old_k0.png` | `harvester_guide_k0.png` | П-harvester-0 | Харвестер, восток |
| `harvester_k1` | `harvester_old_k1.png` | `harvester_guide_k1.png` | П-harvester-1 | Харвестер, северо-восток |
| `harvester_k2` | `harvester_old_k2.png` | `harvester_guide_k2.png` | П-harvester-2 | Харвестер, север |
| `harvester_k3` | `harvester_old_k3.png` | `harvester_guide_k3.png` | П-harvester-3 | Харвестер, северо-запад |
| `harvester_k4` | `harvester_old_k4.png` | `harvester_guide_k4.png` | П-harvester-4 | Харвестер, запад |
| `harvester_k5` | `harvester_old_k5.png` | `harvester_guide_k5.png` | П-harvester-5 | Харвестер, юго-запад |
| `harvester_k6` | `harvester_old_k6.png` | `harvester_guide_k6.png` | П-harvester-6 | Харвестер, юг |
| `harvester_k7` | `harvester_old_k7.png` | `harvester_guide_k7.png` | П-harvester-7 | Харвестер, юго-восток |

Промпты — дословно, без правок и дополнений.

П-harvester-0:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-1:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-2:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-3:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-4:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-5:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-6:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-harvester-7:

```text
Redraw the harvester from image 1 as seen from a higher camera.
Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same harvester from the camera of image 2, turned the same way as the block: the front of the harvester points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the harvester itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and silver armour, red trim, small glowing yellow lights, the wide dark tracked base, wear and the painted game-sprite look. Keep the size of the harvester as in image 1 and centre it on the canvas.
Fill everything outside the harvester with flat pure magenta RGB 255,0,255. No ground, no sand, no dust, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет Харвестера или их больше одного;
- на картинке есть песок, пыль или земля;
- Харвестер обрезан краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисован брусок или стрелка;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.
Неточный пурпурный фон — не повод для повтора.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 24. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U5-gen | <время UTC из date -u>`:
- `## PLAN-U5-gen` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 16 итоговых файлов;
- «Отказы модерации» — случаи и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.
Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 16 генераций → повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев: два направления; в бриф — промпты дословно, правило копирования, правила повтора и отказа модерации.
- Остановки — блок `## Q-U5-gen-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка и после каждого готового субагента.
