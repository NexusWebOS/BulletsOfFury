from pathlib import Path
p=Path('_BUILD_SOURCE/test_fl.js')
g=p.read_bytes().decode('utf-8')
for a,b in [
    ("SUBBOSS[6].kind==='tempestleviathan'", "SUBBOSS[6].kind==='tempestbrothers'"),
    ("_f220[6].kind==='tempestleviathan' && _f220[6].name==='TEMPEST LEVIATHAN'", "_f220[6].kind==='tempestbrothers' && _f220[6].name==='TEMPEST LEVIATHAN BROTHERS'"),
    ("=== 'tempestleviathan', \"stage 6's miniboss", "=== 'tempestbrothers', \"stage 6's miniboss"),
    ("debugFightFor(6,'mini').kind==='tempestleviathan' && debugBossName('tempestleviathan')==='TEMPEST LEVIATHAN'", "debugFightFor(6,'mini').kind==='tempestbrothers' && debugBossName('tempestbrothers')==='TEMPEST LEVIATHAN BROTHERS'")
]:
    assert a in g,a
    g=g.replace(a,b)
marker="console.log('\\n============================================');"
assert g.count(marker)==1
block=Path('_BUILD_SOURCE/tempest_source_0913/qa-tests.js').read_text(encoding='utf-8')
g=g.replace(marker,block.replace('\r\n','\n').replace('\n','\r\n')+'\r\n'+marker)
p.write_bytes(g.encode('utf-8'))
print('Updated intentional Stage 6 pins and added 20 native duo behavior checks.')
