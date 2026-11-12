S = 'C:/Users/Slaven/AppData/Local/Temp/claude/570e86ef5805dee8/ccfbda10-8ab1-41c6-ab77-cb504ef7f2ea/scratchpad/'
t = open(S + 'p8a/win-brief.md', encoding='utf-8').read()
pairs = [
    ('ветку `codex/p8a` игры', 'ветку `codex/p10c` игры'),
    ('снять одну сцену режима отладки интерфейса — площадки заводов', 'снять четыре сцены режима отладки интерфейса — страницы окна настроек'),
    ('switch codex/p8a`', 'switch codex/p10c`'),
    ('выводит `9f5b6102c`', 'выводит `66e9892fb`'),
    ('scratchpad\\p8a\\win\\', 'scratchpad\\p10c\\win\\'),
    ('строки 32 случаев с тегом `[P8A]` (их имена начинаются с `P8A `): запусти `ctest -R "^P8A " -V`',
     'строки 33 случаев с тегом `[P10C]` (их имена начинаются с `P10C `): запусти `ctest -R "^P10C " -V`'),
    ('5. **Сцены зданий.**', '5. **Сцены окна настроек.**'),
    ('`game-factory-pad`, `game-refinery-harvester`, `game-radar-dish`',
     '`options-game-game`, `options-game-controls`, `options-game-diagnostics`, `options-game-keybind`'),
    ('- Файл настроек игры `C:\\Users\\Slaven\\AppData\\Roaming\\D2TM\\Dune II - The Maker\\preferences.ini` не меняй и не удаляй.',
     '- Файл настроек игры `C:\\Users\\Slaven\\AppData\\Roaming\\D2TM\\Dune II - The Maker\\preferences.ini`: игра пишет его при выходе. До шага 4 скопируй его в папку отчёта как `preferences.ini.bak` (если файла нет — запиши это); после шага 5 верни копию на место побайтно (`Copy-Item` поверх) или, если файла не было, удали созданный игрой файл; выпиши sha256 файла до шага 4 и после возврата — они равны.'),
]
for a, b in pairs:
    assert a in t, a
    t = t.replace(a, b)
open(S + 'p10c/win-brief.md', 'w', encoding='utf-8').write(t)
print(t.count('p8a'), t.count('P8A'), t.count('p10c'))
