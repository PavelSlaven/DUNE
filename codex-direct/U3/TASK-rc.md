# Задание U3-rc — перекраска группы A по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u3`, ветка `codex/u3`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U3.

## Цель

Получить 40 перекрасок пяти новых юнитов под 63° (`trike`, `launcher`, `deviator`, `sonic`, `mcv`, направления k0…k7), где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `<юнит>_pick_k0.png` … `<юнит>_pick_k7.png` | новый юнит под 63°, направления k0…k7 |
| `<юнит>_oldmask_k0.png` … `<юнит>_oldmask_k7.png` | старый юнит, камера 36°: части цвета Дома залиты чистым зелёным |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U3-rc-01` и стоп.

```text
83afcec33b956156b32df4e098775cd5827631dafc7b1b7c1d3a62117affcbc5  .tmp/input-rc/deviator_oldmask_k0.png
6ff269631119e95bdf1c44b2edb7d484952500f56039ef1dd24fe8569bd3d647  .tmp/input-rc/deviator_oldmask_k1.png
edda2d0938d73ba00ec44d2dbcd39e7ad6a13ad43d437971be5abbc007000aec  .tmp/input-rc/deviator_oldmask_k2.png
81da383038e97d56c7947a00e21a5f62cfdce6f27c5e8b5affce95aad374d5c0  .tmp/input-rc/deviator_oldmask_k3.png
afe1108e895e65c269b491d14c6c20babb71d6ed9b734e51dab49e3faf61d380  .tmp/input-rc/deviator_oldmask_k4.png
13c47fc8a7303f6b7b4b04dab1636689f6d17b2952a45d48b6e95b6d4adff7f5  .tmp/input-rc/deviator_oldmask_k5.png
53de87fdd45c954a84aef7cb44a6f8ba3699c6ad3c85f20449d93b5739f820af  .tmp/input-rc/deviator_oldmask_k6.png
3a283a9cfab36140aa3172d2f89550de9f6ac3993f3d2c81c01858e87092f50e  .tmp/input-rc/deviator_oldmask_k7.png
979726bf0e5267c59950a88ebd11989fbe13c2b506a1ccb414a6fab61dc671e4  .tmp/input-rc/deviator_pick_k0.png
4924ba0bf45a4ecd1e399050f8b272909cec12bf95b37b3e05b07da11da54fb7  .tmp/input-rc/deviator_pick_k1.png
d1517a51c3630363565931cec9a3af2cf358ad6d7b785e9bde5345036c2ea181  .tmp/input-rc/deviator_pick_k2.png
0dd67753c3b7d603dbe14f4e1c5c347b888c90a145dbcb79d37c97459bc4a311  .tmp/input-rc/deviator_pick_k3.png
3a6f7863bbf7f313a7edc06ec7acf45c99a558de85c8cd40128e353d9d32277d  .tmp/input-rc/deviator_pick_k4.png
55da10be12cb28870c75a7be12fdb1e8fb28b460df83331b4d6d06444e36aba7  .tmp/input-rc/deviator_pick_k5.png
1d34883e67799bf01b04cd4b27fa7e89d31bb67119fdc1a07f5278d0f0216d17  .tmp/input-rc/deviator_pick_k6.png
9d53b52f42fd55387e845283aaeaa8b6250b386ea5a6936ff2b8785f9876b533  .tmp/input-rc/deviator_pick_k7.png
dff62a8437d090a7db10743e7eb67aa805754f5c543da9fdfbc82a4fb53e8171  .tmp/input-rc/launcher_oldmask_k0.png
6699873d222ec2cc68638fe25a0e3d6e456be951bc07eebe6f5660feb4df908e  .tmp/input-rc/launcher_oldmask_k1.png
b610e2dbaa48653c1375807a75c81f39ac445ca9fd73fee7c9adbe6b69d598dc  .tmp/input-rc/launcher_oldmask_k2.png
c71972685275dd732c66f0080d4e1ca360b5d013337c626342c92872558f838e  .tmp/input-rc/launcher_oldmask_k3.png
fe50e886e5f0e9eb90fdb67ac3b3fc84846d0e1745e9558893a8dceea01a7dac  .tmp/input-rc/launcher_oldmask_k4.png
bd46a8f5b91189c15cc77d0c0a1619a78a73a0f832fe7068a67e02bf0a14f8df  .tmp/input-rc/launcher_oldmask_k5.png
8ce88e328084a4459910ee5017601fb4e73509384a7cfdd613bbe0e456f56286  .tmp/input-rc/launcher_oldmask_k6.png
dea490628a95ba43393ca04396a8af5059c5f7416a1d0e0d4f7241069f177f75  .tmp/input-rc/launcher_oldmask_k7.png
b44579c09fcb8420f31efe28adbdcdf873f27692665401088cdb4cf3f45e3891  .tmp/input-rc/launcher_pick_k0.png
c1264b72292d2290bb63f7204b0b0b54273fd66a27c64a1ffd296fd334ca47b4  .tmp/input-rc/launcher_pick_k1.png
d705b05acb929924585c324c7aaaee7956555836e27a3f58d22edbf2eb8798f6  .tmp/input-rc/launcher_pick_k2.png
c2b315e261321f888419e1796dcf55886962ddb232dfc97ad7684928f9994141  .tmp/input-rc/launcher_pick_k3.png
cf5a635d7e5a3b3d93aa823aa9e818b562d60245f176e8fc0bebdda709193469  .tmp/input-rc/launcher_pick_k4.png
270a986f8348c0d3a507b6ef6a9ba3a41b65ae1c1230f519d32fca30e5a27aa5  .tmp/input-rc/launcher_pick_k5.png
8c806973a6e2730d575f1583909d283803163ca21d28e9a1a3ba27923d2cd710  .tmp/input-rc/launcher_pick_k6.png
4cadfdc37e064693b6cfa97eb30bf33ddd2b566151ec09669e022d18b71c2ab3  .tmp/input-rc/launcher_pick_k7.png
716fc799c038b43735a7a42a9e6e0321ab78cf00a859478d0c9d7d8c8d01b2a2  .tmp/input-rc/mcv_oldmask_k0.png
ebfff69521020ace6d24e7140194c9c98a62129fe24024c4caf4efc2a95d69d5  .tmp/input-rc/mcv_oldmask_k1.png
946f642c29bf301693cd3752edfbf59835deba264ed73209ad38a3c58df1db8a  .tmp/input-rc/mcv_oldmask_k2.png
b7e1a96ba5897eda9fda4ef658e9237da6fd8582e2511a0c213c4b9ab72c5b7e  .tmp/input-rc/mcv_oldmask_k3.png
cd94e9f8374c04e469c184dc53bed8447600f426a7129b266701f733aa2f1551  .tmp/input-rc/mcv_oldmask_k4.png
84d6a4f8ceed2ed3cc4334994e1874aeec8877ca589d13fd33666d6336da9865  .tmp/input-rc/mcv_oldmask_k5.png
fdc715d86298011b72af7b211a9c470d51960b381379579e15c2b17439efdcdc  .tmp/input-rc/mcv_oldmask_k6.png
22ba3e04d09aa9aa0988acf3a0f10a82e83b02f22c702cf71a6fa8af0993359b  .tmp/input-rc/mcv_oldmask_k7.png
601a0a890710894429d34d5b7abbe1e95a4f9234877cb28a5876deccf7b38f43  .tmp/input-rc/mcv_pick_k0.png
c3b911be32e77760ea34fa980e4f360f1484fc3bf0f06ab2b90d65b40fb00f33  .tmp/input-rc/mcv_pick_k1.png
ee90c04a4caa5f96d973f39f4de6b3f47553ae027e5ff4cf21ca6cd82ee66754  .tmp/input-rc/mcv_pick_k2.png
4bc5f79ec18b4bdc96208ecb0f1656a8f353639a2daea90a6470e42905c8a7fc  .tmp/input-rc/mcv_pick_k3.png
84a92fc8b3b04dfbcdcc3a2854452b328ca656903dcaec95b707c73ffea88b4b  .tmp/input-rc/mcv_pick_k4.png
9898f957117ef5abaee27cc8fe05b4180c3553b0576cad881df874fce4961604  .tmp/input-rc/mcv_pick_k5.png
4afc91ab23aa3f9d5350d1b4ce5515acd4a940cf929e37f4901c44c0af413247  .tmp/input-rc/mcv_pick_k6.png
15b4e0f497ce0c25ed8d1f3d677c2b290ec22d1b83614437c052c9d25dc5d815  .tmp/input-rc/mcv_pick_k7.png
aaf38b952e1ed3a06b44a0f429828f13b632bed68605422e42c10c5b12233c1d  .tmp/input-rc/sonic_oldmask_k0.png
75006b8d9ed19736c60039fccae92cda02c7ff4d2645d542ec928cc5c1a8cffc  .tmp/input-rc/sonic_oldmask_k1.png
e22e380a5860d930b6e184150a3a80b8a8447629b2f77d59fbf7238cc8b237a9  .tmp/input-rc/sonic_oldmask_k2.png
13669869d9e138b2e9d808af970d445a29af4832ef2ed58ab0624c27fa62c431  .tmp/input-rc/sonic_oldmask_k3.png
0a9075c0c6bdc6f454375b72705bdc4345ee4f9bef08059401dca99631ab251f  .tmp/input-rc/sonic_oldmask_k4.png
9ec6bfc4edf7b1c700b02f788e4fbab8aeae0865bf44198d9abf7b0c209043a6  .tmp/input-rc/sonic_oldmask_k5.png
565fc0030a7c0099c572405a08f8ad24d8dee4c45ad110aa43d61f415a1e305b  .tmp/input-rc/sonic_oldmask_k6.png
5fee9935a165c6e2f1faa12445c985da3c9710ff9a0e86045db01044854d2039  .tmp/input-rc/sonic_oldmask_k7.png
bd937bd12a9da905fb63b5d7badfc7c23e73f08d1249122529431a90a07c9fc6  .tmp/input-rc/sonic_pick_k0.png
42699643289d0b62705981f25e08a1e23bb7fe9af674efc43cb6e011d915e3d5  .tmp/input-rc/sonic_pick_k1.png
d4fae98c802f136ce9d86cbfd676025d7b799a5a1089dd62d3147af5456c5a4f  .tmp/input-rc/sonic_pick_k2.png
5b82512e2041f13a19c1174a6fd7a5a378b92d59fa61b6d7f8dc3581e9dae281  .tmp/input-rc/sonic_pick_k3.png
3a6192dd9e08e49364a69e20d522a67e8be0806f633e5be349fad8cf61272a88  .tmp/input-rc/sonic_pick_k4.png
f9f5dc5cc52ccd8a6a12b097bed487822ca3edd1f9c93fc2ac7daf5151d40856  .tmp/input-rc/sonic_pick_k5.png
1660154655bf7e5f2f20b750b628bafad1cd8b69d4e44c0239167fd2025f7088  .tmp/input-rc/sonic_pick_k6.png
650fa2fc32766fad9746b81b0e8b36cb1bdfbad576ec9d8ae18712db45c6b4ec  .tmp/input-rc/sonic_pick_k7.png
310a973499db274866e1c0ec2bcca4ed438e97427eb7993ba5b9b1b89eb7a76c  .tmp/input-rc/trike_oldmask_k0.png
c3863c146777556488777b1d72623d28850da16541ea50ba00fbac17b7959e47  .tmp/input-rc/trike_oldmask_k1.png
973fa077fa16c687562c6d2799b3ac22d585f0a65d853a924d5f22c9d774e95c  .tmp/input-rc/trike_oldmask_k2.png
1ba69b1190b118a35fe02d6e887d59b86fc880822a5a86d231a441ea50b0b33c  .tmp/input-rc/trike_oldmask_k3.png
9063977c8dfc4c82b3f3cca56c4111e37413e5bbec741bb1debe4290dbf993e7  .tmp/input-rc/trike_oldmask_k4.png
f393efd2af1b4fd44c5aa91dc076c129394aa9d93781eb3243f79b63295d0290  .tmp/input-rc/trike_oldmask_k5.png
02211330ecb71d66529a92ead8c0a805fcd82c723b02728800c88a8591bce5d0  .tmp/input-rc/trike_oldmask_k6.png
cd5aa3faaaf01a2d98637ffd19e328c48ae0e54d2e7d026bb32c486eea429ae8  .tmp/input-rc/trike_oldmask_k7.png
d69b7bf73d7b83769d1761837a0ed3236725624595941a4d0fb1676a9f43f60f  .tmp/input-rc/trike_pick_k0.png
75425563b8451cee6f68b7e909f10e4b53c459fbd3da39fb832cbc2786aac5a7  .tmp/input-rc/trike_pick_k1.png
cfdbfb66e4e0b1817f5ffaf7d254dbce1397e92ed4cea6691c5f4454386ed04d  .tmp/input-rc/trike_pick_k2.png
f4525ab1d2fb7696475718267a9b5c132cf1e02f957d72ff14d54fcf81c5d526  .tmp/input-rc/trike_pick_k3.png
b398ef9542bbc5ff7ed46d4fdb42cc20e334f7da0b7afdd3d67481f26b8f33c4  .tmp/input-rc/trike_pick_k4.png
825d0e749de033261acaaa53fab55758b7e4ecf7bdecc0142d7da6c225bdcf08  .tmp/input-rc/trike_pick_k5.png
69f097ca23ff31f4683b5bbe372608f279500e270258c072f66065b96bab01bf  .tmp/input-rc/trike_pick_k6.png
cc843244cc814f912d1fe8d929b05c442595c2d4f78d805ab5bfc0d729dbf9cd  .tmp/input-rc/trike_pick_k7.png
```

## Что сделать

40 случаев `<юнит>_c<k>`. Для случая `<юнит>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<юнит>` и двумя входными изображениями: первое — `<юнит>_pick_k<k>.png`, второе — `<юнит>_oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out-rc/` под именем `<юнит>_recolour_k<k>.png` сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-trike** (юнит `trike`):

```text
Edit image 1. Image 1 is a sprite of a light three-wheeled armoured trike with one front wheel and two large rear wheels from a real-time strategy game on a flat magenta background. Image 2 shows the same trike from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the trike that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the trike in image 1 exactly as they are. Do not recolour any other part of the trike or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-launcher** (юнит `launcher`):

```text
Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of long tubes on its back from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour any other part of the vehicle or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-deviator** (юнит `deviator`):

```text
Edit image 1. Image 1 is a sprite of a tracked tank with a large twin box on its turret from a real-time strategy game on a flat magenta background. Image 2 shows the same tank from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the tank that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the tank in image 1 exactly as they are. Do not recolour any other part of the tank or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-sonic** (юнит `sonic`):

```text
Edit image 1. Image 1 is a sprite of a tracked tank with a large golden dish on its turret from a real-time strategy game on a flat magenta background. Image 2 shows the same tank from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the tank that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the tank in image 1 exactly as they are. Do not recolour any other part of the tank or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-mcv** (юнит `mcv`):

```text
Edit image 1. Image 1 is a sprite of a large eight-wheeled construction vehicle with a folded crane arm on its roof from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour any other part of the vehicle or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет первую попытку: первая переносится в `.tmp/out-rc-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 56. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U3-rc | <время UTC из date -u>`:
- `## PLAN-U3-rc` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 40 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации по 3 одновременно, пока случаи не кончатся; каждому — свой юнит, промпт дословно и правило копирования.
- Остановки — блок `## Q-U3-rc-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc.md`, строка после каждого шага порядка и после каждого готового юнита.
