from pathlib import Path
import sys,json,http.server,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_terminal_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));checks=[];errors=[];states=[]
def ck(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
SETUP="""()=>{run.stage=8;curStage=STAGES[7];setState(GS.PLAY);diffKey='furious';spawnBoss('vileexistence');bossActive=true;window.B=boss;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=340;B.y=190;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;player.x=340;player.y=440;DBGT.god=true;for(const k of Object.keys(Input.keys))Input.keys[k]=false;pBullets=[];eBullets=[];RD84.events=[];B._lastPart=B.parts[0];modularHit(B.hp);window.D=dr5State(B);window.Q=D.rd84;}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');p.evaluate(SETUP);ck('Native final hit enters terminal death with every life pool exhausted',p.evaluate('B.hp===0&&V18.forms.every(i=>j3State(B).hp[i]===0)&&B._r30.mode==="dr5Death"&&!!Q'))
  ck('Immediate old runtime snapshot debris and automatic fire bursts are retired',p.evaluate('!B._fv21Final&&S78.debris.every(q=>q.owner!==B)&&FV21.fx.every(q=>q.owner!==B)'))
  for count,label in [(150,'tremble'),(280,'overload'),(180,'downloads'),(230,'shatter'),(300,'portal'),(420,'reunion')]:
   p.evaluate(STEP,count);s=p.evaluate('({t:B._r30.t,mode:B._r30.mode,phase:Q.phase,hp:B.hp,flash:Q.flash,stage:Q.stage,squad:Q.squad,fx:Q.fx.length,state})');states.append(s);print(label,s,flush=True);p.screenshot(path=str(W/('native-'+label+'.png')))
   if label=='tremble':
    frozen='({t:B._r30.t,age:Q.age,pose:Q.posePhase,beat:Q.beat,fx:Q.fx.map(f=>f.t)})';before=p.evaluate(frozen);p.evaluate("setState('paused')");p.evaluate(STEP,90);ck('Pause freezes death pose acceleration, lightning and explosion clocks',before==p.evaluate(frozen));p.evaluate('setState(GS.PLAY)')
   if label=='overload':ck('Death remains protected, motion stays centred, and no attacks or battle pickups survive',p.evaluate('dr5Locked()&&B.hp===0&&eBullets.length===0&&pBullets.length===0&&powerups.every(q=>q.dead)&&Math.abs(B.x-(camLeftX()+viewW()/2))<1'))
  ev=p.evaluate('RD84.events');ck('Exactly24 accelerating formation-style lightning strikes occur',len([e for e in ev if e['event']=='lightning-strike'])==24)
  ck('Rapid montage downloads stages1 through9 and actual coastal StageX',set(e['level']for e in ev if e['event']=='arena-download')==set(range(1,11)))
  ck('Full source-body breakup occurs once with56 irregular authored pieces',len([e for e in ev if e['event']=='whole-body-shatter'])==1 and p.evaluate('RD84_ART.shatterPieces')==56)
  ck('Electrified explosions are bounded and used during overload and shatter',len([e for e in ev if e['event']=='electric-burst'])>=20 and all(s['fx']<=12 for s in states))
  ck('Blue gate and above-ground squad reunion are each entered once',len([e for e in ev if e['event']=='blue-gated-portal'])==1 and len([e for e in ev if e['event']=='above-ground-reunion'])==1)
  ck('All eight other current pilots wait above ground, excluding the selected pilot',p.evaluate('Q.squad?.length===8&&!Q.squad.includes(run.pilot)&&new Set(Q.squad).size===8'))
  p.evaluate(STEP,440);print('HANDOFF',p.evaluate('({t:B._r30.t,mode:B._r30.mode,state,rewarded:B._r30.rewarded,trueFinal:run._trueFinaleCleared,debug:!!debugFight,active:bossActive})'),flush=True);ck('Native reunion awards once and returns the isolated debug fight to its menu',p.evaluate('B._r30.rewarded===true&&run._trueFinaleCleared&&state==="debugmenu"'))
  ck('Final death never restores a life pool',p.evaluate('V18.forms.every(i=>j3State(B).hp[i]===0)'))
  ck('No native page, draw or missing-image errors',not errors)
  # Repeated entry is idempotent, then stage reset retires local ownership.
  p.evaluate('window.oldTerminal=Q;j3FinalDeath(B)');ck('Repeated final-death notification cannot restart or duplicate the ending',p.evaluate('D.rd84===oldTerminal'))
  p.close();p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');p.evaluate(SETUP);p.evaluate('debugFight=null;run.mode="campaign"');p.evaluate(STEP,2000);ck('Campaign checkpoint reaches real Stage Clear through the existing reward owner',p.evaluate('B._r30.rewarded===true&&run._trueFinaleCleared&&state===GS.STAGECLEAR'))
  p.evaluate('beginStage(1)');ck('Starting another stage clears terminal owner and scene override',p.evaluate('!rd84Own(boss)'))
  br.close()
finally:stop()
s=(R/'assets/dracodia_terminal_art_1030.js').read_text();A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0];frames=[a for rows in A['banks'].values()for a in rows]
ck('All994 authored frames have even cells and stable per-bank pivots',len(frames)==994 and all(a['w']%2==a['h']%2==0 for a in frames)and all(len({tuple(a['logical'])+tuple(a['pivot'])for a in rows})==1 for rows in A['banks'].values()))
ck('Every packed frame fits within its actual texture page',all(a['rect'][0]+a['w']<=A['pages'][a['key']]['w']and a['rect'][1]+a['h']<=A['pages'][a['key']]['h']for a in frames))
ck('All texture pages are present at their exact exported dimensions',all(Image.open(R/a['path']).size==(a['w'],a['h'])for a in A['pages'].values()))
ck('Core engine remains byte-identical',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'events':ev,'errors':errors},indent=2));assert all(q['passed']for q in checks),[q['name']for q in checks if not q['passed']]
