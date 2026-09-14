"""Author and pack Command bitmap fonts. Glyph masks are the editable design source.

No system-font dependency, AI letter recognition, or edits to old atlases. Sheet,
metrics and runtime registration are emitted together by this owning workflow.
"""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];O=R/'assets/game/fonts/command_0914';O.mkdir(exist_ok=True)
# Five-column master cuts: open counters, distinct 0/O and 1/I, full uppercase coverage.
ROWS={
'A':'01110 11011 11011 11111 11011 11011 11011',
'B':'11110 11011 11011 11110 11011 11011 11110',
'C':'01111 11000 11000 11000 11000 11000 01111',
'D':'11110 11011 11011 11011 11011 11011 11110',
'E':'11111 11000 11000 11110 11000 11000 11111',
'F':'11111 11000 11000 11110 11000 11000 11000',
'G':'01111 11000 11000 11011 11011 11011 01111',
'H':'11011 11011 11011 11111 11011 11011 11011',
'I':'111 010 010 010 010 010 111',
'J':'00111 00011 00011 00011 00011 11011 01110',
'K':'11011 11011 11110 11100 11110 11011 11011',
'L':'11000 11000 11000 11000 11000 11000 11111',
'M':'10001 11011 11111 10101 10001 10001 10001',
'N':'11001 11001 11101 11111 11011 11011 11001',
'O':'01110 11011 11011 11011 11011 11011 01110',
'P':'11110 11011 11011 11110 11000 11000 11000',
'Q':'01110 11011 11011 11011 11011 11110 00111',
'R':'11110 11011 11011 11110 11100 11010 11011',
'S':'01111 11000 11000 01110 00011 00011 11110',
'T':'11111 00100 00100 00100 00100 00100 00100',
'U':'11011 11011 11011 11011 11011 11011 01110',
'V':'11011 11011 11011 11011 11011 01010 00100',
'W':'10001 10001 10001 10101 11111 11011 10001',
'X':'11011 11011 01010 00100 01010 11011 11011',
'Y':'11011 11011 01010 00100 00100 00100 00100',
'Z':'11111 00011 00110 01100 11000 11000 11111',
'0':'01110 11011 11111 11111 11011 11011 01110',
'1':'010 110 010 010 010 010 111',
'2':'01110 11011 00011 00110 01100 11000 11111',
'3':'11110 00011 00011 01110 00011 00011 11110',
'4':'11011 11011 11011 11111 00011 00011 00011',
'5':'11111 11000 11000 11110 00011 00011 11110',
'6':'01110 11000 11000 11110 11011 11011 01110',
'7':'11111 00011 00010 00110 00100 01100 01000',
'8':'01110 11011 11011 01110 11011 11011 01110',
'9':'01110 11011 11011 01111 00011 00011 01110',
'!':'1 1 1 1 1 0 1','?':'11110 00011 00011 00110 00100 00000 00100',
'.':'00 00 00 00 00 00 11',',':'00 00 00 00 00 01 01 10',
':':'0 1 1 0 1 1 0',';':'00 01 01 00 01 01 10',
"'":'1 1 0 0 0 0 0','"':'101 101 000 000 000 000 000',
'-':'000 000 000 111 000 000 000','_':'00000 00000 00000 00000 00000 00000 11111',
'+':'00000 00100 00100 11111 00100 00100 00000',
'=':'00000 00000 11111 00000 11111 00000 00000',
'/':'00001 00010 00010 00100 01000 01000 10000',
'\\':'10000 01000 01000 00100 00010 00010 00001',
'(':'001 010 100 100 100 010 001',')':'100 010 001 001 001 010 100',
'[':'111 100 100 100 100 100 111',']':'111 001 001 001 001 001 111',
'{':'011 010 010 110 010 010 011','}':'110 010 010 011 010 010 110',
'<':'0001 0010 0100 1000 0100 0010 0001','>':'1000 0100 0010 0001 0010 0100 1000',
'%':'11001 11010 00010 00100 01000 01011 10011',
'&':'01100 10010 10100 01000 10101 10010 01101',
'#':'01010 01010 11111 01010 11111 01010 01010',
'$':'00100 01111 10100 01110 00101 11110 00100',
'@':'01110 10001 10111 10101 10111 10000 01111',
'*':'00000 10101 01110 11111 01110 10101 00000',
'^':'00100 01010 10001 00000 00000 00000 00000',
'|':'1 1 1 1 1 1 1','~':'00000 00000 01001 10110 00000 00000 00000',
'`':'10 01 00 00 00 00 00',
'\u2190':'00000 00100 01000 11111 01000 00100 00000',
'\u2192':'00000 00100 00010 11111 00010 00100 00000',
'\u2191':'00100 01110 10101 00100 00100 00100 00000',
'\u2193':'00000 00100 00100 00100 10101 01110 00100',
'\u2022':'000 000 010 111 010 000 000',
}
# Dialogue cuts are leaner than display cuts, keeping counters spacious at 12-16px.
LEAN={c:v.replace('11011','10001').replace('11000','10000').replace('00011','00001') for c,v in ROWS.items() if c.isalnum()}
LEAN.update({'0':'01110 10001 10011 10101 11001 10001 01110','N':'10001 11001 11001 10101 10011 10011 10001','M':'10001 11011 10101 10101 10001 10001 10001'})
FAMILIES={
'dialogue':('Command Signal','#ffffff','#ffffff','#ffffff',1,1,0),
'game':('Command Alloy','#f2f7ff','#c6d5e9','#587795',3,3,0),
'1':('Canopy Regiment','#eef7cc','#b4c96c','#526331',3,3,0),
'2':('Furnace Strike','#fff3b1','#ffa13c','#9f391d',3,3,1),
'3':('Glacier Bastion','#f3ffff','#86d8fa','#296290',3,3,0),
'4':('Iron Command','#fff0c2','#c8ae69','#645236',4,3,0),
'5':('Orbital Spear','#f5eaff','#cf91ff','#663b99',3,3,1),
'6':('Skyward Wing','#eaffff','#84c7eb','#315a84',4,3,1),
'7':('Toxic Warning','#f5ffd2','#a9e05d','#496b26',3,3,0),
'8':('Crimson Dominion','#fff0d7','#dda899','#85334d',4,3,0),
'9':('Void Vanguard','#fff0ff','#c99aff','#5e468c',3,3,1),
}
def rgb(s):return tuple(bytes.fromhex(s[1:]))+(255,)
def build(key,cfg):
 name,top,mid,low,sx,sy,slant=cfg;dialogue=key=='dialogue';pad=0 if dialogue else 1
 cellw=32;cellh=32;cols=16;chars=list(ROWS);rows=math.ceil(len(chars)/cols)
 sheet=Image.new('RGBA',(cellw*cols,cellh*rows));glyphs={};frames={};font={};ride={}
 cap=7*sy+pad*2
 for i,ch in enumerate(chars):
  pattern=(LEAN.get(ch,ROWS[ch])if dialogue else ROWS[ch]).split();w=len(pattern[0]);mask=Image.new('L',(w*sx+slant*3+pad*2+1,len(pattern)*sy+pad*2+1));md=ImageDraw.Draw(mask)
  for y,row in enumerate(pattern):
   for x,v in enumerate(row):
    if v=='1':
     shift=(6-min(6,y))//2*slant;xx=pad+x*sx+shift;yy=pad+y*sy
     md.rectangle((xx,yy,xx+sx-1,yy+sy-1),fill=255)
  # A cut-metal stencil break on military families; never applied to dialogue or small marks.
  if key in ['1','4','7']and ch.isalpha():
   for x in range(mask.width):
    if x==mask.width//2 and ch not in 'I':
     for y in range(3*sy,4*sy):mask.putpixel((x,y),0)
  ink=Image.new('RGBA',mask.size)
  for y in range(mask.height):
   for x in range(mask.width):
    if mask.getpixel((x,y)):
     c=rgb(top if y<=pad+sy else mid if y<pad+5*sy else low)
     if not dialogue and y>0 and not mask.getpixel((x,y-1)):c=rgb(top)
     ink.putpixel((x,y),c)
  box=ink.getbbox();assert box,ch
  tile=ink.crop(box);x=(i%cols)*cellw;y=(i//cols)*cellh;sheet.alpha_composite(tile,(x,y))
  rect=[x,y,tile.width,tile.height];glyphs[ch]={'sprite_rect':rect,'bounds_in_cell':list(box),'x_advance':w*sx+slant*3+(1 if dialogue else 3)}
  gkey='command_'+key+'_'+str(ord(ch));frames[gkey]=rect;font[ch]=gkey
  slack=cap-tile.height
  if slack>0:ride[ch]=round(max(0,box[1]-pad)/slack,5)
 glyphs[' ']={'sprite_rect':[0,0,0,0],'bounds_in_cell':[0,0,0,0],'x_advance':3 if dialogue else 3*sx}
 for a,b in {'\u2019':"'",'\u2018':"'",'\u201c':'"','\u201d':'"','\u2013':'-','\u2014':'-','\u00d7':'X','\u2026':'.'}.items():glyphs[a]=glyphs[b];font[a]=font[b]
 m={'schema':'coleforge.bitmap-font.v2','family':name,'capsOnly':True,'line_height':8 if dialogue else cap,'baseline':7 if dialogue else cap-pad,'glyphs':glyphs,'source':'Hand-authored editable pixel masks in build_fonts.py','texture_filter':'nearest'}
 path='assets/game/fonts/command_0914/'+key
 sheet.save(O/(key+'-alpha.png'));(O/(key+'-map.json')).write_text(json.dumps(m,indent=2)+'\n')
 return m,{'atlas':path+'-alpha.png','frames':frames,'font':font,'ride':ride},path
maps={};arts={};paths={}
for k,c in FAMILIES.items():maps[k],arts[k],paths[k]=build(k,c)
maps['cutscene']=maps['dialogue'];paths['cutscene']=paths['dialogue'];arts['final']=arts['game']
data={'faces':paths,'maps':maps,'stageFonts':arts,'names':{k:v[0]for k,v in FAMILIES.items()}}
script='// Generated by _BUILD_SOURCE/readable_type_0914/build_fonts.py.\nwindow.BOF_COMMAND_FONTS='+json.dumps(data,separators=(',',':'))+';\n'
script+='Object.assign(window.BOF_BMF_MAPS,window.BOF_COMMAND_FONTS.maps);\nObject.assign(window.BOF.stageFontV4,window.BOF_COMMAND_FONTS.stageFonts);\n'
(O/'fonts.js').write_text(script,encoding='utf-8')
(O/'README.md').write_text('# Command font family\n\nEleven new code-authored bitmap faces: clear all-caps dialogue, Command Alloy game lettering, and nine biome display variants. All glyphs, spacing, punctuation and registration are rebuilt together by `_BUILD_SOURCE/readable_type_0914/build_fonts.py`. Original fonts remain stored. No external typeface or AI-generated letter sheet is used.\n')
print('Built',len(FAMILIES),'font faces,',len(ROWS),'mapped visible glyphs each.')
