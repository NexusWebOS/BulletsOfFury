"""Native rebirth observation, rendered continuity and labelled damage fixtures."""
from barrage_review_common_1025 import ROOT,boot,advance
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,argparse

ap=argparse.ArgumentParser();ap.add_argument('--depth',action='store_true');ap.add_argument('--climax',action='store_true');ap.add_argument('--strikes',action='store_true');ap.add_argument('--polish',action='store_true');ap.add_argument('--dna',action='store_true');ap.add_argument('--palette',action='store_true');args=ap.parse_args();args.dna=args.dna or args.palette;args.polish=args.polish or args.dna;args.strikes=args.strikes or args.polish;args.climax=args.climax or args.strikes;args.depth=args.depth or args.climax
O=ROOT/('_shots/dracodia_palette_1026/probe'if args.palette else'_shots/dracodia_dna_1026/probe'if args.dna else'_shots/dracodia_polish_1026/probe'if args.polish else'_shots/dracodia_strikes_1026/probe'if args.strikes else'_shots/dracodia_climax_1026/probe'if args.climax else'_shots/dracodia_depth_1026/probe'if args.depth else'_shots/dracodia_download_reveal_1025/probe');O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];trace=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
def shot(p,name):
 p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)}',timeout=180000)
  ck('Native portal entrance reaches the original first host',advance(p,"boss._r30.mode==='fight'&&j3State(boss).encounter===0",1000,12)and p.evaluate("RB23.events.some(e=>e.event==='arena-teleported')"))
  initial=p.evaluate('({host:boss.maxhp,pools:j3State(boss).hp,forms:V18.forms})')
  ck('The existing authored 24-pose carrier and final plates are ready',p.evaluate("ER23_ART.banks.symbiote.count===24&&XART.rdy(ER23_ART.banks.symbiote.key)&&V18_ART.models.colossus.frames.every(f=>Object.values(f).every(a=>XART.rdy(a.key)))"))
  if args.polish:
   d=p.evaluate("""()=>{let n=0,bad=[];for(const [name,a]of Object.entries(R25_ART.host))for(let f=0;f<a.count;f++)for(const id of ['left','right']){const q=a.frames[f].targets[id],im=r25Layer(name,id,f),p=im.getContext('2d').getImageData(q[0],q[1],1,1).data;n++;if(p[3]<=96)bad.push({name,f,id,q});}return{n,bad};}""")
   ck('All ninety revised arm targets overlap native opaque arm pixels',d['n']==90 and not d['bad'],d)
   p.evaluate("""()=>{window.rd27ProbeHost=r25HostSample(boss);window.rd27HostPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(256-boss.x,256-boss.y);bi24Draw(rd27ProbeHost,boss,360);const d=ctx.getImageData(0,0,cv.width,210).data.slice();ctx.restore();return d;};window.rd27BeforeBody=rd27HostPixels();for(const p of boss.parts.filter(p=>p.id!=='core')){boss._lastPart=p;modularHit(p.hp+1);}}""")
   p.evaluate(STEP,40);shot(p,'first-host-both-arms-broken')
   d=p.evaluate("""()=>{const a=rd27BeforeBody,z=rd27HostPixels();let different=0,ink=0;for(let i=0;i<a.length;i+=4){if(a[i]+a[i+1]+a[i+2]>30)ink++;if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])different++;}drawWorld(0);return{different,ink,arms:boss.parts.filter(p=>p.id!=='core').map(p=>p.destroyed)};}""")
   ck('First-host crown and full-width shoulders remain intact after actual arm destruction',d['different']==0 and d['ink']>1000 and all(d['arms']),d)
  # Explicit native-damage checkpoint, identical to the recorded demonstration.
  p.evaluate("()=>{RB23.events=[];for(const p of boss.parts.filter(p=>p.id!=='core')){boss._lastPart=p;modularHit(p.hp+1);}boss._lastPart=boss.parts[0];modularHit(boss.parts[0].hp+1);}")
  ck('Native core exhaustion starts one protected rebirth',p.evaluate("boss._r30.mode==='dr5er23rebirth'&&boss._noHit&&boss.hp===0"))
  if args.polish:
   d=p.evaluate("""()=>{function pixels(draw){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);draw();const d=ctx.getImageData(0,0,cv.width,cv.height).data.slice();ctx.restore();return d;}const a=pixels(()=>v18Body(boss)),z=pixels(()=>bi24Draw(bi24Sample('dracodia_recover',1),boss,360));let different=0,ink=0;for(let i=0;i<a.length;i+=4){if(a[i]+a[i+1]+a[i+2]>30)ink++;if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])different++;}drawWorld(0);return{different,ink};}""")
   ck('Falling first host retains the same complete authored body after core exhaustion',d['different']==0 and d['ink']>1000,d)
  marks=[13.98,14.02,15.5,18,20.5,23,24.7,25.22,25.62,28.48]+([6.5,7.25,8.5,10.5,11.5,12.5,13.9,14.5,15.5,16.0]if args.polish else[])+([25.45,25.59,25.75,26.1]if args.climax else[]);seen=set()
  for i in range(1850):
   p.evaluate(STEP,1)
   q=p.evaluate("""()=>{const b=boss,S=b._r30,R=S.v18.rb23Rebirth,F=typeof RD26==='undefined'?null:RD26.fx;return{clock:S.clock,t:S.t,mode:S.mode,x:b.x,y:b.y,hp:b.hp,pools:j3State(b).hp,encounter:j3State(b).encounter,protected:b._noHit,bolts:R?.bolts,download:RD25.last,dna:typeof RD28==='undefined'?null:RD28.last,intro:typeof RD27==='undefined'?null:RD27.intro,targets:retinaBossTargets(b).length,effects:F?{front:F.front.length,back:F.back.length,strikes:F.strikes}:null};}""");trace.append(q)
   if q['mode']=='dr5er23rebirth':
    for mark in marks:
     if mark not in seen and q['t']>=mark:seen.add(mark);shot(p,'native-'+str(mark))
    if args.dna and q['t']>=11.5 and'dna-pixels'not in seen:
     seen.add('dna-pixels')
     data=p.evaluate("""()=>{const out={};for(const name of ['rd28Strands','rd28CodeSkin']){drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,fn=window[name];window[name]=()=>{};try{drawWorld(0);}finally{window[name]=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<z.length;i+=4)if(z[i]!==a[i]||z[i+1]!==a[i+1]||z[i+2]!==a[i+2])changed++;out[name]=changed;}drawWorld(0);return out;}""")
     ck('Living DNA strands and fluid symbiote blobs visibly form around the skeleton',data['rd28Strands']>1000,data)
     ck('Animated code visibly downloads inside the actual skeletal silhouette',data['rd28CodeSkin']>100,data)
     if args.palette:
      d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,fn=rd28Strands;rd28Strands=()=>{};try{drawWorld(0);}finally{rd28Strands=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let colored=0;for(let i=0;i<a.length;i+=4)if((a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])&&a[i]>a[i+1]*1.2&&a[i+2]>a[i+1]*1.1)colored++;drawWorld(0);return{colored,ready:rd28Ready(),banks:Object.values(RD28_PALETTE).map(a=>a.count)};}""")
      ck('Actual DNA uses Dracodia violet and red-magenta energy pixels',d['colored']>1000 and d['ready']and d['banks']==[12,32],d)

    if args.depth and q['t']>=24 and'effects'not in seen:
     seen.add('effects');p.evaluate('window.rd26ProbeRebirth=boss._r30.v18.rb23Rebirth')
     data=p.evaluate("""()=>{const out={};for(const name of ['rd25UnderEffects','rd25OverEffects','rd25Lightning']){drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;const fn=window[name];window[name]=()=>{};try{drawWorld(0);}finally{window[name]=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<z.length;i+=4)if(z[i]!==a[i]||z[i+1]!==a[i+1]||z[i+2]!==a[i+2])changed++;out[name]=changed;}drawWorld(0);return out;}""")
     ck('Rear and foreground electric helices visibly wrap the native body',data['rd25UnderEffects']>30 and data['rd25OverEffects']>30,data)
     ck('Overhead lightning visibly strikes down through the scene',data['rd25Lightning']>50,data)
     if args.climax:
      data=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,fn=rd26AmbientLightning;rd26AmbientLightning=()=>{};try{drawWorld(0);}finally{rd26AmbientLightning=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<z.length;i+=4)if(z[i]!==a[i]||z[i+1]!==a[i+1]||z[i+2]!==a[i+2])changed++;drawWorld(0);return{changed};}""")
      ck('Distant cinematic strikes visibly change native scene pixels',data['changed']>100,data)
   if q['mode']=='dr5Monologue':shot(p,'native-live-final-form');break
   if i%12==0:p.wait_for_timeout(1)
  relevant=[q for q in trace if q['mode']=='dr5er23rebirth'and q['t']>=14.05 and q.get('download')]
  if args.dna:
   forming=[q['dna']for q in trace if 8<q['t']<13.5 and q.get('dna')]
   ck('Double helix retains foreground background crosslinks and moving liquid lobes',bool(forming)and all(q['front']>10 and q['back']>10 and q['rungs']==9 and len(q['blobs'])==14 for q in forming))
   ck('Code formation begins with Coles reaction before the skeleton becomes solid',any(q.get('dna')and q['dna']['alpha']>0 for q in trace if 6.4<q['t']<7))
   ck('DNA code and fluid use their complete authored animation banks',len({q['codeFrame']for q in forming})==12 and len({q['fluidFrame']for q in forming})==32)
   handoff=[q['dna']for q in trace if 14<q['t']<15.8 and q.get('dna')]
   ck('Living strands converge into the native download before lightning begins',bool(handoff)and handoff[-1]['absorb']>.98 and handoff[-1]['alpha']<.02 and all(q.get('dna')is None for q in trace if q['t']>=15.8))
  ck('The turning carrier keeps animating throughout the partial download',len({q['download']['frame']for q in relevant if q['t']<24.2})==24)
  if args.depth:
   ck('Generated side and back views animate through the complete depth turntable',len({q['download']['depthFrame']for q in relevant if q['t']<23.6})==16)
   ck('Forming body stays upright while its actual depth poses turn',all(q['download']['angle']==0 and q['download'].get('depth')for q in relevant))
   fx=[q['effects']for q in relevant if 23.5<q['t']<25.2]
   ck('Electric wrap retains separate front and rear depth layers',all(v and v['front']>0 and v['back']>0 for v in fx))
   strikes=[s for v in fx for s in v['strikes']]
   ck('All main strikes travel downward from above the boss',bool(strikes)and all(s['from']['y']<s['chest']['y']<s['to']['y']and abs(s['to']['x']-s['from']['x'])<70 for s in strikes))
   if args.climax:
    spinning=[q['download']for q in relevant if q['t']<25.6]
    ck('Rotation accelerates continuously without a final settling pause',all(z['rotationRate']>a['rotationRate']and z['rotationTurns']>a['rotationTurns']for a,z in zip(spinning,spinning[1:]))and spinning[-1]['rotationRate']>spinning[0]['rotationRate']*2.9,{'firstRate':spinning[0]['rotationRate'],'lastRate':spinning[-1]['rotationRate']})
    ck('Late fast loops keep traversing front side and back poses',len({q['depthFrame']for q in spinning if q['t']>24.6})==16)
    ck('Complete final body remains withheld until peak whiteout',all(not q['fullForm']and q['nativeBlend']==0 and q['materialProgress']<1 for q in spinning)and all(q['download']['fullForm']for q in relevant if q['t']>=25.6))
    ambient=[s for v in fx for s in v['strikes']if s.get('kind')=='ambient']
    ck('Cinematic lightning reaches all nine screen lanes',len({s['lane']for s in ambient})==9,{'lanes':sorted({s['lane']for s in ambient})})
    if args.strikes:
     d=p.evaluate("""()=>{const R=window.rd26ProbeRebirth,out=[];for(const phase of [7.2,7.4]){const t=23+(-5+Math.sqrt(25+12*phase))/6,Q=rd25Pose(boss,t);RD26.fx={front:[],back:[],strikes:[]};rd25Lightning(boss,Q,R);out.push({yaw:Q.yaw,geometry:RD26.fx.strikes.map(s=>({kind:s.kind,from:s.from,chest:s.chest,to:s.to}))});}const rates=[23,24,25,25.59].map(t=>rd26StrikeClock(t,R).rate);drawWorld(0);return{out,rates,quiet:rd26StrikeClock(23+(-5+Math.sqrt(25+12*7.9))/6,R).age};}""")
     ck('Downward strike positions stay fixed while the boss keeps rotating',d['out'][0]['yaw']!=d['out'][1]['yaw']and d['out'][0]['geometry']==d['out'][1]['geometry'],d)
     ck('Ending strike cadence accelerates independently to over twenty per second',all(z>a for a,z in zip(d['rates'],d['rates'][1:]))and d['rates'][-1]>20,d['rates'])
     ck('Separate strike pulses have a release interval',d['quiet']>.72,d['quiet'])
     ck('Surrounding spiral appears only in the final storm',all(q['effects']['front']==0 and q['effects']['back']==0 for q in relevant if q['t']<23))

    d=p.evaluate("""()=>{const out=[];for(const t of [24.7,25.22,25.59]){const Q=rd25Pose(boss,t),fn=ce20Body;let calls=0;ce20Body=function(){calls++;return fn.apply(this,arguments);};let bands;try{bands=rd25Body(boss,Q);}finally{ce20Body=fn;}out.push({t,calls,bands,full:Q.fullForm});}drawWorld(0);return out;}""")
    ck('Actual preflash renderer retains partial bands and never draws native complete body',all(q['calls']==0 and q['bands']<128 and not q['full']for q in d),d)
   d=p.evaluate("""()=>{const a=RD26_ART,out=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);for(const f of [0,5,8,11]){ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(XART.get(a.body.key),...a.cells[f],0,0,512,512);const d=ctx.getImageData(0,0,Math.min(512,cv.width),512).data;let n=0,x0=999,x1=-1,h=0;const w=Math.min(512,cv.width);for(let i=0;i<d.length;i+=4)if(d[i]+d[i+1]+d[i+2]>55){const x=i/4%w;n++;x0=Math.min(x0,x);x1=Math.max(x1,x);h=(h+d[i]*3+d[i+1]*5+d[i+2]*7)>>>0;}out.push({frame:f,ink:n,width:x1-x0+1,hash:h});}ctx.restore();drawWorld(0);return out;}""")
   ck('Rendered profile narrows in depth and back art differs from the front',d[1]['width']<d[0]['width']*.65 and d[3]['width']<d[0]['width']*.65 and d[2]['hash']!=d[0]['hash']and all(v['ink']>1000 for v in d),d)
  ck('Native final-form data progressively fills the same rotating assembly',all(q['download']['source']=='native-colossus'for q in relevant)and len({q['download']['bands']for q in relevant})>=60)
  ck('The assembled form stays protected and exposes no premature Retina target',all(q['protected']and q['targets']==0 for q in relevant))
  ck('All five native final-form health budgets survive the complete download',all(q['pools']==initial['pools']for q in trace),initial)
  ck('Exactly 24 native lightning beats precede the final arena',p.evaluate("RB23.events.filter(e=>e.event==='corrupted-lightning').length===24&&RB23.events.filter(e=>e.event==='final-arena-whiteout').length===1"))
  ck('The native reveal enters final speech once',q['mode']=='dr5Monologue'and q['encounter']==2 and p.evaluate("RB23.events.filter(e=>e.event==='rebirth-complete').length===1"))
  done=next(q for q in relevant if q['t']>=25.22)
  ck('Download completes upright at the native combat scale',done['download']['progress']==1 and done['download']['angle']==0 and done['download']['size']==p.evaluate('v18Size(boss)'),done['download'])
  last=trace[-2];current=trace[-1];ck('The completed body enters speech without a position jump',abs(last['x']-current['x'])<.1 and abs(last['y']-current['y'])<.2,{'before':[last['x'],last['y']],'after':[current['x'],current['y']]})
  # Pure renderer fixture: same clock, pose and native drawImage source pixels.
  d=p.evaluate("""(t)=>{const Q=rd25Pose(boss,t);Q.x=240;Q.y=250;function pixels(draw){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);draw();const d=ctx.getImageData(0,0,cv.width,cv.height).data.slice();ctx.restore();return d;}const a=pixels(()=>rd25Body(boss,Q)),b=pixels(()=>ce20Body(boss._r30.clock,Q.x-Q.dx,Q.y-Q.dy,Q.size));let n=0,total=0;for(let i=0;i<a.length;i+=4){if(a[i+3]||b[i+3])total++;if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3])n++;}drawWorld(0);return{different:n,opaque:total};}""",26.1)
  ck('Completed download pixels match the actual native final-form renderer',d['opaque']>1000 and d['different']<d['opaque']*.015,d)
  d=p.evaluate("""()=>{const Q=rd25Pose(boss,14),A=ER23_ART.banks.symbiote;Q.x=240;Q.y=250;function pixels(draw){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);draw();const d=ctx.getImageData(0,0,cv.width,cv.height).data.slice();ctx.restore();return d;}const a=pixels(()=>rd25Body(boss,Q)),b=pixels(()=>er23DrawBank('symbiote',Q.frame,Q.x-RD25.carrierHeart[0]+128,Q.y-RD25.carrierHeart[1]+128));let n=0,total=0;for(let i=0;i<a.length;i+=4){if(a[i+3]||b[i+3])total++;if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3])n++;}drawWorld(0);return{different:n,opaque:total};}""")
  ck('Download begins with the same authored turning carrier pixels',d['opaque']>1000 and d['different']<d['opaque']*.015,d)
  if args.polish:
   intro=[q['intro']for q in trace if 7<q['t']<14 and q.get('intro')]
   ck('Skeleton gains visibility through all24 stepped opacity frames before lightning',len({q['frame']for q in intro})==24 and min(q['alpha']for q in intro)==.25 and max(q['alpha']for q in intro)==1)
   d=p.evaluate("""()=>{const out=[];for(const kind of ['carrier','body','wire']){const a=rd27Blend(kind,1-1e-7),x=a.getContext('2d').getImageData(0,0,a.width,a.height).data.slice(),b=rd27Blend(kind,1e-7),y=b.getContext('2d').getImageData(0,0,b.width,b.height).data;let diff=0;for(let i=0;i<x.length;i++)if(x[i]!==y[i])diff++;out.push({kind,diff});}const gains=RD27.audio.map(q=>q.gain);return{out,gains,ending:RD27.audio.filter(q=>q.kind==='ending').length};}""")
   ck('Carrier material and wire have pixel-continuous cyclic frame seams',all(q['diff']==0 for q in d['out']),d['out'])
   ck('Each native and ending lightning beat receives increasing mixer gain',len(d['gains'])>50 and all(z>a for a,z in zip(d['gains'],d['gains'][1:]))and d['ending']>=33,d)
  # Let the complete native speech finish; normal combat then owns the hit fixture.
  advance(p,"boss._r30.mode==='fight'",1400,12)
  if args.polish:
   d=p.evaluate("({screams:DR5.events.filter(e=>e.event==='dracodiaShriek').length,faces:DR5.intro.map(q=>q[1]),mode:boss._r30.mode})")
   ck('Only the last speech line performs one native roar and arm lift',d['screams']==1 and d['faces'][-1]==5 and 5 not in d['faces'][:-1]and d['mode']=='fight',d)
  d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;boss._lastPart=boss.parts[0];hitBoss(1);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,mode:boss._r30.mode,state,t:boss._r30.t};}""")
  ck('Final form resumes native combat and visibly flashes on a real hit',d['mode']=='fight'and d['white']>15,d);shot(p,'native-final-hit')
  p.evaluate(STEP,30);ck('Native final-form hit flash expires normally',p.evaluate('boss.flash<=0&&boss.parts.every(p=>p.flash<=0)'))
  d=p.evaluate("""async()=>{const c=Snd._audioCtx();await c.resume();const b=await c.decodeAudioData(await(await fetch(BOFA.sfx.combatEnergy0927)).arrayBuffer());let peak=0;for(const v of b.getChannelData(0))peak=Math.max(peak,Math.abs(v));return{peak,duration:b.duration};}""")
  ck('Download energy uses an approved audible mixer cue',d['peak']>.01 and d['duration']>0,d);br.close()
finally:stop()
ck('Native renderer has no page or console errors',not errors,errors)
(O/'report.json').write_text(json.dumps({'checks':checks,'trace':trace,'errors':errors},indent=2),encoding='utf8')
im=Image.new('RGB',(1280,((len(shots)+2)//3)*285),(5,10,17));g=ImageDraw.Draw(im)
for i,(f,n)in enumerate(shots):im.paste(Image.open(f).convert('RGB').resize((426,266)),((i%3)*426,(i//3)*285));g.text(((i%3)*426+3,(i//3)*285+266),n,fill='white')
im.save(O/'contact.jpg');print(json.dumps({'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks)}),flush=True)
raise SystemExit(0 if all(q['passed']for q in checks)else 1)
