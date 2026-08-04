#pragma once

#include <memory>
#include "drawers/cTextDrawer.h"
class cTextDrawer;

class TextContext {

public:
    TextContext(
        std::unique_ptr<cTextDrawer> smallTextDrawer,
        std::unique_ptr<cTextDrawer> beneTextDrawer,
        std::unique_ptr<cTextDrawer> gameTextDrawer,
        std::unique_ptr<cTextDrawer> menuTextDrawer,
        std::unique_ptr<cTextDrawer> mentatHdTextDrawer
    );

    void resetCache() const;

    [[nodiscard]] cTextDrawer* getSmallTextDrawer() const;
    [[nodiscard]] cTextDrawer* getBeneTextDrawer() const;
    [[nodiscard]] cTextDrawer* getGameTextDrawer() const;
    [[nodiscard]] cTextDrawer* getMenuTextDrawer() const;
    [[nodiscard]] cTextDrawer* getMentatHdTextDrawer() const;

private:
    std::unique_ptr<cTextDrawer> m_smallTextDrawer;
    std::unique_ptr<cTextDrawer> m_beneTextDrawer;
    std::unique_ptr<cTextDrawer> m_gameTextDrawer;
    std::unique_ptr<cTextDrawer> m_menuTextDrawer;
    std::unique_ptr<cTextDrawer> m_mentatHdTextDrawer;
};
