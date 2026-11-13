#!/usr/bin/env python3
"""Build isolated HD4 masters for the remaining SDL interface artwork.

The images are deliberately redrawn as procedural panel art rather than being
resampled copies.  Nothing under resources/ is modified by this tool.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from hd_assets import read_pack, decode_image, scale_image, safe_name

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACK = ROOT / "resources" / "bin" / "data" / "sdl_inter.dat"
OUT = ROOT / "artifacts" / "hd_completion" / "interface"
SCALE = 4
APPROVED_MASTER_ROOT = ROOT / "resources" / "hd" / "master4" / "sdl_inter"
APPROVED_SIDEBAR_CONTROLS = {
    "BTN_ORDER",
    "LIST_BTN_CONSTYARD",
    "LIST_BTN_FACTORY",
    "LIST_BTN_INFANTRY",
    "LIST_BTN_PALACE",
    "LIST_BTN_STARPORT",
    "LIST_BTN_UPGRADE",
}

NAMES = set([*(f"PROGRESS{i:03d}" for i in range(1, 33)), "PROGRESSFIX", "PROGRESSNA", "READY01", "READY02",
             *(f"STAT{i:02d}" for i in range(1, 22)), "ICON_POWER", "ICON_POWER_HIGH", "ICON_SOLARIS_LOW", "ICON_SOLARIS", "ICON_SOLARIS_FULL",
             "BTN_OPTIONS", "BTN_ORDER", "LIST_BTN_CONSTYARD", "LIST_BTN_FACTORY", "LIST_BTN_INFANTRY", "LIST_BTN_PALACE", "LIST_BTN_STARPORT", "LIST_BTN_UPGRADE",
             "GRID_0X0", "GRID_1X1", "GRID_2X2", "GRID_3X2", "GRID_3X3", "MESSAGE_LEFT", "MESSAGE_MIDDLE", "MESSAGE_RIGHT",
             "BMP_GERALD_CANDYBAR_BALL", "BMP_GERALD_CANDYBAR_BOTTOM", "BMP_GERALD_CANDYBAR_PIECE", "BMP_GERALD_CANDYBAR_TOP", "BMP_GERALD_ICONLIST_BACKGROUND", "BMP_GERALD_SIDEBAR_PIECE", "BMP_GERALD_TOP_BAR", "BMP_TOPBAR_BACKGROUND", "HORIZONTAL_CANDYBAR", "CREDITS_BAR",
             "BMP_D2TM", "BMP_GAME_DUNE", "BMP_GENERATING", "BMP_LOSING", "BMP_SELECT_YOUR_HOUSE", "BMP_UNKNOWNMAP", "BMP_WINNING", "CREDITS_DUNE2_CORE_TEAM", "D2TM_TITLE"])

GROUPS = {
    "progress": lambda n: n.startswith("PROGRESS") or n.startswith("READY"),
    "status": lambda n: n.startswith("STAT") or n.startswith("ICON_"),
    "controls": lambda n: n.startswith(("BTN_", "LIST_", "GRID_", "MESSAGE_")),
    "chrome": lambda n: n.startswith("BMP_GERALD") or n in {"BMP_TOPBAR_BACKGROUND", "HORIZONTAL_CANDYBAR", "CREDITS_BAR"},
    "screens": lambda n: n in {"BMP_D2TM", "BMP_GAME_DUNE", "BMP_GENERATING", "BMP_LOSING", "BMP_SELECT_YOUR_HOUSE", "BMP_UNKNOWNMAP", "BMP_WINNING", "CREDITS_DUNE2_CORE_TEAM", "D2TM_TITLE"},
}

GRAPHITE=(25, 30, 33, 255); DARK=(11, 14, 16, 255); BRASS=(174, 127, 49, 255); GOLD=(225, 178, 77, 255)
HOUSE=[(62, 132, 185, 255), (192, 65, 48, 255), (88, 168, 103, 255)]

def hseed(name: str) -> int: return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)
def px(v: int) -> int: return max(1, v * SCALE)

def canvas(size, alpha=True): return Image.new("RGBA", (px(size[0]), px(size[1])), (0, 0, 0, 0) if alpha else DARK)

def texture(im, seed, alpha=255):
    """Fine deterministic brushed graphite texture, with top-left lighting."""
    p=im.load(); w,h=im.size
    for y in range(h):
        for x in range(w):
            wave=((x*17+y*31+seed) ^ (x*5+y*11+seed>>3)) & 15
            light=int(18*(1-x/max(1,w)-y/max(1,h)))
            v=max(0, min(255, 41 + light + wave - 7))
            p[x,y]=(v, v+4, v+6, alpha)

def line(draw, pts, fill, width=1): draw.line(pts, fill=fill, width=px(width), joint="curve")
def rect(draw, box, fill=None, outline=None, width=1):
    box=tuple(px(int(v)) for v in box); draw.rectangle(box, fill=fill, outline=outline, width=px(width))

def panel(size, seed, inset=0, accent=BRASS, alpha=True):
    im=canvas(size, alpha); texture(im,seed,0 if alpha else 255); d=ImageDraw.Draw(im)
    w,h=size
    # bevel: common two-pixel / eight HD pixel panel language.
    rect(d,(inset,inset,w-1-inset,h-1-inset),outline=(7,9,10,255),width=1)
    line(d,[(px(inset+1),px(h-2-inset)),(px(inset+1),px(inset+1)),(px(w-2-inset),px(inset+1))],(132,142,136,255),1)
    line(d,[(px(w-2-inset),px(inset+2)),(px(w-2-inset),px(h-2-inset)),(px(inset+2),px(h-2-inset))],(5,6,7,255),1)
    if w>8 and h>8: rect(d,(inset+2,inset+2,w-3-inset,h-3-inset),outline=accent,width=1)
    return im,d

def progress(name,size):
    im,d=panel(size,hseed(name),accent=(105,75,30,255)); w,h=size
    level=(int(name[-3:]) if name[-3:].isdigit() else 0) / 32
    if name=="PROGRESSFIX": level=.58
    if name=="PROGRESSNA": level=0
    y=h*.53; x0=5; x1=w-5
    rect(d,(x0,y-4,x1,y+4),fill=(5,8,9,255),outline=(117,87,35,255))
    if level:
        fill=x0+(x1-x0)*level
        for x in range(int(x0)+1,int(fill)):
            c=(199+((x*3)%32), 133+((x*5)%31), 43,255)
            d.line((px(x),px(y-3),px(x),px(y+3)),fill=c,width=px(1))
        for x in range(int(x0)+2,int(fill),4): line(d,[(px(x),px(y-2)),(px(x+2),px(y+2))],(255,218,115,150),1)
    return im

def stat(name,size):
    im,d=panel(size,hseed(name),inset=2,accent=(105,75,30,255)); w,h=size; seed=hseed(name)
    # tactical diorama/grid: intentionally no letters, all status meaning is graphical.
    for i in range(7):
        x=12+i*15; line(d,[(px(x),px(13)),(px(x-18),px(h-13))],(48,59,58,190),1)
        y=14+i*14; line(d,[(px(12),px(y)),(px(w-13),px(y+26))],(48,59,58,190),1)
    for i in range(10):
        x=15+((seed>>i)&0x7f)%96; y=17+((seed>>(i+7))&0x7f)%87
        col=HOUSE[i%3] if i%3 else GOLD
        d.ellipse((px(x-2),px(y-2),px(x+2),px(y+2)),fill=col)
        line(d,[(px(x-4),px(y)),(px(x+4),px(y))],col,1)
    return im

def icon(name,size):
    im,d=panel(size,hseed(name),inset=0,accent=(122,91,36,255)); w,h=size
    col=(235,184,72,255) if "POWER" in name else HOUSE[0]
    if "HIGH" in name or "FULL" in name: col=(239,91,51,255) if "HIGH" in name else (117,210,120,255)
    if "POWER" in name:
        poly=[(w*.56,2),(w*.27,w*.56),(w*.48,w*.56),(w*.4,h-2),(w*.75,w*.39),(w*.55,w*.39)]
        d.polygon([(px(int(x)),px(int(y))) for x,y in poly],fill=col)
    else:
        for r in (2,4,6): d.arc((px(8-r),px(8-r),px(8+r),px(8+r)),200,340,fill=col,width=px(1))
        d.ellipse((px(7),px(7),px(9),px(9)),fill=col)
    return im

def button(name,size):
    im,d=panel(size,hseed(name),inset=1,accent=(145,105,40,255)); w,h=size
    # mechanical stamped token / order-slot, text remains engine-owned.
    if name.startswith("LIST_"):
        col=HOUSE[hseed(name)%3]; rect(d,(7,5,w-8,h-6),fill=(20,26,28,255),outline=col)
        d.polygon([(px(w*.32),px(h*.28)),(px(w*.72),px(h*.5)),(px(w*.32),px(h*.72))],fill=col)
    elif name.startswith("GRID_"):
        cells=name.split("_")[1].split("X"); a,b=map(int,cells); a=max(1,a); b=max(1,b)
        for yy in range(b):
            for xx in range(a): rect(d,(4+xx*(11/a),4+yy*(11/b),14+xx*(11/a),14+yy*(11/b)),fill=(64,72,69,255),outline=GOLD)
    elif name.startswith("MESSAGE_"):
        rect(d,(1,5,w-2,h-6),fill=(47,40,28,255),outline=BRASS)
        for x in range(5,w-4,7): d.ellipse((px(x),px(h/2-1),px(x+2),px(h/2+1)),fill=GOLD)
    else:
        rect(d,(5,5,w-6,h-6),fill=(37,43,43,255),outline=GOLD)
        for x in range(12,w-8,12): line(d,[(px(x),px(11)),(px(x+5),px(h-11))],(94,102,92,255),1)
    return im

def chrome(name,size):
    im,d=panel(size,hseed(name),accent=(125,89,32,255)); w,h=size
    if "BALL" in name:
        d.ellipse((px(3),px(3),px(w-4),px(h-4)),fill=(121,85,33,255),outline=GOLD,width=px(1)); d.ellipse((px(7),px(6),px(w*.55),px(h*.48)),fill=(255,226,142,220))
    elif "CANDYBAR" in name or name=="HORIZONTAL_CANDYBAR":
        rect(d,(2,3,w-3,h-4),fill=(37,32,23,255),outline=BRASS)
        for x in range(5,w-4,8): line(d,[(px(x),px(4)),(px(x-3),px(h-5))],(104,77,35,255),1)
    elif "TOP" in name:
        line(d,[(px(1),px(h*.45)),(px(w-2),px(h*.45))],GOLD,1); line(d,[(px(1),px(h*.72)),(px(w-2),px(h*.72))],(5,6,7,255),1)
    elif "SIDEBAR" in name or "ICONLIST" in name:
        for y in range(8,h-4,16): rect(d,(5,y,w-6,y+10),fill=(32,38,39,255),outline=(88,103,95,255))
    else:
        for x in range(4,w-3,9): line(d,[(px(x),px(3)),(px(x-5),px(h-4))],(87,67,37,255),1)
    return im

def screen(name,size):
    im,d=panel(size,hseed(name),inset=1,accent=(144,100,35,255)); w,h=size; seed=hseed(name)
    # A silent strategic/astral display: no typography so runtime captions remain legible.
    for r in range(12, max(14,min(w,h)//2), 16):
        d.arc((px(w/2-r),px(h/2-r),px(w/2+r),px(h/2+r)),205,338,fill=(99,78,37,180),width=px(1))
    for i in range(max(8,(w*h)//3500)):
        x=6+((seed*(i+11)+i*i*43)%(max(1,w-12))); y=6+((seed*(i+3)+i*31)%(max(1,h-12)))
        col=HOUSE[i%3] if i%7==0 else (188,147,67,180)
        d.ellipse((px(x),px(y),px(x+1),px(y+1)),fill=col)
    # centerpiece hierarchy differs by asset but stays language-consistent.
    if "UNKNOWNMAP" in name:
        for x in range(20,w-18,16): line(d,[(px(x),px(14)),(px(x-11),px(h-15))],(82,104,94,255),1)
        for y in range(18,h-14,15): line(d,[(px(16),px(y)),(px(w-16),px(y+18))],(82,104,94,255),1)
    else:
        d.ellipse((px(w*.35),px(h*.28),px(w*.65),px(h*.72)),fill=(28,43,47,255),outline=GOLD,width=px(1))
        d.arc((px(w*.38),px(h*.31),px(w*.62),px(h*.69)),190,30,fill=HOUSE[seed%3],width=px(2))
    return im

def category(name): return next(k for k,v in GROUPS.items() if v(name))

def render(name,size):
    group=category(name)
    if group=="progress": return progress(name,size)
    if group=="status": return stat(name,size) if name.startswith("STAT") else icon(name,size)
    if group=="controls": return button(name,size)
    if group=="chrome": return chrome(name,size)
    return screen(name,size)

def contact_sheet(items, destination, title):
    thumb=(220,160); cols=4; rows=math.ceil(len(items)/cols); im=Image.new("RGBA",(cols*thumb[0],rows*thumb[1]),(13,16,18,255)); d=ImageDraw.Draw(im)
    for i,(name,path) in enumerate(items):
        tile=Image.open(path).convert("RGBA"); tile.thumbnail((200,112),Image.Resampling.LANCZOS)
        x=(i%cols)*thumb[0]+10; y=(i//cols)*thumb[1]+25
        im.alpha_composite(tile,(x+(200-tile.width)//2,y+(112-tile.height)//2))
        d.text((x,y+118),name,fill=(231,193,107,255))
    d.text((10,5),title,fill=(255,222,145,255))
    im.save(destination)

def main():
    if not SOURCE_PACK.is_file(): raise SystemExit(f"missing {SOURCE_PACK}")
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    entries=[e for e in read_pack(SOURCE_PACK) if e.name in NAMES]
    if len(entries) != len(NAMES): raise SystemExit(f"expected {len(NAMES)} targets, found {len(entries)}")
    records=[]; sheets={key:[] for key in GROUPS}
    for entry in entries:
        src=decode_image(entry.payload)
        if src is None: raise SystemExit(f"{entry.name} is not image")
        name=f"{entry.index:04d}_{safe_name(entry.name)}.png"; group=category(entry.name)
        path=OUT/group/name; path.parent.mkdir(exist_ok=True)
        if entry.name in APPROVED_SIDEBAR_CONTROLS:
            approved_path = (
                APPROVED_MASTER_ROOT
                / f"{entry.index:04d}_{safe_name(entry.name)}.png"
            )
            if not approved_path.is_file():
                raise SystemExit(
                    f"missing approved sidebar master {approved_path}; "
                    "run build_sidebar_controls_from_reference.py first"
                )
            master = Image.open(approved_path).convert("RGBA")
            expected_size = (src.width * SCALE, src.height * SCALE)
            if master.size != expected_size:
                raise SystemExit(
                    f"invalid approved sidebar master {approved_path}: "
                    f"{master.size}, expected {expected_size}"
                )
        else:
            master = render(entry.name, src.size)
        master.save(path, optimize=True)
        nearest=scale_image(src, SCALE).convert("RGBA")
        lanczos=src.convert("RGBA").resize(master.size,Image.Resampling.LANCZOS)
        alpha=master.getchannel("A"); bbox=alpha.getbbox()
        rec={"id":entry.index,"name":entry.name,"group":group,"source_size":list(src.size),"hd_size":list(master.size),"file":path.relative_to(OUT).as_posix(),"mode":master.mode,"alpha_nonempty":bbox is not None,"differs_from_nearest":master.tobytes()!=nearest.tobytes(),"differs_from_lanczos":master.tobytes()!=lanczos.tobytes(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
        if not (rec["alpha_nonempty"] and rec["differs_from_nearest"] and rec["differs_from_lanczos"]): raise SystemExit(f"validation failed for {entry.name}")
        records.append(rec); sheets[group].append((entry.name,path))
    for group,items in sheets.items(): contact_sheet(items,OUT/f"contact_{group}.png",f"HD4 interface masters — {group}")
    manifest={"format":1,"source_pack":str(SOURCE_PACK),"scale":SCALE,"asset_count":len(records),"description":"Procedural graphite, aged brass and ochre interface redraws; PAL_INTER deliberately excluded.","assets":records}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(f"wrote {len(records)} masters to {OUT}")

if __name__ == "__main__": main()
