"""Refresh twelve local guide cards. Original media and the complete reel stay
archived; no Git/GitHub publication. --install updates the local server whitelist.
"""
from pathlib import Path
import json,sys,re,subprocess,hashlib,math
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage1_followup_1031';V=W/'video';D=Path('D:/BOF-Downloads/2026-10-31');H=D/'hub';ff=imageio_ffmpeg.get_ffmpeg_exe()
mapping={'stage1-s1jetdelta-2':'s1jetdelta','stage1-s1boatpatrol':'s1boatpatrol','stage1-s1corvette':'s1corvette','stage1-s1jetbomber':'s1jetbomber','stage1-s1tankheavy':'s1tankheavy','stage1-s1tankapc':'s1tankapc','stage1-s1tanklight':'s1tanklight','stage1-s1jetdelta-b':'s1jetdelta_b','stage1-s1truckmissile':'s1truckmissile','stage1-modturret':'modturret-missile','stage1-modturret-2':'modturret-mg','stage1-s1jetdelta-b-2':'s1jetdelta_b_kamikaze'}
data=json.loads((R/'_shots/stage1_amplify_1031/guide-manifest-current.json').read_text(encoding='utf-8'));files={};receipt=[]
def local(s):return s.replace('https://github.com/NexusWebOS/BulletsOfFury/releases/download/','/_releases/').replace('https://nexuswebos.github.io/BulletsOfFury/','/')
for item in data['items']:
 if item['id']not in mapping:continue
 name=mapping[item['id']];folder=V/name;report=json.loads((folder/'report.json').read_text());movie=folder/'preview.mp4';assert movie.is_file();T=report['timeline'];S=report['stats']
 assert not report['errors']and not S['tapErrors']and not S['botErrors'],name
 assert not any(q['playerDead']or q['state']!='play'for q in T),name+' observer left native combat'
 assert all(all(t==('modturret'if name.startswith('modturret')else name.replace('_kamikaze',''))for t in q['actors'])for q in T),name+' unrelated wave'
 attack=T[-1]['bombs']if name=='s1jetbomber'else T[-1]['shots'];assert attack>0 or name.endswith('_kamikaze')and max(q['y']for q in T)>400,name+' attack was not recorded'
 assert name!='s1tankheavy'or T[-1]['pairs']>=2
 f=ff;decode=subprocess.run([f,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
 reader=imageio_ffmpeg.read_frames(str(movie));meta=next(reader);reader.close();duration=meta['duration']
 candidates=[q for q in T if not q['dead']and (q['shots']or q['bombs']or q['pairs'])and q['seconds']<duration-.2]
 if name.startswith('s1jetdelta'):
  c=[q for q in T if not q['dead']and q.get('heading')not in (0,None)and 60<q['x']<620 and q['y']<420];q=max(c,key=lambda q:abs(math.atan2(math.sin(q['angle']-math.pi/2),math.cos(q['angle']-math.pi/2))))if c else T[len(T)//2]
 else:q=candidates[min(2,len(candidates)-1)]if candidates else T[len(T)//2]
 poster=folder/'poster.jpg';subprocess.run([ff,'-y','-ss',str(min(duration-.1,q['seconds']+.1)),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/stage1-physical-'+name;files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve())
 item.setdefault('previousVideo',item['video']);item.setdefault('previousPoster',item['poster']);item.update(video=route+'.mp4',poster=route+'.jpg',duration=duration,fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1),attackEvents=attack,hitFrames=sum(z['hp']<a['hp']for a,z in zip(T,T[1:])),audioCues=len(S['playing']),maxHP=report['setup']['hp'],sound=True,errors=[],outcome='Destroyed'if T[-1]['hp']<=0 else'Exited screen'if T[-1]['dead']else'Combat sample',source='October31 physical weapons and camo pass; isolated native sortie; invulnerable input-only observer')
 if name=='s1tanklight':item['title']='Light Jungle Tank / Black Camo';item['difficultyRule']='Hard and Furious only'
 receipt.append(dict(id=item['id'],type=name,duration=duration,attacks=attack,pairs=T[-1]['pairs'],fps=item['fps'],sourceHashes=report['sourceHashes'],movieSha256=hashlib.sha256(movie.read_bytes()).hexdigest(),decoded=True,audio=S['playing']))
data['seconds']=round(sum(i['duration']for i in data['items']),2);manifest=W/'guide-manifest-current.json';manifest.write_text(local(json.dumps(data,indent=2,ensure_ascii=False))+'\n',encoding='utf-8')
html=local((H/'enemy-showcase-1031.html').read_text(encoding='utf-8'))
banner='<p style="padding:12px 18px;border:1px solid #477d8c;background:#102a36;color:#d5faff"><strong>October31 weapon alignment:</strong> Current Stage1 previews show physical twin weapons, three-turret Patrol attacks, straight Corvette fire, crimson/silver bombs, turning Strike Fighters and the rapid Black Camo tank (Hard/Furious only). The original complete reel remains an archive.</p>'
html,n=re.subn(r'(<h1[^>]*>.*?</h1>)',lambda m:m.group(1)+banner,html,count=1,flags=re.S);assert n==1
page=W/'enemy-showcase-current.html';page.write_text(html,encoding='utf-8');files['/enemy-showcase-1031.html']=str(page.resolve());files['/enemy-showcase-1031/manifest.json']=str(manifest.resolve());(W/'guide-update.json').write_text(json.dumps(dict(cards=receipt,files=files),indent=2))
if '--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed local guide updates for',len(receipt),'cards')
else:print('Prepared local guide updates for',len(receipt),'cards; use --install after review')
