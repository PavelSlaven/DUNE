# Поправка ведущего к разведке P9R

Выборочная сверка — `SPOTCHECK.md`: 13 из 15 фактов совпали.

1. `src/cGame.h@9208dcf`: `class MusicController;` стоит на строке 47, а не 46 (на строке 46 — `class SaveGameManager;`); поле `std::unique_ptr<MusicController>` — строка 333.
2. Число 33 в пункте 4 — вызовы `MIX_…(` в `src/` ревизии `616280c`. Все вхождения подстроки `MIX_`, включая объявления типов и константы `MIX_PROP_*`, дают 60 (`git grep -c "MIX_" 616280c -- src`).
