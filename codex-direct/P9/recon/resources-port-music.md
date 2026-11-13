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

