#include "gamestates/OptionsMenuLayout.hpp"
#include "utils/RenderScale.hpp"

#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <string>
#include <string_view>

namespace {
struct Case {
    int Wc;
    int Hc;
    int bh;
    bool playing;
};

std::ostream &operator<<(std::ostream &out, const Case &input)
{
    return out << "Wc=" << input.Wc << " Hc=" << input.Hc
               << " bh=" << input.bh << " playing=" << input.playing;
}

struct Check {
    const char *name;
    std::size_t failures = 0;

    bool fail(const Case &input, std::string_view field)
    {
        ++failures;
        if (failures > 20) {
            return false;
        }
        std::cerr << name << ": " << input << " field=" << field;
        return true;
    }

    void finish() const
    {
        if (failures != 0) {
            std::cerr << name << ": всего провалов " << failures << '\n';
        }
    }
};

void equal(Check &check, const Case &input, std::string_view field, int actual, int expected)
{
    if (actual != expected && check.fail(input, field)) {
        std::cerr << " actual=" << actual << " expected=" << expected << '\n';
    }
}

void rectangleEqual(
    Check &check,
    const Case &input,
    std::string_view field,
    const cRectangle &actual,
    const cRectangle &expected)
{
    const std::string prefix(field);
    equal(check, input, prefix + ".x", actual.getX(), expected.getX());
    equal(check, input, prefix + ".y", actual.getY(), expected.getY());
    equal(check, input, prefix + ".width", actual.getWidth(), expected.getWidth());
    equal(check, input, prefix + ".height", actual.getHeight(), expected.getHeight());
}

bool compactSpacing(const Case &input)
{
    const int margin = 8;
    const int actionGap = std::max(2, margin / 2);
    const int contentGap = 2;
    const int actionRows = input.playing ? 2 : 1;
    const int preferredApplyY = 10 * (input.bh + contentGap);
    const int preferredHeight = preferredApplyY + input.bh + margin
        + actionRows * input.bh + (actionRows - 1) * actionGap + margin;
    return preferredHeight > input.Hc - 8;
}

int expectedContentTop(const Case &input)
{
    const int titleHeight = input.bh - 10;
    const int minimumContentTop = 2 + titleHeight + 2;
    return compactSpacing(input)
        ? std::max(28, minimumContentTop)
        : input.bh + 2;
}

struct Field {
    const char *name;
    cRectangle OptionsMenuLayout::*member;
    bool playingOnly;
};

constexpr std::array<Field, 10> fields{{
    {"window", &OptionsMenuLayout::window, false},
    {"apply", &OptionsMenuLayout::apply, false},
    {"advanced", &OptionsMenuLayout::advanced, false},
    {"status", &OptionsMenuLayout::status, false},
    {"quit", &OptionsMenuLayout::quit, false},
    {"mainMenu", &OptionsMenuLayout::mainMenu, false},
    {"back", &OptionsMenuLayout::back, false},
    {"save", &OptionsMenuLayout::save, true},
    {"load", &OptionsMenuLayout::load, true},
    {"missionSelect", &OptionsMenuLayout::missionSelect, true},
}};

std::array<cRectangle, 10> expectedRectangles(const Case &input)
{
    const int m = 8;
    const int preferredActionGap = std::max(2, m / 2);
    const int c = 2;
    const int contentX = 24;
    const int applyWidth = 170;
    const int advancedWidth = 220;
    const int W = std::min(input.Wc - 32, 680);
    const int oldH = std::min(input.Hc - 32, 680);
    const int n = input.playing ? 2 : 1;
    const bool compact = compactSpacing(input);
    const int contentTop = expectedContentTop(input);
    const int actionGap = compact ? 2 : preferredActionGap;
    const int applyGap = compact ? 2 : m;
    const int applyY = compact ? contentTop + 9 * (input.bh + c) : 10 * (input.bh + c);
    const int bottomMargin = compact ? 4 : m;
    const int required = applyY + input.bh + applyGap
        + n * input.bh + (n - 1) * actionGap + bottomMargin;
    const int H = std::min(input.Hc - 8, std::max(oldH, required));
    const int statusX = contentX + applyWidth + m + advancedWidth + m;
    const int colW = (W - 4 * m) / 3;
    const int x0 = m;
    const int x1 = 2 * m + colW;
    const int x2 = 3 * m + 2 * colW;
    const int lastW = W - m - x2;
    const int bottomY = H - bottomMargin - input.bh;
    const int upperY = bottomY - actionGap - input.bh;

    return {{
        {(input.Wc - W) / 2, (input.Hc - H) / 2, W, H},
        {contentX, applyY, applyWidth, input.bh},
        {contentX + applyWidth + m, applyY, advancedWidth, input.bh},
        {statusX, applyY, std::max(0, W - m - statusX), input.bh},
        {x0, bottomY, colW, input.bh},
        {x1, bottomY, colW, input.bh},
        {x2, bottomY, lastW, input.bh},
        input.playing ? cRectangle(x0, upperY, colW, input.bh) : cRectangle(),
        input.playing ? cRectangle(x1, upperY, colW, input.bh) : cRectangle(),
        input.playing ? cRectangle(x2, upperY, lastW, input.bh) : cRectangle(),
    }};
}

void exact(Check &check, const Case &input, const OptionsMenuLayout &actual)
{
    const auto expected = expectedRectangles(input);
    for (std::size_t i = 0; i < fields.size(); ++i) {
        rectangleEqual(check, input, fields[i].name, actual.*fields[i].member, expected[i]);
    }
    const int contentGap = 2;
    const cRectangle speedLabel(
        16,
        expectedContentTop(input) + 2 * (input.bh + contentGap),
        122,
        input.bh
    );
    rectangleEqual(check, input, "speedLabel", actual.speedLabel, speedLabel);
    equal(check, input, "contentTop", actual.contentTop, expectedContentTop(input));
    equal(check, input, "contentGap", actual.contentGap, contentGap);
}

void table(Check &check)
{
    struct Row {
        Case input;
        cRectangle window;
        int bottomY;
        int upperY;
        int x0;
        int x1;
        int x2;
        int colW;
        int lastW;
    };
    const std::array<Row, 4> rows{{
        {{1067, 600, 42, true}, {193, 7, 680, 586}, 536, 490, 8, 232, 456, 216, 216},
        {{1067, 600, 42, false}, {193, 16, 680, 568}, 518, 0, 8, 232, 456, 216, 216},
        {{1920, 1080, 42, true}, {620, 200, 680, 680}, 630, 584, 8, 232, 456, 216, 216},
        {{801, 600, 42, true}, {60, 7, 680, 586}, 536, 490, 8, 232, 456, 216, 216},
    }};
    for (const auto &row : rows) {
        const auto &input = row.input;
        const auto actual = OptionsMenuLayout::create(
            input.Wc, input.Hc, input.bh, input.playing);
        rectangleEqual(check, input, "window", actual.window, row.window);
        equal(check, input, "quit.y(bottomY)", actual.quit.getY(), row.bottomY);
        equal(check, input, "quit.x(x0)", actual.quit.getX(), row.x0);
        equal(check, input, "mainMenu.x(x1)", actual.mainMenu.getX(), row.x1);
        equal(check, input, "back.x(x2)", actual.back.getX(), row.x2);
        equal(check, input, "quit.width(colW)", actual.quit.getWidth(), row.colW);
        equal(check, input, "back.width(lastW)", actual.back.getWidth(), row.lastW);
        if (input.playing) {
            equal(check, input, "save.y(upperY)", actual.save.getY(), row.upperY);
        } else {
            rectangleEqual(check, input, "save", actual.save, cRectangle());
            rectangleEqual(check, input, "load", actual.load, cRectangle());
            rectangleEqual(check, input, "missionSelect", actual.missionSelect, cRectangle());
        }
    }
}

void inside(Check &check, const Case &input, const OptionsMenuLayout &actual)
{
    const auto &window = actual.window;
    if (window.getX() < 0 || window.getX() + window.getWidth() > input.Wc ||
        window.getY() < 4 || window.getY() + window.getHeight() > input.Hc - 4) {
        if (check.fail(input, "window")) {
            std::cerr << " выходит за границы холста с вертикальным полем 4\n";
        }
    }
    for (std::size_t i = 1; i < fields.size(); ++i) {
        const auto &field = fields[i];
        if (field.playingOnly && !input.playing) {
            continue;
        }
        const auto &button = actual.*field.member;
        if (button.getX() < 0 || button.getY() < 0 || button.getWidth() <= 0 ||
            button.getX() + button.getWidth() > window.getWidth() ||
            button.getY() + button.getHeight() > window.getHeight()) {
            if (check.fail(input, field.name)) {
                std::cerr << " выходит за границы окна или имеет неположительную ширину\n";
            }
        }
    }
}

void headerSpacing(Check &check, const Case &input, const OptionsMenuLayout &actual)
{
    const int titleHeight = input.bh - 10;
    const int minimumContentTop = 2 + titleHeight + 2;
    if (actual.contentTop < minimumContentTop && check.fail(input, "header/contentTop")) {
        std::cerr << " actual=" << actual.contentTop
                  << " expected_at_least=" << minimumContentTop << '\n';
    }
}

bool intersects(const cRectangle &a, const cRectangle &b)
{
    return a.getX() < b.getX() + b.getWidth() &&
           b.getX() < a.getX() + a.getWidth() &&
           a.getY() < b.getY() + b.getHeight() &&
           b.getY() < a.getY() + a.getHeight();
}

void overlap(Check &check, const Case &input, const OptionsMenuLayout &actual)
{
    for (std::size_t i = 1; i < fields.size(); ++i) {
        const auto &a = fields[i];
        if (a.playingOnly && !input.playing) {
            continue;
        }
        const auto &button = actual.*a.member;
        for (std::size_t j = i + 1; j < fields.size(); ++j) {
            const auto &b = fields[j];
            if ((!b.playingOnly || input.playing) && intersects(button, actual.*b.member)) {
                if (check.fail(input, std::string(a.name) + "/" + b.name)) {
                    std::cerr << " прямоугольники пересекаются\n";
                }
            }
        }
        for (int k = 1; k <= 9; ++k) {
            const cRectangle row(
                                 0,
                                 actual.contentTop + (k - 1) * (input.bh + actual.contentGap),
                                 actual.window.getWidth(), input.bh);
            if (intersects(button, row)) {
                if (check.fail(input, std::string(a.name) + "/row" + std::to_string(k))) {
                    std::cerr << " прямоугольники пересекаются\n";
                }
            }
        }
    }
}
}

