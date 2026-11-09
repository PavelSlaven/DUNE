#include "utils/cDataPack.hpp"

#include <catch2/catch_test_macros.hpp>

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

struct ExpectedEntry {
    int index;
    std::string name;
    int width;
    int height;
};

std::vector<std::string> splitTabs(const std::string &line)
{
    std::vector<std::string> fields;
    std::istringstream input(line);
    std::string field;
    while (std::getline(input, field, '\t')) {
        fields.push_back(field);
    }
    return fields;
}

}

TEST_CASE("T4 HD4 packs can be read by DataPack", "[T4][hd4]")
{
    const std::filesystem::path sourceRoot = D2TM_SOURCE_DIR;
    const std::filesystem::path expectedPath = sourceRoot / "tests/data/hd4_packs_expected.tsv";
    std::ifstream expectedFile(expectedPath);
    REQUIRE(expectedFile.is_open());

    std::string line;
    REQUIRE(static_cast<bool>(std::getline(expectedFile, line)));
    const auto header = splitTabs(line);
    REQUIRE(header.size() >= 6);
    REQUIRE(header[0] == "pack");
    REQUIRE(header[1] == "index");
    REQUIRE(header[2] == "name");
    REQUIRE(header[3] == "extension");
    REQUIRE(header[4] == "width");
    REQUIRE(header[5] == "height");

    std::unordered_map<std::string, std::vector<ExpectedEntry>> packs;
    while (std::getline(expectedFile, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        if (line.empty()) {
            continue;
        }
        const auto fields = splitTabs(line);
        REQUIRE(fields.size() >= 6);
        packs[fields[0]].push_back({std::stoi(fields[1]), fields[2], std::stoi(fields[4]), std::stoi(fields[5])});
    }

    REQUIRE(packs.size() == 22);
    for (const auto &[relativePack, entries] : packs) {
        (void)entries;
        INFO("HD4 pack: " << relativePack);
        const std::filesystem::path packPath = sourceRoot / "resources/bin/data" / relativePack;
        REQUIRE(std::filesystem::is_regular_file(packPath));
    }

    for (const auto &[relativePack, entries] : packs) {
        INFO("HD4 pack: " << relativePack);
        const std::filesystem::path packPath = sourceRoot / "resources/bin/data" / relativePack;
        std::ifstream packFile(packPath, std::ios::binary);
        REQUIRE(packFile.is_open());

        std::string firstLine;
        std::getline(packFile, firstLine);
        if (!firstLine.empty() && firstLine.back() == '\r') {
            firstLine.pop_back();
        }
        if (firstLine == "version https://git-lfs.github.com/spec/v1") {
            SKIP("HD4 pack is a Git LFS pointer: " << relativePack);
        }

        std::unordered_map<std::string, int> minimumIndexByName;
        for (const auto &entry : entries) {
            const auto [it, inserted] = minimumIndexByName.emplace(entry.name, entry.index);
            if (!inserted) {
                it->second = std::min(it->second, entry.index);
            }
        }

        DataPack pack(packPath.string(), nullptr);
        REQUIRE(pack.getNumberOfFile() == static_cast<int>(entries.size()));
        for (const auto &entry : entries) {
            INFO("entry " << entry.index << ": " << entry.name);
            SDL_Surface *surface = pack.getSurface(entry.index);
            REQUIRE(surface != nullptr);
            CHECK(surface->w == entry.width);
            CHECK(surface->h == entry.height);
            CHECK(pack.getIndexFromName(entry.name) == minimumIndexByName.at(entry.name));
        }
    }
}
