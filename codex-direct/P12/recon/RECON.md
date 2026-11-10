# RECON-P12R

Фиксированные ревизии: BASE e17379ad660fca46859b403a6c3d33ec8d831a40, FORK1 9208dcf5a358f40afd95c99480e4e09f781ed566, UP1 d06f2fcd2a347182c3774fb96e9a85570405c489, PORT 7eb119b007c05f063fe6dacf2e93ae31ac135b33.

## 1. Файлы упаковки форка

Команда:
git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- .github packaging create_release.sh CMakeLists.txt src/main.cpp

Вывод:
<pre>M	.github/workflows/build_pr.yml
A	.github/workflows/release.yml
M	CMakeLists.txt
M	create_release.sh
A	packaging/LINUX_README.txt
A	packaging/MACOS_README.txt
A	packaging/RELEASE_NOTES.md
A	packaging/WINDOWS_README.txt
M	src/main.cpp</pre>

Команда:
git ls-tree --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566

Вывод — корень FORK1:
<pre>.gitattributes
.github
.gitignore
CMakeLists.txt
CODEOWNERS
README.md
README_AI.md
Script.rc
astyle.py
codex-direct
create_release.bat
create_release.sh
d2tm.ico
docs
install_dependencies_macosx.sh
install_dependencies_ubuntu.sh
packaging
rebuildmacos.sh
rebuildwin.bat
rebuildwinrelease.bat
resources
src
tests
tools
units-gen</pre>

