# Точные stdout diff-команд для дорожки 1

Ревизии: BASE `e17379ad660fca46859b403a6c3d33ec8d831a40`, FORK1 `9208dcf5a358f40afd95c99480e4e09f781ed566`, PORT `832c953a94a632d57872349013f7ed1a37434715`.
Команды выполнены с контекстом Git по умолчанию (3 строки). В каждом блоке сохранён полный stdout соответствующей команды без фильтрации.

## src/drawers/CreditsDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.cpp
```

stdout (6253 байт):

````text
diff --git a/src/drawers/CreditsDrawer.cpp b/src/drawers/CreditsDrawer.cpp
index da5a87ab..119e8466 100644
--- a/src/drawers/CreditsDrawer.cpp
+++ b/src/drawers/CreditsDrawer.cpp
@@ -7,16 +7,22 @@
 #include "utils/cSoundPlayer.h"
 #include "drawers/SDLDrawer.hpp"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/TextContext.hpp"
+#include "sidebar/HudLayout.hpp"
 #include <SDL2/SDL.h>
+#include <algorithm>
+#include <format>
 
 #include "data/gfxaudio.h"
 
 CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
     m_player(player),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer())
 {
     assert(player);
 
@@ -31,7 +37,7 @@ CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
     previousCredits = 0;
 
     // center credits bar within sidebar
-    int widthCreditsBar = (m_gfxinter->getSurface(CREDITS_BAR))->w;
+    int widthCreditsBar = m_gfxinter->getLogicalWidth(CREDITS_BAR);
     drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
     drawY = 0;
 }
@@ -179,25 +185,64 @@ void CreditsDrawer::thinkAboutIndividualCreditOffsets()
  */
 void CreditsDrawer::draw()
 {
-    auto *tex = m_gfxinter->getTexture(CREDITS_BAR);
-    renderDrawer->renderSprite(tex, drawX, drawY);
-    renderDrawer->setClippingFor(drawX+1, drawY+5, drawX+tex->w-1, drawY+tex->h-5);
-    drawCurrentCredits(drawX, drawY);
-    drawPreviousCredits(drawX, drawY);
-    renderDrawer->resetClippingFor();
-
-}
-
-int CreditsDrawer::getXDrawingOffset(int amount)
-{
-    int offset = 1;
-    if (amount > 0)		offset =  4;
-    if (amount < 10)	offset =  5;
-    if (amount > 99)	offset =  3;
-    if (amount > 999)	offset =  2;
-    if (amount > 9999) 	offset =  1;
-    if (amount > 99999) offset =  0;
-    return offset;
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const cRectangle &rect = layout.credits;
+    const Color panel{15, 19, 21, 255};
+    const Color border{155, 116, 43, 255};
+    const Color label{208, 196, 157, 255};
+    const Color amount{255, 210, 82, 255};
+
+    renderDrawer->renderRectFillColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        panel
+    );
+    renderDrawer->renderRectColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        border
+    );
+    renderDrawer->renderRectFillColor(
+        rect.getX() + 7,
+        rect.getY() + 10,
+        12,
+        14,
+        Color{205, 133, 35, 255}
+    );
+    renderDrawer->renderRectColor(
+        rect.getX() + 7,
+        rect.getY() + 10,
+        12,
+        14,
+        Color{255, 215, 103, 255}
+    );
+    m_gameTextDrawer->drawText(
+        rect.getX() + 26,
+        rect.getY() + 10,
+        label,
+        localization::text("CREDITS", "КРЕДИТЫ"),
+        false
+    );
+
+    const std::string credits = std::format(
+        "{}",
+        std::max(0, currentCredits)
+    );
+    const int amountWidth = m_gameTextDrawer->getTextLength(credits);
+    m_gameTextDrawer->drawText(
+        rect.getEndX() - amountWidth - 9,
+        rect.getY() + 10,
+        amount,
+        credits,
+        false
+    );
 }
 
 int CreditsDrawer::getCreditDrawId(char c)
@@ -215,75 +260,6 @@ int CreditsDrawer::getCreditDrawId(char c)
     return CREDITS_NONE;
 }
 
-// current credits are either drawn from 'above' or from below. (depending on direction)
-// the offset pushes them more up or down.
-void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
-{
-    if (currentCredits < 0) currentCredits = 0;
-
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", currentCredits);
-
-    int offset = getXDrawingOffset(currentCredits);
-
-    for (int i=0; i < 6; i++) {
-        // the actual position to draw on is: ((game.m_screenX - 120) +
-        //        screen        -  14 + (6 digits (each 20 pixels due borders))
-        int dx = ((offset + i) * 20);
-        int dy = 0;
-
-        // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = 20 - (int)offset_credit[i];
-        }
-        else if (offset_direction[i] == 2) {
-            dy = -20 + (int)offset_credit[i];
-        }
-
-        int nr = getCreditDrawId(credits[i]);
-
-        if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
-        }
-    }
-}
-
-// current credits are either drawn from 'above' or from below. (depending on direction)
-// the offset pushes them more up or down.
-void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
-{
-    if (previousCredits < 0) previousCredits = 0;
-
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", previousCredits);
-
-    int offset = getXDrawingOffset(previousCredits);
-
-    for (int i=0; i < 6; i++) {
-        // the actual position to draw on is: ((game.m_screenX - 120) +
-        //        screen        -  14 + (6 digits (each 20 pixels due borders))
-        int dx = ((offset + i) * 20);
-        int dy = 0;
-
-        // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = (int)offset_credit[i] * -1;
-        }
-        else if (offset_direction[i] == 2) {
-            dy = (int)offset_credit[i];
-        }
-        int nr = getCreditDrawId(credits[i]);
-
-        if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
-        }
-    }
-}
-
 // the think method will gradually update the currentCredits array so that it is 'the same'
 bool CreditsDrawer::hasDrawnCurrentCredits()
 {
````

## src/drawers/CreditsDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/CreditsDrawer.cpp
```

stdout (16086 байт):

