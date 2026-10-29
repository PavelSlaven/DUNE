# Задание U3-gen — генерации группы A под 63°: Трайк, Ракетная установка, Девиатор, Звуковой танк, MCV

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u3`, ветка `codex/u3`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U3.

## Цель

Получить 80 картинок: пять юнитов, перерисованных под камеру 63° в восьми направлениях, по две попытки на направление. Облик и выбор попыток оценивает ведущий, не ты.

## Входы

Папка `.tmp/input/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255). `<юнит>_old_k<k>.png` — старый спрайт юнита из игры, камера 36°; `<юнит>_guide_k<k>.png` — брусок-ориентир под 63°, стрелка на крыше — направление носа. Юниты: `trike`, `launcher`, `deviator`, `sonic`, `mcv`; направления k0…k7: восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U3-gen-01` и стоп.

```text
3f8236b6cd223910d2e905f7702ffeb1607238059a8d5d4577e6cc7120bf4b8c  .tmp/input/deviator_guide_k0.png
c0cd604f4a242fd82dfc95513959803012da6cb88afc144a45221867e7acb86c  .tmp/input/deviator_guide_k1.png
b63d6f70d3018013e729328a2eafab4da72d993382943601e4d64029b3d391ef  .tmp/input/deviator_guide_k2.png
b0d3d86b41b4a5af282abff17007679d4dc65deac48d782f53a7f1984910ad7e  .tmp/input/deviator_guide_k3.png
63821eb32ce71a3d4be77de79893e5956adb70462f09f060fe91c54eb4758036  .tmp/input/deviator_guide_k4.png
5df981de0b96156ec5d81a8b4407d777d8e35d302cfbbc736aba0cb1f946ad3f  .tmp/input/deviator_guide_k5.png
01a482914bfdf9a32a3da0bfe2964fb103220b7faaf07bda4cbdd57ba56b5a34  .tmp/input/deviator_guide_k6.png
6cce782969cfc447768e013aea55c1c55e4d82b1318d072191bffde3624fa9f4  .tmp/input/deviator_guide_k7.png
b48e2b6d9291155a34ef5422e41d706ffaf32b51ac7dbff02b3c436be8e4edac  .tmp/input/deviator_old_k0.png
e97c86001eff7fd0e652ab52a08592accbf7fdbb4b943ce32f5a341f1fcd51dd  .tmp/input/deviator_old_k1.png
9b1f20754a6a99e069f017b8574b63bf6bd21b49ef43e931b7b35cf8534b296e  .tmp/input/deviator_old_k2.png
cb7a23f560bdf2d9f71ce6383579efd878cc5449b7ce33a97bad11fabd1ee7d7  .tmp/input/deviator_old_k3.png
df0fd09c7ad02d3522a9c990890d8cf2ca5905910ceec5244cb7fa07a2f337e1  .tmp/input/deviator_old_k4.png
689d6f027bb729bb947a5aa408b81a129e73dc94bdd733175d97356c84a5be02  .tmp/input/deviator_old_k5.png
5713c5bb2a35864f0a101065c3018e0806140bc5e3af26c0147ead41feb0b442  .tmp/input/deviator_old_k6.png
797393aef330d6e2cb99f234bb794fa66b794951ea77f8195eeee1b388cf32a0  .tmp/input/deviator_old_k7.png
07c5cf589918d4b07823c40192e9aaa36c50cd6d9fcb12de30a1d51d74dd1896  .tmp/input/launcher_guide_k0.png
ebd290c429ec11cf7dee23995ccb4bb4a9ceb9c290756d1e9495d61398981da4  .tmp/input/launcher_guide_k1.png
07db99f82708c3b2d542d6d4c272c6f5ccb3daa55095a7cd059ca9d9c92c8af9  .tmp/input/launcher_guide_k2.png
7ea1bea98c82e2478ba951bf10b210eb7a7cad5791c2fa59e7f3a3f57b42027a  .tmp/input/launcher_guide_k3.png
06f8df7249bf6b5813702ebd743909bb794b94c5d8c794db6f01d8c1c9888d7e  .tmp/input/launcher_guide_k4.png
d19d0b1ba1b9e3fd9ea89c77138eec603e46cc14b8036f1768567493348739d9  .tmp/input/launcher_guide_k5.png
cd5a92ed83041862591b6980ce577a44d9bf1525232cc75a56f72c48857190d6  .tmp/input/launcher_guide_k6.png
4a7aaa096cd618c7bba60364a5a38b86efdb513bb22e7013708f9389894df874  .tmp/input/launcher_guide_k7.png
7b1f740d7e1959595b3ad9977c64e403d767dad168cab279b125171177990f76  .tmp/input/launcher_old_k0.png
05e3959116e3c27595e1368034a63a6fa68ef64950bb613cc99b01754ad045b0  .tmp/input/launcher_old_k1.png
0628ec89db055d49a6d9e184fa50da34e2ffb29b1cb07f89d55d1bd71f122583  .tmp/input/launcher_old_k2.png
1fbbd443b6c39cb09b82b79941776f14332b7c35a245e078a04e744db08cc801  .tmp/input/launcher_old_k3.png
3b41f740974e3103135654dbfd7fe2582e909d53f1118f586760212829b9f487  .tmp/input/launcher_old_k4.png
ce08fa83530c4305acefe9a6df31a1d428df3ace3a1bd0921e3f1e04a184cc34  .tmp/input/launcher_old_k5.png
45b0d4ec79832855e0d886f8e56b4039591d3397507655c0fd73c7e6eef32a9c  .tmp/input/launcher_old_k6.png
29f8d672c77d49951558c87df5711348e7504fca3bb6f3d2a1ee5afe3560be4e  .tmp/input/launcher_old_k7.png
0fba1e4e48347079effa6b0602f7e727bbc20970b602bbbd4ea16cc1af6970e0  .tmp/input/mcv_guide_k0.png
ce4e4001cbfe0ace3d33d697acb093a9fe421acab6b6d3b006102ef4de3c7d3d  .tmp/input/mcv_guide_k1.png
9b8bb4d259b8dd7e76ad8c33befa395c404e74dcb0bee50da02910b126c48e71  .tmp/input/mcv_guide_k2.png
500c69b14fd33777a7426823715dacd639f9bf8b88a6df8743522c4c9f2d62df  .tmp/input/mcv_guide_k3.png
db9daaa5e5dfbe7dbfe026f35b35cdbe5249b1638444f86e0cf25c60dbf46ddc  .tmp/input/mcv_guide_k4.png
4f8429452e2e9c2d936222fb1dc75e8426700583e1620bba5a0e39003c217333  .tmp/input/mcv_guide_k5.png
45118f8a5f06c13f89a763654dcc640641630978d1ac840147bf274125720a70  .tmp/input/mcv_guide_k6.png
ddb980354ef455b0f2476c5a5d186eb28bbacad8d2d8263d793f9a4d01da530d  .tmp/input/mcv_guide_k7.png
e1af5683c1f12ad26502447bff96f2fba35290eccc3df59c5e149ff9ea24cda9  .tmp/input/mcv_old_k0.png
9075c302017c7f39543e5c42917744500e39406b8bcdf75bf04bb0f28005d12f  .tmp/input/mcv_old_k1.png
43697fef2a0fbf360e281a6afc408b524e424f664279d027f6f87e720a61bbf0  .tmp/input/mcv_old_k2.png
1a87fb436b3ccc44d8162add51f991ad2e81abab9422035254d38f73914f3229  .tmp/input/mcv_old_k3.png
671826186f1ff2b6f8de783f75b0bf914e0acd70fc124e968b344aed4b7a600f  .tmp/input/mcv_old_k4.png
4dbc2de6d32c440530e3eae5db15d13b75cc850be7c88fbc67aae753737c85d6  .tmp/input/mcv_old_k5.png
c8af63d65b564e829f3899aa70b355a3ce187f7b5aa656effec44ef5e350e4e0  .tmp/input/mcv_old_k6.png
5f4f42c64dd5378df0039554596400b040b28ca7f915b409380371ef7770d7b3  .tmp/input/mcv_old_k7.png
d0afe15446b4f13ee51a6c0985fd7fae9ae862d62f94823fe36669331a9e2ac2  .tmp/input/sonic_guide_k0.png
cf627aa38d1670834a13316ce5a3018f815b9abbf1da06292cd25e0240387b6d  .tmp/input/sonic_guide_k1.png
be02c6cbe90150bbcc07707075f763e628182317a3fe0c399568ca412518d811  .tmp/input/sonic_guide_k2.png
38b0017a3b87004ad8436f2b06b79de41a1e861cd2478de02429593423144131  .tmp/input/sonic_guide_k3.png
c04b0ae850b38c93643f63e4f2750defb36d037b56f591e9277f14131622a4f4  .tmp/input/sonic_guide_k4.png
3460cbf6e736fa1880b62c493478f66e90da053e00ccb099de7e4e707ceece35  .tmp/input/sonic_guide_k5.png
e64eb072a6615e2a5355ffb888176ee6503f5ec50bdbfc463f3dd42b8dbf29ba  .tmp/input/sonic_guide_k6.png
d86fdef31bda2c06c9cff6286825f76c3127f835f16167ddebf8b1388ea09d34  .tmp/input/sonic_guide_k7.png
dd53042ee21ce65a648ac6d8c7bb0965b68b9909a0af6f1327fbb33f1162a6b6  .tmp/input/sonic_old_k0.png
a06e9b27dd3ae12d98cf5f272f769a8919e8be918fac7d4dcac015c5dd301581  .tmp/input/sonic_old_k1.png
15bcdf83cbfa8c0f27760163163713db141f5bfa422ff1ca34e5c30362ed6f03  .tmp/input/sonic_old_k2.png
41e62932a020ab028f59b4a2086c474183d7397f96e12f26ef1fbef3a4883675  .tmp/input/sonic_old_k3.png
08699fa73beb185277ba31d15dde6d5c7e58e5d52032c21fcea17540ed53fb39  .tmp/input/sonic_old_k4.png
1c7b5b20ae5d904cfcd40f41f19557023f2eab43935da6f59f7510bc99ef41f9  .tmp/input/sonic_old_k5.png
d0234374001536f1e927938756838aafc9ea1d440654ee00d743a766a70a0f5e  .tmp/input/sonic_old_k6.png
d82ebfd3e05d0a266589795047bfb44d5537da0f4cb75a7a48628c2f886adcf8  .tmp/input/sonic_old_k7.png
4e3252e717d397430af43a58e3c74332e8511c73197bc4c226ea68077e8dcbe3  .tmp/input/trike_guide_k0.png
b104085b24fd05197c7829c54ded5b53a470231653b95977d5f92d149c29139d  .tmp/input/trike_guide_k1.png
71d22f99fb4025f85a3fff22d36b084bb7ad4d07ab1eeb093e6b803adfe1a000  .tmp/input/trike_guide_k2.png
19f990aa534232433363c85f9931b9b09261e61e3f598ec54b0a1a8494999b4f  .tmp/input/trike_guide_k3.png
fb1f2d6b3ca9a8d540998998bf291114e4474dc7935fcf1483428cb262852458  .tmp/input/trike_guide_k4.png
efb2ca8132c8a926b777ec16390f418e6d5f30904713d3a87622709188fb12a4  .tmp/input/trike_guide_k5.png
d44fbe2c12f279321a459af4a5fa0ac6e87784480fc7f35638b6f5039d07bec9  .tmp/input/trike_guide_k6.png
d378f7daa4ccbfb583647b4fdbd278a638bfe7c8e82da536130d51e0108febb1  .tmp/input/trike_guide_k7.png
f6838d8447aaa030b1efd0d011891dd139714b210913902f39880f2dc47bab55  .tmp/input/trike_old_k0.png
d1c3d98baa410cd05d4b1f344ffdbb09d7b4caa4f247cfaef964897233c71627  .tmp/input/trike_old_k1.png
91ec39d2b44e460e0d5553232c343c8522194c49b37831217edd7f1c7d19cd63  .tmp/input/trike_old_k2.png
a915cee962868aa69c09985cb18bd66ce18eb9fa469b92a322d914ea037189f8  .tmp/input/trike_old_k3.png
a37516aad556102e2222d989500f66a8490b055dcdce27c475e2ba2de03b45ce  .tmp/input/trike_old_k4.png
36366ea30556f82633dc4e6e574e5e025b66bfeabda9b392434477cb6f955220  .tmp/input/trike_old_k5.png
28965afa6f295105b2f508efab28bd021b1fe800951540503f73d4a3085a82bd  .tmp/input/trike_old_k6.png
7aec2a9c0342f900d0c24d35f0dfb76f85979325331be77e523ac6676332d218  .tmp/input/trike_old_k7.png
```

## Что сделать

40 случаев — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out/` под именем `<случай>_<попытка>.png`, например `trike_k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт | Юнит и направление |
|---|---|---|---|---|
| `trike_k0` | `trike_old_k0.png` | `trike_guide_k0.png` | П-trike-0 | Трайк, восток |
| `trike_k1` | `trike_old_k1.png` | `trike_guide_k1.png` | П-trike-1 | Трайк, северо-восток |
| `trike_k2` | `trike_old_k2.png` | `trike_guide_k2.png` | П-trike-2 | Трайк, север |
| `trike_k3` | `trike_old_k3.png` | `trike_guide_k3.png` | П-trike-3 | Трайк, северо-запад |
| `trike_k4` | `trike_old_k4.png` | `trike_guide_k4.png` | П-trike-4 | Трайк, запад |
| `trike_k5` | `trike_old_k5.png` | `trike_guide_k5.png` | П-trike-5 | Трайк, юго-запад |
| `trike_k6` | `trike_old_k6.png` | `trike_guide_k6.png` | П-trike-6 | Трайк, юг |
| `trike_k7` | `trike_old_k7.png` | `trike_guide_k7.png` | П-trike-7 | Трайк, юго-восток |
| `launcher_k0` | `launcher_old_k0.png` | `launcher_guide_k0.png` | П-launcher-0 | Ракетная установка, восток |
| `launcher_k1` | `launcher_old_k1.png` | `launcher_guide_k1.png` | П-launcher-1 | Ракетная установка, северо-восток |
| `launcher_k2` | `launcher_old_k2.png` | `launcher_guide_k2.png` | П-launcher-2 | Ракетная установка, север |
| `launcher_k3` | `launcher_old_k3.png` | `launcher_guide_k3.png` | П-launcher-3 | Ракетная установка, северо-запад |
| `launcher_k4` | `launcher_old_k4.png` | `launcher_guide_k4.png` | П-launcher-4 | Ракетная установка, запад |
| `launcher_k5` | `launcher_old_k5.png` | `launcher_guide_k5.png` | П-launcher-5 | Ракетная установка, юго-запад |
| `launcher_k6` | `launcher_old_k6.png` | `launcher_guide_k6.png` | П-launcher-6 | Ракетная установка, юг |
| `launcher_k7` | `launcher_old_k7.png` | `launcher_guide_k7.png` | П-launcher-7 | Ракетная установка, юго-восток |
| `deviator_k0` | `deviator_old_k0.png` | `deviator_guide_k0.png` | П-deviator-0 | Девиатор, восток |
| `deviator_k1` | `deviator_old_k1.png` | `deviator_guide_k1.png` | П-deviator-1 | Девиатор, северо-восток |
| `deviator_k2` | `deviator_old_k2.png` | `deviator_guide_k2.png` | П-deviator-2 | Девиатор, север |
| `deviator_k3` | `deviator_old_k3.png` | `deviator_guide_k3.png` | П-deviator-3 | Девиатор, северо-запад |
| `deviator_k4` | `deviator_old_k4.png` | `deviator_guide_k4.png` | П-deviator-4 | Девиатор, запад |
| `deviator_k5` | `deviator_old_k5.png` | `deviator_guide_k5.png` | П-deviator-5 | Девиатор, юго-запад |
| `deviator_k6` | `deviator_old_k6.png` | `deviator_guide_k6.png` | П-deviator-6 | Девиатор, юг |
| `deviator_k7` | `deviator_old_k7.png` | `deviator_guide_k7.png` | П-deviator-7 | Девиатор, юго-восток |
| `sonic_k0` | `sonic_old_k0.png` | `sonic_guide_k0.png` | П-sonic-0 | Звуковой танк, восток |
| `sonic_k1` | `sonic_old_k1.png` | `sonic_guide_k1.png` | П-sonic-1 | Звуковой танк, северо-восток |
| `sonic_k2` | `sonic_old_k2.png` | `sonic_guide_k2.png` | П-sonic-2 | Звуковой танк, север |
| `sonic_k3` | `sonic_old_k3.png` | `sonic_guide_k3.png` | П-sonic-3 | Звуковой танк, северо-запад |
| `sonic_k4` | `sonic_old_k4.png` | `sonic_guide_k4.png` | П-sonic-4 | Звуковой танк, запад |
| `sonic_k5` | `sonic_old_k5.png` | `sonic_guide_k5.png` | П-sonic-5 | Звуковой танк, юго-запад |
| `sonic_k6` | `sonic_old_k6.png` | `sonic_guide_k6.png` | П-sonic-6 | Звуковой танк, юг |
| `sonic_k7` | `sonic_old_k7.png` | `sonic_guide_k7.png` | П-sonic-7 | Звуковой танк, юго-восток |
| `mcv_k0` | `mcv_old_k0.png` | `mcv_guide_k0.png` | П-mcv-0 | MCV, восток |
| `mcv_k1` | `mcv_old_k1.png` | `mcv_guide_k1.png` | П-mcv-1 | MCV, северо-восток |
| `mcv_k2` | `mcv_old_k2.png` | `mcv_guide_k2.png` | П-mcv-2 | MCV, север |
| `mcv_k3` | `mcv_old_k3.png` | `mcv_guide_k3.png` | П-mcv-3 | MCV, северо-запад |
| `mcv_k4` | `mcv_old_k4.png` | `mcv_guide_k4.png` | П-mcv-4 | MCV, запад |
| `mcv_k5` | `mcv_old_k5.png` | `mcv_guide_k5.png` | П-mcv-5 | MCV, юго-запад |
| `mcv_k6` | `mcv_old_k6.png` | `mcv_guide_k6.png` | П-mcv-6 | MCV, юг |
| `mcv_k7` | `mcv_old_k7.png` | `mcv_guide_k7.png` | П-mcv-7 | MCV, юго-восток |

Промпты — дословно, без правок и дополнений.

П-trike-0:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-1:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-2:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-3:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-4:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-5:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-6:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-trike-7:

```text
Redraw the trike from image 1 as seen from a higher camera.
Image 1 is a sprite of a fast three-wheeled armoured trike with one front wheel, two large rear wheels and a small gun on top from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same trike from the camera of image 2, turned the same way as the block: the front of the trike with its single front wheel points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the trike itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark steel-blue armour, glowing cyan lights, black tyres, wear and the painted game-sprite look. Keep the size of the trike as in image 1 and centre it on the canvas.
Fill everything outside the trike with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-0:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-1:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-2:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-3:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-4:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-5:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-6:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-launcher-7:

