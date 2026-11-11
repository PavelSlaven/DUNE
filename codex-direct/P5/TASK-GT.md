# Задание P5GT — приёмочные тесты ядра режима отладки интерфейса (шаг П5г, часть 1)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high`; прогоны сборки и игры делает один субагент `gpt-6-luna` `xhigh`.

Рабочая копия: `/srv/dune/worktrees/u34`, ветка `codex/p5g`, `HEAD` — `4aa980e36ee7a8ff0e651ce10c4f55869d86f08d` (вершина ветки порта после шага П5в). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p5gt/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи.

## Цель

Написать приёмочные тесты первой части шага П5г по контракту ниже: тест Catch2 разбора аргументов и три скрипта Python, которые запускают игру. Получить красные прогоны A и B и зелёный прогон C теста Catch2, проверить посылку о размере холста прогоном D, получить красный прогон E скриптов Python и заморозить тесты хэшем. Код игры не менять, кроме временных файлов прогонов B и C (шаг 2), которые убираются сразу после каждого из них.

## Что уже решено

Первая часть шага П5г переносит в порт ядро режима отладки интерфейса форка (`ui-audit`): разбор аргументов `--ui-audit-*`, каталог сцен с одной сценой `main-menu`, ранние выходы `--ui-audit-list` и `--ui-audit-scales`, снимок сцены в PNG и файл геометрии JSONL с записями текста и элементов интерфейса. Остальные сцены и вызовы режима из кода игры — следующие части шага. В режиме отладки игра не пишет файл настроек `preferences.ini`.

Тесты пишутся до кода. Их потом выполняет другой исполнитель, который пишет код по тому же контракту и тесты не меняет. Скрипты Python запускают установленную игру и в CTest не входят: в CI нет данных Git LFS.

## Прочитать до работы

Прочитай целиком до первого действия, каждый файл отдельным вызовом, пути — от корня рабочей копии:

- `tests/utils/test_HudLayout.cpp` — образец теста Catch2 в порту;
- `tests/CMakeLists.txt`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/UiAuditArgumentsTests.cpp` — тест форка, который переносишь;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.hpp` и `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp`;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/ui_audit_runtime_support.py`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/ui_audit_main_menu_png.py`, `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/ui_audit_unknown_scene.py` — скрипты форка, которые переносишь;
- вывод `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditCapture.cpp | sed -n '155,211p;369,422p'` — формат файла геометрии и ранних выходов форка.

Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

## Контракт поведения

Этот раздел дословно входит и в задание исполнителя кода.

