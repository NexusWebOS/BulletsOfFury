const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
function once(old,replacement,label){const n=s.split(old).length-1;if(n!==1)throw new Error(label+' anchor count '+n);s=s.replace(old,replacement);}
once(
"function archBlit(key,frame,x,y,h,tint,rot){const q=hammerArchFrame(key,frame,tint);if(!q)return false;const w=h*q.sw/q.sh;ctx.save();ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,-w/2,-h/2,w,h);ctx.restore();return true;}",
"function archBlit(key,frame,x,y,h,tint,rot,alpha){const q=hammerArchFrame(key,frame,tint);if(!q)return false;const w=h*q.sw/q.sh;ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,-w/2,-h/2,w,h);ctx.restore();return true;}",
'archBlit alpha');
once(
"    combatWarningDraw(b,{x:g.x,y:g.y,ex:h.throwX,ey:VH,progress:k,width:42});",
"    combatWarningDraw(b,{x:g.x,y:g.y,ex:h.throwX,ey:VH,progress:k,width:42,alertX:b.x+76,alertY:b.y-82});",
'boomerang alert placement');
once(
"  else if(h.state==='throw'){key='twirl_throw';f=15;if(h.throw){for(let i=h.throw.trail.length-1;i>=1;i--)archBlit('hammer_spin',(Math.floor(h.throw.trail[i].angle/TAU*8)&7),h.throw.trail[i].x,h.throw.trail[i].y,118,null,h.throw.trail[i].angle);archBlit('hammer_spin',(Math.floor(h.throw.angle/TAU*8)&7),h.throw.x,h.throw.y,128,null,h.throw.angle);}}",
`  else if(h.state==='throw'){
    key='twirl_throw';f=15;
    if(h.throw){
      /* The active weapon stays solid. Sparse, faint authored frames show its path without
         reading as a chain of additional hammers or extra collision objects. */
      for(let i=h.throw.trail.length-1;i>=1;i-=2){const q=h.throw.trail[i],a=Math.min(.22,.05+(h.throw.trail.length-i)*.04);archBlit('hammer_spin',(Math.floor(q.angle/TAU*8)&7),q.x,q.y,118,null,q.angle,a);}
      archBlit('hammer_spin',(Math.floor(h.throw.angle/TAU*8)&7),h.throw.x,h.throw.y,128,null,h.throw.angle,1);
    }
  }`,
'boomerang authored afterimages');
if(s.includes('\r'))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s,'utf8');console.log('PATCHED_ARCHMAGE_BOOMERANG_VISUAL_0916');
