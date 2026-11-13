#include "debug/UiAudit.hpp"

// The recorder lives with the game loop in UiAuditCapture.cpp; tests run with the UI audit off and never call it.
namespace uiaudit
{
void recordText(const std::string &, int, int, int, int, const Rect *) {}
void recordGui(const char *, int, int, int, int) {}
void recordClick(const char *, int, int, int, int) {}
BoxScope::BoxScope(int, int, int, int) {}
BoxScope::~BoxScope() {}
}
