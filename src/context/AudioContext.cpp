/**
 * @file AudioContext.cpp
 *
 * Dune 2 - The Maker
 *
 * @author Stefan Hendriks & the D2TM Team
 * @www http://www.dune2themaker.com
 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
 * @license This software is released under the MIT License. See LICENSE.md.
 *
 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
 *
 * This is a non-commercial educational project.
 */

#include "AudioContext.hpp"

#include "audio/MusicController.h"
#include "audio/MusicTransitionPolicy.hpp"
#include "game/cGameSettings.h"
#include "utils/cSoundPlayer.h"
#include "utils/Log.h"
#include "include/definitions.h"
#include "data/gfxaudio.h"
#include "include/cAssert.h"

#include <format>
#include <array>
#include <filesystem>
#include <vector>

namespace {
const char* musicTypeName(eMusicType type)
{
    switch (type) {
    case eMusicType::WIN: return "WIN";
    case eMusicType::LOSE: return "LOSE";
    case eMusicType::ATTACK: return "ATTACK";
    case eMusicType::PEACE: return "PEACE";
    case eMusicType::MENU: return "MENU";
    case eMusicType::CONQUEST: return "CONQUEST";
    case eMusicType::BRIEFING: return "BRIEFING";
    }
    return "UNKNOWN";
}
} // namespace

AudioContext::AudioContext(std::unique_ptr<cSoundPlayer> soundPlayer, cGameSettings* settings) :
    m_soundPlayer(std::move(soundPlayer)),
    m_settings(settings)
{
    d2tm_assert(m_soundPlayer != nullptr);
    d2tm_assert(m_settings != nullptr);
    const std::filesystem::path gameDirectory = std::filesystem::current_path();
    struct MusicPool {
        MusicCategory category;
        const char *directory;
        std::vector<int> fallbackIds;
    };
    const std::array<MusicPool, 8> pools{{
        {MusicCategory::Gameplay, "music/gameplay",
         {MIDI_BUILDING01, MIDI_BUILDING02, MIDI_BUILDING03, MIDI_BUILDING04, MIDI_BUILDING05,
          MIDI_BUILDING06, MIDI_BUILDING07, MIDI_BUILDING08, MIDI_BUILDING09}},
        {MusicCategory::Menu, "music/menu", {MIDI_MENU}},
        {MusicCategory::Conquest, "music/conquest", {MIDI_SCENARIO}},
        {MusicCategory::BriefingAtreides, "music/briefing/atreides", {MIDI_MENTAT_ATR}},
        {MusicCategory::BriefingHarkonnen, "music/briefing/harkonnen", {MIDI_MENTAT_HAR}},
        {MusicCategory::BriefingOrdos, "music/briefing/ordos", {MIDI_MENTAT_ORD}},
        {MusicCategory::Victory, "music/victory", {MIDI_WIN01, MIDI_WIN02, MIDI_WIN03}},
        {MusicCategory::Defeat, "music/defeat", {MIDI_LOSE01, MIDI_LOSE02, MIDI_LOSE03}},
    }};
    for (const MusicPool &pool : pools) {
        std::error_code createError;
        std::filesystem::create_directories(gameDirectory / pool.directory, createError);
        if (createError) {
            Logger::warn(COMP_SOUND, "Music directory", "Could not create {}: {}",
                         (gameDirectory / pool.directory).string(), createError.message());
        }
    }
    m_musicController = std::make_unique<MusicController>(m_soundPlayer.get(), gameDirectory);
    for (const MusicPool &pool : pools) {
        m_musicController->configure(pool.category, pool.directory, pool.fallbackIds);
    }
}

AudioContext::~AudioContext() = default;

cSoundPlayer* AudioContext::getSoundPlayer() const
{
    return m_soundPlayer.get();
}

void AudioContext::playSound(int sampleId) const
{
    m_soundPlayer->playSound(sampleId);
}

void AudioContext::playSound(int sampleId, int vol) const
{
    m_soundPlayer->playSound(sampleId, vol);
}

void AudioContext::playVoice(int sampleId, int house) const
{
    m_soundPlayer->playVoice(sampleId, house);
}

int AudioContext::getMaxVolume() const
{
    return m_soundPlayer->getMaxVolume();
}

void AudioContext::playMusicByTypeForStateTransition(eMusicType iType, int humanHouse)
{
    playMusicByType(iType, false, false, humanHouse);
}

bool AudioContext::playMusicByType(eMusicType iType, bool triggerWithVoice, bool isCurrentlyPlayingMission, int humanHouse)
{
    Logger::info(COMP_SOUND, "AudioContext::playMusicByType", "iType = {}. triggerWithVoice = {}", musicTypeName(iType), triggerWithVoice);

    if (iType == eMusicType::ATTACK) {
        iType = eMusicType::PEACE;
    }
    const bool repeatedCategory = m_settings->getMusicType() == iType;
    m_settings->setMusicType(iType);
    Logger::info(COMP_SOUND, "AudioContext::playMusicByType", "m_musicType = {}", musicTypeName(iType));

    const MusicCategory category = musicCategoryFor(iType, humanHouse);
    if (!m_settings->isPlayMusic()) {
        m_musicController->selectCategory(category);
        return false;
    }
    m_musicController->activate(category, shouldAdvanceRepeatedMusicCategory(repeatedCategory, isCurrentlyPlayingMission));
    return true;
}

void AudioContext::thinkFast()
{
    if (!m_settings->isPlayMusic()) {
        return;
    }
    m_musicController->update();
}

void AudioContext::toggleMusic()
{
    setMusicEnabled(!m_settings->isPlayMusic());
}

void AudioContext::setMusicEnabled(bool enabled)
{
    m_settings->setPlayMusic(enabled);
    m_soundPlayer->setMusicEnabled(enabled);
    if (enabled) {
        m_musicController->replayCurrent();
    }
    else {
        m_musicController->stop();
    }
}

void AudioContext::playPreviousTrack()
{
    if (m_settings->isPlayMusic()) {
        m_musicController->previous();
    }
}

void AudioContext::playNextTrack()
{
    if (m_settings->isPlayMusic()) {
        m_musicController->next();
    }
}

std::string AudioContext::getCurrentMusicTrackName() const
{
    return m_musicController->currentDisplayName();
}

void AudioContext::changeMusicVolume(int delta) const
{
    m_soundPlayer->changeMusicVolume(delta);
}
