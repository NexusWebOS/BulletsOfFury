from pathlib import Path
import sys,json,http.server
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/neural_optics_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));errors=[];checks=[];states=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
SETUP="""rank=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,6);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.arenaPhase=2;B.x=340;B.y=220;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;player.x=340;player.y=VH-65;DBGT.god=true;for(const k of Object.keys(Input.keys))Input.keys[k]=false;NB80.events=[];nb23Start(B,'eyeExpansion');window.P=B._r30.v18.attack;}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   for side in [-1,1]:
    p.evaluate(SETUP,rank);q=p.evaluate('side=>{DBGT.god=false;window.goal=340+105*side;return{tell:P.tell,hp:B.hp};}',side)
    for i in range(240):p.evaluate('()=>{Input.keys.a=player.x>goal+2;Input.keys.d=player.x<goal-2;}');p.evaluate(STEP,1)
    s=p.evaluate('({dead:player.dead,x:player.x,hp:B.hp,goal,events:NB80.events,attack:!!B._r30.v18.attack})');states.append({'rank':rank,'side':side,'state':s})
    ck(rank+(' left'if side<0 else' right')+' full-width eye beam escape survives without GOD',not s['dead']and abs(s['x']-s['goal'])<7)
    ck(rank+(' left'if side<0 else' right')+' escape preserves original brain HP',s['hp']==q['hp'])
   p.evaluate(SETUP,rank);p.evaluate('()=>{DBGT.god=false;player.x=nb23Eyes(B)[0].x;}');p.evaluate(STEP,round((q['tell']+.7)*60));ck(rank+' standing in the actual beam triggers native death',p.evaluate('player.dead'))
  p.evaluate(SETUP,'furious');p.evaluate(STEP,42)
  ck('Charge warnings draw all three native FOV colours',p.evaluate('NB80.draws.warning_green>0&&NB80.draws.warning_yellow>0&&NB80.draws.warning_red>0'))
  ck('Charge remains harmless before release',p.evaluate('!P.fired&&!player.dead'))
  before=p.evaluate('({t:P.t,eyes:nb23Eyes(B),clock:B._r30.clock})');p.evaluate("setState('paused')");p.evaluate(STEP,90);ck('Pause freezes charge, pose and eye origins',p.evaluate('({t:P.t,eyes:nb23Eyes(B),clock:B._r30.clock})')==before);p.evaluate('setState(GS.PLAY)')
  p.evaluate(STEP,13);s=p.evaluate('({width:NB80_ART.widths[P.widthStep],q:nb80Beam(P).a,eyes:P.eyes,drawEyes:nb23Eyes(B)})');ck('Beam launches at a full32px eye aperture instead of a hairline',s['width']==32)
  ck('First launch frame grows outward from the eye rather than appearing detached',s['q'].get('length',600)<600 and s['eyes']==s['drawEyes'])
  p.screenshot(path=str(W/'launch-verified.png'));p.evaluate(STEP,45)
  ck('Both beams expand through the42px maximum and600px continuous length',p.evaluate('P.widthStep===5&&nb80Beam(P).name==="beam_5"&&nb80Beam(P).a.logical[1]===624'))
  s=p.evaluate('''()=>{const a=nb23Actor(B),eyes=nb23Eyes(B),root=nb80Lens(B),same=root.a===a;return{same,eyes,expected:a.eyes.map(q=>({x:Math.round(B.x-192)+q[0],y:Math.round(B.y-192)+q[1]}))};}''');ck('Render, warning and damage use this exact whole-body frame eye sockets',s['same']and s['eyes']==s['expected'])
  p.evaluate('()=>{window.oldEyes=nb23Eyes(B);B.x+=31;B.y+=17;window.moved=nb23Eyes(B);B.x-=31;B.y-=17;}');ck('Moving the brain moves both beam origins by the identical offset',p.evaluate('moved.every((q,i)=>q.x-oldEyes[i].x===31&&q.y-oldEyes[i].y===17)'))
  p.evaluate('()=>{B._lastPart=B.parts[0];window.hpBefore=B.hp;modularHit(11);}');p.evaluate(STEP,1);p.screenshot(path=str(W/'hit-verified.png'))
  ck('Actual damage retains the white hit flash and visible emitting eye layer',p.evaluate('hpBefore-B.hp===11&&B.flash>0&&B.parts[0].flash>0&&NB80.draws.eyes_focus>0'))
  p.evaluate(STEP,12);ck('Hit flash expires normally during laser fire',p.evaluate('B.flash<=0&&B.parts[0].flash<=0'))
  while p.evaluate('P.t<P.tell+P.active+.1'):p.evaluate(STEP,1)
  ck('Laser recovery uses authored dissipation frames',p.evaluate('NB80.draws.recover>0'))
  p.evaluate('()=>{DBGT.god=false;player.invuln=0;player.x=nb23Eyes(B)[0].x;player.y=447;}');p.evaluate(STEP,8)
  ck('Recovery is harmless inside the fading beam artwork',p.evaluate('!player.dead'))
  # Exact source alpha and visible full core versus warning extents.
  p.evaluate(SETUP,'furious');p.evaluate(STEP,100)
  q=p.evaluate('''()=>{const a=nb80Beam(P).a,eye=nb23Eyes(B)[0];let good=0,bad=0;for(let y=0;y<a.h;y+=17)for(let x=0;x<a.w;x+=3){const row=a.spans[y];let expect=false;for(let i=0;i<row.length;i+=2)if(x>=row[i]&&x<row[i+1])expect=true;const hit=nb80Inside(a,eye,eye.x+a.offset[0]+x+.1,eye.y+a.offset[1]+y+.1);good++;if(expect!==hit)bad++;}return{good,bad};}''');ck('Beam damage follows the exact current authored shaft alpha',q['good']>200 and q['bad']==0)
  p.evaluate('v18Clear(B)');ck('Cancelling the attack immediately removes beam ownership',p.evaluate('!nb80Act(B)&&!B._r30.v18.attack'))
  p.evaluate(SETUP,'furious');p.evaluate('()=>{B._lastPart=B.parts[0];modularHit(B.hp);}');p.evaluate(STEP,435);ck('Native brain defeat cancels beams and downloads home without healing dead copy HP',p.evaluate('B._r30.v18.form===0&&B._r30.mode==="fight"&&j3State(B).hp[6]===0&&!nb80Act(B)'))
  p.evaluate(SETUP,'furious');p.evaluate('()=>{v18Clear(B);nb23Start(B,"cloudAegis");window.C=B._r30.v18.attack;C.t=C.tell+.4;window.hpBefore=B.hp;modularHit(25);}');ck('Existing cloud shield still protects native brain HP',p.evaluate('B.hp===hpBefore&&C.shield===C.maxShield-25&&!nb80Act(B)'))
  p.evaluate('()=>{v18Clear(B);nb23Start(B,"codeGeysers");window.G=B._r30.v18.attack;}');p.evaluate(STEP,230);ck('Existing committed geysers retain their original staggered releases',p.evaluate('G.targets.length===5&&G.targets.every(q=>q.released)&&!nb80Act(B)'))
  p.evaluate('()=>{v18Enter(B,2,1);B._r30.mode="fight";B.enter=B._noHit=false;}');ck('Revised helicopter stays under its separate owner',p.evaluate('hc79Own(B)&&!nb80Act(B)'))
  p.evaluate('()=>{v18Enter(B,2,0);B._r30.mode="fight";B.enter=B._noHit=false;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;rd78Start(B);}');ck('Main-body Luminaire stays under its existing owner',p.evaluate('!!rd78Act(B)&&!nb80Act(B)'))
  ck('No native draw or browser errors',not errors);br.close()
finally:stop()
s=(R/'assets/neural_optics_art_1030.js').read_text();A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
colours=[];all_continuous=True;actual_widths=[]
for level in range(6):
 for a in A['banks']['beam_'+str(level)]:
  sh=Image.open(R/A['pages'][a['key']]['path']).convert('RGBA');x,y,w,h=a['rect'];v=np.array(sh.crop((x,y,x+w,y+h)));alpha=v[:,:,3]>48;all_continuous &= all(np.count_nonzero(row)==a['width']and np.all(row[np.flatnonzero(row)[0]:np.flatnonzero(row)[-1]+1])for row in alpha);colours.append(v[:,:,:3][alpha]);actual_widths.append(a['width'])
rgb=np.concatenate(colours);ck('All96 flowing beam frames have continuous fully filled source rows',bool(all_continuous))
ck('Laser pixels use eye-matched hot reds/yellows without blue or violet shafts',bool(np.all(rgb[:,0]>=rgb[:,1])and np.all((rgb[:,1]>=rgb[:,2])|(rgb[:,0].astype(int)>=rgb[:,2].astype(int)*4))))
ck('Every beam phase retains an uninterrupted bright incandescent core',all((Image.open(R/A['pages'][a['key']]['path']).convert('RGBA').crop((a['rect'][0]+a['w']//2,a['rect'][1],a['rect'][0]+a['w']//2+1,a['rect'][1]+a['h'])).getextrema()[1][0]>220)for a in A['banks']['beam_5']))
ck('All166 exports retain even dimensions and source rectangles',sum(map(len,A['banks'].values()))==166 and all(a['w']%2==a['h']%2==0 for rows in A['banks'].values()for a in rows))
(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
