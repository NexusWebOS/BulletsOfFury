const fs=require('fs');const file=__dirname+'/engine.js';let s=fs.readFileSync(file,'utf8');s=s.replace("this.speed=1700}","this.speed=1700;this.rig=Array.from({length:4},()=>({a:Math.PI/2,recoil:0,flash:0,charge:0}));this.salvoKey=''}");
const a=s.indexOf('turrets(){'),b=s.indexOf('\nstep(',a);s=s.slice(0,a)+`turrets(){return[-1,1].flatMap((side,j)=>[0,1].map(i=>{const id=j*2+i,baseX=side*(148+i*75),baseY=94+i*95,slide=Math.sin(this.time*1.1+i+j)*12,x=baseX+side*slide*.8,y=baseY+slide*.55,a=this.boss.a;return{id,localX:x,localY:y,baseX,baseY,x:this.boss.x+x*Math.cos(a)-y*Math.sin(a),y:this.boss.y+x*Math.sin(a)+y*Math.cos(a),...this.rig[id]}}))}
aimRig(dt){const facing=['pursuit','frenzy'].includes(this.phase)&&!this.vulnerable?-Math.PI/2:Math.PI/2;for(const q of this.turrets()){const r=this.rig[q.id],target=facing+clamp(wrap(Math.atan2(this.player.y-q.y,this.player.x-q.x)-facing),-.66,.66);r.a+=clamp(wrap(target-r.a),-1.65*dt,1.65*dt);r.recoil=Math.max(0,r.recoil-dt*50);r.flash=Math.max(0,r.flash-dt);r.charge=0}}
fireMount(id,offset=0,speed=280,kind='pellet'){const q=this.turrets()[id],a=q.a;this.spawn(q.x+Math.cos(a)*39,q.y+Math.sin(a)*39,a+offset,speed,kind);this.rig[id].recoil=6;this.rig[id].flash=.09;this.events.push('shot')}
battery(t,strong=false){const period=strong?5.2:5.8,u=t%period,cycle=Math.floor(t/period);let key='';
if(u<.65){for(const r of this.rig)r.charge=u/.65;this.pattern='CANNONS TRACKING'}
else if(u<1.45){const n=Math.floor((u-.65)/.2);key=cycle+':burst:'+n;this.pattern='ALTERNATING CANNON BURST';if(key!==this.salvoKey){const id=(n+cycle)%4;this.fireMount(id,0,310);if(strong)this.fireMount((id+2)%4,0,310)}}
else if(u<2.25){this.pattern='BATTERIES COOLING'}
else if(u<2.8){this.pattern='SPREAD CHARGING';for(const r of this.rig)r.charge=(u-2.25)/.55}
else if(u<3.7){const n=Math.floor((u-2.8)/.55);key=cycle+':fan:'+n;this.pattern='SHORT SPREAD';if(key!==this.salvoKey)for(const off of [-.17,0,.17])this.fireMount((cycle+n)%4,off,250)}
else if(u<4.35){this.pattern='MISSILE LOCK';this.missileWarning=true}
else if(u<4.5){key=cycle+':missiles';this.pattern='RAZOR SALVO';if(key!==this.salvoKey&&strong)for(const id of [1,3]){const q=this.turrets()[id];this.spawn(q.x,q.y,q.a,180,'missile');this.events.push('shot')}}
else this.pattern='RELOAD • PRESS THE ATTACK';if(key)this.salvoKey=key;
}
`+s.slice(b);
s=s.replace("const p=this.player,b=this.boss;", "this.missileWarning=false;this.aimRig(dt);const p=this.player,b=this.boss;");
let start=s.indexOf("const beat=Math.floor(this.t/(hell?.44:.75))"),end=s.indexOf("\nelse if(this.phase==='pursuit'",start);s=s.slice(0,start)+"this.battery(this.t,hell);this.mode+=' • '+this.pattern;}"+s.slice(end);
start=s.indexOf("const beat=Math.floor(c/(frantic?.20:.38))");end=s.indexOf("}else if(c<end)",start);s=s.slice(0,start)+"this.battery(c,false);"+s.slice(end);
start=s.indexOf("const beat=Math.floor(c/(frantic?.32:.65))");end=s.indexOf("if(c>end+6)",start);s=s.slice(0,start)+"this.battery(c-end,frantic);"+s.slice(end);
s=s.replace("this.beat=-1;this.cycle=0;this.bullets", "this.beat=-1;this.cycle=0;this.salvoKey='';this.bullets");
fs.writeFileSync(file,s);
const game=__dirname+'/game.js';s=fs.readFileSync(game,'utf8').replace("'turret','missile'","'turret','turret-mounted','turret-carriage','missile','enemy-pellet'");
start=s.indexOf("for(const side of [-1,1]){sprite('lightning'");end=s.indexOf("if(g.hp<=2000||g.phase==='death'",start);
s=s.slice(0,start)+`for(const side of [-1,1])sprite('lightning',side*83,295,38,115+Math.sin(g.time*40)*18,0,.7);ctx.restore();
for(const q of g.turrets()){const outer=q.id%2,sz=outer?78:94;ctx.save();ctx.translate(b.x,b.y);ctx.rotate(b.a);sprite('turret-carriage',q.baseX,q.baseY,sz,sz*1.12);ctx.strokeStyle='#667780';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(q.baseX,q.baseY);ctx.lineTo(q.localX,q.localY);ctx.stroke();ctx.restore();const dx=Math.cos(q.a),dy=Math.sin(q.a);sprite('turret-mounted',q.x-dx*q.recoil,q.y-dy*q.recoil,sz,sz,q.a+Math.PI/2);if(q.charge>0){ctx.strokeStyle='rgba(255,169,90,'+(q.charge*.6)+')';ctx.lineWidth=1.3;ctx.setLineDash([7,12]);ctx.beginPath();ctx.moveTo(q.x+dx*38,q.y+dy*38);ctx.lineTo(q.x+dx*220,q.y+dy*220);ctx.stroke();ctx.setLineDash([])}if(q.flash>0)sprite('fire',q.x+dx*43,q.y+dy*43,23,36,q.a+Math.PI/2,.95)}
`+s.slice(end);
start=s.indexOf("else{ctx.fillStyle='#08263d'",s.indexOf('for(const q of g.bullets)'));end=s.indexOf('for(const f of g.fx)',start);
s=s.slice(0,start)+"else{sprite('enemy-pellet',q.x,q.y,16,22,q.a-Math.PI/2)}}if(g.missileWarning){ctx.strokeStyle='#ffa74a';ctx.lineWidth=2;ctx.beginPath();ctx.arc(g.player.x,g.player.y,28,0,Math.PI*2);ctx.stroke()}"+s.slice(end);
fs.writeFileSync(game,s);
