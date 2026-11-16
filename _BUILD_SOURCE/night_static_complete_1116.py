from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';p=R/'_BUILD_SOURCE/night_static_1116.py';s=p.read_text(encoding='utf8')
if "finalSummaryReached"not in s:
 s=s.replace("report['inlineScripts']=inline", "report['inlineScripts']=inline\nreport['finalSummaryReached']='==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in final\nassert report['finalSummaryReached'] and report['final']['passes']>=report['baseline']['passes'], 'Full suite has not reached its final summary'")
 p.write_text(s,encoding='utf8',newline='\n')
old=O/'static-final.log';dest=O/'static-before-suite-complete.log'
if old.exists()and not dest.exists():dest.write_bytes(old.read_bytes())
print('Require final summary and complete baseline assertion count')
