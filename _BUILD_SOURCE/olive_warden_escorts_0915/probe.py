"""Native Chromium proof for the Olive Warden Hard/Furious escorts."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'olive_warden_escorts_0915'
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(value,label):
        checks.append({'pass':bool(value),'label':label});print(('ok  ' if value else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)))
        page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000)
        page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        fight=page.evaluate("()=>window.__fight(4,'mini','yuri')")
        ok(fight.get('ok'),'native Stage-4 miniboss route opens in Chromium')
        page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};warnT=0;warnKind=null;stagePlan=[];waveIdx=0;
          enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];boss=null;bossActive=false;state=GS.PLAY;stateT=1;
          player.x=worldWidth()*.42;player.y=650;player.invuln=1e9;player.dead=false;
          window.__escortGets=[];const old=XART.get.bind(XART);XART.get=function(k){window.__escortGets.push(k);return old(k);};
          for(const k of ['nsb_olivewarden_intact','nsb_olive_carrier','s4w_drone_barrel_0','bpfx_proj_missile_0','mgcf_1_5'])XART.rdy(k);
        }""")
        for _ in range(240):
            ready=page.evaluate("()=>['nsb_olivewarden_intact','nsb_olive_carrier','s4w_drone_barrel_0','bpfx_proj_missile_0'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(30)
        ok(ready,'Warden, Olive Carrier, rotary barrel and missile art decode before capture')

        def setup(level):
            return page.evaluate("""k=>{run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];subBoss=null;subBossActive=false;
              eBullets=[];pBullets=[];spawnSubBoss('olivewarden');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=subBoss._s4war.homeY;
              subBoss._drawY=subBoss.y;subBoss.fireCd=999;subBossActive=true;for(let i=0;i<150;i++)stage4MiniDirector(subBoss,1/60);
              for(const d of subBoss._s4war.drones)if(!d.dead)d.fireCd=0;for(let i=0;i<3;i++)stage4MiniDirector(subBoss,1/60);
              return {count:subBoss._s4war.drones.length,roles:subBoss._s4war.drones.map(d=>d.role),summoned:subBoss._s4war.summoned};}""",level)
        def capture(name):
            page.evaluate("()=>{shake=0;window.__escortGets=[];drawWorld(0);}")
            detail=page.evaluate("""()=>({mode:subBoss._s4war.mode,gets:window.__escortGets.slice(),drones:subBoss._s4war.drones.map(d=>({role:d.role,x:d.x,y:d.y,active:d.active,hp:d.hp,shield:d.shield,shots:d.shots,art:d.art})),
              bullets:eBullets.filter(q=>q._s4EscortRole).map(q=>({role:q._s4EscortRole,kind:q._s4wKind,shootable:!!q._shootable,x:q.x,y:q.y}))})""")
            raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'{name}.png';path.write_bytes(base64.b64decode(raw));shots.append(path);return detail

        hard_setup=setup('hard');hard=capture('warden_escort_01_hard_pair')
        ok(hard_setup['count']==2 and hard_setup['roles']==['gunner','protector'],'Hard fields one stationary gunner and one player-like protector')
        ok(all(d['art']=='nsb_olive_carrier' and d['active']>=.99 for d in hard['drones']),'both Hard escorts use the authored matching Olive Carrier hull')
        ok('nsb_olive_carrier' in hard['gets'],'the live renderer requests the exact authored escort hull')
        ok(any(q['role']=='gunner' and q['kind']=='machine' for q in hard['bullets']),'the flank gunner releases mounted machine rounds')
        ok(any(q['role']=='protector' and q['kind']=='rocket' and q['shootable'] for q in hard['bullets']),'the protector releases a shootable committed missile')
        hit=page.evaluate("""()=>{const d=subBoss._s4war.drones[0],hp=d.hp,shield=d.shield;_lastHitX=d.x;_lastHitY=d.y;hitSubBoss(Math.max(1,Math.floor(shield*.25)),d.x,d.y);
          return {solid:subBossSolidAt(d.x,d.y),shieldBefore:shield,shieldAfter:d.shield,hpBefore:hp,hpAfter:d.hp};}""")
        ok(hit['solid'] and hit['shieldAfter']<hit['shieldBefore'] and hit['hpAfter']==hit['hpBefore'],'real miniboss hit routing damages the escort shield before its hull')

        furious_setup=setup('furious');furious=capture('warden_escort_02_furious_trio')
        ok(furious_setup['count']==3 and furious_setup['roles'].count('protector')==2,'Furious fields the complete three-escort formation')
        ok(all(d['shield']>0 and d['hp']>0 for d in furious['drones']),'each Furious escort owns independent shield and hull pools')
        ok(all(d['shots']>0 for d in furious['drones']),'all three Furious escorts contribute live weapon pressure')

        normal_setup=setup('normal')
        ok(normal_setup['count']==0 and not normal_setup['summoned'],'Normal keeps the approved solo Olive Warden fight')
        for path in shots:
            image=Image.open(path).convert('RGB');ok(image.size==(960,1024) and image.getbbox() is not None,f'{path.stem} is a non-empty native gameplay frame')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'hardSetup':hard_setup,'hard':hard,'hit':hit,'furiousSetup':furious_setup,'furious':furious,'normalSetup':normal_setup,'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)

if __name__=='__main__':main()
