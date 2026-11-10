## Ответ на Q-P5A-10

Конфликт подтверждаю. В порту апстрим перевёл темы на `cGuiThemeBuilder`, а `struct GuiTheme` (`src/gui/GuiTheme.hpp`) имеет 12 полей вместо шести у форка. Решение:

- В `struct GuiTheme` добавляются две статические функции `GuiTheme::Remaster()` и `GuiTheme::RemasterInactive()`. Имена — как в плане, поэтому вызовы `.withTheme(GuiTheme::Remaster())` и `.withTheme(GuiTheme::RemasterInactive())` в дорожках B и C не меняются.
- Каждая функция заполняет все 12 полей порта по именам: `GuiTheme theme{};`, затем по строке `theme.<поле> = Color{…};` на каждое поле, затем `return theme;`. Так ни один цвет не попадёт в чужое поле.
- Значения полей:

| Поле | `Remaster()` | `RemasterInactive()` |
|---|---|---|
| `fillColor` | `Color{24, 29, 33, 238}` | `Color{20, 24, 27, 220}` |
| `borderLight` | `Color{190, 145, 58, 255}` | `Color{91, 84, 66, 255}` |
| `borderDark` | `Color{71, 50, 24, 255}` | `Color{46, 42, 34, 255}` |
| `background` | `Color{32, 32, 32, 255}` | `Color{32, 32, 32, 255}` |
| `textColor` | `Color{236, 229, 202, 255}` | `Color{132, 132, 124, 255}` |
| `textDarkColor` | `Color{225, 177, 21, 255}` | `Color{225, 177, 21, 255}` |
| `textColorHover` | `Color{255, 202, 83, 255}` | `Color{154, 146, 124, 255}` |
| `textColorShadow` | `Color{4, 6, 7, 220}` | `Color{4, 6, 7, 220}` |
| `disabledTextColor` | `Color{132, 132, 124, 255}` | `Color{132, 132, 124, 255}` |
| `disabledFillColor` | `Color{20, 24, 27, 220}` | `Color{20, 24, 27, 220}` |
| `disabledBorderLight` | `Color{91, 84, 66, 255}` | `Color{91, 84, 66, 255}` |
| `disabledBorderDark` | `Color{46, 42, 34, 255}` | `Color{46, 42, 34, 255}` |

Откуда значения: шесть цветов каждой темы — из `src/gui/GuiTheme.hpp@9208dcf` в одноимённые поля порта; `background` и `textDarkColor` — значения, одинаковые у всех трёх тем `cGuiThemeBuilder` порта (`dark()`, `inactive()`, `light()`); четыре поля `disabled…` — цвета `RemasterInactive()` форка, чтобы кнопка с `setEnabled(false)` в теме `Remaster()` выглядела как неактивная кнопка форка. `cGuiThemeBuilder` не меняется. Поправка 5 плана остаётся в силе.

## Продолжение

Рабочее дерево чистое. Продолжи план `PLAN-P5A` с шага «реализация A, B и C одновременно»: дорожки A, B и C запускаются заново, A — с этим ответом в брифе. Остальной план не меняется.
