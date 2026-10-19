"""Native Chromium proof for PixelLab Stage 8 sprites and finite boss lives.
Invulnerable test pilot; combat and rendered geometry still use live paths.
"""
from pathlib import Path
import ast,base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_pixellab_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  html=(R/'index.html').read_text(encoding='utf-8')
  if 'assets/stage8_pixellab_1018.js' not in html:
   html=html.replace('</body>','<script src="assets/stage8_pixellab_art_1018.js"></script><script src="assets/stage8_pixellab_1018.js"></script></body>')
   p.route('**/index.html',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V18!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.vHits=0;playerHit=function(){vHits++;};window.vPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  window.vChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
  window.vPick=(part)=>{const v=v18Rig(B).find(v=>v.p.id===part),m=v18Mask(v.a),target={x:(v.a.bounds[0]+v.a.bounds[2])/2,y:(v.a.bounds[1]+v.a.bounds[3])/2};let best=null,dist=1e20;
   for(let y=0;y<v.a.h;y++)for(let x=0;x<v.a.w;x++)if(m[y*v.a.w+x]>200){const d=(x-target.x)**2+(y-target.y)**2;if(d<dist){dist=d;best={x:v.bodyX+(x-160)*v.k,y:v.bodyY+(y-160)*v.k};}}return best;};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);'+extra+'drawWorld(1/60);debugRecFrame();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(phase=0,form=0,diff='normal',fight=True):
   p.evaluate(SETUP,dict(stage=8,diff=diff,kind='vileexistence',pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}')
   p.evaluate('''([phase,form,fight])=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    stagePlan=[];warnT=0;warnKind=null;subBossDone=true;subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];
    v18Budget(B);v18Enter(B,phase,form);B._r30.v18.arenaPhase=phase;if(fight)v18Fight(B);else v18SetMode(B,'v18arrival');
    player.x=worldWidth()/2;player.y=VH-70;player.invuln=0;run.shield=0;run.spaceMode=false;bossWarned=true;bossDefeated=false;
    for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;V18.events=[];V18.draws={};__bofFit();}''',[phase,form,fight])
  setup(fight=False);frames(100);snap('arrival');frames(125);snap('conversion');frames(145)
  check('native arrival and 32-pose infection reach active phase1',p.evaluate('B._r30.mode==="fight"&&j3State(B).encounter===0&&Object.keys(V18.draws).filter(k=>k.startsWith("v18_conversion_")).length===32'),p.evaluate('({mode:B._r30.mode,poses:Object.keys(V18.draws).filter(k=>k.startsWith("v18_conversion_")).length})'))
  for bank in ['infused','ghost','colossus','hammer','helicopter','harrier','volcano']:
   result=p.evaluate('''bank=>{const m=V18_ART.models[bank],hashes=[],bounds=[];for(let i=0;i<m.frames.length;i++){
    const out=document.createElement('canvas');out.width=out.height=320;const g=out.getContext('2d');for(const a of Object.values(m.frames[i])){if(a.w%2||a.h%2||a.pivot.join()!=='160,160')throw Error('bad registration');g.drawImage(XART.get(a.key),0,0);}const rgba=g.getImageData(0,0,320,320).data;let h=2166136261,n=0;for(let j=0;j<rgba.length;j++){h=Math.imul(h^rgba[j],16777619)>>>0;if(j%4===3&&rgba[j]>128)n++;}hashes.push(h);bounds.push(n);}
    return{unique:new Set(hashes).size,n:m.frames.length,min:Math.min(...bounds),max:Math.max(...bounds)};}''',bank)
   check(bank+' sixteen genuine native poses and even fixed module canvases',result['unique']>=15 and result['n']==16 and result['min']>1500 and result['max']<80000,result)
  for diff in ['normal','hard','furious']:
   for phase,form in [(0,0),(1,0),(2,0),(2,8),(2,1),(2,6),(2,2)]:
    setup(phase,form,diff);p.evaluate('''()=>{window.vOriginalBudget=j3State(B).hp.slice();if(j3State(B).encounter===2)for(const id of V18.forms)if(id!==B._r30.v18.form)j3State(B).hp[id]=0;}''')
    frames(1020)
    row=p.evaluate('''()=>({phase:j3State(B).encounter,form:B._r30.v18.form,diff:diffKey,name:v18Model(B),hp:B.hp,shots:B._r30.v18.shots||0,
      attacks:V18.events.filter(e=>e.event==='attack-release').map(e=>({type:e.type,tell:e.reaction})),targets:retinaBossTargets(B).length,mode:B._r30.mode,draws:Object.keys(V18.draws).length})''');rows.append(row)
    check(diff+' '+row['name']+' repeatedly releases its distinct attacks',len(row['attacks'])>=3 and len({a['type'] for a in row['attacks']})>=3 and row['draws']>=32,row)
    check(diff+' '+row['name']+' three real native Retina modules',row['targets']==3,row)
    if diff=='normal':snap(row['name']+'-normal')
    p.evaluate('''()=>{B._r30.v18.attack=null;B._r30.attack=null;B._r30.v18.beams=[];B._r30.cd=999;window.vStableClock=B._r30.clock;for(const p of B.parts)p.flash=0;B.flash=0;}''')
    for part in ['core','left','right']:
     hit=p.evaluate('''part=>{B._r30.clock=vStableClock;const q=vPick(part),p=B.parts.find(p=>p.id===part),a=vPixels(()=>r30DrawBoss(B)),hp=B.hp;B._lastPart=r30At(B,q.x,q.y);const selected=B._lastPart?.id;hitBoss(1);const c=vPixels(()=>r30DrawBoss(B));return {damage:hp-B.hp,selected,pixels:vChanged(a,c),flash:p.flash,owner:B.flash};}''',part)
     check(diff+' '+row['name']+' '+part+' real damaged pixels flash',hit['damage']>0 and hit['selected']==part and hit['pixels']>20 and hit['flash']>0 and hit['owner']>0,hit)
     frames(12);check(diff+' '+row['name']+' '+part+' flash expires',p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
    p.evaluate('''()=>{const p=B.parts.find(p=>p.id==='left');B._lastPart=p;hitBoss(p.hp+.1);}''')
    check(diff+' '+row['name']+' destroyed weapon removes its pixels, muzzle and lock',p.evaluate('!v18Rig(B).some(v=>v.p.id==="left")&&!v18Ports(B).some(v=>v.module==="left")&&retinaBossTargets(B).length===2'))
    if diff=='normal':snap(row['name']+'-left-broken')
    if diff=='normal':
     p.evaluate('''()=>{enemies=[];eBullets=[];pBullets=[];run.weapon=0;run.wvars[0]=null;run.wlevels[0]=run.wlevel=0;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];chaingunUnlocked=false;run._earnedUnlocks.chaingun=false;powerups=[];player.fireCd=0;window.vBeforeGun=B.hp;Input.keys.j=true;}''')
     frames(75,'const q=vPick("core");player.x=q.x;player.y=B.y+180;powerups=[];');p.evaluate('Input.keys.j=false')
     check(row['name']+' actual centred J primary can damage core',p.evaluate('B.hp<vBeforeGun'),p.evaluate('({before:vBeforeGun,hp:B.hp})'))
  for name in ['infused','ghost','colossus','hammer','helicopter','harrier','volcano']:
   rr=[next(r for r in rows if r['name']==name and r['diff']==d) for d in ['normal','hard','furious']]
   check(name+' warning reactions tighten on Hard and Furious',rr[0]['attacks'][0]['tell']>rr[1]['attacks'][0]['tell']>rr[2]['attacks'][0]['tell'],[r['attacks'][0] for r in rr])
  # Long-running generation may finish while native combat observations run.
  # Only accept the completed generated bank; never substitute static frames.
  for _ in range(6000):
   data=json.loads((R/'assets/stage8_pixellab_art_1018.js').read_text().split('const V18_ART=',1)[1].strip().removesuffix(';'))
   if len(data['clips'].get('morph_volcano',{}).get('frames',[]))==16:break
   p.wait_for_timeout(100)
  assert len(data['clips'].get('morph_volcano',{}).get('frames',[]))==16,'Final volcano transformation not yet built'
  p.evaluate('(clips)=>Object.assign(V18_ART.clips,clips)',data['clips']);p.wait_for_function('v18Warm()')
  for clip in data['clips']:
   result=p.evaluate('''name=>{const bank=V18_ART.clips[name],hashes=[];for(const a of bank.frames){if(a.w!==320||a.h!==320||a.pivot.join()!=='160,160')throw Error('clip mount');
    const rgba=vPixels(()=>v18Cell(a,camX+240,230,320));let h=2166136261,n=0;for(let j=0;j<rgba.length;j++){h=Math.imul(h^rgba[j],16777619)>>>0;if(j%4===3&&rgba[j]>128)n++;}hashes.push(h);}return{count:bank.frames.length,unique:new Set(hashes).size};}''',clip)
   check(clip+' every generated pose draws distinctly through native game context',result['count']==result['unique'] and result['count']>=16,result)
  setup(0);p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(60);snap('fade-out')
  check('phase1 background has not switched before blackout',p.evaluate('j3State(B).encounter===0&&B._r30.v18.arenaPhase===0'))
  frames(8);check('phase2 arena switches only at full blackout',p.evaluate('j3State(B).encounter===1&&B._r30.v18.arenaPhase===1&&v18Fade(B)===1&&V18.events.some(e=>e.event==="arena-swap"&&e.blackout===1)'))
  frames(110);snap('ghost-reform');frames(130)
  check('phase2 reform fully restores gameplay without old hazards',p.evaluate('B._r30.mode==="fight"&&!B.enter&&!B._noHit&&!B._r30.v18.transition&&B._r30.v18.beams.length===0'))
  p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');frames(180);snap('colossus-reform');frames(130)
  check('phase3 owns exactly main plus four finite health pools',p.evaluate('j3State(B).hp.map((v,i)=>v>0?i:null).filter(i=>i!=null).join()===V18.forms.slice().sort((a,b)=>a-b).join()&&j3State(B).encounter===2'))
  check('the established Dracodia speech survives the new reform',p.evaluate('B._r30.mode==="dr5Monologue"&&!!dr5State(B).radio'))
  snap('dracodia-speech')
  for _ in range(20):
   if p.evaluate('B._r30.mode!=="dr5Monologue"'):break
   p.evaluate('()=>{const D=dr5State(B);if(D.radio)D.radio.t=dr5TalkDuration(D.radio.text)+.05;}');frames(3)
  check('Dracodia speech ends in a damageable main form',p.evaluate('B._r30.mode==="fight"&&!B.enter&&!B._noHit'))
  setup(2)
  visited=[]
  for n in range(4):
   p.evaluate('j3Morph(B,v18Next(B))');frames(190);visited.append(p.evaluate('B._r30.v18.form'));p.evaluate('j3Morph(B,"home")');frames(190)
  check('timer visits exactly Hammer helicopter Harrier volcano without retired forms',visited==[8,1,6,2],visited)
  # Damage persists and a dead form never returns. Leave main pool until last.
  for form in [8,1,6,2]:
   p.evaluate('(f)=>{j3Mimic(B,f);v18Fight(B);B._lastPart=B.parts[0];hitBoss(1e8);}',form);frames(190)
   check('destroyed form '+str(form)+' stays depleted and returns to main',p.evaluate('(f)=>j3State(B).hp[f]===0&&B._r30.v18.form===0&&B._r30.mode==="fight"',form))
  p.evaluate('B._lastPart=B.parts[0];hitBoss(1e8)');check('all five forms feed the one established Dracodia final death',p.evaluate('B._r30.mode==="dr5Death"&&dr5State(B).deathStarted&&j3State(B).hp.every(h=>h<=0)'))
  frames(900);snap('final-death');frames(950)
  check('native red portal and reunion award one final stage clear',p.evaluate('run._trueFinaleCleared&&run._realmReturned&&state===GS.STAGECLEAR'),p.evaluate('({state,mode:B._r30.mode,cleared:run._trueFinaleCleared,returned:run._realmReturned})'))
  check('no page console drawing or asset errors',not errors,errors)
  br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors,observations=rows,invulnerable=True)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps(dict(passed=data['passed'],failed=data['failed'],errors=errors)),flush=True);sys.exit(bool(data['failed']))
