from pathlib import Path
import ast,json,sys,hashlib,datetime
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/chronos_dialogue_1102';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
tree=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});(W/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print('PASS' if ok else 'FAIL',name,str(data)[:1200] if not ok else '',flush=True);assert ok,(name,data)
def snap(p,name):p.locator('#screen').screenshot(path=str(W/(name+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:http.append((r.status,r.url.split('?')[0])) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4&&!!window.BOF_CHRONOS_DIALOGUE',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate(SETUP,{'stage':5,'pilot':'cole','diff':'furious'})
  p.evaluate('()=>{spawnBoss(curStage.boss);window.B=boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=VH*.34;B._drawY=B.y;}')
  ck('Fixture uses the real Stage5 Chronos actor',p.evaluate('!!B._hammer&&ht23Own(B)'),p.evaluate('({kind:curStage.boss,ship:B._ship,hammer:!!B._hammer})'))
  p.wait_for_function('()=>{stageLoadTick();c113Warm();return stageLoadReady(5)&&Object.values(C113_ART.poses).every(a=>Object.keys(a.files).every(k=>XART.rdy(k)))}',timeout=180000)
  ck('All four avatar views and fixed portrait sizes preload before Stage5',p.evaluate('Object.keys(C113_ART.poses).length===4&&Object.values(C113_ART.poses).every(a=>Object.values(a.compact).every(k=>XART.rdy(k)))'))
  p.evaluate('()=>{if(fb2Intro)fb2Intro.done=true;BOFCinematicDirector.cancel();H3.ending=null;setState(GS.PLAY);}')
  result=p.evaluate('''()=>{const out=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const pose of Object.keys(C113_ART.poses)){const key=c113Compact(pose),im=XART.get(key);ctx.fillStyle='#132131';ctx.fillRect(0,0,200,90);const r=ui20Portrait(ctx,key,{x:10,y:10,w:74,h:68});ctx.drawImage(im,110,10);const a=ctx.getImageData(r.x,r.y,68,68).data,z=ctx.getImageData(110,10,68,68).data;let difference=0;for(let i=0;i<a.length;i++)if(a[i]!==z[i])difference++;out.push({pose,key:r.key,difference,w:r.w,h:r.h,x:r.x,y:r.y});}ctx.restore();return out;}''')
  for row in result:ck(row['pose']+' uses exact approved compact pixels at native size',row['difference']==0 and row['w']==row['h']==68,row)
  result=p.evaluate('''()=>{const out=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const key of C113.aliases){const im=XART.get(key),expected=XART.get(C113_ART.poses.neutral.full);ctx.clearRect(0,0,512,512);ctx.drawImage(im,0,0);const a=ctx.getImageData(0,0,512,512).data;ctx.clearRect(0,0,512,512);ctx.drawImage(expected,0,0);const z=ctx.getImageData(0,0,512,512).data;let diff=0;for(let i=0;i<a.length;i++)if(a[i]!==z[i])diff++;out.push({key,diff});}ctx.restore();return out;}''')
  for row in result:ck(row['key']+' resolves the new full portrait',row['diff']==0,row)
  samples=[('I am Chronos.','neutral'),('Coming up here was merely a trap.','turn_right'),('Dodge THIS!','turn_left'),('Chromium Armor, Activated!','stern')]
  for text,pose in samples:
   p.evaluate('''text=>{ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);dlgBox({who:'CHRONOS',full:text,shown:text,forceShown:true,portraitKey:'fb1002_hammer_portrait'});}''',text)
   row=p.evaluate('()=>({dialogue:UI20.dialogue,portrait:C113.last,panel:CD27.last})')
   a=row['portrait'];r=row['dialogue']['portraitRect'];ck(pose+' is selected and fits inside the shared avatar bay',a['pose']==pose and a['x']>=r['x'] and a['y']>=r['y'] and a['x']+a['w']<=r['x']+r['w'] and a['y']+a['h']<=r['y']+r['h'] and row['panel']['h']==84,row)
   snap(p,'dialogue-'+pose)
  p.evaluate('''()=>{fb2IntroStart(B);fb2Intro.i=1;fb2Intro.t=1;fb2Intro.shown=5;ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);}''')
  ck('Unknown first-contact Chronos uses the new framed avatar',p.evaluate('UI20.dialogue.who==="???"&&UI20.dialogue.portrait.startsWith("c113_")&&C113.last.pose==="neutral"'),p.evaluate('({who:UI20.dialogue.who,key:UI20.dialogue.portrait})'));snap(p,'first-contact')
  p.evaluate('()=>{fb2Intro.done=true;BOFCinematicDirector.cancel();}')
  for text,pose in samples[1:]:
   p.evaluate('''text=>{BOFCinematicDirector.cancel();BOFCinematicDirector.play('c113-combat',[{who:'CHRONOS',art:'fb1002_hammer_portrait',text}],()=>{},true);BOFCinematicDirector.tick(.6);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);}''',text)
   row=p.evaluate('()=>({radio:C113.radio,portrait:C113.last,dialogue:UI20.dialogue,live:BOFCinematicDirector.current?.combatLive})')
   ck('Combat line '+text+' draws a portrait dialogue window',row['live'] and row['radio']['pose']==pose and row['portrait']['pose']==pose and row['dialogue']['who']=='CHRONOS',row)
   snap(p,'combat-'+pose)
  q=p.evaluate('''()=>{const t=stageTimer,clock=efxClock,s=BOFCinematicDirector.current;for(let i=0;i<30;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/60);}return{play:state===GS.PLAY,stageMoved:stageTimer>t,fxMoved:efxClock>clock,live:s.combatLive,portrait:C113.last,radio:C113.radio};}''')
  ck('Combat and simulation continue while Chronos talks',q['play'] and q['stageMoved'] and q['fxMoved'] and q['live'],q)
  p.evaluate('''()=>{BOFCinematicDirector.cancel();HT23.speech.length=0;ht23Say(B,'Chromium Armor, Activated!');updatePlay(1/60);BOFCinematicDirector.tick(.6);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);}''')
  q=p.evaluate('()=>({id:BOFCinematicDirector.current?.id,live:BOFCinematicDirector.current?.combatLive,radio:C113.radio,portrait:C113.last})')
  ck('Actual tactical announcement queue draws the stern avatar during live combat',q['id'].startswith('ht23-announcement-') and q['live'] and q['portrait']['pose']=='stern' and q['radio']['text']=='Chromium Armor, Activated!',q);snap(p,'actual-armor-announcement')
  p.evaluate('''()=>{BOFCinematicDirector.cancel();BOFCinematicDirector.play('c113-pilot',[{who:'DECKER',text:'Bring that back in one piece!'}],()=>{},true);BOFCinematicDirector.tick(.6);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);}''')
  ck('Decker still uses his own portrait and name color',p.evaluate('UI20.dialogue.who==="DECKER"&&!UI20.dialogue.portrait.startsWith("c113_")&&UI20.dialogue.color==="#ffd24a"'),p.evaluate('({who:UI20.dialogue.who,key:UI20.dialogue.portrait,color:UI20.dialogue.color})'))
  p.evaluate('()=>BOFCinematicDirector.cancel()')
  q=p.evaluate('''()=>{const old=H3.ending;try{H3.ending={sm10:{portrait:0}};const values=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const level of [0,1]){H3.ending.sm10.portrait=level;ctx.clearRect(0,0,512,512);ctx.drawImage(XART.get('sm10_hammer_portrait'),0,0);const a=ctx.getImageData(0,0,512,512).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]>245&&a[i+1]>245&&a[i+2]>245)n++;values.push(n);}ctx.restore();return values;}finally{H3.ending=old;}}''')
  ck('Final speech retains native terminal portrait whitening',q[1]>q[0]+2000,q)
  p.evaluate('''()=>{BOFCinematicDirector.preview('cronos','cole');}''');p.wait_for_function('()=>{const s=BOFCinematicDirector.current,b=s.beats[s.i];return XART.rdy(BOFCinematicDirector.artFor(b))}',timeout=120000)
  p.evaluate('()=>{const s=BOFCinematicDirector.current;s.shown=s.beats[s.i].text.length;ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw();}')
  ck('Cinematic Chronos speech uses the same new avatar system',p.evaluate('c113Who(UI20.dialogue.who)&&UI20.dialogue.portrait.startsWith("c113_")'),p.evaluate('({who:UI20.dialogue.who,key:UI20.dialogue.portrait})'));snap(p,'cinematic')
  ck('No browser, canvas, or missing-asset errors',not errors and not http,{'errors':errors,'http':http});b.close()
 (W/'report.json').write_text(json.dumps({'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'scope':'Native portrait pixels and existing dialogue owners; not a complete boss-balance playthrough.'},indent=2),encoding='utf8');print('RESULT',len(checks),'passed',flush=True)
finally:stop()
