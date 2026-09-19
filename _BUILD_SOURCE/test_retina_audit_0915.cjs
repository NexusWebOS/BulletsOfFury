module.exports=function(vm,ctxv,ok){
  console.log('=== 304b. Retina encounter router audit ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss,subBoss,bossActive,subBossActive,enemies,retina,dmg:_dmgBullet};const o={};
    try{
      enemies=[];retina={target:null};_dmgBullet=null;

      subBoss=null;subBossActive=false;bossActive=true;
      boss={x:240,y:155,w:220,h:220,hp:500,maxhp:500,dead:false,enter:false,_furnace:true,
        _fz:{phase:'arms',trans:0,a:0,arm:{left:{a:0,recoil:0},right:{a:0,recoil:0}},pools:{left:100,right:100,body:180,head:120},flash:{}},
        _mwBarrier:{active:false}};
      let list=_lockTargets(),left=list.find(t=>t._retinaId==='left');
      o.furnaceParts=list.length===2&&list.every(t=>t.kind.indexOf('furnace ')===0)&&list.indexOf(boss)<0;
      retinaMissileDamage(left,7,{x:left.x,y:left.y});o.furnaceRoute=boss._fz.pools.left===93&&boss._fz.pools.right===100;
      boss._mwBarrier.active=true;o.furnaceShield=_lockTargets().length===0;

      boss=null;bossActive=false;subBossActive=true;
      subBoss={x:240,y:150,w:196,h:180,hp:300,maxhp:300,dead:false,enter:false,_ql:true,_qlHullOpen:false,
        _qlCan:[{id:'L',hb:[60,90,40,55],hp:30,max:30,dead:false},{id:'R',hb:[284,90,40,55],hp:30,max:30,dead:false}]};
      list=_lockTargets();let turret=list[0],other=list[1];retinaMissileDamage(turret,5,{x:turret.x,y:turret.y});
      o.quadTurrets=list.length===2&&list.indexOf(subBoss)<0&&turret.hp===25&&other.hp===30;
      subBoss._qlCan.forEach(c=>{c.dead=true;c.hp=0;});o.quadHull=_lockTargets()[0]===subBoss;

      subBoss={x:240,y:150,w:130,h:125,hp:400,maxhp:400,dead:false,enter:false,
        _rzb:{state:'guns',trans:0,a:0,pools:{left:40,right:40,turret:100,hull:100},flash:{},clankT:0}};
      list=_lockTargets();left=list.find(t=>t._retinaId==='left');retinaMissileDamage(left,6,{x:left.x,y:left.y});
      o.razorback=list.length===3&&list.some(t=>t._retinaId==='turret'&&!t.dead)&&subBoss._rzb.pools.left===34&&subBoss._rzb.pools.right===40&&subBoss._rzb.pools.turret===100;

      subBoss={x:240,y:150,w:77,h:84,hp:200,maxhp:200,dead:false,enter:false,
        _tlv:{vuln:true,phase:'chase',ap:[0,1,2,3].map(()=>({hp:10,max:10}))}};
      list=_lockTargets();let aperture=list.find(t=>t._retinaId==='aperture 2');retinaMissileDamage(aperture,3,{x:aperture.x,y:aperture.y});
      o.tempest=list.length===5&&subBoss._tlv.ap[2].hp===7&&subBoss._tlv.ap[1].hp===10;

      const mkJet=(gray,x)=>({x:x,y:150,w:77,h:84,dead:false,_tempestGray:gray,_jet:{angle:0},
        _tlv:{vuln:true,ap:[0,1,2,3].map(()=>({hp:8,max:8}))},_ai:{hp:100}});
      subBoss={x:240,y:150,w:240,h:100,hp:400,maxhp:400,dead:false,enter:false,
        _tempestDuo:{ships:[mkJet(false,170),mkJet(true,310)]}};
      list=_lockTargets();o.tempestDuo=list.length===10&&list.filter(t=>t.kind==='tempest hull').length===2;

      subBoss={x:240,y:150,w:180,h:160,hp:300,maxhp:300,dead:false,enter:false,
        _rapWing:{L:{hp:50,max:50,dead:false},R:{hp:50,max:50,dead:false}}};
      list=_lockTargets();left=list.find(t=>t._retinaId==='wing L');retinaMissileDamage(left,4,{x:left.x,y:left.y});
      o.blacksteel=list.length===3&&list.indexOf(subBoss)>=0&&subBoss._rapWing.L.hp===46&&subBoss._rapWing.R.hp===50;

      subBoss=null;subBossActive=false;bossActive=true;
      boss={x:240,y:160,w:300,h:230,hp:800,maxhp:800,dead:false,enter:false,_s7warden:{noHit:false,final:{phase:'stun',cores:[{side:-1,hp:30,dead:false},{side:1,hp:30,dead:false}]}}};
      list=_lockTargets();left=list.find(t=>t._retinaId==='core -1');retinaMissileDamage(left,5,{x:left.x,y:left.y});
      o.warden=list.length===2&&list.indexOf(boss)<0&&boss._s7warden.final.cores[0].hp===21&&boss._s7warden.final.cores[1].hp===30;

      boss={x:240,y:150,w:180,h:180,hp:500,maxhp:500,dead:false,enter:false,
        _sx:{code:'l6j',hp:{nose:100,left_wing:100,right_wing:100,body:100,tail:100},dead:{nose:false,left_wing:false,right_wing:true,body:false,tail:false}}};
      list=_lockTargets();o.sectional=list.length===4&&list.every(t=>t.kind.indexOf('section ')===0)&&!list.some(t=>t._retinaId==='right_wing');

      const meta=_mechMeta('mbg2'),parts={};for(const id of meta.drawOrder)parts[id]={hp:50,state:'intact',docked:true};
      boss={x:240,y:150,w:288,h:288,hp:500,maxhp:500,dead:false,enter:false,_mech:{tag:'mbg2',scale:1,phase:'fight',order:meta.drawOrder,parts:parts}};
      list=_lockTargets();o.mech=list.length>0&&list.every(t=>t.kind.indexOf('mech ')===0)&&!list.some(t=>/torso|head/.test(t._retinaId));
      return JSON.stringify(o);
    }finally{boss=save.boss;subBoss=save.subBoss;bossActive=save.bossActive;subBossActive=save.subBossActive;enemies=save.enemies;retina=save.retina;_dmgBullet=save.dmg;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Retina encounter router audit: '+k);
  return out;
};
