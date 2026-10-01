"""fix_sfx_arrays.py - give every take's sound log the files of the cues BOFA.sfx holds as VARIATION ARRAYS.

    python fix_sfx_arrays.py            # patch takes9/*/audio_events.json, delete their sfx.wav so they re-render

capture3.py's __audioDump (v7/v8) recorded a cue's file only when BOFA.sfx held a STRING, and five cues are arrays of
authored variations at runtime - missile, enemyMissile, nuclearLaunch, spaceVolleyLaunch, volleyLaunch - so every
one of those plays was logged, counted as played, and rendered as SILENCE ('skipped' in render_audio.py's counts).
The dump is fixed for new takes; this repairs takes already recorded, from the live table (inspect9.py).
"""
import os, sys, json, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = subprocess.run([sys.executable, os.path.join(HERE, 'inspect9.py'),
                          "(() => { const o = {}; for (const k in BOFA.sfx) if (Array.isArray(BOFA.sfx[k])) o[k] = BOFA.sfx[k]; return o; })()"],
                         capture_output=True, text=True, check=True).stdout
    arr = json.loads(out[out.index('{'):])
    print('array-valued sfx:', sorted(arr))
    n = 0
    for p in glob.glob(os.path.join(HERE, 'takes9', '*', 'audio_events.json')):
        a = json.load(open(p))
        ch = False
        for k, v in list(a.get('files', {}).items()):
            if v is None and k in arr:
                a['files'][k] = arr[k]
                ch = True
        if ch:
            json.dump(a, open(p, 'w'))
            n += 1
            w = os.path.join(os.path.dirname(p), 'sfx.wav')
            if os.path.exists(w):
                os.remove(w)
    print('patched %d takes' % n)


if __name__ == '__main__':
    main()
