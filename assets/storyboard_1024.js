"use strict";
/* Storyroom edits narrative data only. Native callbacks still own progression,
   rewards, combat clocks and aircraft. Empty data is an exact native pass-through. */
const SB24={finaleDuration:IP21.end-IP21.finaleAt,data:globalThis.BOF_STORYBOARD_DATA,base:{play:BOFCinematicDirector.play,
 intro:campaignIntroStart,line:ip21Line,finale:ip21Finale,block:msgDrawBlock,
 ending:inv20Draw,caption:inv20Text},intro:IP21.beats.map(b=>({...b})),
 dr5:DR5.intro.map(b=>[...b]),shots:INV20.shots.map(b=>[...b]),end:INV20.end,
 observed:new Map(),previewing:false,preview:null,endingRow:null};
const sb24Clone=o=>JSON.parse(JSON.stringify(o));
function sb24Id(id){return String(id).replace(/^(preview-|review-)/,'');}
function sb24Rows(id,pilot,native){const target=SB24.data?.triggers?.[id]||id;
 const edit=SB24.data?.overrides?.[target]?.[pilot];if(!edit)return (target===id?native:sb24Native(target,pilot)).map(b=>({...b}));
 const source=target===id?native:sb24Native(target,pilot);
 return edit.filter(c=>c.enabled!==false).map(c=>{const row={...(source[c.source]||{})};
  for(const k of c.edited||[])if(Object.hasOwn(c.fields,k))row[k]=c.fields[k];if((c.edited||[]).includes('text'))row._sbText=true;if((c.edited||[]).includes('who'))row._sbWho=true;
  if(c.source<0)Object.assign(row,c.fields);return row;});
}
function sb24Native(id,pilot){const old=run.pilot;run.pilot=pilot;
 try{
  if(id==='opening')return SB24.intro.map(b=>({...b,who:b.who||(b.pilotLine?pilot.toUpperCase():''),text:SB24.base.line(b,{pilot})}));
  if(id==='opening-finale'){const name=PILOTS.find(p=>p.key===pilot)?.name||pilot;
   return [{who:'NARRATOR',text:`Detecting anomalies over the mysterious jungle, ${name} sets off to find answers while ${['lizzie','falva'].includes(pilot)?'her':'his'} communications system is down.`},{who:'NARRATOR',text:"Good luck Commander. You'll need it."}];}
  if(/^post-[1-9]$/.test(id))return BOFCinematicDirector.script(Number(id.slice(5)),pilot);
  if(id==='cronos')return BOFCinematicDirector.cronos();
  if(id.startsWith('route-'))return BOFCinematicDirector.routeScript(id.slice(6),pilot);
  if(id==='rebel-contact')return BOFCinematicDirector.rebelScript(pilot);
  if(id.startsWith('stage-x-'))return BOFCinematicDirector.rebelScript(pilot,id.slice(8));
  if(id==='stage7-approach')return cr17Approach();
  if(id==='dracodia-monologue')return SB24.dr5.map(([text,expression])=>({who:'DRACODIA',text,expression}));
  if(id==='ending')return sb24EndingNative(pilot);
  if(SB24.transitions?.[id])return SB24.transitions[id].map(b=>({...b,who:b.who==='$PILOT'?pilot.toUpperCase():b.who==='$CONTACT'?(pilot==='decker'?'COLE':'DECKER'):b.who,art:DR5_ART.portrait[0].key}));
  return SB24.observed.get(id)?.map(b=>({...b}))||[];
 }finally{run.pilot=old;}
}
BOFCinematicDirector.play=function(id,beats,done,live=false){const key=sb24Id(id);if(BOFCinematicDirector.current)return false;
 if(!SB24.previewing)SB24.observed.set(key,beats.map(b=>({...b})));
 const rows=SB24.previewing?beats:sb24Rows(key,run.pilot,beats);
 // A disabled sequence still completes through its original callback once.
 if(!rows.length){if(done)done();return true;}
 Snd.prepare([...new Set(rows.map(b=>b.c22Cue).filter(Boolean))]);return SB24.base.play.call(this,id,rows,done,live);
};
// Read the actual trap conversation, without starting a scene or its callback.
{const play=BOFCinematicDirector.play;try{BOFCinematicDirector.play=(id,rows)=>{SB24.observed.set(id,rows);return false;};fb1002HammerDialogue({_hammer:{}});}finally{BOFCinematicDirector.play=play;}}
ip21Line=function(b,c){return b._sbText?b.text:SB24.base.line(b,c);};
SB24.base.introCaption=ip21Caption;ip21Caption=function(b,c){if(b._sbWho)b={...b,pilotLine:null,text:ip21Line(b,c)};return SB24.base.introCaption.call(this,b,c,...Array.from(arguments).slice(2));};
function sb24InstallIntro(pilot){const rows=sb24Rows('opening',pilot,sb24Native('opening',pilot));let t=0;
 for(const b of rows){
  b.duration=Math.max(.25,b.duration||5.5,(b.text||'').length/CAMPAIGN_INTRO_CPS+CAMPAIGN_INTRO_READ_HOLD);
  b.at=t;b.to=t+=b.duration;}
 IP21.beats=rows;IP21.finaleAt=t;IP21.end=t+SB24.finaleDuration;
 const mon=sb24Rows('dracodia-monologue',pilot,sb24Native('dracodia-monologue',pilot));
 SB24.monologue=mon;DR5.intro.splice(0,DR5.intro.length,...(mon.length?mon:[{text:'',expression:0}]).map(b=>[b.text,b.expression||0]));
 const ending=sb24Rows('ending',pilot,sb24Native('ending',pilot));
 SB24.ending=ending;INV20.end=26.4+ending.reduce((t,b)=>t+(b.duration||5),0);
}
campaignIntroStart=function(){if(SB24.data&&Object.keys(SB24.data.overrides||{}).length)sb24InstallIntro(run.pilot);return SB24.base.intro.apply(this,arguments);};
SB24.base.begin=beginStage;beginStage=function(){const r=SB24.base.begin.apply(this,arguments);
 if(SB24.data&&Object.keys(SB24.data.overrides||{}).length)sb24InstallIntro(run.pilot);return r;};
