#!/usr/bin/env python3
"""
make_reel_0916.py - cut a finished video out of the captured clips.

    python _BUILD_SOURCE/make_reel_0916.py bosses
    python _BUILD_SOURCE/make_reel_0916.py bosses --music assets/game/music/boss1_minderaser.mp3
    python _BUILD_SOURCE/make_reel_0916.py --list

THE LAYOUT PROBLEM, AND WHY IT IS SOLVED THIS WAY
  The game records at 960x1152 -- taller than it is wide, because it is a vertical shmup and the
  capture takes the whole cabinet (HUD strip, EQUIPPED box, play field). YouTube is 16:9. The three
  ways to square that are: crop (throws away a third of a playfield the player needs to see),
  stretch (ruins hand-authored pixel art), or frame it.

  Framed it is. The clip sits centre at its native aspect against a darkened blur of the cover
  painting, with the wordmark in the left panel and the encounter's name in the right -- an arcade
  cabinet, which is what the game is. Nothing is cropped and nothing is resampled non-uniformly.

  ⚠ THE CLIPS ARE SILENT. The in-game recorder is video-only -- drop 0910d says so directly
  ("Audio is still not captured and is a bigger job"). So the bed is a music track, and the
  sound effects are simply absent. Say so if anyone asks; do not imply the trailer is diegetic.
"""
import argparse, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
CLIPS = os.path.join(GAME, 'docs', 'marketing_0916', 'clips')
OUT = os.path.join(GAME, 'docs', 'marketing_0916', 'video')
LOGO = os.path.join(GAME, 'assets', 'game', 'ui', 'logo_0916', 'bof_logo.png')
COVER = os.path.join(GAME, 'docs', 'marketing_0916', 'cover_b_with_logo.png')

W, H = 1920, 1080
EMBER = (255, 122, 26)

# clip stem -> (stage line, encounter name, seconds to use, start offset)
REELS = {
    'bosses': {
        'title': 'EVERY BOSS IN BULLETS OF FURY',
        'music': 'assets/game/music/boss1_minderaser.mp3',
        'items': [
            ('boss_s1_overlordx', 'STAGE 1  -  RUMBLE IN THE JUNGLE', 'JUNGLE OVERLORD-X', 13, 4),
            ('boss_s2_furnace', "STAGE 2  -  IT'S HOT IN HERE", 'FURNACE TYRANT', 13, 4),
            ('boss_s3_rimewall', "STAGE 3  -  ICE STILL CAN'T SEE", 'RIME WALL', 13, 4),
            ('boss_s4_sovereign', 'STAGE 4  -  CROUCHING MISSILES', 'STORM SOVEREIGN MK II', 13, 4),
            ('boss_s6_carrier', 'STAGE 6  -  HEAVY TURBULENCE', 'DOOMSDAY CARRIER MK II', 13, 4),
            ('boss_s7_warden', 'STAGE 7  -  NOT ANOTHER SEWER LEVEL', 'TOXIC PORTAL WARDEN', 13, 4),
            ('boss_s8_cocoon', 'STAGE 8  -  FURIOUS DEATH', 'BLACK COCOON', 13, 4),
            ('boss_s9_sentinels', 'STAGE 9  -  THE VELOCITY VOID', 'WARP SENTINELS', 13, 4),
        ],
    },
    'minis': {
        'title': 'THE MINIBOSSES',
        'music': 'assets/game/music/miniboss_fireboss.mp3',
        'items': [
            ('mini_s1_razorback', 'STAGE 1', 'RAZORBACK SIEGE TANK', 12, 4),
            ('mini_s3_frost', 'STAGE 3', 'FROST CRUISER', 12, 4),
            ('mini_s6_tempest', 'STAGE 6', 'TEMPEST LEVIATHAN BROTHERS', 12, 4),
            ('mini_s9_horizon', 'STAGE 9', 'EVENT HORIZON', 12, 4),
        ],
    },
    'pilots': {
        'title': 'NINE PILOTS, NINE DIFFERENT GUNS',
        'music': 'assets/game/music/pilot_select.mp3',
        # ⚠ THE AFFILIATIONS ARE THE GAME'S OWN, READ OUT OF `AINTRO_AFFIL` IN game.js.
        # They exist ONLY in that table -- CLAUDE.md records that they were baked pixels in the
        # arcade intro plates until they were transcribed there, and that nothing else carries
        # them. Inventing a plausible-sounding one for a trailer would be putting fake lore in
        # front of the audience, so they are copied, never guessed.
        'items': [
            ('pilot_cole', 'FURY FOUNDER', 'COLE', 10, 3),
            ('pilot_juggernaut', 'BROTHERHOOD OF FURY', 'JUGGERNAUT', 10, 3),
            ('pilot_freezer', 'AIRFORCE', 'FREEZER', 10, 3),
            ('pilot_lizzie', 'STRATEGIC ORDNANCE', 'LIZZIE', 10, 3),
            ('pilot_maverick', 'INDEPENDENT', 'MAVERICK', 10, 3),
            ('pilot_yuri', 'INDEPENDENT', 'YURI', 10, 3),
            ('pilot_falva', 'PRINCESSES OF THE SKY', 'FALVA', 10, 3),
            ('pilot_axel', 'AIRFORCE', 'AXEL', 10, 3),
            ('pilot_decker', 'ORDER OF THE MATRIX', 'DECKER', 10, 3),
        ],
    },
    'stages': {
        'title': 'NINE STAGES',
        'music': 'assets/game/music/title_main_menu.mp3',
        'items': [
            ('stage_s2_lava', 'STAGE 2', "IT'S HOT IN HERE", 10, 3),
            ('stage_s3_ice', 'STAGE 3', "ICE STILL CAN'T SEE", 10, 3),
            ('stage_s5_space', 'STAGE 5', 'ALL FOR ONE, NONE FOR ALL', 10, 3),
            ('stage_s6_storm', 'STAGE 6', 'HEAVY TURBULENCE', 10, 3),
            ('stage_s9_void', 'STAGE 9', 'THE VELOCITY VOID', 10, 3),
        ],
    },
}


