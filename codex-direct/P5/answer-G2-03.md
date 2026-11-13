## Ответ на Q-P5G2-08

Ошибка в задании: команда проверки 8 содержала `rm -rf`, а среда исполнителя такие команды отклоняет. Проверка 8 теперь без удаления: у каждого запуска своя новая папка из `mktemp -d` внутри `.tmp/p5g2/` (папка данных игры и папка снимков в ней), ничего не удаляется. Всё остальное в ответе на Q-P5G2-02 (прошлый ход) — шаг 12, порядок проверок, ожидания, форма сдачи — не меняется; строки об удалении `rep-xdg` и `rep-out` отменены.

Проверка 8, из корня рабочей копии; перед командой — `L=check-08-red.log` для красной проверки (до шага 12) и `L=check-08-green.log` для зелёной (после шага 12 и сборки):

```bash
R=$PWD/.tmp/p5g2; (cd .tmp/out/run/bin && for s in skirmish-setup-random skirmish-setup-ready-map; do for i in $(seq 1 20); do X=$(mktemp -d $R/rep-XXXXXX); LD_LIBRARY_PATH=/srv/dune/worktrees/u34/.tmp/deps/prefix/lib SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=$X timeout 120 ./d2tm -windowed -screenWidth 1024 -screenHeight 768 --ui-audit-scene $s --ui-audit-out $X/out > /dev/null 2>&1; echo "$s $i exit=$?"; done; done) > $R/$L 2>&1; grep -c 'exit=0' $R/$L
```

Ожидается: красная — число меньше 40 (у ведущего этой же командой на текущей сборке — 22); зелёная — ровно `40`. Папки `.tmp/p5g2/rep-*` в разделе «Рабочие места» сдачи — с пометкой `удалить`; удаляет их ведущий.

Механику — правку, сборку, проверки — делают только помощники. Не отступай от плана, не переусложняй.
