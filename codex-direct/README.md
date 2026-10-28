# Задания исполнителям Codex

- `TASK-RULES.md` — обязательные правила; запускающий дописывает их в конец каждого задания перед отправкой.
- `<id>/TASK.md` — задание. Ответы исполнителя (`PLAN`, `Q`, `DONE`) и ответы ведущего хранятся рядом: `<id>/reply-NN.md`, `<id>/answer-NN.md`.
- Исполнитель работает на servak в `/srv/dune/worktrees/<id>` (клон этого репозитория) в ветке `codex/<id>`; ветку забирает ведущий.
- Входные данные вне репозитория, только для чтения: паки — `/srv/dune/inputs/packs/`, модели пилота — `/srv/dune/inputs/glb/`. Blender — `/srv/dune/tools/blender-5.2.3-linux-x64/blender`, Python — `/srv/dune/venv/bin/python`.
- Текущий план работ — закреплённый issue репозитория; общий план — `docs/PLAN_units_sega_upstream.md`; решения владельца — `docs/decisions.md`.
