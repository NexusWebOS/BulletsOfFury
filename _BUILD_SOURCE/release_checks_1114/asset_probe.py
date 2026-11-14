from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Release-checks-1114';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True);c=br.new_context();p=boot(c,port,5,errors,'mini');p.wait_for_function('()=>["attack","roll"].every(a=>Array.from({length:8},(_,i)=>"s8"+(a==="attack"?"atk":"roll")+"_armored_leech_"+i).every(k=>XART.rdy(k)))',timeout=60000)
  q=p.evaluate('''()=>({helpersShareOwner:BOF_DIFFICULTY_RULES_15.state===DR15&&typeof DR15.base.EHP==='function',cells:['atk','roll'].flatMap(a=>Array.from({length:8},(_,i)=>{const k='s8'+a+'_armored_leech_'+i,im=XART.get(k);return{k,root:XART.root(k),width:im.width,height:im.height}}))})''')
  assert q['helpersShareOwner']and len(q['cells'])==16 and all(r['root']=='nca_stage8_leech_recovery_1114'and r['width']==r['height']==256 for r in q['cells'])and not errors
  br.close()
finally:stop()
syntax=[]
for n in ['assets/difficulty_helpers_1114.js','assets/difficulty_rules_1101.js','assets/stage8_leech_recovery_1114.js','assets/stage5_bomber_assault_1114.js','assets/stage5_bomber_assault_art_1114.js','_BUILD_SOURCE/test_fl.js','_BUILD_SOURCE/test_difficulty_helpers_1114.cjs','_BUILD_SOURCE/test_mutator_1003.cjs','_BUILD_SOURCE/test_stage8_1003.cjs','_BUILD_SOURCE/test_campaign_focus_1004b.cjs','_BUILD_SOURCE/test_campaign_controls_1004h.cjs']:
 r=subprocess.run(['node','--check',str(R/n)],capture_output=True,text=True);assert r.returncode==0,r.stderr;syntax.append(n)
(O/'asset-helper-checks.json').write_text(json.dumps(dict(helpers=q['helpersShareOwner'],nativeCells=q['cells'],errors=errors,syntax=syntax),indent=2));print('All16 recovered cells decode in native XART; browser shares the early difficulty owner; all changed sources parse.',flush=True)
