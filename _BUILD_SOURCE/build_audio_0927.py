"""Master authorized ElevenLabs cues with ColeForge's deterministic SFX engine."""
from pathlib import Path
import importlib.util,subprocess,json
import numpy as np
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/sfx_0927';QA=ROOT/'_shots/overnight_0927';QA.mkdir(exist_ok=True,parents=True)
spec=importlib.util.spec_from_file_location('coleforge',ROOT/'_SFXGenerator_upload/tools/build_bof_arcade_combat_pack.py')
cf=importlib.util.module_from_spec(spec);spec.loader.exec_module(cf)
ff=imageio_ffmpeg.get_ffmpeg_exe();SR=cf.SR
def decode(p):
 r=subprocess.run([ff,'-v','error','-i',str(p),'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True,check=True)
 return np.frombuffer(r.stdout,dtype='<f4').reshape(-1,2).astype(float)
def trim(x,maxdur):
 env=np.max(np.abs(x),axis=1);active=np.flatnonzero(env>max(.008,env.max()*.012))
 if len(active):x=x[max(0,active[0]-int(.006*SR)):min(len(x),active[-1]+int(.08*SR))]
 x=x[:int(maxdur*SR)].copy();n=min(len(x)//3,int(.08*SR));x[-n:]*=np.linspace(1,0,n)[:,None];return x
def render(name,x):
 x=cf.master(x,presence=.5,drive=1.02,bits=16);peak=np.max(np.abs(x));x*=.82/max(peak,1e-9)
 wav=QA/(name+'.wav');cf.write_wav16(wav,x)
 subprocess.run([ff,'-v','error','-y','-i',str(wav),'-c:a','libmp3lame','-b:a','160k',str(OUT/(name+'.mp3'))],check=True)
 return {'name':name,'seconds':round(len(x)/SR,3),'peak':round(float(np.max(np.abs(x))),4),'rms':round(float(np.sqrt(np.mean(x*x))),4),'clipped':int((np.abs(x)>=1).sum())}
report=[]
for i in [1,3]:
 x=trim(decode(OUT/f'missile_launch_take{i}.mp3'),.85)
 mech=cf.launcher(927+i,'missile');cf.place(x,mech,0,.22)
 report.append(render('missile_auto_'+str(i),x))
for name,limit in [('boss_charge',1.8),('hammer_slam',1.0),('stun',1.5),('beam',1.3),('toxic',1.2),('ice',1.1),('alien',1.8)]:
 x=trim(decode(OUT/(name+'_source.mp3')),limit)
 if name in ['hammer_slam','beam','toxic','ice']:cf.place(x,cf.impact(927,heavy=True),0,.15)
 report.append(render(name,x))
for name,x in [('cannon',cf.launcher(927,'grenade')),('module_break',cf.impact(932,True)),('energy_release',cf.charge_transition(927,'release',True)),('servo_charge',cf.charge_transition(929,'start',True)),('plasma_orb',cf.orb(927,'fire','shoot'))]:
 report.append(render(name,x))
(QA/'audio-masters.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
