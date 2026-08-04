cmake_minimum_required(VERSION 3.21)

set(CMAKE_CXX_STANDARD 20)

project(d2tm)

include(CTest)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "No build type selected, defaulting to Debug")
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

if(DEFINED ENV{ENV_D2TM_VERSION})
    SET(D2TM_VERSION "$ENV{ENV_D2TM_VERSION}")
elseif(DEFINED ENV{GITHUB_SHA})
    SET(D2TM_VERSION "$ENV{GITHUB_SHA}")
else()
    SET(D2TM_VERSION "unset")
endif()

message(STATUS "D2TM-Version determined to be: ${D2TM_VERSION}")

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

CONFIGURE_FILE (
  "${CMAKE_CURRENT_SOURCE_DIR}/src/include/config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/include/config.h"
)

if(APPLE)
    message(STATUS "Using pkg-config to locate SDL2 libraries on macOS")

    find_package(PkgConfig REQUIRED)

    pkg_check_modules(SDL2 REQUIRED sdl2)
    pkg_check_modules(SDL2_IMAGE REQUIRED SDL2_image)
    pkg_check_modules(SDL2_TTF REQUIRED SDL2_ttf)
    pkg_check_modules(SDL2_MIXER REQUIRED SDL2_mixer)

    if(EXISTS "/opt/homebrew/bin/brew")
        set(HOMEBREW_PREFIX "/opt/homebrew")
    else()
        set(HOMEBREW_PREFIX "/usr/local")
    endif()

    set(CMAKE_PREFIX_PATH
            "${HOMEBREW_PREFIX}"
            # These libraries are keg-only and not loaded into
            # the root prefix by default (to avoid clashes).
            "${HOMEBREW_PREFIX}/opt/lapack"
            "${HOMEBREW_PREFIX}/opt/openblas"
            "${HOMEBREW_PREFIX}/opt/gcc/lib/gcc/15"
    )

    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "arm64")
        message(STATUS "Apple Silicon (arm64)")
        set(CMAKE_C_COMPILER "${HOMEBREW_PREFIX}/bin/gcc-15")
        set(CMAKE_CXX_COMPILER "${HOMEBREW_PREFIX}/bin/g++-15")
    elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        message(STATUS "Apple Intel X64")
        set(CMAKE_C_COMPILER "clang")
        set(CMAKE_CXX_COMPILER "clang++")
    endif()

    message(STATUS "Mac GCC C compiler: ${CMAKE_C_COMPILER}")
    message(STATUS "Mac GCC C++ compiler: ${CMAKE_CXX_COMPILER}")

    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        add_compile_options(-stdlib=libstdc++)
        add_link_options(-stdlib=libstdc++)
    endif()

    include_directories(
      ${SDL2_INCLUDE_DIRS}
      ${SDL2_IMAGE_INCLUDE_DIRS}
      ${SDL2_TTF_INCLUDE_DIRS}
      ${SDL2_MIXER_INCLUDE_DIRS}
    )

    link_directories(
      ${SDL2_LIBRARY_DIRS}
      ${SDL2_IMAGE_LIBRARY_DIRS}
      ${SDL2_TTF_LIBRARY_DIRS}
      ${SDL2_MIXER_LIBRARY_DIRS}
    )

else()
    message(STATUS "Using CMake's find_package to locate SDL2 libraries")

    find_package(SDL2 REQUIRED)
    find_package(SDL2_ttf REQUIRED)
    find_package(SDL2_image REQUIRED)
    find_package(SDL2_mixer REQUIRED)

    link_libraries(SDL2 SDL2_ttf SDL2_mixer SDL2_image)
endif()

add_subdirectory(src)

add_executable(${PROJECT_NAME} ${D2TM_SRC} Script.rc)

target_include_directories(${PROJECT_NAME}
	PRIVATE
    	${CMAKE_CURRENT_SOURCE_DIR}/src
    	${CMAKE_CURRENT_SOURCE_DIR}/src/include
        /usr/local/include/SDL2
        /usr/local/include
)

if (APPLE)

    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "arm64")
    elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        target_compile_definitions(${PROJECT_NAME} PRIVATE D2TM_CLANG=1)
    endif()

    target_link_libraries(${PROJECT_NAME}
        PRIVATE
            ${SDL2_LIBRARIES}
            ${SDL2_IMAGE_LIBRARIES}
            ${SDL2_TTF_LIBRARIES}
            ${SDL2_MIXER_LIBRARIES}
    )
    target_compile_options(${PROJECT_NAME}
      PRIVATE
        ${D2TM_OPTMIZATION}
        "-Wall"
        "-Wextra"
        "-Wpedantic"
        "-Wzero-as-null-pointer-constant"
        "-Wextra-semi"
    )
