FURYBOT.audio=async function(){
 const Q=this,ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination();Q.audioDest=dest;
 const attached=new WeakSet(),base=HTMLMediaElement.prototype.play;
 function attach(el){
  if(attached.has(el))return;
  try{
   if(el._bofNode){el._bofNode.connect(dest);attached.add(el);return;}
   // Unfiltered/native media keeps the same signal and volume. A stable media
   // source survives pool reuse; captureStream tracks can end between shots.
   const src=ac.createMediaElementSource(el),gain=ac.createGain();gain.gain.value=1;src.connect(gain);gain.connect(ac.destination);gain.connect(dest);el._bofNode=gain;attached.add(el);
  }catch(e){(Q.audioErrors??=[]).push(String(e));}
 }
 HTMLMediaElement.prototype.play=function(){const r=base.apply(this,arguments);attach(this);if(r?.then)r.then(()=>attach(this)).catch(()=>{});return r;};
 for(const el of Object.values(Snd.music||{}))if(el instanceof HTMLMediaElement&&!el.paused)attach(el);
 return dest.stream;
};
