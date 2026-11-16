from pathlib import Path
R=Path(__file__).resolve().parents[1];P=Path(__file__).with_name('night_position_1116.py');s=P.read_text(encoding='utf8')
s=s.replace("/position'","/position-more'").replace("[(1,'hard'),(4,'normal'),(4,'hard'),(4,'furious'),(6,'hard'),(9,'hard')]","[(2,'hard'),(3,'hard'),(5,'hard'),(7,'hard'),(8,'hard'),(8,'furious')]")
s=s.replace("p.on('pageerror'", "p.on('response',lambda r:err.append(str(r.status)+' '+r.url.split('?')[0])if r.status>=400 else None);p.on('pageerror'")
s=s.replace("await p.evaluate('''()=>{if(!run.spaceMode)", "await p.evaluate('''()=>{const base=ctx.drawImage;window.QRect16={calls:0,bad:[]};ctx.drawImage=function(im,...a){QRect16.calls++;const W=im.naturalWidth||im.videoWidth||im.width,H=im.naturalHeight||im.videoHeight||im.height;if(a.length===8&&(a[0]<0||a[1]<0||a[0]+a[2]>W+.01||a[1]+a[3]>H+.01)&&QRect16.bad.length<30)QRect16.bad.push({size:[W,H],rect:a.slice(0,4),stack:new Error().stack});return base.call(this,im,...a);};if(!run.spaceMode)")
s=s.replace("p.evaluate('()=>QPOS16')", "p.evaluate('()=>({...QPOS16,sourceRectAudit:QRect16})')")
s=s.replace("'noBrowserErrors':not err", "'noBrowserErrors':not err,'noInvalidSources':not q['sourceRectAudit']['bad']")
(R/'_BUILD_SOURCE/night_position_more_1116.py').write_text(s,encoding='utf8',newline='\n')
