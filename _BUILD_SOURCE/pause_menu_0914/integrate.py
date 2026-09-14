from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/pause_menu_0914/game.before.js';path=ROOT/'assets/game.js'
s=before.read_bytes().decode('utf-8')
def replace(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:100])
 s=s.replace(a,b,1)
def fn(name,body):
 global s
 a=s.index('\nfunction '+name+'(');b=s.index('\n}',a)+2;s=s[:a]+'\n'+body+s[b:]
replace('const COMBAT_WARNING_SECONDS=3.0;',(HERE/'engine.js').read_text(encoding='utf-8')+'\nconst COMBAT_WARNING_SECONDS=3.0;')
fn('_pausePresentation',"function _pausePresentation(on){\n try{for(const id of ['hud','equipcv']){const el=document.getElementById(id);if(el)el.style.filter=on?'grayscale(1) brightness(.82)':'';}const screen=document.getElementById('screen');if(screen)screen.style.filter='';}catch(_){}\n try{Audio.setMusicDuck(on?.28:1);Snd.setVol('music',Audio.getVol('music'));}catch(_){}\n}")
replace('  const _prevState=state;',"  const _prevState=state;\n  if(_prevState==='paused'&&playPause&&(playPause.mode==='options'||playPause.mode==='help')&&s===GS.TITLE){playPauseSubmenuReturn();return;}\n  if(s==='paused'&&_prevState!=='paused')playPauseBegin();")
replace("  if(s==='paused'&&_prevState!=='paused')_pausePresentation(true);\n  else if(_prevState==='paused'&&s!=='paused')_pausePresentation(false);\n  state=s; stateT=0;", "  state=s;\n  if(s==='paused'&&_prevState!=='paused')_pausePresentation(true);\n  else if(_prevState==='paused'&&s!=='paused')_pausePresentation(false);\n  stateT=0;")
replace("case 'paused':   drawWorld(0); return drawPaused();","case 'paused':   playPauseWorldDraw(); return drawPaused(dt);")
fn('drawPaused','function drawPaused(dt){playPauseDraw(dt);}')
replace('function drawGameOver(dt){','function drawGameOver(dt){\n  if(playPause&&playPause.exit){playPauseGameOverDraw(dt);return;}')
replace('let volMaster=0.8, volMusic=0.72, volSfx=0.74, muted=false;','let volMaster=0.8, volMusic=0.72, volSfx=0.74, muted=false, musicDuck=1;')
replace('if(kind===\'music\'){volMusic=v; if(musicGain)musicGain.gain.value=v;}',"if(kind==='music'){volMusic=v; if(musicGain)musicGain.gain.value=v*musicDuck;}")
replace('  function getVol(kind){', '  function setMusicDuck(v){musicDuck=v;if(musicGain)musicGain.gain.value=volMusic*musicDuck;}\n  function getVol(kind){')
replace('return {init,resume,SFX,startMusic,stopMusic,setVol,getVol,','return {init,resume,SFX,startMusic,stopMusic,setVol,setMusicDuck,getVol,')
# All live HTML music gains share the pause duck, including warp echoes.
for old in ['A.vol.music*A.vol.master*A.warpMix','A.vol.music*A.vol.master']:
 s=s.replace(old,old+'*pauseMusicDuck()') if old.endswith('warpMix')else s
s=s.replace('c01(A.vol.music*A.vol.master);','c01(A.vol.music*A.vol.master*pauseMusicDuck());')
s=s.replace('musicGain.gain.value=volMusic; musicGain.connect(master);','musicGain.gain.value=volMusic*musicDuck; musicGain.connect(master);')
fn('campCanContinue',"function campCanContinue(){\n if(campSession)return true;\n try{const name=localStorage.getItem('bof_autosave_latest');if(!/^Autosav0[123][.]json$/.test(name||''))return false;const data=JSON.parse(localStorage.getItem(name)||'null');if(data&&data.v===CAMP_SAVE_VER&&data.mode==='campaign'){campSession=data;return true;}}catch(_){}\n return false;\n}")
# Preserve new autosaves when the controls reset keeps existing manual saves.
replace("  let mist=null;try{mist=localStorage.getItem(LASER_MIST_UNLOCK_KEY);}catch(e){}", "  const autoKeys=['Autosav01.json','Autosav02.json','Autosav03.json','bof_autosave_latest','bof_autosave_next'];const autos=autoKeys.map(k=>{try{return localStorage.getItem(k);}catch(_){return null;}});\n  let mist=null;try{mist=localStorage.getItem(LASER_MIST_UNLOCK_KEY);}catch(e){}")
replace("  if(mist!=null)try{localStorage.setItem(LASER_MIST_UNLOCK_KEY,mist);}catch(e){}", "  autoKeys.forEach((k,i)=>{if(autos[i]!=null)try{localStorage.setItem(k,autos[i]);}catch(_){}});\n  if(mist!=null)try{localStorage.setItem(LASER_MIST_UNLOCK_KEY,mist);}catch(e){}")
expected=s.encode('utf-8');out=ROOT/'_shots/pause_menu_0914/game.expected.js'if '--dry-run'in sys.argv else path
if out==path and path.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent edits present')
out.write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
