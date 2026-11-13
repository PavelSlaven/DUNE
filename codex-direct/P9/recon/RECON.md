## RECON-P9R | Tue Nov 10 16:43:24 UTC 2026

## Чтение до разведки

Отдельными вызовами прочитаны:

1. `/srv/dune/tasks/load-check/PORT_PLAN.md` целиком (`cat`). Для П9 прочитаны строки таблицы шага П9, содержание «П9 — музыка на SDL3_mixer» и строка открытого вопроса П9 в разделе 6.
2. `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '9,36p;564,591p;800,845p'`. Вывод содержит строку функции `music-pools`, пути её кода и тестов, а также записи трёх музыкальных тестов реестра.
3. `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р63\.'`. Вывод — одна строка Р63 о переносе на свежий апстрим, принятии новых возможностей как есть и вопросе владельцу при конфликте с функцией форка.
4. Дополнительно к заданному списку прочитаны отдельными вызовами `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/PLAN_units_sega_upstream.md | sed -n '1,260p'` и `git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:codex-direct/launch-card-27.md` целиком. План прямо задаёт для Б9 перенос музыкальных пулов, историю и клавиши `[`/`]` на SDL3_mixer, а также тесты из карты. Карточка 27 подтверждает решения Р4 и Р63.

### Первоначальные команды и релевантные выводы

Команда карты переноса:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/PORT_MAP.md | sed -n '9,36p;564,591p;800,845p'
```

Релевантный вывод:

```text
| music-pools | Музыкальные пулы, история и переключение треков | README_AI §1 | rewrite | adaptive-layout, localization | Б9 | 42 |
### music-pools — Музыкальные пулы, история и переключение треков
Перенести музыкальные пулы, историю воспроизведения и управление треками.
- `CMakeLists.txt` — изменён
- `src/audio/MusicController.cpp` — отсутствует
- `src/audio/MusicController.h` — отсутствует
- `src/audio/MusicPlaylist.cpp` — отсутствует
- `src/audio/MusicPlaylist.h` — отсутствует
- `src/audio/MusicTransitionPolicy.hpp` — отсутствует
- `src/cGame.h` — удалён
- `src/cGame_logic.cpp` — удалён
- `src/drawers/cMessageDrawer.cpp` — изменён
- `src/managers/cDrawManager.cpp` — изменён
- `src/managers/cDrawManager.h` — изменён
- `src/player/cPlayer.cpp` — перемещён в `src/gameobjects/players/cPlayer.cpp`
- `src/player/cPlayer.h` — перемещён в `src/gameobjects/players/cPlayer.h`
- `src/sidebar/MusicControlsLayout.hpp` — отсутствует
- `src/utils/cSoundPlayer.cpp` — изменён
- `src/utils/cSoundPlayer.h` — изменён
- `tests/MusicControlsLayoutTests.cpp` — отсутствует
- `tests/MusicPlaylistTests.cpp` — отсутствует
- `tests/MusicTransitionPolicyTests.cpp` — отсутствует
Остальные пути по каталогу второго уровня: resources/bin: 22; tools: 1
| `tests/MusicControlsLayoutTests.cpp@9208dcf:47` | `music_controls_layout_geometry` (`CMakeLists.txt:431`) | кнопки музыки в HUD; `1`→`src/sidebar/HudLayout.hpp`; `2`→`src/sidebar/MusicControlsLayout.hpp` |
| `tests/MusicPlaylistTests.cpp@9208dcf:22` | `music_playlist_shuffle_history` (`CMakeLists.txt:407`) | shuffle-bag и история треков; `1`→`src/audio/MusicPlaylist.h` |
| `tests/MusicTransitionPolicyTests.cpp@9208dcf:3` | `music_transition_policy` (`CMakeLists.txt:418`) | смена музыкальной категории; `1`→`src/audio/MusicTransitionPolicy.hpp` |
```

Команда решения владельца:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/decisions.md | grep -E '^- \*\*Р63\.'
```

Вывод:

```text
- **Р63. Волна 4 — перенос форка на свежий апстрим.** Графика и перерисовка закончены; задача волны — перенести всё на новый код апстрима, сохранив наработки форка (Р4). Новая база `UP1` — master апстрима в момент запуска первой задачи, `d06f2fcd` на 2026-11-09. Новые возможности апстрима (туман войны с памятью, значок нехватки энергии, предел юнитов, вступительный ролик, `preferences.ini`, папки музыки) берутся как есть; где новинка спорит с функцией форка, ведущий спрашивает владельца на шаге этой функции. Новых задач по графике нет; код и данные игры в `main` не меняются до перемотки на ветку порта, в `main` идут только документы процесса и карта переноса. Шаги П1–П15 — по карточке `codex-direct/launch-card-27.md`. Владелец, 2026-11-09, по карточке 27: «Свежий master», «Все как есть», «Мы закончили с графикой и перерисовкой. Теперь задача всё перенести на их новый код, сохранив наши наработки.»
```

### Недостающие источники

Применимого правила, нормы или контракта, нужного для этих фактических проверок и отсутствующего в задании и перечисленных источниках, не выявлено. Ссылки PORT_PLAN на план обновления и карточку запуска прочитаны до сдачи; тесты, сборки и игровое поведение в этой разведке не исполняются.

## Корневая выборочная сверка

По заданию корневая нить проверила не более трёх фактов каждого помощника.

### Дорожка 1: пункты 1 и 6

Команда и вывод проверки категорий:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.h | sed -n '12,22p'
```

```text
enum class MusicCategory : std::size_t {
    Gameplay,
    Menu,
    Conquest,
    BriefingAtreides,
    BriefingHarkonnen,
    BriefingOrdos,
    Victory,
    Defeat,
    Count
};
```

Команда и вывод проверки внешних файлов:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicPlaylist.cpp | sed -n '122,148p'
```

```text
std::vector<MusicTrack> MusicPlaylist::discoverExternalTracks(const std::filesystem::path &directory)
{
    std::vector<MusicTrack> result;
    std::error_code error;
    if (!std::filesystem::is_directory(directory, error)) {
        return result;
    }

    for (const auto &entry : std::filesystem::directory_iterator(directory, error)) {
        if (error || !entry.is_regular_file(error)) {
            continue;
        }
        if (isSupportedMusicFile(entry.path())) {
            result.push_back(MusicTrack{-1, entry.path()});
        }
    }
    std::sort(result.begin(), result.end(), [](const MusicTrack &left, const MusicTrack &right) {
        return lowerAscii(left.key()) < lowerAscii(right.key());
    });
    return result;
}

bool MusicPlaylist::isSupportedMusicFile(const std::filesystem::path &file)
{
    const std::string extension = lowerAscii(utf8String(file.extension()));
    return extension == ".ogg" || extension == ".mp3" || extension == ".wav" || extension == ".flac";
}
```

Команда и вывод проверки ссылки настройки:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 0a33444:src/game/Preferences.cpp | sed -n '93p'
```

```text
        settings.playMusic = section.getBoolean("playMusic");
```

Все три результата совпали с таблицей дорожки 1.

### Дорожка 2: пункты 2 и 4

Команда и вывод проверки папок апстрима:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 616280c8926ec642d86144a9fe2db105ceaf4061:src/context/MusicJukeBox.cpp | sed -n '37,52p'
```

```text
std::filesystem::path repertoryDir(eMusicType type, int house)
{
    switch (type) {
    case eMusicType::WIN: return "win";
    case eMusicType::LOSE: return "lose";
    case eMusicType::ATTACK: return "attack";
    case eMusicType::PEACE: return "peace";
    case eMusicType::MENU: return "menu";
    case eMusicType::CONQUEST: return "conquest";
    case eMusicType::BRIEFING:
        switch (house) {
        case ATREIDES: return "briefing/atreides";
        case HARKONNEN: return "briefing/harkonnen";
        case ORDOS: return "briefing/ordos";
        case SARDAUKAR: return "briefing/sardaukar";
        default: return "";
```

Команда и вывод проверки загрузки пользовательского аудио через SDL3_mixer:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp | sed -n '193,212p'
```

```text
bool cSoundPlayer::playMusicFile(const std::string &path)
{
    if (!m_isMusicEnabled || !m_musicTrack) {
        return true; // nothing to play, so nothing failed
    }
    SDL_IOStream *io = SDL_IOFromFile(path.c_str(), "rb");
    if (!io) {
        Logger::error(COMP_SOUND, "playMusicFile", "Could not open [{}]: {}", path, SDL_GetError());
        return false;
    }
    MIX_Audio *audio = MIX_LoadAudio_IO(m_mixer, io, false, true);
    if (!audio) {
        Logger::error(COMP_SOUND, "playMusicFile", "Could not load [{}]: {}", path, SDL_GetError());
        return false;
    }
    startMusic(audio);
    releaseMusicFile();
    m_musicFileAudio = audio;
    return true;
}
```

Команда и вывод проверки включения BRIEFING в апстримном gamestate:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show d06f2fcd2a347182c3774fb96e9a85570405c489:src/gamestates/cSelectYourNextConquestState.cpp | sed -n '464p'
```

```text
    m_audioContext->playMusicByType(eMusicType::BRIEFING, false, false, m_objects->getPlayer(HUMAN)->getHouse());
```

Все три результата совпали с таблицами дорожки 2.

### Дорожка 3: пункты 3 и 5

Команда и вывод проверки трёх CTest-регистраций:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt | sed -n '407p;418p;431p'
```

```text
    add_test(NAME music_playlist_shuffle_history COMMAND music_playlist_tests)
    add_test(NAME music_transition_policy COMMAND music_transition_policy_tests)
    add_test(NAME music_controls_layout_geometry COMMAND music_controls_layout_tests)
```

Команда и вывод проверки поля AudioContext в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cGame.h | sed -n '196p'
```

```text
    AudioContext* m_audioContext = nullptr;
```

Команда и вывод проверки внешних файлов в плейлист-тесте:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MusicPlaylistTests.cpp | sed -n '58,66p'
```

```text
    assert(discovered.size() == 4U);
    assert(discovered[0].externalPath.filename() == "alpha.mp3");
    assert(discovered[1].externalPath.filename() == "track.wav");
    assert(discovered[2].externalPath.filename() == "zeta.OGG");
    assert(std::any_of(discovered.begin(), discovered.end(), [&](const MusicTrack &track) {
        return track.externalPath.filename() == unicodeFile.filename();
    }));
    assert(MusicPlaylist::isSupportedMusicFile("theme.FLAC"));
    assert(!MusicPlaylist::isSupportedMusicFile("notes.txt"));
```

Все три результата совпали с таблицей дорожки 3. Выборка не заменяет построчные команды и полные таблицы вкладов.

# Пункты 1 и 6: механизм музыки FORK1 и настройки

Ревизия форка: `FORK1 = 9208dcf5a358f40afd95c99480e4e09f781ed566`. Все строки исходников форка ниже относятся к этой ревизии. Таблица полного перечня символов — `.tmp/p9r/fork-music.tsv`; её строки указывают объявления или определения всех функций, классов, структур, перечисления, значений перечисления, полей структур и именованных `constexpr` в шести заданных файлах.

## 1. Механизм музыки

### Категории и источники треков

| Категория | Объявление категории | Каталог пользовательской музыки и строка конфигурации | Встроенный fallback |
|---|---|---|---|
| Gameplay | `src/audio/MusicController.h@9208dcf:13` | `music/gameplay`, `src/cGame_logic.cpp@9208dcf:1121,1142-1146` | `MIDI_BUILDING01`–`MIDI_BUILDING09`, `src/cGame_logic.cpp@9208dcf:1145-1146` |
| Menu | `src/audio/MusicController.h@9208dcf:14` | `music/menu`, `src/cGame_logic.cpp@9208dcf:1122,1147` | `MIDI_MENU`, `src/cGame_logic.cpp@9208dcf:1147` |
| Conquest | `src/audio/MusicController.h@9208dcf:15` | `music/conquest`, `src/cGame_logic.cpp@9208dcf:1123,1148` | `MIDI_SCENARIO`, `src/cGame_logic.cpp@9208dcf:1148` |
| BriefingAtreides | `src/audio/MusicController.h@9208dcf:16` | `music/briefing/atreides`, `src/cGame_logic.cpp@9208dcf:1124,1149` | `MIDI_MENTAT_ATR`, `src/cGame_logic.cpp@9208dcf:1149` |
| BriefingHarkonnen | `src/audio/MusicController.h@9208dcf:17` | `music/briefing/harkonnen`, `src/cGame_logic.cpp@9208dcf:1125,1150` | `MIDI_MENTAT_HAR`, `src/cGame_logic.cpp@9208dcf:1150` |
| BriefingOrdos | `src/audio/MusicController.h@9208dcf:18` | `music/briefing/ordos`, `src/cGame_logic.cpp@9208dcf:1126,1151` | `MIDI_MENTAT_ORD`, `src/cGame_logic.cpp@9208dcf:1151` |
| Victory | `src/audio/MusicController.h@9208dcf:19` | `music/victory`, `src/cGame_logic.cpp@9208dcf:1127,1152` | `MIDI_WIN01`, `MIDI_WIN02`, `MIDI_WIN03`, `src/cGame_logic.cpp@9208dcf:1152` |
| Defeat | `src/audio/MusicController.h@9208dcf:20` | `music/defeat`, `src/cGame_logic.cpp@9208dcf:1128,1153` | `MIDI_LOSE01`, `MIDI_LOSE02`, `MIDI_LOSE03`, `src/cGame_logic.cpp@9208dcf:1153` |

Категории перечислены как `MusicCategory` в `src/audio/MusicController.h@9208dcf:12-22`; `Count` на строке 21 задаёт число ячеек массива, а не самостоятельный музыкальный пул. Каталог пользователя собирается из текущего каталога процесса и относительной папки: `src/cGame_logic.cpp@9208dcf:1116-1120`, `src/audio/MusicController.cpp@9208dcf:31-32`. Комментарий указывает, что текущий каталог переключён на каталог исполняемого файла и пользовательская музыка находится рядом с `d2tm.exe`: `src/cGame_logic.cpp@9208dcf:1116-1119`.

Каждая папка создаётся при инициализации: `src/cGame_logic.cpp@9208dcf:1120-1139`. Вызовы `configure` передают восемь путей и встроенные ID: `src/cGame_logic.cpp@9208dcf:1141-1153`. `MusicController::configure` ищет внешние файлы в переданной папке и выбирает найденные файлы либо встроенный список: `src/audio/MusicController.cpp@9208dcf:31-55`. Внешний список не задан в коде поимённо или в ini: `MusicPlaylist::discoverExternalTracks` обходит обычные файлы непосредственно в указанной папке, а не подпапки, принимает расширения `.ogg`, `.mp3`, `.wav`, `.flac` без учёта регистра и сортирует найденные треки по ключу: `src/audio/MusicPlaylist.cpp@9208dcf:122-148`. Следовательно, источник внешнего списка — содержимое каталога, фильтр — расширение файла; явной маски имени трека нет.

### Перемешивание и история

`MusicPlaylist` по умолчанию получает seed от `std::random_device`, а затем инициализирует `std::mt19937`: `src/audio/MusicPlaylist.h@9208dcf:21,43`, `src/audio/MusicPlaylist.cpp@9208dcf:36-38`. При установке списка сбрасываются мешок и история: `src/audio/MusicPlaylist.cpp@9208dcf:40-47`. Заполнение мешка создаёт перестановку всех индексов и перемешивает её; если следующий элемент оказался таким же, как последний сыгранный, и треков больше одного, крайние элементы меняются местами: `src/audio/MusicPlaylist.cpp@9208dcf:49-60`. `next` сначала воспроизводит вперёд уже существующую историю, а после её конца извлекает индекс из мешка и добавляет его в историю: `src/audio/MusicPlaylist.cpp@9208dcf:62-82`. `previous` двигает позицию назад, не опуская её ниже нуля: `src/audio/MusicPlaylist.cpp@9208dcf:84-93`. `discardCurrent` удаляет из списка все треки с тем же ключом и очищает историю и мешок: `src/audio/MusicPlaylist.cpp@9208dcf:104-120`. Ключ внешнего трека — лексически нормализованный путь, ключ встроенного — ID: `src/audio/MusicPlaylist.cpp@9208dcf:23-26`.

### Выбор и смена категории

`musicCategoryFor` отображает `MUSIC_PEACE` и `MUSIC_ATTACK` в Gameplay, `MUSIC_MENU` в Menu, `MUSIC_CONQUEST` в Conquest, `MUSIC_WIN` в Victory, `MUSIC_LOSE` в Defeat; `MUSIC_BRIEFING` выбирает пул по дому человека, а неизвестный тип — Menu: `src/cGame_logic.cpp@9208dcf:96-116`. До выбора категории `MUSIC_ATTACK` заменяется на `MUSIC_PEACE`, после чего вычисляется признак повторной категории сравнением с прошлым `m_musicType`: `src/cGame_logic.cpp@9208dcf:2229-2236`. Вызов контроллера и политика повторного входа находятся на `src/cGame_logic.cpp@9208dcf:2242-2251`.

`shouldAdvanceRepeatedMusicCategory` игнорирует параметр `playingState` и возвращает `!repeatedCategory`: `src/audio/MusicTransitionPolicy.hpp@9208dcf:3-8`. `activate` устанавливает категорию и запускает следующий трек, когда категория новая, параметр продвижения истинен или проигрыватель в этот момент не играет: `src/audio/MusicController.cpp@9208dcf:67-75`. Поэтому повторная категория обычно сохраняет текущий трек, но после остановки запускает следующий. `update` запускает следующий трек при завершении текущего: `src/audio/MusicController.cpp@9208dcf:77-82`. В `cGame` пользовательские кнопки предыдущего и следующего трека вызывают методы контроллера только при включённой музыке и состоянии игры: `src/cGame_logic.cpp@9208dcf:2256-2267`; клавиши `[` и `]` вызывают эти же действия: `src/cGame_logic.cpp@9208dcf:2105-2110`. Переключение музыки клавишами `M`/Mute останавливает её или повторно запускает текущий трек: `src/cGame_logic.cpp@9208dcf:2092-2102`.

### Назначение символов в шести файлах

Точный перечень API, вспомогательных функций, полей структур, enum values и констант с входами и выходами содержится в `.tmp/p9r/fork-music.tsv`. Функции и данные контроллера объявлены в `src/audio/MusicController.h@9208dcf:10-63`, их реализации находятся в `src/audio/MusicController.cpp@9208dcf:8-186`. `MusicTrack` и `MusicPlaylist` объявлены в `src/audio/MusicPlaylist.h@9208dcf:10-44`, реализации находятся в `src/audio/MusicPlaylist.cpp@9208dcf:7-148`. Политика повтора объявлена и реализована в `src/audio/MusicTransitionPolicy.hpp@9208dcf:3-8`. `MusicControlsLayout` и его функции находятся в `src/sidebar/MusicControlsLayout.hpp@9208dcf:7-65`; `create` возвращает пустую разметку при доступной ширине меньше 200, ограничивает ширину значением 520 и вычисляет прямоугольники панели музыки и скорости; `showsLabel` показывает подпись при ширине не меньше 80.

Команда, которой прочитаны полные пронумерованные исходники, и её вывод приведены ниже. Она показывает реализацию каждого перечисленного символа; таблица выше и `fork-music.tsv` фиксируют входы, выходы и поведение.

## 6. Настройки музыки

Строки отбора: `.tmp/p8r/fork-settings.tsv` — строки 16–17 (`playMusic`, `playSound`); `.tmp/p8r/preferences.tsv` — строки 16–19 и 42–45 (`playMusic`, `customMusic`, `playSound`, `playCreditsSound` для ревизий `0a33444` и `d06f2fc`). Таблица проверок — `.tmp/p9r/settings.tsv`: в ней 34 ссылки на исходные строки, все 34 имеют результат `совпало`.

Для каждой ссылки проверка повторяла форму `git show <ревизия>:<путь> | sed -n '<строка>p'`. Все фактические команды и их выводы приведены ниже. Сверялась каждая ссылка `путь@ревизия:строка` из отобранной строки, включая декларацию поля, чтение и запись настройки, а также строку ini, если она указана.

Прямой поиск `customMusic` в коде FORK1 и `resources/bin/settings.ini` не нашёл совпадений; отдельный вывод поиска пустой. Поэтому строки `customMusic` из `preferences.tsv` относятся к указанным в самой таблице ревизиям `0a33444` и `d06f2fc`, а не к `FORK1`.

## Команды и выводы

### Пронумерованные исходники FORK1

#### `src/audio/MusicController.h`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.h | nl -ba`

