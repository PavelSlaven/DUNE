# Задание P9 — музыка форка на SDL3_mixer (шаг П9)

Исполнитель: корневая нить Codex `gpt-6.1-sol` `high` и три помощника `gpt-6-luna` `xhigh` — A, B и C (раздел «Организация работы»).

Рабочая копия: `/srv/library/dune/worktrees/p9`, ветка `codex/p9`, `HEAD` — `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6` (вершина ветки порта `port/up-d06f2fcd`). Файлы Git LFS в этой рабочей копии — настоящие данные. Временные файлы — в `.tmp/p9/`. Коммитов не делай: коммиты делает ведущий по списку из сдачи. Файлы задания лежат в папке `/srv/dune/tasks/p9/` (дальше — «папка задания»).

## Цель

Музыка игры целиком берётся из версии форка. Рядом с игрой лежит папка `music` с восемью пулами (`gameplay`, `menu`, `conquest`, `briefing/atreides`, `briefing/harkonnen`, `briefing/ordos`, `victory`, `defeat`); игра создаёт недостающие пустые папки при запуске. Из пула играют файлы `.ogg`, `.mp3`, `.wav`, `.flac` в случайном порядке без повторов, пока не сыграны все; пустой пул или пул без проигрываемых файлов играет встроенными MIDI-треками. В верхней панели боя есть кнопки `<` и `>`, название трека, подпись «SPEED» («СКОРОСТЬ») и регулятор скорости игры; клавиши `[` и `]` включают предыдущий и следующий трек; клавиша `M` выключает музыку и включает её снова с того же трека. Боевой темы при встрече врага нет: игрок слышит голосовое предупреждение о вражеском юните не чаще одного раза в 30 секунд. Музыка апстрима (`MusicJukeBox`, папки `audio/<тип>`, ключ `customMusic`) игрой не вызывается. Готово, когда новые тесты Catch2 и сборка со всеми тестами зелёные, в журнале игры есть восемь строк о пулах с верным числом файлов, а сцена режима отладки `game-music` и её проверка проходят. Музыку на слух и вид панели оценивает владелец в игре; этот шаг их не доказывает. Голоса и звуки `AudioContext`, `MusicJukeBox`, тест апстрима `test_MusicJukeBox.cpp` и чтение и запись ключа `customMusic` остаются как были.

## Что уже решено

Ревизия `B` = `6ceb29d1604ad0a487436bb9f1a0c60a746deeb6`; её дерево равно ревизии `a1e63b860482d7e7a82e502359965e2caefd6470`. Ревизия форка `FORK1` = `9208dcf5a358f40afd95c99480e4e09f781ed566`. Ревизия апстрима `UP1` = `d06f2fcd2a347182c3774fb96e9a85570405c489`. Все факты о коде порта ниже — о файлах ревизии `B`; номера строк `FORK1` — этой ревизии.

- **Решение владельца Р79** (`docs/decisions.md`): «музыка из нашей версии вся». Остаются музыкальные пулы форка, 22 трека `.wav` в папке `music` рядом с игрой, перемешивание с историей, кнопки `<` и `>`, клавиши `[` и `]`, название трека и регулятор скорости в верхней панели боя; боевой темы при встрече врага нет; выбор музыки апстрима игра не использует.
- **Рабочий каталог игры** — каталог исполняемого файла (Р78); переключение каталога делает шаг П8 в `src/main.cpp`. Этот шаг `src/main.cpp` не меняет. Корень пулов — `std::filesystem::current_path()` на момент создания `AudioContext`. В сборке на servak игра запускается из `.tmp/out/run/bin`, поэтому папка `music` лежит там (пункт 10 контракта).
- **Граница между кодом апстрима и контроллером форка.** Контроллер музыки `MusicController` принадлежит `AudioContext` (поле `std::unique_ptr<MusicController> m_musicController`), а не `cGame`: все вызовы выбора музыки порта идут через `AudioContext` (`cGame_logic.cpp`, `cSelectYourNextConquestState.cpp`, `cSetupSkirmishState.cpp`, `cPlayer.cpp`), и так их тела вызывающих файлов не меняются. Перечень функций:
  - **заменяются телом** в `src/context/AudioContext.cpp`: конструктор, `playMusicByTypeForStateTransition`, `playMusicByType`, `thinkFast`, `setMusicEnabled`;
  - **удаляются** в `src/context/AudioContext.hpp` и `AudioContext.cpp`: функция `startMusic`, поля `m_jukeBox`, `m_newMusic`, `m_newMusicCountdown`;
  - **добавляются** в `AudioContext`: `playPreviousTrack`, `playNextTrack`, `getCurrentMusicTrackName`;
  - **не меняются**: `getSoundPlayer`, `playSound` (обе), `playVoice`, `getMaxVolume`, `toggleMusic`, `changeMusicVolume`, `cGame::playMusicByType`, `cGame::playMusicByTypeForStateTransition`, `cGame::thinkFast_audio`, `src/context/MusicJukeBox.hpp`, `src/context/MusicJukeBox.cpp`, `src/context/MusicChoice.hpp`, `tests/utils/test_MusicJukeBox.cpp`, чтение и запись `customMusic` в `src/game/Preferences.cpp`, `cGameSettings`, `InitialGameSettings`, `cMainMenuState.cpp`, `cOptionsState.cpp`.
- **Категории.** Тип музыки порта `eMusicType` (`src/include/definitions.h`) переводится в категорию пула функцией `musicCategoryFor` форка (`FORK1:src/cGame_logic.cpp`, строки 96–117): PEACE и ATTACK — `Gameplay`; MENU — `Menu`; CONQUEST — `Conquest`; WIN — `Victory`; LOSE — `Defeat`; BRIEFING — по дому: HARKONNEN — `BriefingHarkonnen`, ORDOS — `BriefingOrdos`, любой другой дом (в том числе SARDAUKAR и GENERALHOUSE) — `BriefingAtreides`. Отдельного пула Сардаукаров нет.
- **Повторный вход в категорию** не меняет играющий трек: `activate(category, shouldAdvanceRepeatedMusicCategory(repeated, playing))`, где `repeated` — совпадение нового типа музыки (после замены ATTACK на PEACE) с `m_settings->getMusicType()`; трек сменяется, только если он уже закончился. Тип ATTACK заменяется на PEACE до этого сравнения.
- **`cSoundPlayer`.** Порт играет музыку через SDL3_mixer (`MIX_Track`, `MIX_LoadAudio_IO`). Функция форка `playMusicFile(const std::filesystem::path &file, std::string &error)` заменяет функцию порта `playMusicFile(const std::string &path)`: при выключенной музыке она возвращает `false` с текстом `music is disabled` (у порта было `true`). Вызов `Mix_Init` с флагами кодеков в порт не переносится: декодеры подключает `MIX_Init` в `src/game/cSDLSystem.cpp`.
- **Журнал.** Вместо `cLogger` форка — `Logger::info`/`Logger::warn` с `COMP_SOUND` из `src/utils/Log.h`.
- **Тексты.** Все видимые игроку строки идут через `localization::text(en, ru)` (`src/utils/Localization.hpp`); подпись встроенного трека `Dune II #N` из `MusicTrack::displayName` остаётся без перевода, как в форке.
- **Клавиши.** Новые действия `cKeyBindings`: `MUSIC_PREVIOUS_TRACK` (по умолчанию `[`) и `MUSIC_NEXT_TRACK` (по умолчанию `]`); имена скан-кодов SDL — `SDL_SCANCODE_LEFTBRACKET` и `SDL_SCANCODE_RIGHTBRACKET`. Ни одно действие порта не занимает эти клавиши (`git grep -n BRACKET` по ревизии `B` пуст).
- **Данные.** 22 файла `.wav` из `FORK1:resources/bin/music/` уже лежат в рабочей копии в `resources/bin/music/`, их не меняй; проверка sha256 — в разделе «Проверки», пункт 5. Правило LFS для них в `.gitattributes` добавляет пункт 10 контракта, а коммит файлов делает ведущий.

## Прочитать до работы

Прочитай сразу после `create_goal` и до любого другого действия, каждый файл или вывод отдельным вызовом. Пути без `/srv/` — от корня рабочей копии. Перед командами Git: `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH`.

Файлы порта целиком (и вывод `nl -ba resources/bin/settings.ini | sed -n '60,72p'`):

- `src/context/AudioContext.hpp`;
- `src/context/AudioContext.cpp`;
- `src/context/MusicJukeBox.hpp`;
- `src/utils/cSoundPlayer.h`;
- `src/utils/cSoundPlayer.cpp`;
- `src/drawers/cMessageDrawer.cpp`;
- `src/managers/cDrawManager.h`;
- `src/controls/eKeyAction.h`;
- `src/debug/UiAudit.hpp`;
- `tests/utils/test_MusicJukeBox.cpp`;
- `tests/ui_audit/ui_audit_part3b_catalog.py`;
- `tests/ui_audit/ui_audit_part3b_scenes.py`.

Выводы команд:

- `nl -ba src/managers/cDrawManager.cpp | sed -n '16,62p;121,177p;281,375p'`;
- `nl -ba src/gameobjects/players/cPlayer.cpp | sed -n '16,60p;204,254p;2068,2146p'`;
- `nl -ba src/gameobjects/players/cPlayer.h | sed -n '16,40p;590,630p'`;
- `nl -ba src/controls/cKeyBindings.cpp | sed -n '16,60p;138,150p'`;
- `nl -ba src/game/cGame_logic.cpp | sed -n '1527,1590p'`;
- `nl -ba src/debug/UiAuditAccess.cpp | sed -n '1,60p;770,830p'`;
- `nl -ba src/debug/UiAuditScenes.cpp | sed -n '448,456p'`;
- `nl -ba src/CMakeLists.txt | sed -n '1,12p'`;
- `nl -ba tests/CMakeLists.txt | sed -n '1,80p'`;
- `nl -ba tools/upstream/build_upstream_linux.sh | sed -n '224,240p'`;
- `nl -ba resources/bin/settings.ini | sed -n '94,125p'`;
- `tail -n 5 .gitattributes`.

