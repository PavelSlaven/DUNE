#include "audio/MusicTransitionPolicy.hpp"
#include "audio/MusicController.h"

#include <catch2/catch_test_macros.hpp>

TEST_CASE("P9 repeated music category does not advance the track", "[P9]")
{
    REQUIRE_FALSE(shouldAdvanceRepeatedMusicCategory(true, true));
    REQUIRE_FALSE(shouldAdvanceRepeatedMusicCategory(true, false));
    REQUIRE(shouldAdvanceRepeatedMusicCategory(false, false));
}

TEST_CASE("P9 music category routing follows the fork pools", "[P9]")
{
    REQUIRE(musicCategoryFor(eMusicType::PEACE, 0) == MusicCategory::Gameplay);
    REQUIRE(musicCategoryFor(eMusicType::ATTACK, 0) == MusicCategory::Gameplay);
    REQUIRE(musicCategoryFor(eMusicType::MENU, 0) == MusicCategory::Menu);
    REQUIRE(musicCategoryFor(eMusicType::CONQUEST, 0) == MusicCategory::Conquest);
    REQUIRE(musicCategoryFor(eMusicType::WIN, 0) == MusicCategory::Victory);
    REQUIRE(musicCategoryFor(eMusicType::LOSE, 0) == MusicCategory::Defeat);
    REQUIRE(musicCategoryFor(eMusicType::BRIEFING, ATREIDES) == MusicCategory::BriefingAtreides);
    REQUIRE(musicCategoryFor(eMusicType::BRIEFING, HARKONNEN) == MusicCategory::BriefingHarkonnen);
    REQUIRE(musicCategoryFor(eMusicType::BRIEFING, ORDOS) == MusicCategory::BriefingOrdos);
    REQUIRE(musicCategoryFor(eMusicType::BRIEFING, SARDAUKAR) == MusicCategory::BriefingAtreides);
    REQUIRE(musicCategoryFor(eMusicType::BRIEFING, GENERALHOUSE) == MusicCategory::BriefingAtreides);
}
