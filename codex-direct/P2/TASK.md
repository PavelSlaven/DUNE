# Задание P2 — слой данных и паки на ветке порта

## Цель

На ветке порта лежат паки форка в раскладке, которую понимает код апстрима, и два постоянных инструмента, которые эту раскладку строят.

- Классические паки `resources/bin/data/` слиты по записям из трёх ревизий: общий предок, форк, апстрим. Отчёт слияния не содержит нерешённых записей.
- Четыре графических HD4-пака форка выровнены по константам апстрима: запись с индексом `i` — картинка той константы апстрима, значение которой равно `i`. Записи форка, которых нет среди констант апстрима, стоят после последней константы и ищутся по имени.
- 18 HD4-паков сцен форка лежат на ветке порта без изменений.
- Код чтения паков апстрима (`DataPack`, `ReaderPack`) на SDL3 читает все 22 HD4-пака: приёмочный тест C++ проходит в сборке Linux.

Код игры в `src/` не меняется: загрузку HD4-паков игрой делает следующий шаг П3. После этого задания игра по-прежнему грузит классические паки и доходит до главного меню.

## Ревизии и рабочая копия

- `BASE` = `e17379ad660fca46859b403a6c3d33ec8d831a40` — общий предок.
- `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566` — форк, тег `v0.8.0-ru-hd.10`.
- `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489` — апстрим.
- Рабочая копия — `/srv/dune/worktrees/p2`, ветка `codex/p2`. Перед заданием в ней закоммичены приёмочные тесты; HEAD указан в строке запуска.
- Python — `/srv/dune/venv/bin/python`. Перед командами git выполни `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.
- Скрипты и тесты Python запускаются из корня рабочей копии. Модуль `tools/hd_assets.py` импортируется как `from tools import hd_assets`.
- Журнал хода — `.tmp/p2/progress.md`: строка на каждый подпункт шагов (что сделано, команда, итог). Логи — `.tmp/p2/`.

### Как получить файл из ревизии

Файл `<путь>` ревизии `<R>` кладётся в `.tmp/p2/rev/<R>/<путь>`, где `<R>` — `BASE`, `FORK1` или `UP1`.

1. Выполни `git show <SHA ревизии>:<путь>`.
2. Если вывод — указатель LFS (первая строка `version https://git-lfs.github.com/spec/v1`), возьми `oid` из строки `oid sha256:<oid>`. Скопируй объект `/srv/dune/worktrees/u63/.git/lfs/objects/<oid[0:2]>/<oid[2:4]>/<oid>` и сверь sha256 копии с `oid`.
3. Иначе запиши вывод `git show` в файл как есть.

Команды `git checkout` для чужих ревизий и `git lfs smudge` не используй. Если объекта LFS нет или sha256 не совпадает — блок `Q-P2-02` с путём и `oid` и стоп.

## Шаги

### 1. Вход

Расхождение в любом пункте — блок `Q-P2-01` со строками вывода и стоп.

- `git rev-parse HEAD` равен HEAD из строки запуска. `git status --short` без строк `.tmp/` пуст.
- `git merge-base --is-ancestor UP1 HEAD` завершается кодом 0.
- `df -m /srv` показывает в столбце `Available` не меньше 5000.
- `sha256sum -c .tmp/p2/tests.sha256` печатает `OK` для каждого файла. Файл хэшей приёмочных тестов пишет ведущий до запуска.
- Базовый прогон тестов Python: `/srv/dune/venv/bin/python -m unittest discover -s tools/upstream/tests -v`, лог `.tmp/p2/tests-before.log`. Ожидается падение приёмочных тестов по причинам, записанным в их сдаче: нет модулей `tools.hd_assets`, `tools.upstream.merge_classic_packs` и `tools.upstream.align_hd4_packs`, нет файлов паков.

### 2. Исходные файлы

- Из `FORK1` по способу «Как получить файл из ревизии» получи:
  - четыре пака `resources/bin/data/sdl_data_hd4.dat`, `resources/bin/data/sdl_inter_hd4.dat`, `resources/bin/data/sdl_mentat_hd4.dat`, `resources/bin/data/sdl_world_hd4.dat`;
  - 18 паков `resources/bin/data/scenes/hd4/sdl_*.dat` — список путей даёт `git ls-tree -r --name-only FORK1 resources/bin/data/scenes/hd4/`;
  - `tools/hd_assets.py`.
