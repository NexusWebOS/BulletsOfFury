#!/usr/bin/env python3
"""Recover the approved Level-5 and Level-9 combat reels from their preview GIFs."""

from __future__ import annotations

from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "_BUILD_SOURCE" / "review_combat_packs_2026-08-24" / \
    "CF_EnemyCombatPatterns-Vol.1"

STAGES = {
    5: {
        "source": PACK / "Level-5" / "Documentation" / "CF_EnemyCombatSystems-Lvl5-preview.gif",
        "elite": PACK / "Level-5" / "Elite-Previews" / "VFX-Elite-fracture-halo" /
                 "lvl5-elite-fracture-halo-preview.gif",
        "elite_name": "fracture_halo",
        "names": [
            "beam_frigate", "comet_rammer", "debris_skimmer", "gravity_orb",
            "heavy_interceptor", "mine_layer", "missile_satellite", "portal_mine",
            "repair_drone", "salvage_tug", "shield_leech", "twin_station",
        ],
        "label": (171, 207, 255, 255),
    },
    9: {
        "source": PACK / "Level-9" / "Documentation" / "CF_EnemyCombatSystems-Lvl9-preview.gif",
        "elite": PACK / "Level-9" / "Elite-Previews" / "VFX-Elite-warp-lattice" /
                 "lvl9-elite-warp-lattice-preview.gif",
        "elite_name": "warp_lattice",
        "names": [
            "alien_beacon", "chronal_crawler_tank", "comet_skimmer", "dimensional_gunship",
            "galaxy_interceptor", "gate_carrier", "gate_turret", "gravity_artillery",
            "hyperspace_prism", "mini_warp_tank", "ring_drone", "singularity_mine",
        ],
        "label": (105, 241, 255, 255),
    },
}


def edge_clear(cell: Image.Image) -> Image.Image:
    rgba = cell.convert("RGBA")
    colors = Counter(rgba.getdata())
    background = {px for px, count in colors.most_common(10)
                  if count > 500 and max(px[:3]) < 85}
    w, h = rgba.size; pix = rgba.load()
    seen: set[tuple[int, int]] = set(); todo: deque[tuple[int, int]] = deque()
    for x in range(w): todo.extend(((x, 0), (x, h - 1)))
    for y in range(h): todo.extend(((0, y), (w - 1, y)))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or pix[x, y] not in background: continue
        seen.add((x, y)); pix[x, y] = (0, 0, 0, 0)
        if x: todo.append((x - 1, y))
        if x + 1 < w: todo.append((x + 1, y))
        if y: todo.append((x, y - 1))
        if y + 1 < h: todo.append((x, y + 1))
    return rgba


def keep_hull(cell: Image.Image, floor: int = 196) -> Image.Image:
    w, h = cell.size; px = cell.load()
    for y in range(floor, h):
        for x in range(w): px[x, y] = (0, 0, 0, 0)
    alpha = cell.getchannel("A"); ap = alpha.load()
    unseen = {(x, y) for y in range(h) for x in range(w) if ap[x, y]}
    comps = []
    while unseen:
        start = unseen.pop(); pts = [start]; todo = [start]
        while todo:
            x, y = todo.pop()
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in unseen: unseen.remove(q); todo.append(q); pts.append(q)
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        comps.append((pts,(min(xs),min(ys),max(xs)+1,max(ys)+1)))
    if not comps: return cell
    main, box = max(comps, key=lambda c: len(c[0])); keep=set(main)
    mx0,my0,mx1,my1=box
    for pts,(x0,y0,x1,y1) in comps:
        if pts is main: continue
        # Preview captions are detached five-pixel-tall glyphs immediately beneath the hull.
        # They survived the old broad proximity test and appeared as extra pixels/words inside
        # the runtime sprite box. Reject only that caption geometry; detached engine sparks that
        # overlap the hull's vertical range remain authored animation.
        if y0 >= my1 + 1 and y1 - y0 <= 7 and len(pts) <= 100:
            continue
        cx=(x0+x1)/2
        if len(pts)>=5 and mx0-18<=cx<=mx1+18 and y0<=my1+10 and y1>=my0-10:
            keep.update(pts)
    out=Image.new("RGBA",cell.size,(0,0,0,0)); src,dst=cell.load(),out.load()
    for x,y in keep: dst[x,y]=src[x,y]
    return out


