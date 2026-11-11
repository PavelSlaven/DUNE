# Замеры интерфейса «до»

Инструмент: `codex-direct/ui-redesign/tools/measure_ui.py` (`--selftest` напечатал `selftest ok`).
Обработаны сочетания: `1024x768/en/hd` (108 PNG) и `1920x1080/en/hd/r100w0` (108 PNG). Сочетание `1920x1080/en/hd` на момент запуска: 0 PNG и 0 журналов, не обработано.

Команда (для каждого сочетания C, T = C с `_` вместо `/`):
`python -X utf8 -B measure_ui.py --logs .cache/ui-redesign/before/logs/C --png .cache/ui-redesign/before/png/C --out .cache/ui-redesign/before/measure/T.tsv`
TSV и сводки: `.cache/ui-redesign/before/measure/T.tsv`, `T.summary.txt`.

Замечание: самые низкие контрасты (1.06-1.9) дают записи `text` из одних пробелов (mentat speak/win), это артефакт журнала, а не читаемый текст; по спецификации они учтены. Среди «настоящих» строк минимум 2.62 (`Startpoints: 4`, skirmish-setup-ready-map) и 4.51 (`Apply`, options-menu-applied).

## Сводка 1024x768/en/hd
```
scenes: 108
text records: 571
min text height: 10
5 smallest text:
  mentat-briefing-atreides-await	'Mission select'	10
  mentat-briefing-atreides-speak	'Mission select'	10
  mentat-briefing-harkonnen-await	'Mission select'	10
  mentat-briefing-harkonnen-speak	'Mission select'	10
  mentat-briefing-ordos-await	'Mission select'	10
click records: 284
min click side: 15
5 smallest click:
  mentat-briefing-atreides-await	GuiButton:Mission select	101x15
  mentat-briefing-atreides-speak	GuiButton:Mission select	101x15
  mentat-briefing-harkonnen-await	GuiButton:Mission select	101x15
  mentat-briefing-harkonnen-speak	GuiButton:Mission select	101x15
  mentat-briefing-ordos-await	GuiButton:Mission select	101x15
contrast records: 571
contrast min: 1.06  p5: 9.85  median: 13.63
contrast < 4.5: 9  < 3.0: 9
10 lowest contrast:
  mentat-win-sardaukar-speak	'        '	1.06
  mentat-win-sardaukar-speak	'        '	1.08
  mentat-briefing-sardaukar-speak	'                       '	1.11
  mentat-briefing-sardaukar-speak	'                       '	1.15
  mentat-briefing-atreides-speak	'                       '	1.30
  mentat-briefing-atreides-speak	'                       '	1.31
  mentat-win-atreides-speak	'        '	1.92
  mentat-win-atreides-speak	'        '	1.94
  skirmish-setup-ready-map	'Startpoints: 4'	2.62
  options-menu-applied	'Apply'	4.51
```

## Сводка 1920x1080/en/hd/r100w0
```
scenes: 108
text records: 680
min text height: 10
5 smallest text:
  mentat-briefing-atreides-await	'Mission select'	10
  mentat-briefing-atreides-speak	'Mission select'	10
  mentat-briefing-harkonnen-await	'Mission select'	10
  mentat-briefing-harkonnen-speak	'Mission select'	10
  mentat-briefing-ordos-await	'Mission select'	10
click records: 348
min click side: 15
5 smallest click:
  mentat-briefing-atreides-await	GuiButton:Mission select	101x15
  mentat-briefing-atreides-speak	GuiButton:Mission select	101x15
  mentat-briefing-harkonnen-await	GuiButton:Mission select	101x15
  mentat-briefing-harkonnen-speak	GuiButton:Mission select	101x15
  mentat-briefing-ordos-await	GuiButton:Mission select	101x15
contrast records: 680
contrast min: 1.11  p5: 9.86  median: 16.65
contrast < 4.5: 9  < 3.0: 9
10 lowest contrast:
  mentat-win-sardaukar-speak	'        '	1.11
  mentat-win-sardaukar-speak	'        '	1.12
  mentat-briefing-sardaukar-speak	'                       '	1.24
  mentat-briefing-sardaukar-speak	'                       '	1.25
  mentat-briefing-atreides-speak	'                       '	1.47
  mentat-briefing-atreides-speak	'                       '	1.49
  mentat-win-atreides-speak	'        '	2.46
  mentat-win-atreides-speak	'        '	2.53
  skirmish-setup-ready-map	'Startpoints: 4'	2.62
  options-menu-applied	'Apply'	4.51
```

