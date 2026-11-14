from pathlib import Path
import json,hashlib,zipfile,subprocess,urllib.parse,urllib.request,time
from github_api import R,REPO,session,api
from remote_zip import PartsReader
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';P=json.loads((O/'package-receipt.json').read_text());V=json.loads((O/'package-verification.json').read_text());H=json.loads((O/'native-host-checks.json').read_text());F=json.loads((O/'portable-checks.json').read_text());assert not V['errors']and all(q['passed']for q in V['checks'])and all(q['passed']for q in H['checks'])and F['exit']==0
s=session();tag=P['tag'];rid=P['releaseId'];release=api(s,'GET','repos/'+REPO+'/releases/'+str(rid));assert release['tag_name']==tag;existing={q['name']:q for q in release['assets']};base='https://github.com/'+REPO+'/releases/download/'+tag+'/';assets=[]
for q in P['parts']:q=dict(q);q['url']=base+q['name'];assets.append(q)
def upload(path):
 size=path.stat().st_size;h=hashlib.sha256(path.read_bytes()).hexdigest();url='https://uploads.github.com/repos/'+REPO+'/releases/'+str(rid)+'/assets?name='+urllib.parse.quote(path.name)
 if path.name in existing:r=existing[path.name]
 else:
  with path.open('rb')as f:response=s.request('POST',url,data=f,headers={'Content-Type':'application/octet-stream','Content-Length':str(size)},timeout=600)
  assert response.ok,(response.status_code,response.text[:200]);r=response.json()
 assert r['size']==size and r.get('digest')=='sha256:'+h;row=dict(name=path.name,bytes=size,sha256=h,url=base+path.name,id=r['id'],verified=True);assets.append(row);print('VERIFIED RELEASE ASSET',path.name,flush=True);return row
helper=O/'helper';helper.mkdir(exist_ok=True);ps=(R/'_BUILD_SOURCE/desktop_windows_1106/Install-BulletsOfFury.ps1').read_text();a=ps.index('$parts=@(');b=ps.index('$bofOutput=',a);block='$parts=@(\n'+''.join("    @{Name='"+q['name']+"'; Bytes="+str(q['bytes'])+"; Sha256='"+q['sha256']+"'; Url='"+base+q['name']+"'}\n"for q in P['parts'])+')\n';ps=ps[:a]+block+ps[b:];ps=ps.replace('2026-11-06-RevF','2026-11-14-RevG').replace('3885709224',str(P['installerBytes'])).replace('ab019939bc940a79ff41e3333787b08ac532347e71a6e0a6019fe4fff9266d37',P['installerSha256'])
assert'2026-11-06-RevF'not in ps and ps.count("Name='BulletsOfFury-Setup-2026-11-14-RevG.exe.part")==len(P['parts']);(helper/'Install-BulletsOfFury.ps1').write_text(ps,encoding='utf-8');(helper/'Install-BulletsOfFury.cmd').write_bytes((R/'_BUILD_SOURCE/desktop_windows_1106/Install-BulletsOfFury.cmd').read_bytes());(helper/'READ-ME.txt').write_bytes((O/'READ-ME.txt').read_bytes())
cmd="$e=$null;$t=$null;[System.Management.Automation.Language.Parser]::ParseFile('"+str(helper/'Install-BulletsOfFury.ps1')+"',[ref]$t,[ref]$e)|Out-Null;if($e.Count){$e|ForEach-Object {$_.Message};exit 1}"
q=subprocess.run(['powershell','-NoProfile','-Command',cmd],capture_output=True,text=True);assert q.returncode==0,q.stdout+q.stderr
hp=O/'BOF-Install-Helper-RevG.zip'
if not hp.exists():
 with zipfile.ZipFile(hp,'x',zipfile.ZIP_DEFLATED)as z:
  for p in helper.iterdir():z.write(p,p.name)
with zipfile.ZipFile(hp)as z:
 assert not z.testzip();assert z.read('Install-BulletsOfFury.ps1')==(helper/'Install-BulletsOfFury.ps1').read_bytes()
upload(hp);upload(O/'READ-ME.txt')
for name,path in [('BOF-Stage5-Targeting-RevG.mp4',W.parents[1]/'outputs/Release-checks-1114/bomber-retina-rotation-flash-beeps.mp4'),('BOF-Stage5-Bomber-RevG.mp4',W.parents[1]/'outputs/Stage5-bomber-assault/stage5-bomber-furious-final.mp4'),('BOF-Draconus-Rage-RevG.mp4',W.parents[1]/'outputs/Draconus-new-rage/draconus-new-rage-kamehameha-and-center-smash.mp4')]:
 if path.is_file():dest=O/name;dest.write_bytes(path.read_bytes());upload(dest)
validation=dict(fullSuite=dict(passed=F['passed'],failures=0,exit=F['exit'],portableReferenceFiles=F['referenceFiles']),nativeHostChecks=len(H['checks']),cleanPackageChecks=V['checks'],allPayloadEntrySizesVerified=V['files'],remoteReadBackFiles=len(V['readBackVerifiedFiles']),remotePartDigests=V['remotePartDigests'],sourceCommit=P['sourceCommit'],limits='Current development prerelease. Review clips use invulnerable native checkpoints. Full unassisted experience/balance playtest pending.')
vp=O/'BOF-validation-RevG.json';vp.write_text(json.dumps(validation,indent=2));upload(vp)
manifest=dict(repository=REPO,tag=tag,sourceCommit=P['sourceCommit'],version=P['version'],installer=dict(name=P['installerName'],bytes=P['installerBytes'],sha256=P['installerSha256'],parts=len(P['parts']),unpackedFiles=P['files'],unpackedBytes=P['unpackedBytes']),assets=assets.copy(),validation=validation)
mp=O/'BOF-Release-Manifest-RevG.json';mp.write_text(json.dumps(manifest,indent=2));upload(mp);sums=O/'BOF-SHA256SUMS-RevG.txt';sums.write_text(''.join(q['sha256']+'  '+q['name']+'\n'for q in assets));upload(sums)
remote=api(s,'GET','repos/'+REPO+'/releases/'+str(rid));actual={q['name']:q for q in remote['assets']};assert len(actual)==len(assets)
for q in assets:r=actual[q['name']];assert r['size']==q['bytes']and r['state']=='uploaded'and r.get('digest')=='sha256:'+q['sha256']
published=api(s,'PATCH','repos/'+REPO+'/releases/'+str(rid),json=dict(draft=False,prerelease=True,make_latest='false',target_commitish=P['sourceCommit']));assert not published['draft']and published['prerelease']and published['tag_name']==tag
# Anonymous public retrieval: helper ZIP plus beginning/end of the installer.
with urllib.request.urlopen(base+hp.name,timeout=120)as f:data=f.read()
assert hashlib.sha256(data).hexdigest()==next(q['sha256']for q in assets if q['name']==hp.name)
public=PartsReader(sorted([q for q in published['assets']if'.exe.part'in q['name']],key=lambda q:int(q['name'].rsplit('part',1)[1])));assert public.read(2)==b'MZ';public.seek(-64,2);assert public.read(16)==b'BOFSETUP1106DATA'
(O/'published-release.json').write_text(json.dumps(dict(url=published['html_url'],tag=tag,id=rid,publishedAt=published['published_at'],sourceCommit=P['sourceCommit'],assets=assets,allRemoteDigestsVerified=True,anonymousHelperVerified=True,anonymousInstallerRangesVerified=True,validation=validation),indent=2));print('PUBLISHED AND PUBLICLY VERIFIED',published['html_url'],len(assets),'assets',flush=True)
