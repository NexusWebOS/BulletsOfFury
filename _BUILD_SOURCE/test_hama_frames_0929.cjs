module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const [file,sentinel] of [['hammer_time_art_0927.js','HAMMER_TIME_ART'],['hammer_time_0927.js','ht27Variant'],
 ['hama_art_0928.js','HAMA_ART'],['hama_0928.js','HAMA_VARIANT'],['hama_frames_art_0929.js','HAMA_FRAMES_ART_29'],['hama_frames_0929.js','HAMA29']])
 if(vm.runInContext('typeof '+sentinel,ctxv)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 // Re-run the encounter tests after installing these hooks, so the original
 // throw/catch, STOP timings, immunity and cleanup exercise the integrated code.
 require('./test_hama_0928.cjs')(vm,ctxv,ok);
 console.log('=== HAMA 0929 authored reels: startup, contact frames, attachments, targetable flight and isolation ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;
 setState(GS.PASSWORD);pwInput='HAMA';submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');startRun(PENDING_STAGE);
 const b=boss,d=b._hammerTime,H=d.hama,m=Snd.music.hama;m.readyState=4;m.paused=false;m.currentTime=0;
 const ready=XART.rdy;XART.rdy=function(k){return k==='hama29_helper_airborne_tumble'?false:ready.call(XART,k);};updatePlay(1/60);
 o['the soundtrack waits for the real thrown-helper atlas']=!d.musicStarted&&d.clock===0;
 XART.rdy=ready;updatePlay(1/60);o['all reels ready opens the shared art/music start gate']=d.musicStarted;
 o['112 live authored frames registered in 13 lazy atlases']=Object.keys(HAMA29).length===13&&Object.values(HAMA29).reduce((n,a)=>n+a.frames.length,0)===112&&Object.values(HAMA29).every(a=>XART._src[a.key]===a.path);
 const s=HAMA_CUES.stops[0];o['HAMMER and TIME use distinct contact drawings']=hama29SlamFrame(s.t)===2&&hama29SlamFrame(s.t+HAMA_P)===7;
 o['full turns cover front, both sides and back over one bar']=[0,1,2,3].map(i=>hama29Cycle(i,12,4)).join()==='0,3,6,9';
 d.mode='toss';H.toss={t:1.3,held:{},wait:0};const p=hamaHandPoint(b),pp=hama29Point('hammer_toss_helper_throw',7,HAMA29.hammer_toss_helper_throw.held[7],b.x,b.y+94,HAMA29_TOSS);
 o['held target follows the authored carry pose']=Math.hypot(p.x-pp.x,p.y-pp.y)<.001;
 H.toss.t=1.65;const p2=hamaHandPoint(b);o['helper moves to the shoulder before its release']=Math.hypot(p2.x-p.x,p2.y-p.y)>30;
 d.mode='dance';ht27Summon(d,true);for(const q of d.helpers){q.spawn=1;q.dead=false;}
 hamaTossStart(b,d);let summons=0;const summon=ht27Summon;ht27Summon=function(){summons++;return summon.apply(this,arguments);};
 for(let i=0;i<180;i++){hamaHammerTick(d,1/60);hamaTossTick(b,d,1/60);}
 ht27Summon=summon;o['replacement helper is recalled once at the authored summon cue']=summons===1&&H.toss.recalled&&d.helpers.length===4;
 o['detached hammer leaves the authored overhead drum']=H.flyHammer===null||H.flyHammer.x0<b.x;
 for(const q of d.helpers)q.spawn=1; // the newly recalled replacement has arrived
 const get=XART.get,draw=ctx.drawImage,rotate=ctx.rotate,oldBoss=HT27_BASE.draw;
 let keys=[],turns=0,draws=0;XART.get=function(k){keys.push(k);return get.call(XART,k);};ctx.drawImage=function(){draws++;};ctx.rotate=function(){turns++;};
 // A single draw owns the troupe; engine body draw must not draw it again.
 HT27_BASE.draw=function(){};d.mode='attack';H.thrown=[];H.lines=[];ht27Draw(b);
 o['combat draws each of the four helpers once']=keys.filter(k=>k==='hama29_helper_lasso_360').length===4;
 d.mode='intro';d.shipFrame=null;H.thrown=[];H.toss=null;H.lines=[];
 for(const c of [6,9,12])for(const dir of [-1,1]){d.clock=c;d.shield=c>=7;H.moonDir=dir;ht27Draw(b);}
 o['shield rise keeps both moonwalk directions on the regular black-steel body']=keys.includes('hama29_boss_moonwalk_left')&&keys.includes('hama29_boss_moonwalk_right')&&!keys.some(k=>k.startsWith('hama29_armored_'));
 const T={t:.1,wait:0};H.toss=T;H.caught=0;d.mode='toss';d.shield=false;keys=[];ht27Draw(b);
 o['nearby helper composite reserves its buddy instead of drawing a duplicate']=keys.includes('hama29_hammer_toss_helper_throw')&&keys.filter(k=>k==='hama29_helper_lasso_360').length===3;
 T.wait=.7;keys=[];ht27Draw(b);
 o['waiting for replacements does not invent a helper in the carry plate']=!keys.includes('hama29_hammer_toss_helper_throw')&&keys.includes('hama29_boss_vocal_leap')&&keys.filter(k=>k==='hama29_helper_lasso_360').length===4;
 d.mode='dance';H.toss=null;H.lines=[{who:'boss',text:'HEY!',t:.18,dur:1},{who:'crew',text:'HEY!',t:.18,dur:1}];H.thrown=[{x:180,y:240,t:0,dead:false,flash:0}];keys=[];ht27Draw(b);
 o['thrown helper renders authored flight views without canvas rotation']=keys.includes('hama29_helper_airborne_tumble')&&turns===0;
 o['front helmets sing at their neck attachments']=keys.includes('hama29_boss_speaker_sing')&&keys.includes('hama29_helper_speaker_sing');
 d.mode='breakdown';d.clock=HAMA_A.phase;H.pose='lasso';keys=[];ht27Draw(b);
 o['breakdown uses the dedicated boss/helper turns and chanting heads']=keys.includes('hama29_boss_lasso_360')&&keys.includes('hama29_helper_lasso_360')&&keys.includes('hama29_boss_speaker_chant')&&keys.includes('hama29_helper_speaker_chant');
 HT27_BASE.draw=oldBoss;XART.get=get;ctx.drawImage=draw;ctx.rotate=rotate;
 setState(GS.TITLE);setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();startRun(PENDING_STAGE);
 o['original HAMMER bypasses HAMA frames and keeps its remix']=!hamaOn()&&ht27SongName()==='hammerTime';setState(GS.TITLE);
 return o;})())`,ctxv));
 for(const k in out)ok(out[k],'HAMA frames 0929: '+k);
};
