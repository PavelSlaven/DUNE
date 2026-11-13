# Задание U2-gen2 — перекраска Квадроцикла по старой маске

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u2`, ветка `codex/u2`. Коммитов не делай: результат — файлы в `.tmp/out2/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U2.

## Цель

Получить восемь перекрасок нового Квадроцикла под 63°, где чистым зелёным окрашены те же части, что окрашены цветом Дома в старом спрайте. Облик и точность перекраски оценивает ведущий, не ты.

## Входы

Папка `.tmp/input2/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255).

| Файлы | Что это |
|---|---|
| `pick_k0.png` … `pick_k7.png` | новый Квадроцикл под 63°, направления k0…k7 |
| `oldmask_k0.png` … `oldmask_k7.png` | старый Квадроцикл, камера 36°: части цвета Дома залиты чистым зелёным |

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U2-gen2-01` и стоп.

```text
7cfdd5dcc7308dd7b9cef5091f39a7ff677923a65fc416283f2d5361cb6a3719  .tmp/input2/oldmask_k0.png
f24a803758d68a1293675cf8aee05b7a7b7949cef99d08796d654fe8239953de  .tmp/input2/oldmask_k1.png
d5a3b317179049bdc7b58430258718eabbb59f11835b24bd785e10200b4ea36a  .tmp/input2/oldmask_k2.png
c844a3f8268690bf8ab4f7c23f03a4aa56f6d5a818e704d02375eddabcac9f1b  .tmp/input2/oldmask_k3.png
8d8302e08a7adebca9450e0537492df11c369833fd58d9c71e07ab8abfd03131  .tmp/input2/oldmask_k4.png
28904ed7dfbd97299f8004f1fd1fa6eb5a0963be2215551a2508036d994bd409  .tmp/input2/oldmask_k5.png
ad9b65f76928f604b7eac0186674580d39c451e20b4bb43646837b54887e8742  .tmp/input2/oldmask_k6.png
278306f42ba103fb1358a3624c872f65792d882e00fee030aca60644bf79a24d  .tmp/input2/oldmask_k7.png
31aec30026066d7256803c43c5b3d25a9e0ef652c5d8ebc421bcd11a70c973c8  .tmp/input2/pick_k0.png
f7108f26714c9f70f57554005ef64237053798ceca8b6617661ee5879ad0f622  .tmp/input2/pick_k1.png
8fdd4e12e9c348b134d1c418d50e39f43d3b2068f6cf6518ed7dd6effadf4958  .tmp/input2/pick_k2.png
65a90f3431f1ed679f00b328c7f0361cc8c4875e23b39cd8cbbdd00aa0d4b22b  .tmp/input2/pick_k3.png
e29eecb60f1545a486bb983ee5263836819bb71d56a2c56f2fbb3ec34dc90781  .tmp/input2/pick_k4.png
517f1d6c48706fa7ca9061af39d2b36fcb6dec3f4b5342b4aaae8949c0116537  .tmp/input2/pick_k5.png
b36029e4f5a392ec983ec944ea7218ddc751a06f323b8f470173b7e076f03730  .tmp/input2/pick_k6.png
3953f60bdc6070a418a6084ba14d87d20c259be07f6d35a7d0ec2ac077763a5c  .tmp/input2/pick_k7.png
```

## Что сделать

Восемь случаев `c0`…`c7`. Для случая `c<k>` вызови `image_gen.imagegen` с промптом ПК и двумя входными изображениями: первое — `pick_k<k>.png`, второе — `oldmask_k<k>.png`. Одна попытка на случай. Картинку скопируй в `.tmp/out2/` под именем `quad_recolour_k<k>.png` сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

ПК:

```text
Edit image 1. Image 1 is a sprite of a light four-wheeled armoured buggy from a real-time strategy game on a flat magenta background. Image 2 shows the same buggy from a lower camera; in image 2 the parts that carry the team colour are painted flat pure green.
Recolour in image 1 the same parts of the buggy that are green in image 2 to flat pure green RGB 0,255,0. Keep the shape, outline, position and size of the buggy in image 1 exactly as they are. Do not recolour any other part of the buggy or the background.
Keep the background flat pure magenta RGB 255,0,255. Do not add anything: no shading or texture on the green, no text, letters, numbers, logos or watermarks.
```

Промпт — дословно, без правок и дополнений.

**Доля зелёного** картинки — число пикселей с `G − max(R, B) ≥ 80`, делённое на число всех пикселей; считай скриптом `/srv/dune/venv/bin/python`.

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет машины или машин больше одной;
- машина обрезана краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- доля зелёного меньше 0,02.

Неточный пурпурный фон и неточный зелёный — не повод для повтора. Всего генераций, вместе с повторами, — не больше 12.

Запиши `.tmp/out2/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, фактический размер, путь исходного файла генерации, доля зелёного, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U2-gen2 | <время UTC из date -u>`:
- `## PLAN-U2-gen2` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out2/` → случай → путь исходного файла генерации → фактический размер → доля зелёного → повтор (нет или причина);
- SHA-256 восьми итоговых файлов;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → восемь генераций → доли зелёного и повторы → `prompts.md` → сдача.
- Параллельно: восемь генераций независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев, промпт дословно и правило копирования.
- Остановки — блок `## Q-U2-gen2-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress2.md`, строка после каждого шага порядка.
