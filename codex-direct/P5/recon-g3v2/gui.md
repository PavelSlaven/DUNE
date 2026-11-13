### src/gui/GuiObject.h@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.h | nl -ba
     1	/**
     2	 * @file GuiObject.h
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "observers/cInputObserver.h"
    19	#include "utils/cRectangle.h"
    20	#include "gui/GuiTheme.hpp"
    21	
    22	#include <functional>
    23	#include <string>
    24	
    25	class cTextDrawer;
    26	
    27	enum GuiRenderKind {
    28	    OPAQUE_WITH_BORDER = 0,
    29	    OPAQUE_WITHOUT_BORDER = 1,
    30	    TRANSPARENT_WITH_BORDER = 2,
    31	    TRANSPARENT_WITHOUT_BORDER = 3,
    32	    WITH_TEXTURE = 4,
    33	    WITH_STRETCHED_TEXTURE = 5,
    34	    REMASTER_BUTTON = 6
    35	};
    36	
    37	enum GuiTextAlignHorizontal {
    38	    LEFT,
    39	    CENTER
    40	};
    41	
    42	class GuiTextual {
    43	public:
    44	    virtual ~GuiTextual() = default;
    45	    virtual void setTextDrawer(cTextDrawer* drawer) = 0;
    46	    virtual void setTextAlignHorizontal(GuiTextAlignHorizontal align) {
    47	        (void)align;
    48	    }
    49	    virtual void setText(const std::string& text) = 0;
    50	};
    51	
    52	class GuiClickable {
    53	public:
    54	    virtual ~GuiClickable() = default;
    55	    virtual void setEnabled(bool enabled) = 0;
    56	    virtual bool isEnabled() const = 0;
    57	    virtual void setOnLeftMouseButtonClickedAction(std::function<void()> action) = 0;
    58	    virtual void setOnRightMouseButtonClickedAction(std::function<void()> action) = 0;
    59	};
    60	
    61	class GuiStatefulVisual {
    62	public:
    63	    enum class VisualState {
    64	        Normal,
    65	        Hover,
    66	        Pressed,
    67	        Disabled
    68	    };
    69	
    70	    virtual ~GuiStatefulVisual() = default;
    71	    virtual void setVisualState(VisualState state) = 0;
    72	    virtual VisualState visualState() const = 0;
    73	};
    74	
    75	class SDLDrawer;
    76	
    77	class GuiObject : public cInputObserver {
    78	public:
    79	    virtual ~GuiObject() = default;
    80	    virtual void draw() const = 0;
    81	    virtual bool hasKeyboardFocus() const {
    82	        return false;
    83	    }
    84	
    85	    void setTheme(const GuiTheme& theme);
    86	    void setPosition(int x, int y);
    87	    void setSize(int width, int height);
    88	protected:
    89	    explicit GuiObject(SDLDrawer* drawer, const cRectangle &rect);
    90	    // any gui object has a position and size. Hence its always a 'rect'.
    91	    cRectangle m_rect;
    92	    GuiTheme m_theme;
    93	    SDLDrawer* m_sdlDrawer = nullptr;
    94	    void drawRectBorder(Color borderRect, Color borderBottomRight) const;
    95	    void drawRectFillBorder(const GuiTheme& theme) const;
    96	    void auditRecord(const char *type) const;
    97	    void auditClick(const std::string &name) const;
    98	};
```

### src/gui/GuiObject.cpp@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp | nl -ba
     1	/**
     2	 * @file GuiObject.cpp
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#include "gui/GuiObject.h"
    17	#include "debug/UiAudit.hpp"
    18	#include "drawers/SDLDrawer.hpp"
    19	#include <iostream>
    20	#include "include/cAssert.h"
    21	
    22	
    23	GuiObject::GuiObject(SDLDrawer* drawer, const cRectangle &rect) : 
    24	    m_rect(rect), m_sdlDrawer(drawer)
    25	{
    26	    d2tm_assert(drawer != nullptr);
    27	}
    28	
    29	
    30	void GuiObject::setTheme(const GuiTheme& theme)
    31	{
    32	    m_theme = theme;
    33	}
    34	
    35	void GuiObject::auditRecord(const char *type) const
    36	{
    37	    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
    38	}
    39	
    40	void GuiObject::auditClick(const std::string &name) const
    41	{
    42	    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
    43	}
    44	
    45	void GuiObject::setPosition(int x, int y)
    46	{
    47	    m_rect.move(x, y);
    48	}
    49	void GuiObject::setSize(int width, int height)
    50	{
    51	    m_rect.resize(width, height);
    52	}
    53	
    54	void GuiObject::drawRectBorder(Color borderRect, Color borderBottomRight) const
    55	{
    56	    int x1= m_rect.getX();
    57	    int y1 = m_rect.getY();
    58	    int width = m_rect.getWidth();
    59	    int height = m_rect.getHeight();
    60	    //std::cout <<":" << x1 << " " << y1 << " " << width << " " << height << std::endl;
    61	    m_sdlDrawer->renderRectColor(m_rect,borderRect);
    62	    m_sdlDrawer->renderLine(x1+width, y1, x1+width, y1+height,borderBottomRight);
    63	    m_sdlDrawer->renderLine(x1, y1+height, x1+width, y1+height, borderBottomRight);
    64	}
    65	
    66	void GuiObject::drawRectFillBorder(const GuiTheme& theme) const
    67	{
    68	    m_sdlDrawer->renderRectFillColor(m_rect, theme.fillColor);
    69	    drawRectBorder(theme.borderLight, theme.borderDark);
    70	}
```

### src/gui/GuiBar.h@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiBar.h | nl -ba
     1	/**
     2	 * @file GuiBar.h
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "GuiObject.h"
    19	
    20	#include <string>
    21	#include <vector>
    22	
    23	class SDLDrawer;
    24	
    25	enum class GuiBarPlacement :char {
    26	    HORIZONTAL = 0,
    27	    VERTICAL = 1
    28	};
    29	
    30	class GuiBar : protected GuiObject {
    31	public:
    32	    explicit GuiBar(SDLDrawer* drawer, const cRectangle &rect, GuiBarPlacement placement, int iconSize = 40);
    33	    ~GuiBar() noexcept override;
    34	
    35	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    36	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    37	
    38	    void draw() const override;
    39	
    40	    void addGuiObject(std::unique_ptr<GuiObject> guiObject);
    41	    void addAutoGuiObject(std::unique_ptr<GuiObject> guiObject);
    42	
    43	    cRectangle getRelativeRect(int x, int y, int width, int height);
    44	
    45	    void setTheme(const GuiTheme& _theme) {
    46	        GuiObject::setTheme(_theme);
    47	    }
    48	
    49	    void beginPlacement(int value) {
    50	        placementPosition = value;
    51	    }
    52	private:
    53	    std::vector<std::unique_ptr<GuiObject>> gui_objects;
    54	    GuiBarPlacement m_placement;
    55	    int placementPosition;
    56	    int heightBarSize;
    57	    int halfMarginBetweenButtons;
    58	};
    59	
```

### src/gui/GuiBar.cpp@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiBar.cpp | nl -ba
     1	/**
     2	 * @file GuiBar.cpp
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#include "gui/GuiBar.h"
    17	
    18	#include "drawers/SDLDrawer.hpp"
    19	#include "include/cAssert.h"
    20	
    21	GuiBar::GuiBar(SDLDrawer* drawer, const cRectangle &rect, GuiBarPlacement placement, int heightBarSize) :
    22	    GuiObject(drawer, rect), /*gui_objects(std::vector<GuiObject *>(0)),*/ m_placement(placement), placementPosition(0), heightBarSize(heightBarSize)
    23	{
    24	    d2tm_assert(drawer != nullptr);
    25	    if (m_placement == GuiBarPlacement::HORIZONTAL) {
    26	       halfMarginBetweenButtons = (rect.getHeight()-heightBarSize)/2;
    27	    } else {
    28	        halfMarginBetweenButtons = (rect.getWidth()-heightBarSize)/2;
    29	    }
    30	}
    31	
    32	GuiBar::~GuiBar() noexcept
    33	{
    34	    // Smart pointers handle cleanup
    35	    // for (auto gui_object : gui_objects) {
    36	    //     delete gui_object;
    37	    // }
    38	}
    39	
    40	void GuiBar::draw() const
    41	{
    42	    // draw window itself...
    43	    //drawRectFillBorder(m_theme);
    44	    //drawRectBorder(m_theme.borderLight,m_theme.borderLight);
    45	    drawRectFillBorder(m_theme);
    46	    for (auto &guiObject : gui_objects) {
    47	        guiObject->draw();
    48	    }
    49	
    50	}
    51	
    52	void GuiBar::addGuiObject(std::unique_ptr<GuiObject> guiObject)
    53	{
    54	    gui_objects.push_back(std::move(guiObject));
    55	}
    56	
    57	void GuiBar::addAutoGuiObject(std::unique_ptr<GuiObject> guiObject)
    58	{
    59	    int x = 0, y = 0;
    60	    if (m_placement == GuiBarPlacement::HORIZONTAL) {
    61	        x = placementPosition;
    62	        y = halfMarginBetweenButtons;
    63	        placementPosition += heightBarSize + 2*halfMarginBetweenButtons;
    64	    } else {
    65	        x = m_rect.getX() + halfMarginBetweenButtons;
    66	        y = m_rect.getY() + placementPosition;
    67	        placementPosition += heightBarSize + 2*halfMarginBetweenButtons;
    68	    }
    69	    guiObject->setPosition(x,y);
    70	    gui_objects.push_back(std::move(guiObject));
    71	}
    72	
    73	void GuiBar::onNotifyMouseEvent(const s_MouseEvent &event)
    74	{
    75	    if (!event.coords.isWithinRectangle(&m_rect))
    76	        return;
    77	    for (auto &guiObject : gui_objects) {
    78	        guiObject->onNotifyMouseEvent(event);
    79	    }
    80	}
    81	
    82	cRectangle GuiBar::getRelativeRect(int x, int y, int width, int height)
    83	{
    84	    return cRectangle(x + m_rect.getX(), y + m_rect.getY(), width, height);
    85	}
    86	
    87	void GuiBar::onNotifyKeyboardEvent(const cKeyboardEvent &event)
    88	{
    89	    for (auto &guiObject : gui_objects) {
    90	        guiObject->onNotifyKeyboardEvent(event);
    91	    }
    92	}
