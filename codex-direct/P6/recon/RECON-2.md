# RECON-P6R-2

## Рабочие ревизии

`BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `UP1=d06f2fcd2a347182c3774fb96e9a85570405c489`, `PORT=0a33444e9032ef935dfe4cdde6bb622771484230`, `MAIN=62e1ff6585d8f1f047a3f983c63d990662e6afb6`. Перед командами Git выставлялся `PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`; Python — `/srv/dune/venv/bin/python`. Ревизии читались только по явным SHA.

## 1. Имена записей в HD4-паках

Формат индекса проверен по `git show PORT:src/utils/cPack.cpp | nl -ba | sed -n '33,37p;64,100p;103,124p;127,156p;160,164p'`. Вывод `src/utils/cPack.cpp@0a33444:33-37,64-100,103-124,127-156,160-164` задаёт: заголовок `D2TM`; `uint16` числа записей; по каждой записи — 40-байтовое имя, расширение 4 байта, `uint32` offset и `uint32` size; данные начинаются после заголовка и индексной таблицы. `getIndexFromName` возвращает расстояние записи от начала вектора, поэтому индексы начинаются с 0 (`cPack.cpp@0a33444:127-136`). Размер записи берётся из поля `fileSize` (`cPack.cpp@0a33444:86-99,154-156`).

OID и пути LFS объектов установлены командами:

```text
git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/data/sdl_data_hd4.dat
version https://git-lfs.github.com/spec/v1
oid sha256:781d3f7cea009d357d8b1236c11f681f6bbe831e8245bcb3c81ee46e3646a0c1
size 38474836

git cat-file -p 0a33444e9032ef935dfe4cdde6bb622771484230:resources/bin/data/sdl_data_hd4.dat
version https://git-lfs.github.com/spec/v1
oid sha256:e260cd4091532269adb0b4476b9e07d34493e330b1b29a4eeeecd9890b76fa83
size 38497548

git rev-parse --git-common-dir
/srv/dune/worktrees/u63/.git
```

Команда `ls -l /srv/dune/worktrees/u63/.git/lfs/objects/78/1d/781d3f7cea009d357d8b1236c11f681f6bbe831e8245bcb3c81ee46e3646a0c1 /srv/dune/worktrees/u63/.git/lfs/objects/e2/60/e260cd4091532269adb0b4476b9e07d34493e330b1b29a4eeeecd9890b76fa83` подтвердила наличие объектов размером соответственно 38,474,836 и 38,497,548 байт. Оба объекта прочитаны; пропуска по отсутствующему объекту нет.

Скрипт `.tmp/p6r/pack_index.py` разбирает оба объекта и записывает все записи в `.tmp/p6r/pack-fork.tsv` и `.tmp/p6r/pack-port.tsv`. Запуск `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; /srv/dune/venv/bin/python .tmp/p6r/pack_index.py` вывел:

```text
fork: oid=sha256:781d3f7cea009d357d8b1236c11f681f6bbe831e8245bcb3c81ee46e3646a0c1; bytes=38474836; records=241; tsv=.tmp/p6r/pack-fork.tsv
port: oid=sha256:e260cd4091532269adb0b4476b9e07d34493e330b1b29a4eeeecd9890b76fa83; bytes=38497548; records=242; tsv=.tmp/p6r/pack-port.tsv
family=HV_* fork_records=0 port_records=0
  only_fork=нет
  only_port=нет
family=HOUSEVARIANT_* fork_records=0 port_records=0
  only_fork=нет
  only_port=нет
family=HOUSEMASK_* fork_records=0 port_records=0
  only_fork=нет
  only_port=нет
family=HM_HV_* fork_records=0 port_records=0
  only_fork=нет
  only_port=нет
family=HM_* (без HM_HV_*) fork_records=37 port_records=37
  only_fork=нет
  only_port=нет
family=BUILD_*_FLAG fork_records=12 port_records=12
  only_fork=нет
  only_port=нет
family=BUILDING_FOUNDATION_HD fork_records=0 port_records=0
  only_fork=нет
  only_port=нет
