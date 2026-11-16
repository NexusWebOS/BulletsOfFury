(function(){
  'use strict';
  const config=window.BOF_ONLINE_CONFIG||{};
  const enabled=/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.url||'') &&
    /^sb_publishable_/.test(config.publishableKey||'');
  const actions=['left','right','up','down','fire','bomb','retina','charge','start'];
  const remote={hold:{},tap:{},at:0};
  let client=null,user=null,channel=null,room=null,peer=null,data=null,stream=null,frame=0;
  let role='',panel=null,statusNode=null,body=null,video=null,keys={},lastSent='',lastSentAt=0,pendingIce=[];
  let topScores=[];
  let submitRun=0,submitted=-1;
  const safe=s=>String(s||'').replace(/[^a-zA-Z0-9 _-]/g,'').slice(0,18);
  const status=s=>{if(statusNode)statusNode.textContent=s;};
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n;};
  const button=(label,fn)=>{const b=el('button','bof-online-btn',label);b.type='button';b.onclick=fn;return b;};
  const clear=()=>{if(body)body.replaceChildren();};

  function ensurePanel(){
    if(panel)return;
    const style=el('style');style.textContent=`
      #bof-online{position:fixed;inset:0;z-index:999990;background:#02050bdc;display:none;align-items:center;justify-content:center;color:#d9ecf8;font:17px BOFCommandSignal,monospace}
      #bof-online.open{display:flex}#bof-online .shell{width:min(92vw,650px);max-height:88vh;overflow:auto;background:#091522;border:4px solid #457899;box-shadow:0 0 0 4px #101a28,0 0 45px #00afff88;padding:18px}
      #bof-online h2{color:#ffbb59;margin:0 0 14px;font-size:26px}#bof-online .bar{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}#bof-online .muted{color:#8ba9bb;font-size:14px}
      #bof-online button,#bof-online input,#bof-online select{font:inherit}#bof-online button{cursor:pointer;background:#152d3f;border:2px solid #4e96c6;color:#ebf6ff;padding:8px 11px}#bof-online button:hover{border-color:#ffba43;color:#fff}
      #bof-online input,#bof-online select{background:#050f1c;color:#fff;border:2px solid #5686a7;padding:9px;max-width:95%}#bof-online .row{padding:8px 2px;border-bottom:1px solid #33506a}
      #bof-online video{width:100%;max-height:68vh;background:#000;object-fit:contain;image-rendering:pixelated}
    `;document.head.appendChild(style);
    panel=el('div');panel.id='bof-online';panel.tabIndex=-1;panel.setAttribute('role','dialog');panel.setAttribute('aria-label','Bullets of Fury online');
    const shell=el('div','shell'),head=el('div','bar');
    head.append(el('h2','', 'ONLINE OPERATIONS'),button('CLOSE',closePanel));
    shell.append(head);statusNode=el('div','muted','');shell.append(statusNode);
    body=el('div');shell.append(body);panel.append(shell);document.body.appendChild(panel);
    panel.addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Escape')closePanel();});
    panel.addEventListener('keyup',e=>e.stopPropagation());
  }
  function loadSDK(){
    if(window.supabase&&window.supabase.createClient)return Promise.resolve();
    return new Promise((resolve,reject)=>{
      const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
      s.onload=resolve;s.onerror=()=>reject(new Error('Supabase library did not load'));document.head.appendChild(s);
    });
  }
  async function connect(){
    if(!enabled)throw new Error('ColeForge online project is not connected yet');
    if(client&&user)return client;
    await loadSDK();
    client=window.supabase.createClient(config.url,config.publishableKey);
    let result=await client.auth.getUser();
    if(!result.data.user){
      const sign=await client.auth.signInAnonymously();
      if(sign.error)throw sign.error;
      result=await client.auth.getUser();
    }
    user=result.data.user;
    if(!user)throw new Error('Could not start an online pilot session');
    const session=await client.auth.getSession();
    if(session.data.session)client.realtime.setAuth(session.data.session.access_token);
    return client;
  }
  async function open(){
    ensurePanel();panel.classList.add('open');menu();panel.focus();
    if(enabled){status('CONNECTING TO COLEFORGE...');try{await connect();status('ONLINE PILOT READY');}catch(e){status('ONLINE UNAVAILABLE: '+e.message);}}
    else status('ONLINE SETUP PENDING — LOCAL CO-OP IS AVAILABLE');
  }
  function closePanel(){if(panel)panel.classList.remove('open');}
  function menu(){
    clear();const bar=el('div','bar');body.append(bar);
    bar.append(button('LOCAL CO-OP',()=>{closePanel();if(window.BOFOnlineGameStart)window.BOFOnlineGameStart();}));
    bar.append(button('HOST ONLINE',()=>host()));bar.append(button('JOIN ONLINE',()=>joinForm()));
    bar.append(button('LEADERBOARD',()=>ranks()));bar.append(button('ANNOUNCEMENTS',()=>announcements()));
    const callsign=el('input');callsign.maxLength=18;callsign.placeholder='LEADERBOARD CALLSIGN';
    try{callsign.value=localStorage.getItem('bof_callsign')||'';}catch(_){}
    callsign.onchange=()=>{callsign.value=safe(callsign.value);try{localStorage.setItem('bof_callsign',callsign.value);}catch(_){}};
    body.append(callsign);
    body.append(el('p','muted','Online co-op uses a private room code. The host chooses both pilots and the guest controls seat two.'));
  }
  async function ranks(){
    clear();body.append(button('BACK',menu));const select=el('select');
    for(const d of ['all','normal','hard','furious','insanity','easy']){const o=el('option','',d.toUpperCase());o.value=d;select.append(o);}body.append(select);
    const list=el('div');body.append(list);
    async function refresh(){
      list.textContent='LOADING...';try{await connect();let q=client.from('bof_scores').select('callsign,pilot,difficulty,stage,score').order('score',{ascending:false}).limit(20);
        if(select.value!=='all')q=q.eq('difficulty',select.value);
        const {data,error}=await q;if(error)throw error;list.replaceChildren();
        if(!data.length)list.append(el('p','muted','No scores yet.'));
        data.forEach((r,i)=>list.append(el('div','row',`${i+1}. ${safe(r.callsign)}  ${Number(r.score).toLocaleString()}  L${r.stage}  ${r.difficulty.toUpperCase()}  ${r.pilot.toUpperCase()}`)));
      }catch(e){list.textContent='LEADERBOARD UNAVAILABLE: '+e.message;}}
    select.onchange=refresh;refresh();
  }
  async function announcements(){
    clear();body.append(button('BACK',menu));const list=el('div','', 'LOADING...');body.append(list);
    try{await connect();const {data,error}=await client.from('bof_announcements').select('title,body,published_at').order('published_at',{ascending:false}).limit(10);
      if(error)throw error;list.replaceChildren();if(!data.length)list.append(el('p','muted','No announcements yet.'));
      data.forEach(a=>{const row=el('div','row');row.append(el('strong','',a.title),el('p','',a.body));list.append(row);});
    }catch(e){list.textContent='ANNOUNCEMENTS UNAVAILABLE: '+e.message;}
  }
  async function subscribe(topic){
    channel=client.channel(topic,{config:{private:true,broadcast:{self:false},presence:{key:user.id}}});
    channel.on('broadcast',{event:'signal'},({payload})=>signal(payload));
    await new Promise((resolve,reject)=>channel.subscribe((s,e)=>s==='SUBSCRIBED'?resolve():['CHANNEL_ERROR','TIMED_OUT','CLOSED'].includes(s)?reject(e||new Error('Room connection failed')):null));
    await channel.track({seat:role==='host'?1:2});
  }
  async function host(){
    clear();body.append(button('BACK',menu));status('CREATING ROOM...');
    try{await connect();const {data,error}=await client.rpc('bof_create_room');if(error)throw error;
      room=data[0];role='host';await subscribe(room.topic);status('ROOM READY — SHARE THE CODE WITH YOUR WINGMAN');
      body.append(el('h2','',room.join_code),el('p','muted','Keep this window open until your wingman joins.'));
      body.append(button('START TWO-PILOT RUN',()=>{closePanel();if(window.BOFOnlineGameStart)window.BOFOnlineGameStart();startCapture();}));
      body.append(button('CLOSE ROOM',()=>leave()));
    }catch(e){status('ROOM ERROR: '+e.message);}
  }
  function joinForm(){
    clear();body.append(button('BACK',menu));const input=el('input');input.maxLength=12;input.placeholder='12-CHARACTER ROOM CODE';input.autocomplete='off';
    body.append(input,button('JOIN',()=>join(input.value)));input.focus();
  }
  async function join(code){
    status('JOINING ROOM...');try{await connect();const {data,error}=await client.rpc('bof_join_room',{p_code:String(code||'').trim().toUpperCase()});if(error)throw error;
      room=data[0];role='guest';await subscribe(room.topic);clear();
      body.append(button('LEAVE ROOM',leave));video=el('video');video.autoplay=true;video.playsInline=true;video.muted=true;body.append(video);
      body.append(el('p','muted','WASD/ARROWS: FLY   SPACE/J: FIRE   K: MISSILE   C: RETINA   SHIFT: CHARGE   ENTER: PAUSE'));
      status('CONNECTED TO ROOM — WAITING FOR THE HOST');await send({kind:'hello'});
    }catch(e){status('JOIN FAILED: '+e.message);}
  }
  async function send(payload){if(channel)await channel.send({type:'broadcast',event:'signal',payload});}
  function newPeer(){
    peer=new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});
    peer.onicecandidate=e=>{if(e.candidate)send({kind:'ice',candidate:e.candidate.toJSON()});};
    peer.onconnectionstatechange=()=>{if(peer&&peer.connectionState==='failed')status('DIRECT CONNECTION FAILED — TRY ANOTHER NETWORK');};
    if(role==='guest')peer.ontrack=e=>{if(video)video.srcObject=e.streams[0];status('WINGMAN VIEW LIVE');};
    return peer;
  }
  async function signal(m){
    if(!m||!room)return;
    try{
      if(m.kind==='hello'&&role==='host'){
        if(peer)peer.close();newPeer();startCapture();if(stream)for(const track of stream.getTracks())peer.addTrack(track,stream);
        data=peer.createDataChannel('seat2',{ordered:false,maxRetransmits:0});data.onmessage=onInput;
        const offer=await peer.createOffer();await peer.setLocalDescription(offer);await send({kind:'offer',sdp:offer.sdp});status('WINGMAN JOINED — ESTABLISHING DIRECT LINK');
      }else if(m.kind==='offer'&&role==='guest'){
        if(peer)peer.close();newPeer();await peer.setRemoteDescription({type:'offer',sdp:m.sdp});
        peer.ondatachannel=e=>{data=e.channel;data.onopen=()=>status('WINGMAN CONTROLS LIVE');};
        const answer=await peer.createAnswer();await peer.setLocalDescription(answer);await send({kind:'answer',sdp:answer.sdp});
        for(const ice of pendingIce.splice(0))await peer.addIceCandidate(ice);
      }else if(m.kind==='answer'&&role==='host'&&peer){await peer.setRemoteDescription({type:'answer',sdp:m.sdp});
        for(const ice of pendingIce.splice(0))await peer.addIceCandidate(ice);
        status('WINGMAN CONTROLS LIVE');}
      else if(m.kind==='ice'){if(peer&&peer.remoteDescription)await peer.addIceCandidate(m.candidate);else pendingIce.push(m.candidate);}
    }catch(e){status('CO-OP LINK ERROR: '+e.message);}
  }
  function startCapture(){
    if(stream)return;const source=document.getElementById('screen'),hud=document.getElementById('hud');if(!source)return;
    const combined=document.createElement('canvas');combined.width=480;combined.height=574;const c=combined.getContext('2d',{alpha:false});
    let last=0;function draw(t){frame=requestAnimationFrame(draw);if(t-last<40)return;last=t;
      c.fillStyle='#020712';c.fillRect(0,0,480,574);if(hud)c.drawImage(hud,0,0,480,62);c.drawImage(source,0,62,480,512);
    }frame=requestAnimationFrame(draw);stream=combined.captureStream(24);
  }
  function onInput(e){
    try{const m=JSON.parse(e.data);if(!m||m.type!=='input')return;
      for(const a of actions){const next=!!m[a],old=!!remote.hold[a];remote.hold[a]=next;if(next&&!old)remote.tap[a]=true;}
      remote.at=performance.now();
    }catch(_badInput){}
  }
  function remoteHold(a){return role==='host'&&room&&performance.now()-remote.at<300&&!!remote.hold[a];}
  function remoteTap(a){if(role!=='host'||!room||performance.now()-remote.at>=300)return false;
    const on=!!remote.tap[a];remote.tap[a]=false;return on;}
  const keyAction={a:'left',ArrowLeft:'left',d:'right',ArrowRight:'right',w:'up',ArrowUp:'up',s:'down',ArrowDown:'down',
    j:'fire',' ':'fire',k:'bomb',c:'retina',Shift:'charge',Enter:'start'};
  function inputKey(e,on){if(role!=='guest'||!panel||!panel.classList.contains('open')||!video)return;
    const a=keyAction[e.key];if(!a)return;e.preventDefault();e.stopImmediatePropagation();keys[a]=on;sendInput();}
  function padInput(){
    const gp=navigator.getGamepads&&Array.from(navigator.getGamepads()).find(p=>p&&p.connected);
    if(!gp)return {};
    const b=i=>!!(gp.buttons[i]&&gp.buttons[i].pressed),x=gp.axes[0]||0,y=gp.axes[1]||0;
    return {left:x<-.3||b(14),right:x>.3||b(15),up:y<-.3||b(12),down:y>.3||b(13),
      fire:b(0)||b(7),bomb:b(1),retina:b(3),charge:b(2),start:b(9)};
  }
  function sendInput(){if(role!=='guest'||!data||data.readyState!=='open')return;
    const pad=padInput(),m={type:'input'};for(const a of actions)m[a]=!!keys[a]||!!pad[a];const json=JSON.stringify(m);
    if(json!==lastSent||performance.now()-lastSentAt>120){lastSent=json;lastSentAt=performance.now();data.send(json);}}
  document.addEventListener('keydown',e=>inputKey(e,true),true);document.addEventListener('keyup',e=>inputKey(e,false),true);
  setInterval(()=>{if(role==='guest')sendInput();},80);
  async function leave(){
    if(role==='host'&&room&&client)try{await client.rpc('bof_close_room',{p_room:room.room_id});}catch(_){}
    if(role==='guest'&&room&&client)try{await client.rpc('bof_leave_room',{p_room:room.room_id});}catch(_){}
    if(channel&&client)await client.removeChannel(channel);channel=null;
    if(peer)peer.close();peer=null;if(data)data.close();data=null;
    if(stream){stream.getTracks().forEach(t=>t.stop());stream=null;}if(frame)cancelAnimationFrame(frame);frame=0;
    room=null;role='';video=null;pendingIce=[];remote.hold={};remote.tap={};menu();status('ROOM CLOSED');
  }
  async function refreshTop(){
    try{await connect();const {data,error}=await client.from('bof_scores').select('callsign,score').order('score',{ascending:false}).limit(4);
      if(error)throw error;topScores=data||[];
    }catch(_offline){topScores=[];}
  }
  function submitScore(meta){
    if(submitted===submitRun||!meta||!Number.isFinite(meta.score)||meta.score<=0)return;
    submitted=submitRun;
    connect().then(async()=>{
      let name='';try{name=safe(localStorage.getItem('bof_callsign'));}catch(_){}
      const row={user_id:user.id,pilot:meta.pilot,callsign:name.length>=2?name:safe(meta.pilot||'PILOT'),
        difficulty:meta.difficulty,mode:meta.mode,stage:meta.stage,score:Math.floor(meta.score)};
      const {error}=await client.from('bof_scores').insert(row);if(error)console.warn('Online score submission:',error.message);else refreshTop();
    }).catch(e=>console.warn('Online score submission:',e.message));
  }
  window.BOFOnline={open,close:closePanel,remoteHold,remoteTap,submitScore,startRun:()=>{submitRun++;submitted=-1;},
    get active(){return role==='host'&&!!room;},get connected(){return !!user;},get topScores(){return topScores;}};
  if(enabled){refreshTop();setInterval(refreshTop,60000);}
})();