```

### src/gui/GuiWindow.h@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiWindow.h | nl -ba
     1	/**
     2	 * @file GuiWindow.h
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "GuiObject.h"
    19	#include <string>
    20	#include <vector>
    21	#include <memory>
    22	
    23	class SDLDrawer;
    24	class cTextDrawer;
    25	
    26	class GuiWindow : protected GuiObject {
    27	public:
    28	    explicit GuiWindow(SDLDrawer* drawer, const cRectangle &rect, cTextDrawer* _textDrawer);
    29	    ~GuiWindow() noexcept override;
    30	
    31	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    32	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    33	
    34	    void draw() const override;
    35	
    36	    bool hasFocusedInput() const;
    37	
    38	    void addGuiObject(std::unique_ptr<GuiObject> guiObject);
    39	
    40	    cRectangle getRelativeRect(int x, int y, int width, int height);
    41	
    42	    void setTitle(const std::string &value) {
    43	        title = value;
    44	    }
    45	    void setTheme(const GuiTheme& _theme) {
    46	        GuiObject::setTheme(_theme);
    47	    }
    48	private:
    49	    std::vector<std::unique_ptr<GuiObject>> gui_objects;
    50	    std::string title;
    51	    cTextDrawer* m_textDrawer = nullptr;
    52	};
    53	
```