````text
diff --git a/src/drawers/CreditsDrawer.cpp b/src/drawers/CreditsDrawer.cpp
index da5a87ab..daa24388 100644
--- a/src/drawers/CreditsDrawer.cpp
+++ b/src/drawers/CreditsDrawer.cpp
@@ -1,39 +1,85 @@
-#include "CreditsDrawer.h"
+/**
+ * @file CreditsDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
-#include "d2tmc.h"
+#include "CreditsDrawer.h"
+#include "CreditsMath.hpp"
+#include "include/sGameServices.h"
+#include "utils/common.h"
+#include "context/AudioContext.hpp"
+#include "game/cGameSettings.h"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
+#include "sidebar/cSideBar.h"
 #include "utils/cSoundPlayer.h"
 #include "drawers/SDLDrawer.hpp"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
-#include <SDL2/SDL.h>
-
 #include "data/gfxaudio.h"
 
-CreditsDrawer::CreditsDrawer(GameContext* ctx, cPlayer *player) :
+#include <SDL3/SDL.h>
+#include "include/cAssert.h"
+#include "include/Texture.hpp"
+#include <algorithm>
+#include <cstdlib>
+#include <string>
+
+namespace {
+// digits of the credits, cut off / padded with '\0' to 8 characters (what the old char[9] buffers held)
+std::string creditsToDigits(int credits)
+{
+    std::string digits = std::to_string(credits);
+    digits.resize(8, '\0');
+    return digits;
+}
+}
+
+CreditsDrawer::CreditsDrawer(GameContext* ctx, cGameSettings *settings, cPlayer *player) :
     m_player(player),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_gfxdata(ctx->getGraphicsContext()->gfxdata.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_playCreditsSound(settings->isPlayCreditsSound())
 {
-    assert(player);
-
-    memset(offset_credit, 0, sizeof(offset_credit));
-    memset(offset_direction, 0, sizeof(offset_direction));
-    initial = true;
-    soundType = -1;
-    rollSpeed = 0.0F;
-    rolled = 0;
-    soundsMade = 0;
-    currentCredits = 0;
-    previousCredits = 0;
+    d2tm_assert(player!= nullptr);
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(settings != nullptr);
+
+    std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+    std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
+    m_initial = true;
+    m_soundType = -1;
+    m_rollSpeed = 0.0F;
+    m_rolled = 0;
+    m_soundsMade = 0;
+    m_currentCredits = 0;
+    m_previousCredits = 0;
 
     // center credits bar within sidebar
-    int widthCreditsBar = (m_gfxinter->getSurface(CREDITS_BAR))->w;
-    drawX = game.m_screenW - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
-    drawY = 0;
+    int widthCreditsBar = m_gfxinter->getTexture(CREDITS_BAR)->w;
+    m_drawX = settings->getScreenW() - (cSideBar::SidebarWidthWithoutCandyBar / 2) - (widthCreditsBar / 2);
+    m_drawY = 0;
+}
+
+void CreditsDrawer::serviceInit(sGameServices* services)
+{
+    m_audioContext = services->ctx->getAudioContext();
+    m_mapCamera = services->mapCamera;
+    m_objects = services->objects;
 }
 
 CreditsDrawer::~CreditsDrawer()
@@ -48,71 +94,58 @@ void CreditsDrawer::setCredits()
 
 void CreditsDrawer::setCredits(int amount)
 {
-    initial = true;
-    previousCredits = amount;
-    currentCredits = amount;
-    memset(offset_credit, 0, sizeof(offset_credit));
-    memset(offset_direction, 0, sizeof(offset_direction));
+    m_initial = true;
+    m_previousCredits = amount;
+    m_currentCredits = amount;
+    std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+    std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
 }
 
 // timer based method
 void CreditsDrawer::thinkFast()
 {
 
-    if (hasDrawnCurrentCredits() || initial) {
-        soundsMade = 0;
+    if (hasDrawnCurrentCredits() || m_initial) {
+        m_soundsMade = 0;
 
-        memset(offset_credit, 0, sizeof(offset_credit));
-        memset(offset_direction, 0, sizeof(offset_direction));
+        std::fill(std::begin(m_offset_credit), std::end(m_offset_credit), 0.0f);
+        std::fill(std::begin(m_offset_direction), std::end(m_offset_direction), 0);
 
-        // determine new currentCredits
+        // determine new m_currentCredits
         // TODO: make it 'roll' instead of 'jump' to the newest credits?
-        previousCredits = currentCredits;
+        m_previousCredits = m_currentCredits;
         auto newCurrentCredits = m_player->getCredits();
 
-        if (newCurrentCredits != previousCredits) {
-            int diff = newCurrentCredits - previousCredits;
-            // when big difference, slice it up in pieces so we
-            // have a more fluent transition
-            if (diff > 200) {
-                currentCredits = previousCredits + (diff / 8);
-            }
-            else if (diff > 20) {
-                currentCredits = previousCredits + (diff / 4);
-            }
-            else {
-                currentCredits = newCurrentCredits;
-            }
-        }
+        m_currentCredits = CreditsMath::nextDisplayedCredits(m_previousCredits, newCurrentCredits);
 
         // decide what sound to play when done
-        if (currentCredits > previousCredits) {
-            soundType = SOUND_CREDITUP;
+        if (m_currentCredits > m_previousCredits) {
+            m_soundType = SOUND_CREDITUP;
         }
-        else if (currentCredits < previousCredits) {
-            soundType = SOUND_CREDITDOWN;
+        else if (m_currentCredits < m_previousCredits) {
+            m_soundType = SOUND_CREDITDOWN;
         }
         else {
-            soundType = -1;
+            m_soundType = -1;
         }
 
-        TIMER_money++;
-        if (TIMER_money > 20) {
-            if (rollSpeed > 0.0F) {
-                rollSpeed -= 0.005;
+        m_TIMER_money++;
+        if (m_TIMER_money > 20) {
+            if (m_rollSpeed > 0.0F) {
+                m_rollSpeed -= 0.005;
             }
-            if (rollSpeed < 0.0F) {
-                rollSpeed = 0.0F;
-                TIMER_money = 0;
+            if (m_rollSpeed < 0.0F) {
+                m_rollSpeed = 0.0F;
+                m_TIMER_money = 0;
             }
         }
 
-        initial = false;
+        m_initial = false;
     }
     else {
-        TIMER_money = 0;
-        if (rollSpeed < 3.0F) {
-            rollSpeed += 0.005;
+        m_TIMER_money = 0;
+        if (m_rollSpeed < 3.0F) {
+            m_rollSpeed += 0.005;
         }
         thinkAboutIndividualCreditOffsets();
     }
@@ -122,54 +155,50 @@ void CreditsDrawer::thinkFast()
 // it has to go 'up' or 'down'
 void CreditsDrawer::thinkAboutIndividualCreditOffsets()
 {
-    char current_credits[9];
-    char previous_credits[9];
-    memset(current_credits, 0, sizeof(current_credits));
-    memset(previous_credits, 0, sizeof(previous_credits));
-    snprintf(current_credits, sizeof(current_credits), "%d", currentCredits);
-    snprintf(previous_credits, sizeof(previous_credits), "%d", previousCredits);
+    std::string current_credits = creditsToDigits(m_currentCredits);
+    std::string previous_credits = creditsToDigits(m_previousCredits);
 
     for (int i = 0; i < 6; i++) {
-        int currentId = getCreditDrawId(current_credits[i]);
-        int previousId = getCreditDrawId(previous_credits[i]);
+        int currentId = CreditsMath::getCreditDrawId(current_credits[i]);
+        int previousId = CreditsMath::getCreditDrawId(previous_credits[i]);
 
-        if (offset_direction[i] == 0) {
+        if (m_offset_direction[i] == 0) {
             if (currentId == CREDITS_NONE || previousId == CREDITS_NONE) {
                 // either of the 2 is unidentifiable. Do nothing
-                offset_direction[i] = 3;
+                m_offset_direction[i] = 3;
                 continue; // next
             }
 
             // UP/DOWN ANIMATION: Is over the entire sum of money, so all 'credits' move the same
             // way.
-            if (currentCredits > previousCredits) {
-                offset_direction[i] = 1;
+            if (m_currentCredits > m_previousCredits) {
+                m_offset_direction[i] = 1;
             }
-            else if (previousCredits > currentCredits) {
-                offset_direction[i] = 2;
+            else if (m_previousCredits > m_currentCredits) {
+                m_offset_direction[i] = 2;
             }
 
             // when the same, do not animate
             if (currentId == previousId) {
-                offset_direction[i] = 3;
+                m_offset_direction[i] = 3;
             }
 
         }
 
         // always 'add' here, the draw routine knows how to handle this for up/down movement.
-        if (offset_credit[i] > 18.0F) {
-            //offset_credit[i] = 18.1F; // so we do not keep matching our IF :)
-            offset_credit[i] = 0.0F; // so we do not keep matching our IF :)
-            if (soundsMade < 7) {
-                game.playSound(soundType, 32);
-                soundsMade++;
+        if (m_offset_credit[i] > 18.0F) {
+            //m_offset_credit[i] = 18.1F; // so we do not keep matching our IF :)
+            m_offset_credit[i] = 0.0F; // so we do not keep matching our IF :)
+            if (m_playCreditsSound && m_soundsMade < 7) {
+                playSoundWithDistance(m_audioContext, m_mapCamera, m_objects, m_soundType, 32);
+                m_soundsMade++;
             }
             // it is fully 'moved'. Now update the array.
             previous_credits[i] = current_credits[i];
-            previousCredits = atoi(previous_credits);
+            m_previousCredits = std::atoi(previous_credits.c_str());
         }
         else {
-            offset_credit[i] += 1.0F * rollSpeed;
+            m_offset_credit[i] += 1.0F * m_rollSpeed;
         }
     }
 }
@@ -180,52 +209,23 @@ void CreditsDrawer::thinkAboutIndividualCreditOffsets()
 void CreditsDrawer::draw()
 {
     auto *tex = m_gfxinter->getTexture(CREDITS_BAR);
-    renderDrawer->renderSprite(tex, drawX, drawY);
-    renderDrawer->setClippingFor(drawX+1, drawY+5, drawX+tex->w-1, drawY+tex->h-5);
-    drawCurrentCredits(drawX, drawY);
-    drawPreviousCredits(drawX, drawY);
-    renderDrawer->resetClippingFor();
+    m_sdlDrawer->renderSprite(tex, m_drawX, m_drawY);
+    m_sdlDrawer->setClippingFor(m_drawX+1, m_drawY+5, m_drawX+tex->w-1, m_drawY+tex->h-5);
+    drawCurrentCredits(m_drawX, m_drawY);
+    drawPreviousCredits(m_drawX, m_drawY);
+    m_sdlDrawer->resetClippingFor();
 
 }
 
-int CreditsDrawer::getXDrawingOffset(int amount)
-{
-    int offset = 1;
-    if (amount > 0)		offset =  4;
-    if (amount < 10)	offset =  5;
-    if (amount > 99)	offset =  3;
-    if (amount > 999)	offset =  2;
-    if (amount > 9999) 	offset =  1;
-    if (amount > 99999) offset =  0;
-    return offset;
-}
-
-int CreditsDrawer::getCreditDrawId(char c)
-{
-    if (c == '0') return CREDITS_0;
-    if (c == '1') return CREDITS_1;
-    if (c == '2') return CREDITS_2;
-    if (c == '3') return CREDITS_3;
-    if (c == '4') return CREDITS_4;
-    if (c == '5') return CREDITS_5;
-    if (c == '6') return CREDITS_6;
-    if (c == '7') return CREDITS_7;
-    if (c == '8') return CREDITS_8;
-    if (c == '9') return CREDITS_9;
-    return CREDITS_NONE;
-}
-
 // current credits are either drawn from 'above' or from below. (depending on direction)
 // the offset pushes them more up or down.
 void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
 {
-    if (currentCredits < 0) currentCredits = 0;
+    if (m_currentCredits < 0) m_currentCredits = 0;
 
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", currentCredits);
+    std::string credits = creditsToDigits(m_currentCredits);
 
-    int offset = getXDrawingOffset(currentCredits);
+    int offset = CreditsMath::getXDrawingOffset(m_currentCredits);
 
     for (int i=0; i < 6; i++) {
         // the actual position to draw on is: ((game.m_screenX - 120) +
@@ -234,18 +234,18 @@ void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
         int dy = 0;
 
         // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = 20 - (int)offset_credit[i];
+        if (m_offset_direction[i] == 1) {
+            // up, means it comes from 'below' and the m_offset_credit is the 'coming up' part.
+            dy = 20 - static_cast<int>(m_offset_credit[i]);
         }
-        else if (offset_direction[i] == 2) {
-            dy = -20 + (int)offset_credit[i];
+        else if (m_offset_direction[i] == 2) {
+            dy = -20 + static_cast<int>(m_offset_credit[i]);
         }
 
-        int nr = getCreditDrawId(credits[i]);
+        int nr = CreditsMath::getCreditDrawId(credits[i]);
 
         if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
+            m_sdlDrawer->renderSprite(m_gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
         }
     }
 }
@@ -254,13 +254,11 @@ void CreditsDrawer::drawCurrentCredits(int drawX, int drawY)
 // the offset pushes them more up or down.
 void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
 {
-    if (previousCredits < 0) previousCredits = 0;
+    if (m_previousCredits < 0) m_previousCredits = 0;
 
-    char credits[9];
-    memset(credits, 0, sizeof(credits));
-    snprintf(credits, sizeof(credits), "%d", previousCredits);
+    std::string credits = creditsToDigits(m_previousCredits);
 
-    int offset = getXDrawingOffset(previousCredits);
+    int offset = CreditsMath::getXDrawingOffset(m_previousCredits);
 
     for (int i=0; i < 6; i++) {
         // the actual position to draw on is: ((game.m_screenX - 120) +
@@ -269,25 +267,25 @@ void CreditsDrawer::drawPreviousCredits(int drawX, int drawY)
         int dy = 0;
 
         // the Y is per credit direction
-        if (offset_direction[i] == 1) {
-            // up, means it comes from 'below' and the offset_credit is the 'coming up' part.
-            dy = (int)offset_credit[i] * -1;
+        if (m_offset_direction[i] == 1) {
+            // up, means it comes from 'below' and the m_offset_credit is the 'coming up' part.
+            dy = static_cast<int>(m_offset_credit[i]) * -1;
         }
-        else if (offset_direction[i] == 2) {
-            dy = (int)offset_credit[i];
+        else if (m_offset_direction[i] == 2) {
+            dy = static_cast<int>(m_offset_credit[i]);
         }
-        int nr = getCreditDrawId(credits[i]);
+        int nr = CreditsMath::getCreditDrawId(credits[i]);
 
         if (nr != CREDITS_NONE) {
-            renderDrawer->renderSprite(gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
+            m_sdlDrawer->renderSprite(m_gfxdata->getTexture(nr), drawX+dx+8, drawY+dy+8);
         }
     }
 }
 
-// the think method will gradually update the currentCredits array so that it is 'the same'
+// the think method will gradually update the m_currentCredits array so that it is 'the same'
 bool CreditsDrawer::hasDrawnCurrentCredits()
 {
-    return previousCredits == currentCredits;
+    return m_previousCredits == m_currentCredits;
 }
 
 void CreditsDrawer::setPlayer(cPlayer *thePlayer)
@@ -300,7 +298,7 @@ void CreditsDrawer::setPlayer(cPlayer *thePlayer)
 // thinkAboutIndividualCreditOffsets
 //
 //			if (currentId > previousId) {
-//				offset_direction[i] = 1; // UP
+//				m_offset_direction[i] = 1; // UP
 //			} else if (currentId < previousId) {
-//				offset_direction[i] = 2; // DOWN
+//				m_offset_direction[i] = 2; // DOWN
 //			}
````

## src/drawers/CreditsDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/CreditsDrawer.h
```

stdout (794 байт):

````text
diff --git a/src/drawers/CreditsDrawer.h b/src/drawers/CreditsDrawer.h
index 76f39a43..9b9d6498 100644
--- a/src/drawers/CreditsDrawer.h
+++ b/src/drawers/CreditsDrawer.h
@@ -10,6 +10,7 @@
 class GameContext;
 class Graphics;
 class cPlayer;
+class cTextDrawer;
 struct SDL_Surface;
 
 // the credits drawer takes state of a player, and draws the credits accordingly
@@ -30,12 +31,10 @@ private:
     cPlayer *m_player;  //
     GameContext* m_ctx;
     Graphics* m_gfxinter;
+    cTextDrawer *m_gameTextDrawer;
 
     void thinkAboutIndividualCreditOffsets();
-    void drawCurrentCredits(int drawX, int drawY);
-    void drawPreviousCredits(int drawX, int drawY);
     int getCreditDrawId(char c);
-    int getXDrawingOffset(int amount);
 
     int TIMER_money;	// timer needed to do logic
 
````

## src/drawers/CreditsDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/CreditsDrawer.h
```

stdout (3443 байт):

````text
diff --git a/src/drawers/CreditsDrawer.h b/src/drawers/CreditsDrawer.h
index 76f39a43..689811ff 100644
--- a/src/drawers/CreditsDrawer.h
+++ b/src/drawers/CreditsDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file CreditsDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /*
  * CreditsDrawer.h
  *
@@ -8,17 +23,25 @@
 #pragma once
 
 class GameContext;
+class cGameSettings;
 class Graphics;
 class cPlayer;
 struct SDL_Surface;
+class SDLDrawer;
+class AudioContext;
+class cMapCamera;
+class cGameObjectContext;
+struct sGameServices;
 
 // the credits drawer takes state of a player, and draws the credits accordingly
 
 class CreditsDrawer {
 public:
-    explicit CreditsDrawer(GameContext* ctx, cPlayer *player);
+    explicit CreditsDrawer(GameContext* ctx, cGameSettings *settings, cPlayer *player);
     virtual ~CreditsDrawer();
 
+    void serviceInit(sGameServices* services);
+
     void thinkFast(); // set animation counters and such, time based. Also make sound when needed.
 
     void draw();
@@ -29,34 +52,38 @@ public:
 private:
     cPlayer *m_player;  //
     GameContext* m_ctx;
+    AudioContext* m_audioContext = nullptr;
+    cMapCamera* m_mapCamera = nullptr;
+    cGameObjectContext* m_objects = nullptr;
     Graphics* m_gfxinter;
+    Graphics* m_gfxdata;
+    SDLDrawer* m_sdlDrawer = nullptr;
+    bool m_playCreditsSound = true;
 
     void thinkAboutIndividualCreditOffsets();
     void drawCurrentCredits(int drawX, int drawY);
     void drawPreviousCredits(int drawX, int drawY);
-    int getCreditDrawId(char c);
-    int getXDrawingOffset(int amount);
 
-    int TIMER_money;	// timer needed to do logic
+    int m_TIMER_money;	// timer needed to do logic
 
-    float rollingSpeed;	// the 'rolling speed' of the credits. Need to be sped up when just starting
+    float m_rollingSpeed;	// the 'rolling speed' of the credits. Need to be sped up when just starting
     // to withdrawn money.
 
-    int currentCredits;		// current credits we want to draw
-    int previousCredits;	// previous credits we wanted to draw
+    int m_currentCredits;		// current credits we want to draw
+    int m_previousCredits;	// previous credits we wanted to draw
 
     // the offset of the current 'credit' being drawn (the Y offset)
-    float offset_credit[7];
-    int offset_direction[7]; // direction (0 = not yet determined / finished, 1 = UP, 2 = DOWN , 3 = DO NOTHING
+    float m_offset_credit[7];
+    int m_offset_direction[7]; // direction (0 = not yet determined / finished, 1 = UP, 2 = DOWN , 3 = DO NOTHING
 
     bool hasDrawnCurrentCredits();	// returns true whenever the new state has been finalized.
 
-    bool initial;
-    int soundType;
-    float rollSpeed;
-    int rolled; // how many credits did get rolled over?
-    int soundsMade; // sounds made per time frame
+    bool m_initial;
+    int m_soundType;
+    float m_rollSpeed;
+    int m_rolled; // how many credits did get rolled over?
+    int m_soundsMade; // sounds made per time frame
 
     // topleft position of credits-bar bmp
-    int drawX, drawY;
+    int m_drawX, m_drawY;
 };
````

## src/drawers/cBuildingListDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.cpp
```

stdout (28207 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.cpp b/src/drawers/cBuildingListDrawer.cpp
index eb979610..8b935d08 100644
--- a/src/drawers/cBuildingListDrawer.cpp
+++ b/src/drawers/cBuildingListDrawer.cpp
@@ -5,18 +5,67 @@
 #include "data/gfxinter.h"
 #include "player/cPlayer.h"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
+#include "utils/common.h"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 
 #include <SDL2/SDL.h>
+#include <algorithm>
 #include <format>
+#include <sstream>
+#include <vector>
+
+namespace {
+void removeLastUtf8CodePoint(std::string &text)
+{
+    if (text.empty()) {
+        return;
+    }
+    std::size_t position = text.size() - 1;
+    while (position > 0 &&
+           (static_cast<unsigned char>(text[position]) & 0xC0U) == 0x80U) {
+        --position;
+    }
+    text.erase(position);
+}
+
+std::string fitWithEllipsis(
+    const cTextDrawer *drawer,
+    std::string text,
+    int maximumWidth)
+{
+    if (drawer->getTextLength(text) <= maximumWidth) {
+        return text;
+    }
+    constexpr const char *ellipsis = "…";
+    while (!text.empty() &&
+           drawer->getTextLength(text + ellipsis) > maximumWidth) {
+        removeLastUtf8CodePoint(text);
+    }
+    return text + ellipsis;
+}
+
+std::string compactCardName(const std::string &name)
+{
+    // Keep canonical names in status messages and save-independent game data,
+    // but use familiar short forms in the narrow construction cards.
+    if (name == localization::text("Hi-Tech", "Авиазавод")) return localization::text("Hi-Tech", "Авиазавод");
+    if (name == localization::text("Spice Refinery", "Переработчик пряности")) return localization::text("Refinery", "Переработчик");
+    if (name == localization::text("MCV", "Мобильная база")) return localization::text("MCV", "Мобильная база");
+    if (name == localization::text("Light Infantry", "Отряд пехоты")) return localization::text("Infantry", "Пехота");
+    if (name == localization::text("Troopers", "Отряд ракетчиков")) return localization::text("Troopers", "Ракетчики");
+    return name;
+}
+}
 
 cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
     m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
     m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_player(player),
-    m_renderListIds(false)
+    m_renderListIds(false),
+    m_readyLabel(localization::text("READY", "ГОТОВО"))
 {
 }
 
@@ -48,8 +97,8 @@ void cBuildingListDrawer::drawButtonHoverRectangle(cBuildingList *list)
     int y = list->getButtonDrawY();
     int id = list->getButtonIconIdUnpressed();
 
-    int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int width = list->getButtonWidth();
+    int height = list->getButtonHeight();
 
     Color color = m_player->getSelectFadingColor();
 
@@ -76,47 +125,77 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
     }
 
 //	int width = (gfxinter->getSurface(id))->w;
-    int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
-
-    // clear
-    renderDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
-
-    // set blender
-    renderDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
-
+    int width = list->getButtonWidth();
+    int height = list->getButtonHeight();
+
+    const Color panel{18, 22, 25, 255};
+    const Color border{93, 78, 49, 255};
+    const Color active{217, 164, 54, 255};
+    renderDrawer->renderRectFillColor(x, y, width, height, panel);
+
+    Texture *icon = m_gfxinter->getTexture(id);
+    const int availableWidth = std::max(1, width - 8);
+    const int availableHeight = std::max(1, height - 6);
+    const float scale = std::min(
+        static_cast<float>(availableWidth) / icon->w,
+        static_cast<float>(availableHeight) / icon->h
+    );
+    const int iconWidth = std::max(1, static_cast<int>(icon->w * scale));
+    const int iconHeight = std::max(1, static_cast<int>(icon->h * scale));
+    const cRectangle iconRect(
+        x + (width - iconWidth) / 2,
+        y + (height - iconHeight) / 2,
+        iconWidth,
+        iconHeight
+    );
+    renderDrawer->renderStrechFullSprite(
+        icon,
+        iconRect,
+        list->isAvailable() ? 255 : 96
+    );
     if (!list->isAvailable()) {
-        renderDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
+        renderDrawer->renderRectFillColor(
+            iconRect,
+            Color{20, 22, 23, 255},
+            138
+        );
     }
-
+    renderDrawer->renderRectColor(
+        x,
+        y,
+        width,
+        height,
+        pressed ? active : border
+    );
     if (pressed) {
+        renderDrawer->renderRectFillColor(
+            x + 2,
+            y + height - 3,
+            width - 4,
+            2,
+            active
+        );
         list->stopFlashing();
-
-        Color color = m_player->getHouseFadingColor();
-
-        renderDrawer->renderRectColor(x, y, width, height, color);
-        renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
     }
-    else {
-        if (list->isFlashing()) {
-            Color color = list->getFlashingColor();
-
-            renderDrawer->renderRectColor(x, y, width, height, color);
-            renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
-            renderDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
-        }
+    else if (list->isFlashing()) {
+        renderDrawer->renderRectColor(
+            x + 1,
+            y + 1,
+            width - 2,
+            height - 2,
+            list->getFlashingColor()
+        );
     }
 }
 
-
 int cBuildingListDrawer::getDrawX()
 {
-    return (game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar) + 2;
+    return getLayout().cards.getX();
 }
 
 int cBuildingListDrawer::getDrawY()
 {
-    return cSideBar::TopBarHeight + 230 + 30;
+    return getLayout().cards.getY();
 }
 
 /**
@@ -126,6 +205,9 @@ int cBuildingListDrawer::getDrawY()
  */
 void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)
 {
+    const HudLayout layout = getLayout(list);
+    const int scrollRow = getScrollRow(list);
+
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
@@ -138,11 +220,18 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     std::array<int, 6> isBuildingItemInList = list->isBuildingItem();
 
     // Start drawing the 'icons grid'
-    int withOfIcon = 63;
-    int heightOfIcon = 47;
-
-    // draw the icons, in rows of 3
-    int rowNr = 0;
+    int withOfIcon = getCardWidth();
+    int heightOfIcon = getCardHeight();
+
+    renderDrawer->setClippingFor(
+        layout.cards.getX(),
+        layout.cards.getY(),
+        layout.cards.getEndX(),
+        layout.cards.getEndY()
+    );
+
+    // Draw the visible icon rows. HD positions come from HudLayout so drawing
+    // and hit testing cannot drift apart.
     for (int i = 0; i < end; i++) {
         cBuildingListItem *item = list->getItem(i);
 
@@ -150,6 +239,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             continue; // allow gaps in the list data structure (just not with rendering)
         }
 
+        const cRectangle card = layout.cardRect(i, scrollRow);
+        if (card.getEndY() <= layout.cards.getY() ||
+            card.getY() >= layout.cards.getEndY()) {
+            continue;
+        }
+        iDrawX = card.getX();
+        iDrawY = card.getY();
+
         int iDrawXEnd = iDrawX + withOfIcon;
         int iDrawYEnd = iDrawY + heightOfIcon;
 
@@ -159,7 +256,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         // icon id must be set , assert it.
         assert(item->getIconId() > -1);
 
-        renderDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
+        drawHdCard(item, iDrawX, iDrawY);
 
         if (shouldDrawStructureSize) {
             drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
@@ -170,27 +267,52 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             int iFrame = item->getBuildProgressFrame();
 
             if (!item->isDoneBuilding() || iFrame < 31) {
-                // draw the other progress stuff
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+                const int progressWidth = std::clamp(
+                    (withOfIcon - 4) * iFrame / 31,
+                    0,
+                    withOfIcon - 4
+                );
+                const int progressY = iDrawY + heightOfIcon - 36;
+                renderDrawer->renderRectFillColor(
+                    iDrawX + 2,
+                    progressY,
+                    withOfIcon - 4,
+                    4,
+                    15,
+                    18,
+                    20,
+                    230
+                );
+                renderDrawer->renderRectFillColor(
+                    iDrawX + 2,
+                    progressY,
+                    progressWidth,
+                    4,
+                    selectFadingColor
+                );
             }
             else {
                 if (item->shouldPlaceIt()) {
-                    // TODO: draw white/red (flicker)
-                    int icon = READY01;
-                    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) {
-                        icon = READY02;
-                    }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    const Color readyColor = m_player->isContextMouseState(
+                        eMouseState::MOUSESTATE_PLACE
+                    ) ? Color{225, 48, 42, 255} : Color::white();
+                    m_smallTextDrawer->drawTextScaledCenteredInBox(
+                        m_readyLabel,
+                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
+                        1.0F,
+                        readyColor
+                    );
                 }
                 else if (item->shouldDeployIt()) {
-                    // TODO: draw white/red (flicker)
-                    // TODO: draw DEPLOY
-                    int icon = READY01;
-                    if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) {
-                        icon = READY02;
-                    }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    const Color readyColor = m_player->isContextMouseState(
+                        eMouseState::MOUSESTATE_DEPLOY
+                    ) ? Color{225, 48, 42, 255} : Color::white();
+                    m_smallTextDrawer->drawTextScaledCenteredInBox(
+                        m_readyLabel,
+                        cRectangle(iDrawX + 2, iDrawY + 2, withOfIcon - 4, heightOfIcon - 32),
+                        1.0F,
+                        readyColor
+                    );
                 }
             }
         }
@@ -213,7 +335,16 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             }
 
             if (!item->isAvailable() || isBuildingSameSubListItem) {
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                renderDrawer->renderRectFillColor(
+                    iDrawX,
+                    iDrawY,
+                    withOfIcon,
+                    heightOfIcon - 32,
+                    0,
+                    0,
+                    0,
+                    128
+                );
 
                 // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
                 if (item->isPendingUpgrading()) {
@@ -223,7 +354,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
                     Color red = Color{255, 0, 0,255};
-                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
+                    m_smallTextDrawer->drawTextCenteredInBox(localization::text("Upgrade", "Улучшение"), iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
                 }
 
                 // Pending building (ie: a build is progressing, blocking the upgrade)
@@ -234,10 +365,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
                     Color red = Color{255, 0, 0, 255};
-                    int height = heightOfIcon / 3;
-                    m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, red);
+                    m_smallTextDrawer->drawTextCenteredInBox(
+                        localization::text("OCCUPIED", "ЗАНЯТО"),
+                        iDrawX,
+                        iDrawY,
+                        withOfIcon,
+                        heightOfIcon,
+                        red
+                    );
                 }
             }
 
@@ -245,7 +380,16 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 // only for starport show you can't pay it, as we allow building units when you cannot pay it (ie partial
                 // payment/progress)
                 if (cannotPayIt) {
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                    renderDrawer->renderRectFillColor(
+                        iDrawX,
+                        iDrawY,
+                        withOfIcon,
+                        heightOfIcon - 32,
+                        0,
+                        0,
+                        0,
+                        128
+                    );
                     Color errorFadingColor = m_player->getErrorFadingColor();
                     renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
                     renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
@@ -273,13 +417,24 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 
         if (showAmount) {
             // draw number of times to build this thing (queueing)
-            int textX = iDrawX + 41;
-            int textY = iDrawY + 16;
+            int textX = iDrawX + withOfIcon - 20;
+            int textY = iDrawY + heightOfIcon - 51;
 
             if (amountToShow < 10) {
-                textX += 10;
+                textX += 6;
             }
 
+            renderDrawer->renderRectFillColor(
+                textX - 3,
+                textY - 1,
+                withOfIcon - (textX - iDrawX) - 1,
+                16,
+                8,
+                10,
+                12,
+                220
+            );
+
             // draw
             m_gameTextDrawer->drawText(textX, textY, std::format("{}",amountToShow));
         }
@@ -306,18 +461,10 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
             }
         }
-
-        // update coordinates, 3 icons in a row
-        if (rowNr < 2) {
-            iDrawX+=66;
-            rowNr++;
-        }
-        else {
-            rowNr = 0;
-            iDrawX=getDrawX();
-            iDrawY+=50;
-        }
     }
