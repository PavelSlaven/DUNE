#include "context/TextContext.hpp"

TextContext::TextContext(
    std::unique_ptr<cTextDrawer> smallTextDrawer,
    std::unique_ptr<cTextDrawer> beneTextDrawer,
    std::unique_ptr<cTextDrawer> gameTextDrawer,
    std::unique_ptr<cTextDrawer> menuTextDrawer,
    std::unique_ptr<cTextDrawer> mentatHdTextDrawer) :
m_smallTextDrawer(std::move(smallTextDrawer)),
m_beneTextDrawer(std::move(beneTextDrawer)),
m_gameTextDrawer(std::move(gameTextDrawer)),
m_menuTextDrawer(std::move(menuTextDrawer)),
m_mentatHdTextDrawer(std::move(mentatHdTextDrawer))
{
}

void TextContext::resetCache() const {
    m_smallTextDrawer->resetCache();
    m_beneTextDrawer->resetCache();
    m_gameTextDrawer->resetCache();
    m_menuTextDrawer->resetCache();
    m_mentatHdTextDrawer->resetCache();
}

cTextDrawer * TextContext::getSmallTextDrawer() const {
    return m_smallTextDrawer.get();
}

cTextDrawer * TextContext::getBeneTextDrawer() const {
    return m_beneTextDrawer.get();
}

cTextDrawer * TextContext::getGameTextDrawer() const {
    return m_gameTextDrawer.get();
}

cTextDrawer * TextContext::getMenuTextDrawer() const {
    return m_menuTextDrawer.get();
}

cTextDrawer * TextContext::getMentatHdTextDrawer() const {
    return m_mentatHdTextDrawer.get();
}
