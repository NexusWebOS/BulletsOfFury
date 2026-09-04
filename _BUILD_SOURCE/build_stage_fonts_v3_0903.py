#!/usr/bin/env python3
"""
build_stage_fonts_v3_0903.py - restore the nine authored stage alphabets as ONE packed face sheet.

    python _BUILD_SOURCE/build_stage_fonts_v3_0903.py            # report, write nothing
    python _BUILD_SOURCE/build_stage_fonts_v3_0903.py --write    # build the sheet + manifest block

Mike (0903, with four screenshots of the pilot screen): "remove these old fonts, replace with the
better stage fonts asap."

WHAT THE OLD ONES ARE. The pilot screen draws its heading and the pilot's name through
`pilotFont(P.font)`, which returns `ASSETS.stageArt[N]` - the alphabet embedded in that stage's
CARD sheet. Those are incomplete: stage 5 carries 44 glyphs and has NO LETTER S, which is why
Mike's Juggernaut screenshot says CHOO E YOUR PILOT. Stages 1/3/4 carry 45, stage 2 carries 58,
and stages 6-9 have no card alphabet at all.

WHAT THE BETTER ONES ARE. `stagefont1..9_v3.png` - nine 2688x1152 sheets, 47 glyphs each
(A-Z 0-9 . , ! ? - : + / % ' ( ) ), one authored face per stage. They were deleted from disk on
2026-08-31 (58252627, the cinematic/boss overhaul) and their sliced atlas cells `sfont<N>_<char>`
were unregistered and pixel-cleared on 2026-09-02 (dfeff4ce, retire_legacy_password_fonts.py).
Nothing replaced them: `A.stageFont` became a plain alias of `A.stageArt`.

⚠ THE PIXELS ARE STILL IN GIT and this reads them from there - commit 58252627^, the last tree
where the cells are intact. `BOFX.sfontv3` (name, cap 254, and a 47-entry advance table per stage)
was never removed, so the metrics survived the art.

WHAT THIS BUILDS. One sheet, `assets/game/atlas/fonts_stage.png`, holding all nine faces trimmed to
their ink and scaled to a 96px cap - above the largest size any caller draws (H=44 on a 2x backing store =
88 device px), so nothing is ever upscaled, and a fraction of the 27.9 Mpx the nine originals cost. It emits
`BOF.stageFontV3`, shaped exactly like a `stageArt` entry (`{atlas, frames, font}`) so `stageText`,
`glyphBox` and `fontCapH` consume it unchanged.

⚠ TIGHT INK BOXES ARE THE CONTRACT, NOT A CHOICE. `glyphBox` derives the cap from the tallest
letter frame and bottom-aligns every glyph in that box, with FONT_RIDE/FONT_DESC placing the marks
(drop 0822a). A frame with padding would shift its glyph off the baseline by the padding.

⚠ AND THE MAGENTA IN STAGES 5 AND 9 IS AUTHORED, NOT A HALO. Measured: 147,334 of stage 5's
147,365 magenta pixels are INTERIOR (the face is purple), and 39,457 of 39,465 on stage 9. The
standing rule converts an OUTER-BOUNDARY halo to a black edge and leaves interior colour alone;
there are 31 and 8 edge pixels respectively, i.e. none. Nothing is recoloured here.
"""
import io, os, re, sys, json, math, subprocess, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
os.chdir(GAME)
WRITE = '--write' in sys.argv
SRC_COMMIT = '58252627^'          # last tree where the sfont<N>_<char> cells are intact
OUT_PNG = 'assets/game/atlas/fonts_stage.png'
CAP_TARGET = 96                   # px. MEASURED, not guessed: the largest stageText in the game is
                                  # H=44 on a 2x backing store = 88 device px, so 96 upscales nothing.
                                  # (H=58 is the 3-2-1 countdown, which is msgText on the stage-1 card
                                  # alphabet, not this face.) 128 cost 6.9 MB for headroom nobody uses.
PAD = 2
GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?-:+/%'()"

from PIL import Image


def safe_name(ch):
    return ch if re.match(r'^[A-Za-z0-9]$', ch) else ('p%02d' % ord(ch))


def git_show(path):
    r = subprocess.run(['git', 'show', '%s:%s' % (SRC_COMMIT, path)], capture_output=True)
    if r.returncode != 0: raise SystemExit('git show failed for %s: %s' % (path, r.stderr[:200]))
    return r.stdout


def load_old_cells():
    """the sfont<N>_<char> cell table from the source commit's manifest"""
    src = git_show('assets/manifest.js').decode('utf-8')
    m = re.search(r'window\.BOFX\s*=\s*', src); i = m.end(); d = 0; j = i
    while True:
        c = src[j]
        if c in '{[': d += 1
        elif c in '}]':
            d -= 1
            if d == 0: break
        j += 1
    X = json.loads(src[i:j + 1])
    return {k: v for k, v in X['cells'].items() if re.match(r'^sfont[1-9]_', k)}