ip21Finale=function(){const old=SB24.finaleLine;SB24.finaleLine=0;try{return SB24.base.finale.apply(this,arguments);}finally{SB24.finaleLine=old;}};
msgDrawBlock=function(o){if(SB24.finaleLine!=null&&SB24.data?.overrides?.['opening-finale']?.[run.pilot]){
 const rows=sb24Rows('opening-finale',run.pilot,sb24Native('opening-finale',run.pilot)),b=rows[SB24.finaleLine++];
 if(b){o={...o,text:b.text,budget:Math.min(b.text.length,Math.floor((o.budget||0)/Math.max(1,o.text.length)*b.text.length))};}}
 return SB24.base.block.call(this,o);};
function sb24EndingNative(pilot){if(SB24.endingCache?.[pilot])return sb24Clone(SB24.endingCache[pilot]);
 const out=[],draw=inv20Text,oldPilot=run.pilot;run.pilot=pilot;
 try{inv20Text=(who,text)=>{SB24.capture={who,text};};
  for(const [name,start,end]of SB24.shots){if(!Number.isFinite(end))continue;
   const chunks=name==='federation'?3:1,dur=(end-start)/chunks;
   for(let i=0;i<chunks;i++){SB24.capture=null;
    // The production renderer selects the real authored dialogue, including pilot variants.
    SB24.base.ending(start+i*dur+.2,VW,VH,{});
    const bgName={report:'hq_regroup',relief:'hq_regroup',alarm:'hq_alarm',federation:'earth_invasion',horror:'hq_alarm',base:'air_invasion',waters:'coast_invasion',earth:'earth_invasion',solar:'solar',growth:'solar',scream:'solar',escape:'solar',return:'hq_hangar',credits:'hq_regroup'}[name];
    out.push({who:SB24.capture?.who||'',text:SB24.capture?.text||'',duration:dur,bg:C22_ART.images[bgName]?.key,
     nativeShot:name,nativeStart:start+i*dur,nativeDuration:dur,title:name.replaceAll('_',' ')});}
  }
 }finally{inv20Text=draw;run.pilot=oldPilot;}
 SB24.endingCache??={};SB24.endingCache[pilot]=out;return sb24Clone(out);
}
inv20Draw=function(t,W,H,S){const edit=SB24.data?.overrides?.ending?.[run.pilot];
 if(!edit)return SB24.base.ending.apply(this,arguments);
 const rows=SB24.ending||sb24Rows('ending',run.pilot,sb24Native('ending',run.pilot));let at=26.4;
 const finish=26.4+rows.reduce((n,b)=>n+(b.duration||5),0);INV20.end=finish;
 const b=rows.find(b=>{const from=at;at+=b.duration||5;return t>=from&&t<at;});
 const elapsed=b?t-(at-(b.duration||5)):0;
 SB24.endingRow=b?{b,elapsed}:null;SB24.captionDrawn=false;
 try{INV20.end=SB24.end;const mapped=b?b.nativeStart+elapsed/(b.duration||5)*b.nativeDuration:SB24.end+Math.max(0,t-finish);
  const result=SB24.base.ending(mapped,W,H,S);if(b?._sbText&&b.text&&!SB24.captionDrawn)SB24.base.caption(b.who||'',b.text,W,H,Math.min(b.text.length,Math.floor(elapsed*37)),1);return result;
 }finally{INV20.end=finish;SB24.endingRow=null;}
};
inv20Text=function(who,text,W,H,shown,alpha){const q=SB24.endingRow;
 if(q){SB24.captionDrawn=true;if(!q.b.text)return;who=q.b.who;text=q.b.text;shown=Math.min(text.length,Math.floor(q.elapsed*37));}
 return SB24.base.caption.call(this,who,text,W,H,shown,alpha);
};
function sb24Scenes(pilot){const groups=[['opening','Campaign opening','Opening'],['opening-finale','Opening narration','Opening'],
 ...Array.from({length:9},(_,i)=>['post-'+(i+1),'After Stage '+(i+1),'Campaign']),
 ['cronos','Chronos — first contact','Encounters'],['hammer-trap1002','Chronos — the trap','Encounters'],
 ['route-left','Stage 6 — Harrier route','Encounters'],['route-right','Stage 6 — Rebel route','Encounters'],
 ['rebel-contact','Rebel squad — contact','Encounters'],...['voss','nyx','rook','kaia','jace'].map(k=>['stage-x-'+k,'Stage X — '+k.toUpperCase(),'Encounters']),
 ['stage7-approach','Stage 7 — river approach','Campaign'],...Object.keys(SB24.transitions||{}).map(id=>[id,id==='dracodia-rebirth'?'Dracodia - rebirth responses':id==='dracodia-transform'?'Dracodia - transformation responses':'Dracodia - final defeat','Finale']),['dracodia-monologue','Dracodia — monologue','Finale'],['ending','Invasion ending','Finale']];
 for(const id of SB24.observed.keys())if(!groups.some(a=>a[0]===id)&&!id.startsWith('ht23-announcement-'))groups.push([id,id,'Discovered']);
 return groups.map(([id,title,group])=>({id,title,group,kind:id==='opening'?'opening':id==='ending'?'ending':SB24.transitions?.[id]?'action':id==='dracodia-monologue'?'monologue':id==='opening-finale'?'narration':'director',beats:sb24Native(id,pilot)}));
}
function sb24Art(b,pilot){if(b.expression!=null&&/^DRACODIA$/i.test(b.who||''))return DR5_ART.portrait[b.expression||0]?.key;return b.bg||(b.c22&&C22_ART.images[b.c22]?.key)||b.art||
 (b.federation?C22_ART.images.satellite_clean.key:b.dispatch?C22_ART.images[b.dispatch==='dispatch'?'hq_regroup':'hq_alarm']?.key:
 b.pilotCam?'cin_pilot_'+b.pilotCam+'_helmet':b.pilotLine?'cin_pilot_'+pilot+'_helmet':null)||
 (/chronos/i.test(b.who||'')?'fb1002_hammer_portrait':PILOTS.some(p=>p.key===(b.who||'').toLowerCase())?'cin_pilot_'+b.who.toLowerCase()+'_open':null);
}
async function sb24Thumbnail(b,pilot){const key=sb24Art(b,pilot);if(!key)return null;const end=performance.now()+12000;
 while(!XART.rdy(key)){if(performance.now()>end)return null;await new Promise(r=>setTimeout(r,60));}
 const im=XART.get(key),c=document.createElement('canvas');c.width=384;c.height=216;const g=c.getContext('2d'),k=Math.min(c.width/im.width,c.height/im.height);
 g.imageSmoothingEnabled=false;g.drawImage(im,(384-im.width*k)/2,(216-im.height*k)/2,im.width*k,im.height*k);return c.toDataURL('image/webp');}
