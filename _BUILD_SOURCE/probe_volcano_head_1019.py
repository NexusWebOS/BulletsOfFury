"""Native head poses, registered laser roots, alpha hit mask and real damage."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/volcano';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.VHP19={draws:[]};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(key){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,key);return im;};ctx.drawImage=function(im){const key=tags.get(im);if(key?.startsWith('vh19_')){const m=this.getTransform();VHP19.draws.push({key,rect:[...arguments].slice(1),matrix:{a:m.a,b:m.b,c:m.c,d:m.d,e:m.e,f:m.f}});}return draw.apply(this,arguments);};
   window.vhp19Paint=v=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,ctx.canvas.width/SS,ctx.canvas.height/SS);v19Paint(v,B);return Array.from(ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data);};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{B=boss;v18Budget(B);v18Enter(B,2,2);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+200;B._drawY=B.y;P=gd4Create(B,2).p;F=P._fz;
    for(const q of B.parts)if(q.id!=='head'){q.hp=0;q.destroyed=true;F.pools[q.id==='core'?'body':q.id]=0;}furnaceEnter(P,'head');F.trans=0;F.dir=1;F._v19Head=null;B.hp=P.hp=F.pools.head;P.x=B.x;P.y=B.y;
    H3.release=false;H3.ending=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;
    enemies=[];eBullets=[];pBullets=[];powerups=[];Input.keys={};Input.mouse.down=false;player.invuln=1e9;player.fireCd=999999;VHP19.draws=[];SC12.refresh();__bofFit();}''')
   rows=p.evaluate('''()=>{const out=[],C=f17Tune();for(const bank of ['charge','spin'])for(let i=0;i<VH19_ART.banks[bank].length;i++){
    const a=VH19_ART.banks[bank][i];F.at=bank==='spin'?C.warm+C.active*a.angle/TAU:C.warm*.999*i/15;F.beams=[];F.tells=[];furnaceHeadCombat(P,0);const v=v19VolcanoRig(B)[0],n=VHP19.draws.length;vhp19Paint(v);const actual=VHP19.draws.slice(n).find(q=>q.key===a.key),sockets=vh19Sockets(B),rays=bank==='spin'?F.beams:F.tells;
    let error=0;if(actual){const m=actual.matrix;for(let eye=0;eye<2;eye++){const x=(a.eyes[eye][0]-64)*v.k,y=(a.eyes[eye][1]-64)*v.k,at={x:(x*m.a+y*m.c+m.e)/SS,y:(x*m.b+y*m.d+m.f)/SS},ray=rays[eye];if(ray)error=Math.max(error,Math.hypot(at.x-ray.x,at.y-ray.y));else if(i>0)error=999;}}
    const mask=v18Mask(a),testPoints=[];for(let y=0;y<128;y+=8)for(let x=0;x<128;x+=8){const q=v19WorldPoint(v,[x+.1,y+.1]);testPoints.push(v19AtRect(v,q.x,q.y)===(mask[y*128+x]>48));}
    out.push({bank,i,want:a.key,key:v.key,drawn:!!actual,rayError:error,mask:testPoints.every(Boolean),rays:rays.length,angle:v.rot,canvas:[a.w,a.h],pivot:a.pivot,k:v.k});}return out;}''')
   ck(diff+' all48 accepted poses actually blit',len(rows)==48 and all(q['drawn'] and q['want']==q['key'] for q in rows),[q for q in rows if not q['drawn'] or q['want']!=q['key']])
   ck(diff+' identical even cells,pivots and one proportional scale',all(q['canvas']==[128,128] and q['pivot']==[64,64] for q in rows) and len(set(q['k'] for q in rows))==1)
   ck(diff+' twin warning/laser roots match the actual drawn eyes',all(q['rayError']<.01 and q['rays']==2 for q in rows),{'maxError':max(q['rayError'] for q in rows),'rays':sorted(set(q['rays'] for q in rows))})
   ck(diff+' native alpha damage mask follows every pose',all(q['mask'] for q in rows))
   ck(diff+' generated surfaces supply the turn with only small residual rotation',max(abs(q['angle']) for q in rows)<.01,{'maxResidual':max(abs(q['angle']) for q in rows)})
   # A live native cycle, not a pose selection fixture: no forced transition.
   p.evaluate('F.at=0;F._v19Head=null;VHP19.draws=[];')
   for sec in range(10):
    frames(60)
    if sec in [0,2,5] and diff=='normal':p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'native-{sec+1:02}.jpg'),type='jpeg',quality=87)
   row=p.evaluate('({keys:[...new Set(VHP19.draws.map(q=>q.key))],turns:V19.events.filter(q=>q.event==="volcano-full-head-turn").length,phase:F.phase,finite:Number.isFinite(B.x+B.y+B.hp)})');ck(diff+' native clock completes a real full turn',row['turns']>0 and row['finite'] and any(k.startswith('vh19_spin') for k in row['keys']),row)
   p.evaluate('''()=>{F.at=0;F.trans=0;P.x=B.x;P.y=B.y;run.spaceMode=false;run.wlevels||=Array(8).fill(0);run.wvars||=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.x=B.x-(wm26PlayerNose().x-player.x);player.y=B.y+140;player.fireCd=0;VHP19.hp=B.hp;}''');p.keyboard.down('j');frames(45);p.keyboard.up('j');row=p.evaluate('({loss:VHP19.hp-B.hp,head:F.pools.head,phase:F.phase,part:B._lastPart?.id})');ck(diff+' actual ordinary primary damages the detached head',row['loss']>0,row)
   p.evaluate('pBullets=[];eBullets=[];');frames(30)
   row=p.evaluate('''()=>{VHP19.pose=v19VolcanoRig(B)[0];VHP19.before=vhp19Paint(VHP19.pose);B._lastPart=B.parts.find(q=>q.id==='head');const hp=B.hp;hitBoss(1);const after=vhp19Paint(VHP19.pose);let changed=0;for(let i=0;i<after.length;i+=4)if(after[i]!==VHP19.before[i]||after[i+1]!==VHP19.before[i+1]||after[i+2]!==VHP19.before[i+2])changed++;return{loss:hp-B.hp,changed,owner:B.flash,part:B._lastPart.flash};}''');ck(diff+' actual head damage flashes owner and part pixels',row['loss']>0 and row['changed']>30 and row['owner']>0 and row['part']>0,row)
   frames(30);row=p.evaluate('''()=>{const after=vhp19Paint(VHP19.pose),before=VHP19.before;let error=0,ink=0;for(let i=0;i<after.length;i+=4){if(Math.max(after[i],after[i+1],after[i+2],before[i],before[i+1],before[i+2])>16)ink++;for(let c=0;c<3;c++)error+=Math.abs(after[i+c]-before[i+c]);}return{owner:B.flash,part:B.parts.find(q=>q.id==='head').flash,error:error/Math.max(1,ink*3*255)};}''');ck(diff+' head damage expires to the authored palette',row['owner']<=0 and row['part']<=0 and row['error']<.005,row)
  br.close()
finally:stop()
ck('No page/console/draw/asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(bool(report['failed']))
