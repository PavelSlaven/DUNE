"""Prepare selected redraws and old recolour masks for the recolour pass."""

from pathlib import Path

from PIL import Image

from tools.units3d.redraw_common import flat, keyed, old_canvas


def run(unit, args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for record in unit.frames:
        name = f"r{record['row']}k{record['k']}"
        candidate = keyed(unit.path(record['attempts'][record['pick']]))
        flat(candidate).save(output / f"pick_{name}.png")

        body = unit.old_frame('body', record)
        mask = unit.old_frame('house_mask', record)
        body[mask[..., 3] > 127, :3] = (0, 255, 0)
        old_canvas(body).save(output / f"oldmask_{name}.png")
        count += 2
    print(f"{count} recolour inputs: {output}")
    return 0
