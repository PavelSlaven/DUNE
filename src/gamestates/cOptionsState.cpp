#include "cOptionsState.h"

#include "d2tmc.h"
#include "config.h"

#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "gui/GuiLabel.hpp"
#include "gui/GuiCheckBox.hpp"
#include "gui/GuiSlider.hpp"
#include "context/GameContext.hpp"
#include "gamestates/AdvancedOptionsHeaderLayout.hpp"
#include "gamestates/OptionsMenuLayout.hpp"
#include "save/SaveGameManager.hpp"
#include "save/SaveSlotsDialog.hpp"
#include "utils/GameSettings.hpp"
#include "utils/RenderScale.hpp"
#include "utils/WorldScale.hpp"
#include "utils/common.h"
#include "utils/cLog.h"
#include "utils/cSoundPlayer.h"

#include <SDL2/SDL.h>

#include <algorithm>
#include <array>
#include <cmath>
#include <format>

namespace {
std::string optionText(const GameSettings &settings,
                       std::string_view english,
                       std::string_view russian)
{
    return std::string(settings.language == "en" ? english : russian);
}

bool isEnglishLanguage(const GameSettings &settings)
{
    return settings.language == "en";
}
}

cOptionsState::cOptionsState(cGame &theGame, GameContext *ctx, int prevState)
    : cGameState(theGame, ctx),
    m_textDrawer(
        theGame.isHdGraphicsActive()
            ? ctx->getTextContext()->getMenuTextDrawer()
            : ctx->getTextContext()->getBeneTextDrawer()
    ),
    m_hdLayout(theGame.isHdGraphicsActive()),
    m_prevState(prevState),
    m_guiWindow(nullptr)
{
    initializeDisplaySettings();
    m_saveDialog = std::make_unique<SaveSlotsDialog>(
        m_game,
        m_textDrawer,
        [this]() {
            m_game.initiateFadingOut();
        },
        [this]() {
            if (!m_loadGameButton) {
                return;
            }
            m_loadGameButton->setEnabled(true);
            m_loadGameButton->setTheme(
                m_hdLayout ? GuiTheme::Remaster() : GuiTheme::Light()
            );
        }
    );
    refresh();
    m_backgroundTexture = m_game.getScreenTexture();
}

void cOptionsState::initializeDisplaySettings()
{
    const std::unique_ptr<GameSettings> settings = loadSettingsFromIni("settings.ini");
    m_selectedSettings = *settings;
    if (m_selectedSettings.language != "en" && m_selectedSettings.language != "ru") {
        m_selectedSettings.language = "ru";
    }
    m_savedLanguage = m_selectedSettings.language;
    m_savedResolution = {settings->screenW, settings->screenH};
    m_savedRenderScalePercent = settings->renderScalePercent;
    m_savedWorldScalePercent = isWorldScaleSupported(
        settings->worldScalePercent
    ) ? settings->worldScalePercent : AutomaticWorldScale;
    m_savedFullscreen = !settings->windowed;
    m_selectedFullscreen = m_savedFullscreen;
    m_savedGraphicsMode = settings->graphicsMode;
    m_selectedGraphicsMode = m_savedGraphicsMode;
    m_worldScaleOptions.assign(
        ManualWorldScales.begin(),
        ManualWorldScales.end()
    );
    m_worldScaleOptions.insert(
        m_worldScaleOptions.begin(),
        AutomaticWorldScale
    );
    const auto selectedWorldScale = std::find(
        m_worldScaleOptions.begin(),
        m_worldScaleOptions.end(),
        m_savedWorldScalePercent
    );
    m_selectedWorldScaleIndex = selectedWorldScale ==
            m_worldScaleOptions.end()
        ? 0
        : static_cast<std::size_t>(
            std::distance(m_worldScaleOptions.begin(), selectedWorldScale)
        );

    SDL_DisplayMode desktopMode{};
    int desktopWidth = m_game.m_screenW;
    int desktopHeight = m_game.m_screenH;
    if (SDL_GetCurrentDisplayMode(0, &desktopMode) == 0) {
        desktopWidth = desktopMode.w;
        desktopHeight = desktopMode.h;
    }

    constexpr std::array<ResolutionOption, 35> standardResolutions{{
        {800, 600},
        {1024, 600},
        {1024, 768},
        {1152, 864},
        {1280, 720},
        {1280, 768},
        {1280, 800},
        {1280, 960},
        {1280, 1024},
        {1360, 768},
        {1366, 768},
        {1440, 900},
        {1600, 900},
        {1600, 1024},
        {1600, 1200},
        {1680, 1050},
        {1920, 1080},
        {1920, 1200},
        {2048, 1080},
        {2048, 1152},
        {2048, 1536},
        {2560, 1080},
        {2560, 1440},
        {2560, 1600},
        {2880, 1620},
        {2880, 1800},
        {3200, 1800},
        {3440, 1440},
        {3840, 1600},
        {3840, 2160},
        {4096, 2160},
        {5120, 1440},
        {5120, 2160},
        {5120, 2880},
        {7680, 4320}
    }};

    const auto addResolution = [this](ResolutionOption resolution) {
        if (std::find(m_resolutionOptions.begin(), m_resolutionOptions.end(), resolution) ==
            m_resolutionOptions.end()) {
            m_resolutionOptions.push_back(resolution);
        }
    };

    m_resolutionOptions.clear();
    for (const ResolutionOption resolution : standardResolutions) {
        if (resolution.width <= desktopWidth && resolution.height <= desktopHeight) {
            addResolution(resolution);
        }
    }
    addResolution(m_savedResolution);
    addResolution({desktopWidth, desktopHeight});

    std::ranges::sort(
        m_resolutionOptions,
        [](const ResolutionOption &left, const ResolutionOption &right) {
            const long long leftPixels =
                static_cast<long long>(left.width) * static_cast<long long>(left.height);
            const long long rightPixels =
                static_cast<long long>(right.width) * static_cast<long long>(right.height);
            if (leftPixels != rightPixels) {
                return leftPixels < rightPixels;
            }
            if (left.width != right.width) {
                return left.width < right.width;
            }
            return left.height < right.height;
        }
    );

    const auto selected = std::find(
        m_resolutionOptions.begin(),
        m_resolutionOptions.end(),
        m_savedResolution
    );
    m_selectedResolutionIndex = static_cast<std::size_t>(
        std::distance(m_resolutionOptions.begin(), selected)
    );
    rebuildRenderScaleOptions(m_savedRenderScalePercent);
}