Выводы из форка (`git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь>`, у файлов с номерами строк — `| nl -ba | sed -n '<строки>p'`):

- `src/audio/MusicPlaylist.h`, `src/audio/MusicPlaylist.cpp`, `src/audio/MusicController.h`, `src/audio/MusicController.cpp`, `src/audio/MusicTransitionPolicy.hpp`, `src/sidebar/MusicControlsLayout.hpp` — целиком;
- `tests/MusicPlaylistTests.cpp`, `tests/MusicTransitionPolicyTests.cpp`, `tests/MusicControlsLayoutTests.cpp` — целиком;
- `tools/export_music.py` — целиком;
- `src/utils/cSoundPlayer.cpp` — строки 151–204;
- `src/cGame_logic.cpp` — строки 96–117, 1114–1153, 2092–2111, 2215–2273;
- `src/drawers/cMessageDrawer.cpp` — строки 39–126;
- `src/managers/cDrawManager.cpp` — строки 288–422;
- `src/player/cPlayer.cpp` — строки 1874–1935;
- `src/debug/UiAuditAccess.cpp` — строки 827–842;
- `.gitattributes` — строки 65–79.

## Контракт

Правила переноса (пункт «Правила переноса» ниже) применяются к каждой строке форка, которую контракт переносит в порт, если пункт контракта не говорит иначе. Другой код порта, кроме названного в пунктах контракта, не меняется.

### Правила переноса

1. Вызов `cLogger::getInstance()->log(LOG_WARN, COMP_SOUND, "<событие>", std::format("<формат>", <аргументы>))` → `Logger::warn(COMP_SOUND, "<событие>", "<формат>", <аргументы>)`; то же для `LOG_INFO` → `Logger::info`. Подключение `utils/cLog.h` → `utils/Log.h`; подключение `<format>` удаляется, если после замены оно не нужно.
2. `renderDrawer->` → `m_sdlDrawer->` (тот же метод, те же аргументы).
3. `game.m_screenW` → `<настройки>->getScreenW()`, `game.m_screenH` → `<настройки>->getScreenH()`, где `<настройки>` — указатель на `cGameSettings`, названный в пункте контракта.
4. `game.getMouse()` → `m_mouse`.
5. Подключения `<SDL2/...>` и `d2tmc.h` не переносятся; нужные заголовки берутся такими, какие подключает порт.
6. Вызов функции форка, у которой нет пары в порту и которая не названа в контракте, — блок `## Q-P9-NN` и стоп.

### Пункты контракта

1. **Новые файлы, копии файлов форка** (команда `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:<путь> > <путь>`, содержимое не правится):
   - `src/audio/MusicPlaylist.h`;
   - `src/audio/MusicPlaylist.cpp`;
   - `src/audio/MusicTransitionPolicy.hpp`;
   - `src/sidebar/MusicControlsLayout.hpp`.
2. **`src/audio/MusicController.h`** — копия файла форка, затем три правки:
   - после строки `#include "audio/MusicPlaylist.h"` добавляется строка `#include "definitions.h"`;
   - в класс `MusicController` сразу после строки `    void activate(MusicCategory category, bool advanceOnRepeatedEntry = true);` добавляется строка `    void selectCategory(MusicCategory category);`;
   - после закрывающей `};` класса `MusicController`, через одну пустую строку, добавляется функция:
     ```cpp
     [[nodiscard]] inline MusicCategory musicCategoryFor(eMusicType type, int house)
     {
         switch (type) {
             case eMusicType::PEACE:
             case eMusicType::ATTACK:
                 return MusicCategory::Gameplay;
             case eMusicType::MENU:
                 return MusicCategory::Menu;
             case eMusicType::CONQUEST:
                 return MusicCategory::Conquest;
             case eMusicType::WIN:
                 return MusicCategory::Victory;
             case eMusicType::LOSE:
                 return MusicCategory::Defeat;
             case eMusicType::BRIEFING:
                 if (house == HARKONNEN) return MusicCategory::BriefingHarkonnen;
                 if (house == ORDOS) return MusicCategory::BriefingOrdos;
                 return MusicCategory::BriefingAtreides;
         }
         return MusicCategory::Menu;
     }
     ```
   Строка `    friend class UiAuditAccess;` остаётся.
3. **`src/audio/MusicController.cpp`** — копия файла форка, затем правки:
   - строки `#include "utils/cLog.h"` и `#include <format>` заменяются: остаётся `#include "utils/Log.h"` и `#include "utils/cSoundPlayer.h"`; порядок — `audio/MusicController.h`, `utils/Log.h`, `utils/cSoundPlayer.h`;
   - четыре вызова `cLogger` (форк, строки 44–48, 56–64, 137–141, 159–163) переписываются по правилу 1; значения событий и форматов сохраняются, то есть получаются ровно эти вызовы:
     - `Logger::warn(COMP_SOUND, "Custom music skipped", "{}: unsupported file type", utf8String(entry.path()));`
     - `Logger::info(COMP_SOUND, "Music pool", "{}: {} custom track(s){}", utf8String(state.directory), customTracks.size(), state.usingCustom ? "" : "; using built-in fallback");`
     - `Logger::warn(COMP_SOUND, "Custom music skipped", "{}: {}", utf8String(track->externalPath), error);`
     - `Logger::warn(COMP_SOUND, "Music pool fallback", "No playable custom music in {}; using built-in music", utf8String(state.directory));`
   - сразу перед определением `void MusicController::activate(MusicCategory category, bool advanceOnRepeatedEntry)` добавляется определение:
     ```cpp
     void MusicController::selectCategory(MusicCategory category)
     {
         m_activeCategory = category;
         m_hasActiveCategory = true;
     }
     ```
     Назначение: когда музыка выключена, `AudioContext` запоминает категорию, чтобы `replayCurrent` после включения (клавиша `M` или окно настроек) начал трек этой категории; у форка при запуске игры с выключенной музыкой включение клавишей `M` молчало до смены экрана.
4. **`src/CMakeLists.txt`.** Сразу после строки `    context/MusicJukeBox.cpp` добавляются две строки: `    audio/MusicController.cpp` и `    audio/MusicPlaylist.cpp`. Заголовки в список не добавляются.
5. **`src/utils/cSoundPlayer.h` и `src/utils/cSoundPlayer.cpp`.**
   - В `cSoundPlayer.h`: после строки `#include <memory>` добавляется строка `#include <filesystem>`; объявление `bool playMusicFile(const std::string &path);` заменяется строкой `bool playMusicFile(const std::filesystem::path &file, std::string &error);`; комментарий над ним остаётся.
   - В `cSoundPlayer.cpp` определение `bool cSoundPlayer::playMusicFile(const std::string &path)` заменяется определением:
     ```cpp
     bool cSoundPlayer::playMusicFile(const std::filesystem::path &file, std::string &error)
     {
         if (!m_isMusicEnabled || !m_musicTrack) {
             error = "music is disabled";
             return false;
         }
         const auto utf8Path = file.u8string();
         const std::string filename(utf8Path.begin(), utf8Path.end());
         SDL_IOStream *io = SDL_IOFromFile(filename.c_str(), "rb");
         if (!io) {
             error = SDL_GetError();
             return false;
         }
         MIX_Audio *audio = MIX_LoadAudio_IO(m_mixer, io, false, true);
         if (!audio) {
             error = SDL_GetError();
             return false;
         }
         startMusic(audio);
         releaseMusicFile();
         m_musicFileAudio = audio;
         error.clear();
         return true;
     }
     ```
     Ошибки в журнал здесь не пишутся: их пишет `MusicController`. Остальные функции `cSoundPlayer` не меняются.
