#!/usr/bin/env python3
"""
make_short_0916.py - a 9:16 vertical cut for YouTube Shorts / Reels / TikTok.

    python _BUILD_SOURCE/make_short_0916.py boss_s2_furnace --title "FURNACE TYRANT"
    python _BUILD_SOURCE/make_short_0916.py boss_s7_warden --seconds 28

The game records at 960x1152 (5:6) -- already nearly portrait, which is lucky, because a vertical
shmup is the one genre that fits a phone without being butchered.

⚠ DO NOT CROP TO 9:16 AND DO NOT PAD WITH BLACK. Cropping 5:6 to 9:16 throws away a third of the
playfield sideways, which on this game removes the bullets you are meant to be dodging. Black bars
read as a lazy re-upload and the platforms' own UI sits on top of them. The clip is scaled to full
width and the remaining top/bottom is filled with a blurred, darkened blow-up of the clip's own
frame, so the palette always matches the shot and the eye stays in the middle.

Output: docs/marketing_0916/video/<stem>_short.mp4
"""
import argparse, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
import social_kit_0916 as sk  # noqa: E402

CLIPS = os.path.join(GAME, 'docs', 'marketing_0916', 'clips')
OUT = os.path.join(GAME, 'docs', 'marketing_0916', 'video')
W, H = 1080, 1920


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v',
                        '-show_entries', 'stream=width,height', '-of', 'json', path],
                       capture_output=True, text=True)
    s = json.loads(r.stdout)['streams'][0]
    return int(s['width']), int(s['height'])


def build_plate(title, gy, gh):
    """Wordmark above the clip, title below it, both clear of the platform UI.

    ⚠ The bottom ~15% of a Short is covered by the caption, the like/share rail and the progress
    bar on every platform. Nothing legible goes there.
    """
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    lg = sk.fit(sk.logo(), int(W * 0.72), int(H * 0.11))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ly = max(40, (gy - lg.height) // 2)
    layer.paste(lg, ((W - lg.width) // 2, ly), lg)
    im = Image.alpha_composite(im, sk.glow(layer, sk.EMBER, 34, 0.9))
    im = Image.alpha_composite(im, layer)

    if title:
        below = H - (gy + gh)
        ty = gy + gh + max(24, (below - 150) // 2)
        size = 84
        while size > 34 and sk.measure_tagline(title, size) > W - 100:
            size -= 4
        im = sk.draw_tagline(im, title, (W // 2, ty), height=size, colour=(255, 234, 196))

    d = ImageDraw.Draw(im)
    d.rectangle((0, gy - 3, W, gy - 1), fill=(255, 170, 90, 180))
    d.rectangle((0, gy + gh + 1, W, gy + gh + 3), fill=(255, 170, 90, 180))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stem')
    ap.add_argument('--title', default=None)
    ap.add_argument('--seconds', type=float, default=None)
    ap.add_argument('--start', type=float, default=3.0)
    ap.add_argument('--music', default='assets/game/music/boss1_minderaser.mp3')
    args = ap.parse_args()

    src = os.path.join(CLIPS, args.stem + '.mp4')
    if not os.path.exists(src):
        print('no clip', src); sys.exit(1)
    os.makedirs(OUT, exist_ok=True)

    cw, ch = probe(src)
    gw = W
    gh = int(round(ch * gw / cw))
    gy = (H - gh) // 2

    plate = build_plate(args.title or args.stem.replace('_', ' ').upper(), gy, gh)
    pp = os.path.join(OUT, '_short_plate.png')
    plate.save(pp)

    dur = args.seconds
    if dur is None:
        total = float(subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
            capture_output=True, text=True).stdout.strip())
        dur = min(58.0, max(6.0, total - args.start))

    out = os.path.join(OUT, args.stem + '_short.mp4')
    fc = (
        # the backdrop is the clip itself, blown up to fill 9:16, blurred and dimmed
        '[0:v]trim=start=%f:duration=%f,setpts=PTS-STARTPTS,split=2[bgsrc][fgsrc];'
        '[bgsrc]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,'
        'gblur=sigma=42,eq=brightness=-0.22[bg];'
        '[fgsrc]scale=%d:%d:flags=lanczos[fg];'
        '[bg][fg]overlay=0:%d[v0];'
        '[v0][1:v]overlay=0:0,format=yuv420p[v]'
        % (args.start, dur, W, H, W, H, gw, gh, gy)
    )
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', src,
           '-loop', '1', '-t', str(dur), '-i', pp]
    mp = os.path.join(GAME, args.music)
    if os.path.exists(mp):
        cmd += ['-stream_loop', '-1', '-i', mp]
        fc += ';[2:a]volume=0.85,afade=in:st=0:d=0.8,afade=out:st=%f:d=1.2[a]' % max(0, dur - 1.2)
        maps = ['-map', '[v]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k']
    else:
        maps = ['-map', '[v]', '-an']
    cmd += ['-filter_complex', fc] + maps + [
        '-t', str(dur), '-r', '60', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
        '-movflags', '+faststart', out]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print((r.stderr or '')[-1200:]); sys.exit(1)
    os.remove(pp)
    print('  short  %s  (%.0fs, %dx%d)' % (out, dur, W, H))


if __name__ == '__main__':
    main()
