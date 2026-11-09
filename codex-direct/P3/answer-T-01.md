## A-P3T-01 — правка приёмочного теста после CI

Тесты приняты и закоммичены (`39525092`), код П3 сдан (`afe836b0`, `81ccd38c`). В CI GitHub все пять сборок упали на одном тесте:

```text
260/268 Test #260: P3 Graphics loads HD4 data pack with density 4 ...***Failed
Graphics: Failed to load image 145 : Parameter 'context' is invalid
tests/utils/test_Hd4Loading.cpp:115: FAILED:
  REQUIRE( t != nullptr )
```

Причина: CI не скачивает файлы Git LFS, и `resources/bin/data/sdl_data_hd4.dat` там — текстовый указатель LFS. Тест паков П2 в этом случае пропускается: `tests/utils/test_Hd4Packs.cpp`, строки 77–87, читает первую строку файла пака, отрезает конечный `\r` и при строке `version https://git-lfs.github.com/spec/v1` вызывает `SKIP`.

Код игры не меняется. Меняется только `tests/utils/test_Hd4Loading.cpp`.

1. В `TEST_CASE("P3 Graphics loads HD4 data pack with density 4", "[P3]")` первым действием, до `SDL_SetHint` и `SDL_Init`, прочитай первую строку файла `D2TM_SOURCE_DIR/resources/bin/data/sdl_data_hd4.dat` тем же способом, что в `test_Hd4Packs.cpp:77-87`. При строке `version https://git-lfs.github.com/spec/v1` вызови `SKIP("HD4 pack is a Git LFS pointer: sdl_data_hd4.dat")`. Подключи `<fstream>`, если его нет.
2. Проверь остальные девять `TEST_CASE` файла: читает ли тест содержимое файла, который в репозитории хранится в Git LFS. Хранится ли файл в LFS, определяй командой `git check-attr filter -- <путь>` (значение `lfs` — в LFS). Тест, который только проверяет существование файла (`std::filesystem::is_regular_file`), правки не требует. Тест, который читает содержимое LFS-файла, получает такой же `SKIP` по своему файлу. Ожидания и проверки тестов не меняй.
3. Сборка и прогон: проверь свободное место (`df -m /`, не меньше 5000 МБ, иначе стоп с `Q-P3T-04`), затем `DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p3t/build-fix.log 2>&1`. Ожидается код выхода `0`, в `ctest.log` — `100% tests passed`, десять тестов `P3 ` со статусом `Passed` (в этой рабочей копии паки настоящие, поэтому тест пункта 1 не пропускается).
4. Пересчитай хэши: `sha256sum tests/utils/test_Hd4Loading.cpp tests/CMakeLists.txt > .tmp/p3t/tests.sha256` и проверь `sha256sum -c .tmp/p3t/tests.sha256`.

Сдача — блок `## DONE-P3T-01 | <время UTC из date -u> | HEAD <sha>`: дифф `git diff -- tests`, строки `ctest.log` с `P3 ` и итоговой строкой, вывод `sha256sum -c`, итог пункта 2 по каждому из десяти тестов, список коммита (одно сообщение и файл `tests/utils/test_Hd4Loading.cpp`, последняя строка `Behavior changes: none`), `### Не проверено`, `### git status --short`.

### Организация работы

Порядок: пункты 1 и 2, затем пункт 3, затем пункт 4, затем сдача и стоп.

Параллельно: пункт 2 делает помощник одновременно с твоей правкой пункта 1.

Помощники: не больше одного, `gpt-6-luna` `xhigh`; он делает пункт 2 и прогон пункта 3.

Остановки: только на `## DONE-P3T-01` и на блоках `Q-P3T-NN`.

Рамка правок: `tests/utils/test_Hd4Loading.cpp`, `.tmp/p3t/` и `.tmp/progress.md`. Файлы `src/`, `resources/` и `tests/CMakeLists.txt` не меняй. Коммитов не делай.
