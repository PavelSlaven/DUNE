#pragma once

#include <format>
#include <string>
#include <string_view>

// UI screens are constructed after settings have been applied.  Keeping the
// selected locale here avoids repeatedly parsing settings.ini while drawing.
namespace localization {

inline bool english = false;

inline void setLanguage(const std::string_view language)
{
    english = language == "en" || language == "EN";
}

[[nodiscard]] inline const char *text(
    const char *englishText,
    const char *russianText)
{
    return english ? englishText : russianText;
}

[[nodiscard]] inline bool isEnglish()
{
    return english;
}

[[nodiscard]] inline const char *campaignRoot()
{
    return english ? "campaign_en" : "campaign";
}

template<typename... Args>
[[nodiscard]] inline std::string format(
    const char *englishFormat,
    const char *russianFormat,
    Args&&... args)
{
    return std::vformat(
        text(englishFormat, russianFormat),
        std::make_format_args(args...));
}

} // namespace localization
