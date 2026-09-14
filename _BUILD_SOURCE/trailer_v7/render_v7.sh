#!/bin/sh
# v7 render: the game's own audio for every re-recorded take, then the edit, video, mix, checks, master, phone copy, pages.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
IDS="S1_axel S1_falva S1_maverick S2_falva C_icebreath C_fireorb C_shotgun D_s2 D2_s2 E_s2 E2_s2 G_death2 \
E3_s2_form E3_s2_arms E3_s2_core E3_s2_head \
C2_spread D_s5 D2_s5 E_s5 E2_s5 F_intro_s5 F_s5 S1_freezer S2_cole S2_juggernaut W_warp C_lasercannon C_shadoworb X_launch5 \
S1_juggernaut J_charge C_lasermist C_thermo C_missiles C_sonic L_rack T_tempest"
python render_audio.py $IDS --force > render_audio_v7.log 2>&1; echo "--- render_audio: $(grep -c ' audio ' render_audio_v7.log) takes"; grep -i -E "error|missing|traceback" render_audio_v7.log | head -5
python edit3.py > edit3_v7.log 2>&1; echo "--- edit3:"; tail -22 edit3_v7.log
python check_warn_pick.py
python compose.py edl3.json trailer_v3_video.mp4 --workers 8 > compose3.log 2>&1 && tail -1 compose3.log
python mix3.py edl3.json mix3.wav > mix3.log 2>&1; tail -5 mix3.log
python mixcheck3.py edl3.json mix3.wav > mixcheck3.log 2>&1; tail -20 mixcheck3.log
python mix3.py mux trailer_v3_video.mp4 mix3.wav trailer_v3.mp4 && python phone3.py trailer_v3.mp4 trailer_v3_phone.mp4 && python stills3.py trailer_v3.mp4 edl3.json trailer_v3_stills.jpg && python stills3.py trailer_v3.mp4 edl3.json trailer_v3_pilots.jpg --pilots
ls -la trailer_v3.mp4 trailer_v3_phone.mp4 | awk '{print $5, $9}'
