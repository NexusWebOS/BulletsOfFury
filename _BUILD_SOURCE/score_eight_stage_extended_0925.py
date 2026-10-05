"""Use the current field and boss themes in the extended eight-stage review."""
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
folder = root / '_shots/eight_stage_review_0925'
source = folder / 'BulletsOfFury_Stages1-8_Review_0925_extended.mp4'
target = folder / 'BulletsOfFury_Stages1-8_Review_0925_extended_with_music.mp4'
log = json.loads((folder / 'review_log_extended.json').read_text())
themes = [
    ('Level1.mp3', 'Level1b.mp3'),
    ('Level2.mp3', 'Level2b.mp3'),
    ('Level3.mp3', 'Level3b.mp3'),
    ('Level4.mp3', 'Level4b.mp3'),
    ('Level5.mp3', 'Level5mb.mp3'),
    ('Level6.mp3', 'Level6b.mp3'),
    ('Level7.mp3', 'boss7.mp3'),
    ('Unused_Egypt.mp3', 'Level8b.mp3'),
]
assert source.is_file() and len(log) == 8
segments = []
for row, pair in zip(log, themes):
    for role, name in zip(('field', 'boss'), pair):
        path = root / 'assets/game/music' / name
        assert path.is_file(), path
        segments.append((path, row[role + 'Frames'] / 10))

cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', str(source)]
for path, _ in segments:
    cmd += ['-i', str(path)]
filters = []
for i, (_, duration) in enumerate(segments):
    fade = min(.35, duration * .08)
    filters.append(f'[{i+1}:a]aresample=44100,atrim=0:{duration:.3f},asetpts=PTS-STARTPTS,'
                   f'afade=t=in:st=0:d={fade:.3f},'
                   f'afade=t=out:st={duration-fade:.3f}:d={fade:.3f},volume=0.37[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(len(segments)))+
               f'concat=n={len(segments)}:v=0:a=1[music]')
cmd += ['-filter_complex', ';'.join(filters), '-map', '0:v:0', '-map', '[music]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest',
        '-movflags', '+faststart', str(target)]
subprocess.run(cmd, check=True)
print(target, target.stat().st_size)
