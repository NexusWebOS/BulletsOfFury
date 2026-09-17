#!/usr/bin/env python3
"""
make_thumbs_0916.py - YouTube thumbnails, built on REAL captured frames.

    python _BUILD_SOURCE/make_thumbs_0916.py

Pulls a hero frame out of each clip in docs/marketing_0916/clips/ and lays the wordmark and a
title over it. Output: docs/marketing_0916/social/thumbs/

WHY A HERO FRAME AND NOT COVER ART
  A gameplay video thumbnailed with cover art is a promise the video does not keep, and the
  genre audience reads it instantly as a cheat. The frame chosen here is picked by MEASUREMENT --
  the candidate with the most lit, saturated pixels in the play area, i.e. the busiest moment of
  the fight -- not by taking frame 0 and hoping.

⚠ CHECK EVERY THUMBNAIL AT 210px WIDE. That is the size YouTube actually draws it in a sidebar.
  The contact sheet this writes shows each one at full size AND at 210, for that reason.
"""
import os, subprocess, sys, glob
from PIL import Image, ImageStat

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
import social_kit_0916 as sk  # noqa: E402

CLIPS = os.path.join(GAME, 'docs', 'marketing_0916', 'clips')
OUT = os.path.join(GAME, 'docs', 'marketing_0916', 'social', 'thumbs')

# clip stem -> thumbnail title. Three or four words; longer and it dies at sidebar size.
TITLES = {
    'boss_s1_overlordx': 'JUNGLE OVERLORD-X',
    'boss_s2_furnace': 'FURNACE TYRANT',
    'boss_s3_rimewall': 'THE RIME WALL',
    'boss_s4_sovereign': 'STORM SOVEREIGN',
    'boss_s6_carrier': 'DOOMSDAY CARRIER',
    'boss_s7_warden': 'PORTAL WARDEN',
    'boss_s8_cocoon': 'BLACK COCOON',
    'boss_s9_sentinels': 'WARP SENTINELS',
    'mini_s1_razorback': 'RAZORBACK TANK',
    'mini_s3_frost': 'FROST CRUISER',
    'mini_s6_tempest': 'TEMPEST BROTHERS',
    'mini_s9_horizon': 'EVENT HORIZON',
    'pilot_cole': 'COLE  /  SONIC BOOM',
    'pilot_juggernaut': 'JUGGERNAUT  /  WRECKING BALLS',
    'pilot_freezer': 'FREEZER  /  ICE BREATH',
    'pilot_lizzie': 'LIZZIE  /  TURRET MOUNT',
    'pilot_maverick': 'MAVERICK  /  LASER',
    'pilot_yuri': 'YURI  /  LIGHTNING ORB',
    'stage_s2_lava': "IT'S HOT IN HERE",
    'stage_s3_ice': "ICE STILL CAN'T SEE",
    'stage_s5_space': 'THE TRANSFORMATION',
    'stage_s6_storm': 'HEAVY TURBULENCE',
    'stage_s9_void': 'THE VELOCITY VOID',
}


def hero_frame(mp4, tmpdir, n=9):
    """Sample n frames and keep the busiest one.

    'Busiest' is mean saturation x mean brightness over the PLAY AREA only -- the HUD strip is
    lit and colourful on every single frame, so including it scores every candidate the same.
    """
    stem = os.path.splitext(os.path.basename(mp4))[0]
    pat = os.path.join(tmpdir, stem + '_%02d.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4,
                    '-vf', 'fps=1/2,scale=960:-1', '-frames:v', str(n), pat],
                   check=False)
    best, score = None, -1
    for p in sorted(glob.glob(os.path.join(tmpdir, stem + '_*.png'))):
        im = Image.open(p).convert('RGB')
        play = im.crop((0, int(im.height * 0.14), im.width, im.height))
        hsv = play.convert('HSV')
        s = ImageStat.Stat(hsv)
        v = s.mean[1] * s.mean[2]

        # ⚠ PENALISE BLOWN FRAMES. Every boss death and most big hits run a full-screen WHITE
        # flash, and white is maximum brightness -- so a "brightest, most saturated" score walks
        # straight to it. The first pass picked the Doomsday Carrier's whiteout: a thumbnail that
        # is 60% blank, with no boss visible in it at all.
        g = play.convert('L')
        hist = g.histogram()
        blown = sum(hist[236:]) / float(sum(hist))
        if blown > 0.22:
            v *= (1.0 - min(1.0, (blown - 0.22) * 3.2))

        if v > score:
            best, score = p, v
    return best


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, '_frames')
    os.makedirs(tmp, exist_ok=True)

    made = []
    for mp4 in sorted(glob.glob(os.path.join(CLIPS, '*.mp4'))):
        stem = os.path.splitext(os.path.basename(mp4))[0]
        if stem.startswith('test_'):
            continue
        title = TITLES.get(stem, stem.replace('_', ' ').upper())
        fr = hero_frame(mp4, tmp)
        if not fr:
            print('  no frame for', stem)
            continue
        name = 'thumb_' + stem + '.png'
        sk.build_thumb_from_frame(fr, title, name)
        made.append((stem, title, os.path.join(sk.OUT, name)))
        print('  %-24s %s' % (stem, title))

    if not made:
        print('no clips found in', CLIPS)
        return

    # contact sheet at full size and at the size YouTube actually draws
    cols = 3
    rows = (len(made) + cols - 1) // cols
    cw, ch = 420, 236 + 140
    sheet = Image.new('RGB', (cols * cw + 20, rows * ch + 20), (18, 18, 22))
    for i, (stem, title, path) in enumerate(made):
        im = Image.open(path)
        x = 10 + (i % cols) * cw
        y = 10 + (i // cols) * ch
        sheet.paste(im.resize((400, 225), Image.LANCZOS), (x, y))
        sheet.paste(im.resize((210, 118), Image.LANCZOS), (x + 95, y + 240))
    sp = os.path.join(OUT, '_contact.png')
    sheet.save(sp)
    print('\n  %d thumbnails -> %s' % (len(made), sk.OUT))
    print('  contact sheet (full size + 210px) -> %s' % sp)


if __name__ == '__main__':
    main()
