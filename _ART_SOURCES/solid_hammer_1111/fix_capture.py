from pathlib import Path
W=Path(__file__).resolve().parent
p=W/'front_record_loaded.py'; s=p.read_text(); s=s[:s.index(" raw=O/(unit+'-hammer.webm')")]
s+='''
 # Step the real native loop and capture its rendered pixels. This avoids a stalled live MediaRecorder.
 import io
 from PIL import Image
 from shoot import STEP
 video=O/(unit+'-hammer.mp4'); encoder=imageio_ffmpeg.write_frames(str(video),(1280,800),fps=20,codec='libx264',quality=7,output_params=['-movflags','+faststart'])
 encoder.send(None); chapters=[]; seen=[]; total=0
 try:
  for material in ['regular','chrome']:
   chapters.append(dict(name=material,at=total/20))
   if stage==5:p.evaluate("m=>seed119('furious',m)",material)
   else:p.evaluate("m=>{diffKey='furious';DIFF=difficultyForRun(run.mode,diffKey);B._r30.mode='fight';B._r30.v18.donorAge=0;B.hp=B.maxhp;B.enter=B._noHit=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+200;Q.rf1110=null;Q.rage=false;Q.chrome=m==='chrome';Q.action=null;Q.cool=999;Q.speech=null;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;eBullets=[];pBullets=[];hb20Start(B,'skystrike');}",material)
   for i in range(140):
    err=p.evaluate(STEP,3); assert err is None,err
    p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}')
    encoder.send(Image.open(io.BytesIO(p.screenshot())).convert('RGB').tobytes());total+=1
    if i%20==0:
     q=p.evaluate("s=>{const p=s===5?ha21Blue(B):hb20Pose(B);return{bank:p?.a.bank,frame:p?.a.frame}}",stage);seen.append(dict(material=material,i=i,**q));print('Captured '+unit+' '+material+' '+str(i+1)+'/140',flush=True)
 finally: encoder.close()
 dst=O/'gifs'/f'{unit}-hammer.gif';vf='crop=750:800:265:0,scale=420:448:flags=neighbor,fps=20,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle'
 subprocess.run([ff,'-v','error','-y','-i',str(video),'-filter_complex',vf,'-loop','0',str(dst)],check=True)
 record=dict(unit=unit,video=str(video),seconds=total/20,chapters=chapters,frames=total,audioIncluded=False,method='Deterministic native game loop, one screenshot per three60Hz ticks; silent20FPS playback',sampledPoses=seen)
 (Path(__file__).resolve().parent/(unit+'-recording.json')).write_text(json.dumps(dict(records=[record],errors=errors),indent=2));p.close();print('Finished native frame-step capture '+unit,flush=True)
'''
p.write_text(s)
p=W/'verify_password.py';s=p.read_text().replace('outputs/Front-facing-hammer','outputs/Solid-metal-hammers');p.write_text(s)
print('Prepared bounded native frame-step capture and password output.')
