# Отчёт: запуск тестовой копии DUNE до меню и выжимка лога

Бриф: scratchpad\g3\brief-launch.md. Тестовая копия: C:\Users\Slaven\Projects\DUNE-pilot-test.

## Шаг 1. Переименование прежнего лога

Команда: Rename-Item -LiteralPath <копия>\log.txt -NewName log-before-g3.txt (после проверки, что log-before-g3.txt отсутствует).
Вывод: renamed. Далее: log-before-g3.txt, 6109225 байт, LastWriteTime 29.10.2026 15:24:29. log.txt в копии до запуска присутствовал, log-before-g3.txt — нет.

## Шаг 2. Запуск игры

Команда: Start-Process d2tm.exe с аргументами -windowed -debug -noai -nomusic -screenWidth 1600 -screenHeight 1000, PATH с msys64 из run_test.bat.
Вывод: started PID=3292. Ошибки запуска не было.

## Шаг 3. Ожидание 30 секунд и состояние процесса

Команда: Wait-Process -Id 3292 -Timeout 30 (вместо Start-Sleep, который среда блокирует), затем Get-Process -Id 3292.
Вывод: STILL ALIVE after 30s wait (Wait-Process timed out), elapsed=30s; Get-Process: ALIVE PID=3292 Name=d2tm Responding=True.
Процесс жив через 30 секунд. Код выхода не применим: процесс не завершился сам.

## Шаг 4. Остановка процесса

Команда: Stop-Process -Id 3292; затем Wait-Process -Id 3292 -Timeout 5.
Вывод: Stop-Process issued; STILL ALIVE 5s after Stop-Process; Get-Process: PID 3292 absent.
Пояснение: строка «STILL ALIVE» ложная. Wait-Process выдаёт ошибку и для уже отсутствующего PID, поэтому сработал catch. Независимая проверка: CIM: PID 3292 absent; No d2tm process running. Процесс остановлен.

## Шаг 5. Сведение логов (скриптом)

Правила: ключевые слова error, fail, cannot, missing, exception, assert ищутся подстрокой без учёта регистра. Старый лог декодирован как cp1251, новый как UTF-8. Лидирующий префикс «число|» (счётчик тиков по виду строк, не метка времени) срезан. Пакет: строки нового лога с sdl_data_hd4 или DEVASTATOR, без учёта регистра.

- Строк: новый log.txt = 213; прежний log-before-g3.txt = 37853.
- Строк с ключевыми словами: новый = 0, уникальных текстов = 0; прежний = 307, уникальных текстов = 128.
- «Новые» тексты (есть в новом, нет в прежнем): 0.
- Строки нового лога с sdl_data_hd4 или DEVASTATOR: 2.

### Уникальные тексты прежнего лога (ключевые слова)

