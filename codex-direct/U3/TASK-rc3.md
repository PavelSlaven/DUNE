# Задание U3-rc3 — перекраска других попыток Звукового танка и Ракетной установки

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u3`, ветка `codex/u3`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc3/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U3.

## Цель

Получить по две перекраски для трёх случаев под 63° — `sonic_c4`, `sonic_c7`, `launcher_c3`, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc3/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `sonic_pick_k4.png`, `sonic_pick_k7.png`, `launcher_pick_k3.png` | новый юнит под 63°, направления k4, k7 и k3 |
| `sonic_oldmask_k4.png`, `sonic_oldmask_k7.png`, `launcher_oldmask_k3.png` | старый юнит, камера 36°: части цвета Дома залиты чистым зелёным |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U3-rc3-01` и стоп.

```text
0a9075c0c6bdc6f454375b72705bdc4345ee4f9bef08059401dca99631ab251f  .tmp/input-rc3/sonic_oldmask_k4.png
1dde1052b15dce39d5613bdc19f92c9ed0e8be48920f32db86a2432a57870400  .tmp/input-rc3/launcher_pick_k3.png
5fee9935a165c6e2f1faa12445c985da3c9710ff9a0e86045db01044854d2039  .tmp/input-rc3/sonic_oldmask_k7.png
66e0320970d3e68c335817b002516fe752ecb362d1a574c8b9f3521f1167e10f  .tmp/input-rc3/sonic_pick_k7.png
c71972685275dd732c66f0080d4e1ca360b5d013337c626342c92872558f838e  .tmp/input-rc3/launcher_oldmask_k3.png
fa3e96ec0fe83e8e5908c9cdf6a1039e97ffa37d7529ff48efcbf4058622cc54  .tmp/input-rc3/sonic_pick_k4.png
```

## Что сделать

Три случая из раздела «Цель». Для случая `<юнит>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<юнит>` и двумя входными изображениями: первое — `<юнит>_pick_k<k>.png`, второе — `<юнит>_oldmask_k<k>.png`. Две попытки на случай с одним и тем же промптом: `a` и `b`. Каждую картинку скопируй в `.tmp/out-rc3/` под именем `<юнит>_recolour_k<k>_<попытка>.png`, например `sonic_recolour_k4_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-launcher** (юнит `launcher`):

```text
Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of long tubes on its back from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle that are green in image 2 to flat pure green RGB 0,255,0. The open bed of the vehicle between the cab and the base of the tube rack is not team colour: keep the floor and the inner walls of that bed in their original colours. Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour any other part of the vehicle or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-sonic** (юнит `sonic`):

```text
Edit image 1. Image 1 is a sprite of a tracked tank with a large golden dish on its turret from a real-time strategy game on a flat magenta background. Image 2 shows the same tank from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the tank that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the tank in image 1 exactly as they are. Do not recolour any other part of the tank or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет свою попытку: заменённая картинка переносится в `.tmp/out-rc3-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 9. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc3/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U3-rc3 | <время UTC из date -u>`:
- `## PLAN-U3-rc3` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc3/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 6 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: три субагента `gpt-6-luna` `xhigh` делают генерации сразу, каждый — один случай и обе его попытки, промпт дословно и правило копирования.
- Остановки — блок `## Q-U3-rc3-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc3.md`, строка после каждого шага порядка и после каждого готового случая.
