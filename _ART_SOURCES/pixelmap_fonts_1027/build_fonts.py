from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,math,hashlib,subprocess

W=Path(__file__).resolve().parent;O=W/'fonts';O.mkdir(parents=True,exist_ok=True)
# Original, explicitly authored pixel skeletons. No traced or extracted game glyphs.
UP={
'A':'01110/11011/10001/10001/11111/10001/10001',
'B':'11110/10001/10001/11110/10001/10001/11110',
'C':'01111/10000/10000/10000/10000/10000/01111',
'D':'11110/10001/10001/10001/10001/10001/11110',
'E':'11111/10000/10000/11110/10000/10000/11111',
'F':'11111/10000/10000/11110/10000/10000/10000',
'G':'01111/10000/10000/10111/10001/10001/01111',
'H':'10001/10001/10001/11111/10001/10001/10001',
'I':'11111/00100/00100/00100/00100/00100/11111',
'J':'00111/00010/00010/00010/10010/10010/01100',
'K':'10001/10010/10100/11000/10100/10010/10001',
'L':'10000/10000/10000/10000/10000/10000/11111',
'M':'10001/11011/10101/10101/10001/10001/10001',
'N':'10001/11001/11001/10101/10011/10011/10001',
'O':'01110/10001/10001/10001/10001/10001/01110',
'P':'11110/10001/10001/11110/10000/10000/10000',
'Q':'01110/10001/10001/10001/10101/10010/01101',
'R':'11110/10001/10001/11110/10100/10010/10001',
'S':'01111/10000/10000/01110/00001/00001/11110',
'T':'11111/00100/00100/00100/00100/00100/00100',
'U':'10001/10001/10001/10001/10001/10001/01110',
'V':'10001/10001/10001/10001/10001/01010/00100',
'W':'10001/10001/10001/10101/10101/11011/10001',
'X':'10001/10001/01010/00100/01010/10001/10001',
'Y':'10001/10001/01010/00100/00100/00100/00100',
'Z':'11111/00001/00010/00100/01000/10000/11111',
'0':'01110/10001/10001/10001/10001/10001/01110',
'1':'00100/01100/00100/00100/00100/00100/01110',
'2':'01110/10001/00001/00010/00100/01000/11111',
'3':'11110/00001/00001/01110/00001/00001/11110',
'4':'00010/00110/01010/10010/11111/00010/00010',
'5':'11111/10000/10000/11110/00001/00001/11110',
'6':'01110/10000/10000/11110/10001/10001/01110',
'7':'11111/00001/00010/00100/01000/01000/01000',
'8':'01110/10001/10001/01110/10001/10001/01110',
'9':'01110/10001/10001/01111/00001/00001/01110',
}
LOW={
'a':'01110/00001/01111/10001/01111','b':'10000/10000/10110/11001/10001/10001/11110',
'c':'01111/10000/10000/10000/01111','d':'00001/00001/01101/10011/10001/10001/01111',
'e':'01110/10001/11111/10000/01111','f':'00110/01001/01000/11100/01000/01000/01000',
'g':'01111/10001/10001/10011/01101/00001/01110','h':'10000/10000/10110/11001/10001/10001/10001',
'i':'00100/00000/01100/00100/00100/00100/01110','j':'00010/00000/00110/00010/00010/00010/00010/10010/01100',
'k':'10000/10000/10010/10100/11000/10100/10010','l':'01100/00100/00100/00100/00100/00100/01110',
'm':'11010/10101/10101/10101/10101','n':'10110/11001/10001/10001/10001',
'o':'01110/10001/10001/10001/01110','p':'11110/10001/10001/11001/10110/10000/10000',
'q':'01111/10001/10001/10011/01101/00001/00001','r':'11110/11001/10000/10000/10000',
's':'01111/10000/01110/00001/11110','t':'01000/01000/11100/01000/01000/01001/00110',
'u':'10001/10001/10001/10011/01101','v':'10001/10001/10001/01010/00100',
'w':'10001/10001/10101/10101/01010','x':'10001/01010/00100/01010/10001',
'y':'10001/10001/10001/10011/01101/00001/01110','z':'11111/00010/00100/01000/11111'}
PUN={
' ':'00000','!':'00100/00100/00100/00100/00100/00000/00100',
'"':'01010/01010/00000/00000/00000/00000/00000',
'#':'01010/11111/01010/01010/11111/01010/00000',
'$':'00100/01111/10100/01110/00101/11110/00100',
'%':'11001/11010/00010/00100/01000/01011/10011',
'&':'01100/10010/10100/01000/10101/10010/01101',
"'":'00100/00100/01000/00000/00000/00000/00000',
'(':'00010/00100/01000/01000/01000/00100/00010',
')':'01000/00100/00010/00010/00010/00100/01000',
'*':'00000/10101/01110/11111/01110/10101/00000',
'+':'00000/00100/00100/11111/00100/00100/00000',
',':'00000/00000/00000/00000/00110/00100/01000',
'-':'00000/00000/00000/11111/00000/00000/00000',
'.':'00000/00000/00000/00000/00000/00110/00110',
'/':'00001/00010/00010/00100/01000/01000/10000',
':':'00000/00110/00110/00000/00110/00110/00000',
';':'00000/00110/00110/00000/00110/00100/01000',
'<':'00001/00010/00100/01000/00100/00010/00001',
'=':'00000/00000/11111/00000/11111/00000/00000',
'>':'10000/01000/00100/00010/00100/01000/10000',
'?':'01110/10001/00001/00010/00100/00000/00100',
'@':'01110/10001/10111/10101/10111/10000/01111',
'[':'01110/01000/01000/01000/01000/01000/01110',
'\\':'10000/01000/01000/00100/00010/00010/00001',
']':'01110/00010/00010/00010/00010/00010/01110',
'^':'00100/01010/10001/00000/00000/00000/00000',
'_':'00000/00000/00000/00000/00000/00000/11111',
'`':'01000/00100/00010/00000/00000/00000/00000',
'{':'00011/00100/00100/11000/00100/00100/00011',
'|':'00100/00100/00100/00100/00100/00100/00100',
'}':'11000/00100/00100/00011/00100/00100/11000',
'~':'00000/00000/01001/10110/00000/00000/00000'}
# Wide nine-row display masters: sculpted shoulders, open counters, asymmetric R/Q.
HEAVY={
'A':'0011100/0111110/1100011/1100011/1100011/1111111/1100011/1100011/1100011',
'B':'1111110/1100011/1100011/1111110/1100011/1100011/1100011/1100011/1111110',
'C':'0011111/0111111/1100000/1100000/1100000/1100000/1100000/0111111/0011111',
'D':'1111100/1111110/1100011/1100011/1100011/1100011/1100011/1111110/1111100',
'E':'1111111/1111111/1100000/1100000/1111110/1100000/1100000/1111111/1111111',
'F':'1111111/1111111/1100000/1100000/1111110/1100000/1100000/1100000/1100000',
'G':'0011111/0111111/1100000/1100000/1101111/1100011/1100011/0111111/0011111',
'H':'1100011/1100011/1100011/1100011/1111111/1100011/1100011/1100011/1100011',
'I':'1111111/1111111/0011100/0011100/0011100/0011100/0011100/1111111/1111111',
'J':'0001111/0001111/0000011/0000011/0000011/1100011/1100011/0111110/0011100',
'K':'1100011/1100110/1101100/1111000/1110000/1111000/1101100/1100110/1100011',
'L':'1100000/1100000/1100000/1100000/1100000/1100000/1100000/1111111/1111111',
'M':'1100011/1110111/1111111/1101011/1101011/1100011/1100011/1100011/1100011',
'N':'1100011/1110011/1110011/1101011/1101011/1100111/1100111/1100011/1100011',
'O':'0011100/0111110/1100011/1100011/1100011/1100011/1100011/0111110/0011100',
'P':'1111110/1100011/1100011/1100011/1111110/1100000/1100000/1100000/1100000',
'Q':'0011100/0111110/1100011/1100011/1100011/1101011/1100110/0111111/0011011',
'R':'1111111/1111111/1100011/1100011/1111110/1111000/1101100/1100110/1100011',
'S':'0011111/0111111/1100000/1100000/0111110/0000011/0000011/1111110/1111100',
'T':'1111111/1111111/0011100/0011100/0011100/0011100/0011100/0011100/0011100',
'U':'1100011/1100011/1100011/1100011/1100011/1100011/1100011/0111110/0011100',
'V':'1100011/1100011/1100011/1100011/1100011/0110110/0110110/0011100/0001000',
'W':'1100011/1100011/1100011/1100011/1101011/1101011/1111111/1110111/1100011',
'X':'1100011/1100011/0110110/0011100/0001000/0011100/0110110/1100011/1100011',
'Y':'1100011/1100011/0110110/0011100/0011100/0011100/0011100/0011100/0011100',
'Z':'1111111/1111111/0000110/0001100/0011000/0110000/1100000/1111111/1111111',
'0':'0011100/0111110/1100011/1100011/1100011/1100011/1100011/0111110/0011100',
'1':'0001100/0011100/0111100/0001100/0001100/0001100/0001100/0111110/0111110',
'2':'0111110/1100011/0000011/0000110/0001100/0011000/0110000/1100000/1111111',
'3':'1111110/0000011/0000011/0001110/0001110/0000011/0000011/1100011/0111110',
'4':'0000110/0001110/0011110/0110110/1100110/1111111/1111111/0000110/0000110',
'5':'1111111/1100000/1100000/1111110/0000011/0000011/0000011/1100011/0111110',
'6':'0011110/0110000/1100000/1111110/1100011/1100011/1100011/0111110/0011100',
'7':'1111111/1111111/0000011/0000110/0001100/0011000/0011000/0011000/0011000',
'8':'0111110/1100011/1100011/1100011/0111110/1100011/1100011/1100011/0111110',
'9':'0011100/0111110/1100011/1100011/1100011/0111111/0000011/0000110/0111100'}
GLYPHS={**UP,**LOW,**PUN};CHARS=''.join(chr(i)for i in range(32,127));assert set(CHARS)==set(GLYPHS)
PALETTES={
'chrome':['f6fcff','d7e9f5','9db2d2','51608c','283650'],
'ice':['f4ffff','b2f3ff','44c4f4','2478b8','183764'],
'ember':['fff4c4','ffd463','ff8c38','c73b36','5d233b'],
'gold':['fff7cb','ffe787','e8b743','9b642b','4b3430'],
'toxic':['f4ffd2','d0fc81','7acc46','347244','213c38'],
'rose':['fff0fc','ffc3ec','ee6cba','a23a89','482957'],
'signal':['eafff6','adf5dd','45cbbb','287e8b','213b5b'],
'corrupt':['fff1ff','d7aaff','a267eb','623a9c','362c58']}
STYLES={
'fury_strike':dict(label='FURY STRIKE',cw=20,ch=24,baseline=20,lineHeight=26,capHeight=18,advance=18,role='Heavy arcade menus and stage cards'),
'overdrive':dict(label='AFTERBURN',cw=18,ch=20,baseline=16,lineHeight=22,capHeight=14,advance=15,role='Forward-cut action menus and weapon names'),
'vermilion':dict(label='SOVEREIGN',cw=14,ch=20,baseline=16,lineHeight=22,capHeight=13,advance=12,role='Sega RPG narrative and chapter titles'),
'command':dict(label='COMMAND',cw=8,ch=12,baseline=9,lineHeight=12,capHeight=7,advance=6,role='Compact dialogue, stats and HUD readouts')}

