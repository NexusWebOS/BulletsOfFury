from pathlib import Path
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');f=R/'assets/online.js';s=f.read_text(encoding='utf8');(R/'_ART_SOURCES/release_qa_1116/online.js.capture-before').write_bytes(f.read_bytes())
s=s.replace("let captureAudio=null;","let captureAudio=null,started=false;")
s=s.replace("    if(room){body.append(el('p','muted',role==='host'?'YOUR PRIVATE ROOM IS STILL OPEN':'YOUR WINGMAN LINK IS STILL OPEN'));body.append(button(role==='host'?'CLOSE ROOM':'LEAVE ROOM',leave));}","""    if(room){
      body.append(el('p','muted',role==='host'?'YOUR PRIVATE ROOM IS STILL OPEN':'YOUR WINGMAN LINK IS STILL OPEN'));
      if(role==='host')body.append(button(started?'RESUME GAME':'START TWO-PILOT RUN',startHostedRun));
      else if(video)body.append(video);
      body.append(button(role==='host'?'CLOSE ROOM':'LEAVE ROOM',leave));return;
    }""")
s=s.replace("  async function host(){\n", "  function startHostedRun(){closePanel();if(!started){started=true;if(window.BOFOnlineGameStart)window.BOFOnlineGameStart();}startCapture();}\n  async function host(){\n")
s=s.replace("body.append(button('START TWO-PILOT RUN',()=>{closePanel();if(window.BOFOnlineGameStart)window.BOFOnlineGameStart();startCapture();}));", "body.append(button('START TWO-PILOT RUN',startHostedRun));")
s=s.replace("if(role==='guest')peer.ontrack=e=>{if(video){video.srcObject=e.streams[0];video.play().catch(()=>{if(video&&body){status('PRESS PLAY TO ENABLE WINGMAN AUDIO');body.append(button('PLAY GAME AUDIO',()=>video&&video.play()));}});}status('WINGMAN VIEW LIVE');};", """if(role==='guest')peer.ontrack=e=>{if(video&&video.srcObject!==e.streams[0]){video.srcObject=e.streams[0];video.play().catch(err=>{if(err.name==='NotAllowedError'&&video&&body&&!body.querySelector('[data-online-audio]')){status('PRESS PLAY TO ENABLE WINGMAN AUDIO');const play=button('PLAY GAME AUDIO',()=>video&&video.play());play.dataset.onlineAudio='1';body.append(play);}});}status('WINGMAN VIEW LIVE');};""")
s=s.replace("if(stream)for(const track of stream.getTracks())peer.addTrack(track,stream);", """if(stream)for(const track of stream.getTracks()){
          const sender=peer.addTrack(track,stream);
          if(track.kind==='video'){track.contentHint='detail';const p=sender.getParameters();p.degradationPreference='maintain-resolution';p.encodings=p.encodings?.length?p.encodings:[{}];p.encodings[0].maxBitrate=6000000;p.encodings[0].maxFramerate=30;p.encodings[0].scaleResolutionDownBy=1;sender.setParameters(p).catch(()=>{});}
        }""")
s=s.replace("room=null;role='';video=null;", "room=null;role='';started=false;video=null;")
assert 'function startHostedRun' in s and 'err.name===' in s
f.write_text(s,encoding='utf8',newline='\n');print('Retained active-room controls and corrected stream-play race.')