- Из каждой из трёх ревизий получи каждый файл `*.dat` дерева `resources/bin/data/` этой ревизии, кроме путей, которые оканчиваются на `_hd4.dat`, и путей внутри `resources/bin/data/scenes/hd4/`. Список путей ревизии даёт `git ls-tree -r --name-only <SHA> resources/bin/data/`.
- Скопируй `.tmp/p2/rev/FORK1/tools/hd_assets.py` в `tools/hd_assets.py`. Файл не правь: `cmp` с исходником даёт пустой вывод.

### 3. LFS для путей форка

В конец `.gitattributes` добавь ровно две строки:

```
resources/bin/data/*_hd4.dat filter=lfs diff=lfs merge=lfs -text
resources/bin/data/scenes/hd4/*.dat filter=lfs diff=lfs merge=lfs -text
```

Другие строки `.gitattributes` не меняются. Классические паки апстрима остаются обычными файлами git, без LFS: так слияния с апстримом не дают конфликтов «файл против указателя LFS».

### 4. Скрипт слияния классических паков

Файл `tools/upstream/merge_classic_packs.py`. Запуск:

```
python -m tools.upstream.merge_classic_packs --base-dir <каталог> --fork-dir <каталог> --upstream-dir <каталог> --out-dir <каталог> --report <файл.tsv>
```

Каждый из трёх входных каталогов — дерево `resources/bin/data` одной ревизии.

**Какие паки.** Скрипт обрабатывает каждый относительный путь `*.dat`, который есть хотя бы в одном входном каталоге. Пропускаются пути, которые оканчиваются на `_hd4.dat`, и пути с компонентом `scenes/hd4/`.

**Пак по наличию файла:**

| BASE | FORK1 | UP1 | Результат |
|---|---|---|---|
| есть | есть | есть | слияние по записям, правила ниже |
| нет | нет | есть | файл UP1 |
| нет | есть | нет | файл FORK1 |
| нет | есть | есть | файл UP1, если файлы FORK1 и UP1 побайтно равны; иначе ошибка |
| есть | нет | есть или нет | ошибка «пак удалён» |
| есть | есть | нет | ошибка «пак удалён» |

**Слияние по записям.** Пак читается функцией `hd_assets.read_pack`.

- Ключ записи — имя записи и её порядковый номер среди записей с тем же именем в этом паке: первая запись `X` — `X#1`, вторая — `X#2`.
- Запись равна другой, когда у них совпадают имя, расширение и данные.
- Форк может только менять данные записи на месте. Если множество ключей FORK1 не равно множеству ключей BASE или индекс записи с одним ключом в FORK1 и BASE различается — ошибка «форк добавил, удалил или переставил записи».
- Запись изменена форком, если запись FORK1 не равна записи BASE с тем же ключом.
- Запись изменена апстримом, если в UP1 нет записи с этим ключом или запись UP1 не равна записи BASE с тем же ключом.
- Результат — записи UP1 в порядке UP1. Запись UP1 с ключом, который форк изменил, заменяется записью FORK1.
- Конфликт — ключ, который изменили обе стороны, если записи FORK1 и UP1 с этим ключом не равны. Ключ, который форк изменил, а в UP1 его нет, — тоже конфликт.

**Запись результата.**

- Если записи результата равны записям UP1 (то же число, по порядку попарно равны), файл UP1 копируется побайтно.
- Иначе, если записи результата так же равны записям FORK1, побайтно копируется файл FORK1.
- Иначе файл пишется функцией `hd_assets.write_pack`.

**Ошибки.** При любой ошибке или хотя бы одном конфликте скрипт не пишет ни одного файла в `--out-dir` и завершается кодом 1. В stderr — путь пака, вид ошибки и ключи конфликтующих записей. Код 2 — ошибка аргументов.

**Отчёт** `--report` — TSV с заголовком `pack	index	key	fork	upstream	source`, по строке на каждую запись каждого результата слияния по записям, в порядке путей паков и индексов:

- `pack` — относительный путь пака;
- `index` — индекс записи в результате;
- `key` — ключ записи;
- `fork` — `unchanged` или `changed`;
- `upstream` — `unchanged`, `changed` или `added`; `added` — ключа нет в BASE;
- `source` — `fork`, если запись взята из FORK1; `upstream`, если апстрим её изменил или добавил; иначе `base`.

