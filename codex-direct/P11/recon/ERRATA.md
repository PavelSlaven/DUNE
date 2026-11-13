# Поправка ведущего к разведке П11

Выборочная сверка Haiku (`SPOTCHECK.md`) — 13 из 15. Оба несовпадения ведущий проверил командами `git show d06f2fcd2a347182c3774fb96e9a85570405c489:<путь> | sed -n '<строки>p'`: строки таблицы указывают начало участка diff `BASE..UP1`, а не строку утверждения.

- `port-mentat.tsv`, строка 46: `MENTAT_SCREEN_W` и `MENTAT_SCREEN_H` стоят на `src/gameobjects/mentat/AbstractMentat.cpp@d06f2fc:284` (`cRectangle dest`), вызов `m_sdlDrawer->renderStrechFullSprite` — на строке 285. Строка таблицы верна для первой половины утверждения.
- `port-mentat.tsv`, строка 79: участок нового файла начинается на `src/gameobjects/mentat/OrdosMentat.h@d06f2fc:1`; объявление `class OrdosMentat : public AbstractMentat` — строка 20.

Строки таблиц `port-mentat.tsv` с пометкой `hunk:` в столбце функции читать как начало участка diff.