```text
Redraw the missile launcher from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked missile launcher vehicle with a raised rack of long missiles on its back from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same missile launcher from the camera of image 2, turned the same way as the block: the front of the missile launcher with the missile tips points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the missile launcher itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, sand-coloured camouflage armour, missiles, tracks, wear and the painted game-sprite look. Keep the size of the missile launcher as in image 1 and centre it on the canvas.
Fill everything outside the missile launcher with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-0:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-1:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-2:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-3:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-4:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-5:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-6:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-deviator-7:

```text
Redraw the launcher tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked launcher tank with a large twin box launcher on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same launcher tank from the camera of image 2, turned the same way as the block: the front of the launcher tank points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the launcher tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, dark blue armour, yellow and pink lights, white stripes, tracks, wear and the painted game-sprite look. Keep the size of the launcher tank as in image 1 and centre it on the canvas.
Fill everything outside the launcher tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-0:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-1:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-2:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-3:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-4:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-5:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-6:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-sonic-7:

```text
Redraw the sonic tank from image 1 as seen from a higher camera.
Image 1 is a sprite of a tracked tank with a large golden sound-wave emitter dish on its turret from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same sonic tank from the camera of image 2, turned the same way as the block: the front of the sonic tank with the emitter dish points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the sonic tank itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, green and cream camouflage armour, golden dish, tracks, wear and the painted game-sprite look. Keep the size of the sonic tank as in image 1 and centre it on the canvas.
Fill everything outside the sonic tank with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-0:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-1:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, up and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-2:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, straight up, away from the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-3:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, up and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-4:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-5:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, down and to the left. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-6:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, straight down, towards the viewer. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

П-mcv-7:

```text
Redraw the construction vehicle from image 1 as seen from a higher camera.
Image 1 is a sprite of a large eight-wheeled mobile construction vehicle with a folded crane arm on its roof from a real-time strategy game, seen from a low camera about 36 degrees above the horizon. Image 2 is a camera guide: a plain grey block seen from the target camera, orthographic, 63 degrees above the horizon; the dark arrow on its roof points to the front.
Show the same construction vehicle from the camera of image 2, turned the same way as the block: the front of the construction vehicle points where the arrow points, down and to the right. Use image 2 only for the camera angle and the facing direction, not for the shape, size or colours. Keep the construction vehicle itself exactly as in image 1: its design, every part and its position on the hull, proportions, materials, colours, grey and dark armour, red trim, wheels, wear and the painted game-sprite look. Keep the size of the construction vehicle as in image 1 and centre it on the canvas.
Fill everything outside the construction vehicle with flat pure magenta RGB 255,0,255. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks. Do not draw the block or the arrow.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- на картинке нарисован брусок или стрелка;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.

Неточный пурпурный фон — не повод для повтора. Всего генераций, вместе с повторами, — не больше 100.

Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U3-gen | <время UTC из date -u>`:
- `## PLAN-U3-gen` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 80 итоговых файлов;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 80 генераций → повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев (например, один юнит), промпты дословно и правило копирования.
- Остановки — блок `## Q-U3-gen-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress.md`, строка после каждого шага порядка и после каждого готового юнита.
