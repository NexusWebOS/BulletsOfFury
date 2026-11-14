from pathlib import Path
import json,shutil,subprocess,hashlib
from github_api import R,REPO,session,api
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';P=json.loads((O/'package-receipt.json').read_text());U=json.loads((O/'published-release.json').read_text());V=json.loads((O/'package-verification.json').read_text());F=json.loads((O/'portable-checks.json').read_text());H=json.loads((O/'native-host-checks.json').read_text());assert U['allRemoteDigestsVerified']and U['anonymousHelperVerified']and U['anonymousInstallerRangesVerified']and not V['errors']and F['exit']==0
url=U['url'];tag=U['tag'];helper='https://github.com/'+REPO+'/releases/download/'+tag+'/BOF-Install-Helper-RevG.zip'
readme=f'''# Current Windows build publication — November14,2026

Release: {url}

Download [BOF-Install-Helper-RevG.zip]({helper}), extract it, and run Install-BulletsOfFury.cmd. The helper downloads{len(P['parts'])} byte-exact installer parts, verifies each SHA256, joins them in order, verifies the complete setup EXE and opens native Fury HQ setup. It preserves earlier releases and local saves. Allow16GB free during download/setup. Windows10/11 x64; all game graphics/audio, the unchanged byte-verified Fury HQ host and signed offline WebView2 runtime are included. No Python or separate browser is required to play.

This is the current development prerelease for playtesting. Mike's unassisted full experience/balance review remains pending. The older RevF stable release is retained.

## Source and complete payload

The full pending source/art update was committed as636ee1165cf697c7cdbfef6e8e1947dd93c49026. Tracked development-only reference fixtures and publication tooling followed in{P['sourceCommit']}. Both existing publication branches, main and codex/build-2026-10-26, were fast-forwarded together without rewriting history. All current Chronus/Draconus animation, rage, ship and modular-gun work, Stage5 bomber behavior/targeting, pilot/playtest work, authored editable sources, documents and regression fixes are included. The final receipt/documentation commit follows the tagged runtime snapshot without changing gameplay.

The complete installer is{P['installerBytes']:,} bytes with SHA256 `{P['installerSha256']}`. Its payload contains{P['files']:,} owned files totaling{P['unpackedBytes']:,} unpacked bytes. All committed runtime inputs matched their Git blob IDs while being packaged; the exact legacy signed offline runtime bytes matched their known hash. All remote installer-part digests match the local streamed bytes. The embedded footer, complete deployment manifest, unique entry names and every entry size were read back from GitHub and verified. {len(V['readBackVerifiedFiles'])} critical/active-script files were fully read back, decompressed and SHA256-checked against the deployment manifest. The existing native installer verifies every extracted payload file's SHA256 again when installed.

## Checks and previews

- Full regression runner reaches its final summary with{F['passed']:,} passing assertions, zero failures and exit0, using only the tracked reference fixtures rather than the optional local ignored archive.
- Actual native Windows host:{len(H['checks'])} self-tests passed. Its executable and embedded original launcher artwork are unchanged from the previous verified host.
- A clean build directory with byte-identical hard links avoids a second4GB copy. Its fresh title and Stages5/6/7/8 load/update/render checks pass with no page/update/draw errors. The directory's files are bound to the uploaded manifest and source identities; the uploaded payload itself is separately checked above.
- Current source also retains the previously verified60 native bomber/weapon checks,7 active-targeting checks,256 exact editable retina frames and restored16 native leech cells.
- All{len(U['assets'])} published assets have verified GitHub SHA256 digests. Anonymous retrieval verifies the helper ZIP and sample beginning/footer bytes from the public installer parts.

Three native checkpoint previews accompany the build: new beeping/rotating/flashing bomber target lock; two full bomber attack/flight cycles; Draconus's new rage/two-handed wave/center smash. Their invulnerable review labels remain visible. They are behavior previews, not unassisted full-stage clears. Previous full-stage films keep their original dates.

See qa/github_windows_publication_1114.json, qa/github_publication_1114/ and the release validation/checksum manifests for exact counts, source hashes and verification limits. Publication scripts are retained in _BUILD_SOURCE/github_upload_1114. They use the existing GitHub login only in memory; no credential or signed asset URL is published. Large temporary installer parts are removed locally only after their remote SHA256 is confirmed. No existing user data or prior GitHub release assets are deleted.
'''
p=R/'docs/GITHUB_WINDOWS_PUBLICATION_1114.md';p.write_text(readme,encoding='utf-8');p=R/'README.md';b=p.read_bytes();text=b.decode('utf-8');marker='Release source branch: `codex/build-2026-10-26`';section=f'''\n\n## Current Windows build — November14,2026 / Rev G

[Download the current Windows build]({url}). Extract **BOF-Install-Helper-RevG.zip** and run **Install-BulletsOfFury.cmd**. The helper retrieves/verifies all installer parts and opens the complete Fury HQ setup. All current game art, audio and the offline Windows runtime are included. Allow16GB free during download/setup.

Includes the current boss/hammer/rage/ship/gun work, Stage5 bomber pursuit and active beeping target optics, pilot/playtest improvements and shared health-helper repairs. The full suite now finishes with **8,969 passed, zero failures**, including the fresh-download reference path. Native launcher and clean packaged Stages5–8 checks pass. This is the current development prerelease for home playtesting; the older stable release remains below.

[Build contents, checks and limits](docs/GITHUB_WINDOWS_PUBLICATION_1114.md).
'''
if'## Current Windows build — November14,2026 / Rev G'not in text:
 assert marker in text;text=text.replace(marker,marker+section,1);text=text.replace('## Windows launcher and complete game — Rev F','## Previous Windows release — Rev F',1);assert p.read_bytes()==b;p.write_bytes(text.encode('utf-8'))
