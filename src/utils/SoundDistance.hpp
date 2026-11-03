#pragma once

[[nodiscard]] constexpr float soundZoomRelativeToWorldScale(float zoomLevel, float worldScaleFactor)
{
    return zoomLevel / worldScaleFactor;
}

[[nodiscard]] constexpr float soundMaxDistance(int maxDistanceInPixels, float zoomLevel, float worldScaleFactor)
{
    return (maxDistanceInPixels / 2) / soundZoomRelativeToWorldScale(zoomLevel, worldScaleFactor);
}

[[nodiscard]] constexpr float soundVolumeFactor(float zoomLevel, float worldScaleFactor)
{
    return 0.7f * soundZoomRelativeToWorldScale(zoomLevel, worldScaleFactor);
}