6. **`src/context/AudioContext.hpp` и `src/context/AudioContext.cpp`.**
   - `AudioContext.hpp`: строка `#include "context/MusicChoice.hpp"` заменяется двумя строками `#include <filesystem>` и `#include <optional>` (файлы, подключающие `AudioContext.hpp`, получали эти заголовки через `MusicChoice.hpp`); строка `class MusicJukeBox;` заменяется строкой `class MusicController;`; сразу после строки `class AudioContext {` добавляется строка `    friend class UiAuditAccess;`; в разделе `public:` после объявления `void thinkFast();` добавляются строки:
     ```cpp
         void playPreviousTrack();
         void playNextTrack();
         [[nodiscard]] std::string getCurrentMusicTrackName() const;
     ```
     в разделе `private:` удаляются объявление `void startMusic(const MusicChoice &choice) const;` и поля `std::unique_ptr<MusicJukeBox> m_jukeBox;`, `MusicChoice m_newMusic;`, `int m_newMusicCountdown;`; после поля `cGameSettings* m_settings = nullptr;` добавляется поле `std::unique_ptr<MusicController> m_musicController;`; после строки `#include <memory>` добавляется строка `#include <string>`.
   - `AudioContext.cpp`, подключения: строка `#include "context/MusicJukeBox.hpp"` заменяется строками `#include "audio/MusicController.h"` и `#include "audio/MusicTransitionPolicy.hpp"`; строка `#include "utils/RNG.hpp"` удаляется; после строки `#include <format>` добавляются строки `#include <array>`, `#include <filesystem>`, `#include <vector>`. Функция `musicTypeName` в анонимном пространстве имён остаётся.
   - Список инициализации конструктора становится `m_soundPlayer(std::move(soundPlayer)), m_settings(settings)`; две строки `d2tm_assert` остаются; строка `m_jukeBox->createRepertoryDirectories();` заменяется блоком:
     ```cpp
         const std::filesystem::path gameDirectory = std::filesystem::current_path();
         struct MusicPool {
             MusicCategory category;
             const char *directory;
             std::vector<int> fallbackIds;
         };
         const std::array<MusicPool, 8> pools{{
             {MusicCategory::Gameplay, "music/gameplay",
              {MIDI_BUILDING01, MIDI_BUILDING02, MIDI_BUILDING03, MIDI_BUILDING04, MIDI_BUILDING05,
               MIDI_BUILDING06, MIDI_BUILDING07, MIDI_BUILDING08, MIDI_BUILDING09}},
             {MusicCategory::Menu, "music/menu", {MIDI_MENU}},
             {MusicCategory::Conquest, "music/conquest", {MIDI_SCENARIO}},
             {MusicCategory::BriefingAtreides, "music/briefing/atreides", {MIDI_MENTAT_ATR}},
             {MusicCategory::BriefingHarkonnen, "music/briefing/harkonnen", {MIDI_MENTAT_HAR}},
             {MusicCategory::BriefingOrdos, "music/briefing/ordos", {MIDI_MENTAT_ORD}},
             {MusicCategory::Victory, "music/victory", {MIDI_WIN01, MIDI_WIN02, MIDI_WIN03}},
             {MusicCategory::Defeat, "music/defeat", {MIDI_LOSE01, MIDI_LOSE02, MIDI_LOSE03}},
         }};
         for (const MusicPool &pool : pools) {
             std::error_code createError;
             std::filesystem::create_directories(gameDirectory / pool.directory, createError);
             if (createError) {
                 Logger::warn(COMP_SOUND, "Music directory", "Could not create {}: {}",
                              (gameDirectory / pool.directory).string(), createError.message());
             }
         }
         m_musicController = std::make_unique<MusicController>(m_soundPlayer.get(), gameDirectory);
         for (const MusicPool &pool : pools) {
             m_musicController->configure(pool.category, pool.directory, pool.fallbackIds);
         }
     ```
   - Тела функций заменяются ровно так:
     ```cpp
     void AudioContext::playMusicByTypeForStateTransition(eMusicType iType, int humanHouse)
     {
         playMusicByType(iType, false, false, humanHouse);
     }

     bool AudioContext::playMusicByType(eMusicType iType, bool triggerWithVoice, bool isCurrentlyPlayingMission, int humanHouse)
     {
         Logger::info(COMP_SOUND, "AudioContext::playMusicByType", "iType = {}. triggerWithVoice = {}", musicTypeName(iType), triggerWithVoice);

         if (iType == eMusicType::ATTACK) {
             iType = eMusicType::PEACE;
         }
         const bool repeatedCategory = m_settings->getMusicType() == iType;
         m_settings->setMusicType(iType);
         Logger::info(COMP_SOUND, "AudioContext::playMusicByType", "m_musicType = {}", musicTypeName(iType));

         const MusicCategory category = musicCategoryFor(iType, humanHouse);
         if (!m_settings->isPlayMusic()) {
             m_musicController->selectCategory(category);
             return false;
         }
         m_musicController->activate(category, shouldAdvanceRepeatedMusicCategory(repeatedCategory, isCurrentlyPlayingMission));
         return true;
     }

     void AudioContext::thinkFast()
     {
         if (!m_settings->isPlayMusic()) {
             return;
         }
         m_musicController->update();
     }

     void AudioContext::setMusicEnabled(bool enabled)
     {
         m_settings->setPlayMusic(enabled);
         m_soundPlayer->setMusicEnabled(enabled);
         if (enabled) {
             m_musicController->replayCurrent();
         }
         else {
             m_musicController->stop();
         }
     }

     void AudioContext::playPreviousTrack()
     {
         if (m_settings->isPlayMusic()) {
             m_musicController->previous();
         }
     }

     void AudioContext::playNextTrack()
     {
         if (m_settings->isPlayMusic()) {
             m_musicController->next();
         }
     }

     std::string AudioContext::getCurrentMusicTrackName() const
     {
         return m_musicController->currentDisplayName();
     }
     ```
     Определение `AudioContext::startMusic` удаляется. Определения `AudioContext::~AudioContext`, `getSoundPlayer`, `playSound`, `playVoice`, `getMaxVolume`, `toggleMusic`, `changeMusicVolume` не меняются.
7. **`src/gameobjects/players/cPlayer.h` и `cPlayer.cpp`: голосовое предупреждение без боевой темы.**
   - `cPlayer.h`: после строки `#include <memory>` добавляется строка `#include <cstdint>`; после строки `    AudioContext *m_audioContext = nullptr;` добавляются строки `    std::uint64_t m_lastEnemyWarningMs = 0;` и `    bool m_hasPlayedEnemyWarning = false;`.
   - `cPlayer.cpp`, функция `cPlayer::init`: после строки `    iTeam = -1;` добавляются строки `    m_lastEnemyWarningMs = 0;` и `    m_hasPlayedEnemyWarning = false;`.
   - `cPlayer.cpp`, функция `cPlayer::onEntityDiscovered(const CommonEvent &event)`: тело (всё между фигурными скобками функции, включая закомментированные строки в начале) заменяется телом:
     ```cpp
         if (!isHuman() || event.entityType != eBuildType::UNIT) {
             return;
         }

         cUnit *pUnit = m_objects->getUnit(event.entityID);
         if (!isSameTeamAs(event.player) || isSameTeamAs(pUnit->getPlayer())) {
             return;
         }

         constexpr Uint64 warningCooldownMs = 30'000;
         const Uint64 now = SDL_GetTicks();
         if (m_hasPlayedEnemyWarning && now - m_lastEnemyWarningMs < warningCooldownMs) {
             return;
         }
         m_lastEnemyWarningMs = now;
         m_hasPlayedEnemyWarning = true;
         m_audioContext->playVoice(pUnit->iType == SANDWORM ? SOUND_VOICE_10_ATR : SOUND_VOICE_09_ATR, getHouse());
     ```
     Это поведение прежней функции без музыки: предупреждение говорит только человек-игрок, только о юните чужой команды, голос Sandworm — `SOUND_VOICE_10_ATR`, прочие — `SOUND_VOICE_09_ATR`; обнаружение строений голоса не давало и не даёт; музыка при этом не меняется, `m_settings->getMusicType()` здесь не читается. Остальные функции файла не меняются.
8. **Клавиши `[` и `]`.**
   - `src/controls/eKeyAction.h`: после строки `    MUSIC_VOLUME_UP,` добавляются строки `    MUSIC_PREVIOUS_TRACK,` и `    MUSIC_NEXT_TRACK,`.
   - `src/controls/cKeyBindings.cpp`, `loadDefaults`: после строки `    bind(eKeyAction::MUSIC_VOLUME_UP,     {SDL_SCANCODE_P,   SDL_SCANCODE_VOLUMEUP});` добавляются строки `    bind(eKeyAction::MUSIC_PREVIOUS_TRACK, {SDL_SCANCODE_LEFTBRACKET});` и `    bind(eKeyAction::MUSIC_NEXT_TRACK,    {SDL_SCANCODE_RIGHTBRACKET});`.
   - `src/controls/cKeyBindings.cpp`, `getActionTable`: после строки `        {"MUSIC_VOLUME_UP",           eKeyAction::MUSIC_VOLUME_UP},` добавляются строки `        {"MUSIC_PREVIOUS_TRACK",      eKeyAction::MUSIC_PREVIOUS_TRACK},` и `        {"MUSIC_NEXT_TRACK",          eKeyAction::MUSIC_NEXT_TRACK},`.
   - `resources/bin/settings.ini`, раздел `[KEYS]`: после строки `MUSIC_VOLUME_UP=P` добавляются строки `MUSIC_PREVIOUS_TRACK=[` и `MUSIC_NEXT_TRACK=]`.
   - `resources/bin/settings.ini`, комментарий о музыке: пять строк подряд — от строки `# play music files from the audio directory (next to settings.ini) instead of the built-in music,` до строки `#customMusic = true` включительно — заменяются тремя строками:
     ```
     # play your own music: put .ogg, .mp3, .wav or .flac files into the music folder next to the game,
     # one folder per music type: music/gameplay, music/menu, music/conquest, music/victory, music/defeat,
     # music/briefing/atreides, music/briefing/harkonnen and music/briefing/ordos
     ```
     Остальные строки файла не меняются.
9. **`src/game/cGame_logic.cpp`, функция `cGame::onKeyPressedGame`.**
   - Блок `if (event.isAction(eKeyAction::TOGGLE_MUSIC)) {…}` заменяется блоком:
     ```cpp
         if (event.isAction(eKeyAction::TOGGLE_MUSIC)) {
             m_audioContext->toggleMusic();
             m_notificationArea->addNotification(
                 m_gameSettings->isPlayMusic() ? localization::text("Music on", "Музыка включена") : localization::text("Music off", "Музыка выключена"),
                 eNotificationType::NEUTRAL);
         }
     ```
   - Сразу после блока `if (event.isAction(eKeyAction::MUSIC_VOLUME_UP)) {…}` и перед блоком `if (event.isAction(eKeyAction::GAME_SPEED_UP)) {` добавляются блоки:
     ```cpp
         if (event.isAction(eKeyAction::MUSIC_PREVIOUS_TRACK) && isState(GAME_PLAYING)) {
             m_audioContext->playPreviousTrack();
         }

         if (event.isAction(eKeyAction::MUSIC_NEXT_TRACK) && isState(GAME_PLAYING)) {
             m_audioContext->playNextTrack();
         }
     ```
   Других правок в `cGame_logic.cpp` нет.
10. **Данные и сборка.**
    - `.gitattributes`: после последней строки (`resources/bin/data/hd4/*.png filter=lfs diff=lfs merge=lfs -text`) добавляется строка `resources/bin/music/**/*.wav filter=lfs diff=lfs merge=lfs -text` — форма правила форка (`*.wav filter=lfs diff=lfs merge=lfs -text`, `FORK1:.gitattributes`, строка 69) с путём в `resources/bin/music`.
    - `tools/upstream/build_upstream_linux.sh`: в команде `cp -a "$repo_root/resources/bin/campaign" "$repo_root/resources/bin/campaign_ru" "$repo_root/resources/bin/data" \` после `"$repo_root/resources/bin/campaign_ru"` добавляется `"$repo_root/resources/bin/music"`; остальная команда не меняется.
11. **`tools/export_music.py`** — копия файла форка: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tools/export_music.py > tools/export_music.py`; содержимое не правится. Его источник `resources/tools/datapack/readerpack.py` есть в порту и совпадает с форком.
12. **`src/drawers/cMessageDrawer.cpp`: строка сообщений правее панели музыки.**
    - После строки `#include "context/TextContext.hpp"` добавляются строки `#include "sidebar/HudLayout.hpp"`, `#include "sidebar/MusicControlsLayout.hpp"`, `#include <algorithm>`.
    - Тело `void cMessageDrawer::draw()` заменяется телом функции форка `cMessageDrawer::draw` (`FORK1:src/drawers/cMessageDrawer.cpp`, строки 39–126, всё между фигурными скобками) по правилам переноса; `<настройки>` — `m_services->settings` (тот же указатель использует `initCombatPosition` порта). Результат: в боевом состоянии рисуется тёмный прямоугольник сообщения правее панели музыки (рамка бронзового цвета), текст сжимается до масштаба не меньше 0,5, картинка-полоса `m_bmpBar` боевого состояния не рисуется; в состоянии `NEXT_CONQUEST` рисуется картинка-полоса, как было.
    - `cMessageDrawer.h` не меняется.
