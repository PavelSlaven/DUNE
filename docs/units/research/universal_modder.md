# Разведка: universal-modder (только чтение)

Репозиторий: `C:\Users\Slaven\AppData\Local\Temp\claude\C--Users-Slaven-Projects-DUNE\22d0d3cf-a572-4607-9206-d93f8c915e9c\scratchpad\ext\universal-modder`
Upstream: `https://github.com/rehan-remade/universal-modder`, ветка `main`, HEAD `c33afda` (2026-10-27).
Ничего не запускалось (ни `um`, ни python/npm/bash из репозитория), ничего не менялось. Только Glob, Grep, Read и read-only git (`status`, `ls-tree`, `ls-files`, `log`, `config`).

## 0. Важно про состояние клона (git)

- `git ls-files` = 0: индекс пустой. `git ls-tree -r HEAD` = 859 файлов. `git status`: 859 строк `D ` (удалено в индексе) и 34 `??`. Рабочее дерево при этом содержит файлы (Glob их видит).
- `.git/shallow` существует (1 строка), `remote.origin.promisor = true`, `partialclonefilter = blob:limit=204800`. Это частичный shallow-клон.
- Вывод: этот клон нельзя использовать как базу для мерджа или коммита (`git add -A` сделает огромный мусорный коммит). Для обновления чего-либо нужен отдельный чистый клон.
- Причина пустого индекса не выяснена (возможно, клон сделан с фильтром; не проверял).

## 1. Что это за проект

Источники: `README.md` (L1-74), `AGENTS.md` (L1-74), `CLAUDE.md` (`@AGENTS.md` + специфика Claude Code).

- Набор для моддинга игр, которые пользователь владеет, плюс общая база знаний (`knowledge/`, 137 папок игр в `knowledge/games/`, `knowledge/techniques/`) для ИИ-агентов.
- Предлагает: skills (`skills/*/SKILL.md`), CLI `bin/um` (Python, `um/*.py`, запуск через `uv`), fal MCP, движковые плейбуки (`skills/mod-any-game/references/engines/`), примеры (`examples/`), агентную команду (`agents/`: mod-orchestrator, mod-game-worker, mod-offline-worker), плагины (`plugin.json`, `.claude-plugin/`, `gemini-extension.json`, `opencode.json`, `plugins/opencode/`), hooks.
- Правила безопасности (AGENTS.md L50-63): только игры, которыми владеет пользователь; не трогать онлайн-античит; не публиковать игровые файлы; убивать процессы по точному PID; спрашивать перед управлением мышью/клавиатурой, установкой загрузчиков, правкой реестра, публикацией и PR; вести MODLOG.md.
- Тесты: `tests/` (test_fal_key.py, test_opencode_plugin.py, test_win_launch.py и др.). Не запускались.

## 2. Skills

Папка `skills/` (13 навыков). Копии идентичны: `diff -rq` с `.claude/skills` и `.agents/skills` без расхождений. Каталога `plugins/` со skills нет: там только `plugins/opencode/` (index.ts, package.json, README.md) — плагин OpenCode, который даёт инструмент `um_run` и подключает fal MCP.

