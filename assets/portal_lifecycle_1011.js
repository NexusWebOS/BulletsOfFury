"use strict";
/* Shared by the game and asset review. Authored poses, one physical aperture,
   continuous frame time. Opening/closing clamp; only the idle bank wraps. */
const PL11 = (() => {
  const phases=['form','loop','close'], buffers=new Map(), art=PL11_ART;
  const parts={
    pl11_gate_shell:'assets/game/shared/fx/portals_bof_1011/gate-shell.png',
    pl11_gate_mask:'assets/game/shared/fx/portals_bof_1011/gate-aperture-mask.png'
  };
  const bounded=(v,a,b)=>Math.max(a,Math.min(b,v));
  function formationRotation(progress) {
    // One clockwise turn, with zero angular speed at both ends. A complete
    // turn settles onto the original loop pose without an orientation reset.
    if(progress<=0||progress>=1)return 0;
    return Math.PI*2*progress*progress*progress*(progress*(progress*6-15)+10);
  }
  function sample(bank,phase,time,options={}) {
    const clip=art[bank]?.[phase];if(!clip)throw new Error('Unknown portal animation '+bank+'/'+phase);
    const count=clip.frames.length, seconds=Math.max(0,Number(time)||0), fps=options.fps||clip.fps;
    const duration=options.duration??count/fps;
    const rawPos=phase==='loop'?seconds*fps:bounded(seconds/Math.max(.001,duration),0,1)*(count-1);
    // Exact frame scrubbing must not select frame 13 for 13.999999999999998.
    const nearest=Math.round(rawPos),pos=Math.abs(rawPos-nearest)<1e-9?nearest:rawPos;
    const whole=Math.floor(pos),from=phase==='loop'?whole%count:Math.min(count-1,whole);
    const to=phase==='loop'?(from+1)%count:Math.min(count-1,from+1);
    const progress=bounded(seconds/Math.max(.001,duration),0,1);
    return {bank,phase,from,to,mix:options.blend===false?0:pos-whole,
      rotation:phase==='form'?formationRotation(progress):0,
      done:phase!=='loop'&&seconds>=duration,duration,seconds};
  }
  function sequence(bank,time,options={}) {
    const fps=art[bank].fps,n=art[bank].loop.frames.length,t=Math.max(0,Number(time)||0);
    const form=options.form??n/fps,loop=options.loop??Infinity,close=options.close??n/fps;
    if(t<form)return sample(bank,'form',t,{duration:form,blend:options.blend});
    if(t<form+loop){
      // A scheduled exit ends on the same authored pose that closing begins
      // with. Adjust cadence slightly to fit whole cycles, never restart it.
      const cycles=Number.isFinite(loop)?Math.max(1,Math.round(loop*fps/n)):0;
      const rate=cycles?cycles*n/Math.max(.001,loop):fps;
      return sample(bank,'loop',t-form,{fps:rate,blend:options.blend});
    }
    return sample(bank,'close',t-form-loop,{duration:close,blend:options.blend});
  }
  function keys(bank) {
    const result=phases.flatMap(p=>art[bank][p].frames.map(f=>f.key));
    if(bank==='amethyst_gate')result.push(...art.gate_energy.form.frames.map(f=>f.key),...Object.keys(parts));
    return result;
  }
  function ready(bank,loader) {return keys(bank).map(k=>loader.rdy(k)).every(Boolean);}
  function bufferFor(name,w,h) {
    let buffer=buffers.get(name);
    if(!buffer){buffer=document.createElement('canvas');buffers.set(name,buffer);}
    if(buffer.width!==w||buffer.height!==h){buffer.width=w;buffer.height=h;}
    return buffer;
  }
  function frameImage(pose,get) {
    const entry=art[pose.bank],frames=entry[pose.phase].frames,a=frames[pose.from],b=frames[pose.to];
    const A=get(a.key),B=pose.mix>0?get(b.key):A;if(!A||!B)return null;
    let image=A;
    if(pose.mix>0&&pose.from!==pose.to){
      const buffer=bufferFor(pose.bank,a.w,a.h);
      const g=buffer.getContext('2d');g.clearRect(0,0,a.w,a.h);g.imageSmoothingEnabled=false;
      // Weighted premultiplied-alpha addition keeps dark apertures opaque.
      // Source-over twice would dim/ghost the throat at the loop boundary.
      g.globalCompositeOperation='source-over';g.globalAlpha=1-pose.mix;g.drawImage(A,0,0);
      g.globalCompositeOperation='lighter';g.globalAlpha=pose.mix;g.drawImage(B,0,0);
      g.globalAlpha=1;g.globalCompositeOperation='source-over';image=buffer;
    }
    return {image,frame:a,entry};
  }
  function formingGate(pose,get) {
    const shell=get('pl11_gate_shell'),mask=get('pl11_gate_mask');
    const energy=frameImage({...pose,bank:'gate_energy'},get);
    if(!shell||!mask||!energy)return null;
    const frame=art.amethyst_gate.form.frames[pose.from];
    // Convert the authored grayscale aperture to alpha once. Rotation is
    // confined to this same opening; neither the shell nor its mask rotates.
    let aperture=buffers.get('gate-aperture');
    if(!aperture){
      aperture=bufferFor('gate-aperture',frame.w,frame.h);
      const g=aperture.getContext('2d');g.drawImage(mask,0,0);
      const pixels=g.getImageData(0,0,frame.w,frame.h);
      for(let i=0;i<pixels.data.length;i+=4)pixels.data[i+3]=pixels.data[i];
      g.putImageData(pixels,0,0);
    }
    const image=bufferFor('forming-gate',frame.w,frame.h),g=image.getContext('2d');
    g.clearRect(0,0,frame.w,frame.h);g.imageSmoothingEnabled=false;
    g.save();g.translate(frame.pivot[0],frame.pivot[1]);g.rotate(pose.rotation);
    const e=energy.frame,k=2.2;
    g.drawImage(energy.image,-e.pivot[0]*k,-e.pivot[1]*k,e.w*k,e.h*k);g.restore();
    g.globalCompositeOperation='destination-in';g.drawImage(aperture,0,0);
    g.globalCompositeOperation='source-over';g.drawImage(shell,0,0);
    return {image,frame,entry:art.amethyst_gate};
  }
  function draw(context,pose,x,y,size,get,alpha=1) {
    const gate=pose.bank==='amethyst_gate'&&pose.phase==='form'&&pose.rotation;
    const result=gate?formingGate(pose,get):frameImage(pose,get);
    if(!result)return false;
    const {image,frame:a,entry}=result;
    const scale=size/entry.scaleWidth;
    context.save();context.globalAlpha*=alpha;context.imageSmoothingEnabled=false;
    if(pose.rotation&&!gate){
      context.translate(x,y);context.rotate(pose.rotation);
      context.drawImage(image,-a.pivot[0]*scale,-a.pivot[1]*scale,a.w*scale,a.h*scale);
    }else context.drawImage(image,x-a.pivot[0]*scale,y-a.pivot[1]*scale,a.w*scale,a.h*scale);
    context.restore();return true;
  }
  return {art,phases,parts,sample,sequence,keys,ready,draw};
})();
globalThis.BOFPortalPlayback=PL11;
