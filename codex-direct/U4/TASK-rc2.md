# Задание U4-rc2 — повтор трёх перекрасок Танка по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u4`, ветка `codex/u4`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc2/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U4.

## Цель

Получить по две новые перекраски для трёх случаев Танка под 63° — `tankbase_c3`, `tanktop_c0`, `tanktop_c4`, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `<часть>_pick_k0.png` … `<часть>_pick_k7.png` | новая часть Танка под 63°, направления k0…k7 |
| `<часть>_oldmask_k0.png` … `<часть>_oldmask_k7.png` | старая часть Танка, камера 36°: части цвета Дома залиты чистым зелёным |

Части: `tankbase` — корпус без башни, `tanktop` — башня без корпуса.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U4-rc2-01` и стоп.

```text
84e47b8dc00323bc84aeca7c18967b307b7aa7a6455f06b31a702cd7eaaa9229  .tmp/input-rc/tankbase_oldmask_k3.png
11abc0da4e1e960ef69f308d13151afc6cfd6e5b11be279b3d953fdb1127ad7e  .tmp/input-rc/tankbase_pick_k3.png
ce3405f6b7aef4b1489bda0d67269e3007061b3fd901b04b361e49cbcb67cf0f  .tmp/input-rc/tanktop_oldmask_k0.png
d42416e8a860276d73af26d213027c202cbebf5795fcdf6131729b7f7c75802d  .tmp/input-rc/tanktop_oldmask_k4.png
eef8eda5a3b4fb85d42f24a0ced2606214396b42319d9d5618bf2e3f47d71348  .tmp/input-rc/tanktop_pick_k0.png
4c976d923d18af8f5918acd51722c0a8786a977a1ef100b77e23fa6ef29d984b  .tmp/input-rc/tanktop_pick_k4.png
```

## Что сделать

Три случая: `tankbase_c3`, `tanktop_c0`, `tanktop_c4`. Для случая `<часть>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<часть>` и двумя входными изображениями: первое — `<часть>_pick_k<k>.png`, второе — `<часть>_oldmask_k<k>.png`. Две попытки на случай с одним и тем же промптом: `a` и `b`. Каждую картинку скопируй в `.tmp/out-rc2/` под именем `<часть>_recolour_k<k>_<попытка>.png`, например `tankbase_recolour_k3_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

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

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет свою попытку: заменённая картинка переносится в `.tmp/out-rc2-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 9. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc2/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U4-rc2 | <время UTC из date -u>`:
- `## PLAN-U4-rc2` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc2/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 6 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: три субагента `gpt-6-luna` `xhigh` делают генерации сразу, каждый — один случай и обе его попытки; в бриф — промпт дословно и правило копирования.
- Остановки — блок `## Q-U4-rc2-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc2.md`, строка после каждого шага порядка и после каждого готового случая.
