"""Create native screenshot contacts and a save-isolated playable review."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,time,imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005';O.mkdir(parents=True,exist_ok=True)
def contact(paths,name,cols=4,w=240):
 cells=[]
 for p in paths:
  im=Image.open(p).convert('RGB');h=round(im.height*w/im.width);im=im.resize((w,h))
  c=Image.new('RGB',(w,h+24),'#091323');c.paste(im,(0,24));ImageDraw.Draw(c).text((6,5),p.stem,fill='white');cells.append(c)
 if not cells:return
 h=max(c.height for c in cells);grid=Image.new('RGB',(cols*w,((len(cells)+cols-1)//cols)*h),'#091323')
 for i,c in enumerate(cells):grid.paste(c,((i%cols)*w,(i//cols)*h))
 grid.save(O/name)
contact([O/f'knight-pose-{i}.png' for i in range(8)],'knight-contact.png')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for file in O.glob('*.webm'):
 dest=O/'video_frames'/file.stem;dest.mkdir(parents=True,exist_ok=True)
 started=time.time()
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(file),'-vf','fps=1/3,scale=240:-1',str(dest/'frame-%03d.png')],check=True)
 # Earlier longer captures may leave extra scratch frames. Keep them preserved,
 # but only use frames rewritten from the current recording in its contact.
 contact(sorted(p for p in dest.glob('*.png') if p.stat().st_mtime>=started-.05),file.stem+'-contact.png')
codes=['BOSS1','BOSS2','BOSS3','BOSS4','BOSS5','HARR6','REBEL6','BOSS7','FINAL1','FINAL2','FINAL3','KNIGHT','HELI8','FURN8','CRYO8','STORM8','ACE8','WARD8','MINI8','HAMMER','HAMA']
buttons=''.join(f'<button data-code="{c}">{c}</button>' for c in codes)
gallery=[('knight-contact.png','Eight intact knight heads and independently attached weapons'),('symbiote-void.png','Black symbiote void'),('symbiote-emergence.png','Colossus emergence'),('beam-hits-rebels.png','Sustained laser hits real Rebel hulls'),('code-shield-shattered.png','Code shield at zero, ballistic digits'),('approved-palette-bombers.png','Approved red/green stealth fighter bombers')]
figures=''.join(f'<figure><img src="{f}" alt="{caption}"><figcaption>{caption}</figcaption></figure>' for f,caption in gallery)
videos=''.join(f'<figure><video controls preload="metadata" src="{f.name}"></video><figcaption>{f.stem.replace("-"," ")} — Furious, live engine and keyboard input; silent canvas recording.</figcaption><details><summary>Frames across the recording</summary><img src="{f.stem}-contact.png" alt="Frames throughout this gameplay recording"></details></figure>' for f in O.glob('*.webm'))
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Overnight combat upgrade</title><style>*{box-sizing:border-box}body{background:#091323;color:#eef6ff;font:16px/1.5 system-ui;margin:0}main{max-width:1260px;margin:auto;padding:30px}h1{font-size:42px}p{max-width:1000px;color:#c2d7ed}.buttons{display:flex;gap:9px;flex-wrap:wrap}button{padding:11px;background:#223d61;color:white;border:1px solid #5d8dc0;font:inherit;cursor:pointer}iframe{width:100%;height:960px;border:1px solid #5d8dc0}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}figure{margin:0;background:#13243d}img,video{width:100%;display:block}img{image-rendering:pixelated}figcaption,summary{padding:12px}a{color:#8feaff}@media(max-width:650px){.grid{grid-template-columns:1fr}}</style><main><h1>Overnight combat upgrade</h1><p>Independent mutated-drone and ghost attack cycles; cinematic symbiote emergence; persistent HP for Dracula and every boss copy. Whole knight body, complete head in every pose, targetable sword/shield, real Hammer attacks, shield smite and Dark Code.</p><p>Code shields exhaust and shatter. Periodic finale pills contain Flash and Time Bombs. Sustained beams and Cole VI/VII/Fusion damage real Rebel hulls; homing shots select individual visible fighters. Gang defense stays in-game, Voss stays fast, Jace and Rook shoot south. Approved stealth bomber palettes and brighter authored enemy rounds are deployed.</p><h2>Playable encounters</h2><p>These buttons use the real encounter routes on Furious with Cole and all laser tiers available. Practice blocks campaign save writes. The normal game still uses your chosen difficulty and pilot. Cole cycles earned VI/VII/VIII with Fire + Multi-retina.</p><div class="buttons">BUTTONS</div><p id="status">Practice does not write campaign saves.</p><iframe id="arena" title="Playable encounter practice" hidden allow="autoplay"></iframe><h2>Native render evidence</h2><div class="grid">FIGURES</div><h2>Recorded gameplay</h2><p>Focused encounter/wave tests, including actual player deaths. These are not a full campaign clear. Recordings capture the game canvas without audio.</p><div class="grid">VIDEOS</div><p><a href="../../index.html?build=overnight-1005">Open game</a> · <a href="verification.json">Native checks</a> · <a href="lasers.json">Actual laser damage</a> · <a href="donors.json">Donor controllers</a> · <a href="../../docs/PASSWORD_ENCOUNTERS_1005.md">All passwords</a></p></main><script>
const f=document.querySelector('#arena'),status=document.querySelector('#status');let timer;
document.querySelectorAll('[data-code]').forEach(btn=>btn.onclick=()=>{clearInterval(timer);f.hidden=false;status.textContent='Loading practice…';const code=btn.dataset.code;
 f.onload=()=>{let tries=0;timer=setInterval(()=>{const w=f.contentWindow;if(++tries>1200){clearInterval(timer);status.textContent='Load timed out.';return;}if(typeof w.on5LaunchEncounter!=='function')return;try{
  w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};
  w.eval('diffKey="furious";DIFF=DIFFS.furious;pilotIndex=PILOTS.findIndex(p=>p.key==="cole");pwInput='+JSON.stringify(code)+';submitPassword();startRun(PENDING_STAGE);run.lives=9;run._primary1003b="mg";run.weapon=0;run.wlevel=6;run.wlevels[0]=8;run._cfUnlocked=8;run._cfTier=6;run.bombs=6;player.invuln=2;Audio.init();Audio.resume();');
  clearInterval(timer);status.textContent='Practice ready.';f.focus();f.scrollIntoView({behavior:'smooth',block:'start'});
 }catch(e){clearInterval(timer);status.textContent='Practice could not start.';console.error(e);}},100);};f.src='../../index.html?build=overnight-1005-practice';});
</script></html>'''.replace('BUTTONS',buttons).replace('FIGURES',figures).replace('VIDEOS',videos)
(O/'review.html').write_text(html,encoding='utf-8');print('Review ready:',O/'review.html')