int main()
{
    Check exactCheck{"exact"};
    Check tableCheck{"table"};
    Check insideCheck{"inside"};
    Check headerSpacingCheck{"header-spacing"};
    Check overlapCheck{"overlap"};
    std::size_t cases = 0;
    const auto checkCanvas = [&](int Wc, int Hc) {
        for (int bh = 32; bh <= 44; ++bh) {
            for (bool playing : {true, false}) {
                const Case input{Wc, Hc, bh, playing};
                const auto actual = OptionsMenuLayout::create(Wc, Hc, bh, playing);
                exact(exactCheck, input, actual);
                inside(insideCheck, input, actual);
                headerSpacing(headerSpacingCheck, input, actual);
                overlap(overlapCheck, input, actual);
                ++cases;
            }
        }
    };
    constexpr std::array<RenderCanvasSize, 35> standardResolutions{{
        {800, 600}, {1024, 600}, {1024, 768}, {1152, 864}, {1280, 720},
        {1280, 768}, {1280, 800}, {1280, 960}, {1280, 1024}, {1360, 768},
        {1366, 768}, {1440, 900}, {1600, 900}, {1600, 1024}, {1600, 1200},
        {1680, 1050}, {1920, 1080}, {1920, 1200}, {2048, 1080}, {2048, 1152},
        {2048, 1536}, {2560, 1080}, {2560, 1440}, {2560, 1600}, {2880, 1620},
        {2880, 1800}, {3200, 1800}, {3440, 1440}, {3840, 1600}, {3840, 2160},
        {4096, 2160}, {5120, 1440}, {5120, 2160}, {5120, 2880}, {7680, 4320},
    }};
    constexpr std::array<RenderCanvasSize, 4> otherOutputs{{
        {801, 600}, {1023, 767}, {1599, 901}, {5119, 1439},
    }};
    const auto checkOutput = [&](RenderCanvasSize output) {
        const auto automatic = calculateRenderCanvasSize(
            output.width, output.height, AutomaticRenderScale);
        checkCanvas(automatic.width, automatic.height);
        for (int scale : ManualRenderScales) {
            if (isManualRenderScaleAvailable(output.width, output.height, scale)) {
                const auto canvas = calculateRenderCanvasSize(output.width, output.height, scale);
                checkCanvas(canvas.width, canvas.height);
            }
        }
    };
    for (const auto output : standardResolutions) {
        checkOutput(output);
    }
    for (const auto output : otherOutputs) {
        checkOutput(output);
    }
    for (int Wc : {800, 801, 1063, 1067, 2133}) {
        for (int Hc = 600; Hc <= 1440; ++Hc) {
            checkCanvas(Wc, Hc);
        }
    }
    for (int Wc = 800; Wc <= 1067; ++Wc) {
        checkCanvas(Wc, 600);
    }
    Check tallButtonCheck{"bh44"};
    for (int Wc = 800; Wc <= 1067; ++Wc) {
        for (bool playing : {true, false}) {
            const Case input{Wc, 600, 44, playing};
            const auto actual = OptionsMenuLayout::create(
                Wc, 600, 44, playing);
            inside(tallButtonCheck, input, actual);
            headerSpacing(headerSpacingCheck, input, actual);
            overlap(tallButtonCheck, input, actual);
        }
    }
    table(tableCheck);
    exactCheck.finish();
    tableCheck.finish();
    insideCheck.finish();
    headerSpacingCheck.finish();
    overlapCheck.finish();
    tallButtonCheck.finish();
    if (exactCheck.failures || tableCheck.failures || insideCheck.failures ||
        headerSpacingCheck.failures || overlapCheck.failures || tallButtonCheck.failures) {
        return 1;
    }
    std::cout << "Проверено случаев матрицы А + Б: " << cases << '\n';
    return 0;
}
