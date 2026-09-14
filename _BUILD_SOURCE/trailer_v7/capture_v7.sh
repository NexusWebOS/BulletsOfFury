#!/bin/sh
# v7 re-record pass: stage-2 takes (every hit flashes, the Furnace included), stage-5 takes (the spaceship everywhere in
# space), Juggernaut's special takes (anchored balls, a visible ram), and every new or re-specified showcase take.
cd "$(dirname "$0")"
PYTHONIOENCODING=utf-8 python capture3.py \
  S1_axel S1_falva S1_maverick S2_falva C_icebreath C_fireorb C_shotgun D_s2 D2_s2 E_s2 E2_s2 G_death2 \
  E3_s2_form E3_s2_arms E3_s2_core E3_s2_head \
  C2_spread D_s5 D2_s5 E_s5 E2_s5 F_intro_s5 F_s5 S1_freezer S2_cole S2_juggernaut W_warp C_lasercannon C_shadoworb X_launch5 \
  S1_juggernaut J_charge \
  C_lasermist C_thermo C_missiles C_sonic L_rack T_tempest \
  --workers 3 > capture_v7.log 2>&1