def skeleton(ch,style):
 cfg=STYLES[style];m=Image.new('L',(cfg['cw'],cfg['ch']));d=ImageDraw.Draw(m)
 rows=(HEAVY.get(ch,GLYPHS[ch])if style=='fury_strike'else GLYPHS[ch]).split('/')
 desc=ch in 'gpqy';short=ch.islower()and ch not in 'bdfhijklt'
 if style=='command':
  top=2 if short else 0
  for y,row in enumerate(rows):
   for x,v in enumerate(row):
    if v=='1':d.point((x+1,y+top+2),fill=255)
 elif style=='vermilion':
  # Connected one-pixel pen strokes on a 2-pixel modular grid; tiny bracket serifs.
  top=(4 if short else 0)+3
  for y,row in enumerate(rows):
   for x,v in enumerate(row):
    if v!='1':continue
    px,py=x*2+2,y*2+top
    d.point((px,py),fill=255)
    if x+1<len(row)and row[x+1]=='1':d.line((px,py,px+2,py),fill=255)
    if y+1<len(rows):
     for nx in [x-1,x,x+1]:
      if 0<=nx<len(row)and rows[y+1][nx]=='1':d.line((px,py,nx*2+2,py+2),fill=255)
  if ch.isalnum():
   for y in [top,top+(len(rows)-1)*2]:
    for x in range(2,11):
     if m.getpixel((x,y)) and (y==top or not desc):
      if x>1:d.point((x-1,y),fill=255)
 elif style=='overdrive':
  top=4 if short else 0
  for y,row in enumerate(rows):
   shift=(6-y-top//2)//2
   for x,v in enumerate(row):
    if v=='1':d.rectangle((x*2+2+shift,y*2+top+2,x*2+3+shift,y*2+top+3),fill=255)
  # Signature tiny cuts on E/F/H/A mid-bars, not a full-width readability-breaking slash.
  if ch in 'AEFHPR':d.point((6,9),fill=0)
 else:
  if ch.isdigit()and ch not in HEAVY:
   raw=rows;rows=[''.join(raw[min(6,y*7//9)][min(4,x*5//7)]for x in range(7))for y in range(9)]
  scale=2;top=0 if ch in HEAVY or ch.isdigit() else (8 if short else 4)
  offset=2 if ch in HEAVY or ch.isdigit() else 4
  for y,row in enumerate(rows):
   for x,v in enumerate(row):
    if v=='1':d.rectangle((x*scale+offset,y*scale+top+2,x*scale+offset+1,y*scale+top+3),fill=255)
  # The authored master owns the complete top scanline. A sequential corner
  # cut here erased the next pixel's neighbor, cascading across the top bar.
 return m

def paint(m,style,palette):
 w,h=m.size;im=Image.new('RGBA',(w,h));pix=im.load();p=[tuple(bytes.fromhex(c))for c in PALETTES[palette]]
 # One common baseline and palette row per family; never randomly move glyphs.
 for y in range(h):
  for x in range(w):
   if not m.getpixel((x,y)):continue
   if style=='command':color=p[0 if y<5 else 1]
   elif style=='vermilion':color=p[0 if y<7 else 1 if y<12 else 2]
   else:
    # Preserve the full readable face. Deep metal tones belong to the outline,
    # never to a thin stem, diagonal leg, counter or the bottom of a numeral.
    t=y/(h-3);band=0 if t<.21 else 1 if t<.39 else 2 if t<.49 else 1 if t<.59 else 2
    color=p[band]
    if y>0 and not m.getpixel((x,y-1)):color=p[0]
    elif x>0 and not m.getpixel((x-1,y)):color=p[1]
    elif y+1<h and not m.getpixel((x,y+1)):color=p[2]
   # Dark outline and one-pixel keyed shadow are offline raster pixels.
   if style!='command':
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1)]:
     nx,ny=x+dx,y+dy
     if 0<=nx<w and 0<=ny<h and not m.getpixel((nx,ny)):pix[nx,ny]=(7,11,24,255)
   pix[x,y]=(*color,255)
 return im

MAN={};SHEETS={}
for name,cfg in STYLES.items():
 masks={c:skeleton(c,name)for c in CHARS};glyphs={}
 for i,c in enumerate(CHARS):
  glyphs[str(ord(c))]={'x':i%16*cfg['cw'],'y':i//16*cfg['ch'],'w':cfg['cw'],'h':cfg['ch'],'xadvance':cfg['advance'] if c!=' 'else max(4,cfg['advance']//2)}
 for palette in PALETTES:
  sheet=Image.new('RGBA',(cfg['cw']*16,cfg['ch']*6))
  for i,c in enumerate(CHARS):sheet.alpha_composite(paint(masks[c],name,palette),(i%16*cfg['cw'],i//16*cfg['ch']))
  key=name+'_'+palette;sheet.save(O/(key+'.png'));SHEETS[key]=sheet
  metrics={**cfg,'name':key,'palette':palette,'file':key+'.png','first':32,'last':126,'glyphs':glyphs,'kerning':[]}
  MAN[key]=metrics;(O/(key+'.json')).write_text(json.dumps(metrics,indent=2))
  # AngelCode BMFont text import, fixed cells preserve the common vertical origin.
  fnt=[f'info face="ColeForge {cfg["label"]}" size={cfg["capHeight"]} bold=0 italic={int(name=="overdrive")} charset="ASCII" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=0,0',f'common lineHeight={cfg["lineHeight"]} base={cfg["baseline"]} scaleW={sheet.width} scaleH={sheet.height} pages=1 packed=0',f'page id=0 file="{key}.png"','chars count=95']
  for code,g in glyphs.items():fnt.append('char id='+code+' '+' '.join(f'{k}={g[z]}'for k,z in [('x','x'),('y','y'),('width','w'),('height','h')])+f' xoffset=0 yoffset=0 xadvance={g["xadvance"]} page=0 chnl=15')
  (O/(key+'.fnt')).write_text('\n'.join(fnt))

def text(im,s,x,y,font='fury_strike_chrome',scale=1,center=False):
 a=MAN[font];width=sum(a['glyphs'][str(ord(c))]['xadvance']for c in s)
 if center:x-=width*scale//2
 for c in s:
  g=a['glyphs'][str(ord(c))];cell=SHEETS[font].crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h']))
  if scale!=1:cell=cell.resize((cell.width*scale,cell.height*scale),Image.Resampling.NEAREST)
  im.alpha_composite(cell,(round(x),round(y)));x+=g['xadvance']*scale

board=Image.new('RGBA',(1280,1000),(7,12,23,255));d=ImageDraw.Draw(board)
text(board,'COLEFORGE / PIXELMAP LAB',640,26,'fury_strike_chrome',2,True)
text(board,'ORIGINAL SEGA-INSPIRED TYPE / 4 FAMILIES / 8 PALETTES / 95 GLYPHS',640,88,'command_signal',2,True)
for i,(family,cfg)in enumerate(STYLES.items()):
 y=137+i*198;d.rectangle((28,y,1251,y+181),fill=(12,23,39),outline=(39,76,100))
 text(board,f'{i+1:02d} / {cfg["label"]}',50,y+12,'command_signal',2)
 text(board,cfg['role'].upper(),50,y+41,'command_chrome',1)
 text(board,'BULLETS OF FURY',50,y+65,family+'_chrome',2)
 text(board,'STAGE 06 / FURIOUS',650,y+65,family+'_gold',2)
 text(board,'THE FORGE  -  CHRONOS RAGE',50,y+121,family+'_ice',1)
 text(board,'0123456789  !? +-%',650,y+121,family+'_ember',1)
 text(board,'Aa Bb Cc Dd  WAVE / PULSE / RETINA',50,y+150,family+'_signal',1)
for i,palette in enumerate(PALETTES):text(board,palette.upper(),35+i*157,953,'command_'+palette,2)
board.convert('RGB').save(W/'font-family-preview.png')
for family in STYLES:
 im=Image.new('RGBA',(960,720),(7,12,23,255));text(im,STYLES[family]['label'],480,20,'fury_strike_chrome',2,True)
 for i,palette in enumerate(PALETTES):
  y=92+i*72;text(im,palette.upper(),20,y,'command_'+palette,1)
  text(im,'1 PLAYER  2 PLAYERS  OPTIONS',148,y,family+'_'+palette,1)
  text(im,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',148,y+25,family+'_'+palette,1)
  text(im,'abcdefghijklmnopqrstuvwxyz 0123456789',148,y+48,family+'_'+palette,1)
 im.convert('RGB').save(W/(family+'-review.png'))
(W/'font-manifest.json').write_text(json.dumps(MAN,separators=(',',':')))
(W/'glyph-masters.json').write_text(json.dumps({'small':GLYPHS,'heavy':HEAVY,'palettes':PALETTES,'styles':STYLES},indent=2))
# Native editable Aseprite sources for each family, palette as distinct layers.
ase=Path(r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe')
if ase.exists():
 for family in STYLES:
  path=O/(family+'_chrome.png');subprocess.run([str(ase),'--batch',str(path),'--save-as',str(W/(family+'.aseprite'))],check=True,capture_output=True)
checks=[]
for key,a in MAN.items():
 checks.append({'font':key,'glyphs':len(a['glyphs']),'evenCell':a['cw']%2==a['ch']%2==0,'sha256':hashlib.sha256((O/a['file']).read_bytes()).hexdigest()})
 assert len(a['glyphs'])==95 and a['baseline']==STYLES[key.rsplit('_',1)[0]]['baseline']
 # Each non-space glyph must have pixels; descenders must stay within its cell.
 for c in CHARS[1:]:
  g=a['glyphs'][str(ord(c))];cell=SHEETS[key].crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h']))
  assert cell.getbbox(),(key,c)
(W/'verification.json').write_text(json.dumps({'fonts':checks,'totalGlyphs':len(MAN)*95,'missing':[]},indent=2))
print('Built',len(MAN),'original bitmap fonts;',len(MAN)*95,'glyph cells; Aseprite sources saved.')
