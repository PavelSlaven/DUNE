include(CheckCXXSourceCompiles)

unset(D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER CACHE)
set(CMAKE_REQUIRED_INCLUDES
    "${CMAKE_CURRENT_SOURCE_DIR}/src"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
    ${SDL2_INCLUDE_DIRS}
)
set(CMAKE_REQUIRED_DEFINITIONS -DSDL_MAIN_HANDLED=1)
check_cxx_source_compiles(
    "#include <type_traits>\n#include \"drawers/SDLDrawer.hpp\"\nstatic_assert(std::is_same_v<decltype(&SDLDrawer::renderStrechSpriteF), void (SDLDrawer::*)(Texture *, cRectangle, SDL_FRect, Uint8, SDL_BlendMode)>);\nint main() { return 0; }"
    D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER
)
unset(CMAKE_REQUIRED_INCLUDES)
unset(CMAKE_REQUIRED_DEFINITIONS)
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/SDLDrawer.hpp" D2TM_UNIT_FRAME_DRAWER_HEADER)
if(D2TM_UNIT_FRAME_DRAWER_HEADER MATCHES "renderStrechSpriteF" AND
   NOT D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER)
    message(FATAL_ERROR
        "D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER failed for ${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/SDLDrawer.hpp containing renderStrechSpriteF"
    )
endif()

set(D2TM_UNIT_FRAME_ENGINE_SRC ${D2TM_SRC})
list(REMOVE_ITEM D2TM_UNIT_FRAME_ENGINE_SRC
    "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/SDLDrawer.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/cTextDrawer.cpp"
)

add_library(d2tm_unit_frame_engine STATIC ${D2TM_UNIT_FRAME_ENGINE_SRC})
target_include_directories(d2tm_unit_frame_engine
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
        "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
)
if(APPLE)
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        target_compile_definitions(d2tm_unit_frame_engine PRIVATE D2TM_CLANG=1)
    endif()
    target_link_libraries(d2tm_unit_frame_engine
        PUBLIC
            ${SDL2_LIBRARIES}
            ${SDL2_IMAGE_LIBRARIES}
            ${SDL2_TTF_LIBRARIES}
            ${SDL2_MIXER_LIBRARIES}
    )
endif()

set_source_files_properties(
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitFrameFixture.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitFrameInteractionsTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitDrawRegressionTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/ZoomStartTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/BuildingRectangleTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/PlacementFrameTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/MouseCellScanTests.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/MouseCellRefreshTests.cpp"
    PROPERTIES COMPILE_OPTIONS "$<$<COMPILE_LANG_AND_ID:CXX,GNU,Clang,AppleClang>:-fno-access-control>"
)

function(add_unit_frame_test target test_name source_file mode)
    if(mode STREQUAL "recorded")
        add_executable(${target}
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/${source_file}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitFrameFixture.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitDrawRecorder.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitTextRecorder.cpp"
        )
        target_link_libraries(${target} PRIVATE d2tm_unit_frame_engine)
        if(D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER)
            target_compile_definitions(${target} PRIVATE D2TM_UNIT_FRAME_HAS_FRACTIONAL_DRAWER=1)
        endif()
    elseif(mode STREQUAL "real")
        add_executable(${target}
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/${source_file}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitFrameFixture.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/SDLDrawer.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/drawers/cTextDrawer.cpp"
        )
        target_link_libraries(${target} PRIVATE d2tm_unit_frame_engine)
    else()
        message(FATAL_ERROR "Unknown unit frame test mode: ${mode}")
    endif()

    target_include_directories(${target}
        PRIVATE
            "${CMAKE_CURRENT_SOURCE_DIR}/src"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
            "${CMAKE_CURRENT_SOURCE_DIR}/tests"
    )
    target_compile_definitions(${target}
        PRIVATE
            D2TM_UNIT_FRAME_FIXTURE_ROOT="${CMAKE_CURRENT_BINARY_DIR}/unit-frame-fixtures/${target}"
    )
    target_compile_definitions(${target} PRIVATE SDL_MAIN_HANDLED=1)
    add_test(NAME ${test_name} COMMAND ${target})
    set_tests_properties(${test_name} PROPERTIES
        ENVIRONMENT "SDL_VIDEODRIVER=dummy;SDL_RENDER_DRIVER=software;SDL_AUDIODRIVER=dummy"
    )
endfunction()

add_executable(unit_sprite_layout_tests
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/UnitSpriteLayoutTests.cpp"
)
target_link_libraries(unit_sprite_layout_tests PRIVATE d2tm_unit_frame_engine)
target_include_directories(unit_sprite_layout_tests
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
        "${CMAKE_CURRENT_SOURCE_DIR}/src/include"
        "${CMAKE_CURRENT_SOURCE_DIR}/tests"
)
target_compile_definitions(unit_sprite_layout_tests PRIVATE SDL_MAIN_HANDLED=1)
add_test(NAME unit_sprite_layout COMMAND unit_sprite_layout_tests)
set_tests_properties(unit_sprite_layout PROPERTIES
    ENVIRONMENT "SDL_VIDEODRIVER=dummy;SDL_RENDER_DRIVER=software;SDL_AUDIODRIVER=dummy"
)

add_unit_frame_test(unit_hd_frame_draw_tests unit_hd_frame_draw UnitHdFrameDrawTests.cpp recorded)
add_unit_frame_test(unit_frame_interactions_tests unit_frame_interactions UnitFrameInteractionsTests.cpp recorded)
add_unit_frame_test(unit_draw_regression_tests unit_draw_regression UnitDrawRegressionTests.cpp recorded)
add_unit_frame_test(unit_render_pixels_tests unit_render_pixels UnitRenderPixelsTests.cpp real)
add_unit_frame_test(zoom_start_tests zoom_start ZoomStartTests.cpp recorded)
add_unit_frame_test(building_visual_rectangle_tests building_visual_rectangle BuildingRectangleTests.cpp recorded)
add_unit_frame_test(placement_frame_tests placement_frame PlacementFrameTests.cpp recorded)
add_unit_frame_test(mouse_cell_scan_tests mouse_cell_scan MouseCellScanTests.cpp recorded)
add_unit_frame_test(mouse_cell_refresh_tests mouse_cell_refresh MouseCellRefreshTests.cpp recorded)
add_unit_frame_test(mouse_click_init_tests mouse_click_init MouseClickInitTests.cpp recorded)
