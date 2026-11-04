#include "utils/cSoundPlayer.h"
#include "utils/cTimeCounter.h"
#include "utils/cTimeManager.h"
#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "controls/cMouse.h"
#include "drawers/cTextDrawer.h"

#include <memory>

int main()
{
    GameContext context;
    context.setTextContext(std::make_unique<TextContext>(
        std::make_unique<cTextDrawer>(nullptr),
        std::make_unique<cTextDrawer>(nullptr),
        std::make_unique<cTextDrawer>(nullptr),
        std::make_unique<cTextDrawer>(nullptr),
        std::make_unique<cTextDrawer>(nullptr),
        std::make_unique<cTextDrawer>(nullptr)));

    cMouse mouse(&context);
    if (mouse.isLeftButtonClicked()) return 1;
    if (mouse.isRightButtonClicked()) return 2;
    return 0;
}
