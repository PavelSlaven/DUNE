# B1 — сборка UP0 на Windows (ПК владельца)

Итог: UP0 `a51b97f15d0eee2d323a1737f140eb2cbd60973c` собирается на Windows через MSYS2 MINGW64 без правок кода, все тесты зелёные, игра доходит до главного меню.

## Окружение

MSYS2 поставлен через winget в `C:\msys64` (1,84 ГБ). Пакеты — ровно строка `install:` задачи `MSYS2` из `.github/workflows/build_pr.yml`.

| Пакет | Версия |
|---|---|
| `mingw-w64-x86_64-gcc` | 16.2.0-6 |
| `mingw-w64-x86_64-cmake` | 4.4.4-4 |
| `mingw-w64-x86_64-sdl3` | 3.4.18-1 |
| `mingw-w64-x86_64-sdl3-image` | 3.4.8-1 |
| `mingw-w64-x86_64-sdl3-mixer` | 3.2.4-1 |
| `mingw-w64-x86_64-sdl3-ttf` | 3.2.2-3 |
| `mingw-w64-x86_64-catch` | 3.16.1-1 |

MSYS2 обновляется непрерывно, поэтому версии SDL здесь новее закреплённых для Linux в `install_dependencies_ubuntu.sh`; CI апстрима для Windows ставит пакеты так же.

Отклонение от установки по умолчанию: `repo.msys2.org` и `mirror.msys2.org` обрывали загрузку, поэтому эти строки убраны из `C:\msys64\etc\pacman.d\mirrorlist.mingw` и `mirrorlist.msys`. Исходные файлы лежат рядом как `*.orig`.

## Сборка и тесты

Рабочая копия `C:\Users\Slaven\Projects\DUNE-up0` (git worktree на UP0, отделённый HEAD), каталог сборки `build\` (игнорируется git).

```bash
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -G "MinGW Makefiles"
cmake --build . -j8
ctest --output-on-failure
```

- сборка: код выхода 0, предупреждений и ошибок в логе нет;
- `ctest`: `100% tests passed out of 214`, общее время 8,72 с;
- `git status --short` в `DUNE-up0` после сборки пуст.

## Запуск

Рабочий каталог `build\run\bin` собран по `create_release.sh:13–56` (каталоги кампании, данные, сохранения, `game.ini`, `settings.ini`), туда скопирован `d2tm.exe`. DLL берутся из `C:\msys64\mingw64\bin` через `PATH`.

Игра открыла окно `Dune II - The Maker [unset]`, главное меню на снимке [up0-windows-menu.png](up0-windows-menu.png). После штатного закрытия окна код выхода 0, в `nlog.txt` строка 280:

```text
451|INFO|GAME|cGame::setState|Setting state from -1(=INITIALIZE) to 1(=MENU)||
```

Её пишет `src/game/cGame_logic.cpp:903–904`. В логе 190 строк INFO и 100 WARN (разбор `game.ini` и раскладки клавиш апстрима), строк ERROR нет.

Лог пишется буфером: при жёстком завершении процесса `nlog.txt` остаётся пустым, строка появляется только при штатном выходе.
