## Q-P7B-02

T6 на новой сборке завершился с `exit=1`. Полный вывод [лога](.tmp/p7b/run-ui_audit_translation.py.log):

```text
ru choose-house: untranslated text 'Back'
ru options-game-applied: untranslated text 'Saved. Restart the game.'
ru options-menu-applied: untranslated text 'Saved. Restart the game.'
ru outcome-lose: untranslated text 'Click to continue'
ru outcome-win: untranslated text 'Click to continue'
translation: 172 scenes, 5 failures
```

Подтверждены три источника:

- [cChooseHouseState.cpp:142](/srv/dune/worktrees/u34/src/gamestates/cChooseHouseState.cpp:142): `"Back"` отсутствует в таблице.
- [UiAuditAccess.cpp:177](/srv/dune/worktrees/u34/src/debug/UiAuditAccess.cpp:177): отладочная сцена подставляет английское `"Saved. Restart the game."`.
- [cWinLoseState.cpp:88](/srv/dune/worktrees/u34/src/gamestates/cWinLoseState.cpp:88): `"Click to continue"` отсутствует в таблице.

Сборка и все 337 тестов CTest прошли; первые четырнадцать скриптов проверки 4 дали `exit=0`. Проверки 5–7 не запускались. Изменения и [журнал хода](/srv/dune/worktrees/u34/.tmp/p7b/progress.md) сохранены, коммитов нет.

Разрешаете добавить две пропущенные строки в таблицу и локализовать подставляемый статус в `UiAuditAccess.cpp:177`?

Подтверждение требуется из-за правил «Ничего сверх таблицы» и запрета менять `src/debug/*`. По разделу «Вопросы и остановки» работа остановлена до уточнения рамки.