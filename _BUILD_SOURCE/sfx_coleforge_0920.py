"""Build compact arcade cues by layering the project's authored ColeForge recordings.

ElevenLabs generation remains in sfx_gen.py; this offline bank needs no API key.
The source recordings are kept intact. Outputs are mono MP3 runtime assets.
"""
from pathlib import Path
import json
import math
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / 'assets/game/sounds'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100

# filename, target duration, (source, gain, start seconds, playback-rate) layers
RECIPES = {
    'cf_combo_fire_0920': (.31, [('enemy_flame_bolt.mp3', .72, 0, .91), ('explosion_air_small_01.mp3', .29, .025, 1.31)]),
    'cf_combo_ice_0920': (.30, [('enemy_ice_bolt.mp3', .70, 0, 1.17), ('explosion_ice_burst.mp3', .29, .02, 1.58)]),
    'cf_combo_lightning_0920': (.29, [('enemy_electric_bolt.mp3', .72, 0, 1.17), ('explosion_electrical.mp3', .24, .02, 1.72)]),
    'cf_combo_prism_0920': (.34, [('reviewed_enemy_laser.mp3', .61, 0, 1.36), ('shield_graze.mp3', .28, .035, 1.21)]),
    'cf_combo_toxic_0920': (.38, [('enemyToxicSpit.mp3', .63, 0, .82), ('explosion_plasma.mp3', .20, .05, 1.63)]),
    'cf_combo_kinetic_0920': (.28, [('cole_pressure_impact_0913.mp3', .76, 0, 1.07), ('debris_scatter_metal.mp3', .18, .025, 1.84)]),
    'cf_combo_chrome_0920': (.34, [('projectile_ricochet.mp3', .65, 0, .88), ('shield_hit_heavy.mp3', .31, .019, 1.31)]),
    'cf_combo_water_0920': (.35, [('ice_breath_release.mp3', .64, 0, .84), ('shield_graze.mp3', .22, .055, .77)]),
    'cf_combo_dark_0920': (.39, [('reviewed_shadow_orb_impact.mp3', .65, 0, .86), ('enemy_pulse_laser_alien.mp3', .24, .015, .67)]),
    'cf_combo_thermoshock_0920': (.38, [('enemy_flame_bolt.mp3', .49, 0, 1.12), ('explosion_ice_burst.mp3', .48, .025, 1.41)]),
    'cf_fire_wave_0920': (.80, [('firewall_arrive.mp3', .67, 0, 1.20), ('flamethrower_release.mp3', .32, .055, .86)]),
    'cf_fire_burst_0920': (.44, [('explosion_fuel_air.mp3', .60, 0, 1.46), ('enemy_flame_bolt.mp3', .32, .012, .96)]),
    'cf_fire_geyser_0920': (.91, [('s2_geyser_erupt_0918.mp3', .62, 0, 1.18), ('flamethrower_ignite.mp3', .30, .018, 1.31)]),
    'cf_shield_destroy_0920': (.55, [('shield_break.mp3', .65, 0, 1.10), ('explosion_electrical.mp3', .30, .018, 1.20)]),
    'cf_boss_razorback_0920': (.54, [('cole_sonic_full.mp3', .63, 0, .85), ('explosion_tank_cookoff.mp3', .25, .04, 1.58)]),
    'cf_boss_overlord_0920': (.50, [('reviewed_enemy_laser.mp3', .54, 0, .77), ('nsp_rocket_launch.mp3', .33, .01, 1.26)]),
    'cf_boss_warden_0920': (.58, [('enemy_heavy_laser.mp3', .57, 0, .83), ('explosion_electrical.mp3', .31, .03, .74)]),
    'cf_enemy_flame_0920': (.26, [('enemy_flame_bolt.mp3', .72, 0, 1.38), ('flamethrower_ignite.mp3', .17, .008, 1.65)]),
    'cf_enemy_ice_0920': (.26, [('enemy_ice_bolt.mp3', .74, 0, 1.38), ('shield_graze.mp3', .15, .009, 1.70)]),
    'cf_enemy_electric_0920': (.25, [('enemy_electric_bolt.mp3', .73, 0, 1.37), ('projectile_ricochet.mp3', .17, .009, 1.57)]),
}

cache = {}

def source(name):
    if name not in cache:
        path = BANK / name
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = subprocess.check_output([FFMPEG, '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'])
        a = np.frombuffer(raw, dtype='<f4').copy()
        if not len(a):
            raise ValueError(path)
        env = np.convolve(np.abs(a), np.ones(128)/128, mode='same')
        nz = np.flatnonzero(env > max(.002, env.max()*.013))
        if len(nz):
            a = a[max(0, int(nz[0])-int(.004*SR)):]
        cache[name] = a / max(.05, float(np.max(np.abs(a))))
    return cache[name]

def render(name, spec):
    dur, layers = spec
    n = int(dur*SR)
    out = np.zeros(n, dtype=np.float64)
    for filename, gain, offset, rate in layers:
        src = source(filename)
        end = min(len(src)-1, int((n-offset*SR)*rate))
        if end <= 0:
            continue
        samples = np.interp(np.arange(0, end, rate), np.arange(len(src)), src)
        start = int(offset*SR)
        length = min(len(samples), n-start)
        out[start:start+length] += samples[:length]*gain
    # These source swells carry their strongest attack later than an arcade
    # impact allows. Cut to the strike; preserve the requested cue duration.
    lead_cut = {'cf_combo_toxic_0920':.22, 'cf_combo_water_0920':.07,
                'cf_fire_wave_0920':.24, 'cf_fire_burst_0920':.25}.get(name,0)
    if lead_cut:
        skip = int(lead_cut*SR)
        out = np.pad(out[skip:],(0,skip))
    # The ColeForge arcade finish: hard attack and a short dry tail. Sources are
    # already mastered and band-limited; avoid a second filter dulling the shot.
    out -= out.mean()
    fade = min(int(.028*SR), n//5)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:max(1,int(.002*SR))] *= np.linspace(0, 1, max(1,int(.002*SR)))
    out *= .78/max(.01, float(np.max(np.abs(out))))
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as t:
        wav = Path(t.name)
    try:
        import wave
        with wave.open(str(wav), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.asarray(out*32767, dtype='<i2').tobytes())
        dst = BANK / (name+'.mp3')
        subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', str(wav), '-ac', '1', '-ar', str(SR), '-codec:a', 'libmp3lame', '-q:a', '4', str(dst)], check=True)
    finally:
        wav.unlink(missing_ok=True)
    env = np.convolve(np.abs(out), np.ones(256)/256, mode='same')
    peak_at = float(np.argmax(env)/SR)
    return {'file': str(dst.relative_to(ROOT)).replace('\\','/'), 'seconds':dur,
            'peak':round(float(np.max(np.abs(out))),3), 'rms':round(float(np.sqrt(np.mean(out*out))),3),
            'peak_at':round(peak_at,3), 'sources':[row[0] for row in layers]}

if __name__ == '__main__':
    report = {name:render(name,spec) for name,spec in RECIPES.items()}
    (ROOT/'docs/qa/coleforge_sfx_0920.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"Built {len(report)} distinct cues; "+', '.join(f'{k}:{v["peak_at"]:.2f}s' for k,v in report.items()))
