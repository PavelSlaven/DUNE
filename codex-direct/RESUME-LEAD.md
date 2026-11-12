# Продолжение работы ведущего порта DUNE

Остановлено по слову владельца 2026-11-12 в 23:06 МСК: «Пока останови работу, потом продолжим». Этот файл — точка входа для продолжения. Сначала прочитай его целиком, потом `docs/upstream/PORT_PLAN.md` (§8) и `docs/decisions.md` (последнее — Р83).

## Роль и источники

- Сессия ведущего: ccfbda10 (CCD `local_c0bb2f33-c96e-4e43-9bde-bc657f789b83`). Роль — ведущий порта DUNE; ведёт и задачу «Интерфейс игры» (Р74).
- Процесс — навык `team-process-claude` (`~/.claude/skills/team-process-claude`; скрипты `tools/check-literal.py`, `tools/check-reads.py`).
- План — `docs/upstream/PORT_PLAN.md`, ветка `docs/p5` (только локальная, без `origin`). После правки §8 — `scp` на `servak:/srv/dune/tasks/load-check/PORT_PLAN.md`.
- Память проекта: `dune-project-map.md`, `dune-servak.md` (известные ложные FAIL проверки входа Codex, сборка, LFS).

## Что остановлено и как было

| Что | Состояние |
|---|---|
| Нить П13 (Codex sol, основной аккаунт) | убита ведущим по PID в 23:06 МСК; `status` = `finished=2026-11-12T20:06:54Z code=143`; процессов не осталось |
| Ожидатель `b311zz486` | снят |
| Cron надзора `6eb1d1fd` и таймер кэша `711145c7` | удалены |
| acct2 | задач нет |

## П13 — где остановилась нить

- Задание: `/srv/dune/tasks/p13/task.md` (= `codex-direct/P13/TASK-P13.md`; вопросы и ответы — `codex-direct/P13/QUESTIONS-P13.md`; пересказ сверен — `codex-direct/P13/lead/p13-retell-reply.md`).
- Рабочая копия: `/srv/library/dune/worktrees/p13`, ветка `codex/p13` от `0683500a8` (вершина порта после П12). Коммитов нет.
- Session id нити: `01a1d14d-7ec3-7630-9a6f-bf7e837c05a9` (строка `session id:` в `/srv/dune/tasks/p13/reply.txt.run.log`).
- Журнал хода: `/srv/library/dune/worktrees/p13/.tmp/p13/progress.md`.
- Сделано: шаги 1–4 закрыты (тесты 25 методов, красный прогон, `reference_shots.py`, оба TSV побайтно). Шаг 5: проверка 1 (сборка exit 0, CTest 476/476), проверка 2 (25 новых тестов OK, весь набор 258 OK), проверка 3 (каталоги: 0/0/0 отсутствующих, 192 сцены порта) — пройдены.
- Прервано: проверка 4 — серверный прогон `reference_shots.py --no-old --headless --language ru` в `.tmp/p13/ref` (успели 14 из 31 PNG). Проверки 5 (галерея `--gallery --language en`) и 6 (команда для Windows в сдаче) не сделаны.
- Новые файлы в рабочей копии (`git status`): `tools/ui-audit/reference_shots.py`, `tools/ui-audit/reference_pairs.tsv`, `tools/ui-audit/reference_gallery.tsv`, `tools/ui-audit/tests/test_reference_shots.py`.

### Как продолжить П13

1. Лимиты Claude и Codex числами; `df -m /srv` и `/srv/library` (стоп при < 5000 МБ на `/srv`).
2. Ответ нити файлом `task-01.md` (LF): «Прогон остановил ведущий. Продолжи с проверки 4 шага 5 заново, вывод — в новую папку `.tmp/p13/ref2` (старую `.tmp/p13/ref` не трогай: `rm` в песочнице запрещён), затем проверки 5 и 6 и сдача `## DONE-P13`». Загрузить его на servak в `/srv/dune/tasks/p13/` и отдельным ssh-вызовом:
   `bash /srv/dune/tasks/resume-sol.sh p13 /srv/library/dune/worktrees/p13 01a1d14d-7ec3-7630-9a6f-bf7e837c05a9 01`
