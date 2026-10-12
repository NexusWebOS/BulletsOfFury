"""The current 640x480 brief supersedes the historical 800x600 sizing fixture.

The previous source remains in sizing_800x600_fixture_1011.py; its recorded
53-check result remains in docs/qa/overdrive_sizing_1011.json. Run the current
native entrance/card/closer-view checks through this established command.
"""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('probe_boss_intro_1011.py')),run_name='__main__')