### src/gui/GuiWindow.cpp@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiWindow.cpp | nl -ba
     1	/**
     2	 * @file GuiWindow.cpp
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#include "GuiWindow.h"
    17	#include "debug/UiAudit.hpp"
    18	#include "drawers/cTextDrawer.h"
    19	#include "drawers/SDLDrawer.hpp"
    20	#include "include/cAssert.h"
    21	
    22	GuiWindow::GuiWindow(SDLDrawer* drawer, const cRectangle &rect, cTextDrawer* _textDrawer) :
    23	    GuiObject(drawer,rect),
    24	    gui_objects(),
    25	    title(""),
    26	    m_textDrawer(_textDrawer)
    27	{
    28	    d2tm_assert(drawer != nullptr);
    29	    d2tm_assert(_textDrawer != nullptr);
    30	}
    31	
    32	GuiWindow::~GuiWindow() noexcept
    33	{
    34	    // Smart pointers handle cleanup
    35	}
    36	
    37	void GuiWindow::draw() const
    38	{
    39	    if (uiaudit::isEnabled()) {
    40	        auditRecord("GuiWindow");
    41	    }
    42	    // draw window itself...
    43	    drawRectFillBorder(m_theme);
    44	    for (auto &guiObject : gui_objects) {
    45	        guiObject->draw();
    46	    }
    47	
    48	    // draw title
    49	    if (title.empty()) return;
    50	    m_textDrawer->drawTextCentered(title.c_str(), m_rect.getX(), m_rect.getWidth(), m_rect.getY() + 2, Color::Yellow);
    51	}
    52	
    53	void GuiWindow::addGuiObject(std::unique_ptr<GuiObject> guiObject)
    54	{
    55	    gui_objects.push_back(std::move(guiObject));
    56	}
    57	
    58	
    59	void GuiWindow::onNotifyMouseEvent(const s_MouseEvent &event)
    60	{
    61	    for (auto &guiObject : gui_objects) {
    62	        guiObject->onNotifyMouseEvent(event);
    63	    }
    64	}
    65	
    66	cRectangle GuiWindow::getRelativeRect(int x, int y, int width, int height)
    67	{
    68	    return cRectangle(x + m_rect.getX(), y + m_rect.getY(), width, height);
    69	}
    70	
    71	void GuiWindow::onNotifyKeyboardEvent(const cKeyboardEvent &event)
    72	{
    73	    if (event.isType(eKeyEventType::PRESSED)) {
    74	        for (auto &guiObject : gui_objects) {
    75	            guiObject->onNotifyKeyboardEvent(event);
    76	        }
    77	    }
    78	}
    79	
    80	bool GuiWindow::hasFocusedInput() const
    81	{
    82	    for (const auto &guiObject : gui_objects) {
    83	        if (guiObject->hasKeyboardFocus()) {
    84	            return true;
    85	        }
    86	    }
    87	
    88	    return false;
    89	}
```

### src/gui/GuiButton.h@c583461

```console
$ git show c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiButton.h | nl -ba
     1	/**
     2	 * @file GuiButton.h
     3	 *
     4	 * Dune 2 - The Maker
     5	 *
     6	 * @author Stefan Hendriks & the D2TM Team
     7	 * @www http://www.dune2themaker.com
     8	 * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
     9	 * @license This software is released under the MIT License. See LICENSE.md.
    10	 *
    11	 * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
    12	 *
    13	 * This is a non-commercial educational project.
    14	 */
    15	
    16	#pragma once
    17	
    18	#include "GuiObject.h"
    19	class cRectangle;
    20	
    21	#include <string>
    22	#include <functional>
    23	#include <memory>
    24	
    25	class SDLDrawer;
    26	class cTextDrawer;
    27	
    28	
    29	class GuiButton : public GuiObject, public GuiClickable, public GuiTextual, public GuiStatefulVisual {
    30	public:
    31	    GuiButton(SDLDrawer* drawer, const cRectangle &rect, const std::string &btnText);
    32	    ~GuiButton();
    33	
    34	    // From cInputObserver
    35	    void onNotifyMouseEvent(const s_MouseEvent &event) override;
    36	    void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
    37	
    38	    // From GuiObject
    39	    void draw() const override;
    40	
    41	    // From GuiTextual
    42	    void setTextAlignHorizontal(GuiTextAlignHorizontal value) override;
    43	    void setTextDrawer(cTextDrawer *cTextDrawer) override;
    44	    void setText(const std::string& text) override;
    45	
    46	    // From GuiClickable
    47	    void setEnabled(bool value) override;
    48	    bool isEnabled() const override;
    49	    void setOnLeftMouseButtonClickedAction(std::function<void()> action) override;
    50	    void setOnRightMouseButtonClickedAction(std::function<void()> action) override;
    51	
    52	    // From GuiStatefulVisual
    53	    void setVisualState(VisualState state) override;
    54	    VisualState visualState() const override;
    55	
    56	    void setRenderKind(GuiRenderKind value);
    57	    void setTexture(Texture *tex);
    58	    void setTextScale(float scale);
    59	    void setTextOffsetY(int offset);
    60	
    61	    void nextRenderKind();
    62	
    63	    void toggleTextAlignHorizontal();
    64	
    65	private:
    66	    cTextDrawer *m_textDrawer;
    67	    std::string m_buttonText;
    68	    GuiRenderKind m_renderKind;
    69	    GuiTextAlignHorizontal m_textAlignHorizontal;
    70	    std::function<void()> m_onLeftMouseButtonClickedAction;
    71	    std::function<void()> m_onRightMouseButtonClickedAction;
    72	    Texture *m_tex;
    73	
    74	    bool m_focus;
    75	
    76	    // pressed state
    77	    bool m_pressed;
    78	    bool m_enabled;
    79	    float m_textScale = 1.0F;
    80	    int m_textOffsetY = 0;
    81	    VisualState m_visualState = VisualState::Normal;
    82	
    83	    // Functions
    84	    void drawText() const;
    85	
    86	    void onMouseMovedTo(const s_MouseEvent &event);
    87	
    88	    void onMouseRightButtonPressed(const s_MouseEvent &event);
    89	    void onMouseRightButtonClicked(const s_MouseEvent &event);
    90	    void onMouseLeftButtonPressed(const s_MouseEvent &event);
    91	    void onMouseLeftButtonClicked(const s_MouseEvent &event);
    92	};
    93	
    94	
    95	class GuiButtonBuilder {
    96	public:
    97	    GuiButtonBuilder& withTextDrawer(cTextDrawer* drawer) {
    98	        this->m_drawer = drawer;
    99	        return *this;
   100	    }
   101	
   102	    GuiButtonBuilder& withRect(const cRectangle& rect) {
   103	        this->m_rect = rect;
   104	        return *this;
   105	    }
   106	
   107	    GuiButtonBuilder& withRenderer(SDLDrawer* render) {
   108	        this->m_renderer = render;
   109	        return *this;
   110	    }
   111	
   112	    GuiButtonBuilder& withLabel(const std::string& label) {
   113	        this->m_label = label;
   114	        return *this;
   115	    }
   116	
   117	    GuiButtonBuilder& withKind(GuiRenderKind kind) {
   118	        this->m_kind = kind;
   119	        return *this;
   120	    }
   121	
   122	    GuiButtonBuilder& withTheme(const GuiTheme& theme) {
   123	        this->m_theme = theme;
   124	        return *this;
   125	    }
   126	
   127	    GuiButtonBuilder& withTextAlign(GuiTextAlignHorizontal align) {
   128	        this->m_align = align;
   129	        return *this;
   130	    }
   131	
   132	    GuiButtonBuilder& onClick(std::function<void()> callback) {
   133	        this->m_onLeftClick = std::move(callback);
   134	        return *this;
   135	    }
   136	
   137	    GuiButtonBuilder& onRightClick(std::function<void()> callback) {
   138	        this->m_onRightClick = std::move(callback);
   139	        return *this;
   140	    }
   141	
   142	    GuiButtonBuilder& withTexture(Texture* tex) {
   143	        this->m_tex = tex;
   144	        return *this;
   145	    }
   146	
   147	    GuiButtonBuilder& withTextScale(float scale) {
   148	        this->m_textScale = scale;
   149	        return *this;
   150	    }
   151	
   152	    GuiButtonBuilder& withTextOffsetY(int offset) {
   153	        this->m_textOffsetY = offset;
   154	        return *this;
   155	    }
   156	
   157	    GuiButtonBuilder& withEnabled(bool enabled) {
   158	        this->m_enabled = enabled;
   159	        return *this;
   160	    }
   161	
   162	    std::unique_ptr<GuiButton> build() const {
   163	        auto btn = std::make_unique<GuiButton>(m_renderer, m_rect, m_label);
   164	        btn->setTextDrawer(m_drawer);
   165	        btn->setRenderKind(m_kind);
   166	        btn->setTheme(m_theme);
   167	        btn->setTextAlignHorizontal(m_align);
   168	        btn->setTextScale(m_textScale);
   169	        btn->setTextOffsetY(m_textOffsetY);
   170	        btn->setTexture(m_tex);
   171	        btn->setEnabled(m_enabled);
   172	        if (m_onLeftClick) {
   173	            btn->setOnLeftMouseButtonClickedAction(m_onLeftClick);
   174	        }
   175	        if (m_onRightClick) {
   176	            btn->setOnRightMouseButtonClickedAction(m_onRightClick);
   177	        }
   178	        
   179	        return btn;
   180	    }
   181	
   182	private:
   183	    cTextDrawer* m_drawer = nullptr;
   184	    cRectangle m_rect;
   185	    SDLDrawer* m_renderer;
   186	    std::string m_label = "";
   187	    GuiRenderKind m_kind = GuiRenderKind::OPAQUE_WITH_BORDER;
   188	    GuiTheme m_theme = cGuiThemeBuilder().light().build();
   189	    GuiTextAlignHorizontal m_align = GuiTextAlignHorizontal::CENTER;
   190	    std::function<void()> m_onLeftClick = nullptr;
   191	    std::function<void()> m_onRightClick = nullptr;
   192	    Texture *m_tex = nullptr;
   193	    float m_textScale = 1.0F;
   194	    int m_textOffsetY = 0;
   195	    bool m_enabled = true;
   196	};
