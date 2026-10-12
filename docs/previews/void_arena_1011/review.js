"use strict";
const byId=id=>document.getElementById(id),canvas=byId('code'),g=canvas.getContext('2d');
let frame=0,playing=!matchMedia('(prefers-reduced-motion: reduce)').matches,capture=playing,elapsed=0,last=0;
const sprites=AV11_ART.code.map(a=>{const im=new Image();im.src='../../../'+a.path;return im;});
function labels(){byId('capture-toggle').textContent=capture?'Pause capture':'Play capture';byId('capture-toggle').setAttribute('aria-pressed',String(capture));
 byId('code-toggle').textContent=playing?'Pause code':'Play code';byId('code-toggle').setAttribute('aria-pressed',String(playing));}
function captureView(){byId('battle').src='images/'+(capture?'battle-loop.webp':'battle-still.png');labels();}
byId('capture-toggle').onclick=()=>{capture=!capture;captureView();};
byId('code-toggle').onclick=()=>{playing=!playing;labels();};
byId('frame').oninput=e=>{frame=Number(e.target.value);playing=false;elapsed=0;labels();};
function draw(i,alpha){const im=sprites[(i+16)%16];if(!im.complete||!im.naturalWidth)return;
 g.globalAlpha=alpha;g.drawImage(im,40,40,320,320);g.globalAlpha=1;}
function loop(now){const dt=last?Math.min((now-last)/1000,.1):0;last=now;
 if(playing){elapsed+=dt;while(elapsed>=1/16){elapsed-=1/16;frame=(frame+1)%16;}byId('frame').value=String(frame);}
 g.clearRect(0,0,400,400);g.imageSmoothingEnabled=false;
 if(byId('onion').checked){draw(frame-2,.12);draw(frame-1,.24);}draw(frame,1);
 byId('frame-label').textContent=`Frame ${frame+1} / 16 · 320 × 320 · anchor 160, 160`;
 requestAnimationFrame(loop);
}
captureView();requestAnimationFrame(loop);
fetch('../../qa/void_arena_1011.json').then(r=>r.json()).then(q=>{
 byId('verification').textContent=`Verified: ${q.arena.passed} arena checks, ${q.finale.passed} existing finale checks, ${q.regression.passed.toLocaleString()} base assertions. Browser errors: ${q.arena.errors.length+q.finale.errors.length}.`;
}).catch(()=>{byId('verification').textContent='Verification record is being prepared.';});
