from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/beta_priorities_1024';checks=[];errors=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage,kind,role in [(5,'chromehammer','boss'),(6,'warhive','boss'),(8,'heralddeath','mini')]:
   p.evaluate("""o=>{debugStartFight({stage:o[0],role:o[2],kind:o[1],name:o[1]},{pilot:'maverick'});if(o[2]==='boss')spawnBoss(o[1]);else spawnSubBoss__inner(o[1]);window.B=o[2]==='boss'?boss:subBoss;debugFight.spawned=true;B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=B._drawY=210;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;P2M.active=null;DBGT.god=true;setState(GS.PLAY);if(B._whv){B._whv.mode='carrier';B._whv.cx=B.x;B._whv.cy=B.y;if(B._carrier17){B._carrier17.depth=false;B._carrier17.phase='fight';B._carrier17.scale=1;roster17Budget(B);}}if(B._hammer){B._hammer.state='chain_cool';B._hammer.t=0;}GP4.clock=0;}""",[stage,kind,role])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&(run.stage!==5||ht23Warm()&&ch23Warm())&&(run.stage!==8||Object.values(CP22_ART.herald).every(a=>XART.rdy(a.key)))}')
   row=p.evaluate("""role=>{const samples=[],timers=[],before=B.hp;const parts=B._hd1003?.parts||B._carrier17?.parts||B.parts||[];const paint=()=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);if(role==='mini')drawSubBoss();else drawBoss();const d=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>225&&d[i+1]>225&&d[i+2]>225&&d[i+3]>200)n++;return n;};for(let i=0;i<120;i++){GP4.clock=i/60;B.flash=Math.max(0,(B.flash||0)-1/60);for(const q of parts)q.flash=Math.max(0,(q.flash||0)-1/60);if(B._carrier17)B._carrier17.direct='L';else if(B._whv)B._whvHit='hull';if(B._hd1003)hd1003Hit(B,.1,B.x,B.y,'head');else hitBoss(.1);timers.push(B.flash);if(i%3===0)samples.push(paint());}B.flash=Math.max(0,(B.flash||0)-.5);for(const q of parts)q.flash=Math.max(0,(q.flash||0)-.5);const expired=paint();return{damage:before-B.hp,min:Math.min(...samples),max:Math.max(...samples),expired,samples,normalFrames:timers.filter(t=>t<=0).length};}""",role)
   ck(kind+' native damage gives visible hit pixels and palette recovery',row['damage']>0 and row['max']>row['min']+100 and row['normalFrames']>20,row)
   p.screenshot(path=str(O/(kind+'-recovered.png')))
  p.evaluate("""()=>{debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'maverick'});spawnBoss('vileexistence');window.B=boss;debugFight.spawned=true;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;setState(GS.PLAY);}""")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}')
  forms=p.evaluate('V18.forms')
  for form in forms:
   row=p.evaluate("""form=>{v18Enter(B,2,form);v18SetMode(B,'fight');B.enter=B._noHit=false;B._lastPart=form===2?B.parts.find(p=>p.id==='cannonL'):B.parts[0];GP4.clock=0;const samples=[],before=B.hp;let normal=0;for(let i=0;i<120;i++){GP4.clock=i/60;B.flash=Math.max(0,(B.flash||0)-1/60);for(const q of B.parts)q.flash=Math.max(0,(q.flash||0)-1/60);modularHit(.1);if(!B.flash&&!B.parts.some(p=>p.flash>0))normal++;if(i%6===0){ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);r30DrawBoss(B);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let k=0;k<d.length;k+=4)if(d[k]>225&&d[k+1]>225&&d[k+2]>225&&d[k+3]>200)white++;samples.push(white);}}return{form,damage:before-B.hp,normal,min:Math.min(...samples),max:Math.max(...samples)};}""",form)
   ck('Dracodia form '+str(form)+' damage and native palette recovery',row['damage']>0 and row['normal']>20 and row['max']>row['min']+100,row)
  for width,height in [(1280,900),(480,800)]:
   p.set_viewport_size({'width':width,'height':height})
   p.evaluate("""()=>{debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'maverick'});spawnBoss('chromehammer');window.B=boss;debugFight.spawned=true;B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=B._drawY=230;B._hammer.state='chain_cool';B._hammer.t=0;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();BOFCinematicDirector.play('cronos',[{who:'CHRONOS',text:'FURY FLIGHT. YOU WILL NEVER BREAK MY CHROMIUM ARMOR.'}],()=>{},true);}""")
   p.wait_for_function("()=>{stageLoadTick();return stageLoadReady(5)&&XART.rdy('fb1002_hammer_portrait')}")
   row=p.evaluate("""()=>{const before=B.t;for(let i=0;i<15;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);BOFCinematicDirector.draw();return{live:BOFCinematicDirector.current?.combatLive,delta:B.t-before,ui:{x:UI20.dialogue.x,y:UI20.dialogue.y,w:UI20.dialogue.w,h:UI20.dialogue.h},W:VW,H:VH};}""")
   ck('Compact Chronos radio stays combat-live at '+str(width),row.get('live') and row['delta']>0 and row['ui']['w']<row['W']*.85,row)
   p.screenshot(path=str(O/('chronos-radio-'+str(width)+'.png')))
  ck('No page/console errors',not errors,errors);br.close()
finally:stop()
out=dict(passed=sum(q['passed']for q in checks),failed=sum(not q['passed']for q in checks),checks=checks,errors=errors);(O/'boss-pixels.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
