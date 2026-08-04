#include "audio/MusicPlaylist.h"

#include <algorithm>
#include <cctype>
#include <numeric>

namespace {
std::string utf8String(const std::filesystem::path &path)
{
    const auto value = path.u8string();
    return std::string(value.begin(), value.end());
}

std::string lowerAscii(std::string value)
{
    std::transform(value.begin(), value.end(), value.begin(), [](unsigned char ch) {
        return static_cast<char>(std::tolower(ch));
    });
    return value;
}
}

std::string MusicTrack::key() const
{
    return isExternal() ? utf8String(externalPath.lexically_normal()) : std::to_string(builtInId);
}

std::string MusicTrack::displayName() const
{
    if (isExternal()) {
        return utf8String(externalPath.stem());
    }
    return "Dune II #" + std::to_string(builtInId + 1);
}

MusicPlaylist::MusicPlaylist(std::uint32_t seed) : m_rng(seed)
{
}

void MusicPlaylist::setTracks(std::vector<MusicTrack> tracks)
{
    m_tracks = std::move(tracks);
    m_bag.clear();
    m_history.clear();
    m_historyPosition = 0;
    m_hasHistoryPosition = false;
}

void MusicPlaylist::refillBag()
{
    m_bag.resize(m_tracks.size());
    std::iota(m_bag.begin(), m_bag.end(), 0U);
    std::shuffle(m_bag.begin(), m_bag.end(), m_rng);

    const MusicTrack *last = current();
    if (last && m_bag.size() > 1U && m_bag.back() < m_tracks.size() &&
        m_tracks[m_bag.back()].key() == last->key()) {
        std::swap(m_bag.front(), m_bag.back());
    }
}

const MusicTrack *MusicPlaylist::next()
{
    if (m_tracks.empty()) {
        return nullptr;
    }

    if (m_hasHistoryPosition && m_historyPosition + 1U < m_history.size()) {
        ++m_historyPosition;
        return current();
    }

    if (m_bag.empty()) {
        refillBag();
    }
    const std::size_t index = m_bag.back();
    m_bag.pop_back();
    m_history.push_back(index);
    m_historyPosition = m_history.size() - 1U;
    m_hasHistoryPosition = true;
    return current();
}

const MusicTrack *MusicPlaylist::previous()
{
    if (!m_hasHistoryPosition || m_history.empty()) {
        return nullptr;
    }
    if (m_historyPosition > 0U) {
        --m_historyPosition;
    }
    return current();
}

const MusicTrack *MusicPlaylist::current() const
{
    if (!m_hasHistoryPosition || m_historyPosition >= m_history.size()) {
        return nullptr;
    }
    const std::size_t index = m_history[m_historyPosition];
    return index < m_tracks.size() ? &m_tracks[index] : nullptr;
}

void MusicPlaylist::discardCurrent()
{
    const MusicTrack *badTrack = current();
    if (!badTrack) {
        return;
    }
    const std::string badKey = badTrack->key();
    m_tracks.erase(
        std::remove_if(m_tracks.begin(), m_tracks.end(), [&](const MusicTrack &track) {
            return track.key() == badKey;
        }),
        m_tracks.end());
    m_bag.clear();
    m_history.clear();
    m_historyPosition = 0;
    m_hasHistoryPosition = false;
}

std::vector<MusicTrack> MusicPlaylist::discoverExternalTracks(const std::filesystem::path &directory)
{
    std::vector<MusicTrack> result;
    std::error_code error;
    if (!std::filesystem::is_directory(directory, error)) {
        return result;
    }

    for (const auto &entry : std::filesystem::directory_iterator(directory, error)) {
        if (error || !entry.is_regular_file(error)) {
            continue;
        }
        if (isSupportedMusicFile(entry.path())) {
            result.push_back(MusicTrack{-1, entry.path()});
        }
    }
    std::sort(result.begin(), result.end(), [](const MusicTrack &left, const MusicTrack &right) {
        return lowerAscii(left.key()) < lowerAscii(right.key());
    });
    return result;
}

bool MusicPlaylist::isSupportedMusicFile(const std::filesystem::path &file)
{
    const std::string extension = lowerAscii(utf8String(file.extension()));
    return extension == ".ogg" || extension == ".mp3" || extension == ".wav" || extension == ".flac";
}
