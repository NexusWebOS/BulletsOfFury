"""Import Mike's approved ColeForge chip cues into the standalone expansion.

The external library remains read-only. Existing MP3s are copied verbatim;
firewall duration variants are derived from its WAV with pitch-preserving atempo.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/audio/chip_1011'
DEFAULT = Path(r'C:\Users\Mdogg\Desktop\Master Coding Files\ColeForge SFX Generator\Sound Libraries\BOF_Chip_Library_1011')
APPROVED = '''error enemyDie alert shieldBreak forgeComplete bombDrop forgeWeld
weaponFound loadoutSelect loadoutEquip loadoutLaunch element_lightning_hit
geyserLightning stylishDodge furiousCoin achievement timedBombBeep timedBombBlast
chargeDash enemyLaser missileLaunch nuclearLaunch bossCannon railCannon impactMetal
firewallLaunch missileHit bombDropLegacy extraLife playerDeath decker_shell
enemyHeavyLaser quadFire furnaceLaserBurst hammerEradBlast shieldHitLight laserBeamHit
shieldImpact shieldImpactHeavy shieldDeflect blocked slice douse freeze lockon expBoss
expIce enemyLightningChaingun gravityShoot gravitySnap gravityLock gravityScatter
gravityChargeBand shadowCharge shadowRelease laserMistUnlock furyPartArrival
bossShieldTeleport bossShieldStatic'''.split()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tuning(key, group):
    gain, gate = .38, .09
    if group == 'FORGE / LOADOUT': gain, gate = .42, .075
    if group == 'ARCADE / SCORE': gain, gate = .45, .18
    if 'shield' in key.lower() or key in ('impactMetal', 'laserBeamHit', 'element_lightning_hit'):
        gain, gate = .3, .065
    return {
        'error': (.38, .35), 'enemyDie': (.48, .1), 'alert': (.48, 1.2),
        'playerDeath': (.65, .8), 'expBoss': (.7, 1.8), 'chargeDash': (.42, .3),
        'gd_tankEngineLoop': (.08, 0), 'gd_tankTreadLoop': (.2, 0),
        'gd_turretTraverse': (.17, 0), 'gd_alarmLoop': (.25, 0),
        'bossShieldStatic': (.18, 0), 'gd_tankCannon': (.62, .1),
        'bossCannon': (.52, .1), 'railCannon': (.62, .13),
        'gd_soldierRifle': (.38, .055), 'gd_soldierDown': (.42, .16),
        'gd_footstepA': (.24, .08), 'gd_footstepB': (.24, .08),
        'gd_wallBreak': (.52, .09), 'gd_buildingCollapse': (.55, .35),
        'gd_crateBreak': (.4, .08), 'gd_shellImpact': (.5, .08),
        'gd_spotted': (.5, .65), 'enemyHeavyLaser': (.43, .12),
        'missileLaunch': (.5, .1), 'missileHit': (.5, .08),
        'quadFire': (.42, .08), 'firewallLaunch': (.5, .25),
    }.get(key, (gain, gate))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=Path, default=DEFAULT)
    args = parser.parse_args()
    library = args.library.resolve()
    rows = [r for r in json.loads((library / 'library.json').read_text(encoding='utf-8')) if r['kind'] == 'bof']
    keys = {r['key'].removeprefix('chip_') for r in rows}
    assert set(APPROVED) <= keys, 'An explicitly approved source cue is missing'
    boundary = next(i for i, r in enumerate(rows) if r['key'] == 'chip_gd_shellImpact')
    allowed = set(APPROVED) | {r['key'].removeprefix('chip_') for r in rows if r['key'].startswith(('chip_scoreBullet', 'chip_gd_'))}
    allowed |= {r['key'].removeprefix('chip_') for r in rows[boundary:]}
    OUT.mkdir(parents=True, exist_ok=True)
    cues = {}
    for index, row in enumerate(rows):
        key = row['key'].removeprefix('chip_')
        if key not in allowed: continue
        source = library / row['dir'] / row['file']
        mp3, wav, recipe = [source.with_suffix(suffix) for suffix in ('.mp3', '.wav', '.recipe.json')]
        gain, gate = tuning(key, row['group'])
        destination = OUT / mp3.name
        shutil.copyfile(mp3, destination)
        shutil.copyfile(recipe, OUT / recipe.name)
        assert digest(mp3) == digest(destination)
        cues[key] = {'file': mp3.name, 'duration': row['dur'], 'loop': row['loop'], 'gain': gain, 'min': gate,
                     'group': row['group'], 'sourceKey': row['key'], 'libraryOrder': index,
                     'sourceMp3Sha256': digest(mp3), 'sourceWavSha256': digest(wav), 'sourceRecipeSha256': digest(recipe),
                     'qa': row.get('qa', [])}
    variants = []
    source = library / 'bof/chip_firewallLaunch.wav'
    # WAV duration, rather than recipe frame count, owns the audible source span.
    import wave
    with wave.open(str(source)) as w: duration = w.getnframes() / w.getframerate()
    for seconds in (1, 2, 4, 8):
        ratio = duration / seconds
        filters = []
        while ratio < .5:
            filters.append('atempo=0.5'); ratio /= .5
        filters.append(f'atempo={ratio:.10f}')
        filters += [f'apad=whole_dur={seconds}', f'atrim=duration={seconds}']
        target = OUT / f'chip_firewallLaunch_{seconds}s.mp3'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', str(source),
                        '-af', ','.join(filters), '-ar', '44100', '-ac', '2', '-b:a', '112k', str(target)], check=True)
        variants.append({'file': target.name, 'duration': seconds, 'sha256': digest(target),
                         'filter': ','.join(filters), 'sourceWavSha256': digest(source)})
    manifest = {'version': 'overdrive1011-chip', 'sourceLibrary': library.name, 'scope': 'Standalone Overdrive only',
                'approval': {'explicitKeys': APPROVED, 'allScoreBullets': True, 'allGroundSounds': True,
                             'inclusiveTailFrom': 'chip_gd_shellImpact', 'genreBanksIncluded': False},
                'base': 'expansion/topdown/audio/chip_1011/', 'cues': cues, 'firewallVariants': variants,
                'excludedKeys': [r['key'] for r in rows if r['key'].removeprefix('chip_') not in allowed]}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'manifest.js').write_text('/* Code-owned Overdrive chip sound bank; see its import builder. */\nwindow.TD_CHIP_AUDIO = ' + json.dumps(manifest, separators=(',', ':')) + ';\n', encoding='utf-8')
    print(f'Imported {len(cues)} approved MP3s verbatim; {len(variants)} firewall duration variants; excluded {len(manifest["excludedKeys"])} unapproved cues.')


if __name__ == '__main__': main()
