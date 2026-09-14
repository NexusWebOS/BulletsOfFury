"""stills3.py - one labelled page of the finished trailer, read off the RENDERED FILE at the moments that matter.

    python stills3.py trailer_v3.mp4 edl3.json trailer_v3_stills.jpg
    python stills3.py trailer_v3.mp4 edl3.json trailer_v3_pilots.jpg --pilots     # every pilot ability bar, one still each

Each still is decoded from the muxed video, not re-composed from the EDL, so the page shows exactly what was
delivered. Moments are found by clip label, so the page follows the edit if the edit moves.
"""
import io, re, sys, json, subprocess
from PIL import Image, ImageDraw

W, H, STRIP, COLS = 640, 360, 26, 4
MOMENTS = [
    ('COLEFORGE', 'ColeForge Phoenix Engine + chime', 0.75),
    ('BULLETS OF FURY slam', 'the logo slam - "BULLETS OF FURY"', 0.6),
    ('SELECT MODE', 'new game -> campaign', 0.6),
    ('campaign map v2 boot', 'the campaign map in pieces', 0.7),
    ('F_s1', 'BOOM - stage 1', 0.5),
    ('SPACESHIP transformation', 'the spaceship transformation - snap to reveal', 0.35),
    ('SPACESHIP transformation', 'the spaceship revealed', 0.85),
    ('9 PILOTS', 'the nine avatar boxes', 0.85),
    ('YURI  CHAIN LIGHTNING', 'Yuri - Chain Lightning', 0.72),
    ('FALVA  ROLLER BALL', 'Falva - Roller Ball', 0.72),
    ('LIZZIE  ATOM BOMB', 'Lizzie - Atom Bomb', 0.78),
    ('JUGGERNAUT  CHARGE DASH', 'Juggernaut - Charge Dash (secondary)', 0.6),
    ('COLE  NUKE STRIKE - after the stop', 'Cole - the nuke lands as the riff returns', 0.25),
    ('ENEMY APPROACHING', 'minibosses - no names', 0.6),
    ('RETINA LOCK', 'retina lock - the Razor Rack salvo', 0.55),
    ('TEMPEST LEVIATHAN duel', 'stage-6 mini - the Tempest Leviathan duel', 0.5),
    ('(thermoshock balls)', 'Freezer - thermoshock balls', 0.6),
    ('LASER MIST', 'the real laser mist', 0.6),
    ('LASER CANNON', 'laser cannon (space)', 0.6),
    ('SHADOW ORB', 'shadow orb (space)', 0.7),
    ('BOSS s2 forming', 'stage-2 boss forming', 0.6),
    ('vs FURNACE', 'stage-2 boss - the second arm breaks', 0.7),
    ('FURNACE core phase', 'stage-2 boss - core phase', 0.5),
    ('FURNACE head', 'stage-2 boss - the head alone', 0.4),
    ('F_intro_s8 stage card', 'stage card 8', 0.5),
    ('grey slow motion E2_s1', 'tagline - 8 LEVELS', 0.5),
    ('ALERT! boss warning', 'boss warning - descriptor out of frame', 0.5),
    ('BOSS s3', 'level-3 boss - laser warn opens GREEN (25%)', 0.10),
    ('BOSS s3', 'level-3 boss - YELLOW while it is set up', 0.50),
    ('vs boss E2_s3', 'level-3 boss - RED, about to fire', 0.12),
    ('vs boss E2_s3', 'level-3 boss - the laser fires down the lane', 0.45),
    ('SHIP DESTROYED', 'the death spin-out (header rule)', 0.6),
    ('STAB S2_cole', 'tagline - 18 BOSSES', 0.55),
    ('STAB S2_lizzie', 'tagline - 1 HELL OF A CAMPAIGN', 0.45),
    ('WARP DRIVE jump', 'the warp drive jump', 0.6),
    ('END CARD', 'end card', 0.85),
]
ABILITY = re.compile(r'^[A-Z]+  [A-Z]')


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def grab(video, t):
    r = subprocess.run([ffmpeg(), '-v', 'error', '-ss', '%.3f' % t, '-i', video, '-frames:v', '1',
                        '-vf', 'scale=%d:%d:flags=lanczos' % (W, H), '-f', 'image2pipe', '-vcodec', 'png', '-'],
                       capture_output=True, check=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')


def main(video, edl_path, out, pilots=False):
    clips = sorted(json.load(open(edl_path))['clips'], key=lambda c: c['t0'])
    cells = []
    if pilots:
        for c in clips:
            lab = c.get('label') or ''
            if ABILITY.match(lab) and 'after the stop' not in lab:
                t = c['t0'] + (c['t1'] - c['t0']) * 0.72
                cells.append((grab(video, t), '%6.2fs  %s' % (t, lab)))
    else:
        for key, caption, at in MOMENTS:
            c = next((c for c in clips if key in (c.get('label') or '')), None)
            if c is None:
                print('  no clip labelled %r' % key)
                continue
            t = c['t0'] + (c['t1'] - c['t0']) * at
            cells.append((grab(video, t), '%6.2fs  %s' % (t, caption)))
    rows = (len(cells) + COLS - 1) // COLS
    page = Image.new('RGB', (COLS * W, rows * (H + STRIP)), (12, 12, 16))
    d = ImageDraw.Draw(page)
    for k, (im, cap) in enumerate(cells):
        x, y = (k % COLS) * W, (k // COLS) * (H + STRIP)
        page.paste(im, (x, y + STRIP))
        d.text((x + 8, y + 7), cap, fill=(235, 235, 235))
    page.save(out, quality=90)
    print('wrote %s (%d stills)' % (out, len(cells)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], pilots='--pilots' in sys.argv)
