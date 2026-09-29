"""Real Chromium QA: matched fixed workloads, live replay and vent frames."""
import sys,json,base64,ast,time
from pathlib import Path
from PIL import Image
GAME=next(p for p in Path(__file__).resolve().parents if (p/'assets/game.js').is_file())
HERE=Path(__file__).parent
sys.path.insert(0,str(GAME/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

def baseline():
    # Reverse only this pass's guarded edits, keeping the incoming HAMA/mission work.
    s=(GAME/'assets/game.js').read_text(encoding='utf-8')
    helper=next(n.value.value for n in ast.parse((HERE/'patch_pickup_cache.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='helper' for t in n.targets))
    s=s.replace(helper,'')
    a=s.index('function iconBlit(');b=s.index('/* ============================================================\n   GRAVITY MODE V2',a)
    s=s[:a]+s[a:b].replace('lateShadowImage(ctx,','ctx.drawImage(').replace('lateShadowImage(g,','g.drawImage(')+s[b:]
    a=s.index('function drawScrate(');b=s.index('function drawEffects(',a)
    s=s[:a]+s[a:b].replace('lateShadowImage(ctx,','ctx.drawImage(').replace('lateShadowImage(g,','g.drawImage(')+s[b:]
    edits={}
    def capture(p,v):edits[p]=v
    patch=(HERE/'patch_performance.py').read_text(encoding='utf-8')
    exec(patch[patch.index('CACHE='):].replace('edit(', 'capture('),{'capture':capture})
    for old,new in reversed(edits['assets/game.js']):
        assert s.count(new)==1,new[:80]
        s=s.replace(new,old,1)
    import hashlib
    assert hashlib.sha256(s.encode()).hexdigest().startswith('bd466181ffb2'), 'Baseline must exactly match incoming engine'
    return s

SETUP=r'''stage=>{
 ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='cole';
 pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(stage);setState(GS.PLAY);story=null;
 s6Opening=null;run._mission29OpeningDone=true;stageTimer=28;setRenderScale(2);_renderQuality='high';
 player.dead=false;player.invuln=0;run.weapon=0;run.wlevel=6;run.wlevels=WEAPONS.map(()=>6);
 enemies.length=0;eBullets.length=0;pBullets.length=0;particles.length=0;explosions.length=0;powerups.length=0;floaters.length=0;pilotFx.length=0;pImpacts.length=0;
 boss=null;bossActive=false;subBoss=null;subBossActive=false;efxBursts.length=0;story=null;hudCallout=null;stageEvent=null;
 for(let i=0;i<60;i++)pBullets.push({kind:'mg',x:40+(i%10)*42,y:70+Math.floor(i/10)*50,vx:0,vy:-8,lv:6,t:.2,w:5,h:16});
 for(let i=0;i<40;i++)pBullets.push({kind:'coletri',x:35+(i%10)*43,y:95+Math.floor(i/10)*70,vx:0,vy:-8,lv:6,t:.2,w:5,h:16});
 for(let i=0;i<180;i++)particles.push({x:40+(i%18)*22,y:60+Math.floor(i/18)*32,t:.1,life:.4,r:2.5,color:'#ffc23a',vx:0,vy:0});
 for(let i=0;i<4;i++)powerups.push({kind:i%2?'scrate':'sonicbox',x:50+i*110,y:380,t:.25,flash:0});
 if(stage===7){mapScroll=1400;drawBG(0);}
 if(stage===6){_bg6T=28;}
 window.__times=[];window.__intervals=[];window.__last=0;window.__measure=false;window.__fixed=true;
 window.__fixedLoop=function(t){if(!window.__fixed)return;const start=performance.now();drawWorld(0);if(window.__measure){window.__times.push(performance.now()-start);if(window.__last)window.__intervals.push(t-window.__last);window.__last=t;}requestAnimationFrame(window.__fixedLoop);};
 requestAnimationFrame=window.__bofRealRAF;requestAnimationFrame(window.__fixedLoop);
}'''
CHECKS=r'''()=>{
 const o={},di=ctx.drawImage,st=ctx.stroke,lt=ctx.lineTo;let blur=0,filters=0,strokes=0,lines=0,calls=[];
 ctx.drawImage=function(im,...args){blur+=ctx.shadowBlur>0;filters+=ctx.filter!=='none';calls.push(args);return di.call(this,im,...args);};
 ctx.save();ctx.shadowBlur=0;ctx.filter='none';ctx.setTransform(SS,0,0,SS,0,0);
 for(const lv of [1,6,8])for(const rc of P87_ROUND)p87Draw(rc,100,100,0,48,lv,wlvGlow(lv),.65);
 for(const lv of [6,8])coleTriDraw({x:100,y:150,vx:0,vy:-8,t:.1,lv});
 o['rounds and Cole tridents have no live main-canvas blur/filter']=blur===0&&filters===0;
 const src=p87Body(6);for(let i=0;i<250;i++)lateSpriteBake(src,[0,192,192,192],30+i*.1,30,'#aaf',7,null,false);
 o['sprite effect cache stays bounded after more than its cap']=_lateSpriteCache.size<=LATE_SPRITE_CAP&&_lateSpriteBytes<=LATE_SPRITE_BYTES;
 const cap=_GLOW_CAP;_GLOW_CAP=4;let got=true;for(let i=0;i<12;i++)got=got&&!!bakeGlow('msl_lizzie',20+i,44,null,null,'#ffc21a',9,false);
 o['full glow cache evicts rather than restoring live Gaussian blurs']=got&&_glowOrder.size<=4&&Object.keys(_glowc).length<=4;_GLOW_CAP=cap;
 _GLOW_CAP=0;o['explicit cache-disable diagnostic remains available']=bakeGlow('msl_lizzie',30,44,null,null,'#ffc21a',9,false)===null;_GLOW_CAP=cap;
 ctx.stroke=function(){strokes++;return st.apply(this,arguments);};ctx.lineTo=function(){lines++;return lt.apply(this,arguments);};bg6RainDraw(1,VW,0,VH);
 o['dense two-depth rain keeps all 382 drops in three strokes']=strokes===3&&lines===382;ctx.stroke=st;ctx.lineTo=lt;
 const e={x:200,y:120,w:50,h:50};enemies.push(e);const B={t:.1,warm:1,family:'rime'};
 calls=[];o['ordinary enemy warning emits no floating triangle']=!l23WarnSymbolDraw(e,B)&&calls.length===0;
 calls=[];o['lane owned by an ordinary enemy emits no floating triangle']=!l23WarnSymbolDraw({owner:e,x:200,y:120},B)&&calls.length===0;
 calls=[];o['boss warning symbol remains visible']=l23WarnSymbolDraw({x:200,y:120,w:50,h:50},B)&&calls.length>0;enemies.pop();
 o['vent uses the authored buildup, both flow poses and both withdrawal poses']=JSON.stringify([0,.2,.3,.8,1.02].map(stage7SluiceFrame))===JSON.stringify([2,3,4,5,6]);
 ctx.restore();ctx.drawImage=di;return o;
}'''

def main():
 out=GAME/'_shots/performance_0929';out.mkdir(parents=True,exist_ok=True)
 original=baseline();port,stop=sh.serve(str(GAME));result={'benchmarks':{},'checks':{},'errors':[]}
 with sync_playwright() as p:
  for version in ['before','after']:
   br=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
   pg=br.new_page(viewport={'width':1440,'height':1000})
   pg.on('pageerror',lambda e:result['errors'].append(str(e)))
   pg.on('console',lambda m:result['errors'].append(m.text) if m.type=='error' else None)
   if version=='before':pg.route('**/assets/game.js*',lambda route:route.fulfill(body=original,content_type='application/javascript'))
   pg.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=120000)
   pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(sh.TRAP_RAF)
   # Drain the one previously scheduled engine callback before installing a fixed scene.
   # Without this, the first (slowest) sample can advance the simulation once during warmup.
   pg.evaluate('()=>{loop=function(){};}');pg.wait_for_timeout(400)
   result['benchmarks'][version]=[]
   for stage in [6,7,8]:
    pg.evaluate(SETUP,stage);pg.wait_for_timeout(2000)
    pg.evaluate('()=>{window.__measure=true;window.__times=[];window.__intervals=[];window.__last=0;}');pg.wait_for_timeout(4000)
    row=pg.evaluate('''()=>{window.__fixed=false;const a=window.__times.slice(5).sort((a,b)=>a-b),d=window.__intervals.slice(5);return {stage:run.stage,scale:SS,fps:1000/(d.reduce((a,b)=>a+b,0)/d.length),mean:a.reduce((a,b)=>a+b,0)/a.length,p95:a[Math.floor(a.length*.95)],bullets:pBullets.length,particles:particles.length,pickups:powerups.length};}''')
    assert [row['scale'],row['bullets'],row['particles'],row['pickups']]==[2,100,180,4],row
    result['benchmarks'][version].append(row);print(version,json.dumps(row),flush=True)
    pg.evaluate(sh.TRAP_RAF)
    data=pg.evaluate('()=>cv.toDataURL("image/png")');(out/f'fixed_{version}_stage{stage}.png').write_bytes(base64.b64decode(data.split(',')[1]))
   if version=='after':
    pg.wait_for_function("()=>['nca_87','mfx_mg_2_4','mfx_mg_4_4','msl_lizzie','s7sluice_vent','bmfx_alert_green_danger'].every(k=>XART.rdy(k))",timeout=120000)
    result['checks']=pg.evaluate(CHECKS)
    print(json.dumps(result['checks']),flush=True)
    pg.evaluate('''()=>{beginStage(7);setState(GS.PLAY);story=null;mapScroll=1400;drawBG(0);setRenderScale(2);enemies.length=0;pBullets.length=0;eBullets.length=0;powerups.length=0;particles.length=0;explosions.length=0;efxBursts.length=0;floaters.length=0;pilotFx.length=0;hudCallout=null;}''')
    imgs=[]
    for age in [-.5,0,.18,.28,.48,.80,1.02,1.15]:
     pg.evaluate('''age=>{drawBG(0);const events=stage7SluiceEvents();for(const e of events)e.tier=99;for(let i=0;i<2;i++){const e=events[i];e.tier=0;e.side=i===0?-1:1;e.row=_masterSrcY+VH*.55;e.live=true;e.done=age>=1.1;e.t=stage7SluiceWarn()+age;}stage7SluiceDraw();}''',age)
     data=pg.evaluate('()=>cv.toDataURL("image/png")');f=out/f'vent_{str(age).replace(".","_")}.png';f.write_bytes(base64.b64decode(data.split(',')[1]));imgs.append(Image.open(f).copy())
    imgs[0].save(out/'vent_repaired.gif',save_all=True,append_images=imgs[1:],duration=160,loop=0)
   br.close()
 stop();(out/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 return bool(result['errors'] or not all(result['checks'].values()))
if __name__=='__main__':sys.exit(main())