void cOptionsState::rebuildRenderScaleOptions(int preferredScalePercent)
{
    m_renderScaleOptions.clear();
    m_renderScaleOptions.push_back(AutomaticRenderScale);

    if (!m_resolutionOptions.empty()) {
        const ResolutionOption &resolution =
            m_resolutionOptions[m_selectedResolutionIndex];
        for (const int scalePercent : ManualRenderScales) {
            if (isManualRenderScaleAvailable(
                    resolution.width,
                    resolution.height,
                    scalePercent)) {
                m_renderScaleOptions.push_back(scalePercent);
            }
        }
    }

    const auto preferred = std::find(
        m_renderScaleOptions.begin(),
        m_renderScaleOptions.end(),
        preferredScalePercent
    );
    m_selectedRenderScaleIndex = preferred == m_renderScaleOptions.end()
        ? 0
        : static_cast<std::size_t>(
            std::distance(m_renderScaleOptions.begin(), preferred)
        );
}

void cOptionsState::selectPreviousResolution()
{
    if (m_resolutionOptions.empty()) {
        return;
    }
    if (m_selectedResolutionIndex == 0) {
        m_selectedResolutionIndex = m_resolutionOptions.size() - 1;
    }
    else {
        --m_selectedResolutionIndex;
    }
    const int selectedScale = m_renderScaleOptions.empty()
        ? AutomaticRenderScale
        : m_renderScaleOptions[m_selectedRenderScaleIndex];
    rebuildRenderScaleOptions(selectedScale);
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

void cOptionsState::constructAdvancedWindow(int /*prevState*/)
{
    const int mainMenuWidth = m_hdLayout
        ? std::min(m_game.m_screenW - 32, 760)
        : m_game.m_screenW / 2;
    const int mainMenuHeight = m_hdLayout
        ? std::min(m_game.m_screenH - 32, 560)
        : m_game.m_screenH / 2;
    const int frameX = (m_game.m_screenW - mainMenuWidth) / 2;
    const int frameY = (m_game.m_screenH - mainMenuHeight) / 2;
    const int margin = m_hdLayout ? 8 : 4;
    const int buttonHeight = m_hdLayout
        ? std::max(32, m_textDrawer->getFontHeight() + 10)
        : m_textDrawer->getFontHeight() + margin;
    const int labelWidth = m_hdLayout ? 560 : mainMenuWidth - 80;
    const int checkX = m_hdLayout ? 600 : mainMenuWidth - buttonHeight - margin;
    const GuiTheme theme = m_hdLayout ? GuiTheme::Remaster() : GuiTheme::Light();
    const GuiRenderKind buttonKind = m_hdLayout
        ? GuiRenderKind::REMASTER_BUTTON
        : GuiRenderKind::OPAQUE_WITH_BORDER;

    m_guiWindow = new GuiWindow(
        cRectangle(frameX, frameY, mainMenuWidth, mainMenuHeight),
        m_textDrawer
    );
    m_guiWindow->setTheme(theme);
    m_guiWindow->setTitle(
        optionText(m_selectedSettings, "Dune II - Settings", "Dune II — Настройки")
    );

    const auto addTab = [this, theme, buttonKind, buttonHeight](
                            int x, int y, int width, std::string_view label, OptionsPage page) {
        GuiButton *button = GuiButtonBuilder()
                .withRect(m_guiWindow->getRelativeRect(x, y, width, buttonHeight))
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withTheme(theme)
                .withKind(buttonKind)
                .onClick([this, page]() { requestOptionsPage(page); })
                .build();
        m_guiWindow->addGuiObject(button);
    };
    const AdvancedOptionsHeaderLayout headerLayout =
        AdvancedOptionsHeaderLayout::create(
            mainMenuWidth,
            margin,
            buttonHeight,
            m_textDrawer->getFontHeight()
        );
    addTab(headerLayout.tabs[0].getX(), headerLayout.tabs[0].getY(),
           headerLayout.tabs[0].getWidth(),
           optionText(m_selectedSettings, "Main", "Основные"), OptionsPage::Main);
    addTab(headerLayout.tabs[1].getX(), headerLayout.tabs[1].getY(),
           headerLayout.tabs[1].getWidth(),
           optionText(m_selectedSettings, "Gameplay", "Игра"), OptionsPage::Gameplay);
    addTab(headerLayout.tabs[2].getX(), headerLayout.tabs[2].getY(),
           headerLayout.tabs[2].getWidth(),
           optionText(m_selectedSettings, "Controls", "Управление"), OptionsPage::Controls);
    addTab(headerLayout.tabs[3].getX(), headerLayout.tabs[3].getY(),
           headerLayout.tabs[3].getWidth(),
           optionText(m_selectedSettings, "Diagnostics", "Диагностика"),
           OptionsPage::Diagnostics);

    int row = 2;
    const auto addToggle = [this, &row, theme, labelWidth, checkX, buttonHeight](
                               std::string_view label,
                               bool GameSettings::*field) {
        const int y = row++ * (buttonHeight + 4);
        GuiLabel *name = GuiLabelBuilder()
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, y, labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(name);
        GuiCheckBox *check = GuiCheckBoxBuilder()
                .withRect(m_guiWindow->getRelativeRect(checkX, y, buttonHeight, buttonHeight))
                .withTheme(theme)
                .onCheck([this, field]() { m_selectedSettings.*field = true; })
                .onUnCheck([this, field]() { m_selectedSettings.*field = false; })
                .build();
        check->setChecked(m_selectedSettings.*field);
        m_guiWindow->addGuiObject(check);
    };
    const auto addSpeed = [this, &row, theme, labelWidth, checkX, buttonHeight](
                              std::string_view label, float GameSettings::*field) {
        const int y = row++ * (buttonHeight + 4);
        GuiLabel *name = GuiLabelBuilder()
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, y, labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(name);
        GuiSlider *slider = GuiSliderBuilder()
                .withRect(m_guiWindow->getRelativeRect(checkX - 230, y, 230, buttonHeight))
                .withTheme(theme)
                .withMinValue(1)
                .withMaxValue(10)
                .withInitialValue(std::clamp(
                    static_cast<int>(std::lround((m_selectedSettings.*field) * 10.0f)), 1, 10
                ))
                .onValueChanged([this, field](int value) {
                    m_selectedSettings.*field = static_cast<float>(value) / 10.0f;
                })
                .build();
        m_guiWindow->addGuiObject(slider);
    };

    if (m_optionsPage == OptionsPage::Gameplay) {
        addToggle(optionText(m_selectedSettings,
            "Edge scrolling — move camera at screen edge", "Прокрутка краем — камера у границы экрана"),
            &GameSettings::cameraEdgeMove);
        addSpeed(optionText(m_selectedSettings,
            "Keyboard/edge camera speed", "Скорость камеры клавишами и у края"),
            &GameSettings::cameraBorderOrKeyMoveSpeed);
        addSpeed(optionText(m_selectedSettings,
            "Camera drag speed", "Скорость перетаскивания камеры"),
            &GameSettings::cameraDragMoveSpeed);
        addToggle(optionText(m_selectedSettings,
            "Pause when the window loses focus", "Пауза при потере фокуса окна"),
            &GameSettings::pauseWhenLosingFocus);
        addToggle(optionText(m_selectedSettings,
            "Repeat reinforcements", "Повторять подкрепления"),
            &GameSettings::allowRepeatingReinforcements);
        addToggle(optionText(m_selectedSettings,
            "All turrets stop on low power", "Все башни отключать при нехватке энергии"),
            &GameSettings::turretsDownOnLowPower);
        addToggle(optionText(m_selectedSettings,
            "Rocket turrets stop on low power", "Ракетные башни отключать при нехватке энергии"),
            &GameSettings::rocketTurretsDownOnLowPower);
        GuiLabel *rules = GuiLabelBuilder()
                .withLabel(optionText(m_selectedSettings,
                    "Rules file: game.ini (change manually)",
                    "Файл правил: game.ini (меняется вручную)"))
                .withTextDrawer(m_textDrawer).withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, row++ * (buttonHeight + 4), labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT).build();
        m_guiWindow->addGuiObject(rules);
    }
    else if (m_optionsPage == OptionsPage::Controls) {
        const int bindingButtonWidth = m_hdLayout ? 190 : 105;
        const int bindingButtonX = mainMenuWidth - margin - bindingButtonWidth;
        const auto addBinding = [this, &row, theme, buttonKind, buttonHeight,
                                 bindingButtonX, bindingButtonWidth](
                                    std::string_view label,
                                    std::optional<CommandBindingAction> action) {
            const int y = row++ * (buttonHeight + 4);
            GuiLabel *name = GuiLabelBuilder()
                    .withLabel(std::string(label))
                    .withTextDrawer(m_textDrawer)
                    .withTheme(theme)
                    .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                    .withRect(m_guiWindow->getRelativeRect(
                        16, y, bindingButtonX - 32, buttonHeight))
                    .withTextAlign(GuiTextAlignHorizontal::LEFT)
                    .build();
            m_guiWindow->addGuiObject(name);

            std::string value = optionText(m_selectedSettings, "LMB", "ЛКМ");
            if (action) {
                value = m_bindingCapture == action
                    ? optionText(m_selectedSettings, "Press key...", "Клавиша...")
                    : commandBindingDisplayName(
                        commandBinding(m_selectedSettings.commandBindings, *action),
                        isEnglishLanguage(m_selectedSettings));
            }
            GuiButtonBuilder builder;
            builder.withRect(m_guiWindow->getRelativeRect(
                        bindingButtonX, y, bindingButtonWidth, buttonHeight))
                    .withLabel(value)
                    .withTextDrawer(m_textDrawer)
                    .withTheme(theme)
                    .withKind(buttonKind)
                    .withEnabled(action.has_value());
            if (action) {
                builder.onClick([this, action]() {
                    m_bindingCapture = action;
                    refresh();
                });
            }
            m_guiWindow->addGuiObject(builder.build());
        };

        addBinding(optionText(m_selectedSettings, "Move", "Идти"), std::nullopt);
        addBinding(optionText(m_selectedSettings, "Attack", "Атака"), CommandBindingAction::Attack);
        addBinding(optionText(m_selectedSettings, "Repair", "Ремонт"), CommandBindingAction::Repair);
        addBinding(optionText(m_selectedSettings, "Unload", "Разгрузка"), CommandBindingAction::Unload);
        addBinding(optionText(m_selectedSettings, "Deploy", "Развернуть"), CommandBindingAction::Deploy);
        addBinding(optionText(m_selectedSettings, "Rally", "Сбор"), CommandBindingAction::Rally);
        addBinding(optionText(m_selectedSettings, "Release", "Выпустить"), CommandBindingAction::Release);
    }
    else {
        addToggle(optionText(m_selectedSettings, "Debug mode", "Режим отладки"), &GameSettings::debugMode);
        addToggle(optionText(m_selectedSettings, "Disable all AI", "Отключить весь ИИ"), &GameSettings::disableAI);
        addToggle(optionText(m_selectedSettings, "Use one AI player", "Оставить одного ИИ-игрока"), &GameSettings::oneAi);
        addToggle(optionText(m_selectedSettings, "Disable worm AI", "Отключить ИИ червя"), &GameSettings::disableWormAi);
        addToggle(optionText(m_selectedSettings, "Disable reinforcements", "Отключить подкрепления"), &GameSettings::disableReinforcements);
        addToggle(optionText(m_selectedSettings, "Disable remaining AI", "Отключить оставшийся ИИ"), &GameSettings::noAiRest);
        addToggle(optionText(m_selectedSettings, "Show unit debug data", "Показывать отладку юнитов"), &GameSettings::drawUnitDebug);
        addToggle(optionText(m_selectedSettings, "Show resource usage", "Показывать использование ресурсов"), &GameSettings::drawUsages);
    }

    const int footerY = mainMenuHeight - buttonHeight - margin;
    GuiButton *apply = GuiButtonBuilder()
            .withRect(m_guiWindow->getRelativeRect(16, footerY, m_hdLayout ? 180 : 100, buttonHeight))
            .withLabel(optionText(m_selectedSettings, "Apply", "Применить"))
            .withTextDrawer(m_textDrawer).withTheme(theme).withKind(buttonKind)
            .onClick([this]() {
                m_selectedSettings.playMusic = m_ctx->getSoundPlayer()->getMusicEnabled();
                m_selectedSettings.playSound = m_ctx->getSoundPlayer()->getSoundEnabled();
                std::string error;
                if (!saveSettingsToIni("settings.ini", m_selectedSettings, error)) {
                    cLogger::getInstance()->log(LOG_ERROR, COMP_GAMERULES, "Settings", error);
                }
                else {
                    m_game.m_commandBindings = m_selectedSettings.commandBindings;
                }
            }).build();
    m_guiWindow->addGuiObject(apply);
    GuiButton *back = GuiButtonBuilder()
            .withRect(m_guiWindow->getRelativeRect(
                mainMenuWidth - (m_hdLayout ? 180 : 100) - margin, footerY,
                m_hdLayout ? 180 : 100, buttonHeight
            ))
            .withLabel(optionText(m_selectedSettings, "Back", "Назад"))
            .withTextDrawer(m_textDrawer).withTheme(theme).withKind(buttonKind)
            .onClick([this]() { requestOptionsPage(OptionsPage::Main); })
            .build();
    m_guiWindow->addGuiObject(back);
}