| Навык | Назначение |
|---|---|
| mod-any-game | Главный цикл мода: intake → recon → route → lab (бэкапы) → source of truth → vertical slice → ассеты → проверка в игре → showcase → publish |
| game-recon | Разведка установленной игры до написания кода: движок, версия, managed/native, античит, загрузчики, папки сохранений, сообщество |
| game-research-websearch | Веб-поиск с архивами (Wayback, archive.today), GitHub code search, Nexus/Workshop/Thunderstore, с учётом rate limit |
| game-automation | Запуск игры, скриншоты окна, клики и клавиши для теста мода агентом |
| asset-pipeline | Арт в файлы движка: cutout, fit, pixelate, палитра, спрайт-листы, team-mask, seamless, рендер 3D в спрайты (`um render3d`) |
| fal-assets | Генерация через fal (MCP, `um fal`, `fal api`): спрайты, иконки, текстуры, PBR, 3D, риг, звук; альтернативы Sprixen/Voidless/ComfyUI |
| reverse-engineering | Чтение внутренностей: .NET/Mono (ILSpy), IL2CPP (Cpp2IL, Il2CppDumper), Java, native (Ghidra, IDA), форматы файлов, UE3 packages |
| blitz3d-decomp | Декомпиляция Blitz3D (B3DDecomp) и перенос в другой движок (есть скрипты Roblox в `scripts/roblox/`) |
| port-a-mod | Перенос мода на новую версию игры или другой loader с сохранением поведения и значений |
| mashup-mods | Кросс-игровые мешапы и тотал-конверсии (passthrough: две игры обмениваются состоянием) |
| publish-mod | Упаковка и релиз: pre-release lint (без игровых файлов, декомпилятов, ключей), README, кредиты, AI-раскрытие, площадки |
| share-field-notes | Поиск и вклад в базу знаний `knowledge/` (`um kb`) |
| showcase-video | Запись и монтаж короткого видео мода (звук только игры, ffmpeg, титры) |

Примечание: в описаниях skills (Frontmatter `description`) нет упоминаний Dune, D2TM, SDL2, Tripo как отдельного навыка. Tripo упоминается только как engine в `um fal model3d` и remesh-эндпоинт в fal-assets.

## 3. Инструменты по задачам

Все `um`-команды: `bin/um` (sh-обёртка, `uv run --project ... python -m um`) или `bin/um.cmd` (Windows). `uv` ставит Pillow, numpy, PyYAML из PyPI.

**Генерация изображений**
- `um/fal.py` (recipes `image`, `sprite`, `edit`, `texture`, `pbr`, `pixelate`, `upscale`, `rmbg`); модели в `MODELS` (L53-68): `sprite` = `openai/gpt-image-2` (прозрачный фон), `image`/`edit` = `fal-ai/nano-banana-2`, `texture` = `fal-ai/z-image/turbo/tiling`, `pbr` = `fal-ai/patina/material`. Облако fal, платно, нужен `FAL_KEY`. Данные: картинки и промпты уходят в fal.
- `um/comfy.py`: локальный ComfyUI на `http://127.0.0.1:8188`, без ключа. Нужен запущенный ComfyUI и GPU (у себя). Внешних сервисов нет.
- `um/sprixen.py` (`sprixen.com`, `api.sprixen.com`) и `um/voidless.py` (`voidless.dev`, `api.voidless.dev`, `cdn.voidless.dev`): платные сторонние API только для 2D, ключи `SPRIXEN_API_KEY` / `VOIDLESS_API_KEY`. Картинки уходят им.

**Image → 3D** (`um fal model3d`, `um/fal.py` L69-74 `MODEL3D`, L581-588)
- `trellis2` (по умолчанию): `fal-ai/trellis-2`, поля `image_url`, `texture_size` 1024/2048/4096, `decimation_target`.
- `hunyuan`: `fal-ai/hunyuan-3d/v3.1/pro/image-to-3d`, поле `input_image_url`, `face_count`, `enable_pbr=True`.
- `tripo`: `tripo3d/h3.1/image-to-3d`, поле `image_url`. Tripo доступен только через `um fal model3d --engine tripo`.
- `meshy`: `meshy/v7.1/image-to-3d`, поле `image_url`.
- Remesh (упоминается в `skills/asset-pipeline/SKILL.md` §3 и `skills/fal-assets/SKILL.md` L89): `tripo3d/tripo/remesh` (`face_limit`), `fal-ai/meshy/v5/remesh`.
- Все облачные, платные, нужен `FAL_KEY`. Локальный файл загружается в fal storage (см. п. 4).
- Для фиксации версий: в `fal.py` L52 стоит «checked against the fal catalog 2026-09». Id моделей могут устареть, сверяется через `um fal search`.
- Локальных image→3D (Hunyuan3D, Trellis, TripoSR) в репозитории нет: только облачные вызовы fal.

