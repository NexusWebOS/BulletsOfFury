from pathlib import Path
import json,sys,re
from playwright.sync_api import sync_playwright
from atlas_paths_1013 import ROOT as R,OUT as O
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
files=['assets/game.js']+[x.split('?')[0] for x in re.findall(r'<script[^>]+src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8')) if x.split('?')[0].endswith('.js') and x.split('?')[0]!='assets/game.js']
files=list(dict.fromkeys(files));texts={f:(R/f).read_text(encoding='utf-8',errors='replace') for f in files if (R/f).exists()}
game=texts['assets/game.js'];start=game.index('function spawnEnemy(');i=game.index('{',start);level=0;j=i;quote=None
while j<len(game):
 ch=game[j];pair=game[j:j+2]
 if quote:
  if ch=='\\':j+=2;continue
  if ch==quote:quote=None
 elif pair=='//':j=game.find('\n',j);continue
 elif pair=='/*':j=game.find('*/',j+2)+2;continue
 elif ch in "'\"`":quote=ch
 elif ch=='{':level+=1
 elif ch=='}':
  level-=1
  if level==0:break
 j+=1
spawn=game[start:j+1]
candidates=set(re.findall(r"case\s+['\"]([^'\"]+)['\"]\s*:",spawn))
refs={}
for f,t in texts.items():
 for m in re.finditer(r"\bspawnEnemy\s*\(\s*['\"]([^'\"]+)['\"]",t):
  candidates.add(m[1]);refs.setdefault(m[1],[]).append({'file':f,'line':t.count('\n',0,m.start())+1,'kind':'literal-spawn'})
 for declaration in re.finditer(r'\bspawnEnemy\s*=\s*function\s*\(',t):
  for m in re.finditer(r"\btype\s*===?\s*['\"]([^'\"]+)['\"]",t[declaration.end():declaration.end()+2000]):candidates.add(m[1])
names=['STAGES','SUBBOSS','ALTBOSS','SHIPBOSS','MEGABOSS','ON5_CODES','PASSWORDS','AM13_ART','MM1003_DEF','MM1003_SLOTS','MM1003_ART','MM1003_RIGS','EP13','VP12','VP12_ART','REBEL_KEYS','REBEL_SHIPS','FIRETYPES','PROJ','ARSENAL_MINIS','TUR360','BUNKER_DEF','MINI_DEF','ELITE_DEF','ORBITAL','VOLC','SEWER','NEF_S1','NEF_S2','NEF_S3','S1_TANKS','S1_JETS','S1_JET_ELITE','S9_UNITS','SM10_ENEMIES','S81003_ALIENS','DRONE_BEHAV','L6_FLEET','L6X','L6JETS','ELITEX','ELITE8','EX8_PROFILE']
# Include tables declared by active files; only serializable metadata is retained.
for f,t in texts.items():
 names.extend(re.findall(r'^const\s+([A-Z][A-Z0-9_]*(?:DEF|ROSTER|ART|UNITS|FLEET|TYPES|SLOTS|PROFILE|ENEMIES|BANKS|MIMICS))\s*=',t,re.M))