function sb24SetData(data){SB24.data=sb24Clone(data);SB24.ending=null;SB24.monologue=null;IP21.beats=SB24.intro.map(b=>({...b}));IP21.finaleAt=IP21.beats.at(-1).to;IP21.end=IP21.finaleAt+SB24.finaleDuration;DR5.intro.splice(0,DR5.intro.length,...SB24.dr5.map(b=>[...b]));INV20.end=SB24.end;return true;}
async function sb24Preview(id,pilot,cards,index=0,play=true){SB24.previewing=true;SB24.preview={id,pilot,index};
 try{BOFCinematicDirector.cancel();Audio.stopMusic();Snd.loopStopAll();run.pilot=pilot;run.mode='campaign';Input.clearTaps();Input.mouse.down=false;
  const native=sb24Native(id,pilot),rows=cards.filter(c=>c.enabled!==false).map(c=>({...native[c.source],...c.fields,_sbText:(c.edited||[]).includes('text'),_sbWho:(c.edited||[]).includes('who')}));
  if(!rows.length)return;Snd.prepare([...new Set(rows.map(b=>b.c22Cue).filter(Boolean))]);const selected=Math.min(cards.slice(0,index).filter(c=>c.enabled!==false).length,rows.length-1);
  if(id==='opening-finale'){SB24.data.overrides['opening-finale']??={};SB24.data.overrides['opening-finale'][pilot]=cards;sb24InstallIntro(pilot);SB24.base.intro(()=>setState(GS.TITLE));campaignIntro.t=IP21.finaleAt+(selected===0?3:9.01);
  }else if(id==='opening'){IP21.beats=rows;let t=0;for(const b of rows){b._sbText=true;b.duration=Math.max(.25,b.duration||6);b.at=t;b.to=t+=b.duration;}IP21.finaleAt=t;IP21.end=t+SB24.finaleDuration;
   SB24.base.intro(()=>setState(GS.TITLE));campaignIntro.t=rows[selected].at+.01;
  }else if(id==='ending'){SB24.data.overrides.ending??={};SB24.data.overrides.ending[pilot]=cards;SB24.ending=rows;
   run.stage=8;setState(GS.VICTORY);drawVictory._trueEnding=drawVictory._ready=true;drawVictory._t=26.4+rows.slice(0,selected).reduce((s,b)=>s+(b.duration||5),0)+.01;drawVictory._sfx={};
   victoryEndingWarm();
  }else{const previewRows=rows.slice(selected).map(b=>({...b,art:sb24Art(b,pilot)||b.art}));
   SB24.base.play.call(BOFCinematicDirector,'storyboard-preview',previewRows,()=>setState(GS.TITLE),false);}
  SB24.paused=!play;
 }finally{SB24.previewing=false;}}
