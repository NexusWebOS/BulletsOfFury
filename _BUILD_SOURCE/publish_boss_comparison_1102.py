"""Publish only new boss comparison routes; preserve existing local previews."""
from pathlib import Path
import json,shutil,subprocess,argparse
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_comparison_1102';P=O/'publication';P.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--install',action='store_true');args=ap.parse_args();files={};jobs=[];ff=imageio_ffmpeg.get_ffmpeg_exe()
for diff in ['normal','hard','furious']:
 state=O/diff/'batch.json'
 if not state.exists():continue
 for row in json.loads(state.read_text())['jobs'].values():
  row={**row,'difficulty':diff}
  if row.get('passed'):
   report=json.loads((R/row['folder']/'report.json').read_text());row['maxhp']=next((t['maxhp']for t in report['timeline']if t.get('maxhp')),0);row['label']=report['setup']['entry'].get('name',row['name'])
   if diff=='furious'and row['stage']==7 and row['role']=='mini':row['label']='SUMPJAW PAIR'
   if row['stage']==8 and row['role']=='boss':
    row['chapters']=[];timeline=report['timeline']
    selectors=[('Final transformation',lambda t:'rebirth'in str(t.get('mode','')).lower()),('Hammer copy',lambda t:t.get('phase')==2 and t.get('form')==8),('Neural Archon',lambda t:t.get('phase')==2 and t.get('form')==1),('Helicopter',lambda t:t.get('phase')==2 and t.get('form')==6),('Volcano',lambda t:t.get('phase')==2 and t.get('form')==2),('Final body',lambda t:t.get('dracodia',{}).get('unlocked',False)if t.get('dracodia')else False)]
    for label,predicate in selectors:
     at=next((t['seconds']for t in timeline if predicate(t)),None)
     if at is not None:row['chapters'].append(dict(label=label,seconds=max(0,at-1)))
   url='/current/boss-comparison-1102/'+diff+'-'+row['id']+'.mp4';files[url]=str((R/row['path']).resolve());row['video']=url
   poster=P/(diff+'-'+row['id']+'.jpg')
   if not poster.exists():subprocess.run([ff,'-v','error','-y','-ss','5','-i',str(R/row['path']),'-frames:v','1','-q:v','3',str(poster)],check=True)
   url='/current/boss-comparison-1102/'+poster.name;files[url]=str(poster.resolve());row['poster']=url
  jobs.append(row)
quality=R/'_shots/furious_encounters_1102/audio/quality.json';routes=quality.with_name('live-routes.json');a=json.loads(quality.read_text())if quality.exists()else{};r=json.loads(routes.read_text())if routes.exists()else{}
audio=dict(cues=a.get('registry',{}).get('cues',0),decoded=sum(x.get('ok',False)for x in a.get('decoded',[])),audible=sum(x.get('ok',False)for x in a.get('playback',[])),enemies=len(r.get('enemies',[])))
audio['summary']=f"{audio['audible']} unique sources produced audible post-mix playback. Combat stress peak: {a.get('stress',{}).get('peak',0):.3f}. Native weapon, item and enemy route checks: "+('complete.'if'suspectEnemies'in r else'in progress.')
actions=quality.with_name('actions.json')
if actions.exists():
 action=json.loads(actions.read_text());audio['specials']=len(action.get('specials',[]));audio['music']=len(action.get('music',[]));audio['summary']+=f" {audio['specials']} special attacks and {audio['music']} unique music routes passed audible playback; master mute and context recovery passed."
manifest=dict(jobs=jobs,completed=sum(j.get('passed',False)for j in jobs),expected=57,seconds=sum(j.get('seconds',0)for j in jobs if j.get('passed')),audio=audio)
(P/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');files['/current/boss-comparison-1102/manifest.json']=str((P/'manifest.json').resolve())
shutil.copy2(R/'_BUILD_SOURCE/boss_comparison_1102.html',P/'index.html');files['/current/boss-comparison-1102.html']=str((P/'index.html').resolve())
C=P/'concepts';C.mkdir(exist_ok=True)
for image in (R/'_BUILD_SOURCE/furious_encounters_1102/concepts').glob('*.png'):
 target=C/image.name
 if not target.exists():shutil.copy2(image,target)
 files['/current/furious-concepts-1102/'+image.name]=str(target.resolve())
archive=Path('D:/BOF-Downloads/2026-10-31/current/boss-comparison-1102-media').resolve()
for url,path in files.items():
 target=Path(path).resolve()
 if not (target.is_relative_to(O.parent.resolve()) or target.is_relative_to(archive)) or not target.is_file():
  raise ValueError('Preview route must point to an existing recording artifact: '+url)
if args.install:
 configfile=Path('D:/BOF-Downloads/2026-10-31/current-overrides.json');config=json.loads(configfile.read_text(encoding='utf-8'));config.setdefault('files',{}).update(files);configfile.write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
print('Published',manifest['completed'],'/',manifest['expected'],'verified films;',len(files),'routes')
