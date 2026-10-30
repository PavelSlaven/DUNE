"""Estimate one alpha and diagonal shift for the old unit shadow."""

import json
import sys

import numpy as np


def _shifted_alpha(unit, shift):
    fw, fh = unit.frame
    atlas_height, atlas_width = unit.image(unit.atlases['body']).shape[:2]
    shifted = np.zeros((atlas_height, atlas_width), dtype=np.float64)
    if shift >= min(fw, fh):
        return shifted
    for record in unit.frames:
        x, y = record['k'] * fw, record['row'] * fh
        body_alpha = unit.old_frame('body', record)[..., 3]
        shifted[y + shift:y + fh, x + shift:x + fw] = body_alpha[:fh - shift, :fw - shift]
    return shifted


def run(unit, args):
    shadow = unit.image(unit.atlases['shadow'])
    old_alpha = shadow[..., 3].astype(np.float64)
    visible = old_alpha > 0
    if not visible.any():
        print('shadow-rule: old shadow has no visible pixels', file=sys.stderr)
        return 1

    rgb = np.median(shadow[..., :3][visible].astype(np.float64), axis=0)
    best = None
    for shift in range(9):
        body_alpha = _shifted_alpha(unit, shift)
        paired = (body_alpha > 0) & visible
        if not paired.any():
            continue
        alpha = float(np.median(255 * old_alpha[paired] / body_alpha[paired]))
        prediction = body_alpha * alpha / 255
        predicted = prediction.ravel()
        observed = old_alpha.ravel()
        predicted -= predicted.mean()
        observed = observed - observed.mean()
        predicted_norm = float(np.linalg.norm(predicted))
        observed_norm = float(np.linalg.norm(observed))
        if predicted_norm == 0 or observed_norm == 0:
            continue
        corr = float(np.dot(predicted, observed) / (predicted_norm * observed_norm))
        if np.isfinite(corr) and (best is None or corr > best[0]):
            best = corr, shift, alpha

    if best is None:
        print('shadow-rule: no shift has an overlap with nonzero variance', file=sys.stderr)
        return 1

    corr, shift, alpha = best
    result = {
        'shift': shift,
        'alpha': int(round(alpha)),
        'rgb': [int(round(value)) for value in rgb],
        'corr': round(corr, 3),
    }
    print(json.dumps(result))
    return int(corr < 0.95)
