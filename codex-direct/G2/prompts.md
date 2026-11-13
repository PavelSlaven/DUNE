# G2: результаты генерации

## Изображения

| Имя | Случай | Попытка | Входы в порядке подачи | Промпт | Размер | Исходный файл генерации | Повтор |
|---|---|---|---|---|---|---|---|
| g2_v1_k1_a.png | v1_k1 | a | old_k1.png, factory.png | П1 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-bcfc74ae-33f9-488e-9b63-4b7247df66bb.png | нет |
| g2_v1_k1_b.png | v1_k1 | b | old_k1.png, factory.png | П1 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-9583bd04-1de2-41b2-973f-9b175dd3a900.png | нет |
| g2_v1_k6_a.png | v1_k6 | a | old_k6.png, factory.png | П2 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-f611f6cd-8b06-49c1-b49c-6fbb53b035ba.png | нет |
| g2_v1_k6_b.png | v1_k6 | b | old_k6.png, factory.png | П2 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-4c0c48d5-659e-43c9-a9ba-b40eba71239e.png | нет |
| g2_v2_k1_a.png | v2_k1 | a | old_k1.png, guide_k1.png | П3 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-2092efdd-2290-430e-80a9-92062d04d78d.png | нет |
| g2_v2_k1_b.png | v2_k1 | b | old_k1.png, guide_k1.png | П3 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-d0f60a20-d258-4388-a0a4-6de8d07f5130.png | нет |
| g2_v2_k6_a.png | v2_k6 | a | old_k6.png, guide_k6.png | П4 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-79df2e7e-ff47-4720-bd05-d2496fd8647d.png | нет |
| g2_v2_k6_b.png | v2_k6 | b | old_k6.png, guide_k6.png | П4 | 1254x1254 | C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-117d195c-2db8-43c1-bcb7-344103f33ae9.png | нет |

## Точные тексты промптов

### П1
~~~text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a building from the same game, seen from the target camera: orthographic, about 63 degrees above the horizon, a steep top-down view.
Show the same tank from the camera of image 2: more of the roof and top surfaces, less of the sides. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the facing direction of image 1: the front of the tank with its gun barrels points up and to the right, toward the top-right corner. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the building.
~~~

### П2
~~~text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a building from the same game, seen from the target camera: orthographic, about 63 degrees above the horizon, a steep top-down view.
Show the same tank from the camera of image 2: more of the roof and top surfaces, less of the sides. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the facing direction of image 1: the front of the tank with its gun barrels points straight down, toward the viewer. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the building.
~~~

### П3
~~~text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
~~~

### П4
~~~text
Redraw the tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a heavy tank from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same tank from the camera of image 2, turned the same way as the block: the front of the tank with its gun barrels points where the arrow points, straight down toward the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the tank itself exactly as in image 1: its design, every part, proportions, materials, colours, orange accent panels, wear and the painted game-sprite look. Keep the size of the tank as in image 1 and centre it on the canvas.
Fill everything outside the tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
~~~


## Условия повтора
У g2_v2_k6_a.png все четыре угловых пикселя имеют G=0; среднее 0.0 не превышает заданный порог G>100. Повтор не выполнялся.
