#!/usr/bin/env python3
"""
DROP 0813G - WHAT IS DEFINED BUT NEVER SPAWNED?

Mike: "show me what unused mini bosses and bosses and enemies we got left."

Needed because pulling siege ember (stage 2) and thorn rime (stage 3) and moving blacksteel to
stage 6 leaves THREE miniboss slots empty, and only five units carry mini:true.

DEFINED is read from the tables; USED is read from the call sites. A unit counts as used if any of
these name it:
    spawnEnemy('x')      the wave scripts
    spawnBoss('x')       boss spawns
    SUBBOSS   kind:'x'   per-stage miniboss assignment
    STAGES    boss:'x'   per-stage boss assignment

⚠ DEFINED-BUT-UNSPAWNED IS NOT THE SAME AS USABLE. A type can be unspawned because its art was
never wired (herald's mba_vr_ plates are NOT in XART, per game.js:13697) rather than because it is
spare. The art check is a separate pass - this script only says what the CODE reaches.
"""
import os, re, io, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
G = io.open(os.path.join(ROOT, 'assets', 'game.js'), encoding='utf-8', errors='ignore').read()

# ---- DEFINED -------------------------------------------------------------
def table_keys(name):
    m = re.search(r'const\s+%s\s*=\s*\{' % re.escape(name), G)
    if not m: return []
    i = m.end() - 1
    depth = 0
    for j in range(i, len(G)):
        if G[j] == '{': depth += 1
        elif G[j] == '}':
            depth -= 1
            if depth == 0:
                body = G[i+1:j]; break
    else:
        return []
    # top-level keys only
    keys, d = [], 0
    for line in body.split('\n'):
        stripped = line.strip()
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*:', stripped)
        if d == 0 and mm: keys.append(mm.group(1))
        d += line.count('{') - line.count('}')
    return keys

SHIPBOSS = table_keys('SHIPBOSS')
ROSTERS = {}
for t in ('S1_TANKS', 'S1_JETS', 'SEWER', 'VOLC', 'S1_NAVAL', 'S1_AIR'):
    ks = table_keys(t)
    if ks: ROSTERS[t] = ks

# enemy types are the case labels inside spawnEnemy's switch
spawn_i = G.find('function spawnEnemy')
spawn_body = G[spawn_i: spawn_i + 200000] if spawn_i >= 0 else ''
CASES = sorted(set(re.findall(r"case\s+'([a-zA-Z0-9_]+)'\s*:", spawn_body)))

# legacy bosses: case labels in spawnBoss
boss_i = G.find('function spawnBoss')
boss_body = G[boss_i: boss_i + 40000] if boss_i >= 0 else ''
BOSS_CASES = sorted(set(re.findall(r"case\s+'([a-zA-Z0-9_]+)'\s*:", boss_body)))

# ---- USED ----------------------------------------------------------------
used = set()
used |= set(re.findall(r"spawnEnemy\(\s*'([a-zA-Z0-9_]+)'", G))
used |= set(re.findall(r"spawnBoss\(\s*'([a-zA-Z0-9_]+)'", G))
used |= set(re.findall(r"kind\s*:\s*'([a-zA-Z0-9_]+)'", G))
used |= set(re.findall(r"boss\s*:\s*'([a-zA-Z0-9_]+)'", G))
used |= set(re.findall(r"spawnSubBoss__inner\(\s*'([a-zA-Z0-9_]+)'", G))

# per-stage assignments, for the report
sub = dict(re.findall(r"(\d+)\s*:\s*\{at:[^}]*kind:'([a-zA-Z0-9_]+)'", G))
stage_boss = re.findall(r"n:(\d+)[^}]*?boss:'([a-zA-Z0-9_]+)'", G, re.S)

print('=== CURRENT ASSIGNMENTS ===')
sb = {int(k): v for k, v in sub.items()}
bb = {int(k): v for k, v in stage_boss}
print('%-7s %-22s %s' % ('stage', 'boss', 'miniboss'))
for s in range(1, 10):
    if s in bb or s in sb:
        print('%-7d %-22s %s' % (s, bb.get(s, '-'), sb.get(s, '-')))

print('\n=== SHIPBOSS UNITS (the nsb_ family) ===')
for k in SHIPBOSS:
    where = []
    for s, v in sb.items():
        if v == k: where.append('mini s%s' % s)
    for s, v in bb.items():
        if v == k: where.append('BOSS s%s' % s)
    print('  %-18s %s' % (k, ', '.join(where) if where else '*** UNUSED'))

print('\n=== LEGACY BOSSES (spawnBoss switch) ===')
for k in BOSS_CASES:
    where = [('BOSS s%s' % s) for s, v in bb.items() if v == k]
    print('  %-18s %s' % (k, ', '.join(where) if where else '*** not assigned to a stage'))

print('\n=== ENEMY TYPES DEFINED BUT NEVER SPAWNED ===')
unspawned = [c for c in CASES if c not in used]
if not unspawned:
    print('  (none - every case in spawnEnemy is reached)')
else:
    for c in unspawned: print('  %s' % c)
    print('\n  %d of %d enemy cases are never spawned' % (len(unspawned), len(CASES)))

for t, ks in ROSTERS.items():
    un = [k for k in ks if k not in used]
    print('\n=== %s: %d/%d unused ===' % (t, len(un), len(ks)))
    if un: print('  ' + ', '.join(un))
