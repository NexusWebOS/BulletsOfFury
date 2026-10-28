"""Native fan-break motion and complete Carrier red/white pixel verification."""
from pathlib import Path
import ast,json,math,http.server
from playwright.sync_api import sync_playwright
import shoot

R=Path(__file__).resolve().parents[1];O=R/'_shots/carrier_turbulence_1028';O.mkdir(parents=True,exist_ok=True)
tree=ast.parse((R/'_BUILD_SOURCE/probe_carrier_mounts_1028.py').read_text())
strings={n.targets[0].id:n.value.value for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and isinstance(n.value,ast.Constant)and isinstance(n.value.value,str)}
checks=[];errors=[]
def check(name,v,data=None):
 checks.append(dict(name=name,passed=bool(v),data=data));(O/'probe.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));assert v,name
http.server.ThreadingHTTPServer.request_queue_size=256
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&hc32Warm()}');p.evaluate(shoot.TRAP_RAF)
  def step(n):
   for i in range(0,n,24):
    err=p.evaluate(shoot.STEP,min(24,n-i));assert not err,err;p.wait_for_timeout(1)
  def setup():
   p.evaluate(strings['BOOT']);step(220);p.evaluate(strings['HOLD']);p.evaluate('HC32.events=[]')
  def kill(id):p.evaluate("id=>{const C=boss._carrier17,q=C.parts.find(p=>p.id===id);C.direct=id;hitBoss(q.hp+1)}",id)
  def samples(n=180):
   rows=[]
   for i in range(0,n,4):
    step(4);rows.append(p.evaluate("()=>({motion:boss._hc32.motion,x:boss.x,y:boss.y,baseX:camLeftX()+viewW()/2+Math.sin(boss._carrier17.age*.36)*8,baseY:roster17Home(boss)+Math.sin(boss._carrier17.age*.55)*10})"))
   return rows
  def span(rows,key):return max(q['motion'][key]for q in rows)-min(q['motion'][key]for q in rows)
  setup();initial=p.evaluate('({hp:boss.hp,max:boss.maxhp,core:boss._hc32.core})');base=samples(60)
  check('Intact fans add no new turbulence',all(q['motion']['down']==0 and q['motion']['dx']==q['motion']['dy']==0 for q in base))
  kill('L');left=samples();p.screenshot(path=str(O/'one-side.png'));one=dict(x=span(left[15:],'dx'),y=span(left[15:],'dy'))
  check('First real fan break produces bounded whole-hull turbulence',all(q['motion']['down']==1 for q in left)and one['x']>5 and one['y']>3,one)
  check('Left-side break is recorded once through the native damage owner',p.evaluate('HC32.events.filter(e=>e.event==="fan-turbulence"&&e.mask===1).length===1'))
  kill('R');both=samples();p.screenshot(path=str(O/'both-sides.png'));two=dict(x=span(both[15:],'dx'),y=span(both[15:],'dy'))
  check('Both destroyed fans produce substantially stronger turbulence',all(q['motion']['down']==2 for q in both)and two['x']>one['x']*1.8 and two['y']>one['y']*1.8,dict(one=one,both=two))
  long=samples(600);check('Turbulence does not accumulate into positional drift',max(abs(q['x']-q['baseX'])for q in long)<35 and max(abs(q['y']-q['baseY'])for q in long)<25)
  q=p.evaluate("()=>{const b=boss,C=b._carrier17,p=C.parts.find(p=>p.id==='laser0'),m=roster17Mount(b,p),t=retinaBossTargets(b).find(t=>t._retinaId==='harrier laser0');return{m,target:{x:t.x,y:t.y},hit:roster17At(b,m.x,m.y),live:C.parts.filter(p=>!p.dead).length,core:b._hc32.core,max:b.maxhp};}")
  check('Live turret collision and Retina remain attached during the shudder',q['hit']=='laser0'and abs(q['m']['x']-q['target']['x'])<.01 and abs(q['m']['y']-q['target']['y'])<.01,q)
  check('Fan losses preserve the protected hull and remaining eight modules',q['core']==initial['core']and q['max']==initial['max']and q['live']==8)
  setup();kill('R');step(1);check('A right-side-first break also starts the native turbulence',p.evaluate('boss._hc32.motion.down===1&&HC32.events.some(e=>e.event==="fan-turbulence"&&e.mask===2)'))
  kill('L');p.evaluate("()=>{for(const q of boss._carrier17.parts.filter(p=>!p.dead)){boss._carrier17.direct=q.id;hitBoss(q.hp+1)}}");step(2)
  check('All parts exhausted expose the original intact hull reserve',p.evaluate('boss._hc32.exposed&&boss._hc32.core>0&&!boss._s6CarrierFall&&!boss.dead'))
  pixel="""t=>{const b=boss,S=b._hc32;if(t!=null){S.t=t;S.flash=0;}const draw=ctx.drawImage,get=XART.get;let key='',plates=0,shutters=0,wrecks=0;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);
   XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...a){if(HC32_ART.aliases[key]||key==='whv_twreck'){if(key==='whv_twreck')wrecks++;else if(a.length===8)shutters++;else plates++;return draw.call(this,im,...a)}};
   try{roster17Draw(b);s6r18CarrierOverlay(b,b._carrier17)}finally{ctx.drawImage=draw;XART.get=get;ctx.restore()}
   const d=ctx.getImageData(0,0,cv.width,cv.height).data,count=[0,0,0,0],red=[0,0,0,0];let bright=0,white=0;
   for(let y=0;y<cv.height;y++)for(let x=0;x<cv.width;x++){const i=(y*cv.width+x)*4,r=d[i],g=d[i+1],blue=d[i+2];if(d[i+3]<128||Math.max(r,g,blue)<30)continue;const part=(y>=b.y?2:0)+(x>=b.x?1:0);count[part]++;bright++;if(r>g+18&&r>blue+18)red[part]++;if(r>245&&g>245&&blue>245)white++;}
   return{red:count.map((n,i)=>red[i]/Math.max(1,n)),count,bright,white,frame:hc32HeatFrame(b),plates,shutters,wrecks};}"""
  on=p.evaluate(pixel,.05);check('Entire native hull and both fan wrecks turn red in all four quadrants',min(on['red'])>.90 and on['wrecks']==2 and on['shutters']==2,on)
  p.evaluate('()=>drawScene(0)');p.screenshot(path=str(O/'full-red.png'))
  off=p.evaluate(pixel,.21);check('Full red pulse releases cleanly to the original metal palette',max(off['red'])<.06 and off['frame']==-1,off);p.evaluate('()=>drawScene(0)');p.screenshot(path=str(O/'pulse-release.png'))
  check('Red pulses use complete authored heat cells immediately',p.evaluate('[0,.34,.67,1,1.34,2,3].every(t=>{boss._hc32.t=t;return hc32HeatFrame(boss)>=12})'))
  q=p.evaluate("()=>{const red=hc32Wreck(false),source=HC32.base.get.call(XART,'whv_twreck'),c=document.createElement('canvas');c.width=red.width;c.height=red.height;const g=c.getContext('2d');g.drawImage(source,0,0);const a=g.getImageData(0,0,c.width,c.height).data,b=red.getContext('2d').getImageData(0,0,c.width,c.height).data;return Array.from({length:c.width*c.height},(_,i)=>a[i*4+3]===b[i*4+3]).every(Boolean)}")
  check('Fan wreck red variant retains every original alpha pixel',q)
  p.evaluate("()=>{boss._carrier17.direct='hull';hitBoss(3)}");hit=p.evaluate(pixel,None);check('Real hull damage still flashes every damaged hull pixel white',hit['frame']==16 and hit['white']>hit['bright']*.99,hit);step(20);expired=p.evaluate(pixel,None);check('White hit feedback expires into the animated red/metal cycle',expired['frame']!=16 and expired['white']<hit['white']*.1)
  check('No game, draw, console or asset errors',not errors,errors);b.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),passed=all(q['passed']for q in checks))))