elseif (UNIX)
    target_compile_options(${PROJECT_NAME}
      PRIVATE
        ${D2TM_OPTMIZATION}
        "-Wall"
        "-Wextra"
        "-Wno-dangling-reference"
        "-Wpedantic"
        "-Wuseless-cast"
        "-Wredundant-tags"
        "-Wzero-as-null-pointer-constant"
        "-Wextra-semi"
        #"-Wsuggest-override"
        #"-Wmismatched-tags"
        #"-Wdeprecated-declarations"
    )
else()
    target_compile_options(${PROJECT_NAME}
      PRIVATE
        ${D2TM_OPTMIZATION}
        "-Wall"
        "-Wextra"
        "-Wno-dangling-reference"
        "-Wpedantic"
        "-Wuseless-cast"
        "-Wredundant-tags"
        "-Wzero-as-null-pointer-constant"
        "-Wextra-semi"
    )
  	target_link_libraries(${PROJECT_NAME}
  	PRIVATE
    # fmt::fmt
    -static-libgcc
    -static-libstdc++
    -lmingw32
    -lSDL2main
    -lSDL2
    -mwindows
  )
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

if(BUILD_TESTING)
    add_executable(
        command_bindings_tests
        tests/CommandBindingsTests.cpp
        src/controls/cKeyboardEvent.cpp
    )
    target_include_directories(
        command_bindings_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME command_bindings COMMAND command_bindings_tests)

    add_executable(
        render_scale_tests
        tests/RenderScaleTests.cpp
        src/utils/RenderScale.cpp
    )
    target_include_directories(
        render_scale_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME render_scale_calculations COMMAND render_scale_tests)

    add_executable(
        graphics_mode_tests
        tests/GraphicsModeTests.cpp
    )
    target_include_directories(
        graphics_mode_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME graphics_mode_selection COMMAND graphics_mode_tests)

    add_executable(
        hud_layout_tests
        tests/HudLayoutTests.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        hud_layout_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME hud_layout_geometry COMMAND hud_layout_tests)

    add_executable(
        options_menu_layout_tests
        tests/OptionsMenuLayoutTests.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        options_menu_layout_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME options_menu_layout_geometry COMMAND options_menu_layout_tests)

    add_executable(
        command_bar_layout_tests
        tests/CommandBarLayoutTests.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        command_bar_layout_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME command_bar_layout_geometry COMMAND command_bar_layout_tests)

    add_executable(
        terrain_variation_tests
        tests/TerrainVariationTests.cpp
    )
    target_include_directories(
        terrain_variation_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME terrain_variation_selection COMMAND terrain_variation_tests)

    add_executable(
        world_scale_tests
        tests/WorldScaleTests.cpp
        src/utils/WorldScale.cpp
    )
    target_include_directories(
        world_scale_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME world_scale_selection COMMAND world_scale_tests)

    add_executable(
        world_object_scale_tests
        tests/WorldObjectScaleTests.cpp
    )
    target_include_directories(
        world_object_scale_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME world_object_scale_selection COMMAND world_object_scale_tests)

    add_executable(
        hd_presentation_tests
        tests/HdPresentationTests.cpp
    )
    target_include_directories(
        hd_presentation_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME hd_presentation_selection COMMAND hd_presentation_tests)

    add_executable(
        campaign_map_layout_tests
        tests/CampaignMapLayoutTests.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        campaign_map_layout_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME campaign_map_layout_geometry COMMAND campaign_map_layout_tests)

    add_executable(
        render_target_state_tests
        tests/RenderTargetStateTests.cpp
        src/drawers/SDLDrawer.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        render_target_state_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME render_target_state_restoration COMMAND render_target_state_tests)

    add_executable(
        save_file_codec_tests
        tests/SaveFileCodecTests.cpp
        src/save/SaveFileCodec.cpp
    )
    target_include_directories(
        save_file_codec_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME save_file_codec_roundtrip COMMAND save_file_codec_tests)

    add_executable(
        save_slot_name_tests
        tests/SaveSlotNameTests.cpp
    )
    target_include_directories(
        save_slot_name_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME save_slot_name_handling COMMAND save_slot_name_tests)

    add_executable(
        music_playlist_tests
        tests/MusicPlaylistTests.cpp
        src/audio/MusicPlaylist.cpp
    )
    target_include_directories(
        music_playlist_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME music_playlist_shuffle_history COMMAND music_playlist_tests)

    add_executable(
        music_transition_policy_tests
        tests/MusicTransitionPolicyTests.cpp
    )
    target_include_directories(
        music_transition_policy_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
    )
    add_test(NAME music_transition_policy COMMAND music_transition_policy_tests)

    add_executable(
        music_controls_layout_tests
        tests/MusicControlsLayoutTests.cpp
        src/utils/cRectangle.cpp
    )
    target_include_directories(
        music_controls_layout_tests
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    )
    add_test(NAME music_controls_layout_geometry COMMAND music_controls_layout_tests)
endif()
