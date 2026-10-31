from pathlib import Path
import subprocess,imageio_ffmpeg
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_09/boss/tidal_sovereign_1029/audio'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(D/'tidal_wave_master_1029.mp3'),'-af','highpass=f=70,alimiter=limit=0.89:level=false,afade=t=out:st=1.85:d=0.15','-ar','44100','-ac','2','-c:a','libmp3lame','-b:a','192k',str(D/'tidal_wave_rush_1029.mp3')],check=True)
