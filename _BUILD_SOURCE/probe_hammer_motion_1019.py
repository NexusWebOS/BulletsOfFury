"""Native Hammer reel, full-pose blits, anatomy targets and actual hit pixels."""
from pathlib import Path
import ast,base64,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/hammer';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.HMP19={draws:[]};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};ctx.drawImage=function(im){const key=tags.get(im);if(key?.startsWith('hm19_'))HMP19.draws.push({key,args:[...arguments].slice(1),matrix:[...['a','b','c','d','e','f'].map(k=>this.getTransform()[k])]});return draw.apply(this,arguments);};
   window.hmp19Pixels=()=>Array.from(ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data);
   window.hmp19Draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,ctx.canvas.width/SS,ctx.canvas.height/SS);v19DonorDraw(B);};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{B=boss;v18Budget(B);v18Enter(B,2,8);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+190;B._drawY=B.y;H=gd4Create(B,8).p._hammer;P=gd4Create(B,8).p;
    H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;
    enemies=[];eBullets=[];pBullets=[];player.invuln=1e9;Input.keys={};Input.mouse.down=false;H.hc11Counter=null;H.throw=null;H.hammerDestroyed=false;HMP19.draws=[];SC12.refresh();__bofFit();}''')
   row=p.evaluate('''()=>{const out=[];for(const bank of ['ball','twirl'])for(let i=0;i<HM19_ART.banks[bank].length;i++){
    H.state=bank==='ball'?'ball':'whirlwind';H.angle=(i+.2)/HM19_ART.banks[bank].length*Math.PI*2;H.whirl={reel:i};H.t=.4;const v=v19HammerRig(B)[0],n=HMP19.draws.length;hmp19Draw();const draws=HMP19.draws.slice(n),a=HM19_ART.banks[bank][i];
    out.push({bank,i,expected:a.key,key:v.key,drawn:draws.some(q=>q.key===a.key),rot:v.rot,canvas:[a.w,a.h],k:v.k,pivot:a.pivot,onlyTwoParts:B.parts.map(p=>p.id),head:a.head?{at:r30At(B,B.x+(a.head[0]-128)*v.k,B.y+(a.head[1]-128)*v.k)?.id,inside:v18Mask(a)[a.head[1]*a.w+a.head[0]]}:null});}return out;}''')
   ck(diff+' all 39 real poses blit through the native boss renderer',len(row)==39 and all(q['expected']==q['key'] and q['drawn'] for q in row),row)
   ck(diff+' fixed even cells, common pivots and proportional bank scales',all(q['canvas']==[256,256] and q['pivot']==[128,128] and q['rot']==0 and abs(q['k']-(.76/(.85 if q['bank']=='ball' else .55)))<1e-9 for q in row))
   ck(diff+' all eight hammer retinas follow the actual opaque hammer head; no extra arm',all(q['onlyTwoParts']==['core','hammer'] and (q['head'] is None or q['head']['at']=='hammer' and q['head']['inside']>48) for q in row),[q for q in row if q['head']])
   # Use the real native controller's advancing reel. Draw poses before and
   # after each tick to avoid confusing the previous rendered frame with state.
   row=p.evaluate('''()=>{const A=fr27Armor(P)||fr27BeginArmor(P);A.activated=true;A.barrier=0;H.frAct=null;P._noHit=false;hammerWhirlStart(P);hammerState(P,'whirlwind');const out=[],initial={state:H.state,mode:H.mode,whirl:H.whirl,stage:run.stage};for(let i=0;i<180;i++){hammerBossTick(P,1/60);if(H.state!=='whirlwind')break;const a=hm19Frame(H);out.push({reel:H.whirl.reel,key:a?.key,want:HM19_ART.banks.twirl[Math.floor(H.whirl.reel)%8].key});}return{out,initial,final:{state:H.state,mode:H.mode,counter:!!H.hc11Counter}};}''')
   ck(diff+' actual Stage 5 whirlwind reel selects every directional drawing',len(row['out'])>30 and all(q['key']==q['want'] for q in row['out']),{'samples':len(row['out']),'unique':len(set(q['key'] for q in row['out'])),'initial':row['initial'],'final':row['final']})
   for state in ['spin','fr_twirl','ball']:
    p.evaluate('s=>{H.state=s;H.t=.6;H.angle=1.1;H.whirl=null;B.x=P.x=worldWidth()/2;B.y=P.y=VH*.37;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}',state)
    if diff=='normal':p.screenshot(path=str(O/(state+'.png')))
   # Route real primary rounds through the current moving whole-body rig.
   p.evaluate('''()=>{H.state='whirl_warn';H.t=0;H.whirl=null;H.hc11Counter=null;P.x=B.x;P.y=B.y;P._noHit=false;run.spaceMode=false;run.wlevels||=Array(8).fill(0);run.wvars||=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.x=B.x-(wm26PlayerNose().x-player.x);player.y=B.y+150;player.fireCd=0;window.hmp19Before=B.hp;}''')
   p.evaluate('window.hmp19Armor=fr27Armor(P)?.hp||0;window.hmp19Tool=H.hammerHP;window.hmp19Hits=stageStats.hits||0;');p.keyboard.down('j');frames(45);p.keyboard.up('j');loss=p.evaluate('({core:hmp19Before-B.hp,armor:hmp19Armor-(fr27Armor(P)?.hp||0),tool:hmp19Tool-H.hammerHP,state:H.state,hit:stageStats.hits,pbullets:pBullets.length,noHit:B._noHit,mode:B._r30.mode})');ck(diff+' ordinary primary damages the Hammer form or its native armor',loss['core']>0 or loss['armor']>0 or loss['tool']>0,loss)
   # Fixed pose before/after damage isolates actual changed pixels from motion.
   row=p.evaluate('''()=>{H.state='whirl_warn';H.t=0;H.whirl=null;H.hc11Counter=null;P.x=B.x;P.y=B.y;B.flash=0;for(const p of B.parts)p.flash=0;hmp19Draw();const before=hmp19Pixels(),part=B.parts.find(p=>p.id==='hammer');B._lastPart=part;hitBoss(1);hmp19Draw();const after=hmp19Pixels();let changed=0;for(let i=0;i<before.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])changed++;return{changed,owner:B.flash,part:part.flash};}''')
   ck(diff+' actual owner and hammer damage visibly flash',row['changed']>20 and row['owner']>0 and row['part']>0,row)
   p.evaluate('pBullets=[];eBullets=[];');frames(30);row=p.evaluate('''()=>{const expiry={owner:B.flash,part:B.parts.find(p=>p.id==='hammer').flash};H.state='whirl_warn';H.t=0;H.whirl=null;H.hc11Counter=null;const draw=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.filter='none';ctx.clearRect(0,0,ctx.canvas.width/SS,ctx.canvas.height/SS);v19Body(B);},rig=()=>v18Rig(B).map(v=>({key:v.key,id:v.p.id,flash:v.p.flash,alpha:v.alpha,x:v.x,y:v.y,rot:v.rot,k:v.k}));draw();const before=hmp19Pixels(),beforeRig=rig();HMP19.before=cv.toDataURL();B.flash=0;for(const p of B.parts)p.flash=0;draw();HMP19.after=cv.toDataURL();const after=hmp19Pixels(),afterRig=rig();let diff=0,significant=0,maxDelta=0,totalError=0,ink=0,whiteBefore=0,whiteAfter=0;for(let i=0;i<before.length;i++){const delta=Math.abs(before[i]-after[i]);if(delta)diff++;if(delta>8)significant++;maxDelta=Math.max(maxDelta,delta);if(i%4!==3)totalError+=delta;if(i%4===0){if(Math.max(before[i],before[i+1],before[i+2],after[i],after[i+1],after[i+2])>16)ink++;if(Math.min(before[i],before[i+1],before[i+2])>224&&Math.max(before[i],before[i+1],before[i+2])-Math.min(before[i],before[i+1],before[i+2])<16)whiteBefore++;if(Math.min(after[i],after[i+1],after[i+2])>224&&Math.max(after[i],after[i+1],after[i+2])-Math.min(after[i],after[i+1],after[i+2])<16)whiteAfter++;}}return{...expiry,diff,significant,maxDelta,normalizedError:totalError/Math.max(1,ink*3*255),whiteBefore,whiteAfter,beforeRig,afterRig,proxyFlash:P.flash};}''')
   for bank in ['before','after']:(O/(diff+'-expiry-'+bank+'.png')).write_bytes(base64.b64decode(p.evaluate('k=>HMP19[k]',bank).split(',')[1]))
   # Chromium's fractional nearest-neighbour blits differ at a few edge
   # texels after readback. Require <0.5% mean RGB error over actual ink and
   # the same white-pixel population, as well as expired native timers.
   ck(diff+' damage timers expire and original palette pixels return',row['owner']<=0 and row['part']<=0 and row['normalizedError']<.005 and abs(row['whiteBefore']-row['whiteAfter'])<=max(3,row['whiteBefore']*.02),row)
   row=p.evaluate('''()=>{H.hammerDestroyed=true;H.state='fr_stun';const v=v19HammerRig(B)[0],dead=hm19Frame(H);H.hammerDestroyed=false;H.state='throw';H.throw={};const thrown=hm19Frame(H);H.throw=null;return{broken:dead,thrown,key:v.key,newBank:!!v._hm19};}''')
   ck(diff+' broken and thrown hammer keep their authored native animation owners',row['broken'] is None and row['thrown'] is None and not row['newBank'],row)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
