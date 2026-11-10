## RECON-P11R | Tue Nov 10 18:10:11 UTC 2026

Полный отчёт: [`.tmp/p11r/RECON.md`](/srv/dune/worktrees/u13g/.tmp/p11r/RECON.md).

- **Пункт 1:** В FORK1 найдены 28 подходящих функций ментатов; имена сцен и подсчёты записей HD4 приведены в [fork-mentat.tsv](/srv/dune/worktrees/u13g/.tmp/p11r/fork-mentat.tsv).
- **Пункт 2:** В PORT описаны 24 функции и 64 участка diff; формулы кадров, прямоугольники, файлы и записи перечислены в [port-mentat.tsv](/srv/dune/worktrees/u13g/.tmp/p11r/port-mentat.tsv).
- **Пункт 3:** Для титров указаны девять методов в каждой ревизии и 2 237 внешних путей из пяти коммитов. Два HD4-изображения — LFS-указатели с совпадающими OID в FORK1 и PORT. Данные находятся в [credits.tsv](/srv/dune/worktrees/u13g/.tmp/p11r/credits.tsv).
- **Пункт 4:** Вступительный ролик вызывается из главного меню при наличии `intro.pak`; мышь и клавиатура пропускают его. Фактический путь `VideoFlow.hpp` — `src/game/VideoFlow.hpp`, указанный в задании `src/VideoFlow.hpp` отсутствует. Подробности — в [intro.tsv](/srv/dune/worktrees/u13g/.tmp/p11r/intro.tsv).
- **Пункт 5:** Найдены четыре проверки HD-представления и регистрация в CTest; файл тестов и использованный API отсутствуют в PORT. Подробности — в [tests.tsv](/srv/dune/worktrees/u13g/.tmp/p11r/tests.tsv).

**Сверка:** помощник 4 проверил 9 фактов, совпало 9. Команды и выводы: [spotcheck.md](/srv/dune/worktrees/u13g/.tmp/p11r/spotcheck.md).

**Чтение:** прочитаны `PORT_PLAN.md`, фрагменты карты `hd4-assets` и `credits-art`, решения Р34/Р63. Дополнительно прочитаны разделы 3.2, поток Б и 5.3 `docs/PLAN_units_sega_upstream.md` и целиком `codex-direct/launch-card-27.md`, поскольку на них ссылается план. В задании не совпадает путь заголовка VideoFlow с путём в UP1; команда и ошибка указаны в отчёте.

**Файлы `.tmp/p11r/`:** `RECON.md`, `progress.md`, `fork-mentat.tsv`, `port-mentat.tsv`, `credits.tsv`, `intro.tsv`, `tests.tsv`, `spotcheck.md`.

### Не проверено

Сборки, CTest и запуск игры не выполнялись согласно заданию. Реальное воспроизведение и содержимое внешнего `intro.pak` не проверялись; tracked-файл отсутствует в UP1 и PORT.

### Рабочие места

Вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p11r --size`:

```text
path	kind	branch	head_date	size	dirty	untracked	unpushed	worktrees	procs	refs
/srv/dune/worktrees/u13g/.tmp/p11r	dir	-	-	1301251	-	-	-	-	0	0
```

`.tmp/p11r` — **оставить — разведка для ведущего**.

Файлы вне `.tmp/p11r` не менялись; коммитов нет.