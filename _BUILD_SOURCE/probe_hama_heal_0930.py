"""Reuse the live hammer-hit probe against the HAMA soundtrack route."""
import sys
import probe_hammer_heal_break_0929 as probe
probe.SETUP=probe.SETUP.replace('ht27Pending=true; startRun(5);','ht27Pending=true; hamaPending=true; startRun(5);').replace('Snd.music.hammerTime.pause()','Snd.music.hama.pause()')
if '--secret' not in sys.argv:sys.argv.append('--secret')
if '--label' not in sys.argv:sys.argv.extend(['--label','hama_0930'])
sys.exit(probe.main())
