'use strict';
/* Chronos's approved modular exception: one authored whole body, one separate
   rotary chaingun and foreground grip. Native HP/arsenal/death owners remain. */
const CH23={base:{draw:hammerBossDraw,chain:hammerChainStart,fire:hammerBossChaingunFire,mount:hammerBlasterMount,hit:hammerBlasterHit,damage:hammerBossDamage,tick:hammerBossTick,load:stageLoadBegin,play:updatePlay},events:[],masks:new Map(),draws:{}};
for(const s of Object.values(CH23_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(CH23_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
function ch23Own(b){return ht23Own(b)&&!b._hammerTime?.hama;}
function ch23Armed(b){return ch23Own(b)&&!b._hammer.chainDestroyed&&!b._hammer.hb20Pickup&&(['chain_warn','chaingun','chain_cool'].includes(b._hammer.state)||b._hammer.state==='fr_activation'&&b._hammer._ht23ArmorGun);}
function ch23Warm(){return Object.values(CH23_ART.sheets).map(s=>XART.rdy(s.key)).every(Boolean);}
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['hammerChaingun','bossWeaponCharge']);return CH23.base.load.call(this,n,[...(keys||[]),...(n===5?Object.values(CH23_ART.sheets).map(s=>s.key):[])]);};
function ch23Cell(bank,b,f=0){const variant=ht23Variant(b),rows=CH23_ART.banks[bank+variant]||CH23_ART.banks[bank];return rows[Math.max(0,Math.min(rows.length-1,f|0))];}
function ch23Blit(a,x,y,flash=0){const key=flash>0&&a.white?a.white:a.key;if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]));CH23.draws[key]=(CH23.draws[key]||0)+1;return true;}
function ch23GunFrame(b){return b._hammer.ch23Rev>.04?1+Math.floor(b._hammer.ch23Spin||0)%8:0;}
function ch23Recoil(b){return b._hammer.state==='chaingun'?-3.5*clamp((b._hammer.chainMuzzle||0)/.09,0,1):0;}
function ch23BodyFrame(b){const rows=CH23_ART.banks.body;return b._hammer.state==='chaingun'?Math.floor(b._hammer.t*18)%rows.length:0;}
function ch23Mount(b){const a=ch23Cell('barrel',b,ch23GunFrame(b)),x=b.x+CH23_ART.gunSocket[0],y=b.y+CH23_ART.gunSocket[1]+ch23Recoil(b);return{x,y,muzzleY:y+CH23_ART.muzzle[1]-a.pivot[1],left:x-a.pivot[0],top:y-a.pivot[1],scale:1,a};}
hammerBlasterMount=function(b){return ch23Armed(b)?ch23Mount(b):CH23.base.mount.apply(this,arguments);};
hammerBlasterHit=function(b,x,y){if(!ch23Armed(b))return CH23.base.hit.apply(this,arguments);const m=ch23Mount(b),a=m.a;if(!XART.rdy(a.key))return false;let mask=CH23.masks.get(a.key);if(!mask){const im=XART.get(a.key),c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.drawImage(im,0,0);mask=g.getImageData(0,0,a.w,a.h).data;CH23.masks.set(a.key,mask);}const px=Math.floor(x-m.left),py=Math.floor(y-m.top);return px>=0&&py>=0&&px<a.w&&py<a.h&&mask[(py*a.w+px)*4+3]>48;};
function ch23Module(b){const m=ch23Mount(b),h=b._hammer;return{id:'chaingun',hp:h.chainHP,max:h.chainMax,dead:!!h.chainDestroyed,x:m.x,y:m.muzzleY-30,muzzle:{x:m.x,y:m.muzzleY},frame:ch23GunFrame(b),rev:h.ch23Rev||0};}
// A destroyed module cannot own a stationary fan: its fire callback correctly
// emits no rounds, so it can never reach the volley-count exit. Continue the
// native recovery beat instead of re-entering an attack with a broken gun.
// Keep chain_cool: Furious checks its final recovery/rage checkpoint there.
hammerChainStart=function(b){if(ch23Own(b)&&b._hammer.chainDestroyed){b._hammer.chainHeat=0;return hammerState(b,'chain_cool');}const r=CH23.base.chain.apply(this,arguments);if(!ch23Own(b))return r;const h=b._hammer;
 h.ch23Pattern=(h.ch23Cycle||0)%2?'fan':'down';h.ch23Cycle=(h.ch23Cycle||0)+1;h.ch23Volleys=0;
 if(h.ch23Pattern==='fan'){h.chainDir=0;h.chainStartX=(camLeftX()+camRightX())/2;h.chainEndX=h.chainStartX-1;}
 else{h.ch23SweepDir=-(h.ch23SweepDir||-1);h.chainDir=h.ch23SweepDir;h.chainStartX=h.chainDir>0?h.chainL:h.chainR;h.chainEndX=h.chainDir>0?h.chainR:h.chainL;}
 Audio.SFX.bossWeaponCharge?.();CH23.events.push({type:'rev-up',pattern:h.ch23Pattern});return r;
};
function ch23Round(q,dir,pattern){q._ch23Round=true;q._ch23Direction=dir;q._ch23Pattern=pattern;q._archBlaster=true;q._noArsenal=true;q._boss=true;q._weaponProof=true;q.w=7;q.h=20;return q;}
hammerBossChaingunFire=function(b){if(!ch23Own(b))return CH23.base.fire.apply(this,arguments);const h=b._hammer;if(h.chainDestroyed)return;
 h.chainMuzzle=.09; // Recoil, actual gun pixels and the native muzzle agree.
 if(h.ch23Pattern!=='fan'){const first=eBullets.length,r=CH23.base.fire.apply(this,arguments);for(const q of eBullets.slice(first))ch23Round(q,4,'down');return r;}
 const m=ch23Mount(b),ids=hammerFurious()?[0,1,2,3,4,5,6,7,8]:hammerHard()?[0,1,3,4,5,7,8]:[0,2,4,6,8],speed=hammerFurious()?5.6:hammerHard()?5.2:4.8;
 // One native launcher/audio partner per volley; remaining rounds share its
 // pressure/speed assignment silently instead of stacking9 muzzle/audio reports.
 eMG(m.x,m.muzzleY,Math.PI/2,speed,'#a5cfff');const lead=eBullets[eBullets.length-1],v=Math.hypot(lead.vx,lead.vy);ch23Round(lead,4,'fan');
 for(const i of ids)if(i!==4){const a=Math.PI/2+CH23_ART.angles[i];eBullets.push(ch23Round({...lead,vx:Math.cos(a)*v,vy:Math.sin(a)*v},i,'fan'));}
 if((h.chainSfxCd||0)<=0){Audio.SFX.hammerChaingun?.();h.chainSfxCd=1.45;}
 h.ch23Volleys=(h.ch23Volleys||0)+1;const total=hammerFurious()?7:hammerHard()?6:5;h.chainHeat=Math.min(1,h.ch23Volleys/total);h.chainMuzzle=.09;h.shotCd=hammerFurious()?.24:hammerHard()?.29:.34;
 CH23.events.push({type:'fan-volley',rounds:ids.length,x:m.x,y:m.muzzleY});if(h.ch23Volleys>=total)hammerState(b,'chain_cool');
};
hammerBossTick=function(b,dt){if(ch23Own(b)&&b._hammer.chainDestroyed&&['chain_warn','chaingun'].includes(b._hammer.state))hammerState(b,'chain_cool');if(ch23Own(b)){const h=b._hammer,warm=hammerFurious()?.65:hammerHard()?.75:.85,want=h.state==='chain_warn'?clamp(h.t/warm,0,1):h.state==='chaingun'?1:h.state==='chain_cool'?Math.max(0,1-h.t/.7):0;
 h.ch23GunFlash=Math.max(0,(h.ch23GunFlash||0)-dt);h.ch23Rev=clamp((h.ch23Rev||0)+clamp(want-(h.ch23Rev||0),-dt*1.8,dt*2.8),0,1);h.ch23Spin=(h.ch23Spin||0)+dt*(h.ch23Rev>.01?2+22*h.ch23Rev:0);b.name='CHRONOS';}
 return CH23.base.tick.apply(this,arguments);
};
hammerBossDamage=function(b,dmg){const h=b?._hammer,gun=ch23Armed(b)&&b._hammerModuleHit==='chaingun',hp=h?.chainHP,r=CH23.base.damage.apply(this,arguments);if(gun&&h.chainHP<hp){if(gp4FlashRequest(h,'ch23GunFlash',.12))h.ch23GunFlash=.12;CH23.events.push({type:'gun-damaged',hp:h.chainHP});}return r;};
function ch23Warn(b){const h=b._hammer,m=ch23Mount(b),warm=hammerFurious()?.65:hammerHard()?.75:.85,u=clamp(h.t/warm,0,1),kind=h.ch23Pattern==='fan'?'fan':'down',color=l23FovPhase(u),a=CH23_ART.banks['warn_'+kind+'_'+color][0];ch23Blit(a,m.x,m.muzzleY);}
hammerBossDraw=function(b){if(!ch23Armed(b))return CH23.base.draw.apply(this,arguments);const h=b._hammer,m=ch23Mount(b),f=ch23BodyFrame(b),flash=Math.max(b.flash||0,b._lastPart?.flash||0),y=b.y+ch23Recoil(b),body=ch23Cell('body',b,f);
 hammerBossAtmosphereDraw(b);hf22Aura(b);ctx.save();ctx.imageSmoothingEnabled=false;
 if(h.state==='chain_warn')ch23Warn(b);
 if(typeof c27TraceAura==='function'){c27TraceAura(b,{a:body,k:1,rot:0},b.x,y);c27TraceAura(b,{a:m.a,k:1,rot:0},m.x,m.y);}
 ch23Blit(body,b.x,y,flash);ch23Blit(m.a,m.x,m.y,Math.max(flash,h.ch23GunFlash||0));ch23Blit(ch23Cell('hands',b,f),b.x,y,flash);
 if(h.chainMuzzle>0)wm26Draw(ctx,'chaingun',m.x,m.muzzleY,Math.PI/2,1-h.chainMuzzle/.09,48);
 ctx.restore();hm10WallDraw(b);hf19Caption(b);
};
function ch23BulletDraw(q){if(!q?._ch23Round)return false;const phase=((q._ph||0)+Math.floor(efxClock*18))&1,a=CH23_ART.banks.round[(q._ch23Direction??4)*2+phase];return ch23Blit(a,q.x,q.y);}
updatePlay=function(dt){if(BOFCinematicDirector.current?.id.startsWith('ht23-announcement-')&&HT23.speechOwner===boss&&boss?._hammer)boss._hammer.ch23GunFlash=Math.max(0,(boss._hammer.ch23GunFlash||0)-Math.max(0,dt||0));return CH23.base.play.apply(this,arguments);};
window.BOF_CHRONOS_MODULAR=CH23;ch23Warm();
