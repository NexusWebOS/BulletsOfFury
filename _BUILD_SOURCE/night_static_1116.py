from pathlib import Path
import re,subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';checks=[]
sources=re.findall(r'<script[^>]+src=["\x27]([^"\x27]+)',(R/'index.html').read_text(encoding='utf8'))
for url in sources:
 if re.match('https?://',url):continue
 f=R/url.split('?')[0];q=subprocess.run(['node','--check',str(f)],capture_output=True,text=True,encoding='utf8',errors='replace')if f.exists()else None
 checks.append({'file':url,'exists':f.exists(),'exit':q.returncode if q else None,'error':(q.stderr or q.stdout)[-1200:]if q and q.returncode else''})
raw=(R/'assets/game.js').read_bytes();t=(R/'_BUILD_SOURCE/test_fl.js').read_bytes()
inline=[]
for i,code in enumerate(re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>',(R/'index.html').read_text(encoding='utf8'))):
 if not code.strip():continue
 q=subprocess.run(['node','--check','--input-type=commonjs'],input=code,capture_output=True,text=True,encoding='utf8',errors='replace')
 inline.append({'block':i,'exit':q.returncode,'error':q.stderr[-1000:]if q.returncode else''})
baseline=(R/'_shots/release_qa_1116_baseline.log').read_text(encoding='utf8');final=(O/'full-suite-final.log').read_text(encoding='utf8')
fails=lambda s:[v for v in s.splitlines()if 'ASSERT FAIL:'in v or 'FAILED —'in v]
report={'activeScripts':len(checks),'checks':checks,'baseline':{'passes':sum(v.startswith('  ok  ')for v in baseline.splitlines()),'failures':fails(baseline)},'final':{'passes':sum(v.startswith('  ok  ')for v in final.splitlines()),'failures':fails(final),'summary':final.splitlines()[-1]},'newFailures':sorted(set(fails(final))-set(fails(baseline))),'gameLF':b'\r\n'not in raw,'testsCRLF':t.count(b'\r\n')==t.count(b'\n'),'hashes':{str(f):hashlib.sha256((R/f).read_bytes()).hexdigest()for f in ['assets/game.js','_BUILD_SOURCE/test_fl.js','assets/online.js','index.html','assets/release_cinema_1116.js','assets/release_entry_1116.js','assets/night_cinema_1116.js','assets/night_hq_art_1116.js','assets/night_city_atlas_1116.js','assets/night_weather_1116.js','assets/night_missile_stats_1116.js','_BUILD_SOURCE/serve_nocache_1017.py']}}
report['inlineScripts']=inline
report['finalSummaryReached']='==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in final
assert report['finalSummaryReached'] and report['final']['passes']>=report['baseline']['passes'], 'Full suite has not reached its final summary'
(O/'static-report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({k:report[k]for k in ['activeScripts','baseline','final','newFailures','gameLF','testsCRLF']}));print('syntax failures',[(q['file'],q['error'])for q in checks if q['exit']!=0]);print('inline',len(inline),'failures',[q for q in inline if q['exit']]);assert all(q['exit']==0 for q in checks+inline)and not report['newFailures']and report['gameLF']and report['testsCRLF']
