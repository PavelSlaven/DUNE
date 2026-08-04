#include "audio/MusicController.h"

#include "utils/cLog.h"
#include "utils/cSoundPlayer.h"

#include <format>

namespace {
std::size_t indexOf(MusicCategory category)
{
    return static_cast<std::size_t>(category);
}

std::string utf8String(const std::filesystem::path &path)
{
    const auto value = path.u8string();
    return std::string(value.begin(), value.end());
}
}

MusicController::MusicController(cSoundPlayer *soundPlayer, const std::filesystem::path &gameDirectory)
    : m_soundPlayer(soundPlayer), m_gameDirectory(gameDirectory.empty() ? std::filesystem::current_path() : gameDirectory)
{
}

void MusicController::configure(
    MusicCategory category,
    const std::filesystem::path &relativeDirectory,
    std::vector<int> fallbackIds)
{
    CategoryState &state = m_categories[indexOf(category)];
    state.directory = m_gameDirectory / relativeDirectory;
    state.fallback.clear();
    for (const int id : fallbackIds) {
        state.fallback.push_back(MusicTrack{id, {}});
    }

    std::error_code directoryError;
    if (std::filesystem::is_directory(state.directory, directoryError)) {
        for (const auto &entry : std::filesystem::directory_iterator(state.directory, directoryError)) {
            std::error_code fileError;
            if (!directoryError && entry.is_regular_file(fileError) && !fileError &&
                !MusicPlaylist::isSupportedMusicFile(entry.path())) {
                cLogger::getInstance()->log(
                    LOG_WARN,
                    COMP_SOUND,
                    "Custom music skipped",
                    std::format("{}: unsupported file type", utf8String(entry.path())));
            }
        }
    }

    const std::vector<MusicTrack> customTracks = MusicPlaylist::discoverExternalTracks(state.directory);
    state.usingCustom = !customTracks.empty();
    state.playlist.setTracks(state.usingCustom ? customTracks : state.fallback);
    cLogger::getInstance()->log(
        LOG_INFO,
        COMP_SOUND,
        "Music pool",
        std::format(
            "{}: {} custom track(s){}",
            utf8String(state.directory),
            customTracks.size(),
            state.usingCustom ? "" : "; using built-in fallback"));
}

void MusicController::activate(MusicCategory category, bool advanceOnRepeatedEntry)
{
    const bool repeated = m_hasActiveCategory && m_activeCategory == category;
    m_activeCategory = category;
    m_hasActiveCategory = true;
    if (!repeated || advanceOnRepeatedEntry || !m_soundPlayer->isMusicPlaying()) {
        playNextAvailable(false);
    }
}

void MusicController::update()
{
    if (m_hasActiveCategory && !m_soundPlayer->isMusicPlaying()) {
        playNextAvailable(false);
    }
}

void MusicController::next()
{
    if (m_hasActiveCategory) {
        playNextAvailable(false);
    }
}

void MusicController::previous()
{
    if (m_hasActiveCategory) {
        playNextAvailable(true);
    }
}

void MusicController::replayCurrent()
{
    if (!m_hasActiveCategory) {
        return;
    }
    const MusicTrack *track = activeState().playlist.current();
    if (!track || !play(track)) {
        playNextAvailable(false);
    }
}

void MusicController::stop()
{
    m_soundPlayer->stopMusic();
}

std::string MusicController::currentDisplayName() const
{
    if (!m_hasActiveCategory) {
        return {};
    }
    const MusicTrack *track = activeState().playlist.current();
    return track ? track->displayName() : std::string{};
}

bool MusicController::play(const MusicTrack *track)
{
    if (!track) {
        return false;
    }
    if (!track->isExternal()) {
        m_soundPlayer->playMusic(track->builtInId);
        return true;
    }

    std::string error;
    if (m_soundPlayer->playMusicFile(track->externalPath, error)) {
        return true;
    }
    cLogger::getInstance()->log(
        LOG_WARN,
        COMP_SOUND,
        "Custom music skipped",
        std::format("{}: {}", utf8String(track->externalPath), error));
    return false;
}

void MusicController::playNextAvailable(bool backwards)
{
    CategoryState &state = activeState();
    std::size_t remainingAttempts = state.playlist.size();
    while (remainingAttempts-- > 0U) {
        const MusicTrack *track = backwards ? state.playlist.previous() : state.playlist.next();
        if (play(track)) {
            return;
        }
        state.playlist.discardCurrent();
        backwards = false;
    }

    if (state.usingCustom) {
        cLogger::getInstance()->log(
            LOG_WARN,
            COMP_SOUND,
            "Music pool fallback",
            std::format("No playable custom music in {}; using built-in music", utf8String(state.directory)));
        switchToFallback(state);
        if (play(state.playlist.next())) {
            return;
        }
    }
    m_soundPlayer->stopMusic();
}

void MusicController::switchToFallback(CategoryState &state)
{
    state.usingCustom = false;
    state.playlist.setTracks(state.fallback);
}

MusicController::CategoryState &MusicController::activeState()
{
    return m_categories[indexOf(m_activeCategory)];
}

const MusicController::CategoryState &MusicController::activeState() const
{
    return m_categories[indexOf(m_activeCategory)];
}
