"""Native diagonal Sharddart commitment, original controller and hit pixels."""
from pathlib import Path
import http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/drone-commit';O.mkdir(parents=True,exist_ok=True)
matrix=json.loads((R/'_shots/overnight_combat_1019/enemy_matrix/shipping-final-ai/report.json').read_text())
checks=[];rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.DP19={live:false};const play=updatePlay;
   updatePlay=function(dt){const x=typeof E==='undefined'?0:E.x,y=typeof E==='undefined'?0:E.y;if(DP19.live)DP19.time+=dt;const r=play.apply(this,arguments);if(!DP19.live)return r;
    if(E._dr.phase==='tell')DP19.tell??=DP19.time;if(E._dc19Done)DP19.resumed=true;
    const v=Math.hypot(E.x-x,E.y-y);DP19[E._dc19Done?'afterSpeed':'beforeSpeed']=Math.max(DP19[E._dc19Done?'afterSpeed':'beforeSpeed'],v);
    for(const b of eBullets)if(!DP19.seen.has(b)){DP19.seen.add(b);DP19.release??=DP19.time;DP19.rounds++;DP19.shots.push({kind:b.kind,speed:Math.hypot(b.vx,b.vy),angle:Math.atan2(b.vy,b.vx),aim:E._dr.aim});}
    return r;
   };
   window.dp19Snap=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);drawEnemy(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  }''')
  def frames(n):
   for i in range(0,n,6):p.evaluate('EA11.step',min(6,n-i));p.wait_for_timeout(5)
  for diff in ['normal','hard','furious']:
   spec=next(q['spec'] for q in matrix['rows'] if q['stage']==3 and q['difficulty']==diff and q['spec']['type']=='sharddart' and q['spec']['ai']['kind']=='diag')
   for baseline in [True,False]:
    p.evaluate('DP19.live=false');p.evaluate('([s,d])=>EA11.setup(s,d)',[3,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50);p.evaluate('s=>EA11.case(s,{nativePlacement:true})',spec);p.evaluate('drawWorld(0)');p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
    p.evaluate('off=>{window.DC19_OFF=off?1:0;CP12.stage=run.stage;CP12.lastTimer=0;CP12.age=0;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;_adaptiveSpawnT=999999;DP19={live:true,time:0,tell:null,release:null,rounds:0,shots:[],resumed:false,beforeSpeed:0,afterSpeed:0,seen:new WeakSet()};}',baseline)
    captured=False
    for i in range(130):
     frames(6)
     m=p.evaluate('({...DP19,seen:undefined,dead:E.dead,commit:!!E._dc19Commit})')
     if m['release'] is not None and not baseline:break
     if m['dead']:break
    rows.append(dict(difficulty=diff,baseline=baseline,metrics=m))
    if baseline:ck(diff+' disabled control leaves without firing',m['rounds']==0,m);continue
    ck(diff+' diagonal pass finishes its native tell before firing',m['rounds']>0 and m['tell'] is not None and m['release']-m['tell']>=.40-1e-6 and m['commit'],m)
    if m['dead'] or not m['rounds']:continue
    p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/(diff+'-volley.jpg')),type='jpeg',quality=80)
    p.evaluate('DP19.live=false;window.dpClean=dp19Snap();window.dpHP=E.hp;run.pilot="cole";pilotIndex=PILOTS.findIndex(q=>q.key==="cole");PILOTMOD={...PILOTS[pilotIndex]};player.x=E.x;player.y=E.y+80;player.fireCd=0;pBullets=[];weaponFormSelect(0,{kind:"primary1003b",id:"mg"});pShoot();for(const b of pBullets){b.x=E.x;b.y=E.y+4;b.vx=0;b.vy=-1;b.dmg=.25;}');frames(1)
    hit=p.evaluate('''()=>{const a=dp19Snap();let white=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>64&&Math.min(a[i],a[i+1],a[i+2])>160&&Math.min(dpClean[i],dpClean[i+1],dpClean[i+2])<120)white++;return{loss:dpHP-E.hp,flash:E.flash,white};}''')
    ck(diff+' real primary hit visibly flashes the committed hull',hit['loss']>0 and hit['flash']>0 and hit['white']>10,hit)
    p.evaluate('pBullets=[];player.y=VH-50;DP19.live=true');frames(18)
    expiry=p.evaluate('''()=>{const timer=E.flash,a=dp19Snap();E.flash=0;const b=dp19Snap();E.flash=timer;let error=0,ink=0;for(let i=0;i<a.length;i+=4){error+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);if(Math.max(a[i],a[i+1],a[i+2],b[i],b[i+1],b[i+2])>16)ink++;}return{timer,error:error/Math.max(1,ink*3*255),ink,resumed:DP19.resumed,before:DP19.beforeSpeed,after:DP19.afterSpeed};}''')
    ck(diff+' native flash expires and the diagonal flight resumes',expiry['timer']<=0 and expiry['ink']>40 and expiry['error']<.005 and expiry['resumed'],expiry)
  for kind,move in [('cryoeye','rush'),('sharddart','rush')]:
   sample=next(q['spec'] for q in matrix['rows'] if q['stage']==3 and q['difficulty']=='normal' and q['spec']['type']==kind and q['spec']['ai']['kind']==move);controls=[]
   for off in [1,0]:
    p.evaluate('DP19.live=false');p.evaluate('EA11.setup(3,"normal")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50);p.evaluate('s=>EA11.case(s,{nativePlacement:true})',sample);p.evaluate('off=>{window.DC19_OFF=off;DP19={live:false};VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;CP12.stage=run.stage;CP12.lastTimer=0;_adaptiveSpawnT=999999;}',off);frames(120);controls.append(p.evaluate('({x:E.x,y:E.y,phase:E._dr.phase,cd:E._dr.cd,shots:E._ea11.shots})'))
   ck(kind+' '+move+' preserves the real native route and attack clock',controls[0]==controls[1],controls)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');sys.exit(q['failed']>0)
