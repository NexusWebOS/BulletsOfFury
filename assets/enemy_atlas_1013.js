(()=>{'use strict';
 const $=s=>document.querySelector(s),el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n;};
 const labels={enemy:'Field enemies',miniboss:'Minibosses',boss:'Bosses','password-boss':'Password bosses',rebel:'Rebel fighters','boss-form':'Final boss forms','boss-phase':'Boss phases','alternate-boss':'Alternate bosses'};
 let data,selected,api,serial=0,paused=false,sound=false,motion=[],tiles=[],lastPaint=0,motionTime=0,lastTick=0,loading=false,archiveOnly=false;
 const frame=$('#engine'),imageCache=new Map();
 const readable=s=>String(s||'').replace(/[_-]/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
 const getApi=()=>{try{return frame.contentWindow.BOF_ENEMY_ATLAS;}catch(_){return null;}};
 const titleCategory=c=>labels[c]||readable(c);
 function sourceLink(s){const a=el('a',null,s.symbol||s.file);a.href=s.file+(s.line?'#L'+s.line:'');a.target='_blank';return a;}
 function imageFile(path){if(!imageCache.has(path)){const im=new Image();im.src=path;imageCache.set(path,im);}return imageCache.get(path);}
 function buildRoster(){const q=$('#search').value.trim().toLowerCase(),cat=$('#category').value,stage=$('#stage').value,legacy=$('#legacy').checked;
  const rows=data.entries.filter(e=>(legacy||['current','expansion'].includes(e.status))&&(cat==='all'||e.category===cat)&&(stage==='all'||e.stages.includes(+stage))&&(!q||JSON.stringify([e.name,e.id,e.projectileKinds,e.passwords,e.spawn.password,e.attacks]).toLowerCase().includes(q)));
  const root=$('#roster');root.replaceChildren();let group='';
  for(const e of rows){const g=(e.game==='overdrive'?'Overdrive · ':'')+titleCategory(e.category);if(g!==group){root.append(el('p','group-label',g));group=g;}
   const b=el('button',e.id===selected?.id?'active':'');b.type='button';b.dataset.id=e.id;
   if(e.spawn.password)b.append(el('span','roster-code',e.spawn.password));b.append(document.createTextNode(e.name));b.append(el('small',null,(e.stages.length?'STAGE '+e.stages.map(n=>n===10?'X':n).join(' / '):'ARCHIVE')+' · '+e.status));b.onclick=()=>select(e);root.append(b);
  }$('#count').textContent=rows.length+' dossiers shown';if(!rows.length)root.append(el('p','caption','No matches. Try a name, stage, or projectile.'));
 }
 function addAttack(a){const box=el('div','attack');box.append(el('strong',null,a.name||readable(a.id||a.pattern||a.pat||'Attack')));const text=a.description||a.detail||a.notes||a.behavior||a.summary;if(text)box.append(el('p',null,Array.isArray(text)?text.join(' '):text));
  const pieces=[];if(a.projectile||a.proj)pieces.push('Ordnance: '+(a.projectile||a.proj));if(a.cd)pieces.push('Base cadence: '+a.cd+'s');if(a.phase!=null)pieces.push('Phase '+(+a.phase+1));if(a.pattern)pieces.push('Pattern: '+readable(a.pattern));if(pieces.length)box.append(el('p',null,pieces.join(' · ')));$('#attacks').append(box);
 }
 function renderBriefing(e){$('#tag').textContent=(e.game==='overdrive'?'OVERDRIVE / ':'BULLETS OF FURY / ')+titleCategory(e.category).toUpperCase();$('#name').textContent=e.name;
  $('#identity').textContent=[e.stages.length?'Stage '+e.stages.map(n=>n===10?'X':n).join(', '):'Archive',e.spawn.password?'Password: '+e.spawn.password:(e.passwords||[]).join(' / '),e.id].filter(Boolean).join('  •  ');
  $('#attacks').replaceChildren();for(const a of e.attacks||[])addAttack(typeof a==='string'?{name:readable(a)}:a);
  if(!e.attacks?.length)addAttack({name:'Native combat sequence',description:'Watch the live viewport for this unit’s movement, firing tells, weapon effects, and recovery. The demonstration uses its own game controller.'});
  $('#warnings').replaceChildren();if(!['current','expansion'].includes(e.status))$('#warnings').append(el('p','note','Roster status: '+e.status+'. This design is retained for reference; the current campaign may use a replacement.'));
  if(e.runtime?.replacements&&Object.keys(e.runtime.replacements).length)$('#warnings').append(el('p','note','Current stage replacements: '+Object.entries(e.runtime.replacements).map(([k,v])=>k+' → '+v).join('; ')));
  $('#sources').replaceChildren();$('#sources').append(el('p',null,'Controller: '+(e.runtime?.controller||e.runtime?.nativeLaunch||'native encounter controller')));
  for(const s of e.sources||[]){const p=el('p');p.append(sourceLink(s),document.createTextNode(s.line?' · line '+s.line:''));$('#sources').append(p);}
  for(const k of e.artKeys||[])$('#sources').append(el('p',null,k));
  tiles=[];$('#projectiles').replaceChildren();updateProjectiles(e.projectileKinds||[],[]);
  motion=[];$('#animations').replaceChildren();motionTime=0;
  for(const bank of e.animationBanks||[])for(const name of ['heading','roll','idle','attack','fire','move']){const b=bank[name];if(!b)continue;const card=el('div','motion'),canvas=el('canvas');canvas.width=192;canvas.height=160;card.append(canvas,el('span',null,readable(name)),el('small',null,(b.frames?.length||b.frames||'?')+' authored frames'));$('#animations').append(card);motion.push({canvas,bank:b});}
  if(!motion.length){for(const key of(e.artKeys||[]).slice(0,3)){const card=el('div','motion'),canvas=el('canvas');canvas.width=192;canvas.height=160;card.append(canvas,el('span',null,readable(key)));$('#animations').append(card);motion.push({canvas,key});}}
  if(!motion.length)$('#animations').append(el('p','caption','This encounter uses a live rig or layered boss animation. Its complete animation is shown in the viewport above.'));
 }
 function updateProjectiles(kinds,observed){for(let kind of kinds){if(typeof kind!=='string')kind=kind.kind||kind.id;if(!kind||tiles.some(t=>t.kind===kind))continue;
   const card=el('div','projectile'),canvas=el('canvas');canvas.width=96;canvas.height=96;const mark=el('em',null,observed.includes(kind)?'LIVE':'WEAPON LIBRARY');card.append(canvas,el('span',null,kind),mark);$('#projectiles').append(card);tiles.push({kind,canvas,mark});}
  for(const t of tiles)if(observed.includes(t.kind))t.mark.textContent='LIVE';
 }
 async function select(e){const token=++serial;selected=e;loading=true;api=null;paused=false;sound=false;archiveOnly=!['current','expansion','legacy-spawnable'].includes(e.status);$('#pause').textContent='Ⅱ PAUSE';$('#sound').textContent='SOUND OFF';$('#hp').value=100;$('#hp-value').value='100%';$('#loading').hidden=false;$('#loading').textContent='LOADING '+e.name.toUpperCase()+'…';$('#pattern-controls').replaceChildren();renderBriefing(e);history.replaceState(null,'','#'+e.id);buildRoster();
  for(const id of ['pause','step','sound','hp'])$('#'+id).disabled=archiveOnly;
  const url=e.game==='overdrive'?'expansion/topdown/index.html?enemyAtlas=1':'index.html?bossmode=1&enemyAtlas=1';if(frame.getAttribute('src')!==url)frame.src=url;
  const began=performance.now();while(token===serial){api=getApi();const correctEngine=frame.contentWindow.location.pathname.endsWith(e.game==='overdrive'?'/expansion/topdown/index.html':'/index.html')&&(e.game==='overdrive'||!frame.contentWindow.location.pathname.includes('/expansion/'));if(correctEngine&&api?.ready)break;if(performance.now()-began>90000){$('#loading').textContent='The engine took too long to load. Use REPLAY to retry.';loading=false;return;}await new Promise(r=>setTimeout(r,100));}
  if(token!==serial)return;
  if(archiveOnly){api.pause(true);api.mute(true);loading=false;$('#loading').textContent='ARCHIVED DEFINITION — '+e.status.toUpperCase()+'. No verified live scene. Available artwork and source records are shown below.';$('#live-state').textContent='ARCHIVE / '+e.status;return;}
  const result=await api.start(e,$('#difficulty').value);if(token!==serial)return;loading=false;
  if(result?.error){$('#loading').textContent=result.error;return;}api.speed(+$('#speed').value);$('#loading').hidden=true;
  for(const kind of api.patterns||[]){const b=el('button',null,'▶ '+readable(kind));b.onclick=()=>api.pattern(kind);$('#pattern-controls').append(b);}
 }
 function drawBank(o){const c=o.canvas.getContext('2d'),b=o.bank;c.clearRect(0,0,o.canvas.width,o.canvas.height);c.imageSmoothingEnabled=false;if(o.key){api?.image(o.key,o.canvas);return;}
  if(b.kind==='strip'&&b.path){const im=imageFile(b.path);if(!im.complete||!im.naturalWidth)return;const cell=Array.isArray(b.cell)?b.cell:[b.cell,b.cell],f=Math.floor(motionTime*9)%b.frames,cols=Math.round(im.width/cell[0]),scale=Math.min(o.canvas.width/cell[0],o.canvas.height/cell[1]);c.drawImage(im,(f%cols)*cell[0],Math.floor(f/cols)*cell[1],cell[0],cell[1],(o.canvas.width-cell[0]*scale)/2,(o.canvas.height-cell[1]*scale)/2,cell[0]*scale,cell[1]*scale);
  }else if(b.kind==='frames'){const refs=b.refs||b.keys||b.frames;if(Array.isArray(refs)){const ref=refs[Math.floor(motionTime*10)%refs.length];api?.image(typeof ref==='string'?ref:ref.key,o.canvas);}}
 }
 function tick(t){requestAnimationFrame(tick);if(document.hidden||loading)return;const dt=lastTick?Math.min(.1,(t-lastTick)/1000):0;lastTick=t;if(!paused)motionTime+=dt*(+$('#speed').value);
  if(t-lastPaint<100)return;lastPaint=t;api=getApi();if(!api?.ready)return;if(archiveOnly){for(const o of motion)drawBank(o);return;}try{const s=api.snapshot();if(s.error){$('#loading').hidden=false;$('#loading').textContent=s.error;return;}
   updateProjectiles(s.projectiles||[],s.projectiles||[]);const visible=n=>{const r=n.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight;};api.projectiles?.(tiles.filter(t=>visible(t.canvas)));for(const o of motion)if(visible(o.canvas))drawBank(o);
   const a=s.actor;$('#hp').disabled=s.healthControl===false;$('#hp').title=s.healthControl===false?'This encounter manages health through its individual modules.':'Preview different health phases';if(s.healthControl===false)$('#hp-value').value='MODULES';$('#live-state').textContent=[s.paused?'PAUSED':'LIVE',s.elapsed!=null?s.elapsed.toFixed(1)+'s':'',a?.phase!=null?'phase '+a.phase:'',a?.pattern||'',s.liveProjectiles+' traveling shots',s.activeBeams?s.activeBeams+' active beams':''].filter(Boolean).join('  /  ');
  }catch(e){$('#live-state').textContent='Preview error: '+e.message;}}
 $('#pause').onclick=()=>{paused=!paused;api?.pause(paused);$('#pause').textContent=paused?'▶ PLAY':'Ⅱ PAUSE';};$('#step').onclick=()=>{paused=true;motionTime+=1/60;api?.step();$('#pause').textContent='▶ PLAY';};$('#replay').onclick=()=>selected&&select(selected);$('#difficulty').onchange=()=>selected&&select(selected);$('#speed').onchange=()=>api?.speed(+$('#speed').value);$('#sound').onclick=()=>{sound=!sound;api?.mute(!sound);$('#sound').textContent=sound?'SOUND ON':'SOUND OFF';};$('#hp').oninput=e=>{$('#hp-value').value=e.target.value+'%';api?.hp(e.target.value/100);};
 for(const id of ['search','category','stage','legacy'])$('#'+id).addEventListener(id==='search'?'input':'change',()=>buildRoster());
 document.addEventListener('visibilitychange',()=>api?.pause(document.hidden||paused));
 async function boot(){try{const r=await fetch('assets/data/enemy_atlas_1013.json');if(!r.ok)throw new Error('Roster file not available');data=await r.json();data.entries.sort((a,b)=>a.game.localeCompare(b.game)||a.category.localeCompare(b.category)||(a.stages[0]||99)-(b.stages[0]||99)||a.name.localeCompare(b.name));
   for(const c of [...new Set(data.entries.map(e=>e.category))]){const o=el('option',null,titleCategory(c));o.value=c;$('#category').append(o);}for(const n of [...new Set(data.entries.flatMap(e=>e.stages))].sort((a,b)=>a-b)){const o=el('option',null,'Stage '+(n===10?'X':n));o.value=n;$('#stage').append(o);}
   $('#total').textContent=data.entries.length+' DOSSIERS • BOF + OVERDRIVE';$('#coverage').textContent='Roster built from game registries, stage plans, password routes, native spawn audits, and animation manifests. One live engine is reused as you browse. Preview actions and saved-game writes stay in memory; your progress is untouched.';
   const initial=data.entries.find(e=>e.id===decodeURIComponent(location.hash.slice(1)))||data.entries.find(e=>e.id==='bof-enemy-mm1003_riflelocust')||data.entries[0];await select(initial);requestAnimationFrame(tick);
  }catch(e){$('#name').textContent='The atlas could not load';$('#loading').textContent=e.message;}}
 boot();
})();
