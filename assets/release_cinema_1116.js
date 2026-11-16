"use strict";
/* Release QA1116: current approved guitar identity and readable ending holds.
   Reuses native text, portraits, typewriter, skip/input and continuation owners. */
const READ16={base:{rows:c16Rows,play:BOFCinematicDirector.play},adjusted:[],art:{"key":"release16_juggernaut_guitar","path":"assets/game/shared/cinematics/release_qa_1116/juggernaut-guitar.webp","w":512,"h":512,"cols":3,"frames":6,"pivot":[256,256],"durations":[220,180,250,260,320,700],"sha256":"d1701e43341f0f97590c7a5b109d21e670e234537e6bcc0842f3d80da6c08f19"},comicArt:{"key":"release16_comic_guitar","path":"assets/game/shared/cinematics/release_qa_1116/juggernaut-guitar-comic.webp","w":270,"h":270,"cols":4,"frames":6,"pivot":[135,135],"source":"assets/game/shared/cinematics/release_qa_1116/juggernaut-guitar.webp","sourceScale":0.52734375,"sha256":"265ffde4b2a5382d43b165a67cbebd5f590510412a514a4bcd0c6de516dd4adf"}};
D1110_ART.banks['juggernaut-guitar']=READ16.art;
XART._src[READ16.art.key]=READ16.art.path+'?v='+READ16.art.sha256.slice(0,12);
C16_ART.banks['art-juggernaut-guitar']=READ16.comicArt;
XART._src[READ16.comicArt.key]=READ16.comicArt.path+'?v='+READ16.comicArt.sha256.slice(0,12);
function read16Rows(rows,ending=false){return rows.map(b=>{
 if(!b.d1110||!b.cm3||!b.text||(!ending&&!String(b.id).startsWith('ENDING-')))return b;
 const readAt=Number(b.cm3.readAt)||0,typed=String(b.text).length/30,words=(String(b.text).match(/\S+/g)||[]).length,
  hold=Math.max(2.25,Math.min(5,words/6)),required=readAt+typed+hold+.18,duration=Math.max(Number(b.duration)||0,required);
 const q={...b,duration,cm3:{...b.cm3,baseDuration:duration-readAt-.14},read16:{typed,hold,readAt,minimum:required}};
 READ16.adjusted.push({id:b.id,before:b.duration,after:duration});if(READ16.adjusted.length>256)READ16.adjusted.shift();return q;
});}
c16Rows=function(){return read16Rows(READ16.base.rows.apply(this,arguments),arguments[0]==='ending');};
C16.rows=CM3.rows=FP5.rows=c16Rows;
BOFCinematicDirector.play=function(id,rows,done,live=false){return READ16.base.play.call(this,id,read16Rows(rows,id==='ending'),done,live);};
