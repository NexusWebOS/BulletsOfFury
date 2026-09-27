"""Native optional-rival menu, five-ship locks, and two-ally cooldown inspection.
Selected campaign fixture, then controlled threats to exercise both defensive moves.
No claim of a full campaign or balanced player victory.
"""
import base64,http.server,json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/rival-route');OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(60000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  report['menu']=p.evaluate("""()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');campaign.unlockedMax=8;campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];openStageSelect(8,{});stateT=2;Input.injectTap('arrowdown');const focus=Rival24.mapInput();Input.injectTap('enter');Rival24.mapInput();return {focus,state};}""")
  for _ in range(5):p.evaluate(sh.STEP,2);p.wait_for_timeout(100)
  shot(p,'ally-selection')
  report['selection']=p.evaluate("""()=>{Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('arrowright');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);return {chosen:Rival24.active?.chosen,state,boss:boss?.kind,arena:Rival24.arenaStage()};}""")
  p.wait_for_timeout(200);p.evaluate('()=>{stateT=1;ctx.setTransform(SS,0,0,SS,0,0);drawIntro(.016);}')
  p.wait_for_timeout(200);p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawIntro(.016);}')
  shot(p,'stage-card')
  p.evaluate("""()=>{setState(GS.PLAY);story=null;s6Opening=null;special=null;timeScale=1;player.invuln=999;window.allyRefs=new Map();window.moves=[];window.probeTime=0;const nav=s6WingNavigate;s6WingNavigate=function(q,w,d){if(Rival24.active)allyRefs.set(q.key,q);return nav(q,w,d);};const dodge=ally27Dodge;ally27Dodge=function(q,...a){const yes=dodge(q,...a);if(yes&&Rival24.active)moves.push({key:q.key,mode:q.dodgeMode,at:probeTime,duration:q.dodgeDuration});return yes;};}""")
  for sec in range(30):
   p.evaluate("""()=>{for(let f=0;f<60;f++){probeTime+=1/60;player.invuln=999;
    // Four-second spacing gives the initial ally approach and real rival attacks time.
    if(f===0&&Math.floor(probeTime)%4===3)for(const q of allyRefs.values())if(!q.dead)eShootT(q.x,q.y-56,Math.PI/2,2.4,'s6tracer',{silent:true,w:8,h:20});
    updatePlay(1/60);if(f%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.1);}}}""")
   p.wait_for_timeout(15)
   if sec in [4,12,21]:shot(p,'fight-'+str(sec))
  report['combat']=p.evaluate("""()=>({seconds:probeTime,allies:[...allyRefs.values()].map(q=>({key:q.key,hp:q.hp,dead:q.dead,phase:q.phase,rollCool:q.rollCool,somerCool:q.somerCool})),moves,targets:retinaBossTargets(boss).map(t=>({id:t._retinaId,x:t.x,y:t.y})),hulls:boss._rebels.ships.map(q=>({key:q.key,x:q.x,y:q.y,dead:q.dead,hp:q.hp})),finite:[...eBullets,...pBullets].every(q=>Number.isFinite(q.x+q.y))})""")
  report['damage']=p.evaluate("""()=>{const out=[];for(const t of retinaBossTargets(boss)){const before=boss._rebels.ships.map(q=>q.hp);retinaMissileDamage(t,17,{kind:'gmiss',x:t.x,y:t.y});out.push({target:t._retinaId,changed:boss._rebels.ships.filter((q,i)=>q.hp<before[i]).map(q=>q.key)});}return out;}""")
  report['updateOnly']=p.evaluate("""()=>{const first=[...allyRefs.values()].map(q=>q.t);for(let i=0;i<60;i++)updatePlay(1/60);return [...allyRefs.values()].map((q,i)=>q.t-first[i]);}""")
  report['lifecycle']=p.evaluate("""()=>{const saved=campSnapshot(),prior=boss;setState('paused');playPauseChoose(2);const restarted=Rival24.active&&boss!==prior&&boss.kind==='rebelsquad'&&Rival24.active.chosen.join(',')==='axel,decker'&&state===GS.INTRO;beginStage(4);const clear=!Rival24.active&&Rival24.arenaStage()===null;return {savedStage:saved.stage,restarted,clear,crewStillAvailable:campaign.rivalDefeated.every(x=>!x)};}""")
  report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert report['selection']['chosen']==['axel','decker'] and report['selection']['boss']=='rebelsquad'
assert report['combat']['finite'] and len(report['combat']['allies'])==2
assert all(x['changed']==[x['target']] for x in report['damage'])
assert all(abs(t-1)<1e-6 for t in report['updateOnly'])
assert report['lifecycle']=={'savedStage':8,'restarted':True,'clear':True,'crewStillAvailable':True}
for key in ['axel','decker']:
 for mode,cool in [('roll',5),('somer',7)]:
  ev=[e for e in report['combat']['moves'] if e['key']==key and e['mode']==mode]
  assert len(ev)>=2,(key,mode,ev)
  assert all(b['at']-a['at']>=cool+a['duration']-.02 for a,b in zip(ev,ev[1:])),ev
