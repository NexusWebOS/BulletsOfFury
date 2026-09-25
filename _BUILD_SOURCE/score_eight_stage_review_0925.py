#!/usr/bin/env python3
"""Lay each stage's own music under its six-second review segment."""
from pathlib import Path
import subprocess
import imageio_ffmpeg

root=Path(__file__).resolve().parents[1]
folder=root/'_shots/eight_stage_review_0925'
source=folder/'BulletsOfFury_Stages1-8_Review_0925.mp4'
target=folder/'BulletsOfFury_Stages1-8_Review_0925_with_music.mp4'
tracks=[
    'stage1_rumble_in_the_jungle.mp3',
    'stage2_its_hot_in_here.mp3',
    'stage3_ice_still_cant_see.mp3',
    'stage4_crouching_missiles.mp3',
    'lvl3-alt.mp3',
    'stage6_city_in_the_sky.mp3',
    'stage7_over_the_horizon_0925.mp3',
    'stage5_egypt.mp3',
]
paths=[root/'assets/game/music'/x for x in tracks]
assert source.is_file() and all(p.is_file() for p in paths)
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',str(source)]
for p in paths:cmd+=['-i',str(p)]
filters=[]
for i in range(8):
    filters.append(f'[{i+1}:a]aresample=44100,atrim=0:6,asetpts=PTS-STARTPTS,'
                   f'afade=t=in:st=0:d=0.2,afade=t=out:st=5.7:d=0.3,volume=0.38[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(8))+'concat=n=8:v=0:a=1[music]')
cmd+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[music]',
      '-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(target)]
subprocess.run(cmd,check=True)
print(target,target.stat().st_size)