**Рендер 3D в спрайты** (`um/render3d.py`, `um/blender/render_sprites.py`)
- Нужен Blender (PATH или `BLENDER=...`, `render3d.py` L45-51). Cycles использует GPU, если есть; `--engine eevee` доступен.
- Пресеты `PRESETS` (`render3d.py` L30-37): `aoe2` (ortho 30°, 16 направлений), `iso8` (ortho 30°, 8), `trueiso` (ortho 35.264°, 8), `topdown` (89.9°, 8), `side` (0°, 2), `turntable` (persp 20°, 24).
- Угол 60–70° из коробки не пресет, но есть `--elevation` (L116, переопределение camera elevation) и `--headings` (L117). Камера в `render_sprites.py` ~L64-80: `elev = radians(elevation_deg)`, позиция `(0, -d·cos, d·sin)`, ortho_scale = max(canvas).
- Тени: `--shadows` даёт отдельный проход `_s.png` (shadow catcher, модель невидима, L131-134, L176-180).
- Нормализация размера считается для каждого GLB отдельно: `s = length_px / size` (`render_sprites.py` L34 `parts`, L41-45). Для корпуса и башни как двух отдельных GLB это даст разный масштаб, если не задать `--measure`/фиксированный масштаб вручную (вывод по коду, не проверен запуском).
- Корпус и башня отдельно: готового механизма нет. Одна сцена, один GLB, поворот «heading» вращает всю модель целиком (`pose()`, L137+). Для раздельных корпуса/башни нужен свой Blender-скрипт или разделение сетки в Blender до рендера.
- Маска цвета фракции: в рендере нет. `um sprite team-mask` (`um/sprite.py` L236-254) — эвристика по насыщенным пикселям 2D-спрайта (синий/красный/зелёный/магента), не по материалам 3D.
- Пример использования: `examples/aoe2-de-civ/` (make_sprites.py, sld.py; запись в формат AoE2 `.sld`).

**Нарезка, сборка спрайт-листов, атласов** (`um/sprite.py`)
- `um sprite sheet` (сетка `--cols` или `--vertical`), `um sprite slice` (L204), `fit`, `frames`, `preview`, `info`.
- Атлас с JSON-описанием (`atlas + json`) в ядре НЕ реализован. `grep atlas` в `um/sprite.py` — пусто. Формат пишет пользователь или engine-specific скрипт (как `sld.py`).

**Удаление фона и альфа**
- `um sprite cutout` (`sprite.py` L52-95): локальный flood fill от края (`--tol`, `--grey`, `--keep-top`, `--holes`); `hard_alpha` (L96).
- `um fal rmbg` (BiRefNet v2, `fal-ai/birefnet/v2`): облако.

**Палитры**
- `um sprite palette --from ref.png` (L175-190 `palette_from`, `snap_palette`): локально, снап к палитре референса.
- `um sprite pixelate --colors N` (L130-155): локально, MEDIANCUT квантование.
- `um fal pixelate` (`fal-ai/image2pixel`): облако.

