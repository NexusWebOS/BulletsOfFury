// A committed Stage 4 ram owns the space needed for its visible escape route.
// Existing missiles keep flying; attached helpers resume with a fresh tell.
const BALANCE_HELPERS_1007B=fb1002Helpers;
fb1002Helpers=function(b,dt){
 const E=b?._mr27?.ram1002;
 if(run.stage===4&&b._ship==='stormsovereign'&&!b._gp4Host&&E&&(E.state==='tell'||E.state==='drive')){
  for(const d of b._s4war?.coreTurrets||[])if(d._pressure1002){d._pressure1002.aim=null;d._pressure1002.cd=Math.max(1,d._pressure1002.cd);}
  return;
 }
 return BALANCE_HELPERS_1007B.apply(this,arguments);
};
