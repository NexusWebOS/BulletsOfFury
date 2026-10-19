"use strict";
/* Mike requested slower Lizzie Spread pellets. The observed cadence already
   matches Cole; tune travel only, preserving the centered authored fan/muzzle. */
const LSP19={scale:.85,base:{shoot:pShoot},shots:0};
pShoot=function(){const pilot=_pilotKey(),spread=run.weapon===1&&!spaceWeaponsActive(),first=pBullets.length,r=LSP19.base.shoot.apply(this,arguments);
 if(pilot==='lizzie'&&spread)for(let i=first;i<pBullets.length;i++){const q=pBullets[i];
  if(q.kind!=='spread'||q.ally||q._lsp19)continue;q.vx*=LSP19.scale;q.vy*=LSP19.scale;q._lsp19=true;LSP19.shots++;
 }return r;
};
window.BOF_LIZZIE_SPREAD={state:LSP19};
