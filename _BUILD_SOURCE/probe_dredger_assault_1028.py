"""Explicit native-render/controller fixtures for Dredger's October28 revision."""
from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
from shoot import serve,STEP
from barrage_review_common_1025 import boot

R=Path(__file__).resolve().parents[1];O=R/'_shots/dredger_assault_1028/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS 'if value else'FAIL ')+name,flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,7,errors,'mini')
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
  p.wait_for_function("()=>Object.values(DC40_ART).every(a=>XART.rdy(a.key))&&XART.rdy('er28_toxic_slug')",timeout=180000)
  p.evaluate(r"""()=>{
   window.dcSetup=(mode='recover',y=180)=>{const b=reviewActor,M=s7mInit(b);b.enter=false;b.x=worldWidth()/2;b.y=y;b._drawY=y;M.height=M.drop=M.lean=0;M.frExit=null;M.counterTell=null;M._mission29IntroDone=true;player.x=worldWidth()/2;player.y=VH-55;eBullets=[];s7mSet(b,mode);return M;};
   window.dcPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#181c20';ctx.fillRect(0,0,cv.width,cv.height);s7mDraw(reviewActor);const out=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return out;};
   dcSetup();
  }""")
  def shot(name):
   p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(name+'.png')))
  ck('All fixed cells have even dimensions, stable pivots and matching hit banks',p.evaluate("()=>Object.entries(DC40_ART).every(([n,a])=>a.cw%2===0&&a.ch%2===0&&XART.get(a.key).width%a.cw===0&&XART.get(a.key).height%a.ch===0&&(!DC40_ART[n+'_hit']||JSON.stringify(DC40_ART[n+'_hit'].pivot)===JSON.stringify(a.pivot)))"))
  ck('Native two-gun/core health budget is unchanged',p.evaluate("()=>{const b=reviewActor,M=b._s7mod;return M.parts.length===2&&b.maxhp===M.coreMax+M.parts.reduce((s,p)=>s+p.max,0)&&b.hp===b.maxhp;}"))
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('entry',100),old=M.dc40Track,start=dcPixels();for(let i=0;i<11;i++)s7mTick(b,1/60);const travelled=b.y-100,phase=M.dc40Track;b.y=100;const out=dcPixels();let n=0;for(let i=0;i<start.length;i+=4)if(start[i]!==out[i]||start[i+1]!==out[i+1]||start[i+2]!==out[i+2])n++;return{changed:n,phase,old,travelled};}""")
  ck('Authored moving tread frames visibly change native rendered pixels',q['changed']>100,q)
  q=p.evaluate("()=>{const M=dcSetup('entry',50),start=M.dc40Track;for(let i=0;i<12;i++)s7mTick(reviewActor,1/60);const moving=M.dc40Track;s7mSet(reviewActor,'dc40-guns');for(let i=0;i<12;i++)s7mTick(reviewActor,1/60);return{start,moving,stopped:M.dc40Track};}")
  ck('Tread phase follows real chassis travel and stops while braced',q['start']!=q['moving']and abs(q['moving']-q['stopped'])<.001,q)
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('recover',220),rows=[];for(const tx of [0,100,340,580,680]){player.x=tx;const ps=s7mPose(b).filter(p=>p.id.startsWith('gun'));const masks=[];for(const v of ps){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);const q=s7mWorld(b,v);er28Blit('dc40_gun',v.dc40Frame,q.x,q.y,true);masks.push(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();}let overlap=0;for(let i=0;i<masks[0].length;i+=4)if(masks[0][i]>200&&masks[1][i]>200)overlap++;rows.push({tx,overlap,mounts:ps.map(p=>[p.x,p.y]),angles:ps.map(p=>p.a)});}return rows;}""")
  ck('Twin turret hulls never overlap through extreme cross-screen aim',all(r['overlap']==0 for r in q),q)
  ck('Both physical trunnions remain fixed for every aim',all(r['mounts']==[[-43,66],[43,66]]for r in q))
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('dc40-guns',220),ps=s7mPose(b).filter(p=>p.id.startsWith('gun')),out=[];for(const p of ps)for(let barrel=0;barrel<2;barrel++){const q=dc40Barrel(b,p.id,barrel),w=s7mWorld(b,p);out.push({id:p.id,barrel,opaque:er28AlphaAt('dc40_gun',p.dc40Frame,q.x-w.x,q.y-w.y-1),x:q.x,y:q.y});}return out;}""")
  ck('All four measured muzzle mouths touch actual authored barrel alpha',len(q)==4 and all(r['opaque']for r in q),q)
  q=p.evaluate("()=>{const b=reviewActor;return s7mTargets(b).filter(q=>q._retinaId.startsWith('gun')).map(t=>({id:t._retinaId,impact:s7mBeamImpact(b,{x:t.x,top:0,bot:player.y,w:4})}));}")
  ck('Native player beams reach the exposed turret alpha from the south',len(q)==2 and all(r['impact']and r['impact']['id']==r['id']for r in q),q)
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('dc40-guns',220),before=dcPixels();sw28Slug(b,'gunL');sw28Slug(b,'gunR');const after=dcPixels();let changed=0;for(let i=0;i<after.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])changed++;const out={changed,count:eBullets.length,proof:eBullets.every(q=>q._er28Slug&&!q._shootable&&!enemyOrdnanceCanIntercept(q)),recoil:s7mPose(b).filter(p=>p.id.startsWith('gun')).map(p=>Math.floor(p.dc40Frame/64))};for(let i=0;i<9;i++)s7mTick(b,1/60);out.rest=s7mPose(b).filter(p=>p.id.startsWith('gun')).map(p=>Math.floor(p.dc40Frame/64));return out;}""")
  ck('Each turret fires exactly two slugs rather than balls',q['count']==4 and q['proof'],q)
  ck('Shot-linked recoil changes pixels and returns to rest',q['changed']>20 and q['recoil']==[1,1]and q['rest']==[0,0],q)
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('dc40-ram',145),rows=[];const startBlocks=DBGT.stats.godBlocks;for(let i=0;i<240;i++){s7mTick(b,1/60);rows.push({t:M.t,mode:M.mode,phase:M.dc40?.phase,y:b.y,track:M.dc40Track,safe:b._s4MiniSafe,shots:eBullets.length});}return {rows,blocks:DBGT.stats.godBlocks-startBlocks};}""")
  rows=q['rows'];dash=[r for r in rows if r['phase']=='dash'];reverse=[r for r in rows if r['phase']=='reverse'];opening=[r for r in rows if r['phase']=='open']
  ck('Committed fast ram reaches player contact within 0.42 seconds',dash and dash[-1]['t']-dash[0]['t']<=.42 and q['blocks']>0,dict(duration=(dash[-1]['t']-dash[0]['t'])if dash else 999,blocks=q['blocks']))
  ck('Reverse movement actually runs the tread animation backward',len(reverse)>10 and reverse[0]['y']>reverse[-1]['y']+70 and len({int(r['track'])for r in reverse})>=5)
  ck('Mid-screen opening lasts 1.65 seconds, stays vulnerable and does not fire',len(opening)>=95 and all(abs(r['y']-512*.46)<.01 and not r['safe']and r['shots']==0 for r in opening),dict(frames=len(opening),y=opening[0]['y']if opening else None))
  ck('Ram returns to the advancing native attack book',any(r['mode']=='recover'for r in rows))
  p.evaluate("()=>{dcSetup('dc40-ram',145);for(let i=0;i<122;i++)s7mTick(reviewActor,1/60);}");shot('reverse-opening')
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('dc40-circle',210);const counts=[],pixels=[];for(const t of [.12,.72,1.28]){M.t=t;const noGlow=M.dc40;M.dc40=null;const base=dcPixels();M.dc40=noGlow;const on=dcPixels();let extra=0;for(let i=0;i<on.length;i+=4)if(on[i+1]>base[i+1])extra++;pixels.push(extra);counts.push(l23FovPhase(M.t/M.warn));}return {counts,pixels,angles:M.dc40.angles};}""")
  ck('Top cannon gains visible own-pixel 1015 light during charge',min(q['pixels'])>5,q['pixels'])
  ck('Circular FOV uses all three native warning phases',q['counts']==['green','yellow','red'],q['counts'])
  ck('Committed 300-degree barrage leaves its warned south escape sector',all(abs(__import__('math').atan2(__import__('math').sin(a-__import__('math').pi/2),__import__('math').cos(a-__import__('math').pi/2)))>=__import__('math').pi/6-.001 for a in q['angles']))
  for t,name in [(.12,'circle-green'),(.72,'circle-yellow'),(1.28,'circle-red')]:
   p.evaluate("t=>{dcSetup('dc40-circle',210);reviewActor._s7mod.t=t;}",t);shot(name)
  q=p.evaluate("()=>{const b=reviewActor,M=dcSetup('dc40-circle',210);for(let i=0;i<175;i++)s7mTick(b,1/60);return{count:eBullets.length,all:eBullets.every(q=>q._dc40Circle&&!enemyOrdnanceCanIntercept(q)),round:M.dc40?.round,mode:M.mode};}")
  ck('Top cannon releases three finite slug waves from its own opening',q['count']==60 and q['all'],q)
  p.evaluate('drawWorld(0)');shot('top-barrage')
  q=p.evaluate(r"""()=>{const b=reviewActor,M=dcSetup('dc40-guns',220),part=M.parts[0];function whites(){const a=dcPixels();let n=0;for(let i=0;i<a.length;i+=4)if(a[i]>240&&a[i+1]>240&&a[i+2]>240)n++;return n;}const base=whites(),hp=part.hp;sw28Slug(b,part.id);s7mHit(b,2,0,0,part.id);const hit=whites();for(let i=0;i<18;i++)s7mTick(b,1/60);const out={base,hit,end:whites(),hp:part.hp,before:hp,flash:part.flash};s7mHit(b,part.hp,0,0,part.id);out.cancelled=eBullets.filter(q=>q._dc40Gun===part.id).every(q=>q.dead);out.targetRemoved=!s7mTargets(b).some(q=>String(q._retinaId||q.id).includes(part.id));return out;}""")
  ck('Actual turret damage flashes native white pixels and expires',q['hp']<q['before']and q['hit']>q['base']+100 and q['end']<q['hit']and q['flash']==0,q)
  ck('Destroyed gun cancels its rounds and native Retina target',q['cancelled']and q['targetRemoved'],q)
  q=p.evaluate(r"""()=>{const b=reviewActor,d=D27_MODULE_DEBRIS.find(q=>q._dc40Owner===b);const saved=er28Blit,calls=[];er28Blit=function(name,f,x,y,hit){calls.push({name,f,x,y});return saved.apply(this,arguments);};try{d27ModuleDebrisDraw();}finally{er28Blit=saved;}return {owned:!!d,staticImage:d?.image,frame:calls.find(q=>q.name==='dc40_gun')?.f};}""")
  ck('Broken turret uses the actual twin-barrel bank under native debris flight',q['owned']and q['staticImage']is None and isinstance(q['frame'],int),q)
  q=p.evaluate("()=>{const b=reviewActor,M=dcSetup('dc40-circle',220);for(let i=0;i<94;i++)s7mTick(b,1/60);s7mSet(b,'dead');return{cancel:eBullets.every(q=>q.dead),pending:M.dc40,health:b.hp,parts:M.parts.map(p=>p.hp)};}")
  ck('Native death cancels pending firing and all owned rounds',q['cancel']and q['pending']is None,q)
  q=p.evaluate(r"""()=>{spawnSubBoss('dualscoopdredger');reviewActor=subBoss;const M=s7mInit(subBoss);dcSetup('recover',180);const b=subBoss,start=b.maxhp;s7mHit(b,M.coreMax*3,0,0,'core');const core={hp:M.core,total:b.hp,guns:M.parts.reduce((n,p)=>n+p.hp,0),mode:M.mode,targets:s7mTargets(b).map(t=>t._retinaId)};s7mSet(b,'dc40-guns');eBullets=[];for(let i=0;i<90;i++)s7mTick(b,1/60);const fighting=eBullets.filter(q=>!q.dead).length;s7mHit(b,M.parts[0].hp,0,0,'gunL');const one=M.mode!=='dead'&&M.parts[1].hp>0;s7mHit(b,M.parts[1].hp,0,0,'gunR');return{start,core,fighting,one,dead:M.mode==='dead',allHP:M.core+M.parts.reduce((n,p)=>n+p.hp,0)};}""")
  ck('Spent core removes its Retina while the full surviving gun budget remains live',q['core']['hp']==0 and q['core']['total']==q['core']['guns']and q['core']['mode']!='dead'and q['core']['targets']==['gunL','gunR'],q)
  ck('Surviving turrets keep attacking after core exhaustion',q['fighting']>0 and q['one'],q)
  ck('One native defeat starts only after the complete health budget is exhausted',q['dead']and q['allHP']==0,q)
  ck('Warden scope and source owner remain separate',p.evaluate("()=>{const b={_s7mod:{tank:false}};return !dc40Own(b)&&wl39Own(b);}"))
  ck('No page, console or asset errors',not errors,errors)
  report=dict(checks=checks,errors=errors,events=p.evaluate('DC40.events'));(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');br.close()
finally:stop()
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