13. **`src/managers/cDrawManager.h` и `cDrawManager.cpp`: панель музыки и регулятор скорости.**
    - `cDrawManager.h`: после строки `    void drawTopBarBackground();` добавляются строки `    void drawTopBarMusicControls();` и `    void drawMusicControls(int left, int right);`; после строки `    sGameServices* m_services = nullptr;` добавляется строка `    bool m_speedSliderDragging = false;`.
    - `cDrawManager.cpp`, подключения: после строки `#include "utils/Localization.hpp"` добавляются строки `#include "context/AudioContext.hpp"`, `#include "game/cTimeManager.h"`, `#include "sidebar/HudLayout.hpp"`, `#include "sidebar/MusicControlsLayout.hpp"`, `#include <algorithm>`.
    - `cDrawManager.cpp`, `drawCombatState`: сразу после строки `    drawMessage();` добавляется строка `    drawTopBarMusicControls();`.
    - `cDrawManager.cpp`: сразу после определения `cDrawManager::drawTopBarBackground` и перед определением `cDrawManager::setPlayerToDraw` добавляются определения функций:
      ```cpp
      void cDrawManager::drawTopBarMusicControls()
      {
          const HudLayout layout = HudLayout::create(m_gameSettings->getScreenW(), m_gameSettings->getScreenH());
          const int left = 143;
          const int right = layout.battlefield.getEndX() - 8;
          drawMusicControls(left, right);
      }
      ```
      и `void cDrawManager::drawMusicControls(int left, int right)` — тело функции форка `cDrawManager::drawMusicControls` (`FORK1:src/managers/cDrawManager.cpp`, строки 296–422) по правилам переноса и этим заменам:
      1. `m_messageDrawer.getMessage()` → `m_messageDrawer->getMessage()`;
      2. первой строкой тела добавляется `cTextDrawer *smallTextDrawer = m_ctx->getTextContext()->getSmallTextDrawer();`, и каждое `m_smallTextDrawer->` становится `smallTextDrawer->`;
      3. сразу перед строкой `constexpr int MinSliderValue = 2;` добавляется строка `cTimeManager *timeManager = m_ctx->getTimeManager();`, и каждое `m_timeManager->` становится `timeManager->`;
      4. `cMouse *mouse = game.getMouse();` → `cMouse *mouse = m_mouse;`;
      5. `game.getCurrentMusicTrackName()` → `m_ctx->getAudioContext()->getCurrentMusicTrackName()`; `game.playPreviousGameplayTrack()` → `m_ctx->getAudioContext()->playPreviousTrack()`; `game.playNextGameplayTrack()` → `m_ctx->getAudioContext()->playNextTrack()`;
      6. три вызова `uiaudit::recordClick("music-previous"…)`, `("music-next"…)`, `("music-speed-slider"…)` остаются, как в форке (подключение `debug/UiAudit.hpp` в файле порта уже есть); `localization::text("SPEED", "СКОРОСТЬ")` остаётся.
14. **Режим отладки интерфейса: сцена `game-music`.**
    - `src/debug/UiAudit.hpp`: в перечисление `GameKind` после строки `    Hud,` добавляется строка `    Music,`.
    - `src/debug/UiAuditScenes.cpp`: сразу после строки сцены `game-hud` (`    withHud(onGameScreen(scene("game-hud", …`) добавляется строка `    onGameScreen(scene("game-music", "game-playing", "atreides", kFixedGameFrames, prepareGame<ATREIDES, uiaudit::Music>), false),`.
    - `src/debug/UiAuditAccess.cpp`: после строки `#include "gamestates/cSetupSkirmishState.h"` добавляются строки `#include "audio/MusicController.h"`, `#include "context/AudioContext.hpp"`, `#include <filesystem>`; в `switch (kind)` функции подготовки игровой сцены между блоком `case GameKind::RadarNoPower: return true;` и строкой `case GameKind::Structure:` добавляется блок:
      ```cpp
              case GameKind::Music: {
                  MusicController *music = currentGame.m_audioContext->m_musicController.get();
                  MusicTrack track;
                  track.externalPath = std::filesystem::path(
                      localization::text("Gameplay_theme_with_an_extremely_long_track_title_for_the_layout_audit.ogg",
                                         "Игровая_тема_с_очень_длинным_названием_трека_для_проверки_раскладки.ogg"));
                  auto &state = music->m_categories[static_cast<std::size_t>(MusicCategory::Gameplay)];
                  state.playlist.setTracks({track});
                  state.playlist.next();
                  music->m_activeCategory = MusicCategory::Gameplay;
                  music->m_hasActiveCategory = true;
                  return !music->currentDisplayName().empty();
              }
      ```
      Если в одном из этих файлов порта есть другой `switch` по `GameKind` без ветки `default`, ветка `Music` добавляется и туда с тем же значением, что у `Hud`; такая правка не выходит за рамку.
15. **Скрипты режима отладки интерфейса (сцена `game-music` входит в части 3б).**
    - `tests/ui_audit/ui_audit_part3b_catalog.py`: в кортеже `BASE_SCENES` после элемента `"game-hud", ` добавляется элемент `"game-music", `; строка `EXPECTED_COUNT = 35` становится `EXPECTED_COUNT = 36`.
    - `tests/ui_audit/ui_audit_part3b_scenes.py`: после строки `BUILD_ITEM = "build-item:"` добавляется строка `MUSIC_CLICKS = ("music-previous", "music-next", "music-speed-slider")`; перед функцией `def check_for(scene_id):` добавляется функция:
      ```python
      def check_music(scene_id, header, body, bodies):
          clicks = []
          for name in MUSIC_CLICKS:
              record, error = base.one_record(body, "click", "name", name)
              if error:
                  return error
              clicks.append(record)
          previous, following, slider = clicks
          options = named(body, "click", "top-options")[0]
          outside = [record for record in clicks if not base.inside(record, base.TOP_PANEL)]
          return base.first_error(
              f"click records outside {base.TOP_PANEL}: {outside}" if outside else None,
              None if options["x"] + options["w"] <= previous["x"]
              else f"the music buttons overlap the options button: {options} and {previous}",
              None if previous["x"] + previous["w"] <= following["x"]
              else f"the previous button overlaps the next button: {previous} and {following}",
              None if following["x"] + following["w"] <= slider["x"]
              else f"the next button overlaps the speed slider: {following} and {slider}",
              base.require_text(body, "<"),
              base.require_text(body, ">"),
              base.require_text(body, "SPEED"),
              None if any(record["s"].endswith("...") for record in base.records_of(body, "text"))
              else "no text record with a truncated track name",
          )
      ```
      в словаре `fixed` функции `check_for` после строки `"game-hud": check_nothing_more,` добавляется строка `"game-music": check_music,`. Если проверка падает из-за предположения, которое вывод игры опровергает (порядок прямоугольников или текст записи), правится сама проверка по выводу и это записывается строкой «Решено исполнителем».
16. **Ничего сверх контракта.** Других изменений нет: ни переформатирования, ни новых комментариев, ни переноса строк сверх нужного для правки. `MusicJukeBox.*`, `MusicChoice.hpp`, `cGame.h`, `cMessageDrawer.h`, `src/main.cpp`, `src/game/Preferences.cpp`, `tests/utils/test_MusicJukeBox.cpp` не меняются.

## Сохранить из апстрима

Это поведение порта остаётся после переноса.

1. Звуки и голоса `AudioContext`: `playSound` (обе), `playVoice`, `getMaxVolume`; громкость музыки — `changeMusicVolume`, `cSoundPlayer::setMusicVolume`.
2. `MusicJukeBox`, `MusicChoice`, их тест `tests/utils/test_MusicJukeBox.cpp` (семь случаев, тег `[musicjukebox]`) и ключ `customMusic` в `preferences.ini` (чтение и запись) — без правок; игра `MusicJukeBox` не вызывает.
3. Клавиши `M` и `Mute` (`TOGGLE_MUSIC`), `O` и `P` (громкость) — привязки не меняются; поведение клавиши `M` по пункту 9 контракта.
4. Переключение музыки в главном меню (`cMainMenuState::onNotifyKeyboardEvent`) и флажок музыки в окне настроек (`cOptionsState`, вызов `audioContext->setMusicEnabled`) — код не меняется; флажок теперь вызывает новое тело `setMusicEnabled`.
5. Звук включения радара, звуки кредитов и все прочие вызовы `m_audioContext->playSound` и `playVoice` — не меняются.
6. Сцены режима отладки интерфейса, кроме `game-music`, и их проверки — без правок; новые записи click `music-*` присутствуют в каждой боевой сцене, потому что панель музыки рисуется в каждом боевом кадре.

## Не делать в этом шаге

- Смену рабочего каталога игры (`src/main.cpp`, шаг П8), сохранения (`cGame.h`, `cGame_logic.cpp` вне функции `onKeyPressedGame`), панель приказов (`cDrawManager`: член и вызов панели приказов, `cGamePlaying`), очередь Starport, ментатов.
- Упаковку музыки в релиз и workflows (шаг П12).
- Перевод подписи встроенного трека `Dune II #N`.
- Рисование и новые картинки (Р70).

## Тесты

