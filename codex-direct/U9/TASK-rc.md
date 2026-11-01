# Задание U9-rc — перекраска крупных броневых плит Осадного танка: корпус и башня, k0…k7

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u9`, ветка `codex/u9`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc9/` и сдача. Решение владельца: `docs/decisions.md`, Р28 — цвет Дома Осадного на крупных броневых плитах корпуса и башни, около половины, как у Танка.

## Цель

Получить по две перекраски для шестнадцати случаев Осадного танка под 63° — корпус `siegebase_c0` … `siegebase_c7` и башня `siegetop_c0` … `siegetop_c7`, — где чистым зелёным окрашены крупные броневые плиты, а гусеницы, стволы, тёмные щели, люки, решётки и огни остаются своими цветами. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc9/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `siegebase_pick_k0.png` … `siegebase_pick_k7.png` | корпус Осадного танка без башни под 63°, направления k0…k7 |
| `siegetop_pick_k0.png` … `siegetop_pick_k7.png` | башня Осадного танка отдельно, направления k0…k7 |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U9-rc-01` и стоп.

```text
ce741c36f6c81465fb8f5a3af17f22767d4471033c416e716318e0af6829d778  .tmp/input-rc9/siegebase_pick_k0.png
90dc35aea8a0d7aa5aced97d1cb442f137f4afda19dec3604a6634462348ae63  .tmp/input-rc9/siegebase_pick_k1.png
5920e137f70580d71e70cdc03c2020454443f893d71aa5928ee824f3c8936a9d  .tmp/input-rc9/siegebase_pick_k2.png
da58e3ded2208552a248e0999d8b2a02084b09a3d46bb89d3bd6f01d8885b4fe  .tmp/input-rc9/siegebase_pick_k3.png
2fae7c5db7f1fff43f4535c3cf50f6dcb60f50c33f3f46db2cfd559f8fc1ec50  .tmp/input-rc9/siegebase_pick_k4.png
a3a2997c29cd7955557139b34e12ed3e9233c6a5c51f9b09a15e6891f0c6e7fe  .tmp/input-rc9/siegebase_pick_k5.png
c6ba18d10f0715604e9e609ab2eea390709a845208d408667e67657c68524cd3  .tmp/input-rc9/siegebase_pick_k6.png
03c1b4701d98974ddd293207ab855846ac396f7f7bdfa1ae8b391ee6d13dc517  .tmp/input-rc9/siegebase_pick_k7.png
d13ccbe85c426c417aa237426cd6caa9cdd8934ddb30763aef27e5c62649abe7  .tmp/input-rc9/siegetop_pick_k0.png
55873e66e8a7bfdfa2f805a599d502a330c3b4f57f5981b4330c3b19aa424e27  .tmp/input-rc9/siegetop_pick_k1.png
f213b40887481cb8bb14c5a98b2caffa289767e5f9b2ee61c14145ff3f2452f9  .tmp/input-rc9/siegetop_pick_k2.png
75e7b1d0a13f7241efbed0cf7df0b40b72fdf6e530029a555a46ec7af005455e  .tmp/input-rc9/siegetop_pick_k3.png
f293907de5f015947e435f76dd0ee5491e4426ef6327f2e83ae55cdb170f4971  .tmp/input-rc9/siegetop_pick_k4.png
234d7c6b6e3fb135c94b28f17261235bf782b47ebd6b8b7f62213dd9d9cad92e  .tmp/input-rc9/siegetop_pick_k5.png
d9232262cdf18bd1746f22cb132afce71907b9092f5d932fa744bf41591c3263  .tmp/input-rc9/siegetop_pick_k6.png
1e090595697a7fc23b0614e96d1ff2326e5ed66fc3a8ee4114c72c5847bad1eb  .tmp/input-rc9/siegetop_pick_k7.png
```

## Что сделать

Шестнадцать случаев из раздела «Цель». Для случая `<часть>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<часть>` и одним входным изображением `<часть>_pick_k<k>.png`. Две попытки на случай с одним и тем же промптом: `a` и `b`. Каждую картинку скопируй в `.tmp/out-rc9/` под именем `<часть>_recolour_k<k>_<попытка>.png`, например `siegetop_recolour_k1_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-siegebase** (часть `siegebase`):

```text
Edit image 1. Image 1 is a sprite of a heavy tracked vehicle body without its top module, seen from above at a steep angle, from a real-time strategy game on a flat magenta background. On top of the body there is an empty round ring.
Recolour to flat pure green RGB 0,255,0 the large flat armour plates of the body: the top deck plates around the round ring, the front plate, the rear plate and the long side armour covers above the tracks.
Keep in their original colours: the tracks with their road wheels, the empty round ring and the dark hole inside it, the dark gaps and seams between plates, small vents and grilles, hatches, small lights and glass panels.
Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour the background. Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**ПК-siegetop** (часть `siegetop`):

```text
Edit image 1. Image 1 is a sprite of a separate heavy gun module with two long parallel gun barrels, standing on a round base disc, seen from above at a steep angle, from a real-time strategy game on a flat magenta background.
Recolour to flat pure green RGB 0,255,0 the large flat armour plates of the gun module: its top plates and its side and front plates around the guns.
Keep in their original colours: the two gun barrels with their muzzles, the round base disc under the module, the dark gaps and seams between plates, small vents, hatches and small lights.
Keep the shape, outline, position and size of the module in image 1 exactly as they are. Do not recolour the background. Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или модуля, или их больше одного;
- машина или модуль обрезаны краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет свою попытку: заменённая картинка переносится в `.tmp/out-rc9-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 40. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc9/prompts.md`: по каждой итоговой картинке — имя, входной файл, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U9-rc | <время UTC из date -u>`:
- `## PLAN-U9-rc` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc9/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 32 генерации → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: четыре субагента `gpt-6-luna` `xhigh` делают генерации сразу, каждый — четыре случая и обе попытки каждого: первый — `siegebase_c0`…`siegebase_c3`, второй — `siegebase_c4`…`siegebase_c7`, третий — `siegetop_c0`…`siegetop_c3`, четвёртый — `siegetop_c4`…`siegetop_c7`; каждому — промпт дословно и правило копирования.
- Остановки — блок `## Q-U9-rc-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась и за 30 минут не дописала ни строки в свой журнал (команда, которую оболочка вернула без кода выхода, пока процесс работает, — не сбой; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc9.md`, строка после каждого шага порядка и после каждого готового случая.
- Комментарии в коде. Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.
