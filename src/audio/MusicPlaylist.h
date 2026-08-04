#pragma once

#include <cstdint>
#include <filesystem>
#include <optional>
#include <random>
#include <string>
#include <vector>

struct MusicTrack {
    int builtInId = -1;
    std::filesystem::path externalPath;

    [[nodiscard]] bool isExternal() const { return !externalPath.empty(); }
    [[nodiscard]] std::string key() const;
    [[nodiscard]] std::string displayName() const;
};

class MusicPlaylist {
public:
    explicit MusicPlaylist(std::uint32_t seed = std::random_device{}());

    void setTracks(std::vector<MusicTrack> tracks);
    [[nodiscard]] bool empty() const { return m_tracks.empty(); }
    [[nodiscard]] std::size_t size() const { return m_tracks.size(); }

    const MusicTrack *next();
    const MusicTrack *previous();
    const MusicTrack *current() const;
    void discardCurrent();

    static bool isSupportedMusicFile(const std::filesystem::path &file);
    static std::vector<MusicTrack> discoverExternalTracks(const std::filesystem::path &directory);

private:
    void refillBag();

    std::vector<MusicTrack> m_tracks;
    std::vector<std::size_t> m_bag;
    std::vector<std::size_t> m_history;
    std::size_t m_historyPosition = 0;
    bool m_hasHistoryPosition = false;
    std::mt19937 m_rng;
};
