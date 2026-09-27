"""Native Chromium proof: charged hammer, split Retina spikes, magnetic counter and spiral."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else '_shots/hammer_sign_recovery_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
if '--record' not in sys.argv and (out/'report.json').exists():
 report['videos']=json.loads((out/'report.json').read_text()).get('videos',[])
fixture="""d=>{
 diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];smokeTrails=[];
 // Isolate the requested encounter in these inspection fixtures; campaign asteroid behavior is unchanged.
 l5Rocks=[];l5RockT=9999;
 spawnBoss('chromehammer');boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;boss.enter=false;boss._noHit=false;
 boss._hammer.balance0922=true;player.invuln=1e9;player.dead=false;player.x=boss.x;player.y=VH*.80;
 hammerState(boss,'hammer');
}"""
breakgun="""()=>{boss.hp=boss.maxhp*.35;const h=boss._hammer;h.mode='chaingun';h.state='chain_cool';h.chainHP=1;
 const m=hammerBlasterMount(boss);pBullets.push({x:m.x,y:m.muzzleY-30,vx:0,vy:0,w:8,h:14,dmg:2,t:0});updatePlay(1/60);}"""
def shot(pg,name):
 pg.evaluate("()=>{shake=0;explosions=[];particles=[];smokeTrails=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}")
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')");(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True});pg.evaluate(fixture,'normal')
  pg.wait_for_function("()=>['storm_charge','hammer_throw','hammer_flight','hammer_lightning','chromium_spike','hammer_overhead'].every(k=>XART.rdy('arch_'+k+'_0926'))&&XART.rdy('arch_orbital_sweep_0926')&&XART.rdy('hammer_reticle')&&XART.rdy('bmfx_fov_red_tall')&&['green','yellow','red'].every(c=>XART.rdy('bmfx_badge_'+c))")
  report['worldGeometry']=pg.evaluate('()=>({world:worldWidth(),view:viewW(),retina:96,playX:PLAY.x})');report['storm']=[];report['counters']=[]
  for d in ['normal','hard','furious']:
   pg.evaluate(fixture,d);pg.evaluate(breakgun)
   report['storm'].append(pg.evaluate("""()=>{
    const h=boss._hammer,start=h.state,states=[],counts=[],targets=[],head=[];let old='';
    for(let i=0;i<2700;i++){
      if(h.state!==old){states.push(h.state);old=h.state;if(h.state==='storm_split'){counts.push(h.stormWaves.length);targets.push(h.stormWaves.map(q=>({slot:q.slot,x:q.x,y:q.y,delay:q.delay,retinaWidth:q.retinaWidth})));head.push({p:hammerHeadPoint(boss),target:h.stormTarget});}}
      hammerBossTick(boss,1/60);
    }
    return{difficulty:diffKey,start,mode:h.mode,states,counts,targets,head,charged:h.charged,chainGone:h.chainDestroyed,hammerBack:!h.hammerDestroyed};
   }"""))
   for route in ['ordinary','space','retina']:
    pg.evaluate(fixture,d)
    report['counters'].append(pg.evaluate("""route=>{
      const h=boss._hammer;hammerBoomerangStart(boss);hammerBossTick(boss,HAMMER_SPIN_TIME+.01);hammerBossTick(boss,.28);
      const T=h.throw,hp=boss.hp,partHP=h.hammerHP,bullet={x:T.x,y:T.y,vx:0,vy:0,w:8,h:14,dmg:1,t:0};
      if(route==='ordinary'){pBullets.push(bullet);updatePlay(1/60);}else if(route==='space')spaceBulletHit(bullet,false);else{const target=retinaBossTargets(boss).find(q=>q._retinaId==='hammer');retinaMissileDamage(target,1,{...bullet,kind:'gmiss'});}
      const reflected=!!h.throw?.reflected,states=[];let old='';for(let i=0;i<840;i++){if(h.state!==old){states.push(h.state);old=h.state;}hammerBossTick(boss,1/60);}
      return{difficulty:diffKey,route,reflected,bodyUndamaged:boss.hp===hp,weaponUndamaged:partHP===h.hammerHP,states};
    }""",route))
   pg.wait_for_timeout(30)
  pg.evaluate(fixture,'furious');pg.evaluate(breakgun)
  pg.evaluate("()=>{for(let i=0;i<96;i++)hammerBossTick(boss,1/60)}");shot(pg,'lightning_charge')
  pg.evaluate("()=>{for(let i=0;i<1000&&boss._hammer.state!=='storm_split';i++)hammerBossTick(boss,1/60);for(let i=0;i<20;i++)hammerBossTick(boss,1/60)}");shot(pg,'retina_split')
  pg.evaluate("()=>{for(let i=0;i<88;i++)hammerBossTick(boss,1/60)}");shot(pg,'retina_locked')
  pg.evaluate("()=>{for(let i=0;i<52;i++)hammerBossTick(boss,1/60)}");shot(pg,'red_zone_escape')
  pg.evaluate("()=>{for(let i=0;i<90;i++)hammerBossTick(boss,1/60)}");shot(pg,'chromium_spikes')
  report['spikeCollision']=pg.evaluate("""()=>{
    const h=boss._hammer,q=h.stormWaves[2],old=playerHit;let hits=0;
    try{playerHit=()=>hits++;player.invuln=0;player.x=q.x;player.y=q.y;h.hitCd=0;q.t=q.split+q.delay+q.warm-.1;hammerStormWaveTick(boss,.01);const warning=hits;
      q.t=q.split+q.delay+q.warm+.4;player.y=q.y-q.height*.8;hammerStormWaveTick(boss,.01);const inside=hits-warning;
      player.x=q.x+q.radius+15;h.hitCd=0;hammerStormWaveTick(boss,.01);return{warning,inside,outside:hits-warning-inside};
    }finally{playerHit=old;player.invuln=1e9;}
  }""")
  report['randomWarnings']=pg.evaluate("""()=>{
    const h=boss._hammer,q=h.stormWaves.slice().sort((a,b)=>a.delay-b.delay)[0],old=q.t,samples=[];
    const phases=[];for(const age of [.4,1.4,2.4]){q.t=q.split+q.delay+age;phases.push(l23FovPhase(age/q.warm));}
    for(let t=-1.01;t<=.41;t+=.02){q.t=q.split+q.delay+q.warm+t;samples.push({t,zone:!!hammerStormRedZone(q),hit:hammerStormSpikeHits(q,q.x,q.y)});}
    q.t=old;return{phases,samples,firstDamage:hammerStormSpikeTime(q,.14),order:h.stormWaves.slice().sort((a,b)=>a.delay-b.delay).map(q=>q.slot)};
  }""")
  report['rowAndReach']=pg.evaluate("""()=>{
    const h=boss._hammer,q=h.stormWaves[0],old=q.t;const frames=[];
    for(let f=0;f<16;f++){q.t=q.split+q.delay+q.warm+hammerStormSpikeTime(q,HAMMER_SPIKE_TIMES[f])+.001;const a=hammerStormSpikeShape(q);frames.push({frame:f,height:a.height,tip:q.y-a.height,base:q.y});}
    q.t=old;return{row:h.stormWaves.map(q=>({x:q.x,y:q.y,delay:q.delay,height:q.height})),frames,expected:VH*.75,playTop:PLAY.y};
  }""")
  report['throwWarnings']=pg.evaluate("""()=>{
    const tick=combatWarningTick,draw=combatWarningDraw,ret=hammerGroundReticleDraw;const calls={tick:0,draw:0,retina:0};
    try{combatWarningTick=()=>calls.tick++;combatWarningDraw=()=>calls.draw++;hammerGroundReticleDraw=()=>calls.retina++;
      hammerBoomerangStart(boss);for(let i=0;i<80;i++){hammerBossTick(boss,1/60);hammerBossDraw(boss);}
      hammerSpiralArm(boss);for(let i=0;i<110;i++){hammerBossTick(boss,1/60);hammerBossDraw(boss);}return calls;
    }finally{combatWarningTick=tick;combatWarningDraw=draw;hammerGroundReticleDraw=ret;}
  }""")
  report['spikeArt']=pg.evaluate("""()=>{
    const im=XART.get('arch_chromium_spike_0926'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height).data;
    const cells=[];for(let f=0;f<16;f++){const sx=f%8*181,sy=f<8?0:576,sh=f<8?576:510;let edges=0,minY=Infinity,maxY=0;
      for(let y=sy;y<sy+sh;y++)for(let x=sx;x<sx+181;x++)if(d[(y*c.width+x)*4+3]>128){minY=Math.min(minY,y);maxY=Math.max(maxY,y);if(x===sx||x===sx+180||y===sy||y===sy+sh-1)edges++;}
      cells.push({frame:f,edges,minY,maxY,measuredTip:HAMMER_SPIKE_TIPS[f]});
    }return {width:c.width,height:c.height,cells};
  }""")
  report['draws']=pg.evaluate("""()=>{
    const old=ctx.drawImage,get=XART.get,keys={},frames={};let key='';
    try{XART.get=function(k){key=k;return get.call(this,k)};ctx.drawImage=function(im,...a){if(key?.includes('0926')){keys[key]=(keys[key]||0)+1;(frames[key]||(frames[key]=new Set())).add(a[0]+','+a[1]);}return old.call(this,im,...a);};
      hammerStormStart(boss);for(let i=0;i<2600;i++){hammerBossTick(boss,1/60);hammerBossDraw(boss);}return{keys,frames:Object.fromEntries(Object.entries(frames).map(([k,v])=>[k,v.size]))};
    }finally{ctx.drawImage=old;XART.get=get;}
  }""")
  pg.evaluate(fixture,'normal');pg.evaluate("()=>{hammerSpiralArm(boss);boss._hammer.t=1.5;boss._hammer.spinAngle=28}");shot(pg,'angry_windup')
  report['scrollEdges']=[]
  for d in ['normal','hard','furious']:
   for side in [-1,1]:
    pg.evaluate(fixture,d)
    report['scrollEdges'].append(pg.evaluate("""side=>{
      VIEW_FIT=0;player.x=worldWidth()/2;player.y=350;camX=(worldWidth()-viewW())/2;
      hammerStormStart(boss);hammerStormTarget(boss);hammerStormImpact(boss);
      const h=boss._hammer,edge=side<0?h.stormWaves[0]:h.stormWaves[h.stormWaves.length-1],startCamera=camX;
      const geometry=JSON.stringify(h.stormWaves.map(q=>[q.x,q.y,q.delay,q.retinaWidth])),old=playerHit,hits=[];
      let frame=0;player.invuln=0;h.hitCd=0;
      try{
        playerHit=()=>hits.push({t:frame/60,x:player.x,y:player.y});
        const duration=edge.split+edge.delay+edge.warm+.65;
        for(frame=0;frame<Math.ceil(duration*60);frame++){
          Input.keys.arrowleft=side<0;Input.keys.arrowright=side>0;updatePlay(1/60);updateCamX();
        }
        return{difficulty:diffKey,side,startCamera,finalCamera:camX,playerX:player.x,edgeX:edge.x,hits,
          fixed:geometry===JSON.stringify(h.stormWaves.map(q=>[q.x,q.y,q.delay,q.retinaWidth])),retinaWidths:h.stormWaves.map(q=>q.retinaWidth)};
      }finally{playerHit=old;player.invuln=1e9;Input.keys.arrowleft=false;Input.keys.arrowright=false;}
    }""",side))
  pg.evaluate(fixture,'furious')
  pg.evaluate("()=>{hammerStormStart(boss);hammerStormTarget(boss);hammerStormImpact(boss);boss._hammer.leapFx=0;boss._hammer.t=2.55;for(const q of boss._hammer.stormWaves)q.t=q.split+2.55;}")
  report['cameraViews']=[]
  for name,x in [('left_edge_row',14),('center_row',340),('right_edge_row',670)]:
   pg.evaluate("x=>{player.x=x;player.y=390;for(let i=0;i<100;i++)updateCamX();}",x)
   shot(pg,name)
   report['cameraViews'].append(pg.evaluate("""()=>({camera:camX,left:camLeftX(),right:camRightX(),row:boss._hammer.stormWaves.map(q=>({x:q.x,y:q.y,width:q.retinaWidth,delay:q.delay}))})"""))
  report['escape']=[]
  for d in ['normal','hard','furious']:
   for move in [False,True]:
    pg.evaluate(fixture,d)
    report['escape'].append(pg.evaluate("""move=>{
      hammerStormStart(boss);hammerStormTarget(boss);hammerStormImpact(boss);
      const h=boss._hammer,q=h.stormWaves.find(q=>q.delay===0),old=playerHit;let hits=0,firstHit=null,step=0;
      try{
        for(const a of h.stormWaves)a.t=a.split+2;
        playerHit=()=>{hits++;if(firstHit===null)firstHit=step/60;};player.invuln=0;player.x=q.x;player.y=q.y-80;h.hitCd=0;
        const initial={x:player.x,y:player.y},right=q.x<(camLeftX()+camRightX())/2;
        for(let i=0;i<90;i++){
          step=i+1;
          Input.keys.arrowright=move&&right&&i<21;Input.keys.arrowleft=move&&!right&&i<21;
          updatePlay(1/60);
        }
        return{difficulty:diffKey,move,hits,firstHit,initial,final:{x:player.x,y:player.y},radius:q.radius};
      }finally{playerHit=old;player.invuln=1e9;Input.keys.arrowright=false;Input.keys.arrowleft=false;}
    }""",move))
  report['zonePixels']=pg.evaluate("""()=>{
    const q={x:240,y:430,height:384,radius:20,split:.35,delay:0,warm:3,active:1.52,t:2.5};
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerStormRedZoneDraw(q);
    const data=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height),w=ctx.canvas.width;let checked=0,unwarned=0;
    q.t=q.split+q.warm+.4;
    for(let y=q.y-q.height+1;y<=q.y+3;y+=3)for(let x=q.x-q.radius;x<=q.x+q.radius;x++)if(hammerStormSpikeHits(q,x,y)){
      checked++;if(data.data[(Math.floor(y)*w+Math.floor(x))*4+3]<12)unwarned++;
    }
    const bands=[90,230,390].map(y=>{const xs=[];for(let x=180;x<=300;x++)if(data.data[(y*w+x)*4+3]>12)xs.push(x);return{y,left:Math.min(...xs),right:Math.max(...xs),width:xs.length};});
    const corners=[192,287].map(x=>data.data[(47*w+x)*4+3]),crown=data.data[(48*w+240)*4+3];
    ctx.restore();return{checked,unwarned,bands,corners,crown};
  }""")
  report['signPixels']=pg.evaluate("""()=>{
    const q={x:240,y:430,height:384,retinaWidth:96,split:.35,delay:0,warm:3};const phases=[];
    ctx.save();ctx.setTransform(1,0,0,1,0,0);
    for(const age of [.4,1.4,2.4]){
      q.t=q.split+age;ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerStormRowAlertDraw(q);
      const a=hammerStormRowAlert(q),im=ctx.getImageData(216,50,48,36).data;let opaque=0;const channels=[0,0,0];
      for(let i=0;i<im.length;i+=4)if(im[i+3]>64){opaque++;for(let c=0;c<3;c++)channels[c]+=im[i+c];}
      phases.push({key:a.key,y:a.y,opaque,channels});
    }
    ctx.restore();return phases;
  }""")
  pg.evaluate(fixture,'normal');pg.evaluate("()=>{hammerSpiralArm(boss);boss._hammer.t=1.5;boss._hammer.spinAngle=28}")
  report['artEdges']=pg.evaluate("""()=>{
    return [['arch_storm_charge_0926',HAMMER_CHARGE_REEL],['arch_hammer_throw_0926',HAMMER_THROW_REEL],['arch_hammer_overhead_0926',HAMMER_OVERHEAD_REEL]].map(([key,rects])=>{
      const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height).data;
      const edges=rects.map(r=>{let n=0;for(let x=r[0];x<r[0]+r[2];x++)for(const y of [r[1],r[1]+r[3]-1])if(d[(y*c.width+x)*4+3]>128)n++;for(let y=r[1];y<r[1]+r[3];y++)for(const x of [r[0],r[0]+r[2]-1])if(d[(y*c.width+x)*4+3]>128)n++;return n;});return {key,edges};
    });
  }""")
  report['spiral']=pg.evaluate("""()=>{
    const plan=boss._hammer.spiralPlan;return [-1,1].map(side=>{const T={...plan,side};return{side,points:Array.from({length:41},(_,i)=>hammerSpiralPoint(T,i/40)),center:{x:T.cx,y:T.cy},rx:T.rx,ry:T.ry};});
  }""")
  report['recovery']=[];report['difficultyTiming']=[]
  for d in ['normal','hard','furious']:
   for side in [-1,1]:
    pg.evaluate(fixture,d)
    report['recovery'].append(pg.evaluate("""side=>{
      hammerStormStart(boss);boss.x=side<0?80:600;boss.y=350;hammerStormTarget(boss);hammerStormImpact(boss);
      const h=boss._hammer,plan={...h.stormRecovery},poses=[],points=[];let previous={x:boss.x,y:boss.y},maxStep=0;
      for(let i=0;i<180;i++){
        player.x=i%60<30?10:670;camX=i%60<30?0:worldWidth()-viewW();hammerBossTick(boss,1/60);
        const step=Math.hypot(boss.x-previous.x,boss.y-previous.y);maxStep=Math.max(maxStep,step);previous={x:boss.x,y:boss.y};
        const pose=hammerStormPoseFrame(boss);if(poses[poses.length-1]!==pose)poses.push(pose);
        if(i%6===0)points.push({t:h.t,x:boss.x,y:boss.y,camera:camX,pose});
      }
      return{difficulty:diffKey,side,plan,poses,points,maxStep,done:h.stormRecovery.done,home:h.stormHome,final:{x:boss.x,y:boss.y},state:h.state};
    }""",side))
   report['difficultyTiming'].append(pg.evaluate("""()=>{
     const q=boss._hammer.stormWaves[0],frames=[];let firstDamage=null,peak=null;
     for(let i=0;i<500;i++){
       const t=i/1000;q.t=q.split+q.delay+q.warm+t;const a=hammerStormSpikeShape(q);
       if(a&&frames[frames.length-1]!==a.f)frames.push(a.f);
       if(firstDamage===null&&hammerStormSpikeHits(q,q.x,q.y))firstDamage=t;
       if(peak===null&&a?.height>=q.height-.001)peak=t;
     }
     return{difficulty:diffKey,rate:q.riseRate,firstDamage,peak,frames,redWarning:q.warm-2,spacing:Math.min(...boss._hammer.stormWaves.filter(q=>q.delay>0).map(q=>q.delay))};
   }"""))
  pg.evaluate(fixture,'furious');pg.evaluate("()=>{hammerStormStart(boss);boss.x=80;boss.y=350;hammerStormTarget(boss);hammerStormImpact(boss);player.x=340;camX=100;}")
  for name,time in [('recovery_impact',.10),('recovery_follow',.26),('recovery_lift',.44),('recovery_lower',.64),('recovery_return',1.05),('recovery_home',2.2)]:
   pg.evaluate("t=>{while(boss._hammer.t<t)hammerBossTick(boss,1/60)}",time);shot(pg,name)
  if '--record' in sys.argv:
   report['videos']=[]
   for name,difficulty,seconds in [('storm_normal','normal',24),('storm_hard','hard',24),('storm_furious','furious',24)]:
    mode='storm';pg.evaluate(fixture,difficulty)
    if mode=='storm':pg.evaluate(breakgun)
    else:pg.evaluate("()=>hammerBoomerangStart(boss)")
    data=pg.evaluate("""async({mode,seconds})=>{
      const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2500000}),chunks=[],states=[];
      rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
      const start=performance.now();let sent=false,planned=false;rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{
        const now=performance.now(),t=(now-start)/1000;
        Input.keys.arrowleft=mode==='storm'?t%10<5:t%6<3;Input.keys.arrowright=!Input.keys.arrowleft;
        const h=boss?._hammer;
        if(mode!=='storm'&&h?.throw&&!sent&&h.throw.t>.23){const q=h.throw;pBullets.push({x:q.x,y:q.y,vx:0,vy:0,w:8,h:14,dmg:1,t:0});sent=true;}
        loop(now);
        if(mode!=='storm'&&!planned&&h.state==='revenge_charge'){h.spiralPlan.side=mode==='left'?-1:1;planned=true;}
        const s=h?.state;if(states[states.length-1]!==s)states.push(s);
        if(t>=seconds){clearInterval(timer);Input.keys.arrowleft=false;Input.keys.arrowright=false;resolve();}
      },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return{video,states,seconds};
    }""",{'mode':mode,'seconds':seconds})
    (out/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',',1)[1]));data['file']=name+'.webm';report['videos'].append(data)
  br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors,errors
for q,n in zip(report['storm'],[8,8,8]):
 assert q['start']=='storm_raise' and q['mode']=='storm' and q['charged'] and q['chainGone'] and q['hammerBack'],q
 assert set(q['counts'])=={n} and all(s in q['states'] for s in ['storm_raise','storm_idle','storm_warn','storm_slam','storm_split','spin','throw','hammer_catch']),q
 assert not any(s in q['states'] for s in ['uzi','enrage','core_orbit']),q
 assert all(abs(h['p']['x']-h['target']['x'])<.1 and abs(h['p']['y']-h['target']['y'])<.1 for h in q['head']),q['head']
for encounter in report['storm']:
 for row in encounter['targets']:
  assert len(set(q['delay'] for q in row))==8,row
  assert all(q['retinaWidth']==96 for q in row),row
  assert row[0]['x']==report['worldGeometry']['playX'] and row[-1]['x']==report['worldGeometry']['world']-report['worldGeometry']['playX'],row
 orders=[tuple(q['slot'] for q in sorted(row,key=lambda q:q['delay'])) for row in encounter['targets']]
 assert all(a!=b for a,b in zip(orders,orders[1:])),orders
assert report['randomWarnings']['phases']==['green','yellow','red']
assert all(not q['hit'] for q in report['randomWarnings']['samples'] if q['t']<report['randomWarnings']['firstDamage'])
assert all(q['zone'] for q in report['randomWarnings']['samples'] if q['t']>=-1)
assert any(q['hit'] for q in report['randomWarnings']['samples'] if q['t']>.14)
for q in report['counters']:
 assert q['reflected'] and q['bodyUndamaged'] and q['weaponUndamaged'] and all(s in q['states'] for s in ['throw','hammer_catch','revenge_charge','hammer']),q
assert report['worldGeometry']=={'world':680,'view':480,'retina':96,'playX':4},report['worldGeometry']
for q in report['scrollEdges']:
 assert q['fixed'] and all(w==96 for w in q['retinaWidths']),q
 assert abs(q['finalCamera']-q['startCamera'])>95,q
 assert any(abs(h['x']-q['edgeX'])<20 for h in q['hits']),q
for view in report['cameraViews']:
 assert view['row']==report['cameraViews'][0]['row'],view
assert report['zonePixels']['checked']>1000 and report['zonePixels']['unwarned']==0,report['zonePixels']
assert all(b['width']==96 for b in report['zonePixels']['bands']),report['zonePixels']
assert max(report['zonePixels']['corners'])==0 and report['zonePixels']['crown']>12,report['zonePixels']
assert [a['key'] for a in report['signPixels']]==['bmfx_badge_'+c for c in ['green','yellow','red']]
assert all(a['opaque']>100 and a['y']>=46 for a in report['signPixels']),report['signPixels']
g,y,r=[a['channels'] for a in report['signPixels']]
assert g[1]>g[0] and y[0]>y[2] and y[1]>y[2] and r[0]>r[1],report['signPixels']
for escape in report['escape']:
 if escape['move']:assert escape['hits']==0 and abs(escape['final']['x']-escape['initial']['x'])>escape['radius']+12,escape
 else:assert escape['hits']>0 and escape['firstHit']>=1,escape
assert report['throwWarnings']=={'tick':0,'draw':0,'retina':0},report['throwWarnings']
assert len(set(q['y'] for q in report['rowAndReach']['row']))==1
assert abs(max(f['height'] for f in report['rowAndReach']['frames'])-report['rowAndReach']['expected'])<.1
assert all(q['edges']==0 and abs(q['minY']-q['measuredTip'])<2 for q in report['spikeArt']['cells']),report['spikeArt']
assert report['spikeCollision']=={'warning':0,'inside':1,'outside':0},report['spikeCollision']
for k in ['arch_storm_charge_0926','arch_hammer_lightning_0926','arch_hammer_throw_0926','arch_hammer_overhead_0926','arch_hammer_flight_0926','arch_chromium_spike_0926']:
 assert report['draws']['keys'].get(k,0)>0,(k,report['draws'])
for q in report['artEdges']:assert max(q['edges'])==0,q

for r in report['recovery']:
 assert r['poses']==[7,8,9,10,11] and r['done'] and r['state']=='storm_split',r
 assert r['final']==r['home'] and r['home']=={'x':340,'y':174.08} and r['maxStep']<7,r
 assert all(p['x']>=min(r['plan']['ox'],340)-.001 and p['x']<=max(r['plan']['ox'],340)+.001 and p['y']>=174.08-.001 and p['y']<=350.001 for p in r['points']),r
for r,peak,spacing in zip(report['difficultyTiming'],[.38,.212,.136],[.5,.3,.2]):
 assert abs(r['peak']-peak)<.002 and r['redWarning']==1 and abs(r['spacing']-spacing)<.001,r
 assert r['frames'][:7]==list(range(7)),r
