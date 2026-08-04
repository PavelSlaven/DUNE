#include "audio/MusicPlaylist.h"

#include <algorithm>
#include <cassert>
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
}

int main()
{
    MusicPlaylist playlist(0xD2U);
    playlist.setTracks(builtInTracks(5));

    std::set<std::string> firstCycle;
    for (int index = 0; index < 5; ++index) {
        const MusicTrack *track = playlist.next();
        assert(track != nullptr);
        firstCycle.insert(track->key());
    }
    assert(firstCycle.size() == 5U);

    const std::string lastOfCycle = playlist.current()->key();
    const MusicTrack *firstOfNextCycle = playlist.next();
    assert(firstOfNextCycle != nullptr);
    assert(firstOfNextCycle->key() != lastOfCycle);

    const std::string current = playlist.current()->key();
    const MusicTrack *previous = playlist.previous();
    assert(previous != nullptr);
    assert(previous->key() == lastOfCycle);
    const MusicTrack *forwardFromHistory = playlist.next();
    assert(forwardFromHistory != nullptr);
    assert(forwardFromHistory->key() == current);

    const std::filesystem::path testDirectory =
        std::filesystem::temp_directory_path() / "d2tm_music_playlist_test";
    std::filesystem::remove_all(testDirectory);
    std::filesystem::create_directories(testDirectory);
    for (const std::string &name : {"zeta.OGG", "alpha.mp3", "track.wav", "ignored.txt"}) {
        std::ofstream(testDirectory / name).put('\0');
    }
    const std::filesystem::path unicodeFile = testDirectory / std::filesystem::path(u8"пустыня.flac");
    std::ofstream(unicodeFile).put('\0');
    const auto discovered = MusicPlaylist::discoverExternalTracks(testDirectory);
    assert(discovered.size() == 4U);
    assert(discovered[0].externalPath.filename() == "alpha.mp3");
    assert(discovered[1].externalPath.filename() == "track.wav");
    assert(discovered[2].externalPath.filename() == "zeta.OGG");
    assert(std::any_of(discovered.begin(), discovered.end(), [&](const MusicTrack &track) {
        return track.externalPath.filename() == unicodeFile.filename();
    }));
    assert(MusicPlaylist::isSupportedMusicFile("theme.FLAC"));
    assert(!MusicPlaylist::isSupportedMusicFile("notes.txt"));
    std::filesystem::remove_all(testDirectory);
    return 0;
}
