"""Native scheduler/render coverage. No HP injections in these observation runs."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF, STEP
from PIL import Image,ImageDraw
import json,time,http.server,argparse

R=Path(__file__).resolve().parents[1];O=R/'_shots/bullethell_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];runs=[]
def ck(n,v,data=None):
 checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1'
http.server.ThreadingHTTPServer.request_queue_size=128
parser=argparse.ArgumentParser();parser.add_argument('--fights',default=','.join(f'{n}-mini'for n in range(1,10))+',7-boss,8-boss');args=parser.parse_args()
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  browser_context=br.new_context(viewport={'width':1280,'height':800})
  for token in args.fights.split(','):
   a,role=token.split('-');stage=int(a)
   label=f'{stage}-{role}';p=browser_context.new_page();local=[]
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+json.dumps(m.location))if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
   p.wait_for_function('window.__bofFrames>5&&typeof BH25!=="undefined"',timeout=180000);p.evaluate(TRAP_RAF)
   p.evaluate("""([stage,role])=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(stage,role),{pilot:'cole'});if(role==='mini')spawnSubBoss(debugFightFor(stage,role).kind);else spawnBoss(debugFightFor(stage,role).kind);debugFight.spawned=true;warnT=0;DBGT.god=true;run.lives=3;player.dead=false;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;BH25.events=[];window.bhActor=role==='mini'?subBoss:boss;}""",[stage,role])
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   if stage==6 and role=='mini':p.wait_for_function('()=>{sc13Warm();return SC13.keys.every(k=>XART.rdy(k))}',timeout=180000)
   seen=set();maxlive=0;states=[];proof=True;proofsamples=0;start=time.time()
   for batch in range(650 if stage==6 else 300):
    p.evaluate(STEP,20)
    q=p.evaluate("""()=>{const b=bhActor,P=b._bh25;return{mode:b._er26?.mode||b._s7mod?.mode||b._hd1003?.mode||b._bomber?.mode||b._cargo13?.mode||b._rzb?.attack||b._r30?.mode||b._s9rift?.s5924?.mode,phase:P?.phase,wave:P?.wave,kind:P?.kind,hp:b.hp,enter:b.enter,escorts:enemies.filter(e=>e._sa14Escort?.owner===b&&!e.dead).length,escortTurn:!!b._sa14?.escortTurn,live:eBullets.filter(q=>q._bh25Owner===b&&!q.dead).length,events:BH25.events.filter(e=>e.event==='section-complete').length};}""")
    maxlive=max(maxlive,q['live']);states.append(q)
    if q['live']:
     proofsamples+=1;proof=proof and p.evaluate("eBullets.filter(q=>q._bh25Owner&&!q.dead).every(q=>!enemyOrdnanceCanIntercept(q)&&!q._shootable&&!enemyDefensiveProof(q))")
    key=q.get('phase')+str(q.get('wave')) if q.get('phase') else ''
    if key and key not in seen and(q.get('wave')in[0,2,4,6]or q.get('phase')=='recover'):
     seen.add(key);p.evaluate('drawWorld(0)');file=O/(label+'-'+key+'.png');p.screenshot(path=str(file));shots.append((file,label+' '+key))
    if q['events']>=1:break
    if batch%8==0:p.wait_for_timeout(1)
   ev=p.evaluate('BH25.events');runs.append(dict(stage=stage,role=role,events=ev,states=states,maxlive=maxlive))
   (O/(label+'.json')).write_text(json.dumps(runs[-1],indent=2),encoding='utf8')
   ck(label+' enters its barrage through native decisions',any(e['event']=='section-start'for e in ev),{'mode':q,'wall':round(time.time()-start,1)})
   ck(label+' completes a finite barrage and resumes native combat',any(e['event']=='section-complete'for e in ev),q)
   ck(label+' keeps the bullet budget bounded',0<maxlive<=128,maxlive)
   ck(label+' ordinary rounds allow defensive clears only',proof and proofsamples>0,proofsamples)
   if stage==4 and role=='mini':ck('Olive barrage waits for escort fire and its complete turn to end',all(not x['escorts']and not x['escortTurn']for x in states if x.get('phase')))
   p.close()
  br.close()
finally:
 stop();payload=json.dumps(dict(checks=checks,errors=errors),indent=2)
 (O/'report.json').write_text(payload,encoding='utf8')
 (O/('matrix.json'if len(args.fights.split(','))==11 else'focused-'+args.fights.replace(',','_')+'.json')).write_text(payload,encoding='utf8')
if shots:
 contact=Image.new('RGB',(1280,((len(shots)+3)//4)*222),(5,10,17));g=ImageDraw.Draw(contact)
 for i,(f,label)in enumerate(shots):contact.paste(Image.open(f).convert('RGB').resize((320,200)),((i%4)*320,(i//4)*222));g.text(((i%4)*320+4,(i//4)*222+202),label,fill='white')
 contact.save(O/'contact.jpg')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),errors=errors)),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)and not errors else 1)
