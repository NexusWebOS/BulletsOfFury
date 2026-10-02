module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['hama_vocals_art_1001.js','hama_vocals_1001.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),c,{filename:f});
 console.log('=== 386. HAMA: Mike recordings, music-clock captions and isolated lifecycle ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='HAMA';submitPassword();pilotIndex=0;startRun(PENDING_STAGE);
 const b=boss,d=b._hammerTime,m=ht27Song();m.readyState=4;m.paused=false;m.currentTime=0;updatePlay(1/60);
 out['HAMA uses the single recorded mix on its existing music element']=m===Snd.music.hama&&m.src.includes('hama_mike_robot_mix_1001_v3.mp3')&&BOFA.music.hama===HAMA_VOCALS_1001.music;
 out['mix length retains the original choreography clock']=Math.abs(HAMA_VOCALS_1001.seconds-HAMA_ART.audio.seconds)<.001;
 out['all captions are timed inside the song']=HAMA_VOCALS_1001.captions.every(q=>q.t>=0&&q.end>q.t&&q.end<=HAMA_VOCALS_1001.seconds);
 hamaLyricsTick(b,d,14.6,1/60);out['removed verses have no singing captions']=d.hama.lines.length===0;
 hamaSing(d,'boss','OLD PLACEHOLDER',2);out['attack taunts cannot replace recorded lyrics']=!d.hama.lines.some(q=>q.text==='OLD PLACEHOLDER');
 hamaLyricsTick(b,d,35,1/60);out['mouths stop between recorded phrases']=d.hama.lines.length===0;
 hamaLyricsTick(b,d,32.9,1/60);out['background hook belongs to the helper crew']=d.hama.lines.some(q=>q.who==='crew'&&q.text==='CANT TOUCH THIS');
 hamaLyricsTick(b,d,61.85,1/60);out['spoken Hammer syllable is removed']=d.hama.lines.length===0&&!hama29Vocal(d,'boss');
 out['only approved hooks and OH chants remain']=HAMA_VOCALS_1001.captions.every(q=>['CANT TOUCH THIS','OH! OH-OH!'].includes(q.text))&&HAMA_VOCALS_1001.events.every(e=>['chorus','breakdown chant'].includes(e.label));
 d.hama.stopFlags={0:{stop:true}};hamaLyricsTick(b,d,179,1/60);hamaLyricsTick(b,d,.1,1/60);out['a music loop rearms the recorded STOP choreography']=Object.keys(d.hama.stopFlags).length===0;
 m.currentTime=40;d.clock=40;d.mode='dance';d.locked=false;const pause=m.pause;let pauses=0;m.pause=function(){pauses++;return pause.apply(this,arguments);};setState('paused');out['pause reaches the single music and vocal element']=pauses>0;setState(GS.PLAY);out['resume preserves the same song position']=m.currentTime===40;m.pause=pause;
 setState(GS.TITLE);out['exit stops HAMA and clears its route']=!ht27Active&&Snd.cur!==m;
 setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();startRun(PENDING_STAGE);out['HAMMER remains the separate remix']=ht27Variant===null&&ht27SongName()==='hammerTime'&&!ht27Song().src.includes('hama_mike_robot');setState(GS.TITLE);
 return out;
})())`,c));
 for(const [name,pass] of Object.entries(out))ok(pass,name);
 const data=JSON.parse(vm.runInContext('JSON.stringify(HAMA_VOCALS_1001)',c));ok(fs.existsSync(path.join(__dirname,'..',data.music)),'recorded HAMA mix exists');
};
