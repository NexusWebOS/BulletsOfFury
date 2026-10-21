from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_ART_SOURCES/menu_heart_1021';W=Path(__file__).parent
D=R/'assets/game/shared/ui/menu_windows_1021';D.mkdir(parents=True,exist_ok=True)
crops={'xl':(16,82,1520,882),'l':(14,28,1656,912),'m':(0,16,2024,752),'s':(2,85,1980,671)};art={}
for n,b in crops.items():
 im=Image.open(S/f'menu_{n}.png').convert('RGBA').crop(b);h=round(im.height*720/im.width/2)*2;im=im.resize((720,h),Image.Resampling.NEAREST);p=D/f'{n}.webp';im.save(p,lossless=True)
 art[n]={'key':'mw21_'+n,'path':p.relative_to(R).as_posix(),'w':720,'h':h,'slice':[64,74,64,32],'header':[72,24,576,23],'body':[52,85,616,h-130]}
(R/'assets/menu_windows_art_1021.js').write_text('const MW21_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
Q=R/'_shots/menu_heart_1021';Q.mkdir(parents=True,exist_ok=True)
labels=['Fury Threat Console','Holoscan — Exploded View','Field Manual 95','Arcade Data Cartridge','Hangar Service Lift']
items=[]
for i,label in enumerate(labels,1):
 im=Image.open(S/f'concept_{i}.png');im.save(Q/f'concept-{i}.webp',quality=94)
 items.append(f'<article id="concept-{i}"><h2>{i:02} / {label}</h2><a href="concept-{i}.webp" target="_blank"><img src="concept-{i}.webp" alt="{label}"></a><p>Visual direction for review. Final implementation will use the actual B.O.B. models, live stats and fitted game font.</p></article>')
frames=''.join(f'<article><h2>{n.upper()} menu frame</h2><img src="/assets/game/shared/ui/menu_windows_1021/{n}.webp" alt="{n} avatar-free frame"></article>' for n in ['xl','l','m','s'])
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Menu windows & five boss preview concepts</title><style>*{box-sizing:border-box}body{margin:0;background:#080b12;color:#edf5ff;font:18px/1.5 system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:28px}h1{font-size:clamp(24px,3vw,40px);margin-bottom:8px}h2{color:#ffc879;font-size:22px}p{color:#aebbd0}nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}a{color:#8ee5ff}article{margin:32px 0 56px;border-top:1px solid #334157;padding-top:16px;scroll-margin-top:15px}img{max-width:100%;height:auto;display:block;margin:auto}#frames img{background:#060810}button{padding:12px;font:inherit;background:#182134;color:#fff;border:1px solid #71809b}iframe{border:1px solid #516278;width:100%;height:780px}.note{border-left:3px solid #ff55a9;padding:14px;background:#1e1220}</style><main><h1>BULLETS OF FURY / Design Review</h1><p>Five distinct boss-inspection directions, plus purpose-built avatar-free menu windows.</p><nav>'''+''.join(f'<a href="#concept-{i}">{i:02} {l}</a>' for i,l in enumerate(labels,1))+'''<a href="#frames">XL / L / M / S windows</a><a href="#game">Game</a></nav><p class="note">The preview concepts are choices for your review, not installed replacements. Chrome Heart is an optional secret fight: beat the final fight as Falva or Lizzie, then enter BARBIE.</p>'''+''.join(items)+'<section id="frames"><h1>Menu-exclusive frames</h1><p>No avatars. Separate header/body apertures; preserved corners and measured text fitting.</p>'+frames+'</section><section id="verification"><h1>Live game verification</h1><p><a href="tutorial-mobile.png">Mobile tutorial menu</a> · <a href="tutorial-desktop.png">Desktop tutorial menu</a> · <a href="heart-actions.gif">Chrome Heart attack reel</a> · <a href="verification.json">Verification report</a></p></section><section id="game"><h1>Bullets of Fury</h1><p><a href="/index.html" target="_blank">Open game in its own tab</a></p></section></main>'
(Q/'review.html').write_text(html,encoding='utf-8')
for name in ['menu_windows_1021.js','chrome_heart_1021.js']:
 source=W/name if (W/name).exists() else R/'assets'/name
 if source.resolve()!=(R/'assets'/name).resolve():shutil.copy2(source,R/'assets'/name)
(R/'assets/chrome_heart_music_1021.js').write_text("// Set to a locally supplied, licensed instrumental path. Null keeps native Hammer music.\nconst CH21_MUSIC=null;\n",encoding='utf-8') if not (R/'assets/chrome_heart_music_1021.js').exists() else None
# Normalized frame banks are atlased only after all requested PixelLab jobs complete.
J=json.loads((S/'pixellab-jobs.json').read_text());banks={};sheets={};runtime=R/'assets/game/levels/secret/chrome_heart_1021';runtime.mkdir(parents=True,exist_ok=True)
clean=W/'heart-shield-clean.png'
if not clean.exists():clean=S/'shield-clean.png'
if clean.exists():
 source=S/'shield-clean.png'
 if clean.resolve()!=source.resolve():shutil.copy2(clean,source)
 full=Image.open(source).convert('RGBA');dst=S/'shield-clean';dst.mkdir(exist_ok=True)
 for i in range(16):full.crop(((i%4)*192,(i//4)*224,(i%4+1)*192,(i//4+1)*224)).save(dst/f'{i+1:02}.png')
 (S/'shield-alpha-repair.json').write_text(json.dumps({'tool':'PixelLab pixelart_workbench','original':'b0a0b2b9-7435-4628-813d-fd084cc813bd','edited':'f99183f9-e57b-4742-bf5f-cb4802c429f1','changed_pixels':90873,'preserved':'All bright rim pixels, original16 fixed192x224 cells','reason':'Remove12 observed dark opaque purple background colors from shield opening.'},indent=2))
for n,(job,count) in J.items():
 paths=sorted((S/('shield-clean' if n=='shield' and (S/'shield-clean').exists() else n)).glob('*.png'))
 if len(paths)!=count:print('PENDING',n,len(paths),count);continue
 ims=[Image.open(p).convert('RGBA') for p in paths];original_size=ims[0].size
 if n=='shield':
  padded=[]
  for im in ims:
   q=Image.new('RGBA',(im.width+32,im.height+32));q.alpha_composite(im,(16,16));padded.append(q)
  ims=padded
 cw,ch=ims[0].size
 assert cw%2==ch%2==0 and all(i.size==(cw,ch) for i in ims)
 # Keep every authored frame on its original common canvas; NEVER individually fit frames.
 sheet=Image.new('RGBA',(cw*8,ch*((count+7)//8)));cells=[]
 for i,im in enumerate(ims):
  sheet.alpha_composite(im,((i%8)*cw,(i//8)*ch));cells.append({'key':f'ch21_{n}_{i}','sheet':'ch21_sheet_'+n,'cell':[(i%8)*cw,(i//8)*ch,cw,ch],'bounds':list(im.getbbox() or (0,0,cw,ch))})
 p=runtime/f'{n}.webp';sheet.save(p,lossless=True);sheets[n]={'key':'nca_ch21_sheet_'+n,'path':p.relative_to(R).as_posix()}
 banks[n]={'w':cw,'h':ch,'scaleBase':max(original_size),'pivot':[cw//2,ch//2] if n in ['heart','shield'] else [144,100],'frames':cells}
 if n=='shield':print('shield center alpha',max(im.getpixel((cw//2,ch//2))[3] for im in ims))
(R/'assets/chrome_heart_art_1021.js').write_text('const CH21_ART='+json.dumps({'sheets':sheets,'banks':banks},separators=(',',':'))+';\n',encoding='utf-8')
p=R/'index.html';t=p.read_text(encoding='utf-8');mark='<script src="assets/menu_windows_art_1021.js?v=menu-heart-1021-2"></script>'
if 'assets/menu_windows_art_1021.js?' not in t:t=t.replace('</body>',mark+'\n<script src="assets/menu_windows_1021.js?v=menu-heart-1021-2"></script>\n<script src="assets/chrome_heart_music_1021.js?v=menu-heart-1021-2"></script>\n<script src="assets/chrome_heart_art_1021.js?v=menu-heart-1021-2"></script>\n<script src="assets/chrome_heart_1021.js?v=menu-heart-1021-2"></script>\n</body>')
import re
t=re.sub(r'(assets/(?:menu_windows(?:_art)?|chrome_heart(?:_art|_music)?)_1021.js\?v=)menu-heart-1021-\d+',r'\g<1>menu-heart-1021-2',t);p.write_text(t,encoding='utf-8',newline='\n')
print('built',list(banks),'runtime bytes',sum(p.stat().st_size for p in runtime.glob('*')),'review',Q/'review.html')
