from __future__ import annotations

from collections import deque
from pathlib import Path
import math

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "game" / "stage4_warfare"
PROOF_DIR = ROOT / "docs" / "proofs"

BOSS_SOURCE = SRC_DIR / "storm_sovereign_mk2_generated.png"
DRONE_SOURCE = SRC_DIR / "chaingun_drone_parts_generated.png"
SHIELD_SOURCE = SRC_DIR / "storm_sovereign_lightning_shield_generated.png"
LIGHTNING_BALL_SOURCE = SRC_DIR / "storm_sovereign_lightning_ball_generated.png"
CHAINGUN_ROTATE_SOURCE = SRC_DIR / "storm_sovereign_chaingun_fullrotate_generated.png"
CHAINGUN_CORE_SOURCE = SRC_DIR / "storm_sovereign_chaingun_core_generated.png"
LIGHTNING_MG_SOURCE = SRC_DIR / "storm_sovereign_lightning_mg_generated.png"
NODE_TELEPORT_SOURCE = SRC_DIR / "storm_sovereign_node_teleport_generated.png"
HELPER_CORE_LEFT_SOURCE = SRC_DIR / "storm_sovereign_helper_core_left_ref.png"
HELPER_CORE_RIGHT_SOURCE = SRC_DIR / "storm_sovereign_helper_core_right_ref.png"

CYAN = (38, 220, 255, 255)
ICE = (193, 251, 255, 255)
BLUE = (37, 103, 255, 255)
ROYAL = (17, 52, 145, 255)
STEEL = (105, 126, 153, 255)
DARK = (2, 7, 18, 255)
GOLD = (255, 207, 47, 255)
WHITE = (255, 255, 245, 255)


def remove_connected_light_background(source: Image.Image) -> Image.Image:
    """Remove only the pale checkerboard connected to the canvas edge."""
    rgb = source.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def background(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return min(r, g, b) >= 205 and max(r, g, b) - min(r, g, b) <= 18

    for x in range(width):
        if background(x, 0): queue.append((x, 0))
        if background(x, height - 1): queue.append((x, height - 1))
    for y in range(height):
        if background(0, y): queue.append((0, y))
        if background(width - 1, y): queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        idx = y * width + x
        if seen[idx] or not background(x, y):
            continue
        seen[idx] = 1
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))

    out = source.convert("RGBA")
    alpha = out.getchannel("A")
    ap = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if seen[row + x]:
                ap[x, y] = 0
    out.putalpha(alpha)
    return out


def remove_connected_helper_background(source: Image.Image) -> Image.Image:
    """Remove only the dark checker connected to the edge of the supplied socket crops.

    The gun hole and outline are darker than the checker, so a narrow achromatic range preserves
    both while deleting the 24/38 RGB background cells. Internal metal of the same value remains
    safe because it is enclosed by the black outline and cannot join the edge flood.
    """
    rgb = source.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def background(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        return 20 <= r <= 45 and max(r, g, b) - min(r, g, b) <= 2

    for x in range(width):
        if background(x, 0): queue.append((x, 0))
        if background(x, height - 1): queue.append((x, height - 1))
    for y in range(height):
        if background(0, y): queue.append((0, y))
        if background(width - 1, y): queue.append((width - 1, y))
    while queue:
        x, y = queue.popleft()
        idx = y * width + x
        if seen[idx] or not background(x, y):
            continue
        seen[idx] = 1
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))
    out = source.convert("RGBA")
    alpha = out.getchannel("A")
    ap = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if seen[row + x]:
                ap[x, y] = 0
    out.putalpha(alpha)
    return out


def trim(image: Image.Image, pad: int = 0) -> Image.Image:
    box = image.getchannel("A").getbbox()
    if not box:
        return Image.new("RGBA", (1, 1))
    x0, y0, x1, y1 = box
    return image.crop((max(0, x0 - pad), max(0, y0 - pad), min(image.width, x1 + pad), min(image.height, y1 + pad)))


def keep_largest_alpha_component(image: Image.Image) -> Image.Image:
    """Keep the connected primary hull and discard isolated generation flecks/remnant fins."""
    width, height = image.size
    alpha = image.getchannel("A")
    ap = alpha.load()
    seen = bytearray(width * height)
    best: list[int] = []
    for sy in range(height):
        for sx in range(width):
            start = sy * width + sx
            if seen[start] or ap[sx, sy] <= 8:
                continue
            queue = deque([(sx, sy)])
            component: list[int] = []
            while queue:
                x, y = queue.popleft()
                idx = y * width + x
                if seen[idx] or ap[x, y] <= 8:
                    continue
                seen[idx] = 1
                component.append(idx)
                if x: queue.append((x - 1, y))
                if x + 1 < width: queue.append((x + 1, y))
                if y: queue.append((x, y - 1))
                if y + 1 < height: queue.append((x, y + 1))
            if len(component) > len(best):
                best = component
    keep = bytearray(width * height)
    for idx in best:
        keep[idx] = 1
    out = image.copy()
    oa = out.getchannel("A")
    oap = oa.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if not keep[row + x]:
                oap[x, y] = 0
    out.putalpha(oa)
    return out