source=R/'_BUILD_SOURCE/github_upload_1114';source.mkdir(exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,source/p.name)
qa=R/'docs/qa/github_publication_1114';qa.mkdir(parents=True,exist_ok=True)
for name in ['source-upload.json','portable-checks.json','full-suite-portable.log','native-host-checks.json','package-verification.json','package-receipt.json','published-release.json','secret-scan.json']:shutil.copy2(O/name,qa/name)
# Store stable public URLs in the publication receipt, not draft download links.
p=qa/'package-receipt.json';j=json.loads(p.read_text())
for q in j['parts']:q['url']='https://github.com/'+REPO+'/releases/download/'+tag+'/'+q['name']
p.write_text(json.dumps(j,indent=2))
note=f'''## November14,2026 — Current source and complete Windows RevG on GitHub

Mike authorized all changes and the current build uploaded. Full source/art
snapshot636ee1165 and portable-check follow-up{P['sourceCommit'][:9]} are on main
and codex/build-2026-10-26; no history rewrite. The new development prerelease
{tag} contains the complete Windows installer in{len(P['parts'])} verified parts,
download/join helper, original Fury HQ host/offline runtime and current previews.
Full suite8,969 passed/0 failed with tracked fallback reference fixtures. Native
host14 checks and clean packaged title/Stages5–8 pass; all release digests and
anonymous helper/installer sample downloads verified. Home unassisted experience
playtest remains pending; earlier releases remain. This supersedes earlier
source-only/no-publication notes. Docs: docs/GITHUB_WINDOWS_PUBLICATION_1114.md.
Release: {url}

'''
p=R/'HANDOFF_CODEX.md';b=p.read_bytes()
if note.splitlines()[0].encode()not in b:assert p.read_bytes()==b;p.write_bytes(note.encode()+b)
receipt=dict(repository=REPO,release=url,tag=tag,runtimeSourceCommit=P['sourceCommit'],initialSourceCommit='636ee1165cf697c7cdbfef6e8e1947dd93c49026',installerBytes=P['installerBytes'],installerSha256=P['installerSha256'],payloadFiles=P['files'],parts=len(P['parts']),assets=len(U['assets']),allRemoteSHA256=True,anonymousHelper=True,anonymousInstallerRanges=True,fullAssertions=F['passed'],fullFailures=0,nativeHostChecks=len(H['checks']),cleanPackageChecks=V['checks'],readBackCriticalFiles=len(V['readBackVerifiedFiles']),prerelease=True,unassistedPlaytestPending=True)
target=R/'docs/qa/github_windows_publication_1114.json';target.write_text(json.dumps(receipt,indent=2))
def git(*args):
 q=subprocess.run(['git','-c','gc.auto=0','-C',str(R),*args],capture_output=True,text=True,encoding='utf-8',errors='replace');assert q.returncode==0,q.stderr[-1600:];return q.stdout
git('add','--','README.md','HANDOFF_CODEX.md','docs/GITHUB_WINDOWS_PUBLICATION_1114.md','docs/qa/github_publication_1114','docs/qa/github_windows_publication_1114.json','_BUILD_SOURCE/github_upload_1114');git('commit','-m','Publish verified November 14 Windows Rev G build and download helper');sha=git('rev-parse','HEAD').strip();git('push','--atomic','origin','HEAD:refs/heads/codex/build-2026-10-26','HEAD:refs/heads/main');refs=git('ls-remote','--heads','origin','main','codex/build-2026-10-26');assert len([l for l in refs.splitlines()if l.startswith(sha+'\t')])==2
tagref=api(session(),'GET','repos/'+REPO+'/git/ref/tags/'+tag);assert tagref['object']['sha']==P['sourceCommit'];status=git('status','--porcelain','--untracked-files=all');(O/'status-after.txt').write_text(status);receipt.update(publicationCommit=sha,branchesVerified=True,tagVerified=True,workingTreeClean=not status);(O/'final-receipt.json').write_text(json.dumps(receipt,indent=2));assert not status,'There are still local changes to review before declaring all changes uploaded.'
(O/'pipeline-state.json').write_text(json.dumps(dict(phase='complete'),indent=2))
print('COMPLETE',url,'source',sha,'all branches/tag/assets verified; working tree clean.',flush=True)
