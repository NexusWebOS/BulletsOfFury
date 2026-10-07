"""Native opaque combat-rig transitions; controlled fixtures, not campaign clears."""
from pathlib import Path
import sys,json,base64,ast
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/finale_transform_1007';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];screens=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.add_init_script('navigator.getGamepads=()=>[]')
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  for symbol,names in [('EC7',['engine_combat_1007.js']),('HC7',['hardcorps_finale_art_1007.js','hardcorps_finale_1007.js']),('FP7',['finale_patterns_1007.js']),('FT7',['finale_transform_1007.js'])]:
   if p.evaluate(f'()=>typeof {symbol}==="undefined"'):
    for name in names:
     if (R/'assets'/name).exists():p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/{name}')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'normal'})
  p.evaluate('()=>{j3Encounter(B,2);on5FightStart(B);dr5State(B).introWanted=false;dr5State(B).introSeen=true;story=null;fb2Talk=null;BOFCinematicDirector.cancel();r30Warm();aa5Warm();hc7Warm();for(const P of PILOTS)XART.rdy("ship_"+P.key+"_pv2");}')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(REALM30_ART).every(a=>XART.rdy("r30_"+Object.keys(REALM30_ART).find(k=>REALM30_ART[k]===a)))&&Object.values(HC7_ART).flat().every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate('''()=>{window.ftAudit=function(){const out=[],cell=fmcCell,blit=r30Blit;fmcCell=function(k,part,x,y,w,h,r,a,...rest){out.push({key:k,part,alpha:(a??1)*ctx.globalAlpha});return cell.apply(this,arguments);};r30Blit=function(k,x,y,w,h,r,a){out.push({key:k,alpha:(a??1)*ctx.globalAlpha});return blit.apply(this,arguments);};try{r30DrawBoss(B);}finally{fmcCell=cell;r30Blit=blit;}return out;};window.ftStep=function(n){for(let i=0;i<n;i++)r30Tick(B,1/60);};}''')
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));screens.append(name)
  for i in range(9):
   q=p.evaluate('''i=>{const J=j3State(B),S=B._r30;j3Mimic(B,i);on5FightStart(B);S.attack=null;S.shield=0;S.on5Shield=null;B._lastPart=B.parts.find(p=>p.id==='core');modularHit(37+i);const arm=B.parts.find(p=>p.id!=='core'&&!p.destroyed);if(arm){B._lastPart=arm;modularHit(arm.hp+1);}j3Save(B);window.ftSaved={hp:J.hp.slice(),parts:B.parts,broken:arm?.id,hpSelf:B.hp};j3Morph(B,'home');const clock=S.clock,aa=J.aa5Clock;r30Tick(B,1/60);return{locked:B.enter&&!r30Live(B),single:Math.abs(S.clock-clock-1/60)<1e-8&&Math.abs(J.aa5Clock-aa-1/60)<1e-8,copy:i};}''',i)
   ck(q['locked'],'form '+str(i)+' disassembly is protected');ck(q['single'],'form '+str(i)+' transition advances both clocks exactly once')
   p.evaluate('()=>ftStep(29)');q=p.evaluate('()=>{const d=ftAudit();return{n:d.length,opaque:d.every(v=>v.alpha===1),broken:!FT7.last.pieces.some(v=>v.id===ftSaved.broken),moved:FT7.last.pieces.some((v,k)=>Math.abs(v.rot-(j3State(B).ft7.out[k]?.rot||0))>.2)};}')
   ck(q['n']>0 and q['opaque'] and q['broken'] and q['moved'],'form '+str(i)+' actual draw stays opaque, twists pieces and omits destroyed module');snap('form-'+str(i)+'-out')
   p.evaluate('()=>{for(let i=0;i<170&&B._r30.mode!=="fight";i++)r30Tick(B,1/60);}')
   q=p.evaluate('''i=>{const J=j3State(B);return{home:J.mimic===null,saved:J.hp.every((n,k)=>n===ftSaved.hp[k]),parts:J.modules[i]===ftSaved.parts};}''',i)
   ck(q['home'] and q['saved'] and q['parts'],'form '+str(i)+' returns home without healing any life or replacing saved modules')
   p.evaluate('''i=>{const J=j3State(B);J.cursor=(i+8)%9;j3Morph(B,i);for(let k=0;k<85&&B._r30.mode==='transform1003j';k++)r30Tick(B,1/60);ftStep(28);}''',i)
   q=p.evaluate('''i=>{const J=j3State(B),d=ftAudit();return{mimic:J.mimic===i,hp:B.hp===ftSaved.hpSelf,parts:B.parts.every(v=>v===ftSaved.parts.find(p=>p.id===v.id)),opaque:d.length>0&&d.every(v=>v.alpha===1),broken:!FT7.last.pieces.some(v=>v.id===ftSaved.broken)};}''',i)
   ck(all(q.values()),'form '+str(i)+' physical reassembly restores the same injured form and opaque native cells');snap('form-'+str(i)+'-in')
   p.evaluate('()=>{for(let i=0;i<90&&B._r30.mode!=="fight";i++)r30Tick(B,1/60);}')
   ck(p.evaluate('()=>B._r30.mode==="fight"&&!B.enter&&!B._r30.rewarded'),'form '+str(i)+' finishes in combat without phase reward');snap('form-'+str(i)+'-ready')
  q=p.evaluate('''()=>{const S=B._r30,J=j3State(B);j3Morph(B,'home');const before=JSON.stringify(J.hp),clock=S.clock;for(let i=0;i<12;i++)r30DrawBoss(B);const frozen=clock===S.clock&&before===JSON.stringify(J.hp);S.mode='fight';S.t=0;B.enter=false;const old=FT7.draws;r30DrawBoss(B);return{frozen,interrupt:FT7.draws===old};}''')
  ck(q['frozen'],'repeated render calls never advance clocks or heal pools');ck(q['interrupt'],'leaving a transition immediately restores combat renderer')
  # The same image keys and dimensions used by the fight must speak the monologue.
  q=p.evaluate('''()=>{j3Home(B);const S=B._r30,J=j3State(B),D=dr5State(B);S.mode='fight';S.attack=null;B.flash=0;for(const p of B.parts)p.flash=0;const wanted=ft7Nodes(B);S.mode='dr5Monologue';S.t=0;D.introWanted=true;D.introSeen=false;D.radio=null;D.line=0;DR5.events=[];r30Tick(B,1/60);const mode=S.mode,hp=JSON.stringify(J.hp),clock=S.clock,old=DR5.draws.parts||0;const got=ftAudit();return{keys:got.map(v=>v.key).sort().join('|')===wanted.map(v=>v.key).sort().join('|'),opaque:got.every(v=>v.alpha===1),noOld:(DR5.draws.parts||0)===old,restored:S.mode===mode&&S.clock===clock&&hp===JSON.stringify(J.hp),keysList:got.map(v=>v.key)};}''')
  for k in ['keys','opaque','noOld','restored']:ck(q[k],'monologue '+k+' combat-body proof')
  p.evaluate('()=>{dr5State(B).radio.t=.85;}');snap('combat-body-monologue')
  q=p.evaluate('''()=>{const S=B._r30,D=dr5State(B),text=D.radio.text,duration=dr5TalkDuration(text);D.radio.t=duration-.06;r30Tick(B,.05);const held=D.line===0;r30Tick(B,.02);const advanced=D.line===1;let ticks=0;while(S.mode==='dr5Monologue'&&ticks++<1600)r30Tick(B,.05);const lines=DR5.events.filter(q=>q.event==='dracodiaDialogue'&&q.who==='DRACODIA').map(q=>q.text);return{held,advanced,finished:S.mode==='fight'&&D.introSeen,verbatim:JSON.stringify(lines)===JSON.stringify(DR5.intro.map(q=>q[0])),shriek:DR5.events.filter(q=>q.event==='dracodiaShriek').length===2};}''')
  for k,v in q.items():ck(v,'unchanged speech '+k)
  q=p.evaluate('''()=>{const J=j3State(B),S=B._r30;J.hp=J.hp.map(()=>0);B.hp=0;j3FinalDeath(B);const old=FT7.draws;for(let i=0;i<30;i++)r30Tick(B,.05);r30DrawBoss(B);return{protected:dr5Locked()&&B.enter,delegates:S.mode==='dr5Death'&&FT7.draws===old,reward:!S.rewarded};}''')
  for k,v in q.items():ck(v,'death interrupt '+k)
  # A full native temporal sample makes corkscrew paths and seating readable.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'normal'})
  p.evaluate('()=>{j3Encounter(B,2);dr5State(B).introWanted=false;dr5State(B).introSeen=true;j3Mimic(B,7);on5FightStart(B);j3Morph(B,8);}')
  motion=[]
  for f in range(50):
   data=p.evaluate('()=>{ftStep(3);shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return cv.toDataURL().split(",")[1];}')
   from io import BytesIO
   motion.append(Image.open(BytesIO(base64.b64decode(data))).convert('RGB').resize((480,512)).quantize(colors=160))
  motion[0].save(O/'warden-to-hammer.gif',save_all=True,append_images=motion[1:],duration=50,loop=0,optimize=False)
  p.wait_for_timeout(300);ck(not errors,'zero page/console/404 errors');br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'screens':screens,'scope':'Controlled native transitions and cinematic behavior; no campaign-clear/balance claim.'},indent=2),encoding='utf-8')