family=TERRAIN_*_VAR_* fork_records=24 port_records=24
  only_fork=нет
  only_port=нет
```

Каждый TSV имеет колонки `индекс`, `имя`, `размер_записи_байт`; полные записи находятся в указанных файлах. Сверка `pack-fork.tsv` и `pack-port.tsv` дала `only_fork_all_records=[]`, `only_port_all_records=['EXPLOSION_CARRYALL']`.

Корневая нить повторно проверила числа и различия независимыми командами:

```text
wc -l .tmp/p6r/pack-fork.tsv .tmp/p6r/pack-port.tsv
242 .tmp/p6r/pack-fork.tsv
243 .tmp/p6r/pack-port.tsv

awk -F '\t' 'NR>1 && $2 ~ /^HM_/ && $2 !~ /^HM_HV_/ { n++ } END { print n+0 }' .tmp/p6r/pack-fork.tsv
37
awk -F '\t' 'NR>1 && $2 ~ /^HM_/ && $2 !~ /^HM_HV_/ { n++ } END { print n+0 }' .tmp/p6r/pack-port.tsv
37

comm -13 <(cut -f2 .tmp/p6r/pack-fork.tsv | tail -n +2 | sort) <(cut -f2 .tmp/p6r/pack-port.tsv | tail -n +2 | sort)
EXPLOSION_CARRYALL
comm -23 <(cut -f2 .tmp/p6r/pack-fork.tsv | tail -n +2 | sort) <(cut -f2 .tmp/p6r/pack-port.tsv | tail -n +2 | sort)
```

## 2. Открытые методы `cPack` в PORT

Команда `git show PORT:src/utils/cPack.h | nl -ba` вывела перечисленные ниже публичные методы (`src/utils/cPack.h@0a33444:41-78`); назначение установлено по `git show PORT:src/utils/cPack.cpp | nl -ba`:

| Метод | Сигнатура и строка | Назначение по `cPack.cpp@0a33444` |
|---|---|---|
| `ReaderPack` | `ReaderPack(const std::string &filename);` — `src/utils/cPack.h:44` | Открывает пак, читает заголовок и индекс и загружает данные в память (`cPack.cpp:48-57`). |
| `~ReaderPack` | `~ReaderPack();` — `src/utils/cPack.h:45` | Очищает индекс записей (`cPack.cpp:59-62`). |
| `getData` | `SDL_IOStream *getData(unsigned int index);` — `src/utils/cPack.h:47` | Проверяет индекс и возвращает SDL-поток содержимого записи (`cPack.cpp:139-146`). |
| `getIndexFromName` | `int getIndexFromName(const std::string &fileId) const;` — `src/utils/cPack.h:49` | Ищет имя и возвращает индекс либо `-1` (`cPack.cpp:127-137`). |
| `displayPackFile` | `void displayPackFile();` — `src/utils/cPack.h:51` | Печатает имена, расширения, размеры и смещения записей (`cPack.cpp:148-158`). |
| `getNumberOfFiles` | `int getNumberOfFiles() const { return fileInPak; }` — `src/utils/cPack.h:53-55` | Возвращает число записей, прочитанное из заголовка. |
| `WriterPack` | `WriterPack(const std::string &packName);` — `src/utils/cPack.h:71` | Открывает файл пака для записи (`cPack.cpp:174-177`). |
| `~WriterPack` | `~WriterPack();` — `src/utils/cPack.h:72` | Очищает индекс добавленных записей (`cPack.cpp:179-182`). |
| `addFile` | `bool addFile(const std::string &fileName, const std::string &fileId);` — `src/utils/cPack.h:74` | Добавляет файл и его имя в будущий пак, возвращает успех операции (`cPack.cpp:184-204`). |
| `writePackFilesOnDisk` | `bool writePackFilesOnDisk();` — `src/utils/cPack.h:76` | Записывает заголовок, индекс и данные записей на диск (`cPack.cpp:282-289`). |
| `displayPackFile` | `void displayPackFile();` — `src/utils/cPack.h:78` | Печатает метаданные записей WriterPack (`cPack.cpp:242-252`). |

Открытого способа получить имя записи по индексу нет. `getIndexFromName` даёт обратное направление (`src/utils/cPack.h@0a33444:49`, реализация `src/utils/cPack.cpp@0a33444:127-137`); `fileInPack` — private (`cPack.h@0a33444:56-65,79-85`), а `getData(index)` возвращает только поток байтов (`cPack.h@0a33444:47`).

## 3. Методы рисования текстур в PORT

Команда `git show PORT:src/drawers/SDLDrawer.hpp | nl -ba` вывела методы рисования текстур/поверхностей (`src/drawers/SDLDrawer.hpp@0a33444:33-37`):

| Сигнатура | Строка |
|---|---|
| `void renderSprite(Texture *src, int x, int y, Uint8 opacity = 255);` | `src/drawers/SDLDrawer.hpp:33` |
| `void renderStrechSprite(Texture *src, cRectangle src_pos, cRectangle dest_pos, Uint8 opacity = 255);` | `src/drawers/SDLDrawer.hpp:34` |
| `void renderStrechFullSprite(Texture *src, cRectangle dest_pos, Uint8 opacity = 255);` | `src/drawers/SDLDrawer.hpp:35` |
| `void renderFromSurface(SDL_Surface *src, int x, int y, Uint8 opacity = 255, int density = 1);` | `src/drawers/SDLDrawer.hpp:36` |
| `void renderTexture(SDL_Texture *tex, int x, int y, int w, int h, Uint8 opacity = 255);` | `src/drawers/SDLDrawer.hpp:37` |

`renderStrechFullSprite` присутствует: `src/drawers/SDLDrawer.hpp@0a33444:35`.

## 4. Путь HD4-текстур юнитов и зданий в PORT

HD4-пак загружается как `GFXDATA` с плотностью 4: `src/context/ContextCreator.cpp@0a33444:59`, `kHd4AssetDensity=4` — `src/utils/Graphics.hpp@0a33444:58`. `DataPack::getSurface` ищет индекс записи и декодирует её `IMG_Load_IO` (`src/utils/cDataPack.cpp@0a33444:47-73`). `cInfoContextCreator.cpp@0a33444:186,202,260-262,1448-1449` помещает текстуры типов зданий и юнитов в игровые info-структуры.

Проверка формата записей PORT выполнена на фактическом LFS-объекте `sdl_data_hd4.dat`. Команда `git cat-file -p PORT:resources/bin/data/sdl_data_hd4.dat` дала OID `e260cd4091532269adb0b4476b9e07d34493e330b1b29a4eeeecd9890b76fa83`; команда `git rev-parse --git-common-dir` дала `/srv/dune/worktrees/u63/.git`. Скрипт распарсил 52-байтовый индекс по `src/utils/cPack.cpp@0a33444:64-99,160-164` и Pillow-проверкой установил режим всех PNG с именами `UNIT_*`/`BUILD_*`:

```text
UNIT_/BUILD_ PNG entries 92 modes {'RGBA': 92}
non-RGBA []
```

Выборочно проверенные записи: `UNIT_TANKBASE` и `UNIT_TANKTOP` — RGBA, 1024×128; `BUILD_WINDTRAP` — RGBA, 256×256; `BUILD_WINDTRAP_FLAG` — RGBA, 256×2048; `BUILD_REFINERY` — RGBA, 384×2048.

`cPlayer::setHouse` создаёт текстуры флагов, зданий и юнитов через `createPlayerTextureFromIndexedSurfaceWithPalette` (`src/gameobjects/players/cPlayer.cpp@0a33444:258-318`): флаги — `:276-278`, здания и flash — `:286,298`, тело и верх юнита — `:310,316`. В `SDLDrawer::createTextureFromIndexedSurfaceWithPalette` все 92 RGBA-текстуры проходят ветку `!isSurface8BitPaletted`: создаётся texture напрямую из исходной поверхности без изменения цвета (`src/drawers/SDLDrawer.cpp@0a33444:366-379`). Замена `HouseColors` в slots 144–150 находится только в ветке INDEX8 (`:381-430`). Следовательно, на HD4 RGBA-текстуры юнитов и зданий PORT не наносит цвет Дома ни палитрой, ни маской; `setHouse` при смене владельца заново создаёт текстуры, оставляя пиксели RGBA исходными.

Путь рисования юнита: `cPlayer::getUnitBitmap`/`getUnitTopBitmap` возвращают кэш (`src/gameobjects/players/cPlayer.cpp@0a33444:631-662`); `cUnitDrawer` берёт body texture из `getUnitBitmap` и вызывает `renderStrechSprite` (`src/drawers/cUnitDrawer.cpp@0a33444:259-274`), затем рисует верх из `getUnitTopBitmap` (`:280-295`). Путь здания: `cAbstractStructure::getBitmap` возвращает `getPlayer()->getStructureBitmap(getType())` (`src/gameobjects/structures/cAbstractStructure.cpp@0a33444:141-144`); `drawWithShadow` берёт её и вызывает `renderStrechSprite` (`:929-947`). Те же building textures используются в remembered-structures и ghost-preview путях (`src/drawers/cStructureDrawer.cpp@0a33444:103-115`, `src/drawers/cPlaceItDrawer.cpp@0a33444:202-220`).

Команда Pillow-проверки из фактического пакета:

```sh
/srv/dune/venv/bin/python -c 'import struct,io,collections; from pathlib import Path; from PIL import Image; b=Path("/srv/dune/worktrees/u63/.git/lfs/objects/e2/60/e260cd4091532269adb0b4476b9e07d34493e330b1b29a4eeeecd9890b76fa83").read_bytes(); n=struct.unpack_from("<H",b,4)[0]; start=6+n*52; rows=[(i,b[r:r+40].split(bytes([0]),1)[0].decode("ascii","replace"),b[r+40:r+44].split(bytes([0]),1)[0].decode("ascii","replace"),*struct.unpack_from("<II",b,r+44)) for i in range(n) for r in [6+i*52]]; selected=[(name,ext,size,Image.open(io.BytesIO(b[start+off:start+off+size])).mode) for i,name,ext,off,size in rows if name.startswith(("UNIT_","BUILD_")) and ext=="PNG"]; print("UNIT_/BUILD_ PNG entries",len(selected),"modes",dict(collections.Counter(mode for _,_,_,mode in selected))); print("non-RGBA",[(name,ext,size,mode) for name,ext,size,mode in selected if mode!="RGBA"])'
```

## 5. Вызовы `getHouseTexture` в FORK1 и соответствующее рисование PORT

Команда `git grep -n getHouseTexture FORK1 -- src` вывела 15 строк: 13 вызовов, определение `Graphics::getHouseTexture` и объявление метода. Определение — `src/utils/Graphics.cpp@9208dcf:226`, объявление — `src/utils/Graphics.hpp@9208dcf:46`. Вывод вызовов:

```text
src/drawers/cStructureDrawer.cpp:317
src/drawers/cStructureDrawer.cpp:359
src/drawers/cStructureDrawer.cpp:401
src/drawers/cStructureDrawer.cpp:443
src/drawers/cStructureDrawer.cpp:486
src/drawers/cStructureDrawer.cpp:528
src/drawers/cStructureDrawer.cpp:570
src/drawers/cStructureDrawer.cpp:612
src/drawers/cStructureDrawer.cpp:654
src/drawers/cStructureDrawer.cpp:696
src/drawers/cStructureDrawer.cpp:738
src/drawers/cStructureDrawer.cpp:781
src/player/cPlayer.cpp:278
```

| Вызов в FORK1 | Что рисуется / назначается | То же рисование в PORT |
|---|---|---|
| `src/drawers/cStructureDrawer.cpp@9208dcf:317` | House-маскированный `BUILD_RADAR_FLAG`; рисование — `:338`. | HD-накладки нет; общий `structure->drawFlags()` — `src/drawers/cStructureDrawer.cpp@0a33444:337-339`, затем `src/gameobjects/structures/cAbstractStructure.cpp@0a33444:910-914` и `src/gameobjects/cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:359` | `BUILD_BARRACKS_FLAG`; рисование — `:380-384`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:401` | `BUILD_WOR_FLAG`; рисование — `:422-426`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:443` | `BUILD_REFINERY_FLAG`; рисование — `:465-469`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:486` | `BUILD_WINDTRAP_FLAG`; рисование — `:507-511`. | `src/drawers/cStructureDrawer.cpp@0a33444:289-301` рисует `BUILD_WINDTRAP_FLAG` без House-маски, если флаг найден; dispatch — `:337-339`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:528` | `BUILD_SILO_FLAG`; рисование — `:549-553`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:570` | `BUILD_STARPORT_FLAG`; рисование — `:591-595`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:612` | `BUILD_PALACE_FLAG`; рисование — `:633-637`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:654` | `BUILD_IX_FLAG`; рисование — `:675-679`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:696` | `BUILD_LIGHTFACTORY_FLAG`; рисование — `:717-721`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:738` | `BUILD_HIGHTECH_FLAG`; рисование — `:760-764`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/drawers/cStructureDrawer.cpp@9208dcf:781` | `BUILD_CONSTYARD_FLAG`; рисование — `:802-806`. | HD-накладки нет; общий флаговый путь `cStructureDrawer.cpp@0a33444:337-339` → `cAbstractStructure.cpp@0a33444:910-914` → `cFlag.cpp@0a33444:42-64`. |
| `src/player/cPlayer.cpp@9208dcf:278` | `createHouseTexture` lambda применяет House color/mask к player flags, `structureType.bmp`/flash, `unitType.bmp`/top (`cPlayer.cpp@9208dcf:290-331`). | Текстуры для House создаются в `src/gameobjects/players/cPlayer.cpp@0a33444:276-318`; RGBA pass-through в palette helper. Body/top рисуются через `cUnitDrawer.cpp@0a33444:260-295`; здания — через `cAbstractStructure.cpp@0a33444:141-144,929-947`. |

Общий PORT-флаговый путь проверен командами `git show PORT:src/gameobjects/structures/cAbstractStructure.cpp | nl -ba | sed -n '910,920p'` и `git show PORT:src/gameobjects/cFlag.cpp | nl -ba | sed -n '38,68p'`: `drawFlags` вызывает `flag->draw()`, а `cFlag::draw` берёт `getFlagBitmap` или `getFlagSmallBitmap` из `cPlayer` и рисует его через `renderStrechSprite`. `getFlagBitmap` относится к обычному флагу House, не к отдельному HD-флагу здания.

### Независимая выборочная сверка корневой нитью

Пункт 1 сверялся по полным LFS pointer выводам выше и командами `wc -l`, `awk` и `comm`. Независимые результаты: 241/242 записи (TSV содержат 242/243 строки с заголовком); `HM_*` без `HM_HV_*` — 37 записей в обоих; имена только в PORT — `EXPLOSION_CARRYALL`; только в FORK1 имён нет.

Пункты 2–3 сверялись командами `git show PORT:src/utils/cPack.h | nl -ba` и `git show PORT:src/drawers/SDLDrawer.hpp | nl -ba`. В выводе `cPack.h:49` есть `getIndexFromName`, `cPack.h:47` — `getData`; открытого `getNameFromIndex` нет; `SDLDrawer.hpp:35` объявляет `renderStrechFullSprite(Texture *src, cRectangle dest_pos, Uint8 opacity = 255)`.

Пункты 4–5 сверялись командами `git grep -n getHouseTexture FORK1 -- src`, `git show PORT:src/drawers/cUnitDrawer.cpp | nl -ba | sed -n '235,300p'`, `git show PORT:src/gameobjects/structures/cAbstractStructure.cpp | nl -ba | sed -n '132,150p;929,947p'` и `git show PORT:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '289,301p;337,339p'`. Вывод подтверждает 13 вызовов, unit body/top рисуются после `getUnitBitmap`/`getUnitTopBitmap`, building bitmap берётся из player cache и рисуется `renderStrechSprite`, а `BUILD_WINDTRAP_FLAG` в PORT берётся сырым `getTexture` без передачи House ID, HouseColors или маски.
