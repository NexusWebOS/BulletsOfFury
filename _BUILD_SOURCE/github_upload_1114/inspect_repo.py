from pathlib import Path
import subprocess,json,shutil,collections,os
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/GitHub-upload-1114';O.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
raw=git('status','--porcelain=v1','-z','--untracked-files=all');(O/'status-before.bin').write_bytes(raw);records=[]
for rec in raw.split(b'\0'):
 if not rec:continue
 s=rec.decode('utf-8');flag=s[:2];name=s[3:];p=R/name;records.append(dict(status=flag,path=name,bytes=p.stat().st_size if p.is_file()else 0))
totals=collections.Counter();roots=collections.Counter();sizes=collections.Counter()
for q in records:totals[q['status']]+=1;roots[q['path'].split('/')[0]]+=1;sizes[q['path'].split('/')[0]]+=q['bytes']
files=[]
for top in ['assets','extensions','_BUILD_SOURCE/desktop_windows_1106','_BUILD_SOURCE/BOF-Official-Build-1105']:
 d=R/top;fs=[p for p in d.rglob('*')if p.is_file()]if d.exists()else[];files.append(dict(root=top,files=len(fs),bytes=sum(p.stat().st_size for p in fs)))
gh=shutil.which('gh');dotnet=shutil.which('dotnet');seven=shutil.which('7z')
if not gh:
 for p in [Path(r'C:/Program Files/GitHub CLI/gh.exe'),Path(os.environ['LOCALAPPDATA'])/'Microsoft/WinGet/Links/gh.exe']:
  if p.exists():gh=str(p);break
installed=[]
for root in [Path(os.environ['LOCALAPPDATA'])/'Programs',Path(r'C:/Program Files/ColeForge'),Path(r'C:/Program Files/Bullets of Fury')]:
 if root.exists():installed += [dict(path=str(p),bytes=p.stat().st_size)for p in root.rglob('Bullets of Fury.exe')]
result=dict(branch=git('branch','--show-current').decode().strip(),head=git('rev-parse','HEAD').decode().strip(),upstream=git('rev-parse','--abbrev-ref','@{upstream}').decode().strip(),status=dict(totals),roots=dict(roots),sizes=dict(sizes),changedBytes=sum(q['bytes']for q in records),largeFiles=sorted([q for q in records if q['bytes']>50_000_000],key=lambda q:-q['bytes']),runtime=files,free=shutil.disk_usage(R).free,tools=dict(gh=gh,dotnet=dotnet,seven=seven),installedHosts=installed,remote=git('remote','get-url','origin').decode().strip())
(O/'inventory.json').write_text(json.dumps(result,indent=2));(O/'changes.json').write_text(json.dumps(records,indent=2));print(json.dumps(result,indent=2),flush=True)
if gh:
 for name,args in [('repo',['api','repos/NexusWebOS/BulletsOfFury','--jq','{default_branch,visibility,size,pushed_at}']),('releases',['release','list','--repo','NexusWebOS/BulletsOfFury','--limit','4','--json','tagName,name,isDraft,isPrerelease,publishedAt'])]:
  q=subprocess.run([gh,*args],cwd=R,capture_output=True,text=True);(O/(name+'.json')).write_text(q.stdout or json.dumps(dict(error=q.stderr)),encoding='utf-8');print(name,q.returncode,q.stdout[:2000]or q.stderr[:300],flush=True)
