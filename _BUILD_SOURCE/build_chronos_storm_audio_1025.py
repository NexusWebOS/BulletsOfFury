"""Compile the five archived ElevenLabs recordings to native attack durations."""
from pathlib import Path
import subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1]
source=R/'_ART_SOURCES/chronos_storm_1025'
out=R/'assets/game/shared/combat/chronos_storm_1025'
out.mkdir(parents=True,exist_ok=True)
filters={
 'rage':'atempo=0.5,atempo=0.833333,afade=t=out:st=4.4:d=0.4',
 'wave':'afade=t=out:st=1.35:d=0.25,atrim=duration=1.6',
 'palm':'atrim=duration=0.32,afade=t=out:st=0.20:d=0.12',
 'charge':'atempo=0.5,atempo=0.565,afade=t=out:st=1.5:d=0.2',
 'thunder':'afade=t=out:st=0.65:d=0.35',
 'smash':'anull',
 'hammercharge':'anull'}
for name,fx in filters.items():
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str((R/'_ART_SOURCES/chronos_voice_1025' if name in ['smash','hammercharge'] else source)/(name+'.mp3')),'-af',fx+',alimiter=limit=0.85','-c:a','libmp3lame','-b:a','160k',str(out/(name+'.mp3'))],check=True)