void cOptionsState::selectNextResolution()
{
    if (m_resolutionOptions.empty()) {
        return;
    }
    m_selectedResolutionIndex =
        (m_selectedResolutionIndex + 1) % m_resolutionOptions.size();
    const int selectedScale = m_renderScaleOptions.empty()
        ? AutomaticRenderScale
        : m_renderScaleOptions[m_selectedRenderScaleIndex];
    rebuildRenderScaleOptions(selectedScale);
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

std::string cOptionsState::selectedResolutionText() const
{
    if (m_resolutionOptions.empty()) {
        return optionText(m_selectedSettings, "Unavailable", "Недоступно");
    }
    const ResolutionOption &selected = m_resolutionOptions[m_selectedResolutionIndex];
    return std::format("{}×{}", selected.width, selected.height);
}

void cOptionsState::selectPreviousRenderScale()
{
    if (m_renderScaleOptions.empty()) {
        return;
    }
    if (m_selectedRenderScaleIndex == 0) {
        m_selectedRenderScaleIndex = m_renderScaleOptions.size() - 1;
    }
    else {
        --m_selectedRenderScaleIndex;
    }
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

void cOptionsState::selectNextRenderScale()
{
    if (m_renderScaleOptions.empty()) {
        return;
    }
    m_selectedRenderScaleIndex =
        (m_selectedRenderScaleIndex + 1) % m_renderScaleOptions.size();
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

std::string cOptionsState::selectedRenderScaleText() const
{
    if (m_renderScaleOptions.empty() || m_resolutionOptions.empty()) {
        return optionText(m_selectedSettings, "Unavailable", "Недоступно");
    }

    const int scalePercent = m_renderScaleOptions[m_selectedRenderScaleIndex];
    if (scalePercent != AutomaticRenderScale) {
        return std::format("{}%", scalePercent);
    }

    const ResolutionOption &resolution =
        m_resolutionOptions[m_selectedResolutionIndex];
    return std::format(
        "{} ({}%)",
        optionText(m_selectedSettings, "Auto", "Авто"),
        calculateAutomaticRenderScalePercent(
            resolution.width,
            resolution.height
        )
    );
}

void cOptionsState::selectPreviousWorldScale()
{
    if (m_worldScaleOptions.empty()) {
        return;
    }
    m_selectedWorldScaleIndex = m_selectedWorldScaleIndex == 0
        ? m_worldScaleOptions.size() - 1
        : m_selectedWorldScaleIndex - 1;
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

void cOptionsState::selectNextWorldScale()
{
    if (m_worldScaleOptions.empty()) {
        return;
    }
    m_selectedWorldScaleIndex =
        (m_selectedWorldScaleIndex + 1) % m_worldScaleOptions.size();
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

std::string cOptionsState::selectedWorldScaleText() const
{
    if (m_worldScaleOptions.empty() || m_resolutionOptions.empty()) {
        return optionText(m_selectedSettings, "Unavailable", "Недоступно");
    }
    const int selected = m_worldScaleOptions[m_selectedWorldScaleIndex];
    if (selected != AutomaticWorldScale) {
        return std::format("{}%", selected);
    }
    const int outputHeight =
        m_resolutionOptions[m_selectedResolutionIndex].height;
    return std::format(
        "{} ({}%)",
        optionText(m_selectedSettings, "Auto", "Авто"),
        calculateAutomaticWorldScalePercent(outputHeight)
    );
}

void cOptionsState::toggleGraphicsMode()
{
    m_selectedGraphicsMode =
        m_selectedGraphicsMode == GraphicsMode::Hd
            ? GraphicsMode::Classic
            : GraphicsMode::Hd;
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

std::string cOptionsState::selectedGraphicsModeText() const
{
    return m_selectedGraphicsMode == GraphicsMode::Hd
        ? "HD"
        : optionText(m_selectedSettings, "Classic", "Классика");
}

void cOptionsState::toggleLanguage()
{
    m_selectedSettings.language = isEnglishLanguage(m_selectedSettings) ? "ru" : "en";
    if (m_displayStatusLabel) {
        m_displayStatusLabel->setText("");
    }
    updateDisplayControls();
}

std::string cOptionsState::selectedLanguageText() const
{
    return isEnglishLanguage(m_selectedSettings) ? "English" : "Русский";
}

void cOptionsState::switchOptionsPage(OptionsPage page)
{
    m_bindingCapture.reset();
    m_optionsPage = page;
    refresh();
}

void cOptionsState::requestOptionsPage(OptionsPage page)
{
    m_pendingOptionsPage = page;
}

void cOptionsState::updateDisplaySettingsDirtyState()
{
    if (!m_applyDisplayButton ||
        m_resolutionOptions.empty() ||
        m_renderScaleOptions.empty() ||
        m_worldScaleOptions.empty()) {
        return;
    }
    const bool changed =
        m_resolutionOptions[m_selectedResolutionIndex] != m_savedResolution ||
        m_renderScaleOptions[m_selectedRenderScaleIndex] !=
            m_savedRenderScalePercent ||
        m_worldScaleOptions[m_selectedWorldScaleIndex] !=
            m_savedWorldScalePercent ||
        m_selectedFullscreen != m_savedFullscreen ||
        m_selectedGraphicsMode != m_savedGraphicsMode ||
        m_selectedSettings.language != m_savedLanguage;
    m_applyDisplayButton->setEnabled(changed);
}

void cOptionsState::updateDisplayControls()
{
    if (m_resolutionValueLabel) {
        m_resolutionValueLabel->setText(selectedResolutionText());
    }
    if (m_renderScaleValueLabel) {
        m_renderScaleValueLabel->setText(selectedRenderScaleText());
    }
    if (m_worldScaleValueLabel) {
        m_worldScaleValueLabel->setText(selectedWorldScaleText());
    }
    if (m_graphicsModeValueLabel) {
        m_graphicsModeValueLabel->setText(selectedGraphicsModeText());
    }
    if (m_languageValueLabel) {
        m_languageValueLabel->setText(selectedLanguageText());
    }
    updateDisplaySettingsDirtyState();
}

void cOptionsState::saveDisplaySettings()
{
    if (m_resolutionOptions.empty() ||
        m_renderScaleOptions.empty() ||
        m_worldScaleOptions.empty()) {
        return;
    }

    const ResolutionOption selected = m_resolutionOptions[m_selectedResolutionIndex];
    const int selectedRenderScale =
        m_renderScaleOptions[m_selectedRenderScaleIndex];
    const int selectedWorldScale =
        m_worldScaleOptions[m_selectedWorldScaleIndex];
    std::string errorMessage;
    m_selectedSettings.screenW = selected.width;
    m_selectedSettings.screenH = selected.height;
    m_selectedSettings.windowed = !m_selectedFullscreen;
    m_selectedSettings.renderScalePercent = selectedRenderScale;
    m_selectedSettings.worldScalePercent = selectedWorldScale;
    m_selectedSettings.graphicsMode = m_selectedGraphicsMode;
    m_selectedSettings.playMusic = m_ctx->getSoundPlayer()->getMusicEnabled();
    m_selectedSettings.playSound = m_ctx->getSoundPlayer()->getSoundEnabled();
    if (saveSettingsToIni("settings.ini", m_selectedSettings, errorMessage)) {
        m_savedResolution = selected;
        m_savedRenderScalePercent = selectedRenderScale;
        m_savedWorldScalePercent = selectedWorldScale;
        m_savedFullscreen = m_selectedFullscreen;
        m_savedGraphicsMode = m_selectedGraphicsMode;
        m_savedLanguage = m_selectedSettings.language;
        if (m_displayStatusLabel) {
            m_displayStatusLabel->setText(optionText(
                m_selectedSettings,
                "Saved. Restart the game.",
                "Сохранено. Перезапустите игру."
            ));
        }
    }
    else {
        cLogger::getInstance()->log(
            LOG_ERROR,
            COMP_GAMERULES,
            "Display settings",
            errorMessage
        );
        if (m_displayStatusLabel) {
            m_displayStatusLabel->setText(optionText(
                m_selectedSettings,
                "Could not save settings.ini",
                "Не удалось сохранить settings.ini"
            ));
        }
    }
    updateDisplaySettingsDirtyState();
}

void cOptionsState::constructWindow(int prevState)
{
    if (m_optionsPage != OptionsPage::Main) {
        constructAdvancedWindow(prevState);
        return;
    }
    int mainMenuWidth = m_hdLayout
        ? std::min(m_game.m_screenW - 32, 680)
        : m_game.m_screenW / 2;
    int mainMenuHeight = m_hdLayout
        ? std::min(m_game.m_screenH - 32, 560)
        : m_game.m_screenH / 2;
    int mainMenuFrameX = (m_game.m_screenW - mainMenuWidth) / 2;
    int mainMenuFrameY = (m_game.m_screenH - mainMenuHeight) / 2;

    int margin = m_hdLayout ? 8 : 4;
    int buttonHeight = m_hdLayout
        ? std::max(32, m_textDrawer->getFontHeight() + 10)
        : m_textDrawer->getFontHeight() + margin;
    int buttonWidth = mainMenuWidth - 8;
    const GuiTheme controlTheme = m_hdLayout
        ? GuiTheme::Remaster()
        : GuiTheme::Light();
    const GuiRenderKind buttonKind = m_hdLayout
        ? GuiRenderKind::REMASTER_BUTTON
        : GuiRenderKind::OPAQUE_WITH_BORDER;
    const int contentX = m_hdLayout ? 24 : 5;
    const int audioLabelWidth = m_hdLayout ? 110 : 50;
    const int audioCheckX = m_hdLayout ? 138 : 80;
    const int volumeLabelX = m_hdLayout ? 218 : 5;
    const int volumeLabelWidth = m_hdLayout ? 110 : 50 + buttonWidth / 2;
    const int audioSliderX = m_hdLayout
        ? 350
        : 5 + buttonWidth / 4 + 50 * 2;
    const int audioSliderWidth = m_hdLayout ? 250 : buttonHeight * 5;
    const int contentRowStride = buttonHeight + (m_hdLayout ? 2 : 5);
    const OptionsMenuLayout menuLayout = OptionsMenuLayout::create(
        mainMenuWidth,
        mainMenuHeight,
        buttonHeight,
        margin,
        contentX,
        buttonWidth,
        m_hdLayout,
        m_prevState == GAME_PLAYING
    );
    const auto relativeRect = [this](const cRectangle &rect) {
        return m_guiWindow->getRelativeRect(
            rect.getX(),
            rect.getY(),
            rect.getWidth(),
            rect.getHeight()
        );
    };

    const cRectangle &window = cRectangle(mainMenuFrameX, mainMenuFrameY, mainMenuWidth, mainMenuHeight);
    m_guiWindow = new GuiWindow(window, m_textDrawer);
    m_guiWindow->setTheme(controlTheme);
    cSoundPlayer* soundPlayer = m_ctx->getSoundPlayer();

    // Title
    m_guiWindow->setTitle("Dune II - The Maker - version " + D2TM_VERSION);

    // EXIT
    const cRectangle toMainMenuRect = relativeRect(menuLayout.mainMenu);
    GuiButton *gui_btn_toMenu = GuiButtonBuilder()
            .withRect(toMainMenuRect)        
            .withLabel(optionText(m_selectedSettings, "Main menu", "В главное меню"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_game.setNextStateToTransitionTo(GAME_MENU);
                m_game.initiateFadingOut();})
            .build();
    m_guiWindow->addGuiObject(gui_btn_toMenu);

    // QUIT game
    const cRectangle quitRect = relativeRect(menuLayout.quit);
    GuiButton *gui_btn_Quit = GuiButtonBuilder()
            .withRect(quitRect)        
            .withLabel(optionText(m_selectedSettings, "Quit game", "Выйти из игры"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_game.m_playing = false;
                m_game.initiateFadingOut();})
            .build();
    m_guiWindow->addGuiObject(gui_btn_Quit);

    // BACK to where we came from
    const cRectangle backRect = relativeRect(menuLayout.back);
    
    GuiButton *gui_btn_Back = GuiButtonBuilder()
            .withRect(backRect)        
            .withLabel(optionText(m_selectedSettings, "Back", "Назад"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this,prevState](){
                m_game.setNextStateToTransitionTo(prevState);})
            .build();
    m_guiWindow->addGuiObject(gui_btn_Back);

    // Save controls from options menu, only when playing the game.
    if (m_prevState == GAME_PLAYING) {
        const cRectangle saveRect = relativeRect(menuLayout.save);
        const cRectangle loadRect = relativeRect(menuLayout.load);
        m_loadGameButton = GuiButtonBuilder()
                .withRect(loadRect)
                .withLabel(optionText(m_selectedSettings, "Load game", "Загрузить игру"))
                .withTextDrawer(m_textDrawer)
                .withTheme(
                    SaveGameManager::hasAnySave()
                        ? controlTheme
                        : (m_hdLayout
                            ? GuiTheme::RemasterInactive()
                            : GuiTheme::Inactive())
                )
                .withKind(buttonKind)
                .withEnabled(SaveGameManager::hasAnySave())
                .onClick([this]() {
                    m_saveDialog->open(true, false);
                })
                .build();
        m_guiWindow->addGuiObject(m_loadGameButton);

        GuiButton *saveButton = GuiButtonBuilder()
                .withRect(saveRect)
                .withLabel(optionText(m_selectedSettings, "Save game", "Сохранить игру"))
                .withTextDrawer(m_textDrawer)
                .withTheme(controlTheme)
                .withKind(buttonKind)
                .onClick([this]() {
                    m_saveDialog->open(true, true);
                })
                .build();
        m_guiWindow->addGuiObject(saveButton);

        const cRectangle toMissionSelectRect = relativeRect(menuLayout.missionSelect);
    GuiButton *gui_btn_toMissionSelect = GuiButtonBuilder()
            .withRect(toMissionSelectRect)        
            .withLabel(optionText(m_selectedSettings, "Mission select", "Выбор миссии"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                m_game.setNextStateToTransitionTo(GAME_MISSIONSELECT);})
            .build();
        m_guiWindow->addGuiObject(gui_btn_toMissionSelect);
    }
    const cRectangle &musicRect = m_guiWindow->getRelativeRect(
        contentX,
        contentRowStride,
        audioLabelWidth,
        buttonHeight
    );
    GuiLabel *gui_MusicLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Music", "Музыка"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(musicRect)
            .build();
    m_guiWindow->addGuiObject(gui_MusicLabel);

    const cRectangle &musicCheckRect = m_guiWindow->getRelativeRect(
        audioCheckX,
        contentRowStride,
        buttonHeight,
        buttonHeight
    );
    GuiCheckBox *gui_MusicCheckLabel = GuiCheckBoxBuilder()
            .withRect(musicCheckRect)
            .withTheme(controlTheme)
            .onCheck([soundPlayer]() {
                soundPlayer->setMusicEnabled(true);
            })
            .onUnCheck([soundPlayer]() {
                soundPlayer->setMusicEnabled(false);
            })
            .build();
    gui_MusicCheckLabel->setChecked(soundPlayer->getMusicEnabled());
    m_guiWindow->addGuiObject(gui_MusicCheckLabel);

    const cRectangle &musicVolumeRect = m_guiWindow->getRelativeRect(
        volumeLabelX,
        contentRowStride,
        volumeLabelWidth,
        buttonHeight
    );
    GuiLabel *gui_MusicVolumeLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Volume", "Громкость"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(musicVolumeRect)
            .build();
    m_guiWindow->addGuiObject(gui_MusicVolumeLabel);

    const cRectangle &btn_musicVolumeRect = m_guiWindow->getRelativeRect(
        audioSliderX,
        contentRowStride,
        audioSliderWidth,
        buttonHeight
    );
    GuiSlider *gui_sld_musicVolumeRect = GuiSliderBuilder()
            .withRect(btn_musicVolumeRect)
            .withTheme(controlTheme)
            .withMinValue(0)
            .withMaxValue(10)
            .withInitialValue(soundPlayer->getMusicVolume())
            .onValueChanged([soundPlayer](int newValue) {
                soundPlayer->setMusicVolume(newValue);
            })
            .build();
    m_guiWindow->addGuiObject(gui_sld_musicVolumeRect);

    const cRectangle &soundRect = m_guiWindow->getRelativeRect(
        contentX,
        contentRowStride * 2,
        audioLabelWidth,
        buttonHeight
    );
    GuiLabel *gui_SoundLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Sound", "Звуки"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(soundRect)
            .build();
    m_guiWindow->addGuiObject(gui_SoundLabel);

    const cRectangle &soundCheckRect = m_guiWindow->getRelativeRect(
        audioCheckX,
        contentRowStride * 2,
        buttonHeight,
        buttonHeight
    );
    GuiCheckBox *gui_SoundCheckLabel = GuiCheckBoxBuilder()
            .withRect(soundCheckRect)
            .withTheme(controlTheme)
            .onCheck([soundPlayer]() {
                soundPlayer->setSoundEnabled(true);
            })
            .onUnCheck([soundPlayer]() {
                soundPlayer->setSoundEnabled(false);
            })
            .build();
    gui_SoundCheckLabel->setChecked(soundPlayer->getSoundEnabled());
    m_guiWindow->addGuiObject(gui_SoundCheckLabel);

    const cRectangle &soundVolumeRect = m_guiWindow->getRelativeRect(
        volumeLabelX,
        contentRowStride * 2,
        volumeLabelWidth,
        buttonHeight
    );
    GuiLabel *gui_SoundVolumeLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Volume", "Громкость"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(soundVolumeRect)
            .build();
    m_guiWindow->addGuiObject(gui_SoundVolumeLabel);

    const cRectangle &btn_soundVolumeRect = m_guiWindow->getRelativeRect(
        audioSliderX,
        contentRowStride * 2,
        audioSliderWidth,
        buttonHeight
    );
    GuiSlider *gui_sld_soundVolumeRect = GuiSliderBuilder()
            .withRect(btn_soundVolumeRect)
            .withTheme(controlTheme)
            .withMinValue(0)
            .withMaxValue(10)
            .withInitialValue(soundPlayer->getSoundVolume())
            .onValueChanged([soundPlayer](int newValue) {
                soundPlayer->setSoundVolume(newValue);
            })
            .build();
    m_guiWindow->addGuiObject(gui_sld_soundVolumeRect);

    const cRectangle &speedRect = m_guiWindow->getRelativeRect(
        contentX,
        contentRowStride * 3,
        audioLabelWidth,
        buttonHeight
    );
    GuiLabel *gui_DifficultyLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Game speed", "Скорость"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(speedRect)
            .build();
    m_guiWindow->addGuiObject(gui_DifficultyLabel);

    cTimeManager* timeManager = m_ctx->getTimeManager();
    const cRectangle &sld_speedRect = m_guiWindow->getRelativeRect(
        audioCheckX,
        contentRowStride * 3,
        m_hdLayout ? 220 : 100,
        buttonHeight
    );
    int convertedForSlider = 2 - timeManager->getGlobalSpeed() + 10;
    GuiSlider *gui_sld_speedRect = GuiSliderBuilder()
            .withRect(sld_speedRect)
            .withTheme(controlTheme)
            .withMinValue(2)
            .withMaxValue(10)
            .withInitialValue(convertedForSlider)
            .onValueChanged([timeManager](int newValue) {
                int globalSpeed = 10 - newValue + 2;
                // higher means slower, so convert into opposite
                timeManager->setGlobalSpeed(globalSpeed);
            })
            .build();
    m_guiWindow->addGuiObject(gui_sld_speedRect);

    const int resolutionRowY = contentRowStride * 4;
    const int displayLabelWidth = m_hdLayout ? 160 : 100;
    const cRectangle &resolutionLabelRect =
        m_guiWindow->getRelativeRect(
            contentX,
            resolutionRowY,
            displayLabelWidth,
            buttonHeight
        );
    GuiLabel *resolutionLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Resolution", "Разрешение"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(resolutionLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(resolutionLabel);

    const int arrowWidth = m_hdLayout ? 46 : 30;
    const int resolutionValueWidth = m_hdLayout ? 180 : 110;
    const int selectorX = m_hdLayout ? 198 : 110;
    const cRectangle &previousResolutionRect =
        m_guiWindow->getRelativeRect(selectorX, resolutionRowY, arrowWidth, buttonHeight);
    GuiButton *previousResolutionButton = GuiButtonBuilder()
            .withRect(previousResolutionRect)
            .withLabel("<")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectPreviousResolution();
            })
            .build();
    m_guiWindow->addGuiObject(previousResolutionButton);

    const cRectangle &resolutionValueRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin,
        resolutionRowY,
        resolutionValueWidth,
        buttonHeight
    );
    m_resolutionValueLabel = GuiLabelBuilder()
            .withLabel(selectedResolutionText())
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .withRect(resolutionValueRect)
            .build();
    m_guiWindow->addGuiObject(m_resolutionValueLabel);

    const cRectangle &nextResolutionRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin + resolutionValueWidth + margin,
        resolutionRowY,
        arrowWidth,
        buttonHeight
    );
    GuiButton *nextResolutionButton = GuiButtonBuilder()
            .withRect(nextResolutionRect)
            .withLabel(">")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectNextResolution();
            })
            .build();
    m_guiWindow->addGuiObject(nextResolutionButton);

    const int renderScaleRowY = contentRowStride * 5;
    const cRectangle &renderScaleLabelRect =
        m_guiWindow->getRelativeRect(
            contentX,
            renderScaleRowY,
            displayLabelWidth,
            buttonHeight
        );
    GuiLabel *renderScaleLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Game scale", "Масштаб игры"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(renderScaleLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(renderScaleLabel);

    const cRectangle &previousRenderScaleRect =
        m_guiWindow->getRelativeRect(selectorX, renderScaleRowY, arrowWidth, buttonHeight);
    GuiButton *previousRenderScaleButton = GuiButtonBuilder()
            .withRect(previousRenderScaleRect)
            .withLabel("<")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectPreviousRenderScale();
            })
            .build();
    m_guiWindow->addGuiObject(previousRenderScaleButton);

    const int renderScaleValueWidth = m_hdLayout ? 200 : 130;
    const cRectangle &renderScaleValueRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin,
        renderScaleRowY,
        renderScaleValueWidth,
        buttonHeight
    );
    m_renderScaleValueLabel = GuiLabelBuilder()
            .withLabel(selectedRenderScaleText())
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .withRect(renderScaleValueRect)
            .build();
    m_guiWindow->addGuiObject(m_renderScaleValueLabel);

    const cRectangle &nextRenderScaleRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin + renderScaleValueWidth + margin,
        renderScaleRowY,
        arrowWidth,
        buttonHeight
    );
    GuiButton *nextRenderScaleButton = GuiButtonBuilder()
            .withRect(nextRenderScaleRect)
            .withLabel(">")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectNextRenderScale();
            })
            .build();
    m_guiWindow->addGuiObject(nextRenderScaleButton);

    const int worldScaleRowY = contentRowStride * 6;
    const cRectangle &worldScaleLabelRect =
        m_guiWindow->getRelativeRect(
            contentX,
            worldScaleRowY,
            displayLabelWidth,
            buttonHeight
        );
    GuiLabel *worldScaleLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Object size", "Размер объектов"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(worldScaleLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(worldScaleLabel);

    const cRectangle &previousWorldScaleRect =
        m_guiWindow->getRelativeRect(
            selectorX,
            worldScaleRowY,
            arrowWidth,
            buttonHeight
        );
    GuiButton *previousWorldScaleButton = GuiButtonBuilder()
            .withRect(previousWorldScaleRect)
            .withLabel("<")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectPreviousWorldScale();
            })
            .build();
    m_guiWindow->addGuiObject(previousWorldScaleButton);

    const cRectangle &worldScaleValueRect =
        m_guiWindow->getRelativeRect(
            selectorX + arrowWidth + margin,
            worldScaleRowY,
            renderScaleValueWidth,
            buttonHeight
        );
    m_worldScaleValueLabel = GuiLabelBuilder()
            .withLabel(selectedWorldScaleText())
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .withRect(worldScaleValueRect)
            .build();
    m_guiWindow->addGuiObject(m_worldScaleValueLabel);

    const cRectangle &nextWorldScaleRect =
        m_guiWindow->getRelativeRect(
            selectorX + arrowWidth + margin + renderScaleValueWidth + margin,
            worldScaleRowY,
            arrowWidth,
            buttonHeight
        );
    GuiButton *nextWorldScaleButton = GuiButtonBuilder()
            .withRect(nextWorldScaleRect)
            .withLabel(">")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                selectNextWorldScale();
            })
            .build();
    m_guiWindow->addGuiObject(nextWorldScaleButton);

    const int graphicsModeRowY = contentRowStride * 7;
    const cRectangle &graphicsModeLabelRect =
        m_guiWindow->getRelativeRect(
            contentX,
            graphicsModeRowY,
            displayLabelWidth,
            buttonHeight
        );
    GuiLabel *graphicsModeLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Graphics", "Графика"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(graphicsModeLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(graphicsModeLabel);

    const cRectangle &previousGraphicsModeRect =
        m_guiWindow->getRelativeRect(
            selectorX,
            graphicsModeRowY,
            arrowWidth,
            buttonHeight
        );
    GuiButton *previousGraphicsModeButton = GuiButtonBuilder()
            .withRect(previousGraphicsModeRect)
            .withLabel("<")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                toggleGraphicsMode();
            })
            .build();
    m_guiWindow->addGuiObject(previousGraphicsModeButton);

    const cRectangle &graphicsModeValueRect =
        m_guiWindow->getRelativeRect(
            selectorX + arrowWidth + margin,
            graphicsModeRowY,
            resolutionValueWidth,
            buttonHeight
        );
    m_graphicsModeValueLabel = GuiLabelBuilder()
            .withLabel(selectedGraphicsModeText())
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .withRect(graphicsModeValueRect)
            .build();
    m_guiWindow->addGuiObject(m_graphicsModeValueLabel);

    const cRectangle &nextGraphicsModeRect =
        m_guiWindow->getRelativeRect(
            selectorX + arrowWidth + margin + resolutionValueWidth + margin,
            graphicsModeRowY,
            arrowWidth,
            buttonHeight
        );
    GuiButton *nextGraphicsModeButton = GuiButtonBuilder()
            .withRect(nextGraphicsModeRect)
            .withLabel(">")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                toggleGraphicsMode();
            })
            .build();
    m_guiWindow->addGuiObject(nextGraphicsModeButton);

    const int fullscreenRowY = contentRowStride * 8;
    const cRectangle &fullscreenLabelRect =
        m_guiWindow->getRelativeRect(
            contentX,
            fullscreenRowY,
            m_hdLayout ? 220 : 175,
            buttonHeight
        );
    GuiLabel *fullscreenLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Fullscreen", "Полноэкранный режим"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(fullscreenLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(fullscreenLabel);

    const cRectangle &fullscreenCheckRect =
        m_guiWindow->getRelativeRect(
            m_hdLayout ? 252 : 185,
            fullscreenRowY,
            buttonHeight,
            buttonHeight
        );
    GuiCheckBox *fullscreenCheck = GuiCheckBoxBuilder()
            .withRect(fullscreenCheckRect)
            .withTheme(controlTheme)
            .onCheck([this]() {
                m_selectedFullscreen = true;
                if (m_displayStatusLabel) {
                    m_displayStatusLabel->setText("");
                }
                updateDisplaySettingsDirtyState();
            })
            .onUnCheck([this]() {
                m_selectedFullscreen = false;
                if (m_displayStatusLabel) {
                    m_displayStatusLabel->setText("");
                }
                updateDisplaySettingsDirtyState();
            })
            .build();
    fullscreenCheck->setChecked(m_selectedFullscreen);
    m_guiWindow->addGuiObject(fullscreenCheck);

    const int languageRowY = contentRowStride * 9;
    const cRectangle &languageLabelRect = m_guiWindow->getRelativeRect(
        contentX, languageRowY, displayLabelWidth, buttonHeight
    );
    GuiLabel *languageLabel = GuiLabelBuilder()
            .withLabel(optionText(m_selectedSettings, "Language", "Язык"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(languageLabelRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(languageLabel);
    const cRectangle &previousLanguageRect = m_guiWindow->getRelativeRect(
        selectorX, languageRowY, arrowWidth, buttonHeight
    );
    GuiButton *previousLanguage = GuiButtonBuilder()
            .withRect(previousLanguageRect).withLabel("<").withTextDrawer(m_textDrawer)
            .withTheme(controlTheme).withKind(buttonKind)
            .onClick([this]() { toggleLanguage(); }).build();
    m_guiWindow->addGuiObject(previousLanguage);
    const cRectangle &languageValueRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin, languageRowY, resolutionValueWidth, buttonHeight
    );
    m_languageValueLabel = GuiLabelBuilder()
            .withLabel(selectedLanguageText()).withTextDrawer(m_textDrawer)
            .withTheme(controlTheme).withKind(GuiRenderKind::OPAQUE_WITH_BORDER)
            .withRect(languageValueRect).build();
    m_guiWindow->addGuiObject(m_languageValueLabel);
    const cRectangle &nextLanguageRect = m_guiWindow->getRelativeRect(
        selectorX + arrowWidth + margin + resolutionValueWidth + margin,
        languageRowY, arrowWidth, buttonHeight
    );
    GuiButton *nextLanguage = GuiButtonBuilder()
            .withRect(nextLanguageRect).withLabel(">").withTextDrawer(m_textDrawer)
            .withTheme(controlTheme).withKind(buttonKind)
            .onClick([this]() { toggleLanguage(); }).build();
    m_guiWindow->addGuiObject(nextLanguage);

    const cRectangle applyDisplayRect = relativeRect(menuLayout.apply);
    m_applyDisplayButton = GuiButtonBuilder()
            .withRect(applyDisplayRect)
            .withLabel(optionText(m_selectedSettings, "Apply", "Применить"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() {
                saveDisplaySettings();
            })
            .build();
    m_guiWindow->addGuiObject(m_applyDisplayButton);

    const cRectangle displayStatusRect = relativeRect(menuLayout.status);
    m_displayStatusLabel = GuiLabelBuilder()
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withRect(displayStatusRect)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_guiWindow->addGuiObject(m_displayStatusLabel);

    const cRectangle advancedButtonRect = relativeRect(menuLayout.advanced);
    GuiButton *advancedButton = GuiButtonBuilder()
            .withRect(advancedButtonRect)
            .withLabel(optionText(m_selectedSettings, "More settings", "Дополнительные настройки"))
            .withTextDrawer(m_textDrawer)
            .withTheme(controlTheme)
            .withKind(buttonKind)
            .onClick([this]() { requestOptionsPage(OptionsPage::Gameplay); })
            .build();
    m_guiWindow->addGuiObject(advancedButton);

    updateDisplayControls();
}

cOptionsState::~cOptionsState()
{
    delete m_guiWindow;
    m_loadGameButton = nullptr;
}

void cOptionsState::thinkFast()
{
    if (!m_pendingOptionsPage) {
        return;
    }

    const OptionsPage page = *m_pendingOptionsPage;
    m_pendingOptionsPage.reset();
    switchOptionsPage(page);
}

void cOptionsState::draw() const
{
    if (m_backgroundTexture) {
        renderDrawer->renderSprite(m_backgroundTexture,0,0);
    }
    if (m_hdLayout) {
        renderDrawer->renderRectFillColor(
            0,
            0,
            m_game.m_screenW,
            m_game.m_screenH,
            Color{4, 6, 7, 150}
        );
    }
    m_guiWindow->draw();

    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->draw();
    }
    // MOUSE
    m_game.getMouse()->draw();
}

void cOptionsState::onNotifyMouseEvent(const s_MouseEvent &event)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onMouseEvent(event);
        return;
    }
    m_guiWindow->onNotifyMouseEvent(event);
}

