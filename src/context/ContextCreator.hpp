#pragma once

#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <memory>

class cFileValidator;
class GraphicsContext;
class Graphics;
class TextContext;
class cTextDrawer;

class ContextCreator {
public:
    ContextCreator(
        SDL_Renderer *renderer,
        cFileValidator *settingsValidator,
        int assetDensity = 1
    );
    ContextCreator() = delete;
    ~ContextCreator();

    std::unique_ptr<GraphicsContext> createGraphicsContext();
    std::unique_ptr<TextContext> createTextContext();

private:
    std::shared_ptr<Graphics> gfxmentat;
    std::shared_ptr<Graphics> gfxworld;
    std::shared_ptr<Graphics> gfxinter;
    std::shared_ptr<Graphics> gfxdata;

    TTF_Font *game_font = nullptr; 	// arrakeen.fon
    TTF_Font *bene_font = nullptr;	// benegesserit font.
    TTF_Font *small_font = nullptr;	// small font.
    TTF_Font *menu_font = nullptr;   // larger menu and adaptive UI font.
    TTF_Font *mentat_hd_font = nullptr; // dedicated Cyrillic remaster font.
    TTF_Font *game_fallback_font = nullptr;
    TTF_Font *bene_fallback_font = nullptr;
    TTF_Font *small_fallback_font = nullptr;
    TTF_Font *menu_fallback_font = nullptr;
    TTF_Font *mentat_hd_fallback_font = nullptr;
    int density = 1;
};
