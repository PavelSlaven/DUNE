#pragma once

#include <string>

class Texture;

Texture *loadHdUiTexture(
    const std::string &fileName,
    int preferredDensity,
    const std::string &logContext = "HD UI"
);
