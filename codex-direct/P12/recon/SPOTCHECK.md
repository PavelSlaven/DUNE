# Сверка разведки П12 (Haiku)

Источник фактов: `RECON.md` и таблицы `fork-packaging.tsv`, `workflows.tsv`, `release-script.tsv`, `gallery.tsv` в этой папке. Номер строки таблицы — номер строки TSV-файла (строка 1 — заголовок). Ревизии: FORK1 `9208dcf5a358f40afd95c99480e4e09f781ed566`, PORT `7eb119b007c05f063fe6dacf2e93ae31ac135b33`, UP1 `d06f2fcd2a347182c3774fb96e9a85570405c489`.

## Факт 1

- Таблица: `fork-packaging.tsv`, строка 2 (`.github/workflows/build_pr.yml`).
- Утверждение: триггер `on: pull_request` (ссылка `build_pr.yml@9208dcf:3-4`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:.github/workflows/build_pr.yml | sed -n '3,4p'`
- Вывод:
```
on:
  pull_request: {}
```
- Итог: совпало.

## Факт 2

- Таблица: `fork-packaging.tsv`, строка 3 (`.github/workflows/release.yml`).
- Утверждение: триггеры push тегов `v*` и `workflow_dispatch` с обязательным `inputs.tag` (`release.yml@9208dcf:3-12`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:.github/workflows/release.yml | sed -n '3,12p'`
- Вывод:
```
on:
  push:
    tags:
      - "v*"
  workflow_dispatch:
    inputs:
      tag:
        description: Existing release tag (for example v0.8.0-ru-hd.1)
        required: true
        type: string
```
- Итог: совпало.

## Факт 3

- Таблица: `fork-packaging.tsv`, строка 4 (`CMakeLists.txt`).
- Утверждение: комментарий «These libraries are keg-only and not loaded into» (`CMakeLists.txt@9208dcf:54`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt | sed -n '54p'`
- Вывод:
```
            # These libraries are keg-only and not loaded into
```
- Итог: совпало.

## Факт 4

- Таблица: `fork-packaging.tsv`, строка 10 (`src/main.cpp`).
- Утверждение: первый комментарий начинается с `/*`, текст «Dune II - The Maker» (`src/main.cpp@9208dcf:1-3`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/main.cpp | sed -n '1,3p'`
- Вывод:
```
/*

  Dune II - The Maker
```
- Итог: совпало.

## Факт 5

- Таблица: `workflows.tsv`, строка 2 (UP1, `build_manual.yml`).
- Утверждение: триггер `workflow_dispatch` (`build_manual.yml@d06f2fc:3-4`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:.github/workflows/build_manual.yml | sed -n '3,4p'`
- Вывод:
```
on:
  workflow_dispatch:
```
- Итог: совпало.

## Факт 6

- Таблица: `workflows.tsv`, строка 4 (UP1, `build_pr.yml`).
- Утверждение: действие `actions/upload-artifact@v4` (`build_pr.yml@d06f2fc:145`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show d06f2fcd2a347182c3774fb96e9a85570405c489:.github/workflows/build_pr.yml | sed -n '145p'`
- Вывод:
```
        uses: actions/upload-artifact@v4
```
- Итог: совпало.

## Факт 7

- Таблица: `workflows.tsv`, строка 7 (PORT, `build_master.yml`).
- Утверждение: задание `Cleanup-Old-Releases` (`build_master.yml@7eb119b:201`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:.github/workflows/build_master.yml | sed -n '201p'`
- Вывод:
```
  Cleanup-Old-Releases:
```
- Итог: совпало.

## Факт 8

- Таблица: `workflows.tsv`, строка 9 (PORT, `claude-code-review.yml`).
- Утверждение: секрет `CLAUDE_CODE_OAUTH_TOKEN` (`claude-code-review.yml@7eb119b:48`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:.github/workflows/claude-code-review.yml | sed -n '48p'`
- Вывод:
```
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```
- Итог: совпало.

## Факт 9

- Таблица: `release-script.tsv`, строка 2 (FORK1, `create_release.sh`).
- Утверждение: `mkdir` создаёт корень пакета `bin` (`create_release.sh@9208dcf:8`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:create_release.sh | sed -n '8p'`
- Вывод:
```
mkdir bin
```
- Итог: совпало.

## Факт 10

- Таблица: `release-script.tsv`, строка 21 (FORK1, `create_release.sh`).
- Утверждение: копирование `resources/bin/data/*_hd4.dat` в `bin/data` (`create_release.sh@9208dcf:31`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:create_release.sh | sed -n '31p'`
- Вывод:
```
cp resources/bin/data/*_hd4.dat bin/data
```
- Итог: совпало.

## Факт 11

- Таблица: `release-script.tsv`, строка 56 (PORT, `create_release.sh`).
- Утверждение: копирование `resources/bin/campaign/sardaukar/*.*` в `bin/campaign/sardaukar` (`create_release.sh@7eb119b:24`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:create_release.sh | sed -n '24p'`
- Вывод:
```
cp resources/bin/campaign/sardaukar/*.* bin/campaign/sardaukar
```
- Итог: совпало.

## Факт 12

- Таблица: `release-script.tsv`, строка 81 (FORK1, `packaging/RELEASE_NOTES.md`).
- Утверждение: README говорит, что общий архив содержит двуязычные кампании, графику HD4, шрифты и обновлённые пулы музыки (`packaging/RELEASE_NOTES.md@9208dcf:33-35`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/RELEASE_NOTES.md | sed -n '33,35p'`
- Вывод:
```
The common archive includes the bilingual campaigns, HD4 graphics,
fonts and the refreshed music pools. Existing `settings.ini`, `music` and
`saves` directories should be backed up before updating an older installation.
```
- Итог: совпало.

## Факт 13

- Таблица: `gallery.tsv`, строка 2 (`README.md`).
- Утверждение: ссылка на `docs/screenshots/main-menu.png` (`README.md@9208dcf:10`).
- Команда: `git -C C:/Users/Slaven/Projects/DUNE show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '10p'`
- Вывод:
```
  <img src="docs/screenshots/main-menu.png" alt="Remastered main menu" width="100%">
```
- Итог: совпало.

## Факт 14

- Таблица: `gallery.tsv`, строка 4 (`docs/screenshots/house-selection.png`).
- Утверждение: размер блоба 4019933 байт.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:docs/screenshots/house-selection.png`
- Вывод:
```
4019933
```
- Итог: совпало.

## Факт 15

- Таблица: `gallery.tsv`, строка 6 (`docs/screenshots/ordos-briefing.png`).
- Утверждение: размер блоба 4098230 байт.
- Команда: `git -C C:/Users/Slaven/Projects/DUNE cat-file -s 9208dcf5a358f40afd95c99480e4e09f781ed566:docs/screenshots/ordos-briefing.png`
- Вывод:
```
4098230
```
- Итог: совпало.

Итог: совпало 15 из 15
