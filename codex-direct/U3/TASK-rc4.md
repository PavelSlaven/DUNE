# Задание U3-rc4 — перекраска Ракетной установки по списку частей: k1, k2, k7

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u3`, ветка `codex/u3`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc4/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U3.

## Цель

Получить по две перекраски для трёх случаев Ракетной установки под 63° — `launcher_c1`, `launcher_c2`, `launcher_c7`, — где чистым зелёным окрашена вся наружная броня машины по списку частей промпта: пакет труб снаружи, кабина, борта и юбки над гусеницами по всей длине, задняя плита; гусеницы, открытое ложе с механизмами, наконечники и торцы труб, фары и решётки остаются в своих цветах. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc4/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `launcher_pick_k1.png`, `launcher_pick_k2.png`, `launcher_pick_k7.png` | новая Ракетная установка под 63°, направления k1, k2 и k7 |
| `launcher_oldmask_k1.png`, `launcher_oldmask_k2.png`, `launcher_oldmask_k7.png` | старая Ракетная установка, камера 36°: части цвета Дома залиты чистым зелёным |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U3-rc4-01` и стоп.

```text
4cadfdc37e064693b6cfa97eb30bf33ddd2b566151ec09669e022d18b71c2ab3  .tmp/input-rc4/launcher_pick_k7.png
6699873d222ec2cc68638fe25a0e3d6e456be951bc07eebe6f5660feb4df908e  .tmp/input-rc4/launcher_oldmask_k1.png
b610e2dbaa48653c1375807a75c81f39ac445ca9fd73fee7c9adbe6b69d598dc  .tmp/input-rc4/launcher_oldmask_k2.png
c1264b72292d2290bb63f7204b0b0b54273fd66a27c64a1ffd296fd334ca47b4  .tmp/input-rc4/launcher_pick_k1.png
d705b05acb929924585c324c7aaaee7956555836e27a3f58d22edbf2eb8798f6  .tmp/input-rc4/launcher_pick_k2.png
dea490628a95ba43393ca04396a8af5059c5f7416a1d0e0d4f7241069f177f75  .tmp/input-rc4/launcher_oldmask_k7.png
```

## Что сделать

Три случая из раздела «Цель». Для случая `<юнит>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<юнит>` и двумя входными изображениями: первое — `<юнит>_pick_k<k>.png`, второе — `<юнит>_oldmask_k<k>.png`. Две попытки на случай с одним и тем же промптом: `a` и `b`. Каждую картинку скопируй в `.tmp/out-rc4/` под именем `<юнит>_recolour_k<k>_<попытка>.png`, например `launcher_recolour_k1_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-launcher** (юнит `launcher`):

```text
Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of long tubes on its back from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 to flat pure green RGB 0,255,0 all outer armour of the vehicle: the outer shell of the tube rack, the cab (roof, bonnet, doors and sides), the hull sides and the side skirts above the tracks along their whole length down to the tracks, and the rear plate of the hull. Do not recolour the tracks and road wheels, the open bed between the cab and the base of the tube rack (its floor, inner walls and the machinery in it), the tips and open ends of the tubes, the lights, grilles and vents. Image 2 is only a rough guide to these parts; where image 2 differs from this list, follow this list.
Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет свою попытку: заменённая картинка переносится в `.tmp/out-rc4-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 9. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc4/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U3-rc4 | <время UTC из date -u>`:
- `## PLAN-U3-rc4` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc4/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 6 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: три субагента `gpt-6-luna` `xhigh` делают генерации сразу, каждый — один случай и обе его попытки, промпт дословно и правило копирования.
- Остановки — блок `## Q-U3-rc4-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась и за 30 минут не дописала ни строки в свой журнал (команда, которую оболочка вернула без кода выхода, пока процесс работает, — не сбой; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc4.md`, строка после каждого шага порядка и после каждого готового случая.
