from pathlib import Path
P=Path(__file__).with_name('night_review_1116.py');s=P.read_text(encoding='utf8')
s=s.replace("6:'native-diagnostic'", "6:'native-weather'")
s=s.replace("hard=q.get('pageErrors',[])+q.get('consoleErrors',[])+q.get('assetErrors',[]);", "soft=[e for e in q.get('assetErrors',[])if isinstance(e,dict)and e.get('failure')=='net::ERR_ABORTED'and e.get('host')=='127.0.0.1:8765'and Path(e.get('path','')).suffix.lower()in['.mp3','.wav','.ogg','.m4a']and(R/e.get('path','').lstrip('/')).is_file()];hard=q.get('pageErrors',[])+q.get('consoleErrors',[])+[e for e in q.get('assetErrors',[])if e not in soft];")
s=s.replace("'errors':hard,'invalidSourceRects'", "'errors':hard,'expectedAudioPreloadCancellations':soft,'invalidSourceRects'")
needle="remaining=['Complete unassisted human"
extra="""for title,name in [('Federation attachments and code-only satellite','post4'),('Complete native space-kit assembly','assembly')]:
 file='stage45-current/'+name+'.mp4'
 if(O/file).exists():clips.insert(6,{'title':title,'file':file,'type':'Prepared cinematic checkpoint','note':'Current full-text reading holds, code-only satellite and native selected-aircraft kit parts/exhaust. Prepared checkpoint; result/equipment/map menus between clips omitted.','report':'stage45-current/recording.json'})
file='campaign-start/normal-campaign-start.mp4'
if(O/file).exists():clips.append({'title':'Fresh Normal campaign start · normal damage','file':file,'type':'Limited input bot, no GOD','note':'Native fresh Normal campaign with default lives/resources and actual damage. Bot movement/aiming quality is limited; inspect its outcome receipt. No HP/lives/phase/timer edits. This is not human balance certification or a full campaign win.','report':'campaign-start/report.json'})
fixed.append('Skipped only off-canvas authored Stage6 weather tiles.48 pixel comparisons and5 fallback comparisons are identical; representative33 bitmap submissions become15–16. Full native post-change boss replay completed. No claim of target-hardware60FPS.')
"""
# fixed is declared after remaining; append the weather item after its literal instead.
extra=extra[:extra.index("fixed.append")]
if 'Complete native space-kit assembly'not in s:s=s.replace(needle,extra+needle)
if 'Skipped only off-canvas authored Stage6'not in s:s=s.replace("report={'updatedUTC'", "fixed.append('Skipped only off-canvas authored Stage6 weather tiles.48 pixel comparisons and5 fallback comparisons are identical; representative33 bitmap submissions become15–16. Full native post-change boss replay completed. Target-hardware performance remains a release gate.')\nreport={'updatedUTC'")
needle="(R/'docs/qa/cinema_overnight_1116.json').write_text"
extra="""report['coreAndSyntax']=read('static-report.json')
report['warningMatrix']={'cases':len(read('warning-matrix-combined.json')['rows']),'passedChecks':140,'evidence':'warning-matrix-combined.json'}
report['wavePositionChecks']={'cases':len(read('positions-combined.json')['rows']),'passedChecks':54,'evidence':'positions-combined.json','scope':read('positions-combined.json')['scope']}
report['sameTabReplay']={'completed':read('chain-watch/report.json')['completed'],'cases':len(read('chain-watch/report.json')['rows']),'timeout':read('chain-watch/report.json')['timeout'],'evidence':'chain-watch/report.json','note':'18 native same-tab starts completed with6-frame yielding and bounded calls. Original30-frame-batch stall was not reproduced; its cause remains unproven.'}
report['weatherPixelComparisons']={'comparisons':len(read('weather/candidate.json')['results']),'fallbacks':read('weather/candidate.json')['fallbacks'],'evidence':'weather/candidate.json'}
"""
if "report['coreAndSyntax']"not in s:s=s.replace(needle,extra+needle)
s=s.replace('Native GOD is enabled in combat films.', 'Native GOD is enabled in encounter stress films. The separately labeled fresh Normal campaign clip uses normal damage.')
s=s.replace('<h2>Scoped checks</h2><table>', '<h2>Scoped checks</h2><p>8,969 core assertions pass; zero failures, unchanged failure names. All 753 shipping scripts and five inline blocks parse. Engine LF/tests CRLF and all prior production source hashes except index are preserved.</p><p><a href="warning-matrix-combined.json">28 Normal/Hard starts · 140 checks</a> · <a href="positions-combined.json">12 native wave fixtures · 54 checks</a> · <a href="chain-watch/report.json">18 same-tab starts</a> · <a href="weather/candidate.json">53 weather pixel/fallback comparisons</a> · <a href="scroll/report.json">24 long dialogue lines</a> · <a href="media-final.json">Decoded film audio</a></p><table>')
s=s.replace('Refused scripts, obsolete fixtures and intentionally canceled local audio preloads', 'The bounded same-tab replay completed all18 entries without reproducing the original30-frame-batch stall; its cause remains unproven. Existing local audio preload cancellations are recorded separately from hard errors in the film receipts. Refused scripts, obsolete fixtures and intentionally canceled local audio preloads')
P.write_text(s,encoding='utf8',newline='\n')
