"""Publish the reviewed BOF tree and local review library; preserve other projects.
Source and Pages use separate commits. Large media is stored in a new release.
"""
from pathlib import Path
import argparse,collections,concurrent.futures,hashlib,json,os,re,shutil,subprocess,time,urllib.parse,zipfile
R=Path(__file__).resolve().parents[1];O=R/'_shots/github_upload_1102';O.mkdir(exist_ok=True)
D=Path('D:/BOF-Downloads/2026-10-31/current/github-release-1102')
REPO='NexusWebOS/BulletsOfFury';TAG='bof-complete-update-2026-11-02';BASE='/BulletsOfFury';PUBLIC='https://nexuswebos.github.io'+BASE
RELEASE='https://github.com/'+REPO+'/releases/download/'+TAG
S=R/'docs/previews/review_update_1102'
def command(args,**kwargs):return subprocess.check_output(args,cwd=R,**kwargs).decode('utf-8',errors='replace').strip()
def save(name,value):
 p=O/name;tmp=p.with_suffix(p.suffix+'.partial');tmp.write_text(json.dumps(value,indent=2),encoding='utf-8');os.replace(tmp,p)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def load():return json.loads((O/'plan.json').read_text())
def prepare():
 config=json.loads(Path('D:/BOF-Downloads/2026-10-31/current-overrides.json').read_text(encoding='utf-8'));media=[];static=[];seen={}
 rows=list(config['files'].items())
 for name in command(['git','ls-files','--others','--exclude-standard','--','docs']).splitlines():
  if Path(name).suffix.lower()in ['.mp4','.webm']:rows.append(('/'+name,str(R/name)))
 for route,filename in rows:
  p=Path(filename).resolve();assert p.is_file()and(p.is_relative_to(R)or p.is_relative_to(D.parent)),route
  assert '..'not in Path(route).parts and route.startswith('/'),route
  if p.suffix.lower()in ['.mp4','.webm']:
   digest=sha(p);key=(digest,p.suffix.lower());size=p.stat().st_size;assert size<2_000_000_000,(route,size)
   if key not in seen:
    stem=re.sub('[^A-Za-z0-9._-]+','-',route.strip('/').replace('/','--'))[:-len(p.suffix)][:175];name=stem+'-'+digest[:12]+p.suffix.lower();stage=(D/'media'if p.drive.lower().startswith('d:')else O/'media');stage.mkdir(parents=True,exist_ok=True);target=stage/name
    assert target.resolve().is_relative_to(stage.resolve())
    if not target.exists():os.link(p,target)
    assert target.stat().st_size==size
    seen[key]=dict(name=name,path=str(target),source=str(p),bytes=size,sha256=digest,url=RELEASE+'/'+name,routes=[]);media.append(seen[key])
   seen[key]['routes'].append(route)
  else:static.append(dict(route=route,path=str(p)))
 plan=dict(repository=REPO,tag=TAG,parent=command(['git','rev-parse','HEAD']),media=media,static=static,clips=config.get('clips',{}),additionalClips=config.get('additionalClips',[]),packages=[])
 save('plan.json',plan);print('PREPARED',len(media),'media assets;',round(sum(x['bytes']for x in media)/1e9,2),'GB;',len(static),'static routes',flush=True)
