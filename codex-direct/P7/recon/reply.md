## RECON-P7R | 2026-11-10 14:46:13 UTC

Полный отчёт с командами, выводами и восемью таблицами: [`.tmp/p7r/RECON.md`](/srv/dune/worktrees/u34/.tmp/p7r/RECON.md).

1. В `FORK1` язык хранится в `GameSettings.language`, ключ `Language` читается и записывается в ini, а переключение находится в настройках. Подробные сигнатуры и изменения относительно `BASE` — в `fork-mechanism.tsv`.
2. `localization::text` и `localization::format` встречаются в 291 вызове; найдено 252 уникальные пары RU/EN. Пофайловый вывод `git grep` и сверка с `PORT` — в `fork-calls.tsv`.
3. Инвентарь содержит 136 ресурсов localization. Сводка: 72 добавлены, 63 изменены, один удалён; загрузчики, Git/LFS и язык каждого пути — в `resources.tsv`.
4. В сборке форка используются SDL2_ttf и цель `font_coverage_tests`; в `PORT` найден SDL3_ttf, но соответствующей цели нет. Сопоставления с `PORT` — в `build.tsv`.
5. В `PORT` шрифты `arrakeen.fon`, `benegess.fon` и `small.ttf` загружаются через SDL3_ttf. Сигнатуры и изменения `BASE`→`UP1` — в `port-text.tsv`.
6. В `FORK1` пять из восьми шрифтов покрывают все 66 целевых кодовых точек; три шрифта `PORT` не покрывают ни одной. Результаты по файлам — в `fonts.tsv`.
7. Цель FORK1 — `russian_font_coverage`; статический подсчёт дал 101 логическую проверку. Вызовов функций перевода в тестах форка не найдено; подробности — в `tests.tsv`.
8. В `UP1` и `PORT` тексты кампании Сардаукаров на английском: 310 строк в брифинге и 14 в описаниях миссий. Для Атрейдес в `FORK1` найдено 262 строки RU и 346 EN. Все файлы и точки загрузки — в `campaign-texts.tsv`.

### Чтение

До работы прочитаны `PORT_PLAN.md`, заданные фрагменты `PORT_MAP.md` и строка решения Р63. По ссылкам плана также прочитаны `docs/PLAN_units_sega_upstream.md` и `codex-direct/launch-card-27.md`. Дополнительной нормы или контракта, на которые опирается разведка и которых не хватило бы после чтения этих ссылок, не обнаружено.

### Файлы `.tmp/p7r/`

`RECON.md`, `progress.md`, `fork-mechanism.tsv`, `fork-calls.tsv`, `resources.tsv`, `build.tsv`, `port-text.tsv`, `fonts.tsv`, `tests.tsv`, `campaign-texts.tsv`, `assets_recon.py`, `count_font_checks.py`, `count_pairs.py`, `count_resource_summary.py`, `count_text_rows.py`, `emit_campaign_tsv.py`, `make_calls_tsv.py`.

### Не проверено

Сборки, CTest и запуск игры не выполнялись, как требует задание. Поведение переключения языка и отрисовка кириллицы при запуске не проверялись.

### Рабочие места

Команда `python3 /srv/dune/tools/task-places.py inventory .tmp/p7r --size` вывела:

```text
path    kind    branch  head_date  size    dirty  untracked  unpushed  worktrees  procs  refs
/srv/dune/worktrees/u34/.tmp/p7r  dir  -  -  131098  -  -  -  -  0  0
```

`.tmp/p7r` — оставить: разведка для ведущего.

### git status --short

Вывод пустой. Коммитов нет; файлы вне `.tmp/p7r/` не менялись.