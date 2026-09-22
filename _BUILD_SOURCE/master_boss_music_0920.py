"""Bring the two quiet boss masters up without modifying Mike's originals."""
from pathlib import Path
import subprocess
import imageio_ffmpeg

root=Path(__file__).resolve().parents[1]
music=root/'assets/game/music'
ff=imageio_ffmpeg.get_ffmpeg_exe()
for src,dst,boost in [
    ('boss2_bossfight3.mp3','boss2_bossfight3_loud_0920.mp3',2.0),
    ('boss4_cowboyfromhell.mp3','boss4_cowboyfromhell_loud_0920.mp3',2.5),
]:
    subprocess.run([ff,'-y','-v','error','-i',str(music/src),
                    '-af',f'volume={boost}dB,alimiter=limit=0.98:level=0',
                    '-codec:a','libmp3lame','-q:a','4',str(music/dst)],check=True)
    print(dst)
