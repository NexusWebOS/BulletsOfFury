"""Reuse BOF's actual Options renderer; adapt its data/input to Overdrive."""
from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'assets/game.js'
text=source.read_text(encoding='utf-8')

def function(name):
    found=list(re.finditer(r'\bfunction\s+'+re.escape(name)+r'\s*\(',text))
    start=found[-1].start(); pos=text.index('{',found[-1].end()); depth=0; quote=None; comment=None; escaped=False
    for i in range(pos,len(text)):
        ch=text[i]; nxt=text[i:i+2]
        if comment=='line':
            if ch=='\n':comment=None
            continue
        if comment=='block':
            if text[i-1:i+1]=='*/':comment=None
            continue
        if quote:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch==quote:quote=None
            continue
        if nxt=='//':comment='line';continue
        if nxt=='/*':comment='block';continue
        if ch in "'\"`":quote=ch;continue
        if ch=='{':depth+=1
        if ch=='}':
            depth-=1
            if depth==0:return text[start:i+1]
    raise ValueError(name)

names=['roundRectFill','roundRect','bofPanel','bofTitle','drawCanonBackdrop',
       '_selKey','_selWhite','drawSelArrow','menuSelMark','menuSelWhite',
       'keyName','inputPromptArt','helpGlyph','drawOptions']
original={n:function(n) for n in names}
copied=dict(original)
draw=copied['drawOptions']
begin=draw.index("  const rows=[{t:'head',label:'VOLUME'}];")
end=draw.index('  const selectable=',begin)
draw=draw[:begin]+'  const rows=makeRows();\n'+draw[end:]
draw=draw.replace("rebindAction=selRow.act; rebindWho=(selRow.who||1); Audio.SFX.blip();",'armControl(selRow);')
draw=draw.replace("rebindAction=r.act; rebindWho=(r.who||1); optSelIdx=selectable.findIndex(o=>o.r===r); Audio.SFX.blip();",'armControl(r); optSelIdx=selectable.findIndex(o=>o.r===r);')
draw=draw.replace("active?'PRESS KEY':keyName(_shownBind)","active?(r.who===2?'PRESS BUTTON':'PRESS KEY'):keyName(_shownBind)")
draw=draw.replace("  { const targetY=pad+selY*rh;","  if(followSelection) { const targetY=pad+selY*rh;")
copied['drawOptions']=draw
adapter=(ROOT/'expansion/topdown/_research/original_options_adapter_1011.js').read_text()
assert adapter.count('/* ORIGINAL_RENDERER */')==1
out=ROOT/'expansion/topdown/js/original_options_1011.js'
out.write_text(adapter.replace('/* ORIGINAL_RENDERER */','\n\n'.join(copied[n] for n in names)),encoding='utf-8',newline='\n')
meta={'owner':'build_original_options_1011.py','source':'assets/game.js',
      'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'output':str(out.relative_to(ROOT)).replace('\\','/'),
      'functions':{n:{'originalSha256':hashlib.sha256(original[n].encode()).hexdigest(),
                       'adaptedSha256':hashlib.sha256(copied[n].encode()).hexdigest(),
                       'copiedVerbatim':copied[n]==original[n]} for n in names},
      'adaptations':['Ground keyboard/controller row data; canonical Overdrive saves and actual hardware bindings',
                     'Controller capture says PRESS BUTTON; learn/preset actions use the original key-cap controls',
                     'Wheel scrolling follows navigation when selection changes, so the cursor does not undo pointer scrolling'],
      'viewport':[480,512],'fonts':'Original BOFmil / BOFCommandSignal.ttf',
      'layout':'Original panel, 32px rows, segmented volume strips, key caps, scrollbar and CANCEL/APPLY renderer'}
(ROOT/'expansion/topdown/_research/original_options_provenance_1011.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print('Original Options exported: '+str(sum(v['copiedVerbatim'] for v in meta['functions'].values()))+'/14 renderer functions copied verbatim')
