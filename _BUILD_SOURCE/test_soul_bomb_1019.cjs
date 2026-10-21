module.exports=function(vm,unused,ok){
 const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
 console.log('=== Soul bomb 1019: committed target, safe tells and bounded damage ===');
 const c=vm.createContext({console});
 vm.runInContext(`
 var window={},SOUL19_ART={banks:{charge:[],flight:[],burst:[]}},XART={_src:{},rdy:()=>true};
 var cues=[],hits=[],players=[null,{x:240,y:420,dead:false,out:false,invuln:0}],player=players[1],diffKey='normal',shake=0,coop=false;
 function v18Keys(){return [];}function v18Warm(){return true;}function stageLoadBegin(){}
 function v18StartAttack(b){b._r30.v18.seq++;b._r30.v18.attack={type:'soulBurst',t:0,tx:player.x,ty:player.y};r30Sound('shadowCharge');}
 function v18AttackTick(){}function v18Warnings(){}function r30DrawBoss(){}function v18Rig(){return [];}
 function v18Clear(b){b._r30.v18.attack=null;}function r30Sound(k){cues.push(k);}
 var Snd={play:k=>cues.push(k),prepare:()=>{}};
 function v19Organic(){return true;}function v18Model(){return 'ghost';}function v18Size(){return 320;}
 function seatList(){return coop?[1,2]:[1];}function withSeat(s,fn){const old=player;player=players[s];try{return fn();}finally{player=old;}}
 function playerHit(label){hits.push(label);player.dead=true;}
 function j3State(b){return b.J;}function clamp(v,a,z){return Math.max(a,Math.min(z,v));}function lerp(a,z,t){return a+(z-a)*t;}
 function s81003Distance(x,y,L){const dx=L.ex-L.x,dy=L.ey-L.y,d=dx*dx+dy*dy,t=d?clamp(((x-L.x)*dx+(y-L.y)*dy)/d,0,1):0;return Math.hypot(x-L.x-dx*t,y-L.y-dy*t);}
 function combatWarningTick(){}function combatWarningDraw(){}function groundTargetReticleDraw(){}
 `,c);
 vm.runInContext(fs.readFileSync(path.join(root,'assets/soul_bomb_1019.js'),'utf8'),c);
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};function setup(diff){diffKey=diff;hits=[];cues=[];coop=false;player=players[1]={x:240,y:420,dead:false,out:false,invuln:0};const b={x:240,y:110,dead:false,J:{attacks:0},_r30:{mode:'fight',v18:{seq:1}}};v18StartAttack(b);return b;}
 function step(b,n){for(let i=0;i<n;i++){for(const p of players.slice(1))p.invuln=Math.max(0,p.invuln-1);v18AttackTick(b,1/60);}}
 for(const d of ['easy','normal','hard','furious']){
  let b=setup(d),P=b._r30.v18.attack;out[d+' existing burst slot becomes the soul bomb']=P.type==='soulBomb';
  out[d+' one decoded charge and no doubled legacy cue']=cues.length===1&&cues[0]==='bossWeaponCharge';
  out[d+' human-readable initial warning']=P.tell>=1.3;
  step(b,Math.floor(P.tell*60)-1);out[d+' no damage during charging']=hits.length===0;
  player.x+=120;const target=JSON.stringify(P.target);step(b,400);
  out[d+' fixed target never follows the dodging player']=JSON.stringify(P.target)===target;
  out[d+' a lateral dodge clears flight and blast']=hits.length===0;
  out[d+' attack terminates and releases normal scheduler']=b._r30.v18.attack===null&&b.J.attacks===1;
  out[d+' one charge, one release and one impact cue']=JSON.stringify(cues)===JSON.stringify(['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact']);
  b=setup(d);P=b._r30.v18.attack;step(b,400);out[d+' remaining on the marked target gets hit once']=hits.length===1;
  for(const duration of [.46,.62]){b=setup(d);P=b._r30.v18.attack;P.t=P.tell+P.travel-.20;P.x=P.target.x;P.y=P.target.y;player.invuln=Math.ceil(duration*60)+4;step(b,60);out[d+' '+duration+'s defense outlasts final approach and burst']=hits.length===0;}
  b=setup(d);P=b._r30.v18.attack;v18Clear(b);step(b,400);out[d+' clearing the owner prevents delayed attacks']=hits.length===0&&cues.length===1;
 }
 const b=setup('normal');coop=true;players[2]={x:370,y:420,dead:false,out:false,invuln:0};const targets=[];
 for(let i=0;i<4;i++){v18StartAttack(b);targets.push(b._r30.v18.attack.target.seat);}
 out['Co-op alternates living participant targets']=targets.join(',')==='1,2,1,2'||targets.join(',')==='2,1,2,1';
 return out;})())`,c));
 for(const [name,pass]of Object.entries(rows))ok(pass,name);
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'assets/game/levels/stage_08/effects/soul_bomb_1019/manifest.json'),'utf8'));
 for(const [name,bank]of Object.entries(manifest.banks))ok(bank.length>=8&&bank.every(a=>{const b=fs.readFileSync(path.join(root,a.path));return a.w%2===0&&a.h%2===0&&b.readUInt32BE(16)===a.w&&b.readUInt32BE(20)===a.h&&String(a.pivot)===String(bank[0].pivot);}),name+' actual PNGs retain fixed even geometry and common pivots');
};
