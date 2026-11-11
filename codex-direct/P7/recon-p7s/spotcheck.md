# Выборочная сверка помощника 4

## Пункт 1 — `.tmp/p7s/port-strings.tsv`

### 1.1

Исходная запись таблицы:

```text
src/drawers/cBuildingListDrawer.cpp@dc6e5ff	605	Max
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '605p'
```

Полный stdout:

```text
   605	    m_smallTextDrawer->drawTextCenteredInBox("Max", x, y, width, halfHeight, Color::Red);
```

Итог: **совпало**.

### 1.2

Исходная запись таблицы:

```text
src/drawers/cBuildingListDrawer.cpp@dc6e5ff	606	built
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp | nl -ba | sed -n '606p'
```

Полный stdout:

```text
   606	    m_smallTextDrawer->drawTextCenteredInBox("built", x, y + halfHeight, width, halfHeight, Color::Red);
```

Итог: **совпало**.

### 1.3

Исходная запись таблицы:

```text
src/drawers/cStructureDrawer.cpp@dc6e5ff	262	degrees = {:.1f}, faceAngle = {}
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cStructureDrawer.cpp | nl -ba | sed -n '262p'
```

Полный stdout:

```text
   262	            m_textDrawer->drawText(x1 + 32, y1, std::format("degrees = {:.1f}, faceAngle = {}", degrees, facingAngle));
```

Итог: **совпало**.

### 1.4

Исходная запись таблицы:

```text
src/game/cGame_logic.cpp@dc6e5ff	1520	Screenshot saved.
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp | nl -ba | sed -n '1520p'
```

Полный stdout:

```text
  1520	        m_notificationArea->addNotification("Screenshot saved.", eNotificationType::NEUTRAL);
```

Итог: **совпало**.

## Пункт 2 — `.tmp/p7s/fork-pairs.tsv`

### 2.1

Исходная запись таблицы:

```text
src/cGame_logic.cpp@9208dcf	2048	Game saved.	Игра сохранена.
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2048p'
```

Полный stdout:

```text
  2048	                localization::text("Game saved.", "Игра сохранена."),
```

Итог: **совпало**.

### 2.2

Исходная запись таблицы:

```text
src/cGame_logic.cpp@9208dcf	2061	Game loaded.	Игра загружена.
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2061p'
```

Полный stdout:

```text
  2061	                localization::text("Game loaded.", "Игра загружена."),
```

Итог: **совпало**.

### 2.3

Исходная запись таблицы:

```text
src/cGame_logic.cpp@9208dcf	2097	Music off	Музыка выключена
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2097p'
```

Полный stdout:

```text
  2097	            humanPlayer.addNotification(localization::text("Music off", "Музыка выключена"), eNotificationType::NEUTRAL);
```

Итог: **совпало**.

### 2.4

Исходная запись таблицы:

```text
src/cGame_logic.cpp@9208dcf	2101	Music on	Музыка включена
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2101p'
```

Полный stdout:

```text
  2101	            humanPlayer.addNotification(localization::text("Music on", "Музыка включена"), eNotificationType::NEUTRAL);
```

Итог: **совпало**.

## Пункт 3 — `.tmp/p7s/match.tsv` и `.tmp/p7s/port-only.tsv`

### 3.1 — `match.tsv`

Исходная запись таблицы:

```text
Game saved.	Игра сохранена.	0	нет
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"Game saved."' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | wc -l
```

Полный stdout:

```text
0
```

Итог: **совпало**.

### 3.2 — `match.tsv`

Исходная запись таблицы:

```text
CREDITS	КРЕДИТЫ	3	dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/CreditsDrawer.cpp | dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/gamestates/cMainMenuState.cpp | dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/include/eGameState.cpp
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"CREDITS"' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src | wc -l
```

Полный stdout:

```text
3
```

Итог: **совпало**.

### 3.3 — `port-only.tsv`

Исходная запись таблицы:

```text
Max	dc6e5ffd74f6275390a9c4a676aafdca058df7dd@dc6e5ff:src/drawers/cBuildingListDrawer.cpp
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"Max"' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
```

Полный stdout:

```text
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/drawers/cBuildingListDrawer.cpp:605:    m_smallTextDrawer->drawTextCenteredInBox("Max", x, y, width, halfHeight, Color::Red);
```

Итог: **совпало**.

### 3.4 — `port-only.tsv`

Исходная запись таблицы:

```text
Screenshot saved.	dc6e5ffd74f6275390a9c4a676aafdca058df7dd@dc6e5ff:src/game/cGame_logic.cpp
```

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; git grep -n -F '"Screenshot saved."' dc6e5ffd74f6275390a9c4a676aafdca058df7dd -- src
```

Полный stdout:

```text
dc6e5ffd74f6275390a9c4a676aafdca058df7dd:src/game/cGame_logic.cpp:1520:        m_notificationArea->addNotification("Screenshot saved.", eNotificationType::NEUTRAL);
```

Итог: **совпало**.
