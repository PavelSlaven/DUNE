#pragma once

#include "utils/Localization.hpp"

enum class EditorText {
    NewMapTitle,
    NewMapName,
    NewMapAuthor,
    NewMapDescription,
    NewMapWidth,
    NewMapHeight,
    NewMapRandom,
    NewMapSeed,
    NewMapReturn,
    NewMapCreate,
    ModeTerrain,
    ModeStartPoints,
    ModeSymmetry,
    Save,
    TerrainHill,
    TerrainMountain,
    TerrainRock,
    TerrainSand,
    TerrainSpice,
    TerrainSpiceHill,
    BrushSize,
    StartPoint1,
    StartPoint2,
    StartPoint3,
    StartPoint4,
    StartPoint5,
    MirrorRight,
    MirrorLeft,
    MirrorUp,
    MirrorDown,
    MirrorBottomLeft,
    MirrorBottomRight,
    MirrorTopLeft,
    MirrorTopRight,
    SaveFailed,
    SaveDone,
    SquareRequired,
    Count
};

[[nodiscard]] inline const char *editorText(EditorText id)
{
    using localization::text;
    switch (id) {
        case EditorText::NewMapTitle: return text("New map", "Новая карта");
        case EditorText::NewMapName: return text("Name", "Название");
        case EditorText::NewMapAuthor: return text("Author", "Автор");
        case EditorText::NewMapDescription: return text("Description", "Описание");
        case EditorText::NewMapWidth: return text("Width", "Ширина");
        case EditorText::NewMapHeight: return text("Height", "Высота");
        case EditorText::NewMapRandom: return text("Random map", "Случайная карта");
        case EditorText::NewMapSeed: return text("Dune 2 seed", "Зерно Dune 2");
        case EditorText::NewMapReturn: return text("Return to menu", "В меню");
        case EditorText::NewMapCreate: return text("Create map", "Создать карту");
        case EditorText::ModeTerrain: return text("Terrain", "Рельеф");
        case EditorText::ModeStartPoints: return text("Start points", "Стартовые точки");
        case EditorText::ModeSymmetry: return text("Symmetry", "Симметрия");
        case EditorText::Save: return text("Save", "Сохранить");
        case EditorText::TerrainHill: return text("Hill", "Холм");
        case EditorText::TerrainMountain: return text("Mountain", "Горы");
        case EditorText::TerrainRock: return text("Rock", "Скала");
        case EditorText::TerrainSand: return text("Sand", "Песок");
        case EditorText::TerrainSpice: return text("Spice", "Пряность");
        case EditorText::TerrainSpiceHill: return text("Spice hill", "Холм с пряностью");
        case EditorText::BrushSize: return text("Brush size", "Размер кисти");
        case EditorText::StartPoint1: return text("Start point 1", "Стартовая точка 1");
        case EditorText::StartPoint2: return text("Start point 2", "Стартовая точка 2");
        case EditorText::StartPoint3: return text("Start point 3", "Стартовая точка 3");
        case EditorText::StartPoint4: return text("Start point 4", "Стартовая точка 4");
        case EditorText::StartPoint5: return text("Start point 5", "Стартовая точка 5");
        case EditorText::MirrorRight: return text("Mirror left to right", "Отразить слева направо");
        case EditorText::MirrorLeft: return text("Mirror right to left", "Отразить справа налево");
        case EditorText::MirrorUp: return text("Mirror bottom to top", "Отразить снизу вверх");
        case EditorText::MirrorDown: return text("Mirror top to bottom", "Отразить сверху вниз");
        case EditorText::MirrorBottomLeft: return text("Mirror to bottom left", "Отразить в левый нижний угол");
        case EditorText::MirrorBottomRight: return text("Mirror to bottom right", "Отразить в правый нижний угол");
        case EditorText::MirrorTopLeft: return text("Mirror to top left", "Отразить в левый верхний угол");
        case EditorText::MirrorTopRight: return text("Mirror to top right", "Отразить в правый верхний угол");
        case EditorText::SaveFailed: return text("Unable to save map", "Не удалось сохранить карту");
        case EditorText::SaveDone: return text("Map saved successfully", "Карта сохранена");
        case EditorText::SquareRequired: return text("Diagonal symmetry needs a square map", "Диагональной симметрии нужна квадратная карта");
        case EditorText::Count: break;
    }
    return "";
}
