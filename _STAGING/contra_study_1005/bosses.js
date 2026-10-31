/* Original BOF encounter candidates, world pixels / seconds. No production globals.
   pose() supplies the SAME part transforms used by collision and weapon sockets. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.BOFBosses=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const TAU=Math.PI*2,clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const mix=(a,b,t)=>a+(b-a)*clamp(t,0,1);
  const definitions={
    coupler:{name:'Split Coupler',source:'02 Blade · 27 Cyborg Bros',lesson:'Bait alternating arms; disarm a socket. Cross around the legs when the torso separates; punish the reconnect.',phases:['twin','detach']},
    spindle:{name:'Spindle Bastion',source:'05 Spike · 25 Takedda · 30 Spear Sphere',lesson:'Read alternating extended spokes. Destroy their tips. After the shell retracts, change lanes for the compact-body crossing.',phases:['spokes','cross']},
    regent:{name:'Rupture Regent',source:'32 mutation-route Colonel',lesson:'Duelist crossing → looped neck → hollow mask orbit. Change the escape route with the silhouette; attack the low core during recovery.',phases:['cross','coil','orbit']},
    payload:{name:'Payload Cathedral',source:'35 Living Warhead',lesson:'Breach sockets → serpent column → articulated arms → reaching maw. Each form has its own owners, committed path and grounded recovery.',phases:['breach','column','arms','maw']}
  };
  function distance(p,a,b){const x=b.x-a.x,y=b.y-a.y,z=x*x+y*y,t=z?clamp(((p.x-a.x)*x+(p.y-a.y)*y)/z,0,1):0;return Math.hypot(p.x-a.x-t*x,p.y-a.y-t*y);}
  function collides(p,r,s){return s.kind==='segment'?distance(p,s.a,s.b)<=r+s.r:Math.hypot(p.x-s.x,p.y-s.y)<=r+s.r;}
  class Boss {
    constructor(id='regent',difficulty='Normal',width=960,height=600){
      if(!definitions[id]||!['Easy','Normal','Furious'].includes(difficulty))throw new RangeError('Unknown encounter/difficulty');
      if(!Number.isFinite(width)||!Number.isFinite(height)||width<300||height<300)throw new RangeError('Arena must be finite and at least 300px');
      this.id=id;this.def=definitions[id];this.W=width;this.H=height;this.difficulty=difficulty;
      this.tell=difficulty==='Easy'?1.45:difficulty==='Furious'?1.05:1.25;
      this.active=1.3;this.recovery=2.4;this.period=this.tell+this.active+this.recovery;
      this.time=0;this.frame=0;this.phase=0;this.phaseStart=0;this.hp=100;this.transitionUntil=0;this.dead=false;this.cancelled=false;
      this.parts={};this.projectiles=[];this.events=[];this.fx=[];this.lock=null;this.cycle=-1;this.lastRelease=-1;this.recoveryCycle=-1;
      this.configure();
    }
    configure(){
      const k=this.kind;this.parts={};
      const add=(id,hp)=>this.parts[id]={hp,max:hp,dead:false};
      if(['twin','breach','arms'].includes(k)){add('left',30);add('right',30);}
      if(k==='spokes')for(let i=0;i<4;i++)add('spoke'+i,22);
      if(['coil','column','maw'].includes(k))add('mouth',36);
      if(k==='orbit')for(let i=0;i<8;i++)add('mask'+i,12);
      this.cycle=-1;this.lastRelease=-1;this.recoveryCycle=-1;this.lock=null;
    }
    get kind(){return this.def.phases[this.phase];}
    get state(){
      if(this.cancelled)return 'cancelled';if(this.dead)return 'defeated';if(this.time<this.transitionUntil)return 'transition';
      const t=(this.time-this.phaseStart)%this.period;
      return t<this.tell?'tell':t<this.tell+this.active?'active':'recovery';
    }
    alive(id){return id==='core'?!this.dead:!!this.parts[id]&&!this.parts[id].dead;}
    event(type,data={}){this.events.push({at:this.time,type,phase:this.phase,...data});}
    effect(name,x,y,owner='core'){this.fx.push({name,x,y,owner,start:this.time,life:name==='breach'?1:.65});this.event('fx',{name,x,y,owner});}
    clear(owner){this.projectiles=this.projectiles.filter(b=>b.owner!==owner);this.fx=this.fx.filter(f=>f.owner!==owner);}
    cancel(reason='exit'){this.cancelled=true;this.projectiles=[];this.fx=[];this.lock=null;this.event('cancel',{reason});}
    nextPhase(){
      if(this.dead||this.cancelled)return;
      this.projectiles=[];this.fx=[];this.lock=null;
      if(this.phase+1>=this.def.phases.length){this.dead=true;this.event('defeat');this.effect('breach',this.W*.5,this.H*.5);return;}
      this.phase++;this.hp=100;this.transitionUntil=this.time+1;this.phaseStart=this.transitionUntil;
      this.configure();this.event('phase',{kind:this.kind});this.effect('breach',this.W*.5,this.H*.4);
    }
    damage(id,amount){
      if(!Number.isFinite(amount)||amount<=0)throw new RangeError('Positive finite damage required');
      if(this.cancelled||this.dead||this.state==='transition')return false;
      if(id==='core'){
        if(this.state!=='recovery')return false;
        this.hp=Math.max(0,this.hp-amount);this.event('damage',{owner:id,hp:this.hp});if(!this.hp)this.nextPhase();return true;
      }
      const part=this.parts[id];if(!part||part.dead)return false;
      part.hp=Math.max(0,part.hp-amount);this.event('damage',{owner:id,hp:part.hp});
      if(!part.hp){const p=this.pose().parts.find(p=>p.id===id);part.dead=true;this.clear(id);this.event('disarm',{owner:id});if(p)this.effect('joint',p.x,p.y,id);}
      return true;
    }
    advance(to,targetAt=()=>({x:this.W*.3,y:this.H*.8})){
      if(!Number.isFinite(to)||to<this.time)throw new RangeError('Monotonic finite seconds required');
      const start=this.events.length,end=Math.floor((to+1e-8)*120);
      while(this.frame<end){this.frame++;this.time=this.frame/120;this.tick(targetAt);}
      return this.events.slice(start);
    }
    tick(targetAt){
      if(this.cancelled||this.dead)return;
      this.projectiles=this.projectiles.filter(b=>this.alive(b.owner)&&this.time-b.start<b.life);
      this.fx=this.fx.filter(f=>this.time-f.start<f.life);
      if(this.state==='transition')return;
      const t=this.time-this.phaseStart,c=Math.floor(t/this.period),local=t-c*this.period;
      if(c!==this.cycle){this.cycle=c;this.lock=null;this.lastRelease=-1;this.event('tell',{cycle:c,kind:this.kind});}
      const target=()=>{const p=targetAt(this.time);if(!p||!Number.isFinite(p.x)||!Number.isFinite(p.y))throw new TypeError('Finite world target required');return{x:clamp(p.x,30,this.W-30),y:clamp(p.y,this.H*.35,this.H*.82)};};
      if(!this.lock&&local>=this.tell*.65){this.lock=Object.freeze(target());this.event('lock',{target:this.lock,cycle:c});}
      if(local>=this.tell&&local<this.tell+this.active){
        const slot=Math.floor((local-this.tell+1e-8)/.22);
        if(slot>this.lastRelease){this.lastRelease=slot;this.release(slot);}
      }
      if(this.state==='recovery'&&this.recoveryCycle!==c){this.recoveryCycle=c;this.event('recovery');this.effect('contact',this.W*.5,this.H*.7);}
    }
    shot(owner,p,angle,speed=190,r=8,life=2.2){if(!this.alive(owner))return;this.projectiles.push({owner,x:p.x,y:p.y,angle,speed,r,life,start:this.time});this.event('shot',{owner,angle});}
    release(slot){
      const k=this.kind,pose=this.pose();
      if(k==='twin'||k==='breach'){
        const id=this.cycle%2?'right':'left',p=pose.parts.find(p=>p.id===id);if(!p||!this.alive(id)||slot>2)return;
        const a=Math.atan2(this.lock.y-p.y,this.lock.x-p.x);
        for(const d of [-.12,0,.12])this.shot(id,p,a+d,this.difficulty==='Furious'?220:180);
        if(!slot)this.effect('joint',p.x,p.y,id);
      }else if(k==='column'){
        const p=pose.parts.find(p=>p.id==='mouth');if(!p||!this.alive('mouth'))return;
        this.shot('mouth',{x:this.lock.x,y:p.y},Math.PI/2,220,12,1.9);
        if(!slot)this.effect('joint',this.lock.x,p.y,'mouth');
      }else if(k==='coil'||k==='maw'){
        const p=pose.parts.find(p=>p.id==='mouth');if(!p||slot>1)return;
        const a=Math.atan2(this.lock.y-p.y,this.lock.x-p.x);
        for(const d of [-.3,.3])this.shot('mouth',p,a+d,150,10,1.8);
      }
    }
    pose(target={x:this.W*.3,y:this.H*.8}){
      const W=this.W,H=this.H,k=this.kind,state=this.state;
      const local=Math.max(0,(this.time-this.phaseStart)%this.period),a=clamp((local-this.tell)/this.active,0,1);
      const rec=state==='recovery'?clamp((local-this.tell-this.active)/.35,0,1):0;
      const locked=this.lock||target,c=this.cycle<0?0:this.cycle;
      const root={x:W*.5,y:mix(H*(k==='spokes'?.42:.32),H*.70,rec)};
      const parts=[],segments=[],warnings=[],hazards=[];
      const part=(id,x,y,r=19)=>{if(this.alive(id))parts.push({id,x,y,r,hp:id==='core'?this.hp:this.parts[id].hp,vulnerable:id!=='core'||state==='recovery'});};
      const seg=(owner,p,q,r=11)=>{if(this.alive(owner)){const s={kind:'segment',owner,a:p,b:q,r};segments.push(s);if(state==='active')hazards.push(s);}};
      const warn=(owner,p,q,r=15)=>{if(state==='tell'&&this.alive(owner))warnings.push({kind:'segment',owner,a:p,b:q,r,locked:!!this.lock});};
      if(k==='cross'||k==='detach'){
        const y=clamp(locked.y,H*.40,H*.77),start=c%2?W*.80:W*.20,end=c%2?W*.20:W*.80;
        root.x=state==='active'?mix(start,end,a):state==='recovery'?mix(end,W*.5,rec):start;
        root.y=state==='active'?y:state==='recovery'?mix(y,H*.70,rec):y;
        warn('core',{x:start,y},{x:end,y},31);
        if(k==='detach')segments.push({kind:'segment',owner:'pedestal',a:{x:W*.48,y:H*.60},b:{x:W*.52,y:H*.66},r:18});
      }else if(k==='twin'||k==='breach'){
        for(const [id,x] of [['left',W*.30],['right',W*.70]]){
          const p={x,y:mix(H*.34,H*.70,rec)};part(id,p.x,p.y,24);seg(id,root,p,9);
          if((c%2?'right':'left')===id)warn(id,p,{x:locked.x,y:locked.y},24);
        }
      }else if(k==='spokes'||k==='arms'){
        const count=k==='arms'?2:4;
        for(let i=0;i<count;i++){
          const id=k==='arms'?(i?'right':'left'):'spoke'+i;
          const theta=k==='arms'?(i?0:Math.PI):(Math.PI/4+i*TAU/4);
          const selected=k==='arms'?i===c%2:i%2===c%2;
          const length=state==='recovery'?55:state==='tell'?80:selected?mix(80,Math.min(W,H)*.37,Math.sin(a*Math.PI)):80;
          const turn=selected&&state==='active'?Math.sin(a*Math.PI)*.40:0;
          const angle=theta+turn,p={x:root.x+Math.cos(angle)*length,y:root.y+Math.sin(angle)*length};
          const mid={x:mix(root.x,p.x,.55),y:mix(root.y,p.y,.55)-18*Math.sin(a*Math.PI)};
          seg(id,root,mid,10);seg(id,mid,p,10);part(id,p.x,p.y,21);
          if(selected)warn(id,root,{x:root.x+Math.cos(theta+.4)*Math.min(W,H)*.37,y:root.y+Math.sin(theta+.4)*Math.min(W,H)*.37},30);
        }
      }else if(k==='coil'||k==='maw'||k==='column'){
        const side=c%2?-1:1,points=[root];
        if(k==='column'){
          const tip={x:state==='active'?locked.x:mix(root.x,locked.x,local/this.tell),y:H*.26};
          for(let i=1;i<=8;i++){const z=i/8;points.push({x:mix(root.x,tip.x,z)+Math.sin(z*Math.PI)*side*45,y:mix(root.y,tip.y,z)});}
          warn('mouth',{x:locked.x,y:H*.26},{x:locked.x,y:H*.90},22);
        }else{
          const ext=state==='active'?Math.sin(a*Math.PI):state==='tell'?.08:0;
          for(let i=1;i<=16;i++){const z=i/16,angle=side*(z*TAU*.78-Math.PI/2);points.push({x:root.x+Math.cos(angle)*W*.22*z*ext,y:root.y+Math.sin(angle)*H*.31*z*ext+H*.14*z});}
          if(k==='maw'&&state==='active')for(let i=1;i<points.length;i++){const z=i/(points.length-1);points[i]={x:mix(root.x,locked.x,z*ext),y:mix(root.y,locked.y,z*ext)};}
          warn('mouth',root,k==='maw'?locked:{x:root.x+side*W*.25,y:H*.62},28);
        }
        if(this.alive('mouth')){for(let i=1;i<points.length;i++)seg('mouth',points[i-1],points[i],12);const p=points.at(-1);part('mouth',p.x,p.y,24);}
      }else if(k==='orbit'){
        const unit=Math.min(W,H)/600;
        const radius=unit*(state==='active'?110+45*Math.sin(a*Math.PI):state==='tell'?mix(45,110,local/this.tell):mix(110,45,rec));
        root.x=state==='active'?W*.5+Math.sin(a*TAU)*W*.15:W*.5;
        for(let i=0;i<8;i++){const id='mask'+i,theta=i*TAU/8+this.time*.5;part(id,root.x+Math.cos(theta)*radius,root.y+Math.sin(theta)*radius,17);}
        if(state==='tell')warnings.push({kind:'orbit',owner:'core',x:root.x,y:root.y,r:radius,locked:true});
      }
      part('core',root.x,root.y,k==='cross'?25:32);
      if(state==='active'){
        if(['cross','detach'].includes(k))hazards.push({kind:'circle',owner:'core',...root,r:28});
        for(const p of parts.filter(p=>p.id!=='core'))hazards.push({kind:'circle',owner:p.id,x:p.x,y:p.y,r:p.r});
      }
      if(k==='detach'&&state!=='transition')hazards.push(...segments.filter(s=>s.owner==='pedestal'));
      const bullets=this.projectiles.map(b=>{const age=this.time-b.start;return{...b,kind:'circle',x:b.x+Math.cos(b.angle)*b.speed*age,y:b.y+Math.sin(b.angle)*b.speed*age};});
      if(['transition','defeated','cancelled'].includes(state))return{state,kind:k,parts:[],segments:[],warnings:[],hazards:[],bullets:[],fx:this.fx};
      return{state,kind:k,parts,segments,warnings,hazards,bullets,fx:this.fx};
    }
    hit(point,r=12){const p=this.pose();return [...p.hazards,...p.bullets].some(s=>collides(point,r,s));}
    hitPart(point,r=5){return this.pose().parts.filter(p=>p.vulnerable&&collides(point,r,{kind:'circle',...p})).sort((a,b)=>Math.hypot(point.x-a.x,point.y-a.y)-Math.hypot(point.x-b.x,point.y-b.y))[0];}
  }
  return{Boss,definitions,distance,collides};
});