Паки, взятые целиком по таблице наличия файла, дают в отчёте одну строку: `index` и `key` — `-`, `fork` и `upstream` — `-`, `source` — `upstream-file` или `fork-file`.

### 5. Скрипт выравнивания HD4-паков

Файл `tools/upstream/align_hd4_packs.py`. Запуск — отдельно для каждого пака:

```
python -m tools.upstream.align_hd4_packs --fork-pack <HD4-пак FORK1> --classic-pack <классический пак> --header <заголовок констант> --list <классика без HD .json> --out <выходной пак> --report <файл.tsv>
```

**Константы.** Скрипт читает из `--header` строки двух видов: `#define ИМЯ N` и `constexpr int ИМЯ = N;`, где перед `constexpr` может стоять `inline` или `static`, а `N` — десятичное целое. После числа или `;` может идти комментарий. Остальные строки пропускаются.

- `N` — наибольшее значение. Для каждого `i` от 0 до `N` должна быть ровно одна константа со значением `i`. Пропуск значения или два имени с одним значением — ошибка.

**Список «классика без HD».** JSON-объект: ключ — имя файла пака, значение — список имён. Скрипт использует список под ключом, равным имени файла `--out`; нет ключа — пустой список.

**Раскладка результата:**

1. Позиции `0…N`. На позицию `i` ставится запись для константы со значением `i` (имя `C`):
   - если в `--fork-pack` есть запись с именем `C`, она ставится без изменений;
   - иначе, если `C` есть в списке, ставится новая запись. Имя и расширение — у записи с индексом `i` пака `--classic-pack`. Данные — `hd_assets.encode_png(hd_assets.scale_image(hd_assets.decode_image(<данные этой записи>), 4))`. Если у записи `i` классического пака другое имя, чем `C`, или её данные не декодируются — ошибка;
   - иначе — ошибка «нет записи для константы».
2. Позиции после `N`. Записи `--fork-pack` с индексом больше `N` ставятся в порядке FORK1. Если имя такой записи равно имени константы — ошибка.
3. Хвост. Записи `--fork-pack` с индексом от 0 до `N`, которые не поставлены в пункте 1, дописываются в конец в порядке FORK1.

**Проверки результата.** Нарушение — ошибка.

- Каждая запись `--fork-pack` стоит в результате ровно один раз и равна себе: имя, расширение и данные.
- Имена записей результата не повторяются.
- Каждое имя списка под ключом `--out` использовано в пункте 1.

**Запись результата.** Если записи результата равны записям `--fork-pack` (то же число, по порядку попарно равны), файл `--fork-pack` копируется побайтно. Иначе файл пишется функцией `hd_assets.write_pack`.

**Ошибки.** При ошибке скрипт не пишет `--out` и `--report`, завершается кодом 1, в stderr — вид ошибки, имя и индекс. Код 2 — ошибка аргументов.

**Отчёт** `--report` — TSV с заголовком `index	name	source	fork_index	sha256`, строка на каждую запись результата:

- `source` — `fork` или `classic_x4`;
- `fork_index` — индекс записи в `--fork-pack`; у `classic_x4` — `-`;
- `sha256` — `hd_assets.sha256` данных записи результата.

### 6. Список «классика без HD»

Файл `tools/upstream/classic_without_hd.json` — ровно такой объект, ключи и имена в этом порядке:

```json
{
  "sdl_data_hd4.dat": ["EXPLOSION_CARRYALL"],
  "sdl_inter_hd4.dat": ["BMP_SELECT_HOUSE_SARDAUKAR", "ICON_POWER_LOW"],
  "sdl_mentat_hd4.dat": ["MENTATS"],
  "sdl_gfxeditor.dat": ["BLOOM", "BUILDINGS", "FLIPHORZ", "FLIPVERT", "GRID", "LAYERS", "MOUNTAINS", "SANDLAYER", "SELECT", "SPICELAYER", "STONELAYER", "UNITS", "SOLDIERS", "TERRAN_HILL", "TERRAN_MOUNTAIN", "TERRAN_ROCK", "TERRAN_SAND", "TERRAN_SPICE", "TERRAN_SPICEHILL", "STARTPOSITION", "STARTPOSITION1", "STARTPOSITION2", "STARTPOSITION3", "STARTPOSITION4", "STARTPOSITION5", "FLIPHORZLR", "FLIPHORZRL", "FLIPVERTBT", "FLIPVERTTB", "FLIPDIAGBL", "FLIPDIAGBR", "FLIPDIAGTL", "FLIPDIAGTR", "SAVEICON"]
}
```

