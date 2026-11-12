#include "gamestates/cOptionsState.h"
#include "config.h"
#include "gui/GuiButton.h"
#include "gui/GuiWindow.h"
#include "gui/GuiLabel.hpp"
#include "gui/GuiCheckBox.hpp"
#include "gui/GuiSlider.hpp"
#include "gui/GuiTheme.hpp"
#include "context/GameContext.hpp"
#include "context/TextContext.hpp"
#include "drawers/cTextDrawer.h"
#include "controls/cKeyboard.h"
#include "game/cGameSettings.h"
#include "game/Preferences.hpp"
#include "game/PreferencesPath.hpp"
#include "gamestates/AdvancedOptionsHeaderLayout.hpp"
#include "gamestates/OptionsKeyLabels.hpp"
#include "gamestates/OptionsPageData.hpp"
#include "include/cAssert.h"
#include "utils/Localization.hpp"
#include "utils/Log.h"

#include <algorithm>
#include <cmath>
#include <string_view>

void cOptionsState::constructAdvancedWindow(eGameState)
{
    const int windowWidth = std::min(m_settings->getScreenW() - 32, 760);
    const int windowHeight = std::min(m_settings->getScreenH() - 32, 640);
    const int margin = 8;
    const int buttonHeight = std::max(32, m_textDrawer->getFontHeight() + 10);
    const int labelWidth = windowWidth - 200;
    const int checkX = windowWidth - 160;
    const int rowStride = buttonHeight + 4;
    const int footerY = windowHeight - buttonHeight - margin;
    const int frameX = (m_settings->getScreenW() - windowWidth) / 2;
    const int frameY = (m_settings->getScreenH() - windowHeight) / 2;
    const GuiTheme theme = GuiTheme::Remaster();
    const GuiRenderKind buttonKind = GuiRenderKind::REMASTER_BUTTON;

    m_guiWindow = std::make_unique<GuiWindow>(
        m_sdlDrawer,
        cRectangle(frameX, frameY, windowWidth, windowHeight),
        m_textDrawer
    );
    m_guiWindow->setTheme(theme);
    m_guiWindow->setTitle(localization::text("Dune II - Settings", "Dune II — Настройки"));

    const auto addTab = [this, theme](
                            const cRectangle &rect, std::string_view label, OptionsPage page) {
        auto button = GuiButtonBuilder()
                .withRect(m_guiWindow->getRelativeRect(rect.getX(), rect.getY(), rect.getWidth(), rect.getHeight()))
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withKind(buttonKind)
                .onClick([this, page]() { requestOptionsPage(page); })
                .build();
        m_guiWindow->addGuiObject(std::move(button));
    };
    const AdvancedOptionsHeaderLayout headerLayout = AdvancedOptionsHeaderLayout::create(
        windowWidth, margin, buttonHeight, m_textDrawer->getFontHeight());
    addTab(headerLayout.tabs[0], localization::text("Main", "Основные"), OptionsPage::Main);
    addTab(headerLayout.tabs[1], localization::text("Gameplay", "Игра"), OptionsPage::Gameplay);
    addTab(headerLayout.tabs[2], localization::text("Controls", "Управление"), OptionsPage::Controls);
    addTab(headerLayout.tabs[3], localization::text("Diagnostics", "Диагностика"), OptionsPage::Diagnostics);

    int row = 2;
    const auto addToggle = [this, &row, theme, labelWidth, checkX, buttonHeight, rowStride](
                               std::string_view label, bool InitialGameSettings::*field) {
        const int y = row++ * rowStride;
        auto name = GuiLabelBuilder()
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, y, labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(std::move(name));
        auto check = GuiCheckBoxBuilder()
                .withRect(m_guiWindow->getRelativeRect(checkX, y, buttonHeight, buttonHeight))
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .onCheck([this, field]() { m_selected.*field = true; })
                .onUnCheck([this, field]() { m_selected.*field = false; })
                .build();
        check->setChecked(m_selected.*field);
        m_guiWindow->addGuiObject(std::move(check));
    };
    const auto addSpeed = [this, &row, theme, labelWidth, checkX, buttonHeight, rowStride](
                              std::string_view label, float InitialGameSettings::*field) {
        const int y = row++ * rowStride;
        auto name = GuiLabelBuilder()
                .withLabel(std::string(label))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, y, labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(std::move(name));
        auto slider = GuiSliderBuilder()
                .withRect(m_guiWindow->getRelativeRect(checkX - 230, y, 230, buttonHeight))
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withMinValue(1)
                .withMaxValue(10)
                .withInitialValue(std::clamp(static_cast<int>(std::lround((m_selected.*field) * 10.0f)), 1, 10))
                .onValueChanged([this, field](int value) {
                    m_selected.*field = static_cast<float>(value) / 10.0f;
                })
                .build();
        m_guiWindow->addGuiObject(std::move(slider));
    };

    if (m_optionsPage == OptionsPage::Gameplay) {
        addToggle(localization::text("Edge scrolling — move camera at screen edge", "Прокрутка у края экрана"),
                  &InitialGameSettings::cameraEdgeMove);
        addSpeed(localization::text("Keyboard/edge camera speed", "Скорость камеры с клавиатуры и у края"),
                 &InitialGameSettings::cameraBorderOrKeyMoveSpeed);
        addSpeed(localization::text("Camera drag speed", "Скорость перетаскивания камеры"),
                 &InitialGameSettings::cameraDragMoveSpeed);
        addToggle(localization::text("Pause when the window loses focus", "Пауза при потере фокуса окна"),
                  &InitialGameSettings::pauseWhenLosingFocus);
        addToggle(localization::text("Repeat reinforcements", "Повторять подкрепления"),
                  &InitialGameSettings::allowRepeatingReinforcements);
        addToggle(localization::text("All turrets stop on low power", "Отключать все башни при нехватке энергии"),
                  &InitialGameSettings::turretsDownOnLowPower);
        addToggle(localization::text("Rocket turrets stop on low power", "Отключать ракетные башни при нехватке энергии"),
                  &InitialGameSettings::rocketTurretsDownOnLowPower);
        auto rules = GuiLabelBuilder()
                .withLabel(localization::text("Rules file: game.ini (change manually)",
                                              "Файл правил: game.ini (меняется вручную)"))
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, row++ * rowStride, labelWidth, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(std::move(rules));
    } else if (m_optionsPage == OptionsPage::Controls) {
        const auto &table = cKeyBindings::getActionTable();
        const int totalRows = static_cast<int>(table.size());
        const int listTop = 2 * rowStride;
        const int listBottom = footerY - rowStride;
        const int visibleRows = optionsVisibleRows(listTop, listBottom, rowStride);
        m_controlsScrollRow = optionsClampScrollRow(m_controlsScrollRow, totalRows, visibleRows);
        const int bindingButtonWidth = 220;
        const int bindingButtonX = windowWidth - margin - bindingButtonWidth;
        int shownRows = 0;
        for (int offset = 0; offset < visibleRows && m_controlsScrollRow + offset < totalRows; ++offset) {
            const eKeyAction action = table[m_controlsScrollRow + offset].second;
            const int y = (2 + offset) * rowStride;
            auto name = GuiLabelBuilder()
                    .withLabel(keyActionLabelText(action))
                    .withTextDrawer(m_textDrawer)
                    .withRenderer(m_sdlDrawer)
                    .withTheme(theme)
                    .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                    .withRect(m_guiWindow->getRelativeRect(16, y, bindingButtonX - 32, buttonHeight))
                    .withTextAlign(GuiTextAlignHorizontal::LEFT)
                    .build();
            m_guiWindow->addGuiObject(std::move(name));
            const std::string bindingLabel = m_bindingCapture == action
                ? localization::text("Press key...", "Нажмите клавишу…")
                : m_selectedBindings.getBindingDisplayName(action);
            auto bindingButton = GuiButtonBuilder()
                    .withRect(m_guiWindow->getRelativeRect(bindingButtonX, y, bindingButtonWidth, buttonHeight))
                    .withLabel(bindingLabel)
                    .withTextDrawer(m_textDrawer)
                    .withRenderer(m_sdlDrawer)
                    .withTheme(theme)
                    .withKind(buttonKind)
                    .onClick([this, action]() {
                        m_bindingMessage.clear();
                        m_bindingCapture = action;
                        m_bindingCaptureFinished = false;
                        m_refreshRequested = true;
                    })
                    .build();
            m_guiWindow->addGuiObject(std::move(bindingButton));
            ++shownRows;
        }
        const std::string rangeText = m_bindingMessage.empty()
            ? localization::format("Actions {}-{} of {}", "Действия {}-{} из {}",
                                   m_controlsScrollRow + 1, m_controlsScrollRow + shownRows, totalRows)
            : m_bindingMessage;
        auto rangeLabel = GuiLabelBuilder()
                .withLabel(rangeText)
                .withTextDrawer(m_textDrawer)
                .withRenderer(m_sdlDrawer)
                .withTheme(theme)
                .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
                .withRect(m_guiWindow->getRelativeRect(16, (2 + visibleRows) * rowStride,
                                                       windowWidth - 32, buttonHeight))
                .withTextAlign(GuiTextAlignHorizontal::LEFT)
                .build();
        m_guiWindow->addGuiObject(std::move(rangeLabel));
    } else {
        addToggle(localization::text("Debug mode", "Режим отладки"), &InitialGameSettings::debugMode);
        addToggle(localization::text("Disable all AI", "Отключить ИИ"), &InitialGameSettings::disableAI);
        addToggle(localization::text("Use one AI player", "Оставить одного ИИ"), &InitialGameSettings::oneAi);
        addToggle(localization::text("Disable worm AI", "Отключить ИИ червя"), &InitialGameSettings::disableWormAi);
        addToggle(localization::text("Disable reinforcements", "Отключить подкрепления"), &InitialGameSettings::disableReinforcements);
        addToggle(localization::text("Disable remaining AI", "Отключить остальных ИИ"), &InitialGameSettings::noAiRest);
        addToggle(localization::text("Show unit debug data", "Показывать отладочные данные юнитов"),
                  &InitialGameSettings::drawUnitDebug);
        addToggle(localization::text("Show resource usage", "Показывать расход ресурсов"), &InitialGameSettings::drawUsages);
    }

    auto applyButton = GuiButtonBuilder()
            .withRect(m_guiWindow->getRelativeRect(16, footerY, 180, buttonHeight))
            .withLabel(localization::text("Apply", "Применить"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(theme)
            .withKind(buttonKind)
            .onClick([this]() { applyAdvancedPage(); })
            .build();
    m_guiWindow->addGuiObject(std::move(applyButton));
    auto statusLabel = GuiLabelBuilder()
            .withRect(m_guiWindow->getRelativeRect(16 + 180 + margin, footerY,
                                                   windowWidth - 2 * (16 + 180 + margin), buttonHeight))
            .withLabel("")
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(theme)
            .withKind(GuiRenderKind::TRANSPARENT_WITHOUT_BORDER)
            .withTextAlign(GuiTextAlignHorizontal::LEFT)
            .build();
    m_statusLabel = statusLabel.get();
    m_guiWindow->addGuiObject(std::move(statusLabel));
    auto backButton = GuiButtonBuilder()
            .withRect(m_guiWindow->getRelativeRect(windowWidth - 180 - margin, footerY, 180, buttonHeight))
            .withLabel(localization::text("Back", "Назад"))
            .withTextDrawer(m_textDrawer)
            .withRenderer(m_sdlDrawer)
            .withTheme(theme)
            .withKind(buttonKind)
            .onClick([this]() { requestOptionsPage(OptionsPage::Main); })
            .build();
    m_guiWindow->addGuiObject(std::move(backButton));
}

void cOptionsState::applyAdvancedPage()
{
    std::string error = "Could not get the user data directory";
    const auto prefsFile = PreferencesPath::file(Preferences::FILE_NAME);
    bool saved = false;
    if (prefsFile) {
        switch (m_optionsPage) {
            case OptionsPage::Gameplay:
                saved = Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, GAMEPLAY_PAGE_KEYS), error);
                break;
            case OptionsPage::Diagnostics:
                saved = Preferences::saveValues(*prefsFile, Preferences::valuesOf(m_selected, DIAGNOSTICS_PAGE_KEYS), error);
                break;
            case OptionsPage::Controls: {
                Preferences::KeyValues values;
                for (const auto &[name, action] : cKeyBindings::getActionTable()) {
                    values.emplace_back(name, m_selectedBindings.toIniValue(action));
                }
                saved = Preferences::saveKeyBindings(*prefsFile, values, error);
                break;
            }
            case OptionsPage::Main:
                break;
        }
    }
    if (!saved) {
        Logger::warn(COMP_GAMERULES, "Preferences", "Could not save preferences: {}", error);
        m_statusLabel->setText(localization::text("Could not save preferences.ini", "Не удалось сохранить preferences.ini"));
        return;
    }
    switch (m_optionsPage) {
        case OptionsPage::Gameplay:
            m_settings->setAllowRepeatingReinforcements(m_selected.allowRepeatingReinforcements);
            m_settings->setTurretsDownOnLowPower(m_selected.turretsDownOnLowPower);
            m_settings->setRocketTurretsDownOnLowPower(m_selected.rocketTurretsDownOnLowPower);
            m_statusLabel->setText(localization::text("Saved. Restart the game.", "Сохранено. Перезапустите игру."));
            break;
        case OptionsPage::Diagnostics:
            m_settings->setDebugMode(m_selected.debugMode);
            m_settings->setDisableAI(m_selected.disableAI);
            m_settings->setOneAi(m_selected.oneAi);
            m_settings->setDisableWormAi(m_selected.disableWormAi);
            m_settings->setDisableReinforcements(m_selected.disableReinforcements);
            m_settings->setNoAiRest(m_selected.noAiRest);
            m_settings->setDrawUnitDebug(m_selected.drawUnitDebug);
            m_settings->setDrawUsages(m_selected.drawUsages);
            m_statusLabel->setText(localization::text("Saved.", "Сохранено."));
            break;
        case OptionsPage::Controls:
            *m_keyboard->getKeyBindings() = m_selectedBindings;
            m_statusLabel->setText(localization::text("Saved.", "Сохранено."));
            break;
        case OptionsPage::Main:
            break;
    }
}
