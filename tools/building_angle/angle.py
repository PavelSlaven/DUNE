#!/usr/bin/env python3
"""Guide frames and edge-to-edge fitting for buildings at the Outpost camera angle.

Proportions come from BUILD_RADAR in the HD4 pack, frame 0, opaque box
x 23..232, y 12..247: the front wall is the bottom 27 % of the height and
the top corners are chamfered by 5 %.

  python tools/building_angle/angle.py guide 1024x1024 guide.png
  python tools/building_angle/angle.py fit generated.png 2x2 frame.png
  python tools/building_angle/angle.py stretch atlas.png 2x2 8 out.png
  python tools/building_angle/angle.py shadow atlas.png 2x2 8 out.png
  python tools/building_angle/angle.py check atlas.png 2x2 8
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

TILE = 128
FRONT = 0.27
CHAMFER = 0.05
MIN_EDGE_COVERAGE = 0.85
EDGE_BAND = 3
MAGENTA = (255, 0, 255)
ROOF = (190, 190, 190)
FRONT_WALL = (80, 80, 80)
SEAM = (40, 40, 40)


def parse_pair(text):
    a, b = text.lower().split("x")
    return int(a), int(b)


def frame_size(tiles):
    return tiles[0] * TILE, tiles[1] * TILE


def guide(size):
    width, height = size
    front_top = round(height * (1 - FRONT))
    chamfer = round(min(width, height) * CHAMFER)
    seam = max(2, round(min(width, height) / 256))
    image = Image.new("RGB", size, MAGENTA)
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [(chamfer, 0), (width - 1 - chamfer, 0), (width - 1, chamfer),
         (width - 1, front_top), (0, front_top), (0, chamfer)],
        fill=ROOF,
    )
    draw.rectangle((0, front_top, width - 1, height - 1), fill=FRONT_WALL)
    draw.line((0, front_top, width - 1, front_top), fill=SEAM, width=seam)
    return image


def resize_premultiplied(image, size):
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float64)
    alpha = rgba[..., 3:4] / 255.0
    premultiplied = np.concatenate([rgba[..., :3] * alpha, rgba[..., 3:4]], axis=2)
    channels = [
        np.asarray(
            Image.fromarray(premultiplied[..., c].astype(np.float32), "F").resize(size, Image.Resampling.LANCZOS)
        )
        for c in range(4)
    ]
    out = np.stack(channels, axis=2)
    a = np.clip(out[..., 3], 0, 255)
    safe = np.where(a > 1, a, 1.0)[..., None] / 255.0
    rgb = np.where(a[..., None] > 1, np.clip(out[..., :3] / safe, 0, 255), 0)
    a = np.where(a > 1, a, 0)
    return Image.fromarray(np.dstack([rgb, a]).round().astype(np.uint8), "RGBA")


def key_largest(image):
    rgba = np.asarray(image.convert("RGBA"), dtype=np.int32)
    rgb = rgba[..., :3]
    distance = np.sqrt(((rgb - np.array(MAGENTA)) ** 2).sum(axis=2))
    solid = (distance > 60) & (rgba[..., 3] > 127)
    labels, count = ndimage.label(solid, structure=np.ones((3, 3)))
    if count == 0:
        raise ValueError("no opaque pixels after keying magenta")
    largest = 1 + int(np.argmax(ndimage.sum(solid, labels, range(1, count + 1))))
    keep = labels == largest
    rgba = np.dstack([rgb.astype(np.uint8), np.where(keep, 255, 0).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")


def fit(image, tiles):
    keyed = key_largest(image)
    return resize_premultiplied(keyed.crop(opaque_box(keyed)), frame_size(tiles))


def opaque_box(frame):
    return frame.convert("RGBA").getchannel("A").point(lambda v: 255 if v > 127 else 0).getbbox()


def frames_of(atlas, tiles, count):
    width, height = frame_size(tiles)
    if atlas.size != (width, height * count):
        raise ValueError(f"atlas is {atlas.size}, expected {(width, height * count)}")
    return [atlas.crop((0, i * height, width, (i + 1) * height)) for i in range(count)]


def join(frames):
    width, height = frames[0].size
    atlas = Image.new("RGBA", (width, height * len(frames)))
    for i, frame in enumerate(frames):
        atlas.alpha_composite(frame, (0, i * height))
    return atlas


def stretch(atlas, tiles, count):
    # One box for all frames keeps animated parts registered across frames.
    frames = [f.convert("RGBA") for f in frames_of(atlas, tiles, count)]
    boxes = [opaque_box(f) for f in frames]
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes),
           max(b[2] for b in boxes), max(b[3] for b in boxes))
    return join([resize_premultiplied(f.crop(box), frame_size(tiles)) for f in frames])


def shadow(atlas, tiles, count):
    # Same rule as build_shadow in tools/build_sega_imagegen_buildings.py.
    out = []
    for frame in frames_of(atlas, tiles, count):
        alpha = frame.convert("RGBA").getchannel("A").filter(ImageFilter.GaussianBlur(2.0))
        alpha = alpha.point(lambda value: round(value * 0.22))
        silhouette = Image.new("RGBA", frame.size, (5, 4, 3, 0))
        silhouette.putalpha(alpha)
        shifted = Image.new("RGBA", frame.size)
        shifted.alpha_composite(silhouette, (7, 7))
        out.append(shifted)
    return join(out)


def edge_coverage(frame):
    # A band, not the outermost row: resized edges keep a soft fringe of 1-2 px.
    opaque = np.asarray(frame.convert("RGBA"))[..., 3] > 127
    band = EDGE_BAND
    return {
        "top": float(opaque[:band].any(axis=0).mean()),
        "bottom": float(opaque[-band:].any(axis=0).mean()),
        "left": float(opaque[:, :band].any(axis=1).mean()),
        "right": float(opaque[:, -band:].any(axis=1).mean()),
        "touch": float(opaque[0].any() and opaque[-1].any() and opaque[:, 0].any() and opaque[:, -1].any()),
        "fill": float(opaque.mean()),
    }


def check(atlas, tiles, count):
    rows = [edge_coverage(f) for f in frames_of(atlas, tiles, count)]
    ok = all(min(r["top"], r["bottom"], r["left"], r["right"]) >= MIN_EDGE_COVERAGE and r["touch"] == 1.0 for r in rows)
    return ok, rows


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("guide")
    p.add_argument("size", type=parse_pair)
    p.add_argument("out", type=Path)
    p = sub.add_parser("fit")
    p.add_argument("source", type=Path)
    p.add_argument("tiles", type=parse_pair)
    p.add_argument("out", type=Path)
    for name in ("stretch", "shadow", "check"):
        p = sub.add_parser(name)
        p.add_argument("atlas", type=Path)
        p.add_argument("tiles", type=parse_pair)
        p.add_argument("frames", type=int)
        if name != "check":
            p.add_argument("out", type=Path)
    args = parser.parse_args(argv)

    if args.command == "guide":
        guide(args.size).save(args.out)
    elif args.command == "fit":
        fit(Image.open(args.source), args.tiles).save(args.out)
    elif args.command == "stretch":
        stretch(Image.open(args.atlas), args.tiles, args.frames).save(args.out)
    elif args.command == "shadow":
        shadow(Image.open(args.atlas), args.tiles, args.frames).save(args.out)
    else:
        ok, rows = check(Image.open(args.atlas), args.tiles, args.frames)
        for i, r in enumerate(rows):
            print(f"frame {i}: " + " ".join(f"{k} {v:.3f}" for k, v in r.items()))
        print("edge-to-edge: " + ("pass" if ok else "FAIL"))
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
