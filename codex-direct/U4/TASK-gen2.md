# Задание U4-gen2 — генерации группы B под 63°: корпус и башня Осадного

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u4s`, ветка `codex/u4s`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U4.

## Цель

Получить 32 картинки: корпус Осадного без башни и башню Осадного отдельно, перерисованные под камеру 63° в восьми направлениях, по две попытки на направление. Облик и выбор попыток оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255). `<часть>_old_k<k>.png` — старый спрайт части юнита из игры, камера 36°; `<часть>_guide_k<k>.png` — брусок-ориентир под 63°, стрелка на крыше — направление носа корпуса или ствола башни. Части: `siegebase` — корпус Осадного без башни, `siegetop` — башня Осадного без корпуса; направления k0…k7: восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U4-gen2-01` и стоп.

```text
c50a1cd3de789d43e8f742811544c96bae796ceb012d4353b532cce12ca08030  .tmp/input/siegebase_guide_k0.png
5cee29e98a5ce337be05a0d1b8cc8ffdfcd33b2429a8e11ce9bd4bab1e105f57  .tmp/input/siegebase_guide_k1.png
218df44d936910552b5f96f6dcabb25a1e972c833ffd9bbccc107ca9c9ecb27a  .tmp/input/siegebase_guide_k2.png
1da1baf960061bb49495dcf7d44aaba1937a70920c414791d0db9e2742ff5410  .tmp/input/siegebase_guide_k3.png
f4a6b2f6de90f25423e55a71328b8ffd00a010885640c7ae400180279b8e3485  .tmp/input/siegebase_guide_k4.png
7a637f0da647eca765facad9d0fbc63d516b3e70c4872bcab1145196d4b9aece  .tmp/input/siegebase_guide_k5.png
9ca90abf633f75d5c54de1078a0decfd9a0363d6e078a209845046853180327d  .tmp/input/siegebase_guide_k6.png
0960023f2de9784d9d9bc551c1a282183d150604354ae407ec49726217fea4f6  .tmp/input/siegebase_guide_k7.png
fbdf8c2adbd2db96d6885c6aa5591d86156ff5cab6b93f4bcefd9813302ba87f  .tmp/input/siegebase_old_k0.png
876a3e1a56bfa5d0eeef351ff48e3f5b1599e1da4f57b9ce906355b0c5984a92  .tmp/input/siegebase_old_k1.png
8ba37519c67a50005ce7de920e18d89b4b47cecb8c4699d5b19e28d818fc461e  .tmp/input/siegebase_old_k2.png
fd1ae48df3637927a83ab55886b63c5c66d0efc720bd30381f7e59b7b9d9af30  .tmp/input/siegebase_old_k3.png
162d0da1690c38fb1acc3c231d719fee1e97132318bcc84cfd83f8cdb84456b0  .tmp/input/siegebase_old_k4.png
87f3f7cb3dc9fdaa3cafcd48948a8089e155097f3a92ba3e6c4ad199e88a9a24  .tmp/input/siegebase_old_k5.png
a62cafdab97a5c1604622234df104514dd8e5a4a5647d776427ba426ab602148  .tmp/input/siegebase_old_k6.png
ee6ebaf9fbbab64f217771c78a08d71b37bf66f875bcfe291c4230e615efe6cf  .tmp/input/siegebase_old_k7.png
24650b5941ecd584d0acef92f2afc9fd74f6dbb864c558720ed2b475e194d6c3  .tmp/input/siegetop_guide_k0.png
09fd408fd0a60e7823d7dd5767c0a04350f68658d2b8a054742513b0a5748286  .tmp/input/siegetop_guide_k1.png
a28240e324129b9c3fe927b3be69c4191170e99d7723b1a4888ada1923098e4f  .tmp/input/siegetop_guide_k2.png
d334813604f2fe92284e9e12c6488ed8afc8550a2cf21c01462efd5fdac449b6  .tmp/input/siegetop_guide_k3.png
2bc012d512f66abae478a87d38631f35994c7fe056b162a616ba328b2dcb8b3c  .tmp/input/siegetop_guide_k4.png
1c925e68efb0592e2398b3b799d315f7af67b580dbe189af1dde056ebae7a629  .tmp/input/siegetop_guide_k5.png
3f09cc7e7b13457614938146ad3bc07e5c89d9b5dbdaaaae56903d6cb41e08b0  .tmp/input/siegetop_guide_k6.png
37f258668d27c45d07d22adf783ad7f11b97d70c21eb6c64f47f4f9e973a5ee3  .tmp/input/siegetop_guide_k7.png
546f864f7059b21330c2fc856ab69df07e78578ba2b9b75e8f6f65f875694538  .tmp/input/siegetop_old_k0.png
45903994ba91c20626d4adad1af0170d9e9bebbc0ef5069af4785fdbbbe7092c  .tmp/input/siegetop_old_k1.png
bff93c12567599992527d82d19537a79a914abf72d049473da6e01741ac9daf7  .tmp/input/siegetop_old_k2.png
f042a9dc25cc177f911fc022a30bc5b16ac9e93fc1a2b9afa7f376407a7335d2  .tmp/input/siegetop_old_k3.png
318d47d9f662edefa5b2f1519d137fefa14fa45d19436d9436594858b2231b55  .tmp/input/siegetop_old_k4.png
80b1f9b18368981a99d682cdaadc6a673fdf0d723cb811d581b597c0df228227  .tmp/input/siegetop_old_k5.png
65752e870a4c3a1b748a901ec433b7415bb51fcc58adc1b48b879fe4db81ad45  .tmp/input/siegetop_old_k6.png
6c2084a771c6113dd51ca6c208bc7c8a336c2a36b0f998f9a16b5eb743d0f517  .tmp/input/siegetop_old_k7.png
```

