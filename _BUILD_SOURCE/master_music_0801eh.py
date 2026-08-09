#!/usr/bin/env python3
"""
DROP 0801eh - SOUNDTRACK MASTER PASS

Mike: "make this level 5's music, store level 5's original music as unused. try
to compress all music, and make all volume audiable hearable even with sounds
in-game ... the soundtrack is what makes bof really standout as I wrote it with
my guitar."

THE MEASURED PROBLEM
Integrated loudness across the 20 music tracks ranged from -5.1 LUFS to
-12.9 LUFS. That is nearly 8 dB of spread. Anything down at -12 sits under the
explosions while anything up at -5 is already near the ceiling and cannot be
turned up in the mixer without clipping. That is why some tracks disappear
in play and others do not.

WHAT THIS DOES, PER TRACK
  1. acompressor  - 4:1 above -18 dB, 20 ms attack, 250 ms release.
                    Pulls the peaks down so the average can come up. On a guitar
                    take this is what stops a strummed accent burying the riff
                    underneath it.
  2. loudnorm     - EBU R128 two-pass to a fixed target, so every track arrives
                    at the SAME perceived level rather than the same peak.
  3. alimiter     - a true-peak ceiling at -1.0 dBTP so nothing clips on
                    playback, which matters because the game mixes SFX on top.

TARGET: -10 LUFS integrated.
  Streaming platforms use -14. Game music that has to survive gunfire sits
  louder. -10 puts every track above the loudest current one (-11.8 for the
  jungle theme) while leaving 1 dB of true-peak headroom for the SFX bus.

TWO PASSES, NOT ONE. loudnorm in single-pass mode guesses at the input and
drifts; measuring first and feeding the numbers back gets the target within
about 0.2 LU. The measure pass is where most of the runtime goes.

Nothing is deleted. The originals move to _superseded/music_original/ with a
ledger, so any track can be restored if a master turns out worse than its source.
"""
import json, os, re, shutil, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TARGET_I = -10.0        # LUFS integrated
TARGET_TP = -1.0        # dBTP ceiling
TARGET_LRA = 9.0        # loudness range


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def measure(path):
    """First loudnorm pass - returns the JSON stats ffmpeg needs for pass two."""
    r = run(['ffmpeg', '-hide_banner', '-i', path,
             '-af', f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json',
             '-f', 'null', '-'])
    m = re.search(r'\{[^{}]*"input_i"[\s\S]*?\}', r.stderr)
    return json.loads(m.group(0)) if m else None


def master(src, dst, stats):
    """Compressor -> measured loudnorm -> true-peak limiter -> mp3."""
    ln = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
          f":measured_I={stats['input_i']}:measured_TP={stats['input_tp']}"
          f":measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}"
          f":offset={stats['target_offset']}:linear=false:print_format=summary")
    # linear=true only applies a flat gain, and when the gain it needs would clip
    # it quietly gives up and drifts. First run: tracks already at -5 LUFS came
    # out at -14 to -16, LOUDER sources ending up QUIETER than the quiet ones.
    # linear=false lets loudnorm compress into the target, which is what a track
    # that is already near the ceiling actually needs.
    chain = ('acompressor=threshold=-16dB:ratio=3:attack=20:release=250,'
             + ln + ',alimiter=limit=0.891:level=false')      # 0.891 ~= -1.0 dBTP
    r = run(['ffmpeg', '-hide_banner', '-y', '-i', src, '-af', chain,
             '-c:a', 'libmp3lame', '-b:a', '160k', '-ar', '44100', dst])
    return r.returncode == 0 and os.path.exists(dst)


def loudness_of(path):
    r = run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    m = re.findall(r'I:\s*(-?[\d.]+)\s*LUFS', r.stderr)
    return float(m[-1]) if m else None


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()

    # every distinct music file the manifest points at
    tracks = sorted(set(p for k, p in re.findall(r'"([a-zA-Z0-9_]+)":"(assets/music/[^"]+)"', man)))
    print('music tracks registered: %d' % len(tracks))

    arch = os.path.join(ROOT, '_superseded/music_original')
    os.makedirs(arch, exist_ok=True)
    ledger, done, failed = [], [], []

    for rel in tracks:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            continue
        before = loudness_of(src)
        stats = measure(src)
        if not stats:
            failed.append((rel, 'could not measure'))
            continue
        # always land on .mp3 - the one .wav in the set is 9 MB for 47 seconds
        out_rel = os.path.splitext(rel)[0] + '.mp3'
        tmp = os.path.join(ROOT, out_rel + '.tmp.mp3')
        if not master(src, tmp, stats):
            failed.append((rel, 'encode failed'))
            if os.path.exists(tmp):
                os.remove(tmp)
            continue
        after = loudness_of(tmp)
        # keep the original before overwriting anything
        shutil.copy2(src, os.path.join(arch, os.path.basename(src)))
        ledger.append({'orig': rel, 'archived': '_superseded/music_original/' + os.path.basename(src),
                       'before_lufs': before, 'after_lufs': after})
        if out_rel != rel:
            os.remove(src)
            man = man.replace('"%s"' % rel, '"%s"' % out_rel)
        os.replace(tmp, os.path.join(ROOT, out_rel))
        done.append((out_rel, before, after, os.path.getsize(os.path.join(ROOT, out_rel))))

    open(man_path, 'w', encoding='utf-8').write(man)
    json.dump(ledger, open(os.path.join(ROOT, '_superseded/MUSIC_LEDGER.json'), 'w'), indent=1)

    print()
    print('  %-46s %8s -> %8s   size' % ('track', 'before', 'after'))
    for rel, b, a, sz in done:
        print('  %-46s %7.1f  -> %7.1f   %5.1f MB'
              % (os.path.basename(rel), b if b is not None else 0, a if a is not None else 0, sz / 1e6))
    if done:
        after_vals = [a for _, _, a, _ in done if a is not None]
        print()
        print('  mastered %d tracks   spread now %.1f LU (was 7.8)'
              % (len(done), max(after_vals) - min(after_vals)))
    if failed:
        print('  FAILED: %s' % failed)


if __name__ == '__main__':
    main()
