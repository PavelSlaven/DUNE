# Сверка помощников 1–3

Проверка выполнена на PORT `acddd297b21ec200c7090dd2f1b73e014e2b74c0`. Для каждого факта запущена отдельная команда.

## Помощник 1 — файлы и дома

### 1. `src/include/eGameState.h@acddd29:18` — объявлен `enum class eGameState : char`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.h | sed -n '18p'
```

Вывод:

```text
enum class eGameState : char {
```

Итог: **совпало**.

### 2. `src/include/eGameState.h@acddd29:69` — `GAME_MAX_STATES` равен `22`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/eGameState.h | sed -n '69p'
```

Вывод:

```text
inline constexpr int GAME_MAX_STATES = 22;
```

Итог: **совпало**.

### 3. `src/gamestates/cMainMenuState.h@acddd29:49` — объявлен метод `buildHdMenu`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMainMenuState.h | sed -n '49p'
```

Вывод:

```text
    void buildHdMenu();
```

Итог: **совпало**.

### 4. `src/include/definitions.h@acddd29:104` — константа `SARDAUKAR` равна `4`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/include/definitions.h | sed -n '104p'
```

Вывод:

```text
inline constexpr int SARDAUKAR = 4;
```

Итог: **совпало**.

## Помощник 2 — функции

### 5. `src/game/cGame_logic.cpp@acddd29:1494` — переход проверяет, равен ли следующий статус `GAME_BRIEFING`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1494p'
```

Вывод:

```text
        if (m_nextState == GAME_BRIEFING) {
```

Итог: **совпало**.

### 6. `src/game/cGame_logic.cpp@acddd29:1496` — при этом вызывается `prepareMentatForPlayer()`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1496p'
```

Вывод:

```text
            prepareMentatForPlayer();
```

Итог: **совпало**.

### 7. `src/game/cGame_logic.cpp@acddd29:1505` — метод присваивает `newState` полю `m_nextState`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1505p'
```

Вывод:

```text
    m_nextState = newState;
```

Итог: **совпало**.

### 8. `src/game/CampaignProgress.cpp@acddd29:157` — `nextMission` возвращает значение по индексу `houseIndex(house)`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/CampaignProgress.cpp | sed -n '157p'
```

Вывод:

```text
    return m_nextMission[houseIndex(house)];
```

Итог: **совпало**.

## Помощник 3 — места имён

### 9. `src/game/cGame_logic.cpp@acddd29:485` — вызов `playVoice` получает дом игрока `HUMAN`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '485p'
```

Вывод:

```text
    m_audioContext->playVoice(SOUND_VOICE_07_ATR, m_gameObjectsContext->getPlayer(HUMAN)->getHouse());
```

Итог: **совпало**.

### 10. `src/game/cGame_logic.cpp@acddd29:963` — `GAME_REGION` сопоставляется с `eGameState::REGION`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '963p'
```

Вывод:

```text
            case GAME_REGION: mapped = eGameState::REGION; return true;
```

Итог: **совпало**.

### 11. `src/game/cGame_logic.cpp@acddd29:1257` — определение `cGame::prepareMentatToTellAboutHouse` принимает `int house`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/game/cGame_logic.cpp | sed -n '1257p'
```

Вывод:

```text
void cGame::prepareMentatToTellAboutHouse(int house)
```

Итог: **совпало**.

### 12. `src/gamestates/cMentatState.cpp@acddd29:84` — создаётся `AtreidesMentat` и сохраняется в `m_mentat`.

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH && git show acddd297b21ec200c7090dd2f1b73e014e2b74c0:src/gamestates/cMentatState.cpp | sed -n '84p'
```

Вывод:

```text
                m_mentat = std::make_unique<AtreidesMentat>(m_ctx, m_settings, m_stateTransitions, m_mentatFlow, m_allowMissionSelect);
```

Итог: **совпало**.
