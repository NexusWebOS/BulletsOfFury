"""Natural first storm orb, GOD disabled on release; native exclusive player death."""
from pathlib import Path
import sys,json,subprocess
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text()
pilot="""if(cfg.deathDemo){const B=subBoss,A=reviewBot;for(const k of ['j','k','c','q','e'])Input.keys[k]=false;if(player.dead){for(const k of ['a','d','w','s'])Input.keys[k]=false;return;}const x=worldWidth()/2,y=VH*.76;Input.keys.a=player.x>x+5;Input.keys.d=player.x<x-5;Input.keys.w=player.y>y+5;Input.keys.s=player.y<y-5;if(B?._rw118?.state==='orb-flight'&&!A.orbUnlocked){DBGT.god=false;A.orbUnlocked=true;}return;}"""
insert="capture=capture.replace('video/webm;codecs=vp8,opus','video/mp4').replace('function aim(elapsed){','function aim(elapsed){'+"+repr(pilot)+")\n"
insert+='capture=capture.replace(\'cv.captureStream(30)\',\'cv.captureStream(0)\').replace(\'if(cfg.playfield){\',"if(cfg.playfield){const frame=Math.floor(elapsed*30);if(frame!==window.captureFrame118){window.captureFrame118=frame;window.reviewRecorder?.stream.getVideoTracks()[0]?.requestFrame();}")\n'
text=text.replace("paths=['index.html']",insert+"paths=['index.html']")
text=text.replace("rec.CONFIG={**job,","rec.CONFIG={'deathDemo':True,**job,")
text=text.replace("src=original.replace(","rec.SNAPSHOT=rec.SNAPSHOT.replace(\"bossDefeated:reviewConfig.role==='mini'?(subBossDone&&debugFight?.spawned):bossDefeated\",\"bossDefeated:!!player._rw118Death&&!!player._spin?.crashed\")\n src=original.replace(")
text=text.replace("src=src.replace(\"'-crf', '20'\"", "src=src.replace(\"q['seconds'] - completed_at > 7\",\"q['seconds'] - completed_at > .55\").replace(\"reason='native defeat'\",\"reason='native vortex crash'\")\n src=src.replace(\"'-crf', '20'\"")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-mini','--track','razorwake-vortex-final-1105','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
F=R/'_shots/boss_comparison_1102/razorwake-vortex-final-1105';batch=json.loads((F/'batch.json').read_text());job=batch['jobs']['stage6-mini'];folder=R/job['folder'];report=json.loads((folder/'report.json').read_text());report['method']=__doc__;report['invulnerable']='GOD during earlier attacks; disabled when the first natural wind orb releases';report['completed']=report['reason']=='native vortex crash';(folder/'report.json').write_text(json.dumps(report,indent=2))
movie=R/job['path'];clip=folder/'vortex-death.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss','51','-i',str(movie),'-c:v','libx264','-threads','2','-crf','21','-c:a','aac','-movflags','+faststart','-y',str(clip)],check=True);print('NATIVE_DEATH_CLIP',clip,flush=True)
