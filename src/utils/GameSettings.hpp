#pragma once
#include "controls/CommandBindings.hpp"
#include "utils/GraphicsMode.hpp"

#include <string>

struct GameSettings {
    int screenW = 800;
    int screenH = 600;
    int renderScalePercent = 0;
    int worldScalePercent = 0;
    GraphicsMode graphicsMode = GraphicsMode::Hd;
    float cameraDragMoveSpeed = 0.5f;
    float cameraBorderOrKeyMoveSpeed = 0.5f;
    bool cameraEdgeMove = true;
    bool windowed = false;
    bool allowRepeatingReinforcements = false;
    bool turretsDownOnLowPower = false;
    bool rocketTurretsDownOnLowPower = false;
    bool playMusic = true;
    bool playSound = true;
    bool debugMode = false;
    bool drawUnitDebug = false;
    bool disableAI = false;
    bool oneAi = false;
    bool disableWormAi = false;
    bool disableReinforcements = false;
    bool noAiRest = false;
    bool drawUsages = false;
    bool pauseWhenLosingFocus = false;
    // Persisted language selection.  It is consumed by screens that have
    // localized resources; changing it takes effect after reopening/restart.
    std::string language = "ru";
    CommandBindings commandBindings;
    std::string gameFilename = "game.ini";
};
