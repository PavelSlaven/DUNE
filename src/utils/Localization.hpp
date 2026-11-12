#pragma once

#include <format>
#include <string>
#include <string_view>

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