1. **Разбор аргументов (новые файлы).** `src/debug/UiAuditArguments.hpp` и `src/debug/UiAuditArguments.cpp` — дословные копии одноимённых файлов ревизии форка `9208dcf5a358f40afd95c99480e4e09f781ed566`. В них: структура `uiaudit::Options` с полями `bool list`, `std::string scales`, `std::string scene`, `std::string outDir`; функции `void uiaudit::consumeArguments(int &argc, char **argv)`, `const uiaudit::Options &uiaudit::options()`, `bool uiaudit::isEnabled()`. `consumeArguments` убирает из `argv` аргументы `--ui-audit-list`, `--ui-audit-scales <значение>`, `--ui-audit-scene <значение>`, `--ui-audit-out <значение>` и оставляет остальные в прежнем порядке; режим включён, если есть `--ui-audit-list`, или непустой `--ui-audit-scales`, или вместе непустые `--ui-audit-scene` и `--ui-audit-out`.
2. **Запуск игры с аргументами режима.** Игра `d2tm` запускается из каталога установки сборки порта (рабочий каталог процесса — этот каталог) с аргументами `-windowed -screenWidth 1024 -screenHeight 768` и аргументами режима ниже; переменные среды `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy`, `XDG_DATA_HOME=<пустая временная папка>`.
   1. `--ui-audit-list` — код выхода 0; весь вывод stdout без пробельных символов по краям — один объект JSON с ключом `scenes`: список объектов, у каждого ровно ключи `id`, `group`, `state`, `screen`, `game_screen`, `house`, `hud`, `hd_only`, `hover`, `readiness`. В списке ровно одна сцена с `id` `main-menu`, и она равна объекту `{"id": "main-menu", "group": "main-menu", "state": "GAME_MENU", "screen": "cMainMenuState", "game_screen": false, "house": "", "hud": false, "hd_only": false, "hover": null, "readiness": "StateSettled"}`.
   2. `--ui-audit-scales 1024x768` — код выхода 0; весь вывод stdout без пробельных символов по краям — объект JSON ровно с ключами `resolution`, `render`, `world`; `resolution` — `"1024x768"`; `render` — непустой список целых чисел, первое — 0; `world` — `[0, 100, 110, 125, 150]`. `--ui-audit-scales abc` — код выхода 2, stderr содержит строку `ui-audit: bad resolution abc`.
   3. `--ui-audit-scene no-such-scene__nothing --ui-audit-out <папка>` — код выхода 2; stderr содержит строку `ui-audit: unknown scene no-such-scene__nothing`; в папке `<папка>` нет файлов.
   4. `--ui-audit-scene main-menu --ui-audit-out <папка>` — код выхода 0 не позже чем через 120 секунд; в `<папка>` есть файлы `main-menu.png` и `main-menu.geometry.jsonl`. PNG — 1024 × 768 точек. Каждая строка файла геометрии — объект JSON. Первая строка — заголовок, в нём значения ключей `k`, `scene`, `resolution`, `language`, `graphics`, `canvas`, `game_screen`, `render_scale`, `world_scale` равны `"header"`, `"main-menu"`, `"1024x768"`, `"en"`, `"hd"`, `{"w": 800, "h": 600}`, `false`, `0`, `0`, а `version` — строка. Есть хотя бы одна запись с `"k": "text"`, у каждой такой записи ровно ключи `k`, `s`, `x`, `y`, `w`, `h`, `box`. Есть хотя бы одна запись с `"k": "gui"`, у каждой такой записи ровно ключи `k`, `t`, `x`, `y`, `w`, `h`. После выхода игры в папке `XDG_DATA_HOME` нет файла с именем `preferences.ini` ни на каком уровне вложенности.

## Шаг 1. Тесты — корневая нить сама

### Новый файл `tests/utils/test_UiAuditArguments.cpp`

Ровно такого вида:

```cpp
#include <catch2/catch_test_macros.hpp>

#include "debug/UiAuditArguments.hpp"

#include <string>
#include <vector>

namespace {
struct Argv {
    explicit Argv(std::vector<std::string> values) : storage(std::move(values))
    {
        for (auto &value : storage) {
            pointers.push_back(value.data());
        }
        pointers.push_back(nullptr);
        argc = static_cast<int>(storage.size());
    }

    std::vector<std::string> storage;
    std::vector<char *> pointers;
    int argc = 0;
    char **argv() { return pointers.data(); }
};

bool remaining(Argv &args, const std::vector<std::string> &expected)
{
    if (args.argc != static_cast<int>(expected.size())) {
        return false;
    }
    for (int i = 0; i < args.argc; i++) {
        if (expected[i] != args.argv()[i]) {
            return false;
        }
    }
    return true;
}
}

TEST_CASE("P5G ui audit stays off on a plain launch", "[P5G]")
{
    Argv args({"d2tm"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
    CHECK_FALSE(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm"}));
}

TEST_CASE("P5G ui audit keeps ordinary game arguments", "[P5G]")
{
    Argv args({"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
    CHECK(remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024", "-screenHeight", "768"}));
}

TEST_CASE("P5G ui audit needs a scene besides the output directory", "[P5G]")
{
    Argv args({"d2tm", "--ui-audit-out", "somewhere", "-windowed"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
}

TEST_CASE("P5G ui audit scene and output enable the mode and are removed", "[P5G]")
{
    Argv args({"d2tm", "-windowed", "--ui-audit-scene", "main-menu", "--ui-audit-out", "out dir", "-screenWidth", "1024"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK(uiaudit::isEnabled());
    CHECK(uiaudit::options().scene == "main-menu");
    CHECK(uiaudit::options().outDir == "out dir");
    CHECK_FALSE(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm", "-windowed", "-screenWidth", "1024"}));
}

TEST_CASE("P5G ui audit list enables the mode and is removed", "[P5G]")
{
    Argv args({"d2tm", "--ui-audit-list"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK(uiaudit::isEnabled());
    CHECK(uiaudit::options().list);
    CHECK(remaining(args, {"d2tm"}));
}

TEST_CASE("P5G ui audit is switched off again by a later plain launch", "[P5G]")
{
    Argv enabling({"d2tm", "--ui-audit-list"});
    uiaudit::consumeArguments(enabling.argc, enabling.argv());
    REQUIRE(uiaudit::isEnabled());
    Argv args({"d2tm"});
    uiaudit::consumeArguments(args.argc, args.argv());
    CHECK_FALSE(uiaudit::isEnabled());
}
```

