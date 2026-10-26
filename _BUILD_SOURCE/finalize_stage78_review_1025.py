"""Consolidate measured delivery evidence without replacing the original takes."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage78_review_1025'
def main():
 probes=[json.loads((O/p/'report.json').read_text())for p in ('probe','pixels')]
 browser=json.loads((O/'browser-playback.json').read_text());clips=[]
 for stage in (7,8):
  p=max((O/'full').glob(f'stage{stage}*/verification.json'),key=lambda p:p.stat().st_mtime);v=json.loads(p.read_text());report=json.loads((p.parent/'report.json').read_text());timeline=report['timeline']
  clips.append(dict(stage=stage,video=v['video'],duration=v['duration'],defeatSeconds=report['defeatSeconds'],mediaChecks=v['checks'],allFurious=all(q['difficulty']=='furious'for q in timeline),allNativeGod=all(q['god']for q in timeline),sourceFPS=round(report['audio']['frames']/timeline[-1]['seconds'],2),pageErrors=report['pageErrors'],consoleErrors=report['consoleErrors'],assetErrors=report['assetErrors']))
 native=[c for p in probes for c in p['checks']];runtime=['assets/game.js','assets/stage78_review_1025.js','assets/stage78_review_art_1025.js','assets/dracodia_rebirth_1023.js','assets/boss_integrity_1024.js']
 hashes={name:hashlib.sha256((R/name).read_bytes()).hexdigest()for name in runtime};old=json.loads((R/'_shots/furious_789_1025/build-fingerprint.json').read_text())['files']
 result=dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),nativePassed=sum(c['passed']for c in native),nativeFailed=sum(not c['passed']for c in native),nativeErrors=[e for p in probes for e in p['errors']],clips=clips,browserChecks=all(all(c['checks'].values())for c in browser['clips']),findingJumpsToOriginal=browser['finding']['jumpsToOriginal'],browserErrors=browser['errors'],runtimeHashes=hashes,gameJsMatchesOriginalCapture=hashes['assets/game.js']==old['assets/game.js'],fullSuite=dict(exitCode=1,reachedSummary=False,reason='Pre-existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs'),review=json.loads((O/'server.json').read_text())['url'])
 (O/'delivery.json').write_text(json.dumps(result,indent=2),encoding='utf8');(R/'docs/qa/stage78_review_1025.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 assert result['nativeFailed']==0 and not result['nativeErrors']and result['browserChecks']and result['findingJumpsToOriginal']and not result['browserErrors']
 assert all(all(c['mediaChecks'].values())and c['allFurious']and c['allNativeGod']for c in clips)
 print(json.dumps(dict(nativePassed=result['nativePassed'],nativeFailed=result['nativeFailed'],videos=len(clips),browserVerified=result['browserChecks'],gameJsPreserved=result['gameJsMatchesOriginalCapture'],review=result['review'])))
if __name__=='__main__':main()
