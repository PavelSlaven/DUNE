#include "gui/GuiObject.h"
#include "d2tmc.h"
#include "drawers/SDLDrawer.hpp"
#include "debug/UiAudit.hpp"
#include <iostream>

void GuiObject::setTheme(const GuiTheme& theme)
{
    m_theme = theme;
}

void GuiObject::auditRecord(const char *type) const
{
    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
}

void GuiObject::auditClick(const std::string &name) const
{
    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
}

void GuiObject::drawRectBorder(Color borderRect, Color borderBottomRight) const
{
    int x1= m_rect.getX();
    int y1 = m_rect.getY();
    int width = m_rect.getWidth();
    int height = m_rect.getHeight();
    //std::cout <<":" << x1 << " " << y1 << " " << width << " " << height << std::endl;
    renderDrawer->renderRectColor(m_rect,borderRect);
    renderDrawer->renderLine(x1+width, y1, x1+width, y1+height,borderBottomRight);
    renderDrawer->renderLine(x1, y1+height, x1+width, y1+height, borderBottomRight);
}

void GuiObject::drawRectFillBorder(const GuiTheme& theme) const
{
    renderDrawer->renderRectFillColor(m_rect, theme.fillColor);
    drawRectBorder(theme.borderLight, theme.borderDark);
}