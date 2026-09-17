#!/usr/bin/env python3
"""
capture_batch_0916.py - the marketing clip reel, captured from the real game.

One process per clip on purpose. shoot.py's own note records that a long headless run
accumulates memory until the renderer faults ("Target crashed"), and the fault surfaces as
whatever you happened to be capturing at the time -- which once cost a whole pass being read
as a boss-death crash. A fresh browser per clip costs ~20s of boot and removes that entirely.

    python _BUILD_SOURCE/capture_batch_0916.py              everything
    python _BUILD_SOURCE/capture_batch_0916.py bosses       one group
    python _BUILD_SOURCE/capture_batch_0916.py --dry
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUT = os.path.join(GAME, 'docs', 'marketing_0916', 'clips')

# name, extra args. `fight` jumps through the game's own debugFightList, so a clip of "the stage 6
# miniboss" is the encounter the game names rather than a stage number and a stopwatch.
REEL = {
    'bosses': [
        ('boss_s1_overlordx', ['--fight', 'JUNGLE OVERLORD-X', '--stage', '1', '--seconds', '22']),
        ('boss_s2_furnace', ['--fight', 'FURNACE TYRANT', '--stage', '2', '--seconds', '22']),
        ('boss_s3_rimewall', ['--fight', 'RIME WALL', '--stage', '3', '--seconds', '22']),
        ('boss_s4_sovereign', ['--fight', 'STORM SOVEREIGN', '--stage', '4', '--seconds', '22']),
        ('boss_s6_carrier', ['--fight', 'DOOMSDAY CARRIER', '--stage', '6', '--seconds', '22']),
        ('boss_s7_warden', ['--fight', 'TOXIC PORTAL WARDEN', '--stage', '7', '--seconds', '22']),
        ('boss_s8_cocoon', ['--fight', 'BLACK COCOON', '--stage', '8', '--seconds', '22']),
        ('boss_s9_sentinels', ['--fight', 'WARP SENTINELS', '--stage', '9', '--seconds', '22']),
    ],
    'minis': [
        ('mini_s1_razorback', ['--fight', 'RAZORBACK', '--stage', '1', '--seconds', '20']),
        ('mini_s3_frost', ['--fight', 'FROST CRUISER', '--stage', '3', '--seconds', '20']),
        ('mini_s6_tempest', ['--fight', 'TEMPEST LEVIATHAN', '--stage', '6', '--seconds', '20']),
        ('mini_s9_horizon', ['--fight', 'EVENT HORIZON', '--stage', '9', '--seconds', '20']),
    ],
    'stages': [
        ('stage_s2_lava', ['--stage', '2', '--seconds', '16', '--settle', '5']),
        ('stage_s3_ice', ['--stage', '3', '--seconds', '16', '--settle', '5']),
        ('stage_s5_space', ['--stage', '5', '--seconds', '16', '--settle', '6']),
        ('stage_s6_storm', ['--stage', '6', '--seconds', '16', '--settle', '5']),
        ('stage_s9_void', ['--stage', '9', '--seconds', '16', '--settle', '5']),
    ],
    # The weapon showcase, all nine.
    #
    # ⚠ EACH ONE NEEDS ITS WEAPON SLOT, ITS TIER AND ITS SPECIAL, OR THEY ARE THE SAME CLIP.
    # A pilot's identity in this game is the special and the upgraded primary; at the default
    # slot 0 tier 1 every pilot fires the same orange stream and the first pilot reel came back
    # as six clips of one gun. Slots: 0 mg 1 spread 2 missile 3 laser 4 flame 5 iceorb
    # 6 lasermist 7 chaingun 8 lightning.
    'pilots': [
        # ⚠ COLE IS CAPPED AT 5 HERE ON PURPOSE, THOUGH HIS TIERS RUN TO 8.
        # At tier 8 `coleTier()>=8` returns out of pShoot immediately -- the fusion cannon
        # replaces the machine gun and fires through its own path, which this autopilot does not
        # drive. Measured: tier 8 gave 705 shots and a score of 0->0, tier 5 gave 540 shots and
        # 0->5970. That is this harness not reaching the cannon, not a defect in the weapon;
        # showing the fusion cannon needs its fire path driven, which nobody has done yet.
        ('pilot_cole', ['--stage', '4', '--pilot', 'cole', '--seconds', '15', '--settle', '5',
                        '--weapon', '0', '--wlevel', '5', '--special']),
        # ⚠⚠ THE WEAPON SLOT BELOW IS CHOSEN FOR CAPTURE RATE, NOT ONLY FOR FLAVOUR, AND THAT IS
        # A MEASURED CONSTRAINT. Same stage, same pilot, same tier 5, 8 seconds, only the weapon
        # differing: MACHINE GUN 54.7 fps / ICE ORB 30.7 / SPREAD FIRE 8.9 / LASER 1.5. So a
        # pilot showcased on spread or laser captures as a slideshow. The SPECIALS are cheap --
        # Juggernaut went 7.7 fps on spread to 50.9 on the machine gun with the wrecking balls
        # still running -- so each pilot keeps their special, which is the real identity anyway.
        ('pilot_juggernaut', ['--stage', '4', '--pilot', 'juggernaut', '--seconds', '15', '--settle', '5',
                              '--weapon', '0', '--wlevel', '5', '--special']),
        # Freezer's slot 4 is ICE BREATH, not the flamethrower -- a separate attack, not a recolour
        ('pilot_freezer', ['--stage', '3', '--pilot', 'freezer', '--seconds', '15', '--settle', '5',
                           '--weapon', '4', '--wlevel', '5', '--special']),
        ('pilot_lizzie', ['--stage', '4', '--pilot', 'lizzie', '--seconds', '15', '--settle', '5',
                          '--weapon', '0', '--wlevel', '5', '--special']),
        # ⚠ MAVERICK CANNOT BE CAPTURED HERE AND THAT IS NOT A SETTINGS PROBLEM. The widening
        # laser IS his identity -- he is the only pilot who keeps it -- and the laser is the 1.5
        # fps weapon. There is no substitute that still shows Maverick. Mike records this one on
        # his own GPU with `R` in debug mode. Left in at tier 3 so the entry exists and the fps
        # line in the log keeps saying so.
        ('pilot_maverick', ['--stage', '1', '--pilot', 'maverick', '--seconds', '10', '--settle', '4',
                            '--weapon', '3', '--wlevel', '3', '--special']),
        ('pilot_yuri', ['--stage', '6', '--pilot', 'yuri', '--seconds', '15', '--settle', '5',
                        '--weapon', '8', '--wlevel', '3', '--special']),
        ('pilot_falva', ['--stage', '1', '--pilot', 'falva', '--seconds', '15', '--settle', '5',
                         '--weapon', '0', '--wlevel', '5', '--special']),
        ('pilot_axel', ['--stage', '4', '--pilot', 'axel', '--seconds', '15', '--settle', '5',
                        '--weapon', '0', '--wlevel', '5', '--special']),
        # Decker's shotgun is `dkFire`, which claims the trigger ahead of the primary, so his
        # identity survives the machine-gun slot untouched
        ('pilot_decker', ['--stage', '4', '--pilot', 'decker', '--seconds', '15', '--settle', '5',
                          '--weapon', '0', '--wlevel', '5', '--special']),
    ],
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    groups = args or list(REEL.keys())
    os.makedirs(OUT, exist_ok=True)

    jobs = []
    for g in groups:
        if g not in REEL:
            print('no group %r; have %s' % (g, ', '.join(REEL)))
            sys.exit(1)
        jobs += REEL[g]

    print('%d clips -> %s' % (len(jobs), OUT))
    log = []
    for i, (name, extra) in enumerate(jobs, 1):
        cmd = [sys.executable, os.path.join(ROOT, 'capture_clip_0916.py'),
               '--name', name, '--out', OUT] + extra
        print('\n[%d/%d] %s' % (i, len(jobs), name))
        if dry:
            print('   ', ' '.join(cmd[2:]))
            continue
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        keep = [l for l in (r.stdout or '').splitlines()
                if not l.startswith('127.0.0.1') and l.strip()]
        for l in keep:
            print('   ', l)
        if r.returncode != 0:
            print('    FAILED rc=%d' % r.returncode)
            for l in (r.stderr or '').splitlines()[-6:]:
                print('    !', l)
        log.append((name, r.returncode, time.time() - t0))

    if not dry:
        print('\n--- batch ------------------------------------------------')
        for name, rc, dt in log:
            print('  %-24s %s  %.0fs' % (name, 'ok' if rc == 0 else 'FAILED', dt))


if __name__ == '__main__':
    main()
