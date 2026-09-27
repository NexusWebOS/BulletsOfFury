"""Real Chromium firing, muzzle pixels, hardpoint tracking and audio decode."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/muzzles_0926');out.mkdir(exist_ok=True,parents=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
RESET="""c=>{run.pilot=c.pilot||'cole';pilotIndex=PILOTS.findIndex(p=>p.key===run.pilot);run.weapon=c.weapon||0;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.forge={};run.forgeForms={};run.infusion=null;run.wvars=WEAPONS.map(()=>null);run.sonicT=0;run.dkT=0;run._dkCd=0;run.spaceMode=false;run.gravityShipReady=false;run._chainOverheat=0;run._chainHeat=0;special=null;gravityMode=null;lzMount=null;flame=null;rollers=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];wm26Releases=[];_navalFlashes=[];player.reset();player.x=worldWidth()/2;player.y=350;player.invuln=0;player.dead=false;player.out=false;player.roll=0;player.somer=null;player._dkMuz=null;camX=player.x-VW/2;stagePlan=[];waveIdx=999;spawnClock=9999;story=null;}"""
def shot(pg,name):
 pg.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 pg.wait_for_timeout(80);pg.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 data=pg.evaluate('()=>ctx.canvas.toDataURL()');(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1100})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True});pg.evaluate(RESET,{})
  pg.wait_for_function('()=>Object.values(WM26_REELS).flatMap(r=>Array.from({length:r.n},(_,i)=>XART.rdy(r.key+i))).every(Boolean)',timeout=60000)
  # Actual player firing across every pilot and ordinary weapon family.
  report['players']=[]
  for pilot in ['cole','axel','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
   for weapon in [0,1,2,3,5,7,8]:
    if weapon==8 and pilot!='yuri':continue
    pg.evaluate(RESET,{'pilot':pilot,'weapon':weapon})
    r=pg.evaluate("""()=>{yuriLightningOrbUnlocked=true;run._yuriOrbCd=0;pShoot();return {pilot:run.pilot,weapon:run.weapon,shots:pBullets.length,kinds:pBullets.map(q=>q.kind),flashes:wm26Releases.map(f=>({family:f.family,x:f.x,y:f.y,life:f.life})),held:pBullets.some(q=>q.kind==='beam')};}""")
    assert r['shots']>0,r
    assert r['flashes'] or r['held'],r
    report['players'].append(r)
    if pilot=='cole':
     pg.wait_for_timeout(70);pg.evaluate('()=>wm26Tick(.035)');shot(pg,'player-'+str(weapon))
  report['specials']=[]
  for name in ['decker','maverick','falva','freezer','yuri','manual-missile','space-volley','shadow-orb']:
   pg.evaluate(RESET,{'pilot':name if name in ['decker','maverick','falva','freezer','yuri'] else 'cole'})
   pg.evaluate("""name=>{window.testSpecial=name;
    if(name==='decker'){run.dkT=10;dkAmmo=2;dkReload=0;pShoot();}
    if(name==='maverick')special={pilot:name,t:10,mavCharging:true,mavCharge:MAV_FULL*.8};
    if(name==='falva')special={pilot:name,t:10,charging:true,charge:FALVA_FULL*.8,orbPhase:0};
    if(name==='freezer'){run.weapon=4;run.wvars[4]='icebreath';flameFire(3);updatePlay(1/60);}
    if(name==='yuri'){special={pilot:name,t:10};yuriChainStrike();}
    if(name==='manual-missile'){run.bombs=3;useBomb();}
    if(name==='space-volley'){run.spaceMode=true;run.gravityShipReady=true;spaceVolleyLaunchRack(3);}
    if(name==='shadow-orb'){run.spaceMode=true;run.gravityShipReady=true;spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);}
   }""",name)
   pg.wait_for_timeout(120);pg.evaluate('()=>{wm26Tick(.035);if(testSpecial==="decker")player._dkMuz=.08;}');shot(pg,name)
   r=pg.evaluate('()=>({name:testSpecial,flashes:wm26Releases.map(f=>f.family),shotgun:player._dkMuz,flame:!!flame})');report['specials'].append(r)
  # Art/raster proof uses the game context's own drawImage, and alpha of its output.
  report['reels']=pg.evaluate("""()=>{const rows=[];for(const family of Object.keys(WM26_REELS)){const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const frames=[];for(let i=0;i<WM26_REELS[family].n;i++){g.clearRect(0,0,128,128);const ok=wm26Draw(g,family,64,64,-Math.PI/2,(i+.1)/WM26_REELS[family].n,64,family==='ice'?'#67dfff':null);const d=g.getImageData(0,0,128,128).data;let ink=0;for(let a=3;a<d.length;a+=4)if(d[a]>20)ink++;frames.push({ok,ink});}rows.push({family,frames});}return rows;}""")
  assert all(f['ok'] and f['ink']>10 for r in report['reels'] for f in r['frames']),report['reels']
  # No damage / movement ownership in feedback; flash follows moving ship exactly.
  pg.evaluate(RESET,{});report['lifecycle']=pg.evaluate("""()=>{pShoot();const f=wm26Releases[0],p=wm26Point(f);player.x+=37;player.y-=19;const q=wm26Point(f);wm26Tick(.3);return {dx:q.x-p.x,dy:q.y-p.y,expired:wm26Releases.length===0};}""")
  assert report['lifecycle']=={'dx':37,'dy':-19,'expired':True},report['lifecycle']
  report['bosses']=[]
  for kind,stage,mini in [('magmaward',2,True),('olivewarden',4,True),('stormsovereign',4,False)]:
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True});pg.evaluate(RESET,{})
   pg.evaluate("""c=>{diffKey='furious';DIFF=DIFFS.furious;run.stage=c.stage;curStage=STAGES[c.stage-1];if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);const b=c.mini?subBoss:boss;window.testActor=b;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;b._drawY=b.y;b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};er26Set(b,c.stage===2?'ash-pursuit':'sovereign-battery');b._er26.t=b._er26.warm+.1;}""",{'kind':kind,'stage':stage,'mini':mini})
   pg.wait_for_timeout(150)
   r=pg.evaluate("""()=>{const b=testActor;b.t+=1/60;er26Tick(b,1/60);const origins=eBullets.map(q=>({x:q.x,y:q.y}));const mounts=['L','R'].map(s=>shipBossMount(b,s));return {kind:b.kind,origins,mounts,maxError:Math.max(...origins.map(q=>Math.min(...mounts.map(p=>Math.hypot(p.x-q.x,p.y-q.y)))))};}""")
   assert r['origins'] and r['maxError']<.01,r
   pg.evaluate('()=>{wm26Tick(.035);tickNavalFlashes(.035);if(testActor._smz)testActor._smz.t=.035;}');shot(pg,kind+'-firing');report['bosses'].append(r)
  # Confirm actual browser decodes both distinct music routes, not merely file existence.
  report['music']=pg.evaluate("""async()=>{const out=[];for(const key of ['mini5','boss5']){const a=new window.Audio(BOFA.music[key]);await new Promise((resolve,reject)=>{a.onloadedmetadata=resolve;a.onerror=()=>reject(new Error(key+' audio decode'));});out.push({key,src:BOFA.music[key],duration:a.duration});a.src='';}return out;}""")
  report['errors']=errors;(out/'verification.json').write_text(json.dumps(report,indent=2));br.close()
finally:stop()
print(json.dumps({'players':len(report.get('players',[])),'specials':report.get('specials'),'lifecycle':report.get('lifecycle'),'music':report.get('music'),'errors':errors},indent=2))
assert not errors,errors