def stable_canvas(cleaned: Image.Image) -> Image.Image:
    bbox=cleaned.getbbox()
    if not bbox: raise RuntimeError("empty recovered frame")
    sprite=cleaned.crop(bbox); canvas=Image.new("RGBA",(256,256),(0,0,0,0))
    if sprite.width>244 or sprite.height>244:
        sprite.thumbnail((244,244),Image.Resampling.LANCZOS)
    canvas.alpha_composite(sprite,((256-sprite.width)//2,min(244-sprite.height,(256-sprite.height)//2)))
    return canvas


def strip_preview_caption(canvas: Image.Image) -> Image.Image:
    """Remove a caption that touched an exhaust flare and joined the main alpha component."""
    alpha = canvas.getchannel("A")
    counts = [sum(alpha.getpixel((x, y)) > 8 for x in range(canvas.width))
              for y in range(canvas.height)]
    for y in range(int(canvas.height * 0.72), canvas.height):
        if counts[y] > 110 and counts[y - 1] < 80:
            out = canvas.copy()
            px = out.load()
            for yy in range(y, out.height):
                for x in range(out.width):
                    px[x, yy] = (0, 0, 0, 0)
            return out
    return canvas


def clear_checker(frame: Image.Image) -> Image.Image:
    rgba=frame.convert("RGBA"); colors=Counter(rgba.getdata())
    checker={px for px,count in colors.most_common(10) if count>1000}
    pix=rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if pix[x,y] in checker: pix[x,y]=(0,0,0,0)
    return rgba


def recover(stage: int, spec: dict) -> None:
    out=ROOT/"assets"/"game"/f"stage{stage}_enemy_attacks"
    elite_out=ROOT/"assets"/"game"/f"stage{stage}_{spec['elite_name']}"
    proof=ROOT/"_BUILD_SOURCE"/f"stage{stage}_enemy_redesign"
    out.mkdir(parents=True,exist_ok=True); elite_out.mkdir(parents=True,exist_ok=True)
    proof.mkdir(parents=True,exist_ok=True)
    src=Image.open(spec["source"]); frames=[]
    for i in range(src.n_frames): src.seek(i); frames.append(src.convert("RGBA"))
    contact=Image.new("RGBA",(4*280,3*270),(6,10,24,255)); draw=ImageDraw.Draw(contact)
    for idx,name in enumerate(spec["names"]):
        col,row=idx%4,idx//4; unit_out=out/name; unit_out.mkdir(parents=True,exist_ok=True)
        recovered=[]
        for fi,frame in enumerate(frames):
            cell=frame.crop((col*256,row*256,col*256+256,row*256+202))
            canvas=stable_canvas(keep_hull(edge_clear(cell)))
            if stage == 9:
                canvas = strip_preview_caption(canvas)
            canvas.save(unit_out/f"{fi+1:02d}.png",optimize=True); recovered.append(canvas)
        thumb=recovered[3].copy(); thumb.thumbnail((228,220),Image.Resampling.NEAREST)
        contact.alpha_composite(thumb,(col*280+(280-thumb.width)//2,row*270+4+(220-thumb.height)//2))
        draw.text((col*280+10,row*270+236),name.upper(),fill=spec["label"])
    contact.save(proof/f"stage{stage}_recovered_roster.png")
    elite=Image.open(spec["elite"]); strip=Image.new("RGBA",(12*128,128),(6,10,24,255))
    for fi in range(elite.n_frames):
        elite.seek(fi); cleaned=clear_checker(elite.convert("RGBA"))
        cleaned.save(elite_out/f"{fi+1:02d}.png",optimize=True)
        thumb=cleaned.copy(); thumb.thumbnail((120,120),Image.Resampling.NEAREST)
        strip.alpha_composite(thumb,(fi*128+(128-thumb.width)//2,(128-thumb.height)//2))
    strip.save(proof/f"stage{stage}_{spec['elite_name']}_strip.png")


if __name__ == "__main__":
    for stage,spec in STAGES.items(): recover(stage,spec)
