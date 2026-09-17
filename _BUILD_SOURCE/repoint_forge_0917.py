#!/usr/bin/env python3
"""repoint_forge_0917.py - section 370 owns its combinations before it combines them.

Its rules block combined fire and ice onto the machine gun on a bare profile, which was correct while
ANY seen element could be welded onto ANY slot. Since Mike's 0917 rule ("you dont unlock all these
weapon combination upgrades ... they drop from the boss") the pair has to have been earned, so the
block grants the two pairs it is about, and adds the refusal for one it does not own - the rule
itself, tested where the rest of the rules are.

⚠ The anchors are built from pieces rather than written as one literal: the line they match ends in
a quote character, and a Python triple-quoted string cannot end in one.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, '_BUILD_SOURCE', 'test_forge_0917.cjs')
s = open(p, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in s else '\n'
Q = chr(34)

def rep(a, b, n=1):
    global s
    a = a.replace('\n', nl); b = b.replace('\n', nl)
    c = s.count(a)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, a[:80])
    s = s.replace(a, b)

SETUP = ('  R(' + Q + 'run.forge={}; run.forgeElems={}; run.loadout=null; run.forgeCombos=2; '
         'run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false;' + Q + ');\n')
GRANT = ('  /* A COMBINATION IS EARNED FROM A BOSS (Mike, 0917), so the pairs this block is about are\n'
         '     granted first - and one it is NOT given proves the gate is real rather than absent. */\n'
         '  R(' + Q + 'var __ownBefore=achievementState.owned; achievementState.owned={}; '
         "forgeComboGrant('fire',0); forgeComboGrant('ice',0);" + Q + ');\n'
         '  ok(R(' + Q + "forgeCombine(0,'toxic')==='locked' && !run.forge[0]" + Q + '),\n'
         "     'a combination that has not been earned is refused, and forges nothing');\n")
rep(SETUP, SETUP + GRANT)

RESPEC = ('  ok(R(' + Q + "forgeRespec(0)==='ok' && !run.forge[0] && run.forgeRespecs===1 && "
          "!run.infusion && weaponDisplayName(0)==='MACHINE GUN'" + Q + '),\n'
          "     'forgeRespec removes the element, spends a re-spec, clears the held element and restores the bare name');\n")
rep(RESPEC, RESPEC + '  R(' + Q + 'achievementState.owned=__ownBefore;' + Q + ');   '
    '/* the profile is left as this section found it */\n')

open(p, 'wb').write(s.encode('utf-8'))
print('section 370 earns its combinations first')
