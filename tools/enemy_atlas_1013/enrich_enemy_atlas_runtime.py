from pathlib import Path
import json,sys,re
from playwright.sync_api import sync_playwright
from atlas_paths_1013 import ROOT as R,OUT as O
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
D=json.loads((O/'enemy_atlas_runtime_1013.json').read_text(encoding='utf-8'))
files=D['activeFiles']; texts={f:(R/f).read_text(encoding='utf-8',errors='replace') for f in files if (R/f).exists()}
names=['EP13','SC13_CFG','MM1003_SLOTS','RZB_ATTACKS','RZB_FURY_ATTACKS','DEBUG_BOSS_NAMES','F1003B_FORMS','RA4_ROLES','RA4_NAMES','FF8','HK5','SG10','HF7_BOOK','ER26_STAGE','BM_ART_EXTRA']
# Current authored atlas metadata and compact attack tables.
for t in texts.values():names += re.findall(r'^const\s+([A-Z][A-Z0-9_]*(?:ATTACKS|BOOK|ROLES|NAMES|ART|PATTERNS))\s*=',t,re.M)
kinds={}
g=texts['assets/game.js']
for role,a,b in [('boss',g.index('function spawnBoss('),g.index('function spawnSubBoss()')),('mini',g.index('function spawnSubBoss__inner('),g.index('function updateSubBoss('))]:
 for k in re.findall(r"(?:case\s+|kind\s*===?\s*)['\"]([^'\"]+)['\"]",g[a:b]):kinds[k]=role
for k in D['runtime']['registries']['MEGABOSS']:kinds[k]='boss'
port,stop=shoot.serve(str(R));result={}
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page()
  p.goto(f'http://localhost:{port}/index.html?bossmode=1');p.wait_for_function('window.BOFDEBUG && window.__bofFrames>3',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  result['registries']=p.evaluate('''names=>{const o={};for(const n of new Set(names))try{const v=eval(n);if(v!=null&&typeof v!=='function')o[n]=JSON.parse(JSON.stringify(v,(k,v)=>typeof v==='function'?undefined:v))}catch{}return o}''',names)
  result['bossAssets']=p.evaluate('''kinds=>Object.fromEntries(kinds.map(k=>[k,{name:debugBossName(k),keys:bossmodeArtKeys(k)}]))''',list(kinds))
  result['bossDefinitions']=kinds
  result['encounters']=[]
  requests=D['runtime']['fights']+[dict(req,code=code) for code,req in D['runtime']['registries']['ON5_CODES'].items() if not re.fullmatch(r'(?:BOSS|MINI)\d',code)]
  for req in requests:
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':req['stage'],'pilot':'cole','invuln':True})
   result['encounters'].append(p.evaluate('''req=>{let b=on5LaunchEncounter({...req,role:req.role==='alt'?'mini':req.role});let books={};try{if(er26Owns(b)){er26Init(b);books.er26={};for(const n of [0,1,2]){b._er26.level=n;books.er26[n]=er26Book(b)}}}catch{};try{if(b._late27)books.late27=late27Book(b._late27)}catch{};
   const simple=(v,n=0)=>{if(v==null||typeof v==='string'||typeof v==='number'||typeof v==='boolean')return v;if(n>2)return Array.isArray(v)?{arrayLength:v.length}:undefined;if(Array.isArray(v))return v.slice(0,30).map(x=>simple(x,n+1));if(typeof v==='object'){let out={};for(const[k,w]of Object.entries(v))if(!['owner','b','ref','target','from','to','img','image'].includes(k))out[k]=simple(w,n+1);return out;}};return{request:req,name:b.name,books,state:simple(b)}}''',req))
  result['xartSources']=p.evaluate('()=>XART._src');browser.close()
finally:stop()
(O/'enemy_atlas_enrichment_1013.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8');print('Enrichment saved',len(result.get('encounters',[])))