def font(px, bold=True):
    for c in ([r'C:\Windows\Fonts\impact.ttf'] if bold else []) + \
             [r'C:\Windows\Fonts\arialbd.ttf', r'C:\Windows\Fonts\segoeuib.ttf',
              r'C:\Windows\Fonts\arial.ttf']:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, px)
            except Exception:
                pass
    return ImageFont.load_default()


def tracked(d, text, f, x, y, sp, fill, shadow=(0, 0, 0, 220), anchor='l'):
    """Letter-spaced text with a hard drop shadow. Returns the width drawn."""
    ws = [(f.getbbox(c)[2] - f.getbbox(c)[0]) if c != ' ' else f.size // 3 for c in text]
    total = sum(ws) + sp * max(0, len(text) - 1)
    if anchor == 'c':
        x -= total // 2
    elif anchor == 'r':
        x -= total
    for c, cw in zip(text, ws):
        if c != ' ':
            d.text((x + 2, y + 3), c, font=f, fill=shadow)
            d.text((x, y), c, font=f, fill=fill)
        x += cw + sp
    return total


def build_bed():
    """The static backdrop: the cover painting, blurred and dimmed to 16:9."""
    cv = Image.open(COVER).convert('RGB')
    r = max(W / cv.width, H / cv.height)
    s = cv.resize((int(cv.width * r) + 1, int(cv.height * r) + 1), Image.LANCZOS)
    s = s.crop(((s.width - W) // 2, (s.height - H) // 2,
                (s.width - W) // 2 + W, (s.height - H) // 2 + H))
    s = s.filter(ImageFilter.GaussianBlur(26))
    s = ImageEnhance.Brightness(s).enhance(0.34)
    return s.convert('RGBA')


def video_box(clip_w, clip_h):
    """Where the gameplay sits: full height minus a margin, native aspect."""
    vh = H - 60
    vw = int(round(clip_w * vh / clip_h))
    return ((W - vw) // 2, (H - vh) // 2, vw, vh)


def build_plate(stage_line, name, box, index=None, total=None):
    """The overlay for one segment: frame, wordmark left, encounter name right."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x, y, vw, vh = box

    # a lit edge around the play area, and a soft ember bloom outside it
    bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom).rectangle((x - 6, y - 6, x + vw + 5, y + vh + 5),
                                    outline=EMBER + (255,), width=10)
    im = Image.alpha_composite(im, bloom.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im)
    d.rectangle((x - 3, y - 3, x + vw + 2, y + vh + 2), outline=(255, 190, 110, 235), width=3)
    d.rectangle((x - 1, y - 1, x + vw, y + vh), outline=(40, 22, 10, 255), width=1)

    panel = x - 40                     # usable width of the left panel
    # wordmark, left panel, vertically near the top
    lg = Image.open(LOGO).convert('RGBA')
    lw = min(int(panel * 0.86), 420)
    lg = lg.resize((lw, max(1, int(lg.height * lw / lg.width))), Image.LANCZOS)
    im.alpha_composite(lg, (max(24, (x - lg.width) // 2), 80))

    # encounter name, right panel, stacked and wrapped by hand so it never runs out
    rx = x + vw + 40
    rw = W - rx - 40
    f_name = font(56)
    yy = 150
    # ⚠ FIT THE STAGE LINE TO THE PANEL, DO NOT TRUNCATE IT TO A CHARACTER COUNT.
    # A 46-character cut shipped "STAGE 7 - NOT ANOTHER SEWER LEVE" running off the right edge:
    # the limit is the panel's WIDTH in pixels and these subtitles vary from 8 to 34 characters.
    # Measured down from 26px until it fits, with a floor so it stays readable.
    null = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    for px in range(26, 13, -1):
        f_stage = font(px)
        if tracked(null, stage_line, f_stage, 0, 0, 3, (0, 0, 0, 0), (0, 0, 0, 0)) <= rw:
            break
    tracked(d, stage_line, f_stage, rx, yy, 3, (255, 176, 96, 255))
    yy += 54
    d.line((rx, yy, rx + min(rw, 380), yy), fill=(255, 140, 50, 200), width=3)
    yy += 26

    words, line, lines = name.split(' '), '', []
    for wd in words:
        t = (line + ' ' + wd).strip()
        if tracked(ImageDraw.Draw(Image.new('RGBA', (10, 10))), t, f_name, 0, 0, 2,
                   (0, 0, 0, 0), (0, 0, 0, 0)) > rw and line:
            lines.append(line); line = wd
        else:
            line = t
    if line:
        lines.append(line)
    for ln in lines[:4]:
        tracked(d, ln, f_name, rx, yy, 2, (255, 240, 215, 255))
        yy += 66

    if index is not None:
        f_idx = font(150)
        tracked(d, '%d' % index, f_idx, W - 60, H - 230, 0, (255, 255, 255, 40), (0, 0, 0, 0), 'r')
        f_of = font(24)
        tracked(d, 'OF %d' % total, f_of, W - 60, H - 80, 4, (255, 170, 90, 150), (0, 0, 0, 0), 'r')

    return im


def build_card(title, sub=None, big=True):
    """A full-frame title / end card."""
    im = build_bed()
    lg = Image.open(LOGO).convert('RGBA')
    lw = int(W * (0.46 if big else 0.34))
    lg = lg.resize((lw, max(1, int(lg.height * lw / lg.width))), Image.LANCZOS)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ly = int(H * (0.24 if big else 0.30))
    layer.paste(lg, ((W - lg.width) // 2, ly), lg)
    g = Image.new('RGBA', (W, H), EMBER + (0,))
    g.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(40)).point(lambda v: min(255, int(v * 0.9))))
    im = Image.alpha_composite(im, g)
    im = Image.alpha_composite(im, layer)
    d = ImageDraw.Draw(im)
    yy = ly + lg.height + 46
    if title:
        tracked(d, title, font(52), W // 2, yy, 6, (255, 236, 200, 255), anchor='c')
        yy += 84
    if sub:
        tracked(d, sub, font(34), W // 2, yy, 5, (255, 176, 96, 255), anchor='c')
    return im


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v',
                        '-show_entries', 'stream=width,height', '-of', 'json', path],
                       capture_output=True, text=True)
    s = json.loads(r.stdout)['streams'][0]
    return int(s['width']), int(s['height'])


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('ffmpeg failed:\n', ' '.join(cmd[:14]), '...\n', (r.stderr or '')[-1400:])
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reel', nargs='?', default='bosses')
    ap.add_argument('--music', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--no-music', action='store_true')
    args = ap.parse_args()

    if args.list:
        for k, v in REELS.items():
            have = sum(1 for it in v['items']
                       if os.path.exists(os.path.join(CLIPS, it[0] + '.mp4')))
            print('%-8s %-36s %d/%d clips present' % (k, v['title'], have, len(v['items'])))
        return

    spec = REELS[args.reel]
    os.makedirs(OUT, exist_ok=True)
    items = [it for it in spec['items']
             if os.path.exists(os.path.join(CLIPS, it[0] + '.mp4'))]
    missing = [it[0] for it in spec['items'] if it not in items]
    if missing:
        print('missing clips (skipped):', ', '.join(missing))
    if not items:
        print('no clips for reel %r -- run capture_batch_0916.py first' % args.reel)
        sys.exit(1)

    tmp = tempfile.mkdtemp(prefix='bofreel_')
    segs = []

    bed = build_bed()
    bed_p = os.path.join(tmp, 'bed.png')
    bed.convert('RGB').save(bed_p)

    # --- opening card
    card = build_card(spec['title'], 'A NINE-STAGE VERTICAL SHMUP  -  IN DEVELOPMENT')
    cp = os.path.join(tmp, 'card_open.png')
    card.convert('RGB').save(cp)
    seg = os.path.join(tmp, 'seg_open.mp4')
    run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', '3.2', '-i', cp,
         '-vf', 'fade=in:0:20,fade=out:st=2.7:d=0.5,format=yuv420p',
         '-r', '60', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', seg])
    segs.append(seg)

    # --- one segment per encounter
    for i, (stem, stage_line, name, secs, off) in enumerate(items, 1):
        src = os.path.join(CLIPS, stem + '.mp4')
        cw, ch = probe(src)
        box = video_box(cw, ch)
        plate = build_plate(stage_line, name, box, i, len(items))
        pp = os.path.join(tmp, 'plate_%02d.png' % i)
        plate.save(pp)

        seg = os.path.join(tmp, 'seg_%02d.mp4' % i)
        x, y, vw, vh = box
        fc = (
            '[1:v]trim=start=%f:duration=%f,setpts=PTS-STARTPTS,scale=%d:%d:flags=lanczos[g];'
            '[0:v]scale=%d:%d[bed];'
            '[bed][g]overlay=%d:%d[v1];'
            '[v1][2:v]overlay=0:0,fade=in:0:14,fade=out:st=%f:d=0.45,format=yuv420p[v]'
            % (off, secs, vw, vh, W, H, x, y, secs - 0.45)
        )
        run(['ffmpeg', '-y', '-loglevel', 'error',
             '-loop', '1', '-t', str(secs), '-i', bed_p,
             '-i', src,
             '-loop', '1', '-t', str(secs), '-i', pp,
             '-filter_complex', fc, '-map', '[v]',
             '-r', '60', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
             '-t', str(secs), seg])
        segs.append(seg)
        print('  cut %s (%ds)' % (stem, secs))

    # --- end card
    endc = build_card('WISHLIST ON STEAM', 'SOON  -  @BULLETSOFFURY', big=False)
    ep = os.path.join(tmp, 'card_end.png')
    endc.convert('RGB').save(ep)
    seg = os.path.join(tmp, 'seg_end.mp4')
    run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', '4.0', '-i', ep,
         '-vf', 'fade=in:0:20,fade=out:st=3.4:d=0.6,format=yuv420p',
         '-r', '60', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', seg])
    segs.append(seg)

    lst = os.path.join(tmp, 'list.txt')
    with open(lst, 'w') as f:
        for s in segs:
            f.write("file '%s'\n" % s.replace('\\', '/'))

    out = args.out or os.path.join(OUT, '%s_reel.mp4' % args.reel)
    music = args.music or spec.get('music')
    mp = os.path.join(GAME, music) if music and not os.path.isabs(music) else music

    if args.no_music or not (mp and os.path.exists(mp)):
        if not args.no_music:
            print('no music at %r -- rendering silent' % music)
        run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
             '-c', 'copy', out])
    else:
        joined = os.path.join(tmp, 'joined.mp4')
        run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
             '-c', 'copy', joined])
        dur = float(subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', joined], capture_output=True, text=True).stdout.strip())
        run(['ffmpeg', '-y', '-loglevel', 'error', '-i', joined,
             '-stream_loop', '-1', '-i', mp,
             '-filter_complex',
             '[1:a]volume=0.82,afade=in:st=0:d=1.2,afade=out:st=%f:d=2.0[a]' % max(0, dur - 2.0),
             '-map', '0:v', '-map', '[a]', '-t', str(dur),
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
             '-movflags', '+faststart', out])

    print('\n  reel  %s' % out)
    print('  music %s' % (mp if (mp and os.path.exists(mp or '')) else 'NONE (clips are silent)'))
    print('  NOTE  the clips carry no game audio -- the in-game recorder is video only.')


if __name__ == '__main__':
    main()