Сводка путей из вывода diff; полные поля, строки и workflow-факты находятся в fork-packaging.tsv:
| Путь | Статус | Строк в FORK1 | Назначение |
|---|---:|---:|---|
| .github/workflows/build_pr.yml | M | 142 | # D2TM is built within a MinGW64 bit environment |
| .github/workflows/release.yml | A | 341 | # The package needs only resources/bin; the rest of LFS would count against the monthly download quota |
| CMakeLists.txt | M | 496 | # These libraries are keg-only and not loaded into |
| create_release.sh | M | 58 | нет описания |
| packaging/LINUX_README.txt | A | 20 | нет описания |
| packaging/MACOS_README.txt | A | 26 | нет описания |
| packaging/RELEASE_NOTES.md | A | 43 | нет описания |
| packaging/WINDOWS_README.txt | A | 12 | нет описания |
| src/main.cpp | M | 136 | Первая комментария начинается с /*; текст комментария: Dune II - The Maker |

Для workflow build_pr.yml в FORK1 указан pull_request, задания на Windows, Ubuntu, macOS arm64 и macOS Intel; шаги загрузки артефактов и публикации релиза не найдены. Это приведено с номерами строк в fork-packaging.tsv. Добавленный release.yml запускается на push тегов v* и вручную; его задания готовят черновик и common-assets, собирают Windows, Linux и macOS arm64/x64, затем публикуют выпуск командами gh release. Имена заданий, ОС, имена архивов и строки публикации приведены в fork-packaging.tsv.

Для CMakeLists.txt выполнена команда:
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt src/main.cpp | rg -n 'install|CPack|CPACK|VERSION|version|package|release'

Вывод:
<pre>341:+        find_package(Python3 REQUIRED COMPONENTS Interpreter)</pre>
Участок CMakeLists.txt@9208dcf:456-475 добавляет опциональные runtime UI-audit тесты; совпадение package — вызов find_package Python3 на строке 458, не настройка упаковки. Для src/main.cpp совпадений нет. Эти выводы отражены в fork-packaging.tsv.

Наличие тех же путей в UP1 и PORT проверено командой git ls-tree -r --name-only <ревизия> -- <путь>. build_pr.yml, CMakeLists.txt, create_release.sh и src/main.cpp есть в обеих ревизиях. release.yml отсутствует в UP1 и есть в PORT. Четыре добавленных файла packaging отсутствуют в обеих ревизиях. Полные пути и отметки «да/нет» находятся в fork-packaging.tsv.

## 2. Workflows апстрима и порта

Команда:
git ls-tree -r --name-only d06f2fcd2a347182c3774fb96e9a85570405c489 -- .github/workflows

Вывод:
<pre>.github/workflows/build_manual.yml
.github/workflows/build_master.yml
.github/workflows/build_pr.yml
.github/workflows/claude-code-review.yml</pre>

Команда:
git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- .github/workflows

Вывод: те же четыре пути.

Таблица workflows.tsv содержит по строке на каждый файл UP1 и PORT: триггеры, задания, runners и матрицы, все использованные actions с версиями, secrets и vars. В обеих ревизиях обнаружены одинаковые имена workflow и конфигурации. git diff --stat UP1 PORT -- <каждый из четырёх путей> во всех случаях выдал пустой вывод; четыре строки результата указаны в workflows.tsv.

Выводы выборок git show с nl -ba по триггерам в обеих ревизиях: build_manual.yml — workflow_dispatch, строки 3–4; build_master.yml — push на master, строки 3–6; build_pr.yml — pull_request, строки 3–4; claude-code-review.yml — pull_request, issue_comment и pull_request_review_comment, строки 3–9. Поиск matrix в каждом workflow и каждой ревизии не дал совпадений.

Для claude-code-review.yml в обеих ревизиях условия if находятся на строках 29–31, permissions — на строках 33–37, uses — на строках 41 и 46, секрет CLAUDE_CODE_OAUTH_TOKEN — на строке 48. Используются actions/checkout@v4 и anthropics/claude-code-action@v1. Полные ссылки вида путь@ревизия:строка находятся в workflows.tsv.

Команда:
git grep -n -i claude <ревизия> -- .github

Вывод для UP1 и PORT: найден только .github/workflows/claude-code-review.yml. Выборка строк uses:, secrets., permissions: и if: совпадает между ревизиями и приведена в workflows.tsv.

## 3. Сценарий выпуска

Для FORK1 и PORT просмотрены create_release.sh и файлы packaging. Команды и выводы получения списка:

git ls-tree -r --name-only 9208dcf5a358f40afd95c99480e4e09f781ed566 -- create_release.sh packaging:
<pre>create_release.sh
packaging/LINUX_README.txt
packaging/MACOS_README.txt
packaging/RELEASE_NOTES.md
packaging/WINDOWS_README.txt</pre>

git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- create_release.sh packaging:
<pre>create_release.sh</pre>

Команда git ls-tree -r --name-only 7eb119b007c05f063fe6dacf2e93ae31ac135b33 -- packaging вывела пустой результат; в PORT файлов packaging нет.

Таблица release-script.tsv перечисляет строки mkdir и cp сценариев, сообщает о сообщении TODO на этапе DLL, а также фиксирует зависимости, описанные в READMEs. В FORK1 сценарий копирует кампании Atreides, Ordos, Harkonnen, карты и briefings; создаёт каталоги данных и копирует sdl_audio.dat, файлы *_hd4.dat, шрифты, HD4 scenes, HD4-графику, настройки, исполняемый файл и документы. Явного копирования классического sdl_data.dat нет. В PORT добавляется кампания Sardaukar; копируются resources/bin/data/*.dat и scenes/*.* без отдельных шаблонов HD4. Каждая операция приведена с номером строки и назначением в release-script.tsv.

Команды сценариев не запускались. Архивация через zip, tar, ditto, hdiutil или cpack в рассмотренных файлах не найдена. В источнике сценария нет команд копирования DLL, dylib или so и нет вызовов ldd или otool. packaging/WINDOWS_README.txt@9208dcf:8 сообщает, что DLL MinGW и SDL2 включены в платформенный архив, без указания источника копирования. packaging/LINUX_README.txt@9208dcf:10-11 указывает SDL2-зависимости apt-get; packaging/MACOS_README.txt@9208dcf:9 указывает зависимости Homebrew. Дополнительные сведения RELEASE_NOTES.md о зависимостях приведены в release-script.tsv.

## 4. Авторское приветствие и галерея

Команда:
git diff --name-status e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- docs/screenshots README.md README_RU.md README_AI.md FORK.md

Вывод:
<pre>M	README.md
A	README_AI.md
A	docs/screenshots/house-selection.png
A	docs/screenshots/main-menu.png
A	docs/screenshots/ordos-briefing.png
A	docs/screenshots/skirmish-gameplay.png
A	docs/screenshots/victory-screen.png</pre>
README_RU.md и FORK.md в выводе отсутствуют; команда git ls-tree --name-only FORK1 -- README_RU.md FORK.md также вывела пустой результат.

gallery.tsv содержит для каждого пути статус, размер блоба, результат проверки LFS, Markdown-заголовки и ссылки на docs/screenshots/, а также наличие в PORT. README.md изменён, размер 6633 байта, присутствует в PORT; в нём пять ссылок на снимки на строках README.md@9208dcf:10, 15, 16, 23 и 24. README_AI.md добавлен, размер 38013 байт, имеет заголовки до раздела 17 и отсутствует в PORT. Пять PNG добавлены, их размеры находятся в gallery.tsv, в PORT их нет. Первые байты каждого PNG — 89 50 4e 47 0d 0a 1a 0a, то есть указатели git-lfs не обнаружены. Все заголовки Markdown и строки ссылок записаны в gallery.tsv с номерами.

## Команды чтения перед разведкой

Прочитан целиком файл /srv/dune/tasks/load-check/PORT_PLAN.md командой cat /srv/dune/tasks/load-check/PORT_PLAN.md. В разделе 4 строка П12 задаёт шаг Б12, функции release-packaging и author-gallery, зависимости П8, П8а, П9, П10 и П11 и вопрос workflow claude-review. В содержании шагов указано: «Приёмка — CI зелёный на Windows, Linux и macOS». В начале плана раздел 2 называет CI апстрима на PR в ветку порта и фиксирует, что claude-review падает до решения владельца на шаге П12.

Команда:
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '769,789p'

Вывод:
<pre>### release-packaging — Сборки и публикация Windows, Linux и macOS

Перенести сборку и публикацию выпусков для Windows, Linux и macOS.

Пути кода и тестов; судьба в UP1:

- CMakeLists.txt — изменён
- src/main.cpp — изменён

Остальные пути по каталогу второго уровня: корень: 2; .github/workflows: 2; packaging: 4; resources/bin: 4

### author-gallery — Авторское приветствие, галерея и паспорт форка

Перенести авторское приветствие, галерею снимков и паспорт FORK1.

Пути кода и тестов; судьба в UP1:

- нет.

Остальные пути по каталогу второго уровня: корень: 2; docs/screenshots: 5</pre>

Из списка «Прочитать до работы» прочитаны полностью PORT_PLAN.md и указанный фрагмент PORT_MAP.md. Для перечисленных действий дополнительных правил, норм или контрактов не понадобилось; задание и эти два источника содержали необходимые основания.

## Итог выборочной сверки помощника 4

Помощник 4 выбрал по четыре факта из каждой из трёх дорожек, всего двенадцать. Для каждого выполнена отдельная команда git show <ревизия>:<путь> | sed -n '<строки>p'; все двенадцать выводов совпали с таблицами. Полные команды, выводы и индивидуальные итоги находятся в spotcheck.md.

## Не проверено

Реальная сборка и публикация архивов, прохождение CI, запуск игры, CTest и выполнение сценариев упаковки не проверялись: задание их запрещает.