Вывод:

```text
     1	#pragma once
     2	
     3	#include "audio/MusicPlaylist.h"
     4	
     5	#include <array>
     6	#include <filesystem>
     7	#include <string>
     8	#include <vector>
     9	
    10	class cSoundPlayer;
    11	
    12	enum class MusicCategory : std::size_t {
    13	    Gameplay,
    14	    Menu,
    15	    Conquest,
    16	    BriefingAtreides,
    17	    BriefingHarkonnen,
    18	    BriefingOrdos,
    19	    Victory,
    20	    Defeat,
    21	    Count
    22	};
    23	
    24	class MusicController {
    25	    friend class UiAuditAccess;
    26	
    27	public:
    28	    MusicController(cSoundPlayer *soundPlayer, const std::filesystem::path &gameDirectory);
    29	
    30	    void configure(
    31	        MusicCategory category,
    32	        const std::filesystem::path &relativeDirectory,
    33	        std::vector<int> fallbackIds);
    34	    void activate(MusicCategory category, bool advanceOnRepeatedEntry = true);
    35	    void update();
    36	    void next();
    37	    void previous();
    38	    void replayCurrent();
    39	    void stop();
    40	
    41	    [[nodiscard]] std::string currentDisplayName() const;
    42	    [[nodiscard]] bool hasActiveCategory() const { return m_hasActiveCategory; }
    43	
    44	private:
    45	    struct CategoryState {
    46	        MusicPlaylist playlist;
    47	        std::vector<MusicTrack> fallback;
    48	        bool usingCustom = false;
    49	        std::filesystem::path directory;
    50	    };
    51	
    52	    bool play(const MusicTrack *track);
    53	    void playNextAvailable(bool backwards);
    54	    void switchToFallback(CategoryState &state);
    55	    CategoryState &activeState();
    56	    const CategoryState &activeState() const;
    57	
    58	    cSoundPlayer *m_soundPlayer;
    59	    std::filesystem::path m_gameDirectory;
    60	    std::array<CategoryState, static_cast<std::size_t>(MusicCategory::Count)> m_categories;
    61	    MusicCategory m_activeCategory = MusicCategory::Menu;
    62	    bool m_hasActiveCategory = false;
    63	};
```

#### `src/audio/MusicController.cpp`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicController.cpp | nl -ba`

Вывод:

```text
     1	#include "audio/MusicController.h"
     2	
     3	#include "utils/cLog.h"
     4	#include "utils/cSoundPlayer.h"
     5	
     6	#include <format>
     7	
     8	namespace {
     9	std::size_t indexOf(MusicCategory category)
    10	{
    11	    return static_cast<std::size_t>(category);
    12	}
    13	
    14	std::string utf8String(const std::filesystem::path &path)
    15	{
    16	    const auto value = path.u8string();
    17	    return std::string(value.begin(), value.end());
    18	}
    19	}
    20	
    21	MusicController::MusicController(cSoundPlayer *soundPlayer, const std::filesystem::path &gameDirectory)
    22	    : m_soundPlayer(soundPlayer), m_gameDirectory(gameDirectory.empty() ? std::filesystem::current_path() : gameDirectory)
    23	{
    24	}
    25	
    26	void MusicController::configure(
    27	    MusicCategory category,
    28	    const std::filesystem::path &relativeDirectory,
    29	    std::vector<int> fallbackIds)
    30	{
    31	    CategoryState &state = m_categories[indexOf(category)];
    32	    state.directory = m_gameDirectory / relativeDirectory;
    33	    state.fallback.clear();
    34	    for (const int id : fallbackIds) {
    35	        state.fallback.push_back(MusicTrack{id, {}});
    36	    }
    37	
    38	    std::error_code directoryError;
    39	    if (std::filesystem::is_directory(state.directory, directoryError)) {
    40	        for (const auto &entry : std::filesystem::directory_iterator(state.directory, directoryError)) {
    41	            std::error_code fileError;
    42	            if (!directoryError && entry.is_regular_file(fileError) && !fileError &&
    43	                !MusicPlaylist::isSupportedMusicFile(entry.path())) {
    44	                cLogger::getInstance()->log(
    45	                    LOG_WARN,
    46	                    COMP_SOUND,
    47	                    "Custom music skipped",
    48	                    std::format("{}: unsupported file type", utf8String(entry.path())));
    49	            }
    50	        }
    51	    }
    52	
    53	    const std::vector<MusicTrack> customTracks = MusicPlaylist::discoverExternalTracks(state.directory);
    54	    state.usingCustom = !customTracks.empty();
    55	    state.playlist.setTracks(state.usingCustom ? customTracks : state.fallback);
    56	    cLogger::getInstance()->log(
    57	        LOG_INFO,
    58	        COMP_SOUND,
    59	        "Music pool",
    60	        std::format(
    61	            "{}: {} custom track(s){}",
    62	            utf8String(state.directory),
    63	            customTracks.size(),
    64	            state.usingCustom ? "" : "; using built-in fallback"));
    65	}
    66	
    67	void MusicController::activate(MusicCategory category, bool advanceOnRepeatedEntry)
    68	{
    69	    const bool repeated = m_hasActiveCategory && m_activeCategory == category;
    70	    m_activeCategory = category;
    71	    m_hasActiveCategory = true;
    72	    if (!repeated || advanceOnRepeatedEntry || !m_soundPlayer->isMusicPlaying()) {
    73	        playNextAvailable(false);
    74	    }
    75	}
    76	
    77	void MusicController::update()
    78	{
    79	    if (m_hasActiveCategory && !m_soundPlayer->isMusicPlaying()) {
    80	        playNextAvailable(false);
    81	    }
    82	}
    83	
    84	void MusicController::next()
    85	{
    86	    if (m_hasActiveCategory) {
    87	        playNextAvailable(false);
    88	    }
    89	}
    90	
    91	void MusicController::previous()
    92	{
    93	    if (m_hasActiveCategory) {
    94	        playNextAvailable(true);
    95	    }
    96	}
    97	
    98	void MusicController::replayCurrent()
    99	{
   100	    if (!m_hasActiveCategory) {
   101	        return;
   102	    }
   103	    const MusicTrack *track = activeState().playlist.current();
   104	    if (!track || !play(track)) {
   105	        playNextAvailable(false);
   106	    }
   107	}
   108	
   109	void MusicController::stop()
   110	{
   111	    m_soundPlayer->stopMusic();
   112	}
   113	
   114	std::string MusicController::currentDisplayName() const
   115	{
   116	    if (!m_hasActiveCategory) {
   117	        return {};
   118	    }
   119	    const MusicTrack *track = activeState().playlist.current();
   120	    return track ? track->displayName() : std::string{};
   121	}
   122	
   123	bool MusicController::play(const MusicTrack *track)
   124	{
   125	    if (!track) {
   126	        return false;
   127	    }
   128	    if (!track->isExternal()) {
   129	        m_soundPlayer->playMusic(track->builtInId);
   130	        return true;
   131	    }
   132	
   133	    std::string error;
   134	    if (m_soundPlayer->playMusicFile(track->externalPath, error)) {
   135	        return true;
   136	    }
   137	    cLogger::getInstance()->log(
   138	        LOG_WARN,
   139	        COMP_SOUND,
   140	        "Custom music skipped",
   141	        std::format("{}: {}", utf8String(track->externalPath), error));
   142	    return false;
   143	}
   144	
   145	void MusicController::playNextAvailable(bool backwards)
   146	{
   147	    CategoryState &state = activeState();
   148	    std::size_t remainingAttempts = state.playlist.size();
   149	    while (remainingAttempts-- > 0U) {
   150	        const MusicTrack *track = backwards ? state.playlist.previous() : state.playlist.next();
   151	        if (play(track)) {
   152	            return;
   153	        }
   154	        state.playlist.discardCurrent();
   155	        backwards = false;
   156	    }
   157	
   158	    if (state.usingCustom) {
   159	        cLogger::getInstance()->log(
   160	            LOG_WARN,
   161	            COMP_SOUND,
   162	            "Music pool fallback",
   163	            std::format("No playable custom music in {}; using built-in music", utf8String(state.directory)));
   164	        switchToFallback(state);
   165	        if (play(state.playlist.next())) {
   166	            return;
   167	        }
   168	    }
   169	    m_soundPlayer->stopMusic();
   170	}
   171	
   172	void MusicController::switchToFallback(CategoryState &state)
   173	{
   174	    state.usingCustom = false;
   175	    state.playlist.setTracks(state.fallback);
   176	}
   177	
   178	MusicController::CategoryState &MusicController::activeState()
   179	{
   180	    return m_categories[indexOf(m_activeCategory)];
   181	}
   182	
   183	const MusicController::CategoryState &MusicController::activeState() const
   184	{
   185	    return m_categories[indexOf(m_activeCategory)];
   186	}
```

#### `src/audio/MusicPlaylist.h`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicPlaylist.h | nl -ba`

Вывод:

```text
     1	#pragma once
     2	
     3	#include <cstdint>
     4	#include <filesystem>
     5	#include <optional>
     6	#include <random>
     7	#include <string>
     8	#include <vector>
     9	
    10	struct MusicTrack {
    11	    int builtInId = -1;
    12	    std::filesystem::path externalPath;
    13	
    14	    [[nodiscard]] bool isExternal() const { return !externalPath.empty(); }
    15	    [[nodiscard]] std::string key() const;
    16	    [[nodiscard]] std::string displayName() const;
    17	};
    18	
    19	class MusicPlaylist {
    20	public:
    21	    explicit MusicPlaylist(std::uint32_t seed = std::random_device{}());
    22	
    23	    void setTracks(std::vector<MusicTrack> tracks);
    24	    [[nodiscard]] bool empty() const { return m_tracks.empty(); }
    25	    [[nodiscard]] std::size_t size() const { return m_tracks.size(); }
    26	
    27	    const MusicTrack *next();
    28	    const MusicTrack *previous();
    29	    const MusicTrack *current() const;
    30	    void discardCurrent();
    31	
    32	    static bool isSupportedMusicFile(const std::filesystem::path &file);
    33	    static std::vector<MusicTrack> discoverExternalTracks(const std::filesystem::path &directory);
    34	
    35	private:
    36	    void refillBag();
    37	
    38	    std::vector<MusicTrack> m_tracks;
    39	    std::vector<std::size_t> m_bag;
    40	    std::vector<std::size_t> m_history;
    41	    std::size_t m_historyPosition = 0;
    42	    bool m_hasHistoryPosition = false;
    43	    std::mt19937 m_rng;
    44	};
```

#### `src/audio/MusicPlaylist.cpp`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicPlaylist.cpp | nl -ba`

Вывод:

```text
     1	#include "audio/MusicPlaylist.h"
     2	
     3	#include <algorithm>
     4	#include <cctype>
     5	#include <numeric>
     6	
     7	namespace {
     8	std::string utf8String(const std::filesystem::path &path)
     9	{
    10	    const auto value = path.u8string();
    11	    return std::string(value.begin(), value.end());
    12	}
    13	
    14	std::string lowerAscii(std::string value)
    15	{
    16	    std::transform(value.begin(), value.end(), value.begin(), [](unsigned char ch) {
    17	        return static_cast<char>(std::tolower(ch));
    18	    });
    19	    return value;
    20	}
    21	}
    22	
    23	std::string MusicTrack::key() const
    24	{
    25	    return isExternal() ? utf8String(externalPath.lexically_normal()) : std::to_string(builtInId);
    26	}
    27	
    28	std::string MusicTrack::displayName() const
    29	{
    30	    if (isExternal()) {
    31	        return utf8String(externalPath.stem());
    32	    }
    33	    return "Dune II #" + std::to_string(builtInId + 1);
    34	}
    35	
    36	MusicPlaylist::MusicPlaylist(std::uint32_t seed) : m_rng(seed)
    37	{
    38	}
    39	
    40	void MusicPlaylist::setTracks(std::vector<MusicTrack> tracks)
    41	{
    42	    m_tracks = std::move(tracks);
    43	    m_bag.clear();
    44	    m_history.clear();
    45	    m_historyPosition = 0;
    46	    m_hasHistoryPosition = false;
    47	}
    48	
    49	void MusicPlaylist::refillBag()
    50	{
    51	    m_bag.resize(m_tracks.size());
    52	    std::iota(m_bag.begin(), m_bag.end(), 0U);
    53	    std::shuffle(m_bag.begin(), m_bag.end(), m_rng);
    54	
    55	    const MusicTrack *last = current();
    56	    if (last && m_bag.size() > 1U && m_bag.back() < m_tracks.size() &&
    57	        m_tracks[m_bag.back()].key() == last->key()) {
    58	        std::swap(m_bag.front(), m_bag.back());
    59	    }
    60	}
    61	
    62	const MusicTrack *MusicPlaylist::next()
    63	{
    64	    if (m_tracks.empty()) {
    65	        return nullptr;
    66	    }
    67	
    68	    if (m_hasHistoryPosition && m_historyPosition + 1U < m_history.size()) {
    69	        ++m_historyPosition;
    70	        return current();
    71	    }
    72	
    73	    if (m_bag.empty()) {
    74	        refillBag();
    75	    }
    76	    const std::size_t index = m_bag.back();
    77	    m_bag.pop_back();
    78	    m_history.push_back(index);
    79	    m_historyPosition = m_history.size() - 1U;
    80	    m_hasHistoryPosition = true;
    81	    return current();
    82	}
    83	
    84	const MusicTrack *MusicPlaylist::previous()
    85	{
    86	    if (!m_hasHistoryPosition || m_history.empty()) {
    87	        return nullptr;
    88	    }
    89	    if (m_historyPosition > 0U) {
    90	        --m_historyPosition;
    91	    }
    92	    return current();
    93	}
    94	
    95	const MusicTrack *MusicPlaylist::current() const
    96	{
    97	    if (!m_hasHistoryPosition || m_historyPosition >= m_history.size()) {
    98	        return nullptr;
    99	    }
   100	    const std::size_t index = m_history[m_historyPosition];
   101	    return index < m_tracks.size() ? &m_tracks[index] : nullptr;
   102	}
   103	
   104	void MusicPlaylist::discardCurrent()
   105	{
   106	    const MusicTrack *badTrack = current();
   107	    if (!badTrack) {
   108	        return;
   109	    }
   110	    const std::string badKey = badTrack->key();
   111	    m_tracks.erase(
   112	        std::remove_if(m_tracks.begin(), m_tracks.end(), [&](const MusicTrack &track) {
   113	            return track.key() == badKey;
   114	        }),
   115	        m_tracks.end());
   116	    m_bag.clear();
   117	    m_history.clear();
   118	    m_historyPosition = 0;
   119	    m_hasHistoryPosition = false;
   120	}
   121	
   122	std::vector<MusicTrack> MusicPlaylist::discoverExternalTracks(const std::filesystem::path &directory)
   123	{
   124	    std::vector<MusicTrack> result;
   125	    std::error_code error;
   126	    if (!std::filesystem::is_directory(directory, error)) {
   127	        return result;
   128	    }
   129	
   130	    for (const auto &entry : std::filesystem::directory_iterator(directory, error)) {
   131	        if (error || !entry.is_regular_file(error)) {
   132	            continue;
   133	        }
   134	        if (isSupportedMusicFile(entry.path())) {
   135	            result.push_back(MusicTrack{-1, entry.path()});
   136	        }
   137	    }
   138	    std::sort(result.begin(), result.end(), [](const MusicTrack &left, const MusicTrack &right) {
   139	        return lowerAscii(left.key()) < lowerAscii(right.key());
   140	    });
   141	    return result;
   142	}
   143	
   144	bool MusicPlaylist::isSupportedMusicFile(const std::filesystem::path &file)
   145	{
   146	    const std::string extension = lowerAscii(utf8String(file.extension()));
   147	    return extension == ".ogg" || extension == ".mp3" || extension == ".wav" || extension == ".flac";
   148	}
```

#### `src/audio/MusicTransitionPolicy.hpp`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/audio/MusicTransitionPolicy.hpp | nl -ba`

Вывод:

```text
     1	#pragma once
     2	
     3	[[nodiscard]] constexpr bool shouldAdvanceRepeatedMusicCategory(
     4	    bool repeatedCategory,
     5	    bool /*playingState*/)
     6	{
     7	    return !repeatedCategory;
     8	}
```

#### `src/sidebar/MusicControlsLayout.hpp`

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/sidebar/MusicControlsLayout.hpp | nl -ba`

Вывод:

```text
     1	#pragma once
     2	
     3	#include "utils/cRectangle.h"
     4	
     5	#include <algorithm>
     6	
     7	struct MusicControlsLayout {
     8	    bool visible = false;
     9	    cRectangle panel;
    10	    cRectangle musicPanel;
    11	    cRectangle previous;
    12	    cRectangle label;
    13	    cRectangle next;
    14	    cRectangle speedPanel;
    15	    cRectangle speedLabel;
    16	    cRectangle speedSlider;
    17	
    18	    [[nodiscard]] static MusicControlsLayout create(
    19	        int left,
    20	        int right,
    21	        int reservedMessageWidth = 0)
    22	    {
    23	        constexpr int MinimumWidth = 200;
    24	        constexpr int MaximumWidth = 520;
    25	        const int availableWidth = std::max(0, right - left);
    26	        const int controlsWidth = reservedMessageWidth > 0
    27	            ? availableWidth - reservedMessageWidth - 8
    28	            : availableWidth;
    29	        if (controlsWidth < MinimumWidth) {
    30	            return {};
    31	        }
    32	
    33	        const int width = std::min(controlsWidth, MaximumWidth);
    34	        constexpr int buttonSize = 33;
    35	        constexpr int y = 4;
    36	        const int gap = 5;
    37	        constexpr int sectionGap = 8;
    38	        const int contentWidth = width - sectionGap;
    39	        const int musicWidth = contentWidth / 2;
    40	        const int speedWidth = contentWidth - musicWidth;
    41	        const int labelX = left + buttonSize + gap;
    42	        const int labelWidth = std::max(0, musicWidth - buttonSize * 2 - gap * 2);
    43	        const int speedX = left + musicWidth + sectionGap;
    44	        const int speedLabelWidth = std::min(76, speedWidth / 2);
    45	        const int speedSliderX = speedX + speedLabelWidth + gap;
    46	        const int speedSliderWidth = std::max(0, speedWidth - speedLabelWidth - gap);
    47	
    48	        MusicControlsLayout result;
    49	        result.visible = true;
    50	        result.panel = cRectangle(left, y, width, buttonSize);
    51	        result.musicPanel = cRectangle(left, y, musicWidth, buttonSize);
    52	        result.previous = cRectangle(left, y, buttonSize, buttonSize);
    53	        result.label = cRectangle(labelX, y, labelWidth, buttonSize);
    54	        result.next = cRectangle(left + musicWidth - buttonSize, y, buttonSize, buttonSize);
    55	        result.speedPanel = cRectangle(speedX, y, speedWidth, buttonSize);
    56	        result.speedLabel = cRectangle(speedX, y, speedLabelWidth, buttonSize);
    57	        result.speedSlider = cRectangle(speedSliderX, y, speedSliderWidth, buttonSize);
    58	        return result;
    59	    }
    60	
    61	    [[nodiscard]] bool showsLabel() const
    62	    {
    63	        return label.getWidth() >= 80;
    64	    }
    65	};
