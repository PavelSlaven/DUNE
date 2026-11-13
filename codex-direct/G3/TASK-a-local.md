# Задание G3a (локальный запуск) — Девастатор под 63°: шесть направлений

stop caveman. Пиши полным литературным языком.

Режим: работу ведёшь сам, без остановок до сдачи. Плана на утверждение не нужно: первой частью сдачи запиши `## PLAN-G3a` для записи. Исполнитель: Codex `gpt-6-luna` `xhigh` на ПК владельца, с инструментом генерации изображений `image_gen__imagegen`.
Рабочая папка: `C:\Users\Slaven\AppData\Local\Temp\claude\C--Users-Slaven-Projects-DUNE\22d0d3cf-a572-4607-9206-d93f8c915e9c\scratchpad\codex\g3a-local\work` — папка, из которой тебя запустили. Она не репозиторий git.

## Цель

Получить двенадцать картинок: старый спрайт танка из игры в шести направлениях, перерисованный так, будто камера поднята с 36° до 63° над горизонтом. Танк должен остаться тем же: дизайн, детали, материалы и окраска — из старого спрайта; ракурс и направление носа — из бруска-ориентира. Облик оценивает ведущий, не ты.

## Входы

Папка `.tmp\input\` рабочей папки. Все файлы — 1024×1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файл | Что это |
|---|---|
| `old_k0.png` | старый спрайт танка, направление «восток» |
| `guide_k0.png` | брусок-ориентир под 63°, нос — на восток |
| `old_k2.png` | старый спрайт танка, направление «север» |
| `guide_k2.png` | брусок-ориентир под 63°, нос — на север |
| `old_k3.png` | старый спрайт танка, направление «северо-запад» |
| `guide_k3.png` | брусок-ориентир под 63°, нос — на северо-запад |
| `old_k4.png` | старый спрайт танка, направление «запад» |
| `guide_k4.png` | брусок-ориентир под 63°, нос — на запад |
| `old_k5.png` | старый спрайт танка, направление «юго-запад» |
| `guide_k5.png` | брусок-ориентир под 63°, нос — на юго-запад |
| `old_k7.png` | старый спрайт танка, направление «юго-восток» |
| `guide_k7.png` | брусок-ориентир под 63°, нос — на юго-восток |

Перед работой сверь SHA-256 входов с этим списком. При расхождении — `Q-G3a-01` и стоп.

```text
c108d0c2fa9a5cbf8ad1ff77dc1f4e5116ae2af44a8445c2357ab9c3a6179ded  .tmp/input/guide_k0.png
266ec21142f4d8118c60270388dbe40a907049e6ba11c40dcf8eea4bc9558093  .tmp/input/guide_k2.png
d388e518e0dd564ed5bc4a7a2890819bef46ef57c6e1f782448851edf32e19c8  .tmp/input/guide_k3.png
3f7f11d4aad26a2823dc6aadc1dc36b6c23bcc9255e163d63745d35ae3767367  .tmp/input/guide_k4.png
53357bc7633db96d9665dbb52c9dc97f511b204e14bc070e670ef45b2b2b56ad  .tmp/input/guide_k5.png
3965b944df5a52f5c06d6b9c563e63855351f88149aacfe945027912f0b2c219  .tmp/input/guide_k7.png
e52f9320940b88b3f41e74c1c21bdae3c797627b28bb5ca4e5be612f738005aa  .tmp/input/old_k0.png
c4bc3982dd24c0a5bbe45d0357ef79c43bf09295eda5d9b3727f33b3153173ea  .tmp/input/old_k2.png
32917341fbd30fca638abd429c59053b4f2d975abc5d3d2fc5644ee0849c6c25  .tmp/input/old_k3.png
033f0b0259c35b0422c6f584d361ace7958342226c3d35ceb031311ab0617a30  .tmp/input/old_k4.png
1d94a41cbfd700dc7a91e78e54ef6d8341357e3dc1446b85a0841a6bfc53677a  .tmp/input/old_k5.png
66bd9e0dc7dcca3ad928402a57450739203fb22a3229cdeaba44c25b407cbbea  .tmp/input/old_k7.png
```

## Что сделать

Шесть случаев. Для каждого случая вызови `image_gen__imagegen` с промптом этого случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`.

| Случай | Первое изображение | Второе изображение | Промпт | Направление |
|---|---|---|---|---|
| `k0` | `old_k0.png` | `guide_k0.png` | П1 | восток |
| `k2` | `old_k2.png` | `guide_k2.png` | П2 | север |
| `k3` | `old_k3.png` | `guide_k3.png` | П3 | северо-запад |
| `k4` | `old_k4.png` | `guide_k4.png` | П4 | запад |
| `k5` | `old_k5.png` | `guide_k5.png` | П5 | юго-запад |
| `k7` | `old_k7.png` | `guide_k7.png` | П6 | юго-восток |

Скопируй каждую полученную картинку в `.tmp\out\` под именем `g3_<случай>_<попытка>.png`, например `g3_k0_a.png`. Размер не меняй: копируй файл генерации как есть. Если скопировать файл генерации в рабочую папку невозможно, запиши в сдачу полный путь каждого файла и продолжай.

Запиши `.tmp\out\prompts.md`: по каждой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

Промпты — дословно, без правок и дополнений.

П1:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П2:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П3:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П4:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П5:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П6:

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Попытку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет танка или танков больше одного;
- танк обрезан краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисован брусок или стрелка;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.

Неточный пурпурный фон (например, RGB 244, 12, 243) — не повод для повтора. Причину повтора запиши в `prompts.md`. Всего генераций, вместе с повторами, — не больше 16.

## Сдача

Последнее сообщение — `## DONE-G3a | время UTC`:
- `## PLAN-G3a` для записи: шаги по порядку;
- таблица: файл в `.tmp\out\` → случай → попытка → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 двенадцати итоговых файлов;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика, сравнение попыток и выбор лучшей не делай. Числа в сдаче — только из вывода команд. Не выдумывай файлы и результаты; непроверенное помечай «не проверено».

## Не трогать

Писать можно только в `.tmp\` рабочей папки. Файлы вне рабочей папки только читать. Ничего не устанавливать и не скачивать.

## Организация работы

- Порядок: сверка SHA-256 входов → генерации шести случаев → копии и `prompts.md` → `DONE-G3a`.
- Параллельно: генерации шести случаев независимы.
- Помощники: не запускай; всё делаешь сам.
- Остановки — блок `## Q-G3a-NN` и стоп:
  - SHA-256 входов не совпал;
  - `image_gen__imagegen` недоступен;
  - `image_gen__imagegen` не принимает два входных изображения — генерацию без них не делай;
  - команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp\`.
- Журнал: `.tmp\progress.md`, строка после каждого шага порядка.
- Без фоновых команд: после твоей остановки тебя никто не разбудит.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
