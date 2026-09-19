from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js';s=p.read_text(encoding='utf-8')
a="""        const sc=w/BMBAR.frameW;
        const h=BMBAR.frameH*sc, tabH=BMTAB.h*sc;
        const sy=cy-h/2+h+tabH+2;
        drawShieldBarArt(sf, cx, sy+h/2, w);"""
b="""        const sc=w/BMBAR.frameW;
        const h=BMBAR.frameH*sc, sh=82*(w/881);
        drawShieldBarArt(sf,cx,cy+h/2+sh/2+3,w);"""
if s.count(a)!=1:raise SystemExit(f'shield spacing matches: {s.count(a)}')
p.write_text(s.replace(a,b,1),encoding='utf-8',newline='\n')
