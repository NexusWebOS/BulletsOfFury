/* BOF Retina for ground combat: tap/cycle, travelling seeker, a five-second
 * lock and hold-to-maintain. Missiles retain the exact acquired target. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,A=TD.Audio,I=TD.Input;
  const COLORS={yuri:'#e02020',axel:'#2f6fff',cole:'#39ff5a',decker:'#ffe11a',juggernaut:'#ff8a1a',lizzie:'#ffc21a',falva:'#ff4fa3',freezer:'#9a4fe0',maverick:'#1f7a3a',hotwire:'#ffb458',phoenix:'#ff6454',niel:'#76f4c1'};
  function targets(G){
    const all=G.units.filter(u=>!u.dead).map(u=>({id:u,point:()=>u,valid:()=>!u.dead}));
    if(G.boss?.alive()&&G.boss.retinaTargets)all.push(...G.boss.retinaTargets().map(t=>({...t,boss:true})));
    return all;
  }
  function visible(p,target){
    if(!target.valid())return false;
    const q=target.point(),c=TD.Cam,z=c.zoom||1;
    // Like BOF, visible hostiles are selectable across the whole playfield.
    // The ground stage still requires a clear route past solid cover.
    return q.x>=c.x&&q.x<=c.x+TD.VW/z&&q.y>=c.y+45/z&&q.y<=c.y+(TD.VH-25)/z&&!W.rayBlock(p.x,p.y,q.x,q.y);
  }
  function clear(r){r.target=null;r.phase=null;r.t=0;r.locked=false;r.lockT=0;}
  TD.Retina={targets,visible,
    colors:COLORS,
    warm:[...Array.from({length:4},(_,i)=>['retm_'+i,'retmb_'+i]).flat(),...Object.keys(COLORS).filter(p=>!['hotwire','phoenix','niel'].includes(p)).map(p=>'nbret_'+p)],
    cycle(p,G){
      const r=p.retina||(p.retina={target:null,t:0,locked:false});
      if(p.missiles<=0){clear(r);G.say('NO MISSILES',p);A.play('error');return false;}
      const candidates=targets(G).filter(t=>visible(p,t)).sort((a,b)=>{const x=a.point(),y=b.point();return M.dist(p.x,p.y,x.x,x.y)-M.dist(p.x,p.y,y.x,y.y);});
      if(!candidates.length){clear(r);return false;}
      const at=candidates.findIndex(t=>t.id===r.target?.id),target=candidates[(at+1)%candidates.length];
      const ox=r.phase&&r.x!=null?r.x:p.x,oy=r.phase&&r.y!=null?r.y:p.y-10;
      Object.assign(r,{target,phase:'seek',locked:false,t:0,ox,oy,x:ox,y:oy,scale:2.2,spin:0,lockT:0,lockSpin:0});
      A.play('charge',.5);A.play('blip',.35);return true;
    },
    tick(p,G,dt){
      const r=p.retina||(p.retina={target:null,t:0,locked:false});r.animT=(r.animT||0)+dt;
      if(p.dead||p.onfoot){clear(r);return;}
      if(r.target&&!visible(p,r.target))clear(r);
      if(I.tap('retina')||(!r.target&&I.down('retina')&&p.missiles>0))this.cycle(p,G);
      if(!r.target)return;
      const q=r.target.point();
      if(r.phase==='seek'){
        r.t+=dt;const fraction=M.clamp(r.t/.45,0,1),ease=1-(1-fraction)**3;
        r.x=M.lerp(r.ox,q.x,ease);r.y=M.lerp(r.oy,q.y,ease);r.scale=M.lerp(2.2,1,ease);r.spin+=dt*14;
        if(fraction>=1){r.phase='locked';r.locked=true;r.lockT=5;r.lockSpin=7;A.play('lock');}
      }else if(r.phase==='locked'){
        r.x=q.x;r.y=q.y;r.spin+=dt*r.lockSpin;r.lockSpin=Math.max(0,r.lockSpin-dt*14);
        r.lockT=I.down('retina')?5:r.lockT-dt;
        if(r.lockT<=0){clear(r);A.play('error',.3);}
      }
    },
    fire(p,G,power){
      const r=p.retina;if(!r?.locked||!r.target||!visible(p,r.target))return false;
      if(p.missiles<=0){G.say('NO MISSILES',p);A.play('error');p.canCd=15;return true;}
      const q=r.target.point(),a=M.angTo(p.x,p.y,q.x,q.y),f=M.fwd(a),md=TD.muzzleDist(p);
      p.missiles--;p.canCd=45;p.recoil=power?10:6;r.lockT=5;TD.Achievements?.unlock('lock');
      G.shots.push({k:'homing',retinaTarget:r.target,x:p.x+f[0]*md,y:p.y+f[1]*md,a,vx:f[0]*3.5,vy:f[1]*3.5,dmg:power?14:6,life:140,r:5,t:0,splash:power?40:26,sdmg:power?5:2});
      TD.FX.flash(p.x+f[0]*md,p.y+f[1]*md,a,.25);A.play('missile');TD.Stealth.noise(p.x,p.y,360,.6,G.units);return true;
    },
    draw(ctx,p){
      const r=p.retina;if(!r?.target||!r.phase||!visible(p,r.target))return;
      const col=COLORS[p.pilot]||COLORS.cole,seek=r.phase==='seek',flashing=!seek&&r.lockT<=1.2;
      if(flashing&&Math.floor(r.animT*1000/90)%2)return;
      const bossKey='nbret_'+p.pilot,boss=r.target.boss&&ART.has(bossKey);
      const frame=Math.floor(r.animT*1000/(seek?90:130))%4,key=boss?bossKey:(seek?'retm_':'retmb_')+frame;
      const g=ART.get(key);if(!g)return;
      const size=boss?58:seek?32*r.scale:34;
      ctx.save();ctx.shadowColor=col;ctx.shadowBlur=flashing?16:seek?10:8;
      ART.draw(ctx,key,r.x,r.y,{s:size/g.sw,a:(r.spin||0)*(boss?.35:1),alpha:flashing?.95:.9,palette:boss?null:col});
      ctx.restore();
    },
  };
}(window));
