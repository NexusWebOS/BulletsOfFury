"""Native Stage4-9 flight/weapon audit. Retains authored wave specs.
No combat behavior is replaced by this verification-only script.
"""
from pathlib import Path
import sys,json,base64,argparse,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
P=argparse.ArgumentParser();P.add_argument('--stages',nargs='+',type=int,default=list(range(4,10)));P.add_argument('--after',action='store_true');args=P.parse_args()
O=R/'_shots/enemy_flight_1031';O.mkdir(exist_ok=True);D=O/('after'if args.after else'before');D.mkdir(exist_ok=True);(D/'frames').mkdir(exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));rows=[];errors=[]
LAB=r'''()=>{
 window.E=null;window.FA31={owner:null,allowSpawn:true,keys:new WeakMap(),seen:new WeakSet(),draws:[],shots:[],muzzles:[],cues:[],base:{get:XART.get,tint:xartTint,draw:ctx.drawImage,enemy:drawEnemy,spawn:spawnEnemy,shoot:eShootT,wm:wm26Emit,naval:navalFlash,begin:ai27Begin,end:ai27End,play:Snd.play}};
 spawnEnemy=function(){if(!FA31.allowSpawn&&ai27Context!==E)return null;return FA31.base.spawn.apply(this,arguments);};
 drawEnemy=function(e){const old=FA31.owner,root=FA31.root;FA31.owner=e===E?e:null;if(e===E)FA31.root=ctx.getTransform();try{return FA31.base.enemy.apply(this,arguments)}finally{FA31.owner=old;FA31.root=root;}};
 XART.get=function(k){const im=FA31.base.get.apply(this,arguments);if(im)FA31.keys.set(im,{key:k});return im;};
 xartTint=function(k,c){const im=FA31.base.tint.apply(this,arguments);if(im)FA31.keys.set(im,{key:k,color:c});return im;};
 ctx.drawImage=function(im,...a){const e=FA31.owner;if(e){const tag=FA31.keys.get(im)||{},m=ctx.getTransform(),root=FA31.root,ang=Math.atan2(m.b,m.a)-Math.atan2(root.b,root.a),sz=a.slice(-2),t={key:tag.key||'cached',color:tag.color,angle:ang,rect:a.length===8?a.slice(0,4):null,size:sz,alpha:ctx.globalAlpha};if(Math.max(...sz.map(Math.abs))>Math.max(e.w,e.h)*.45&&FA31.draws.length<1200)FA31.draws.push(t);}return FA31.base.draw.call(this,im,...a);};
 FA31.round=function(b,e){if(!b||b.dead||b._ai27Held||FA31.seen.has(b))return;FA31.seen.add(b);FA31.shots.push({x:b.x,y:b.y,a:Math.atan2(b.vy,b.vx),kind:b.kind,ex:e.x,ey:e.y,at:e.t,proof:enemyOrdnanceCanIntercept(b),w:b.w,h:b.h});};
 eShootT=function(x,y,a,s,k,opt){const e=opt?.owner||ai27Context||FA31.current,r=FA31.base.shoot.apply(this,arguments);if(e===E)FA31.round(r,e);return r;};
 wm26Emit=function(e,x,y,a){if(e===E)FA31.muzzles.push({x,y,a,at:e.t});return FA31.base.wm.apply(this,arguments);};
 navalFlash=function(e,p){if((e||ai27Context)===E)FA31.muzzles.push({x:p.x,y:p.y,at:E.t});return FA31.base.naval.apply(this,arguments);};
 Snd.play=function(k){if(FA31.current)FA31.cues.push(k);return FA31.base.play.apply(this,arguments);};
 ai27Begin=function(e,dt){const old=FA31.base.begin.apply(this,arguments);FA31.current=e;if(e===E)e._fa31First=eBullets.length;return old;};
 ai27End=function(e,old){if(e===E)for(let i=e._fa31First||0;i<eBullets.length;i++)FA31.round(eBullets[i],e);const r=FA31.base.end.apply(this,arguments);FA31.current=null;return r;};
 FA31.render=function(){drawWorld(0);return cv.toDataURL().split(',')[1];};
 FA31.reset=function(){FA31.draws=[];FA31.shots=[];FA31.muzzles=[];FA31.cues=[];FA31.seen=new WeakSet();FA31.allowSpawn=false;thaw=null;story=null;fb2Talk=null;bossWarned=false;CP12.next=VP12.next=99999;CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;if(typeof R46!=='undefined'){R46.glyphMisses.clear();R46.glyphDraws=R46.staticDraws=0;}};
 FA31.step=function(n){for(let i=0;i<n;i++){if(!E||E.dead||E._dyingT!=null)break;FA31.current=E;updatePlay(1/60);FA31.current=null;if(i%12===0)FA31.render();}return{dead:!E||E.dead,hp:E?.hp,x:E?.x,y:E?.y,phase:E?._phase||E?._ep13?.phase||E?._cp22Sewer?.phase||E?.phase,heading:E?.spin||0,pattern:E?.pattern,draw:E?._bf22Rendered||E?._af21Rendered||null,keys:FA31.draws.slice(-20)};};
}'''
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  for stage in args.stages:
   p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate(LAB)
   p.evaluate('(s)=>EA11.setup(s,"furious")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000);specs=p.evaluate('EA11.collect()');(D/f'stage{stage}-specs.json').write_text(json.dumps(specs,indent=2));print('STAGE',stage,len(specs),'variants',flush=True)
   for i,spec in enumerate(specs):
    row={'stage':stage,'index':i,'spec':spec};case=f's{stage}-{i:02}-{spec["type"]}'
    try:
     if not p.evaluate('s=>{FA31.allowSpawn=true;return EA11.case(s)}',spec):row['error']='not spawned';rows.append(row);continue
     p.evaluate('FA31.reset()');samples=[]
     for batch in range(21):
      met=p.evaluate('FA31.step(40)');samples.append(met);p.wait_for_timeout(3)
      if batch in [3,9,16]and not met['dead']:
       data=p.evaluate('FA31.render()');(D/'frames'/f'{case}-{batch}.png').write_bytes(base64.b64decode(data))
      if met['dead']:break
     row.update(samples=samples,stats=p.evaluate('()=>({shots:FA31.shots,muzzles:FA31.muzzles,cues:FA31.cues,draws:FA31.draws,flags:Object.keys(E).filter(k=>k.startsWith("_")&&typeof E[k]==="object"),hp:E.hp,dead:E.dead,body:[E.w,E.h,E._drawW,E._drawH],air:!!AM13_ART[E.type]||AIR13.aliases.has(E.type),bf:bf22Model(E)?.id})'))
    except Exception as err:row['error']=str(err)
    rows.append(row);(D/'audit.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2));print(case,'shots',len(row.get('stats',{}).get('shots',[])),'muzzles',len(row.get('stats',{}).get('muzzles',[])),row.get('error',''),flush=True)
   if args.after:
    result=p.evaluate('()=>({glyphMisses:[...R46.glyphMisses],glyphDraws:R46.glyphDraws,staticDraws:R46.staticDraws})')
   else:result={}
   (D/f'stage{stage}-audit.json').write_text(json.dumps({'rows':[q for q in rows if q['stage']==stage],'errors':errors,**result},indent=2))
   p.close()
  br.close()
finally:stop();(D/'audit.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2))
