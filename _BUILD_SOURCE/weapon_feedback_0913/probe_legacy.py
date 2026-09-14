"""Run the existing chain geometry regression without overwriting its previous proof."""
import runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
m=runpy.run_path(str(ROOT/'_BUILD_SOURCE/probe_wreckdash_0912z.py'))
m['main'].__globals__['OUT']=str(ROOT/'_shots/weapon_feedback_0913/legacy_wreckdash')
m['main']()
