"""Export current native portrait pixels, then assemble non-destructive identity references."""
from pathlib import Path
import base64, json, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import shoot

R = Path(__file__).resolve().parents[1]
O = R / '_ART_SOURCES/cast_cinematics_1102/references'
O.mkdir(parents=True, exist_ok=True)
pilots = ['cole', 'axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva']
errors = []
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel='msedge')
        p = b.new_page(viewport={'width': 1366, 'height': 768})
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text[:400]) if m.type == 'error' else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function('window.__bofFrames > 4', timeout=120000)
        p.evaluate(shoot.TRAP_RAF)
        for pilot in pilots:
            key = p.evaluate('p=>pilotPortrait(p,"idle")', pilot)
            p.wait_for_function('k=>XART.rdy(k)', arg=key, timeout=120000)
            data = p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');
                c.width=im.width;c.height=im.height;const g=c.getContext('2d');
                g.drawImage(im,0,0);return c.toDataURL().split(',')[1];}''', key)
            (O / f'{pilot}-portrait.png').write_bytes(base64.b64decode(data))
        b.close()
finally:
    stop()
audit = Image.new('RGB', (1440, 1440), '#17202c')
draw = ImageDraw.Draw(audit)
for i, pilot in enumerate(pilots):
    body = (R / f'assets/game/pilots/{pilot}/body_frames/front_identity_1020/cole-neutral.webp' if pilot == 'cole'
            else R / f'assets/game/pilots/{pilot}/body_frames/cinematic_characters/{pilot}/poses/01_front_neutral.png')
    reference = Image.new('RGBA', (1024, 1024))
    im = Image.open(body).convert('RGBA')
    im.thumbnail((480, 960), Image.Resampling.LANCZOS)
    reference.alpha_composite(im, ((512-im.width)//2, 32))
    face = Image.open(O / f'{pilot}-portrait.png').convert('RGBA')
    face.thumbnail((480, 480), Image.Resampling.NEAREST)
    reference.alpha_composite(face, (528+(480-face.width)//2, 160))
    reference.save(O / f'{pilot}-identity.png')
    reference.thumbnail((464, 440), Image.Resampling.LANCZOS)
    x, y = (i%3)*480, (i//3)*480
    audit.paste(reference, (x+8,y+25), reference)
    draw.text((x+15,y+8), pilot.upper(), fill='white')
audit.save(O / 'identity-audit.jpg', quality=93)
(O / 'native-export.json').write_text(json.dumps({'pilots': pilots, 'page_console_errors': errors}, indent=2)+'\n')
print(json.dumps({'references': len(pilots), 'errors': errors}))
