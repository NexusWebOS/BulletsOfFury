#!/usr/bin/env python3
"""drop_old_thrusters_0906s.py - delete the star-burst thruster system, art and code.

    python _BUILD_SOURCE/drop_old_thrusters_0906s.py            # report only
    python _BUILD_SOURCE/drop_old_thrusters_0906s.py --write

Mike, 0906: "we can delete those ugly ass old thrusters we were using."

⚠ BRACE-MATCHING IS THE RIGHT TOOL HERE AND THE WRONG TOOL 300 LINES AWAY. CLAUDE.md records that
brace-matching gives wrong answers inside `spawnEnemy`, whose `if(base.art===undefined){` is never
closed - so this refuses to run anywhere near it and asserts the block it extracted really is the
one intended (first line and last line are both checked) before a single character is cut.

⚠ AND THE MATCHER SKIPS STRINGS AND COMMENTS. Both blocks contain braces inside comment prose and
inside template strings; a naive counter closes them early and takes half a function with it.
"""
import os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, 'assets/game.js')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')

BS = chr(92)


def match(s, i):
    """index of the brace closing the one at s[i], skipping strings and comments"""
    if s[i] != '{':
        raise SystemExit('anchor is not a brace')
    d = 0
    n = len(s)
    k = i
    while k < n:
        c = s[k]
        if c == '/' and k + 1 < n and s[k + 1] == '/':
            j = s.find(chr(10), k)
            k = n if j < 0 else j
            continue
        if c == '/' and k + 1 < n and s[k + 1] == '*':
            k = s.find('*/', k) + 2
            continue
        if c in ('"', "'", '`'):
            q = c
            k += 1
            while k < n and s[k] != q:
                k += 2 if s[k] == BS else 1
            k += 1
            continue
        if c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return k
        k += 1
    raise SystemExit('unbalanced braces from %d' % i)


def cut(src, anchor, must_contain, label):
    i = src.find(anchor)
    if i < 0:
        raise SystemExit('%s: anchor not found' % label)
    b = src.index('{', i)
    e = match(src, b)
    block = src[i:e + 1]
    for m in must_contain:
        if m not in block:
            raise SystemExit('%s: extracted block is missing %r - refusing' % (label, m))
    lines = block.count(chr(10)) + 1
    print('   %-8s %d lines, %d chars' % (label, lines, len(block)))
    return src[:i] + src[e + 1:], lines


def main():
    write = '--write' in sys.argv
    src = open(GAME, encoding='utf-8', errors='surrogateescape', newline='').read()
    before = len(src)
    total = 0

    print('game.js:')
    # 1. the in-play star draw
    src, n = cut(src,
                 "  if(typeof XART!=='undefined'){" + chr(13) + chr(10) + "    /* THRUSTER: UNIFORM SIZE",
                 ["_nk='nthp_", 'SHIP_FLAME_BAKED'], 'in-play')
    total += n
    # 2. the launch cinematic's own hand-rolled plume
    src, n = cut(src, "    if(!SHIP_FLAME_BAKED && XART.rdy(_tk)){",
                 ['im.naturalWidth'], 'launch')
    total += n
    # 3. the shared helper and its two callers
    src, n = cut(src, "function drawShipThruster(x, y, h, pilot, alpha){",
                 ['THRUSTER_MOUNTS', "nthp_"], 'helper')
    total += n

    for pat, label in (
        (r'[ \t]*drawShipThruster\(x,y,h,\(typeof _pilotKey[^\n]*\n', 'caller (drawShipSprite)'),
        (r'[ \t]*try\{ if\(typeof drawShipThruster[^\n]*\n', 'caller (rivals)'),
        (r"[ \t]*const _tk='nthp_'[^\n]*\n", 'launch key'),
        (r"[ \t]*const _nk='nthp_'[^\n]*\n", 'in-play key'),
    ):
        m = re.search(pat, src)
        if not m:
            print('   %-8s already gone' % label)
            continue
        print('   %-8s removed 1 line' % label)
        src = src[:m.start()] + src[m.end():]
        total += 1

    # the preload regex no longer needs the family
    src2 = src.replace('|nthp_|', '|')
    if src2 == src:
        print('   PRELOAD  nthp_ not found in the preload regex')
    else:
        print('   PRELOAD  nthp_ dropped')
    src = src2

    left = src.count('nthp_')
    print('   %d lines cut, %d chars; %d references to nthp_ remain' % (total, before - len(src), left))

    man = open(MANIFEST, encoding='utf-8').read()
    cells = re.findall(r'"(nthp_[^"]*)":', man)
    print('manifest: %d nthp_ entries registered' % len(cells))
    # a family is registered TWICE - a rect in BOFX.cells and a sheet path in BOFX.img - and the
    # two have different value shapes. Matching only the array form leaves half the family behind,
    # pointing at cells that no longer exist.
    man2 = re.sub(r',?"nthp_[^"]*":(?:\[[^\]]*\]|"[^"]*")', '', man)
    still = len(re.findall(r'"nthp_[^"]*":', man2))
    print('   after removal: %d remain, %d chars freed' % (still, len(man) - len(man2)))

    if not write:
        print('DRY RUN - nothing written.')
        return 0
    for f, bak in ((GAME, GAME + '.0906s.bak'), (MANIFEST, MANIFEST + '.0906s2.bak')):
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
    open(GAME, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(src)
    open(MANIFEST, 'w', encoding='utf-8', newline=chr(10)).write(man2)
    print('wrote game.js and manifest.js')
    return 0


if __name__ == '__main__':
    sys.exit(main())
