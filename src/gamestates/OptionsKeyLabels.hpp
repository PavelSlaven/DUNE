#pragma once

#include "controls/eKeyAction.h"
#include "utils/Localization.hpp"

#include <array>
#include <string>

struct KeyActionLabel {
    eKeyAction action;
    const char *english;
    const char *russian;
};

inline constexpr std::array<KeyActionLabel, 86> KEY_ACTION_LABELS{{
    {eKeyAction::SCREENSHOT, "Take screenshot", "Снимок экрана"},
    {eKeyAction::TOGGLE_MUSIC, "Toggle music", "Включить или выключить музыку"},
    {eKeyAction::MUSIC_VOLUME_DOWN, "Music volume down", "Музыка тише"},
    {eKeyAction::MUSIC_VOLUME_UP, "Music volume up", "Музыка громче"},
    {eKeyAction::MUSIC_PREVIOUS_TRACK, "Previous music track", "Предыдущий трек"},
    {eKeyAction::MUSIC_NEXT_TRACK, "Next music track", "Следующий трек"},
    {eKeyAction::GAME_SPEED_UP, "Game speed up", "Игра быстрее"},
    {eKeyAction::GAME_SPEED_DOWN, "Game speed down", "Игра медленнее"},
    {eKeyAction::TOGGLE_FULLSCREEN, "Toggle fullscreen", "Переключить полноэкранный режим"},
    {eKeyAction::TOGGLE_CHEAT, "Toggle cheat mode", "Переключить режим читов"},
    {eKeyAction::SCROLL_LEFT, "Scroll map left", "Прокрутка карты влево"},
    {eKeyAction::SCROLL_RIGHT, "Scroll map right", "Прокрутка карты вправо"},
    {eKeyAction::SCROLL_UP, "Scroll map up", "Прокрутка карты вверх"},
    {eKeyAction::SCROLL_DOWN, "Scroll map down", "Прокрутка карты вниз"},
    {eKeyAction::CENTER_ON_HOME, "Center on home", "К стартовой точке"},
    {eKeyAction::CENTER_ON_STRUCTURE, "Center on structure", "К выбранному зданию"},
    {eKeyAction::ZOOM_RESET, "Reset zoom", "Сбросить масштаб карты"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_1, "Save view bookmark 1", "Запомнить вид 1"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_2, "Save view bookmark 2", "Запомнить вид 2"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_3, "Save view bookmark 3", "Запомнить вид 3"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_4, "Save view bookmark 4", "Запомнить вид 4"},
    {eKeyAction::SAVE_VIEWPORT_BOOKMARK_5, "Save view bookmark 5", "Запомнить вид 5"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_1, "Go to view bookmark 1", "Перейти к виду 1"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_2, "Go to view bookmark 2", "Перейти к виду 2"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_3, "Go to view bookmark 3", "Перейти к виду 3"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_4, "Go to view bookmark 4", "Перейти к виду 4"},
    {eKeyAction::JUMP_TO_VIEWPORT_BOOKMARK_5, "Go to view bookmark 5", "Перейти к виду 5"},
    {eKeyAction::QUICK_SAVE, "Quick save", "Быстрое сохранение"},
    {eKeyAction::QUICK_LOAD, "Quick load", "Быстрая загрузка"},
    {eKeyAction::TOGGLE_FPS, "Show FPS", "Показать или скрыть FPS"},
    {eKeyAction::TOGGLE_TIME_DISPLAY, "Show game time", "Показать или скрыть время игры"},
    {eKeyAction::OPEN_MENU, "Open menu", "Открыть меню"},
    {eKeyAction::DEPLOY_UNIT, "Deploy / Release", "Развернуть / Выпустить"},
    {eKeyAction::SET_PRIMARY, "Set primary structure", "Сделать основным зданием"},
    {eKeyAction::ATTACK_MODE, "Attack / Rally", "Атаковать / Точка сбора"},
    {eKeyAction::ADD_TO_SELECTION, "Add to selection", "Добавить к выбору"},
    {eKeyAction::REPAIR_UNIT, "Repair", "Ремонт"},
    {eKeyAction::RETURN_TO_BASE, "Return to base", "Вернуться на базу"},
    {eKeyAction::SEND_TO_REFINERY, "Unload", "Разгрузить"},
    {eKeyAction::SELECT_SAME_TYPE_ON_MAP, "Select units of the same type on map", "Выбрать такие же юниты на карте"},
    {eKeyAction::SELECT_SAME_TYPE_ON_SCREEN, "Select units of the same type on screen", "Выбрать такие же юниты на экране"},
    {eKeyAction::SELECT_INFANTRY_ON_MAP, "Select infantry on map", "Выбрать пехоту на карте"},
    {eKeyAction::SELECT_INFANTRY_ON_SCREEN, "Select infantry on screen", "Выбрать пехоту на экране"},
    {eKeyAction::SELECT_WHEELS_ON_MAP, "Select wheeled units on map", "Выбрать колёсную технику на карте"},
    {eKeyAction::SELECT_WHEELS_ON_SCREEN, "Select wheeled units on screen", "Выбрать колёсную технику на экране"},
    {eKeyAction::SELECT_TANKS_ON_MAP, "Select tanks on map", "Выбрать танки на карте"},
    {eKeyAction::SELECT_TANKS_ON_SCREEN, "Select tanks on screen", "Выбрать танки на экране"},
    {eKeyAction::TRACK_UNIT, "Track selected units", "Следить за выбранными"},
    {eKeyAction::SELECT_LAUNCHERS_ON_MAP, "Select launchers on map", "Выбрать ракетные установки на карте"},
    {eKeyAction::SELECT_LAUNCHERS_ON_SCREEN, "Select launchers on screen", "Выбрать ракетные установки на экране"},
    {eKeyAction::SELECT_HARVESTERS_ON_MAP, "Select harvesters on map", "Выбрать харвестеры на карте"},
    {eKeyAction::SELECT_HARVESTERS_ON_SCREEN, "Select harvesters on screen", "Выбрать харвестеры на экране"},
    {eKeyAction::SELECT_ATTACKING_ON_MAP, "Select attacking units on map", "Выбрать атакующих на карте"},
    {eKeyAction::GROUP_1, "Select group 1", "Выбрать группу 1"},
    {eKeyAction::GROUP_2, "Select group 2", "Выбрать группу 2"},
    {eKeyAction::GROUP_3, "Select group 3", "Выбрать группу 3"},
    {eKeyAction::GROUP_4, "Select group 4", "Выбрать группу 4"},
    {eKeyAction::GROUP_5, "Select group 5", "Выбрать группу 5"},
    {eKeyAction::GROUP_6, "Select group 6", "Выбрать группу 6"},
    {eKeyAction::EDITOR_SAVE, "Editor: save map", "Редактор: сохранить карту"},
    {eKeyAction::EDITOR_ZOOM_IN, "Editor: zoom in", "Редактор: приблизить"},
    {eKeyAction::EDITOR_ZOOM_OUT, "Editor: zoom out", "Редактор: отдалить"},
    {eKeyAction::EDITOR_DISPLAY_GRID, "Editor: show grid", "Редактор: сетка"},
    {eKeyAction::EDITOR_DISPLAY_AXES, "Editor: show axes", "Редактор: оси"},
    {eKeyAction::EDITOR_UNDO, "Editor: undo", "Редактор: отменить"},
    {eKeyAction::EDITOR_REDO, "Editor: redo", "Редактор: повторить"},
    {eKeyAction::EDITOR_COPY, "Editor: copy", "Редактор: копировать"},
    {eKeyAction::EDITOR_PASTE, "Editor: paste", "Редактор: вставить"},
    {eKeyAction::EDITOR_CUT, "Editor: cut", "Редактор: вырезать"},
    {eKeyAction::MENU_BACK, "Menu: back", "Меню: назад"},
    {eKeyAction::MENU_CONFIRM, "Menu: confirm", "Меню: подтвердить"},
    {eKeyAction::MENU_CANCEL, "Menu: cancel", "Меню: отмена"},
    {eKeyAction::DEBUG_WIN, "Debug: win mission", "Отладка: победа в миссии"},
    {eKeyAction::DEBUG_LOSE, "Debug: lose mission", "Отладка: поражение в миссии"},
    {eKeyAction::DEBUG_GIVE_CREDITS, "Debug: give credits", "Отладка: выдать кредиты"},
    {eKeyAction::DEBUG_DESTROY_AT_CURSOR, "Debug: destroy at cursor", "Отладка: уничтожить под курсором"},
    {eKeyAction::DEBUG_REVEAL_MAP, "Debug: reveal map", "Отладка: открыть карту"},
    {eKeyAction::DEBUG_DAMAGE_AT_CURSOR, "Debug: damage at cursor", "Отладка: повредить под курсором"},
    {eKeyAction::DEBUG_KILL_CARRYALLS, "Debug: kill carryalls", "Отладка: уничтожить транспортники"},
    {eKeyAction::DEBUG_SPAWN_ORNITHOPTER, "Debug: spawn ornithopter", "Отладка: создать орнитоптер"},
    {eKeyAction::DEBUG_SPAWN_WORM, "Debug: spawn worm", "Отладка: создать червя"},
    {eKeyAction::DEBUG_CLEAR_SHROUD_AT_CURSOR, "Debug: clear shroud at cursor", "Отладка: снять туман под курсором"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_0, "Debug: switch to player 0", "Отладка: переключиться на игрока 0"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_1, "Debug: switch to player 1", "Отладка: переключиться на игрока 1"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_2, "Debug: switch to player 2", "Отладка: переключиться на игрока 2"},
    {eKeyAction::DEBUG_SWITCH_PLAYER_3, "Debug: switch to player 3", "Отладка: переключиться на игрока 3"},
}};

[[nodiscard]] inline const KeyActionLabel *findKeyActionLabel(eKeyAction action)
{
    for (const KeyActionLabel &label : KEY_ACTION_LABELS) {
        if (label.action == action) {
            return &label;
        }
    }
    return nullptr;
}

[[nodiscard]] inline std::string keyActionLabelText(eKeyAction action)
{
    const KeyActionLabel *label = findKeyActionLabel(action);
    return label == nullptr ? std::string() : std::string(localization::text(label->english, label->russian));
}
