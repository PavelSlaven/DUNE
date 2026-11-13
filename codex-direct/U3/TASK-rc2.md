# Задание U3-rc2 — повтор перекрасок Девиатора и Ракетной установки

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u3`, ветка `codex/u3`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc2/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U3.

## Цель

Получить по две новые перекраски для девяти случаев под 63° — `deviator_c0`, `deviator_c1`, `deviator_c2`, `deviator_c4`, `deviator_c5`, `deviator_c6`, `deviator_c7`, `launcher_c0`, `launcher_c4`, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `<юнит>_pick_k0.png` … `<юнит>_pick_k7.png` | новый юнит под 63°, направления k0…k7 |
| `<юнит>_oldmask_k0.png` … `<юнит>_oldmask_k7.png` | старый юнит, камера 36°: части цвета Дома залиты чистым зелёным |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U3-rc2-01` и стоп.

```text
83afcec33b956156b32df4e098775cd5827631dafc7b1b7c1d3a62117affcbc5  .tmp/input-rc/deviator_oldmask_k0.png
6ff269631119e95bdf1c44b2edb7d484952500f56039ef1dd24fe8569bd3d647  .tmp/input-rc/deviator_oldmask_k1.png
edda2d0938d73ba00ec44d2dbcd39e7ad6a13ad43d437971be5abbc007000aec  .tmp/input-rc/deviator_oldmask_k2.png
afe1108e895e65c269b491d14c6c20babb71d6ed9b734e51dab49e3faf61d380  .tmp/input-rc/deviator_oldmask_k4.png
13c47fc8a7303f6b7b4b04dab1636689f6d17b2952a45d48b6e95b6d4adff7f5  .tmp/input-rc/deviator_oldmask_k5.png
53de87fdd45c954a84aef7cb44a6f8ba3699c6ad3c85f20449d93b5739f820af  .tmp/input-rc/deviator_oldmask_k6.png
3a283a9cfab36140aa3172d2f89550de9f6ac3993f3d2c81c01858e87092f50e  .tmp/input-rc/deviator_oldmask_k7.png
979726bf0e5267c59950a88ebd11989fbe13c2b506a1ccb414a6fab61dc671e4  .tmp/input-rc/deviator_pick_k0.png
4924ba0bf45a4ecd1e399050f8b272909cec12bf95b37b3e05b07da11da54fb7  .tmp/input-rc/deviator_pick_k1.png
d1517a51c3630363565931cec9a3af2cf358ad6d7b785e9bde5345036c2ea181  .tmp/input-rc/deviator_pick_k2.png
3a6f7863bbf7f313a7edc06ec7acf45c99a558de85c8cd40128e353d9d32277d  .tmp/input-rc/deviator_pick_k4.png
55da10be12cb28870c75a7be12fdb1e8fb28b460df83331b4d6d06444e36aba7  .tmp/input-rc/deviator_pick_k5.png
1d34883e67799bf01b04cd4b27fa7e89d31bb67119fdc1a07f5278d0f0216d17  .tmp/input-rc/deviator_pick_k6.png
9d53b52f42fd55387e845283aaeaa8b6250b386ea5a6936ff2b8785f9876b533  .tmp/input-rc/deviator_pick_k7.png
dff62a8437d090a7db10743e7eb67aa805754f5c543da9fdfbc82a4fb53e8171  .tmp/input-rc/launcher_oldmask_k0.png
fe50e886e5f0e9eb90fdb67ac3b3fc84846d0e1745e9558893a8dceea01a7dac  .tmp/input-rc/launcher_oldmask_k4.png
b44579c09fcb8420f31efe28adbdcdf873f27692665401088cdb4cf3f45e3891  .tmp/input-rc/launcher_pick_k0.png
cf5a635d7e5a3b3d93aa823aa9e818b562d60245f176e8fc0bebdda709193469  .tmp/input-rc/launcher_pick_k4.png
```

## Что сделать

Девять случаев из раздела «Цель». Для случая `<юнит>_c<k>` вызови `image_gen.imagegen` с промптом `ПК-<юнит>` и двумя входными изображениями: первое — `<юнит>_pick_k<k>.png`, второе — `<юнит>_oldmask_k<k>.png`. Две попытки на случай с одним и тем же промптом: `a` и `b`. Каждую картинку скопируй в `.tmp/out-rc2/` под именем `<юнит>_recolour_k<k>_<попытка>.png`, например `deviator_recolour_k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-launcher** (юнит `launcher`):

```text
Edit image 1. Image 1 is a sprite of a tracked vehicle with a raised rack of long tubes on its back from a real-time strategy game on a flat magenta background. Image 2 shows the same vehicle from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the vehicle that are green in image 2 to flat pure green RGB 0,255,0. The open bed of the vehicle between the cab and the base of the tube rack is not team colour: keep the floor and the inner walls of that bed in their original colours. Keep the shape, outline, position and size of the vehicle in image 1 exactly as they are. Do not recolour any other part of the vehicle or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```
**ПК-deviator** (юнит `deviator`):

```text
Edit image 1. Image 1 is a sprite of a tracked tank with a large twin box on its turret from a real-time strategy game on a flat magenta background. Image 2 shows the same tank from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green. In image 1 the team colour is the steel-blue paint of the tank.
Recolour in image 1 every steel-blue painted part of the tank to flat pure green RGB 0,255,0, including small panels, the lower band of the hull and the end plates of the box. Keep the shape, outline, position and size of the tank in image 1 exactly as they are. Do not recolour parts that are not steel blue: tan patches, dark metal, tracks, lights, white stripes and markings keep their colours. Do not recolour the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет свою попытку: заменённая картинка переносится в `.tmp/out-rc2-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 27. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc2/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U3-rc2 | <время UTC из date -u>`:
- `## PLAN-U3-rc2` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc2/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 18 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации по 3 одновременно, пока случаи не кончатся; каждому — один случай и обе его попытки, промпт дословно и правило копирования.
- Остановки — блок `## Q-U3-rc2-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc2.md`, строка после каждого шага порядка и после каждого готового случая.
