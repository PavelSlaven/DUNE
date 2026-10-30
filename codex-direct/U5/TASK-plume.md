# Задание U5-plume — песчаный шлейф Харвестера под 63°: ряды 1–3

Режим: **«Ведёт sol»** (см. «Режимы задания» в конце). Исполнитель: Codex `gpt-6.1-sol` `high` с инструментом генерации изображений `image_gen.imagegen`; генерации — субагентам `gpt-6-luna` `xhigh`.
Рабочая копия: `/srv/dune/worktrees/u5`, ветка `codex/u5`. Коммитов не делай: результат — файлы в `.tmp/out-plume/` и сдача. План работ: `docs/units/REDRAW_PLAN.md`, фаза U5.

## Цель

Получить 48 картинок: новый Харвестер под 63° с песчаным шлейфом сбора спайса, восемь направлений × три кадра анимации, по две попытки на кадр. Облик и выбор попыток оценивает ведущий, не ты.

## Входы

Папка `.tmp/input-plume/` рабочей копии. Все файлы — 1024 × 1024, фон сплошной пурпурный RGB (255, 0, 255). `harvester_pick_k<k>.png` — новый Харвестер под 63° без песка, направление k; `harvester_old_r<r>k<k>.png` — старый спрайт Харвестера из игры, камера 36°, во время сбора спайса: из задней части сыплется песок, кадр анимации r = 1, 2, 3. Направления k0…k7: восток, северо-восток, север, северо-запад, запад, юго-запад, юг, юго-восток.

Перед работой сверь SHA-256 входов с этим списком командой `sha256sum -c`. При расхождении — `Q-U5-plume-01` и стоп.

```text
3d51a9a0ec7f064189cbe6a797970e14ebadffd597b0b62c5b6b7b9091b2f6cb  .tmp/input-plume/harvester_old_r1k0.png
90a59b6c88e06154df7f0940281e7ad7b5b2ec1b750588bf813f8190177c0fdb  .tmp/input-plume/harvester_old_r1k1.png
79ab0dc476394f0fffe4d9aa917ce4b1017c1d696ae8e969a15a83106b1b4021  .tmp/input-plume/harvester_old_r1k2.png
7dd59fc94da56f77958394a86a236f6925a09fa833caee2e50ae6cc20683a31a  .tmp/input-plume/harvester_old_r1k3.png
11d42691d4c6d22e4ea320344a9024ea22c80e93a94c7c4415d49a5018382a65  .tmp/input-plume/harvester_old_r1k4.png
0662fae07c8ab6622505b99a86cd201090598a78445d4abadb44259256b96455  .tmp/input-plume/harvester_old_r1k5.png
6cc10d68e3fb2b3145c5fbf856c7a85ff4d70b764bbd10252889e177a6a760aa  .tmp/input-plume/harvester_old_r1k6.png
270be4033baa35a7792bb36b8ecf8434e801ff5f7b6f06ff8ea1ec37550d0142  .tmp/input-plume/harvester_old_r1k7.png
22078b970ddd135c57cf3b6d58c2df19d16e46c90aeba24a5451184e4e621b81  .tmp/input-plume/harvester_old_r2k0.png
2f0fc9c8fb78c5b2a05eb9fe5cccc21e673958c57e8ce4d031bcec22fccaf468  .tmp/input-plume/harvester_old_r2k1.png
6963e1bb94d114f0bc836bedccfbe75eba17b2c3947c7a69ef61abf04f35967f  .tmp/input-plume/harvester_old_r2k2.png
3ee7f77ecf63c590715e0468525ce973288db5a2ceb86cbcf7aa02ebceff9e4b  .tmp/input-plume/harvester_old_r2k3.png
e5b05696b13644dec3eb30258cd681ab580f0d6609f8ac2acbe08967eab01d56  .tmp/input-plume/harvester_old_r2k4.png
d64af621da20c0ba793cfc016441c9f0ece8306032f9d99acfa494fce85d105c  .tmp/input-plume/harvester_old_r2k5.png
558a2c248b094df11c9510ebebc3f9f9784cf6e5b287916cadd22b24de3983c9  .tmp/input-plume/harvester_old_r2k6.png
194d0b969b49a173261726747fd7845eb4a5d3979277e6a3e52176e1d0a4c192  .tmp/input-plume/harvester_old_r2k7.png
cf21d79027fb54757d72ee1342f539ed84e206f52f7ac1b0a1502586fcf115ca  .tmp/input-plume/harvester_old_r3k0.png
a518f9744291d7055408df67f6484006ea207cdb67f97826e1bcbbce2d4a7022  .tmp/input-plume/harvester_old_r3k1.png
910420dcc5fa9ca80245737108cce461d990474342a0fd42b670ec818f9e061e  .tmp/input-plume/harvester_old_r3k2.png
18368149768a1ad1c86f941e0f72c6a0f71d355bd36bb0472f61686570403bf0  .tmp/input-plume/harvester_old_r3k3.png
8dbcfcbc5915a6989bbce4bba3da11d93dba498393a66a1e127b48af913b45ba  .tmp/input-plume/harvester_old_r3k4.png
1699ebc9159b03a85649ff3ab43d9ab6a8f6268debd31c8e12084011acfd03ca  .tmp/input-plume/harvester_old_r3k5.png
effb026b84e8fadd4457436175b15c9044ec6d1d08089f1add0645590a9b2e2b  .tmp/input-plume/harvester_old_r3k6.png
6856e2b0be30b7d990dc1ccd4eccc6066692436094789bc41b5c14fc982a6b58  .tmp/input-plume/harvester_old_r3k7.png
af28a2fafcb4d6bfbcd008de1c76942beda3fb71444a665c1927b1c346c94777  .tmp/input-plume/harvester_pick_k0.png
73824148cf6e6be3f5676944212e5640ccade5595107c89b2dcf45fe5ed86c48  .tmp/input-plume/harvester_pick_k1.png
802994683cbfaaa1d7cd2f91d9df27d0610f077d680397dcf91fedd8282ce607  .tmp/input-plume/harvester_pick_k2.png
66ba09efe80a651f011603968ebd317e634a295697aa70e283175310522cf724  .tmp/input-plume/harvester_pick_k3.png
9a567a49c3a679c29024cf27a39662c9a1a58bdaf9e6beee6ee971642432ffb8  .tmp/input-plume/harvester_pick_k4.png
7c18f1f3f4c79d7191d360e7e56ffd5bee9bbbfe9d6e9907867f8c3cf58e52ea  .tmp/input-plume/harvester_pick_k5.png
ea9918083ba0c14b708732e948915a88618b9cedbd641c70c6a6b2080d4214be  .tmp/input-plume/harvester_pick_k6.png
7d0fd60df432dd989e81b7fcaff39eaa2e30b9ce8fe4bdac6b6a24930612b2e9  .tmp/input-plume/harvester_pick_k7.png
```