## Проверки наложений (скрипты tools/ui-audit, вывод в `.cache/ui-redesign/before/checks/<скрипт>-<T>.txt`)

| скрипт | сочетание | код возврата | число проблем | главное |
|---|---|---|---|---|
| check_geometry | 1024x768/en/hd | 0 | 52 флага | rule 4 (текст на тексте): 34, rule 9 (зоны нажатия): 18; сцены credits-*, mentat-*-speak, tellhouse-*; rule 9: credits-speed-up (0,0 800x600) перекрывает GuiButton:Back |
| check_geometry | 1920x1080/en/hd/r100w0 | 0 | 52 флага | те же 34 + 18, те же сцены |
| check_options_geometry | 1024x768/en/hd | 1 | 0 флагов, расхождение с планом | logs 1, planned 3; нет options-game-main-nosaves, options-game-main-saves; rule 3 и 9: 0 |
| check_options_geometry | 1920x1080/en/hd/r100w0 | 1 | 0 флагов, расхождение с планом | то же |
| check_scenes | 1024x768/en/hd | 1 | 0 | scenes checked: 0 (скрипт не нашёл ни одной проверяемой сцены; код 1 из-за пустого результата) |
| check_scenes | 1920x1080/en/hd/r100w0 | 1 | 0 | то же |
| check_screens | 1024x768/en/hd | 1 | 16 | «no scene and no exclusion» для GAME_PLAYING, GAME_EDITOR, GAME_WINNING, GAME_LOSING, GAME_NEW_MAP_EDITOR, GAME_SCORING, GAME_VIDEO, cCreatorState, cEditorState, cGamePlaying, cMentatState, cNewMapEditorState, cScoringState, cTellHouseState, cVideoState, cWinLoseState |
| check_screens | 1920x1080/en/hd/r100w0 | 1 | 16 | те же 16 |
| check_completeness | 1024x768/en/hd | 0 | 0 | OK |
| check_completeness | 1920x1080/en/hd/r100w0 | 1 | 82 | все 82 строки `extra-png` (лишние PNG: для не-legacy сочетания скрипт ждёт PNG только у сцен с флагами), пропавших файлов нет |
| check_credits | 1024x768/en/hd | 0 | 0 | OK |
| check_credits | 1920x1080/en/hd/r100w0 | 0 | 0 | OK |

Как подавались входы: check_geometry с `--json` (флаги в `checks/geometry-flags-T.json`); check_options_geometry с `--combos checks/combos-T.txt` (одна строка C); check_completeness с `--flags` из check_geometry и `--order checks/order-T.json` (только обработанное сочетание); check_screens с `--catalog before/catalog.json --root W --exclusions tools/ui-audit/exclusions.tsv`; check_scenes и check_credits — на папке журналов сочетания.

## Каких входов не хватило

- Полного списка сочетаний (`run_all.py` order/plan) нет: `--order` и `--combos` составлены только из двух обработанных сочетаний, поэтому вывод check_completeness для r100w0 и check_options_geometry зависит от этого урезания.
- В снимках нет сцен options-game-main-nosaves и options-game-main-saves (ожидаются check_options_geometry).
- check_screens работал по дереву исходников из W (оно есть); 16 «проблем» — состояния, у которых нет сцены в catalog.json и нет строки в exclusions.tsv: либо каталог неполон, либо нужны исключения; решение не принималось.
- Сочетание `1920x1080/en/hd` не снято к моменту запуска, замеров и проверок по нему нет.