// Pausing a rehearsal never changes the shipping game's clocks.
SB24.base.cut=drawCutsceneState;drawCutsceneState=function(dt){return SB24.base.cut.call(this,SB24.paused&&SB24.preview?0:dt);};
SB24.base.openingDraw=drawCampaignIntro;drawCampaignIntro=function(dt){return SB24.base.openingDraw.call(this,SB24.paused&&SB24.preview?0:dt);};
SB24.base.victoryDraw=drawVictory;drawVictory=function(dt){return SB24.base.victoryDraw.call(this,SB24.paused&&SB24.preview?0:dt);};
globalThis.BOF_STORYBOARD={catalog:sb24Scenes,native:sb24Native,thumbnail:sb24Thumbnail,art:sb24Art,setData:sb24SetData,preview:sb24Preview,
 pause(v){SB24.paused=v;},stop(){SB24.preview=null;SB24.paused=false;BOFCinematicDirector.cancel();Snd.loopStopAll();Audio.stopMusic();setState(GS.TITLE);},
 duration(id,b){if(id==='ending')return b.duration||5;if(id==='opening-finale')return 7;if(id==='dracodia-monologue'||SB24.transitions?.[id])return dr5TalkDuration(b.text||'');return Math.max(b.duration||0,b.c22Action ? .25 : (b.text||'').length/(id==='opening'?CAMPAIGN_INTRO_CPS:38)+(id==='opening'?CAMPAIGN_INTRO_READ_HOLD:2.7));},
 get cues(){return Object.keys(BOFA.sfx).sort();},
 get project(){return sb24Clone(SB24.data);},get ready(){return true;},
 get assets(){return Object.entries(C22_ART.images).map(([name,a])=>({name,key:a.key,path:a.path}));},
 get pilots(){return PILOTS.filter(p=>CE20.pilots.includes(p.key)).map(p=>({key:p.key,name:p.name}));}};

