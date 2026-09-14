"""Export the exact Command Signal pixel cuts as a real uppercase game font.

Requires fonttools==4.55.3; the native bitmap renderer remains preferred at small sizes.
"""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'_shots/readable_type_0914/fontdeps'))
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from build_fonts import ROWS,LEAN,O
fb=FontBuilder(800,isTTF=True);order=['.notdef','space']+['u%04X'%ord(c)for c in ROWS];fb.setupGlyphOrder(order)
cmap={32:'space'}
for c in ROWS:cmap[ord(c)]='u%04X'%ord(c)
for c in 'abcdefghijklmnopqrstuvwxyz':cmap[ord(c)]=cmap[ord(c.upper())]
for a,b in {'\u2019':"'",'\u2018':"'",'\u201c':'"','\u201d':'"','\u2013':'-','\u2014':'-','\u00d7':'X','\u2026':'.'}.items():cmap[ord(a)]=cmap[ord(b)]
fb.setupCharacterMap(cmap);glyphs={};metrics={}
for name in ['.notdef','space']:
 pen=TTGlyphPen(None);glyphs[name]=pen.glyph();metrics[name]=(300,0)
for c in ROWS:
 pen=TTGlyphPen(None);pattern=LEAN.get(c,ROWS[c]).split();name=cmap[ord(c)]
 for y,row in enumerate(pattern):
  # Each filled run is an exact horizontal pixel cluster, never a system-font outline.
  start=None
  for x,val in enumerate(row+'0'):
   if val=='1'and start is None:start=x
   if val=='0'and start is not None:
    x0=start*100;x1=x*100;bottom=(6-y)*100;top=bottom+100
    pen.moveTo((x0,bottom));pen.lineTo((x0,top));pen.lineTo((x1,top));pen.lineTo((x1,bottom));pen.closePath();start=None
 glyphs[name]=pen.glyph();metrics[name]=((len(pattern[0])+1)*100,0)
fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=800,descent=-200)
fb.setupNameTable({'familyName':'Bullets of Fury Command Signal','styleName':'Regular','uniqueFontIdentifier':'BOF-Command-Signal-0914','fullName':'Bullets of Fury Command Signal','psName':'BOFCommandSignal-Regular','version':'Version 1.000'})
fb.setupOS2(sTypoAscender=800,sTypoDescender=-200,usWinAscent=800,usWinDescent=200,sxHeight=700,sCapHeight=700)
fb.setupPost();fb.setupMaxp();gasp=newTable('gasp');gasp.gaspRange={65535:1};fb.font['gasp']=gasp
fb.save(O/'BOFCommandSignal.ttf');print('Wrote real uppercase TrueType fallback from the same bitmap glyph cuts.')
