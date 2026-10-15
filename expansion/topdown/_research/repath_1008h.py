"""1008h: follow 12dc7982 "Organize game assets", which moved assets/game/* into per-pilot / per-stage /
shared folders. Only hard-coded paths needed this; keys resolved through the manifest moved with it.
Unused_UnknownBossTheme.mp3 went to the local-only archive on 1007 (2d5b72b9), so the boss plays
Unused11 (an old stage-2 boss mix nothing else uses). Life Up is the current winged plate (0915).
Safe to re-run.
"""
import os
HERE = os.path.join(os.path.dirname(__file__), '..')
MAP = {
    'js/art.js': [
        ("'assets/game/bosses/razorback/rzb_'", "'assets/game/levels/stage_01/miniboss/bosses/razorback/rzb_'"),
        ("'assets/game/pilots_0922/portraits/' + p + '-idle.png'", "'assets/game/pilots/' + p + '/portraits/pilots_0922/portraits/' + p + '-idle.png'"),
        ("'assets/game/ui/debrief_0916/rankplate_'", "'assets/game/shared/ui/ui/debrief_0916/rankplate_'"),
        ("'assets/game/ui/logo_0916/bof_logo.png'", "'assets/game/shared/ui/ui/logo_0916/bof_logo.png'"),
        ("'assets/game/ui/pickups_0915/life_up.png'", "'assets/game/shared/ui/ui/pickups_0915/life_up_wings.png'"),
        ("'assets/game/ui/pickups_0917b/", "'assets/game/shared/ui/ui/pickups_0917b/"),
    ],
    'js/core.js': [
        ("'assets/game/music/Unused_UnknownBossTheme.mp3'", "'assets/game/shared/audio/music/Unused11.mp3'"),
        ("'assets/game/music/", "'assets/game/shared/audio/music/"),
        ("'assets/game/sounds/'", "'assets/game/shared/audio/sounds/'"),
    ],
    'index.html': [
        ("../../assets/game/fonts/command_0914/", "../../assets/game/shared/fonts/fonts/command_0914/"),
        ("V = '1008g'", "V = '1008h'"),
    ],
}
for f, pairs in MAP.items():
    p = os.path.join(HERE, f); s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        if old in s: s = s.replace(old, new)
        else: assert new in s, (f, old)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('repathed', f)
