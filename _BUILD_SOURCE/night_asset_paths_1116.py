from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/asset-paths';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:8765/index.html?night-paths=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 q=p.evaluate('''()=>{const rows=[];for(const[owner,obj]of[['XART',XART._src],['BOFX.img',BOFX.img]])for(const[key,original]of Object.entries(obj||{})){const root=XART.root(key),raw=XART._src[root]||BOFX.img?.[root]||original,path=typeof bofAssetPath==='function'?bofAssetPath(raw):raw;if(typeof path==='string'&&path.startsWith('assets/'))rows.push({owner,key,root,original,path:path.split('?')[0]});}return rows;}''');b.close()
missing=[a for a in q if not(R/a['path']).is_file()];report={'registeredLocalKeys':len(q),'uniquePaths':len(set(a['path']for a in q)),'missing':missing,'errors':errors,'scope':'Current runtime local XART and BOFX image registrations. Missing registrations are candidates until a current live owner is confirmed; retained legacy registrations may be inactive.'};(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2)[:9000])
