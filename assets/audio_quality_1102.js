"use strict";
/* AQ112: one shared post-mix headroom/compression stage for actual HTTP media.
   Native cue gains, slider settings, filters, voice caps and retrigger gates stay
   with Snd. File:// deliberately retains direct playback to avoid silent CORS. */
const AQ112={base:{play:HTMLMediaElement.prototype.play,shape:Snd._shape},bus:null,ctx:null,
 routed:0,errors:[],peaks:[],pending:new WeakSet(),nodes:new WeakSet()};
function aq112Bus(){const c=Snd._audioCtx();if(!c)return null;if(AQ112.bus&&AQ112.ctx===c)return AQ112.bus;
 const compressor=c.createDynamicsCompressor();compressor.threshold.value=-8;compressor.knee.value=4;compressor.ratio.value=16;compressor.attack.value=.001;compressor.release.value=.12;
 const output=c.createGain();output.gain.value=.88;compressor.connect(output);output.connect(c.destination);AQ112.ctx=c;AQ112.bus={input:compressor,output,compressor};return AQ112.bus;
}
function aq112Route(a){if(location.protocol==='file:'||!a)return false;const c=Snd._audioCtx();if(!c)return false;
 if(c.state!=='running'){if(!AQ112.pending.has(a)){AQ112.pending.add(a);Promise.resolve(c.resume()).then(()=>{AQ112.pending.delete(a);if(c.state==='running')aq112Route(a);}).catch(()=>AQ112.pending.delete(a));}return false;}
 const bus=aq112Bus();if(!bus)return false;
 try{
  if(!a._bofNode&&a._aq112Cfg)AQ112.base.shape.call(Snd,a,a._aq112Cue,a._aq112Cfg);
  let node=a._bofNode;
  if(!node){const src=c.createMediaElementSource(a),gain=c.createGain();gain.gain.value=1;src.connect(gain);a._bofNode=node=gain;}
  if(!AQ112.nodes.has(node)){try{node.disconnect(c.destination);}catch(_direct){}node.connect(bus.input);AQ112.nodes.add(node);AQ112.routed++;}
  return true;
 }catch(e){if(AQ112.errors.length<24)AQ112.errors.push(String(e));return false;}
}
Snd._shape=function(a,name,cfg){a._aq112Cue=name;a._aq112Cfg=cfg;return AQ112.base.shape.apply(this,arguments);};
HTMLMediaElement.prototype.play=function(){aq112Route(this);return AQ112.base.play.apply(this,arguments);};
function aq112Tap(){const b=aq112Bus();if(!b)return null;if(Snd.cur)aq112Route(Snd.cur);for(const p of Object.values(Snd.pools))for(const s of p.slots||[])if(s?.attached)aq112Route(s.el);return b.output;}
globalThis.BOF_AUDIO_QUALITY_1102={state:AQ112,tap:aq112Tap,route:aq112Route};
