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
    ('stage1_rumble_in_the_jungle.mp3', 'boss1_helicopterboss.mp3'),
    ('stage2_its_hot_in_here.mp3', 'boss2_bossfight3_loud_0920.mp3'),
    ('stage3_ice_still_cant_see.mp3', 'boss3_pandemonium.mp3'),
    ('stage4_crouching_missiles.mp3', 'boss4_cowboyfromhell_loud_0920.mp3'),
    ('lvl3-alt.mp3', 'boss5_deadly_night.mp3'),
    ('stage6_city_in_the_sky.mp3', 'boss6_battle_in_the_sky.mp3'),
    ('stage7_over_the_horizon_0925.mp3', 'boss7.mp3'),
    ('stage5_egypt.mp3', 'final_boss_phase1_0925.mp3'),
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