names=list(dict.fromkeys(names))
names += ['F1003B_FORMS','HF7_BOOK','SG10','S81003_ROLES','SC13_CFG','AC10','ARSENAL_DRONES']
port,stop=shoot.serve(str(R));out={'activeFiles':files,'staticCandidates':sorted(candidates),'literalSpawnReferences':refs}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://localhost:{port}/index.html?bossmode=1',timeout=120000);p.wait_for_function('window.BOFDEBUG && window.__bofFrames>3',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  out['runtime']=p.evaluate('''names=>{const clean=v=>JSON.parse(JSON.stringify(v,(k,v)=>typeof v==='function'?undefined:v instanceof Map?Object.fromEntries(v):v instanceof Set?[...v]:v));const regs={};for(const n of names)try{const v=eval(n);if(v!=null&&typeof v!=='function')regs[n]=clean(v)}catch{};return {registries:regs,tables:clean(BOFDEBUG.tables()),roster:clean(BOFDEBUG.roster()),fights:debugFightList(),passwordPages:pc5Pages(),fireKinds:BOFDEBUG.fireKinds(),xartSources:clean(XART._src),xartKeys:Object.keys(XART._src),bossNames:Object.fromEntries([...new Set([...Object.keys(SHIPBOSS),...Object.keys(MEGABOSS),...debugFightList().map(f=>f.kind)])].map(k=>[k,debugBossName(k)]))}}''',names)
  out['plans']=[]
  for stage in range(1,10):
   print('stage',stage,flush=True)
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   for difficulty in ['easy','normal','hard','furious','insanity']:
    result=p.evaluate('''({stage,difficulty})=>{diffKey=difficulty;DIFF=DIFFS[difficulty]||DIFFS.furious;beginStage(stage);const plan=stagePlan;let calls=[],faults=[],wave=-1;const base=spawnEnemy;spawnEnemy=function(type,x,y,opt){calls.push({type,x,y,opt:opt||{},wave});return {type,x,y,hp:100,w:40,h:40,dead:false}};try{for(let i=0;i<plan.length;i++){wave=i;try{plan[i].fn()}catch(e){faults.push({wave:i,error:String(e)})}}}finally{spawnEnemy=base};return{stage,difficulty,waves:plan.map((w,i)=>({index:i,time:w.t,code:String(w.fn)})),calls,faults}}''',{'stage':stage,'difficulty':difficulty})
    out['plans'].append(result)
  alltypes=set(candidates)
  alltypes.update(x['type'] for x in out['runtime']['roster'])
  alltypes.update('mm1003_'+k for k in out['runtime']['registries'].get('MM1003_DEF',{}))
  alltypes.update(out['runtime']['tables'].get('DRONE_BEHAV',{}))
  alltypes.update(out['runtime']['registries'].get('S81003_ROLES',{}))
  alltypes.update(x['type'] for p0 in out['plans'] for x in p0['calls'])
  out['spawnAudit']=[]
  for stage in range(1,10):
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   result=p.evaluate('''types=>{const out=[];for(const type of types){enemies=[];try{const q=BOFDEBUG.spawn(type,240,125,{atlasProbe:true});const e=q?.err?null:q;out.push(e?{type,actual:e.type,name:e.name||null,ground:!!e.ground,pattern:e.pattern,fk:e.fk,atk:e._atk,art:e._art||null,w:e.w,h:e.h,hp:e.hp,volley:BOFDEBUG.volleyFor(e.type),flags:Object.keys(e).filter(k=>k.startsWith('_')&&e[k]!=null&&e[k]!==false),fields:Object.fromEntries(Object.entries(e).filter(([k,v])=>(typeof v==='string'||typeof v==='number'||typeof v==='boolean')&&!['x','y','t','phase','flash'].includes(k)))}:{type,error:q?.err||'no actor'})}catch(error){out.push({type,error:String(error)})}}enemies=[];return out}''',sorted(alltypes))
   out['spawnAudit'].append({'stage':stage,'rows':result})
  out['errors']=errors
  # Native encounter configurations and attack books, including password routes.
  requests=[]
  for f in out['runtime']['fights']:requests.append(dict(f))
  for code,entry in out['runtime']['registries']['ON5_CODES'].items():requests.append(dict(entry,code=code))
  out['encounterAudit']=[]
  for req in requests:
   for difficulty in ['easy','normal','hard','furious']:
    p.evaluate(shoot.SETUP,{'state':'PLAY','stage':req['stage'],'pilot':'cole','invuln':True})
    q=p.evaluate('''({req,difficulty})=>{diffKey=difficulty;DIFF=DIFFS[difficulty];try{let b=on5LaunchEncounter({...req,role:req.role==='alt'?'mini':req.role});const fields=Object.fromEntries(Object.entries(b).filter(([k,v])=>typeof v==='string'||typeof v==='number'||typeof v==='boolean'));let books={};for(const fn of ['er26Book','s7mBook','f1003bDef'])try{if((fn==='er26Book'&&b._er26)||(fn==='s7mBook'&&b._s7mod)||(fn==='f1003bDef'&&b._r30?.finale1003b))books[fn]=eval(fn)(b)}catch{};return{request:req,difficulty,name:b.name,fields,flags:Object.keys(b).filter(k=>k.startsWith('_')&&b[k]!=null),books,parts:typeof debugBossComponents==='function'?debugBossComponents(b):[]}}catch(e){return{request:req,difficulty,error:String(e)}}}''',{'req':req,'difficulty':difficulty})
    out['encounterAudit'].append(q)
  p.goto(f'http://localhost:{port}/expansion/topdown/index.html',timeout=120000);p.wait_for_function('window.TD && TD.MISSIONS',timeout=60000)
  out['overdrive']=p.evaluate('''()=>{const clean=v=>JSON.parse(JSON.stringify(v,(k,v)=>typeof v==='function'?undefined:v));return{keys:Object.keys(TD),missions:clean(TD.MISSIONS),makeFunctions:Object.keys(TD).filter(k=>k.startsWith('make')),registries:Object.fromEntries(Object.entries(TD).filter(([k,v])=>v&&typeof v==='object'&&/ART|DATA|UNITS|TYPE|BANK|MISSION|^ET$|^PROP$|FOOT_EXTRA|MUSEUM/.test(k)).map(([k,v])=>[k,clean(v)])),art:Object.fromEntries(Object.entries(window).filter(([k,v])=>/^TD_.*ART$/.test(k)&&v&&typeof v==='object').map(([k,v])=>[k,clean(v)]))}}''')
  b.close()
finally:
 stop();(O/'enemy_atlas_runtime_1013.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('saved',O/'enemy_atlas_runtime_1013.json',flush=True)
