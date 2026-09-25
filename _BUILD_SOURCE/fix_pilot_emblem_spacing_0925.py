"""Reserve subtitle width only when the affiliation badge actually decoded."""
from pathlib import Path

path = Path('assets/game.js')
source = path.read_bytes()
assert b'\r\n' not in source
old = (b"          if(row) pcFontLeft(row,x0,ty,pcFontFit(row,width-(ci===3?28:0),idH,7),ci===3?'#cfeaff':P.tint,1);\n"
       b"          if(ci===3){ const emblem=affilEmblemKey(M.affil);\n"
       b"            if(emblem)psBlitFit(emblem,x1-11,ty,23,idH*2.2,.95); }\n")
new = (b"          const emblem=ci===3?affilEmblemKey(M.affil):null;\n"
       b"          const emblemReady=!!(emblem&&XART.rdy(emblem));\n"
       b"          if(row)pcFontLeft(row,x0,ty,pcFontFit(row,width-(emblemReady?28:0),idH,7),ci===3?'#cfeaff':P.tint,1);\n"
       b"          if(emblemReady)psBlitFit(emblem,x1-11,ty,23,idH*2.2,.95);\n")
assert source.count(old) == 1
path.write_bytes(source.replace(old, new))
