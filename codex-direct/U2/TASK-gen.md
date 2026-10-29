# Задание U2-gen — генерации пробы U2: Квадроцикл под 63° и перекраска Девастатора по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u2`, ветка `codex/u2`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U2.

## Цель

Получить 24 картинки: Квадроцикл, перерисованный под камеру 63° в восьми направлениях, по две попытки на направление (16 картинок), и восемь перекрасок Девастатора, где зелёным окрашены части цвета Дома по образцу старой маски. Облик, выбор попыток и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `old_k0.png` … `old_k7.png` | старый спрайт Квадроцикла из игры, камера 36°, направления k0…k7 |
| `guide_k0.png` … `guide_k7.png` | брусок-ориентир под 63°, стрелка на крыше — направление носа |
| `pick_k0.png` … `pick_k7.png` | новый Девастатор под 63°, направления k0…k7 |
| `oldmask_k0.png` … `oldmask_k7.png` | старый Девастатор, камера 36°: части цвета Дома залиты чистым зелёным |

Направления: k0 — восток, k1 — северо-восток, k2 — север, k3 — северо-запад, k4 — запад, k5 — юго-запад, k6 — юг, k7 — юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U2-gen-01` и стоп.

```text
cfbebe56245bf53fcc0f675aa4297490a2f38b17c53c1bb0a3f3eddd73fcc881  .tmp/input/guide_k0.png
1ea4dd0ffe357bdf9ea4e5bfe9bc70ec4b3006f6b47bd39f40de9799e973918a  .tmp/input/guide_k1.png
afcf56aaa479d9713ab6887f7238bf2c7961940e86f9a8a900b418f3653693c3  .tmp/input/guide_k2.png
346fe9ab7f6233e8e68ce25fa48f5d70ab3218fbeba817b73f71296de1979f7e  .tmp/input/guide_k3.png
9bfbac7c83fba91243447d0642197fbae3d52017f6b59e112d5b3d3e74611afa  .tmp/input/guide_k4.png
5d7ccefc3b1fadee4ea20c660151119a7dac72942769442d31ee840fa268f45c  .tmp/input/guide_k5.png
c14ff36122a60bb47350e44f2d9ab969e4bdde107e198a94d5b6724ebb482179  .tmp/input/guide_k6.png
9b206a86badb56d86a3243f9250ceb175bbb6b4f688c01adfb0ac188a3399e41  .tmp/input/guide_k7.png
42df357bba11c086da5d190a931701dfb436eaba2230789cf04525b352c0ee69  .tmp/input/old_k0.png
afac4ff03946ac20844f85f0b0e76c679e766bf957666d2785f080b1e2512ea9  .tmp/input/old_k1.png
e9851f0a6dd9838537354957fd5a488c3d5364a99793a02ac0ec0ddabf9b978e  .tmp/input/old_k2.png
01a76d95b0e0c159b654f0480a915299884d9f225a9e88bfe640f946d9f3c9ea  .tmp/input/old_k3.png
655b894f0c1e72722881f97189ef68558e08e11cbf17d5db4e91048ce4406fae  .tmp/input/old_k4.png
5530d3aa36f437844285178276db4eb43215cce6245684b803805873ee585082  .tmp/input/old_k5.png
44b51dcdfceab313991409849ee4825782fbcff5155ff99a188a6200eff81810  .tmp/input/old_k6.png
fb02aa29edb4133d8b44c62179bc86c616f2dfc0745dc0fe742ec615e25fb2cb  .tmp/input/old_k7.png
4c5aff1195746d50de43706ba9010da19da639751198226880adc157003948fb  .tmp/input/oldmask_k0.png
f67eb231c29bf2eae0bac73e8eb0e69f4c442192f030d5d40bef5b7c9d6fbe0a  .tmp/input/oldmask_k1.png
b52bbf3a44363a8f5fb56ce8ce02cf25317bb04e757526534adad6f19728fb74  .tmp/input/oldmask_k2.png
e0275345035adae9a7245d70323f7634b96709061ec96d51ceb5b4e9c85a2718  .tmp/input/oldmask_k3.png
f067e8a55ef2b058a56d96bf5b2bc723a803796ebedb0721fac489e59740ce67  .tmp/input/oldmask_k4.png
08aa1296efba87b6b7c4b3b251599479f041e6c8dcd1f20687f0c8e3a14e77fb  .tmp/input/oldmask_k5.png
a73d7c37fe0d99a0f06c503a2e496bd9631b0fd71fa0b572cc31722507be6f91  .tmp/input/oldmask_k6.png
374def1af430af427b5d75fc0108e1ddc2a17d010fc62d5cee61e0ad86a01d25  .tmp/input/oldmask_k7.png
792c024033a553fc10fd7fffe28bd746ada50c8e95abe48ef86cf88e5d8e52ca  .tmp/input/pick_k0.png
35ff737ac4a0759f39ceeb16268c6af19034ff781e3439bab2c39a748cd9dcfe  .tmp/input/pick_k1.png
f5028c2ad286eba3114469f0f54a41c621cb1cfc97d24927e148b97e03b8b965  .tmp/input/pick_k2.png
7f70209ebba8c446cf4999de6e45a3c3843a3a74479595538e1040c6472c7329  .tmp/input/pick_k3.png
98fc45738ba108d0ab732858bcf89932609172b954937e6dc2379023914ec584  .tmp/input/pick_k4.png
b6ea4477ac43cd5c6224fce789cfeebbe91ff916702f1bc558c49ee7e321d6cc  .tmp/input/pick_k5.png
4e09c172cf82758a684c95ddacbffdd2c11373dce4b348e440f3e03cd89180a9  .tmp/input/pick_k6.png
16c79bb87b5681655154372baab05cc14f1de7ea4aecc3924176646f552d71a0  .tmp/input/pick_k7.png
```

## Что сделать

### Часть 1 — Квадроцикл

Восемь случаев `q0`…`q7`. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out/` под именем `quad_k<k>_<попытка>.png`, например `quad_k0_a.png`.

