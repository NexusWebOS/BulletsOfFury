from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'_BUILD_SOURCE/test_fl.js';s=p.read_bytes();needle=b"require('./test_soul_bomb_1019.cjs')(vm,ctxv,ok);";assert needle in s
if b"require('./test_boss_redesign_1020.cjs')" not in s:s=s.replace(needle,needle+b"\r\nrequire('./test_boss_redesign_1020.cjs')(vm,ctxv,ok);",1)
p.write_bytes(s);print('Asset regressions added, original line endings preserved')
