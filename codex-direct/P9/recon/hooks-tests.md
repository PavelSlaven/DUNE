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