3. Поставить ожидатель (фоновый ssh-цикл по `/srv/dune/tasks/p13/status` с маркером mtime) и cron надзора по тексту «Надзор DUNE (ведущий)…» (см. ниже).
4. После `DONE-P13` — порядок приёмки:
   - проверка входа Codex: t-задание sha = файлу задания; ложные FAIL — `dune-servak.md` (в т.ч. `<turn_aborted>` от этой остановки);
   - check-reads по образцу `codex-direct/P13/lead/p12-templates/reads.sh`: base = `git archive 0683500a` + `fork/` из `9208dcf5a`; скрипт `/srv/dune/tasks/load-check/check-reads.py` на servak; диапазоны обрезать по длине файла;
   - дифф против контракта задания;
   - коммиты на servak группами исполнителя: PATH git-lfs, `-c lfs.storage=.tmp/p13/lfs`, user `PavelSlaven` / `55245062+PavelSlaven@users.noreply.github.com`, сообщение `-F` файлом, последняя строка `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (образцы — `p12-templates/mkmsg.py`, `commit.sh`);
   - перенос через `C:\Users\Slaven\Projects\DUNE-p2`: `git switch --detach`; `git fetch servak:/srv/library/dune/worktrees/p13 codex/p13:codex/p13`; `git push origin codex/p13`;
   - PR в `port/up-d06f2fcd` (тело по образцу `p12-templates/pr.md`, последняя строка `🤖 Generated with [Claude Code](https://claude.com/claude-code)`), `bind_pr`;
   - слияние после зелёного CI: `gh pr merge N --repo PavelSlaven/DUNE --merge --match-head-commit <полный sha>`;
   - затем `rm -r .tmp/out/logs/*/previous-run` в рабочей копии p13.
5. Затем прогон на Windows (исполнитель Sonnet по брифу, образец `codex-direct/P13/lead/p10c-templates/win-brief.md`): старая сборка — свежая распаковка выпуска `v0.8.0-ru-hd.10` (`Language=ru`, `RenderScale=0`), новая — сборка порта; `preferences.ini` пользователя в `%APPDATA%\D2TM\Dune II - The Maker\` сохранить и вернуть, на время прогона `RenderScale`/`WorldScale` = 0. Команда — из сдачи П13. Разбор отличий «старое | новое» — ведущий.
6. Выбор пяти новых снимков галереи (`docs/screenshots/`: `house-selection`, `main-menu`, `ordos-briefing`, `skirmish-gameplay`, `victory-screen`) и правка подписей `README.md` (Р83) — ведущий после осмотра.

## Дальше по плану

- П14 — догоняющий merge апстрима, связывание истории, перемотка `main`; перед перемоткой — приёмка владельца в игре.
- П15 — `docs/UPSTREAM_SYNC.md`, `tools/upstream_sync_report.py`.
- Релиз — номер решает владелец.

## Брифы и шаблоны (копии из временной папки сессии)

- `codex-direct/P13/lead/common3.md` — общая часть брифа черновика (уроки дня, clang на macOS `-Wunused-lambda-capture`); `step-P13.md` — бриф шага П13.
- `codex-direct/P13/lead/p12-templates/` — check-reads, сообщения коммитов, коммит на servak, тело PR.
- `codex-direct/P13/lead/p10c-templates/` — бриф прогона на Windows, `mkwin.py`, проверка слияния.

## Таймеры при продолжении

- Cron надзора раз в 30 минут (не на :00/:30), текст дословно: «Надзор DUNE (ведущий). Одна ssh-проверка на servak: `/usr/bin/python3 /srv/dune/tools/codex-load-check.py --config /srv/dune/tasks/load-check/config.json; echo exit=$?` (0 — норма, 3 — сигналы, 2 — ошибка конфига), живые прогоны `pgrep -af "[c]odex-exec.sh"`, свободное место `df -m /srv` (стоп при < 5000 МБ). Сигнал разобрать в том же ходе по fleet.md «Проверка загрузки Codex»: дробить план, запускать готовое, поправить нить; сигнал 4а при прогоне, который ждёт моего плана или ответа, — это мой простой: ответить. Владельцу 2–4 строки только при изменении; без изменений — одна строка. Прогонов DUNE нет и ждать нечего — cron удалить.»
- Таймер кэша — одноразовый, через ~58 минут, не на :00/:30, текст «обновление кэша, действий не требуется», ответ одной строкой; цепочкой.
- Сигналы надзора: 1б/4а у acct2 — простой малого аккаунта, задач нет; 4б у sol в фазе чтения — норма.

## Лимиты (снимок 2026-11-12 ~23:25)

- Claude неделя 88 %, Fable 96 %, сброс 15.11 в 19:59 МСК. Беречь: черновики — только Sonnet, Opus — приёмка; новых разведок без нужды не заводить.
- Codex: sol-аккаунт (`/srv/novgorod-work/codex-direct/home`) 28 % на ~19:45, acct2 18 %.
- Свободно `/srv` 6,6 ГБ.

## Открытые вопросы владельцу

- Отзыв о переводе Сардаукаров (`codex-direct/P7/ru/SARDAUKAR-READ.md`) и о таблице слов П7б.
- «Раньше/Дальше» в стычке.
- Замечания вида окна настроек П10в (активная вкладка не выделена, подписи выше кнопок) — в переработку интерфейса (ИФ). Сессию Fable `local_39cdbc6b` не архивировать без «да» владельца.
- Открытые issue: #133–#135, #137.

## Запреты владельца

- Ветки — только через `DUNE-p2`; `gh` всегда с `--repo PavelSlaven/DUNE`.
- CI не опрашивать: статус — `get_status` или один `gh pr checks` на событие; слияние вручную после зелёного CI.
- Novgorod не трогать; пакеты не ставить; сборки с `CCACHE_DISABLE=1`, на HDD `/srv/library/dune`.
- Абзац о комментариях — дословно в каждый бриф; не больше 3 помощников на нить.
- После приёмки удалять `previous-run`.
- С владельцем — пещерный русский; Python-скрипты — через Write, не heredoc Bash.
