#!/usr/bin/env python3
"""
slim_audio_0801kq.py — RECLAIM SPACE FROM AUDIO WITHOUT TOUCHING THE ART

Mike: "why my zip is even 500 mb to begin with."

The art turned out to be genuinely needed — 2 unreferenced files, 6 MB of
duplicates, ~0% lossless PNG headroom. Audio is where the free space is, and
unlike the art none of it is addressed by a runtime-assembled key, so changing
it cannot break a lookup the way deleting a boss prefix would.

TWO CHANGES, BOTH SAFE:

1. STRIP EMBEDDED COVER ART + METADATA FROM EVERY MP3  (~3.0 MB)
   Every music file carries a PNG album cover inside it. ffprobe reports a
   second `codec_name=png` stream on each one. The game never displays it.
   `-vn -c:a copy` drops the picture and re-muxes the SAME audio bytes — this is
   lossless, the waveform is not re-encoded.

2. AMBIENCE WAV -> MP3  (~11.3 MB)
   assets/sounds/amb/ ships six beds as raw PCM at 705 kbps, 13.12 MB for six
   looping background textures. At 96 kbps mono they are 1.79 MB. These are
   low-frequency environment beds under music and gunfire, which is the one
   place the bitrate will not be noticed.

3. MUSIC 160 kbps -> 112 kbps, STILL STEREO  (~14 MB)
   Held back on the first pass and A/B'd instead: Mike listened to stage 1 at
   both rates and approved 112k. STEREO IS KEPT. Dropping to mono saves more but
   collapses the stereo image, which is far more audible on music than bitrate,
   and none of the size pressure justifies it.
   Only files ABOVE 112 kbps are touched, so re-running this cannot re-encode an
   already-converted file and stack generation loss.

Ambience is referenced by manifest KEY (amb_jungle), never by path in game.js,
so the extension change is a one-line manifest edit per file.
"""
import json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(ROOT, '_superseded', 'audio_0801kq')


def sh(*a):
    return subprocess.run(a, capture_output=True).returncode == 0


def mb(n):
    return f'{n/1048576:.2f} MB'


def main(apply=False):
    os.makedirs(BACKUP, exist_ok=True) if apply else None
    before = after = 0
    n_mp3 = n_amb = n_enc = 0

    # ---- 1. strip cover art from every mp3 (lossless)
    mp3s = []
    for root, _, fs in os.walk(os.path.join(ROOT, 'assets')):
        for f in fs:
            if f.endswith('.mp3'):
                mp3s.append(os.path.join(root, f))
    for p in mp3s:
        a = os.path.getsize(p)
        # NOTE: the temp file must keep a .mp3 extension. Naming it '.tmp' made
        # ffmpeg unable to infer the container and every strip silently no-opped.
        tmp = p[:-4] + '.__slim.mp3'
        if not sh('ffmpeg', '-v', 'error', '-y', '-i', p, '-vn',
                  '-c:a', 'copy', '-map_metadata', '-1', '-f', 'mp3', tmp):
            if os.path.exists(tmp): os.remove(tmp)
            continue
        b = os.path.getsize(tmp)
        before += a; after += b; n_mp3 += 1
        if apply and b < a:
            bp = os.path.join(BACKUP, os.path.relpath(p, ROOT).replace('/', '__'))
            if not os.path.exists(bp): shutil.copy2(p, bp)
            os.replace(tmp, p)
        else:
            os.remove(tmp)

    # ---- 3. music down to 112k stereo (approved after an A/B on stage 1)
    for p in mp3s:
        try:
            br = subprocess.run(['ffprobe','-v','error','-select_streams','a:0',
                                 '-show_entries','stream=bit_rate','-of','csv=p=0',p],
                                capture_output=True, text=True).stdout.strip()
            br = int(br) if br.isdigit() else 0
        except Exception:
            br = 0
        if br <= 120000:          # already at or below target: leave it alone
            continue
        a = os.path.getsize(p)
        tmp = p[:-4] + '.__enc.mp3'
        if not sh('ffmpeg','-v','error','-y','-i',p,'-c:a','libmp3lame',
                  '-b:a','112k','-ac','2','-f','mp3',tmp):
            if os.path.exists(tmp): os.remove(tmp)
            continue
        b = os.path.getsize(tmp)
        if b >= a:
            os.remove(tmp); continue
        before += a; after += b; n_enc += 1
        if apply:
            bp = os.path.join(BACKUP, 'music__' + os.path.relpath(p, ROOT).replace('/', '__'))
            if not os.path.exists(bp): shutil.copy2(p, bp)
            os.replace(tmp, p)
        else:
            os.remove(tmp)

    # ---- 2. ambience wav -> mp3, and repoint the manifest
    ambdir = os.path.join(ROOT, 'assets/sounds/amb')
    conv = {}
    if os.path.isdir(ambdir):
        for f in sorted(os.listdir(ambdir)):
            if not f.endswith('.wav'): continue
            src = os.path.join(ambdir, f)
            dst = src[:-4] + '.mp3'
            a = os.path.getsize(src)
            if not sh('ffmpeg', '-v', 'error', '-y', '-i', src,
                      '-c:a', 'libmp3lame', '-b:a', '96k', '-ac', '1', dst):
                continue
            b = os.path.getsize(dst)
            before += a; after += b; n_amb += 1
            conv[f'assets/sounds/amb/{f}'] = f'assets/sounds/amb/{f[:-4]}.mp3'
            if apply:
                bp = os.path.join(BACKUP, ('assets__sounds__amb__' + f))
                if not os.path.exists(bp): shutil.copy2(src, bp)
                os.remove(src)
            else:
                os.remove(dst)

    if apply and conv:
        mp = os.path.join(ROOT, 'assets/manifest.js')
        s = open(mp).read()
        for old, new in conv.items():
            s = s.replace('"' + old + '"', '"' + new + '"')
        open(mp, 'w').write(s)
        # verify every new path resolves
        bad = [v for v in conv.values() if not os.path.exists(os.path.join(ROOT, v))]
        stale = [k for k in conv if '"' + k + '"' in open(mp).read()]
        print(f'manifest repointed: {len(conv)} ambience keys, '
              f'{len(bad)} missing files, {len(stale)} stale references')

    print(f'mp3 cover-art stripped : {n_mp3} files')
    print(f'music -> 112k stereo   : {n_enc} files')
    print(f'ambience re-encoded    : {n_amb} files')
    print(f'audio {mb(before)} -> {mb(after)}   saved {mb(before-after)}')
    print('APPLIED' if apply else 'DRY RUN — pass --apply')


if __name__ == '__main__':
    main('--apply' in sys.argv)
