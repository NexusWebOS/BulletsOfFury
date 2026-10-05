"""Register the regression extension without changing the suite's CRLF bytes."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'_BUILD_SOURCE/test_fl.js';b=p.read_bytes()
line=b"require('./test_campaign_controls_1004h.cjs')(vm,ctxv,ok);\r\n"
if line not in b:
 anchor=b"require('./test_campaign_landscape_1004e.cjs')(vm,ctxv,ok);\r\n"
 assert anchor in b;b=b.replace(anchor,anchor+line);p.write_bytes(b)
# Old map review fixtures now use verified persistent demo slots, not silent no-ops.
for name in ['review_campaign_markers_1004f.py','review_campaign_stagex_1004g.py']:
 p=R/'_BUILD_SOURCE'/name;s=p.read_text(encoding='utf-8')
 if 'map4hPreviewStorage' not in s:
  anchor="(O/'review.html').write_text" if 'stagex' in name else "O=R/'_shots/campaign_markers_1004f';"
  at=s.index(anchor)
  s=s[:at]+"s=s.replace('w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};','w.map4hPreviewStorage();')\n"+s[at:]
  p.write_text(s,encoding='utf-8')
print('Registered slot regression with CRLF intact and repaired review storage.')
