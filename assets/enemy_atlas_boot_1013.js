/* Only loaded by index.html?enemyAtlas=1. The atlas never writes player progress. */
(()=>{'use strict';
 const cache=new WeakMap(),original={get:Storage.prototype.getItem,set:Storage.prototype.setItem,remove:Storage.prototype.removeItem,clear:Storage.prototype.clear};
 const map=s=>{if(!cache.has(s))cache.set(s,new Map());return cache.get(s);};
 Storage.prototype.getItem=function(k){k=String(k);const m=map(this);if(m.has(k))return m.get(k);if(/bossmode|boss_mode/i.test(k))return null;return original.get.call(this,k);};
 Storage.prototype.setItem=function(k,v){map(this).set(String(k),String(v));};
 Storage.prototype.removeItem=function(k){map(this).set(String(k),null);};
 Storage.prototype.clear=function(){const m=map(this);for(const k of m.keys())m.set(k,null);for(let i=0;i<this.length;i++)m.set(this.key(i),null);};
 const nativeRAF=requestAnimationFrame.bind(window),queue=new Map();let id=0,last=performance.now(),clock=last;
 const control=window.BOF_ATLAS_CLOCK={paused:false,speed:1,steps:0,frames:0,after:null};
 window.requestAnimationFrame=cb=>{queue.set(++id,cb);return id;};window.cancelAnimationFrame=k=>queue.delete(k);
 function pump(now){const dt=Math.max(0,Math.min(40,now-last));last=now;
  if(!control.paused||control.steps>0){clock+=control.paused?1000/60:dt*control.speed;if(control.steps>0)control.steps--;
   const work=Array.from(queue.values());queue.clear();for(const cb of work)cb(clock);control.frames++;control.after?.();}
  nativeRAF(pump);
 }nativeRAF(pump);
 const style=document.createElement('style');style.textContent=`html,body{margin:0!important;padding:0!important;width:100%!important;height:100%!important;overflow:hidden!important;background:#060a0e!important}#room,#game-frame,#screen-area{position:fixed!important;inset:0!important;display:block!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;border:0!important;transform:none!important;max-width:none!important;max-height:none!important}#screen{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;margin:0!important;transform:none!important;object-fit:contain!important;image-rendering:pixelated}#hud-row,#hud-wrap,#hud-top,#hud-bottom,#hud-bot,#hud-div,#hud-div2,#credit-left,#credit-right,#fs-btn,#hint,.siege-side,#siege-compact,#equip-dom{display:none!important}`;document.head.appendChild(style);
})();
