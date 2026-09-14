from pathlib import Path
HERE=Path(__file__).resolve().parent
p=HERE.parents[1]/'_BUILD_SOURCE/test_fl.js'
b=p.read_bytes();marker=b"console.log('\\n============================================');"
assert b.count(marker)==1
addition=(HERE/'tests.js').read_text().replace('\r\n','\n').replace('\n','\r\n').encode()
if b'// ===== 298.'not in b:p.write_bytes(b.replace(marker,addition+b'\r\n'+marker))
print('Feedback regression checks appended with CRLF preserved')
