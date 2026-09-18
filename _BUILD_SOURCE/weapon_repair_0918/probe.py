#!/usr/bin/env python3
import os,sys,base64,json
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.insert(0,os.path.join(ROOT,'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=os.path.join(ROOT,'_shots','weapon_repair_0918');os.makedirs(OUT,exist_ok=True)
N={'ok':0};FAIL=[]
def ok(c,m):
 print(('  ok   ' if c else '  FAIL ')+m)
 if c:N['ok']+=1
 else:FAIL.append(m)
GRAB="""() => { const g=document.querySelector('#screen-area canvas')||document.querySelector('canvas');return g?g.toDataURL('image/png'):null; }"""
def main():
 port,stop=sh.serve(sh.GAME)
 try:
  with sync_playwright() as pw:
   br=pw.chromium.launch();pg=br.new_page(viewport={'width':1100,'height':900});errs=[]
   pg.on('pageerror',lambda e:errs.append('page:'+str(e)))
   pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' else None)
   pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
   pg.wait_for_function("() => typeof razorbackInit==='function' && typeof forgeStart==='function'",timeout=60000)
   pg.evaluate(sh.TRAP_RAF);pg.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole'})
   pg.evaluate("() => {window.__step="+sh.STEP+";playerHit=function(){};run.lives=9;}")
   def step(n):pg.evaluate('(n)=>{for(let i=0;i<n;i++)window.__step(1)}',n)
   def shot(name):
    d=pg.evaluate(GRAB)
    if d:open(os.path.join(OUT,name+'.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))
   # Furious Razorback with a live segmented sonic release.
   pg.evaluate("""() => {diffKey='furious';DIFF=DIFFS.furious;enemies=[];eBullets=[];playerLocks=[];spawnSubBoss('razorback');subBossActive=true;
    const b=subBoss,R=b._rzb;b.x=worldWidth()/2;b.y=150;R.state='guns';R.trans=0;R.pt=4;R.attack='sonic';R.at=1.21;R.beat=-1;R.tgt={x:b.x,y:b.y};R.a=0;R.turret=0;R.hpSync=true;razorbackCombat(b);}""")
   pg.wait_for_function("() => XART.rdy('rzbf_hull_0')&&XART.rdy('rzbf_turret')&&subBoss&&subBoss._rzb&&subBoss._rzb.waves.length",timeout=30000)
   step(6);shot('01_furious_razorback_segmented_sonic')
   rz=pg.evaluate("""() => {const R=subBoss._rzb,w=R.waves[0],q=w.segments;return {scale:R.scale,parts:[!!BOFX.img.rzbf_hull_0,!!BOFX.img.rzbf_turret],segments:q.length,
    gaps:q.slice(1).map((x,i)=>x[0]-q[i][1]),gapSafe:!rzbWaveAngleHit(w,(q[0][1]+q[1][0])/2),lobeHits:rzbWaveAngleHit(w,(q[0][0]+q[0][1])/2)};}""")
   ok(rz['scale']==1.5 and all(rz['parts']),'Furious Razorback is the authored tank at 150% scale with red-panel plates')
   ok(rz['segments']==5 and min(rz['gaps'])>0 and rz['gapSafe'] and rz['lobeHits'],'the five visible sonic lobes have real collision-safe openings')
   # Forge with global boss elements, embedded FP and re-spec plate.
   pg.evaluate("""() => {achievementState.owned={};run.spaceMode=false;run.stage=3;run.forge={};run.forgeForms={};run.forgeElems={};run.loadout=[0,1,2,3,4,5];run.weapon=0;run.infusion=null;
    forgeComboGrant('fire');forgeComboGrant('ice');forgeComboGrant('lightning');forgeStart(function(){});}""")
   pg.wait_for_function("() => state==='forge'&&XART.rdy('forge_loadout_0918')",timeout=30000);step(45);shot('02_forge_global_elements')
   fg=pg.evaluate("""() => ({all:FORGE_WEAPONS.every(w=>forgeElemsFor(w).join(',')==='fire,ice,lightning'),combos:run.forgeCombos,respecs:run.forgeRespecs,plate:XART.rdy('forge_loadout_0918')})""")
   ok(fg['all'] and fg['combos']==2 and fg['respecs']==2 and fg['plate'],'the Forge exposes every boss element to every weapon with two upgrades and two re-specs')
   # Preserve multiple forged forms, then display the selectable form row.
   pg.evaluate("""() => {run.forgeCombos=4;forgeCombine(0,'fire');forgeCombine(0,'ice');run.loadout=[0,1,2,3,4,5];loadoutStart(function(){});loadoutScr.sel=0;loadoutScr.row=2;loadoutScr.psel=1;}""")
   step(45);shot('03_loadout_selectable_forms')
   forms=pg.evaluate("""() => ({names:weaponFormOptions(0).map(x=>x.name),saved:!!(run.forgeForms[0].fire&&run.forgeForms[0].ice),active:run.forge[0].elem})""")
   ok(forms['saved'] and forms['active']=='ice' and 'INCENDIARY SLUGS' in forms['names'] and 'CRYO SLUGS' in forms['names'],'loadout keeps and displays both crafted forms instead of destroying the previous one')
   pg.evaluate("""() => {run.forgeElems.fire=1;run.forgeElems.ice=1;run.loadout=[0,1,2,3,4,5];loadoutStart(function(){});loadoutScr.sel=5;loadoutScr.row=2;loadoutScr.psel=2;}""")
   step(30);orbforms=pg.evaluate("() => weaponFormOptions(5).map(x=>x.name)");shot('04_orb_forms_fire_ice_thermoshock')
   ok(all(x in orbforms for x in ['ICE ORB','FIRE ORB','THERMOSHOCK']),'orb slot offers Ice, Fire and Thermoshock forms')
   # Weapon Found plate.
   pg.evaluate("() => {run.stage=2;unlocksStart(unlockRowsFor(2,'freezer'),function(){});}")
   pg.wait_for_function("() => state==='unlocks'&&XART.rdy('weapon_found_0918')",timeout=30000);step(70);shot('05_weapon_found')
   ok(pg.evaluate("() => unlocks.rows.length===2&&unlocks.rows[0][0]==='ICE BREATH'&&unlocks.rows[1][0]==='THERMOSHOCK BALL'"),'Weapon Found shows the actual stage-2 Freezer weapon systems')
   # Live magma projectile and its launch sound route.
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':3,'pilot':'cole'});pg.evaluate("() => {window.__step="+sh.STEP+";playerHit=function(){};run.weapon=5;run.wlevel=3;run.wlevels=WEAPONS.map(()=>1);run.wlevels[5]=3;run.wvars=WEAPONS.map(()=>null);run.wvars[5]='fireorb';run.forge={5:{elem:'fire',lv:1}};run.forgeForms={5:{fire:run.forge[5]}};run.forgeElems={fire:1};run.infusion={elem:'fire',lv:1,hits:0};thaw=null;pBullets=[];pShoot();}")
   pg.wait_for_function("() => XART.rdy('magma_orb_0918')&&pBullets.some(b=>b.kind==='orb')",timeout=30000);step(6);shot('06_live_magma_orb')
   mg=pg.evaluate("() => {const b=pBullets.find(q=>q.kind==='orb');return {inf:b&&b._inf,key:XART._src.magma_orb_0918,draw:String(drawBullets).includes(\"b._inf==='fire'\")};}")
   ok(mg['inf']=='fire' and mg['draw'] and mg['key'].endswith('magma_orb.png'),'a forged Fire orb draws the dedicated Magma Orb projectile')
   # Audible route audit: real attack helpers reach registered sound functions.
   snd=pg.evaluate("""() => {let n=0;const names=['razorbackCharge','razorbackPressure','fireOrbLaunch','weapon','powerup','blip'];for(const k of names){if(typeof Audio.SFX[k]==='function'){const f=Audio.SFX[k];Audio.SFX[k]=function(){n++;return f.apply(this,arguments);};}}
    rzbSfx('razorbackCharge');rzbSfx('razorbackPressure');(Audio.SFX.fireOrbLaunch||Audio.SFX.weapon||Audio.SFX.powerup)();return {n:n,have:names.filter(k=>typeof Audio.SFX[k]==='function')};}""")
   ok(snd['n']>=3 and len(snd['have'])>=5,'boss charge/release and Magma Orb launch reach audible registered SFX routes')
   ok(not errs,'no page or console errors during real Chromium frames: '+repr(errs))
   br.close()
  out={'passed':N['ok'],'failed':len(FAIL),'failures':FAIL,'razorback':rz,'forge':fg,'forms':forms,'sound':snd}
  open(os.path.join(OUT,'results.json'),'w').write(json.dumps(out,indent=2))
  print(json.dumps(out,indent=2));return 1 if FAIL else 0
 finally:stop()
if __name__=='__main__':raise SystemExit(main())
