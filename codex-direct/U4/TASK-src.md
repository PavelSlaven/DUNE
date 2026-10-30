# Задание U4-src — перекраска корпуса и башни Осадного по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u4s`, ветка `codex/u4s`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U4.

## Цель

Получить 16 перекрасок Осадного под 63° — корпуса (`siegebase`) и башни (`siegetop`), направления k0…k7, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `<часть>_pick_k0.png` … `<часть>_pick_k7.png` | новая часть Осадного под 63°, направления k0…k7 |
| `<часть>_oldmask_k0.png` … `<часть>_oldmask_k7.png` | старая часть Осадного, камера 36°: части цвета Дома залиты чистым зелёным |

Части: `siegebase` — корпус без башни, `siegetop` — башня без корпуса.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U4-src-01` и стоп.

```text
edf0e209484226147a4bb770ad29eec1b506deb75b9d87d3027ca92ae1df49d6  .tmp/input-rc/siegebase_oldmask_k0.png
e20de553f7761fd1bd87208bfeedee08b7a2385a2c44486a46e9b01818bf4752  .tmp/input-rc/siegebase_oldmask_k1.png
844241936cdd43a1a0568f8dbd7ba0aeead59661111229b9f7c2fd5eb9895569  .tmp/input-rc/siegebase_oldmask_k2.png
73a095b3313d9848ca0c8b31656d34bc1e596abae74968a58750d8e774daf3ef  .tmp/input-rc/siegebase_oldmask_k3.png
184db7cf416c74194aee8934d060f0248e7e6cebbbdd6a248f441b74b8c44852  .tmp/input-rc/siegebase_oldmask_k4.png
a853c8a5683db85d43a53f31bfd9eb6ee2a157aa007b0c63e57ec59795d42c97  .tmp/input-rc/siegebase_oldmask_k5.png
9bead70310e3650a0146a89d5d7b28e1d31d460c819b4c9ace492b5b68fe0a62  .tmp/input-rc/siegebase_oldmask_k6.png
511d2c2f4bf2f60353b8633f584db4e46fb3080501a2acb1f72469221c133de3  .tmp/input-rc/siegebase_oldmask_k7.png
ce741c36f6c81465fb8f5a3af17f22767d4471033c416e716318e0af6829d778  .tmp/input-rc/siegebase_pick_k0.png
90dc35aea8a0d7aa5aced97d1cb442f137f4afda19dec3604a6634462348ae63  .tmp/input-rc/siegebase_pick_k1.png
5920e137f70580d71e70cdc03c2020454443f893d71aa5928ee824f3c8936a9d  .tmp/input-rc/siegebase_pick_k2.png
da58e3ded2208552a248e0999d8b2a02084b09a3d46bb89d3bd6f01d8885b4fe  .tmp/input-rc/siegebase_pick_k3.png
2fae7c5db7f1fff43f4535c3cf50f6dcb60f50c33f3f46db2cfd559f8fc1ec50  .tmp/input-rc/siegebase_pick_k4.png
a3a2997c29cd7955557139b34e12ed3e9233c6a5c51f9b09a15e6891f0c6e7fe  .tmp/input-rc/siegebase_pick_k5.png
c6ba18d10f0715604e9e609ab2eea390709a845208d408667e67657c68524cd3  .tmp/input-rc/siegebase_pick_k6.png
03c1b4701d98974ddd293207ab855846ac396f7f7bdfa1ae8b391ee6d13dc517  .tmp/input-rc/siegebase_pick_k7.png
f1ec549df988517b194ebba329cedfd7228dc19d1d334bb36868f6ed0eff8310  .tmp/input-rc/siegetop_oldmask_k0.png
2b16fdf62c2e4c2360bc25c2433d70beaca3abfbe4d4ed839b3b3a9c77be4504  .tmp/input-rc/siegetop_oldmask_k1.png
1244b4dc066b7838d9bb00762b3c557b1acc7de7fc047e0ef0d6f697bab5c569  .tmp/input-rc/siegetop_oldmask_k2.png
b504ee9f77f3ce2d9637ac1ff9277f24256355ad987e2cfc558d548cdd463ef6  .tmp/input-rc/siegetop_oldmask_k3.png
a692eee7807622d7ee31bc5eba3781ca420c4b89c27eeac3553a705717c5cfed  .tmp/input-rc/siegetop_oldmask_k4.png
208edd4d55771737ae6e712c7fee1334062c211fe88f339172a4aea57df2c44b  .tmp/input-rc/siegetop_oldmask_k5.png
993d320bd9c12fd160d3a462e918344de819c0a1957bf7d5982f4dd3ce5c3be3  .tmp/input-rc/siegetop_oldmask_k6.png
8f346a32c3db4346b87967e0da9fa48d02a8b8fe4808cc1ec308b8a4bcd46c86  .tmp/input-rc/siegetop_oldmask_k7.png
d13ccbe85c426c417aa237426cd6caa9cdd8934ddb30763aef27e5c62649abe7  .tmp/input-rc/siegetop_pick_k0.png
55873e66e8a7bfdfa2f805a599d502a330c3b4f57f5981b4330c3b19aa424e27  .tmp/input-rc/siegetop_pick_k1.png
f213b40887481cb8bb14c5a98b2caffa289767e5f9b2ee61c14145ff3f2452f9  .tmp/input-rc/siegetop_pick_k2.png
75e7b1d0a13f7241efbed0cf7df0b40b72fdf6e530029a555a46ec7af005455e  .tmp/input-rc/siegetop_pick_k3.png
f293907de5f015947e435f76dd0ee5491e4426ef6327f2e83ae55cdb170f4971  .tmp/input-rc/siegetop_pick_k4.png
234d7c6b6e3fb135c94b28f17261235bf782b47ebd6b8b7f62213dd9d9cad92e  .tmp/input-rc/siegetop_pick_k5.png
d9232262cdf18bd1746f22cb132afce71907b9092f5d932fa744bf41591c3263  .tmp/input-rc/siegetop_pick_k6.png
1e090595697a7fc23b0614e96d1ff2326e5ed66fc3a8ee4114c72c5847bad1eb  .tmp/input-rc/siegetop_pick_k7.png
```

## Что сделать

16 случаев `<часть>_c<k>`. Для случая `<часть>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<часть>` и двумя входными изображениями: первое — `<часть>_pick_k<k>.png`, второе — `<часть>_oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out-rc/` под именем `<часть>_recolour_k<k>.png` сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-siegebase** (часть `siegebase`):

```text
Edit image 1. Image 1 is a sprite of a large tracked vehicle body without its top module: on top of the body there is an empty round ring from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle body from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle body that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the vehicle body in image 1 exactly as they are. Do not recolour any other part of the vehicle body or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**ПК-siegetop** (часть `siegetop`):

```text
Edit image 1. Image 1 is a sprite of a separate heavy top module with a blocky armoured top on a round base and two long parallel tubes, drawn alone from a real-time strategy game on a flat magenta background. Image 2 shows the same module from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the module that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the module in image 1 exactly as they are. Do not recolour any other part of the module or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет корпуса (для `siegebase`) или башни (для `siegetop`), или их больше одного;
- часть обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,008 для `siegebase` или меньше 0,0015 для `siegetop` (у старых масок частей Дома мало: 0,016–0,021 и 0,003–0,005 картинки).

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет первую попытку: первая переносится в `.tmp/out-rc-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 24. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U4-src | <время UTC из date -u>`:
- `## PLAN-U4-src` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 16 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации по 4 одновременно, пока случаи не кончатся; каждому — одна часть и четыре направления, промпт дословно и правило копирования.
- Остановки — блок `## Q-U4-src-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc.md`, строка после каждого шага порядка и после каждой готовой части.
