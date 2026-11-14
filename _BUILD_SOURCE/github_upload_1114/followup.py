from pathlib import Path
import json,subprocess,shutil
from github_api import R
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';checks=json.loads((O/'portable-checks.json').read_text());assert checks['exit']==0 and checks['summary'];prior=json.loads((O/'source-upload.json').read_text())
dest=R/'_BUILD_SOURCE/github_upload_1114';dest.mkdir(exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,dest/p.name)
(dest/'README.md').write_text('November14 publication tools and provenance. Uses the existing authenticated Git login only in memory; no credential is embedded. The complete current Windows payload reuses the byte-verified existing Fury HQ host and signed offline runtime, with all current game files validated against the source commit. Parts are uploaded and checked one at a time to bound local storage. Local output/review paths are configured for Mike\'s working environment. These tools are development-only and not shipped inside the playable payload.\n',encoding='utf-8')
def git(*args):
 p=subprocess.run(['git','-c','gc.auto=0','-C',str(R),*args],capture_output=True,text=True,encoding='utf-8',errors='replace');assert p.returncode==0,p.stderr[-1500:];return p.stdout
git('add','--','_BUILD_SOURCE/test_references_1022','_BUILD_SOURCE/retired_art_archive_1022.cjs','_BUILD_SOURCE/release_checks_1114/repair.py','_BUILD_SOURCE/release_checks_1114/references','_BUILD_SOURCE/github_upload_1114')
git('commit','-m','Make full checks reproducible from a fresh GitHub download');sha=git('rev-parse','HEAD').strip();print('PORTABLE SOURCE COMMIT',sha,flush=True)
git('push','--atomic','origin','HEAD:refs/heads/codex/build-2026-10-26','HEAD:refs/heads/main');refs=git('ls-remote','--heads','origin','main','codex/build-2026-10-26');assert len([l for l in refs.splitlines()if l.startswith(sha+'\t')])==2
prior['initialCommit']=prior['commit'];prior['commit']=sha;prior['portableFullAssertions']=checks['passed'];(O/'source-upload.json').write_text(json.dumps(prior,indent=2));print('PORTABLE SOURCE PUSHED AND VERIFIED',sha,flush=True)