Список задан решением владельца Р65 в `docs/decisions.md`:
- Значки редактора карт остаются классикой в паке апстрима `sdl_gfxeditor.dat`. Скрипт выравнивания ключ `sdl_gfxeditor.dat` не читает; ключ нужен проверке «каждая картинка апстрима имеет HD4-запись или стоит в списке».
- Для четырёх картинок игры рисуются HD-версии отдельной задачей. До неё на их местах в HD4-паках стоит классика ×4, поэтому их имена стоят в списке.

### 7. Прогон

1. Слияние классических паков:
   `python -m tools.upstream.merge_classic_packs --base-dir .tmp/p2/rev/BASE/resources/bin/data --fork-dir .tmp/p2/rev/FORK1/resources/bin/data --upstream-dir .tmp/p2/rev/UP1/resources/bin/data --out-dir resources/bin/data --report docs/upstream/p2/classic_packs_merge.tsv`.
   Код 1 со строками конфликтов — блок `Q-P2-03` с выводом stderr и стоп.
2. Выравнивание — четыре запуска, по строке таблицы. `--fork-pack` — `.tmp/p2/rev/FORK1/resources/bin/data/<HD4-пак>`, `--classic-pack` — `resources/bin/data/<классический пак>` рабочей копии после пункта 1, `--list` — `tools/upstream/classic_without_hd.json`, `--out` — `resources/bin/data/<HD4-пак>`, `--report` — `docs/upstream/p2/hd4_alignment_<HD4-пак без .dat>.tsv`.

   | HD4-пак | Классический пак | `--header` |
   |---|---|---|
   | `sdl_data_hd4.dat` | `sdl_data.dat` | `src/data/gfxdata.h` |
   | `sdl_inter_hd4.dat` | `sdl_inter.dat` | `src/data/gfxinter.h` |
   | `sdl_mentat_hd4.dat` | `sdl_mentat.dat` | `src/include/gfxmentat.h` |
   | `sdl_world_hd4.dat` | `sdl_world.dat` | `src/include/gfxworld.h` |

   Код 1 — блок `Q-P2-04` с выводом stderr и стоп.
3. Скопируй 18 паков сцен из `.tmp/p2/rev/FORK1/resources/bin/data/scenes/hd4/` в `resources/bin/data/scenes/hd4/` побайтно.

**Ожидаемый итог.** Расхождение — блок `Q-P2-05` с числами и стоп.

- Скрипт слияния завершился кодом 0. В отчёте слияния нет строк, у которых `fork` = `changed` и `upstream` = `changed`.
- `resources/bin/data/sdl_inter.dat` — 146 записей: 54 записи с `source` = `fork`, записи 144 `BMP_SELECT_HOUSE_SARDAUKAR` и 145 `ICON_POWER_LOW` с `source` = `upstream`.
- `resources/bin/data/sdl_world.dat` побайтно равен файлу FORK1 (sha256 `ebf869028eae8d477e03f368c8a4d5e7040c5b204a151386792fa61c9f77aaa3`).
- `git diff --stat UP1 -- resources/bin/data/sdl_audio.dat resources/bin/data/sdl_data.dat resources/bin/data/sdl_mentat.dat resources/bin/data/sdl_gfxeditor.dat` пуст.
- `sdl_data_hd4.dat` — 242 записи: 167 — `EXPLOSION_CARRYALL` (`classic_x4`), 168–240 — те же записи, что 168–240 в FORK1, 241 — `HM_BUILD_REFINERY`.
- `sdl_inter_hd4.dat` — 146 записей: 144 и 145 — `classic_x4`.
- `sdl_mentat_hd4.dat` — 52 записи: 51 — `MENTATS` (`classic_x4`).
- `sdl_world_hd4.dat` побайтно равен файлу FORK1 (sha256 `94cf42fef1a755cc36b3b70f34900b15f76f28a540a38b73f69483f41b311d68`).
- Каждый из 18 паков сцен побайтно равен файлу FORK1.
- `git check-attr filter` даёт `lfs` для 22 HD4-паков и `unspecified` для классических паков.

### 8. Проверки

