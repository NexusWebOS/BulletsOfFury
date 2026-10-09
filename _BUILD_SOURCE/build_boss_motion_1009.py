"""Cut the approved generated reels; retain native RGBA and measured landmarks.

Owns boss_motion_art_1009.js and the dedicated loose cells. No shared atlas edits.
The generator's spacing is not an exact grid: measured rectangles are deliberate.
Connected foreground extraction only excludes adjacent poses from overlapping
rectangles; it never paints, keys dark armor away, or synthesizes sprite pixels.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '_ART_SOURCES/boss_motion_1009'
DEST = ROOT / 'assets/game/shared/combat/boss_motion_1009'
DEST.mkdir(parents=True, exist_ok=True)

# Global source coordinates: crop, body/shoulder pivot, physical hand/weapon tip.
DATA = {
 'dracodia_core': [
  ([0,0,384,522],[192,270],[192,150]),([384,0,768,522],[576,270],[576,150]),
  ([768,0,1152,522],[960,270],[960,150]),([1152,0,1536,522],[1344,270],[1344,150]),
  ([0,512,384,1024],[192,782],[192,662]),([384,512,768,1024],[576,782],[576,662]),
  ([768,512,1152,1024],[960,782],[960,662]),([1152,512,1536,1024],[1344,782],[1344,662])],
 'hammer_death': [
  ([25,65,440,496],[219,186],[219,186]),([412,66,772,496],[585,185],[585,185]),
  ([793,67,1140,495],[979,186],[979,186]),([1166,47,1511,497],[1317,182],[1317,182]),
  ([5,571,435,984],[218,690],[218,690]),([406,514,760,986],[587,697],[587,697]),
  ([765,514,1126,986],[944,704],[944,704]),([1128,514,1536,1016],[1342,705],[1342,705])],
 'hammer_counter': [
  ([8,55,429,443],[288,189],[58,137]),([447,16,819,443],[651,189],[526,85]),
  ([862,84,1365,443],[1034,188],[1298,209]),([1328,88,1774,443],[1497,183],[1707,249]),
  ([29,474,445,866],[176,607],[378,568]),([451,441,798,866],[614,612],[716,507]),
  ([791,500,1289,866],[1098,600],[872,634]),([1299,501,1724,866],[1574,609],[1365,655])],
 'dracodia_arms': [
  ([113,4,332,512],[228,88],[219,437]),([429,0,699,294],[504,151],[579,51]),
  ([857,4,1167,470],[981,90],[1091,380]),([1197,4,1471,511],[1280,88],[1370,435]),
  ([115,512,339,1019],[226,598],[230,942]),([456,481,716,798],[648,655],[547,551]),
  ([751,512,1072,970],[980,600],[816,896]),([1168,512,1457,1018],[1384,600],[1253,942])],
 'spider_claws': [
  ([28,19,292,513],[241,93],[108,462]),([347,43,710,353],[405,116],[643,179]),
  ([724,31,1130,497],[856,108],[1060,427]),([1065,42,1514,477],[1193,105],[1448,403]),
  ([36,515,332,1002],[79,587],[267,948]),([319,524,662,821],[611,590],[386,651]),
  ([656,528,1074,995],[958,590],[719,916]),([1086,522,1505,963],[1432,582],[1159,893])],
 'spider_legs': [
  ([104,94,400,487],[170,177],[300,445]),([442,17,714,390],[505,100],[592,340]),
  ([827,0,1116,519],[878,71],[1032,479]),([1188,30,1486,493],[1247,104],[1416,445]),
  ([55,605,337,999],[273,683],[164,952]),([439,523,711,899],[650,600],[551,850]),
  ([797,504,1097,1015],[1038,566],[867,975]),([1202,537,1481,1000],[1426,612],[1296,950])]
}
# Effects have uniform authored cells; the impact foot has a measured baseline.
for name, pivots in {
 'landing':[(244,383),(660,383),(1080,383),(1520,383),(225,800),(675,800),(1100,800),(1530,800)],
 'turret_charge':[(220,220),(666,220),(1112,220),(1555,220),(220,665),(666,665),(1112,665),(1555,665)]
}.items():
    im = Image.open(SOURCE/(name+'.png'))
    DATA[name] = [([round(i%4*im.width/4),round(i//4*im.height/2),
                   round((i%4+1)*im.width/4),round((i//4+1)*im.height/2)],list(p),list(p))
                 for i,p in enumerate(pivots)]

def components(mask):
    """Run-length connected component labels, without another imaging dependency."""
    parents, stats, runs, prev = [], [], [], []
    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    for y, row in enumerate(mask):
        d = np.diff(np.r_[False, row, False].astype('int8'))
        cur, j = [], 0
        for l, r in zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)):
            i = len(parents)
            parents.append(i); stats.append([int(r-l), int(l), y, int(r), y+1])
            cur.append((l, r, i)); runs.append((y, l, r, i))
            while j < len(prev) and prev[j][1] < l: j += 1
            k = j
            while k < len(prev) and prev[k][0] <= r:
                a, b = root(prev[k][2]), root(i)
                if a != b: parents[a] = b
                k += 1
        prev = cur
    groups = {}
    labels = np.zeros(mask.shape, dtype=np.int32)
    for i, s in enumerate(stats):
        q = root(i)
        if q not in groups: groups[q] = s.copy()
        else:
            b = groups[q]; b[0] += s[0]
            b[1] = min(b[1],s[1]); b[2] = min(b[2],s[2])
            b[3] = max(b[3],s[3]); b[4] = max(b[4],s[4])
    for y, l, r, i in runs: labels[y,l:r] = root(i)+1
    return labels, {k+1:v for k,v in groups.items() if v[0] > 5000}

manifest = {}
for name, rows in DATA.items():
    im = Image.open(SOURCE / (name+'.png')).convert('RGBA')
    pixels = np.array(im)
    labels, groups = components(pixels[:,:,3] > 160)
    frames = []
    for i, (rect, pivot, tip) in enumerate(rows):
        l,t,r,b = rect
        cell = pixels[t:b,l:r].copy()
        # Select the main continuous authored limb/body closest to its landmark.
        def distance(g):
            _,x0,y0,x1,y1=g
            return max(x0-pivot[0],0,pivot[0]-x1)**2+max(y0-pivot[1],0,pivot[1]-y1)**2
        own = min(groups, key=lambda k:distance(groups[k]))
        foreign = [k for k,g in groups.items() if k != own and
                   not (name == 'hammer_death' and i == 7 and g[1] >= 1128)]
        if name not in ('landing','turret_charge'):
            cell[:,:,3][np.isin(labels[t:b,l:r],foreign)] = 0
        out = DEST / f'{name}_{i}.png'
        Image.fromarray(cell).save(out, optimize=True)
        key = f'bm9_{name}_{i}'
        frames.append({'key':key,'path':out.relative_to(ROOT).as_posix(),
                       'w':r-l,'h':b-t,'pivot':[pivot[0]-l,pivot[1]-t],
                       'tip':[tip[0]-l,tip[1]-t],'sourceRect':rect})
    manifest[name] = frames
(SOURCE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/boss_motion_art_1009.js').write_text(
    '"use strict";\n// Generated only by _BUILD_SOURCE/build_boss_motion_1009.py.\n'+
    'const BM9_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Built',sum(map(len,manifest.values())),'authored frames with native RGBA landmarks.')
