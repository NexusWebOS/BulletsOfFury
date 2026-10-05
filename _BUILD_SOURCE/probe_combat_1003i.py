"""Real Chromium combat fixtures; uses shoot.py, not a simulated renderer."""
from pathlib import Path
import base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_1003i';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('PASS ' if v else 'FAIL ')+name,flush=True)
def frames(p,n,code='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,15):p.evaluate('(n)=>{for(let i=0;i<n;i++){'+code+'}}',min(15,n-i));p.wait_for_timeout(8)
def shot(p,name,draw='drawWorld(0);'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+'}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(name)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.wait_for_function('()=>{av3Warm();return ["parts","beams","muzzles"].every(k=>XART.rdy("av3_"+(k==="parts"?"reaver_parts":"laser_"+k)));}',timeout=60000)
  p.evaluate('()=>{window.av3Blits=[];const d=ctx.drawImage;ctx.drawImage=function(){av3Blits.push(window.av3Key);return d.apply(this,arguments);};const get=XART.get;XART.get=function(k){window.av3Key=k;return get.apply(this,arguments);};}')
  for diff in ['normal','furious']:
   p.evaluate(SETUP,{'stage':2,'kind':'magmaward','mini':True,'diff':diff})
   ck(p.evaluate('()=>B._av3Reaver.parts.length===6&&!B._mr27'),diff+' Reaver owns six independent modules')
   p.evaluate('()=>{window.rot0=av3Part(B,"wingL").rot;er26Set(B,"furnace-lance");}')
   frames(p,30);shot(p,'reaver-'+diff+'-tell')
   ck(p.evaluate('()=>Math.abs(av3Part(B,"wingL").rot-rot0)>.001'),diff+' wing animates independently')
   frames(p,160);shot(p,'reaver-'+diff+'-beam')
   ck(p.evaluate('()=>av3Blits.includes("av3_reaver_parts")&&av3Blits.includes("av3_laser_beams")&&av3Blits.includes("av3_laser_muzzles")'),diff+' actual game context blits generated modules/beams/muzzles')
   p.evaluate('()=>{er26Set(B,"recover");B._l23Beam=null;B._noHit=false;window.gun=av3Part(B,"gunL");window.gunHP=gun.hp;window.center=av3PartPoint(B,gun,.35,.80);pBullets.push({kind:"mg",x:center.x,y:center.y,vx:0,vy:0,w:5,h:12,dmg:15,t:0});}')
   frames(p,1)
   report[diff+'Projectile']=p.evaluate('()=>({hp:gun.hp,before:gunHP,flash:gun.flash,other:av3Part(B,"gunR").flash,point:center,hit:subBossHitPart(center.x,center.y),projectiles:pBullets.map(q=>({kind:q.kind,dead:q.dead,x:q.x,y:q.y})),nohit:B._noHit,neutral:B._er26.neutralOpening})');print(report[diff+'Projectile'],flush=True)
   ck(p.evaluate('()=>gun.hp<gunHP&&gun.flash>0&&av3Part(B,"gunR").flash===0'),diff+' real projectile damages and flashes only the struck gun')
   p.evaluate('()=>{window.target=retinaBossTargets(B).find(q=>q._retinaId==="reaver-gunL");window.gunHP=gun.hp;run.bombs=30;run.missileTier="standard";window.fired=useBomb(target);}')
   frames(p,110)
   ck(p.evaluate('()=>fired&&gun.hp<gunHP'),diff+' actual Retina missile damages moving gun')
   p.evaluate('()=>{er26Set(B,"recover");B._noHit=false;for(let i=0;i<40&&!gun.dead;i++)av3ReaverHit(B,100,center.x,center.y,"gunL");window.count=eBullets.length;er26Shot(B,"L",Math.PI/2,2,{});}')
   ck(p.evaluate('()=>gun.dead&&!mr27CanFire(B,"L")&&eBullets.length===count&&!retinaBossTargets(B).some(t=>t._retinaId==="reaver-gunL")'),diff+' destroyed gun disables shot path and missile lock')
   shot(p,'reaver-'+diff+'-disarmed')
   ck(p.evaluate('()=>{const q=av3PartPose(B,av3Part(B,"wingL"));return !av3ReaverAt(B,B.x-120,B.y-90)&&!!subBossBeamImpact(B,{x:B.x,w:12,top:B.y-150,bot:B.y+180});}'),diff+' transparent gaps pass through and finite held beam reaches visible hull')
   p.evaluate('()=>{er26Set(B,"recover");B._noHit=false;for(let i=0;i<500&&!B.dead;i++)av3ReaverHit(B,100,B.x,B.y,"core");}')
   frames(p,160)
   ck(p.evaluate('()=>B.dead&&subBossDone&&!subBossActive'),diff+' modular encounter still finishes and releases stage')
  # All six generated colors through the actual game context.
  shot(p,'laser-contact-sheet','ctx.fillStyle="#09131e";ctx.fillRect(0,0,VW,VH);for(let i=0;i<6;i++){av3Beam(ctx,40,50+i*72,0,VW-80,27,i,.2);}')
  # Existing laser callers: fixtures retain their real emitters and renderer.
  renderers=[('jungle',1,'junglecruiser',True,'B._jc.beamActive=true;B._jc.t=1;B._jc.beamAng=.12;jungleCruiserDrawUnder(B);'),
   ('furnace',2,'infernoreaver',False,'fztBeamDraw({x:B.x,y:180,a:0,len:VH,width:16,kind:"eye"});'),
   ('frost',3,'frostcruiser',True,'B._l23Beam=null;B._jc=B._jc||{};B._jc.beamActive=true;B._jc.t=1;jungleCruiserDrawUnder(B);'),
   ('hammer',5,'chromehammer',False,'hammerChromiumDraw(B.x,180,VH,110,1,3);'),
   ('bomber',6,'siegebomber',True,'B._bomber.mode="beam";siegeBomberBeamDraw(B);'),
   ('harrier',6,'chaosharrier',False,'B._chActiveLaser={slot:"C",a:Math.PI/2,width:35};chaosHarrierLaserDraw(B);'),
   ('herald',8,'heralddeath',True,'S81003.beams=[];s81003Beam(B,{x:B.x-60,y:B.y,ex:B.x-100,ey:VH,width:26},"alien",1);s81003BeamsDraw();'),
   ('warhive',6,'warhive',False,'B._whv.cx=B.x;B._whv.cy=B.y=160;B._whv.hard=true;B._whv.st="hold";B._whv.dep={L:1,R:1};B._whv.beam={side:"L",t:2,warn:1,fire:3,w:32};whvDrawShots(B);'),
   ('carrier',6,'doomsdaycarriermk2',False,'B._cnBeamFrame=3;shipBossDraw(B);'),
   ('tempest',6,'tempestleviathan',True,'B._tlv.beams=[{x:B.x,y:B.y,dir:1,ang:Math.PI/2,active:true}];tempestDraw(B);'),
   ('sentinel',9,'warpsentinel',True,'B._s9Beam={t:2,charge:1,off:4,ang:.1,w:30};s9aBeamDraw(B);')]
  for name,stage,kind,mini,code in renderers:
   p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':mini});p.wait_for_timeout(60)
   if name=='warhive':
    p.evaluate('()=>{'+code+'}');p.wait_for_function('()=>["whv_closed_w","whv_fan","whv_cannon"].every(k=>XART.rdy(k))',timeout=60000)
   p.evaluate('()=>{AV3.draws.beam=0;AV3.draws.muzzle=0;}')
   if name in ['warhive','carrier','tempest']:
    p.evaluate('()=>{'+code+'}');p.evaluate('()=>{AV3.draws.beam=0;AV3.draws.muzzle=0;}');shot(p,'beam-'+name)
   else:shot(p,'beam-'+name,'drawWorld(0);'+code)
   ck(p.evaluate('()=>AV3.draws.beam>0&&AV3.draws.muzzle>0'),name+' live renderer uses beam and muzzle art')
  # Native audio decoding catches broken downloads and silent samples.
  p.evaluate(SETUP,{'stage':6,'pilot':'cole'});p.evaluate('()=>{Audio.init();Audio.resume();Audio.stopMusic();window.qaAudio=new AudioContext();}')
  sounds=p.evaluate('''async()=>{await qaAudio.resume();const out=[];for(const name of AV3_CUES){const raw=await (await fetch(BOFA.sfx['av3_'+name])).arrayBuffer(),b=await qaAudio.decodeAudioData(raw);let peak=0,sum=0,n=0;for(let ch=0;ch<b.numberOfChannels;ch++){const d=b.getChannelData(ch);for(let i=0;i<d.length;i++){peak=Math.max(peak,Math.abs(d[i]));sum+=d[i]*d[i];n++;}}out.push({name,duration:b.duration,peak,rms:Math.sqrt(sum/n)});}return out;}''')
  report['audio']=sounds;ck(len(sounds)==20 and all(s['peak']>.01 and s['rms']>.001 for s in sounds),'all 20 generated cues decode with nonzero sound')
  # Route real mixer elements to a test analyser (production keeps native playback).
  p.evaluate('()=>{Snd.vol.sfx=1;Snd.vol.master=1;window.qaMeter=qaAudio.createAnalyser();qaMeter.fftSize=2048;qaMeter.connect(qaAudio.destination);window.qaMeters=new WeakSet();window.measure=()=>{const d=new Float32Array(2048);qaMeter.getFloatTimeDomainData(d);return Math.max(...d.map(Math.abs));};window.attachMeter=el=>{if(!qaMeters.has(el)){qaAudio.createMediaElementSource(el).connect(qaMeter);qaMeters.add(el);}};}')
  for lv in [6,7]:
   p.evaluate('(lv)=>{run.weapon=0;run.wlevel=lv;AV3.last.clear();coleTrident(lv);window.loop=Snd.loops["av3_cole_laser"+lv];attachMeter(loop.el);}',lv)
   peak=0
   for _ in range(10):p.evaluate('(lv)=>{coleTrident(lv);Snd.loopTick(.05);}',lv);p.wait_for_timeout(50);peak=max(peak,p.evaluate('()=>measure()'))
   report['cole'+str(lv)+'Peak']=peak
   ck(peak>.001 and p.evaluate('()=>loop.el.currentTime>0&&!loop.el.paused'), 'Cole tier '+str(lv)+' actually outputs generated sustained laser audio')
   p.evaluate('()=>{player._av3ColeUntil=0;av3AudioTick(0);Snd.loopOff("av3_cole_laser6");Snd.loopOff("av3_cole_laser7");for(let i=0;i<30;i++)Snd.loopTick(1/60);}')
   ck(p.evaluate('()=>loop.el.paused&&!loop.on'),'Cole tier '+str(lv)+' loop ends after trigger release')
  p.evaluate('()=>{run.wlevel=8;AV3.last.clear();coleFuseRelease();}')
  ck(p.evaluate('()=>AV3.events.at(-1).cue==="fusion_cannon"&&pBullets.filter(q=>q.kind==="colefuse").length===2'),'actual Fusion release preserves two lances and plays dedicated sound')
  p.evaluate('()=>{run.stage=2;bossActive=false;wfx.fseq={wave:{x:100,y:100}};av3AudioTick(0);}')
  ck(p.evaluate('()=>AV3.loops.has("firewall_burn")'),'Stage 2 advancing firewall refreshes its own sound bed')
  p.evaluate('()=>setState(GS.PAUSE)')
  ck(p.evaluate('()=>Object.entries(Snd.loops).filter(([k])=>k.startsWith("av3_")).every(([k,L])=>!L.on&&L.el.paused)'),'pause immediately stops every new loop')
  # New shot families exercise actual enemy fire paths on levels 6-8.
  report['events']=p.evaluate('()=>AV3.events')
  ck(not errors,'zero page or console errors');br.close()
finally:
 stop();report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(0 if all(q['ok'] for q in report['checks']) and not errors else 1)
