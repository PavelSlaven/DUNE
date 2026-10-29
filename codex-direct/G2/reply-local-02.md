## DONE-G2 | 2026-10-29 16:04:42 UTC

## PLAN-G2

- Сверить SHA-256 входов.
- Сгенерировать четыре случая по две попытки с исходными промптами и входами в заданном порядке.
- Скопировать результаты без изменения размера и записать метаданные с текстами промптов.
- Проверить итоговые файлы, размеры и SHA-256.

В `.tmp/out` сохранены восемь PNG; SHA-256 каждой копии совпадает с файлом генерации. Все восемь имеют размер `1254x1254`. [prompts.md](C:/Users/Slaven/AppData/Local/Temp/claude/C--Users-Slaven-Projects-DUNE/22d0d3cf-a572-4607-9206-d93f8c915e9c/scratchpad/codex/g2-local/work/.tmp/out/prompts.md) содержит порядок входов, номера промптов, пути источников, сведения о повторах и точные тексты П1–П4.

| Файл в `.tmp/out/` | Случай | Попытка | Промпт | Исходный файл генерации | Размер | Повтор |
|---|---|---|---|---|---|---|
| `g2_v1_k1_a.png` | v1_k1 | a | П1 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-bcfc74ae-33f9-488e-9b63-4b7247df66bb.png` | 1254x1254 | нет |
| `g2_v1_k1_b.png` | v1_k1 | b | П1 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-9583bd04-1de2-41b2-973f-9b175dd3a900.png` | 1254x1254 | нет |
| `g2_v1_k6_a.png` | v1_k6 | a | П2 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-f611f6cd-8b06-49c1-b49c-6fbb53b035ba.png` | 1254x1254 | нет |
| `g2_v1_k6_b.png` | v1_k6 | b | П2 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-4c0c48d5-659e-43c9-a9ba-b40eba71239e.png` | 1254x1254 | нет |
| `g2_v2_k1_a.png` | v2_k1 | a | П3 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-2092efdd-2290-430e-80a9-92062d04d78d.png` | 1254x1254 | нет |
| `g2_v2_k1_b.png` | v2_k1 | b | П3 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-d0f60a20-d258-4388-a0a4-6de8d07f5130.png` | 1254x1254 | нет |
| `g2_v2_k6_a.png` | v2_k6 | a | П4 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-79df2e7e-ff47-4720-bd05-d2496fd8647d.png` | 1254x1254 | нет |
| `g2_v2_k6_b.png` | v2_k6 | b | П4 | `C:\Users\Slaven\.codex\generated_images\01a1883b-6091-73d0-a6b6-de64d3259c5d\exec-117d195c-2db8-43c1-bcb7-344103f33ae9.png` | 1254x1254 | нет |

## SHA-256 итоговых файлов

- `g2_v1_k1_a.png` — `9d8809d741d57e15dcc58d6418d5c86e82562a279ff1267397b0f6ffbb5762e3`
- `g2_v1_k1_b.png` — `e26e2977f5a7292d80719e3cdb92e722538d4b1eae912754bbb638d3b4c337d9`
- `g2_v1_k6_a.png` — `edc5cf6c0402420498942b6e9f177235d9403e71989e1ea033a21aa3ba5c2b13`
- `g2_v1_k6_b.png` — `fc7c03c3ccb2878513725e99dabbc6efeb35ba1ed34af59df7e6656ffb91fe4a`
- `g2_v2_k1_a.png` — `7e836121a7bc471d572f775f8129fd40201e2d7afd63a28c054440b68569c25c`
- `g2_v2_k1_b.png` — `d9e4367733fef55184d80a87de009724f81c30de52a0faefbff5a185a4c91d6f`
- `g2_v2_k6_a.png` — `cd14d72f56532fc6b822b947adfa68d476e21476532c3cf1845651a58463c65c`
- `g2_v2_k6_b.png` — `03062d407223d7f3d9c9e06ac8eb617b0e422198b79026b6da7d3db63450c2d6`

## Не проверено

Точность ракурса, сохранность деталей и соответствие внешнего вида оригиналу не оценивались — их оценивает ведущий. У `g2_v2_k6_a.png` фон чёрный: среднее G углов равно `0.0`, ниже заданного порога повтора `100`, поэтому повтор не выполнялся.