"""Shared portable paths for the source roster export/build commands."""
from pathlib import Path
import argparse

SOURCE_DIR=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Export or build the native Bullets of Fury roster catalogue.')
parser.add_argument('--root',type=Path,help='Game checkout root (auto-detected when installed under tools).')
parser.add_argument('--workdir',type=Path,help='Directory holding the runtime/enrichment snapshots.')
parser.add_argument('--output',type=Path,help='Catalogue destination (builder only).')
args=parser.parse_args()
candidate=next((p for p in SOURCE_DIR.parents if (p/'assets/game.js').is_file()),None)
ROOT=(args.root or candidate or Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')).resolve()
OUT=(args.workdir or (ROOT/'_shots/enemy_atlas_1013' if candidate else SOURCE_DIR)).resolve()
OUT.mkdir(parents=True,exist_ok=True)
OUTPUT=(args.output or OUT/'enemy_atlas_1013.json').resolve()
