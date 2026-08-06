#pragma once

#include "AbstractMentat.h"

class OrdosMentat : public AbstractMentat {
public:
    OrdosMentat(GameContext* ctx, bool allowMissionSelect);
    void think();
private:
    void draw_mouth() override;
    void draw_eyes() override;
    void draw_other() override;
    void draw() override;
    void clearHdMovieOpening(Texture *background) override;
};
