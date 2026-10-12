"""Migrate source layout checks to the new card owner, retaining CRLF bytes."""
from pathlib import Path
p=Path(__file__).resolve().parent/'test_fl.js';b=p.read_bytes()
pairs=[
("PC_SPECIAL.decker.name===SPECIAL_INFO.decker.name","PC_SPECIAL.decker.name===SPECIAL_INFO.decker.name+' + INCENDIARY SHOTGUN'"),
("PC_SPECIAL.juggernaut.name===SPECIAL_INFO.juggernaut.name","PC_SPECIAL.juggernaut.name===SPECIAL_INFO.juggernaut.name+' + CHARGE DASH'"),
("ok(_src.indexOf('stats.length*step')>0 && _src.indexOf('specialY-19')>0,","var _pt11CardSource=fs.readFileSync(path.join(ROOT,'assets/playthrough_ui_1011.js'),'utf8');\r\n  ok(_pt11CardSource.includes('statH=stats.length*13') && _pt11CardSource.includes('infoY+infoH-specialH-statH-9'),"),
("ok(_src.indexOf('bioBot')>0,","ok(_pt11CardSource.includes('bioBottom=statY-5') && _pt11CardSource.includes('bioTop+11*i<bioBottom'),"),
("'the blocks under the bio are placed from where it actually ENDED, not from a fixed y'","'biography rows stop before the reserved statistics and ability area'"),
("ok(_src.indexOf('const emblemReady=!!(emblem&&XART.rdy(emblem))')>0 &&\r\n     _src.indexOf('width-(emblemReady?28:0)')>0,","ok(_pt11CardSource.includes('emblemReady=!!(emblem&&XART.rdy(emblem))') &&\r\n     _pt11CardSource.includes('emblemSpace=emblemReady?eh+8:0'),"),
("_opn.length===4 && _opn[3].k==='cover' && _opn[3].d>=7 && _opn.slice(0,3).every(b=>b.d>=6)","_opn.length===5 && _opn[3].k==='roll' && _opn[3].d>=18 && _opn[4].k==='cover' && _opn[4].d>=7 && _opn.slice(0,3).every(b=>b.d>=6)")]
for old,new in pairs:
 old=old.encode();new=new.encode()
 if new in b:continue
 assert b.count(old)==1,(old,b.count(old));b=b.replace(old,new)
p.write_bytes(b)
print('Updated menu expectations while retaining the original CRLF.')