// Event-bound responses retain the native physical action/callback. Reordering
// these cards changes which line is spoken at each response beat.
SB24.transitions={
 'dracodia-rebirth':[
  {who:'$PILOT',text:'What the heck was that?'},{who:'$PILOT',text:"Uhh, what's going on...?"},{who:'$PILOT',text:'...'}],
 'dracodia-transform':[
  {who:'$PILOT',text:'What in the world is that..'},{who:'$CONTACT',text:"It's...Reforming?!"},
  {who:'$PILOT',text:'.......'},{who:'$PILOT',text:'No amount of training could ever have prepared me for this.'}],
 'dracodia-defeat':[
  {who:'$PILOT',text:'You. Are. Terminated!'},{who:'$PILOT',text:'The code is collapsing! That portal is my way home.'}]
};
SB24.base.say=dr5Say;
dr5Say=function(b,who,text,face=0){
 if(b?._r30?.mode==='dr5Monologue'&&SB24.monologue){const row=SB24.monologue[dr5State(b).line];if(row){who=row.who;text=row.text;face=row.expression||0;}}
 else for(const [id,original]of Object.entries(SB24.transitions)){const i=original.findIndex(q=>q.text===text);if(i<0||!SB24.data?.overrides?.[id]?.[run.pilot])continue;
  const row=sb24Rows(id,run.pilot,sb24Native(id,run.pilot))[i];who=row?.who||who;text=row?.text||'';break;}
 return SB24.base.say.call(this,b,who,text,face);
};

SB24.base.directorTick=BOFCinematicDirector.tick;
BOFCinematicDirector.tick=function(dt){const scene=this.current,b=scene?.beats[scene.i];
 if(b&&!b.c22&&b.c22Cue&&!b._sbCuePlayed){b._sbCuePlayed=true;Snd.play(b.c22Cue);}
 return SB24.base.directorTick.apply(this,arguments);
};