contact=Image.new('RGB',(750,9*282),'#0c1118');d=ImageDraw.Draw(contact)
for i in range(9):
 for j,state in enumerate(['out','in','ready']):
  im=Image.open(O/f'form-{i}-{state}.png').convert('RGB').resize((250,264));contact.paste(im,(j*250,i*282+18));d.text((j*250+8,i*282+3),f'{i} {state}',fill='white')
contact.save(O/'all-nine-forms.jpg',quality=90)
(O/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Opaque final boss transformations</title><style>body{background:#08111a;color:#e4f2ff;font:16px system-ui;margin:24px}img{max-width:100%}section{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}figure{margin:0}h2{margin-top:30px}</style><h1>Combat bodies: all nine forms</h1><p>Controlled native captures. Each form has a damaged pool and destroyed module retained across return.</p><img src="warden-to-hammer.gif">'+''.join('<h2>Form '+str(i)+'</h2><section>'+''.join('<figure><img src="form-'+str(i)+'-'+s+'.png"><figcaption>'+s+'</figcaption></figure>' for s in ['out','in','ready'])+'</section>' for i in range(9))+'<h2>Actual combat body delivering unchanged speech</h2><img src="combat-body-monologue.png">',encoding='utf-8')
print(json.dumps({'checks':len(checks),'failed':[q['name'] for q in checks if not q['ok']],'errors':errors}))
if errors or any(not c['ok'] for c in checks):raise SystemExit(1)
