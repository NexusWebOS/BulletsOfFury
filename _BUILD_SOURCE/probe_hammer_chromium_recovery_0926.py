"""Actual game canvas, native weapon routes, slow heal / cancellation / reconstruction."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_chromium_recovery_0926');out.mkdir(exist_ok=True)
report={};errors=[];port,stop=sh.serve(sh.GAME)
fixture="""d=>{
 diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];smokeTrails=[];l5Rocks=[];l5RockT=9999;
 spawnBoss('chromehammer');boss.x=340;boss.y=256;boss.enter=false;boss._noHit=false;boss.hp=boss.maxhp*.35;boss._hammer.balance0922=true;
 player.x=340;player.y=410;player.invuln=1e9;player.dead=false;camX=100;boss._hammer.chainDestroyed=true;hammerStormStart(boss);
}"""
hit="""route=>{
 const h=boss._hammer,head=hammerHeadPoint(boss),bullet={x:head.x,y:head.y,vx:0,vy:0,w:8,h:14,dmg:h.recovery.coreHP+1,t:0};
 if(route==='ordinary'){pBullets.push(bullet);updatePlay(1/60);}
 else if(route==='space')spaceBulletHit(bullet,false);
 else{const target=retinaBossTargets(boss).find(q=>q._retinaId==='hammer');retinaMissileDamage(target,bullet.dmg,{...bullet,kind:'gmiss'});}
}"""
def shot(pg,name):
 pg.evaluate('()=>{shake=0;powerups=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')");(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True});pg.evaluate(fixture,'normal')
  pg.wait_for_function("()=>['arch_storm_charge_0926','arch_orbital_sweep_0926','arch_stun_0920','arch_stun_static_0926','arch_effects','arch_hammer_lightning_0926','bmbar_fill_solid','bmbar_frame_boss'].every(k=>XART.rdy(k))")
  report['routes']=[];report['completion']=[]
  for d in ['normal','hard','furious']:
   for route in ['ordinary','space','retina']:
    pg.evaluate(fixture,d)
    before=pg.evaluate("""()=>{
     const initial=boss.hp,max=boss.maxhp;for(let i=0;i<240;i++)hammerBossTick(boss,1/60);
     const R=boss._hammer.recovery,target=retinaBossTargets(boss).find(q=>q._retinaId==='hammer');
     return{initial,max,hp:boss.hp,applied:R.applied,pending:R.amount-R.applied,target:!!target,head:hammerHeadPoint(boss)};
    }""")
    pg.evaluate(hit,route)
    after=pg.evaluate("""()=>{
     const h=boss._hammer,broken={hp:boss.hp,state:h.state,status:h.recovery.status,applied:h.recovery.applied,revoked:h.recovery.revoked,target:retinaBossTargets(boss).some(q=>q._retinaId==='hammer'),burst:!!h.coreBurst};
     const states=[];for(let i=0;i<420;i++){if(states[states.length-1]!==h.state)states.push(h.state);hammerBossTick(boss,1/60);}
     return{broken,states,hp:boss.hp,restored:!h.hammerDestroyed&&h.empowered&&h.charged,status:h.recovery.status};
    }""")
    report['routes'].append({'difficulty':d,'route':route,'before':before,'after':after})
   pg.evaluate(fixture,d)
   report['completion'].append(pg.evaluate("""()=>{
    const initial=boss.hp,max=boss.maxhp,h=boss._hammer,samples=[];
    for(let i=0;i<510;i++){hammerBossTick(boss,1/60);if(i%30===0)samples.push({t:(i+1)/60,hp:boss.hp,state:h.state,level:h.empowerLevel});}
    return{difficulty:diffKey,initial,max,hp:boss.hp,status:h.recovery.status,applied:h.recovery.applied,state:h.state,samples};
   }"""))
  pg.evaluate(fixture,'normal')
  for name,t in [('unpowered',.7),('pixel_rise',2.1),('charging',4.1),('charged',6.8),('heal_complete',7.6)]:
   pg.evaluate("t=>{while(boss._hammer.t<t)updatePlay(1/60)}",t);shot(pg,name)
  pg.evaluate(fixture,'normal');pg.evaluate("()=>{for(let i=0;i<240;i++)updatePlay(1/60)}");pg.evaluate(hit,'retina');pg.evaluate("()=>{for(let i=0;i<8;i++)updatePlay(1/60)}");shot(pg,'core_burst')
  for name,t in [('stunned',1.2),('rebuild',4.85),('restored',6.65)]:
   # The state clock resets; advance by fixed duration from the preceding capture.
   delta={'stunned':1.2,'rebuild':3.65,'restored':1.8}[name]
   pg.evaluate("n=>{for(let i=0;i<n;i++)updatePlay(1/60)}",round(delta*60));shot(pg,name)
  report['pixels']=pg.evaluate("""()=>{
    const h=boss._hammer,key='arch_storm_charge_0926',original=XART.get(key),tones=[];
    for(let tone=0;tone<3;tone++){
      const im=hammerChromiumSheet(key,tone);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);ctx.drawImage(im,1163,0,373,506,0,0,373,506);
      const data=ctx.getImageData(0,0,373,506).data;let solid=0,sum=[0,0,0];for(let i=0;i<data.length;i+=4)if(data[i+3]>128){solid++;for(let j=0;j<3;j++)sum[j]+=data[i+j];}ctx.restore();tones.push({tone,solid,sum});
    }
    return{tones};
  }""")
  pg.evaluate(fixture,'normal')
  report['jitter']=pg.evaluate("""()=>{
    const samples=[];for(let i=0;i<150;i++)hammerBossTick(boss,1/60);for(let i=0;i<60;i++){hammerBossTick(boss,1/60);samples.push(hammerChargeJitter(boss));}return samples;
  }""")
  report['barPixels']=pg.evaluate("""()=>{
    const h=boss._hammer,R=h.recovery,lo=boss.hp/boss.maxhp,hi=(boss.hp+R.amount-R.applied)/boss.maxhp,frames=[];
    ctx.save();ctx.setTransform(1,0,0,1,0,0);
    for(const t of [1.50,1.57,1.64]){
      h.chromiumT=t;ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerRecoveryBarDraw(20,20,400,18,false);
      const d=ctx.getImageData(0,0,450,60).data;let min=450,max=0,pixels=0,totalAlpha=0;
      for(let y=20;y<38;y++)for(let x=0;x<450;x++){const a=d[(y*450+x)*4+3];if(a>12){min=Math.min(min,x);max=Math.max(max,x);pixels++;totalAlpha+=a;}}
      frames.push({min,max,pixels,totalAlpha});
    }
    R.status='cancelled';ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerRecoveryBarDraw(20,20,400,18,false);
    const gone=ctx.getImageData(0,0,450,60).data.every((v,i)=>i%4!==3||v===0);ctx.restore();return{lo,hi,frames,gone};
  }""")
  report['hitFlashPixels']=pg.evaluate("""()=>{
    const h=boss._hammer;h.empowered=true;h.empowerLevel=1;h.state='storm_idle';h.t=0;boss.x=240;boss.y=230;
    const sums=[];ctx.save();ctx.setTransform(1,0,0,1,0,0);
    for(const f of [0,.16]){boss.flash=f;ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerStormDraw(boss);
      const d=ctx.getImageData(160,160,160,160).data;let sum=0;for(let i=0;i<d.length;i++)sum+=d[i];sums.push(sum);}
    ctx.restore();return sums;
  }""")
  if '--record' in sys.argv:
   report['videos']=[]
   for name,counter,seconds in [('successful_recovery',False,20),('break_core_cancel_heal',True,20)]:
    pg.evaluate(fixture,'normal')
    data=pg.evaluate("""async({counter,seconds})=>{
      const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:3000000}),chunks=[],states=[];
      rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
      const start=performance.now();let shot=false;rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{
        const now=performance.now(),t=(now-start)/1000,h=boss._hammer;
        if(counter&&!shot&&t>4.5){const target=retinaBossTargets(boss).find(q=>q._retinaId==='hammer');retinaMissileDamage(target,h.recovery.coreHP+1,{kind:'gmiss',x:target.x,y:target.y});shot=true;}
        loop(now);if(states[states.length-1]!==h.state)states.push(h.state);
        if(t>=seconds){clearInterval(timer);resolve();}
      },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return{video,states,seconds};
    }""",{'counter':counter,'seconds':seconds})
    (out/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',',1)[1]));data['file']=name+'.webm';report['videos'].append(data)
  elif (out/'report.json').exists():report['videos']=json.loads((out/'report.json').read_text()).get('videos',[])
  br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors,errors
for r in report['routes']:
 b,a=r['before'],r['after'];assert b['target'] and b['initial']<b['hp']<b['initial']+b['max']*.25,r
 assert a['broken']['state']=='storm_stun' and a['broken']['status']=='cancelled' and not a['broken']['target'] and a['broken']['burst'],r
 assert abs(a['broken']['hp']-b['initial'])<.001 and abs(a['hp']-b['initial'])<.001 and a['restored'],r
 assert all(s in a['states'] for s in ['storm_stun','storm_rebuild','storm_idle']),r
for r in report['completion']:
 assert r['status']=='complete' and abs(r['hp']-r['initial']-r['max']*.25)<.001,r
 assert all(a['hp']<=b['hp'] for a,b in zip(r['samples'],r['samples'][1:])),r
assert len(set((j['x'],j['y']) for j in report['jitter']))>10,report['jitter']
assert len(set(tuple(t['sum']) for t in report['pixels']['tones']))==3,report['pixels']
bar=report['barPixels'];assert bar['gone'] and len(set(f['totalAlpha'] for f in bar['frames']))>1,bar
assert all(abs(f['min']-(20+400*bar['lo']))<2 and abs(f['max']-(20+400*bar['hi']))<2 and f['pixels']>100 for f in bar['frames']),bar
assert report['hitFlashPixels'][0]!=report['hitFlashPixels'][1],report['hitFlashPixels']