## Что сделать

24 случая — таблица ниже. Для каждого случая вызови `image_gen.imagegen` с промптом случая и двумя входными изображениями в указанном порядке. Сделай две попытки с одним и тем же промптом: попытки `a` и `b`. Каждую картинку скопируй в `.tmp/out-plume/` под именем `<случай>_<попытка>.png`, например `plume_r1k0_a.png`, сразу после генерации; файл копируй как есть, размер не меняй, исходный файл в `generated_images` не удаляй.

| Случай | Первое изображение | Второе изображение | Промпт | Направление и кадр |
|---|---|---|---|---|
| `plume_r1k0` | `harvester_pick_k0.png` | `harvester_old_r1k0.png` | П-plume-0 | восток, кадр 1 |
| `plume_r2k0` | `harvester_pick_k0.png` | `harvester_old_r2k0.png` | П-plume-0 | восток, кадр 2 |
| `plume_r3k0` | `harvester_pick_k0.png` | `harvester_old_r3k0.png` | П-plume-0 | восток, кадр 3 |
| `plume_r1k1` | `harvester_pick_k1.png` | `harvester_old_r1k1.png` | П-plume-1 | северо-восток, кадр 1 |
| `plume_r2k1` | `harvester_pick_k1.png` | `harvester_old_r2k1.png` | П-plume-1 | северо-восток, кадр 2 |
| `plume_r3k1` | `harvester_pick_k1.png` | `harvester_old_r3k1.png` | П-plume-1 | северо-восток, кадр 3 |
| `plume_r1k2` | `harvester_pick_k2.png` | `harvester_old_r1k2.png` | П-plume-2 | север, кадр 1 |
| `plume_r2k2` | `harvester_pick_k2.png` | `harvester_old_r2k2.png` | П-plume-2 | север, кадр 2 |
| `plume_r3k2` | `harvester_pick_k2.png` | `harvester_old_r3k2.png` | П-plume-2 | север, кадр 3 |
| `plume_r1k3` | `harvester_pick_k3.png` | `harvester_old_r1k3.png` | П-plume-3 | северо-запад, кадр 1 |
| `plume_r2k3` | `harvester_pick_k3.png` | `harvester_old_r2k3.png` | П-plume-3 | северо-запад, кадр 2 |
| `plume_r3k3` | `harvester_pick_k3.png` | `harvester_old_r3k3.png` | П-plume-3 | северо-запад, кадр 3 |
| `plume_r1k4` | `harvester_pick_k4.png` | `harvester_old_r1k4.png` | П-plume-4 | запад, кадр 1 |
| `plume_r2k4` | `harvester_pick_k4.png` | `harvester_old_r2k4.png` | П-plume-4 | запад, кадр 2 |
| `plume_r3k4` | `harvester_pick_k4.png` | `harvester_old_r3k4.png` | П-plume-4 | запад, кадр 3 |
| `plume_r1k5` | `harvester_pick_k5.png` | `harvester_old_r1k5.png` | П-plume-5 | юго-запад, кадр 1 |
| `plume_r2k5` | `harvester_pick_k5.png` | `harvester_old_r2k5.png` | П-plume-5 | юго-запад, кадр 2 |
| `plume_r3k5` | `harvester_pick_k5.png` | `harvester_old_r3k5.png` | П-plume-5 | юго-запад, кадр 3 |
| `plume_r1k6` | `harvester_pick_k6.png` | `harvester_old_r1k6.png` | П-plume-6 | юг, кадр 1 |
| `plume_r2k6` | `harvester_pick_k6.png` | `harvester_old_r2k6.png` | П-plume-6 | юг, кадр 2 |
| `plume_r3k6` | `harvester_pick_k6.png` | `harvester_old_r3k6.png` | П-plume-6 | юг, кадр 3 |
| `plume_r1k7` | `harvester_pick_k7.png` | `harvester_old_r1k7.png` | П-plume-7 | юго-восток, кадр 1 |
| `plume_r2k7` | `harvester_pick_k7.png` | `harvester_old_r2k7.png` | П-plume-7 | юго-восток, кадр 2 |
| `plume_r3k7` | `harvester_pick_k7.png` | `harvester_old_r3k7.png` | П-plume-7 | юго-восток, кадр 3 |

