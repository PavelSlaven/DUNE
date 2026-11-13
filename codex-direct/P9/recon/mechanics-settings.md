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