+
+    renderDrawer->resetClippingFor();
+    drawHdScrollbar(list, layout);
 }
 
 /**
@@ -347,14 +494,19 @@ void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
         iTile = GRID_3X3;
     }
 
-    renderDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
+    const int gridX = x + getCardWidth() - 22;
+    const int gridY = y + 3;
+    renderDrawer->renderRectFillColor(gridX, gridY,19,19,8,10,12,220);
+    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), gridX, gridY);
+    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), gridX, gridY);
 }
 
 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
 {
-    if (x >= drawX && x <= (drawX + 64) && y >= drawY && y < (drawY + 48)) {
+    if (x >= drawX &&
+        x <= drawX + getCardWidth() &&
+        y >= drawY &&
+        y < drawY + getCardHeight()) {
         return true;
     }
     return false;
@@ -363,33 +515,204 @@ bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX,
 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
 {
     assert(list != nullptr);
-    // starting draw coordinates
-    int iDrawX=getDrawX();
-    int iDrawY=getDrawY();
-
-    int end = MAX_ITEMS;
 
-    int rowNr = 0;
-    for (int i = 0; i < end; i++) {
+    const HudLayout layout = getLayout(list);
+    if (!layout.cards.isPointWithin(x, y)) {
+        return nullptr;
+    }
+    const int scrollRow = getScrollRow(list);
+    for (int i = 0; i < list->getItemCount(); ++i) {
         cBuildingListItem *item = list->getItem(i);
-        if (item == nullptr) break;
-
-        if (isOverItemCoordinates_Boolean(x, y, iDrawX, iDrawY)) {
+        if (item == nullptr) {
+            continue;
+        }
+        const cRectangle card = layout.cardRect(i, scrollRow);
+        if (card.getY() < layout.cards.getY() ||
+            card.getEndY() > layout.cards.getEndY()) {
+            continue;
+        }
+        if (card.isPointWithin(x, y)) {
             return item;
         }
+    }
+    return nullptr;
+}
+
+int cBuildingListDrawer::getCardWidth() const
+{
+    return getLayout().cardWidth;
+}
 
-        if (rowNr < 2) {
-            rowNr++;
-            iDrawX+=66;
+int cBuildingListDrawer::getCardHeight() const
+{
+    return getLayout().cardHeight;
+}
+
+void cBuildingListDrawer::drawHdCard(
+    cBuildingListItem *item,
+    int x,
+    int y)
+{
+    const int cardWidth = getCardWidth();
+    const int cardHeight = getCardHeight();
+    const int labelHeight = 32;
+    const int imageHeight = cardHeight - labelHeight;
+    const Color panelColor{18, 22, 25, 255};
+    const Color borderColor{142, 111, 51, 255};
+    const Color innerBorder{56, 61, 62, 255};
+    const Color labelColor{232, 225, 196, 255};
+    const Color priceColor{255, 205, 73, 255};
+
+    renderDrawer->renderRectFillColor(
+        x,
+        y,
+        cardWidth,
+        cardHeight,
+        panelColor
+    );
+
+    Texture *icon = m_gfxinter->getTexture(item->getIconId());
+    renderDrawer->renderStrechSprite(
+        icon,
+        cRectangle(0, 0, icon->w, icon->h),
+        cRectangle(x + 3, y + 3, cardWidth - 6, imageHeight - 5)
+    );
+
+    renderDrawer->renderRectFillColor(
+        x + 1,
+        y + imageHeight,
+        cardWidth - 2,
+        labelHeight - 1,
+        panelColor
+    );
+    renderDrawer->renderRectColor(
+        x,
+        y,
+        cardWidth,
+        cardHeight,
+        borderColor
+    );
+    renderDrawer->renderRectColor(
+        x + 1,
+        y + 1,
+        cardWidth - 2,
+        cardHeight - 2,
+        innerBorder
+    );
+    renderDrawer->renderLine(
+        x + 2,
+        y + imageHeight,
+        x + cardWidth - 3,
+        y + imageHeight,
+        borderColor
+    );
+
+    const std::string name = compactCardName(item->getNameString());
+    const int textWidth = cardWidth - 6;
+    if (m_smallTextDrawer->getTextLength(name) <= textWidth) {
+        m_smallTextDrawer->drawTextCenteredInBox(
+            name,
+            x + 3,
+            y + imageHeight,
+            textWidth,
+            labelHeight,
+            labelColor
+        );
+    }
+    else {
+        std::istringstream stream(name);
+        std::vector<std::string> words;
+        std::string word;
+        while (stream >> word) {
+            words.push_back(word);
+        }
+
+        std::string firstLine;
+        std::string secondLine;
+        for (const auto &candidateWord : words) {
+            const std::string candidate = firstLine.empty()
+                ? candidateWord
+                : firstLine + " " + candidateWord;
+            if (secondLine.empty() &&
+                m_smallTextDrawer->getTextLength(candidate) <= textWidth) {
+                firstLine = candidate;
+            }
+            else {
+                secondLine += secondLine.empty()
+                    ? candidateWord
+                    : " " + candidateWord;
+            }
+        }
+
+        firstLine = fitWithEllipsis(
+            m_smallTextDrawer,
+            firstLine.empty() ? name : firstLine,
+            textWidth
+        );
+        secondLine = fitWithEllipsis(
+            m_smallTextDrawer,
+            secondLine,
+            textWidth
+        );
+
+        if (secondLine.empty()) {
+            m_smallTextDrawer->drawTextCenteredInBox(
+                firstLine,
+                x + 3,
+                y + imageHeight,
+                textWidth,
+                labelHeight,
+                labelColor
+            );
         }
         else {
-            iDrawY += 50;
-            iDrawX=getDrawX();
-            rowNr = 0;
+            const int firstLineY = y + imageHeight + 2;
+            m_smallTextDrawer->drawTextCentered(
+                firstLine,
+                x + 3,
+                textWidth,
+                firstLineY,
+                labelColor
+            );
+            m_smallTextDrawer->drawTextCentered(
+                secondLine,
+                x + 3,
+                textWidth,
+                firstLineY + m_smallTextDrawer->getFontHeight(),
+                labelColor
+            );
         }
     }
 
-    return nullptr;
+    if (item->getBuildCost() > 0) {
+        const std::string price = std::format("${}", item->getBuildCost());
+        const int priceWidth = m_smallTextDrawer->getTextLength(price);
+        const int priceX = x + 6;
+        renderDrawer->renderRectFillColor(
+            priceX - 3,
+            y + 3,
+            priceWidth + 4,
+            17,
+            8,
+            10,
+            12,
+            220
+        );
+        renderDrawer->renderRectColor(
+            priceX - 3,
+            y + 3,
+            priceWidth + 4,
+            17,
+            Color{126, 94, 35, 255}
+        );
+        m_smallTextDrawer->drawText(
+            priceX,
+            y + 4,
+            priceColor,
+            price,
+            false
+        );
+    }
 }
 
 void cBuildingListDrawer::setPlayer(cPlayer *player)
@@ -397,9 +720,147 @@ void cBuildingListDrawer::setPlayer(cPlayer *player)
     this->m_player = player;
 }
 
-void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &)
+HudLayout cBuildingListDrawer::getLayout(cBuildingList *list) const
 {
-    // NOOP
+    const bool reserveOrderArea =
+        list != nullptr &&
+        list->getType() == eListType::LIST_STARPORT;
+    return HudLayout::create(
+        game.m_screenW,
+        game.m_screenH,
+        reserveOrderArea
+    );
+}
+
+int cBuildingListDrawer::getScrollRow(cBuildingList *list) const
+{
+    if (list == nullptr) {
+        return 0;
+    }
+    const int listId = eListTypeAsInt(list->getType());
+    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
+        return 0;
+    }
+    return std::clamp(
+        m_scrollRows[listId],
+        0,
+        getLayout(list).maxScrollRow(list->getItemCount())
+    );
+}
+
+void cBuildingListDrawer::setScrollRow(cBuildingList *list, int row)
+{
+    if (list == nullptr) {
+        return;
+    }
+    const int listId = eListTypeAsInt(list->getType());
+    if (listId < 0 || listId >= static_cast<int>(m_scrollRows.size())) {
+        return;
+    }
+    m_scrollRows[listId] = std::clamp(
+        row,
+        0,
+        getLayout(list).maxScrollRow(list->getItemCount())
+    );
+}
+
+void cBuildingListDrawer::scrollSelectedList(int rowDelta)
+{
+    if (m_player == nullptr || m_player->getSideBar() == nullptr) {
+        return;
+    }
+    cSideBar *sidebar = m_player->getSideBar();
+    const int selectedId = sidebar->getSelectedListID();
+    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
+        return;
+    }
+    cBuildingList *list = sidebar->getList(selectedId);
+    setScrollRow(list, getScrollRow(list) + rowDelta);
+}
+
+void cBuildingListDrawer::drawHdScrollbar(
+    cBuildingList *list,
+    const HudLayout &layout)
+{
+    const Color track{10, 13, 15, 245};
+    const Color border{83, 69, 43, 255};
+    const Color thumb{181, 135, 44, 255};
+    renderDrawer->renderRectFillColor(
+        layout.scrollbar.getX(),
+        layout.scrollbar.getY(),
+        layout.scrollbar.getWidth(),
+        layout.scrollbar.getHeight(),
+        track
+    );
+    renderDrawer->renderRectColor(
+        layout.scrollbar.getX(),
+        layout.scrollbar.getY(),
+        layout.scrollbar.getWidth(),
+        layout.scrollbar.getHeight(),
+        border
+    );
+
+    if (layout.maxScrollRow(list->getItemCount()) <= 0) {
+        return;
+    }
+    const cRectangle thumbRect = layout.scrollbarThumb(
+        list->getItemCount(),
+        getScrollRow(list)
+    );
+    renderDrawer->renderRectFillColor(
+        thumbRect.getX() + 2,
+        thumbRect.getY() + 2,
+        thumbRect.getWidth() - 4,
+        thumbRect.getHeight() - 4,
+        thumb
+    );
+}
+
+void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
+{
+    if (m_player == nullptr ||
+        m_player->getSideBar() == nullptr) {
+        return;
+    }
+
+    cSideBar *sidebar = m_player->getSideBar();
+    const int selectedId = sidebar->getSelectedListID();
+    if (selectedId < 0 || selectedId >= cSideBar::LIST_MAX) {
+        return;
+    }
+    cBuildingList *list = sidebar->getList(selectedId);
+    if (list == nullptr) {
+        return;
+    }
+
+    const HudLayout layout = getLayout(list);
+    if (!layout.catalog.isPointWithin(event.coords.x, event.coords.y)) {
+        return;
+    }
+
+    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_UP) {
+        scrollSelectedList(-1);
+        return;
+    }
+    if (event.eventType == eMouseEventType::MOUSE_SCROLLED_DOWN) {
+        scrollSelectedList(1);
+        return;
+    }
+    if (event.eventType != eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED ||
+        !layout.scrollbar.isPointWithin(event.coords.x, event.coords.y)) {
+        return;
+    }
+
+    const cRectangle thumb = layout.scrollbarThumb(
+        list->getItemCount(),
+        getScrollRow(list)
+    );
+    if (event.coords.y < thumb.getY()) {
+        scrollSelectedList(-layout.visibleRows());
+    }
+    else if (event.coords.y > thumb.getEndY()) {
+        scrollSelectedList(layout.visibleRows());
+    }
 }
 
 void cBuildingListDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
````

## src/drawers/cBuildingListDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cBuildingListDrawer.cpp
```

stdout (22221 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.cpp b/src/drawers/cBuildingListDrawer.cpp
index eb979610..529e15c5 100644
--- a/src/drawers/cBuildingListDrawer.cpp
+++ b/src/drawers/cBuildingListDrawer.cpp
@@ -1,23 +1,63 @@
-#include "cBuildingListDrawer.h"
+/**
+ * @file cBuildingListDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cBuildingListDrawer.h"
+#include "include/sGameServices.h"
 #include "drawers/SDLDrawer.hpp"
-#include "d2tmc.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/structures/cOrderProcesser.h"
+#include "gameobjects/players/cPlayer.h"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "controls/cMouse.h"
+#include "utils/common.h"
+#include "utils/Log.h"
 
-#include <SDL2/SDL.h>
+#include <SDL3/SDL.h>
 #include <format>
 
+#include "gameobjects/structures/cStructureFactory.h"
+#include "gameobjects/units/cUnits.h"
+#include "include/cAssert.h"
+#include "include/Texture.hpp"
+#include "context/TextContext.hpp"
+#include "drawers/cTextDrawer.h"
+#include "game/cGameSettings.h"
+#include "gameobjects/structures/cStructureInfo.h"
+
 cBuildingListDrawer::cBuildingListDrawer(const GameContext *ctx, cPlayer *player) :
     m_gameTextDrawer(ctx->getTextContext()->getGameTextDrawer()),
     m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer()),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_player(player),
     m_renderListIds(false)
 {
+    d2tm_assert(player != nullptr);
+    d2tm_assert(ctx != nullptr);
+}
+
+void cBuildingListDrawer::serviceInit(sGameServices* services)
+{
+    m_infos = services->info;
+    m_settings = services->settings;
+    m_mouse = services->mouse;
+    m_objects = services->objects;
 }
 
 void cBuildingListDrawer::drawList(cBuildingList *list, int listIDToDraw)
@@ -42,24 +82,24 @@ void cBuildingListDrawer::drawListWithUnitsOrAbilities(cBuildingList *list)
 
 void cBuildingListDrawer::drawButtonHoverRectangle(cBuildingList *list)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
 
     int x = list->getButtonDrawX();
     int y = list->getButtonDrawY();
     int id = list->getButtonIconIdUnpressed();
 
     int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int height = m_gfxinter->getTexture(id)->h;
 
     Color color = m_player->getSelectFadingColor();
 
-    renderDrawer->renderRectColor(x, y, width, height, color);
-    renderDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
+    m_sdlDrawer->renderRectColor(x, y, width, height, color);
+    m_sdlDrawer->renderRectColor(x + 1, y + 1, width-2, height-2, color);
 }
 
 void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
 
     int x = list->getButtonDrawX();
     int y = list->getButtonDrawY();
@@ -71,22 +111,22 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
     if (id < 0) {
         // this is not good
-        logbook("ERROR UNABLE TO DRAW LIST BECAUSE ID IS NOT VALID!?");
+        Logger::error(COMP_GAME, "cBuildingListDrawer::drawButton","unable to draw list because id is not valid!? id={}", id);
         return;
     }
 
 //	int width = (gfxinter->getSurface(id))->w;
     int width = 33;
-    int height = (m_gfxinter->getSurface(id))->h;
+    int height = m_gfxinter->getTexture(id)->h;
 
     // clear
-    renderDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(list->getButtonIconIdUnpressed()), x, y);		// draw pressed button version (unpressed == default in gui)
 
     // set blender
-    renderDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(id), x, y,128);
 
     if (!list->isAvailable()) {
-        renderDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
+        m_sdlDrawer->renderRectFillColor(x, y, width, height, 0,0,0,96);
     }
 
     if (pressed) {
@@ -94,16 +134,16 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
         Color color = m_player->getHouseFadingColor();
 
-        renderDrawer->renderRectColor(x, y, width, height, color);
-        renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
+        m_sdlDrawer->renderRectColor(x, y, width, height, color);
+        m_sdlDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
     }
     else {
         if (list->isFlashing()) {
             Color color = list->getFlashingColor();
 
-            renderDrawer->renderRectColor(x, y, width, height, color);
-            renderDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
-            renderDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
+            m_sdlDrawer->renderRectColor(x, y, width, height, color);
+            m_sdlDrawer->renderRectColor(x + 1, y + 1, width - 2, height - 2, color);
+            m_sdlDrawer->renderRectColor(x + 2, y + 2, width - 3, height - 3, color);
         }
     }
 }
@@ -111,7 +151,7 @@ void cBuildingListDrawer::drawButton(cBuildingList *list, bool pressed)
 
 int cBuildingListDrawer::getDrawX()
 {
-    return (game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar) + 2;
+    return (m_settings->getScreenW() - cSideBar::SidebarWidthWithoutCandyBar) + 2;
 }
 
 int cBuildingListDrawer::getDrawY()
@@ -121,18 +161,16 @@ int cBuildingListDrawer::getDrawY()
 
 /**
  * Draw the list, start from startId, until the max icons in the list to be drawn.
- *
- * @param startId
  */
-void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructureSize)
+void cBuildingListDrawer::drawList(cBuildingList *list, const bool shouldDrawStructureSize)
 {
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
 
-    Color selectFadingColor = m_player->getSelectFadingColor();
+    const Color selectFadingColor = m_player->getSelectFadingColor();
 
-    int end = MAX_ITEMS;
+    constexpr int end = MAX_ITEMS;
 
     // is building an item in the list?
     std::array<int, 6> isBuildingItemInList = list->isBuildingItem();
@@ -141,6 +179,9 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     int withOfIcon = 63;
     int heightOfIcon = 47;
 
+    bool structureLimitReached = list->isType(eListType::LIST_CONSTYARD) && m_objects->getStructureFactory()->isStructureLimitReached();
+    bool unitLimitReached = (list->isType(eListType::LIST_FOOT_UNITS) || list->isType(eListType::LIST_UNITS)) && m_objects->getUnits()->isUnitLimitReached();
+
     // draw the icons, in rows of 3
     int rowNr = 0;
     for (int i = 0; i < end; i++) {
@@ -153,13 +194,12 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         int iDrawXEnd = iDrawX + withOfIcon;
         int iDrawYEnd = iDrawY + heightOfIcon;
 
-        // asumes drawing for human player
         bool cannotPayIt = !m_player->hasEnoughCreditsFor(item->getBuildCost());
 
         // icon id must be set , assert it.
-        assert(item->getIconId() > -1);
+        d2tm_assert(item->getIconId() > -1);
 
-        renderDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(item->getIconId()), iDrawX, iDrawY);
 
         if (shouldDrawStructureSize) {
             drawStructureSize(item->getBuildId(), iDrawX, iDrawY);
@@ -171,8 +211,12 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 
             if (!item->isDoneBuilding() || iFrame < 31) {
                 // draw the other progress stuff
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+                m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSFIX), iDrawX+2, iDrawY+2,128);
+                m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESS001+iFrame), iDrawX+2, iDrawY+2,128);
+
+                if (item->isPaused()) {
+                    m_smallTextDrawer->drawTextCenteredInBox("Paused", iDrawX, iDrawY, withOfIcon, heightOfIcon, Color::Yellow);
+                }
             }
             else {
                 if (item->shouldPlaceIt()) {
@@ -181,7 +225,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     if (m_player->isContextMouseState(eMouseState::MOUSESTATE_PLACE)) {
                         icon = READY02;
                     }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
                 }
                 else if (item->shouldDeployIt()) {
                     // TODO: draw white/red (flicker)
@@ -190,9 +234,14 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                     if (m_player->isContextMouseState(eMouseState::MOUSESTATE_DEPLOY)) {
                         icon = READY02;
                     }
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(icon), iDrawX + 3, iDrawY + 16);
                 }
             }
+
+            // units being built (or queued) while no unit slot is left: they can only wait
+            if (unitLimitReached && item->isTypeUnit()) {
+                drawMaxBuilt(iDrawX, iDrawY, withOfIcon, heightOfIcon);
+            }
         }
         else {   // not building
             // this item is not being built. So we do not draw a progress indicator.
@@ -212,51 +261,59 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
                 }
             }
 
-            if (!item->isAvailable() || isBuildingSameSubListItem) {
-                renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+            bool cannotBuildDueStructureLimit = structureLimitReached && !cStructureFactory::isModifyingTerrain(item->getBuildId());
+            bool cannotBuildDueUnitLimit = unitLimitReached && item->isTypeUnit();
+            bool cannotBuildDueLimit = cannotBuildDueStructureLimit || cannotBuildDueUnitLimit;
 
-                // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
-                if (item->isPendingUpgrading()) {
-                    Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+            if (!item->isAvailable() || isBuildingSameSubListItem || cannotBuildDueLimit) {
 
-                    Color red = Color{255, 0, 0,255};
-                    m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, red);
-                }
+                if (!cannotBuildDueLimit) {
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                    // Pending upgrading (ie: an upgrade is progressing, blocking the construction of these items)
+                    if (item->isPendingUpgrading()) {
+                        Color errorFadingColor = m_player->getErrorFadingColor();
+                        m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
 
-                // Pending building (ie: a build is progressing, blocking the upgrade)
-                if (item->isPendingBuilding()) {
-                    Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
-
-                    Color red = Color{255, 0, 0, 255};
-                    int height = heightOfIcon / 3;
-                    m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, red);
-                    m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, red);
+                        m_smallTextDrawer->drawTextCenteredInBox("Upgrading", iDrawX, iDrawY, withOfIcon, heightOfIcon, Color::Red);
+                    }
+
+                    // Pending building (ie: a build is progressing, blocking the upgrade)
+                    if (item->isPendingBuilding()) {
+                        Color errorFadingColor = m_player->getErrorFadingColor();
+                        m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                        m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+
+                        int height = heightOfIcon / 3;
+                        m_smallTextDrawer->drawTextCenteredInBox("Building", iDrawX, iDrawY, withOfIcon, height, Color::Red);
+                        m_smallTextDrawer->drawTextCenteredInBox("in", iDrawX, iDrawY + height, withOfIcon, height, Color::Red);
+                        m_smallTextDrawer->drawTextCenteredInBox("progress", iDrawX, iDrawY + (height * 2), withOfIcon, height, Color::Red);
+                    }
+                } else {
+                    drawMaxBuilt(iDrawX, iDrawY, withOfIcon, heightOfIcon);
                 }
             }
 
             if (list->getType() == eListType::LIST_STARPORT) {
                 // only for starport show you can't pay it, as we allow building units when you cannot pay it (ie partial
                 // payment/progress)
-                if (cannotPayIt) {
-                    renderDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
+                cOrderProcesser *orderProcesser = m_player->getOrderProcesser();
+                bool orderIsAwaitingFrigate = orderProcesser->isOrderPlaced() || orderProcesser->isFrigateSent();
+                if (cannotPayIt || orderIsAwaitingFrigate) {
+                    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), iDrawX, iDrawY,64);
                     Color errorFadingColor = m_player->getErrorFadingColor();
-                    renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
-                    renderDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
+                    m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, errorFadingColor);
+                    m_sdlDrawer->renderLine( iDrawX, iDrawY, iDrawXEnd, iDrawYEnd, errorFadingColor);
+                    m_sdlDrawer->renderLine( iDrawX, iDrawY + heightOfIcon, iDrawX + withOfIcon, iDrawY, errorFadingColor);
                 }
             }
 
             // last built id
             if (list->getLastClickedId() == i) {
-                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
-                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
+                m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
+                m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
             }
         }
 
@@ -284,7 +341,7 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
             m_gameTextDrawer->drawText(textX, textY, std::format("{}",amountToShow));
         }
 
-        if (game.isDebugMode()) {
+        if (m_settings->isDebugMode()) {
             if (m_renderListIds) {
                 int textX = iDrawX + 41;
                 int textY = iDrawY + 40;
@@ -294,16 +351,15 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
         }
 
         // draw rectangle when mouse hovers over icon
-        auto m_mouse = game.getMouse();
         if (isOverItemCoordinates_Boolean(m_mouse->getX(), m_mouse->getY(), iDrawX, iDrawY)) {
-            renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
-            renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
+            m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), selectFadingColor);
+            m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, selectFadingColor);
         }
         else {
             Color color = list->getFlashingColor();
             if (item->isFlashing()) {
-                renderDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
-                renderDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
+                m_sdlDrawer->renderRectColor((iDrawX + 1), (iDrawY + 1), (iDrawXEnd - 1)-(iDrawX + 1), (iDrawYEnd - 1)-(iDrawY + 1), color);
+                m_sdlDrawer->renderRectColor(iDrawX, iDrawY, iDrawXEnd-iDrawX, iDrawYEnd-iDrawY, color);
             }
         }
 
