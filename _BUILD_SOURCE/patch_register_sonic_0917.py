#!/usr/bin/env python3
"""register test_sonic_0917.cjs in test_fl.js (CRLF file) right after the forge section - single-line needle."""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, '_BUILD_SOURCE', 'test_fl.js')
s = open(p, 'rb').read()
needle = b"require('./test_forge_0917.cjs')(vm,ctxv,ok);\r\n"
add = b"require('./test_sonic_0917.cjs')(vm,ctxv,ok);\r\n"
if add in s:
    print('already registered'); raise SystemExit(0)
assert s.count(needle) == 1, 'forge registration line not found exactly once'
s = s.replace(needle, needle + add)
open(p, 'wb').write(s)
print('registered test_sonic_0917.cjs after test_forge_0917.cjs')
