# Сверка таблиц P12R

## Помощник 1 — fork-packaging.tsv и gallery.tsv

### 1. `.github/workflows/release.yml@9208dcf:24-27`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:.github/workflows/release.yml | sed -n '24,27p'
```

Вывод:

```text
jobs:
  prepare-release:
    name: Prepare draft release
    runs-on: ubuntu-latest
```

Итог: совпало.

### 2. `README.md@9208dcf:1`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '1p'
```

Вывод:

```text
# Dune II — The Maker RU/HD Remaster
```

Итог: совпало.

### 3. `README.md@9208dcf:10`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README.md | sed -n '10p'
```

Вывод:

```text
  <img src="docs/screenshots/main-menu.png" alt="Remastered main menu" width="100%">
```

Итог: совпало.

### 4. `README_AI.md@9208dcf:447`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:README_AI.md | sed -n '447p'
```

Вывод:

```text
### GitHub Release
```

Итог: совпало.

## Помощник 2 — workflows.tsv

### 5. `.github/workflows/build_manual.yml@d06f2fc:3-4`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:.github/workflows/build_manual.yml | sed -n '3,4p'
```

Вывод:

```text
on:
  workflow_dispatch:
```

Итог: совпало.

### 6. `.github/workflows/build_pr.yml@d06f2fc:145`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:.github/workflows/build_pr.yml | sed -n '145p'
```

Вывод:

```text
        uses: actions/upload-artifact@v4
```

Итог: совпало.

### 7. `.github/workflows/claude-code-review.yml@7eb119b:46`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:.github/workflows/claude-code-review.yml | sed -n '46p'
```

Вывод:

```text
        uses: anthropics/claude-code-action@v1
```

Итог: совпало.

### 8. `.github/workflows/build_master.yml@d06f2fc:13`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show d06f2fcd2a347182c3774fb96e9a85570405c489:.github/workflows/build_master.yml | sed -n '13p'
```

Вывод:

```text
  changes:
```

Итог: совпало.

## Помощник 3 — release-script.tsv

### 9. `create_release.sh@9208dcf:31`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:create_release.sh | sed -n '31p'
```

Вывод:

```text
cp resources/bin/data/*_hd4.dat bin/data
```

Итог: совпало.

### 10. `create_release.sh@7eb119b:50`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 7eb119b007c05f063fe6dacf2e93ae31ac135b33:create_release.sh | sed -n '50p'
```

Вывод:

```text
cp -p build/d2tm bin
```

Итог: совпало.

### 11. `packaging/WINDOWS_README.txt@9208dcf:8`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/WINDOWS_README.txt | sed -n '8p'
```

Вывод:

```text
The required MinGW and SDL2 DLLs are included in this platform archive.
```

Итог: совпало.

### 12. `packaging/RELEASE_NOTES.md@9208dcf:33-35`

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:packaging/RELEASE_NOTES.md | sed -n '33,35p'
```

Вывод:

```text
The common archive includes the bilingual campaigns, HD4 graphics,
fonts and the refreshed music pools. Existing `settings.ini`, `music` and
`saves` directories should be backed up before updating an older installation.
```

Итог: совпало.
