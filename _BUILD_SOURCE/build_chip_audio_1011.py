"""Import the approved ColeForge library for BOF without changing its originals.

The main game owns this small portable bank; Overdrive keeps its existing bank.
No generated base manifest or unapproved recording is rewritten.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import wave
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/game/shared/audio/chip_1011'
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
# Context-specific menu/reward cues are wired at their events, not by replacing
# shared blip/powerup/hit sounds. Aliases below are the actual weapon bus names.
ALIASES = {
    'shieldBreak': ['shieldBreakCombat'],
    'enemyLaser': ['laserShot', 'enemyPulseLaserBlue', 'enemyPulseLaserRed', 'enemyPulseLaserAlien'],
    'missileLaunch': ['missile', 'volleyLaunch'],
    'bossCannon': ['enemyBossCannon', 'combatCannon0927'],
    'railCannon': ['enemyRailCannon', 'helixVolley'],
    'impactMetal': ['av3_impact_metal'],
    'firewallLaunch': ['firewallArrive', 'av3_firewall_launch'],
    'bombDropLegacy': ['bomb'], 'extraLife': ['life'], 'playerDeath': ['death'],
    'decker_shell': ['dkShell'], 'chargeDash': ['juggernautRamLaunch'],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=Path, default=DEFAULT)
    library = parser.parse_args().library.resolve()
    rows = [r for r in json.loads((library / 'library.json').read_text(encoding='utf-8')) if r['kind'] == 'bof']
    assert set(APPROVED) <= {r['key'].removeprefix('chip_') for r in rows}
    tail = next(i for i, r in enumerate(rows) if r['key'] == 'chip_gd_shellImpact')
    allowed = set(APPROVED) | {r['key'].removeprefix('chip_') for r in rows
                             if r['key'].startswith(('chip_scoreBullet', 'chip_gd_'))}
    allowed |= {r['key'].removeprefix('chip_') for r in rows[tail:]}
    OUT.mkdir(parents=True, exist_ok=True)
    cues = {}
    for i, r in enumerate(rows):
        key = r['key'].removeprefix('chip_')
        if key not in allowed:
            continue
        source = library / r['dir'] / r['file']
        mp3, wav, recipe = [source.with_suffix(s) for s in ('.mp3', '.wav', '.recipe.json')]
        for p in (mp3, recipe):
            shutil.copyfile(p, OUT / p.name)
            assert digest(p) == digest(OUT / p.name)
        cues[key] = dict(file=mp3.name, duration=r['dur'], loop=r['loop'], group=r['group'],
                         sourceKey=r['key'], libraryOrder=i, target=r['target'], aliases=ALIASES.get(key, []),
                         sourceMp3Sha256=digest(mp3), sourceWavSha256=digest(wav), sourceRecipeSha256=digest(recipe))
    source = library / 'bof/chip_firewallLaunch.wav'
    with wave.open(str(source)) as w:
        duration = w.getnframes() / w.getframerate()
    variants = []
    for seconds in (1, 2, 4, 8):
        ratio, filters = duration / seconds, []
        while ratio < .5:
            filters.append('atempo=0.5')
            ratio /= .5
        filters += [f'atempo={ratio:.10f}', f'apad=whole_dur={seconds}', f'atrim=duration={seconds}']
        dst = OUT / f'chip_firewallLaunch_{seconds}s.mp3'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', str(source),
                        '-af', ','.join(filters), '-ar', '44100', '-ac', '2', '-b:a', '112k', str(dst)], check=True)
        variants.append(dict(file=dst.name, duration=seconds, sha256=digest(dst), filter=','.join(filters),
                             sourceWavSha256=digest(source)))
    bank = dict(version='bof-chip-1011', base=OUT.relative_to(ROOT).as_posix()+'/', sourceLibrary=library.name,
                approval=dict(explicitKeys=APPROVED, allScoreBullets=True, allGroundSounds=True,
                              inclusiveTailFrom='chip_gd_shellImpact', genreBanksIncluded=False),
                cues=cues, firewallVariants=variants,
                excludedKeys=[r['key'] for r in rows if r['key'].removeprefix('chip_') not in allowed])
    (OUT/'manifest.json').write_text(json.dumps(bank, indent=2)+'\n', encoding='utf-8')
    (OUT/'manifest.js').write_text('/* Owned by _BUILD_SOURCE/build_chip_audio_1011.py. */\nwindow.BOF_CHIP_AUDIO='+json.dumps(bank, separators=(',', ':'))+';\n', encoding='utf-8')
    print(f'BOF: {len(cues)} approved cues, {len(variants)} pitch-preserving firewall variants; {len(bank["excludedKeys"])} excluded.')


if __name__ == '__main__':
    main()
