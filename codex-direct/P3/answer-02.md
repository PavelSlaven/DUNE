## A-P3-08

Ты прав: в перечне подключения пропущен шестнадцатый вызов. Рамка правок расширяется на один файл.

1. В `src/gameobjects/particles/cParticle.cpp` в строке 869 вызов получает пятый аргумент `m_gfxdata->getDensity()`:
   `auto recoloredBmp = createPlayerTextureFromIndexedSurfaceWithPalette(m_renderer, player, tex, TransparentColorIndex, m_gfxdata->getDensity());`
   Других правок в этом файле нет.
2. Проверка пункта 3 раздела «Подключение» теперь такая: `git grep -n "createPlayerTextureFromIndexedSurfaceWithPalette(" -- src` вне `src/utils/texture_utils.*` находит ровно 16 вызовов, и каждый передаёт пятым аргументом `getDensity()` того объекта `Graphics`, из которого взята поверхность.
3. Файл `src/gameobjects/particles/cParticle.cpp` входит во вторую группу коммитов (подключение).

### Организация работы

Порядок: правка пункта 1, затем дорожка C с проверками 1–5, затем твоя сверка диффа с контрактом и сдача.

Параллельно: ничего, дорожка C зависит от правки пункта 1.

Помощники: не больше одного одновременно, `gpt-6-luna` `xhigh`.

Остановки: те же, что в задании и в твоём плане (`Q-P3-01` … `Q-P3-07`), и новая `Q-P3-NN`, если найдётся ещё один вызов или место вне рамки.

Рамка правок: файлы из раздела «Файлы» твоего плана, `src/gameobjects/particles/cParticle.cpp`, `.tmp/progress.md` и `.tmp/p3/`. Тесты не менять.

Последнее сообщение — блок `## DONE-P3` по форме задания либо блок `Q-P3-NN`.
