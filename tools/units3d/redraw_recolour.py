"""Prepare selected redraws and old recolour masks for the recolour pass."""

from pathlib import Path

from PIL import Image

from tools.units3d.redraw_common import bbox, flat, frame_input, frame_name, keyed, old_canvas


def run(unit, args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for record in unit.frames:
        name = frame_name(record)
        attempt_path = unit.path(record['attempts'][record['pick']])
        with frame_input(record, attempt_path):
            candidate = keyed(attempt_path, figures=unit.data.get('figures', 1))
            bbox(candidate[..., 3])
        flat(candidate).save(output / f"pick_{name}.png")

        with frame_input(record, unit.pack_path):
            body = unit.old_frame('body', record)
            mask = unit.old_frame('house_mask', record)
        body[mask[..., 3] > 127, :3] = (0, 255, 0)
        old_canvas(body).save(output / f"oldmask_{name}.png")
        count += 2
    print(f"{count} recolour inputs: {output}")
    return 0
