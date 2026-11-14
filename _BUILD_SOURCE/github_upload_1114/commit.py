from pathlib import Path
import subprocess,json,hashlib,shutil,time
from github_api import R
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';plan=json.loads((O/'object-plan.json').read_text());remote=json.loads((O/'remote.json').read_text());verification=json.loads((W.parents[1]/'outputs/Release-checks-1114/verification.json').read_text())
assert verification['fullFailures']==0 and verification['fullExit']==0
for n,h in verification['sourceHashes'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
def git(*args,check=True):
 p=subprocess.run(['git','-c','gc.auto=0','-C',str(R),*args],capture_output=True,text=True,encoding='utf-8',errors='replace');assert not check or p.returncode==0,p.stderr[-1600:];return p
head=git('rev-parse','HEAD').stdout.strip();assert head==remote['refs']['HEAD'],'HEAD changed; review before committing'
assert not git('ls-files','--unmerged').stdout
free=shutil.disk_usage(R).free;print('STAGING all changes; available MB',round(free/1e6),'upper-bound new objects MB',round(plan['compressedBytes']/1e6),flush=True);assert free>plan['compressedBytes']+150_000_000,'Insufficient space for the verified upload object plan'
git('add','--all');count=len(git('diff','--cached','--name-only').stdout.splitlines());assert count>0
check=git('diff','--cached','--check',check=False);(O/'staged-whitespace-check.log').write_text(check.stdout+check.stderr,encoding='utf-8')
p=git('commit','-m','Update November 14 gameplay, boss art and full-check fixes','-m','Include the current Chronus and Draconus attack, rage, ship and modular-gun work; Stage 5 bomber pursuit and active target optics; current pilot/playtest improvements; authored sources and validation evidence. Fix shared difficulty initialization and complete the full regression suite with 8,969 passing assertions and zero failures.');(O/'commit.log').write_text(p.stdout+p.stderr,encoding='utf-8');sha=git('rev-parse','HEAD').stdout.strip();print('COMMITTED',sha,'files',count,'free MB',round(shutil.disk_usage(R).free/1e6),flush=True)
# Fast-forward both existing publication branches together. No history rewrite.
p=subprocess.run(['git','-c','gc.auto=0','-c','pack.windowMemory=64m','-c','pack.threads=2','-c','pack.deltaCacheSize=16m','-C',str(R),'push','--atomic','origin','HEAD:refs/heads/codex/build-2026-10-26','HEAD:refs/heads/main'],capture_output=True,text=True,encoding='utf-8',errors='replace');(O/'push.log').write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,p.stderr[-2000:]
refs=git('ls-remote','--heads','origin','main','codex/build-2026-10-26').stdout;assert len([l for l in refs.splitlines()if l.startswith(sha+'\t')])==2
(O/'source-upload.json').write_text(json.dumps(dict(commit=sha,files=count,branches=['main','codex/build-2026-10-26'],remoteVerified=True,fullAssertions=verification['fullPasses']),indent=2));print('PUSHED AND VERIFIED',sha,'on main and production branch',flush=True)
