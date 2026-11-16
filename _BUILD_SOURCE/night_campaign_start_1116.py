from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,sys,json,time,base64
import imageio_ffmpeg,subprocess
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/campaign-start';O.mkdir(parents=True,exist_ok=True)
tree=ast.parse((R/'_BUILD_SOURCE/night_diagnostic_1116.py').read_text(encoding='utf8'));CAP=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPTURE'for t in n.targets))
a=CAP.index(' function aim(');z=CAP.index(' function render()',a)
CAP=CAP[:a]+''' function aim(elapsed){
 const A=reviewBot,K=Input.keys;for(const k of Object.keys(K))K[k]=false;
 const bind=keybindFor(1),key=a=>(bind[a]||[]).find(k=>!k.startsWith('mouse')&&!k.startsWith('pad_'));
 const hold=(a,on)=>{const k=key(a);if(k)K[k]=!!on;};
 if(state===GS.STAGESEL&&stateT>1.3&&elapsed-(A.lastMenu||-99)>1.5){Input.injectTap(key('fire')||'j');A.lastMenu=elapsed;}
 if(state!==GS.PLAY||player.dead||BOFCinematicDirector.active)return;
 const targets=_lockTargets().filter(t=>!t.dead&&t.hp>0&&t.y<player.y-30),target=targets.sort((a,b)=>Math.abs(a.x-player.x)+Math.abs(a.y-player.y)*.25-Math.abs(b.x-player.x)-Math.abs(b.y-player.y)*.25)[0];
 const left=Math.max(22,camLeftX()+22),right=Math.min(worldWidth()-22,camRightX()-22),goalX=target?.x??worldWidth()/2,goalY=PLAY.y+PLAY.h*.77;
 if(!A.goal||elapsed-A.goal.at>.09){let best=Infinity,chosen=null;for(const x0 of[player.x-48,player.x,player.x+48,goalX])for(const y0 of[player.y-42,player.y,player.y+42,goalY]){const x=clamp(x0,left,right),y=clamp(y0,PLAY.y+PLAY.h*.48,PLAY.y+PLAY.h-28);let risk=Math.abs(x-goalX)*.22+Math.abs(y-goalY)*.14+Math.hypot(x-player.x,y-player.y)*.12;for(const p of eBullets){if(p.dead)continue;for(const lead of[0,10,20]){const d=Math.hypot(x-p.x-(p.vx||0)*lead,y-p.y-(p.vy||0)*lead);if(d<48)risk+=(48-d)*4;}}for(const e of[...enemies,boss,subBoss]){if(!e||e.dead||e.ground||e._dyingT!=null)continue;const d=Math.hypot(x-e.x,y-e.y);risk+=Math.max(0,(Math.max(e.w||30,e.h||30)*.5+38)-d)*8;}for(const g of groundTargetingFx){if(g.dead||g.delay>0)continue;const d=Math.hypot(x-g.x,y-g.y);risk+=Math.max(0,(g.radius||28)+30-d)*5;}if(risk<best){best=risk;chosen={x,y,at:elapsed,risk};}}A.goal=chosen;}
 const q=A.goal;hold('left',player.x>q.x+5);hold('right',player.x<q.x-5);hold('up',player.y>q.y+5);hold('down',player.y<q.y-5);hold('fire',elapsed%.9<.66);hold('retina',!!target);
 if((bossActive||subBossActive)&&run.bombs>0&&elapsed-A.lastMissile>1.5){Input.injectTap(key('bomb')||'k');A.lastMissile=elapsed;}
 A.targetInfo=target?{x:target.x,y:target.y,hp:target.hp,kind:target.kind||target.type}:null;
 }
'''+CAP[z:]
a=CAP.index(" diffKey='furious';debugUnlocked=true;");z=CAP.index(' return {entry,difficulty:',a)
CAP=CAP[:a]+" diffKey='normal';debugUnlocked=false;debugFight=null;DBGT.god=false;DBGT.speed=1;P2M.pending=null;P2M.active=null;P2M.choice='campaign';run.mode='campaign';coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');const entry={stage:1,role:'fresh campaign'};startRun(1);\n"+CAP[z:]
CAP=CAP.replace("'STAGE '+cfg.stage+' / FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES / '","'NORMAL / FRESH CAMPAIGN / LIMITED INPUT BOT / NO GOD OR HP WRITES / '")
report={'scope':'Fresh native Normal campaign start with Cole and default resources. Limited input-only movement/fire/Retina/missiles; no GOD, invulnerability, enemy HP, lives, phase or timer writes. One-stage flow/survival smoke, not human balance certification or a full campaign win.','errors':[],'timeline':[]}
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(150000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?night-native-campaign=1116');p.wait_for_function('window.__bofFrames>6');p.mouse.click(3,3)
 with(O/'capture.webm').open('wb')as f:
  p.expose_function('saveCaptureChunk',lambda q:f.write(base64.b64decode(q)));report['setup']=p.evaluate(CAP,{'stage':1});start=time.monotonic();nextShot=0;endAt=None
  while time.monotonic()-start<720:
   p.wait_for_timeout(500);q=p.evaluate('''()=>({seconds:(performance.now()-captureStart)/1000,state,stage:run.stage,mode:run.mode,lives:run.lives,score:run.score,weapon:run.weapon,level:run.wlevel,god:DBGT.god,dead:player.dead,boss:boss?{kind:boss.kind,hp:boss.hp,max:boss.maxhp,dead:boss.dead}:null,mini:subBoss?{kind:subBoss.kind,hp:subBoss.hp,dead:subBoss.dead}:null,bossDefeated,scene:BOFCinematicDirector.current?.id,frames:__bofFrames,botErrors:reviewBot.errors,stats:{...stageStats},screen:[cv.width,cv.height]})''');report['timeline'].append(q)
   if q['seconds']>=nextShot:nextShot+=25;p.screenshot(path=str(O/f'frame-{int(q["seconds"]):04d}.jpg'),type='jpeg',quality=84);print(json.dumps(q),flush=True);(O/'progress.json').write_text(json.dumps(report,indent=2),encoding='utf8')
   if report['errors']or q['botErrors']or q['state']in['stageclear','continue','gameover']or q['stage']>1:
    if endAt is None:endAt=time.monotonic()
    if time.monotonic()-endAt>2:break
  report['capture']=p.evaluate('''async()=>{captureLive=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;return{...captureStats,drawAudit:cinemaDrawAudit};}''')
 report['outcome']=report['timeline'][-1];report['nativeStage1Defeat']=any(q['bossDefeated']for q in report['timeline']);report['limitReached']=time.monotonic()-start>=720;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');b.close()
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-i',str(O/'capture.webm'),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(O/'normal-campaign-start.mp4')],stdout=subprocess.DEVNULL,stderr=(O/'encode.log').open('w'),check=True);print('FINISH '+json.dumps(report['outcome']),flush=True)
