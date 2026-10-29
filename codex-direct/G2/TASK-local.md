# Задание G2 (локальный запуск) — проба: перерисовка старого спрайта Девастатора под угол камеры 63°

stop caveman. Пиши полным литературным языком.

Режим: работу ведёшь сам, без остановок до сдачи. Плана на утверждение не нужно: первой частью сдачи запиши `## PLAN-G2` для записи. Исполнитель: Codex `gpt-6-luna` `xhigh` на ПК владельца, с инструментом генерации изображений `image_gen__imagegen`.
Рабочая папка: `C:\Users\Slaven\AppData\Local\Temp\claude\C--Users-Slaven-Projects-DUNE\22d0d3cf-a572-4607-9206-d93f8c915e9c\scratchpad\codex\g2-local\work` — папка, из которой тебя запустили. Она не репозиторий git.

## Цель

Получить восемь картинок: старый спрайт танка из игры, перерисованный так, будто камера поднята с 36° до 63° над горизонтом. Танк должен остаться тем же: дизайн, детали, материалы и окраска — из старого спрайта. Проба сравнивает два способа задать новый угол камеры: `v1` — здание игры как пример ракурса, `v2` — серый брусок-ориентир с точным ракурсом и направлением. Облик оценивает ведущий, не ты.

## Входы

Папка `.tmp\input\` рабочей папки. Все файлы — 1024×1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файл | Что это |
|---|---|
| `old_k1.png` | старый спрайт танка, направление «северо-восток» |
| `old_k6.png` | старый спрайт танка, направление «юг» |
| `factory.png` | здание игры, снятое целевой камерой |
| `guide_k1.png` | брусок-ориентир под 63°, нос — на северо-восток |
| `guide_k6.png` | брусок-ориентир под 63°, нос — на юг |

Перед работой сверь SHA-256 входов с этим списком. При расхождении — `Q-G2-01` и стоп.

```text
135742f7f01c8670401dc9a4fd73f3d1b238768b3e03008910685d47607bd694  .tmp/input/factory.png
7a735914bc51b71c4c4772f28e1152b1c24ad7f0416e8e48d758be3620a7d4b2  .tmp/input/guide_k1.png
4ab4a76178a91d742f6385e7fd8e068ba3a1c44609dac7b404f25396793240f0  .tmp/input/guide_k6.png
7ce5426bb1389c932ccf427438b5546e9f3795a72398f1651398921265b14dd4  .tmp/input/old_k1.png
5e3537fe661e22de5cd85b1e8a416d1ed1500593e853e2d5b03e1af301f4f8c8  .tmp/input/old_k6.png
```

## Что сделать

Четыре случая. Для каждого случая вызови `image_gen__imagegen` с промптом этого случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`.

| Случай | Первое изображение | Второе изображение | Промпт |
|---|---|---|---|
| `v1_k1` | `old_k1.png` | `factory.png` | П1 |
| `v1_k6` | `old_k6.png` | `factory.png` | П2 |
| `v2_k1` | `old_k1.png` | `guide_k1.png` | П3 |
| `v2_k6` | `old_k6.png` | `guide_k6.png` | П4 |

Скопируй каждую полученную картинку в `.tmp\out\` под именем `g2_<случай>_<попытка>.png`, например `g2_v1_k1_a.png`. Размер не меняй: копируй файл генерации как есть. Если скопировать файл генерации в рабочую папку невозможно, запиши в сдачу полный путь каждого файла и продолжай.

Запиши `.tmp\out\prompts.md`: по каждой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

Промпты — дословно, без правок и дополнений.

П1:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a building from the same game, seen from the target camera: orthographic, about 63 degrees above the horizon, a steep top-down view.
Show the same tank from the camera of image 2: more of the roof and top surfaces, less of the sides. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the facing direction of image 1: the front of the tank with its gun barrels points up and to the right, toward the top-right corner. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the building.
```

П2:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a building from the same game, seen from the target camera: orthographic, about 63 degrees above the horizon, a steep top-down view.
Show the same tank from the camera of image 2: more of the roof and top surfaces, less of the sides. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the facing direction of image 1: the front of the tank with its gun barrels points straight down, toward the viewer. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the building.
```

П3:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П4:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, straight down toward the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Попытку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет танка или танков больше одного;
- танк обрезан краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисовано здание, брусок или стрелка;
- фон не пурпурный: среднее значение канала G четырёх угловых пикселей больше 100.

Неточный пурпурный фон (например, RGB 244, 12, 243) — не повод для повтора. Причину повтора запиши в `prompts.md`. Всего генераций, вместе с повторами, — не больше 12.

## Сдача

Последнее сообщение — `## DONE-G2 | время UTC`:
- `## PLAN-G2` для записи: шаги по порядку;
- таблица: файл в `.tmp\out\` → случай → попытка → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 восьми итоговых файлов;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика, сравнение попыток и выбор лучшей не делай. Числа в сдаче — только из вывода команд. Не выдумывай файлы и результаты; непроверенное помечай «не проверено».

## Не трогать

Писать можно только в `.tmp\` рабочей папки. Файлы вне рабочей папки только читать. Ничего не устанавливать и не скачивать.

## Организация работы

- Порядок: сверка SHA-256 входов → генерации четырёх случаев → копии и `prompts.md` → `DONE-G2`.
- Параллельно: генерации четырёх случаев независимы.
- Помощники: не запускай; всё делаешь сам.
- Остановки — блок `## Q-G2-NN` и стоп:
  - SHA-256 входов не совпал;
  - `image_gen__imagegen` недоступен;
  - `image_gen__imagegen` не принимает два входных изображения — генерацию без них не делай.
- Рамка правок: только `.tmp\`.
- Журнал: `.tmp\progress.md`, строка после каждого шага порядка.
- Без фоновых команд: после твоей остановки тебя никто не разбудит.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
