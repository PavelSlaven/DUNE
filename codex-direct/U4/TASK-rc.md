# Задание U4-rc — перекраска корпуса и башни Танка по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u4`, ветка `codex/u4`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U4.

## Цель

Получить 16 перекрасок Танка под 63° — корпуса (`tankbase`) и башни (`tanktop`), направления k0…k7, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `<часть>_pick_k0.png` … `<часть>_pick_k7.png` | новая часть Танка под 63°, направления k0…k7 |
| `<часть>_oldmask_k0.png` … `<часть>_oldmask_k7.png` | старая часть Танка, камера 36°: части цвета Дома залиты чистым зелёным |

Части: `tankbase` — корпус без башни, `tanktop` — башня без корпуса.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U4-rc-01` и стоп.

```text
8ba45d36e380fb1a594cd03dec21000acacac94566d8d75aa0c76f85fc6e81a4  .tmp/input-rc/tankbase_oldmask_k0.png
c103561c106bf23583c9d74239f37ce4e56fd87ec58329f88b0edd57bb94eab1  .tmp/input-rc/tankbase_oldmask_k1.png
5ee4fe069d112ba26033668092625ebbb90f937dd26c3c6d72aa434dd7ee4981  .tmp/input-rc/tankbase_oldmask_k2.png
84e47b8dc00323bc84aeca7c18967b307b7aa7a6455f06b31a702cd7eaaa9229  .tmp/input-rc/tankbase_oldmask_k3.png
55367c77200a1c0afdce1834d7cb8ea752d3f383d57b6d35e784dac284c7307f  .tmp/input-rc/tankbase_oldmask_k4.png
8d3acfc99bfca73c08cbb8191b6021cb0576e7c7c07b50dbd6b4e484b1181008  .tmp/input-rc/tankbase_oldmask_k5.png
fe4b9d63dbc1cd96e500ae06ffdced2adca99a9e51aa983ffd81e72e71601b26  .tmp/input-rc/tankbase_oldmask_k6.png
825006f12ab3ec95f8bbb77fe181aee2387664010ed38c30592fddb87f53aaa4  .tmp/input-rc/tankbase_oldmask_k7.png
3df6addb711d9f29bbf1a2be3c70d60f60ed37ad7f1bce1ce834f54eba37036c  .tmp/input-rc/tankbase_pick_k0.png
b58d1bfdafad997b09b1db92d8598c933b7bfcb2023f9986f5f62f7f3dfcaf16  .tmp/input-rc/tankbase_pick_k1.png
8d1ec7a027858b723e7347891e45597086cd1a271015711234c2f3d465f3cb7c  .tmp/input-rc/tankbase_pick_k2.png
11abc0da4e1e960ef69f308d13151afc6cfd6e5b11be279b3d953fdb1127ad7e  .tmp/input-rc/tankbase_pick_k3.png
07787c9dcfa8893d7a45e598fac564cd66fca73c99817144b8d8aed746d05661  .tmp/input-rc/tankbase_pick_k4.png
444dcf0552ae62cfec2ce8bf54e758fdcc39b270a93f9e5c75ccc321d528395f  .tmp/input-rc/tankbase_pick_k5.png
d11790ee9520d86bf8749f4ee804188f8ff6d1cd3a727421353b8b5d297e9df5  .tmp/input-rc/tankbase_pick_k6.png
e31817da633e9b990c43f5265d9950e799b57f7455f461d90588991e1b161d51  .tmp/input-rc/tankbase_pick_k7.png
ce3405f6b7aef4b1489bda0d67269e3007061b3fd901b04b361e49cbcb67cf0f  .tmp/input-rc/tanktop_oldmask_k0.png
e52c344bc334c7740ed228ad0336698087b69cfae070863e2958306310ade8c2  .tmp/input-rc/tanktop_oldmask_k1.png
404f884de712a46cf6c8862c4862e72af54aeffab6ce0217733407ebdf4b44fd  .tmp/input-rc/tanktop_oldmask_k2.png
ea357f7e36fcea44bfdc9bc777462b2251bb972c486b9f96bea61395bdf68c14  .tmp/input-rc/tanktop_oldmask_k3.png
d42416e8a860276d73af26d213027c202cbebf5795fcdf6131729b7f7c75802d  .tmp/input-rc/tanktop_oldmask_k4.png
c97dfaac01fa298a364359740237f63803d14e08e64d0b46cb2bad521525fa06  .tmp/input-rc/tanktop_oldmask_k5.png
ef911f76049c601ae32a1fa25801cf3080f0a99412864f5020cbeeea8b642079  .tmp/input-rc/tanktop_oldmask_k6.png
85b82604b940052cb40b2d502207710e7da68b8b883ec9059b66b4aaedd8fca6  .tmp/input-rc/tanktop_oldmask_k7.png
eef8eda5a3b4fb85d42f24a0ced2606214396b42319d9d5618bf2e3f47d71348  .tmp/input-rc/tanktop_pick_k0.png
8704d2cf77ab49de6a36202d393820e070ab929b77730f36dcedfaf608f3d91b  .tmp/input-rc/tanktop_pick_k1.png
21edc5203db61345f9f66273d0103ec0e7e9f69c83da3837a96dca5f083649bf  .tmp/input-rc/tanktop_pick_k2.png
bf927bf4bdc7ea1397d269cfce2afd7f7c8f518e89d9648fb181e0159e2f142b  .tmp/input-rc/tanktop_pick_k3.png
4c976d923d18af8f5918acd51722c0a8786a977a1ef100b77e23fa6ef29d984b  .tmp/input-rc/tanktop_pick_k4.png
80411fde714309bc9c9e904a229b27fd8f4d3a52528890f748cd0a96c5b543a6  .tmp/input-rc/tanktop_pick_k5.png
9d321e41940dbf5c46cbc9119b76c00ddeb3d16f1320c36b82333d9eb1f37bff  .tmp/input-rc/tanktop_pick_k6.png
7e2faea23ebff7993fc9a43dbf1c65bb00c37cdbda590282e22bff4ec3bbdb74  .tmp/input-rc/tanktop_pick_k7.png
```

## Что сделать

16 случаев `<часть>_c<k>`. Для случая `<часть>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<часть>` и двумя входными изображениями: первое — `<часть>_pick_k<k>.png`, второе — `<часть>_oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out-rc/` под именем `<часть>_recolour_k<k>.png` сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-tankbase** (часть `tankbase`):

```text
Edit image 1. Image 1 is a sprite of a tracked vehicle body without its top module: on top of the body there is an empty round ring from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle body from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle body that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the vehicle body in image 1 exactly as they are. Do not recolour any other part of the vehicle body or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**ПК-tanktop** (часть `tanktop`):

```text
Edit image 1. Image 1 is a sprite of a separate round top module with one long tube, drawn alone from a real-time strategy game on a flat magenta background. Image 2 shows the same module from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the module that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the module in image 1 exactly as they are. Do not recolour any other part of the module or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет корпуса (для `tankbase`) или башни (для `tanktop`), или их больше одного;
- часть обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет первую попытку: первая переносится в `.tmp/out-rc-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 24. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U4-rc | <время UTC из date -u>`:
- `## PLAN-U4-rc` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 16 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации по 4 одновременно, пока случаи не кончатся; каждому — одна часть и четыре направления, промпт дословно и правило копирования.
- Остановки — блок `## Q-U4-rc-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc.md`, строка после каждого шага порядка и после каждой готовой части.
