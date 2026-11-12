#include <catch2/catch_test_macros.hpp>

#include "controls/cKeyBindings.h"
#include "game/Preferences.hpp"
#include "gamestates/AdvancedOptionsHeaderLayout.hpp"
#include "gamestates/OptionsKeyLabels.hpp"
#include "gamestates/OptionsMenuLayout.hpp"
#include "gamestates/OptionsPageData.hpp"

#include <algorithm>
#include <set>
#include <string>
#include <string_view>
#include <vector>

namespace {
bool overlaps(const cRectangle &first, const cRectangle &second)
{
    return first.getX() < second.getX() + second.getWidth() &&
           second.getX() < first.getX() + first.getWidth() &&
           first.getY() < second.getY() + second.getHeight() &&
           second.getY() < first.getY() + first.getHeight();
}

void checkRectangle(const cRectangle &actual, int x, int y, int width, int height)
{
    CHECK(actual.getX() == x);
    CHECK(actual.getY() == y);
    CHECK(actual.getWidth() == width);
    CHECK(actual.getHeight() == height);
}

void checkRectangleEqual(const cRectangle &left, const cRectangle &right)
{
    CHECK(left.getX() == right.getX());
    CHECK(left.getY() == right.getY());
    CHECK(left.getWidth() == right.getWidth());
    CHECK(left.getHeight() == right.getHeight());
}
}

TEST_CASE("P10C the settings title does not overlap a tab", "[P10C]")
{
    const auto layout = AdvancedOptionsHeaderLayout::create(760, 8, 34, 24);

    for (const auto &tab : layout.tabs) {
        CHECK_FALSE(overlaps(layout.title, tab));
    }
}

TEST_CASE("P10C the settings header has the exact geometry", "[P10C]")
{
    const auto layout = AdvancedOptionsHeaderLayout::create(760, 8, 34, 24);

    checkRectangle(layout.title, 0, 2, 760, 24);
    checkRectangle(layout.tabs[0], 8, 34, 180, 34);
    checkRectangle(layout.tabs[1], 196, 34, 180, 34);
    checkRectangle(layout.tabs[2], 384, 34, 180, 34);
    checkRectangle(layout.tabs[3], 572, 34, 180, 34);
}

TEST_CASE("P10C the list scroll helpers", "[P10C]")
{
    CHECK(optionsVisibleRows(76, 560, 38) == 12);
    CHECK(optionsVisibleRows(100, 100, 38) == 1);
    CHECK(optionsVisibleRows(0, 1000, 0) == 1);
    CHECK(optionsMaxScrollRow(86, 12) == 74);
    CHECK(optionsMaxScrollRow(10, 12) == 0);
    CHECK(optionsClampScrollRow(100, 86, 12) == 74);
    CHECK(optionsClampScrollRow(-5, 86, 12) == 0);
    CHECK(optionsClampScrollRow(30, 86, 12) == 30);
}

TEST_CASE("P10C resolution choices follow the desktop", "[P10C]")
{
    const std::vector<ResolutionOption> expected{
        {800, 600}, {1024, 600}, {1024, 768}, {1280, 720}, {1280, 768}, {1152, 864},
        {1280, 800}, {1360, 768}, {1366, 768}, {1280, 960}, {1440, 900}, {1280, 1024},
        {1600, 900}, {1600, 1024}, {1680, 1050}, {1920, 1080},
    };
    const auto choices = resolutionChoices(1920, 1080, {1280, 720});

    CHECK(choices == expected);
    CHECK(resolutionChoices(1366, 700, {1000, 700}) ==
          std::vector<ResolutionOption>{{800, 600}, {1024, 600}, {1000, 700}, {1366, 700}});
}

TEST_CASE("P10C the saved resolution is selected", "[P10C]")
{
    const auto choices = resolutionChoices(1920, 1080, {1280, 720});

    CHECK(resolutionChoiceIndex(choices, {1280, 720}) == 3);
    CHECK(resolutionChoiceIndex(choices, {123, 45}) == 0);
}

TEST_CASE("P10C every table action has a label", "[P10C]")
{
    const auto &table = cKeyBindings::getActionTable();
    std::set<std::string> english;
    std::set<std::string> russian;

    REQUIRE(KEY_ACTION_LABELS.size() == 86);
    REQUIRE(table.size() == KEY_ACTION_LABELS.size());
    for (std::size_t index = 0; index < table.size(); ++index) {
        CHECK(KEY_ACTION_LABELS[index].action == table[index].second);
        CHECK(std::string(KEY_ACTION_LABELS[index].english).empty() == false);
        CHECK(std::string(KEY_ACTION_LABELS[index].russian).empty() == false);
        english.emplace(KEY_ACTION_LABELS[index].english);
        russian.emplace(KEY_ACTION_LABELS[index].russian);
    }
    CHECK(english.size() == KEY_ACTION_LABELS.size());
    CHECK(russian.size() == KEY_ACTION_LABELS.size());
    CHECK(findKeyActionLabel(eKeyAction::GROUP_ASSIGN_1) == nullptr);
}

TEST_CASE("P10C the page keys are the chosen keys", "[P10C]")
{
    std::set<std::string_view> pageKeys;
    pageKeys.insert(MAIN_PAGE_KEYS.begin(), MAIN_PAGE_KEYS.end());
    pageKeys.insert(GAMEPLAY_PAGE_KEYS.begin(), GAMEPLAY_PAGE_KEYS.end());
    pageKeys.insert(DIAGNOSTICS_PAGE_KEYS.begin(), DIAGNOSTICS_PAGE_KEYS.end());
    const std::set<std::string_view> chosenKeys(Preferences::CHOSEN_KEYS.begin(), Preferences::CHOSEN_KEYS.end());

    CHECK(MAIN_PAGE_KEYS.size() == 6);
    CHECK(GAMEPLAY_PAGE_KEYS.size() == 7);
    CHECK(DIAGNOSTICS_PAGE_KEYS.size() == 8);
    CHECK(pageKeys.size() == 21);
    CHECK(pageKeys == chosenKeys);
}

TEST_CASE("P10C the options menu layout keeps its rows without extra rows", "[P10C]")
{
    const auto original = OptionsMenuLayout::create(1920, 1080, 42, true);
    const auto explicitZero = OptionsMenuLayout::create(1920, 1080, 42, true, -1, 0);

    checkRectangleEqual(original.window, explicitZero.window);
    checkRectangleEqual(original.apply, explicitZero.apply);
    checkRectangleEqual(original.save, explicitZero.save);
    checkRectangleEqual(original.quit, explicitZero.quit);
    CHECK(original.apply.getY() == 440);
}

TEST_CASE("P10C two extra content rows move the action rows down", "[P10C]")
{
    const auto withoutSave = OptionsMenuLayout::create(1920, 1080, 42, false, -1, 2);
    const auto withSave = OptionsMenuLayout::create(1920, 1080, 42, true, -1, 2);

    checkRectangle(withoutSave.apply, 24, 528, 170, 42);
    checkRectangle(withoutSave.window, 620, 200, 680, 680);
    CHECK(withoutSave.quit.getY() == 630);
    CHECK(withoutSave.contentTop == 44);
    CHECK(withSave.apply.getY() == 528);
    CHECK(withSave.save.getY() == 584);
}
