# Задание U5-rc — перекраска Харвестера по старой маске, ряд 0

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u5`, ветка `codex/u5`. Коммитов не делай: правило «коммит на каждый законченный подпункт» из правил в конце к этому заданию не относится, результат — файлы в `.tmp/out-rc/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U5.

## Цель

Получить 8 перекрасок Харвестера под 63°, направления k0…k7, — где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-rc/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `harvester_pick_k0.png` … `harvester_pick_k7.png` | новый Харвестер под 63°, направления k0…k7 |
| `harvester_oldmask_k0.png` … `harvester_oldmask_k7.png` | старый Харвестер, камера 36°: части цвета Дома залиты чистым зелёным |


Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U5-rc-01` и стоп.

```text
da24bf2b122822b9e71a145be512c4aa8946174368f6e51db35dd4d802571379  .tmp/input-rc/harvester_oldmask_k0.png
110828867c3e970a100bdb051af8b5bdbe07c437be9aa39301769b2ec1293f02  .tmp/input-rc/harvester_oldmask_k1.png
45e0473b168d0e80a7f84f2d19bd4718914825fea7d37d0baaf8ad2638c1fec0  .tmp/input-rc/harvester_oldmask_k2.png
b3f8d88ef27bbabf3289ae66149fa997d91f08fcf21aaf8c9699c2efde422fa2  .tmp/input-rc/harvester_oldmask_k3.png
0167e5c1fa3f8443cbc9a954e4874838eee932f48401cf128254eddda339dadf  .tmp/input-rc/harvester_oldmask_k4.png
8541addaf9f4e12ba84dde5c29a1ec253f3d794f92af8c40ab93ccee26b591a8  .tmp/input-rc/harvester_oldmask_k5.png
7daa77985de5407d0070acbfeb871f2c509e1ca831cfc3e34a67edad33b35ec8  .tmp/input-rc/harvester_oldmask_k6.png
934737bd54908b2fd7ff56c2b3b953a9342453e832801be45025d4bc039be02b  .tmp/input-rc/harvester_oldmask_k7.png
af28a2fafcb4d6bfbcd008de1c76942beda3fb71444a665c1927b1c346c94777  .tmp/input-rc/harvester_pick_k0.png
73824148cf6e6be3f5676944212e5640ccade5595107c89b2dcf45fe5ed86c48  .tmp/input-rc/harvester_pick_k1.png
802994683cbfaaa1d7cd2f91d9df27d0610f077d680397dcf91fedd8282ce607  .tmp/input-rc/harvester_pick_k2.png
66ba09efe80a651f011603968ebd317e634a295697aa70e283175310522cf724  .tmp/input-rc/harvester_pick_k3.png
9a567a49c3a679c29024cf27a39662c9a1a58bdaf9e6beee6ee971642432ffb8  .tmp/input-rc/harvester_pick_k4.png
7c18f1f3f4c79d7191d360e7e56ffd5bee9bbbfe9d6e9907867f8c3cf58e52ea  .tmp/input-rc/harvester_pick_k5.png
ea9918083ba0c14b708732e948915a88618b9cedbd641c70c6a6b2080d4214be  .tmp/input-rc/harvester_pick_k6.png
7d0fd60df432dd989e81b7fcaff39eaa2e30b9ce8fe4bdac6b6a24930612b2e9  .tmp/input-rc/harvester_pick_k7.png
```

## Что сделать

8 случаев `harvester_c<k>`, k = 0…7. Для случая `harvester_c<k>` вызови `image_gen.imagegen` с промптом `ПК-harvester` и двумя входными изображениями: первое — `harvester_pick_k<k>.png`, второе — `harvester_oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out-rc/` под именем `harvester_recolour_k<k>.png` сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

Промпты — дословно, без правок и дополнений:

**ПК-harvester**:

```text
Edit image 1. Image 1 is a sprite of a large tracked harvester vehicle with a long armoured body on a wide dark tracked base from a real-time strategy game on a flat magenta background. Image 2 shows the same harvester from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the harvester that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the harvester in image 1 exactly as they are. Do not recolour any other part of the harvester or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет Харвестера или их больше одного;
- Харвестер обрезан краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,04 (у старой маски — 0,083–0,101 картинки).

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Повтор заменяет первую попытку: первая переносится в `.tmp/out-rc-first/` под своим именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел.** Всего запросов к генератору, вместе с повторами и отказами, — не больше 12. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-rc/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U5-rc | <время UTC из date -u>`:
- `## PLAN-U5-rc` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-rc/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 итоговых файлов;
- раздел «Отказы модерации» (нет — так и написать);
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 8 генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга; повтор картинки начинается после того, как её первая попытка проверена.
- Помощники: два субагента `gpt-6-luna` `xhigh` делают генерации сразу, каждому — четыре направления, промпт дословно и правило копирования.
- Остановки — блок `## Q-U5-rc-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-rc.md`, строка после каждого шага порядка и после каждого готового субагента.
