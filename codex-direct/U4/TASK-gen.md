# Задание U4-gen — генерации пробы группы B под 63°: корпус и башня Танка

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u4`, ветка `codex/u4`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U4.

## Цель

Получить 32 картинки: корпус Танка без башни и башню Танка отдельно, перерисованные под камеру 63° в восьми направлениях, по две попытки на направление. Облик и выбор попыток оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255). `<часть>_old_k<k>.png` — старый спрайт части юнита из игры, камера 36°; `<часть>_guide_k<k>.png` — брусок-ориентир под 63°, стрелка на крыше — направление носа корпуса или ствола башни. Части: `tankbase` — корпус Танка без башни, `tanktop` — башня Танка без корпуса; направления k0…k7: восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U4-gen-01` и стоп.

```text
1adb42230c30e7da688d92a3b2db56a0751b31d21bd72bef7a8d5a3da2599339  .tmp/input/tankbase_guide_k0.png
0b5c93526bff5efd028c27e015455fe16e348d4900896fca7a2448d24f06e96c  .tmp/input/tankbase_guide_k1.png
1bf08edc9ac0da387b766c02f89698662a0d57d94ee1c4c8d9bb6022cbc0559b  .tmp/input/tankbase_guide_k2.png
8de8d0a27632b4dc74a5bde26da56f3b14eb2a1d59d1998e24392707fd0213c8  .tmp/input/tankbase_guide_k3.png
7f1e12755e79851673aec40da7b923fe48217c69d84419bf13fc69b900858d3a  .tmp/input/tankbase_guide_k4.png
568fed6e401ef9abc27e0dec2ae181680d10bc6a34e24addfb7eb46e6c3fdd5e  .tmp/input/tankbase_guide_k5.png
ea0d0a6e1a9b3e37ad14ff5b2decc3b4be5db6b5b876127de2cba4180458b84e  .tmp/input/tankbase_guide_k6.png
503eb05114ed5d81c16f886ef4ab19cec3d353657370a4e915688267580bcf27  .tmp/input/tankbase_guide_k7.png
e8268a8ba305c5d312c1a1e66b3c31feef504a0606cc0a7f94f29b6a3c0cf081  .tmp/input/tankbase_old_k0.png
78d530216b136376f8d7debb505b3d9bc98de527caf87454952de7382d688c06  .tmp/input/tankbase_old_k1.png
7475dc0d06c9cdb8470daf179fa1f1f79ade81e02d4dbe23874e12f99382aad9  .tmp/input/tankbase_old_k2.png
ebc8e2604adfc8dd47333a3a4fed505269247c90c78a33b13702cb259185066a  .tmp/input/tankbase_old_k3.png
dc33d6b1ba0acd196d67dc50c6b61e9dcd94b5d0621224c867ffbe27a330daa6  .tmp/input/tankbase_old_k4.png
dccb965df7080663417ec75a376e9cc9c778a17643dcdcd5369ba623c21b536b  .tmp/input/tankbase_old_k5.png
c8752ea740881226044e2531a5bac53fb316e5380cfe67c229d53693a4e7d031  .tmp/input/tankbase_old_k6.png
b6856b48903f2428f0b2169caf572b7192cd5ca53cbe77791bcfacf9b829de57  .tmp/input/tankbase_old_k7.png
6a686e1432542e8bee769cc964eac0e9c915e9a350a2cad0168b14b31c602f10  .tmp/input/tanktop_guide_k0.png
c38ae796c94eb17415e225ff752256bbede3dfd9dfca8b4493831a444dc30c19  .tmp/input/tanktop_guide_k1.png
2c3178a956a09017b8a7f296e9f79b61cb0986fd71082780e06ca81d480a8f7c  .tmp/input/tanktop_guide_k2.png
d5bc8db0c57ccc526a7482026ce1e8a619d078e06a25ca5f413df13892eab2d0  .tmp/input/tanktop_guide_k3.png
bc7bb6d8b6454c14d4797ee670e827a53b2a8682eaf6d90de568163fac35445d  .tmp/input/tanktop_guide_k4.png
d17ac9c210b3b77ee491e09ea68286d03bc5296f8335419c4a0378cccd150aa0  .tmp/input/tanktop_guide_k5.png
916df2cc44b6ebfdf356fbcb2d9c47e414377bf30c122f2fb28fe14375cff822  .tmp/input/tanktop_guide_k6.png
4719211602d00c50f3b3105b65d57e3369088dd5be2f8a5fd1f4717b723c8e61  .tmp/input/tanktop_guide_k7.png
aede9cd59a2a2d47bf6df22f7693c9c019913b47839329316637dc0b3bcdfd3a  .tmp/input/tanktop_old_k0.png
2e2a824489765f5003162094bf6ed3ace43347d1c97220f5af17321afedd677c  .tmp/input/tanktop_old_k1.png
d11a84984686e7fdd10205e795ce15caef154fffaba6eb26b8fc698a6f15fbd6  .tmp/input/tanktop_old_k2.png
56fc8b07d38c6183067562edaa4fce169996cea5d52d990975077fafebebd0c1  .tmp/input/tanktop_old_k3.png
d25e3639a103c18b11873611193cb7100fb82afe080753c678facf932f318ceb  .tmp/input/tanktop_old_k4.png
ac155e5c5854e820e2f628bcf2c021a459b5f3452b72c42916765b81bb01fd98  .tmp/input/tanktop_old_k5.png
3a0a32deaa2ff5fad877101fcf32187352955c2d6d3ee755bedac32882bb451c  .tmp/input/tanktop_old_k6.png
c2a102dd84c74d1e08d4dbc48d4acc5d22e8b683d9b108659540e238131937f7  .tmp/input/tanktop_old_k7.png
```

