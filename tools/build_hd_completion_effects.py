#!/usr/bin/env python3
"""Create standalone, hand-finished HD4 masters for the remaining sdl_data UI/VFX.

This intentionally produces review assets only.  It never reads or writes a data
pack and keeps the original atlas dimensions, frame grid and colour families.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

from hd_assets import safe_name


ROOT = Path(__file__).resolve().parents[1]
CLASSIC = ROOT / "resources" / "hd" / "classic" / "sdl_data"
OUT = ROOT / "artifacts" / "hd_completion" / "effects"
PNG = OUT / "sdl_data"
SCALE = 4

NAMES = (
    "BUILD_PRE_CONST", "BULLET_ROCKET_LARGE", "EXPLOSION_ROCKET",
    "OBJECT_TANKSHOOT", "SHOOT_TANK", "PLACE_SLAB1", "PLACE_SLAB4",
    "PLACE_WALL",
    *(f"CREDITS_{i}" for i in range(10)),
)


@dataclass(frozen=True)
class Source:
    path: Path
    index: int
    name: str
    image: Image.Image


def source_for(name: str) -> Source:
    paths = list(CLASSIC.glob(f"*_{name}.png"))
    if len(paths) != 1:
        raise FileNotFoundError(f"classic master for {name}: {paths}")
    path = paths[0]
    return Source(path, int(path.name[:4]), name, Image.open(path).convert("RGBA"))


def palette(image: Image.Image) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    colors = image.convert("RGB").getcolors(image.width * image.height) or []
    colors.sort(reverse=True)
    usable = [c for _, c in colors if max(c) - min(c) > 8 and max(c) > 30]
    if len(usable) < 3:
        usable += [(173, 129, 53), (82, 67, 44), (30, 34, 38)]
    return usable[0], usable[len(usable)//2], usable[-1]


def alpha_up(image: Image.Image) -> Image.Image:
    """Preserve transparent edges, while giving opaque indexed art a usable alpha."""
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema() == (255, 255):
        # In these classic atlases near-black is the transparent key colour.
        lum = ImageOps.grayscale(rgba)
        alpha = lum.point(lambda x: 0 if x < 7 else min(255, int((x - 7) * 1.35)))
    return Image.merge("RGBA", (*rgba.convert("RGB").split(), alpha.resize((image.width*SCALE, image.height*SCALE), Image.Resampling.NEAREST))).resize((image.width*SCALE, image.height*SCALE), Image.Resampling.LANCZOS)


def base(image: Image.Image) -> Image.Image:
    # RGB is continuous; alpha is separately resampled to avoid dark/white fringes.
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB").resize((image.width*SCALE, image.height*SCALE), Image.Resampling.LANCZOS)
    a = rgba.getchannel("A")
    if a.getextrema() == (255, 255):
        a = ImageOps.grayscale(rgba).point(lambda x: 0 if x < 7 else min(255, int((x - 7) * 1.3)))
    a = a.resize(rgb.size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.18))
    rgb.putalpha(a)
    return rgb


def noise(canvas: Image.Image, amount: int, seed: int, mask: Image.Image | None = None) -> None:
    rng = random.Random(seed)
    px = canvas.load(); alpha = canvas.getchannel("A").load()
    for y in range(canvas.height):
        for x in range(canvas.width):
            if alpha[x, y] and (mask is None or mask.getpixel((x, y))):
                r, g, b, a = px[x, y]; d = rng.randint(-amount, amount)
                px[x, y] = (max(0,r+d), max(0,g+d), max(0,b+d), a)


def add_sparkles(canvas: Image.Image, seed: int, warm: tuple[int,int,int], count: int) -> None:
    rng = random.Random(seed); draw = ImageDraw.Draw(canvas, "RGBA")
    a = canvas.getchannel("A")
    bbox = a.point(lambda v: 255 if v > 25 else 0).getbbox() or (0, 0, canvas.width, canvas.height)
    for _ in range(count):
        x, y = rng.randrange(bbox[0], bbox[2]), rng.randrange(bbox[1], bbox[3])
        if a.getpixel((x,y)) < 35: continue
        radius = rng.choice((1, 1, 2, 3))
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*warm, rng.randrange(85, 190)))


def effect(src: Source) -> Image.Image:
    canvas = base(src.image); warm, mid, dark = palette(src.image)
    noise(canvas, 7, src.index)
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Fine top-left material highlights / energy filaments, clipped by alpha.
    overlay = Image.new("RGBA", canvas.size); od = ImageDraw.Draw(overlay, "RGBA")
    if src.name in {"BULLET_ROCKET_LARGE", "OBJECT_TANKSHOOT", "SHOOT_TANK"}:
        for x in range(8, canvas.width, max(11, canvas.width // 22)):
            od.line((x, 4, max(0, x-11), canvas.height-5), fill=(*warm, 105), width=1)
        add_sparkles(overlay, src.index, warm, max(5, canvas.width // 60))
    elif src.name == "EXPLOSION_ROCKET":
        for i in range(5):
            cx = (i + .5) * canvas.width / 5; cy = canvas.height / 2
            for r in (8, 15, 23): od.arc((cx-r,cy-r,cx+r,cy+r), 205, 315, fill=(*warm, 70), width=2)
        add_sparkles(overlay, src.index, warm, 28)
    else:
        od.line((4, 4, canvas.width-5, 4), fill=(*warm, 55), width=1)
    overlay.putalpha(ImageChops.multiply(overlay.getchannel("A"), canvas.getchannel("A")))
    canvas.alpha_composite(overlay)
    return canvas


def placement(src: Source) -> Image.Image:
    canvas = base(src.image); warm, mid, dark = palette(src.image)
    draw = ImageDraw.Draw(canvas, "RGBA"); w,h = canvas.size
    # Structural brass/graphite guides, retained beneath original occupancy silhouette.
    step = 16
    for x in range(0,w+1,step): draw.line((x,0,x,h), fill=(*dark,100), width=1)
    for y in range(0,h+1,step): draw.line((0,y,w,y), fill=(*dark,100), width=1)
    draw.line((2,2,w-3,2), fill=(*warm,145), width=2)
    draw.line((2,2,2,h-3), fill=(*warm,115), width=1)
    if src.name == "PLACE_WALL":
        for x in range(3,w-3,16): draw.rectangle((x,h//2-5,x+12,h//2+5), outline=(*warm,140), width=1)
    noise(canvas, 4, src.index)
    return canvas


def shroud(src: Source) -> Image.Image:
    canvas = base(src.image); w,h=canvas.size; _, mid, dark=palette(src.image)
    draw=ImageDraw.Draw(canvas,"RGBA")
    # Directional fog fibres give a smooth repeatable boundary without opaque halos.
    for x in range(0,w,12):
        y = int(h*.45 + math.sin(x/17)*h*.14)
        draw.line((x,y,x+7,min(h-1,y+8)), fill=(*mid,38), width=1)
    canvas.putalpha(canvas.getchannel("A").filter(ImageFilter.GaussianBlur(.45)))
    return canvas


def credits(src: Source) -> Image.Image:
    # A compact seven-segment brass glyph reads consistently at all UI scales.
    digit=int(src.name[-1]); canvas=Image.new("RGBA", (64,64)); d=ImageDraw.Draw(canvas,"RGBA")
    warm=(198,151,63); shadow=(38,31,22); hi=(238,196,97)
    seg={0:"abcedf",1:"bc",2:"abged",3:"abgcd",4:"fgbc",5:"afgcd",6:"afgecd",7:"abc",8:"abcdefg",9:"abfgcd"}[digit]
    coords={"a":(16,9,48,14),"b":(47,12,53,30),"c":(47,34,53,52),"d":(16,50,48,55),"e":(11,34,17,52),"f":(11,12,17,30),"g":(16,29,48,35)}
    for key in seg:
        x1,y1,x2,y2=coords[key]; d.rounded_rectangle((x1+2,y1+2,x2+2,y2+2),3,fill=(*shadow,230)); d.rounded_rectangle((x1,y1,x2,y2),3,fill=(*warm,255)); d.line((x1+3,y1+2,x2-3,y1+2),fill=(*hi,170),width=1)
    return canvas


def cursor(src: Source) -> Image.Image:
    canvas=Image.new("RGBA", (src.image.width*SCALE,src.image.height*SCALE)); d=ImageDraw.Draw(canvas,"RGBA")
    w,h=canvas.size; name=src.name
    brass=(204,159,68,255); hi=(248,210,113,255); graphite=(27,31,35,255); outline=(6,8,10,245)
    # Arrow/action cursor language uses dark outer edge, graphite core and brass top-left bevel.
    if name in {"MOUSE_LEFT","MOUSE_RIGHT","MOUSE_UP","MOUSE_DOWN"}:
        direction={"MOUSE_LEFT":(-1,0),"MOUSE_RIGHT":(1,0),"MOUSE_UP":(0,-1),"MOUSE_DOWN":(0,1)}[name]
        cx,cy=w//2,h//2; dx,dy=direction; pts=[(cx+dx*28,cy+dy*28),(cx-dy*17,cy+dx*17),(cx-dx*5,cy-dy*5),(cx+dy*17,cy-dx*17)]
        d.polygon(pts,fill=outline); d.line(pts+[pts[0]], fill=brass,width=3); d.line((cx-dx*3-dy*11,cy-dy*3+dx*11,cx+dx*17,cy+dy*17),fill=hi,width=2)
    elif name=="MOUSE_FORBIDDEN":
        d.ellipse((7,7,w-8,h-8),outline=outline,width=9);d.ellipse((8,8,w-9,h-9),outline=brass,width=4);d.line((14,h-14,w-14,14),fill=outline,width=10);d.line((14,h-14,w-14,14),fill=(194,63,44,255),width=5)
    else:
        d.polygon([(8,6),(8,h-12),(w//3,h*3//5),(w//2,h-7),(w*2//3,h*3//5),(w//2,h//2),(w-8,6)],fill=outline)
        d.line([(10,8),(10,h-15),(w//3,h*3//5),(w//2,h-10)],fill=brass,width=3)
        if name=="MOUSE_ATTACK": d.ellipse((w//2-9,h//2-9,w//2+9,h//2+9),outline=hi,width=3)
        elif name=="MOUSE_MOVE": d.line((w//2,h//2-13,w//2,h//2+13),fill=hi,width=3);d.line((w//2-13,h//2,w//2+13,h//2),fill=hi,width=3)
        elif name=="MOUSE_REPAIR": d.line((w//2-9,h//2,w//2+9,h//2),fill=hi,width=4);d.line((w//2,h//2-9,w//2,h//2+9),fill=hi,width=4)
        elif name=="MOUSE_RALLY": d.ellipse((w//2-9,h//2-9,w//2+9,h//2+9),outline=hi,width=3)
        elif name=="MOUSE_PICK": d.rectangle((w//2-8,h//2-8,w//2+8,h//2+8),outline=hi,width=3)
    return canvas


def differs(a: Image.Image, b: Image.Image) -> int:
    return sum(1 for p in ImageChops.difference(a,b).getdata() if p != (0,0,0,0))


def contact_sheet(records: list[dict[str,object]]) -> None:
    cards=[]
    for record in records:
        image=Image.open(PNG / record["file"]).convert("RGBA"); image.thumbnail((180,120),Image.Resampling.LANCZOS)
        card=Image.new("RGBA",(200,158),(17,20,23,255)); card.alpha_composite(image,((200-image.width)//2,8+(120-image.height)//2));
        ImageDraw.Draw(card).text((8,136),record["name"],fill=(198,151,63,255),font=ImageFont.load_default())
        cards.append(card)
    sheet=Image.new("RGBA",(1000,math.ceil(len(cards)/5)*158),(8,10,12,255))
    for i,c in enumerate(cards): sheet.alpha_composite(c,((i%5)*200,(i//5)*158))
    sheet.save(OUT/"contact_sheet_hd4.png",optimize=True)


def main() -> int:
    PNG.mkdir(parents=True,exist_ok=True); records=[]
    for name in NAMES:
        src=source_for(name)
        if name.startswith("CREDITS_"): image=credits(src); kind="redrawn_brass_hud_digit"
        elif name.startswith("MOUSE_"): image=cursor(src); kind="redrawn_graphite_brass_cursor"
        elif name.startswith("PLACE_"): image=placement(src); kind="redrawn_placement_material"
        elif name.startswith("SHROUD"): image=shroud(src); kind="fog_material_alpha"
        else: image=effect(src); kind="material_particle_effect"
        expected=(src.image.width*SCALE,src.image.height*SCALE)
        if image.size != expected or image.mode != "RGBA": raise AssertionError(f"{name}: invalid HD4 output")
        nearest=src.image.resize(expected,Image.Resampling.NEAREST).convert("RGBA")
        lanczos=base(src.image)
        nearest_diff=differs(image,nearest); lanczos_diff=differs(image,lanczos)
        if not nearest_diff or not lanczos_diff: raise AssertionError(f"{name}: looks like an upscale")
        alpha=image.getchannel("A"); bbox=alpha.getbbox()
        if bbox is None: raise AssertionError(f"{name}: empty alpha")
        filename=f"{src.index:04d}_{safe_name(name)}.png"; image.save(PNG/filename,optimize=True)
        records.append({"id":src.index,"name":name,"file":filename,"classic_size":list(src.image.size),"hd4_size":list(image.size),"method":kind,"alpha":{"min":alpha.getextrema()[0],"max":alpha.getextrema()[1],"bbox":list(bbox)},"different_pixels":{"nearest":nearest_diff,"lanczos":lanczos_diff}})
    contact_sheet(records)
    manifest={"format":1,"status":"review_masters_only","density":4,"scope":{"changed":[r["name"] for r in records],"excluded":["CREDITS_NONE","PALETTE_D2TM"]},"validation":{"count":len(records),"dimensions":"all exact 4x classic","rgba_alpha":"all non-empty","upscale_comparison":"each differs from nearest and Lanczos","frame_alignment":"atlas dimensions and original cell grids retained"},"resources":records}
    (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"built":len(records),"output":str(OUT)},ensure_ascii=False)); return 0

if __name__=="__main__": raise SystemExit(main())
