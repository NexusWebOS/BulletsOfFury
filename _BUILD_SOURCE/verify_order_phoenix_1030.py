from pathlib import Path
import sys,json,http.server,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/order_phoenix_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256
# Only the fixture definition is shared, never execute the first probe again.
src=(Path(__file__).parent/'probe_order_phoenix_1030.py').read_text() if Path(__file__).parent.name=='_BUILD_SOURCE' else (W/'probe.py').read_text();SETUP=src.split('SETUP="""',1)[1].split('"""',1)[0]
checks=[];errors=[];runs=[]
def ck(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  seeds=p.evaluate('()=>{const out={};for(let seed=1;seed<10000;seed++){const s={seed,lastCorner:-1};ph83Bag(s);const side=ph83Rand(s)<.5?"north":"south",n=8+Math.floor(ph83Rand(s)*5);if(!out[n])out[n]={seed,side};if(out[8]&&out[12])break;}return out;}');print('SEEDS',seeds,flush=True)
  for rank in ['normal','hard','furious']:
   for count,side in [(8,-1),(12,1)]:
    p.evaluate(SETUP,{'rank':rank,'seed':seeds[str(count)]['seed']});p.evaluate('DBGT.god=false');maxlive=0;seen=set();moves=[]
    for i in range(230):
     p.evaluate('''side=>{const cast=['charge','barrage','cooldown','exitTwist','exit','return'].includes(P.phase),goal=cast?(side<0?camLeftX()+30:camRightX()-30):(camLeftX()+camRightX())/2;Input.keys.a=player.x>goal+2;Input.keys.d=player.x<goal-2;}''',side)
     p.evaluate(STEP,15);s=p.evaluate('({phase:P.phase,live:P.echoes.length,dead:player.dead,x:player.x,y:player.y,count:P.count,sent:P.sent})');maxlive=max(maxlive,s['live']);seen.add(s['phase']);moves.append(s)
     if p.evaluate('PH83.events.some(e=>e.event==="order-complete")'):break
    ev=p.evaluate('PH83.events');ok=not p.evaluate('player.dead')and any(e['event']=='order-complete'for e in ev)
    ck(f'{rank} {count}-echo cast and four rushes survive by ordinary movement on '+('left'if side<0 else'right')+' without GOD',ok)
    ck(f'{rank} count{count} uses requested native RNG outcome and bounded echo overlap',len([e for e in ev if e['event']=='phoenix-launch'])==count and maxlive<=4)
    runs.append({'rank':rank,'count':count,'seed':seeds[str(count)],'states':moves,'events':ev})
  p.evaluate(SETUP,{'seed':11});p.evaluate(STEP,810)
  ck('Background charge rejects direct core damage and body/part Retina targeting',p.evaluate('()=>{const hp=B.hp;B._lastPart=ph21Part(B,"core");modularHit(99);return B._noHit&&hp===B.hp&&retinaBossTargets(B).filter(t=>!t.dead&&t.hp>0).length===0;}'))
  for side,x in [('left',30),('right',650)]:
   p.evaluate('x=>{player.x=x;}',x);p.evaluate(STEP,30)
   ck('Whole background caster and fire wind remain visible at the '+side+' camera extreme',p.evaluate('()=>{const rows=PH83_ART.banks.wind_rear_4;return Math.abs(P.chargeAt.x-worldWidth()/2)<.01&&rows.every(a=>B.x+a.offset[0]>=camLeftX()&&B.x+a.offset[0]+a.w<=camRightX());}'))
   p.screenshot(path=str(W/('caster-camera-'+side+'.png')))
  p.evaluate(STEP,255)
  while not p.evaluate('P.echoes.length>0'):p.evaluate(STEP,1)
  frozen='({t:P.t,age:P.age,wing:P.wing,wind:P.wind,echo:P.echoes.map(q=>[q.t,q.x,q.y]),x:B.x,y:B.y,arena:PH82.arena.frame})';before=p.evaluate(frozen);p.evaluate("setState('paused')");p.evaluate(STEP,90);ck('Pause freezes fire wing clocks, echo depth, body motion and lava frames',before==p.evaluate(frozen));p.evaluate('setState(GS.PLAY)')
  ck('Echo landing targets stay committed when the player changes sides',p.evaluate('()=>{const q=P.echoes[0],x=q?.targetX;player.x=camLeftX()+30;ph83EchoTick(B,P,.01);return !!q&&q.targetX===x;}'))
  p.screenshot(path=str(W/'charge-and-fire-verified.png'))
  p.evaluate('''()=>{window.savedEcho=P.echoes[0];const q=savedEcho;q.t=q.life*.65;ph83EchoTick(B,P,0);const a=ph83EchoFrame(q);window.echoTest=null;for(let y=0;y<a.spans.length&&!echoTest;y++){const row=a.spans[y]||[];for(let i=0;i<row.length;i+=2){const xx=q.x+a.offset[0]+(row[i]+row[i+1])/2,yy=q.y+a.offset[1]+y;if(yy>viewTopY()+50&&yy<VH-18&&xx>camLeftX()+18&&xx<camRightX()-18){echoTest={x:xx,y:yy};break;}}}player.x=echoTest.x;player.y=echoTest.y;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;DBGT.god=false;ph83EchoTick(B,P,0);}''')
  ck('Contact with actual foreground solid fire pixels causes native player death',p.evaluate('player.dead'))
  p.evaluate(SETUP,{});p.evaluate(STEP,810);p.evaluate('()=>{const q={id:1,t:0,life:2,origin:{x:B.x,y:B.y},targetX:340,markY:432,phase:0,x:B.x,y:B.y,warning:-1};P.echoes=[q];player.x=B.x;player.y=B.y;DBGT.god=false;player.dead=player.out=false;player.invuln=0;ph83EchoTick(B,P,.1);}');ck('Distant perspective copies are harmless before reaching the foreground',not p.evaluate('player.dead'))
  p.evaluate('v18Clear(B)');ck('Cancellation removes every local echo, action and warning owner',p.evaluate('!Q.action&&!B._r30.v18.attack'))
  p.evaluate(SETUP,{});p.evaluate('window.oldHP=B.hp;B._lastPart=ph21Part(B,"wingL");modularHit(11)');p.evaluate(STEP,1);p.screenshot(path=str(W/'hit-verified.png'));ck('Actual foreground part hit damages native HP and draws the authored white flash',p.evaluate('oldHP-B.hp===11&&B.flash>0&&ph21Part(B,"wingL").flash>0'))
  p.evaluate(STEP,15);ck('Native white damage flash expires normally',p.evaluate('B.flash<=0&&ph21Part(B,"wingL").flash<=0'))
  p.evaluate(SETUP,{});p.evaluate('j3State(B).hp[0]=5330;B._r30.v18.donorAge=47');p.evaluate(STEP,2350);live=p.evaluate('({mode:B._r30.mode,form:B._r30.v18.form,hp:j3State(B).hp,events:PH83.events})');print('LIVE RETURN',json.dumps(live),flush=True);ck('A live timed copy finishes its whole new combo before downloading home',p.evaluate('B._r30.v18.form===0&&j3State(B).hp[2]===2624&&PH83.events.some(e=>e.event==="order-complete")'))
  p.evaluate(SETUP,{});p.evaluate('()=>{B._lastPart=ph21Part(B,"core");modularHit(B.hp);}');p.evaluate(STEP,190);ck('Last copied-life death preserves the zero-HP native final anatomy',p.evaluate('B._r30.mode==="v19FinalReform"&&B.parts.map(p=>p.id).join()==="core,left,right"&&B.parts.every(p=>p.hp===0)'))
  p.evaluate(STEP,240);ck('Final destruction still starts with surviving old wings safely retired',p.evaluate('B._r30.mode==="dr5Death"&&B.hp===0'))
  p.evaluate('()=>{spawnBoss("vileexistence");B=boss;v18Enter(B,2,2);B._r30.mode="fight";B.enter=B._noHit=false;}');p.evaluate(STEP,3);ck('Phoenix cannon stage remains with the original PH82 turbo/core controller',p.evaluate('ph82Full(B)&&!ph83Own(B)'))
  p.evaluate('()=>{v18Enter(B,2,6);B._r30.mode="fight";B.enter=B._noHit=false;B._r30.v18.arenaPhase=6;nb23Start(B,"codeGeysers");}');p.evaluate(STEP,3);ck('Brain night storm remains with its existing owner',p.evaluate('!!nb81Act(B)&&NB81.scene?.theme==="night-clouds"'))
  p.evaluate('()=>{v18Enter(B,2,1);B._r30.mode="fight";B.enter=B._noHit=false;B._r30.v18.arenaPhase=1;}');p.evaluate(STEP,3);ck('Digital-jungle helicopter remains with its existing owner',p.evaluate('hc79Own(B)&&HC79.draws.ground>0'))
  ck('No native runtime, drawing or asset errors throughout all six movement runs',not errors);br.close()
finally:stop()
s=(R/'assets/order_phoenix_art_1030.js').read_text();A=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
frames=[a for rows in A['banks'].values()for a in rows]
ck('All702 frames retain even cells, source offsets and stable512px pivots',len(frames)==702 and all(a['w']%2==a['h']%2==0 and a['logical']==[512,512]for a in frames))
ck('All packed frames fit inside their actual texture page without clipping',all(a['rect'][0]>=0 and a['rect'][1]>=0 and a['rect'][0]+a['w']<=A['pages'][a['key']]['w']and a['rect'][1]+a['h']<=A['pages'][a['key']]['h']for a in frames))
ck('Every emitted page is present at the recorded dimensions',all(Image.open(R/a['path']).size==(a['w'],a['h'])for a in A['pages'].values()))
s=(R/'assets/phoenix_turbo_core_art_1030.js').read_text();old=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
ck('All467 upstream cannon/core frames also fit complete texture pages',all(a['rect'][0]+a['w']<=old['pages'][a['key']]['w']and a['rect'][1]+a['h']<=old['pages'][a['key']]['h']for rows in old['banks'].values()for a in rows))
ck('Core game engine remains byte-identical',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
(W/'quality.json').write_text(json.dumps({'checks':checks,'runs':runs,'errors':errors},indent=2));assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