Промпты — дословно, без правок и дополнений; промпт случая — по направлению k, общий для трёх кадров.

П-plume-0:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points to the left. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-1:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points down and to the left. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-2:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points straight down, towards the viewer. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-3:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points down and to the right. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-4:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points to the right. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-5:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points up and to the right. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-6:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points straight up, away from the viewer. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

П-plume-7:

```text
Edit image 1. Image 1 is a sprite of a tracked harvester vehicle from a real-time strategy game, seen from a high camera, on a flat magenta background. Image 2 shows the same harvester from a lower camera while it is harvesting: a stream of sand pours out of its back end and falls to the ground.
Add to image 1 the same stream of sand pouring out of the back end of the harvester, shaped and sized as in image 2 but seen from the higher camera of image 1. The back end of the harvester in image 1 points up and to the left. Keep the harvester in image 1 exactly as it is: do not move, resize, recolour or redraw it. The sand is loose light tan sand and dust in the colours of image 2, with soft uneven edges.
Keep the background flat pure magenta RGB 255,0,255 everywhere else. No ground, no cast shadow, no glow, no text, letters, numbers, logos or watermarks.
```

**Повтор.** Картинку можно повторить один раз тем же промптом, только если выход нарушает одно из правил:
- на картинке нет Харвестера или их больше одного;
- песка мало: пикселей с R ≥ 150, 90 ≤ G ≤ 215, B ≤ 170, R − B ≥ 50, G < R − 15 и G > B + 20 меньше 5000 (считай скриптом `/srv/dune/venv/bin/python`);
- на картинке есть земля;
- Харвестер обрезан краем картинки;
- на картинке есть текст, буквы или цифры;
- фон не пурпурный: среднее четырёх угловых пикселей не удовлетворяет всем трём условиям R ≥ 150, B ≥ 150, G ≤ 100.
Неточный пурпурный фон — не повод для повтора.

**Отказ модерации.** Генератор вернул `moderation_blocked` — повтори ту же генерацию тем же промптом, не больше двух раз. Отказал три раза подряд — запиши случай и `request_id` в журнал и в раздел сдачи «Отказы модерации», иди к следующим случаям. Отказ модерации не останавливает работу.

**Предел генераций.** Всего запросов к генератору — вместе с повторами и отказами модерации — не больше 64. Предел исчерпан, а случаи остались — перечисли их в сдаче и сдавай.

Запиши `.tmp/out-plume/prompts.md`: по каждой итоговой картинке — имя, входные файлы в порядке подачи, номер промпта, фактический размер, путь исходного файла генерации, повтор (нет или причина).

## Сдача

Последнее сообщение — `## DONE-U5-plume | <время UTC из date -u>`:
- `## PLAN-U5-plume` для записи: шаги по порядку и кто их делал;
- таблица: файл в `.tmp/out-plume/` → случай → путь исходного файла генерации → фактический размер → повтор (нет или причина);
- SHA-256 48 итоговых файлов;
- «Отказы модерации» — случаи и `request_id` или «нет»;
- **Не проверено** — раздел обязателен; пустой — только с пояснением.
Оценку облика не делай. Числа в сдаче — только из вывода команд.

## Организация работы

- Порядок: сверка SHA-256 входов → 48 генераций → повторы → `prompts.md` → сдача.
- Параллельно: все генерации независимы друг от друга.
- Помощники: субагенты `gpt-6-luna` `xhigh` делают генерации сразу, по 4 одновременно, пока случаи не кончатся; каждому — свой список случаев: два направления, все три кадра каждого; в бриф — промпты дословно, правило копирования, правила повтора и отказа модерации.
- Остановки — блок `## Q-U5-plume-NN` и стоп: SHA-256 входов не совпал; `image_gen.imagegen` недоступен или не принимает входные изображения; команда оболочки не вернула вывод дважды подряд.
- Рамка правок: только `.tmp/` рабочей копии; файлы вне неё только читать.
- Журнал: `.tmp/progress-plume.md`, строка после каждого шага порядка и после каждого готового субагента.
