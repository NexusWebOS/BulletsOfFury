"use strict";
(() => {
  const root='../../../',$=id=>document.getElementById(id),ART=PL11_ART;
  const main=['amethyst_gate','black_void','blue_rift','red_rift','green_rift'];
  const short={amethyst_gate:'Fury breach gate',black_void:'Chromium void',blue_rift:'Ion-blue rift',red_rift:'Crimson rift',green_rift:'Emerald rift'};
  const descriptions={
    amethyst_gate:'The violet membrane turns a full circle as it forms inside the stationary armored frame. Closing leaves the machinery standing.',
    black_void:'Black chromium unfolds and turns around the throat. Closing pinches the hole shut, pulling the ribs into a violet implosion.',
    blue_rift:'Blue plasma turns a full circle as the rift forms, settling smoothly into its open loop. Closing draws the blades inward into fading sparks.',
    red_rift:'Crimson ignition spins into a scarlet plasma loop, then collapses inward. Its aperture stays centered throughout the turn.',
    green_rift:'Emerald ignition turns into jade plasma with mint-white arcs. Its circular formation settles into the green open loop.'
  };
  const images={},byKey={},thumbnails={},canvas=$('stage'),ctx=canvas.getContext('2d');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const state={bank:'blue_rift',mode:'sequence',time:0,frame:0,phase:'form',playing:!reduced,speed:1,
    onion:false,anchor:false,seam:false,blend:true,backdrop:'dark',ready:false};
  let last=0,arena=null;
  const load=path=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error('Could not load '+path));im.src=root+path;});
  function timing(){const d=32/ART[state.bank].fps;return {form:d,loop:2*d,close:d};}
  function total(){return 128/ART[state.bank].fps;}
  function current(){return state.mode==='sequence'?PL11.sequence(state.bank,state.time,{...timing(),blend:state.blend}):PL11.sample(state.bank,state.mode,state.time,{blend:state.blend});}
  function backdrop(g,w,h){
    g.globalAlpha=1;g.globalCompositeOperation='source-over';g.fillStyle=state.backdrop==='dark'?'#030508':'#15212b';g.fillRect(0,0,w,h);
    if(state.backdrop==='checker'){g.fillStyle='#26333e';for(let y=0;y<h;y+=32)for(let x=0;x<w;x+=32)if((x/32+y/32)%2===0)g.fillRect(x,y,32,32);}
    else if(state.backdrop==='arena'&&arena){const k=Math.max(w/arena.width,h/arena.height);g.drawImage(arena,(w-arena.width*k)/2,(h-arena.height*k)/2,arena.width*k,arena.height*k);}
  }
  function marker(g,x,y){g.save();g.strokeStyle='#94ffc3';g.lineWidth=1;g.beginPath();g.moveTo(x-11,y+.5);g.lineTo(x+11,y+.5);g.moveTo(x+.5,y-11);g.lineTo(x+.5,y+11);g.stroke();g.restore();}
  function paint(g,pose,x,y,size,alpha=1){return PL11.draw(g,pose,x,y,size,key=>byKey[key],alpha);}
  function draw(){
    backdrop(ctx,768,768);ctx.imageSmoothingEnabled=false;
    const pose=current();state.phase=pose.phase;state.frame=pose.from;
    const size=state.bank==='amethyst_gate'?512:640;
    paint(ctx,pose,384,408,size);
    if(state.onion){
      ctx.globalCompositeOperation='screen';
      for(const delta of [-1,1]){
        const f=pose.phase==='loop'?(pose.from+32+delta)%32:Math.max(0,Math.min(31,pose.from+delta));
        const t=pose.phase==='loop'?f/ART[state.bank].fps:f/31*pose.duration;
        paint(ctx,PL11.sample(state.bank,pose.phase,t,{duration:pose.duration,blend:false}),384,408,size,.24);
      }ctx.globalCompositeOperation='source-over';
    }
    if(state.anchor)marker(ctx,384,408);
    for(const bank of main){const g=thumbnails[bank].getContext('2d');g.fillStyle='#030508';g.fillRect(0,0,256,224);
      paint(g,PL11.sample(bank,'loop',state.time),128,122,bank==='amethyst_gate'?164:256);}
    $('frame').max=state.mode==='sequence'?128:31;
    $('frame').value=state.mode==='sequence'?Math.min(128,state.time*ART[state.bank].fps):pose.from;
    $('frameNumber').textContent=String(pose.from+1).padStart(2,'0')+' / 32';
    $('playState').textContent=(state.playing?'PLAYING':'PAUSED')+' · '+pose.phase.toUpperCase()+(pose.done?' · COMPLETE':'');
    $('play').textContent=state.playing?'Pause':pose.done?'Replay':'Play';
    $('pivotText').textContent='FIXED APERTURE';
    const clip=ART[state.bank][pose.phase];
    $('sheetLink').href=root+clip.sheet.path;$('loopLink').href=root+clip.webp;
    $('activePhase').textContent=pose.phase==='form'?'FORMING':pose.phase==='loop'?'OPEN LOOP':'CLOSING';
  }
  function select(bank){
    state.bank=main.includes(bank)?bank:'blue_rift';state.time=0;
    const art=ART[state.bank],f=art.form.frames[0];
    $('title').textContent=art.label;$('stageLabel').textContent=short[state.bank].toUpperCase();$('description').textContent=descriptions[state.bank];
    $('specs').replaceChildren(...[f.w+' × '+f.h,'32 + 32 + 32 frames',art.fps+' fps','pivot '+f.pivot.join(', ')].map(s=>{const e=document.createElement('span');e.textContent=s;return e;}));
    $('refLink').href=root+'_ART_SOURCES/portals_bof_1011/reference/bof-style-board.png';
    for(const b of $('banks').children)b.setAttribute('aria-pressed',String(b.dataset.bank===state.bank));
    const url=new URL(location.href);url.searchParams.set('effect',state.bank);history.replaceState(null,'',url);draw();
  }
  function mode(value){state.mode=['sequence','form','loop','close'].includes(value)?value:'sequence';state.time=0;state.seam=false;$('seam').checked=false;$('seam').disabled=state.mode!=='loop';$('mode').value=state.mode;state.playing=!reduced;draw();}
  for(const bank of main){const b=document.createElement('button');b.className='bank';b.dataset.bank=bank;b.setAttribute('aria-pressed','false');
    const cv=document.createElement('canvas');cv.width=256;cv.height=224;cv.setAttribute('aria-hidden','true');thumbnails[bank]=cv;
    const label=document.createElement('span');label.textContent=short[bank];const sub=document.createElement('small');sub.textContent='Form · loop · close';label.append(sub);b.append(cv,label);b.onclick=()=>select(bank);$('banks').append(b);}
  function step(delta){state.playing=false;const fps=ART[state.bank].fps;
    if(state.mode==='sequence')state.time=Math.max(0,Math.min(total(),state.time+delta/fps));
    else {const f=current().from,n=state.mode==='loop'?(f+32+delta)%32:Math.max(0,Math.min(31,f+delta));
      state.time=state.mode==='loop'?n/fps:n/31*(32/fps);}
    draw();}
  $('play').onclick=()=>{if(current().done)state.time=0;state.playing=!state.playing;last=0;draw();};
  $('prev').onclick=()=>step(-1);$('next').onclick=()=>step(1);
  $('frame').oninput=e=>{state.playing=false;const n=Number(e.target.value),fps=ART[state.bank].fps;
    state.time=state.mode==='sequence'?n/fps:state.mode==='loop'?n/fps:n/31*(32/fps);draw();};
  $('mode').onchange=e=>mode(e.target.value);$('speed').onchange=e=>{state.speed=Number(e.target.value);draw();};
  $('backdrop').onchange=e=>{state.backdrop=e.target.value;draw();};
  for(const key of ['onion','anchor','blend'])$(key).onchange=e=>{state[key]=e.target.checked;draw();};
  $('seam').onchange=e=>{state.seam=e.target.checked;state.time=28/ART[state.bank].fps;draw();};
  document.addEventListener('keydown',e=>{if(e.target.matches('input,select,button,a'))return;if(e.code==='Space'){e.preventDefault();$('play').click();}else if(e.key==='ArrowRight')step(1);else if(e.key==='ArrowLeft')step(-1);});
  document.addEventListener('visibilitychange',()=>{last=0;});
  function advance(dt){if(!state.ready||!state.playing||document.hidden)return;
    const fps=ART[state.bank].fps;state.time+=Math.max(0,Math.min(.1,dt))*state.speed;
    if(state.seam&&state.mode==='loop'&&state.time>=36/fps)state.time=28/fps+(state.time-36/fps);
    if(state.mode==='sequence'&&state.time>=total()){state.time=total();state.playing=false;}
    else if(state.mode!=='sequence'&&state.mode!=='loop'&&state.time>=32/fps){state.time=32/fps;state.playing=false;}
    draw();
  }
  window.PORTAL_REVIEW={state,draw,select,mode,images,current,advance};
  select(new URLSearchParams(location.search).get('effect'));mode(new URLSearchParams(location.search).get('phase')||'sequence');
  const framesReady=Promise.all(main.map(async bank=>{images[bank]={};await Promise.all(PL11.phases.map(async phase=>{
    images[bank][phase]=await Promise.all(ART[bank][phase].frames.map(async f=>{const im=await load(f.path);byKey[f.key]=im;return im;}));
  }));}));
  const gateReady=Promise.all([...ART.gate_energy.form.frames.map(f=>[f.key,f.path]),...Object.entries(PL11.parts)]
    .map(async([key,path])=>{byKey[key]=await load(path);}));
  Promise.all([framesReady,gateReady]).then(async()=>{arena=await load('assets/game/levels/stage_08/stage/void_arena_1011/void-depth.png');state.ready=true;$('play').disabled=false;$('loadStatus').textContent='480 main frames + rotating gate components loaded · shared game playback';draw();})
    .catch(err=>{state.playing=false;$('loadStatus').textContent=err.message;$('loadStatus').className='note error';console.error(err);});
  function tick(time){const dt=last?(time-last)/1000:0;last=time;advance(dt);requestAnimationFrame(tick);}requestAnimationFrame(tick);
})();
