# G3a — журнал промптов

Размер каждого PNG ниже получен чтением файлов: 1254x1254.

| Файл | Случай | Попытка | Входы в порядке подачи | Промпт | Размер | Исходный файл генерации | Повтор |
|---|---|---|---|---|---:|---|---|
| g3_k0_a.png | k0 | a | old_k0.png, затем guide_k0.png | P1 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-33be8655-7faf-4fdb-853d-a336962a65a9.png` | нет |
| g3_k0_b.png | k0 | b | old_k0.png, затем guide_k0.png | P1 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-05d1a83a-1fc0-43b7-a76b-27439359a771.png` | нет |
| g3_k2_a.png | k2 | a | old_k2.png, затем guide_k2.png | P2 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-b5ad436c-1474-449e-9235-f650ca9266db.png` | нет |
| g3_k2_b.png | k2 | b | old_k2.png, затем guide_k2.png | P2 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-1b60c19f-80b5-43a7-beb5-79f684b91816.png` | нет |
| g3_k3_a.png | k3 | a | old_k3.png, затем guide_k3.png | P3 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-e518f3f7-4ebc-407e-baca-0faf0552d4cc.png` | повтор: исходный фон не прошёл порог угловых пикселей; среднее RGB (0, 0, 0). Первичный источник: C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-d0271066-c4b3-4388-a203-b4400a0bc464.png |
| g3_k3_b.png | k3 | b | old_k3.png, затем guide_k3.png | P3 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-d13464e6-503a-4999-b973-36b867bf7260.png` | нет |
| g3_k4_a.png | k4 | a | old_k4.png, затем guide_k4.png | P4 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-6ac5fa77-91e9-4866-b6f3-6e1095c59f39.png` | нет |
| g3_k4_b.png | k4 | b | old_k4.png, затем guide_k4.png | P4 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-3b35f746-9246-433e-b175-621164c0dacb.png` | нет |
| g3_k5_a.png | k5 | a | old_k5.png, затем guide_k5.png | P5 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-b5073821-81c4-4ec7-becb-34fa36738f42.png` | нет |
| g3_k5_b.png | k5 | b | old_k5.png, затем guide_k5.png | P5 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-cda0a0a0-c88e-4d11-b696-b2db4ae9f2b4.png` | нет |
| g3_k7_a.png | k7 | a | old_k7.png, затем guide_k7.png | P6 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-a9d07721-e10a-48cc-b442-b32620f1ab07.png` | повтор: исходный фон не прошёл порог угловых пикселей; среднее RGB (0, 0, 0). Первичный источник: C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-48888515-20c8-4b3c-ae39-dc3b4ae56b77.png |
| g3_k7_b.png | k7 | b | old_k7.png, затем guide_k7.png | P6 | 1254x1254 | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-6fc9ee67-a0e2-4114-992b-76934bfd8497.png` | нет |

## Промпты

### P1

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### P2

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### P3

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### P4

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### P5

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### P6

```text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```


