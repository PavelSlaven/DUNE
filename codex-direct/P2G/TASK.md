# Задание P2G — генерации HD-рисунков трёх картинок апстрима

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая папка: `/srv/dune/worktrees/p2g` — пустой репозиторий git без коммитов, в нём только `.tmp/`. Коммитов не делай: результат — файлы в `.tmp/out/` и сдача. План работ: `docs/upstream/PORT_PLAN.md` репозитория DUNE, шаг П2г; решение владельца Р65.

## Цель

Получить 12 картинок: по четыре попытки на каждый из трёх случаев — карточку выбора дома Сардаукаров, обломки разбитого перевозчика и экран ментата Сардаукаров. Облик, выбор попыток и подгонку под размеры игры делает ведущий, не ты.

## Входы

Папка `.tmp/input/`:

| Файл | Размер | Что на нём |
|---|---|---|
| `card_classic.png` | 720 × 784 | старая пиксельная карточка дома Сардаукаров, увеличенная |
| `card_refs.png` | 1128 × 392 | три HD-карточки других домов рядом, образец стиля |
| `wreck_classic.png` | 512 × 512 | старый пиксельный спрайт обломков перевозчика на пурпурном фоне, увеличенный |
| `wreck_carryall.png` | 768 × 384 | HD-перевозчик в двух направлениях на пурпурном фоне, образец облика |
| `mentat_harkonnen.png` | 1800 × 1200 | HD-экран ментата Харконненов; слева и справа чёрные поля по 100 px |
| `mentat_classic.png` | 1800 × 1200 | старый пиксельный экран ментата Сардаукаров, увеличенный; слева и справа чёрные поля по 100 px |

Перед работой сверь SHA-256 входов командой `sha256sum -c .tmp/input.sha256` из рабочей папки. Список в файле:

```text
5ecdda0a987de798f14bda828ff4e2af949d3cb12272aaa679500de8c62378e7  .tmp/input/card_classic.png
09b80d04eb6bf83be24ea366f106bb0570e9cb113c39b6ae4dc33417e823d46b  .tmp/input/card_refs.png
b3a940e6a5fe399d7f78d0b80051d304ac0e8b18d9ae935dfd07c67de8d78c30  .tmp/input/mentat_classic.png
73f0db3bb15ee1a7edc7af3729052f96095f626a89ad018916b84570c087ff4b  .tmp/input/mentat_harkonnen.png
37a502901218d7bc529a6e649fc9195ee9c4b930647b1967147ca02bd0cc92de  .tmp/input/wreck_carryall.png
8712e2f32baedc25bb189b754a09dd0c9408f25f92e8dd28a2632a488a654761  .tmp/input/wreck_classic.png
```

Хоть одна строка не `OK` — блок `Q-P2G-01` с выводом и стоп.

## Что сделать

Три случая — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и входными изображениями в указанном порядке. Сделай четыре попытки с одним и тем же промптом: `a`, `b`, `c`, `d`. Каждую картинку скопируй в `.tmp/out/` под именем `<случай>_<попытка>.png`, например `card_a.png`, сразу после генерации. Файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт |
|---|---|---|---|
| `card` | `card_classic.png` | `card_refs.png` | П-card |
| `wreck` | `wreck_classic.png` | `wreck_carryall.png` | П-wreck |
| `mentat` | `mentat_harkonnen.png` | `mentat_classic.png` | П-mentat |

Промпты — дословно, без правок и дополнений.

П-card:

```text
Draw a new house emblem card in exactly the same style as the three cards in image 2.
Image 2 shows three emblem cards of other houses from a strategy game, side by side. Each card is a round medallion: a bronze-gold metal ring with small rivets and ornaments, a coloured enamel field inside the ring and a metal relief emblem in the centre, on a dark grey textured stone background. Image 1 is an old low-resolution pixel-art card of the Sardaukar house: a golden lion head in profile facing left on a blue-violet oval inside a purple frame, with a name plate below.
Draw one new medallion card for the Sardaukar in the style of image 2: the same kind of bronze-gold ring with rivets, the same lighting, materials, level of detail and painted realism, the same dark grey textured background. Inside the ring there is a deep purple enamel field. In the centre there is a golden lion head in profile facing left, as in image 1, in polished gold metal relief. Small violet gems may decorate the ring. Do not use the eagle, the ram skull or the snake from image 2.
The medallion is centred. Its diameter is about 85 percent of the canvas width, and the whole ring is inside the canvas. The dark textured background fills the canvas to every edge. No name plate, no chains, no text, letters, numbers, logos or watermarks.
```

