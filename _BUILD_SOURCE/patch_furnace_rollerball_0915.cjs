const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const file = path.join(root, 'assets', 'game.js');
let src = fs.readFileSync(file, 'utf8');
if (src.includes('\r\n')) throw new Error('assets/game.js must remain LF-only');

function replaceOnce(from, to, label) {
  const count = src.split(from).length - 1;
  if (count !== 1) throw new Error(`${label}: expected one match, found ${count}`);
  src = src.replace(from, to);
}

replaceOnce(
  "const FZT_ATTACKS={arms:['spin900','cannon','sweep','cannon'], core:['ring','coreLaser','rotor','ring','coreLaser'], head:['eyeBurst','eyeSweep']};",
  "const FZT_ATTACKS={arms:['spin900','cannon','sweep','cannon'], core:['ring','coreLaser','rollerball','rotor','ring','coreLaser'], head:['eyeBurst','eyeSweep']};",
  'Furnace core attack roster'
);

replaceOnce(
  "    introY0:null, cues:{}, eye:{'-1':Math.PI*0, '1':0}, eyeLock:0, lanceX:W/2, ppx:null, pvx:0, pvy:0, ppy:null, flash:{}};",
  "    introY0:null, cues:{}, eye:{'-1':Math.PI*0, '1':0}, eyeLock:0, lanceX:W/2, ppx:null, pvx:0, pvy:0, ppy:null, flash:{},\n    rollY:null,rollStartY:null,rollFrom:null,rollTo:null,rollLeg:-1,rollLive:false};",
  'Furnace roller state'
);

replaceOnce(
  "  F.shotBeat=-1; F.burstBeat=-1; F.beams=[];\n  if(F.phase==='head'){",
  "  F.shotBeat=-1; F.burstBeat=-1; F.beams=[];\n  F.rollY=null;F.rollStartY=null;F.rollFrom=null;F.rollTo=null;F.rollLeg=-1;F.rollLive=false;\n  if(F.phase==='head'){",
  'Furnace attack reset'
);

replaceOnce(
  "  F.charge=0; F.arm.left.recoil=0; F.arm.right.recoil=0; F.arm.left.charge=0; F.arm.right.charge=0;",
  "  F.charge=0; F.rollLive=false; F.arm.left.recoil=0; F.arm.right.recoil=0; F.arm.left.charge=0; F.arm.right.charge=0;",
  'Furnace roller live reset'
);

replaceOnce(
  "    F.a=(F.attack==='rotor')?F.a:0; b.y=fztPy(235)+Math.sin(F.t*0.8)*14*FZT_S;",
  "    F.a=(F.attack==='rotor'||F.attack==='rollerball')?F.a:0;\n    if(F.attack!=='rollerball')b.y=fztPy(235)+Math.sin(F.t*0.8)*14*FZT_S;",
  'Furnace core rotation ownership'
);

const rotor = `    } else if(F.attack==='rotor'){
      const u=clamp((t-1)/4.4,0,1);
      F.a=F.dir*Math.PI*2*1.6*fztSmooth(u); b.x=W/2+Math.sin(u*Math.PI*2)*190*FZT_S;`;

const roller = `    } else if(F.attack==='rollerball'){
      /* A committed horizontal lane gives the player a fair vertical escape, while roll and
         somersault i-frames remain a valid high-skill answer. Both the spin and crossings ramp
         from slow through medium/fast into the final super-fast pass. */
      const WARN=1.45, legs=[1.24,1.00,.80,.64,.52,.44], margin=Math.max(96,b.w*.5);
      if(F.rollY==null){
        F.rollY=clamp(P.y,fztPy(315),VH-96);F.rollStartY=b.y;
        F.rollFrom=F.dir>0?margin:W-margin;F.rollTo=F.dir>0?W-margin:margin;
        fztSfx('bossWeaponCharge');
      }
      if(t<WARN){
        const u=fztSmooth(t/WARN);b.x=fztMix(F.startX,F.rollFrom,u);b.y=fztMix(F.rollStartY,F.rollY,u);
        F.a+=F.dir*dt*fztMix(1.4,4.2,u);
        F.tells.push({x:F.rollFrom,y:F.rollY,ex:F.rollTo,ey:F.rollY,progress:t/WARN,width:118});
        combatWarningTick(b,'furnace-rollerball',t,WARN);
      }else{
        let active=t-WARN,total=0;for(const d of legs)total+=d;
        if(active<total){
          let leg=0,base=0;while(leg<legs.length-1&&active>=base+legs[leg])base+=legs[leg++];
          const local=clamp((active-base)/legs[leg],0,1),forward=(leg&1)===0;
          b.x=fztMix(forward?F.rollFrom:F.rollTo,forward?F.rollTo:F.rollFrom,fztSmooth(local));b.y=F.rollY;
          const ramp=clamp(active/total,0,1);F.a+=F.dir*dt*fztMix(5.0,25.0,Math.pow(ramp,.78));F.rollLive=true;
          if(leg>F.rollLeg){F.rollLeg=leg;shake=Math.max(shake,4+leg);fztSfx('whip');}
        }else{
          const recover=clamp((active-total)/.82,0,1),lastAt=legs.length&1?F.rollTo:F.rollFrom;
          b.x=fztMix(lastAt,W/2,fztSmooth(recover));b.y=fztMix(F.rollY,fztPy(235),fztSmooth(recover));
          F.a+=F.dir*dt*fztMix(5,0,recover);
          if(recover>=1){F.a=0;furnaceNext(b);}
        }
      }
` + rotor;

replaceOnce(rotor, roller, 'Furnace rollerball branch');

replaceOnce(
  "    if(F.trans<=0) for(const q of furnaceBoxes(b)) if(Math.hypot(q.x-P.x,q.y-P.y) < q.r+10*FZT_S){ playerHit(); break; }",
  "    if(F.rollLive && Math.hypot(b.x-P.x,b.y-P.y)<78*FZT_S+Math.max(P._hx||9,P._hy||10))playerHit();\n    if(F.trans<=0) for(const q of furnaceBoxes(b)) if(Math.hypot(q.x-P.x,q.y-P.y) < q.r+10*FZT_S){ playerHit(); break; }",
  'Furnace roller collision'
);

const backupDir = path.join(root, '_shots', 'backups');
fs.mkdirSync(backupDir, {recursive:true});
fs.copyFileSync(file, path.join(backupDir, 'game_pre_furnace_rollerball_0915.js'));
fs.writeFileSync(file, src, 'utf8');
console.log('PATCHED_FURNACE_ROLLERBALL_0915');
