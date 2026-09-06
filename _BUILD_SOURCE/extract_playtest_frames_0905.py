#!/usr/bin/env python3
"""extract_playtest_frames_0905.py - turn Mike's four playtest recordings into something readable.

    python _BUILD_SOURCE/extract_playtest_frames_0905.py

Mike, 0905: "then observe all vidoes and fix projectiles, gameplay and more."

⚠ I CANNOT WATCH AN MP4. What I can do is decode it and look at frames, which is a strictly weaker
thing and needs saying out loud: a sampled grid shows what is ON SCREEN, not how it MOVED. Timing,
feel, and whether a projectile reads as fast are exactly the properties that fall between samples.
So this is for spotting visible defects - overlapping UI, wrong sprites, bad colour - and Mike's
own description of the videos remains the authority on how they PLAY.

⚠ ffmpeg is not on PATH on this machine; PyAV is. Decoding is done by seeking to timestamps rather
than walking every frame - these are 55MB-508MB screen captures and a full decode of all four is
minutes of work for frames nobody looks at.
"""
import os, sys, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'playtest_0905')
VIDS = [
    r'C:/Users/Mdogg/Videos/2026-09-05 22-54-43.mp4',
    r'C:/Users/Mdogg/Videos/2026-09-05 22-58-07.mp4',
    r'C:/Users/Mdogg/Videos/2026-09-05 23-06-22.mp4',
]
N = 24                      # frames sampled per video


def main():
    import av
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(OUT, exist_ok=True)
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()

    for vi, path in enumerate(VIDS):
        if not os.path.exists(path):
            print('MISSING %s' % path)
            continue
        tag = os.path.basename(path).replace('.mp4', '').replace(' ', '_')
        with av.open(path) as c:
            st = c.streams.video[0]
            dur = float(st.duration * st.time_base) if st.duration else \
                  (float(c.duration) / 1000000.0 if c.duration else 0)
            w, h = st.codec_context.width, st.codec_context.height
            print('\n%s  %dx%d  %.1fs' % (tag, w, h, dur))
            shots = []
            for i in range(N):
                t = dur * (i + 0.5) / N
                try:
                    c.seek(int(t / st.time_base), stream=st)
                    img = None
                    for frame in c.decode(st):
                        img = frame.to_image()
                        break
                    if img is None:
                        continue
                    shots.append((t, img))
                except Exception as e:
                    print('  seek %.1fs failed: %s' % (t, e))
            if not shots:
                print('  no frames decoded')
                continue
            # full-size singles for the ones worth reading closely, plus one contact sheet
            for t, img in shots:
                img.save(os.path.join(OUT, '%s_t%04d.png' % (tag, int(t))))
            TH = 300
            tiles = [(t, im.resize((int(im.width * TH / im.height), TH), Image.LANCZOS))
                     for t, im in shots]
            cols = 4
            rows = (len(tiles) + cols - 1) // cols
            cw, ch = tiles[0][1].width, TH + 22
            sheet = Image.new('RGB', (cw * cols, ch * rows), (12, 12, 16))
            d = ImageDraw.Draw(sheet)
            for i, (t, im) in enumerate(tiles):
                x, y = (i % cols) * cw, (i // cols) * ch
                sheet.paste(im, (x, y))
                d.text((x + 6, y + TH + 3), '%s  t=%.0fs' % (tag[-8:], t), font=F, fill=(230, 235, 245))
            p = os.path.join(OUT, 'SHEET_%d_%s.png' % (vi + 1, tag))
            sheet.save(p)
            print('  %d frames -> %s' % (len(shots), os.path.basename(p)))
    print('\nall output in %s' % OUT)


if __name__ == '__main__':
    main()
