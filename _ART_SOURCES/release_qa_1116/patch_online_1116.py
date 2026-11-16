from pathlib import Path
import hashlib,json
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');A=R/'_ART_SOURCES/release_qa_1116';A.mkdir(parents=True,exist_ok=True)
f=R/'assets/online.js';old=f.read_text(encoding='utf8');(A/'online.js.before').write_bytes(f.read_bytes())
new=old.replace("let topScores=[];","let topScores=[];\n  let captureAudio=null;")
new=new.replace("    clear();const bar=el('div','bar');body.append(bar);","    clear();const bar=el('div','bar');body.append(bar);\n    if(room){body.append(el('p','muted',role==='host'?'YOUR PRIVATE ROOM IS STILL OPEN':'YOUR WINGMAN LINK IS STILL OPEN'));body.append(button(role==='host'?'CLOSE ROOM':'LEAVE ROOM',leave));}",1)
new=new.replace("video.playsInline=true;video.muted=true;body.append(video);","video.playsInline=true;video.muted=false;body.append(video);")
new=new.replace("if(role==='guest')peer.ontrack=e=>{if(video)video.srcObject=e.streams[0];status('WINGMAN VIEW LIVE');};","""if(role==='guest')peer.ontrack=e=>{if(video){video.srcObject=e.streams[0];video.play().catch(()=>{if(video&&body){status('PRESS PLAY TO ENABLE WINGMAN AUDIO');body.append(button('PLAY GAME AUDIO',()=>video&&video.play()));}});}status('WINGMAN VIEW LIVE');};""")
start=new.index('  function startCapture(){');end=new.index('  function onInput(e){',start)
new=new[:start]+'''  function startCapture(){
    if(stream)return;const source=document.getElementById('screen');if(!source)return;
    // The current Siege HUD lives on separate visible canvases. Compose the
    // host's actual layout; the retired hidden #hud is not the player's HUD.
    const combined=document.createElement('canvas');combined.width=1824;combined.height=1024;
    const c=combined.getContext('2d',{alpha:false});c.imageSmoothingEnabled=false;
    const ids=['screen','siege-left','siege-right','siege-compact','hud-top','hud-bot','equipcv','wide-left','wide-right','wide-clock'];
    let last=0;function draw(t){frame=requestAnimationFrame(draw);if(t-last<1000/30)return;last=t;
      const layers=ids.map(id=>document.getElementById(id)).filter(Boolean).map(canvas=>{
        let opacity=1;for(let n=canvas;n;n=n.parentElement){const s=getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden')opacity=0;opacity*=Number(s.opacity);}
        return{canvas,r:canvas.getBoundingClientRect(),opacity};
      }).filter(v=>v.opacity>0&&v.r.width>0&&v.r.height>0);
      c.globalAlpha=1;c.fillStyle='#020712';c.fillRect(0,0,combined.width,combined.height);
      if(!layers.length)return;
      const x=Math.min(...layers.map(v=>v.r.left)),y=Math.min(...layers.map(v=>v.r.top)),
        w=Math.max(...layers.map(v=>v.r.right))-x,h=Math.max(...layers.map(v=>v.r.bottom))-y,
        k=Math.min(combined.width/w,combined.height/h),ox=(combined.width-w*k)/2,oy=(combined.height-h*k)/2;
      for(const v of layers){c.globalAlpha=v.opacity;c.drawImage(v.canvas,Math.round(ox+(v.r.left-x)*k),Math.round(oy+(v.r.top-y)*k),Math.round(v.r.width*k),Math.round(v.r.height*k));}c.globalAlpha=1;
    }draw(performance.now());stream=combined.captureStream(30);
    // Mirror the existing native mixer, including music, without creating a
    // second local speaker route or changing the host's volume settings.
    try{if(typeof Snd!=='undefined'&&typeof aq112Bus==='function'){
      const ac=Snd._audioCtx(),output=aq112Bus().output,destination=ac.createMediaStreamDestination();
      output.connect(destination);captureAudio={output,destination};
      for(const track of destination.stream.getAudioTracks())stream.addTrack(track);
      ac.resume().catch(()=>{});
    }}catch(e){console.warn('Online audio capture:',e.message);}
  }
''' + new[end:]
new=new.replace("if(stream){stream.getTracks().forEach(t=>t.stop());stream=null;}if(frame)","if(captureAudio){try{captureAudio.output.disconnect(captureAudio.destination);}catch(_){}captureAudio=null;}\n    if(stream){stream.getTracks().forEach(t=>t.stop());stream=null;}if(frame)")
new=new.replace("room=null;role='';video=null;pendingIce=[];remote.hold={};remote.tap={};menu();","room=null;role='';video=null;pendingIce=[];keys={};lastSent='';lastSentAt=0;remote.hold={};remote.tap={};remote.at=0;menu();")
new=new.replace("  setInterval(()=>{if(role==='guest')sendInput();},80);","  setInterval(()=>{if(role==='guest')sendInput();},80);\n  window.addEventListener('blur',()=>{keys={};lastSent='';sendInput();});\n  document.addEventListener('visibilitychange',()=>{if(document.hidden){keys={};lastSent='';sendInput();}});")
assert new!=old and 'combined.height=574'not in new
f.write_text(new,encoding='utf8',newline='\n')
(A/'online-change.json').write_text(json.dumps({'file':'assets/online.js','before':hashlib.sha256(old.encode()).hexdigest(),'after':hashlib.sha256(f.read_bytes()).hexdigest()},indent=2),encoding='utf8')
print('Updated native online capture, audio, room access and input cleanup.')