Тесты пишутся в шаге 1 плана. В шаге 2 они собираются и краснеют до правок шагов 3 и 4: без файлов `src/audio/MusicPlaylist.cpp`, `MusicPlaylist.h`, `MusicController.h`, `MusicTransitionPolicy.hpp` и `src/sidebar/MusicControlsLayout.hpp` сборка тестов не проходит. У всех случаев тег `[P9]`, названия случаев начинаются со слов `P9 `. Все файлы подключают `<catch2/catch_test_macros.hpp>`. Тесты форка — отдельные программы с `main()`, не Catch2; число проверок в новых файлах не меньше числа проверок в файлах форка (15 + 3 + 4).

### T1 — `tests/utils/test_MusicPlaylist.cpp` (источник — `FORK1:tests/MusicPlaylistTests.cpp`)

Подключает `audio/MusicPlaylist.h`, `<algorithm>`, `<filesystem>`, `<fstream>`, `<set>`, `<string>`, `<vector>`. Помощник `builtInTracks(int count)` — как в форке (строки 12–19). Помощник `TempDirectory` — структура с полем `std::filesystem::path path = std::filesystem::temp_directory_path() / "d2tm_music_playlist_test"`; конструктор делает `remove_all` и `create_directories`; деструктор делает `remove_all` с `std::error_code`.

- **Случай 1** `"P9 music playlist shuffles every track once and keeps history"`: `MusicPlaylist playlist(0xD2U); playlist.setTracks(builtInTracks(5));` Цикл из пяти вызовов `next()`: каждый результат не `nullptr` (`REQUIRE(track != nullptr)` внутри цикла), ключи `key()` пяти треков собираются в `std::set<std::string>`; затем `REQUIRE(firstCycle.size() == 5U)`. `lastOfCycle` — ключ `current()`; следующий `next()` не `nullptr`, и его ключ не равен `lastOfCycle`. `current` — ключ `current()`; `previous()` не `nullptr`, и его ключ равен `lastOfCycle`; следующий `next()` не `nullptr`, и его ключ равен `current`. Итого восемь `REQUIRE`.
- **Случай 2** `"P9 music playlist discovers external tracks by extension"`: каталог `TempDirectory`; файлы `zeta.OGG`, `alpha.mp3`, `track.wav`, `ignored.txt` и `std::filesystem::path(u8"пустыня.flac")`, в каждый записан один байт `'\0'`. `MusicPlaylist::discoverExternalTracks(каталог)`: `REQUIRE(discovered.size() == 4U)`; имена файлов `discovered[0]`, `[1]`, `[2]` равны `alpha.mp3`, `track.wav`, `zeta.OGG` (три `REQUIRE` на `externalPath.filename()`); `REQUIRE(std::any_of(…))` — файл `пустыня.flac` найден; `REQUIRE(MusicPlaylist::isSupportedMusicFile("theme.FLAC"))`; `REQUIRE_FALSE(MusicPlaylist::isSupportedMusicFile("notes.txt"))`. Итого семь `REQUIRE`.
- **Случай 3** `"P9 music tracks have display names and a discarded track leaves the playlist"` (новый): `REQUIRE(MusicTrack{4, {}}.displayName() == "Dune II #5")`; `REQUIRE(MusicTrack{-1, "music/gameplay/Track 1.wav"}.displayName() == "Track 1")`; `MusicPlaylist playlist(0xD2U); playlist.setTracks(builtInTracks(3)); playlist.next(); playlist.discardCurrent();` затем `REQUIRE(playlist.size() == 2U)` и `REQUIRE(playlist.current() == nullptr)`.

### T2 — `tests/utils/test_MusicTransitionPolicy.cpp` (источник — `FORK1:tests/MusicTransitionPolicyTests.cpp`)

Подключает `audio/MusicTransitionPolicy.hpp` и `audio/MusicController.h`.

- **Случай 4** `"P9 repeated music category does not advance the track"`: `REQUIRE_FALSE(shouldAdvanceRepeatedMusicCategory(true, true))`; `REQUIRE_FALSE(shouldAdvanceRepeatedMusicCategory(true, false))`; `REQUIRE(shouldAdvanceRepeatedMusicCategory(false, false))`.
- **Случай 5** `"P9 music category routing follows the fork pools"` (новый): `REQUIRE(musicCategoryFor(<тип>, <дом>) == <категория>)` для одиннадцати наборов: `PEACE, 0` → `Gameplay`; `ATTACK, 0` → `Gameplay`; `MENU, 0` → `Menu`; `CONQUEST, 0` → `Conquest`; `WIN, 0` → `Victory`; `LOSE, 0` → `Defeat`; `BRIEFING, ATREIDES` → `BriefingAtreides`; `BRIEFING, HARKONNEN` → `BriefingHarkonnen`; `BRIEFING, ORDOS` → `BriefingOrdos`; `BRIEFING, SARDAUKAR` → `BriefingAtreides`; `BRIEFING, GENERALHOUSE` → `BriefingAtreides` (типы — `eMusicType::…`, категории — `MusicCategory::…`).

### T3 — `tests/utils/test_MusicControlsLayout.cpp` (источник — `FORK1:tests/MusicControlsLayoutTests.cpp`)

Подключает `sidebar/HudLayout.hpp`, `sidebar/MusicControlsLayout.hpp`, `<algorithm>`, `<array>`, `<cstdlib>`. Помощник `checkMusicControls(int width, int height)` строит `const HudLayout hud = HudLayout::create(width, height);` и `const MusicControlsLayout music = MusicControlsLayout::create(143, hud.battlefield.getEndX() - 8);`, затем содержит ровно двенадцать проверок в этом порядке:

1. `REQUIRE(music.visible)`;
2. `REQUIRE(music.panel.getWidth() <= 520)`;
3. `REQUIRE_FALSE(music.previous.isOverlapping(music.next))`;
4. `REQUIRE(music.panel.getEndX() <= hud.battlefield.getEndX())`;
5. `REQUIRE(music.panel.getEndY() <= HudLayout::TopBarHeight)`;
6. прямоугольник `message` строится как в форке (строки 21–26: `music.panel.getEndX() + 8`, `4`, `std::max(0, hud.battlefield.getEndX() - 8 - music.panel.getEndX() - 8)`, `33`); при `message.getWidth() > 0` выполняется `REQUIRE_FALSE(message.isOverlapping(music.panel))`;
7. при `music.showsLabel()` выполняется `REQUIRE_FALSE(music.label.isOverlapping(music.previous))`;
8. в том же условии выполняется `REQUIRE_FALSE(music.label.isOverlapping(music.next))`;
9. `REQUIRE_FALSE(music.musicPanel.isOverlapping(music.speedPanel))`;
10. `REQUIRE_FALSE(music.speedLabel.isOverlapping(music.speedSlider))`;
11. `REQUIRE(music.speedSlider.getWidth() >= 50)`;
12. `REQUIRE(std::abs(music.musicPanel.getWidth() - music.speedPanel.getWidth()) <= 1)`.

- **Случай 6** `"P9 music controls fit the top bar on three canvases"`: цикл по `std::array<std::array<int, 2>, 3>{{{800, 600}, {1920, 1080}, {3440, 1440}}}`; перед вызовом помощника `INFO("canvas " << width << "x" << height);`.

### T4 — `tests/controls/test_MusicKeyBindings.cpp` (новый; в форке клавиши `[` и `]` читались скан-кодами без таблицы)

Подключает `<catch2/catch_test_macros.hpp>`, `<bitset>`, `<string>`, `controls/cKeyBindings.h`, `utils/cIniFile.h`. Помощник `pressed(SDL_Scancode)` — как в `tests/controls/test_cKeyBindings.cpp` (`std::bitset<SDL_SCANCODE_COUNT>` с одним взведённым битом). Помощник `loadedFromSettingsIni()` создаёт `cKeyBindings`, вызывает `loadDefaults()`, создаёт `cIniFile ini(std::string(D2TM_SOURCE_DIR) + "/resources/bin/settings.ini");`, вызывает `loadFromSection(ini.getSection("KEYS"))` и возвращает привязки.

- **Случай 7** `"P9 music track keys are bound to square brackets by default"`: после `loadDefaults()` `REQUIRE(matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK))`; `REQUIRE(matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK))`; `REQUIRE_FALSE(matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_NEXT_TRACK))`; `REQUIRE_FALSE(matches(pressed(SDL_SCANCODE_RIGHTBRACKET), s_KeysCombo{}, eKeyAction::MUSIC_PREVIOUS_TRACK))`.
- **Случай 8** `"P9 music track keys load from the shipped settings.ini"`: секция `KEYS` файла `resources/bin/settings.ini`: `REQUIRE(section.hasValue("MUSIC_PREVIOUS_TRACK"))`, `REQUIRE(section.getStringValue("MUSIC_PREVIOUS_TRACK") == "[")`, `REQUIRE(section.hasValue("MUSIC_NEXT_TRACK"))`, `REQUIRE(section.getStringValue("MUSIC_NEXT_TRACK") == "]")`; затем те же четыре проверки `matches`, что в случае 7, на привязках из `loadedFromSettingsIni()`.
- **Случай 9** `"P9 square bracket keys are not shared with another action"`: на привязках из `loadedFromSettingsIni()` для каждого значения `i` от `0` до `static_cast<int>(eKeyAction::DEBUG_SWITCH_PLAYER_3)` включительно считается число действий `static_cast<eKeyAction>(i)`, для которых `matches(pressed(SDL_SCANCODE_LEFTBRACKET), s_KeysCombo{}, <действие>)` истинно; `REQUIRE(count == 1)`; так же для `SDL_SCANCODE_RIGHTBRACKET`. Это проверка, что `checkForClashes` не находит общей клавиши у новых действий и прежних.

### Таблица «проверка форка → случай Catch2»

«Номер `REQUIRE`» — порядковый номер проверки внутри случая в порядке, описанном выше.