## Что сделать

16 случаев — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out/` под именем `<случай>_<попытка>.png`, например `tankbase_k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт | Часть и направление |
|---|---|---|---|---|
| `tankbase_k0` | `tankbase_old_k0.png` | `tankbase_guide_k0.png` | П-tankbase-0 | корпус Танка, восток |
| `tankbase_k1` | `tankbase_old_k1.png` | `tankbase_guide_k1.png` | П-tankbase-1 | корпус Танка, северо-восток |
| `tankbase_k2` | `tankbase_old_k2.png` | `tankbase_guide_k2.png` | П-tankbase-2 | корпус Танка, север |
| `tankbase_k3` | `tankbase_old_k3.png` | `tankbase_guide_k3.png` | П-tankbase-3 | корпус Танка, северо-запад |
| `tankbase_k4` | `tankbase_old_k4.png` | `tankbase_guide_k4.png` | П-tankbase-4 | корпус Танка, запад |
| `tankbase_k5` | `tankbase_old_k5.png` | `tankbase_guide_k5.png` | П-tankbase-5 | корпус Танка, юго-запад |
| `tankbase_k6` | `tankbase_old_k6.png` | `tankbase_guide_k6.png` | П-tankbase-6 | корпус Танка, юг |
| `tankbase_k7` | `tankbase_old_k7.png` | `tankbase_guide_k7.png` | П-tankbase-7 | корпус Танка, юго-восток |
| `tanktop_k0` | `tanktop_old_k0.png` | `tanktop_guide_k0.png` | П-tanktop-0 | башня Танка, восток |
| `tanktop_k1` | `tanktop_old_k1.png` | `tanktop_guide_k1.png` | П-tanktop-1 | башня Танка, северо-восток |
| `tanktop_k2` | `tanktop_old_k2.png` | `tanktop_guide_k2.png` | П-tanktop-2 | башня Танка, север |
| `tanktop_k3` | `tanktop_old_k3.png` | `tanktop_guide_k3.png` | П-tanktop-3 | башня Танка, северо-запад |
| `tanktop_k4` | `tanktop_old_k4.png` | `tanktop_guide_k4.png` | П-tanktop-4 | башня Танка, запад |
| `tanktop_k5` | `tanktop_old_k5.png` | `tanktop_guide_k5.png` | П-tanktop-5 | башня Танка, юго-запад |
| `tanktop_k6` | `tanktop_old_k6.png` | `tanktop_guide_k6.png` | П-tanktop-6 | башня Танка, юг |
| `tanktop_k7` | `tanktop_old_k7.png` | `tanktop_guide_k7.png` | П-tanktop-7 | башня Танка, юго-восток |

Промпты — дословно, без правок и дополнений.

П-tankbase-0:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-1:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-2:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-3:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-4:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-5:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-6:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tankbase-7:

```text
Redraw the tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a tracked tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark grey-green armour, glowing cyan lights, dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-0:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-1:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-2:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-3:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-4:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-5:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-6:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-tanktop-7:

```text
Redraw the tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate round tank turret with one long barrel from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the barrel points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the long barrel, proportions, materials, colours, dark grey-green armour, glowing cyan lights, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет корпуса (для `tankbase`) или башни (для `tanktop`), или их больше одного;
- на картинке корпуса `tankbase` есть башня или ствол;
- на картинке башни `tanktop` есть корпус, гусеницы или земля;
- часть обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисован брусок или стрелка;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.
Неточный пурпурный фон — не повод для повтора.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 48. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U4-gen | <время UTC из date -u>`:
- `## PLAN-U4-gen` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 32 итоговых файлов;
- «Отказы модерации» — случаи и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.
Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 32 генерации → повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев: одна часть и четыре направления; в бриф — промпты дословно, правило копирования, правила повтора и отказа модерации.
- Остановки — блок `## Q-U4-gen-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка и после каждой готовой части.
