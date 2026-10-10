/* Ground Retina: hold to acquire a visible hostile, then release the charged
 * cannon to launch a missile at that exact unit or modular boss part. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,A=TD.Audio;
  function targets(G){
    const all=G.units.filter(u=>!u.dead).map(u=>({id:u,point:()=>u,valid:()=>!u.dead}));
    if(G.boss?.alive()&&G.boss.retinaTargets)all.push(...G.boss.retinaTargets());
    return all;
  }
  function visible(p,target){
    if(!target.valid())return false;
    const q=target.point(),c=TD.Cam;
    return M.dist(p.x,p.y,q.x,q.y)<320&&q.x>=c.x&&q.x<=c.x+TD.VW&&q.y>=c.y+45&&q.y<=c.y+TD.VH-25&&!W.rayBlock(p.x,p.y,q.x,q.y);
  }
  TD.Retina={targets,visible,
    tick(p,G,dt){
      p.retina=p.retina||{target:null,t:0,locked:false};const r=p.retina;
      if(p.dead||p.onfoot||!TD.Input.down('retina')){r.target=null;r.t=0;r.locked=false;return;}
      if(r.target&&!visible(p,r.target)){r.target=null;r.t=0;r.locked=false;}
      if(!r.target){
        const candidates=targets(G).filter(t=>visible(p,t)).map(t=>{const q=t.point();return{t,angle:Math.abs(M.wrap(M.angTo(p.x,p.y,q.x,q.y)-p.aim)),d:M.dist(p.x,p.y,q.x,q.y)};}).filter(t=>t.angle<1.25).sort((a,b)=>(a.angle*100+a.d)-(b.angle*100+b.d));
        if(candidates.length){r.target=candidates[0].t;A.play('charge',.5);}
      }
      if(!r.target)return;r.t+=dt;
      if(!r.locked&&r.t>=.45){r.locked=true;A.play('lock');G.say('RETINA LOCK',r.target.point());}
    },
    fire(p,G,power){
      const r=p.retina;if(!r?.locked||!r.target||!visible(p,r.target))return false;
      if(p.missiles<=0){G.say('NO MISSILES',p);p.canCd=15;return true;}
      const q=r.target.point(),a=M.angTo(p.x,p.y,q.x,q.y),f=M.fwd(a),md=TD.muzzleDist(p);
      p.missiles--;p.canCd=45;p.recoil=power?10:6;
      G.shots.push({k:'homing',retinaTarget:r.target,x:p.x+f[0]*md,y:p.y+f[1]*md,a,vx:f[0]*3.5,vy:f[1]*3.5,dmg:power?14:6,life:140,r:5,t:0,splash:power?40:26,sdmg:power?5:2});
      TD.FX.flash(p.x+f[0]*md,p.y+f[1]*md,a,.25);A.play('missile');TD.Stealth.noise(p.x,p.y,360,.6,G.units);return true;
    },
    draw(ctx,p){const r=p.retina;if(!r?.target||!visible(p,r.target))return;const q=r.target.point();
      ART.draw(ctx,'target_retina',q.x,q.y,{s:r.locked?.22:.32-M.clamp(r.t/.45,0,1)*.1,a:r.locked?0:r.t*2,alpha:r.locked?1:.55+Math.sin(r.t*30)*.25});
    },
  };
}(window));