| Проверка форка | Случай Catch2 и номер `REQUIRE` |
|---|---|
| `MusicPlaylistTests.cpp:30` (`track != nullptr` в цикле) | случай 1, номер 1 |
| `:33` (`firstCycle.size() == 5U`) | случай 1, номер 2 |
| `:37`, `:38` | случай 1, номера 3 и 4 |
| `:42`, `:43` | случай 1, номера 5 и 6 |
| `:45`, `:46` | случай 1, номера 7 и 8 |
| `:58` (`discovered.size() == 4U`) | случай 2, номер 1 |
| `:59`, `:60`, `:61` (имена по порядку) | случай 2, номера 2, 3 и 4 |
| `:62`–`:64` (файл `пустыня.flac`) | случай 2, номер 5 |
| `:65`, `:66` (`isSupportedMusicFile`) | случай 2, номера 6 и 7 |
| `MusicTransitionPolicyTests.cpp:6`, `:7`, `:8` | случай 4, номера 1, 2 и 3 |
| `MusicControlsLayoutTests.cpp:14`–`:17` (пять условий первого `if`) | случай 6, проверки 1–5 помощника `checkMusicControls` |
| `:27` (сообщение не пересекает панель) | случай 6, проверка 6 помощника |
| `:31`, `:32` (подпись не пересекает кнопки) | случай 6, проверки 7 и 8 помощника |
| `:36`–`:39` (секции музыки и скорости) | случай 6, проверки 9–12 помощника |

### Подключение к сборке

- **`tests/CMakeLists.txt`, `TEST_FILES`:** сразу после строки `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MusicJukeBox.cpp` добавляются четыре строки, в этом порядке:
  - `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MusicPlaylist.cpp`;
  - `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MusicTransitionPolicy.cpp`;
  - `    ${CMAKE_CURRENT_SOURCE_DIR}/utils/test_MusicControlsLayout.cpp`;
  - `    ${CMAKE_CURRENT_SOURCE_DIR}/controls/test_MusicKeyBindings.cpp`.
- **`tests/CMakeLists.txt`, `TEST_SOURCES`:** сразу после строки `    ${CMAKE_SOURCE_DIR}/src/context/MusicJukeBox.cpp` добавляется строка `    ${CMAKE_SOURCE_DIR}/src/audio/MusicPlaylist.cpp`. Остальные строки обоих списков не меняются; `cRectangle.cpp`, `cKeyBindings.cpp` и `cIniFile.cpp` в `TEST_SOURCES` уже есть.

## PLAN-P9

| шаг | файлы | что сделать | кто |
|---|---|---|---|
| 1 | `tests/utils/test_MusicPlaylist.cpp`, `tests/utils/test_MusicTransitionPolicy.cpp`, `tests/utils/test_MusicControlsLayout.cpp`, `tests/controls/test_MusicKeyBindings.cpp`, `tests/CMakeLists.txt` | Раздел «Тесты». | помощник A |
| 2 | — | Красный прогон: команда сборки проверки 1, у которой вместо `.tmp/p9/build.log` стоит `.tmp/p9/red-build.log`, — `exit` не `0`, в логе есть строка с `src/audio/MusicPlaylist.cpp`. Запускается до того, как шаги 3 и 4 записали файлы `src/audio/MusicPlaylist.h`, `src/audio/MusicPlaylist.cpp`, `src/audio/MusicController.h`, `src/audio/MusicController.cpp`, `src/audio/MusicTransitionPolicy.hpp`, `src/sidebar/MusicControlsLayout.hpp` и правку `src/CMakeLists.txt`. | помощник A |
| 3 | `src/audio/MusicPlaylist.h`, `src/audio/MusicPlaylist.cpp`, `src/audio/MusicController.h`, `src/audio/MusicController.cpp`, `src/audio/MusicTransitionPolicy.hpp`, `src/sidebar/MusicControlsLayout.hpp`, `src/CMakeLists.txt`, `src/utils/cSoundPlayer.h`, `src/utils/cSoundPlayer.cpp`, `src/context/AudioContext.hpp`, `src/context/AudioContext.cpp`, `src/gameobjects/players/cPlayer.h`, `src/gameobjects/players/cPlayer.cpp`, `src/controls/eKeyAction.h`, `src/controls/cKeyBindings.cpp`, `resources/bin/settings.ini`, `src/game/cGame_logic.cpp`, `.gitattributes`, `tools/upstream/build_upstream_linux.sh`, `tools/export_music.py` | Пункты 1–11 контракта. | помощник B |
| 4 | `src/drawers/cMessageDrawer.cpp`, `src/managers/cDrawManager.h`, `src/managers/cDrawManager.cpp`, `src/debug/UiAudit.hpp`, `src/debug/UiAuditAccess.cpp`, `src/debug/UiAuditScenes.cpp`, `tests/ui_audit/ui_audit_part3b_catalog.py`, `tests/ui_audit/ui_audit_part3b_scenes.py` | Пункты 12–15 контракта. | помощник C |
| 5 | — | Проверки раздела «Проверки» по порядку. | помощник A |

## Проверки

Все команды — из корня рабочей копии `/srv/library/dune/worktrees/p9`.

1. **Место и сборка.**
   - `df -m /srv/library` — в столбце `Available` не меньше 5000, иначе блок `## Q-P9-NN` и стоп.
   - Сборка: `mkdir -p .tmp/p9 && CCACHE_DISABLE=1 DUNE_DEPS_DIR=/srv/library/dune/deps DUNE_OUT_DIR=$PWD/.tmp/out bash tools/upstream/build_upstream_linux.sh d06f2fcd2a347182c3774fb96e9a85570405c489 > .tmp/p9/build.log 2>&1; echo exit=$?` — `exit=0`.
   - Итоговая строка `ctest.log` последней папки логов `.tmp/out/logs/` — `100% tests passed, 0 tests failed out of <N>`, где `<N>` больше 345.
   - `cd .tmp/out/build && ctest -N -R '^P9 ' | tail -n 1` — `Total Tests: 9`.
   - `mkdir -p .tmp/p9/tmp && cd .tmp/out/build && TMPDIR=$PWD/../../p9/tmp ctest -R '^P9 ' --output-on-failure | tail -n 3` — строка `100% tests passed, 0 tests failed out of 9`.
   - `CCACHE_DISABLE=1` обязателен: `ccache` пишет в `/root/.cache`, который песочница нити держит только для чтения. Папку `/srv/library/dune/deps` сборка только читает; в неё ничего не пиши.
2. `grep -n 'warning:' .tmp/out/logs/<последняя папка>/full.log | grep -F -f .tmp/p9/changed-paths.txt` — пустой вывод. Файл `.tmp/p9/changed-paths.txt` — пути файлов `.cpp`, `.hpp` и `.h` из шагов 1, 3 и 4 плана, по одному на строку.
3. В `game-dummy.log` и `stdout-dummy.log` последней папки логов нет строки `Imminent crash`.
4. **Пулы музыки в журнале игры.** В `game-dummy.log` последней папки логов:
   - `grep -c 'custom track(s)' <файл>` — `8`;
   - `grep -c 'music/gameplay: 11 custom track(s)' <файл>` — `1`;
   - `grep -cE 'music/(menu|conquest|briefing/atreides|briefing/harkonnen|briefing/ordos): 1 custom track\(s\)' <файл>` — `5`;
   - `grep -cE 'music/(victory|defeat): 3 custom track\(s\)' <файл>` — `2`;
   - `grep -c 'Custom music skipped' <файл>` — `0`.
5. **Данные музыки.** Команда:
   `export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; F=9208dcf5a358f40afd95c99480e4e09f781ed566; git ls-tree -r --name-only $F resources/bin/music | while IFS= read -r f; do want=$(git show "$F:$f" | sed -n 's/^oid sha256://p'); have=$(sha256sum "$f" | cut -d' ' -f1); if [ "$want" = "$have" ]; then echo "OK $f"; else echo "BAD $f"; fi; done > .tmp/p9/music-sha.log; grep -c '^OK ' .tmp/p9/music-sha.log; grep -c '^BAD ' .tmp/p9/music-sha.log` — выводы `22` и `0`.
6. **Сверки `grep`** (в скобках — ожидаемый вывод):
   - `git grep -n 'createRepertoryDirectories' -- src | grep -v 'src/context/MusicJukeBox\.'; echo done` (одна строка `done`);
   - `git grep -n 'MusicJukeBox' -- src | grep -v 'src/context/MusicJukeBox\.'` (ровно одна строка — `src/CMakeLists.txt` со строкой `context/MusicJukeBox.cpp`);
   - `git grep -n 'eMusicType::ATTACK' -- src/gameobjects src/gamestates src/game; echo done` (одна строка `done`);
   - `git grep -n 'playMusicFile' -- src` (ровно три строки: `src/audio/MusicController.cpp`, `src/utils/cSoundPlayer.cpp`, `src/utils/cSoundPlayer.h`);
   - `git grep -nE 'cLogger|cLog\.h|SDL2/|renderDrawer|game\.m_screen|game\.getMouse' -- src/audio src/sidebar/MusicControlsLayout.hpp src/drawers/cMessageDrawer.cpp src/managers/cDrawManager.cpp src/debug; echo done` (одна строка `done`);
   - `git grep -nE 'm_newMusic|m_jukeBox|startMusic' -- src/context/AudioContext.cpp src/context/AudioContext.hpp; echo done` (одна строка `done`);
   - `grep -c 'MUSIC_PREVIOUS_TRACK' src/controls/eKeyAction.h src/controls/cKeyBindings.cpp resources/bin/settings.ini` (`src/controls/eKeyAction.h:1`, `src/controls/cKeyBindings.cpp:2`, `resources/bin/settings.ini:1`);
   - `grep -c 'drawMusicControls' src/managers/cDrawManager.cpp src/managers/cDrawManager.h` (`src/managers/cDrawManager.cpp:2`, `src/managers/cDrawManager.h:1`);
   - `grep -c 'drawTopBarMusicControls' src/managers/cDrawManager.cpp` (`2`);
   - `grep -c 'recordClick("music-' src/managers/cDrawManager.cpp` (`3`);
   - `grep -c 'game-music' src/debug/UiAuditScenes.cpp tests/ui_audit/ui_audit_part3b_catalog.py tests/ui_audit/ui_audit_part3b_scenes.py` (по `1` у каждого файла);
   - `grep -cE '\b(REQUIRE|REQUIRE_FALSE|CHECK)\(' tests/utils/test_MusicPlaylist.cpp tests/utils/test_MusicTransitionPolicy.cpp tests/utils/test_MusicControlsLayout.cpp` (числа не меньше 15, 3 и 4 соответственно).