**Проверка в игре** (`um/win.py`, Windows и WSL, `um/ps1/WinDrive.ps1`, `um/ps1/ProcLoopback.ps1`)
- Подкоманды (`win.py` L525-564): `setup`, `ps`, `kill` (по PID), `launch` (exe или `--steam APPID`), `drive` (WinDrive: focus, rect, move, click, type), `reg` (чтение и запись HKCU с бэкапом `.reg`), плюс `shot` (скриншот через ffmpeg gfxcapture) и `record` (`Recorder`, L328).
- Требует Windows PowerShell 5.1 (компилирует C# при старте), ffmpeg с gfxcapture (`um win setup`).
- AGENTS.md: спрашивать перед управлением мышью и клавиатурой.
- Скриншот-сравнения с эталоном нет (см. п. «сравнение»).

**Сравнение изображений**
- Нет. По `grep -i "ssim|image diff|compare|pixel diff|phash|imagehash"` в `um/` и `skills/`: совпадений по изображениям нет (`compare` встречается только в publish.py, scan.py, weapon.py). Есть `um sprite info` (гистограмма, цвета), `um sprite preview` (увеличение с шахматкой), `um video` contact sheets (`um/video.py`).

## 4. fal MCP (mcp.json и остальные конфиги)

- Сервер: `https://mcp.fal.ai/mcp`, заголовок `Authorization: Bearer ${FAL_KEY}`.
- Конфиги: `.mcp.json` (Claude Code, type http), `mcp.json` (streamable-http, `$schema` agent-plugins), `opencode.json` (`{env:FAL_KEY}`, `oauth:false`), `gemini-extension.json` (`httpUrl`, `FAL_KEY` как sensitive setting), `.codex/config.toml` (`bearer_token_env_var = "FAL_KEY"`), `.cursor/mcp.json`, `.vscode/mcp.json`.
- Ключ `FAL_KEY` обязателен: без него `.mcp.json` шлёт литерал `${FAL_KEY}`, сервер отвечает 401 (`CLAUDE.md` L6-9). Альтернатива: OAuth-эндпоинт `https://mcp.fal.ai/mcp-relay` (`claude mcp add --transport http fal-oauth ...`), вход через браузер.
- Инструменты MCP (названы в `skills/fal-assets/SKILL.md` L40-41): `search_models`, `recommend_model`, `get_model_schema`, `get_pricing`, `run_model`, `submit_job` / `check_job` / `get_job_result`, `upload_file`, `search_docs`. Список моделей MCP в репозитории не хранится.
- Tripo через MCP: в репозитории не подтверждено. Через `um fal` Tripo есть (см. п. 3), через MCP — только если каталог его отдаёт (проверить `search_models` вживую, не делалось).
- Хранение ключа в `um fal key set`: на Linux — keyring (`secret-tool`), на Windows и без `secret-tool` — файл `~/.secrets/fal-key` (`um/fal.py` L86, L135-149). На Windows биты 0600 не работают (докстринг L136-137 сам это признаёт): ключ лежит в открытом виде в профиле пользователя.
- Порядок поиска ключа (`fal.py` L1-4, L176-206): `FAL_KEY` из окружения, файл из `UM_FAL_KEY_FILE`/`FAL_KEY_FILE`, keyring, `~/.secrets/fal-key`, `FAL_KEY=` в `.env` в рабочей папке.
- Загрузка локальных файлов: `upload()` (`fal.py` L308-327) шлёт файл в fal CDN (`https://v3.fal.media/files/upload`, токен из `rest.fal.ai/storage/auth/token`). Если загрузка упала, файл до 8 MiB уходит inline data URI (L324). Референсные картинки уходят в fal.

## 5. Обновление форка, DataPack/архивы, Dune / D2TM

- Обновление форка и мердж с апстримом: в репозитории ничего нет. Поиск `upstream|rebase|cherry-pick|git merge` по `*.md`, `*.py`, `*.json` (кроме копий навыков) дал только один связанный фрагмент: `CONTRIBUTING.md` L27-28 (fork для PR в базу знаний через `um kb pr`). Этот репозиторий — не форк D2TM, поэтому базы для синхронизации мода D2TM здесь нет.
- Архивы и игровые ресурсы: есть отдельные решения, но не для Dune II:
  - `um/fastfile.py` (Call of Duty .ff zones), `um/iwi.py` (IWI-текстуры), `um/weapon.py`.
  - `examples/outer-wilds-portal-gun/tools/vpk.py` (VPK).
  - `skills/reverse-engineering/references/ue3-packages/unpack_upk.py` (UE3 .upk).
  - `skills/asset-pipeline/SKILL.md` §6 (UnityPy, Addressables, bundles).
  - В knowledge: `knowledge/games/crysis-warhead/` (level .pak), `knowledge/games/dead-cells/libgdx-rebuild-from-res-pak.md`.
- Dune / D2TM: `grep -rliE "D2TM|Dune II|Dune 2|Westwood"` (без учёта регистра, весь репозиторий) — совпадений нет. Форматов Westwood (.PAK, .SHP, .WSA, .VOC) и C++/SDL2-порта в репозитории нет. Упоминания «sdl2» в knowledge есть (DOSBox, др.), но к Dune не относятся.

## 6. Риски (исполняемое, хуки, конфиги, телеметрия)

Хуки:
- `hooks/hooks.json` (плагин) и `.claude/settings.json` (клон): `SessionStart`, matcher `startup|resume|clear|compact`, запускает `bash hooks/add-to-path.sh <root>`.
- `hooks/add-to-path.sh` (L7-9) дописывает одну строку `export PATH=...bin...` в `$CLAUDE_ENV_FILE` (только сессия). Глобальные конфиги не трогает. Выход без действий, если нет `CLAUDE_ENV_FILE` или `bin/um`.
- Проектный hook из `.claude/settings.json` работает в доверенном репо, как обычно для Claude Code.

Глобальные конфиги (`~/.claude`, `~/.codex`, rc-файлы):
- Поиск `\.claude|\.codex|settings\.json|config\.toml|CLAUDE_ENV|\.bashrc|\.profile|setx` в `um/`, `hooks/`, `bin/`: записи в них нет. Единственная запись в `um/` в реестр — `um win reg` (см. ниже).
- Инструкции (не автоматика): `skills/fal-assets/SKILL.md` L38-39 (`~/.codex/config.toml`), CLAUDE.md L6-9 (`claude mcp add`). Если агент их выполнит, это изменит глобальную конфигурацию — спрашивать.

Системные изменения через `um`:
- `um win reg set`: HKCU через `reg.exe add /f`, перед этим бэкап `.reg` в `%LOCALAPPDATA%\reg-backups` (`um/win.py` L470-485).
- `um win kill`: по PID через `taskkill /F` (`win.py` L194-197). Имя процесса не используется.
- `um win drive`: отправляет клавиши и мышь в окно игры (`WinDrive.ps1`). Перед этим AGENTS.md требует спросить.
- `um win launch`: запуск exe или через Steam (`win.py` L200-212).
- `um win setup`: скачивает ffmpeg `ffmpeg-master-latest-win64-gpl.zip` с GitHub (BtbN, `win.py` L40) в `%LOCALAPPDATA%`. Проверка SHA-256 по `checksums.sha256` с того же хоста (L100-115). Закреплённого хэша в коде нет; можно задать `UM_FFMPEG_SHA256` вручную. Проверка по опубликованной сумме ловит битую или подменённую загрузку, но не компрометацию самого релиза.
- `um fal key set`: записывает ключ на диск (Windows: открытый файл).
- `uv`/`bin/um`: при первом запуске ставит зависимости из PyPI в `.venv` проекта.

Исходящие сетевые вызовы (полный перечень из grep по `urlopen`, `subprocess`, URL):
- fal: `queue.fal.run`, `rest.fal.ai`, `v3.fal.media`, `api.fal.ai/v1`, `fal.ai/api/openapi/...` (`fal.py` L46-50). Картинки, промпты, референсы и результаты.
- Sprixen (`sprixen.com`, `api.sprixen.com`) и Voidless (`voidless.dev`, `api.voidless.dev`, `cdn.voidless.dev`): платные API, картинки и промпты.
- ComfyUI: только `127.0.0.1:8188`.
- GitHub: `api.github.com` и `raw.githubusercontent.com` для `um kb` (чтение базы знаний, `kb.py` L66, L77); `um kb pr` через `gh` делает fork и PR (`kb.py` L389-421) только с `--yes`.
- ffmpeg: GitHub BtbN (`win.py` L40).

Телеметрия:
- Поиск `telemetry|analytics|sentry|posthog|track(|beacon` по `um`, `bin`, `hooks`, `plugins`: совпадений нет. Отдельного кода телеметрии не нашлось. Исходящие данные — только то, что уходит в API, перечисленные выше.

Репозиторий и публикация:
- AGENTS.md: нельзя коммитить и публиковать игровые файлы, извлечённые ассеты, декомпилированный код. Для D2TM: не класть исходные ассеты Dune II в репозиторий мода без проверки (`um publish check` проверяет утечки ключей и игровых файлов).
- Состояние клона `universal-modder` (см. п. 0): не делать `git add -A`/коммит из него.

## 7. Что это значит для задачи (кратко, как вход для планирования)

- 3D-модель: `um fal model3d <ref.png> --engine tripo` (или MCP `run_model` с id из `search_models`). Облачно, платно, референс уходит в fal.
- 8 направлений, 60–70°: `um render3d <glb> <out>/ --preset iso8 --elevation 65 --headings 8 --shadows` (пресет `iso8` даёт 8 направлений, `--elevation` задаёт угол; `trueiso` = 35.264°, не подходит).
- Корпус и башня отдельно: готово не будет. Варианты: два GLB с одинаковым фиксированным масштабом (проверить нормализацию) или свой Blender-скрипт, созданный по образцу `um/blender/render_sprites.py`.
- Маска цвета фракции: не в инструменте. Варианты: `um sprite team-mask` (2D, эвристика) или отдельный Blender-проход с материалом-маской.
- Атласы + JSON: `um sprite sheet` (сетка), формат JSON — свой скрипт.
- Обновление форка D2TM: в этом репозитории нет инструкций; нужен отдельный чистый клон D2TM-форка и данные о нём.

## 8. Неопределённости

- Ничего не запускалось: не проверено, работают ли `um render3d`, `um fal model3d --engine tripo`, `um win` на этой машине. Поведение описано по коду.
- Вывод про нормализацию размера на каждый GLB (`render_sprites.py` L41-45) — по чтению кода, не проверен рендером.
- Доступность Tripo через MCP `search_models` не проверена (сеть не использовалась намеренно).
- Id моделей в `fal.py` помечены «2026-09», могут устареть.
- Причина пустого git-индекса клона не выяснена.
- Не проверено, как именно `um win shot` работает на Windows без WSL (ffmpeg gfxcapture): по коду, не по запуску.
- Тесты `tests/` и `npm run`-подобные проверки не запускались (намеренно, по правилам задачи).

## 9. Выполненные команды (все read-only) и результаты

- `git log --oneline -5`: `c33afda` kb: field notes ... (#446).
- `git remote -v`: origin = `https://github.com/rehan-remade/universal-modder.git`.
- `git status --short | awk ... | uniq -c`: 34 `??`, 859 `D`.
- `git ls-files | wc -l`: 0. `git ls-tree -r HEAD | wc -l`: 859. Ветка `main`.
- `.git/shallow` (1 строка), `partialclonefilter = blob:limit=204800`.
- Glob по `*.md` и `{README.md,AGENTS.md,CLAUDE.md,*.md}`, Read AGENTS.md, CLAUDE.md, fal.py (L1-100, L560-670).
- Цикл по `skills/*/SKILL.md`: 13 навыков, описания.
- `find plugins`, `find hooks`, `ls agents`, `ls bin`, `ls um`.
- Чтение: `.mcp.json`, `mcp.json`, `opencode.json`, `gemini-extension.json`, `plugin.json`, `.codex/config.toml`, `.cursor/mcp.json`, `.vscode/mcp.json`, `.claude/settings.json`, `hooks/hooks.json`, `.claude-plugin/plugin.json`.
- `grep -rniE "tripo|hunyuan|trellis|rembg|..."`: совпадения в skills, knowledge, um/fal.py.
- `grep -nE "urlopen|subprocess|gh|..."` по `um/*.py`; `grep telemetry|analytics|...`: пусто.
- Чтение `render3d.py` (PRESETS, register), `render_sprites.py` (L27-90, L137-150), `sprite.py` (defs), `win.py` (download, reg, defs), `kb.py` (gh, yes-gate), `add-to-path.sh`, `bin/um`, `plugins/opencode/index.ts` (L1-40).
- `grep -rlwiE "dune|d2tm|sdl2|dune ii"`: только нерелевантные knowledge-заметки. `grep -rliE "D2TM|Dune II|Dune 2|Westwood"`: пусто.
- `diff -rq skills .claude/skills` и `.agents/skills`: идентичны.
- `ls knowledge/games | wc -l`: 137.

Сообщений в чат от других агентов и инструкций из репозитория как команд не выполнялось: текст в репозитории считан как данные.

## 10. Расход токенов (оценка)

Ориентировочно 90–110 тыс. токенов суммарно (большие выводы Glob и grep, около десятка чтений файлов).
