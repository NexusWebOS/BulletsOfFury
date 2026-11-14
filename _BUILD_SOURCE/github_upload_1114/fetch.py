from pathlib import Path
import json,subprocess,hashlib
from github_api import session,api,R,REPO
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';before=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip()
p=subprocess.run(['git','-C',str(R),'fetch','origin'],capture_output=True,text=True);(O/'fetch.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
refs={n:subprocess.check_output(['git','-C',str(R),'rev-parse',n]).decode().strip()for n in ['HEAD','origin/main','origin/codex/build-2026-10-26']};changes=subprocess.check_output(['git','-C',str(R),'log','--oneline','HEAD..origin/main']).decode();print('Fetched heads',json.dumps(refs),'incoming commits:',changes[:1500]or'none',flush=True)
s=session();user=api(s,'GET','user');repo=api(s,'GET','repos/'+REPO);releases=api(s,'GET','repos/'+REPO+'/releases?per_page=5');base=api(s,'GET','repos/'+REPO+'/releases/tags/bof-windows-2026-11-06-revf')
(O/'remote.json').write_text(json.dumps(dict(refs=refs,user=user['login'],defaultBranch=repo['default_branch'],releases=[{k:r[k]for k in ['tag_name','name','draft','prerelease','target_commitish']}for r in releases],base=base,incoming=changes),indent=2));print('Authenticated GitHub upload account:',user['login'],'base release assets:',len(base['assets']),flush=True)
