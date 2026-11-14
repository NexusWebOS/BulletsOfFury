from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import sys,json,base64,io,subprocess
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-assault';sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];rows=[];frames=[];checks={}
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("()=>{EA11.setup(7,'furious');stagePlan=[];waveIdx=0;enemies=[];powerups=[];CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=false;player.invuln=99999;for(const k in Input.keys)Input.keys[k]=false;spawnSubBoss('dualscoopdredger');window.B=subBoss;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&sj98Ready()}');p.evaluate(STEP,100)
  # Start at the new attack-book chapter; every subsequent transition is native.
  p.evaluate('()=>{sj123Side(B,0);window.proof123={facing:[],hiddenShots:0,buriedFrames:0,apex:[false,false],land:[false,false],warnColors:new Set()};const orig=sj120Shoot;sj120Shoot=function(b,a,angle,speed){if(a.underground)proof123.hiddenShots++;return orig(b,a,angle,speed);};}')
  saved=set();finished=False
  for i in range(440):
   err=p.evaluate(STEP,4);assert err is None,err
   r=p.evaluate('''()=>{const C=B._sj120,G=B._sj98;const row={t:B.t,mode:C.mode,ct:C.t,pass:C.sidePass,speed:C.sideSpeed,hp:B.hp,actors:G.actors.map(a=>({i:a.i,x:a.x,y:a.y,gy:a.gy,h:a.height,heading:a.heading,buried:a.underground,depth:a.buryDepth,visible:a.segments.filter(p=>!p.hidden).length}))};if(C.mode==='side-run')for(const a of G.actors){const s=sj123SidePoint(a,clamp(C.t/C.dur,0,1));proof123.facing.push(Math.abs(ss116Wrap(a.heading-Math.atan2(-s.dx,s.dy))));}if(C.mode==='underground'&&G.actors.every(a=>a.underground))proof123.buriedFrames++;if(C.mode==='arch')for(const a of G.actors){if(a.height>100)proof123.apex[a.i]=true;if(C.t>a.i*.18+1.32&&a.height<20)proof123.land[a.i]=true;}if(C.mode==='side-warn')proof123.warnColors.add(Math.min(2,Math.floor(C.t/C.dur*3)));return row;}''');rows.append(r);im=shot(p);frames.append(im)
   tag=r['mode']+('-'+str(r['pass'])if r['mode'].startswith('side')else'')
   if tag not in saved and r['ct']>(.4 if r['mode']=='arch'else .2):saved.add(tag);im.save(O/(tag+'.png'));print(json.dumps({'mode':r['mode'],'pass':r['pass'],'t':r['t']}),flush=True)
   if r['mode']=='arch-exit'and r['ct']>.35:finished=True;break
  data=p.evaluate('({events:SJ120.events,draws:SA123.draws,warningDraws:SA123.warningDraws,proof:{facing:proof123.facing,hiddenShots:proof123.hiddenShots,buriedFrames:proof123.buriedFrames,apex:proof123.apex,land:proof123.land,colors:[...proof123.warnColors]},target:B._sj120.archTarget})')
  events=data['events'];shots=[e for e in events if e['event']=='large-orb'and e['mode']=='side-run'];releases=[e for e in events if e['event']=='side-release'];proof=data['proof']
  checks['complete_requested_sequence']=finished;checks['four_increasing_speeds']=[e['speed']for e in releases]==[430,560,700,880];checks['both_snakes_fire_forward']=all(any(e['actor']==i for e in shots)for i in[0,1])and all(abs((e['angle']-e['heading'])-1.5707963267948966)<1e-6 for e in shots);checks['head_faces_travel']=bool(proof['facing'])and max(proof['facing'])<.001;checks['all_warning_colors_drawn']=set(proof['colors'])=={0,1,2}and data['warningDraws']>0;checks['both_burrow_fully']=proof['buriedFrames']>3;checks['no_underground_launches']=proof['hiddenShots']==0;checks['both_make_high_arches']=all(proof['apex']);checks['both_arches_finish_landing']=all(proof['land']);checks['health_is_unchanged']=all(r['hp']==14000 for r in rows);checks['new_authored_hole_and_burrow_frames_draw']=data['draws'].get('hole',0)>0 and data['draws'].get('dive-body0',0)>0 and data['draws'].get('riseL-body0',0)>0 and data['draws'].get('riseR-body0',0)>0
  # Pause must freeze underground clocks and pit animations too.
  p.evaluate('()=>{sj123Side(B,0);sj123Approach(B);B._sj120.t=B._sj120.dur;sj120Motion(B,B._sj98.actors[0],0);sj120Motion(B,B._sj98.actors[1],0);sj123Next(B);sj123Under(B);}')
  frozen=p.evaluate('JSON.stringify([B.t,B._sj120.t,B._sj120.holes,B._sj98.actors.map(a=>[a.clock,a.x,a.y,a.height])])');p.evaluate("setState('paused')");p.evaluate(STEP,30);checks['pause_freezes_burrow_and_holes']=frozen==p.evaluate('JSON.stringify([B.t,B._sj120.t,B._sj120.holes,B._sj98.actors.map(a=>[a.clock,a.x,a.y,a.height])])');p.evaluate('setState(GS.PLAY)')
  # Partner defeat must cancel holes and let the surviving native actor continue.
  p.evaluate('()=>{sj123Cancel(B);sj123Side(B,0);sj120Set(B,"row-fire",99);B._sj120.rowSlots=new Map([[0,-77],[1,77]]);for(const a of B._sj98.actors){a.x=340+(a.i?77:-77);a.gy=210;a.height=0;a.y=210;a.heading=0;}const a=B._sj98.actors[0];for(const q of a.pools)for(let i=0;i<8&&q.hp>0;i++)sj98Damage(B,q.hp+100,null,null,{a,p:q});}');checks['independent_solo_half']=p.evaluate('B._sj98.actors[0].dead&&!B._sj98.actors[1].dead&&B.hp===7000&&B._sj120.holes.length===0');p.evaluate('()=>{sj123Side(B,0);}');p.evaluate(STEP,85);checks['solo_enters_new_pattern']=p.evaluate('B._sj120.mode==="side-run"&&B._sj98.actors.filter(a=>!a.dead).length===1')
  br.close()
finally:stop()
checks['no_native_errors']=not errors;report={'checks':checks,'errors':errors,'data':data,'rows':rows,'frames':len(frames)};(O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({'checks':checks,'errors':errors,'frames':len(frames)}),flush=True)
# Keep a GIF at the actual480x512 game view.60/70/70ms preserves15fps timing.
contact=Image.new('RGB',(1920,2048))
for i in range(16):contact.paste(frames[round(i*(len(frames)-1)/15)],(i%4*480,i//4*512))
contact.save(O/'sequence-contact.png');pal=contact.quantize(colors=128,method=Image.Quantize.MEDIANCUT);q=[f.quantize(palette=pal,dither=Image.Dither.NONE)for f in frames];durations=[60 if i%3==0 else 70 for i in range(len(q))];q[0].save(O/'both-snakes-full-sequence.gif',save_all=True,append_images=q[1:],duration=durations,loop=0,optimize=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(O/'both-snakes-full-sequence.gif'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'both-snakes-full-sequence.mp4')],check=True)
assert all(checks.values()),checks