def fit_canvas(image: Image.Image, size: tuple[int, int], margin: int) -> Image.Image:
    image = trim(image, 2)
    scale = min((size[0] - margin * 2) / image.width, (size[1] - margin * 2) / image.height)
    dims = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    image = image.resize(dims, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size)
    canvas.alpha_composite(image, ((size[0] - dims[0]) // 2, (size[1] - dims[1]) // 2))
    return canvas


def rotate_stable(image: Image.Image, angle: float, scale_x: float = 1.0) -> Image.Image:
    transformed = image.rotate(angle, Image.Resampling.BICUBIC, expand=False)
    if abs(scale_x - 1.0) > 0.001:
        w = max(1, round(image.width * scale_x))
        transformed = transformed.resize((w, image.height), Image.Resampling.BICUBIC)
        fixed = Image.new("RGBA", image.size)
        fixed.alpha_composite(transformed, ((image.width - w) // 2, 0))
        transformed = fixed
    return transformed


def generated_rgba(path: Path) -> Image.Image:
    """Honor real generated alpha and remove only an edge-connected pale checker otherwise."""
    source = Image.open(path)
    if source.mode == "RGBA" and source.getchannel("A").getextrema()[0] < 250:
        return source
    return remove_connected_light_background(source)


def normalize_generated_strip(path: Path, cols: int, rows: int,
                              size: tuple[int, int], margin: int,
                              primary_component: bool = False) -> list[Image.Image]:
    """Split a generated sheet with one shared scale and one stable center anchor.

    A whole-strip generation pass preserves the authored axial rotation.  Shared scaling here
    prevents the game-sized weapon from breathing as the upper housing turns through profile.
    """
    source = generated_rgba(path)
    slot_w, slot_h = source.width / cols, source.height / rows
    trimmed: list[Image.Image] = []
    for index in range(cols * rows):
        col, row = index % cols, index // cols
        box = (round(col * slot_w), round(row * slot_h),
               round((col + 1) * slot_w), round((row + 1) * slot_h))
        sprite = source.crop(box)
        if primary_component:
            sprite = keep_largest_alpha_component(sprite)
        trimmed.append(trim(sprite, 1))
    max_w = max(frame.width for frame in trimmed)
    max_h = max(frame.height for frame in trimmed)
    scale = min((size[0] - margin * 2) / max_w, (size[1] - margin * 2) / max_h)
    out: list[Image.Image] = []
    for frame in trimmed:
        dims = (max(1, round(frame.width * scale)), max(1, round(frame.height * scale)))
        frame = frame.resize(dims, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size)
        canvas.alpha_composite(frame, ((size[0] - dims[0]) // 2, (size[1] - dims[1]) // 2))
        out.append(canvas)
    return out


def alpha_clip_overlay(base: Image.Image, overlay: Image.Image) -> Image.Image:
    mask = ImageChops.multiply(overlay.getchannel("A"), base.getchannel("A"))
    overlay.putalpha(mask)
    out = base.copy()
    out.alpha_composite(overlay)
    return out


def charged_frame(base: Image.Image, frame: int, count: int = 12) -> Image.Image:
    q = frame / max(1, count - 1)
    overlay = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(overlay)
    cx, cy = base.width // 2, round(base.height * 0.52)
    phase = frame % 4
    # Internal reactor ladder. All lighting is clipped to the hull alpha; no halo is created.
    for i in range(11):
        fy = round(base.height * (0.72 - i * 0.044))
        on = max(0.0, min(1.0, q * 1.42 - i * 0.075))
        if on <= 0:
            continue
        width = 7 + ((i + phase) & 1) * 4
        color = (92, 228, 255, round(80 + 160 * on))
        draw.rectangle((cx - width, fy - 3, cx + width, fy + 3), fill=color)
    for side in (-1, 1):
        for i in range(6):
            x = cx + side * round(base.width * (0.10 + i * 0.038))
            y = round(base.height * (0.60 - i * 0.035))
            on = max(0.0, min(1.0, q * 1.55 - i * 0.13))
            if on:
                draw.rectangle((x - 4, y - 4, x + 4, y + 4), fill=(40, 172, 255, round(70 + 170 * on)))
    radius = round(9 + q * 24 + math.sin(frame * math.pi / 2) * 2)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(96, 233, 255, round(60 + q * 150)))
    draw.ellipse((cx - radius // 2, cy - radius // 2, cx + radius // 2, cy + radius // 2), fill=(235, 255, 255, round(120 + q * 120)))
    return alpha_clip_overlay(base, overlay)


def isolate_hull_and_power_node(cleaned: Image.Image) -> tuple[Image.Image, Image.Image]:
    """Detach the four disconnected generator pods and remove their small side fins.

    The generated composition has four deliberately identical circles around one connected hull.
    Normalized rectangles are used rather than a color key, so no blue hull pixels are lost.
    """
    w, h = cleaned.size
    boxes = [
        (round(w * .145), round(h * .070), round(w * .335), round(h * .245)),
        (round(w * .680), round(h * .070), round(w * .875), round(h * .245)),
        (round(w * .145), round(h * .635), round(w * .335), round(h * .805)),
        (round(w * .680), round(h * .635), round(w * .875), round(h * .805)),
    ]
    hull = cleaned.copy()
    for box in boxes:
        ImageDraw.Draw(hull).rectangle(box, fill=(0, 0, 0, 0))

    node = trim(cleaned.crop(boxes[0]), 2)
    nw, nh = node.size
    shape = Image.new("L", node.size)
    draw = ImageDraw.Draw(shape)
    cx = nw / 2
    radius = min(nw * .355, nh * .39)
    cy = nh * .36
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=255)
    # Keep the armored lower control block, while the two lateral winglets remain outside.
    draw.rounded_rectangle((cx - nw * .29, nh * .33, cx + nw * .29, nh * .91),
                           radius=max(2, round(nh * .12)), fill=255)
    node.putalpha(ImageChops.multiply(node.getchannel("A"), shape))
    node = fit_canvas(trim(node), (160, 160), 8)
    return keep_largest_alpha_component(hull), node


def energized_frame(base: Image.Image, frame: int, count: int = 12) -> Image.Image:
    """Animate only existing cyan/blue hull pixels—no exterior halo or silhouette drift."""
    out = base.copy()
    pixels = out.load()
    phase = frame * math.tau / count
    for y in range(out.height):
        band = .5 + .5 * math.sin((y / out.height) * math.tau * 5.0 - phase)
        for x in range(out.width):
            r, g, b, a = pixels[x, y]
            if not a or b < 92 or b < r * 1.12:
                continue
            side = .5 + .5 * math.sin((x / out.width) * math.tau * 3.0 + phase * 1.37)
            pulse = .28 + .72 * band * side
            pixels[x, y] = (
                min(255, round(r + 28 * pulse)),
                min(255, round(g + 92 * pulse)),
                min(255, round(b + 58 * pulse)),
                a,
            )
    return out


def open_chaingun_socket_apertures(core: Image.Image) -> Image.Image:
    """Make the two authored black socket interiors true apertures.

    The generated core already contains the correct blue armored rims.  Only the narrow black
    interiors are cleared here so a gun drawn behind the core remains visible through the hole,
    while the rim itself can mask the gun collar and sell the mechanical insertion.
    """
    out = core.copy()
    alpha = out.getchannel("A")
    mask = Image.new("L", out.size, 255)
    draw = ImageDraw.Draw(mask)
    # Normalized from the approved 224x224 core.  The sockets are deliberately tall and narrow.
    for cx in (20, 204):
        draw.ellipse((cx - 7, 112 - 22, cx + 7, 112 + 22), fill=0)
    out.putalpha(ImageChops.multiply(alpha, mask))
    return out


def save_power_node_frames(node: Image.Image) -> None:
    node.save(OUT_DIR / "s4w_power_node.png")
    for frame in range(16):
        angle = -frame * 360 / 16
        spun = node.rotate(angle, Image.Resampling.BICUBIC, expand=False)
        # A travelling internal cyan glint makes every 22.5-degree step readable at game scale.
        overlay = Image.new("RGBA", spun.size)
        draw = ImageDraw.Draw(overlay)
        a = frame * math.tau / 16
        cx = spun.width / 2 + math.cos(a) * spun.width * .20
        cy = spun.height / 2 + math.sin(a) * spun.height * .20
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(210, 255, 255, 150))
        alpha_clip_overlay(spun, overlay).save(OUT_DIR / f"s4w_power_node_{frame:02d}.png")


def save_generated_shield_frames() -> Image.Image:
    source = remove_connected_light_background(Image.open(SHIELD_SOURCE))
    shield = fit_canvas(source, (512, 512), 6)
    px = shield.load()
    cx, cy = shield.width / 2, shield.height / 2
    max_r = min(cx, cy)
    # The generated sphere is intentionally vivid; turn its center into a translucent field while
    # retaining the strong lightning rim and white electrical junctions.
    for y in range(shield.height):
        for x in range(shield.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            dist = math.hypot(x - cx, y - cy) / max_r
            white = max(0.0, min(1.0, (min(r, g, b) - 120) / 135))
            rim = max(0.0, min(1.0, (dist - .58) / .34))
            alpha_mul = .10 + .50 * rim + .34 * white
            px[x, y] = (r, g, b, max(4, min(255, round(a * alpha_mul))))
    for frame in range(12):
        shield.rotate(-frame * 30, Image.Resampling.BICUBIC, expand=False).save(
            OUT_DIR / f"s4w_lightning_shield_{frame:02d}.png")
    return shield


def save_generated_lightning_ball_frames() -> Image.Image:
    source = Image.open(LIGHTNING_BALL_SOURCE).convert("RGBA")
    ball = fit_canvas(source, (160, 160), 5)
    for frame in range(16):
        ball.rotate(-frame * 360 / 16, Image.Resampling.BICUBIC, expand=False).save(
            OUT_DIR / f"s4w_lightning_ball_{frame:02d}.png")
    return ball


def save_final_phase_assets() -> tuple[Image.Image, Image.Image]:
    """Normalize the generated 25% HP twin-chaingun and shield-redeployment kit."""
    guns = normalize_generated_strip(CHAINGUN_ROTATE_SOURCE, 8, 1, (128, 192), 5, True)
    for frame, image in enumerate(guns):
        image.save(OUT_DIR / f"s4w_final_chaingun_{frame:02d}.png")

    core = fit_canvas(generated_rgba(CHAINGUN_CORE_SOURCE), (224, 224), 4)
    core = open_chaingun_socket_apertures(core)
    core.save(OUT_DIR / "s4w_final_chaingun_core.png")
    # The core is a mounted reactor rather than a static sticker: only existing energized pixels
    # pulse, so its silhouette and the two gun sockets never drift.
    for frame in range(8):
        energized_frame(core, frame, 8).save(OUT_DIR / f"s4w_final_chaingun_core_{frame:02d}.png")

    rounds = normalize_generated_strip(LIGHTNING_MG_SOURCE, 8, 1, (48, 80), 3, True)
    for frame, image in enumerate(rounds):
        image.save(OUT_DIR / f"s4w_lightning_mg_round_{frame:02d}.png")

    teleports = normalize_generated_strip(NODE_TELEPORT_SOURCE, 4, 3, (176, 176), 3)
    for frame, image in enumerate(teleports):
        image.save(OUT_DIR / f"s4w_node_teleport_{frame:02d}.png")
    return core, guns[0]


def prepare_helper_core(path: Path, side: int) -> Image.Image:
    """Normalize one user-supplied socket pod and open its gun aperture."""
    source = remove_connected_helper_background(Image.open(path))
    alpha = source.getchannel("A")
    mask = Image.new("L", source.size, 255)
    draw = ImageDraw.Draw(mask)
    if side < 0:
        cx, cy, rx, ry = source.width * .55, source.height * .58, source.width * .115, source.height * .19
    else:
        cx, cy, rx, ry = source.width * .47, source.height * .53, source.width * .105, source.height * .17
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=0)
    source.putalpha(ImageChops.multiply(alpha, mask))
    return fit_canvas(trim(source, 1), (128, 128), 5)


def save_helper_core_assets() -> tuple[Image.Image, Image.Image]:
    left = prepare_helper_core(HELPER_CORE_LEFT_SOURCE, -1)
    right = prepare_helper_core(HELPER_CORE_RIGHT_SOURCE, 1)
    for name, core in (("left", left), ("right", right)):
        core.save(OUT_DIR / f"s4w_helper_core_{name}.png")
        for frame in range(8):
            energized_frame(core, frame, 8).save(OUT_DIR / f"s4w_helper_core_{name}_{frame:02d}.png")
    return left, right


def helper_overheat_palette(image: Image.Image, frame: int) -> Image.Image:
    """Palette-swap blue energy into a red/orange heat state without changing silhouette."""
    source = image.convert("RGBA")
    out = Image.new("RGBA", source.size)
    src, dst = source.load(), out.load()
    pulse = .82 + .18 * math.sin(frame / 8 * math.tau)
    for y in range(source.height):
        for x in range(source.width):
            r, g, b, a = src[x, y]
            if not a:
                continue
            lum = (r * 3 + g * 5 + b * 2) / 10
            if b > r * 1.08 or g > r * 1.22:
                target = (255, min(235, round(32 + lum * .76)), min(72, round(lum * .15)))
                mix = .78 * pulse
            else:
                target = (min(255, round(lum * 1.12 + 54)), min(185, round(lum * .58 + 14)),
                          min(105, round(lum * .26 + 6)))
                mix = .20 * pulse
            dst[x, y] = tuple(round(c * (1 - mix) + target[i] * mix) for i, c in enumerate((r, g, b))) + (a,)
    return out


def save_locked_dual_helper_assets() -> None:
    """Bake the user-approved south-facing dual socket as one stable 8-frame unit.

    Every frame uses the identical silhouette and anchor.  Only reel/specular pixels and the
    internal core energy pulse change; neither gun nor the plate rotates or gimbals.
    """
    for frame in range(8):
        core = Image.open(OUT_DIR / f"s4w_final_chaingun_core_{frame:02d}.png")
        gun = Image.open(OUT_DIR / f"s4w_final_chaingun_{frame:02d}.png")
        assembly = Image.new("RGBA", (160, 160))
        composite_socketed_assembly(assembly, core, gun, (80, 70), 96, (44, 68),
                                    (math.pi / 2, math.pi / 2))
        assembly.save(OUT_DIR / f"s4w_helper_dual_{frame:02d}.png")
        helper_overheat_palette(assembly, frame).save(OUT_DIR / f"s4w_helper_dual_hot_{frame:02d}.png")


def save_boss_frames() -> tuple[Image.Image, Image.Image]:
    raw = Image.open(BOSS_SOURCE)
    cleaned = remove_connected_light_background(raw)
    hull, node = isolate_hull_and_power_node(cleaned)
    base = fit_canvas(hull, (512, 512), 18)
    base.save(OUT_DIR / "s4w_boss_idle.png")
    angles = (0, -2, -5, -8, -5, -2, 0, 2, 5, 8, 5, 2)
    for i, angle in enumerate(angles):
        frame = rotate_stable(base, angle, 1.0 - abs(angle) * 0.0025)
        frame.save(OUT_DIR / f"s4w_boss_flight_{i:02d}.png")
    for i in range(12):
        charged_frame(base, i).save(OUT_DIR / f"s4w_boss_charge_{i:02d}.png")
        energized_frame(base, i).save(OUT_DIR / f"s4w_boss_energized_{i:02d}.png")
    save_power_node_frames(node)
    return base, node


def split_drone_parts() -> tuple[Image.Image, Image.Image]:
    sheet = Image.open(DRONE_SOURCE).convert("RGBA")
    left = trim(sheet.crop((0, 0, sheet.width // 2, sheet.height)), 4)
    right = trim(sheet.crop((sheet.width // 2, 0, sheet.width, sheet.height)), 4)
    body = fit_canvas(left, (160, 160), 8)
    barrel = fit_canvas(right, (96, 128), 4)
    body.save(OUT_DIR / "s4w_drone_body.png")
    barrel.save(OUT_DIR / "s4w_drone_barrel.png")
    # Rotary motion is represented by travelling specular/cyan highlights across the distinct tubes.
    for frame in range(8):
        out = barrel.copy()
        overlay = Image.new("RGBA", barrel.size)
        draw = ImageDraw.Draw(overlay)
        for lane in range(5):
            bright = ((lane - frame) % 5) == 0
            x = round(barrel.width * (0.31 + lane * 0.095))
            draw.rectangle((x - 2, 36, x + 2, 91), fill=(210, 249, 255, 105 if bright else 18))
        muzzle_phase = frame % 4
        for lane in range(5):
            ang = -math.pi / 2 + lane * math.tau / 5 + muzzle_phase * math.tau / 20
            x = barrel.width / 2 + math.cos(ang) * 13
            y = barrel.height * 0.80 + math.sin(ang) * 7
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(105, 234, 255, 150))
        alpha_clip_overlay(out, overlay).save(OUT_DIR / f"s4w_drone_barrel_{frame:02d}.png")
    return body, barrel


def transparent(size: tuple[int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", size)
    return image, ImageDraw.Draw(image)


def polygon(draw: ImageDraw.ImageDraw, points, fill):
    draw.polygon([(round(x), round(y)) for x, y in points], fill=fill)


def save_mg_rounds() -> None:
    for frame in range(6):
        image, draw = transparent((40, 64))
        pulse = frame % 3
        polygon(draw, [(20, 2), (28, 14), (26, 48), (20, 62), (14, 48), (12, 14)], DARK)
        polygon(draw, [(20, 7), (25, 16), (23, 46), (20, 56), (17, 46), (15, 16)], GOLD)
        draw.rectangle((18, 10 + pulse * 2, 22, 47 - pulse), fill=WHITE)
        draw.rectangle((16, 48, 24, 54), fill=BLUE)
        image.save(OUT_DIR / f"s4w_mg_round_{frame:02d}.png")

    for frame in range(8):
        image, draw = transparent((56, 72))
        phase = frame * math.tau / 8
        polygon(draw, [(28, 2), (40, 16), (37, 55), (28, 70), (19, 55), (16, 16)], DARK)
        polygon(draw, [(28, 7), (36, 18), (33, 51), (28, 63), (23, 51), (20, 18)], BLUE)
        draw.rectangle((25, 13, 31, 54), fill=ICE)
        for s in (-1, 1):
            y = 31 + round(math.sin(phase + s) * 7)
            polygon(draw, [(28 + s * 5, y - 7), (28 + s * 14, y), (28 + s * 5, y + 7)], CYAN)
        image.save(OUT_DIR / f"s4w_spread_round_{frame:02d}.png")


def save_orb_and_lightning() -> None:
    for frame in range(12):
        image, draw = transparent((96, 96))
        cx = cy = 48
        draw.ellipse((18, 18, 78, 78), fill=DARK)
        draw.ellipse((23, 23, 73, 73), fill=ROYAL)
        draw.ellipse((31, 31, 65, 65), fill=(9, 23, 62, 255))
        draw.ellipse((39, 39, 57, 57), fill=ICE)
        phase = frame * math.tau / 12
        for arm in range(4):
            a = phase + arm * math.tau / 4
            pts = []
            for k, radius in enumerate((13, 21, 30, 39)):
                jitter = (-1 if k & 1 else 1) * 0.10
                pts.append((cx + math.cos(a + jitter) * radius, cy + math.sin(a + jitter) * radius))
            draw.line(pts, fill=CYAN, width=4)
            draw.line(pts, fill=WHITE, width=1)
        image.save(OUT_DIR / f"s4w_lightning_orb_{frame:02d}.png")

    for frame in range(8):
        image, draw = transparent((72, 112))
        phase = frame * 0.9
        points = [(36, 2)]
        for i in range(1, 9):
            y = 2 + i * 13
            x = 36 + math.sin(phase + i * 1.7) * (7 + (i % 3) * 2)
            points.append((round(x), y))
        draw.line(points, fill=DARK, width=12, joint="curve")
        draw.line(points, fill=BLUE, width=8, joint="curve")
        draw.line(points, fill=CYAN, width=4, joint="curve")
        draw.line(points, fill=WHITE, width=1, joint="curve")
        image.save(OUT_DIR / f"s4w_lightning_lance_{frame:02d}.png")


def save_muzzle_family(name: str, palette: tuple[tuple[int, int, int, int], ...], frames: int = 8) -> None:
    for frame in range(frames):
        image, draw = transparent((96, 96))
        q = (frame + 1) / frames
        cx, cy = 48, 28
        length = round(18 + math.sin(q * math.pi) * 54)
        width = round(5 + math.sin(q * math.pi) * 19)
        polygon(draw, [(cx, cy - 8), (cx + width, cy + length * .30), (cx + 8, cy + length),
                       (cx, cy + length * .72), (cx - 8, cy + length), (cx - width, cy + length * .30)], palette[0])
        polygon(draw, [(cx, cy - 4), (cx + width * .55, cy + length * .24), (cx + 3, cy + length * .78),
                       (cx, cy + length * .58), (cx - 3, cy + length * .78), (cx - width * .55, cy + length * .24)], palette[1])
        draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=palette[2])
        image.save(OUT_DIR / f"s4w_muzzle_{name}_{frame:02d}.png")


def composite_center(canvas: Image.Image, sprite: Image.Image, center: tuple[int, int], size: tuple[int, int] | None = None) -> None:
    if size:
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
    canvas.alpha_composite(sprite, (round(center[0] - sprite.width / 2), round(center[1] - sprite.height / 2)))


def composite_socketed_gun(canvas: Image.Image, gun: Image.Image, socket: tuple[float, float],
                           size: tuple[int, int], angle: float) -> None:
    """Rotate a complete chaingun around the collar seated inside one socket."""
    gun = gun.resize(size, Image.Resampling.LANCZOS)
    diameter = max(size) * 3
    plate = Image.new("RGBA", (diameter, diameter))
    pivot = diameter // 2
    # The approved strip points down.  Its upper housing is buried slightly into the socket so
    # the core rim, composited afterwards, clips it like a real gimbal collar.
    plate.alpha_composite(gun, (round(pivot - size[0] / 2), round(pivot - size[1] * .11)))
    plate = plate.rotate(-math.degrees(angle - math.pi / 2), Image.Resampling.BICUBIC, expand=False)
    canvas.alpha_composite(plate, (round(socket[0] - pivot), round(socket[1] - pivot)))


def composite_socketed_assembly(canvas: Image.Image, core: Image.Image, gun: Image.Image,
                                center: tuple[float, float], core_size: int,
                                gun_size: tuple[int, int], angles: tuple[float, float]) -> None:
    """Draw guns behind the blue rims, but through the transparent socket apertures."""
    offset = 92 / 224 * core_size
    for side, angle in zip((-1, 1), angles):
        composite_socketed_gun(canvas, gun, (center[0] + side * offset, center[1]), gun_size, angle)
    composite_center(canvas, core, (round(center[0]), round(center[1])), (core_size, core_size))


def rigid_socketed_plate(core: Image.Image, gun: Image.Image, core_size: int,
                         gun_size: tuple[int, int], turn: float, dual: bool) -> Image.Image:
    """Build one rigid unit, then rotate that complete unit around its centre.

    The gun housings never gimbal around their socket holes.  Frame changes on ``gun`` are only
    internal reel/specular animation; their collars, bodies and aim remain bolted to the plate.
    """
    diameter = math.ceil(max(core_size + gun_size[0] * 2, core_size + gun_size[1] * 2) * 1.18)
    diameter += diameter & 1
    plate = Image.new("RGBA", (diameter, diameter))
    center = (diameter / 2, diameter / 2)
    if dual:
        composite_socketed_assembly(plate, core, gun, center, core_size, gun_size,
                                    (math.pi / 2, math.pi / 2))
    else:
        composite_socketed_gun(plate, gun, center, gun_size, math.pi / 2)
        composite_center(plate, core, (round(center[0]), round(center[1])), (core_size, core_size))
    return plate.rotate(-math.degrees(turn), Image.Resampling.BICUBIC, expand=False)


def build_socketed_chaingun_preview(bg: Image.Image) -> None:
    """Proof that the approved dual-socket piece remains locked while its reels animate."""
    frames: list[Image.Image] = []
    for index in range(48):
        frame = bg.copy()
        shade = Image.new("RGBA", frame.size, (1, 5, 16, 92))
        frame.alpha_composite(shade)
        assembly = Image.open(OUT_DIR / f"s4w_helper_dual_{index % 8:02d}.png")
        composite_center(frame, assembly, (400, 285), (220, 220))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    for name in ("stage4_dual_socket_locked_preview.gif", "stage4_dual_socket_360_preview.gif"):
        frames[0].save(PROOF_DIR / name, save_all=True, append_images=frames[1:],
                       duration=55, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1440, 650), (7, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 20), "STORM SOVEREIGN - LOCKED DUAL SOCKET / REELS SPIN + FIRE",
              fill=(226, 244, 255, 255))
    for column, frame_index in enumerate((0, 2, 4, 6)):
        center = (180 + column * 360, 300)
        assembly = Image.open(OUT_DIR / f"s4w_helper_dual_{frame_index:02d}.png")
        composite_center(sheet, assembly, center, (205, 205))
        label = f"LOCKED SOUTH - INTERNAL REEL FRAME {frame_index}"
        box = draw.textbbox((0, 0), label)
        draw.text((center[0] - (box[2] - box[0]) / 2, 540), label, fill=(126, 231, 255, 255))
    sheet.save(PROOF_DIR / "stage4_dual_socket_locked_contact_sheet.png")
    sheet.save(PROOF_DIR / "stage4_dual_socket_360_contact_sheet.png")


def build_side_helper_preview(bg: Image.Image) -> None:
    """Preview two destructible copies of the same locked dual-chaingun helper."""
    frames: list[Image.Image] = []
    centers = ((190, 290), (610, 290))
    for index in range(64):
        frame = bg.copy()
        frame.alpha_composite(Image.new("RGBA", frame.size, (1, 5, 16, 104)))
        assembly = Image.open(OUT_DIR / f"s4w_helper_dual_{index % 8:02d}.png")
        for center in centers:
            composite_center(frame, assembly, center, (132, 132))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    frames[0].save(PROOF_DIR / "stage4_side_core_helpers_360_preview.gif", save_all=True,
                   append_images=frames[1:], duration=48, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1280, 700), (7, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "50% HP SIDE HELPERS - LOCKED SOUTH / DUAL REELS SPIN + FIRE",
              fill=(226, 244, 255, 255))
    for column, frame_index in enumerate((0, 2, 4, 6)):
        center = (160 + column * 320, 320)
        assembly = Image.open(OUT_DIR / f"s4w_helper_dual_{frame_index:02d}.png")
        composite_center(sheet, assembly, center, (150, 150))
        label = f"LOCKED SOUTH - REEL FRAME {frame_index}"
        box = draw.textbbox((0, 0), label)
        draw.text((center[0] - (box[2] - box[0]) / 2, 555), label, fill=(126, 231, 255, 255))
    sheet.save(PROOF_DIR / "stage4_side_core_helpers_contact_sheet.png")


def build_helper_heat_preview(bg: Image.Image) -> None:
    """Show the authored wind-up/fire/overheat/cooldown readability cycle."""
    frames: list[Image.Image] = []
    for index in range(64):
        frame = bg.copy()
        frame.alpha_composite(Image.new("RGBA", frame.size, (1, 5, 16, 108)))
        q = index / 63
        reel = round((q * q * 36 if q < .28 else q * 96)) % 8
        base = Image.open(OUT_DIR / f"s4w_helper_dual_{reel:02d}.png")
        hot = Image.open(OUT_DIR / f"s4w_helper_dual_hot_{reel:02d}.png")
        if q < .58:
            heat = max(0.0, (q - .28) / .30 * .34)
        elif q < .76:
            heat = .34 + (q - .58) / .18 * .66
        else:
            heat = max(0.0, 1 - (q - .76) / .24)
        sprite = Image.blend(base, hot, heat)
        composite_center(frame, sprite, (400, 290), (220, 220))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    frames[0].save(PROOF_DIR / "stage4_dual_helper_heat_cycle.gif", save_all=True,
                   append_images=frames[1:], duration=55, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1280, 700), (7, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "DUAL CHAINGUN HELPER - WIND-UP / FIRE / VULNERABLE OVERHEAT / RECOVER",
              fill=(226, 244, 255, 255))
    entries = ((0, 0.0, "WIND-UP - REELS ACCELERATE"),
               (3, .28, "FIRING - LOCKED BLUE"),
               (6, 1.0, "OVERHEAT - VULNERABLE"),
               (1, .48, "COOLING - HEAT FALLS"))
    for column, (frame_index, heat, label) in enumerate(entries):
        center = (160 + column * 320, 320)
        base = Image.open(OUT_DIR / f"s4w_helper_dual_{frame_index:02d}.png")
        hot = Image.open(OUT_DIR / f"s4w_helper_dual_hot_{frame_index:02d}.png")
        composite_center(sheet, Image.blend(base, hot, heat), center, (180, 180))
        box = draw.textbbox((0, 0), label)
        draw.text((center[0] - (box[2] - box[0]) / 2, 555), label, fill=(126, 231, 255, 255))
    sheet.save(PROOF_DIR / "stage4_dual_helper_heat_contact_sheet.png")


def build_preview(base: Image.Image, drone: Image.Image) -> None:
    bg_path = ROOT / "assets" / "game" / "stage4.png"
    bg = Image.open(bg_path).convert("RGB") if bg_path.exists() else Image.new("RGB", (800, 600), (29, 33, 39))
    bg = bg.resize((800, 600), Image.Resampling.LANCZOS).convert("RGBA")
    shade = Image.new("RGBA", bg.size, (3, 8, 18, 72))
    bg.alpha_composite(shade)
    frames = []
    for index in range(24):
        frame = bg.copy()
        charge = 8 <= index < 17
        bank = round(math.sin(index * math.tau / 24) * 7)
        boss = charged_frame(base, min(11, max(0, (index - 8) * 2))) if charge else rotate_stable(base, bank)
        composite_center(frame, boss, (400 + round(math.sin(index * math.tau / 24) * 80), 180), (300, 300))
        for side in (-1, 1):
            dx = 400 + side * 230 + round(math.sin(index * .38 + side) * 22)
            dy = 232 + round(math.cos(index * .32 + side) * 18)
            composite_center(frame, drone, (dx, dy), (94, 94))
            barrel = Image.open(OUT_DIR / f"s4w_drone_barrel_{index % 8:02d}.png")
            composite_center(frame, barrel, (dx, dy + 28), (44, 58))
            if index % 4 < 2:
                muzzle = Image.open(OUT_DIR / f"s4w_muzzle_mg_{index % 8:02d}.png")
                composite_center(frame, muzzle, (dx, dy + 68), (42, 42))
        if index >= 12:
            for lane in range(5):
                orb = Image.open(OUT_DIR / f"s4w_lightning_orb_{(index + lane * 2) % 12:02d}.png")
                composite_center(frame, orb, (180 + lane * 110, 350 + ((index * 17 + lane * 41) % 240)), (42, 42))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    preview = PROOF_DIR / "stage4_warfare_preview.gif"
    frames[0].save(preview, save_all=True, append_images=frames[1:], duration=75, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1050, 720), (7, 12, 22, 255))
    labels = ImageDraw.Draw(sheet)
    entries = [
        ("NEW STORM SOVEREIGN MK II", Image.open(OUT_DIR / "s4w_boss_idle.png"), (210, 235), (330, 330)),
        ("BANK LEFT", Image.open(OUT_DIR / "s4w_boss_flight_03.png"), (525, 170), (230, 230)),
        ("CORE CHARGE", Image.open(OUT_DIR / "s4w_boss_charge_11.png"), (820, 170), (230, 230)),
        ("CHAINGUN DRONE", drone, (525, 495), (145, 145)),
        ("SEPARATE ROTARY BARREL", Image.open(OUT_DIR / "s4w_drone_barrel_04.png"), (735, 495), (82, 110)),
        ("LIGHTNING ORB", Image.open(OUT_DIR / "s4w_lightning_orb_04.png"), (910, 490), (94, 94)),
    ]
    for label, sprite, center, dims in entries:
        composite_center(sheet, sprite, center, dims)
        box = labels.textbbox((0, 0), label)
        labels.text((center[0] - (box[2] - box[0]) / 2, center[1] + dims[1] / 2 + 12), label, fill=(226, 244, 255, 255))
    sheet.save(PROOF_DIR / "stage4_warfare_contact_sheet.png")


def build_shield_preview(base: Image.Image, node: Image.Image, shield: Image.Image, ball: Image.Image) -> None:
    bg_path = ROOT / "assets" / "game" / "stage4.png"
    bg = Image.open(bg_path).convert("RGB") if bg_path.exists() else Image.new("RGB", (800, 600), (24, 28, 34))
    bg = bg.resize((800, 600), Image.Resampling.LANCZOS).convert("RGBA")
    frames = []
    positions = ((150, 180), (650, 180), (150, 375), (650, 375))
    for index in range(32):
        frame = bg.copy()
        boss = energized_frame(base, index % 12)
        composite_center(frame, boss, (400, 255), (300, 300))
        if index < 24:
            sf = Image.open(OUT_DIR / f"s4w_lightning_shield_{index % 12:02d}.png")
            composite_center(frame, sf, (400, 250), (390, 390))
        alive = 4 if index < 10 else (3 if index < 14 else (2 if index < 18 else (1 if index < 22 else 0)))
        for ni, pos in enumerate(positions):
            if ni >= alive:
                continue
            pn = Image.open(OUT_DIR / f"s4w_power_node_{(index * 2 + ni * 3) % 16:02d}.png")
            composite_center(frame, pn, pos, (78, 78))
        if index >= 20:
            lb = Image.open(OUT_DIR / f"s4w_lightning_ball_{index % 16:02d}.png")
            composite_center(frame, lb, (400 + round(math.sin(index * .8) * 170), 350 + (index - 20) * 25), (70, 70))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    frames[0].save(PROOF_DIR / "stage4_storm_shield_preview.gif", save_all=True,
                   append_images=frames[1:], duration=75, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1120, 760), (7, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    entries = [
        ("ENERGIZED HULL", Image.open(OUT_DIR / "s4w_boss_energized_08.png"), (250, 260), (370, 370)),
        ("FINLESS POWER CIRCLE", Image.open(OUT_DIR / "s4w_power_node_04.png"), (620, 185), (170, 170)),
        ("POWER CIRCLE 180 DEG", Image.open(OUT_DIR / "s4w_power_node_12.png"), (860, 185), (170, 170)),
        ("GENERATED LIGHTNING SHIELD", Image.open(OUT_DIR / "s4w_lightning_shield_03.png"), (630, 510), (300, 300)),
        ("GENERATED LIGHTNING BALL", Image.open(OUT_DIR / "s4w_lightning_ball_06.png"), (930, 505), (160, 160)),
    ]
    for label, sprite, center, dims in entries:
        composite_center(sheet, sprite, center, dims)
        box = draw.textbbox((0, 0), label)
        draw.text((center[0] - (box[2] - box[0]) / 2, center[1] + dims[1] / 2 + 12), label,
                  fill=(226, 244, 255, 255))
    sheet.save(PROOF_DIR / "stage4_storm_shield_contact_sheet.png")


def build_rearm_preview(base: Image.Image) -> None:
    bg_path = ROOT / "assets" / "game" / "stage4.png"
    bg = Image.open(bg_path).convert("RGB") if bg_path.exists() else Image.new("RGB", (800, 600), (24, 28, 34))
    bg = bg.resize((800, 600), Image.Resampling.LANCZOS).convert("RGBA")
    frames = []
    node_pos = ((125, 170), (675, 170), (125, 385), (675, 385))
    for index in range(40):
        frame = bg.copy()
        composite_center(frame, energized_frame(base, index % 12), (400, 240), (300, 300))
        # Re-arm teleport: aperture opens, generator resolves, then the shield becomes solid.
        tele = min(11, index // 2)
        for ni, pos in enumerate(node_pos):
            fx = Image.open(OUT_DIR / f"s4w_node_teleport_{tele:02d}.png")
            if index < 24:
                composite_center(frame, fx, pos, (112, 112))
            if index >= 12:
                pn = Image.open(OUT_DIR / f"s4w_power_node_{(index + ni * 3) % 16:02d}.png")
                alpha = min(1.0, (index - 11) / 8)
                pn = pn.copy(); pn.putalpha(pn.getchannel("A").point(lambda a: round(a * alpha)))
                composite_center(frame, pn, pos, (78, 78))
        if index >= 20:
            shield = Image.open(OUT_DIR / f"s4w_lightning_shield_{index % 12:02d}.png")
            composite_center(frame, shield, (400, 235), (390, 390))
        if index >= 27:
            core = Image.open(OUT_DIR / f"s4w_final_chaingun_core_{index % 8:02d}.png")
            gun = Image.open(OUT_DIR / f"s4w_final_chaingun_{index % 8:02d}.png")
            q = min(1.0, (index - 27) / 12)
            turn = q * math.tau
            assembly = rigid_socketed_plate(core, gun, 126, (58, 88), turn, True)
            composite_center(frame, assembly, (400, 270))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    frames[0].save(PROOF_DIR / "stage4_storm_rearm_preview.gif", save_all=True,
                   append_images=frames[1:], duration=75, loop=0, disposal=2)

    sheet = Image.new("RGBA", (1180, 760), (7, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    entries = [
        ("FULL-ASSEMBLY ROTATION 0", Image.open(OUT_DIR / "s4w_final_chaingun_00.png"), (125, 230), (112, 168)),
        ("FULL-ASSEMBLY ROTATION 2", Image.open(OUT_DIR / "s4w_final_chaingun_02.png"), (315, 230), (112, 168)),
        ("FULL-ASSEMBLY ROTATION 4", Image.open(OUT_DIR / "s4w_final_chaingun_04.png"), (505, 230), (112, 168)),
        ("FULL-ASSEMBLY ROTATION 6", Image.open(OUT_DIR / "s4w_final_chaingun_06.png"), (695, 230), (112, 168)),
        ("TWIN-GUN POWER CORE", Image.open(OUT_DIR / "s4w_final_chaingun_core_04.png"), (940, 215), (190, 190)),
        ("NODE TELEPORT / STATIC", Image.open(OUT_DIR / "s4w_node_teleport_07.png"), (255, 535), (170, 170)),
        ("LIGHTNING MG ROUND", Image.open(OUT_DIR / "s4w_lightning_mg_round_04.png"), (520, 535), (80, 134)),
        ("REARMED POWER CIRCLE", Image.open(OUT_DIR / "s4w_power_node_09.png"), (760, 535), (150, 150)),
        ("SHIELD RE-FORMATION", Image.open(OUT_DIR / "s4w_lightning_shield_05.png"), (1010, 535), (190, 190)),
    ]
    for label, sprite, center, dims in entries:
        composite_center(sheet, sprite, center, dims)
        box = draw.textbbox((0, 0), label)
        draw.text((center[0] - (box[2] - box[0]) / 2, center[1] + dims[1] / 2 + 12), label,
                  fill=(226, 244, 255, 255))
    sheet.save(PROOF_DIR / "stage4_storm_rearm_contact_sheet.png")
    build_socketed_chaingun_preview(bg)
    build_side_helper_preview(bg)
    build_helper_heat_preview(bg)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    boss, node = save_boss_frames()
    drone, _ = split_drone_parts()
    shield = save_generated_shield_frames()
    ball = save_generated_lightning_ball_frames()
    save_final_phase_assets()
    save_helper_core_assets()
    save_locked_dual_helper_assets()
    save_mg_rounds()
    save_orb_and_lightning()
    save_muzzle_family("mg", (DARK, GOLD, WHITE))
    save_muzzle_family("orb", (DARK, BLUE, ICE))
    save_muzzle_family("lightning", (ROYAL, CYAN, WHITE))
    build_preview(boss, drone)
    build_shield_preview(boss, node, shield, ball)
    build_rearm_preview(boss)
    print(f"Built Stage 4 warfare assets in {OUT_DIR}")


if __name__ == "__main__":
    main()