7. **Скрипты режима отладки интерфейса.**
   - Скрипты: `ui_audit_list_and_scales.py`, `ui_audit_unknown_scene.py`, `ui_audit_main_menu_png.py`, `ui_audit_part3b_catalog.py`, `ui_audit_part3b_scenes.py`, `ui_audit_language.py`, `ui_audit_translation.py`.
   - Команда для каждого `<скрипт>`: `mkdir -p .tmp/p9/tmp && TMPDIR=$PWD/.tmp/p9/tmp LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib timeout 1800 python3 -B tests/ui_audit/<скрипт> --run-dir .tmp/out/run/bin > .tmp/p9/run-<скрипт>.log 2>&1; echo exit=$?` — у каждого `exit=0`.
   - Команду проверки не прерывай: ни Ctrl+C, ни kill, ни другой сигнал. Каждая команда сама ограничена `timeout 1800`; жди, пока она вернёт код выхода. `ui_audit_part3b_scenes.py` и `ui_audit_translation.py` идут по несколько минут — это норма.
   - После проверки — `rm -r tests/ui_audit/__pycache__`, если эта папка появилась.
8. **Выгрузка MIDI.** `mkdir -p .tmp/p9/tmp && LD_LIBRARY_PATH=/srv/library/dune/deps/prefix/lib python3 -B tools/export_music.py resources/bin/data/sdl_audio.dat .tmp/p9/export-music; echo exit=$?; ls .tmp/p9/export-music | wc -l` — вывод скрипта `Extracted 26 tracks to .tmp/p9/export-music`, `exit=0`, `28` файлов (26 файлов `.mid`, `README_RU.md`, `music_manifest.csv`).
9. `git -c lfs.storage=$PWD/.tmp/p9/lfs status --short` — изменённые (` M`) пути — только пути шагов 1, 3 и 4 плана; новые (`??`) — только `src/audio/`, `src/sidebar/MusicControlsLayout.hpp`, `tests/controls/test_MusicKeyBindings.cpp`, `tests/utils/test_MusicPlaylist.cpp`, `tests/utils/test_MusicTransitionPolicy.cpp`, `tests/utils/test_MusicControlsLayout.cpp`, `tools/export_music.py` и `resources/bin/music/` (его кладёт ведущий).

Расхождение в любой проверке, которое не убирается правкой в рамке правок по плану, — блок `## Q-P9-NN` с выводом и стоп. Ожидания существующих тестов и скрипты в `tests/ui_audit/`, кроме двух файлов пункта 15 контракта, не меняй.

## Сдача

Последнее сообщение — блок `## DONE-P9 | <время UTC из date -u> | HEAD <sha>` по форме из правил ниже. В нём:

- журнал хода (`.tmp/p9/progress.md`): строка на каждый шаг плана;
- красный прогон шага 2: строки `.tmp/p9/red-build.log` с `error` (не больше 30);
- вывод каждой проверки 1–9 с кодами выхода (не больше 40 строк на проверку);
- `git diff --stat` и список для коммитов:
  1. тесты: файлы шага 1;
  2. перенос музыки форка: файлы `src/audio/*`, `src/sidebar/MusicControlsLayout.hpp`, `src/CMakeLists.txt`, `src/utils/cSoundPlayer.*`, `src/context/AudioContext.*`, `src/gameobjects/players/cPlayer.*`, `src/controls/eKeyAction.h`, `src/controls/cKeyBindings.cpp`, `resources/bin/settings.ini`, `src/game/cGame_logic.cpp`, `.gitattributes`, `tools/upstream/build_upstream_linux.sh`, `tools/export_music.py`;
  3. панель музыки и режим отладки: файлы шага 4.

  У каждого коммита — сообщение на английском, последняя строка — `Behavior changes: …`;
- раздел «Решено исполнителем» — каждая такая строка по правилам исполнителя ниже;
- раздел «Рабочие места»: вывод `python3 /srv/dune/tools/task-places.py inventory .tmp/p9 --size`; у `.tmp/p9` пометка `оставить — логи проверок нужны ревью`. Копию `previous-run` в папке логов сборки не удаляй — её удаляет ведущий после приёмки.

Числа в сдаче — только из вывода команд.

## Организация работы

- **Порядок:**
  1. `create_goal` первым действием, по правилам исполнителя ниже; objective — текст раздела «Цель» дословно.
  2. Раздел «Прочитать до работы».
  3. Шаг 1 (помощник A), шаг 3 (помощник B) и шаг 4 (помощник C) — одновременно. Помощник B не создаёт файлы `src/audio/*`, `src/sidebar/MusicControlsLayout.hpp` и не правит `src/CMakeLists.txt`, пока помощник A не записал в журнал хода строку о конце шага 2; остальные файлы своего шага он правит сразу.
  4. Шаг 2 (помощник A) — сразу после шага 1.
  5. Шаг 5 (помощник A) — после шагов 2, 3 и 4.
  6. Сдача и стоп.
- **Параллельно:** шаги 1, 3 и 4 правят разные файлы. Общего у них только порядок записи новых файлов (пункт 3 порядка) и имена, которые контракт называет заранее: `AudioContext::playPreviousTrack`, `playNextTrack`, `getCurrentMusicTrackName`, члены `AudioContext::m_musicController` и `MusicController::m_categories`, `m_activeCategory`, `m_hasActiveCategory`. Помощник C пишет вызовы по этим именам и не ждёт помощника B. Собирает их вместе проверка 1 шага 5.
- **Помощники:** три, `gpt-6-luna` `xhigh`, без вложенных; одновременно работают все три. Ожидаемое время: помощник A — 40 минут на шаги 1–2 и 90 минут на шаг 5; помощник B — 60 минут; помощник C — 60 минут.
  - В бриф каждого помощника дословно входят: разделы «Что уже решено», «Сохранить из апстрима» и «Не делать в этом шаге»; его шаги плана; абзац «Комментарии в коде»; запрет править файлы вне его шагов плана и `.tmp/p9/`. Кроме того, дословно входят: у помощника A — разделы «Тесты» и «Проверки»; у помощника B — подраздел «Правила переноса» и пункты 1–11 и 16 контракта; у помощника C — подраздел «Правила переноса» и пункты 12–16 контракта.
  - Корневая нить раздаёт шаги, разбирает ошибки сборки и проверок по выводу помощников и поручает правку помощнику того шага, чей файл. Скрипты и правки корневая нить сама не делает.
- **Остановки:** только на `## DONE-P9` и на блоках `## Q-P9-NN`. Команда оболочки дважды подряд не завершилась (нет кода выхода) — блок `## Q-P9-NN` и стоп.
- **Рамка правок:** файлы шагов 1, 3 и 4 плана и папка `.tmp/p9/`. Понадобился другой файл — блок `## Q-P9-NN` и стоп. Сборка пишет в `.tmp/out/`, игра — в `.tmp/out/run/bin/` (там же создаётся `music/` при запуске) и во временные папки скриптов; это не правка.
- Не больше трёх помощников одновременно.

Не отступай от плана, не переусложняй.

## Комментарии в коде

Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.

<!-- team-process:executor-rules sha256=a9bda9c6318255670aecab75810e663ed3ef91095a214b541ff20d2adede49dd -->
## Обязательно: правила исполнителя

«Ведущий» в этих правилах — тот, кто ведёт твою задачу: он дал задание и принимает сдачу.