eGameStateType cOptionsState::getType()
{
    return GAMESTATE_OPTIONS;
}

void cOptionsState::onNotifyKeyboardEvent(const cKeyboardEvent &event)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onKeyboardEvent(event);
        return;
    }
    if (m_optionsPage == OptionsPage::Controls &&
        m_bindingCapture &&
        event.isType(eKeyEventType::PRESSED)) {
        const SDL_Scancode scancode = event.firstKey();
        if (scancode != SDL_SCANCODE_ESCAPE &&
            scancode != SDL_SCANCODE_UNKNOWN) {
            setCommandBinding(
                m_selectedSettings.commandBindings,
                *m_bindingCapture,
                scancode
            );
        }
        m_bindingCapture.reset();
        refresh();
    }
}

void cOptionsState::onTextInput(std::string_view text)
{
    if (m_saveDialog && m_saveDialog->isOpen()) {
        m_saveDialog->onTextInput(text);
    }
}

/**
 * Reconstructs window so that it knows to which previous state it should go 'back to'
 * @param prevState
 */
void cOptionsState::setPrevState(int prevState)
{
    m_prevState = prevState;
    refresh();
}

void cOptionsState::refresh()
{
    if (m_saveDialog) {
        m_saveDialog->close();
    }
    delete m_guiWindow;
    m_guiWindow = nullptr;
    m_resolutionValueLabel = nullptr;
    m_renderScaleValueLabel = nullptr;
    m_worldScaleValueLabel = nullptr;
    m_graphicsModeValueLabel = nullptr;
    m_languageValueLabel = nullptr;
    m_displayStatusLabel = nullptr;
    m_applyDisplayButton = nullptr;
    m_loadGameButton = nullptr;
    constructWindow(m_prevState);
    m_backgroundTexture = nullptr;
}
