from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');O=R/'_shots/kit_dialogue_1114';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.goto('http://127.0.0.1:8765/index.html?kit18ref');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 keys=p.evaluate("()=>[...PILOTS.map(p=>'pav_'+p.key),'ui20_dialogue-a','cd27_neutral_460',DP20.key,c113Compact('neutral',68)]")
 p.wait_for_function('ks=>ks.every(k=>XART.rdy(k))',arg=keys,polling=50)
 for k in keys:
  data=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png');}",k)
  (O/(k+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
 p.evaluate("()=>D1110.preview('post-4','cole')");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 q=p.evaluate("()=>{const tails=pf27TailParts('ship_cole');return {tail:tails,ship:d27ShipFrames('ship_cole')?.length,fn:pt11OpeningShip.toString(),box:dlgBox.toString().slice(0,180)};}")
 (O/'reference-info.json').write_text(json.dumps(q,indent=2));print(json.dumps(q));b.close()
