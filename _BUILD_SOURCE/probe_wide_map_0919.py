"""Compatibility entry point: the single-canvas campaign renderer replaces the extender."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('probe_campaign_full_0922.py')), run_name='__main__')
