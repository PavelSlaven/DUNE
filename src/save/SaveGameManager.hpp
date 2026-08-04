#pragma once

#include <filesystem>
#include <string>
#include <vector>

class cGame;

namespace save_game_detail {
struct SaveSnapshot;
}

struct SaveSlotInfo {
    int slot = 0;
    bool exists = false;
    bool valid = false;
    std::string name;
};

class SaveGameManager {
public:
    static constexpr int FormatVersion = 1;
    static constexpr int MaximumSlots = 10;

    [[nodiscard]] static std::filesystem::path quickSavePath();
    [[nodiscard]] static bool hasQuickSave();
    [[nodiscard]] static std::filesystem::path slotPath(int slot);
    [[nodiscard]] static SaveSlotInfo slotInfo(int slot);
    [[nodiscard]] static std::vector<SaveSlotInfo> listSlots();
    [[nodiscard]] static bool hasAnySave();

    static bool saveQuickGame(cGame &game, std::string &errorMessage);
    static bool loadQuickGame(cGame &game, std::string &errorMessage);
    static bool saveGame(
        cGame &game,
        int slot,
        const std::string &name,
        std::string &errorMessage
    );
    static bool loadGame(
        cGame &game,
        int slot,
        std::string &errorMessage
    );

private:
    static save_game_detail::SaveSnapshot captureSnapshot(cGame &game);
    static bool restoreSnapshot(
        cGame &game,
        const save_game_detail::SaveSnapshot &snapshot,
        std::string &errorMessage
    );
};
