"""Build a local review from native game captures and the verified encounter log."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_1003b'
data=json.loads((O/'verification.json').read_text(encoding='utf-8'))
names=['Orbital Host','Hive Helicopter','Alien Furnace','Cryo Hive','Storm Organism','Null Knight','Void Harrier','Last Warden']
desc=['Independent breakable arms and lunging talon sweeps; gravity well and paired code lasers.','Sweeping machine guns, committed bomb zones and interceptable guided missiles.','Complete arms on every pose; shootable magma, floor eruptions and charged beams.','Rapid ice gun streams, twin charge lasers and outward orbiting cold ordnance.','Targetable missile waves, charged central lightning and a committed ram.','Shield guard, chained jumping downcuts, quick horizontal follow-ups and teleport resets.','Turbine gravity, missile batteries and dual carrier laser lanes.','Chaingun sweeps, gravity stomp, charged scissors and code lanes.']
sections=[]
for i,(title,body) in enumerate(zip(names,desc),1):
 pics=[O/f'form-{i}-idle.png']+sorted(O.glob(f'form-{i}-*-tell.png'))
 imgs=''.join(f'<a href="{p.name}" target="_blank"><img loading="lazy" src="{p.name}" alt="{html.escape(p.stem)}"></a>' for p in pics)
 sections.append(f'<section id="form-{i}"><h2>{i}. {title}</h2><p>{body}</p><div class="shots">{imgs}</div></section>')
extra=''.join(f'<a href="{n}.png"><img loading="lazy" src="{n}.png" alt="{n}"></a>' for n in ['yuri-chainguns','sewer-pod-replacements','machine-gun-loadout','eight-bars-filling','eight-bars-full','host-arm-broken'])
video='<video controls preload="metadata" src="combat-motion.webm"></video>' if (O/'combat-motion.webm').exists() else ''
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eight lives — Bullets of Fury</title><style>
*{box-sizing:border-box}body{margin:0;background:#080c16;color:#e6eefb;font:16px/1.5 system-ui}main{max-width:1400px;margin:auto;padding:28px}h1{font-size:38px;line-height:1.1;margin:14px 0}h2{margin:0}a{color:#71e6ff}header,section{padding:22px;border:1px solid #27374d;background:#0c1422;margin-bottom:22px;border-radius:12px}small{color:#a3b5cb}nav{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0}.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.shots img{width:100%;display:block;max-height:450px;object-fit:contain;background:#020407}video{width:100%;max-height:650px}p{max-width:950px}.tag{color:#fdd574;text-transform:uppercase;letter-spacing:.16em;font-size:12px}.button{display:inline-block;padding:10px 18px;background:#173f55;border:1px solid #71e6ff;border-radius:6px;text-decoration:none}
</style><main><header><div class="tag">October 3 • Local build</div><h1>Eight lives. Every previous boss returns.</h1><p>Stage 8 now has eight separate alien identities and eight colored health bars. All pilots default to anchored chainguns from Level 6, including password starts and older saves. Machine guns remain selectable in Loadout. Remaining Stage 7 toxic pods now deploy selected mutants.</p><a class="button" href="/index.html?build=d69cffa4-finale-1003b" target="_blank">Play updated build</a><nav>'''
page+=''.join(f'<a href="#form-{i}">{i}. {n}</a>' for i,n in enumerate(names,1))
page+=f'</nav><small>{len(data["checks"])} native Chromium checks; {sum(not c["ok"] for c in data["checks"])} failures; {len(data["errors"])} browser errors. Controlled fixtures, not a human campaign win or final difficulty certification. Click images for full-size captures.</small></header>'+video
page+='<section><h2>Chainguns, sewer replacements and the stacked gauge</h2><div class="shots">'+extra+'</div></section>'+''.join(sections)+'</main></html>'
(O/'review.html').write_text(page,encoding='utf-8');print(O/'review.html')