- Ожидания существующих тестов не менять; единственное исключение и порядок вопроса — раздел «Вопросы и остановки». Новый тест добавлять можно. Тест падает из-за программы — чинить программу, а не обходить ошибку в тесте.
- Не утверждать прогон без лога. Не выдумывать файлы, API, цитаты, результаты. Непроверенное пометить «не проверено». Уверенность данных не выше источника. Отметку о выполнении в списке задач ставить только со следом проверки — тестом или строкой вывода.
- Один круг самоаудита на сдачу; повторный обход того же — `Q`.
- Фоновые команды. Среда сама будит тебя, когда фоновая команда кончилась (сессия Claude: запуск с `run_in_background`), — долгий прогон запускай в фоне и делай тем временем то, что от него не зависит. Среда не будит (нить Codex) — фоновых команд нет: после остановки исполнителя никто его не разбудит; длинные прогоны — в переднем плане, с таймаутом до 30 минут. Ожидание циклом (`while …; sleep`) запрещено в обоих случаях.
- Git по договорённости с ведущим. Например: Codex по договорённости не пишет в git — ветку и коммиты делает ведущий после ревью; Claude и Cursor коммитят сами; никто не делает `push`, `rebase`, `reset --hard`, `clean`, `gh … create/edit/merge`. Пуш — через ведущего.
- Добавлять в коммит только свои файлы по именам, без `git add -A`; перед коммитом смотреть `git diff --cached --summary` и `--stat`; всё, что не относится к пункту, — отдельным коммитом.
- Режимы файлов (chmod от `npm ci`) и машинные пути в коммит не попадают.
- Общая машина: чужие сервисы и контейнеры не останавливать и не менять (пользоваться ими как клиент можно), секреты не печатать, писать только в отведённую папку, тесты с БД — только через выданный слот. Крупные артефакты (сборки, дампы, модели) — в одном экземпляре. Останавливать только свои процессы — по PID или группе, записанным при запуске; `pkill` и `killall` по имени запрещены: тем же именем на общей машине идут чужие прогоны.
- Папка задачи. Всё, что создаёшь вне рабочей копии (клоны, деревья сборки, копии для стендов, временные файлы), клади только в папку задачи из задания; временные файлы — в её `tmp`, системные `/tmp` и `%TEMP%` не используй. В репозиторий и в корень рабочей копии ничего временного не клади. Новую полную копию исходников не создавай, если можно обойтись `git worktree add` от имеющегося клона. Нужно место вне папки задачи — `Q`. Удалять что-либо вне своей `tmp` — только по разделу «Уборка».
- Механику — субагентам младших моделей и скриптам; сам — суждение и итоговая сверка.
- Субагенту, которого запускаешь, назначь ожидаемое время работы и запиши его в журнал хода. Время вышло, а итога нет — проверь, как он идёт: скриптом по его журналу или списком агентов среды, а не ожиданием. Стоит или ушёл в сторону — останови и перезапусти с более узкой задачей.
- **Чтение.** До разведки и работы прочитать целиком всё из раздела задания «Прочитать до работы». В разведке `RECON`, а без неё в первой сдаче, — раздел «Чтение»: что прочитано из списка, и «не хватает в задании» — правило, норма или контракт, на которые опираются действия задания, но которых нет в списке (ссылка в задании или в прочитанном документе); их прочитать до этой сдачи и назвать с причиной. Каждый файл — отдельным вызовом; вывод обрезан (`Warning: truncated output`) — дочитать частями до конца. Ведущий проверяет чтение скриптом по транскрипту: обрезанный вывод — не чтение.
- **Цель нити (исполнитель Codex).** Задание даёт цель нити — первым действием вызвать `create_goal` с objective из задания дословно; после каждого сжатия контекста и перед каждым подпунктом читать файл цели и работать по нему; `update_goal` со статусом `complete` — только после сообщения ведущего о приёмке; субагентам цель не ставить.
- **Строка хода (исполнитель Codex).** После чтения до работы и после каждого закрытого пункта задания или плана ведущего — отдельной строкой ответа: `ХОД: [x] <пункт>; [>] <пункт>; [ ] <пункт>`. В строке все пункты по порядку: `[x]` — сделан, `[>]` — в работе, `[ ]` — впереди. По этой строке панель ведущего и владельца показывает план и ход. Исполнитель в сессии Claude строку хода не пишет.
- **Сжатие контекста (исполнитель в сессии Claude).** На границе своих частей — часть закрыта, журнал хода обновлён — сам вызови `request_compact` и закончи ход. В `instructions`: задание, текущая часть и следующий шаг, id фоновых задач и сессий, пути, решения, открытые вопросы и строка «после сжатия перечитай раздел правил в задании». Посреди части не сжимай. После сжатия перечитай задание и журнал хода.

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
- дословное исполнение задания оставляет обход цели, отвергает честный случай или спорит с целью — `Q` до работы, а не пометка в сдаче;
- конфликт плана с кодом, нормой или данными;
- у технического вопроса нет рекомендации;
- исправление своего инструмента задевает замороженные файлы, assert или production-код, либо тот же инструмент ломается третий раз.

**Без вопроса.** В журнал хода и в сдачу — строка «Решено исполнителем: <что> → <решение>; файл:строка, было → стало; основание: <требование задания, вывод команды или проверка>».
- технический вопрос с твоей рекомендацией — выбор способа внутри рамки правок и критерия готовности задания: имя и место своего файла, порядок своих действий внутри одного шага плана, толкование формата вывода, которое не меняет результат проверки;
- подготовка данных своего теста, в том числе способом, уже применённым в том же файле;
- ошибка компиляции или времени жизни в тестовом помощнике, если проверки не меняются;
- ожидание существующего незамороженного теста, которое прямо противоречит требованию задания;
- известный обход среды, названный в задании;
- ошибка своего инструмента (скрипт сверки, подготовка запроса теста, сбор логов): исправь и повтори в том же прогоне, сохранив вывод каждого запуска; «один круг самоаудита» относится к сдаче, а не к своим инструментам.

**Вопросы — одним блоком.** До первой остановки пройди этап до первого действия, меняющего файлы, и задай все вопросы этапа одним блоком `Q`.

## Объём и порядок работы

- Делать продукт, а не доказательства. Отчётных артефактов сверх формы сдачи, журнала хода и того, что прямо называет задание, не заводить: квитанций, «официальных прогонов», привязки к хэшам сборки, новых отчётных документов. Доказательство — коммит, тест и строка вывода прогона. Журнал хода — один файл, по строке на законченный подпункт (что сделано, коммит, тест); отдельных документов на подпункт не заводить. Причина: исполнитель уже тратил около трёх четвертей работы на квитанции, журналы и «официальные прогоны» вместо продукта.
- Не заводить себе правил, которые останавливают работу (например, полный прогон после каждой правки): по ходу — точечные тесты, полный прогон — полная команда проверки, названная в задании (другие наборы проверок репозитория не добавлять), после последней правки (упал — исправить причину и повторить).
- Не добавлять цели и результаты, которых нет в задании (примеры из практики: установщики, аудиты лицензий, подготовка к распространению); шаги реализации требуемого результата допускаются. Новый результат — только с согласия ведущего или владельца; найденное вне задачи — перечислить в сдаче.
- **Обязательно: простейшее решение, которое полностью закрывает задачу.** Не предусматривать сценарии, которых нет ни в задании, ни в данных продукта; не строить «на будущее» защиту, обобщения, настройки и проверки случаев, невозможность которых следует из контракта продукта (отсутствие случая в выборке данных невозможность не доказывает). Сомнение, нужен ли случай, — неблокирующий вопрос в сдаче, а не код. Причина: исполнитель склонен переусложнять и тратить токены на непрошенное вместо функциональности.
- **Общее, а не частное.** Код и поведение — универсальные и масштабируемые: одна логика и одни правила для всего продукта, в любом месте и с любыми сущностями и предметами, а не под конкретное место, персонажа или вещь; частное задают данные. Проблему чинить системно, в общем механизме, а не отдельным исключением для найденного случая.
- **Комментарии в коде.** Категорически запрещено писать комментарий по принципу «полезен, если верен и относится к делу». По умолчанию комментария нет; он должен доказать право на существование: только неочевидное «почему» — инвариант, причина обхода, ссылка на внешнее ограничение. Пересказ кода, планы и история — нет. Внутренние номера находок, планов и решений (`F7`, `A-11b`, `D88`) в комментарий не писать: суть словами. Субагентам и исполнителям этот абзац передавать в бриф дословно.
- План и сдача — буквальным языком: каждое утверждение допускает одно прочтение. Вместо «по возможности», «при необходимости», «и т. п.», «аналогично» — точный список, условие или число; вместо «это», «там», «такой» без ясного предмета — название предмета.
- План пишет ведущий; исполнитель планов не пишет. Не хватает фактов — сдать разведку `RECON` (факты файл:строка, команды и выводы) без развилок, предложений, рекомендаций, плана и правок; план ведущего выполнять дословно и в его порядке; конфликт плана с кодом, нормой или данными — `Q` и стоп.
- Задачи из списка — строго по порядку; независимые части одной задачи идут параллельно, как велит её раздел «Организация работы».
- Замечания ведущего выполнять до следующей задачи. Пришло новое замечание посреди работы — зафиксировать начатое (коммитом, если исполнитель коммитит; иначе строкой журнала хода: что сделано, какие файлы изменены) и перейти к замечанию.
- Не раздувать задачу: тестировать путь пользователя и найденные ошибки, без перебора всех сочетаний.

## Коммиты

- Если исполнитель коммитит по договорённости — коммит на каждый законченный подпункт; от первой правки после последнего коммита до следующего коммита — не дольше 2 часов. Если не коммитит — после законченного подпункта строка журнала хода со списком изменений поведения.
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
- В целевую ветку сливают только ветку с зелёным CI на её последнем коммите; кто сливает (обычно ведущий), тот после слияния проверяет CI целевой ветки и красной её не оставляет.

## Замеры

- «Проверено на <данных>» — только с цифрами: команда замера и строка её вывода (что измерено и сколько вышло, например «страница 244, 126 нажатий, P95 18 мс»); отдельного отчёта о замере не заводить.
- Бюджет скорости задан в задании, правилах проекта или контракте продукта — замерить фактическое значение и сравнить с бюджетом. Превышение — в сдачу с замером; issue заводит ведущий.

## Сдача

Сдача — блок `## DONE-<id> | время | HEAD <sha>`, один на задачу; после возврата `REVIEW` — новая сдача. В ней:

- журнал хода без изменений (строка на подпункт: что сделано, коммит, тест) и строки вывода проверок — красный до правки, зелёный после; отдельной таблицы нет;
- числа только из логов, а не из памяти;
- свои вызовы и вызовы субагентов — числами скрипта по транскрипту: Claude — `tools/usage-daily.py <папка> --session <id>`, Codex — `tools/codex-watch.py`;
- раздел «не проверено» — обязателен; пустым без пояснения не бывает;
- раздел «Рабочие места» — по разделу «Уборка»;
- находки вне задачи — списком; issue заводит ведущий;
- `git status --short`;
- три пункта для владельца простыми словами: что изменилось для пользователя, что не сделано, что нужно от владельца. Отдельного отчёта владельцу не создавать.

## Уборка

- В сдаче — раздел «Рабочие места»: каждый путь из вывода `task-places.py inventory` и каждый путь вне коммитов ветки, созданный задачей и не попавший в вывод. У каждого — размер (`du -sh`), назначение и пометка: `удалить` или `оставить — <почему>`. Назначение — доказательство (на него ссылаются сдача, PR или журнал) или промежуточное; доказательства — только `оставить`.
- Удаляешь только после ответа ведущего `CLEAN-OK-<id задачи>` и только пути из его перечня. Молчание и `CLEAN-CHANGES-<id задачи>` — не удаляешь. Объекты сборки, ненужные для повторной проверки, — тоже только после `CLEAN-OK`.
- Порядок: `task-places.py remove <пути> --refs <живые файлы из задания> --archive <архив из задания> --dry-run`; в выводе есть путь не из перечня `CLEAN-OK` — `Q` и стоп; иначе тот же вызов без `--dry-run`. Итог (удалено, освобождено, архив) — последним сообщением `## CLEAN-DONE-<id задачи>`.
- Свою `tmp` в папке задачи удаляешь сам, без `CLEAN-OK`. Чужое, общее и постоянное не удаляешь.

<!-- /team-process:executor-rules -->
