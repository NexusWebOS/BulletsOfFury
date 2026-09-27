"""Native Chromium whirlwind/disarm/stun and second-half encounter verification."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_overdrive_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
fixture="""d=>{
 diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];
 spawnBoss('chromehammer');boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;boss.enter=false;boss._noHit=false;
 boss._hammer.balance0922=true;player.invuln=1e9;player.dead=false;player.x=boss.x;player.y=VH*.8;
 hammerState(boss,'hammer');
}"""
def screenshot(pg,name):
 pg.evaluate("()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}")
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')")
 (out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True});pg.evaluate(fixture,'normal')
  pg.wait_for_function("()=>['arch_stun_static_0926','arch_arsenal_cast_0926','arch_whirlwind_0926','arch_orbital_sweep_0926','arch_stun_0920','arch_hammer_spin','arch_chromium_beam_0926'].every(k=>XART.rdy(k))")
  report['whirl']=[];report['disarm']=[];report['arsenal']=[];report['core']=[]
  for d in ['normal','hard','furious']:
   pg.evaluate(fixture,d)
   report['whirl'].append(pg.evaluate("""()=>{
    const b=boss,h=b._hammer;hammerWhirlStart(b);const states=[],passes=[],speeds=[],frames=new Set();let prior='',oldPass=-1;
    const bounds={l:h.whirl.l,r:h.whirl.r};
    for(let i=0;i<900;i++){
      const s=h.state;if(s!==prior){states.push(s);prior=s;}
      if(!h.whirl)break;
      const w=h.whirl;if(s==='whirlwind'){
        if(w.pass!==oldPass){passes.push({pass:w.pass,start:b.x,target:w.endX,lane:w.y,dir:w.dir});oldPass=w.pass;}
        frames.add(hammerWhirlFrame(b));speeds[w.pass]=Math.max(speeds[w.pass]||0,w.speed||0);
      }
      hammerBossTick(b,1/60);
    }
    return {difficulty:diffKey,bounds,states,passes,speeds,frames:[...frames],end:h.state};
   }"""))
   pg.evaluate(fixture,d)
   report['disarm'].append(pg.evaluate("""()=>{
    const b=boss,h=b._hammer;hammerWhirlStart(b);for(let i=0;i<67;i++)hammerBossTick(b,1/60);
    const hits=hammerFurious()?8:hammerHard()?6:4,trace=[];
    for(let j=0;j<hits;j++){
      // Ordinary native player bullets: collision and hitBoss route, no direct disarm call.
      pBullets.push({x:b.x,y:b.y,vx:0,vy:0,w:8,h:14,dmg:1,t:0});
      updatePlay(1/60);trace.push({state:h.state,hits:h.whirlHits});
      if(j<hits-1)for(let i=0;i<9;i++)updatePlay(1/60);
    }
    const result={difficulty:diffKey,trace,state:h.state,loose:!!h.knockedHammer,weaponGone:h.hammerDestroyed,whirlCancelled:!h.whirl,doubleDamage:hammerBossDamage(b,3)===6};
    b.hp=b.maxhp*.49;hammerBossTick(b,2);result.stunNotSkipped=h.state==='hammer_stun';result.stunVisible=b.x>camLeftX()+90&&b.x<camRightX()-90&&b.y+120<bottomHudLayout().rail.y;hammerBossTick(b,3.1);result.next=h.state;
    return result;
   }"""))
   pg.evaluate(fixture,d)
   report['arsenal'].append(pg.evaluate("""()=>{
    const b=boss,h=b._hammer;b.hp=b.maxhp*.49;const states=[],shots={},columns=[];let old='';
    for(let i=0;i<3600;i++){
      if(h.state!==old){states.push(h.state);old=h.state;if(h.state==='spell')columns.push(h.spellTargets.length);}
      eBullets=[];const before=h.state;hammerBossTick(b,1/60);shots[before]=(shots[before]||0)+eBullets.length;
    }
    return {difficulty:diffKey,states,shots,columns,phaseTwo:h.phaseTwo,chainUnbroken:!h.chainDestroyed};
   }"""))
   pg.evaluate(fixture,d)
   report['core'].append(pg.evaluate("""()=>{
    const b=boss,h=b._hammer;b.hp=b.maxhp*.35;h.mode='chaingun';h.chainHP=1;h.state='chaingun';b._hammerModuleHit='chaingun';hammerBossDamage(b,2);
    const states=[],shots={},speeds=[];let old='';for(let i=0;i<2700;i++){
      if(h.state!==old){states.push(h.state);old=h.state;}
      eBullets=[];const before=h.state,t=h.t;hammerBossTick(b,1/60);shots[before]=(shots[before]||0)+eBullets.length;
      if(before==='uzi'&&t<.7&&eBullets.length)throw new Error('Uzi fires during warning');
      if(before==='uzi')for(const q of eBullets)speeds.push(Math.hypot(q.vx,q.vy));
    }
    return {difficulty:diffKey,mode:h.mode,states,shots,maxUziSpeed:Math.max(...speeds)};
   }"""))
   pg.wait_for_timeout(30)
  pg.evaluate(fixture,'normal')
  report['contact']=pg.evaluate("""()=>{
    const old=playerHit,h=boss._hammer;let count=0;
    try{playerHit=()=>count++;hammerWhirlStart(boss);for(let i=0;i<67;i++)hammerBossTick(boss,1/60);
      player.x=boss.x;player.y=boss.y+36;h.hitCd=0;hammerBossTick(boss,1/60);const inside=count;
      player.y=boss.y-180;h.hitCd=0;hammerBossTick(boss,1/60);return {inside,outside:count-inside};
    }finally{playerHit=old;}
  }""")
  pg.evaluate(fixture,'furious')
  pg.evaluate("()=>{hammerWhirlStart(boss);hammerState(boss,'whirlwind');hammerWhirlDisarm(boss);boss._hammer.t=.45}")
  screenshot(pg,'static_stun')
  report['staticFrames']=pg.evaluate("""()=>{
    const draw=ctx.drawImage,get=XART.get,frames=new Set();let key='';
    try{XART.get=function(k){key=k;return get.call(this,k)};ctx.drawImage=function(im,...a){if(key==='arch_stun_static_0926')frames.add(a[0]+','+a[1]);return draw.call(this,im,...a)};
      for(let i=0;i<12;i++){boss._hammer.t=(i+.1)/16;hammerBossDraw(boss);}return [...frames];
    }finally{ctx.drawImage=draw;XART.get=get;}
  }""")
  pg.evaluate(fixture,'furious');pg.evaluate("()=>{boss.hp=boss.maxhp*.49;hammerBossTick(boss,1/60);for(let i=0;i<185;i++)hammerBossTick(boss,1/60)}");screenshot(pg,'cannon_rake')
  pg.evaluate("()=>{hammerSpellStart(boss);boss._hammer.t=2.1}");screenshot(pg,'committed_columns')
  report['reticleClearance']=pg.evaluate("()=>bottomHudLayout().radar.y-hammerWarningFloorY()")
  if '--record' in sys.argv:
   report['videos']=[]
   for name,mode,seconds in [('whirlwind_crossings','whirl',19),('whirlwind_disarm_static','disarm',10),('below_half_arsenal','arsenal',35),('broken_cannon_core','core',22)]:
    pg.evaluate(fixture,'furious' if mode in ['whirl','disarm'] else 'normal')
    pg.evaluate("""mode=>{if(mode==='whirl'||mode==='disarm')hammerWhirlStart(boss);else if(mode==='arsenal')boss.hp=boss.maxhp*.49;
      else{boss.hp=boss.maxhp*.35;boss._hammer.mode='chaingun';boss._hammer.chainHP=1;boss._hammer.state='chaingun';boss._hammerModuleHit='chaingun';hammerBossDamage(boss,2);}}""",mode)
    data=pg.evaluate("""async({mode,seconds})=>{
      const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2300000}),chunks=[],states=[];
      rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>{rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));}});
      const start=performance.now();let shotAt=0;rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{
        const now=performance.now(),t=(now-start)/1000;
        Input.keys.arrowleft=t%7<3.5;Input.keys.arrowright=!Input.keys.arrowleft;
        if(mode==='disarm'&&boss?._hammer.state==='whirlwind'&&t>=shotAt){pBullets.push({x:boss.x,y:boss.y,vx:0,vy:0,w:8,h:14,dmg:1,t:0});shotAt=t+.18;}
        loop(now);const s=boss?._hammer.state;if(states[states.length-1]!==s)states.push(s);
        if(t>=seconds){clearInterval(timer);Input.keys.arrowleft=false;Input.keys.arrowright=false;resolve();}
      },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return {video,states,seconds};
    }""",{'mode':mode,'seconds':seconds})
    (out/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',',1)[1]));data['file']=name+'.webm';report['videos'].append(data)
  br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors
for q,n in zip(report['whirl'],[2,3,4]):
 assert len(q['passes'])==n and len(q['frames'])==8,q
 assert all(q['speeds'][i]<q['speeds'][i+1] for i in range(n-1)),q
 assert all(abs(p['start']-(q['bounds']['l'] if p['dir']>0 else q['bounds']['r']))<.1 for p in q['passes']),q
 assert q['end']==('giant_idle' if q['difficulty']=='furious' else 'leap_reset'),q
for q in report['disarm']:
 assert q['state']=='hammer_stun' and q['loose'] and q['weaponGone'] and q['whirlCancelled'] and q['doubleDamage'] and q['stunNotSkipped'] and q['stunVisible'] and q['next']=='chaingun_draw',q
 assert all(t['state']!='hammer_stun' for t in q['trace'][:-1]),q
for q,n in zip(report['arsenal'],[3,4,5]):
 assert q['phaseTwo'] and q['chainUnbroken'] and set(q['columns'])=={n},q
 assert all(s in q['states'] for s in ['chaingun_draw','chain_warn','chaingun','chain_cool','spell','spell_blast','mega_charge','mega_beam']),q
 assert q['shots'].get('chaingun',0)>0 and q['shots'].get('chain_warn',0)==0,q
for q,v in zip(report['core'],[5.4,6,6.6]):
 assert all(s in q['states'] for s in ['uzi','mega_charge','mega_beam','spell','spell_blast']) and abs(q['maxUziSpeed']-v)<.001,q
assert report['contact']=={'inside':1,'outside':0},report['contact']
assert len(report['staticFrames'])==12,report['staticFrames']
assert report['reticleClearance']>=20,report['reticleClearance']