- WARN|NONE|PLAYER [-1(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 2515, iGoalCell = 2515] 'ERROR: Wanted to create sandworm for player other than AI_WORM!?'|(logbook)
- WARN|NONE|PLAYER [-1(=Р‘РµР· Р”РѕРјР°)] : [UNIT[7]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1951, iGoalCell = 1951] 'ERROR: Wanted to create sandworm for player other than AI_WORM!?'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[10]: type = 8(=Р Р°РєРµС‚РЅР°СЏ СѓСЃС‚Р°РЅРѕРІРєР°), iCell = 572, iGoalCell = 896] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[10]: type = 8(=Р Р°РєРµС‚РЅР°СЏ СѓСЃС‚Р°РЅРѕРІРєР°), iCell = 572, iGoalCell = 896] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[10]: type = 8(=Р Р°РєРµС‚РЅР°СЏ СѓСЃС‚Р°РЅРѕРІРєР°), iCell = 572, iGoalCell = 896] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1356] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1356] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1356] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1357] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1357] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 573, iGoalCell = 1357] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 636, iGoalCell = 1357] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 636, iGoalCell = 1357] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[15]: type = 13(=РҐР°СЂРІРµСЃС‚РµСЂ), iCell = 636, iGoalCell = 1357] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[2]: type = 4(=РўСЂР°Р№Рє), iCell = 569, iGoalCell = 896] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[2]: type = 4(=РўСЂР°Р№Рє), iCell = 569, iGoalCell = 896] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[2]: type = 4(=РўСЂР°Р№Рє), iCell = 569, iGoalCell = 896] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[4]: type = 4(=РўСЂР°Р№Рє), iCell = 634, iGoalCell = 896] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[4]: type = 4(=РўСЂР°Р№Рє), iCell = 634, iGoalCell = 896] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[4]: type = 4(=РўСЂР°Р№Рє), iCell = 634, iGoalCell = 896] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[7]: type = 12(=Р—РІСѓРєРѕРІРѕР№ С‚Р°РЅРє), iCell = 436, iGoalCell = 631] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[7]: type = 12(=Р—РІСѓРєРѕРІРѕР№ С‚Р°РЅРє), iCell = 436, iGoalCell = 631] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [0(=РђС‚СЂРµР№РґРµСЃС‹)] : [UNIT[7]: type = 12(=Р—РІСѓРєРѕРІРѕР№ С‚Р°РЅРє), iCell = 436, iGoalCell = 631] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 240] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 240] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 240] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 306] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 306] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 110, iGoalCell = 306] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 241] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 241] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 241] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 306] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 306] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 111, iGoalCell = 306] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 242] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 242] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 242] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 306] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 306] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 306] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 308] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 308] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 308] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 309] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 309] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 112, iGoalCell = 309] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 573] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 573] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 573] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 638] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 638] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1162, iGoalCell = 638] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2408] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2408] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2408] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2882] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2882] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 2882] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 3211] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 3211] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1415, iGoalCell = 3211] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1545, iGoalCell = 1694] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1545, iGoalCell = 1694] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1545, iGoalCell = 1694] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 243] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 243] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 243] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 244] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 244] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 244] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 308] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 308] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 308] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 309] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 309] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 309] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 370] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 370] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 178, iGoalCell = 370] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 246] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 246] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 246] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 309] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 309] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 180, iGoalCell = 309] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 181, iGoalCell = 246] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 181, iGoalCell = 246] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 181, iGoalCell = 246] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 182, iGoalCell = 246] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 182, iGoalCell = 246] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 182, iGoalCell = 246] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 183, iGoalCell = 246] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 183, iGoalCell = 246] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 183, iGoalCell = 246] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 184, iGoalCell = 246] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 184, iGoalCell = 246] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 184, iGoalCell = 246] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3909] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3909] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3909] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3978] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3978] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[13]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1941, iGoalCell = 3978] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1595, iGoalCell = 3999] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1595, iGoalCell = 3999] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1595, iGoalCell = 3999] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1604, iGoalCell = 2692] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1604, iGoalCell = 2692] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[14]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 1604, iGoalCell = 2692] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[19]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3836, iGoalCell = 1799] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[19]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3836, iGoalCell = 1799] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[19]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3836, iGoalCell = 1799] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 2973, iGoalCell = 3294] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 2973, iGoalCell = 3294] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 2973, iGoalCell = 3294] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3037, iGoalCell = 3294] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3037, iGoalCell = 3294] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3037, iGoalCell = 3294] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3101, iGoalCell = 3294] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3101, iGoalCell = 3294] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3101, iGoalCell = 3294] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3165, iGoalCell = 3294] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3165, iGoalCell = 3294] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3165, iGoalCell = 3294] 'Failed to find new cell, backtracking failed!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3229, iGoalCell = 3294] 'CREATE_PATH: Failed to create path!'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3229, iGoalCell = 3294] 'FAILED TO CREATE PATH - nothing found to continue'|(logbook)
- WARN|NONE|PLAYER [6(=Р‘РµР· Р”РѕРјР°)] : [UNIT[6]: type = 17(=РџРµСЃС‡Р°РЅС‹Р№ С‡РµСЂРІСЊ), iCell = 3229, iGoalCell = 3294] 'Failed to find new cell, backtracking failed!'|(logbook)

### Уникальные тексты нового лога (ключевые слова)

нет (0)

### «Новые» тексты

нет (0)

### Строки нового лога с sdl_data_hd4 или DEVASTATOR (первые 20)

- `2368|INFO|INIT|Hooked datafile: sdl_data_hd4.dat|SUCCESS|Load data`
- `2448|INFO|INIT|Hooked datafile: sdl_data_hd4.dat|SUCCESS|Load data`


## Не проверено

- Визуально не проверялось, что игра дошла до главного меню: только процесс и лог. Экран не снимался.
- Код выхода процесса не получен: процесс остановлен Stop-Process, а не завершился сам.
- Длина логов несопоставима: новый лог 213 строк за 30 секунд, прежний 37853 строк. Сравнение выполнено по правилу брифа, без оценки.
- Префикс «число|» принят за счётчик тиков по виду строк; формат лога по исходнику не сверялся.
- Подстрочное совпадение ловит и производные слова (например, failed, errors).
