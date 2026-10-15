'use strict';
const bank=window.BOF_CHIP_AUDIO,entries=Object.entries(bank.cues),base='../../../'+bank.base;
const groups={'MISSING KEYS':'Alerts & feedback','WEAK SAMPLES':'Weapon fire & impacts','SYNTH-ONLY KEYS':'Combat & abilities'};
const el=id=>document.getElementById(id),audio=new Audio();audio.preload='none';audio.volume=.35;
let timer=null;
function stop(){clearTimeout(timer);audio.pause();el('now').textContent='Ready to audition';}
function play(key,seconds){
 stop();const cue=bank.cues[key];if(!cue)return;
 const v=seconds?bank.firewallVariants.reduce((a,b)=>Math.abs(Math.log(a.duration/seconds))<Math.abs(Math.log(b.duration/seconds))?a:b):null;
 audio.src=base+(v?.file||cue.file);audio.loop=!seconds&&cue.loop;audio.preservesPitch=true;audio.playbackRate=v?v.duration/seconds:1;
 el('now').textContent=key+(seconds?' · '+seconds.toFixed(2)+' s':cue.loop?' · loop':'');
 audio.play().then(()=>{if(seconds)timer=setTimeout(stop,seconds*1000);}).catch(e=>{el('now').textContent='Playback unavailable: '+e.message;});
}
for(const group of new Set(entries.map(([,d])=>d.group))){const option=document.createElement('option');option.textContent=groups[group]||group;option.value=group;el('group').append(option);}
function render(){
 const query=el('filter').value.trim().toLowerCase(),group=el('group').value;
 const filtered=entries.filter(([k,d])=>(!group||d.group===group)&&[k,d.target,d.group].join(' ').toLowerCase().includes(query));
 el('rows').replaceChildren();el('count').textContent=filtered.length+' / '+entries.length+' sounds';
 for(const [key,d] of filtered){
  const row=document.createElement('article');row.className='cue';
  const body=document.createElement('div'),tag=document.createElement('div');tag.className='group';tag.textContent=groups[d.group]||d.group;
  const h=document.createElement('h3');h.textContent=key;
  const p=document.createElement('p');p.textContent=d.duration.toFixed(2)+' s'+(d.loop?' · loop':'');
  const button=document.createElement('button');button.textContent='Play';button.setAttribute('aria-label','Play '+key);button.onclick=()=>play(key);
  body.append(tag,h,p);row.append(body,button);el('rows').append(row);
 }
}
el('filter').oninput=render;el('group').onchange=render;el('stop').onclick=stop;
el('volume').oninput=()=>audio.volume=Number(el('volume').value);
el('duration').oninput=()=>el('waveStatus').textContent=Number(el('duration').value).toFixed(2)+' s';
el('wave').onclick=()=>play('firewallLaunch',Number(el('duration').value));
document.querySelectorAll('[data-play]').forEach(b=>b.onclick=()=>play(b.dataset.play));
audio.onended=()=>el('now').textContent='Finished · '+(audio.src.split('/').pop()||'sound');
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);
render();
