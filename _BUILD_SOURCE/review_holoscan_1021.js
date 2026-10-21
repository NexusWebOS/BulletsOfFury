(()=>{'use strict';
 const frame=document.querySelector('#live-scan'),status=document.querySelector('#preview-status');let ticket=0;
 async function boot(){const serial=++ticket;status.hidden=false;status.textContent='LOADING HOLOSCAN…';
  for(let i=0;i<1800&&serial===ticket;i++){
   try{const w=frame.contentWindow;
    if(w.BOFHOLOSCAN&&w.eval('typeof ASSETS!=="undefined"&&ASSETS.ready')){
     const ready=w.eval('(()=>{sg20Warm();return BOFINSTRUCTOR.artReady&&BOFHOLOSCAN.ready;})()');
     if(ready){w.eval(`(()=>{BOFCinematicDirector.cancel();story=null;run.pilot='cole';run.mode='arcade';coopOn=false;diffKey='normal';tutStart({stage:1,lead:'cole',disp:'cole'});BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);warnT=0;TUT.card=false;TUT.i=TUT_LESSONS.findIndex(d=>d.id==='bob_card')-1;tutNext();TUT.typed=10000;return true;})()`);status.hidden=true;return;}
    }
   }catch(e){if(i>1600){status.textContent='Preview could not start: '+e.message;return;}}
   await new Promise(r=>setTimeout(r,100));
  }if(serial===ticket)status.textContent='The preview is still loading. Press RESTART SCAN to retry.';
 }
 frame.addEventListener('load',boot);document.querySelector('#restart-scan').onclick=()=>{ticket++;status.hidden=false;status.textContent='LOADING HOLOSCAN…';frame.src='/index.html?enemyAtlas=1&holoscanReview='+Date.now();};
})();