```

### git grep -h -o -E '\bGui[A-Za-z]+\b' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp | sort | uniq -c

```console
$ git grep -h -o -E '\bGui[A-Za-z]+\b' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gamestates/cEditorState.cpp src/gamestates/cNewmapEditorState.cpp | sort | uniq -c
      6 GuiBar
      4 GuiBarPlacement
      2 GuiButton
      3 GuiButtonBuilder
      5 GuiButtonGroup
      2 GuiCheckBox
      1 GuiCheckBoxBuilder
      1 GuiCycleButton
      2 GuiCycleButtonBuilder
      1 GuiLabel
      7 GuiLabelBuilder
      8 GuiRenderKind
      1 GuiStateButton
     22 GuiStateButtonBuilder
      8 GuiTextAlignHorizontal
      5 GuiTextInput
      1 GuiValueButton
      1 GuiValueButtonBuilder
      2 GuiWindow
```

### git grep -n -i 'audit' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gui

```console
$ git grep -n -i 'audit' c5834615f8fc71789bba7108078a461018cc7d56 -- src/gui
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiButton.cpp:18:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiButton.cpp:49:    if (uiaudit::isEnabled()) {
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiButton.cpp:50:        auditRecord("GuiButton");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiButton.cpp:52:            auditClick("GuiButton:" + m_buttonText);
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiCheckBox.cpp:18:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiCheckBox.cpp:42:    if (uiaudit::isEnabled()) {
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiCheckBox.cpp:43:        auditRecord("GuiCheckBox");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiCheckBox.cpp:45:            auditClick("GuiCheckBox");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiLabel.cpp:17:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiLabel.cpp:42:    if (uiaudit::isEnabled()) {
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiLabel.cpp:43:        auditRecord("GuiLabel");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp:17:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp:35:void GuiObject::auditRecord(const char *type) const
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp:37:    uiaudit::recordGui(type, m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp:40:void GuiObject::auditClick(const std::string &name) const
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.cpp:42:    uiaudit::recordClick(name.c_str(), m_rect.getX(), m_rect.getY(), m_rect.getWidth(), m_rect.getHeight());
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.h:96:    void auditRecord(const char *type) const;
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiObject.h:97:    void auditClick(const std::string &name) const;
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiSlider.cpp:17:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiSlider.cpp:76:    if (uiaudit::isEnabled()) {
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiSlider.cpp:77:        auditRecord("GuiSlider");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiSlider.cpp:78:        auditClick("GuiSlider");
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiWindow.cpp:17:#include "debug/UiAudit.hpp"
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiWindow.cpp:39:    if (uiaudit::isEnabled()) {
c5834615f8fc71789bba7108078a461018cc7d56:src/gui/GuiWindow.cpp:40:        auditRecord("GuiWindow");
```
