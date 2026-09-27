"""Real Chromium regression and pixel proof for the single-headed hammer strike cycle."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_consistency_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
def save(pg,name):
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')")
 (out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
fixture="""(d) => {
 diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];
 spawnBoss('chromehammer');boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;
 boss.enter=false;boss._noHit=false;boss._hammer.balance0922=true;
 player.invuln=1e9;player.dead=false;player.x=(camLeftX()+camRightX())/2;player.y=VH*.80;
 hammerState(boss,'hammer');
}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  pg.evaluate(fixture,'normal')
  pg.wait_for_function("()=>['arch_whirlwind_0926','arch_orbital_sweep_0926','arch_leap_strike_0922'].every(k=>XART.rdy(k))")
  report['assets']=pg.evaluate("""()=>{
    const key='arch_orbital_sweep_0926',im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;
    const g=c.getContext('2d');g.drawImage(im,0,0);const p=g.getImageData(0,0,c.width,c.height).data;
    const edgePixels=HAMMER_STRIKE_REEL.map(r=>{let n=0;for(let x=r[0];x<r[0]+r[2];x++)for(const y of [r[1],r[1]+r[3]-1])if(p[(y*c.width+x)*4+3]>64)n++;
      for(let y=r[1];y<r[1]+r[3];y++)for(const x of [r[0],r[0]+r[2]-1])if(p[(y*c.width+x)*4+3]>64)n++;return n;});
    return {strike:XART._src[key],whirl:XART._src.arch_whirlwind_0926,width:im.width,height:im.height,edgePixels};
  }""")
  report['cycles']=[]
  for d in ['normal','hard','furious']:
   pg.evaluate(fixture,d)
   result=pg.evaluate("""()=>{
    const b=boss,h=b._hammer,states=[],frames={},idleDurations=[];let prior='',started=0;
    for(let i=0;i<2400;i++){
      if(h.state!==prior){if(prior==='hammer')idleDurations.push((i-started)/60);states.push(h.state);prior=h.state;started=i;}
      (frames[h.state]||(frames[h.state]=new Set())).add(hammerStrikeFrame(b));
      if(h.state==='shield')break;
      hammerBossTick(b,1/60);
    }
    const anchors=[];for(const [state,t] of [['hammer',.1],['warn',.2],['warn',.6],['warn',1],['recover',.1],['recover',.4]]){
      hammerState(b,state);h.t=t;const p=hammerHeadPoint(b),hit=bossHitTest(p.x,p.y),target=retinaBossTargets(b).find(q=>q._retinaId==='hammer');
      anchors.push({state,t,hit:hit&&b._hammerModuleHit==='hammer',lock:!!target&&Math.hypot(target.x-p.x,target.y-p.y)<.001});
    }
    return {difficulty:diffKey,states,frames:Object.fromEntries(Object.entries(frames).map(([k,v])=>[k,[...v]])),idleDurations,anchors};
   }""")
   report['cycles'].append(result)
   pg.wait_for_timeout(30)
  pg.evaluate(fixture,'furious')
  report['giant']=pg.evaluate("""()=>{
    const h=boss._hammer;hammerWhirlStart(boss);const states=[],idles=[],winds=[],idlePositions=[];let prior='',started=0;
    for(let i=0;i<1200;i++){
      if(h.state!==prior){const duration=(i-started)/60;if(prior==='giant_idle')idles.push(duration);if(prior==='giant_windup')winds.push(duration);states.push(h.state);if(h.state==='giant_idle')idlePositions.push({x:boss.x,y:boss.y,homeX:(camLeftX()+camRightX())/2,homeY:VH*.34});prior=h.state;started=i;}
      if(h.state==='leap_reset')break;
      hammerBossTick(boss,1/60);
    }
    hammerState(boss,'giant_dive');h.t=.25;const counter=hammerDiveCounter(boss),state=h.state;
    return {states,idles,winds,idlePositions,counter,state};
  }""")
  pg.evaluate("""()=>{
    ctx.canvas.width=1200;ctx.canvas.height=1110;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#172838';ctx.fillRect(0,0,1200,1110);
    const names=['LOWERED IDLE','LIFT','WIND-UP','CROUCH','JUMP','APEX','STRIKE','IMPACT','FOLLOW-THROUGH','LOWER','SETTLE','IDLE AGAIN'];
    boss.flash=0;for(let f=0;f<12;f++){boss.x=150+(f%4)*300;boss.y=160+Math.floor(f/4)*370;hammerOrbitalPose(boss,f,1);
      ctx.fillStyle='#dae6f0';ctx.font='15px sans-serif';ctx.textAlign='center';ctx.fillText(names[f],boss.x,340+Math.floor(f/4)*370);}
  }""");save(pg,'strike_contact')
  pg.evaluate("""()=>{
    ctx.canvas.width=1200;ctx.canvas.height=710;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#172838';ctx.fillRect(0,0,1200,710);
    hammerState(boss,'whirlwind');for(let f=0;f<8;f++){boss.x=160+(f%4)*300;boss.y=150+Math.floor(f/4)*350;boss._hammer.t=(f+.1)/18;hammerCombatDraw(boss);}
  }""");save(pg,'whirl_contact')
  pg.evaluate(fixture,'furious')
  pg.evaluate("""()=>{ctx.canvas.width=VW*SS;ctx.canvas.height=VH*SS;hammerState(boss,'hammer');shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}""")
  pg.wait_for_timeout(100)
  pg.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}");save(pg,'idle_in_game')
  if '--record' in sys.argv:
   report['videos']=[]
   for name,d,seconds,orbital in [('normal_strikes','normal',9,False),('furious_strikes','furious',14,False),('furious_orbital','furious',14,True)]:
    pg.evaluate(fixture,d)
    if orbital:pg.evaluate('()=>hammerWhirlStart(boss)')
    data=pg.evaluate("""async({seconds})=>{
      const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2100000}),chunks=[],states=[];
      rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
      const finished=new Promise(resolve=>{rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));}});
      const start=performance.now();rec.start();
      await new Promise(resolve=>{const timer=setInterval(()=>{
        const now=performance.now(),t=(now-start)/1000;
        Input.keys.arrowleft=t%6<3;Input.keys.arrowright=!Input.keys.arrowleft;loop(now);
        const s=boss?._hammer?.state;if(states[states.length-1]!==s)states.push(s);
        if(t>=seconds){clearInterval(timer);Input.keys.arrowleft=false;Input.keys.arrowright=false;resolve();}
      },1000/60);});
      rec.stop();const video=await finished;stream.getTracks().forEach(t=>t.stop());return {video,states,seconds};
    }""",{'seconds':seconds})
    (out/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',',1)[1]));data['file']=name+'.webm';report['videos'].append(data)
  br.close()
finally:stop()
report['errors']=errors
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
assert not errors
assert all(n==0 for n in report['assets']['edgePixels']),report['assets']
for q,n in zip(report['cycles'],[2,4,6]):
 assert q['states'].count('leap')==n,q
 assert all(t>=.30-1e-5 for t in q['idleDurations']),q
 assert q['frames']['hammer']==[11] and q['frames']['back']==[11],q
 assert q['frames']['warn']==[0,1,2,3] and q['frames']['leap']==[4,5,6],q
 assert q['frames']['recover']==[7,9,10,11],q
 assert all(a['hit'] and a['lock'] for a in q['anchors']),q
g=report['giant']
assert g['states'].count('giant_dive')==2 and len(g['idles'])==2 and min(g['idles'])>=.46,g
assert len(g['winds'])==2 and min(g['winds'])>=.48,g
assert abs(g['idlePositions'][1]['y']-g['idlePositions'][1]['homeY'])<.01,g
assert abs(g['idlePositions'][1]['x']-g['idlePositions'][1]['homeX'])<.01,g
assert g['counter'] and g['state']=='giant_knockback',g
