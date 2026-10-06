"""Review native Dracodia captures and launch isolated real-engine sequences."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_1005';O.mkdir(parents=True,exist_ok=True)
setup=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
def contact(items,target,cols=4):
 cards=[]
 for name,im in items:
  im=im.convert('RGB');im.thumbnail((240,256));c=Image.new('RGB',(240,280),'#091323');c.paste(im,((240-im.width)//2,24));ImageDraw.Draw(c).text((7,5),name,fill='white');cards.append(c)
 out=Image.new('RGB',(cols*240,((len(cards)+cols-1)//cols)*280),'#091323')
 for i,c in enumerate(cards):out.paste(c,((i%cols)*240,(i//cols)*280))
 out.save(O/target)
contact([(p.stem,Image.open(p)) for p in sorted(O.glob('death-pose-*.png'),key=lambda p:int(p.stem.split('-')[-1]))],'death-contact.png')
clips=['first-destruction-reform','ghost-destruction-reform','dracodia-speech','dracodia-destruction','portal-home']
for name in clips:
 p=O/(name+'.gif');im=Image.open(p);samples=[]
 for i in range(0,im.n_frames,10):im.seek(i);samples.append((f'{i/5:.1f}s',im.copy()))
 contact(samples,name+'-timeline.png')
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(p),'-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(name+'.mp4'))],check=True)
buttons=''.join(f'<button data-scene="{scene}">{label}</button>' for scene,label in [('host','First destruction / reform'),('ghost','Ghost destruction / reform'),('speech','Dracodia reveal / speech'),('combat','Final combat'),('death','Dracodia destruction / home')])
video=''.join(f'<figure><video controls preload="metadata" src="{n}.mp4"></video><figcaption>{n.replace("-"," ")}</figcaption><details><summary>Inspect the timeline</summary><img src="{n}-timeline.png" alt="Sequence timeline"></details></figure>' for n in clips)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dracodia cinematic review</title><style>*{box-sizing:border-box}body{margin:0;background:#080e17;color:#e7f5ff;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:24px}button,select{padding:10px;background:#183831;color:#fff;border:1px solid #79b4a0;font:inherit;margin:4px}button{cursor:pointer}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}img,video{width:100%;display:block}img{image-rendering:pixelated}figure{margin:0;background:#16202b}figcaption,summary{padding:12px}iframe{width:100%;height:960px;border:1px solid #497567}a{color:#9feaff}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style><main><h1>Dracodia: reform, reveal and destruction</h1><p>Three outer fights remain intact: mutated drone, ghost, then Dracodia with eight persistent copied forms. These buttons start isolated sequences in the actual engine. Practice prevents campaign storage writes.</p><label>Pilot <select id="pilot"></select></label><label><input type="checkbox" id="coop"> Two pilots</label><div>BUTTONS</div><p id="status">Select a sequence. Audio plays inside the game; captured clips below are silent.</p><iframe id="game" hidden title="Dracodia practice" allow="autoplay"></iframe><h2>Native sequence captures</h2><p>Automated isolated progression with real damage handoffs and render calls. These are cinematic checks, not an unassisted campaign clear.</p><div class="grid">VIDEOS</div><h2>Destruction poses</h2><img src="death-contact.png" alt="Arms, head turns, rupture and charred remains"><h2>Generated components</h2><img src="asset-contact.png" alt="Fifty-five alpha art cells"><p><a href="verification.json">Browser verification</a> · <a href="../../docs/DRACODIA_CINEMATIC_1005.md">Implementation and remaining review</a> · <a href="../../index.html">Game</a></p></main><script>
const setup=SETUP,f=document.querySelector('#game'),status=document.querySelector('#status');let timer;
for(const p of ['cole','decker','axel','yuri','maverick','freezer','falva','juggernaut','lizzie']){const o=document.createElement('option');o.value=p;o.textContent=p.toUpperCase();document.querySelector('#pilot').append(o);}
document.querySelectorAll('[data-scene]').forEach(btn=>btn.onclick=()=>{clearInterval(timer);f.hidden=false;status.textContent='Loading real engine…';const scene=btn.dataset.scene,pilot=document.querySelector('#pilot').value,coop=document.querySelector('#coop').checked;
 f.onload=()=>{let tries=0;timer=setInterval(()=>{const w=f.contentWindow;if(++tries>1200){clearInterval(timer);status.textContent='Load timed out.';return;}try{if(!w.eval('typeof dr5Warm==="function"'))return;w.eval('dr5Warm();aa5Warm();r30Warm();');if(!w.eval('Object.values(DR5_ART).every(a=>a.every(c=>XART.rdy(c.key)))'))return;
 w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};
 w.eval('('+setup+')('+JSON.stringify({stage:8,kind:'vileexistence',pilot,diff:'furious'})+');run.lives=9;run.missiles=100;player.invuln=120;Audio.init();Audio.resume();');
 if(coop)w.eval('coopOn=true;withSeat(2,()=>{run.pilot="decker";player.reset();player.x=worldWidth()/2+95;player.y=VH-135;});');
 const code={host:'on5FightStart(B);B._lastPart=B.parts[0];modularHit(B.hp+1);',ghost:'j3Encounter(B,1);on5FightStart(B);B._lastPart=B.parts[0];modularHit(B.hp+1);',speech:'j3Encounter(B,2);',combat:'j3Encounter(B,2);dr5State(B).introSeen=true;dr5State(B).introWanted=false;on5FightStart(B);',death:'j3Encounter(B,2);dr5State(B).introWanted=false;on5FightStart(B);const J=j3State(B);for(let i=1;i<J.hp.length;i++)J.hp[i]=0;J.active=0;J.mimic=null;B.hp=J.hp[0]=1;B._lastPart=B.parts[0];modularHit(10);'}[scene];w.eval(code);
 clearInterval(timer);status.textContent='Live '+scene+' sequence. Practice never writes campaign saves.';f.focus();
 }catch(e){clearInterval(timer);status.textContent='Practice failed: '+e.message;console.error(e);}},100);};f.src='../../index.html?dracodia-review='+Date.now();});
</script></html>'''.replace('BUTTONS',buttons).replace('VIDEOS',video).replace('SETUP',json.dumps(setup))
(O/'review.html').write_text(html,encoding='utf-8');print(O/'review.html')