| Случай | Первое изображение | Второе изображение | Промпт | Направление |
|---|---|---|---|---|
| `q0` | `old_k0.png` | `guide_k0.png` | ПК0 | восток |
| `q1` | `old_k1.png` | `guide_k1.png` | ПК1 | северо-восток |
| `q2` | `old_k2.png` | `guide_k2.png` | ПК2 | север |
| `q3` | `old_k3.png` | `guide_k3.png` | ПК3 | северо-запад |
| `q4` | `old_k4.png` | `guide_k4.png` | ПК4 | запад |
| `q5` | `old_k5.png` | `guide_k5.png` | ПК5 | юго-запад |
| `q6` | `old_k6.png` | `guide_k6.png` | ПК6 | юг |
| `q7` | `old_k7.png` | `guide_k7.png` | ПК7 | юго-восток |

ПК0:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК1:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК2:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК3:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК4:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК5:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК6:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

ПК7:

```text
Redraw the vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same buggy from the camera of image 2, turned the same way as the block: the front of the buggy with its two gun barrels points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the buggy itself exactly as in image 1: its design, every part, proportions, materials, colours, red body panels, black roof, wheels and tyres, wear and the painted game-sprite look. Keep the size of the buggy as in image 1 and centre it on the canvas.
Fill everything outside the buggy with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

### Часть 2 — перекраска Девастатора

Восемь случаев `d0`…`d7`. Для случая `d<k>` вызови `image_gen.imagegen` с промптом ПД и двумя входными изображениями: первое — `pick_k<k>.png`, второе — `oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out/` под именем `deva_recolour_k<k>.png`.

ПД:

```text
Edit image 1. Image 1 is a sprite of a heavy tank from a real-time strategy game on a flat magenta background. Image 2 shows the same tank from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the tank that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the tank in image 1 exactly as they are. Do not recolour any other part of the tank or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

### Общее для обеих частей

- Промпты — дословно, без правок и дополнений.
- Файл генерации копируй как есть, размер не меняй. Инструмент кладёт файлы в папку `generated_images` домашней папки Codex; копируй оттуда в `.tmp/out/` сразу после каждой генерации. Исходные файлы в `generated_images` не удаляй.
- **Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.
- **Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
  - на картинке нет машины или машин больше одной;
  - машина обрезана краем картинки;
  - на картинке есть текст, буквы или цифры;
  - на картинке части 1 нарисован брусок или стрелка;
  - фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
  - у картинки части 2 доля зелёного меньше 0,02.
- Неточный пурпурный фон (например, RGB 244, 12, 243) и неточный зелёный — не повод для повтора. Всего генераций, вместе с повторами, — не больше 32.
- Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, промпт, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U2-gen | <время UTC из date -u>`:
- `## PLAN-U2-gen` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 24 итоговых файлов;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → генерации частей 1 и 2 → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все 24 генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев, промпты дословно и правило копирования. Если у субагента нет инструмента `image_gen.imagegen`, генерации делаешь сам по очереди и пишешь это в сдачу.
- Остановки — блок `## Q-U2-gen-NN` и стоп:
  - SHA-256 входов не совпал;
  - `image_gen.imagegen` недоступен или не принимает входные изображения — генерацию без входов не делай;
  - команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка.