@@ -320,6 +376,22 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
     }
 }
 
+/**
+ * Draws the red cross with "Max built" over an icon, when its item can not be built because a limit is reached.
+ */
+void cBuildingListDrawer::drawMaxBuilt(int x, int y, int width, int height)
+{
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(PROGRESSNA), x, y, 64);
+    Color errorFadingColor = m_player->getErrorFadingColor();
+    m_sdlDrawer->renderRectColor(x, y, width, height, errorFadingColor);
+    m_sdlDrawer->renderLine(x, y, x + width, y + height, errorFadingColor);
+    m_sdlDrawer->renderLine(x, y + height, x + width, y, errorFadingColor);
+
+    int halfHeight = height / 2;
+    m_smallTextDrawer->drawTextCenteredInBox("Max", x, y, width, halfHeight, Color::Red);
+    m_smallTextDrawer->drawTextCenteredInBox("built", x, y + halfHeight, width, halfHeight, Color::Red);
+}
+
 /**
  * Draw the amount of squares a structure would take. The X and Y coordinates are the top
  * left coordinates of an icon.
@@ -331,8 +403,8 @@ void cBuildingListDrawer::drawList(cBuildingList *list, bool shouldDrawStructure
 void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
 {
     // figure out size
-    int iW= sStructureInfo[structureId].bmp_width / 32;
-    int iH= sStructureInfo[structureId].bmp_height / 32;
+    int iW= m_infos->getStructureInfo(structureId).bmp_width / 32;
+    int iH= m_infos->getStructureInfo(structureId).bmp_height / 32;
     int iTile = GRID_1X1;
 
     if (iW == 2 && iH == 2) {
@@ -347,9 +419,9 @@ void cBuildingListDrawer::drawStructureSize(int structureId, int x, int y)
         iTile = GRID_3X3;
     }
 
-    renderDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
-    renderDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
+    m_sdlDrawer->renderRectFillColor(x + 43, y + 20,19,19,0,0,0,192);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(GRID_0X0), x + 43, y + 20);
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(iTile), x + 43, y + 20);
 }
 
 bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY)
@@ -362,7 +434,7 @@ bool cBuildingListDrawer::isOverItemCoordinates_Boolean(int x, int y, int drawX,
 
 cBuildingListItem *cBuildingListDrawer::isOverItemCoordinates(cBuildingList *list, int x, int y)
 {
-    assert(list != nullptr);
+    d2tm_assert(list != nullptr);
     // starting draw coordinates
     int iDrawX=getDrawX();
     int iDrawY=getDrawY();
@@ -404,7 +476,7 @@ void cBuildingListDrawer::onNotifyMouseEvent(const s_MouseEvent &)
 
 void cBuildingListDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 {
-    switch (event.eventType) {
+    switch (event.getType()) {
         case eKeyEventType::HOLD:
             onKeyHold(event);
             break;
````

## src/drawers/cBuildingListDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cBuildingListDrawer.h
```

stdout (1636 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.h b/src/drawers/cBuildingListDrawer.h
index 7a5a52cd..b4f9928d 100644
--- a/src/drawers/cBuildingListDrawer.h
+++ b/src/drawers/cBuildingListDrawer.h
@@ -3,12 +3,17 @@
 #include "cTextDrawer.h"
 #include "observers/cInputObserver.h"
 #include "sidebar/cBuildingList.h"
+#include "sidebar/HudLayout.hpp"
+
+#include <array>
+#include <string>
 
 class cPlayer;
 class GameContext;
 class Graphics;
 
 class cBuildingListDrawer : cInputObserver {
+    friend class UiAuditAccess;
 
 public:
     explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);
@@ -38,6 +43,8 @@ private:
     cPlayer *m_player;
 
     bool m_renderListIds;
+    std::array<int, cSideBar::LIST_MAX> m_scrollRows{};
+    std::string m_readyLabel;
 
     void drawStructureSize(int structureId, int x, int y);
     void drawList(cBuildingList *list, bool shouldDrawStructureSize);
@@ -45,6 +52,14 @@ private:
     void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport
 
     bool isOverItemCoordinates_Boolean(int x, int y, int drawX, int drawY);
+    [[nodiscard]] int getCardWidth() const;
+    [[nodiscard]] int getCardHeight() const;
+    void drawHdCard(cBuildingListItem *item, int x, int y);
+    void drawHdScrollbar(cBuildingList *list, const HudLayout &layout);
+    [[nodiscard]] HudLayout getLayout(cBuildingList *list = nullptr) const;
+    [[nodiscard]] int getScrollRow(cBuildingList *list) const;
+    void setScrollRow(cBuildingList *list, int row);
+    void scrollSelectedList(int rowDelta);
 
     void onKeyHold(const cKeyboardEvent &event);
 
````

## src/drawers/cBuildingListDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cBuildingListDrawer.h
```

stdout (2216 байт):

````text
diff --git a/src/drawers/cBuildingListDrawer.h b/src/drawers/cBuildingListDrawer.h
index 7a5a52cd..f4458f61 100644
--- a/src/drawers/cBuildingListDrawer.h
+++ b/src/drawers/cBuildingListDrawer.h
@@ -1,18 +1,41 @@
+/**
+ * @file cBuildingListDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
-#include "cTextDrawer.h"
+class cTextDrawer;
+class cGameObjectContext;
 #include "observers/cInputObserver.h"
 #include "sidebar/cBuildingList.h"
 
 class cPlayer;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+class cInfoContext;
+class cGameSettings;
+class cMouse;
+struct sGameServices;
 
 class cBuildingListDrawer : cInputObserver {
 
 public:
     explicit cBuildingListDrawer(const GameContext *ctx, cPlayer *player);
 
+    void serviceInit(sGameServices* services);
+
     void onNotifyMouseEvent(const s_MouseEvent &event) override;
     void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
 
@@ -31,15 +54,21 @@ protected:
 
 private:
     // the list to draw
-    cTextDrawer* m_gameTextDrawer;
-    cTextDrawer* m_smallTextDrawer;
-    Graphics* m_gfxinter;
+    cTextDrawer* m_gameTextDrawer = nullptr;
+    cTextDrawer* m_smallTextDrawer = nullptr;
+    Graphics* m_gfxinter = nullptr;
+    SDLDrawer* m_sdlDrawer = nullptr;
 
     cPlayer *m_player;
+    cInfoContext* m_infos = nullptr;
+    cGameSettings* m_settings = nullptr;
+    cMouse* m_mouse = nullptr;
+    cGameObjectContext *m_objects = nullptr;
 
     bool m_renderListIds;
 
     void drawStructureSize(int structureId, int x, int y);
+    void drawMaxBuilt(int x, int y, int width, int height);
     void drawList(cBuildingList *list, bool shouldDrawStructureSize);
     void drawListWithStructures(cBuildingList *list);		// used for const yard
     void drawListWithUnitsOrAbilities(cBuildingList *list); // used for units or palace / starport
````

## src/drawers/cMessageDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMessageDrawer.cpp
```

stdout (5393 байт):

````text
diff --git a/src/drawers/cMessageDrawer.cpp b/src/drawers/cMessageDrawer.cpp
index da9d02fe..feb84567 100644
--- a/src/drawers/cMessageDrawer.cpp
+++ b/src/drawers/cMessageDrawer.cpp
@@ -3,11 +3,14 @@
 #include "d2tmc.h"
 #include "drawers/SDLDrawer.hpp"
 #include "sidebar/cSideBar.h"
+#include "sidebar/HudLayout.hpp"
+#include "sidebar/MusicControlsLayout.hpp"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 
 #include <SDL2/SDL.h>
+#include <algorithm>
 
 // Game Playing State and SelectYourNextConquestState have their own version
 // this class has to be abstracted in such a way so it is used in both those states, yet without the wonky init
@@ -36,11 +39,87 @@ cMessageDrawer::~cMessageDrawer()
 void cMessageDrawer::draw()
 {
     if (m_state == messages::eMessageDrawerState::COMBAT) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y);
+        const HudLayout layout = HudLayout::create(
+            game.m_screenW,
+            game.m_screenH
+        );
+        const int left = 143;
+        const int right = layout.battlefield.getEndX() - 8;
+        const int reservedMessageWidth = m_message.empty()
+            ? 0
+            : m_textDrawer->getTextLength(m_message) + 16;
+        const MusicControlsLayout music = MusicControlsLayout::create(
+            left,
+            right,
+            reservedMessageWidth
+        );
+        const int messageX = music.visible
+            ? music.panel.getEndX() + 8
+            : left;
+        const cRectangle messageRect(
+            messageX,
+            4,
+            std::max(0, right - messageX),
+            33
+        );
+        renderDrawer->renderRectFillColor(
+            messageRect.getX(),
+            messageRect.getY(),
+            messageRect.getWidth(),
+            messageRect.getHeight(),
+            Color{20, 24, 26, 255}
+        );
+        renderDrawer->renderRectColor(
+            messageRect.getX(),
+            messageRect.getY(),
+            messageRect.getWidth(),
+            messageRect.getHeight(),
+            Color{112, 87, 42, 255}
+        );
+        const int messageTextWidth = m_message.empty()
+            ? 0
+            : m_textDrawer->getTextLength(m_message);
+        const int messageContentWidth = messageRect.getWidth() - 16;
+        if (m_alpha > -1 && messageTextWidth > 0 && messageContentWidth > 0) {
+            const Color messageColor{232, 225, 196, Uint8(m_alpha)};
+            if (messageTextWidth <= messageContentWidth) {
+                m_textDrawer->drawText(
+                    messageRect.getX() + 8,
+                    messageRect.getY() + 10,
+                    messageColor,
+                    m_message,
+                    false
+                );
+            } else {
+                const float scale = static_cast<float>(messageContentWidth) /
+                    static_cast<float>(messageTextWidth);
+                if (scale >= 0.5F) {
+                    m_textDrawer->drawTextScaledOpticallyCenteredInBox(
+                        m_message,
+                        cRectangle(
+                            messageRect.getX() + 8,
+                            messageRect.getY(),
+                            messageContentWidth,
+                            messageRect.getHeight()
+                        ),
+                        scale,
+                        messageColor,
+                        false
+                    );
+                }
+            }
+        }
+        return;
     }
 
     if (m_alpha > -1) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha);
+        renderDrawer->renderFromSurface(
+            m_bmpBar,
+            m_position.x,
+            m_position.y,
+            m_alpha,
+            m_gfxinter->getDensity()
+        );
         // draw message
         m_textDrawer->drawText(m_position.x+13, m_position.y+6, Color{0, 0, 0,Uint8(m_alpha)}, m_message, false);
     }
@@ -154,19 +233,34 @@ void cMessageDrawer::createMessageBarBmp(int desiredWidth)
         SDL_FreeSurface(m_bmpBar);
     }
 
-    m_bmpBar = SDL_CreateRGBSurface(0,desiredWidth, 30,32,0,0,0,255);
+    const int density = m_gfxinter->getDensity();
+    m_bmpBar = SDL_CreateRGBSurfaceWithFormat(
+        0,
+        desiredWidth * density,
+        30 * density,
+        32,
+        SDL_PIXELFORMAT_RGBA8888
+    );
     auto color = SDL_MapRGBA(m_bmpBar->format,255,0,255,255);
     SDL_FillRect(m_bmpBar, nullptr, color);
     SDL_BlitSurface(m_gfxinter->getSurface(MESSAGE_LEFT), nullptr, m_bmpBar, nullptr);
 
-    for (int drawX = 11; drawX < m_bmpBar->w; drawX+= 55) {
+    for (
+        int drawX = 11 * density;
+        drawX < m_bmpBar->w;
+        drawX += 55 * density) {
         auto src = m_gfxinter->getSurface(MESSAGE_MIDDLE);
         auto tmp = cRectangle{drawX, 0,src->w,src->h};
         SDL_Rect destRect = tmp.toSDL();
         SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
     }
     auto src = m_gfxinter->getSurface(MESSAGE_RIGHT);
-    auto tmp = cRectangle{m_bmpBar->w - 11, 0,src->w,src->h};
+    auto tmp = cRectangle{
+        m_bmpBar->w - 11 * density,
+        0,
+        src->w,
+        src->h
+    };
     SDL_Rect destRect = tmp.toSDL();
     SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
 }
````

## src/drawers/cMessageDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMessageDrawer.cpp
```

stdout (4906 байт):

````text
diff --git a/src/drawers/cMessageDrawer.cpp b/src/drawers/cMessageDrawer.cpp
index da9d02fe..a69f8d9d 100644
--- a/src/drawers/cMessageDrawer.cpp
+++ b/src/drawers/cMessageDrawer.cpp
@@ -1,27 +1,49 @@
+/**
+ * @file cMessageDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #include "cMessageDrawer.h"
 #include "data/gfxinter.h"
-#include "d2tmc.h"
 #include "drawers/SDLDrawer.hpp"
 #include "sidebar/cSideBar.h"
 #include "utils/Graphics.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "game/cGameSettings.h"
+#include "include/sGameServices.h"
 
-#include <SDL2/SDL.h>
+#include <SDL3/SDL.h>
+#include "include/cAssert.h"
+#include "context/TextContext.hpp"
 
 // Game Playing State and SelectYourNextConquestState have their own version
 // this class has to be abstracted in such a way so it is used in both those states, yet without the wonky init
 // functions
 
-cMessageDrawer::cMessageDrawer(GameContext* ctx) :
+cMessageDrawer::cMessageDrawer(GameContext* ctx, sGameServices* services) :
     m_TIMER_message(0),
     m_alpha(0),
     m_state(messages::eMessageDrawerState::COMBAT),
     m_fadeState(messages::eMessageDrawerFadingState::FADE_IN),
     m_textDrawer(ctx->getTextContext()->getGameTextDrawer()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_ctx(ctx),
-    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get())
+    m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_services(services)
 {
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(services != nullptr);
     m_bmpBar = nullptr;
     m_keepMessage = false;
     m_timeMessageIsVisible = 10;
@@ -36,11 +58,11 @@ cMessageDrawer::~cMessageDrawer()
 void cMessageDrawer::draw()
 {
     if (m_state == messages::eMessageDrawerState::COMBAT) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y);
+        m_sdlDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, 255, m_gfxinter->getDensity());
     }
 
     if (m_alpha > -1) {
-        renderDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha);
+        m_sdlDrawer->renderFromSurface(m_bmpBar, m_position.x, m_position.y, m_alpha, m_gfxinter->getDensity());
         // draw message
         m_textDrawer->drawText(m_position.x+13, m_position.y+6, Color{0, 0, 0,Uint8(m_alpha)}, m_message, false);
     }
@@ -94,7 +116,7 @@ void cMessageDrawer::destroy()
     m_alpha = -1;
     m_TIMER_message = 0;
     if (m_bmpBar != nullptr) {
-        SDL_FreeSurface(m_bmpBar);
+        SDL_DestroySurface(m_bmpBar);
     }
 }
 
@@ -126,7 +148,7 @@ void cMessageDrawer::initCombatPosition()
 
     int margin = 4;
     int widthOfOptionsButton = 160 + margin;
-    int desiredWidth = game.m_screenW - (cSideBar::SidebarWidth + widthOfOptionsButton);
+    int desiredWidth = m_services->settings->getScreenW() - (cSideBar::SidebarWidth + widthOfOptionsButton);
     createMessageBarBmp(desiredWidth);
     // default positions in-game (battle mode)
     m_position.x = widthOfOptionsButton;
@@ -150,23 +172,24 @@ void cMessageDrawer::setMessage(const std::string &msg, bool keepMessage)
 
 void cMessageDrawer::createMessageBarBmp(int desiredWidth)
 {
+    const int density = m_gfxinter->getDensity();
     if (m_bmpBar) {
-        SDL_FreeSurface(m_bmpBar);
+        SDL_DestroySurface(m_bmpBar);
     }
 
-    m_bmpBar = SDL_CreateRGBSurface(0,desiredWidth, 30,32,0,0,0,255);
-    auto color = SDL_MapRGBA(m_bmpBar->format,255,0,255,255);
-    SDL_FillRect(m_bmpBar, nullptr, color);
+    m_bmpBar = SDL_CreateSurface(desiredWidth * density, 30 * density, SDL_PIXELFORMAT_RGBA32);
+    auto color = SDL_MapRGBA(SDL_GetPixelFormatDetails(m_bmpBar->format), SDL_GetSurfacePalette(m_bmpBar), 255, 0, 255, 255);
+    SDL_FillSurfaceRect(m_bmpBar, nullptr, color);
     SDL_BlitSurface(m_gfxinter->getSurface(MESSAGE_LEFT), nullptr, m_bmpBar, nullptr);
 
-    for (int drawX = 11; drawX < m_bmpBar->w; drawX+= 55) {
+    for (int drawX = 11 * density; drawX < m_bmpBar->w; drawX += 55 * density) {
         auto src = m_gfxinter->getSurface(MESSAGE_MIDDLE);
         auto tmp = cRectangle{drawX, 0,src->w,src->h};
         SDL_Rect destRect = tmp.toSDL();
         SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
     }
     auto src = m_gfxinter->getSurface(MESSAGE_RIGHT);
-    auto tmp = cRectangle{m_bmpBar->w - 11, 0,src->w,src->h};
+    auto tmp = cRectangle{m_bmpBar->w - 11 * density, 0,src->w,src->h};
     SDL_Rect destRect = tmp.toSDL();
     SDL_BlitSurface(src, nullptr, m_bmpBar, &destRect);
 }
````

## src/drawers/cMessageDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMessageDrawer.h
```

stdout (436 байт):

````text
diff --git a/src/drawers/cMessageDrawer.h b/src/drawers/cMessageDrawer.h
index fb9584c1..1bfc420a 100644
--- a/src/drawers/cMessageDrawer.h
+++ b/src/drawers/cMessageDrawer.h
@@ -39,7 +39,7 @@ public:
     void initCombatPosition();
 
     void setMessage(const std::string &msg, bool keepMessage = false);
-    std::string getMessage() {
+    std::string getMessage() const {
         return m_message;
     }
     bool hasMessage() {
````

## src/drawers/cMessageDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMessageDrawer.h
```

stdout (1543 байт):

````text
diff --git a/src/drawers/cMessageDrawer.h b/src/drawers/cMessageDrawer.h
index fb9584c1..89edd6bb 100644
--- a/src/drawers/cMessageDrawer.h
+++ b/src/drawers/cMessageDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file cMessageDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
 #include "utils/cPoint.h"
@@ -7,6 +22,8 @@
 struct SDL_Surface;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+struct sGameServices;
 
 namespace messages {
 enum eMessageDrawerState {
@@ -22,9 +39,11 @@ enum eMessageDrawerFadingState {
 
 class cMessageDrawer {
 public:
-    explicit cMessageDrawer(GameContext* ctx);
+    explicit cMessageDrawer(GameContext* ctx, sGameServices* services);
     ~cMessageDrawer();
 
+    void serviceInit(sGameServices*) {}
+
     void draw();
 
     void thinkFast(); // timer based thinking to fade in/out message
@@ -61,8 +80,10 @@ private:
     messages::eMessageDrawerState m_state;
     messages::eMessageDrawerFadingState m_fadeState;
     cTextDrawer* m_textDrawer=nullptr;
+    SDLDrawer* m_sdlDrawer=nullptr;
     GameContext* m_ctx;
     Graphics* m_gfxinter;
+    sGameServices* m_services;
 
     void createMessageBarBmp(int desiredWidth);
 };
````

## src/drawers/cMiniMapDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMiniMapDrawer.cpp
```

stdout (4764 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.cpp b/src/drawers/cMiniMapDrawer.cpp
index 9ca08ea4..58fbb91a 100644
--- a/src/drawers/cMiniMapDrawer.cpp
+++ b/src/drawers/cMiniMapDrawer.cpp
@@ -2,6 +2,7 @@
 
 #include "drawers/SDLDrawer.hpp"
 #include "d2tmc.h"
+#include "debug/UiAudit.hpp"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
 #include "player/cPlayer.h"
@@ -10,6 +11,7 @@
 #include "utils/Graphics.hpp"
 #include <SDL2/SDL.h>
 #include "map/MapGeometry.hpp"
+#include "sidebar/HudLayout.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
 #include <cassert>
@@ -24,32 +26,37 @@ cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMa
     m_mapCamera(mapCamera),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_status(eMinimapStatus::NOTAVAILABLE),
-    m_iStaticFrame(STAT14),
-    m_iTrans(0)
+    m_iStaticFrame(STAT14)
 {
     assert(map);
     assert(player);
     assert(mapCamera);
 
-    int reportX = cSideBar::WidthOfMinimap / getMapWidthInPixels();
-    int reportY = cSideBar::HeightOfMinimap / getMapHeightInPixels();
-    factorZoom = std::min(reportX, reportY);
+    const HudLayout hud = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const cRectangle minimapArea = hud.radarViewport;
 
-    int halfWidthOfMinimap = cSideBar::WidthOfMinimap / 2;
+    int reportX = minimapArea.getWidth() / getMapWidthInPixels();
+    int reportY = minimapArea.getHeight() / getMapHeightInPixels();
+    factorZoom = std::max(1, std::min(reportX, reportY));
+
+    int halfWidthOfMinimap = minimapArea.getWidth() / 2;
     int halfWidthOfMap = getMapWidthInPixels() / 2;
-    int topLeftX = game.m_screenW - cSideBar::WidthOfMinimap;
+    int topLeftX = minimapArea.getX();
     drawX = topLeftX + (halfWidthOfMinimap - factorZoom*halfWidthOfMap);
 
-    int halfHeightOfMinimap = cSideBar::HeightOfMinimap / 2;
+    int halfHeightOfMinimap = minimapArea.getHeight() / 2;
     int halfHeightOfMap = getMapHeightInPixels() / 2;
-    int topLeftY = cSideBar::TopBarHeight;
+    int topLeftY = minimapArea.getY();
     drawY = topLeftY + (halfHeightOfMinimap - factorZoom*halfHeightOfMap);
 
     centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
     centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
 
     m_RectMinimap = cRectangle(drawX, drawY, factorZoom*getMapWidthInPixels(), factorZoom * getMapHeightInPixels());
-    m_RectFullMinimap = cRectangle(topLeftX, topLeftY, cSideBar::WidthOfMinimap, cSideBar::HeightOfMinimap);
+    m_RectFullMinimap = minimapArea;
     mipMapTex = renderDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
 }
 
@@ -63,6 +70,9 @@ cMiniMapDrawer::~cMiniMapDrawer()
 
 void cMiniMapDrawer::draw()
 {
+    if (uiaudit::isEnabled() && m_player->hasAtleastOneStructure(RADAR)) {
+        uiaudit::recordClick("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
+    }
     if (!m_map) {
         return;
     }
@@ -71,6 +81,9 @@ void cMiniMapDrawer::draw()
         return;
     }
 
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("minimap", m_RectFullMinimap.getX(), m_RectFullMinimap.getY(), m_RectFullMinimap.getWidth(), m_RectFullMinimap.getHeight());
+    }
     renderDrawer->renderRectFillColor(m_RectFullMinimap, Color::black());
 
     if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
@@ -84,40 +97,13 @@ void cMiniMapDrawer::draw()
     }
     renderDrawer->renderStrechFullSprite(mipMapTex, m_RectMinimap);
 
-    drawStaticFrame();
     drawViewPortRectangle();
 }
 
-void cMiniMapDrawer::drawStaticFrame()
-{
-    if (m_status == eMinimapStatus::NOTAVAILABLE) return;
-    if (m_status == eMinimapStatus::RENDERMAP) return;
-    if (m_status == eMinimapStatus::LOWPOWER) return;
-
-    if (m_status == eMinimapStatus::POWERDOWN) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
-        return;
-    }
-
-    // Draw static info
-    // < STAT01 frames are going from very transparent to opaque
-    if (m_iStaticFrame < STAT10) {
-        m_iTrans = 255 - healthBar(192, (STAT12 - m_iStaticFrame), 12);
-    } else {
-        m_iTrans = 255;
-    }
-
-    // non-stat01 frames are drawn transparent
-    if (m_iStaticFrame != STAT01) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
-    }
-}
-
 void cMiniMapDrawer::init()
 {
     m_status = eMinimapStatus::NOTAVAILABLE;
     m_iStaticFrame = STAT14;
-    m_iTrans = 0;
     m_isMouseOver = false;
 }
 
````

## src/drawers/cMiniMapDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMiniMapDrawer.cpp
```

stdout (20791 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.cpp b/src/drawers/cMiniMapDrawer.cpp
index 9ca08ea4..62d94b32 100644
--- a/src/drawers/cMiniMapDrawer.cpp
+++ b/src/drawers/cMiniMapDrawer.cpp
@@ -1,56 +1,92 @@
-#include "cMiniMapDrawer.h"
+/**
+ * @file cMiniMapDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
+#include "cMiniMapDrawer.h"
+#include "include/sGameServices.h"
 #include "drawers/SDLDrawer.hpp"
-#include "d2tmc.h"
+#include "gameobjects/structures/cStructures.h"
+#include "gameobjects/units/cUnits.h"
+#include "gameobjects/map/cMapCamera.h"
+#include "game/cGameSettings.h"
+#include "controls/cMouse.h"
+#include "context/AudioContext.hpp"
 #include "data/gfxdata.h"
 #include "data/gfxinter.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
+#include "gameobjects/players/cPlayers.h"
 #include "sidebar/cSideBar.h"
 #include "utils/cSoundPlayer.h"
 #include "utils/Graphics.hpp"
-#include <SDL2/SDL.h>
-#include "map/MapGeometry.hpp"
+#include <SDL3/SDL.h>
+#include "gameobjects/map/MapGeometry.hpp"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
-#include <cassert>
-#include <iostream>
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "gameobjects/map/cMap.h"
+#include "include/cAssert.h"
+#include <algorithm>
+#include <cmath>
+//#include <iostream>
 
 #include "data/gfxaudio.h"
+#include "gameobjects/particles/cParticle.h"
+#include "utils/RNG.hpp"
 
-cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMapCamera *mapCamera) :
+cMiniMapDrawer::cMiniMapDrawer(GameContext *ctx, cGameSettings *settings, cMap *map, cPlayer *player, cMapCamera *mapCamera) :
     m_isMouseOver(false),
     m_map(map),
+    m_mapGeometry(map ? map->getGeometry() : nullptr),
     m_player(player),
     m_mapCamera(mapCamera),
+    m_ctx(ctx),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
     m_status(eMinimapStatus::NOTAVAILABLE),
     m_iStaticFrame(STAT14),
     m_iTrans(0)
 {
-    assert(map);
-    assert(player);
-    assert(mapCamera);
+    d2tm_assert(map!=nullptr);
+    d2tm_assert(m_mapGeometry != nullptr);
+    d2tm_assert(player!=nullptr);
+    d2tm_assert(mapCamera!=nullptr);
+    d2tm_assert(settings!=nullptr);
 
-    int reportX = cSideBar::WidthOfMinimap / getMapWidthInPixels();
-    int reportY = cSideBar::HeightOfMinimap / getMapHeightInPixels();
-    factorZoom = std::min(reportX, reportY);
+    float reportX = cSideBar::WidthOfMinimap*1.f / getMapWidthInPixels();
+    float reportY = cSideBar::HeightOfMinimap*1.f / getMapHeightInPixels();
+    m_factorZoom = std::min(reportX, reportY);
+    //std::cout << "Minimap zoom factor: " << m_factorZoom << std::endl;
 
     int halfWidthOfMinimap = cSideBar::WidthOfMinimap / 2;
     int halfWidthOfMap = getMapWidthInPixels() / 2;
-    int topLeftX = game.m_screenW - cSideBar::WidthOfMinimap;
-    drawX = topLeftX + (halfWidthOfMinimap - factorZoom*halfWidthOfMap);
+    int topLeftX = settings->getScreenW() - cSideBar::WidthOfMinimap;
+    m_drawX = topLeftX + (halfWidthOfMinimap - m_factorZoom*halfWidthOfMap);
 
     int halfHeightOfMinimap = cSideBar::HeightOfMinimap / 2;
     int halfHeightOfMap = getMapHeightInPixels() / 2;
     int topLeftY = cSideBar::TopBarHeight;
-    drawY = topLeftY + (halfHeightOfMinimap - factorZoom*halfHeightOfMap);
+    m_drawY = topLeftY + (halfHeightOfMinimap - m_factorZoom*halfHeightOfMap);
 
-    centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
-    centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
+    m_centerX = topLeftX + (halfWidthOfMinimap - halfWidthOfMap);
+    m_centerY = topLeftY + (halfHeightOfMinimap - halfHeightOfMap);
 
-    m_RectMinimap = cRectangle(drawX, drawY, factorZoom*getMapWidthInPixels(), factorZoom * getMapHeightInPixels());
+    m_RectMinimap = cRectangle(m_drawX, m_drawY, m_factorZoom*getMapWidthInPixels(), m_factorZoom * getMapHeightInPixels());
     m_RectFullMinimap = cRectangle(topLeftX, topLeftY, cSideBar::WidthOfMinimap, cSideBar::HeightOfMinimap);
-    mipMapTex = renderDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
+    //std::cout << "Minimap top left corner: (" << m_RectMinimap.getX() << ", " << m_RectMinimap.getY() << ", " << m_RectMinimap.getWidth() << ", " << m_RectMinimap.getHeight() << ")" << std::endl;
+    //std::cout << "RectFullMinimap: (" << m_RectFullMinimap.getX() << ", " << m_RectFullMinimap.getY() << ", " << m_RectFullMinimap.getWidth() << ", " << m_RectFullMinimap.getHeight() << ")" << std::endl;
+    m_mipMapTex = m_sdlDrawer->createRenderTargetTexture(getMapWidthInPixels(), getMapHeightInPixels());
 }
 
 cMiniMapDrawer::~cMiniMapDrawer()
@@ -61,6 +97,14 @@ cMiniMapDrawer::~cMiniMapDrawer()
     m_status = eMinimapStatus::NOTAVAILABLE;
 }
 
+void cMiniMapDrawer::serviceInit(sGameServices* services)
+{
+    m_objects = services->objects;
+    m_infos = services->info;
+    m_mouse = services->mouse;
+    m_audioContext = services->ctx->getAudioContext();
+}
+
 void cMiniMapDrawer::draw()
 {
     if (!m_map) {
@@ -71,7 +115,7 @@ void cMiniMapDrawer::draw()
         return;
     }
 
-    renderDrawer->renderRectFillColor(m_RectFullMinimap, Color::black());
+    m_sdlDrawer->renderRectFillColor(m_RectFullMinimap, Color::Black);
 
     if (m_status == eMinimapStatus::POWERUP || m_status == eMinimapStatus::RENDERMAP || m_status == eMinimapStatus::POWERDOWN) {
         drawTerrain();
@@ -82,7 +126,7 @@ void cMiniMapDrawer::draw()
         cleanDrawTerrain();
         drawUnitsAndStructures(true);
     }
-    renderDrawer->renderStrechFullSprite(mipMapTex, m_RectMinimap);
+    m_sdlDrawer->renderStrechFullSprite(m_mipMapTex, m_RectMinimap);
 
     drawStaticFrame();
     drawViewPortRectangle();
@@ -95,7 +139,7 @@ void cMiniMapDrawer::drawStaticFrame()
     if (m_status == eMinimapStatus::LOWPOWER) return;
 
     if (m_status == eMinimapStatus::POWERDOWN) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
+        m_sdlDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap);
         return;
     }
 
@@ -109,7 +153,7 @@ void cMiniMapDrawer::drawStaticFrame()
 
     // non-stat01 frames are drawn transparent
     if (m_iStaticFrame != STAT01) {
-        renderDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
+        m_sdlDrawer->renderStrechFullSprite(m_gfxinter->getTexture(m_iStaticFrame), m_RectFullMinimap,m_iTrans);
     }
 }
 
@@ -126,7 +170,10 @@ void cMiniMapDrawer::think()
 {
     if (m_player->hasAtleastOneStructure(RADAR)) {
         if (m_status == eMinimapStatus::NOTAVAILABLE) {
-            m_status = eMinimapStatus::POWERUP;
+            // Route through POWERDOWN instead of jumping straight to POWERUP, so the
+            // power check below (which plays SOUND_RADAR) always gets a chance to run,
+            // even when power is already sufficient the instant the radar completes.
+            m_status = eMinimapStatus::POWERDOWN;
         }
     }
     else {
@@ -143,7 +190,7 @@ void cMiniMapDrawer::think()
             // go to state power down (not enough power)
             m_status = eMinimapStatus::POWERDOWN;
             // "Radar de-activated""
-            game.playVoice(SOUND_VOICE_04_ATR, m_player->getId());
+            m_audioContext->playVoice(SOUND_VOICE_04_ATR, m_player->getHouse());
         }
     }
 
@@ -152,9 +199,9 @@ void cMiniMapDrawer::think()
         if (hasRadarAndEnoughPower) {
             // go to state power up (enough power)
             m_status = eMinimapStatus::POWERUP;
-            game.playSound(SOUND_RADAR);
+            m_audioContext->playSound(SOUND_RADAR);
             // "Radar activated"
-            game.playVoice(SOUND_VOICE_03_ATR, m_player->getId());
+            m_audioContext->playVoice(SOUND_VOICE_03_ATR, m_player->getHouse());
         }
     }
 
@@ -196,27 +243,31 @@ void cMiniMapDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
             onMouseAt(event);
             return;
         case eMouseEventType::MOUSE_LEFT_BUTTON_CLICKED:
-            onMousePressedLeft(event); // click has same behavior as 'press'
-            return;
+            onMouseClickedLeft(event);
+            break;
         case eMouseEventType::MOUSE_LEFT_BUTTON_PRESSED:
             onMousePressedLeft(event);
-            return;
+            break;
+        case eMouseEventType::MOUSE_RIGHT_BUTTON_PRESSED:
+            onMousePressedRight(event);
+            break;
         default:
             return;
     }
 
+    updateMouseCursor();
 }
 
 void cMiniMapDrawer::drawTerrain()
 {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
     Color iColor = Color{0, 0, 0,255};
 
-    for (int x = 0; x < (m_map->getWidth()); x++) {
-        for (int y = 0; y < (m_map->getHeight()); y++) {
+    for (int x = 0; x < m_mapGeometry->getWidth(); x++) {
+        for (int y = 0; y < m_mapGeometry->getHeight(); y++) {
             iColor = Color{0, 0, 0,255};
             //@mira where is map ?
-            int iCll = m_map->getGeometry().makeCell(x, y);
+            int iCll = m_mapGeometry->makeCell(x, y);
 
             if (m_map->isVisible(iCll, m_player->getId())) {
                 iColor = getRGBColorForTerrainType(m_map->getCellType(iCll));
@@ -224,14 +275,14 @@ void cMiniMapDrawer::drawTerrain()
 
             // TODO: make flexible map borders
             // do not show the helper border
-            if (!m_map->isWithinBoundaries(x, y)) {
+            if (!m_mapGeometry->isWithinBoundaries(x, y)) {
                 iColor = Color{0, 0, 0,255};
             }
 
-            renderDrawer->renderDot(x, y, iColor, 1);
+            m_sdlDrawer->renderDot(x, y, iColor, 1);
         }
     }
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 void cMiniMapDrawer::drawViewPortRectangle()
@@ -242,13 +293,16 @@ void cMiniMapDrawer::drawViewPortRectangle()
     iWidth--;
     iHeight--;
 
-    int pixelSize = factorZoom;
+    const float pixelSize = std::max(m_factorZoom, 0.001f);
+
+    const float startXf = m_drawX + ((m_mapCamera->getViewportStartX() / TILESIZE_WIDTH_PIXELS) * pixelSize);
+    const float startYf = m_drawY + ((m_mapCamera->getViewportStartY() / TILESIZE_HEIGHT_PIXELS) * pixelSize);
 
-    int startX = drawX + ((m_mapCamera->getViewportStartX() / TILESIZE_WIDTH_PIXELS) * pixelSize);
-    int startY = drawY + ((m_mapCamera->getViewportStartY() / TILESIZE_HEIGHT_PIXELS) * pixelSize);
+    int startX = static_cast<int>(std::floor(startXf));
+    int startY = static_cast<int>(std::floor(startYf));
 
-    int minimapWidth = iWidth * (pixelSize) + 1;
-    int minimapHeight = iHeight * (pixelSize) + 1;
+    int minimapWidth = std::max(1, static_cast<int>(std::ceil(iWidth * pixelSize + 1.0f)));
+    int minimapHeight = std::max(1, static_cast<int>(std::ceil(iHeight * pixelSize + 1.0f)));
 
     //cap the rectangle to the minimap size
     if (startX < m_RectFullMinimap.getX()) {
@@ -265,7 +319,7 @@ void cMiniMapDrawer::drawViewPortRectangle()
     if (startY + minimapHeight > m_RectFullMinimap.getEndY()) {
         minimapHeight = m_RectFullMinimap.getEndY() - startY;
     }
-    renderDrawer->renderRectColor(startX, startY, minimapWidth, minimapHeight, Color{255, 255, 255,255});
+    m_sdlDrawer->renderRectColor(startX, startY, minimapWidth, minimapHeight, Color{255, 255, 255,255});
 }
 
 /**
@@ -274,14 +328,14 @@ void cMiniMapDrawer::drawViewPortRectangle()
  * @param playerOnly (if false, draws all other players than player)
  */
 void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
