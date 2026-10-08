"""Late visual findings: actual primary fire, unlocked Yuri orb, stable chaingun."""
from pathlib import Path
import json,sys,http.server,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/projectiles_1007/primary';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));report={'errors':[],'cases':[],'tracers':[]}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(120000)
  p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:400]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for f in ['balance_lab_1007.js','projectile_lab_1007.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/f))
  pilots=p.evaluate('()=>PILOTS.map(p=>p.key)')
  for diff in ['easy','normal','hard','furious']:
   cases=[(pilot,7,level) for pilot in pilots for level in [1,3,5]]+ [('yuri',8,level) for level in [1,3,5]]
   for pilot,weapon,level in cases:
    c={'stage':1,'kind':'damkeeper','diff':diff,'pilot':pilot,'weapon':weapon,'level':level,'id':f'{diff}-{pilot}-w{weapon}-L{level}'}
    p.evaluate("""c=>{AP7.begin(c);boss=null;bossActive=false;subBoss=null;subBossActive=false;bossDefeated=false;stagePlan=[];enemies=[];spawnClock=9999;run.missileLevel=0;
     yuriLightningOrbUnlocked=true;run._earnedUnlocks={lightningOrb:true};player.fireCd=0;run._chainHeat=0;run._chainOverheat=false;
     for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;window.PRIMARY={seen:new WeakSet(),shots:{},cal50:0};}
    """,c)
    for chunk in range(4):
     p.evaluate("""()=>{for(let i=0;i<45;i++){player.invuln=99999;updatePlay(1/60);for(const b of pBullets)if(!PRIMARY.seen.has(b)){PRIMARY.seen.add(b);PRIMARY.shots[b.kind]=(PRIMARY.shots[b.kind]||0)+1;if(b._cal50)PRIMARY.cal50++;}if(i%4===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/15);}}}""");p.wait_for_timeout(8)
    r=p.evaluate('()=>({shots:PRIMARY.shots,cal50:PRIMARY.cal50,geometry:AP7.geometry,keys:AP7.keys})');r['case']=c;report['cases'].append(r)
    if diff=='normal' and pilot=='yuri' and level==3:(O/f'weapon{weapon}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   print('PRIMARY',diff,len(report['cases']),flush=True)
   (O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
  p.evaluate("()=>{AP7.begin({stage:1,kind:'damkeeper',diff:'normal',pilot:'yuri',id:'tracer'});boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];window.TRACERS=()=>Object.keys(REPAIR30_ART).filter(k=>k==='chaingun_round'||k.startsWith('chaingun_round_'));for(const k of TRACERS())XART.rdy(REPAIR30_ART[k].key);}");p.wait_for_timeout(400)
  for diff in ['easy','normal','hard','furious']:
   result=p.evaluate("""diff=>{diffKey=diff;DIFF=difficultyForRun('arcade',diff);const out=[];
    for(const name of TRACERS())for(const lv of [1,3,5]){const b={kind:'mg',_cal50:true,lv,x:240,y:256,vx:0,vy:-4,t:0,_visualAge:0,_inf:name==='chaingun_round'?null:name.slice('chaingun_round_'.length)},frames=[];
     for(let f=0;f<24;f++){b.t=b._visualAge=f/24;frames.push(AP7.frame(b,false));}out.push({name,level:lv,frames});}return out;}
   """,diff);report['tracers'].append({'diff':diff,'rows':result})
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('DONE',json.dumps({'cases':len(report['cases']),'errors':report['errors']}),flush=True)
