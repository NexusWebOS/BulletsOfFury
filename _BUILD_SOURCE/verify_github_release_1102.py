"""Create public checksums and verify uploaded bytes against GitHub's digests."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/github_upload_1102'
REPO='NexusWebOS/BulletsOfFury';TAG='bof-complete-update-2026-11-02'
def gh(*args):return json.loads(subprocess.check_output(['gh',*args],cwd=R))
def save(path,data):path.write_text(json.dumps(data,indent=2),encoding='utf-8')
def metadata():
 p=json.loads((O/'plan.json').read_text());assets=p['media']+p['packages'];rows=[{k:a[k]for k in ['name','bytes','sha256','url']}for a in assets]
 source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
 manifest=dict(repository=REPO,tag=TAG,sourceSnapshot=source,media=len(p['media']),runtimePackages=len(p['packages']),assets=rows)
 f=O/'BOF-publication-manifest-2026-11-02.json';save(f,manifest)
 sums=O/'BOF-SHA256SUMS-2026-11-02.txt';sums.write_text(''.join(a['sha256']+'  '+a['name']+'\n'for a in assets),encoding='utf-8')
 validation=O/'BOF-validation-2026-11-02.json';save(validation,dict(packagedRuntime=json.loads((O/'package-playback.json').read_text()),javascriptSyntaxChecks=75,bossPlaybackChecks=57,comparisonUIChecks=11,collectionChecks=20,coreSuite=dict(exitCode=1,completed=False,reason='Existing ignored UNUSED_ASSETS/retired_art_1022/manifest.json is absent; suite exits before assertions or summary.'),captureLimits=dict(razorwakeAverageFPS=41.2,stage7RegularWaveAverageFPS=35.02)))
 p['metadata']=[dict(name=a.name,path=str(a),bytes=a.stat().st_size,sha256=hashlib.sha256(a.read_bytes()).hexdigest(),url='https://github.com/'+REPO+'/releases/download/'+TAG+'/'+a.name)for a in [f,sums,validation]];save(O/'plan.json',p);print('METADATA',len(assets),'checksummed assets;',len(p['metadata']),'metadata files')
def verify():
 p=json.loads((O/'plan.json').read_text());release=gh('release','view',TAG,'--repo',REPO,'--json','databaseId,tagName,isDraft,isPrerelease,targetCommitish,url');pages=gh('api','--paginate','--slurp','repos/'+REPO+'/releases/'+str(release['databaseId'])+'/assets?per_page=100');remote={a['name']:a for page in pages for a in page};checks=[]
 for a in p['media']+p['packages']+p.get('metadata',[]):
  b=remote.get(a['name'],{});checks.append(dict(name=a['name'],passed=b.get('size')==a['bytes']and b.get('state')=='uploaded'and b.get('digest')=='sha256:'+a['sha256'],bytes=b.get('size'),digest=b.get('digest'),state=b.get('state')))
 out=dict(release=release,expected=len(checks),remote=len(remote),passed=sum(x['passed']for x in checks),bytes=sum(a.get('size',0)for a in remote.values()),checks=checks);save(O/'release-integrity.json',out);print('INTEGRITY',out['passed'],'/',out['expected'],'remote assets',out['remote'],'GB',round(out['bytes']/1e9,3));sys.exit(0 if all(x['passed']for x in checks)else 1)
def receipt():
 p=json.loads((O/'plan.json').read_text());integrity=json.loads((O/'release-integrity.json').read_text());public=json.loads((O/'public-playback.json').read_text());manifest=json.loads((O/'BOF-publication-manifest-2026-11-02.json').read_text());assert integrity['passed']==integrity['expected']and not integrity['release']['isDraft'];assert all(x['passed']for x in public)
 p['pagesCommit']=p['preparedPagesCommit'];save(O/'plan.json',p)
 out=dict(repository=REPO,release=integrity['release'],runtimeSnapshot=manifest['sourceSnapshot'],pagesCommit=p['pagesCommit'],releaseFiles=integrity['expected'],verifiedSHA256=integrity['passed'],releaseBytes=integrity['bytes'],mediaFiles=len(p['media']),packages=[{k:a[k]for k in ['name','bytes','sha256','url']}for a in p['packages']],packagedRuntime=json.loads((O/'package-playback.json').read_text()),publicPreview=public,library=dict(bossFilms=57,regularWaveChapters=313,enemyClips=154),limits=dict(fullSuiteExitCode=1,fullSuiteCompleted=False,fullSuiteReason='Existing ignored UNUSED_ASSETS/retired_art_1022/manifest.json is absent.',razorwakeCaptureFPS=41.2,stage7RegularWaveFPS=35.02,concurrentWork='Active cast-performance edits created after the runtime snapshot remain in the working checkout.'))
 target=R/'docs/qa/github_publication_1102.json';target.parent.mkdir(exist_ok=True);save(target,out);print('RECEIPT',target.relative_to(R))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['metadata','verify','receipt']);a=ap.parse_args();globals()[a.action]()