```

#### `src/cGame_logic.cpp` — отображение категорий

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '91,117p'`

Вывод:

```text
    91	namespace {
    92	
    93	constexpr auto kMinAlpha = 0;
    94	constexpr auto kMaxAlpha = 255;
    95	
    96	MusicCategory musicCategoryFor(int musicType, int house)
    97	{
    98	    switch (musicType) {
    99	        case MUSIC_PEACE:
   100	        case MUSIC_ATTACK:
   101	            return MusicCategory::Gameplay;
   102	        case MUSIC_MENU:
   103	            return MusicCategory::Menu;
   104	        case MUSIC_CONQUEST:
   105	            return MusicCategory::Conquest;
   106	        case MUSIC_WIN:
   107	            return MusicCategory::Victory;
   108	        case MUSIC_LOSE:
   109	            return MusicCategory::Defeat;
   110	        case MUSIC_BRIEFING:
   111	            if (house == HARKONNEN) return MusicCategory::BriefingHarkonnen;
   112	            if (house == ORDOS) return MusicCategory::BriefingOrdos;
   113	            return MusicCategory::BriefingAtreides;
   114	        default:
   115	            return MusicCategory::Menu;
   116	    }
   117	}
```

#### `src/cGame_logic.cpp` — создание папок и настройка пулов

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '1116,1154p'`

Вывод:

```text
  1116	    // main() switches the working directory to the executable directory before
  1117	    // settings are loaded. GameDir points at the data pack directory, while
  1118	    // user-owned music lives next to d2tm.exe.
  1119	    const std::filesystem::path resolvedGameDirectory = std::filesystem::current_path();
  1120	    const std::array<std::filesystem::path, 8> musicDirectories{
  1121	        "music/gameplay",
  1122	        "music/menu",
  1123	        "music/conquest",
  1124	        "music/briefing/atreides",
  1125	        "music/briefing/harkonnen",
  1126	        "music/briefing/ordos",
  1127	        "music/victory",
  1128	        "music/defeat"
  1129	    };
  1130	    for (const auto &directory : musicDirectories) {
  1131	        std::error_code createError;
  1132	        std::filesystem::create_directories(resolvedGameDirectory / directory, createError);
  1133	        if (createError) {
  1134	            logger->log(
  1135	                LOG_WARN,
  1136	                COMP_SOUND,
  1137	                "Music directory",
  1138	                std::format("Could not create {}: {}", (resolvedGameDirectory / directory).string(), createError.message()));
  1139	        }
  1140	    }
  1141	    m_musicController = std::make_unique<MusicController>(m_soundPlayer, resolvedGameDirectory);
  1142	    m_musicController->configure(
  1143	        MusicCategory::Gameplay,
  1144	        "music/gameplay",
  1145	        {MIDI_BUILDING01, MIDI_BUILDING02, MIDI_BUILDING03, MIDI_BUILDING04, MIDI_BUILDING05,
  1146	         MIDI_BUILDING06, MIDI_BUILDING07, MIDI_BUILDING08, MIDI_BUILDING09});
  1147	    m_musicController->configure(MusicCategory::Menu, "music/menu", {MIDI_MENU});
  1148	    m_musicController->configure(MusicCategory::Conquest, "music/conquest", {MIDI_SCENARIO});
  1149	    m_musicController->configure(MusicCategory::BriefingAtreides, "music/briefing/atreides", {MIDI_MENTAT_ATR});
  1150	    m_musicController->configure(MusicCategory::BriefingHarkonnen, "music/briefing/harkonnen", {MIDI_MENTAT_HAR});
  1151	    m_musicController->configure(MusicCategory::BriefingOrdos, "music/briefing/ordos", {MIDI_MENTAT_ORD});
  1152	    m_musicController->configure(MusicCategory::Victory, "music/victory", {MIDI_WIN01, MIDI_WIN02, MIDI_WIN03});
  1153	    m_musicController->configure(MusicCategory::Defeat, "music/defeat", {MIDI_LOSE01, MIDI_LOSE02, MIDI_LOSE03});
  1154	
```

#### `src/cGame_logic.cpp` — изменение типа музыки и переходы

Команда: `git show 9208dcf5a358f40afd95c99480e4e09f781ed566:src/cGame_logic.cpp | nl -ba | sed -n '2092,2111p;2215,2273p'`

Вывод:

```text
  2092	    if (event.hasKey(SDL_SCANCODE_M) || event.hasKey(SDL_SCANCODE_MUTE)) {
  2093	        game.m_playMusic = !game.m_playMusic;
  2094	        m_soundPlayer->setMusicEnabled(game.m_playMusic);
  2095	        if (!game.m_playMusic) {
  2096	            if (m_musicController) m_musicController->stop();
  2097	            humanPlayer.addNotification(localization::text("Music off", "Музыка выключена"), eNotificationType::NEUTRAL);
  2098	        }
  2099	        else {
  2100	            if (m_musicController) m_musicController->replayCurrent();
  2101	            humanPlayer.addNotification(localization::text("Music on", "Музыка включена"), eNotificationType::NEUTRAL);
  2102	        }
  2103	    }
  2104	
  2105	    if (event.hasKey(SDL_SCANCODE_LEFTBRACKET)) {
  2106	        playPreviousGameplayTrack();
  2107	    }
  2108	
  2109	    if (event.hasKey(SDL_SCANCODE_RIGHTBRACKET)) {
  2110	        playNextGameplayTrack();
  2111	    }
  2215	void cGame::playMusicByTypeForStateTransition(int iType)
  2216	{
  2217	    playMusicByType(iType, HUMAN, false);
  2218	}
  2219	
  2220	bool cGame::playMusicByType(int iType, int playerId, bool triggerWithVoice)
  2221	{
  2222	    if (playerId != HUMAN) {
  2223	        // skip music we want to play for non human player
  2224	        return false;
  2225	    }
  2226	
  2227	    logbook(std::format("cGame::playMusicByType - iType = {}. playerId = {}, triggerWithVoice = {}", iType, playerId, triggerWithVoice));
  2228	
  2229	    // Attack detection no longer owns the music state. Legacy callers are folded
  2230	    // into the gameplay pool and cannot interrupt the current composition.
  2231	    if (iType == MUSIC_ATTACK) {
  2232	        iType = MUSIC_PEACE;
  2233	    }
  2234	    const bool repeatedCategory = m_musicType == iType;
  2235	    m_musicType = iType;
  2236	    logbook(std::format("m_musicType = {}", m_musicType));
  2237	
  2238	    if (!m_playMusic) {
  2239	        return false; // todo: have a 'no-sound soundplayer' instead of doing this :/
  2240	    }
  2241	
  2242	    if (m_musicController) {
  2243	        const MusicCategory category = musicCategoryFor(iType, players[HUMAN].getHouse());
  2244	        // Keep the current track when adjacent screens use the same category.
  2245	        m_musicController->activate(
  2246	            category,
  2247	            shouldAdvanceRepeatedMusicCategory(
  2248	                repeatedCategory,
  2249	                isState(GAME_PLAYING)
  2250	            )
  2251	        );
  2252	    }
  2253	    return true;
  2254	}
  2255	
  2256	void cGame::playPreviousGameplayTrack()
  2257	{
  2258	    if (m_playMusic && isState(GAME_PLAYING) && m_musicController) {
  2259	        m_musicController->previous();
  2260	    }
  2261	}
  2262	
  2263	void cGame::playNextGameplayTrack()
  2264	{
  2265	    if (m_playMusic && isState(GAME_PLAYING) && m_musicController) {
  2266	        m_musicController->next();
  2267	    }
  2268	}
  2269	
  2270	std::string cGame::getCurrentMusicTrackName() const
  2271	{
  2272	    return m_musicController ? m_musicController->currentDisplayName() : std::string{};
  2273	}
```

### Отбор строк таблиц P8

Команда и код фильтрации:

```sh
python3 - <<'PY'
import pathlib, re
pats = re.compile(r'music|Music|volume|Volume|sound|Sound')
for name in ('fork-settings.tsv', 'preferences.tsv'):
    p = pathlib.Path('.tmp/p8r') / name
    print(f'--- {p} ---')
    for n, line in enumerate(p.read_text().splitlines(), 1):
        if pats.search(line):
            print(f'{n}:{line}')
