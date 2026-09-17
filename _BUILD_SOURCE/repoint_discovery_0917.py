#!/usr/bin/env python3
"""repoint_discovery_0917.py - the discovery block asks the question Mike's rule made it about.

`forgeDiscovered()` used to list what had been SEEN in the field; since 0917 it lists what has been
EARNED from a boss, because seeing an element no longer licenses anything. Both of the pin's actual
claims are kept and re-driven through the new door:

  TABLE ORDER      - the element strip is drawn from this list, and one that reordered itself as
                     combinations were earned would move the cursor under the player's thumb
  A SHUT GATE HIDES - an element you own a combination for but cannot use yet is still not offered

and one claim is added, because it is the whole rule: a SEEN element does not appear here at all.
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

OLD = ('  /* ---- discovery ---- */\n'
       '  R(' + Q + 'run.forgeElems={};' + Q + ');\n'
       '  ok(R(' + Q + 'forgeDiscovered().length===0' + Q + "), 'nothing is discovered on a fresh run');\n"
       '  R(' + Q + "forgeDiscover('lightning'); forgeDiscover('fire'); forgeDiscover('dark');" + Q + ');\n')

NEW = ('  /* ---- what may be combined, and where it comes from (0917) ---- */\n'
       '  R(' + Q + 'run.forgeElems={}; var __ownD=achievementState.owned; achievementState.owned={};' + Q + ');\n'
       '  ok(R(' + Q + 'forgeDiscovered().length===0' + Q + "), 'nothing is combinable on a fresh profile');\n"
       '  /* [!] SEEING AN ELEMENT IN THE FIELD GRANTS NOTHING SINCE 0917 (Mike: "you dont unlock all\n'
       '     these weapon combination upgrades ... they drop from the boss"). It used to license that\n'
       '     element on all nine slots at once, which is exactly what he ruled out. */\n'
       '  R(' + Q + "forgeDiscover('toxic');" + Q + ');\n'
       '  ok(R(' + Q + "forgeDiscovered().indexOf('toxic')<0" + Q + '),\n'
       "     'an element merely SEEN in the field is not combinable - only an earned pair is');\n"
       '  R(' + Q + "forgeComboGrant('lightning',0); forgeComboGrant('fire',3); forgeComboGrant('dark',0);" + Q + ');\n')
rep(OLD, NEW)

OLDPIN = ('  ok(R(' + Q + 'JSON.stringify(forgeDiscovered())===' + "'[" + chr(92) + Q + 'fire'
          + chr(92) + Q + ',' + chr(92) + Q + 'lightning' + chr(92) + Q + "]'" + Q + '),\n'
          "     'forgeDiscovered() is in table order and hides a discovered element whose gate is shut');\n")
NEWPIN = (OLDPIN.replace("'forgeDiscovered() is in table order and hides a discovered element whose gate is shut'",
                         "'forgeDiscovered() is in table order and hides an EARNED element whose gate is shut (dark needs NEW GAME +)'")
          + '  /* and a pair is a pair: the element is on the slot it was earned for, and on no other */\n'
          '  ok(R(' + Q + "forgeElemsFor(0).indexOf('lightning')>=0 && forgeElemsFor(3).indexOf('lightning')<0" + Q + '),\n'
          "     'forgeElemsFor answers per SLOT - lightning was earned for the machine gun, not for the laser');\n"
          '  R(' + Q + 'achievementState.owned=__ownD;' + Q + ');\n')
rep(OLDPIN, NEWPIN)

open(p, 'wb').write(s.encode('utf-8'))
print('the discovery block asks about earned combinations now')