- Тесты Python: `/srv/dune/venv/bin/python -m unittest discover -s tools/upstream/tests -v`, лог `.tmp/p2/tests-after.log`. Ожидается `OK` без пропусков.
- Сборка Linux: `DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489`, лог `.tmp/p2/build.log`. Перед сборкой `df -m /srv` — не меньше 5000 в `Available`, иначе блок `Q-P2-06` и стоп. Успех: код 0, в `ctest.log` тест чтения HD4-паков в состоянии `Passed`, а не `Skipped`; игра доходит до главного меню. Иначе — блок `Q-P2-07` с последними 40 строками лога и стоп.
- `sha256sum -c .tmp/p2/tests.sha256` печатает `OK` для каждого файла.
- `git status --short` без строк `.tmp/` содержит только пути из раздела «Рамка правок». Другой путь — находка в сдаче.

Падение приёмочного теста, который ты считаешь неверным, — блок `Q-P2-08` со строками вывода и твоим объяснением, и стоп. Приёмочные тесты не меняй.

## Рамка правок

- `.gitattributes` — две строки шага 3.
- `tools/hd_assets.py` — копия из FORK1.
- `tools/upstream/merge_classic_packs.py`, `tools/upstream/align_hd4_packs.py`, `tools/upstream/classic_without_hd.json`.
- `resources/bin/data/sdl_inter.dat`, `resources/bin/data/sdl_world.dat`.
- `resources/bin/data/sdl_data_hd4.dat`, `resources/bin/data/sdl_inter_hd4.dat`, `resources/bin/data/sdl_mentat_hd4.dat`, `resources/bin/data/sdl_world_hd4.dat`.
- 18 файлов `resources/bin/data/scenes/hd4/sdl_*.dat`.
- `docs/upstream/p2/classic_packs_merge.tsv` и четыре файла `docs/upstream/p2/hd4_alignment_*.tsv`.
- `.tmp/`.

Файлы `src/`, `tests/`, `tools/upstream/tests/` и `.github/` не меняются. Коммитов не делай.

## Сдача

Блок `## DONE-P2 | <время UTC из date -u> | HEAD <sha>`. В нём:

- строки входа шага 1 и итог базового прогона;
- журнал хода — ссылка на `.tmp/p2/progress.md` и его строки по шагам 4–7;
- по каждому паку слияния: путь, `source` пака или число записей по значениям `source`;
- по каждому HD4-паку: число записей, индексы и имена `classic_x4`, индексы и имена хвоста;
- строки проверок шага 7 «Ожидаемый итог» с фактическими значениями;
- итоги шага 8: строка итога тестов Python, строки `ctest.log` об итоге и о тесте чтения HD4-паков, строка о главном меню из лога сборки, вывод `sha256sum -c`;
- `df -m /srv` после сборки;
- `### Коммиты` — одно английское сообщение `Bring the fork's data packs onto the upstream port branch`, в нём ровно один абзац `Behavior changes:` перед завершающей строкой `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, и список файлов коммита;
- `### Не проверено`;
- `### git status --short`.

## Организация работы

- **Режим:** «Ведёт sol».
- **Порядок:** шаг 1 → шаги 2 и 3 → шаги 4, 5 и 6 → шаг 7 → шаг 8 → `## DONE-P2` и стоп.
- **Параллельно:** шаги 2 и 3 не зависят друг от друга. Шаги 4, 5 и 6 не зависят друг от друга.
- **Помощники:** до 2, `gpt-6-luna` `xhigh`, без вложенных.
  - Помощник 1 — шаг 4: скрипт слияния; готов, когда проходят тесты `tools/upstream/tests/test_merge_classic_packs.py`.
  - Помощник 2 — шаг 5: скрипт выравнивания; готов, когда проходят тесты `tools/upstream/tests/test_align_hd4_packs.py`.
  - Шаги 1, 2, 3, 6, 7, 8, проверку выходов помощников и сдачу делает корневая нить.
  - В бриф помощника дословно входят абзац «Комментарии в коде» ниже и его рамка правок: помощнику 1 — `tools/upstream/merge_classic_packs.py` и `.tmp/p2/`; помощнику 2 — `tools/upstream/align_hd4_packs.py` и `.tmp/p2/`.
- **Остановки:** только на `## DONE-P2` и на блоках `Q-P2-NN`.
- **Рамка правок:** пути раздела «Рамка правок» выше. Коммитов не делай.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами.

Помощнику этот абзац передаётся в бриф дословно.
