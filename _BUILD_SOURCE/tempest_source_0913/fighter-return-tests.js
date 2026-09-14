// ===== 296. TEMPEST THRUST HEADING, FULL EXIT AND PHYSICAL REENTRY (0913) =====
console.log('=== 296. Tempest complete offscreen thrust and return ===');
{
  vm.runInContext(_pre295,ctxv);
  vm.runInContext("tempestJetStart(b,p);J.state='charge';J.t=.99;J.cue='green';J.angle=0;J.lock={x:400,y:870};tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.state==='charge'&&J.thrusts===0&&J.angle>0&&J.angle<Math.PI",ctxv),'a sideways jet completes its visible turn before the booster ignites');
  vm.runInContext("for(var i=0;i<40&&J.state!=='thrust';i++)tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.state==='thrust'&&Math.abs(Math.sin(J.angle)-J.vx/Math.hypot(J.vx,J.vy))<1e-9&&Math.abs(-Math.cos(J.angle)-J.vy/Math.hypot(J.vx,J.vy))<1e-9",ctxv),'the authored nose points along the committed thrust velocity');
  vm.runInContext("J.t=.8;J.vx=840;J.vy=0;J.angle=Math.PI/2;s.boss.x=450;s.boss.y=400;tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.state==='thrust'&&!tempestJetOutside(p)",ctxv),'elapsed thrust time never brakes a jet that is still inside the viewport');
  vm.runInContext("for(var i=0;i<180&&J.state==='thrust';i++)tempestJetTick(b,p,1/60);tempestBrothersSync(b);var exitX=s.boss.x,exitY=s.boss.y;",ctxv);
  ok(vm.runInContext("J.state==='offscreen-turn'&&tempestJetOutside(p,90)&&!p._tlv.vuln&&tempestBrothersPartAt(b,p.x,p.y)===null&&D.striker===p",ctxv),'the whole hull and exhaust clear the edge before turning, with no offscreen hitbox or early ownership release');
  vm.runInContext("for(var i=0;i<90&&J.state==='offscreen-turn';i++)tempestJetTick(b,p,1/60);var rd=Math.atan2((J.reentry.y-s.boss.y)*TLV_KY,(J.reentry.x-s.boss.x)*TLV_KX)+Math.PI/2;",ctxv);
  ok(vm.runInContext("J.state==='return'&&s.boss.x===exitX&&s.boss.y===exitY&&Math.abs(Math.sin(rd-J.angle))<1e-9",ctxv),'the jet turns while fully offscreen and faces its inbound path before moving again');
  vm.runInContext("var returned=false,smooth=true,heading=true;for(var i=0;i<360&&J.state==='return';i++){var bx=s.boss.x,by=s.boss.y;tempestJetTick(b,p,1/60);var dx=(s.boss.x-bx)*TLV_KX,dy=(s.boss.y-by)*TLV_KY,d=Math.hypot(dx,dy);smooth=smooth&&d<=560/60+1e-7;if(d>1e-6)heading=heading&&(dx*Math.sin(J.angle)-dy*Math.cos(J.angle))/d>.999999;returned=returned||!tempestJetOutside(p);}",ctxv);
  ok(vm.runInContext("returned&&smooth&&heading&&J.state==='settle'&&D.striker===p",ctxv),'reentry crosses the edge by actual movement with its nose forward and no teleport');
  vm.runInContext("for(var i=0;i<90&&J.active;i++)tempestJetTick(b,p,1/60);tempestBrothersSync(b);",ctxv);
  ok(vm.runInContext("!J.active&&D.striker===null&&!tempestJetOutside(p)&&p._tlv.vuln&&Math.abs(s.boss.x-J.reentry.x)<1e-6&&Math.abs(s.boss.y-J.reentry.y)<1e-6",ctxv),'the pass releases only after the jet physically reaches its visible upper-arena position');
  vm.runInContext("var allEdges=true;for(var v of [[840,0],[-840,0],[0,840],[0,-840]]){s.boss.x=450;s.boss.y=500;s.vulnerable=true;tempestJetStart(b,p);J.state='thrust';J.t=0;J.vx=v[0];J.vy=v[1];J.angle=Math.atan2(v[1],v[0])+Math.PI/2;J.travel=0;for(var i=0;i<180&&J.state==='thrust';i++)tempestJetTick(b,p,1/60);allEdges=allEdges&&J.state==='offscreen-turn'&&tempestJetOutside(p,90);tempestJetCancel(b,p);}",ctxv);
  ok(vm.runInContext("allEdges",ctxv),'committed thrusts can fully leave any of the four viewport edges');
  vm.runInContext("subBoss=null;subBossActive=false;subBossDone=false;eBullets.length=0;playerLocks=[];",ctxv);
}
