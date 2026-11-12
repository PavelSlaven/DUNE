#define SDL_MAIN_HANDLED
#include <SDL3_ttf/SDL_ttf.h>

#include <catch2/catch_test_macros.hpp>

#include "gameobjects/mentat/MentatTextLayout.hpp"
#include "utils/IniParsing.hpp"
#include "utils/Localization.hpp"

#include <array>
#include <cctype>
#include <filesystem>
#include <fstream>
#include <memory>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

namespace {

struct TtfQuitGuard {
    ~TtfQuitGuard()
    {
        TTF_Quit();
    }
};

struct FontCloser {
    void operator()(TTF_Font *font) const
    {
        if (font) {
            TTF_CloseFont(font);
        }
    }
};

using FontPtr = std::unique_ptr<TTF_Font, FontCloser>;

std::vector<std::string> readLines(const fs::path &path)
{
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("Could not open " + path.string());
    }

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        lines.push_back(line);
    }
    return lines;
}

bool isTextLine(const std::string &line)
{
    static const std::regex pattern(R"(^\s*Text\s*=)");
    return std::regex_search(line, pattern);
}

std::string textValue(const std::string &line)
{
    const auto equals = line.find('=');
    const std::string value = line.substr(equals + 1);
    std::size_t first = 0;
    std::size_t last = value.size();
    while (first < last && (std::isspace(static_cast<unsigned char>(value[first])) || value[first] == '"')) {
        ++first;
    }
    while (last > first && (std::isspace(static_cast<unsigned char>(value[last - 1])) || value[last - 1] == '"')) {
        --last;
    }
    return value.substr(first, last - first);
}

std::set<fs::path> regularFiles(const fs::path &root)
{
    std::set<fs::path> paths;
    for (const auto &entry : fs::recursive_directory_iterator(root)) {
        if (!entry.is_regular_file()) {
            continue;
        }
        paths.insert(entry.path().lexically_relative(root));
    }
    return paths;
}

std::set<fs::path> campaignIniFiles(const fs::path &root)
{
    std::set<fs::path> paths;
    for (const auto &entry : fs::recursive_directory_iterator(root)) {
        if (!entry.is_regular_file() || entry.path().extension() != ".ini") {
            continue;
        }
        const auto relative = entry.path().lexically_relative(root);
        if (relative.begin() != relative.end() && relative.begin()->string() == "maps") {
            continue;
        }
        paths.insert(relative);
    }
    return paths;
}

std::set<int> scenarioNumbers(const fs::path &path)
{
    static const std::regex pattern(R"(^\s*Number\s*=\s*(-?\d+))");
    std::set<int> numbers{0};
    for (const auto &line : readLines(path)) {
        std::smatch match;
        if (std::regex_search(line, match, pattern)) {
            numbers.insert(std::stoi(match[1].str()));
        }
    }
    return numbers;
}

}

TEST_CASE("campaign text uses Russian copies and all mentat pages fit", "[campaign]")
{
    localization::setLanguage("en");
    CHECK(getCampaignTextDirectory() == "campaign");
    localization::setLanguage("ru");
    CHECK(getCampaignTextDirectory() == "campaign_ru");

    const fs::path bin = fs::path(D2TM_SOURCE_DIR) / "resources/bin";
    const fs::path campaign = bin / "campaign";
    const fs::path campaignRu = bin / "campaign_ru";
    const auto englishFiles = campaignIniFiles(campaign);
    REQUIRE(regularFiles(campaignRu) == englishFiles);

    for (const auto &relative : englishFiles) {
        const auto englishLines = readLines(campaign / relative);
        const auto russianLines = readLines(campaignRu / relative);
        REQUIRE(russianLines.size() == englishLines.size());
        for (std::size_t i = 0; i < englishLines.size(); ++i) {
            const bool englishText = isTextLine(englishLines[i]);
            const bool russianText = isTextLine(russianLines[i]);
            CHECK(russianText == englishText);
            if (!englishText) {
                CHECK(russianLines[i] == englishLines[i]);
            } else {
                CHECK(textValue(russianLines[i]).size() <= 254);
            }
        }
    }

    if (!TTF_Init()) {
        throw std::runtime_error("TTF_Init failed");
    }
    TtfQuitGuard ttfQuitGuard;
    FontPtr font(TTF_OpenFont((bin / "data/PTSansNarrow-Regular.ttf").string().c_str(), 14));
    if (!font) {
        throw std::runtime_error("Could not open PTSansNarrow-Regular.ttf");
    }
    const auto width = [&font](const std::string &text) {
        int width = 0;
        int height = 0;
        if (!TTF_GetStringSize(font.get(), text.c_str(), 0, &width, &height)) {
            throw std::runtime_error("Could not measure a mentat line");
        }
        return width;
    };
    const std::array sections{
        eScenarioIniSection::DESCRIPTION,
        eScenarioIniSection::BRIEFING,
        eScenarioIniSection::ADVICE,
        eScenarioIniSection::WIN,
        eScenarioIniSection::LOSE,
    };
    const std::array briefingFiles{"mentata.ini", "mentath.ini", "mentato.ini", "mentats.ini"};
    for (const char *directory : {"campaign", "campaign_ru"}) {
        const bool english = std::string(directory) == "campaign";
        for (const char *briefingFile : briefingFiles) {
            const fs::path path = bin / directory / "briefings" / briefingFile;
            for (const int scenario : scenarioNumbers(path)) {
                for (const auto section : sections) {
                    std::ifstream input(path);
                    REQUIRE(input.good());
                    auto sentences = parseBriefing(input, scenario, section);
                    sentences.resize(10);
                    for (int i = 0; i < 10; i += 2) {
                        const std::array<std::string, 2> original{sentences[i], sentences[i + 1]};
                        const auto lines = layoutMentatPage(original[0], original[1], MENTAT_TEXT_WIDTH, width);
                        CHECK(width(lines[0]) <= MENTAT_TEXT_WIDTH);
                        CHECK(width(lines[1]) <= MENTAT_TEXT_WIDTH);
                        if (english) {
                            CHECK(lines == original);
                        }
                    }
                }
            }
        }
    }
    localization::setLanguage("ru");
}