-    const Color black = Color::black();
-    for (int x = 0; x < m_map->getWidth(); x++) {
-        for (int y = 0; y < m_map->getHeight(); y++) {
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
+    const Color black = Color::Black;
+    for (int x = 0; x < m_mapGeometry->getWidth(); x++) {
+        for (int y = 0; y < m_mapGeometry->getHeight(); y++) {
             // do not show the helper border
-            if (!m_map->isWithinBoundaries(x, y)) continue;
+            if (!m_mapGeometry->isWithinBoundaries(x, y)) continue;
 
-            int iCll = m_map->getGeometry().makeCell(x, y);
+            int iCll = m_mapGeometry->makeCell(x, y);
 
             if (!m_map->isVisible(iCll, m_player->getId())) {
                 // invisible cell
@@ -293,29 +347,33 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
 
             int idOfStructureAtCell = m_map->getCellIdStructuresLayer(iCll);
             if (idOfStructureAtCell > -1) {
-                int iPlr = structure[idOfStructureAtCell]->getOwner();
+                int iPlr = m_objects->getStructures()[idOfStructureAtCell]->getOwner();
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfUnitAtCell = m_map->getCellIdUnitLayer(iCll);
             if (idOfUnitAtCell > -1) {
-                int iPlr = unit[idOfUnitAtCell].iPlayer;
+                cUnit *pUnit = m_objects->getUnit(idOfUnitAtCell);
+                if (m_map->isHiddenByFogOfWar(pUnit)) continue; // hidden in the fog of war
+                int iPlr = pUnit->iPlayer;
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfAirUnitAtCell = m_map->getCellIdAirUnitLayer(iCll);
             if (idOfAirUnitAtCell > -1) {
-                int iPlr = unit[idOfAirUnitAtCell].iPlayer;
+                cUnit *pUnit = m_objects->getUnit(idOfAirUnitAtCell);
+                if (m_map->isHiddenByFogOfWar(pUnit)) continue; // hidden in the fog of war
+                int iPlr = pUnit->iPlayer;
                 if (playerOnly) {
                     if (iPlr != m_player->getId()) continue; // skip non player units
                 }
-                iColor = players[iPlr].getMinimapColor();
+                iColor = m_objects->getPlayer(iPlr)->getMinimapColor();
             }
 
             int idOfWormAtCell = m_map->getCellIdWormsLayer(iCll);
@@ -323,6 +381,7 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
                 if (playerOnly) {
                     continue; // skip sandworms
                 }
+                if (m_map->isHiddenByFogOfWar(m_objects->getUnit(idOfWormAtCell))) continue;
                 iColor = m_player->getSelectFadingColor();
             }
 
@@ -330,10 +389,10 @@ void cMiniMapDrawer::drawUnitsAndStructures(bool playerOnly) const {
             if (iColor.r == black.r && iColor.g == black.g && iColor.b == black.b) {
                 continue;
             }
-            renderDrawer->renderDot(x, y, iColor, 1);
+            m_sdlDrawer->renderDot(x, y, iColor, 1);
         }
     }
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 Color cMiniMapDrawer::getRGBColorForTerrainType(int terrainType)
@@ -366,45 +425,98 @@ Color cMiniMapDrawer::getRGBColorForTerrainType(int terrainType)
 }
 
 int cMiniMapDrawer::getMapHeightInPixels() const {
-    return m_map->getHeight();
+    return m_mapGeometry->getHeight();
 }
 
 int cMiniMapDrawer::getMapWidthInPixels() const {
-    return m_map->getWidth();
+    return m_mapGeometry->getWidth();
 }
 
 void cMiniMapDrawer::onMouseAt(const s_MouseEvent &event)
 {
     m_isMouseOver = m_RectMinimap.isPointWithin(event.coords.x, event.coords.y);
+    updateMouseCursor();
 }
 
-void cMiniMapDrawer::onMousePressedLeft(const s_MouseEvent &event)
+void cMiniMapDrawer::updateMouseCursor()
 {
+    if (m_isMouseOver &&
+        m_status != NOTAVAILABLE) {
+        if (m_player->hasAnyUnitSelected()) {
+            m_mouse->setTile(MOUSE_MOVE);
+        } else {
+            m_mouse->setTile(MOUSE_NORMAL);
+        }
+    }
+}
+
+void cMiniMapDrawer::onMouseClickedLeft(const s_MouseEvent &event) {
     if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
-        !game.getMouse()->isBoxSelecting() // pressed the mouse and not boxing anything..
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
     ) {
+        // left mouse *click* will move any units if selected
+        if (m_player->hasAnyUnitSelected()) {
+            int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
+            cUnits *units = m_objects->getUnits();
+            units->move_to(mouseCellOnMinimap);
+
+            auto absPoint = m_map->getGeometry()->getAbsolutePositionFromCell(mouseCellOnMinimap);
+            cParticle::create(absPoint.x, absPoint.y, D2TM_PARTICLE_MOVE, -1, -1, m_objects, m_infos);
+
+            sSelectedUnitTypes selectedUnitTypes = m_player->getSelectedUnitTypes();
+            if (selectedUnitTypes.hasInfantry) {
+                m_audioContext->playSound(SOUND_MOVINGOUT + RNG::rnd(2));
+            }
+            if (selectedUnitTypes.hasVehicles) {
+                m_audioContext->playSound(SOUND_ACKNOWLEDGED + RNG::rnd(3));
+            }
+        }
+    }
+}
 
-        if (m_player->hasAtleastOneStructure(RADAR)) {
-            auto m_mouse = game.getMouse();
+void cMiniMapDrawer::onMousePressedLeft(const s_MouseEvent &event)
+{
+    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
+    ) {
+        // left-mouse button press only moves viewport if no units are selected
+        if (!m_player->hasAnyUnitSelected()) {
             int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
             m_mapCamera->centerAndJumpViewPortToCell(mouseCellOnMinimap);
         }
     }
 }
 
+void cMiniMapDrawer::onMousePressedRight(const s_MouseEvent &event)
+{
+    if (m_RectFullMinimap.isPointWithin(event.coords.x, event.coords.y) && // on minimap space
+        !m_mouse->isBoxSelecting() && // pressed the mouse and not boxing anything..
+        this->m_status != NOTAVAILABLE // only allow action when not drawing logo
+    ) {
+        // right-mouse button press will always move viewport
+        int mouseCellOnMinimap = getMouseCell(m_mouse->getX(), m_mouse->getY());
+        m_mapCamera->centerAndJumpViewPortToCell(mouseCellOnMinimap);
+    }
+}
+
 void cMiniMapDrawer::cleanDrawTerrain() const {
-    renderDrawer->beginDrawingToTexture(mipMapTex);
-    renderDrawer->renderClearToColor(Color::black());
-    renderDrawer->endDrawingToTexture();
+    m_sdlDrawer->beginDrawingToTexture(m_mipMapTex);
+    m_sdlDrawer->renderClearToColor(Color::Black);
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 int cMiniMapDrawer::getMouseCell(int mouseX, int mouseY)
 {
-    int mouseMiniMapX = mouseX - drawX;
-    int mouseMiniMapY = mouseY - drawY;
-    mouseMiniMapX /= factorZoom;
-    mouseMiniMapY /= factorZoom;
-    auto mouseMiniMapPoint = m_map->fixCoordinatesToBeWithinPlayableMap(mouseMiniMapX, mouseMiniMapY);
+    const float safeZoom = std::max(m_factorZoom, 0.001f);
+    const float mouseMiniMapXf = (mouseX - m_drawX) / safeZoom;
+    const float mouseMiniMapYf = (mouseY - m_drawY) / safeZoom;
+
+    int mouseMiniMapX = static_cast<int>(std::floor(mouseMiniMapXf));
+    int mouseMiniMapY = static_cast<int>(std::floor(mouseMiniMapYf));
+
+    auto mouseMiniMapPoint = m_mapGeometry->fixCoordinatesToBeWithinPlayableMap(mouseMiniMapX, mouseMiniMapY);
 
-    return m_map->getGeometry().getCellWithMapBorders(mouseMiniMapPoint.x, mouseMiniMapPoint.y);
+    return m_mapGeometry->getCellWithMapBorders(mouseMiniMapPoint.x, mouseMiniMapPoint.y);
 }
````

## src/drawers/cMiniMapDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cMiniMapDrawer.h
```

stdout (544 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.h b/src/drawers/cMiniMapDrawer.h
index 858c9515..ceaaec57 100644
--- a/src/drawers/cMiniMapDrawer.h
+++ b/src/drawers/cMiniMapDrawer.h
@@ -34,8 +34,6 @@ public:
 
     void draw();
 
-    void drawStaticFrame();
-
     // in-between solution until we have a proper combat state object
     void init();
 
@@ -78,7 +76,6 @@ private:
     eMinimapStatus m_status;
 
     int m_iStaticFrame;
-    int m_iTrans;							// transparancy
 
     // the top left coordinates for the minimap
     int drawX, drawY;
````

## src/drawers/cMiniMapDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cMiniMapDrawer.h
```

stdout (3708 байт):

````text
diff --git a/src/drawers/cMiniMapDrawer.h b/src/drawers/cMiniMapDrawer.h
index 858c9515..f4cb3ca7 100644
--- a/src/drawers/cMiniMapDrawer.h
+++ b/src/drawers/cMiniMapDrawer.h
@@ -1,3 +1,18 @@
+/**
+ * @file cMiniMapDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 /*
  * cMiniMapDrawer.h
  *
@@ -7,15 +22,27 @@
 
 #pragma once
 
-#include "map/cMap.h"
-#include "map/cMapCamera.h"
+// #include "gameobjects/map/cMap.h"
+// #include "gameobjects/map/cMapCamera.h"
 #include "utils/cRectangle.h"
 #include "utils/Color.hpp"
+#include "controls/sMouseEvent.h"
 
+
+class cMap;
+class MapGeometry;
+class cMapCamera;
 class cPlayer;
 class Texture;
 class GameContext;
+class cGameSettings;
 class Graphics;
+class SDLDrawer;
+class cGameObjectContext;
+class cInfoContext;
+class cMouse;
+class AudioContext;
+struct sGameServices;
 
 // the BuildingListItemState
 enum eMinimapStatus {
@@ -28,7 +55,7 @@ enum eMinimapStatus {
 
 class cMiniMapDrawer {
 public:
-    explicit cMiniMapDrawer(GameContext *ctx, cMap *map, cPlayer *player, cMapCamera *mapCamera);
+    explicit cMiniMapDrawer(GameContext *ctx, cGameSettings *settings, cMap *map, cPlayer *player, cMapCamera *mapCamera);
     cMiniMapDrawer() = delete;
     ~cMiniMapDrawer();
 
@@ -47,6 +74,8 @@ public:
 
     void onNotifyMouseEvent(const s_MouseEvent &event);
 
+    void serviceInit(sGameServices* services);
+
 protected:
 
     void drawTerrain();
@@ -61,19 +90,29 @@ protected:
 private:
     void onMouseAt(const s_MouseEvent &event);
     void onMousePressedLeft(const s_MouseEvent &event);
+    void onMousePressedRight(const s_MouseEvent &event);
+    void onMouseClickedLeft(const s_MouseEvent &event);
+    void updateMouseCursor();
     void cleanDrawTerrain() const;
     int getMouseCell(int mouseX, int mouseY);
 
     bool m_isMouseOver;
 
     //@mira : where is map ? Where is this initialisation ?
-    cMap *m_map;	// the minimap drawer reads data from here
-    cPlayer *m_player;	// the player used as 'context' (ie, for drawing the rectangle / viewport on the minimap)
-    cMapCamera *m_mapCamera;
+    cMap *m_map = nullptr;	// the minimap drawer reads data from here
+    MapGeometry *m_mapGeometry = nullptr;
+    cPlayer *m_player = nullptr;	// the player used as 'context' (ie, for drawing the rectangle / viewport on the minimap)
+    cMapCamera *m_mapCamera = nullptr;
+    GameContext* m_ctx = nullptr;
+    cGameObjectContext* m_objects = nullptr;
+    cInfoContext* m_infos = nullptr;
+    cMouse* m_mouse = nullptr;
+    AudioContext* m_audioContext = nullptr;
     cRectangle m_RectMinimap; // the minimap (map) itself
     cRectangle m_RectFullMinimap; // the total space it could take
-    Texture *mipMapTex;
+    Texture *m_mipMapTex;
     Graphics *m_gfxinter;
+    SDLDrawer *m_sdlDrawer;
 
     eMinimapStatus m_status;
 
@@ -81,9 +120,9 @@ private:
     int m_iTrans;							// transparancy
 
     // the top left coordinates for the minimap
-    int drawX, drawY;
-    int centerX, centerY; // the center of the minimap
+    int m_drawX, m_drawY;
+    int m_centerX, m_centerY; // the center of the minimap
 
     // bool isBigMap;
-    int factorZoom = 1; // factor to zoom the minimap, based on the map size and the minimap size
+    float m_factorZoom = 1.f; // factor to zoom the minimap, based on the map size and the minimap size
 };
````

## src/drawers/cSideBarDrawer.cpp: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cSideBarDrawer.cpp
```

stdout (27651 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.cpp b/src/drawers/cSideBarDrawer.cpp
index 009617be..22c7fa1a 100644
--- a/src/drawers/cSideBarDrawer.cpp
+++ b/src/drawers/cSideBarDrawer.cpp
@@ -1,50 +1,56 @@
 #include "cSideBarDrawer.h"
 
 #include "d2tmc.h"
+#include "debug/UiAudit.hpp"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
 #include "drawers/cOrderDrawer.h"
 #include "managers/cDrawManager.h"
 #include "player/cPlayer.h"
 #include "utils/Graphics.hpp"
+#include "utils/Localization.hpp"
 #include <SDL2/SDL.h>
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/TextContext.hpp"
+#include "sidebar/HudLayout.hpp"
+#include "utils/HdUiTextureLoader.hpp"
 #include <algorithm>
+#include <format>
 
 cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :
     m_player(player),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
     m_buildingListDrawer(ctx, player),
     m_sidebar(nullptr),
-    m_sidebarColor(Color{214, 149, 20,255})
+    m_smallTextDrawer(ctx->getTextContext()->getSmallTextDrawer())
 {
     assert(player);
 
-    candyBarBall = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex);
-    candyBarPiece = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex);
-    candyHorizonBar = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex);
-
-    candiBarRenderer = renderDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, game.m_screenH-40);
-    renderDrawer->beginDrawingToTexture(candiBarRenderer);
-    createCandyBar();
-    renderDrawer->endDrawingToTexture();
+    const int density = game.getGraphicsDensity();
+    m_houseCrests[0] = loadHdUiTexture(
+        "hud_house_atreides.png",
+        density,
+        "HD HUD Atreides crest"
+    );
+    m_houseCrests[1] = loadHdUiTexture(
+        "hud_house_harkonnen.png",
+        density,
+        "HD HUD Harkonnen crest"
+    );
+    m_houseCrests[2] = loadHdUiTexture(
+        "hud_house_ordos.png",
+        density,
+        "HD HUD Ordos crest"
+    );
 }
 
 cSideBarDrawer::~cSideBarDrawer()
 {
-    if (candyBarBall)
-        delete candyBarBall;
-    if (candyBarPiece)
-        delete candyBarPiece;
-    if (candyHorizonBar)
-        delete candyHorizonBar;
-
-    if (candiBarRenderer)
-        delete candiBarRenderer;
+    for (Texture *&crest : m_houseCrests) {
+        delete crest;
+        crest = nullptr;
+    }
 }
 
 void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
@@ -60,340 +66,345 @@ void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 // draws the sidebar on screen
 void cSideBarDrawer::draw()
 {
-    // black out sidebar
-    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, game.m_screenH, Color{0, 0, 0,255});
-
-    drawCandybar();
-
-    drawMinimap();
-    drawCapacities();
-    drawBuildingLists();
+    if (uiaudit::isEnabled()) {
+        UiAuditAccess::recordSidebarClicks(*this);
+    }
+    drawHdSidebar();
 }
 
-void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
+void cSideBarDrawer::drawHdSidebar()
 {
-    m_player = pPlayer;
-    m_buildingListDrawer.setPlayer(pPlayer);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("sidebar", layout.sidebar.getX(), cSideBar::TopBarHeight, layout.sidebar.getWidth(), layout.sidebar.getHeight() - cSideBar::TopBarHeight);
+    }
+    renderDrawer->renderRectFillColor(
+        layout.sidebar.getX(),
+        layout.sidebar.getY(),
+        layout.sidebar.getWidth(),
+        layout.sidebar.getHeight(),
+        Color{12, 15, 17, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        layout.sidebar.getX(),
+        cSideBar::TopBarHeight,
+        5,
+        game.m_screenH - cSideBar::TopBarHeight,
+        Color{32, 36, 38, 255}
+    );
+    renderDrawer->renderLine(
+        layout.sidebar.getX() + 5,
+        cSideBar::TopBarHeight,
+        layout.sidebar.getX() + 5,
+        game.m_screenH,
+        Color{166, 124, 44, 255}
+    );
+
+    drawHdRadarPanel();
+    drawHdCapacities();
+    drawHdBuildingLists();
 }
 
-void cSideBarDrawer::drawBuildingLists()
+Texture *cSideBarDrawer::getHouseCrest() const
 {
-    // draw the sidebar itself (the backgrounds, borders, etc)
-
-    // !??! sidebar is not set earlier...but can be re-set, so keep doing this :(
-    // This basically means the allocation goes wrong somewhere! :(
-    m_sidebar = m_player->getSideBar();
-
-    // draw the buildlist icons
-    int selectedListId = m_sidebar->getSelectedListID();
-
-    int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
-    for (int listId = startPos; listId < cSideBar::LIST_MAX; listId++) {
-        cBuildingList *list = m_sidebar->getList(listId);
-        bool isListIdSelectedList = (selectedListId == listId);
-        m_buildingListDrawer.drawButton(list, isListIdSelectedList);
+    if (m_player->isHouse(ATREIDES)) {
+        return m_houseCrests[0];
     }
-
-    // draw background of buildlist
-    Texture *backgroundSprite = m_gfxinter->getTexture(BMP_GERALD_ICONLIST_BACKGROUND);
-
-    int drawX = game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar + 1;
-
-    int startY = cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight +
-                 cSideBar::HeightOfListButton;
-
-    for (; drawX < game.m_screenW; drawX += backgroundSprite->w) {
-        for (int drawY=startY; drawY < game.m_screenH; drawY += backgroundSprite->h) {
-            renderDrawer->renderSprite(backgroundSprite, drawX, drawY);
-        }
-    }
-
-    // draw the 'lines' between the icons    // draw the buildlist itself (take scrolling into account)
-    cBuildingList *selectedList = nullptr;
-
-    int iDrawX = m_buildingListDrawer.getDrawX();
-    int iDrawY = m_buildingListDrawer.getDrawY();
-
-    Texture *horBar = m_gfxinter->getTexture(BMP_GERALD_SIDEBAR_PIECE);
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
-
-    if (selectedListId > -1) {
-        selectedList = m_sidebar->getList(selectedListId);
+    if (m_player->isHouse(HARKONNEN)) {
+        return m_houseCrests[1];
     }
-
-    int endY = game.m_screenH;
-    int rows = 6;
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        rows = 5;
-        endY = game.m_screenH - 50;
+    if (m_player->isHouse(ORDOS)) {
+        return m_houseCrests[2];
     }
+    return nullptr;
+}
 
-    for (int i = 1; i < 3; i++) {
-        int barX = (iDrawX - 1) + (i * 66);
-        Color darker = Color{89, 56, 0,255};
-        Color veryDark = Color{48, 28, 0,255};
-        renderDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
-        renderDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
-
-        // horizontal lines
-        for (int j = 1; j < rows; j++) {
-            int barY = iDrawY - 1 + (j * 50);
-            renderDrawer->renderLine( iDrawX, barY-1, game.m_screenW, barY - 1, darker);
-            renderDrawer->renderLine( iDrawX, barY, game.m_screenW, barY, veryDark);
-        }
+std::string cSideBarDrawer::getHouseDisplayName() const
+{
+    if (m_player->isHouse(ATREIDES)) {
+        return localization::text("HOUSE ATREIDES", "ДОМ АТРЕЙДЕС");
     }
-
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        renderDrawer->renderRectFillColor(iDrawX, endY, game.m_screenW-iDrawX, game.m_screenH-endY, m_sidebarColor);
-        renderDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
+    if (m_player->isHouse(HARKONNEN)) {
+        return localization::text("HOUSE HARKONNEN", "ДОМ ХАРКОННЕН");
     }
-
-    // vertical lines at the side
-    renderDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, game.m_screenH, Color{255, 211, 125,255}); // left
-    renderDrawer->renderLine( game.m_screenW - 1, iDrawY - 38, game.m_screenW - 1, endY, Color{209, 150, 28,255}); // right
-
-    // END drawing icons grid
-
-    if (selectedList) {
-        m_buildingListDrawer.drawList(selectedList, selectedListId);
+    if (m_player->isHouse(ORDOS)) {
+        return localization::text("HOUSE ORDOS", "ДОМ ОРДОС");
     }
+    return localization::text("UNKNOWN HOUSE", "НЕИЗВЕСТНЫЙ ДОМ");
+}
 
-    // button interaction
-    for (int i = startPos; i < cSideBar::LIST_MAX; i++) {
-        if (i == selectedListId) continue; // skip selected list for button interaction
-        cBuildingList *list = m_sidebar->getList(i);
-
-        if (list->isAvailable() == false) continue; // not available, so no interaction possible
-
-        // render hover over border
-        auto m_mouse = game.getMouse();
-        if (list->isOverButton(m_mouse->getX(), m_mouse->getX())) {
-            m_buildingListDrawer.drawButtonHoverRectangle(list);
-        }
+void cSideBarDrawer::drawHdRadarPanel()
+{
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const Color panel{16, 20, 22, 255};
+    const Color panelInner{7, 10, 11, 255};
+    const Color brass{151, 113, 43, 255};
+    const Color text{235, 225, 191, 255};
+    const Color accent = m_player->getSelectFadingColor();
+
+    renderDrawer->renderRectFillColor(
+        layout.radarPanel.getX(),
+        layout.radarPanel.getY(),
+        layout.radarPanel.getWidth(),
+        layout.radarPanel.getHeight(),
+        panel
+    );
+    renderDrawer->renderRectColor(
+        layout.radarPanel.getX(),
+        layout.radarPanel.getY(),
+        layout.radarPanel.getWidth(),
+        layout.radarPanel.getHeight(),
+        brass
+    );
+    renderDrawer->renderRectFillColor(
+        layout.houseHeader.getX(),
+        layout.houseHeader.getY(),
+        layout.houseHeader.getWidth(),
+        layout.houseHeader.getHeight(),
+        Color{25, 29, 30, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        layout.houseHeader.getX(),
+        layout.houseHeader.getEndY() - 2,
+        layout.houseHeader.getWidth(),
+        2,
+        accent
+    );
+
+    Texture *crest = getHouseCrest();
+    const int headerCrestSize = 24;
+    if (crest != nullptr) {
+        renderDrawer->renderStrechFullSprite(
+            crest,
+            cRectangle(
+                layout.houseHeader.getX() + 3,
+                layout.houseHeader.getY() + 2,
+                headerCrestSize,
+                headerCrestSize
+            )
+        );
     }
-
-    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();
-
-    // allow clicking on the order button
-    if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        orderDrawer->drawOrderButton(m_player);
+    m_smallTextDrawer->drawText(
+        layout.houseHeader.getX() + headerCrestSize + 10,
+        layout.houseHeader.getY() + 7,
+        text,
+        getHouseDisplayName(),
+        false
+    );
+
+    renderDrawer->renderRectFillColor(
+        layout.radarViewport.getX(),
+        layout.radarViewport.getY(),
+        layout.radarViewport.getWidth(),
+        layout.radarViewport.getHeight(),
+        panelInner
+    );
+    renderDrawer->renderRectColor(
+        layout.radarViewport.getX(),
+        layout.radarViewport.getY(),
+        layout.radarViewport.getWidth(),
+        layout.radarViewport.getHeight(),
+        Color{62, 68, 67, 255}
+    );
+
+    if (!m_player->hasRadarAndEnoughPower() && crest != nullptr) {
+        const int crestSize = std::min(
+            96,
+            layout.radarViewport.getHeight() - 18
+        );
+        renderDrawer->renderStrechFullSprite(
+            crest,
+            cRectangle(
+                layout.radarViewport.getX() +
+                    (layout.radarViewport.getWidth() - crestSize) / 2,
+                layout.radarViewport.getY() +
+                    (layout.radarViewport.getHeight() - crestSize) / 2,
+                crestSize,
+                crestSize
+            ),
+            210
+        );
     }
 }
 
-void cSideBarDrawer::drawCapacities()
+void cSideBarDrawer::drawHdMeter(
+    const cRectangle &rect,
+    const std::string &label,
+    int value,
+    int maximum,
+    Color fill,
+    bool warning) const
 {
-    drawPowerUsage();
-    drawCreditsUsage();
+    const int safeMaximum = std::max(1, maximum);
+    const float ratio = std::clamp(
+        static_cast<float>(value) / static_cast<float>(safeMaximum),
+        0.0f,
+        1.0f
+    );
+    const Color border{104, 82, 43, 255};
+    const Color text{225, 218, 190, 255};
+    const Color warningColor = warning
+        ? m_player->getErrorFadingColor()
+        : fill;
+
+    renderDrawer->renderRectFillColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        Color{10, 13, 15, 255}
+    );
+    renderDrawer->renderRectColor(
+        rect.getX(),
+        rect.getY(),
+        rect.getWidth(),
+        rect.getHeight(),
+        border
+    );
+    m_smallTextDrawer->drawText(
+        rect.getX() + 4,
+        rect.getY() + 2,
+        text,
+        label,
+        false
+    );
+    const std::string amount = std::format("{}/{}", value, maximum);
+    const int amountWidth = m_smallTextDrawer->getTextLength(amount);
+    m_smallTextDrawer->drawText(
+        rect.getEndX() - amountWidth - 4,
+        rect.getY() + 2,
+        text,
+        amount,
+        false
+    );
+
+    const int barX = rect.getX() + 4;
+    const int barY = rect.getEndY() - 7;
+    const int barWidth = rect.getWidth() - 8;
+    renderDrawer->renderRectFillColor(
+        barX,
+        barY,
+        barWidth,
+        4,
+        Color{31, 35, 36, 255}
+    );
+    renderDrawer->renderRectFillColor(
+        barX,
+        barY,
+        static_cast<int>(barWidth * ratio),
+        4,
+        warningColor
+    );
 }
 
-void cSideBarDrawer::drawCandybar()
+void cSideBarDrawer::drawHdCapacities()
 {
-    renderDrawer->renderSprite(candiBarRenderer,game.m_screenW - cSideBar::SidebarWidth,40);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH
+    );
+    const int produced = std::max(0, m_player->getPowerProduced());
+    const int used = std::max(0, m_player->getPowerUsage());
+    drawHdMeter(
+        layout.powerMeter,
+        layout.powerMeter.getWidth() < 140 ? localization::text("PWR", "ЭНЕРГ.") : localization::text("POWER", "ЭНЕРГИЯ"),
+        used,
+        produced,
+        Color{72, 202, 103, 255},
+        !m_player->bEnoughPower()
+    );
+
+    drawHdMeter(
+        layout.spiceMeter,
+        layout.spiceMeter.getWidth() < 140 ? localization::text("SPC", "ПРЯН.") : localization::text("SPICE", "ПРЯНОСТЬ"),
+        std::max(0, m_player->getCredits()),
+        std::max(1, static_cast<int>(m_player->getMaxCredits())),
+        Color{218, 139, 47, 255},
+        !m_player->bEnoughSpiceCapacityToStoreCredits()
+    );
 }
 
-void cSideBarDrawer::drawMinimap()
+void cSideBarDrawer::drawHdBuildingLists()
 {
-    Texture *sprite = candyHorizonBar;
-    int drawX = (game.m_screenW - sprite->w) + 1;
-    // 128 pixels (each pixel is a cell) + 8 margin
-    int heightMinimap = cSideBar::HeightOfMinimap;
-    int drawY = cSideBar::TopBarHeight + heightMinimap;
-    renderDrawer->renderSprite(sprite, drawX, drawY);
-
-    // 11, 10
-    // 78, 60
-    // ------
-    // 67, 50 (width/height)
-
-    bool hasRadarAndEnoughPower = m_player->hasRadarAndEnoughPower();
-
-    if (hasRadarAndEnoughPower) {
-        return; // bail, because we render the minimap
+    m_sidebar = m_player->getSideBar();
+    const int selectedListId = m_sidebar->getSelectedListID();
+    cBuildingList *selectedList = nullptr;
+    if (selectedListId >= 0 && selectedListId < cSideBar::LIST_MAX) {
+        selectedList = m_sidebar->getList(selectedListId);
     }
 
-    // else, we render the house emblem
-    renderDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,game.m_screenW-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
-                                      m_player->getEmblemBackgroundColor());
-
-    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS)) {
-        int bitmapId = BMP_SELECT_HOUSE_ATREIDES;
-
-        int srcX = 11;
-        int srcY = 10;
-
-        // draw house emblem, which is the same as the 'select house x' picture, but partially
-        int emblemWidth = 68;
-        int emblemHeight = 50;
-
-        if (m_player->isHouse(HARKONNEN)) {
-            bitmapId = BMP_SELECT_HOUSE_HARKONNEN;
-        }
-
-        if (m_player->isHouse(ORDOS)) {
-            bitmapId = BMP_SELECT_HOUSE_ORDOS;
-            emblemHeight = 49;
-            srcY = 11;
-        }
-
-        int emblemDesiredWidth = (emblemWidth * 2);
-        int emblemDesiredHeight = (emblemHeight * 2);
-
-        drawX += (sprite->w / 2) - (emblemDesiredWidth / 2);
-        drawY = cSideBar::TopBarHeight + ((heightMinimap / 2) - (emblemDesiredHeight / 2));
-
-        cRectangle src = {srcX, srcY, emblemWidth,emblemHeight};
-        cRectangle dest = {drawX, drawY, emblemDesiredWidth, emblemDesiredHeight};
-        renderDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
+    const HudLayout layout = HudLayout::create(
+        game.m_screenW,
+        game.m_screenH,
+        selectedList != nullptr &&
+            selectedList->getType() == eListType::LIST_STARPORT
+    );
+
+    renderDrawer->renderRectFillColor(
+        layout.tabs.getX(),
+        layout.tabs.getY(),
+        layout.tabs.getWidth(),
+        layout.tabs.getHeight(),
+        Color{13, 16, 18, 255}
+    );
+
+    const int startPos = eListTypeAsInt(eListType::LIST_CONSTYARD);
+    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
+        cBuildingList *list = m_sidebar->getList(listId);
+        m_buildingListDrawer.drawButton(
+            list,
+            selectedListId == listId
+        );
     }
-}
 
-void cSideBarDrawer::createCandyBar()
-{
-    int heightInPixels = (game.m_screenH - cSideBar::TopBarHeight);
-    // ball first
-    renderDrawer->renderSprite(candyBarBall, 0,0); // height of ball = 25
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
-    // now draw pieces untill the end (height of piece is 23 pixels)
-    int startY = 26 + 10; // end of ball (26) + height of top m_candybar (=10) , makes 36
-    int heightMinimap = cSideBar::HeightOfMinimap;
-    // auto tmp = cRectangle{0,0,24, heightMinimap - (6 + 1)};  // (add 1 pixel for room between ball and bar)
-    for (int y = startY; y < (heightMinimap); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+    if (uiaudit::isEnabled()) {
+        uiaudit::recordArea("build-list", layout.catalog.getX(), layout.catalog.getY(), layout.catalog.getWidth(), layout.catalog.getHeight());
     }
-    // note: no need to take top bar into account because 'm_candybar' is a separate bitmap so coords start at 0,0
-    // ball is 6 pixels higher than horizontal m_candybar
-    int ballY = (heightMinimap) - 6;
-
-    // draw bottom m_candybar
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
-
-    // draw ball
-    renderDrawer->renderSprite(candyBarBall, 0, ballY); // height of ball = 25
-
-    // draw top m_candybar again
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
-
-    startY = ballY + 26 + 10;
-    for (int y = startY; y < (heightInPixels + 23); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+    renderDrawer->renderRectFillColor(
+        layout.catalog.getX(),
+        layout.catalog.getY(),
+        layout.catalog.getWidth(),
+        layout.catalog.getHeight(),
+        Color{12, 15, 17, 255}
+    );
+    renderDrawer->renderRectColor(
+        layout.catalog.getX(),
+        layout.catalog.getY(),
+        layout.catalog.getWidth(),
+        layout.catalog.getHeight(),
+        Color{93, 75, 40, 255}
+    );
+
+    if (selectedList != nullptr) {
+        m_buildingListDrawer.drawList(selectedList, selectedListId);
     }
-    // draw bottom
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
-}
-
-void cSideBarDrawer::drawPowerUsage() const
-{
-    int arbitraryMargin = 6;
-    int barTotalHeight = game.m_screenH - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
-    int barY = cSideBar::TotalHeightBeforePowerBarStarts + arbitraryMargin;
-    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
-    //cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::black()); //renderDrawer->getColor_BLACK());
-
-    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxPowerOutageOfWindtrap = sStructureInfo[WINDTRAP].power_give;
-    float totalPowerOutput = (1 + (m_player->getAmountOfStructuresForType(WINDTRAP))) * maxPowerOutageOfWindtrap;
-    float powerIn = (float)m_player->getPowerProduced() / totalPowerOutput;
-    float powerUse = (float)m_player->getPowerUsage() / totalPowerOutput;
-
-    float barHeightToDraw = barTotalHeight * powerIn;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerInY = barY + (barTotalHeight - barHeightToDraw);
-
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
-
-    barHeightToDraw = barTotalHeight * powerUse;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerOutY = barY + (barTotalHeight - barHeightToDraw);
-
-    float powerUsageRatio = ((float)m_player->getPowerUsage() + 1) / ((float)m_player->getPowerProduced() + 1);
-    int r = powerUsageRatio * 255;
-    int g = (1.1 - powerUsageRatio) * 255;
-
-    if (r > 255) r = 255;
-    if (g > 255) g = 255;
 
-    if (m_player->bEnoughPower()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{(Uint8)r, (Uint8)g, 32,255});
-    }
-    else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
+    auto mouse = game.getMouse();
+    for (int listId = startPos; listId < cSideBar::LIST_MAX; ++listId) {
+        if (listId == selectedListId) {
+            continue;
+        }
+        cBuildingList *list = m_sidebar->getList(listId);
+        if (list->isAvailable() &&
+            list->isOverButton(mouse->getX(), mouse->getY())) {
+            m_buildingListDrawer.drawButtonHoverRectangle(list);
+        }
     }
 
-    renderDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
-
-    renderDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
-
-    // draw darker 'sides' at the left and top
-    Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
-    if (m_player->bEnoughPower()) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
-    }
-    else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
+    if (selectedList != nullptr &&
+        selectedList->getType() == eListType::LIST_STARPORT) {
+        drawManager->getOrderDrawer()->drawOrderButton(m_player);
     }
 }
 
-void cSideBarDrawer::drawCreditsUsage()
+void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
 {
-    int barTotalHeight = (cSideBar::HeightOfMinimap - 76);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
-    int barY = cSideBar::TopBarHeight + 48;
-    int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
-    // cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
-
-    // STEFAN: 01/05/2021 -> looks like a lot of this code can be moved to the player class to retrieve max spice capacity
-    // and so forth.
-
-    // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxSpiceCapacity = 1000; // this is still hard coded, need to move to INI file
-    int structuresWithSpice = m_player->getAmountOfStructuresForType(REFINERY) + m_player->getAmountOfStructuresForType(SILO);
-    float totalSpiceCapacity = (1 + structuresWithSpice) * maxSpiceCapacity;
-    float maxSpice = m_player->getMaxCredits() / totalSpiceCapacity;
-    float spiceStored = static_cast<float>(m_player->getCredits()) / totalSpiceCapacity;
-
-    float barHeightToDraw = barTotalHeight * maxSpice;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerInY = barY + (barTotalHeight - barHeightToDraw);
-
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
-
-    barHeightToDraw = barTotalHeight * spiceStored;
-    if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
-    int powerOutY = barY + (barTotalHeight - barHeightToDraw);
-
-    auto spiceCapacityRatio = static_cast<float>(m_player->getCredits() + 1) / (m_player->getMaxCredits() + 1);
-    spiceCapacityRatio = std::clamp(spiceCapacityRatio, 0.0f, 1.0f);
-    int r = spiceCapacityRatio * 255;
-    int g = (1.1 - spiceCapacityRatio) * 255;
-
-    if (r > 255) r = 255;
-    if (g > 255) g = 255;
-
-    if (m_player->bEnoughSpiceCapacityToStoreCredits()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, (Uint8)r,(Uint8)g, 32,255);
-    }
-    else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
-    }
-
-    renderDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
-
-    // draw darker 'sides' at the left and top
-    Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
-
-    if (spiceCapacityRatio>0.95) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
-    } else  if (spiceCapacityRatio<0.05) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
-    } else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
-    }
+    m_player = pPlayer;
+    m_buildingListDrawer.setPlayer(pPlayer);
 }
````

## src/drawers/cSideBarDrawer.cpp: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cSideBarDrawer.cpp
```

stdout (23830 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.cpp b/src/drawers/cSideBarDrawer.cpp
index 009617be..0fd34e64 100644
--- a/src/drawers/cSideBarDrawer.cpp
+++ b/src/drawers/cSideBarDrawer.cpp
@@ -1,50 +1,70 @@
-#include "cSideBarDrawer.h"
+/**
+ * @file cSideBarDrawer.cpp
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
 
-#include "d2tmc.h"
+#include "cSideBarDrawer.h"
+#include "include/sGameServices.h"
 #include "data/gfxinter.h"
 #include "drawers/SDLDrawer.hpp"
 #include "drawers/cOrderDrawer.h"
 #include "managers/cDrawManager.h"
-#include "player/cPlayer.h"
+#include "gameobjects/players/cPlayer.h"
 #include "utils/Graphics.hpp"
-#include <SDL2/SDL.h>
+#include "utils/texture_utils.h"
 #include "context/GameContext.hpp"
 #include "context/GraphicsContext.hpp"
+#include "context/cInfoContext.h"
+#include "context/cGameObjectContext.h"
+#include "controls/cMouse.h"
+#include <SDL3/SDL.h>
 #include <algorithm>
+#include "include/cAssert.h"
+#include "game/cGameSettings.h"
+#include "include/Texture.hpp"
 
-cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player) :
+cSideBarDrawer::cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services) :
     m_player(player),
     m_gfxinter(ctx->getGraphicsContext()->gfxinter.get()),
+    m_sdlDrawer(ctx->getSDLDrawer()),
+    m_ctx(ctx),
+    m_services(services),
     m_buildingListDrawer(ctx, player),
     m_sidebar(nullptr),
     m_sidebarColor(Color{214, 149, 20,255})
 {
-    assert(player);
-
-    candyBarBall = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex);
-    candyBarPiece = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex);
-    candyHorizonBar = m_player->createTextureFromIndexedSurfaceWithPalette(
-        m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex);
+    d2tm_assert(player!= nullptr);
+    d2tm_assert(ctx != nullptr);
+    d2tm_assert(services != nullptr);
 
-    candiBarRenderer = renderDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, game.m_screenH-40);
-    renderDrawer->beginDrawingToTexture(candiBarRenderer);
-    createCandyBar();
-    renderDrawer->endDrawingToTexture();
+    m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());
+    createPlayerCandyBar();
 }
 
 cSideBarDrawer::~cSideBarDrawer()
 {
-    if (candyBarBall)
-        delete candyBarBall;
-    if (candyBarPiece)
-        delete candyBarPiece;
-    if (candyHorizonBar)
-        delete candyHorizonBar;
-
-    if (candiBarRenderer)
-        delete candiBarRenderer;
+    // smart pointers handle cleanup
+    // delete m_candyBarBall; --- IGNORE ---
+    // delete m_candyBarPiece; --- IGNORE ---
+    // delete m_candyHorizonBar; --- IGNORE ---
+    // delete m_candiBarRenderer; --- IGNORE ---
+}
+
+void cSideBarDrawer::serviceInit(sGameServices* services)
+{
+    m_infos = services->info;
+    m_mouse = services->mouse;
+    m_buildingListDrawer.serviceInit(services);
 }
 
 void cSideBarDrawer::onNotifyMouseEvent(const s_MouseEvent &event)
@@ -61,7 +81,7 @@ void cSideBarDrawer::onNotifyKeyboardEvent(const cKeyboardEvent &event)
 void cSideBarDrawer::draw()
 {
     // black out sidebar
-    renderDrawer->renderRectFillColor((game.m_screenW - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, game.m_screenH, Color{0, 0, 0,255});
+    m_sdlDrawer->renderRectFillColor((m_services->settings->getScreenW() - cSideBar::SidebarWidth), 0, cSideBar::SidebarWidth, m_services->settings->getScreenH(), Color{0, 0, 0,255});
 
     drawCandybar();
 
@@ -72,8 +92,31 @@ void cSideBarDrawer::draw()
 
 void cSideBarDrawer::setPlayer(cPlayer *pPlayer)
 {
+    const bool houseChanged = m_player->getHouse() != pPlayer->getHouse();
     m_player = pPlayer;
     m_buildingListDrawer.setPlayer(pPlayer);
+    if (houseChanged) {
+        createPlayerCandyBar();
+    }
+}
+
+// (re)creates the house-colored candybar textures and renders them into the candybar texture
+void cSideBarDrawer::createPlayerCandyBar()
+{
+    m_candyBarBall.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_BALL), TransparentColorIndex, m_gfxinter->getDensity()));
+    m_candyBarPiece.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(BMP_GERALD_CANDYBAR_PIECE), TransparentColorIndex, m_gfxinter->getDensity()));
+    m_candyHorizonBar.reset(createPlayerTextureFromIndexedSurfaceWithPalette(m_sdlDrawer,
+        m_player, m_gfxinter->getSurface(HORIZONTAL_CANDYBAR), TransparentColorIndex, m_gfxinter->getDensity()));
+
+    if (m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()) {
+        delete m_candiBarRenderer;
+        m_candiBarRenderer = m_sdlDrawer->createRenderTargetTexture(cSideBar::SidebarWidth, m_services->settings->getScreenH()-40, m_sdlDrawer->getFrameDensity());
+    }
+    m_sdlDrawer->beginDrawingToTexture(m_candiBarRenderer);
+    createCandyBar();
+    m_sdlDrawer->endDrawingToTexture();
 }
 
 void cSideBarDrawer::drawBuildingLists()
@@ -97,14 +140,14 @@ void cSideBarDrawer::drawBuildingLists()
     // draw background of buildlist
     Texture *backgroundSprite = m_gfxinter->getTexture(BMP_GERALD_ICONLIST_BACKGROUND);
 
-    int drawX = game.m_screenW - cSideBar::SidebarWidthWithoutCandyBar + 1;
+    int drawX = m_services->settings->getScreenW() - cSideBar::SidebarWidthWithoutCandyBar + 1;
 
     int startY = cSideBar::TopBarHeight + cSideBar::HeightOfMinimap + cSideBar::HorizontalCandyBarHeight +
                  cSideBar::HeightOfListButton;
 
-    for (; drawX < game.m_screenW; drawX += backgroundSprite->w) {
-        for (int drawY=startY; drawY < game.m_screenH; drawY += backgroundSprite->h) {
-            renderDrawer->renderSprite(backgroundSprite, drawX, drawY);
+    for (; drawX < m_services->settings->getScreenW(); drawX += backgroundSprite->w) {
+        for (int drawY=startY; drawY < m_services->settings->getScreenH(); drawY += backgroundSprite->h) {
+            m_sdlDrawer->renderSprite(backgroundSprite, drawX, drawY);
         }
     }
 
@@ -115,43 +158,43 @@ void cSideBarDrawer::drawBuildingLists()
     int iDrawY = m_buildingListDrawer.getDrawY();
 
     Texture *horBar = m_gfxinter->getTexture(BMP_GERALD_SIDEBAR_PIECE);
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
-    renderDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
+    m_sdlDrawer->renderSprite(horBar, iDrawX-1, iDrawY-38); // above sublist buttons
+    m_sdlDrawer->renderSprite(horBar, iDrawX-1, iDrawY-5); // above normal icons
 
     if (selectedListId > -1) {
         selectedList = m_sidebar->getList(selectedListId);
     }
 
-    int endY = game.m_screenH;
+    int endY = m_services->settings->getScreenH();
     int rows = 6;
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
         rows = 5;
-        endY = game.m_screenH - 50;
+        endY = m_services->settings->getScreenH() - 50; // leave room for button "order" at bottom sidebar
     }
 
     for (int i = 1; i < 3; i++) {
         int barX = (iDrawX - 1) + (i * 66);
         Color darker = Color{89, 56, 0,255};
         Color veryDark = Color{48, 28, 0,255};
-        renderDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
-        renderDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
+        m_sdlDrawer->renderLine( barX - 1, iDrawY, barX - 1, endY, darker);
+        m_sdlDrawer->renderLine( barX, iDrawY, barX, endY, veryDark);
 
         // horizontal lines
         for (int j = 1; j < rows; j++) {
             int barY = iDrawY - 1 + (j * 50);
-            renderDrawer->renderLine( iDrawX, barY-1, game.m_screenW, barY - 1, darker);
-            renderDrawer->renderLine( iDrawX, barY, game.m_screenW, barY, veryDark);
+            m_sdlDrawer->renderLine( iDrawX, barY-1, m_services->settings->getScreenW(), barY - 1, darker);
+            m_sdlDrawer->renderLine( iDrawX, barY, m_services->settings->getScreenW(), barY, veryDark);
         }
     }
 
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
-        renderDrawer->renderRectFillColor(iDrawX, endY, game.m_screenW-iDrawX, game.m_screenH-endY, m_sidebarColor);
-        renderDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
+        m_sdlDrawer->renderRectFillColor(iDrawX, endY, m_services->settings->getScreenW()-iDrawX, m_services->settings->getScreenH()-endY, m_sidebarColor);
+        m_sdlDrawer->renderSprite(horBar, iDrawX-1, endY); // just below the last icons
     }
 
     // vertical lines at the side
-    renderDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, game.m_screenH, Color{255, 211, 125,255}); // left
-    renderDrawer->renderLine( game.m_screenW - 1, iDrawY - 38, game.m_screenW - 1, endY, Color{209, 150, 28,255}); // right
+    m_sdlDrawer->renderLine( iDrawX - 1, iDrawY-38, iDrawX-1, m_services->settings->getScreenH(), Color{255, 211, 125,255}); // left
+    m_sdlDrawer->renderLine( m_services->settings->getScreenW() - 1, iDrawY - 38, m_services->settings->getScreenW() - 1, endY, Color{209, 150, 28,255}); // right
 
     // END drawing icons grid
 
@@ -167,13 +210,12 @@ void cSideBarDrawer::drawBuildingLists()
         if (list->isAvailable() == false) continue; // not available, so no interaction possible
 
         // render hover over border
-        auto m_mouse = game.getMouse();
-        if (list->isOverButton(m_mouse->getX(), m_mouse->getX())) {
+        if (list->isOverButton(m_mouse->getX(), m_mouse->getY())) {
             m_buildingListDrawer.drawButtonHoverRectangle(list);
         }
     }
 
-    cOrderDrawer *orderDrawer = drawManager->getOrderDrawer();
+    cOrderDrawer *orderDrawer = m_services->drawManager->getOrderDrawer();
 
     // allow clicking on the order button
     if (selectedList && selectedList->getType() == eListType::LIST_STARPORT) {
@@ -189,17 +231,21 @@ void cSideBarDrawer::drawCapacities()
 
 void cSideBarDrawer::drawCandybar()
 {
-    renderDrawer->renderSprite(candiBarRenderer,game.m_screenW - cSideBar::SidebarWidth,40);
+    if (m_candiBarRenderer->density != m_sdlDrawer->getFrameDensity()) {
+        createPlayerCandyBar();
+    }
+
+    m_sdlDrawer->renderSprite(m_candiBarRenderer,m_services->settings->getScreenW() - cSideBar::SidebarWidth,40);
 }
 
 void cSideBarDrawer::drawMinimap()
 {
-    Texture *sprite = candyHorizonBar;
-    int drawX = (game.m_screenW - sprite->w) + 1;
+    Texture *sprite = m_candyHorizonBar.get();
+    int drawX = (m_services->settings->getScreenW() - sprite->w) + 1;
     // 128 pixels (each pixel is a cell) + 8 margin
     int heightMinimap = cSideBar::HeightOfMinimap;
     int drawY = cSideBar::TopBarHeight + heightMinimap;
-    renderDrawer->renderSprite(sprite, drawX, drawY);
+    m_sdlDrawer->renderSprite(sprite, drawX, drawY);
 
     // 11, 10
     // 78, 60
@@ -213,10 +259,10 @@ void cSideBarDrawer::drawMinimap()
     }
 
     // else, we render the house emblem
-    renderDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,game.m_screenW-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
+    m_sdlDrawer->renderRectFillColor(drawX + 1, cSideBar::TopBarHeight + 1,m_services->settings->getScreenW()-(drawX + 1), drawY-(cSideBar::TopBarHeight + 1),
                                       m_player->getEmblemBackgroundColor());
 
-    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS)) {
+    if (m_player->isHouse(ATREIDES) || m_player->isHouse(HARKONNEN) || m_player->isHouse(ORDOS) || m_player->isHouse(SARDAUKAR)) {
         int bitmapId = BMP_SELECT_HOUSE_ATREIDES;
 
         int srcX = 11;
@@ -236,6 +282,12 @@ void cSideBarDrawer::drawMinimap()
             srcY = 11;
         }
 
+        if (m_player->isHouse(SARDAUKAR)) {
+            bitmapId = BMP_SELECT_HOUSE_SARDAUKAR;
+            //emblemHeight = 49;
+            //srcY = 11;
+        }
+
         int emblemDesiredWidth = (emblemWidth * 2);
         int emblemDesiredHeight = (emblemHeight * 2);
 
@@ -244,71 +296,71 @@ void cSideBarDrawer::drawMinimap()
 
         cRectangle src = {srcX, srcY, emblemWidth,emblemHeight};
         cRectangle dest = {drawX, drawY, emblemDesiredWidth, emblemDesiredHeight};
-        renderDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
+        m_sdlDrawer->renderStrechSprite(m_gfxinter->getTexture(bitmapId), src, dest);
     }
 }
 
 void cSideBarDrawer::createCandyBar()
 {
-    int heightInPixels = (game.m_screenH - cSideBar::TopBarHeight);
+    int heightInPixels = (m_services->settings->getScreenH() - cSideBar::TopBarHeight);
     // ball first
-    renderDrawer->renderSprite(candyBarBall, 0,0); // height of ball = 25
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
+    m_sdlDrawer->renderSprite(m_candyBarBall.get(), 0,0); // height of ball = 25
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, 26); // height of top = 10
     // now draw pieces untill the end (height of piece is 23 pixels)
     int startY = 26 + 10; // end of ball (26) + height of top m_candybar (=10) , makes 36
     int heightMinimap = cSideBar::HeightOfMinimap;
     // auto tmp = cRectangle{0,0,24, heightMinimap - (6 + 1)};  // (add 1 pixel for room between ball and bar)
     for (int y = startY; y < (heightMinimap); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+        m_sdlDrawer->renderSprite(m_candyBarPiece.get(), 0, y);
     }
     // note: no need to take top bar into account because 'm_candybar' is a separate bitmap so coords start at 0,0
     // ball is 6 pixels higher than horizontal m_candybar
     int ballY = (heightMinimap) - 6;
 
     // draw bottom m_candybar
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, ballY - 10); // height of bottom = 9
 
     // draw ball
-    renderDrawer->renderSprite(candyBarBall, 0, ballY); // height of ball = 25
+    m_sdlDrawer->renderSprite(m_candyBarBall.get(), 0, ballY); // height of ball = 25
 
     // draw top m_candybar again
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_TOP), 0, ballY + 26); // height of top = 10
 
     startY = ballY + 26 + 10;
     for (int y = startY; y < (heightInPixels + 23); y += 24) {
-        renderDrawer->renderSprite(candyBarPiece, 0, y);
+        m_sdlDrawer->renderSprite(m_candyBarPiece.get(), 0, y);
     }
     // draw bottom
-    renderDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
+    m_sdlDrawer->renderSprite(m_gfxinter->getTexture(BMP_GERALD_CANDYBAR_BOTTOM), 0, heightInPixels - 10); // height of top = 10
 }
 
 void cSideBarDrawer::drawPowerUsage() const
 {
     int arbitraryMargin = 6;
-    int barTotalHeight = game.m_screenH - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
+    int barTotalHeight = m_services->settings->getScreenH() - (cSideBar::TotalHeightBeforePowerBarStarts + cSideBar::PowerBarMarginHeight);
+    int barX = (m_services->settings->getScreenW() - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
     int barY = cSideBar::TotalHeightBeforePowerBarStarts + arbitraryMargin;
     int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
     //cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::black()); //renderDrawer->getColor_BLACK());
+    m_sdlDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, Color::Black); //sdlDrawer->getColor_BLACK());
 
     // the maximum power (ie a full bar) is 1 + amount windtraps * power_give (100)
-    int maxPowerOutageOfWindtrap = sStructureInfo[WINDTRAP].power_give;
+    int maxPowerOutageOfWindtrap = m_infos->getStructureInfo(WINDTRAP).power_give;
     float totalPowerOutput = (1 + (m_player->getAmountOfStructuresForType(WINDTRAP))) * maxPowerOutageOfWindtrap;
-    float powerIn = (float)m_player->getPowerProduced() / totalPowerOutput;
-    float powerUse = (float)m_player->getPowerUsage() / totalPowerOutput;
+    float powerIn = static_cast<float>(m_player->getPowerProduced()) / totalPowerOutput;
+    float powerUse = static_cast<float>(m_player->getPowerUsage()) / totalPowerOutput;
 
     float barHeightToDraw = barTotalHeight * powerIn;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerInY = barY + (barTotalHeight - barHeightToDraw);
 
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
+    m_sdlDrawer->renderRectFillColor(barX, powerInY, barWidth, barY+barTotalHeight-powerInY, Color{0, 232, 0,255});
 
     barHeightToDraw = barTotalHeight * powerUse;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerOutY = barY + (barTotalHeight - barHeightToDraw);
 
-    float powerUsageRatio = ((float)m_player->getPowerUsage() + 1) / ((float)m_player->getPowerProduced() + 1);
+    float powerUsageRatio = (static_cast<float>(m_player->getPowerUsage()) + 1) / (static_cast<float>(m_player->getPowerProduced()) + 1);
     int r = powerUsageRatio * 255;
     int g = (1.1 - powerUsageRatio) * 255;
 
@@ -316,36 +368,36 @@ void cSideBarDrawer::drawPowerUsage() const
     if (g > 255) g = 255;
 
     if (m_player->bEnoughPower()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{(Uint8)r, (Uint8)g, 32,255});
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, Color{static_cast<Uint8>(r), static_cast<Uint8>(g), 32,255});
     }
     else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight-powerOutY, m_player->getErrorFadingColor());
     }
 
-    renderDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
+    m_sdlDrawer->renderLine(barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
 
-    renderDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
+    m_sdlDrawer->renderRectColor(barX, barY, barWidth, barTotalHeight, m_sidebarColor);
 
     // draw darker 'sides' at the left and top
     Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
+    m_sdlDrawer->renderLine(barX, barY, barX, barY + barTotalHeight, darker); // left side |
+    m_sdlDrawer->renderLine(barX, barY, barX+barWidth, barY, darker); // top side _
     if (m_player->bEnoughPower()) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER_HIGH),barX-3, barY - 21);
     }
     else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_POWER),barX-3, barY - 21);
     }
 }
 
 void cSideBarDrawer::drawCreditsUsage()
 {
     int barTotalHeight = (cSideBar::HeightOfMinimap - 76);
-    int barX = (game.m_screenW - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
+    int barX = (m_services->settings->getScreenW() - cSideBar::SidebarWidth) + (cSideBar::VerticalCandyBarWidth / 3);
     int barY = cSideBar::TopBarHeight + 48;
     int barWidth = (cSideBar::VerticalCandyBarWidth / 3) - 1;
     // cRectangle powerBarRect(barX, barY, barWidth, barTotalHeight);
-    renderDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
+    m_sdlDrawer->renderRectFillColor(barX, barY, barWidth, barTotalHeight, 0,0,0,255);
 
     // STEFAN: 01/05/2021 -> looks like a lot of this code can be moved to the player class to retrieve max spice capacity
     // and so forth.
@@ -361,7 +413,7 @@ void cSideBarDrawer::drawCreditsUsage()
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
     int powerInY = barY + (barTotalHeight - barHeightToDraw);
 
-    renderDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
+    m_sdlDrawer->renderRectFillColor(barX, powerInY, barWidth, barY + barTotalHeight - powerInY, Color{0, 232, 0,255});
 
     barHeightToDraw = barTotalHeight * spiceStored;
     if (barHeightToDraw > barTotalHeight) barHeightToDraw = barTotalHeight;
@@ -376,24 +428,24 @@ void cSideBarDrawer::drawCreditsUsage()
     if (g > 255) g = 255;
 
     if (m_player->bEnoughSpiceCapacityToStoreCredits()) {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, (Uint8)r,(Uint8)g, 32,255);
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, static_cast<Uint8>(r),static_cast<Uint8>(g), 32,255);
     }
     else {
-        renderDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
+        m_sdlDrawer->renderRectFillColor(barX, powerOutY, barWidth, barY + barTotalHeight - powerOutY, m_player->getErrorFadingColor());
     }
 
-    renderDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
+    m_sdlDrawer->renderLine( barX, powerOutY, barX+barWidth, powerOutY, Color{255, 255, 255,255});
 
     // draw darker 'sides' at the left and top
     Color darker = Color{89, 56, 0,255};
-    renderDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
-    renderDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
+    m_sdlDrawer->renderLine( barX, barY, barX, barY + barTotalHeight, darker); // left side |
+    m_sdlDrawer->renderLine( barX, barY, barX+barWidth, barY, darker); // top side _
 
     if (spiceCapacityRatio>0.95) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_FULL), barX-5, barY-20);
     } else  if (spiceCapacityRatio<0.05) {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS_LOW), barX-5, barY-20);
     } else {
-        renderDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
+        m_sdlDrawer->renderSprite(m_gfxinter->getTexture(ICON_SOLARIS), barX-5, barY-20);
     }
 }
````

## src/drawers/cSideBarDrawer.h: BASE → FORK1

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 9208dcf5a358f40afd95c99480e4e09f781ed566 -- src/drawers/cSideBarDrawer.h
```

stdout (1646 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.h b/src/drawers/cSideBarDrawer.h
index 3e246239..2dc9925b 100644
--- a/src/drawers/cSideBarDrawer.h
+++ b/src/drawers/cSideBarDrawer.h
@@ -6,12 +6,15 @@
 #include "observers/cInputObserver.h"
 #include "sMouseEvent.h"
 
+#include <array>
+
 class Texture;
 class cPlayer;
 class GameContext;
 class Graphics;
 
 class cSideBarDrawer : cInputObserver {
+    friend class UiAuditAccess;
 public:
     explicit cSideBarDrawer(GameContext *ctx, cPlayer *player);
     ~cSideBarDrawer() override;
@@ -27,27 +30,25 @@ public:
 
     void setPlayer(cPlayer *pPlayer);
 
-protected:
-    void drawBuildingLists();
-    void drawCapacities();
-
-    void drawCandybar();
-
-    void drawMinimap();
-
 private:
     cPlayer *m_player;
     Graphics *m_gfxinter;
     cBuildingListDrawer m_buildingListDrawer;
     cSideBar *m_sidebar;
-    Color m_sidebarColor;
-
-    void createCandyBar();
-
-    void drawPowerUsage() const;
-    void drawCreditsUsage();
-    Texture *candyBarBall=nullptr;
-    Texture *candyBarPiece=nullptr;
-    Texture *candyHorizonBar=nullptr;
-    Texture *candiBarRenderer= nullptr;
+    cTextDrawer *m_smallTextDrawer;
+    std::array<Texture *, 3> m_houseCrests{};
+
+    void drawHdSidebar();
+    void drawHdBuildingLists();
+    void drawHdRadarPanel();
+    void drawHdCapacities();
+    void drawHdMeter(
+        const cRectangle &rect,
+        const std::string &label,
+        int value,
+        int maximum,
+        Color fill,
+        bool warning) const;
+    [[nodiscard]] Texture *getHouseCrest() const;
+    [[nodiscard]] std::string getHouseDisplayName() const;
 };
````

## src/drawers/cSideBarDrawer.h: BASE → PORT

Команда:

```sh
export PATH=/srv/dune/tools/git-lfs-3.6.1/usr/bin:$PATH
git diff e17379ad660fca46859b403a6c3d33ec8d831a40 832c953a94a632d57872349013f7ed1a37434715 -- src/drawers/cSideBarDrawer.h
```

stdout (2288 байт):

````text
diff --git a/src/drawers/cSideBarDrawer.h b/src/drawers/cSideBarDrawer.h
index 3e246239..9f01b645 100644
--- a/src/drawers/cSideBarDrawer.h
+++ b/src/drawers/cSideBarDrawer.h
@@ -1,21 +1,44 @@
+/**
+ * @file cSideBarDrawer.h
+ *
+ * Dune 2 - The Maker
+ *
+ * @author Stefan Hendriks & the D2TM Team
+ * @www http://www.dune2themaker.com
+ * @copyright Copyright (c) 2002 - 2026 Stefan Hendriks and contributors
+ * @license This software is released under the MIT License. See LICENSE.md.
+ *
+ * Note: Dune 2 is a trademark of Westwood Studios/Electronic Arts.
+ *
+ * This is a non-commercial educational project.
+ */
+
 #pragma once
 
 #include "cBuildingListDrawer.h"
 #include "cTextDrawer.h"
-#include "controls/cKeyboardEvent.h"
+class cKeyboardEvent;
 #include "observers/cInputObserver.h"
-#include "sMouseEvent.h"
+struct s_MouseEvent;
+
+#include <memory>
 
 class Texture;
 class cPlayer;
 class GameContext;
 class Graphics;
+class SDLDrawer;
+class cInfoContext;
+class cMouse;
+struct sGameServices;
 
 class cSideBarDrawer : cInputObserver {
 public:
-    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player);
+    explicit cSideBarDrawer(GameContext *ctx, cPlayer *player, sGameServices *services);
     ~cSideBarDrawer() override;
 
+    void serviceInit(sGameServices* services);
+
     void onNotifyMouseEvent(const s_MouseEvent &event) override;
     void onNotifyKeyboardEvent(const cKeyboardEvent &event) override;
 
@@ -38,16 +61,22 @@ protected:
 private:
     cPlayer *m_player;
     Graphics *m_gfxinter;
+    SDLDrawer* m_sdlDrawer;
+    GameContext* m_ctx = nullptr;
+    cInfoContext* m_infos = nullptr;
+    cMouse* m_mouse = nullptr;
+    sGameServices* m_services = nullptr;
     cBuildingListDrawer m_buildingListDrawer;
     cSideBar *m_sidebar;
     Color m_sidebarColor;
 
     void createCandyBar();
+    void createPlayerCandyBar();
 
     void drawPowerUsage() const;
     void drawCreditsUsage();
-    Texture *candyBarBall=nullptr;
-    Texture *candyBarPiece=nullptr;
-    Texture *candyHorizonBar=nullptr;
-    Texture *candiBarRenderer= nullptr;
+    std::unique_ptr<Texture> m_candyBarBall;
+    std::unique_ptr<Texture> m_candyBarPiece;
+    std::unique_ptr<Texture> m_candyHorizonBar;
+    Texture *m_candiBarRenderer= nullptr;
 };
````