П-wreck:

```text
Draw the crashed wreck of the flying transport from image 2, lying on the ground, for a top-down real-time strategy game.
Image 2 shows the transport from above, from a camera about 63 degrees above the horizon, in two directions: a long silver-grey metal fuselage with a blue glass cockpit at the front end, a cross beam with a round engine pod at each end, and dark grey tail fins at the back. Image 1 is an old low-resolution pixel-art sprite of the same wreck: the fuselage is broken in two, the front part with the blue cockpit lies at the lower left, and torn grey metal plates lie at the upper right.
Draw the wreck as in image 1, in the painted style, materials, detail and lighting of image 2, from the same camera as image 2: the silver-grey fuselage broken in two pieces, the blue cockpit glass cracked, torn and bent metal plates, a broken engine pod, scorch marks and soot. The wreck is centred and fills about 80 percent of the canvas; no part touches the edges.
Fill everything outside the wreck with flat pure magenta RGB 255,0,255. No ground, no sand, no cast shadow, no smoke, no fire, no glow, no text, letters, numbers, logos or watermarks.
```

П-mentat:

```text
Edit image 1: replace only the man on the left and the picture on the screen; keep everything else in image 1 unchanged.
Image 1 is the briefing screen of an advisor in a strategy game, painted in a realistic dark science-fiction style: a dark metal wall with gold trim, a long bar at the top, a large screen on the right, two empty button plates below the screen, and on the left a bald advisor in a red robe. The black bars at the left and right edges of image 1 are padding. Image 2 is an old low-resolution pixel-art version of a different advisor screen: on the left a stocky middle-aged officer with a stern frown and heavy eyebrows, wearing a black military cap with up-turned sides, a high-collared black uniform with gold braided shoulder boards and a small gold badge on the chest, with his arms crossed.
1. Replace the advisor on the left of image 1 with the officer from image 2: the same man, face, expression, cap, uniform, gold shoulder boards, chest badge and crossed arms. Paint him in the same realistic style, lighting and level of detail as the advisor in image 1, at the same place and at the same size as the advisor in image 1, cut off by the bottom edge in the same way. Use deep purple and violet accents instead of red.
2. Replace the red emblem and the red planet on the screen with a glowing violet emblem, a lion head in profile facing left inside a thin ring, and a dark violet planet, in the same style as the red ones.
Keep the metal wall, the gold trim, the top bar, the screen frame, the button plates, their positions and sizes, and the black padding bars exactly as in image 1. No text, letters, numbers, logos or watermarks.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:

- `card`: на картинке нет медальона или их больше одного; кольцо медальона обрезано краем картинки; на картинке есть текст, буквы или цифры;
- `wreck`: обломки касаются края картинки; на картинке есть текст, буквы или цифры; фон не пурпурный — среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100;
- `mentat`: слева нет человека; на картинке есть текст, буквы или цифры.

Неточный пурпурный фон у `wreck` — не повод для повтора. Повторённая картинка заменяет исходную под тем же именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай, попытку и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим попыткам. Отказ модерации не останавливает работу.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 24. Предел исчерпан, а попытки остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, имя промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-P2G | <время UTC из date -u>`:

- `## PLAN-P2G` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 12 итоговых файлов;
- «Отказы модерации» — случаи и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** сверка SHA-256 входов → 12 генераций → повторы → `prompts.md` → сдача.
- **Параллельно:** все генерации независимы друг от друга.
- **Помощники:** три субагента `gpt-6-luna` `xhigh`, без вложенных, запускаются сразу после сверки входов: каждому — один случай и его четыре попытки. В бриф помощника дословно входят промпт его случая, порядок входных изображений, правило копирования, правила повтора и отказа модерации и его доля предела: 8 запросов. Сверку входов, `prompts.md` и сдачу делает корневая нить.
- **Остановки:** блок `## Q-P2G-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась (нет кода выхода; пустой вывод при коде выхода 0, например поиск без совпадений, — не повод для остановки).
- **Рамка правок:** только `.tmp/` рабочей папки; файлы вне неё только читать.
- **Журнал:** `.tmp/progress.md`, строка после каждого шага порядка и после каждой готовой картинки.
