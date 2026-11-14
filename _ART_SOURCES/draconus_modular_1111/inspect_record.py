from pathlib import Path
import json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/Draconus-rotor-and-full-stages';r=json.loads((O/'stage-8/report.json').read_text())
with sync_playwright()as p:
 b=p.chromium.connect_over_cdp('http://127.0.0.1:'+str(r['diagnostics']['debugport']),timeout=10000)
 page=next(p for c in b.contexts for p in c.pages if '/index.html'in p.url)
 data=page.evaluate('''()=>{const B=boss,J=B?._r30&&j3State(B);return{state,mode:B?._r30?.mode,form:B?._r30?.v18?.form,hp:B?.hp,copies:J?.hp,modules:J?.modules?.map(a=>a?.map(p=>({id:p.id,hp:p.hp,dead:p.destroyed}))),rotor:DGM1111.last,snapshot:film1111Snapshot()}}''')
 (O/'stage-8/inspection.json').write_text(json.dumps(data,indent=2));print(json.dumps(data),flush=True)
