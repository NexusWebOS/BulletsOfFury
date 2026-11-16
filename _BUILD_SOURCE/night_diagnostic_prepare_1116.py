from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'_BUILD_SOURCE/night_sweep_1116.py').read_text(encoding='utf8')
s=s.replace('import time\n','import time\nfrom urllib.parse import urlsplit\n')
s=s.replace("'_shots/cinema_overnight_1116/native-sweep'","'_shots/cinema_overnight_1116/native-diagnostic'")
s=s.replace('port, stop = serve(str(ROOT))','port, stop = 8765, lambda:None')
s=s.replace('errors, console, asset_errors, timeline = [], [], [], []','errors, console, asset_errors, timeline, warnings = [], [], [], [], []')
s=s.replace("page.on('response',", "page.on('console', lambda m: warnings.append(m.text) if m.type == 'warning' else None)\n            page.on('requestfailed', lambda r: asset_errors.append({'host':urlsplit(r.url).netloc,'path':urlsplit(r.url).path,'failure':r.failure}))\n            page.on('response',",1)
s=s.replace('report.update(pageErrors=errors, consoleErrors=console, assetErrors=asset_errors, timeline=timeline)','report.update(pageErrors=errors, consoleErrors=console, assetErrors=asset_errors, consoleWarnings=warnings, timeline=timeline)')
s=s.replace('nativeFrames:window.__bofFrames,', 'screen:{w:cv.width,h:cv.height},view:{zoom:viewZoom(),w:viewW(),h:viewH()},nativeFrames:window.__bofFrames,')
(R/'_BUILD_SOURCE/night_diagnostic_1116.py').write_text(s,encoding='utf8',newline='\n')
print('Prepared stable-origin request failure/warning and viewport diagnostics')
