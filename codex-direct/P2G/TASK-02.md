# Ответ ведущего P2G-02 — причёска ментата вместо фуражки

Владелец посмотрел выбранный экран ментата `mentat_b.png`: на голове офицера в старой картинке не фуражка, а его собственная причёска. Нужна правка только головы на `mentat_b.png`.

## Входы

| Файл | Размер | Что на нём |
|---|---|---|
| `.tmp/out/mentat_b.png` | 1536 × 1024 | выбранный экран ментата; на голове офицера ошибочно нарисована чёрная фуражка с золотым кантом |
| `.tmp/input/mentat_classic_head.png` | 880 × 640 | голова и плечи того же офицера из старой пиксельной картинки |

Перед работой сверь SHA-256 командой `sha256sum -c` по этому списку:

```text
3d4841dbb189234be34f39e1febcfa51b1801a093f9af79119dacde8534e5914  .tmp/out/mentat_b.png
dfa2f839c6c2d490599821c81aa4a03ead2989280c43f09e42f65e8dc9f6b82a  .tmp/input/mentat_classic_head.png
```

Хоть одна строка не `OK` — блок `Q-P2G-02` с выводом и стоп.

## Что сделать

Случай `hair`: вызови `image_gen.imagegen` с промптом П-hair и двумя входными изображениями: первое — `.tmp/out/mentat_b.png`, второе — `.tmp/input/mentat_classic_head.png`. Четыре попытки с одним и тем же промптом: `a`, `b`, `c`, `d`. Каждую картинку скопируй в `.tmp/out/` под именем `hair_<попытка>.png` сразу после генерации. Файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй. Файл `.tmp/out/mentat_b.png` не меняй.

Промпт — дословно, без правок и дополнений.

П-hair:

```text
Edit image 1: change only the top of the officer's head; keep everything else in image 1 unchanged.
In image 1 the officer on the left wears a black cap with a gold rim. That is wrong: in image 2, an old low-resolution pixel-art picture of the same man, the dark shape on his head is his own hair, not a hat.
Repaint the cap as his own hair: thick dark hair, black with grey streaks, combed up and back from the forehead and swept out into two wide stiff wings above the ears that curve upward at the tips, with the same outline as the shape on his head in images 1 and 2. Show real hair texture with strands and natural highlights. No gold rim, no fabric, no brim, no hat of any kind. The forehead, hairline and ears look natural under the hair.
Keep the face, expression, uniform, gold shoulder boards, chest badge, crossed arms, the background wall, the screen with the violet emblem and planet, the button plates, the black padding bars at the left and right edges, the composition and the size of the image exactly as in image 1. No text, letters, numbers, logos or watermarks.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если на ней у офицера осталась шапка или фуражка, слева нет человека или есть текст, буквы или цифры. Повторённая картинка заменяет исходную под тем же именем.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши попытку и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующей попытке.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 8.

Допиши в `.tmp/out/prompts.md` четыре строки по тем же полям, что у остальных картинок.

## Сдача

Последнее сообщение — `## DONE-P2G-02 | <время UTC из date -u>`:

- таблица: файл в `.tmp/out/` → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 четырёх итоговых файлов;
- «Отказы модерации» — попытки и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.

Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** сверка SHA-256 → четыре генерации → повторы → `prompts.md` → сдача.
- **Параллельно:** четыре генерации независимы.
- **Помощники:** один субагент `gpt-6-luna` `xhigh`, без вложенных: делает четыре попытки. В бриф дословно входят промпт, порядок входных изображений, правило копирования, правила повтора и отказа модерации и предел 8 запросов. Сверку входов, `prompts.md` и сдачу делает корневая нить.
- **Остановки:** блок `## Q-P2G-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки дважды подряд не завершилась.
- **Рамка правок:** только `.tmp/` рабочей папки; `.tmp/out/mentat_b.png` и остальные готовые файлы не меняй.
- **Журнал:** `.tmp/progress.md`, строка после каждого шага порядка и после каждой готовой картинки.
