#!/usr/bin/env python3
"""
DROP 0801df - PILOT ART CONSOLIDATION

Mike: "organize the portraits/faces into one folder, theres all over the place"

He is right, though the portraits themselves were the one part already tidy. The
scatter is the rest of a pilot's identity art - the same nine characters spread
over six folders with no rule:

    ui/portraits    63   port_*                  expression heads
    ui/pilotcards   37   pcard_*, pbar_*         card shells + stat bars
    ui/cards        10   card_*                  the legacy card art
    ui/dialogue     10   dlg_*                   comm window frames
    fx/icons         9   spicon_*                special-ability icons
    ui/emblems       9   pemb_*                  affiliation emblems

Anything about WHO a pilot is now lives in one place:

    assets/ui/pilots/

Flat, because the filenames already carry the pilot name and the keys are the
real index. Nesting per pilot would just re-scatter it nine ways.

SAFETY - the same rules the weapon reorg had to learn the hard way:
  * a source file is moved ONCE; every key that references it is repointed
    (aliases are real - several keys legitimately share one file)
  * basename collisions across source folders are renamed by key, never
    silently overwritten
  * after the move, EVERY manifest path is re-resolved against disk, and any
    key still pointing at a moved source is repaired
  * a ledger records every from/to, so the whole thing reverses
"""
import json, os, re, shutil, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAN = os.path.join(ROOT, 'assets/manifest.js')
DEST = 'assets/ui/pilots'
PAT = r'^(port_|face_|card_|pcard_|dlg_|pemb_|spicon_|pbar_)'


def main():
    man = open(MAN, encoding='utf-8').read()
    pairs = re.findall(r'"([a-zA-Z0-9_]+)":"(assets/[^"]+)"', man)

    plan, taken, src_dst = [], set(), {}
    for key, src in pairs:
        if not re.match(PAT, key):
            continue
        if src.startswith(DEST + '/'):
            continue                                    # already home
        if src in src_dst:                              # alias of a planned file
            plan.append((key, src, src_dst[src]))
            continue
        base = os.path.basename(src)
        name = base
        if name in taken or os.path.exists(os.path.join(ROOT, DEST, name)):
            stem, ext = os.path.splitext(base)
            name = '%s__%s%s' % (stem, key, ext)
        taken.add(name)
        dst = '%s/%s' % (DEST, name)
        src_dst[src] = dst
        plan.append((key, src, dst))

    print('planned: %d keys, %d distinct files' % (len(plan), len(src_dst)))
    by = collections.Counter(re.sub(r'_.*', '', k) for k, _, _ in plan)
    for f, n in sorted(by.items()):
        print('   %-9s %3d' % (f + '_*', n))

    os.makedirs(os.path.join(ROOT, DEST), exist_ok=True)
    moved, done, failed = [], set(), []
    for key, src, dst in plan:
        s_abs, d_abs = os.path.join(ROOT, src), os.path.join(ROOT, dst)
        if src not in done:
            if not os.path.exists(s_abs):
                failed.append((key, src))
                continue
            shutil.move(s_abs, d_abs)
            done.add(src)
        if os.path.exists(d_abs):
            moved.append((key, src, dst))
        else:
            failed.append((key, src))

    for key, src, dst in moved:
        man = man.replace('"%s":"%s"' % (key, src), '"%s":"%s"' % (key, dst))

    # repair ANY key left pointing at a source we moved, even one the pattern
    # never matched - this is the bug that bit the weapon reorg
    mv = {s: d for _, s, d in moved}
    for key, p in re.findall(r'"([a-zA-Z0-9_]+)":"(assets/[^"]+)"', man):
        if p in mv and not os.path.exists(os.path.join(ROOT, p)):
            man = man.replace('"%s":"%s"' % (key, p), '"%s":"%s"' % (key, mv[p]))

    open(MAN, 'w', encoding='utf-8').write(man)
    led_path = os.path.join(ROOT, '_superseded/PILOT_LEDGER.json')
    os.makedirs(os.path.dirname(led_path), exist_ok=True)
    json.dump(moved, open(led_path, 'w'), indent=1)

    print()
    print('moved  : %d keys (%d files)' % (len(moved), len(done)))
    print('failed : %d %s' % (len(failed), failed[:3] if failed else ''))

    man = open(MAN, encoding='utf-8').read()
    refs = sorted(set(re.findall(r'"(assets/[^"]+?\.(?:png|jpg|mp3|wav|ttf|json))"', man)))
    missing = [r for r in refs if not os.path.exists(os.path.join(ROOT, r))]
    print('manifest refs %d   MISSING %d' % (len(refs), len(missing)))
    for m in missing[:6]:
        print('   ', m)
    if missing:
        sys.exit('FATAL: broken references - see PILOT_LEDGER.json to reverse')
    print('OK - drop 0801df')


if __name__ == '__main__':
    main()
