#include "audio/MusicPlaylist.h"

#include <catch2/catch_test_macros.hpp>
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <set>
#include <string>
#include <vector>

namespace {
std::vector<MusicTrack> builtInTracks(int count)
{
    std::vector<MusicTrack> result;
    for (int id = 0; id < count; ++id) {
        result.push_back(MusicTrack{id, {}});
    }
    return result;
}

struct TempDirectory {
    std::filesystem::path path = std::filesystem::temp_directory_path() / "d2tm_music_playlist_test";

    TempDirectory()
    {
        std::filesystem::remove_all(path);
        std::filesystem::create_directories(path);
    }

    ~TempDirectory()
    {
        std::error_code error;
        std::filesystem::remove_all(path, error);
    }
};
}

TEST_CASE("P9 music playlist shuffles every track once and keeps history", "[P9]")
{
    MusicPlaylist playlist(0xD2U);
    playlist.setTracks(builtInTracks(5));

    std::set<std::string> firstCycle;
    for (int index = 0; index < 5; ++index) {
        const MusicTrack *track = playlist.next();
        REQUIRE(track != nullptr);
        firstCycle.insert(track->key());
    }
    REQUIRE(firstCycle.size() == 5U);

    const std::string lastOfCycle = playlist.current()->key();
    const MusicTrack *firstOfNextCycle = playlist.next();
    REQUIRE(firstOfNextCycle != nullptr);
    REQUIRE(firstOfNextCycle->key() != lastOfCycle);

    const std::string current = playlist.current()->key();
    const MusicTrack *previous = playlist.previous();
    REQUIRE(previous != nullptr);
    REQUIRE(previous->key() == lastOfCycle);
    const MusicTrack *forwardFromHistory = playlist.next();
    REQUIRE(forwardFromHistory != nullptr);
    REQUIRE(forwardFromHistory->key() == current);
}

TEST_CASE("P9 music playlist discovers external tracks by extension", "[P9]")
{
    TempDirectory directory;
    for (const std::string &name : {"zeta.OGG", "alpha.mp3", "track.wav", "ignored.txt"}) {
        std::ofstream(directory.path / name).put('\0');
    }
    const std::filesystem::path unicodeFile = directory.path / std::filesystem::path(u8"пустыня.flac");
    std::ofstream(unicodeFile).put('\0');

    const auto discovered = MusicPlaylist::discoverExternalTracks(directory.path);
    REQUIRE(discovered.size() == 4U);
    REQUIRE(discovered[0].externalPath.filename() == "alpha.mp3");
    REQUIRE(discovered[1].externalPath.filename() == "track.wav");
    REQUIRE(discovered[2].externalPath.filename() == "zeta.OGG");
    REQUIRE(std::any_of(discovered.begin(), discovered.end(), [&](const MusicTrack &track) {
        return track.externalPath.filename() == unicodeFile.filename();
    }));
    REQUIRE(MusicPlaylist::isSupportedMusicFile("theme.FLAC"));
    REQUIRE_FALSE(MusicPlaylist::isSupportedMusicFile("notes.txt"));
}

TEST_CASE("P9 music tracks have display names and a discarded track leaves the playlist", "[P9]")
{
    const MusicTrack builtInTrack{4, {}};
    const MusicTrack externalTrack{-1, "music/gameplay/Track 1.wav"};
    REQUIRE(builtInTrack.displayName() == "Dune II #5");
    REQUIRE(externalTrack.displayName() == "Track 1");

    MusicPlaylist playlist(0xD2U);
    playlist.setTracks(builtInTracks(3));
    playlist.next();
    playlist.discardCurrent();
    REQUIRE(playlist.size() == 2U);
    REQUIRE(playlist.current() == nullptr);
}
