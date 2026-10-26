# Chronos portraits, taunts, blue recovery and audio

Pilot radio now requests each pilot portrait; Decker retains native gold tint #ffd24a. Chronos lines render beside the boss through curFontArt/stageText, the same authored font owner used by STYLISH. Chronos no longer gets the C34 dialogue box.

Armor break uses c25_empty: standing-to-death-pose, stun hold, then the same authored bank reversed to stand and recall. The remaining C29 stun/recall and C25/BI24 regular armor accents receive the blue correction; hit-white and permanent red variants remain separate.

The outer damage owner absorbs shield contacts before chromium armor can lose HP. Raised-hammer missile counter remains owned by the existing charging mechanic, separate from the shield.

New ElevenLabs effects: smash (1 second) and hammercharge (2 seconds), source archive _ART_SOURCES/chronos_voice_1025, compiled through build_chronos_storm_audio_1025.py. Existing ElevenLabs rage, wave, palm, charge and thunder routes retained. All use C33 shared mixer pools, retrigger gates and owner cancellation. Seven files decode successfully with nonzero samples.

Focused native Chromium checks7/7, screenshots inspected: portraits, stylish side text, absorbing shield with unchanged armor/body HP, death-pose recovery and blue stun. No page/console errors. Syntax checks pass. test_fl exits1 before assertions/final summary due missing retired_art_archive_1022.cjs, the recorded existing blocker. No commit/push.

Final capture: 272 seconds, opening dialogue through defeat, all seven cues played (smash24, hammercharge5), no browser/game errors, delivery8/8. Preview revision portraits-blue-audio-1025.