### Правка `tests/CMakeLists.txt`

1. В список `TEST_FILES` строка `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_UiAuditArguments.cpp` сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_HudLayout.cpp`.
2. В список `TEST_SOURCES` строка `    ${CMAKE_SOURCE_DIR}/src/debug/UiAuditArguments.cpp` сразу после строки `    ${CMAKE_SOURCE_DIR}/src/utils/HdUiTextureLoader.cpp`.

Других правок в `tests/CMakeLists.txt` нет. Строк из пунктов 1 и 2, после которых вставляешь, в файле должно быть ровно по одной (`grep -c`); иначе блок `## Q-P5GT-06` с выводом и стоп.

### Новый файл `tests/ui_audit/ui_audit_runtime_support.py`

Ровно такого вида:

```python
import json
import os
import subprocess
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 120
SCREEN_ARGS = ["-windowed", "-screenWidth", "1024", "-screenHeight", "768"]


class GameRun:
    def __init__(self, run_dir):
        self.run_dir = Path(run_dir).resolve()
        self.directory = tempfile.TemporaryDirectory(prefix="ui-audit-test-")
        root = Path(self.directory.name)
        self.out = root / "out"
        self.out.mkdir()
        self.xdg = root / "xdg"
        self.xdg.mkdir()

    def run(self, extra_args):
        environment = dict(os.environ)
        environment.update(
            SDL_VIDEODRIVER="dummy",
            SDL_RENDER_DRIVER="software",
            SDL_AUDIODRIVER="dummy",
            XDG_DATA_HOME=str(self.xdg),
        )
        return subprocess.run(
            [str(self.run_dir / "d2tm"), *SCREEN_ARGS, *extra_args],
            cwd=self.run_dir,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

    def close(self):
        self.directory.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def png_size(path):
    data = Path(path).read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def read_json(stdout):
    return json.loads(stdout.strip())
```

### Новый файл `tests/ui_audit/ui_audit_list_and_scales.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE_KEYS = {"id", "group", "state", "screen", "game_screen", "house", "hud", "hd_only", "hover", "readiness"}
MAIN_MENU = {
    "id": "main-menu",
    "group": "main-menu",
    "state": "GAME_MENU",
    "screen": "cMainMenuState",
    "game_screen": False,
    "house": "",
    "hud": False,
    "hd_only": False,
    "hover": None,
    "readiness": "StateSettled",
}
WORLD_SCALES = [0, 100, 110, 125, 150]


def check_list(game):
    result = game.run(["--ui-audit-list"])
    if result.returncode != 0:
        return f"--ui-audit-list exited with {result.returncode}\n{result.stderr}"
    try:
        scenes = support.read_json(result.stdout)["scenes"]
    except (ValueError, KeyError, TypeError) as error:
        return f"--ui-audit-list did not print a catalog: {error}\n{result.stdout}"
    for scene in scenes:
        if set(scene) != SCENE_KEYS:
            return f"Scene keys differ: {sorted(scene)}"
    main_menu = [scene for scene in scenes if scene["id"] == "main-menu"]
    if main_menu != [MAIN_MENU]:
        return f"Unexpected main-menu entry: {main_menu}"
    return None


