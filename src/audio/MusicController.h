#pragma once

#include "audio/MusicPlaylist.h"
#include "definitions.h"

#include <array>
#include <filesystem>
#include <string>
#include <vector>

class cSoundPlayer;

enum class MusicCategory : std::size_t {
    Gameplay,
    Menu,
    Conquest,
    BriefingAtreides,
    BriefingHarkonnen,
    BriefingOrdos,
    Victory,
    Defeat,
    Count
};

class MusicController {
    friend class UiAuditAccess;

public:
    MusicController(cSoundPlayer *soundPlayer, const std::filesystem::path &gameDirectory);

    void configure(
        MusicCategory category,
        const std::filesystem::path &relativeDirectory,
        std::vector<int> fallbackIds);
    void activate(MusicCategory category, bool advanceOnRepeatedEntry = true);
    void selectCategory(MusicCategory category);
    void update();
    void next();
    void previous();
    void replayCurrent();
    void stop();

    [[nodiscard]] std::string currentDisplayName() const;
    [[nodiscard]] bool hasActiveCategory() const { return m_hasActiveCategory; }

private:
    struct CategoryState {
        MusicPlaylist playlist;
        std::vector<MusicTrack> fallback;
        bool usingCustom = false;
        std::filesystem::path directory;
    };

    bool play(const MusicTrack *track);
    void playNextAvailable(bool backwards);
    void switchToFallback(CategoryState &state);
    CategoryState &activeState();
    const CategoryState &activeState() const;

    cSoundPlayer *m_soundPlayer;
    std::filesystem::path m_gameDirectory;
    std::array<CategoryState, static_cast<std::size_t>(MusicCategory::Count)> m_categories;
    MusicCategory m_activeCategory = MusicCategory::Menu;
    bool m_hasActiveCategory = false;
};

[[nodiscard]] inline MusicCategory musicCategoryFor(eMusicType type, int house)
{
    switch (type) {
        case eMusicType::PEACE:
        case eMusicType::ATTACK:
            return MusicCategory::Gameplay;
        case eMusicType::MENU:
            return MusicCategory::Menu;
        case eMusicType::CONQUEST:
            return MusicCategory::Conquest;
        case eMusicType::WIN:
            return MusicCategory::Victory;
        case eMusicType::LOSE:
            return MusicCategory::Defeat;
        case eMusicType::BRIEFING:
            if (house == HARKONNEN) return MusicCategory::BriefingHarkonnen;
            if (house == ORDOS) return MusicCategory::BriefingOrdos;
            return MusicCategory::BriefingAtreides;
    }
    return MusicCategory::Menu;
}