def upload():
 plan=load();assets=plan['media']+plan.get('packages',[])+plan.get('metadata',[]);remote=json.loads(command(['gh','release','view',TAG,'--repo',REPO,'--json','assets']))['assets'];known={a['name']:a for a in remote};done={};bad=[]
 pending=[a for a in assets if a['name']not in known or known[a['name']]['size']!=a['bytes']]
 for a in assets:
  if a not in pending:done[a['name']]=dict(bytes=a['bytes'],state='already-uploaded')
 # Interleave large/small assets so progress remains visible while long uploads run.
 pending.sort(key=lambda a:a['bytes'],reverse=True);ordered=[]
 while pending:
  ordered.append(pending.pop(0))
  if pending:ordered.append(pending.pop())
 def put(a):
  for attempt in range(3):
   q=subprocess.run(['gh','release','upload',TAG,a['path'],'--repo',REPO,'--clobber'],cwd=R,capture_output=True,text=True)
   if q.returncode==0:return a,None
   error=q.stderr.strip()[-700:];time.sleep(2*(attempt+1))
  return a,error
 print('UPLOAD_START',len(ordered),'pending;',len(done),'already present',flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
  futures={pool.submit(put,a):a for a in ordered};last=time.time()
  while futures:
   ready,_=concurrent.futures.wait(futures,timeout=20,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in ready:
    a,error=f.result();del futures[f]
    if error:bad.append(dict(name=a['name'],error=error));print('UPLOAD_ERROR',a['name'],error,flush=True)
    else:done[a['name']]=dict(bytes=a['bytes'],state='uploaded');print('UPLOADED',len(done),'/',len(assets),a['name'],flush=True)
    save('upload-progress.json',dict(done=done,failed=bad,pending=len(futures)))
   if time.time()-last>20:print('UPLOAD_PROGRESS',len(done),'/',len(assets),'complete;',len(futures),'remaining',flush=True);last=time.time()
 if bad:raise RuntimeError(str(len(bad))+' uploads failed; rerun resumes verified sizes')
 print('UPLOAD_COMPLETE',len(done),flush=True)
def packages():
 plan=load();paths=json.loads((O/'runtime-files.json').read_text());groups=collections.defaultdict(list)
 for name in paths:
  m=re.match(r'assets/game/levels/stage_(\d+|x)/',name);key='stages-1-5'if m and m[1].isdigit()and int(m[1])<=5 else'stages-6-9-X'if m else'core';groups[key].append(name)
 target=D/'packages';target.mkdir(parents=True,exist_ok=True);rows=[];prefix='BulletsOfFury-2026-11-02/'
 instructions='''BULLETS OF FURY - NOVEMBER 2 BUILD
Extract all three BOF-runtime ZIPs into the SAME folder. Their shared
BulletsOfFury-2026-11-02 directory contains the full playable game.
Run START-BOF.cmd with Python 3 installed, then open http://127.0.0.1:8000 .
Source, video comparisons, concepts and the field manual:
https://nexuswebos.github.io/BulletsOfFury/
'''
 launcher='@echo off\r\ncd /d "%~dp0"\r\necho Open http://127.0.0.1:8000 in your browser.\r\npy -3 -m http.server 8000\r\npause\r\n'
 for key,names in groups.items():
  name='BOF-runtime-'+key+'-2026-11-02.zip';file=target/name;temporary=file.with_suffix('.zip.partial')
  with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True)as z:
   for item in sorted(names):
    p=(R/item).resolve();assert p.is_file()and p.is_relative_to(R);z.write(p,prefix+item)
   if key=='core':z.writestr(prefix+'README-BUILD.txt',instructions);z.writestr(prefix+'START-BOF.cmd',launcher)
  with zipfile.ZipFile(temporary)as z:assert z.testzip()is None
  assert temporary.stat().st_size<2_000_000_000;os.replace(temporary,file);rows.append(dict(name=name,path=str(file),bytes=file.stat().st_size,sha256=sha(file),url=RELEASE+'/'+name,files=len(names)));print('PACKAGE',key,len(names),round(file.stat().st_size/1e6),'MB',flush=True)
 plan['packages']=rows;save('plan.json',plan)
def export():
 plan=load();S.mkdir(parents=True,exist_ok=True);mapping={u:a['url']for a in plan['media']for u in a['routes']}
 def rewrite(text):
  text=text.replace('http://127.0.0.1:8805','').replace('/_releases/','https://github.com/'+REPO+'/releases/download/')
  text=text.replace('href="/"','href="'+BASE+'/"')
  for src in sorted(mapping,key=len,reverse=True):text=re.sub(r'(?<![A-Za-z0-9/_])'+re.escape(src),lambda m:mapping[src],text)
  text=re.sub(r'(?<![A-Za-z0-9/_])/(current|enemy-showcase-1031|game|field-manual)(?=[/.])',lambda m:BASE+'/'+m[1],text)
  return text
 for item in plan['static']:
  target=S/item['route'].lstrip('/');target.parent.mkdir(parents=True,exist_ok=True);p=Path(item['path'])
  if p.suffix.lower()in ['.html','.json','.js','.css']:
   text=p.read_text(encoding='utf-8');text=rewrite(text)
   if item['route'].endswith('/boss-comparison-1102/manifest.json'):
    v=json.loads(text)
    for row in v['jobs']:
     for key in ['path','folder']:row.pop(key,None)
    text=json.dumps(v,indent=2)
   target.write_text(text,encoding='utf-8')
  else:shutil.copyfile(p,target)
 for src,name in [('docs/previews/cast_cinematics_1102/standalone.html','cast-cinematics-1102.html'),('docs/previews/storyboard_1102/index.html','storyboard-1102.html')]:
  text=(R/src).read_text(encoding='utf-8');text=re.sub(r'\.\./\.\./\.\./(assets/[^"\x27<>]+|_ART_SOURCES/[^"\x27<>]+)',lambda m:'https://github.com/'+REPO+'/blob/main/'+m[1],text);(S/name).write_text(rewrite(text),encoding='utf-8')
 old=command(['git','show','origin/gh-pages:index.html']);hero='''<section style="border:2px solid #4fcbcf;padding:24px;margin:18px 0 32px;background:#0c2532"><p class="tag">NOVEMBER 2 · CURRENT BUILD AND VIDEOS</p><h1>Latest Bullets of Fury review</h1><p>57 complete boss fights on Normal, Hard and Furious; all regular waves, the Stage1–9 enemy refits, new storm encounters and four Furious miniboss concept boards.</p><div class="links"><a href="current/boss-comparison-1102.html">57 boss comparisons</a><a href="current/all-waves-1101.html">313 regular-wave chapters</a><a href="enemy-showcase-1031.html">Updated enemy field guide</a><a href="game/index.html">Download playable build</a><a href="storyboard-1102.html">Dialogue storyboard</a><a href="cast-cinematics-1102.html">Cast and pose library</a><a href="field-manual/guide.html">Full field manual</a><a href="https://github.com/REPO/releases/tag/TAG">All November2 downloads</a></div><p class="notes">Boss films use an invulnerable input pilot. Normal6–9 are isolated review entries; the Normal campaign ends at5. Source/art prompts, sound checks and native verification accompany the release.</p></section>'''.replace('REPO',REPO).replace('TAG',TAG)
 old=old.replace('<main>','<main>'+hero,1).replace('Bullets of Fury / Review library','Focused encounter reviews',1);(S/'index.html').write_text(old,encoding='utf-8')
 catalog=json.loads(command(['git','show','origin/gh-pages:manifest.json']));known={c['id']for c in catalog}
 for clip in catalog:clip.update(plan['clips'].get(clip['id'],{}))
 catalog.extend(c for c in plan['additionalClips']if c['id']not in known);(S/'manifest.json').write_text(rewrite(json.dumps(catalog,indent=2)),encoding='utf-8')
 (S/'game').mkdir(exist_ok=True);links=''.join('<li><a href="'+a['url']+'">'+a['name']+'</a> · '+str(round(a['bytes']/1e6))+' MB</li>'for a in plan.get('packages',[]));(S/'game/index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Current BOF build</title><style>body{color:#d9edf8;background:#07111a;font:18px/1.6 system-ui;max-width:900px;margin:40px auto;padding:20px}a{color:#87e5ec}</style><h1>November2 playable build</h1><p>Download and extract all three ZIPs into the same folder. Open the shared BulletsOfFury-2026-11-02 folder and run START-BOF.cmd with Python3 installed. Then open http://127.0.0.1:8000 in your browser.</p><ul>'+links+'</ul><p><a href="../">Back to the review hub</a> · <a href="https://github.com/'+REPO+'/tree/main">Current source</a></p>',encoding='utf-8')
 (S/'.nojekyll').touch();public=dict(tag=TAG,media=[{k:v for k,v in a.items()if k not in ['path','source']}for a in plan['media']],packages=[{k:v for k,v in a.items()if k!='path'}for a in plan.get('packages',[])])
 (S/'publication-1102.json').write_text(json.dumps(public,indent=2),encoding='utf-8');print('EXPORTED',len(list(S.rglob('*'))),'static entries',flush=True)
def pages(publish=True):
 plan=load();env={**os.environ,'GIT_INDEX_FILE':str(O/'pages.index')}
 def git(*a,data=None):return subprocess.run(['git',*a],cwd=R,env=env,input=data,capture_output=True,check=True).stdout.decode().strip()
 parent=git('rev-parse','origin/gh-pages');git('read-tree',parent)
 for p in sorted(S.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(S).as_posix();blob=git('hash-object','-w','--stdin',data=p.read_bytes());git('update-index','--add','--cacheinfo','100644,'+blob+','+rel)
 tree=git('write-tree');commit=git('commit-tree',tree,'-p',parent,data=b'Publish November 2 build, all waves and triple-difficulty boss reviews\n');print(git('diff','--stat',parent,commit));plan['preparedPagesCommit']=commit;save('plan.json',plan)
 if publish:print(command(['git','push','origin',commit+':refs/heads/gh-pages']));plan['pagesCommit']=commit;save('plan.json',plan)
 print('PAGES_COMMIT'if publish else'PREPARED_PAGES_COMMIT',commit,flush=True)
def stagepages():pages(False)
def sourcecheck():
 tracked=command(['git','diff','--name-only','HEAD']).splitlines();new=command(['git','ls-files','--others','--exclude-standard']).splitlines();roots=('assets/','docs/','_BUILD_SOURCE/','_ART_SOURCES/','tools/')
 unrelated=lambda p:any(t in p.lower()for t in ['nightcode','nightcopy','last_dragon','last-dragon','rom_study','tools/spc-studio/'])
 names=sorted({p for p in tracked+new if(p in tracked or p.startswith(roots))and not unrelated(p)and Path(p).suffix.lower()not in ['.mp4','.webm','.mov','.avi']});errors=[];js=[]
 secret=re.compile(r'(?:ghp_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|https?://[^\s<>"\x27]+[?&](?:X-Amz-Signature|X-Goog-Signature|signature|sig|token|credential)=[^\s<>"\x27]+)')
 for name in names:
  p=R/name
  if not p.is_file():continue
  if p.stat().st_size>=100*1024*1024:errors.append(dict(file=name,reason='Git object exceeds100MB'))
  if p.suffix.lower()in ['.py','.js','.json','.html','.md','.txt','.ps1','.cmd','.bat','.cjs','.ts','.yml','.yaml']and secret.search(p.read_text(encoding='utf-8',errors='replace')):errors.append(dict(file=name,reason='Possible credential or signed URL'))
  if p.suffix=='.js':
   q=subprocess.run(['node','--check',str(p)],capture_output=True,text=True);js.append(dict(file=name,passed=q.returncode==0))
   if q.returncode:errors.append(dict(file=name,reason='JavaScript syntax',detail=q.stderr[-700:]))
 save('source-checks.json',dict(files=len(names),js=js,errors=errors));(O/'source-files.nul').write_bytes(b'\0'.join(n.encode('utf-8')for n in names)+b'\0');save('source-files.json',names);print('SOURCE_CHECK',len(names),'files;',len(js),'JavaScript checks;',len(errors),'errors',flush=True)
 if errors:raise RuntimeError(json.dumps(errors))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','packages','export','upload','pages','stagepages','sourcecheck']);args=ap.parse_args();globals()[args.action]()