def check_scales(game):
    result = game.run(["--ui-audit-scales", "1024x768"])
    if result.returncode != 0:
        return f"--ui-audit-scales exited with {result.returncode}\n{result.stderr}"
    try:
        scales = support.read_json(result.stdout)
    except ValueError as error:
        return f"--ui-audit-scales did not print JSON: {error}\n{result.stdout}"
    if set(scales) != {"resolution", "render", "world"} or scales["resolution"] != "1024x768":
        return f"Unexpected scales: {scales}"
    render = scales["render"]
    if not render or render[0] != 0 or not all(type(value) is int for value in render):
        return f"Unexpected render scales: {render}"
    if scales["world"] != WORLD_SCALES:
        return f"Unexpected world scales: {scales['world']}"
    bad = game.run(["--ui-audit-scales", "abc"])
    if bad.returncode != 2 or "ui-audit: bad resolution abc" not in bad.stderr:
        return f"A bad resolution must exit with 2 and be named: {bad.returncode}\n{bad.stderr}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        for check in (check_list, check_scales):
            error = check(game)
            if error:
                print(error, file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Новый файл `tests/ui_audit/ui_audit_unknown_scene.py`

Ровно такого вида:

```python
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

UNKNOWN_SCENE = "no-such-scene__nothing"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        result = game.run(["--ui-audit-scene", UNKNOWN_SCENE, "--ui-audit-out", str(game.out)])
        if result.returncode != 2:
            print(f"An unknown scene must exit with 2, got {result.returncode}\n{result.stderr}", file=sys.stderr)
            return 1
        if f"ui-audit: unknown scene {UNKNOWN_SCENE}" not in result.stderr:
            print(f"The unknown scene is not named on stderr:\n{result.stderr}", file=sys.stderr)
            return 1
        leftovers = sorted(path.name for path in game.out.rglob("*") if path.is_file())
        if leftovers:
            print(f"An unknown scene must not create files: {leftovers}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Новый файл `tests/ui_audit/ui_audit_main_menu_png.py`

Ровно такого вида:

```python
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ui_audit_runtime_support as support  # noqa: E402

SCENE = "main-menu"
HEADER = {
    "k": "header",
    "scene": SCENE,
    "resolution": "1024x768",
    "language": "en",
    "graphics": "hd",
    "canvas": {"w": 800, "h": 600},
    "game_screen": False,
    "render_scale": 0,
    "world_scale": 0,
}
TEXT_KEYS = {"k", "s", "x", "y", "w", "h", "box"}
GUI_KEYS = {"k", "t", "x", "y", "w", "h"}


def check(game):
    result = game.run(["--ui-audit-scene", SCENE, "--ui-audit-out", str(game.out)])
    if result.returncode != 0:
        return f"Game exited with {result.returncode}\n{result.stdout}\n{result.stderr}"
    png = game.out / f"{SCENE}.png"
    log = game.out / f"{SCENE}.geometry.jsonl"
    if not png.is_file() or not log.is_file():
        return f"Missing output: png={png.is_file()} log={log.is_file()}"
    try:
        size = support.png_size(png)
    except ValueError as error:
        return str(error)
    if size != (1024, 768):
        return f"Unexpected PNG size: {size[0]}x{size[1]}"
    try:
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    except ValueError as error:
        return f"A geometry line is not JSON: {error}"
    if not records or not all(isinstance(record, dict) for record in records):
        return "The geometry log must hold JSON objects"
    header = records[0]
    if {key: header.get(key) for key in HEADER} != HEADER or not isinstance(header.get("version"), str):
        return f"Unexpected header: {header}"
    texts = [record for record in records if record.get("k") == "text"]
    if not texts or any(set(record) != TEXT_KEYS for record in texts):
        return f"Text records are missing or malformed: {texts[:3]}"
    guis = [record for record in records if record.get("k") == "gui"]
    if not guis or any(set(record) != GUI_KEYS for record in guis):
        return f"GUI records are missing or malformed: {guis[:3]}"
    preferences = sorted(str(path) for path in game.xdg.rglob("preferences.ini"))
    if preferences:
        return f"An audit run must not write preferences: {preferences}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    with support.GameRun(args.run_dir) as game:
        error = check(game)
        if error:
            print(error, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Другие файлы `tests/` и весь код вне `tests/` не меняются.

## Шаг 2. Прогоны — субагент `gpt-6-luna` `xhigh`

Перед каждой сборкой `df -m /srv`: в столбце `Available` не меньше 5000, иначе блок `## Q-P5GT-01` и стоп. Команда сборки из корня рабочей копии (в `<лог>` — имя файла ниже):

```
DUNE_DEPS_DIR=$PWD/.tmp/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p5gt/<лог> 2>&1
```

Субагент сдаёт корневой нити код выхода каждого прогона, все строки лога прогона и `.tmp/out/logs/<последняя папка>/full.log`, содержащие `error:`, вывод `grep -A3 "CMake Error"` по тем же двум файлам и, если есть `ctest.log` последней папки логов, его строки с `P5G `, `Failed`, `failed` и итоговую строку `tests passed`.

- **Прогон A** — лог `build-red-a.log`, рабочая копия как после шага 1. Ожидается: код выхода не 0; в выводе `grep -A3 "CMake Error"` есть строка, содержащая `src/debug/UiAuditArguments.cpp`.
- **Прогон B** — лог `build-red-b.log`. Перед ним субагент создаёт папку `src/debug` и в ней два временных файла: `src/debug/UiAuditArguments.hpp` — командой `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.hpp > src/debug/UiAuditArguments.hpp`; `src/debug/UiAuditArguments.cpp` — ровно такого вида:
  ```cpp
  #include "UiAuditArguments.hpp"

  namespace uiaudit {

  bool g_enabled = false;

  namespace {
  Options s_options;
  }

  const Options &options()
  {
      return s_options;
  }

  void consumeArguments(int &argc, char **)
  {
      s_options = Options{};
      argc = 1;
      g_enabled = true;
  }

  }
  ```
  Сразу после прогона B — `rm -r src/debug`. Ожидается: строк `error:` нет; код выхода не 0; в `ctest.log` провалены ровно шесть тестов — все шесть тестов `P5G ` из шага 1; остальные тесты — `Passed`.
- **Прогон C** — лог `build-green-c.log`. Перед ним субагент создаёт папку `src/debug` и в ней временные копии файлов форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.hpp > src/debug/UiAuditArguments.hpp` и `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/debug/UiAuditArguments.cpp > src/debug/UiAuditArguments.cpp`. Сразу после прогона C — `rm -r src/debug`. Ожидается: код выхода 0; строк `error:` нет; все шесть тестов `P5G ` — `Passed`; итоговая строка `ctest.log` — `100% tests passed, 0 tests failed out of 318` (312 тестов сборки шага П5в и шесть новых).
- **Прогон D** — посылка о холсте, после прогона C, на игре, которую установил прогон C. Из корня рабочей копии:
  ```
  mkdir -p .tmp/p5gt/xdg-d && (cd .tmp/out/run/bin && SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy XDG_DATA_HOME=/srv/dune/worktrees/u34/.tmp/p5gt/xdg-d timeout 20 ./d2tm -windowed -screenWidth 1024 -screenHeight 768) > .tmp/p5gt/run-d.log 2>&1; echo exit=$?; grep -n 'logical canvas' .tmp/out/run/bin/nlog.txt
  ```
  Ожидается: `exit=124`; ровно одна строка вывода `grep`, и в ней есть `logical canvas 800x600`.
- **Прогон E** — красные скрипты Python, после прогона D, на той же игре. Из корня рабочей копии для каждого скрипта `<скрипт>` из `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`: `python3 tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p5gt/run-e-<скрипт>.log 2>&1; echo exit=$?`. Ожидается: у каждого `exit=1`, в логе — строка из скрипта о коде выхода игры, отличном от ожидаемого, и вывод stderr игры с её сообщением о неизвестном аргументе `--ui-audit-…`. Перед прогоном E — `python3 -m py_compile tests/ui_audit/*.py` с кодом выхода 0; после прогона E — `rm -r tests/ui_audit/__pycache__`, если такая папка появилась.

Проверка уборки после прогонов B и C: `test ! -e src/debug` с кодом выхода 0, иначе блок `## Q-P5GT-05` и стоп.

Ошибка другого рода в файле теста (опечатка, неверный тип, неверный заголовок проекта) — корневая нить исправляет тест так, чтобы его текст по-прежнему совпадал с шагом 1, и повторяет прогоны с A. Ошибки вне файлов шага 1; провал другого теста в прогоне B или C; в прогоне B любой из шести тестов `P5G ` со статусом `Passed` или `Skipped`; в прогоне C любой из шести тестов `P5G ` со статусом, отличным от `Passed`; в прогоне D другой код выхода или другой холст; в прогоне E другой код выхода или другая причина — блок `## Q-P5GT-02` с этими строками и стоп. Ожидание теста под код не подгоняй: тест, который требует правки текста шага 1, — тоже `## Q-P5GT-02`.

## Шаг 3. Заморозка — корневая нить

`sha256sum tests/utils/test_UiAuditArguments.cpp tests/CMakeLists.txt tests/ui_audit/ui_audit_runtime_support.py tests/ui_audit/ui_audit_list_and_scales.py tests/ui_audit/ui_audit_unknown_scene.py tests/ui_audit/ui_audit_main_menu_png.py > .tmp/p5gt/tests.sha256`. После этой команды файлы тестов не меняются.

Проверка: `git -c lfs.storage=$PWD/.tmp/p5gt/lfs status --short` выводит ровно три строки: ` M tests/CMakeLists.txt`, `?? tests/ui_audit/` и `?? tests/utils/test_UiAuditArguments.cpp`. Строки `__pycache__` вне `tests/ui_audit/` в выводе допустимы; другие строки — блок `## Q-P5GT-03` с выводом и стоп.

## Сдача

Последнее сообщение — блок `## DONE-P5GT | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- коды выхода прогонов A, B, C, D и E, их строки `error:`, вывод `grep -A3 "CMake Error"`, строки `ctest.log` из шага 2, вывод `grep` прогона D и по пять последних строк каждого лога прогона E (не больше 80 строк на прогон; если больше — первые 80 и их число);
- число проверок в новом файле Catch2 — вывод `grep -cE '\b(CHECK|CHECK_FALSE|REQUIRE)\(' tests/utils/test_UiAuditArguments.cpp`;
- содержимое `.tmp/p5gt/tests.sha256`;
- вывод `git status --short` из шага 3;
- список коммитов: один пункт — шесть файлов шага 3, сообщение на английском о приёмочных тестах ядра режима отладки интерфейса: перенос теста разбора аргументов форка на Catch2 и скрипты, которые запускают игру и проверяют каталог сцен, масштабы, неизвестную сцену и снимок главного меню; последняя строка сообщения — `Behavior changes: none`;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p5gt --size`; у `.tmp/p5gt` пометка `оставить — хэши тестов нужны исполнителю`. Папки `.tmp/out` и `.tmp/deps` созданы до этой задачи и в раздел не входят. Ничего не удаляй, кроме временных файлов прогонов B и C и папки `tests/ui_audit/__pycache__`.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:** раздел «Прочитать до работы» → шаг 1 → шаг 2 (прогоны A, B, C, D, E по очереди) → шаг 3 → сдача и стоп.
- **Параллельно:** шаги зависят друг от друга, параллельных дорожек нет.
- **Помощники:** один субагент `gpt-6-luna` `xhigh`, без вложенных: шаг 2 — команды сборки и запуска, временные файлы прогонов B и C и их уборка, выписка строк ошибок, строк `ctest.log` и логов прогонов D и E. Бриф дословно содержит раздел «Шаг 2», абзац «Комментарии в коде» и запрет менять файлы, кроме временных файлов прогонов B и C, папки `tests/ui_audit/__pycache__` и файлов в `.tmp/p5gt/`. Шаги 1 и 3, разбор ошибок и сдачу делает корневая нить.
- **Остановки:** только на `## DONE-P5GT` и на блоках `## Q-P5GT-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P5GT-04` и стоп.
- **Рамка правок:** `tests/utils/test_UiAuditArguments.cpp`, `tests/CMakeLists.txt`, папка `tests/ui_audit/`, временные файлы прогонов B и C и папка `.tmp/p5gt/`. Сборка пишет в `.tmp/out/` и `.tmp/deps/`, игра — в `.tmp/out/run/bin/`; это не правка.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=2d86ef51aef14ab0cfe146d96e8768450f1161cc5c1f859bbf13ba4b7ae869e7 -->
## Обязательно: правила исполнителя

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Без фоновых команд: после остановки исполнителя никто его не разбудит. Длинные прогоны — в переднем плане, с таймаутом до 30 минут.
- Git по договорённости с ревьюером. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ревьюер после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ревьюера.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не трогать, секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Временные файлы — только в отведённой временной папке, в репозиторий и в корень рабочей копии ничего временного не класть. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Удалять что-либо вне своей временной папки — только по правилу «Уборка»; чужое, общее и постоянное — не удаляешь. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. В `DONE` — раздел «Рабочие места»: каждый созданный путь, его размер (`du -sh`) и что это — доказательство (на него ссылаются DONE, PR или журнал) или промежуточное. Объекты сборки, ненужные для повторной проверки, удаляешь только по правилу «Уборка»; до `CLEAN-OK` пути задачи не удаляешь.
- Уборка (владелец). В DONE — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер, назначение и пометка: `удалить` или `оставить — <почему>`; доказательства — только `оставить`. Удаляешь только после ответа ведущего-ревьюера `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; если в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`. Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- **Чтение (владелец).** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по журналу: обрезанный вывод — не чтение.
- Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; помощникам цель не ставить.

## Вопросы и остановки

Каждое препятствие сверяй в таком порядке:

1. Подходит под список «`Q` и стоп» — `Q` и стоп, даже если оно подходит и под список «Без вопроса».
2. Иначе подходит под список «Без вопроса» — решай сам и работай дальше.
3. Иначе: без ответа идущий подпункт выполнить нельзя — `Q` и стоп; можно — неблокирующий вопрос: запиши его в сдачу и работай дальше по списку, не простаивай.

`Q` в любом другом пункте этих правил — тоже «`Q` и стоп».

**`Q` и стоп.**
- ответ требует правки вне рамки правок, правки промптов, норм, governance, контрактов или замороженных тестов (файл, assert, смысл проверки);
- удаление данных, сеть или установка пакетов;
- смена цели, рамки или критерия готовности; новый механизм; решение по продукту;
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в DONE;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса (владелец).** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи и журнала хода не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий (владелец); исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи — строго по порядку списка.
- Замечания ревьюера выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения; DONE — один на задачу, после REVIEW — новый DONE.
- Если исполнитель коммитит — незаконченное хранить в своей ветке WIP-коммитом, а не патчами во временной папке. Голый `git stash` не использовать: список stash общий для всех рабочих копий и сессий.
- Перенос и переформатирование кода — отдельным коммитом, изменение поведения — следующим. «Без изменения поведения» писать, только если это правда.
- Последняя строка сообщения коммита — `Behavior changes: …` со списком или `Behavior changes: none`. Называть и мелочи: запасной вариант, удалённое поле, удалённую настройку в тесте, изменённый предел.
- Заголовок не преувеличивает: «finish», «complete» — только если пункт закрыт целиком; остатки назвать в теле.

## Тесты

- Тест проходит путь пользователя через тот вход продукта, которым пользуется пользователь в сценарии: для интерфейса — события мыши и клавиатуры, для API — вызов API. Тестируемый код не подменять заглушками.
- Тест проверяет поведение, а не совпадение хэша или вывода с прошлой сборкой. Изображения сравнивать с эталоном с допуском из задания, а если в задании его нет — из действующего эталонного теста или конфигурации сравнения; ни один источник допуск не задаёт — `Q`.
- Асинхронный результат ждать по нему самому (нужное значение, запись, пиксель), а не по косвенному флагу.
- Нестабильный тест разбирать сразу, с логом и санитайзером, если он уже настроен в проекте. «Не воспроизвелось» проблему не закрывает: исполнитель перечисляет её в сдаче с логом, issue заводит ведущий.
- Тесты пишут только в свои временные папки; общее состояние (синглтоны, кэши) сбрасывать перед каждым тестом.
- Общие помощники тестов и константы — в одном месте, не копировать по файлам.
- Сливать в целевую ветку только ветку с зелёным CI на её последнем коммите; после слияния проверить CI целевой ветки и красной её не оставлять.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Отчёт владельцу

- Три пункта на языке владельца — простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Эти три пункта — часть DONE; отдельного отчёта владельцу не создавать.

<!-- /team-process:executor-rules -->
