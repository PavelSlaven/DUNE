## PLAN-G3a

1. Сверить SHA-256 входных изображений.
2. Создать две попытки для каждого направления с указанными промптами и входами.
3. Проверить условия повтора, скопировать изображения и записать `prompts.md`.
4. Проверить размеры и SHA-256 итоговых файлов.

## DONE-G3a | 2026-10-29 16:59:39 UTC

SHA-256 всех входов совпали с заданным списком. В `.tmp/out/` записаны 12 изображений; каждый файл побайтно совпадает с указанным исходником генерации. Фактический размер всех PNG — 1254×1254.

| Файл | Случай | Попытка | Путь исходного файла генерации | Размер | Повтор |
|---|---|---|---|---|---|
| `.tmp/out/g3_k0_a.png` | k0 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-33be8655-7faf-4fdb-853d-a336962a65a9.png` | 1254×1254 | нет |
| `.tmp/out/g3_k0_b.png` | k0 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-05d1a83a-1fc0-43b7-a76b-27439359a771.png` | 1254×1254 | нет |
| `.tmp/out/g3_k2_a.png` | k2 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-b5ad436c-1474-449e-9235-f650ca9266db.png` | 1254×1254 | нет |
| `.tmp/out/g3_k2_b.png` | k2 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-1b60c19f-80b5-43a7-beb5-79f684b91816.png` | 1254×1254 | нет |
| `.tmp/out/g3_k3_a.png` | k3 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-e518f3f7-4ebc-407e-baca-0faf0552d4cc.png` | 1254×1254 | да: исходный фон не прошёл порог угловых пикселей; среднее RGB — (0, 0, 0) |
| `.tmp/out/g3_k3_b.png` | k3 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-d13464e6-c4b3-4388-a203-b4400a0bc464.png` | 1254×1254 | нет |
| `.tmp/out/g3_k4_a.png` | k4 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-6ac5fa77-91e9-4866-b6f3-6e1095c59f39.png` | 1254×1254 | нет |
| `.tmp/out/g3_k4_b.png` | k4 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-3b35f746-9246-433e-b175-621164c0dacb.png` | 1254×1254 | нет |
| `.tmp/out/g3_k5_a.png` | k5 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-b5073821-81c4-4ec7-becb-34fa36738f42.png` | 1254×1254 | нет |
| `.tmp/out/g3_k5_b.png` | k5 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-cda0a0a0-c88e-4d11-b696-b2db4ae9f2b4.png` | 1254×1254 | нет |
| `.tmp/out/g3_k7_a.png` | k7 | a | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-a9d07721-e10a-48cc-b442-b32620f1ab07.png` | 1254×1254 | да: исходный фон не прошёл порог угловых пикселей; среднее RGB — (0, 0, 0) |
| `.tmp/out/g3_k7_b.png` | k7 | b | `C:\Users\Slaven\.codex\generated_images\01a18875-eaf1-7fb1-a327-e25dc3fb8187\exec-6fc9ee67-a0e2-4114-992b-76934bfd8497.png` | 1254×1254 | нет |

### SHA-256 итоговых файлов

```text
23b066e0086d63ab49b80525e19ea00b1c3ef8c640af4e241a67179ed1525c21  .tmp/out/g3_k0_a.png
dcc0462bae4fdaceaccdc846bbc1d546b5b9bf560bd749ba3290f97fb02b7870  .tmp/out/g3_k0_b.png
447e6b742f32f94a0ae8f1783972aa292c9c0878a991ae948bc5a9bac20aa579  .tmp/out/g3_k2_a.png
715e8482691cd2483bdc04ceea58c879b4983a63fb9be385d3907b59aad3ec8c  .tmp/out/g3_k2_b.png
b2d5428a7135c0511ecfc77228d70ac4dd3c81b5e3b7a446e493e1ff047608f7  .tmp/out/g3_k3_a.png
c192d14223560c44649c51925e4f29e140a94f2b4dc255180fc65d0b694c099c  .tmp/out/g3_k3_b.png
33aabcf9731c9a613ea31d891dcfa2bfcaaacf034d4f9cdfe6a0bad5527d824e  .tmp/out/g3_k4_a.png
5e38e4ed32fb53b783919815327a9fe3c22513bff55b0de4156d41842a40762d  .tmp/out/g3_k4_b.png
f9d2bda0c5c2798a3d49d046a294b461572921a51fe8affbabb9a3490aeaf20a  .tmp/out/g3_k5_a.png
115939800ca1bda8244ec369b263c0dae4bdb053c9ae8cbad9df63c4b34986ac  .tmp/out/g3_k5_b.png
634dad3cc804a2a3edce331ca759e034f01cd041606da2773a79ff57ba84e38e  .tmp/out/g3_k7_a.png
40e9b5ed4f0cc63bc6e7a3f567254c622cf00cbb392555bfdd14c3a3931df022  .tmp/out/g3_k7_b.png
```

Промпты, входы, размеры, пути источников и причины повторов записаны в [`.tmp/out/prompts.md`](</C:/Users/Slaven/AppData/Local/Temp/claude/C--Users-Slaven-Projects-DUNE/22d0d3cf-a572-4607-9206-d93f8c915e9c/scratchpad/codex/g3a-local/work/.tmp/out/prompts.md>). Журнал работы: [`.tmp/progress.md`](</C:/Users/Slaven/AppData/Local/Temp/claude/C--Users-Slaven-Projects-DUNE/22d0d3cf-a572-4607-9206-d93f8c915e9c/scratchpad/codex/g3a-local/work/.tmp/progress.md>).

## Не проверено

Художественное сходство и качество облика не оценивались. Пурпурный цвет всего фона по каждому пикселю не измерялся; числовое условие повтора проверено по среднему четырёх угловых пикселей.