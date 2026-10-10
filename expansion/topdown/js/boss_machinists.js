/* Wren / Foundry, Rolf / Vector and Chaz / Redline are hostile modular tanks.
 * Attack ownership, draw geometry, damage sockets, detached parts and player /
 * companion targeting belong to the same individual tank objects. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,FX=TD.FX,A=TD.Audio;
  const ART_META=root.TD_CAMPAIGN_ART, SCALE=.85;
  TD.makeMachinists=function(G,x,y){
    const names={wren:'WREN / FOUNDRY',rolf:'ROLF / VECTOR',chaz:'CHAZ / REDLINE'};
    const squad={name:'THE MACHINISTS',x,y,state:'enter',gauge:0,t:0,dead:false,wrecked:false,
      tanks:['wren','rolf','chaz'].map((crew,i)=>({crew,name:names[crew],x:230+i*170,y:200+i%2*80,a:0,look:0,
        hp:100,max:100,flash:0,recoil:0,t:0,cd:.5+i*.55,recover:0,dead:false,
        parts:{hull:80,turret:42,left_track:28,right_track:28,special_module:24},initial:{hull:80,turret:42,left_track:28,right_track:28,special_module:24},
        goalX:230+i*170,shots:0,trackDistance:[0,0],mode:'volley'})),
    };
    const world=(u,lx,ly,angle)=>{const c=Math.cos(angle),s=Math.sin(angle);return{x:u.x+lx*c-ly*s,y:u.y+lx*s+ly*c};};
    function geo(u,part){
      const p=ART_META.tanks[u.crew].parts[part].placement;
      const angle=(part==='turret'?u.look:u.a)+Math.PI;
      const center=world(u,(p[0]+p[2]/2-128)*SCALE,(p[1]+p[3]/2-151)*SCALE,angle);
      return {x:center.x,y:center.y,r:part==='hull'?25:part==='turret'?19:part==='special_module'?12:18,angle};
    }
    function muzzle(u,offset){const m=ART_META.tanks[u.crew].muzzle;return world(u,offset||0,(m[1]-151)*SCALE,u.look+Math.PI);}
    function clear(u,part){G.eshots=G.eshots.filter(s=>s.owner!==u||(part&&s.part!==part&&!(s.requires||[]).includes(part)));}
    function detach(u,part){
      if(u.parts[part]<=0)return;const key=TD.modPartKey(u,u.crew,part);u.parts[part]=0;clear(u,part);
      const angle=(part==='turret'?u.look:u.a)+Math.PI;
      FX.fragment(key,u.x,u.y,angle,SCALE,
        part==='left_track'?-80:part==='right_track'?80:30,-35,[128,151]);
      FX.boom(geo(u,part).x,geo(u,part).y,95,'gfx_destruction_',6);A.play('expB');TD.Cam.kick(4);
      u.recover=1.05;u.mode='recover';G.score+=1200;G.say(u.crew.toUpperCase()+' '+part.replace('_',' ').toUpperCase()+' DOWN',u);
    }
    function damage(u,part,dmg){
      if(u.dead||u.parts[part]<=0||squad.state==='enter')return;
      if(part==='hull'&&u.parts.turret>0)dmg*=.28;
      if(u.crew==='wren'&&u.parts.special_module>0&&u.t%9<3&&part!=='special_module')dmg*=.65;
      u.flash=.1;u.parts[part]-=dmg;u.hp=100*Object.values(u.parts).reduce((n,v)=>n+Math.max(0,v),0)/202;G.score+=Math.round(dmg*5);
      if(u.parts[part]<=0){u.parts[part]=1;detach(u,part);}
      if(u.parts.hull<=0){
        u.dead=true;clear(u);u.mode='dead';
        for(const p of ['left_track','right_track','turret','special_module'])detach(u,p);
        FX.boom(u.x,u.y,150,'gfx_destruction_',6);G.wrecks.push({x:u.x,y:u.y,a:u.a,art:'wm_tank_'+u.crew+'_wreck',still:true,s:1.13});G.kills++;G.score+=9000;
        if(squad.tanks.every(q=>q.dead)){squad.dead=true;squad.state='defeated';squad.wrecked=true;G.bossDown();A.stopMusic();}
      }
    }
    function target(u){
      const targets=[G.player,G.ally].filter(p=>p&&!p.dead);
      return targets.sort((a,b)=>M.dist(u.x,u.y,a.x,a.y)-M.dist(u.x,u.y,b.x,b.y))[0]||G.player;
    }
    function emit(u,part,k,a,offset,extra){
      if(u.parts[part]<=0||u.dead||u.recover>0)return;
      const p=muzzle(u,offset),f=M.fwd(a),speed=k==='laser'?5.4:k==='missile'?3.2:4;
      G.eshots.push(Object.assign({k,x:p.x,y:p.y,a,vx:f[0]*speed,vy:f[1]*speed,dmg:k==='mg'?1:2,life:145,r:4,t:0,owner:u,part,target:target(u)},extra));
      u.shots++;u.recoil=4;FX.boom(p.x,p.y,50,'wm_'+u.crew+'_muzzle_',3);A.play(k==='missile'?'missile':k==='laser'?'laser':'eshot',.5);
    }
    squad.alive=()=>!squad.dead&&squad.state!=='enter';
    squad.retinaTargets=()=>squad.tanks.filter(u=>!u.dead).flatMap(u=>Object.keys(u.parts).filter(p=>u.parts[p]>0).map(p=>({id:u.crew+':'+p,point:()=>geo(u,p),valid:()=>squad.alive()&&!u.dead&&u.parts[p]>0})));
    squad.hpFrac=()=>squad.tanks.reduce((sum,u)=>sum+Object.values(u.parts).reduce((n,v)=>n+Math.max(0,v),0),0)/(202*3);
    squad.aim=(sx,sy)=>squad.tanks.filter(u=>!u.dead).flatMap(u=>['turret','hull'].filter(p=>u.parts[p]>0).map(p=>geo(u,p))).sort((a,b)=>M.dist(sx,sy,a.x,a.y)-M.dist(sx,sy,b.x,b.y))[0];
    squad.hit=function(sx,sy,r,dmg,shot){
      for(const u of squad.tanks)if(!u.dead)for(const part of ['left_track','right_track','special_module','turret','hull'])if(u.parts[part]>0){
        const p=geo(u,part);if(M.dist(sx,sy,p.x,p.y)>=r+p.r)continue;
        const id=u.crew+':'+part;if(shot){const seen=shot.bossHits||(shot.bossHits=new Set());if(seen.has(id))continue;seen.add(id);}damage(u,part,dmg);return true;
      }return false;
    };
    squad.blast=function(x,y,r,dmg){for(const u of squad.tanks)if(!u.dead)for(const p of Object.keys(u.parts)){const q=geo(u,p);if(M.dist(x,y,q.x,q.y)<r+q.r)damage(u,p,dmg*.55);}};
    squad.damage=(crew,part,amount)=>damage(squad.tanks.find(u=>u.crew===crew),part,amount);
    squad.geometry=(crew,part)=>geo(squad.tanks.find(u=>u.crew===crew),part);
    squad.tick=function(dt){
      squad.t+=dt;if(squad.dead)return;
      if(squad.state==='enter'){squad.gauge=Math.min(1,squad.t/2);if(squad.t>=2){squad.state='fight';A.playMusic('boss2');for(const u of squad.tanks)u.cd=.5;}return;}
      for(const u of squad.tanks){
        if(u.dead)continue;u.t+=dt;u.flash=Math.max(0,u.flash-dt);u.recoil*=.8;
        const p=target(u);u.targetPilot=p.pilot;u.look=M.turnTo(u.look,M.angTo(u.x,u.y,p.x,p.y),.065);
        if(u.recover>0){u.recover-=dt;u.mode='recover';continue;}
        const cycle=u.t%(u.crew==='chaz'?7:9),wasX=u.x,wasY=u.y,wasA=u.a;
        if(u.parts.left_track>0&&u.parts.right_track>0){
          u.mode=u.crew==='chaz'&&u.parts.special_module>0&&cycle>5?'breach':'volley';
          const want=u.mode==='breach'?M.angTo(u.x,u.y,p.x,p.y):M.angTo(u.x,u.y,u.goalX+Math.sin(u.t*.9)*85,280+Math.sin(u.t*.4)*65);
          u.a=M.turnTo(u.a,want,.065);const f=M.fwd(u.a),speed=u.mode==='breach'?2.8:u.crew==='rolf'?1.25:.9;
          u.x+=f[0]*speed;u.y+=f[1]*speed;u.x=M.clamp(u.x,145,655);u.y=M.clamp(u.y,190,545);
          if(u.mode==='breach')TD.ramStructures(G,wasX,wasY,u.x,u.y,38);
          else W.collide(u,32,false);
        }
        const dist=Math.hypot(u.x-wasX,u.y-wasY),turn=M.wrap(u.a-wasA)*35;
        u.trackDistance[0]+=dist-turn;u.trackDistance[1]+=dist+turn;
        for(const q of squad.tanks)if(q!==u&&!q.dead)TD.pushOut(Object.assign(u,{r:33}),Object.assign(q,{r:33}));
        for(const actor of [G.player,G.ally])if(actor&&!actor.dead&&M.dist(u.x,u.y,actor.x,actor.y)<actor.r+35){if(actor===G.player)TD.hurtPlayer(G,2);else TD.hurtAlly(G,2);TD.pushOut(actor,Object.assign(u,{r:36}));W.collide(actor,actor.r,false);}
        if(u.parts.turret>0&&(u.cd-=dt)<=0&&!W.rayBlock(u.x,u.y,p.x,p.y)){
          u.cd=u.crew==='wren'?1.3:u.crew==='rolf'?2.4:2.8;
          if(u.crew==='wren')for(const offset of [-11,11])for(const d of [-.09,0,.09])emit(u,'turret','mg',u.look+d,offset);
          if(u.crew==='rolf')for(const d of u.parts.special_module>0?[-.28,0,.28]:[0])emit(u,'turret','laser',u.look+d,0,{requires:d?['special_module']:[]});
          if(u.crew==='chaz')for(const d of u.parts.special_module>0?[-.23,0,.23]:[0])emit(u,'turret','missile',u.look+d,d*40,{homing:40,turn:.022,shootable:true,requires:d?['special_module']:[]});
        }
      }
      const live=squad.tanks.filter(u=>!u.dead);if(live.length){squad.x=live.reduce((n,u)=>n+u.x,0)/live.length;squad.y=live.reduce((n,u)=>n+u.y,0)/live.length;}
    };
    squad.drawUnder=function(ctx){for(const u of squad.tanks)if(!u.dead&&u.parts.special_module>0&&u.recover<=0){if(u.crew==='wren'&&u.t%9<3)ART.draw(ctx,'wm_wren_special_'+Math.min(5,Math.floor(u.t%9*2)),u.x,u.y,{s:.7});if(u.crew==='chaz'&&u.mode==='breach')ART.draw(ctx,'wm_chaz_special_3',u.x,u.y,{s:.65,a:u.a+Math.PI});}};
    squad.draw=function(ctx){for(const u of squad.tanks)if(!u.dead){TD.drawModTank(ctx,u,u.crew,SCALE);}};
    squad.drawOver=function(ctx){ctx.font='bold 8px BOFCommand,monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.lineWidth=3;ctx.strokeStyle='#000';for(const u of squad.tanks)if(!u.dead){const label=u.crew.toUpperCase()+(u.mode==='recover'?' - EXPOSED':u.mode==='breach'?' - BREACH':'');ctx.strokeText(label,u.x,u.y+68);ctx.fillStyle=u.mode==='breach'?'#ff6440':'#ffce70';ctx.fillText(label,u.x,u.y+68);}};
    return squad;
  };
  TD.MISSIONS[2].boss=TD.makeMachinists;
}(window));
