from pathlib import Path
import sys,ast,json,time,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
T=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'));SETUP=next(ast.literal_eval(n.value)for n in T.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='SETUP'for x in n.targets))
checks=[];errors=[]
def check(ok,name,data=None):
 checks.append(dict(ok=bool(ok),name=name,data=data));print(('OK 'if ok else'FAIL ')+name,flush=True)
def warm(p,keys):
 p.evaluate('(ks)=>{window.qaKeys=ks;ks.forEach(k=>XART.rdy(k));}',keys)
 for i in range(1500):
  ready=p.evaluate('()=>{if(typeof __stepRAF==="function")__stepRAF(16.667);stageLoadTick();return qaKeys.every(k=>XART.rdy(k));}')
  if ready:return
  # The existing loader queue advances on native RAF, including hidden title state.
  p.evaluate('()=>{if(window.__rafCb){const f=window.__rafCb;window.__rafCb=null;f(performance.now());}}')
  p.wait_for_timeout(20)
 raise RuntimeError('Art load timeout '+str(p.evaluate('qaKeys.filter(k=>!XART.rdy(k))')))
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (W/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1280,'height':900});p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'))
 p.on('pageerror',lambda e:(errors.append(str(e)),print('ERROR '+str(e),flush=True)))
 p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'DRAW ERROR'in m.text else None)
 p.goto('http://127.0.0.1:65042/game/index.html?quality=high&arsenal=1104',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=60000)
 print('BOOT '+str(p.evaluate('({sa:typeof SA114,fx:typeof CFX114,error:window.__bofDrawError})')),flush=True)
 p.evaluate(TRAP_RAF);print(TRAP_RAF[:700],flush=True)
 p.evaluate(SETUP,{'stage':5,'diff':'furious','pilot':'cole'})
 p.evaluate('()=>{CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=999999;_adaptiveSpawnT=999999;tryAdaptiveReinforcement=()=>{};subBossDone=subBossTriggered=aminiTriggered=true;curStage={...curStage,length:99999};gravityMode={...GRAVITY_SHIP_ACTIVE,narrative:false};furyShipWarm();run.spaceWeapon=3;run.spaceLevels=[1,1,1,1,1];sa114Warm();cfx114Warm(5);}')
 keys=p.evaluate('()=>Object.entries(CF114_ART.banks).filter(([id])=>/^(spread|plasma)_(?:[1-5]|muzzle|impact)$/.test(id)||/^(spread|plasma)_icon_[1-5]_(?:36|40|hit)$/.test(id)||/^(ring|smoke|column|fire|small|dust|cole_nuke|atomic)_/.test(id)).map(([,B])=>B.key)')
 warm(p,keys);shot(p,'boot-stage5')
 print('WARM '+str(len(keys)),flush=True)
 print('CANVASES '+str(p.evaluate('[...document.querySelectorAll("canvas")].map(c=>({id:c.id,w:c.width,h:c.height,rect:[c.getBoundingClientRect().width,c.getBoundingClientRect().height]}))')),flush=True)
 checks.extend(p.evaluate((W/'checks.js').read_text(encoding='utf-8-sig')));print('CHECKS '+str(len(checks))+' FAIL '+str([q for q in checks if not q['ok']]),flush=True)
 p.evaluate(SETUP,{'stage':5,'diff':'furious','pilot':'cole','kind':'siegebomber','mini':True})
 extra=p.evaluate("""()=>{const b=subBoss,H=b.hp,core=b._bomber?.core;run.spaceWeapon=4;run.spaceLevels[4]=5;const r={kind:'spaceLaser',_cf114:'plasma',x:b.x,y:b.y,w:20,h:20,dmg:200,lv:5,t:0};spaceDamageTarget(b,200,r);return{hpBefore:H,hpAfter:b.hp,coreBefore:core,coreAfter:b._bomber?.core,parts:b._bomber?.parts.map(p=>({hp:p.hp,max:p.max,id:p.id})),targetable:spaceTargets().includes(b)}}""")
 checks.append({'name':'real Stage5 bomber hull stays protected with live modular parts','ok':extra['hpBefore']==extra['hpAfter'] and extra['coreBefore']==extra['coreAfter'],'data':extra});print('MODULAR '+str(extra),flush=True)
 checks.append({'name':'Armory discovery persists across profile normalization','ok':p.evaluate("()=>{polishRememberItem('space_3');polishRememberItem('space_4');achievementReload();return !!achievementState.owned.arsenal_space_3&&!!achievementState.owned.arsenal_space_4;}" )})
 (W/'native-boot.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8')
 p.screenshot(path=str(W/'page-native.png'))
 b.close()