## Что сделать

16 случаев — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out/` под именем `<случай>_<попытка>.png`, например `siegebase_k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт | Часть и направление |
|---|---|---|---|---|
| `siegebase_k0` | `siegebase_old_k0.png` | `siegebase_guide_k0.png` | П-siegebase-0 | корпус Осадного, восток |
| `siegebase_k1` | `siegebase_old_k1.png` | `siegebase_guide_k1.png` | П-siegebase-1 | корпус Осадного, северо-восток |
| `siegebase_k2` | `siegebase_old_k2.png` | `siegebase_guide_k2.png` | П-siegebase-2 | корпус Осадного, север |
| `siegebase_k3` | `siegebase_old_k3.png` | `siegebase_guide_k3.png` | П-siegebase-3 | корпус Осадного, северо-запад |
| `siegebase_k4` | `siegebase_old_k4.png` | `siegebase_guide_k4.png` | П-siegebase-4 | корпус Осадного, запад |
| `siegebase_k5` | `siegebase_old_k5.png` | `siegebase_guide_k5.png` | П-siegebase-5 | корпус Осадного, юго-запад |
| `siegebase_k6` | `siegebase_old_k6.png` | `siegebase_guide_k6.png` | П-siegebase-6 | корпус Осадного, юг |
| `siegebase_k7` | `siegebase_old_k7.png` | `siegebase_guide_k7.png` | П-siegebase-7 | корпус Осадного, юго-восток |
| `siegetop_k0` | `siegetop_old_k0.png` | `siegetop_guide_k0.png` | П-siegetop-0 | башня Осадного, восток |
| `siegetop_k1` | `siegetop_old_k1.png` | `siegetop_guide_k1.png` | П-siegetop-1 | башня Осадного, северо-восток |
| `siegetop_k2` | `siegetop_old_k2.png` | `siegetop_guide_k2.png` | П-siegetop-2 | башня Осадного, север |
| `siegetop_k3` | `siegetop_old_k3.png` | `siegetop_guide_k3.png` | П-siegetop-3 | башня Осадного, северо-запад |
| `siegetop_k4` | `siegetop_old_k4.png` | `siegetop_guide_k4.png` | П-siegetop-4 | башня Осадного, запад |
| `siegetop_k5` | `siegetop_old_k5.png` | `siegetop_guide_k5.png` | П-siegetop-5 | башня Осадного, юго-запад |
| `siegetop_k6` | `siegetop_old_k6.png` | `siegetop_guide_k6.png` | П-siegetop-6 | башня Осадного, юг |
| `siegetop_k7` | `siegetop_old_k7.png` | `siegetop_guide_k7.png` | П-siegetop-7 | башня Осадного, юго-восток |

Промпты — дословно, без правок и дополнений.

П-siegebase-0:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-1:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-2:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-3:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-4:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-5:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-6:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegebase-7:

```text
Redraw the siege tank hull from image 1 as seen from a higher camera.
Image 1 is a sprite of the hull of a large tracked siege tank from a real-time strategy game, without its turret: on top of the hull there is an empty round turret ring. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same hull from the camera of image 2, turned the same way as the block: the front of the hull points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the hull itself exactly as in image 1: its design, every part and its position on the hull, the empty round turret ring on top, proportions, materials, colours, dark charcoal armour plates, small glowing cyan lights, wide dark tracks, wear and the painted game-sprite look. Do not add a turret. Keep the size of the hull as in image 1 and centre it on the canvas.
Fill everything outside the hull with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-0:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-1:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-2:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-3:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-4:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-5:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-6:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-siegetop-7:

```text
Redraw the siege tank turret from image 1 as seen from a higher camera.
Image 1 is a sprite of a separate heavy turret with a blocky armoured top on a round base and two long parallel barrels from a real-time strategy game, drawn alone, without a hull under it. It is seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same turret from the camera of image 2, turned the same way as the block: the two barrels point where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the turret itself exactly as in image 1: its design, every part and its position on the turret, the round base, the two long barrels, proportions, materials, colours, dark charcoal armour, wear and the painted game-sprite look. Draw the turret alone, without a hull, tracks or ground under it. Keep the size of the turret as in image 1 and centre it on the canvas.
Fill everything outside the turret with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет корпуса (для `siegebase`) или башни (для `siegetop`), или их больше одного;
- на картинке корпуса `siegebase` есть башня или ствол;
- на картинке башни `siegetop` есть корпус, гусеницы или земля;
- часть обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисован брусок или стрелка;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.
Неточный пурпурный фон — не повод для повтора.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 48. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U4-gen2 | <время UTC из date -u>`:
- `## PLAN-U4-gen2` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 32 итоговых файлов;
- «Отказы модерации» — случаи и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.
Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 32 генерации → повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев: одна часть и четыре направления; в бриф — промпты дословно, правило копирования, правила повтора и отказа модерации.
- Остановки — блок `## Q-U4-gen2-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка и после каждой готовой части.