def main():
    cells = load_old_cells()
    print('recovered %d sfont cells from %s' % (len(cells), SRC_COMMIT))
    per = collections.Counter(k.split('_')[0] for k in cells)
    print('  per stage:', dict(sorted(per.items())))

    sheets = {}
    def sheet(n):
        if n not in sheets:
            import tempfile
            data = git_show('assets/game/atlas/nca_%d.png' % n)
            sheets[n] = Image.open(io.BytesIO(data)).convert('RGBA')
        return sheets[n]

    # ---- cut, trim to ink, scale to the target cap -------------------------------------------
    faces = collections.defaultdict(dict)          # stage -> char -> trimmed Image
    for key, c in cells.items():
        st, safe = key.split('_', 1)
        stage = st[5:]
        ch = safe if len(safe) == 1 else chr(int(safe[1:]))
        im = sheet(c[0]).crop((c[1], c[2], c[1] + c[3], c[2] + c[4]))
        bb = im.getbbox()
        if bb is None: continue                     # a glyph with no ink cannot be drawn
        faces[stage][ch] = im.crop(bb)
    for stage in sorted(faces, key=int):
        caps = [im.height for ch, im in faces[stage].items() if ch.isalnum()]
        cap = max(caps) if caps else 0
        sc = CAP_TARGET / cap
        for ch, im in list(faces[stage].items()):
            w = max(1, int(round(im.width * sc))); h = max(1, int(round(im.height * sc)))
            faces[stage][ch] = im.resize((w, h), Image.LANCZOS)
        print('  stage %s: %2d glyphs, source cap %d -> %d  (missing: %s)'
              % (stage, len(faces[stage]), cap, CAP_TARGET,
                 ''.join(sorted(set(GLYPHS) - set(faces[stage]))) or 'none'))

    # ---- pack: shelves, tallest first, near-square sheet --------------------------------------
    items = [(st, ch, im) for st in sorted(faces, key=int) for ch, im in faces[st].items()]
    items.sort(key=lambda t: (-t[2].height, -t[2].width))
    area = sum((im.width + PAD) * (im.height + PAD) for _, _, im in items)
    W = max(int(math.ceil(math.sqrt(area * 1.06) / 32) * 32), max(im.width for _, _, im in items) + PAD)
    x = y = rowh = 0; placed = []
    for st, ch, im in items:
        if x + im.width + PAD > W: x = 0; y += rowh + PAD; rowh = 0
        placed.append((st, ch, im, x, y)); x += im.width + PAD; rowh = max(rowh, im.height)
    H = y + rowh + PAD
    print('sheet: %dx%d (%.2f Mpx), %d glyphs, fill %.0f%%'
          % (W, H, W * H / 1e6, len(placed), 100 * sum(im.width * im.height for _, _, im, _, _ in placed) / (W * H)))

    frames = {}; font = collections.defaultdict(dict)
    for st, ch, im, px, py in placed:
        nm = 'sf%s_%s' % (st, safe_name(ch))
        frames[nm] = [px, py, im.width, im.height]
        font[st][ch] = nm

    if not WRITE:
        print('\nDRY RUN - nothing written. Re-run with --write.')
        return

    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for st, ch, im, px, py in placed: out.paste(im, (px, py))
    out.save(OUT_PNG, optimize=True)
    print('wrote %s  %.2f MB' % (OUT_PNG, os.path.getsize(OUT_PNG) / 1048576))

    # ---- manifest: BOF.stageFontV3, one entry per stage, all pointing at the one sheet --------
    man = io.open('assets/manifest.js', 'rb').read()
    mi = man.find(b'window.BOF='); ms = mi + len(b'window.BOF=')
    depth = 0; me = ms
    while True:
        c = man[me:me + 1]
        if c in (b'{', b'['): depth += 1
        elif c in (b'}', b']'):
            depth -= 1
            if depth == 0: break
        me += 1
    B = json.loads(man[ms:me + 1].decode('utf-8'))
    B['stageFontV3'] = {st: {'atlas': OUT_PNG, 'frames': {n: frames[n] for n in sorted(font[st].values())},
                             'font': font[st]} for st in sorted(font, key=int)}
    body = json.dumps(B, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    io.open('assets/manifest.js', 'wb').write(man[:ms] + body + man[me + 1:])
    print('manifest: BOF.stageFontV3 registered for stages %s' % ', '.join(sorted(font, key=int)))


if __name__ == '__main__':
    main()