PY
```

Вывод:

```text
--- .tmp/p8r/fork-settings.tsv ---
16:resources/bin/settings.ini	SETTINGS	playMusic	bool	true (src/utils/GameSettings.hpp@9208dcf:18)	src/utils/common.cpp@9208dcf:89	src/utils/common.cpp@9208dcf:370	воспроизведение музыки	есть (src/game/Preferences.cpp@0a33444:93)	только комментарий, не активен (resources/bin/settings.ini@0a33444:64)
17:resources/bin/settings.ini	SETTINGS	playSound	bool	true (src/utils/GameSettings.hpp@9208dcf:19)	src/utils/common.cpp@9208dcf:91	src/utils/common.cpp@9208dcf:371	воспроизведение звуков	есть (src/game/Preferences.cpp@0a33444:99)	только комментарий, не активен (resources/bin/settings.ini@0a33444:73)
--- .tmp/p8r/preferences.tsv ---
16:0a33444	SETTINGS	playMusic	bool	true (src/utils/InitialGameSettings.hpp@0a33444:32)	src/game/Preferences.cpp@0a33444:93	src/game/Preferences.cpp@0a33444:171	воспроизведение музыки
17:0a33444	SETTINGS	customMusic	bool	false (src/utils/InitialGameSettings.hpp@0a33444:33)	src/game/Preferences.cpp@0a33444:96	src/game/Preferences.cpp@0a33444:172	воспроизведение музыки из каталогов audio
18:0a33444	SETTINGS	playSound	bool	true (src/utils/InitialGameSettings.hpp@0a33444:34)	src/game/Preferences.cpp@0a33444:99	src/game/Preferences.cpp@0a33444:173	воспроизведение звуков
19:0a33444	SETTINGS	playCreditsSound	bool	true (src/utils/InitialGameSettings.hpp@0a33444:35)	src/game/Preferences.cpp@0a33444:102	src/game/Preferences.cpp@0a33444:174	звук подсчёта получаемых и расходуемых ресурсов
42:d06f2fc	SETTINGS	playMusic	bool	true (src/utils/InitialGameSettings.hpp@d06f2fc:33)	src/game/Preferences.cpp@d06f2fc:92	src/game/Preferences.cpp@d06f2fc:170	воспроизведение музыки
43:d06f2fc	SETTINGS	customMusic	bool	false (src/utils/InitialGameSettings.hpp@d06f2fc:34)	src/game/Preferences.cpp@d06f2fc:95	src/game/Preferences.cpp@d06f2fc:171	воспроизведение музыки из каталогов audio
44:d06f2fc	SETTINGS	playSound	bool	true (src/utils/InitialGameSettings.hpp@d06f2fc:35)	src/game/Preferences.cpp@d06f2fc:98	src/game/Preferences.cpp@d06f2fc:172	воспроизведение звуков
45:d06f2fc	SETTINGS	playCreditsSound	bool	true (src/utils/InitialGameSettings.hpp@d06f2fc:36)	src/game/Preferences.cpp@d06f2fc:101	src/game/Preferences.cpp@d06f2fc:173	звук подсчёта получаемых и расходуемых ресурсов
```

### Проверка каждой ссылки на исходную строку

Команда и код проверки:

```sh
python3 - <<'PY'
import pathlib, re, subprocess
pat = re.compile(r'(?P<path>[\w./-]+)@(?P<rev>[0-9a-f]+):(?P<line>\d+)')
for name in ('fork-settings.tsv', 'preferences.tsv'):
    p = pathlib.Path('.tmp/p8r') / name
    for row, line in enumerate(p.read_text().splitlines(), 1):
        if not re.search(r'music|Music|volume|Volume|sound|Sound', line):
            continue
        for m in pat.finditer(line):
            path, rev, n = m.group('path', 'rev', 'line')
            cmd = f"git show {rev}:{path} | sed -n '{n}p'"
            proc = subprocess.run(['bash', '-o', 'pipefail', '-c', f'export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH; {cmd}'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = proc.stdout.rstrip('\n')
            result = 'совпало' if proc.returncode == 0 and out else 'не совпало'
            print(f'{name}\tстрока {row}\t{m.group(0)}\t{result}')
            print(f'$ {cmd}')
            print(out if out else f'[пустой вывод; exit {proc.returncode}]')
PY
```

Вывод:

```text
fork-settings.tsv	строка 16	src/utils/GameSettings.hpp@9208dcf:18	совпало
$ git show 9208dcf:src/utils/GameSettings.hpp | sed -n '18p'
    bool playMusic = true;
fork-settings.tsv	строка 16	src/utils/common.cpp@9208dcf:89	совпало
$ git show 9208dcf:src/utils/common.cpp | sed -n '89p'
        gameSettings->playMusic = section.getBoolean("playMusic");
fork-settings.tsv	строка 16	src/utils/common.cpp@9208dcf:370	совпало
$ git show 9208dcf:src/utils/common.cpp | sed -n '370p'
        {"playMusic", boolToIni(settings.playMusic)},
fork-settings.tsv	строка 16	src/game/Preferences.cpp@0a33444:93	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '93p'
        settings.playMusic = section.getBoolean("playMusic");
fork-settings.tsv	строка 16	resources/bin/settings.ini@0a33444:64	совпало
$ git show 0a33444:resources/bin/settings.ini | sed -n '64p'
#playMusic = false
fork-settings.tsv	строка 17	src/utils/GameSettings.hpp@9208dcf:19	совпало
$ git show 9208dcf:src/utils/GameSettings.hpp | sed -n '19p'
    bool playSound = true;
fork-settings.tsv	строка 17	src/utils/common.cpp@9208dcf:91	совпало
$ git show 9208dcf:src/utils/common.cpp | sed -n '91p'
        gameSettings->playSound = section.getBoolean("playSound");
fork-settings.tsv	строка 17	src/utils/common.cpp@9208dcf:371	совпало
$ git show 9208dcf:src/utils/common.cpp | sed -n '371p'
        {"playSound", boolToIni(settings.playSound)},
fork-settings.tsv	строка 17	src/game/Preferences.cpp@0a33444:99	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '99p'
        settings.playSound = section.getBoolean("playSound");
fork-settings.tsv	строка 17	resources/bin/settings.ini@0a33444:73	совпало
$ git show 0a33444:resources/bin/settings.ini | sed -n '73p'
#playSound = false
preferences.tsv	строка 16	src/utils/InitialGameSettings.hpp@0a33444:32	совпало
$ git show 0a33444:src/utils/InitialGameSettings.hpp | sed -n '32p'
    bool playMusic = true;
preferences.tsv	строка 16	src/game/Preferences.cpp@0a33444:93	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '93p'
        settings.playMusic = section.getBoolean("playMusic");
preferences.tsv	строка 16	src/game/Preferences.cpp@0a33444:171	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '171p'
    set(ini, "playMusic", toText(settings.playMusic));
preferences.tsv	строка 17	src/utils/InitialGameSettings.hpp@0a33444:33	совпало
$ git show 0a33444:src/utils/InitialGameSettings.hpp | sed -n '33p'
    bool customMusic = false;
preferences.tsv	строка 17	src/game/Preferences.cpp@0a33444:96	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '96p'
        settings.customMusic = section.getBoolean("customMusic");
preferences.tsv	строка 17	src/game/Preferences.cpp@0a33444:172	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '172p'
    set(ini, "customMusic", toText(settings.customMusic));
preferences.tsv	строка 18	src/utils/InitialGameSettings.hpp@0a33444:34	совпало
$ git show 0a33444:src/utils/InitialGameSettings.hpp | sed -n '34p'
    bool playSound = true;
preferences.tsv	строка 18	src/game/Preferences.cpp@0a33444:99	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '99p'
        settings.playSound = section.getBoolean("playSound");
preferences.tsv	строка 18	src/game/Preferences.cpp@0a33444:173	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '173p'
    set(ini, "playSound", toText(settings.playSound));
preferences.tsv	строка 19	src/utils/InitialGameSettings.hpp@0a33444:35	совпало
$ git show 0a33444:src/utils/InitialGameSettings.hpp | sed -n '35p'
    bool playCreditsSound = true;
preferences.tsv	строка 19	src/game/Preferences.cpp@0a33444:102	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '102p'
        settings.playCreditsSound = section.getBoolean("playCreditsSound");
preferences.tsv	строка 19	src/game/Preferences.cpp@0a33444:174	совпало
$ git show 0a33444:src/game/Preferences.cpp | sed -n '174p'
    set(ini, "playCreditsSound", toText(settings.playCreditsSound));
preferences.tsv	строка 42	src/utils/InitialGameSettings.hpp@d06f2fc:33	совпало
$ git show d06f2fc:src/utils/InitialGameSettings.hpp | sed -n '33p'
    bool playMusic = true;
preferences.tsv	строка 42	src/game/Preferences.cpp@d06f2fc:92	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '92p'
        settings.playMusic = section.getBoolean("playMusic");
preferences.tsv	строка 42	src/game/Preferences.cpp@d06f2fc:170	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '170p'
    set(ini, "playMusic", toText(settings.playMusic));
preferences.tsv	строка 43	src/utils/InitialGameSettings.hpp@d06f2fc:34	совпало
$ git show d06f2fc:src/utils/InitialGameSettings.hpp | sed -n '34p'
    bool customMusic = false;
preferences.tsv	строка 43	src/game/Preferences.cpp@d06f2fc:95	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '95p'
        settings.customMusic = section.getBoolean("customMusic");
preferences.tsv	строка 43	src/game/Preferences.cpp@d06f2fc:171	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '171p'
    set(ini, "customMusic", toText(settings.customMusic));
preferences.tsv	строка 44	src/utils/InitialGameSettings.hpp@d06f2fc:35	совпало
$ git show d06f2fc:src/utils/InitialGameSettings.hpp | sed -n '35p'
    bool playSound = true;
preferences.tsv	строка 44	src/game/Preferences.cpp@d06f2fc:98	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '98p'
        settings.playSound = section.getBoolean("playSound");
preferences.tsv	строка 44	src/game/Preferences.cpp@d06f2fc:172	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '172p'
    set(ini, "playSound", toText(settings.playSound));
preferences.tsv	строка 45	src/utils/InitialGameSettings.hpp@d06f2fc:36	совпало
$ git show d06f2fc:src/utils/InitialGameSettings.hpp | sed -n '36p'
    bool playCreditsSound = true;
preferences.tsv	строка 45	src/game/Preferences.cpp@d06f2fc:101	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '101p'
        settings.playCreditsSound = section.getBoolean("playCreditsSound");
preferences.tsv	строка 45	src/game/Preferences.cpp@d06f2fc:173	совпало
$ git show d06f2fc:src/game/Preferences.cpp | sed -n '173p'
    set(ini, "playCreditsSound", toText(settings.playCreditsSound));
```

### Поиск `customMusic` в FORK1

Команда: `git grep -n -i 'customMusic' 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src resources/bin/settings.ini`

Вывод: пустой.

# Вклад по пунктам 2 и 4 P9R

## 2. Музыкальные ресурсы форка

### Команда перечня из карты переноса

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 62e1ff6585d8f1f047a3f983c63d990662e6afb6:docs/upstream/port_inventory.json | /srv/dune/venv/bin/python -c "import json,sys; d=json.load(sys.stdin); [print(k) for k,v in d['paths'].items() if 'music-pools' in v.get('features',[]) and k.startswith('resources/bin/')]"
```

Вывод:

```text
resources/bin/music/briefing/atreides/18_MENTAT_ATR.wav
resources/bin/music/briefing/harkonnen/19_MENTAT_HAR.wav
resources/bin/music/briefing/ordos/20_MENTAT_ORD.wav
resources/bin/music/conquest/22_SCENARIO.wav
resources/bin/music/defeat/15_LOSE1.wav
resources/bin/music/defeat/16_LOSE2.wav
resources/bin/music/defeat/17_LOSE3.wav
resources/bin/music/gameplay/Track 1.wav
resources/bin/music/gameplay/Track 10.wav
resources/bin/music/gameplay/Track 11.wav
resources/bin/music/gameplay/Track 2.wav
resources/bin/music/gameplay/Track 3.wav
resources/bin/music/gameplay/Track 4.wav
resources/bin/music/gameplay/Track 5.wav
resources/bin/music/gameplay/Track 6.wav
resources/bin/music/gameplay/Track 7.wav
resources/bin/music/gameplay/Track 8 .wav
resources/bin/music/gameplay/Track 9.wav
resources/bin/music/menu/21_MENU.wav
resources/bin/music/victory/23_WIN01.wav
resources/bin/music/victory/24_WIN02.wav
resources/bin/music/victory/25_WIN03.wav
```

Категории ресурсов подтверждаются конфигурацией контроллера в `src/cGame_logic.cpp@9208dcf`: Gameplay получает `music/gameplay` и девять MIDI fallback-идентификаторов в строках 1142–1146; Menu — `music/menu` и MIDI_MENU в 1147; Conquest — `music/conquest` и MIDI_SCENARIO в 1148; три категории Briefing — папки домов и соответствующие Mentat MIDI в 1149–1151; Victory — `music/victory` и MIDI_WIN01–03 в 1152; Defeat — `music/defeat` и MIDI_LOSE01–03 в 1153. Код задаёт корень как текущую рабочую папку (`src/cGame_logic.cpp@9208dcf:1119`), а `MusicController::configure` присоединяет к ней относительный каталог категории (`src/audio/MusicController.cpp@9208dcf:32`). Перечисление категорий объявлено в `src/audio/MusicController.h@9208dcf:12`.

### Проверка путей и Git LFS

Скрипт подсчёта и формирования таблицы: `.tmp/p9r/resource_inventory.py`. Команда запуска:

```sh
/srv/dune/venv/bin/python .tmp/p9r/resource_inventory.py
```

Скрипт для каждого пути запускает `git diff --name-status BASE FORK1 -- <путь>`, `git cat-file -s FORK1:<путь>`, `git cat-file -p FORK1:<путь>`, проверяет `git cat-file -e PORT:<путь>`, получает хэши `git rev-parse FORK1:<путь>` и `git rev-parse PORT:<путь>` для путей, присутствующих в PORT, и ищет Git LFS объект в хранилище, указанном `git rev-parse --git-common-dir`. Табличный вывод сохранён в `.tmp/p9r/resources.tsv` с требуемыми столбцами.

Для `git cat-file -p 9208dcf5a358f40afd95c99480e4e09f781ed566:resources/bin/music/gameplay/Track 1.wav | head -n 1` вывод: `version https://git-lfs.github.com/spec/v1`. Все 22 строки `resources.tsv` имеют признак Git LFS `да`; у каждой первая строка указателя такая же. Размер Git-объекта для каждой строки — 133 байта. Для каждой строки размер содержимого взят из поля `size` указателя. Скрипт проверил наличие всех 22 LFS объектов в `<git-common-dir>/lfs/objects/<oid-prefix>/<oid>`; все 22 проверки `os.path.isfile(...)` вывели `True`.

Результат проверки статусом, наличием в PORT и совпадением объектов: `git diff --name-status BASE FORK1 -- <путь>` дал `A` для всех 22 файлов; `git cat-file -e PORT:<путь>` не нашёл ни одного пути; поэтому совпадение объектов не вычислялось и отмечено `-`. В последнем столбце `resources.tsv` у всех файлов стоит категория, заданная конфигурацией форка выше.

Итоги по столбцам, stdout `.tmp/p9r/resource_inventory.py`:

```text
status {"A": 22}
git_size {"133": 22}
lfs {"да": 22}
lfs_size: 22 значения, каждое встречается 1 раз; сумма 532834504 байта
port {"нет": 22}
object_same {"-": 22}
category {"BriefingAtreides": 1, "BriefingHarkonnen": 1, "BriefingOrdos": 1, "Conquest": 1, "Defeat": 3, "Gameplay": 11, "Menu": 1, "Victory": 3}
```

Конкретные размеры содержимого и пути перечислены построчно в `resources.tsv`; команда суммирования указана в `.tmp/p9r/resource_inventory.py` и при запуске печатает `lfs_size_total_bytes\t532834504`.

## 4. Музыка в PORT и апстриме

### Дерево музыкальных файлов

Команда из задания:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git ls-tree -r --name-only 616280c8926ec642d86144a9fe2db105ceaf4061 -- resources/bin | grep -i -E 'music|\.(ogg|mp3|mid|xmi|wav|opus|flac)$'
```

Вывод пустой: под `resources/bin` в PORT не найдено путей, соответствующих `music` или указанным аудиорасширениям. Команда `git ls-tree -r --name-only 616280c8926ec642d86144a9fe2db105ceaf4061 -- audio` также вывела пустую строку, поэтому в дереве репозитория нет отслеживаемых файлов под `audio/`.

Пользовательские каталоги, создаваемые кодом по умолчанию под корнем `audio`, перечислены в `src/context/MusicJukeBox.cpp@616280c:79-82`. Для каждой папки подсчёт отслеживаемых файлов в дереве репозитория — 0; пользовательское содержимое, отсутствующее в Git-дереве, этим подсчётом не охватывается. `listAudioFiles` читает непосредственное содержимое каталога через `std::filesystem::directory_iterator` (`src/context/MusicJukeBox.cpp@616280c:58-67`), принимает расширения `.ogg`, `.mp3`, `.wav`, `.flac` без учёта регистра (`src/context/MusicJukeBox.cpp@616280c:27-34`):

| Папка | Музыкальный тип | Число файлов в Git-дереве | Код выбора каталога | Код чтения |
|---|---|---:|---|---|
| `audio/win` | WIN | 0 | `src/context/MusicJukeBox.cpp@616280c:40` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/lose` | LOSE | 0 | `src/context/MusicJukeBox.cpp@616280c:41` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/attack` | ATTACK | 0 | `src/context/MusicJukeBox.cpp@616280c:42` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/peace` | PEACE | 0 | `src/context/MusicJukeBox.cpp@616280c:43` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/menu` | MENU | 0 | `src/context/MusicJukeBox.cpp@616280c:44` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/conquest` | CONQUEST | 0 | `src/context/MusicJukeBox.cpp@616280c:45` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/briefing/atreides` | BRIEFING, Atreides | 0 | `src/context/MusicJukeBox.cpp@616280c:48` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/briefing/harkonnen` | BRIEFING, Harkonnen | 0 | `src/context/MusicJukeBox.cpp@616280c:49` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/briefing/ordos` | BRIEFING, Ordos | 0 | `src/context/MusicJukeBox.cpp@616280c:50` | `src/context/MusicJukeBox.cpp@616280c:62` |
| `audio/briefing/sardaukar` | BRIEFING, Sardaukar | 0 | `src/context/MusicJukeBox.cpp@616280c:51` | `src/context/MusicJukeBox.cpp@616280c:62` |

### Функции выбора и воспроизведения

`eMusicType` объявлен в `src/include/definitions.h@616280c:158-166`: WIN, LOSE, ATTACK, PEACE, MENU, CONQUEST и BRIEFING. Имена для журнала и архивные MIDI-выборы находятся в `src/context/AudioContext.cpp@616280c:30-42` и `:115-153`. WIN использует случайный выбор из трёх MIDI, LOSE и ATTACK — из шести, PEACE — из девяти; MENU и CONQUEST используют фиксированные MIDI. BRIEFING выбирает MIDI Mentat по дому; для Sardaukar задан MIDI Harkonnen (`:134-149`).

`AudioContext::playMusicByType` (`src/context/AudioContext.cpp@616280c:92`) проверяет повторное голосовое событие и настройку музыки, вычисляет архивный fallback и вызывает `MusicJukeBox::choose` (`:170-172`). Переходная обёртка `playMusicByTypeForStateTransition` не запускает повторно уже активный тип (`:84-89`). `MusicJukeBox::choose` (`src/context/MusicJukeBox.cpp@616280c:90-110`) возвращает fallback, если пользовательская музыка выключена, каталог отсутствует или пуст; иначе сортирует список файлов и выбирает путь через `RNG::rnd`. `AudioContext::startMusic` (`src/context/AudioContext.cpp@616280c:175-181`) использует пользовательский файл, а при неудаче — архивный трек. `AudioContext::thinkFast` (`:183-216`) запускает выбор по окончании отсчёта, ждёт завершения дорожки и повторяет текущую музыку; после ATTACK устанавливает PEACE, а BRIEFING повторяет сохранённый архивный выбор.

`AudioContext::toggleMusic` и `setMusicEnabled` (`src/context/AudioContext.cpp@616280c:219`, `:224`) меняют состояние музыки; при включении `setMusicEnabled` разрешает `thinkFast` запустить текущий тип. `changeMusicVolume` (`:234`) передаёт изменение громкости в проигрыватель.

Команда чтения этих функций:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 616280c8926ec642d86144a9fe2db105ceaf4061:src/context/AudioContext.cpp | nl -ba | sed -n '219,275p'
```

Вывод:

```text
219 void AudioContext::toggleMusic()
220 {
221     setMusicEnabled(!m_settings->isPlayMusic());
222 }
223
224 void AudioContext::setMusicEnabled(bool enabled)
225 {
226     m_settings->setPlayMusic(enabled);
227     m_soundPlayer->setMusicEnabled(enabled);
228     if (enabled) {
229         // let thinkFast() start the music of the current music type; nothing may have been picked yet when booted with -nomusic
230         m_newMusicCountdown = -1;
231     }
232 }
233
234 void AudioContext::changeMusicVolume(int delta) const
235 {
236     m_soundPlayer->changeMusicVolume(delta);
237 }
```

В `src/utils/cSoundPlayer.cpp@616280c` функции `playMusic` (`:177-191`), `playMusicFile` (`:193-212`) и `startMusic` (`:214-220`) передают архивное или загруженное из файла аудио на единственную музыкальную дорожку. `startMusic` выставляет `kNoLoop`, то есть повтор задаёт `AudioContext`; завершение дорожки проверяет `isMusicPlaying` (`:230-236`), остановку выполняет `stopMusic` (`:238-243`). Настройка усиления музыки находится в `setMusicVolume` (`:245-252`), отключение музыки останавливает дорожку в `setMusicEnabled` (`:277-282`). Загрузка пользовательского файла использует `SDL_IOFromFile` и `MIX_LoadAudio_IO` (`:198-210`).

### Вызовы SDL3_mixer

Команда поиска всех вызовов с именем `MIX_`:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'MIX_[A-Za-z0-9_]+[[:space:]]*\(' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src
```

Вывод (каждая найденная строка отражена отдельной строкой в `port-music.tsv`):

```text
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cSDLSystem.cpp:236:    MIX_Quit();
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cSDLSystem.cpp:269:    if (!MIX_Init()) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cSDLSystem.cpp:275:        for (auto i =0; i < MIX_GetNumAudioDecoders();i++) {
616280c8926ec642d86144a9fe2db105ceaf4061:src/game/cSDLSystem.cpp:276:            Logger::info(COMP_SDL2, "SDL_mixer", "Audio decoder {} : {}", i, MIX_GetAudioDecoder(i));
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cDataPack.cpp:37:        if (audio) MIX_DestroyAudio(audio);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cDataPack.cpp:101:    MIX_Audio *out = MIX_LoadAudioWithProperties(props);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:67:    m_mixer = MIX_CreateMixerDevice(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, nullptr);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:77:        m_musicTrack = MIX_CreateTrack(m_mixer);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:79:            MIX_Track *track = MIX_CreateTrack(m_mixer);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:95:        MIX_SetMixerGain(m_mixer, 1.0f);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:98:        MIX_SetTrackGain(track, m_soundVolume / static_cast<float>(MaxVolume));
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:101:        MIX_SetTrackGain(m_musicTrack, m_musicVolume / static_cast<float>(MaxVolume));
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:111:        MIX_StopTrack(m_musicTrack, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:112:        MIX_DestroyTrack(m_musicTrack);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:116:        MIX_StopTrack(track, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:117:        MIX_DestroyTrack(track);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:120:        MIX_DestroyMixer(m_mixer);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:150:            m_sfxTrackBusy[i] = MIX_TrackPlaying(m_sfxTracks[i]);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:156:        MIX_StopTrack(track, kSfxFadeFrames);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:157:        MIX_SetTrackAudio(track, audio);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:158:        MIX_PlayTrack(track, m_sfxPlayOptions);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:203:    MIX_Audio *audio = MIX_LoadAudio_IO(m_mixer, io, false, true);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:216:    MIX_StopTrack(m_musicTrack, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:217:    MIX_SetTrackAudio(m_musicTrack, audio);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:218:    MIX_SetTrackLoops(m_musicTrack, kNoLoop);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:219:    MIX_PlayTrack(m_musicTrack, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:225:        MIX_DestroyAudio(m_musicFileAudio);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:235:    return MIX_TrackPlaying(m_musicTrack);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:241:        MIX_StopTrack(m_musicTrack, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:250:        MIX_SetTrackGain(m_musicTrack, m_musicVolume / static_cast<float>(MaxVolume));
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:265:        MIX_SetTrackGain(track, m_soundVolume / static_cast<float>(MaxVolume));
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:273:        MIX_StopAllTracks(m_mixer, 0);
616280c8926ec642d86144a9fe2db105ceaf4061:src/utils/cSoundPlayer.cpp:281:        MIX_StopTrack(m_musicTrack, 0);
```

### Типы музыки и места включения

Команда проверки перечисления и использований:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'enum class eMusicType|eMusicType::' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src
```

Объявление и назначения типа перечислены выше. В PORT вызовы группируются так: WIN — `src/game/cGame_logic.cpp@616280c:485`; LOSE — `:508`; MENU — `:871`, `:1129`, `:1143`; CONQUEST — `:1049`, `:1122`; BRIEFING — `:1200`, `:1205`, `:1208`, `:1212`, `:1270`, `:1358`, `:1485`; PEACE — `:1309` и состояние Skirmish в `src/gamestates/cSetupSkirmishState.cpp@616280c:1043`; ATTACK — `src/gameobjects/players/cPlayer.cpp@616280c:2126`. Проверка PEACE перед обработкой обнаружения противника находится в `src/gameobjects/players/cPlayer.cpp@616280c:2067`. Состояние следующего завоевания включает BRIEFING в `src/gamestates/cSelectYourNextConquestState.cpp@d06f2fc:464`; настройка Skirmish включает PEACE в `src/gamestates/cSetupSkirmishState.cpp@d06f2fc:975`.

Полный перечень функций выбора/проигрывания, типов, мест включения, папок и всех вызовов `MIX_` — `.tmp/p9r/port-music.tsv`.

### Изменения апстрима между BASE и UP1

Команда по кодовым файлам музыки и пути ресурсов `resources/bin/music`:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git log --format='%h %ad %s' --date=short e17379ad660fca46859b403a6c3d33ec8d831a40..d06f2fcd2a347182c3774fb96e9a85570405c489 -- src/context/AudioContext.cpp src/context/AudioContext.hpp src/context/MusicChoice.hpp src/context/MusicJukeBox.cpp src/context/MusicJukeBox.hpp src/utils/cSoundPlayer.cpp src/utils/cSoundPlayer.h resources/bin/music
```

Вывод:

```text
ac2f17d6 2026-11-08 AudioContext header forward declares MusicJukeBox, MusicChoice has its own header
214407c2 2026-11-08 AudioContext holds the MusicJukeBox through a unique_ptr
6f41fdc3 2026-11-08 Music directories are created at startup
4f2d804e 2026-11-08 Every music type has its own audio directory, briefing music one per house
984decc2 2026-11-08 Attack and peace music can be played from files in audio/attack and audio/peace
037a564d 2026-11-08 Music types are an eMusicType enum class instead of int constants
2d5137f0 2026-11-07 C-style casts in cSoundPlayer.cpp replaced by static_cast
1a8c3a4c 2026-10-27 Briefing music loops again by replaying its stored sample, playMusicByType no longer takes a player id
ea43f50c 2026-10-25 Do not loop briefing music.
1ffc799d 2026-10-23 Music can be enabled from the options menu after booting with -nomusic
daa4aa6f 2026-10-01 Audio logic extracted from cGame into a new AudioContext class
c84c527d 2026-09-14 Header copyright line matches LICENSE.md exactly
2ab4a4f1 2026-09-14 All src files get the standard MIT license header
5a37bfe4 2026-09-12 Double the sfx track pool and make stealing priority-aware
cec7ef61 2026-09-12 Fade sound effects in as well as out, not just out
b2fd2811 2026-09-12 Reuse a member buffer for sfx track busy-state instead of allocating
26b80c6c 2026-09-11 Fade sound-effect tracks out instead of stopping them instantly
463b2fef 2026-09-11 Sound effect tracks no longer stolen from still-playing sounds
cff18043 2026-06-17 SFX tracks stop cleanly before reuse and pool size raised to 32
1f255e21 2026-06-17 Sound slider no longer changes music volume
d4c1d676 2026-06-09 Fix missing replacement
734b1774 2026-06-09 Replace cLogger::getInstance() with Logger:: namespace calls
6b7df3f4 2026-06-09 Music error is logged once and stops retrying on missing audio sample
d13abba3 2026-06-07 Remove unused eLogOutcome
5af13f5e 2026-06-03 Fix SDL3 rendering: fullscreen scaling, HiDPI, text rendering, and audio crash
2801744c 2026-06-02 Rewrite audio subsystem for SDL3_mixer 3.x API
76931213 2026-06-02 Update audio mixer initialisation for SDL3
0e414c9c 2026-06-02 Update all SDL include paths from SDL2 to SDL3
602a2b1e 2026-05-15 Change to cAssert
```


# Вклад по пунктам 3 и 5 задания P9R

Ревизии для строк: `BASE=e17379ad660fca46859b403a6c3d33ec8d831a40`, `FORK1=9208dcf5a358f40afd95c99480e4e09f781ed566`, `PORT=616280c8926ec642d86144a9fe2db105ceaf4061`. Перед каждой командой Git установлен путь `/srv/dune/tools/git-lfs-3.6.1/usr/bin`. Ветка, исходники, сборки и CTest не менялись и не запускались.

## 3. Правки форка вне src/audio/

### Путь файлов и diff

Команда поиска путей для тех же файлов FORK1 в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
for p in CMakeLists.txt src/cGame.h src/cGame_logic.cpp src/drawers/cMessageDrawer.cpp src/managers/cDrawManager.cpp src/managers/cDrawManager.h src/player/cPlayer.cpp src/player/cPlayer.h src/utils/cSoundPlayer.cpp src/utils/cSoundPlayer.h; do
    if git cat-file -e 616280c8926ec642d86144a9fe2db105ceaf4061:$p 2>/dev/null; then
        echo "same $p"
    else
        b=${p##*/}
        echo "search $b"
        git ls-tree -r --name-only 616280c8926ec642d86144a9fe2db105ceaf4061 | grep "/$b\$"
    fi
done
```

Вывод:

```text
same CMakeLists.txt
search cGame.h
src/game/cGame.h
search cGame_logic.cpp
src/game/cGame_logic.cpp
same src/drawers/cMessageDrawer.cpp
same src/managers/cDrawManager.cpp
same src/managers/cDrawManager.h
search cPlayer.cpp
src/gameobjects/players/cPlayer.cpp
search cPlayer.h
src/gameobjects/players/cPlayer.h
same src/utils/cSoundPlayer.cpp
same src/utils/cSoundPlayer.h
```

Команда diff для указанных файлов:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff --no-ext-diff --unified=0 e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- CMakeLists.txt src/cGame.h src/cGame_logic.cpp src/drawers/cMessageDrawer.cpp src/managers/cDrawManager.cpp src/managers/cDrawManager.h src/player/cPlayer.cpp src/player/cPlayer.h src/utils/cSoundPlayer.cpp src/utils/cSoundPlayer.h
```

Выводы hunks, прошедших фильтр имени музыкального символа или `music/Music`, записаны построчно с коротким содержанием изменения и сверкой в PORT в `.tmp/p9r/fork-hooks.tsv`. Ключевые строки исходного вывода diff:

- `CMakeLists.txt@9208dcf:397`, `CMakeLists.txt@9208dcf:407`, `CMakeLists.txt@9208dcf:418`, `CMakeLists.txt@9208dcf:431`: добавлены цели и CTest-регистрации playlist, transition policy и controls layout.
- `src/cGame.h@9208dcf:46`, `src/cGame.h@9208dcf:158`, `src/cGame.h@9208dcf:333`: объявлены MusicController, методы навигации и имени текущей композиции, указатель-владелец.
- `src/cGame_logic.cpp@9208dcf:14`, `src/cGame_logic.cpp@9208dcf:96`, `src/cGame_logic.cpp@9208dcf:568`, `src/cGame_logic.cpp@9208dcf:1116`: включены заголовки контроллера/политики, добавлено сопоставление категорий, цикл обновления, создание восьми каталогов и настройка fallback MIDI.
- `src/cGame_logic.cpp@9208dcf:1444`, `src/cGame_logic.cpp@9208dcf:2094`, `src/cGame_logic.cpp@9208dcf:2096`, `src/cGame_logic.cpp@9208dcf:2100`, `src/cGame_logic.cpp@9208dcf:2105`: музыка включается при переходе состояния, выключается/возобновляется отдельными методами, а клавиши в квадратных скобках переключают треки.
- `src/cGame_logic.cpp@9208dcf:2217`, `src/cGame_logic.cpp@9208dcf:2229`, `src/cGame_logic.cpp@9208dcf:2234`, `src/cGame_logic.cpp@9208dcf:2242`, `src/cGame_logic.cpp@9208dcf:2256`, `src/cGame_logic.cpp@9208dcf:2263`, `src/cGame_logic.cpp@9208dcf:2270`: переход типа передаётся контроллеру, ATTACK сводится к PEACE, категория активируется с политикой повторного входа; добавлены методы previous/next и имя текущего трека.
- `src/drawers/cMessageDrawer.cpp@9208dcf:6`, `src/drawers/cMessageDrawer.cpp@9208dcf:42`: боевое сообщение учитывает занимаемое музыкальным контролом место.
- `src/managers/cDrawManager.cpp@9208dcf:13`, `src/managers/cDrawManager.cpp@9208dcf:89`, `src/managers/cDrawManager.cpp@9208dcf:288`, `src/managers/cDrawManager.h@9208dcf:105`: панель вызывается во время боя; добавлены кнопки треков, подпись трека и слайдер скорости.
- `src/player/cPlayer.cpp@9208dcf:1880`, `src/player/cPlayer.cpp@9208dcf:1884`, `src/player/cPlayer.cpp@9208dcf:1892`, `src/player/cPlayer.cpp@9208dcf:1916`, `src/player/cPlayer.cpp@9208dcf:1926`: убрана смена темы на ATTACK при обнаружении; предупреждающая реплика ограничена cooldown в 30 секунд.
- `src/utils/cSoundPlayer.cpp@9208dcf:62`, `src/utils/cSoundPlayer.cpp@9208dcf:104`, `src/utils/cSoundPlayer.cpp@9208dcf:156`, `src/utils/cSoundPlayer.cpp@9208dcf:161`, `src/utils/cSoundPlayer.cpp@9208dcf:198`, `src/utils/cSoundPlayer.h@9208dcf:24`, `src/utils/cSoundPlayer.h@9208dcf:55`: добавлены Mix_Init optional codecs, загрузка и освобождение внешнего Mix_Music, а также поля владения и метод playMusicFile.

Сверка портового кода по тому же музыкальному пути дала такие строки вывода:

```text
src/game/cGame.h@616280c:196: AudioContext* m_audioContext = nullptr
src/context/MusicJukeBox.cpp@616280c:37; src/context/MusicJukeBox.cpp@616280c:42; src/context/MusicJukeBox.cpp@616280c:46; src/context/MusicJukeBox.cpp@616280c:48: repertoryDir сопоставляет eMusicType каталогам
src/context/MusicJukeBox.cpp@616280c:76; src/context/MusicJukeBox.cpp@616280c:79: createRepertoryDirectories создаёт каталоги
src/context/MusicJukeBox.cpp@616280c:90; src/context/MusicJukeBox.cpp@616280c:102; src/context/MusicJukeBox.cpp@616280c:109: choose выбирает файл из каталога, иначе сохраняет archive fallback
src/context/AudioContext.cpp@616280c:84; src/context/AudioContext.cpp@616280c:86; src/context/AudioContext.cpp@616280c:88: playMusicByTypeForStateTransition
src/context/AudioContext.cpp@616280c:92; src/context/AudioContext.cpp@616280c:115; src/context/AudioContext.cpp@616280c:170: playMusicByType выбирает архивный sample и MusicJukeBox choice
src/context/AudioContext.cpp@616280c:175; src/context/AudioContext.cpp@616280c:177; src/context/AudioContext.cpp@616280c:180: startMusic проигрывает файл или archive track
src/context/AudioContext.cpp@616280c:183; src/context/AudioContext.cpp@616280c:203: thinkFast управляет countdown и повтором музыки
src/context/AudioContext.cpp@616280c:219; src/context/AudioContext.cpp@616280c:224; src/context/AudioContext.cpp@616280c:227: toggleMusic/setMusicEnabled
src/game/cGame_logic.cpp@616280c:1523; src/game/cGame_logic.cpp@616280c:1524: TOGGLE_MUSIC вызывает AudioContext::toggleMusic
src/game/cGame_logic.cpp@616280c:1578; src/game/cGame_logic.cpp@616280c:1583: обёртки перехода и playMusicByType
src/gameobjects/players/cPlayer.cpp@616280c:2067; src/gameobjects/players/cPlayer.cpp@616280c:2077; src/gameobjects/players/cPlayer.cpp@616280c:2126: оставлены PEACE guard, triggerMusic и вызов ATTACK
src/utils/cSoundPlayer.cpp@616280c:193; src/utils/cSoundPlayer.cpp@616280c:198; src/utils/cSoundPlayer.cpp@616280c:203; src/utils/cSoundPlayer.cpp@616280c:208: SDL3 playMusicFile(std::string), загрузка через SDL_IOStream и MIX_LoadAudio_IO
src/utils/cSoundPlayer.cpp@616280c:222; src/utils/cSoundPlayer.cpp@616280c:224; src/utils/cSoundPlayer.cpp@616280c:225: releaseMusicFile освобождает MIX_Audio
```

Для controls-участков `git grep -n -E 'MusicControlsLayout|drawTopBarMusicControls|drawMusicControls|playPreviousGameplayTrack|playNextGameplayTrack|getCurrentMusicTrackName|MusicController' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src CMakeLists.txt` завершился кодом 1 и без вывода. В PORT отсутствуют эти элементы игрового HUD и трековой навигации. Для перемещённых cGame и cPlayer использованы найденные пути; у остальных перечисленных источников те же пути присутствуют.

## 5. Тесты

### Регистрация CTest

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:CMakeLists.txt | nl -ba | sed -n '397,444p'
```

Релевантный вывод:

```text
397 add_executable(
398     music_playlist_tests
399     tests/MusicPlaylistTests.cpp
400     src/audio/MusicPlaylist.cpp
401 )
407 add_test(NAME music_playlist_shuffle_history COMMAND music_playlist_tests)
409 add_executable(
410     music_transition_policy_tests
411     tests/MusicTransitionPolicyTests.cpp
412 )
418 add_test(NAME music_transition_policy COMMAND music_transition_policy_tests)
420 add_executable(
421     music_controls_layout_tests
422     tests/MusicControlsLayoutTests.cpp
423     src/utils/cRectangle.cpp
424 )
431 add_test(NAME music_controls_layout_geometry COMMAND music_controls_layout_tests)
```

### Подсчёт проверок

Первый inline-вызов вспомогательного счётчика завершился `SyntaxError: unexpected character after line continuation character`; это была ошибка кавычек в команде счёта. Повторная команда отдельно читает каждый тест через `git show` и считает вызовы assertion-макросов, блоки `if` и вызовы transition-функции:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
/srv/dune/venv/bin/python -c 'import re,subprocess
rev="9208dcf5a358f40afd95c99480e4e09f781ed566"
files=["tests/MusicControlsLayoutTests.cpp","tests/MusicPlaylistTests.cpp","tests/MusicTransitionPolicyTests.cpp"]
pat=re.compile(r"(?<![A-Za-z0-9_])(?:assert|CHECK|REQUIRE|EXPECT_[A-Z]+|ASSERT_[A-Z]+)\s*\(")
for f in files:
 s=subprocess.run(["git","show",rev+":"+f],text=True,stdout=subprocess.PIPE,check=True).stdout
 a=len(pat.findall(s))
 i=len(re.findall(r"^\s*if\s*\(",s,re.M))
 p=s.count("shouldAdvanceRepeatedMusicCategory(")
 print(f+": assertion_macro_calls="+str(a)+"; if_blocks="+str(i)+"; shouldAdvance_calls="+str(p))'
```

Вывод повторного запуска:

```text
tests/MusicControlsLayoutTests.cpp: assertion_macro_calls=0; if_blocks=4; shouldAdvance_calls=0
tests/MusicPlaylistTests.cpp: assertion_macro_calls=15; if_blocks=0; shouldAdvance_calls=0
tests/MusicTransitionPolicyTests.cpp: assertion_macro_calls=0; if_blocks=0; shouldAdvance_calls=3
```

Команды построчной выборки проверок:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MusicControlsLayoutTests.cpp | rg -n 'assert\s*\(|CHECK\s*\(|REQUIRE\s*\(|EXPECT_[A-Z]+\s*\(|^\s*if\s*\('
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MusicPlaylistTests.cpp | rg -n 'assert\s*\(|CHECK\s*\(|REQUIRE\s*\(|EXPECT_[A-Z]+\s*\('
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git show 9208dcf5a358f40afd95c99480e4e09f781ed566:tests/MusicTransitionPolicyTests.cpp | rg -n 'assert\s*\(|CHECK\s*\(|REQUIRE\s*\(|EXPECT_[A-Z]+\s*\(|shouldAdvanceRepeatedMusicCategory|return valid'
```

Выводы: controls layout имеет четыре явных `if`-проверки, которые вызываются для трёх размеров окна из `tests/MusicControlsLayoutTests.cpp@9208dcf:49, tests/MusicControlsLayoutTests.cpp@9208dcf:50 и tests/MusicControlsLayoutTests.cpp@9208dcf:51`; macros нет. Playlist содержит 15 вызовов assert. Transition policy содержит три входа policy-функции, объединённых в `valid` и проверенных результатом `return valid ? 0 : 1` на строках 5–9; macros нет. Смысл каждой проверки дан построчно в `.tmp/p9r/tests.tsv`.

### Файлы и зависимости тестов

Проверка файлов в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
for p in tests/MusicControlsLayoutTests.cpp tests/MusicPlaylistTests.cpp tests/MusicTransitionPolicyTests.cpp src/audio/MusicPlaylist.h src/audio/MusicPlaylist.cpp src/audio/MusicTransitionPolicy.hpp src/sidebar/MusicControlsLayout.hpp src/sidebar/HudLayout.hpp src/utils/cRectangle.h; do
    if git cat-file -e 616280c8926ec642d86144a9fe2db105ceaf4061:$p 2>/dev/null; then
        echo "$p present"
    else
        echo "$p absent"
    fi
done
```

Вывод:

```text
tests/MusicControlsLayoutTests.cpp absent
tests/MusicPlaylistTests.cpp absent
tests/MusicTransitionPolicyTests.cpp absent
src/audio/MusicPlaylist.h absent
src/audio/MusicPlaylist.cpp absent
src/audio/MusicTransitionPolicy.hpp absent
src/sidebar/MusicControlsLayout.hpp absent
src/sidebar/HudLayout.hpp absent
src/utils/cRectangle.h present
```

Команда проверки имен проектных символов в PORT:
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'class HudLayout|struct HudLayout|class MusicPlaylist|struct MusicTrack|shouldAdvanceRepeatedMusicCategory|struct MusicControlsLayout' 616280c8926ec642d86144a9fe2db105ceaf4061 -- src
Вывод пустой, код возврата 1.

Для имён, чьи точные пути не найдены, использована команда `git ls-tree -r --name-only 616280c8926ec642d86144a9fe2db105ceaf4061 | grep '/<basename>$'`. Поиск `MusicPlaylist.h`, `MusicPlaylist.cpp`, `MusicTransitionPolicy.hpp`, `MusicControlsLayout.hpp`, `HudLayout.hpp` и трёх тестов не выдал ни одного пути. Вывод `git grep` по PORT содержит только совпадения `cRectangle`: `src/utils/cRectangle.h@616280c:21` объявляет класс, src/utils/cRectangle.h@616280c:37, src/utils/cRectangle.h@616280c:39, src/utils/cRectangle.h@616280c:54, src/utils/cRectangle.h@616280c:60, src/utils/cRectangle.h@616280c:63, src/utils/cRectangle.h@616280c:66 дают перекрытие и геометрические методы. Имена MusicPlaylist/MusicTrack/shouldAdvanceRepeatedMusicCategory и обе layout-структуры в PORT не найдены.

`MusicPlaylistTests.cpp` создаёт fixture в `std::filesystem::temp_directory_path() / "d2tm_music_playlist_test"` на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55: четыре ASCII-файла и `пустыня.flac`. tests/MusicPlaylistTests.cpp@9208dcf:57 передаёт каталог в `discoverExternalTracks`; тест проверяет имена и расширения, содержимое файлов не открывает. Controls layout и transition policy тесты внешние файлы не читают. Таблица `.tmp/p9r/tests.tsv` содержит каждый assert/if/policy-вход, смысл, используемые проектные символы и заголовки, наличие каждого в PORT и источник файловых данных.

Проверка CTest-регистраций музыкальных тестов в PORT:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git grep -n -E 'music_playlist|music_transition|music_controls|MusicPlaylistTests|MusicTransitionPolicyTests|MusicControlsLayoutTests' 616280c8926ec642d86144a9fe2db105ceaf4061 -- CMakeLists.txt src/CMakeLists.txt tests
```

Вывод пустой, код возврата 1: регистрации и соответствующие тесты не обнаружены.

## Не проверено

Сборка, CTest и запуск игры не выполнялись, как требует задание. Наблюдаемое поведение тестов в исполнении не проверялось; подсчитаны статические проверки в исходниках.

## Полные таблицы

Таблицы ниже повторены здесь целиком; отдельные файлы `.tsv` остаются пригодными для машинной обработки.

### `fork-music.tsv`

```tsv
путь	символ	путь@9208dcf:строка	входы	выходы	что делает
src/audio/MusicController.h	cSoundPlayer (forward declaration)	src/audio/MusicController.h@9208dcf:10	—	неполное объявление типа	Позволяет объявить зависимость контроллера от проигрывателя
src/audio/MusicController.h	MusicCategory (enum class)	src/audio/MusicController.h@9208dcf:12	—	тип категорий	Задаёт индексы пулов Gameplay, Menu, Conquest, BriefingAtreides, BriefingHarkonnen, BriefingOrdos, Victory, Defeat и Count
src/audio/MusicController.h	MusicCategory::Gameplay	src/audio/MusicController.h@9208dcf:13	—	значение категории	Категория игрового процесса
src/audio/MusicController.h	MusicCategory::Menu	src/audio/MusicController.h@9208dcf:14	—	значение категории	Категория меню
src/audio/MusicController.h	MusicCategory::Conquest	src/audio/MusicController.h@9208dcf:15	—	значение категории	Категория завоевания
src/audio/MusicController.h	MusicCategory::BriefingAtreides	src/audio/MusicController.h@9208dcf:16	—	значение категории	Категория брифинга Атрейдес
src/audio/MusicController.h	MusicCategory::BriefingHarkonnen	src/audio/MusicController.h@9208dcf:17	—	значение категории	Категория брифинга Харконненов
src/audio/MusicController.h	MusicCategory::BriefingOrdos	src/audio/MusicController.h@9208dcf:18	—	значение категории	Категория брифинга Ордосов
src/audio/MusicController.h	MusicCategory::Victory	src/audio/MusicController.h@9208dcf:19	—	значение категории	Категория победы
src/audio/MusicController.h	MusicCategory::Defeat	src/audio/MusicController.h@9208dcf:20	—	значение категории	Категория поражения
src/audio/MusicController.h	MusicCategory::Count	src/audio/MusicController.h@9208dcf:21	—	значение границы массива	Число категорий задаёт размер массива состояний
src/audio/MusicController.h	MusicController (class)	src/audio/MusicController.h@9208dcf:24	cSoundPlayer и каталог игры	API управления пулами	Хранит плейлисты категорий и вызывает проигрыватель; UiAuditAccess объявлен другом класса
src/audio/MusicController.cpp	indexOf	src/audio/MusicController.cpp@9208dcf:9	MusicCategory	std::size_t	Преобразует категорию в индекс массива
src/audio/MusicController.cpp	utf8String	src/audio/MusicController.cpp@9208dcf:14	filesystem::path	std::string	Преобразует UTF-8-представление пути в строку для журнала
src/audio/MusicController.cpp	MusicController::MusicController	src/audio/MusicController.cpp@9208dcf:21	указатель cSoundPlayer, каталог игры	новый MusicController	Сохраняет проигрыватель и каталог; пустой каталог заменяет текущим рабочим каталогом
src/audio/MusicController.cpp	MusicController::configure	src/audio/MusicController.cpp@9208dcf:26	категория, относительный каталог, vector<int> встроенных ID	void	Запоминает пользовательский каталог и fallback; сканирует файлы с неподдерживаемым расширением для предупреждений, находит внешние треки и выбирает внешний список либо fallback
src/audio/MusicController.cpp	MusicController::activate	src/audio/MusicController.cpp@9208dcf:67	категория, advanceOnRepeatedEntry	void	Устанавливает активную категорию и запускает следующий трек при новой категории, разрешённом продвижении или остановленном проигрывателе
src/audio/MusicController.cpp	MusicController::update	src/audio/MusicController.cpp@9208dcf:77	состояние проигрывателя	void	Запускает следующий трек активной категории, если музыка закончилась
src/audio/MusicController.cpp	MusicController::next	src/audio/MusicController.cpp@9208dcf:84	активная категория	void	Переходит к следующему треку при наличии активной категории
src/audio/MusicController.cpp	MusicController::previous	src/audio/MusicController.cpp@9208dcf:91	активная категория	void	Переходит к предыдущей позиции истории при наличии активной категории
src/audio/MusicController.cpp	MusicController::replayCurrent	src/audio/MusicController.cpp@9208dcf:98	активная категория и текущий трек	void	Повторно запускает текущий трек; при отсутствии или ошибке запускает следующий доступный
src/audio/MusicController.cpp	MusicController::stop	src/audio/MusicController.cpp@9208dcf:109	—	void	Останавливает музыку через cSoundPlayer
src/audio/MusicController.cpp	MusicController::currentDisplayName	src/audio/MusicController.cpp@9208dcf:114	активная категория и текущий трек	std::string	Возвращает отображаемое имя текущего трека либо пустую строку
src/audio/MusicController.h	MusicController::hasActiveCategory	src/audio/MusicController.h@9208dcf:42	состояние контроллера	bool	Возвращает флаг наличия активной категории
src/audio/MusicController.cpp	MusicController::play	src/audio/MusicController.cpp@9208dcf:123	MusicTrack pointer	bool	Запускает встроенный ID или внешний файл; при ошибке внешнего файла журналирует предупреждение и возвращает false
src/audio/MusicController.cpp	MusicController::playNextAvailable	src/audio/MusicController.cpp@9208dcf:145	направление перехода	void	Перебирает плейлист; удаляет неиграбельный текущий трек, затем при исчерпании пользовательских треков включает встроенный fallback, иначе останавливает музыку
src/audio/MusicController.cpp	MusicController::switchToFallback	src/audio/MusicController.cpp@9208dcf:172	CategoryState reference	void	Выбирает встроенный список и сбрасывает состояние плейлиста
src/audio/MusicController.cpp	MusicController::activeState	src/audio/MusicController.cpp@9208dcf:178	активная категория	CategoryState reference	Возвращает изменяемое состояние активной категории
src/audio/MusicController.cpp	MusicController::activeState const	src/audio/MusicController.cpp@9208dcf:183	активная категория	const CategoryState reference	Возвращает неизменяемое состояние активной категории
src/audio/MusicController.h	MusicController::CategoryState (nested struct)	src/audio/MusicController.h@9208dcf:45	—	состояние одного пула	Содержит плейлист, встроенный fallback, флаг пользовательских треков и каталог
src/audio/MusicPlaylist.h	MusicTrack (struct)	src/audio/MusicPlaylist.h@9208dcf:10	встроенный ID и/или внешний путь	значение трека	Представляет встроенный или внешний музыкальный трек
src/audio/MusicPlaylist.h	MusicTrack::builtInId	src/audio/MusicPlaylist.h@9208dcf:11	—	int, начальное значение -1	ID встроенного трека
src/audio/MusicPlaylist.h	MusicTrack::externalPath	src/audio/MusicPlaylist.h@9208dcf:12	—	filesystem::path	Путь внешнего трека
src/audio/MusicPlaylist.h	MusicTrack::isExternal	src/audio/MusicPlaylist.h@9208dcf:14	externalPath	bool	Проверяет, задан ли внешний путь
src/audio/MusicPlaylist.cpp	MusicTrack::key	src/audio/MusicPlaylist.cpp@9208dcf:23	поля MusicTrack	std::string	Возвращает нормализованный путь внешнего файла или строковый встроенный ID
src/audio/MusicPlaylist.cpp	MusicTrack::displayName	src/audio/MusicPlaylist.cpp@9208dcf:28	поля MusicTrack	std::string	Возвращает имя файла без расширения или Dune II с номером встроенного трека
src/audio/MusicPlaylist.h	MusicPlaylist (class)	src/audio/MusicPlaylist.h@9208dcf:19	seed генератора	API списка воспроизведения	Хранит треки, мешок случайного порядка, историю и генератор Mersenne Twister
src/audio/MusicPlaylist.cpp	MusicPlaylist::MusicPlaylist	src/audio/MusicPlaylist.cpp@9208dcf:36	uint32_t seed	новый MusicPlaylist	Инициализирует генератор заданным seed
src/audio/MusicPlaylist.cpp	MusicPlaylist::setTracks	src/audio/MusicPlaylist.cpp@9208dcf:40	vector<MusicTrack>	void	Заменяет список треков и очищает мешок и историю
src/audio/MusicPlaylist.h	MusicPlaylist::empty	src/audio/MusicPlaylist.h@9208dcf:24	список треков	bool	Проверяет отсутствие треков
src/audio/MusicPlaylist.h	MusicPlaylist::size	src/audio/MusicPlaylist.h@9208dcf:25	список треков	std::size_t	Возвращает число треков
src/audio/MusicPlaylist.cpp	MusicPlaylist::refillBag	src/audio/MusicPlaylist.cpp@9208dcf:49	список треков, текущая история, генератор	void	Создаёт случайную перестановку индексов и переставляет крайние элементы, если следующий совпадает с последним сыгранным и треков больше одного
src/audio/MusicPlaylist.cpp	MusicPlaylist::next	src/audio/MusicPlaylist.cpp@9208dcf:62	список, история и мешок	const MusicTrack pointer или nullptr	Сначала проходит вперёд по имеющейся истории, затем извлекает следующий индекс из мешка и дописывает его в историю
src/audio/MusicPlaylist.cpp	MusicPlaylist::previous	src/audio/MusicPlaylist.cpp@9208dcf:84	история и позиция	const MusicTrack pointer или nullptr	Сдвигает позицию истории назад, если она больше нуля, и возвращает текущий трек
src/audio/MusicPlaylist.cpp	MusicPlaylist::current	src/audio/MusicPlaylist.cpp@9208dcf:95	история и позиция	const MusicTrack pointer или nullptr	Возвращает трек по текущей позиции после проверки границ
src/audio/MusicPlaylist.cpp	MusicPlaylist::discardCurrent	src/audio/MusicPlaylist.cpp@9208dcf:104	текущий трек и его key	void	Удаляет все треки с тем же key и очищает мешок и историю
src/audio/MusicPlaylist.cpp	MusicPlaylist::discoverExternalTracks	src/audio/MusicPlaylist.cpp@9208dcf:122	каталог	vector<MusicTrack>	Сканирует только обычные файлы верхнего уровня, оставляет поддерживаемые расширения и сортирует по ключу без учёта ASCII-регистра
src/audio/MusicPlaylist.cpp	MusicPlaylist::isSupportedMusicFile	src/audio/MusicPlaylist.cpp@9208dcf:144	путь файла	bool	Сравнивает расширение без учёта регистра с .ogg, .mp3, .wav и .flac
src/audio/MusicPlaylist.cpp	utf8String	src/audio/MusicPlaylist.cpp@9208dcf:8	filesystem::path	std::string	Преобразует UTF-8-представление пути в строку
src/audio/MusicPlaylist.cpp	lowerAscii	src/audio/MusicPlaylist.cpp@9208dcf:14	std::string	std::string	Переводит ASCII-символы строки в нижний регистр
src/audio/MusicTransitionPolicy.hpp	shouldAdvanceRepeatedMusicCategory	src/audio/MusicTransitionPolicy.hpp@9208dcf:3	повторная категория и playingState (не используется)	bool	Возвращает отрицание repeatedCategory
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout (struct)	src/sidebar/MusicControlsLayout.hpp@9208dcf:7	—	разметка панели	Хранит видимость и прямоугольники общей панели, музыки и скорости
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::visible	src/sidebar/MusicControlsLayout.hpp@9208dcf:8	—	bool, начальное значение false	Флаг видимости
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::panel	src/sidebar/MusicControlsLayout.hpp@9208dcf:9	—	cRectangle	Внешняя панель
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::musicPanel	src/sidebar/MusicControlsLayout.hpp@9208dcf:10	—	cRectangle	Панель музыки
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::previous	src/sidebar/MusicControlsLayout.hpp@9208dcf:11	—	cRectangle	Область кнопки предыдущего трека
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::label	src/sidebar/MusicControlsLayout.hpp@9208dcf:12	—	cRectangle	Область названия трека
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::next	src/sidebar/MusicControlsLayout.hpp@9208dcf:13	—	cRectangle	Область кнопки следующего трека
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::speedPanel	src/sidebar/MusicControlsLayout.hpp@9208dcf:14	—	cRectangle	Панель скорости
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::speedLabel	src/sidebar/MusicControlsLayout.hpp@9208dcf:15	—	cRectangle	Область подписи скорости
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::speedSlider	src/sidebar/MusicControlsLayout.hpp@9208dcf:16	—	cRectangle	Область слайдера скорости
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create	src/sidebar/MusicControlsLayout.hpp@9208dcf:18	левая и правая границы, зарезервированная ширина сообщения	MusicControlsLayout	Скрывает панель ниже минимума ширины, иначе вычисляет панели музыки и скорости с ограничением общей ширины
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create::MinimumWidth	src/sidebar/MusicControlsLayout.hpp@9208dcf:23	—	constexpr int 200	Минимальная ширина видимой панели
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create::MaximumWidth	src/sidebar/MusicControlsLayout.hpp@9208dcf:24	—	constexpr int 520	Максимальная ширина панели
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create::buttonSize	src/sidebar/MusicControlsLayout.hpp@9208dcf:34	—	constexpr int 33	Размер кнопок по ширине и высоте
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create::y	src/sidebar/MusicControlsLayout.hpp@9208dcf:35	—	constexpr int 4	Координата панели по вертикали
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::create::sectionGap	src/sidebar/MusicControlsLayout.hpp@9208dcf:37	—	constexpr int 8	Расстояние между секциями
src/sidebar/MusicControlsLayout.hpp	MusicControlsLayout::showsLabel	src/sidebar/MusicControlsLayout.hpp@9208dcf:61	ширина label	bool	Возвращает true при ширине подписи не менее 80 пикселей
src/audio/MusicController.h	MusicController::CategoryState::playlist	src/audio/MusicController.h@9208dcf:46	—	MusicPlaylist	Плейлист треков категории
src/audio/MusicController.h	MusicController::CategoryState::fallback	src/audio/MusicController.h@9208dcf:47	—	vector<MusicTrack>	Встроенный резервный список
src/audio/MusicController.h	MusicController::CategoryState::usingCustom	src/audio/MusicController.h@9208dcf:48	—	bool, начальное значение false	Флаг выбора пользовательского списка
src/audio/MusicController.h	MusicController::CategoryState::directory	src/audio/MusicController.h@9208dcf:49	—	filesystem::path	Путь папки пользовательского пула
src/audio/MusicController.h	MusicController::m_soundPlayer	src/audio/MusicController.h@9208dcf:58	—	cSoundPlayer pointer	Проигрыватель, управляемый контроллером
src/audio/MusicController.h	MusicController::m_gameDirectory	src/audio/MusicController.h@9208dcf:59	—	filesystem::path	Базовый каталог пользовательских папок музыки
src/audio/MusicController.h	MusicController::m_categories	src/audio/MusicController.h@9208dcf:60	—	array<CategoryState, MusicCategory::Count>	Состояние всех пулов
src/audio/MusicController.h	MusicController::m_activeCategory	src/audio/MusicController.h@9208dcf:61	—	MusicCategory, начальное значение Menu	Текущая категория
src/audio/MusicController.h	MusicController::m_hasActiveCategory	src/audio/MusicController.h@9208dcf:62	—	bool, начальное значение false	Флаг активной категории
src/audio/MusicPlaylist.h	MusicPlaylist::m_tracks	src/audio/MusicPlaylist.h@9208dcf:38	—	vector<MusicTrack>	Текущий список треков
src/audio/MusicPlaylist.h	MusicPlaylist::m_bag	src/audio/MusicPlaylist.h@9208dcf:39	—	vector<size_t>	Перестановка ещё не выбранных индексов
src/audio/MusicPlaylist.h	MusicPlaylist::m_history	src/audio/MusicPlaylist.h@9208dcf:40	—	vector<size_t>	Последовательность выбранных индексов
src/audio/MusicPlaylist.h	MusicPlaylist::m_historyPosition	src/audio/MusicPlaylist.h@9208dcf:41	—	size_t, начальное значение 0	Позиция текущего трека в истории
src/audio/MusicPlaylist.h	MusicPlaylist::m_hasHistoryPosition	src/audio/MusicPlaylist.h@9208dcf:42	—	bool, начальное значение false	Флаг валидной позиции в истории
src/audio/MusicPlaylist.h	MusicPlaylist::m_rng	src/audio/MusicPlaylist.h@9208dcf:43	—	std::mt19937	Генератор порядка треков
```

### `resources.tsv`

```tsv
путь	статус	размер объекта Git	Git LFS	размер содержимого Git LFS	есть в PORT	объект совпадает	категория
resources/bin/music/briefing/atreides/18_MENTAT_ATR.wav	A	133	да	21243052	нет	-	BriefingAtreides
resources/bin/music/briefing/harkonnen/19_MENTAT_HAR.wav	A	133	да	41164972	нет	-	BriefingHarkonnen
resources/bin/music/briefing/ordos/20_MENTAT_ORD.wav	A	133	да	27817132	нет	-	BriefingOrdos
resources/bin/music/conquest/22_SCENARIO.wav	A	133	да	25252012	нет	-	Conquest
resources/bin/music/defeat/15_LOSE1.wav	A	133	да	27417772	нет	-	Defeat
resources/bin/music/defeat/16_LOSE2.wav	A	133	да	20751532	нет	-	Defeat
resources/bin/music/defeat/17_LOSE3.wav	A	133	да	24484012	нет	-	Defeat
resources/bin/music/gameplay/Track 1.wav	A	133	да	14876332	нет	-	Gameplay
resources/bin/music/gameplay/Track 10.wav	A	133	да	17740972	нет	-	Gameplay
resources/bin/music/gameplay/Track 11.wav	A	133	да	11474092	нет	-	Gameplay
resources/bin/music/gameplay/Track 2.wav	A	133	да	28600492	нет	-	Gameplay
resources/bin/music/gameplay/Track 3.wav	A	133	да	27625132	нет	-	Gameplay
resources/bin/music/gameplay/Track 4.wav	A	133	да	25866412	нет	-	Gameplay
resources/bin/music/gameplay/Track 5.wav	A	133	да	28723372	нет	-	Gameplay
resources/bin/music/gameplay/Track 6.wav	A	133	да	30213292	нет	-	Gameplay
resources/bin/music/gameplay/Track 7.wav	A	133	да	31541932	нет	-	Gameplay
resources/bin/music/gameplay/Track 8 .wav	A	133	да	24553132	нет	-	Gameplay
resources/bin/music/gameplay/Track 9.wav	A	133	да	36787372	нет	-	Gameplay
resources/bin/music/menu/21_MENU.wav	A	133	да	19138732	нет	-	Menu
resources/bin/music/victory/23_WIN01.wav	A	133	да	16949932	нет	-	Victory
resources/bin/music/victory/24_WIN02.wav	A	133	да	14361772	нет	-	Victory
resources/bin/music/victory/25_WIN03.wav	A	133	да	16251052	нет	-	Victory
```

### `fork-hooks.tsv`

```tsv
путь в FORK1	путь@9208dcf:строка	что добавляет участок одной строкой	путь в PORT	соответствие
CMakeLists.txt	CMakeLists.txt@9208dcf:397	Добавляет три executable и регистрации CTest для playlist, transition policy и controls layout (регистрации: CMakeLists.txt@9208dcf:407, CMakeLists.txt@9208dcf:418, CMakeLists.txt@9208dcf:431).	CMakeLists.txt	нет: релевантных music-тестов и регистраций по поиску в CMakeLists.txt, src/CMakeLists.txt и tests нет.
src/cGame.h	src/cGame.h@9208dcf:46	Объявляет MusicController для указателя в cGame.	src/game/cGame.h	нет для MusicController; в поле аудиозависимости стоит AudioContext (src/game/cGame.h@616280c:196).
src/cGame.h	src/cGame.h@9208dcf:158	Объявляет методы переключения на предыдущий/следующий игровой трек и чтения названия текущего трека.	src/game/cGame.h	нет: методы playPreviousGameplayTrack, playNextGameplayTrack и getCurrentMusicTrackName отсутствуют.
src/cGame.h	src/cGame.h@9208dcf:333	Добавляет поле-владельца std::unique_ptr<MusicController>.	src/game/cGame.h	нет для MusicController; аудиоконтекст хранится в m_audioContext (src/game/cGame.h@616280c:196).
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:14	Подключает MusicController и политику повторного входа в музыкальную категорию.	src/game/cGame_logic.cpp	этих заголовков нет; музыкальная логика вынесена в AudioContext, например src/context/AudioContext.cpp@616280c:92.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:96	Добавляет musicCategoryFor: переводит тип музыки и дом в MusicCategory, включая отдельные пулы для трёх домов в брифинге.	src/context/MusicJukeBox.cpp	нет функции MusicCategory; порт сопоставляет eMusicType каталогам в repertoryDir, src/context/MusicJukeBox.cpp@616280c:37, src/context/MusicJukeBox.cpp@616280c:42, src/context/MusicJukeBox.cpp@616280c:46, src/context/MusicJukeBox.cpp@616280c:48.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:568	Заменяет countdown-цикл think_audio на MusicController::update.	src/context/AudioContext.cpp	похожее место: AudioContext::thinkFast, src/context/AudioContext.cpp@616280c:183 и src/context/AudioContext.cpp@616280c:203; вызов из игры — src/game/cGame_logic.cpp@616280c:517.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:1116	Создаёт восемь каталогов музыки у исполняемого файла и конфигурирует MusicController встроенными MIDI fallback-наборами.	src/context/MusicJukeBox.cpp	похожее создание репертуарных папок и выбор файла: MusicJukeBox.cpp@616280c:76, MusicJukeBox.cpp@616280c:79, MusicJukeBox.cpp@616280c:90, MusicJukeBox.cpp@616280c:102, MusicJukeBox.cpp@616280c:109; каталог по умолчанию объявлен в src/context/MusicJukeBox.hpp@616280c:30.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:1444	Добавляет вызов перехода к MUSIC_PEACE в обработчике смены игрового состояния.	src/game/cGame_logic.cpp	переходы продолжают вызывать playMusicByTypeForStateTransition, например src/game/cGame_logic.cpp@616280c:871; реализация обёртки в src/game/cGame_logic.cpp@616280c:1578.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2094	При клавише M/MUTE обновляет также флаг MusicEnabled в звуковом проигрывателе.	src/game/cGame_logic.cpp	есть переключение через eKeyAction::TOGGLE_MUSIC и AudioContext::toggleMusic, src/game/cGame_logic.cpp@616280c:1523, 1524.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2096	При выключении останавливает музыку через контроллер и показывает локализованное уведомление.	src/context/AudioContext.cpp	есть toggleMusic/setMusicEnabled, src/context/AudioContext.cpp@616280c:219, src/context/AudioContext.cpp@616280c:224, src/context/AudioContext.cpp@616280c:227; отдельного метода stop у контроллера нет.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2100	При включении повторно запускает текущую композицию и показывает локализованное уведомление.	src/context/AudioContext.cpp	нет replayCurrent; setMusicEnabled ставит countdown для последующего запуска, src/context/AudioContext.cpp@616280c:224, src/context/AudioContext.cpp@616280c:230.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2105	Добавляет обработчики клавиш [ и ] для предыдущего и следующего трека игрового пула.	src/game/cGame_logic.cpp	нет этих обработчиков или методов переключения по треку.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2217	Убирает условие по текущему типу перед переходным вызовом playMusicByType.	src/game/cGame_logic.cpp	обёртка перехода остаётся, src/game/cGame_logic.cpp@616280c:1578; у AudioContext собственная проверка MusicType находится в src/context/AudioContext.cpp@616280c:84, src/context/AudioContext.cpp@616280c:86 и src/context/AudioContext.cpp@616280c:88.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2229	Сворачивает MUSIC_ATTACK в MUSIC_PEACE и перестаёт использовать triggerWithVoice для владения состоянием атаки.	src/context/AudioContext.cpp	нет: порт выбирает отдельный ATTACK sample и каталог (src/context/AudioContext.cpp@616280c:122, src/context/AudioContext.cpp@616280c:123; src/context/MusicJukeBox.cpp@616280c:42).
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2234	Фиксирует повторность музыкального типа перед его обновлением.	src/context/AudioContext.cpp	похожее сравнение MusicType только для triggerWithVoice находится в src/context/AudioContext.cpp@616280c:96, src/context/AudioContext.cpp@616280c:97 и src/context/AudioContext.cpp@616280c:103.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2242	Активирует пул категории через MusicController и shouldAdvanceRepeatedMusicCategory.	src/context/AudioContext.cpp	нет такой политики; выбор старого типа и файла выполняют src/context/AudioContext.cpp@616280c:92, src/context/AudioContext.cpp@616280c:115, src/context/AudioContext.cpp@616280c:170, MusicJukeBox.cpp@616280c:90, MusicJukeBox.cpp@616280c:102 и MusicJukeBox.cpp@616280c:109.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2256	Добавляет playPreviousGameplayTrack, доступный только при включённой музыке в игровом состоянии.	src/game/cGame_logic.cpp	нет метода и вызова переключения предыдущего трека.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2263	Добавляет playNextGameplayTrack с теми же ограничениями для следующего трека.	src/game/cGame_logic.cpp	нет метода и вызова переключения следующего трека.
src/cGame_logic.cpp	src/cGame_logic.cpp@9208dcf:2270	Добавляет доступ к display name текущего трека для HUD.	src/game/cGame_logic.cpp	нет метода getCurrentMusicTrackName и названия трека для HUD.
src/drawers/cMessageDrawer.cpp	src/drawers/cMessageDrawer.cpp@9208dcf:6	Подключает расчёт геометрии MusicControlsLayout.	src/drawers/cMessageDrawer.cpp	нет: MusicControlsLayout не найден в исходниках порта.
src/drawers/cMessageDrawer.cpp	src/drawers/cMessageDrawer.cpp@9208dcf:42	В боевом сообщении размещает MusicControlsLayout и резервирует справа место для текста уведомления.	src/drawers/cMessageDrawer.cpp	нет: аналогичного размещения музыкального управления в этом файле нет.
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:13	Подключает MusicControlsLayout для верхней панели.	src/managers/cDrawManager.cpp	нет: MusicControlsLayout не найден в исходниках порта.
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:89	Вызывает drawTopBarMusicControls при отрисовке боевого состояния.	src/managers/cDrawManager.cpp	нет: вызова музыкальной панели в drawCombatState нет.
src/managers/cDrawManager.cpp	src/managers/cDrawManager.cpp@9208dcf:288	Добавляет кнопки предыдущего/следующего трека, название композиции и слайдер скорости игры в верхней панели.	src/managers/cDrawManager.cpp	нет: drawTopBarMusicControls, drawMusicControls и игровые кнопки переключения треков отсутствуют.
src/managers/cDrawManager.h	src/managers/cDrawManager.h@9208dcf:105	Объявляет drawTopBarMusicControls и drawMusicControls.	src/managers/cDrawManager.h	нет: эти методы в заголовке порта отсутствуют.
src/player/cPlayer.cpp	src/player/cPlayer.cpp@9208dcf:1880	Удаляет ранний выход, привязанный к MUSIC_PEACE, из обработки обнаружения врага.	src/gameobjects/players/cPlayer.cpp	старый MUSIC_PEACE guard остаётся в src/gameobjects/players/cPlayer.cpp@616280c:2067.
src/player/cPlayer.cpp	src/player/cPlayer.cpp@9208dcf:1884	Удаляет состояние triggerMusic и зависимость предупреждающей реплики от музыкального режима.	src/gameobjects/players/cPlayer.cpp	старый triggerMusic остаётся в src/gameobjects/players/cPlayer.cpp@616280c:2077.
src/player/cPlayer.cpp	src/player/cPlayer.cpp@9208dcf:1892	Перестаёт помечать обнаружение вражеского юнита как triggerMusic.	src/gameobjects/players/cPlayer.cpp	старый triggerMusic при обнаружении юнита остаётся в src/gameobjects/players/cPlayer.cpp@616280c:2086.
src/player/cPlayer.cpp	src/player/cPlayer.cpp@9208dcf:1916	Убирает triggerMusic для вражеской турели, оставляя без отдельного warning voice.	src/gameobjects/players/cPlayer.cpp	старое присваивание triggerMusic для турели остаётся в src/gameobjects/players/cPlayer.cpp@616280c:2110.
src/player/cPlayer.cpp	src/player/cPlayer.cpp@9208dcf:1926	Заменяет переключение в MUSIC_ATTACK управлением предупреждающими репликами с cooldown 30 секунд.	src/gameobjects/players/cPlayer.cpp	старое условие и вызов AudioContext::playMusicByType(ATTACK) остаются в src/gameobjects/players/cPlayer.cpp@616280c:2120, src/gameobjects/players/cPlayer.cpp@616280c:2123, src/gameobjects/players/cPlayer.cpp@616280c:2126, src/gameobjects/players/cPlayer.cpp@616280c:2133.
src/utils/cSoundPlayer.cpp	src/utils/cSoundPlayer.cpp@9208dcf:62	Запрашивает FLAC/MP3/OGG decoder codecs через Mix_Init и записывает предупреждение при неполном наборе.	src/utils/cSoundPlayer.cpp	отдельного decoder-init нет; SDL3 mixer и музыкальный MIX_Track создаются в src/utils/cSoundPlayer.cpp@616280c:67, src/utils/cSoundPlayer.cpp@616280c:77, src/utils/cSoundPlayer.cpp@616280c:78.
src/utils/cSoundPlayer.cpp	src/utils/cSoundPlayer.cpp@9208dcf:104	При разрушении проигрывателя останавливает музыку, освобождает внешний трек и вызывает Mix_Quit.	src/utils/cSoundPlayer.cpp	похожее освобождение в destructor: остановка MIX_Track и releaseMusicFile, src/utils/cSoundPlayer.cpp@616280c:105, 111, 114.
src/utils/cSoundPlayer.cpp	src/utils/cSoundPlayer.cpp@9208dcf:156	Перед встроенным треком останавливает текущую музыку и освобождает внешний файл.	src/utils/cSoundPlayer.cpp	похожее переключение в playMusic/startMusic и releaseMusicFile, src/utils/cSoundPlayer.cpp@616280c:177, 189, 190, 214, 222.
src/utils/cSoundPlayer.cpp	src/utils/cSoundPlayer.cpp@9208dcf:161	Добавляет загрузку внешнего music файла из filesystem path, UTF-8 имени, обработку ошибок и запуск без зацикливания.	src/utils/cSoundPlayer.cpp	есть playMusicFile(std::string), читающий SDL_IOStream/MIX_Audio и запускающий track, src/utils/cSoundPlayer.cpp@616280c:193, 198, 203, 208; сигнатура другая.
src/utils/cSoundPlayer.cpp	src/utils/cSoundPlayer.cpp@9208dcf:198	Добавляет освобождение внешнего Mix_Music через releaseExternalMusic.	src/utils/cSoundPlayer.cpp	похожий releaseMusicFile освобождает MIX_Audio, src/utils/cSoundPlayer.cpp@616280c:222, 224, 225.
src/utils/cSoundPlayer.h	src/utils/cSoundPlayer.h@9208dcf:24	Добавляет публичный метод загрузки внешней музыки по filesystem path с выходной строкой ошибки.	src/utils/cSoundPlayer.h	есть playMusicFile(const std::string &path), src/utils/cSoundPlayer.h@616280c:40; интерфейс другой.
src/utils/cSoundPlayer.h	src/utils/cSoundPlayer.h@9208dcf:55	Добавляет состояние Mix decoder init, raw external music handle и приватный cleanup.	src/utils/cSoundPlayer.h	похожие владельцы SDL3 Audio и музыкального трека — src/utils/cSoundPlayer.h@616280c:71, src/utils/cSoundPlayer.h@616280c:72, src/utils/cSoundPlayer.h@616280c:75, src/utils/cSoundPlayer.h@616280c:76, src/utils/cSoundPlayer.h@616280c:77; releaseMusicFile: строка 72.
```

### `port-music.tsv`

```tsv
ревизия	путь	символ или папка	путь@ревизия:строка	что делает одной строкой
PORT	src/include/definitions.h	enum class eMusicType	src/include/definitions.h@616280c:158	Объявляет WIN, LOSE, ATTACK, PEACE, MENU, CONQUEST и BRIEFING.
PORT	src/context/AudioContext.cpp	musicTypeName	src/context/AudioContext.cpp@616280c:30	Возвращает строковое имя музыкального типа для журнала.
PORT	src/context/AudioContext.cpp	AudioContext::AudioContext	src/context/AudioContext.cpp@616280c:45	Создаёт MusicJukeBox и заполняет десять пользовательских музыкальных каталогов.
PORT	src/context/AudioContext.cpp	AudioContext::playMusicByTypeForStateTransition	src/context/AudioContext.cpp@616280c:84	Запускает тип музыки при переходе, только когда тип отличается от текущего.
PORT	src/context/AudioContext.cpp	AudioContext::playMusicByType	src/context/AudioContext.cpp@616280c:92	Выбирает встроенный архивный трек по типу и дому, затем просит MusicJukeBox выбрать пользовательский файл.
PORT	src/context/AudioContext.cpp	AudioContext::startMusic	src/context/AudioContext.cpp@616280c:175	Проигрывает выбранный файл, а при его отсутствии или ошибке — встроенный архивный трек.
PORT	src/context/AudioContext.cpp	AudioContext::thinkFast	src/context/AudioContext.cpp@616280c:183	Начинает отложенный трек и повторяет завершившуюся музыку; ATTACK возвращает к PEACE, BRIEFING повторяет сохранённый выбор.
PORT	src/context/AudioContext.cpp	AudioContext::toggleMusic	src/context/AudioContext.cpp@616280c:219	Инвертирует настройку музыки и передаёт новое состояние проигрывателю.
PORT	src/context/AudioContext.cpp	AudioContext::setMusicEnabled	src/context/AudioContext.cpp@616280c:224	Сохраняет состояние музыки и разрешает thinkFast начать текущую категорию после включения.
PORT	src/context/AudioContext.cpp	AudioContext::changeMusicVolume	src/context/AudioContext.cpp@616280c:234	Передаёт изменение громкости музыки проигрывателю.
PORT	src/context/AudioContext.cpp	eMusicType::WIN	src/context/AudioContext.cpp@616280c:116	Для победы выбирает MIDI_WIN01 плюс случайное смещение 0–2.
PORT	src/context/AudioContext.cpp	eMusicType::LOSE	src/context/AudioContext.cpp@616280c:119	Для поражения выбирает MIDI_LOSE01 плюс случайное смещение 0–5.
PORT	src/context/AudioContext.cpp	eMusicType::ATTACK	src/context/AudioContext.cpp@616280c:122	Для атаки выбирает MIDI_ATTACK01 плюс случайное смещение 0–5.
PORT	src/context/AudioContext.cpp	eMusicType::PEACE	src/context/AudioContext.cpp@616280c:125	Для мирного состояния выбирает MIDI_BUILDING01 плюс случайное смещение 0–8.
PORT	src/context/AudioContext.cpp	eMusicType::MENU	src/context/AudioContext.cpp@616280c:128	Для меню выбирает MIDI_MENU.
PORT	src/context/AudioContext.cpp	eMusicType::CONQUEST	src/context/AudioContext.cpp@616280c:131	Для завоевания выбирает MIDI_SCENARIO.
PORT	src/context/AudioContext.cpp	eMusicType::BRIEFING	src/context/AudioContext.cpp@616280c:134	Для брифинга выбирает MIDI_MENTAT по дому; для Sardaukar использует MIDI_MENTAT_HAR.
PORT	src/context/AudioContext.cpp	MusicChoice selection	src/context/AudioContext.cpp@616280c:171	Передаёт настройку пользовательской музыки и получает выбранный файл/архивный fallback.
PORT	src/context/AudioContext.cpp	MusicChoice repeat	src/context/AudioContext.cpp@616280c:209	Для BRIEFING повторяет сохранённый выбор; для ATTACK тип переключается на PEACE в строках 205–207.
PORT	src/context/MusicChoice.hpp	struct MusicChoice	src/context/MusicChoice.hpp@616280c:23	Хранит обязательный архивный fallback и необязательный путь выбранного файла.
PORT	src/context/MusicJukeBox.cpp	isAudioFile	src/context/MusicJukeBox.cpp@616280c:27	Принимает расширения .ogg, .mp3, .wav и .flac без учёта регистра.
PORT	src/context/MusicJukeBox.cpp	repertoryDir	src/context/MusicJukeBox.cpp@616280c:37	Сопоставляет тип музыки пользовательскому каталогу, а BRIEFING — подкаталогу дома.
PORT	src/context/MusicJukeBox.cpp	listAudioFiles	src/context/MusicJukeBox.cpp@616280c:58	Перебирает непосредственные файлы каталога и оставляет поддерживаемые аудиофайлы.
PORT	src/context/MusicJukeBox.cpp	MusicJukeBox::MusicJukeBox	src/context/MusicJukeBox.cpp@616280c:71	Сохраняет корневой путь пользовательских каталогов, по умолчанию audio.
PORT	src/context/MusicJukeBox.cpp	MusicJukeBox::createRepertoryDirectories	src/context/MusicJukeBox.cpp@616280c:76	Создаёт каталоги win, lose, attack, peace, menu, conquest и четыре каталога briefing.
PORT	src/context/MusicJukeBox.cpp	MusicJukeBox::setCustomMusicEnabled	src/context/MusicJukeBox.cpp@616280c:85	Включает или выключает выбор пользовательского файла.
PORT	src/context/MusicJukeBox.cpp	MusicJukeBox::choose	src/context/MusicJukeBox.cpp@616280c:90	При включённой функции сортирует найденные файлы и выбирает один через RNG; иначе оставляет архивный fallback.
PORT	src/context/MusicJukeBox.cpp	audio/win	src/context/MusicJukeBox.cpp@616280c:40	Пользовательская папка для WIN; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/lose	src/context/MusicJukeBox.cpp@616280c:41	Пользовательская папка для LOSE; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/attack	src/context/MusicJukeBox.cpp@616280c:42	Пользовательская папка для ATTACK; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/peace	src/context/MusicJukeBox.cpp@616280c:43	Пользовательская папка для PEACE; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/menu	src/context/MusicJukeBox.cpp@616280c:44	Пользовательская папка для MENU; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/conquest	src/context/MusicJukeBox.cpp@616280c:45	Пользовательская папка для CONQUEST; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/briefing/atreides	src/context/MusicJukeBox.cpp@616280c:48	Пользовательская папка для BRIEFING дома Atreides; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/briefing/harkonnen	src/context/MusicJukeBox.cpp@616280c:49	Пользовательская папка для BRIEFING дома Harkonnen; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/briefing/ordos	src/context/MusicJukeBox.cpp@616280c:50	Пользовательская папка для BRIEFING дома Ordos; в дереве репозитория файлов нет.
PORT	src/context/MusicJukeBox.cpp	audio/briefing/sardaukar	src/context/MusicJukeBox.cpp@616280c:51	Пользовательская папка для BRIEFING дома Sardaukar; в дереве репозитория файлов нет.
PORT	src/game/cGame_logic.cpp	WIN activation	src/game/cGame_logic.cpp@616280c:485	Включает WIN при успешном завершении миссии.
PORT	src/game/cGame_logic.cpp	LOSE activation	src/game/cGame_logic.cpp@616280c:508	Включает LOSE при поражении в миссии.
PORT	src/game/cGame_logic.cpp	MENU activation	src/game/cGame_logic.cpp@616280c:871	Включает MENU при начальной настройке игры.
PORT	src/game/cGame_logic.cpp	CONQUEST activation	src/game/cGame_logic.cpp@616280c:1049	Включает CONQUEST при повторном входе в существующее состояние карты региона.
PORT	src/game/cGame_logic.cpp	CONQUEST activation	src/game/cGame_logic.cpp@616280c:1122	Включает CONQUEST при первичной настройке кампании.
PORT	src/game/cGame_logic.cpp	MENU activation	src/game/cGame_logic.cpp@616280c:1129	Включает MENU при переходе к настройке Skirmish.
PORT	src/game/cGame_logic.cpp	MENU activation	src/game/cGame_logic.cpp@616280c:1143	Включает MENU при переходе в главное меню.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1200	Включает BRIEFING при переходе к сообщению о доме.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1205	Включает BRIEFING при переходе к брифингу.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1208	Включает BRIEFING при переходе к экрану победного брифинга.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1212	Включает BRIEFING с сохранённым домом кампании на экране поражения.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1270	Включает BRIEFING при подготовке нового состояния сообщения о доме.
PORT	src/game/cGame_logic.cpp	PEACE activation	src/game/cGame_logic.cpp@616280c:1309	Включает PEACE при запуске мирного игрового состояния.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1358	Включает BRIEFING после провала первой миссии.
PORT	src/game/cGame_logic.cpp	BRIEFING activation	src/game/cGame_logic.cpp@616280c:1485	Включает BRIEFING при переходе к состоянию брифинга.
PORT	src/game/cGame_logic.cpp	cGame::playMusicByTypeForStateTransition	src/game/cGame_logic.cpp@616280c:1578	Передаёт тип перехода и дом игрока в AudioContext.
PORT	src/game/cGame_logic.cpp	cGame::playMusicByType	src/game/cGame_logic.cpp@616280c:1583	Передаёт тип, флаг голосового события, признак игровой миссии и дом игрока в AudioContext.
PORT	src/gameobjects/players/cPlayer.cpp	PEACE-to-ATTACK decision	src/gameobjects/players/cPlayer.cpp@616280c:2067	Обрабатывает обнаружение противника только если текущая музыкальная категория PEACE.
PORT	src/gameobjects/players/cPlayer.cpp	ATTACK activation	src/gameobjects/players/cPlayer.cpp@616280c:2126	При атаке включает ATTACK; для человеческого игрока может задержать голосовое сообщение.
UP1	src/gamestates/cSelectYourNextConquestState.cpp	BRIEFING activation	src/gamestates/cSelectYourNextConquestState.cpp@d06f2fc:464	Включает BRIEFING при выборе следующего завоевания.
UP1	src/gamestates/cSetupSkirmishState.cpp	PEACE activation	src/gamestates/cSetupSkirmishState.cpp@d06f2fc:975	Включает PEACE после настройки Skirmish.
PORT	src/game/cSDLSystem.cpp	MIX_Quit	src/game/cSDLSystem.cpp@616280c:236	Завершает SDL3_mixer.
PORT	src/game/cSDLSystem.cpp	MIX_Init	src/game/cSDLSystem.cpp@616280c:269	Инициализирует SDL3_mixer.
PORT	src/game/cSDLSystem.cpp	MIX_GetNumAudioDecoders	src/game/cSDLSystem.cpp@616280c:275	Возвращает число доступных аудиодекодеров для журнала.
PORT	src/game/cSDLSystem.cpp	MIX_GetAudioDecoder	src/game/cSDLSystem.cpp@616280c:276	Возвращает имя очередного декодера для журнала.
PORT	src/utils/cDataPack.cpp	MIX_DestroyAudio	src/utils/cDataPack.cpp@616280c:37	Освобождает загруженный архивный аудиообъект.
PORT	src/utils/cDataPack.cpp	MIX_LoadAudioWithProperties	src/utils/cDataPack.cpp@616280c:101	Загружает аудио из архива в SDL3_mixer.
PORT	src/utils/cSoundPlayer.cpp	MIX_CreateMixerDevice	src/utils/cSoundPlayer.cpp@616280c:67	Создаёт микшер для устройства воспроизведения по умолчанию.
PORT	src/utils/cSoundPlayer.cpp	MIX_CreateTrack (music)	src/utils/cSoundPlayer.cpp@616280c:77	Создаёт отдельную дорожку музыки.
PORT	src/utils/cSoundPlayer.cpp	MIX_CreateTrack (SFX)	src/utils/cSoundPlayer.cpp@616280c:79	Создаёт пул дорожек для звуковых эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetMixerGain	src/utils/cSoundPlayer.cpp@616280c:95	Устанавливает общий уровень микшера.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackGain (SFX)	src/utils/cSoundPlayer.cpp@616280c:98	Устанавливает усиление дорожек звуковых эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackGain (music)	src/utils/cSoundPlayer.cpp@616280c:101	Устанавливает усиление дорожки музыки.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (music destructor)	src/utils/cSoundPlayer.cpp@616280c:111	Останавливает музыкальную дорожку при уничтожении проигрывателя.
PORT	src/utils/cSoundPlayer.cpp	MIX_DestroyTrack (music)	src/utils/cSoundPlayer.cpp@616280c:112	Уничтожает музыкальную дорожку.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (SFX destructor)	src/utils/cSoundPlayer.cpp@616280c:116	Останавливает каждую дорожку звуковых эффектов при уничтожении проигрывателя.
PORT	src/utils/cSoundPlayer.cpp	MIX_DestroyTrack (SFX)	src/utils/cSoundPlayer.cpp@616280c:117	Уничтожает каждую дорожку звуковых эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_DestroyMixer	src/utils/cSoundPlayer.cpp@616280c:120	Уничтожает микшер после дорожек.
PORT	src/utils/cSoundPlayer.cpp	MIX_TrackPlaying (SFX)	src/utils/cSoundPlayer.cpp@616280c:150	Собирает занятость дорожек звуковых эффектов перед повторным использованием.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (SFX fade)	src/utils/cSoundPlayer.cpp@616280c:156	Останавливает вытесняемую дорожку с коротким затуханием.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackAudio (SFX)	src/utils/cSoundPlayer.cpp@616280c:157	Привязывает звуковой объект к выбранной дорожке эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_PlayTrack (SFX)	src/utils/cSoundPlayer.cpp@616280c:158	Запускает выбранный звук на дорожке эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_LoadAudio_IO	src/utils/cSoundPlayer.cpp@616280c:203	Загружает пользовательский музыкальный файл из SDL_IOStream.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (music start)	src/utils/cSoundPlayer.cpp@616280c:216	Останавливает прежний музыкальный трек перед заменой.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackAudio (music)	src/utils/cSoundPlayer.cpp@616280c:217	Назначает аудиообъект музыкальной дорожке.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackLoops	src/utils/cSoundPlayer.cpp@616280c:218	Выключает повторы на дорожке; повтором управляет AudioContext.
PORT	src/utils/cSoundPlayer.cpp	MIX_PlayTrack (music)	src/utils/cSoundPlayer.cpp@616280c:219	Запускает музыку на дорожке.
PORT	src/utils/cSoundPlayer.cpp	MIX_DestroyAudio (custom file)	src/utils/cSoundPlayer.cpp@616280c:225	Освобождает ранее загруженный пользовательский файл.
PORT	src/utils/cSoundPlayer.cpp	MIX_TrackPlaying (music)	src/utils/cSoundPlayer.cpp@616280c:235	Проверяет, проигрывается ли музыка.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (music stop)	src/utils/cSoundPlayer.cpp@616280c:241	Останавливает музыку.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackGain (music volume)	src/utils/cSoundPlayer.cpp@616280c:250	Задаёт усиление музыкальной дорожки при изменении громкости.
PORT	src/utils/cSoundPlayer.cpp	MIX_SetTrackGain (SFX volume)	src/utils/cSoundPlayer.cpp@616280c:265	Задаёт усиление дорожек эффектов при изменении громкости эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopAllTracks	src/utils/cSoundPlayer.cpp@616280c:273	Останавливает все дорожки при отключении звуковых эффектов.
PORT	src/utils/cSoundPlayer.cpp	MIX_StopTrack (music disable)	src/utils/cSoundPlayer.cpp@616280c:281	Останавливает музыку при её отключении.
```

### `tests.tsv`

```tsv
файл	проверка и путь@9208dcf:строка	что проверяет	используемые символы и заголовки	есть ли каждый в PORT	читаемые файлы
tests/MusicPlaylistTests.cpp	assert: track != nullptr; tests/MusicPlaylistTests.cpp@9208dcf:30	Каждый из пяти вызовов next() в первом цикле возвращает трек.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: firstCycle.size() == 5U; tests/MusicPlaylistTests.cpp@9208dcf:33	Первый цикл содержит пять разных ключей треков.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: firstOfNextCycle != nullptr; tests/MusicPlaylistTests.cpp@9208dcf:37	После исчерпания первого мешка следующий цикл выдаёт трек.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: firstOfNextCycle->key() != lastOfCycle; tests/MusicPlaylistTests.cpp@9208dcf:38	Первый трек следующего цикла не повторяет последний трек предыдущего.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: previous != nullptr; tests/MusicPlaylistTests.cpp@9208dcf:42	Предыдущий элемент истории доступен после первого элемента следующего цикла.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: previous->key() == lastOfCycle; tests/MusicPlaylistTests.cpp@9208dcf:43	Переход назад возвращает последний трек первого цикла.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: forwardFromHistory != nullptr; tests/MusicPlaylistTests.cpp@9208dcf:45	Переход вперёд по существующей истории возвращает трек.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: forwardFromHistory->key() == current; tests/MusicPlaylistTests.cpp@9208dcf:46	Переход вперёд после previous возвращает зафиксированный текущий трек.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: discovered.size() == 4U; tests/MusicPlaylistTests.cpp@9208dcf:58	Из пяти файлов fixture обнаруживаются четыре поддерживаемых аудиофайла.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: discovered[0] == alpha.mp3; tests/MusicPlaylistTests.cpp@9208dcf:59	Список внешних треков отсортирован так, что alpha.mp3 идёт первым.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: discovered[1] == track.wav; tests/MusicPlaylistTests.cpp@9208dcf:60	Вторым после сортировки идёт track.wav.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: discovered[2] == zeta.OGG; tests/MusicPlaylistTests.cpp@9208dcf:61	Третьим после сортировки идёт zeta.OGG; расширение распознано без учёта регистра.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert std::any_of(... unicodeFile.filename()); tests/MusicPlaylistTests.cpp@9208dcf:62	В списке сохраняется файл с кириллическим именем пустыня.flac.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: isSupportedMusicFile(theme.FLAC); tests/MusicPlaylistTests.cpp@9208dcf:65	Расширение FLAC принимается без учёта регистра.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicPlaylistTests.cpp	assert: !isSupportedMusicFile(notes.txt); tests/MusicPlaylistTests.cpp@9208dcf:66	Файл с расширением txt не считается музыкальным.	MusicPlaylist, MusicTrack; audio/MusicPlaylist.h	нет: тест, MusicPlaylist, MusicTrack и заголовок отсутствуют в PORT	для checks строк 30–46: нет; для discovery checks — entries fixture, созданного на tests/MusicPlaylistTests.cpp@9208dcf:48, tests/MusicPlaylistTests.cpp@9208dcf:52 и tests/MusicPlaylistTests.cpp@9208dcf:55, каталог перечисляется на tests/MusicPlaylistTests.cpp@9208dcf:57; содержимое файлов не читается
tests/MusicControlsLayoutTests.cpp	if layout geometry; tests/MusicControlsLayoutTests.cpp@9208dcf:14	В трёх размерах окна проверяются видимость, максимальная ширина, неперекрытие кнопок, граница battlefield и высота верхней панели. Размеры заданы в tests/MusicControlsLayoutTests.cpp@9208dcf:49, tests/MusicControlsLayoutTests.cpp@9208dcf:50 и tests/MusicControlsLayoutTests.cpp@9208dcf:51.	HudLayout, MusicControlsLayout, cRectangle; sidebar/HudLayout.hpp, sidebar/MusicControlsLayout.hpp	HudLayout и MusicControlsLayout отсутствуют; cRectangle есть: src/utils/cRectangle.h@616280c:21, src/utils/cRectangle.h@616280c:26, src/utils/cRectangle.h@616280c:37, src/utils/cRectangle.h@616280c:39, src/utils/cRectangle.h@616280c:54, src/utils/cRectangle.h@616280c:60, src/utils/cRectangle.h@616280c:63, src/utils/cRectangle.h@616280c:66; заголовки layout отсутствуют	нет: тест проверяет вычисления в памяти
tests/MusicControlsLayoutTests.cpp	if message overlap; tests/MusicControlsLayoutTests.cpp@9208dcf:27	Непустая область уведомления не пересекается с панелью музыки. Размеры заданы в tests/MusicControlsLayoutTests.cpp@9208dcf:49, tests/MusicControlsLayoutTests.cpp@9208dcf:50 и tests/MusicControlsLayoutTests.cpp@9208dcf:51.	HudLayout, MusicControlsLayout, cRectangle; sidebar/HudLayout.hpp, sidebar/MusicControlsLayout.hpp	HudLayout и MusicControlsLayout отсутствуют; cRectangle есть: src/utils/cRectangle.h@616280c:21, src/utils/cRectangle.h@616280c:26, src/utils/cRectangle.h@616280c:37, src/utils/cRectangle.h@616280c:39, src/utils/cRectangle.h@616280c:54, src/utils/cRectangle.h@616280c:60, src/utils/cRectangle.h@616280c:63, src/utils/cRectangle.h@616280c:66; заголовки layout отсутствуют	нет: тест проверяет вычисления в памяти
tests/MusicControlsLayoutTests.cpp	if label overlaps buttons; tests/MusicControlsLayoutTests.cpp@9208dcf:31	Если подпись видна, она не пересекается с кнопками назад и вперёд. Размеры заданы в tests/MusicControlsLayoutTests.cpp@9208dcf:49, tests/MusicControlsLayoutTests.cpp@9208dcf:50 и tests/MusicControlsLayoutTests.cpp@9208dcf:51.	HudLayout, MusicControlsLayout, cRectangle; sidebar/HudLayout.hpp, sidebar/MusicControlsLayout.hpp	HudLayout и MusicControlsLayout отсутствуют; cRectangle есть: src/utils/cRectangle.h@616280c:21, src/utils/cRectangle.h@616280c:26, src/utils/cRectangle.h@616280c:37, src/utils/cRectangle.h@616280c:39, src/utils/cRectangle.h@616280c:54, src/utils/cRectangle.h@616280c:60, src/utils/cRectangle.h@616280c:63, src/utils/cRectangle.h@616280c:66; заголовки layout отсутствуют	нет: тест проверяет вычисления в памяти
tests/MusicControlsLayoutTests.cpp	if speed/music geometry; tests/MusicControlsLayoutTests.cpp@9208dcf:36	Проверяются непересечение секций и частей слайдера, минимальная ширина слайдера и равенство ширин секций с точностью до 1. Размеры заданы в tests/MusicControlsLayoutTests.cpp@9208dcf:49, tests/MusicControlsLayoutTests.cpp@9208dcf:50 и tests/MusicControlsLayoutTests.cpp@9208dcf:51.	HudLayout, MusicControlsLayout, cRectangle; sidebar/HudLayout.hpp, sidebar/MusicControlsLayout.hpp	HudLayout и MusicControlsLayout отсутствуют; cRectangle есть: src/utils/cRectangle.h@616280c:21, src/utils/cRectangle.h@616280c:26, src/utils/cRectangle.h@616280c:37, src/utils/cRectangle.h@616280c:39, src/utils/cRectangle.h@616280c:54, src/utils/cRectangle.h@616280c:60, src/utils/cRectangle.h@616280c:63, src/utils/cRectangle.h@616280c:66; заголовки layout отсутствуют	нет: тест проверяет вычисления в памяти
tests/MusicTransitionPolicyTests.cpp	shouldAdvanceRepeatedMusicCategory(true, true); tests/MusicTransitionPolicyTests.cpp@9208dcf:6	При повторном входе в ту же категорию во время проигрывания возвращается false. Результаты объединяются в valid и проверяются возвратом кода процесса на строке 9.	shouldAdvanceRepeatedMusicCategory; audio/MusicTransitionPolicy.hpp	нет: функция, заголовок и тест отсутствуют в PORT	нет: файловое чтение отсутствует
tests/MusicTransitionPolicyTests.cpp	shouldAdvanceRepeatedMusicCategory(true, false); tests/MusicTransitionPolicyTests.cpp@9208dcf:7	При повторном входе в ту же категорию без проигрывания также возвращается false. Результаты объединяются в valid и проверяются возвратом кода процесса на строке 9.	shouldAdvanceRepeatedMusicCategory; audio/MusicTransitionPolicy.hpp	нет: функция, заголовок и тест отсутствуют в PORT	нет: файловое чтение отсутствует
tests/MusicTransitionPolicyTests.cpp	shouldAdvanceRepeatedMusicCategory(false, false); tests/MusicTransitionPolicyTests.cpp@9208dcf:8	При входе в другую категорию возвращается true. Результаты объединяются в valid и проверяются возвратом кода процесса на строке 9.	shouldAdvanceRepeatedMusicCategory; audio/MusicTransitionPolicy.hpp	нет: функция, заголовок и тест отсутствуют в PORT	нет: файловое чтение отсутствует
```

### `settings.tsv`

```tsv
исходная таблица	ключ	путь@ревизия:строка	итог сверки
fork-settings.tsv	playMusic	src/utils/GameSettings.hpp@9208dcf:18	совпало
fork-settings.tsv	playMusic	src/utils/common.cpp@9208dcf:89	совпало
fork-settings.tsv	playMusic	src/utils/common.cpp@9208dcf:370	совпало
fork-settings.tsv	playMusic	src/game/Preferences.cpp@0a33444:93	совпало
fork-settings.tsv	playMusic	resources/bin/settings.ini@0a33444:64	совпало
fork-settings.tsv	playSound	src/utils/GameSettings.hpp@9208dcf:19	совпало
fork-settings.tsv	playSound	src/utils/common.cpp@9208dcf:91	совпало
fork-settings.tsv	playSound	src/utils/common.cpp@9208dcf:371	совпало
fork-settings.tsv	playSound	src/game/Preferences.cpp@0a33444:99	совпало
fork-settings.tsv	playSound	resources/bin/settings.ini@0a33444:73	совпало
preferences.tsv	playMusic	src/utils/InitialGameSettings.hpp@0a33444:32	совпало
preferences.tsv	playMusic	src/game/Preferences.cpp@0a33444:93	совпало
preferences.tsv	playMusic	src/game/Preferences.cpp@0a33444:171	совпало
preferences.tsv	customMusic	src/utils/InitialGameSettings.hpp@0a33444:33	совпало
preferences.tsv	customMusic	src/game/Preferences.cpp@0a33444:96	совпало
preferences.tsv	customMusic	src/game/Preferences.cpp@0a33444:172	совпало
preferences.tsv	playSound	src/utils/InitialGameSettings.hpp@0a33444:34	совпало
preferences.tsv	playSound	src/game/Preferences.cpp@0a33444:99	совпало
preferences.tsv	playSound	src/game/Preferences.cpp@0a33444:173	совпало
preferences.tsv	playCreditsSound	src/utils/InitialGameSettings.hpp@0a33444:35	совпало
preferences.tsv	playCreditsSound	src/game/Preferences.cpp@0a33444:102	совпало
preferences.tsv	playCreditsSound	src/game/Preferences.cpp@0a33444:174	совпало
preferences.tsv	playMusic	src/utils/InitialGameSettings.hpp@d06f2fc:33	совпало
preferences.tsv	playMusic	src/game/Preferences.cpp@d06f2fc:92	совпало
preferences.tsv	playMusic	src/game/Preferences.cpp@d06f2fc:170	совпало
preferences.tsv	customMusic	src/utils/InitialGameSettings.hpp@d06f2fc:34	совпало
preferences.tsv	customMusic	src/game/Preferences.cpp@d06f2fc:95	совпало
preferences.tsv	customMusic	src/game/Preferences.cpp@d06f2fc:171	совпало
preferences.tsv	playSound	src/utils/InitialGameSettings.hpp@d06f2fc:35	совпало
preferences.tsv	playSound	src/game/Preferences.cpp@d06f2fc:98	совпало
preferences.tsv	playSound	src/game/Preferences.cpp@d06f2fc:172	совпало
preferences.tsv	playCreditsSound	src/utils/InitialGameSettings.hpp@d06f2fc:36	совпало
preferences.tsv	playCreditsSound	src/game/Preferences.cpp@d06f2fc:101	совпало
preferences.tsv	playCreditsSound	src/game/Preferences.cpp@d06f2fc:173	совпало
```

## Факты по пунктам

1. В FORK1 заданы восемь категорий: Gameplay, Menu, Conquest, три дома Briefing, Victory и Defeat; треки берутся из соответствующих относительных каталогов, список строится по расширению файла, а fallback задан встроенными MIDI. Плейлист хранит перемешанный мешок и историю переходов вперёд/назад; повтор категории может сохранить трек по политике `shouldAdvanceRepeatedMusicCategory`. Источники и все символы перечислены в `fork-music.tsv`.
2. Карта относит к music-pools 22 файла в `resources/bin/music/`; все они добавлены в FORK1, Git LFS-указатели по 133 байта с доступными LFS-объектами, отсутствуют в PORT. В таблице разложены размеры, категории и результаты по каждому пути; суммарный размер содержимого — 532834504 байта.
3. Вне `src/audio/` перечислены 38 музыкальных hunks; таблица указывает путь порта и наличие соответствующего вызова, поля или метода. Заметные места — создание пулов в `cGame_logic.cpp`, пользовательские кнопки в `cDrawManager.cpp` и путь загрузки внешнего аудио в `cSoundPlayer.cpp`.
4. В PORT музыку выбирают `AudioContext` и `MusicJukeBox`; загрузка внешнего аудио проходит через SDL_IOStream и `MIX_LoadAudio_IO`. Перечислены 33 вызова MIX_, десять каталогов под `audio/` и код выбора файлов; в текущем Git-дереве этих папок и музыкальных файлов нет. Между BASE и UP1 изменения музыкальной логики и файлов перечислены выводом `git log` в разделе пункта 4.
5. FORK1 регистрирует три музыкальных CTest: playlist, transition policy и controls layout. Таблица содержит 22 статические проверки/условия и используемые символы, заголовки и файловые данные; тесты в PORT не найдены.
6. Из p8r отобраны 34 строки по ключам `playMusic`, `playSound`, `customMusic` и `playCreditsSound`; все 34 строки проверены повторным `git show ... | sed` и совпали.

### Не проверено

Сборки, CTest и запуск игры не выполнялись по запрету задания. Наблюдаемое игровое поведение не запускалось; исследованы исходники, ресурсы, тестовые файлы и статические проверки.
