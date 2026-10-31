/* Original BOF study candidates. Normalized arena units; seconds; no game globals.
   UMD works via require() or a plain browser script. Render art separately. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.BOFPatterns = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const TAU = Math.PI * 2;
  const presets = Object.freeze({
    Easy: Object.freeze({ tell: 1.35, speed: .27, gap: .34, recovery: 1.7 }),
    Normal: Object.freeze({ tell: 1.15, speed: .32, gap: .30, recovery: 1.4 }),
    Furious: Object.freeze({ tell: .95, speed: .37, gap: .27, recovery: 1.15 })
  });
  const recipes = Object.freeze({
    cannon: { name: 'Committed cannon', lesson: 'Bait the aim; leave after LOCK; return during recovery.', source: '30:29 Big Magnum', fit: 'Harrier / turret hardpoint' },
    gate: { name: 'Walking gate', lesson: 'Enter the first opening, then travel with the next opening.', source: 'Omni Bot / reconfiguring bodies', fit: 'Code-wall encounter variation' },
    sweep: { name: 'Raking arm', lesson: 'Read the start edge. Cross before release or stay ahead of the rake.', source: 'Takedda / Spear Sphere geometry', fit: 'Hammer or articulated cannon' },
    radial: { name: 'Broken pressure ring', lesson: 'Find the announced angular exit and move through it.', source: 'Radial arrangements / constellation forms', fit: 'Reactor discharge / alien core' },
    pincer: { name: 'Staggered crossfire', lesson: 'Bait one arm, change sides, then bait the other. Bursts alternate.', source: 'Cyborg Bros / twin emitters', fit: 'Herald cannon arms / dual emitters' },
    eruption: { name: 'Eruption relay', lesson: 'Drop a mark, move away, leave room for the next mark.', source: 'Mandrake / successive arena transformations', fit: 'Existing marked chromium eruptions' }
  });
  const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
  function point(p) {
    if (!p || !Number.isFinite(p.x) || !Number.isFinite(p.y)) throw new TypeError('Finite target x/y required');
    return Object.freeze({x:clamp(p.x,.03,.97), y:clamp(p.y,.03,.97)});
  }
  function angle(a,b) { return Math.atan2(b.y-a.y,b.x-a.x); }
  function delta(a,b) { return Math.atan2(Math.sin(a-b),Math.cos(a-b)); }
  function segmentDistance(p,a,b) {
    const dx=b.x-a.x,dy=b.y-a.y,den=dx*dx+dy*dy;
    const t=den ? clamp(((p.x-a.x)*dx+(p.y-a.y)*dy)/den,0,1) : 0;
    return Math.hypot(p.x-a.x-t*dx,p.y-a.y-t*dy);
  }
  class Encounter {
    constructor(id='cannon',difficulty='Normal',cycle=0) {
      if (!recipes[id] || !presets[difficulty]) throw new RangeError('Unknown recipe or difficulty');
      this.id=id; this.cfg=presets[difficulty]; this.cycle=cycle; this.time=-1;
      this.cancelled=false; this.locks=new Map(); this.events=[]; this.history=[]; this.cursor=0;
      this.plan=[]; this.warnings=[];
      this.build();
      this.plan.sort((a,b)=>a.at-b.at || a.order-b.order);
    }
    add(at,type,data={}) { this.plan.push({at,type,order:this.plan.length,...data}); }
    tell(key,start,lock,fire,shape) {
      this.warnings.push({key,start,lock,fire,...shape});
      this.add(lock,'lock',{key});
    }
    build() {
      const q=this.cfg,T=q.tell;
      const emitter={x:.5,y:.16};
      if(this.id==='cannon') {
        for(let n=0;n<2;n++) {
          const s=n*2.7,k='c'+n;
          this.tell(k,s,s+T*.55,s+T,{kind:'lane',emitter,width:.065});
          this.add(s+T,'beam',{key:k,kind:'lane',emitter,width:.065,duration:.65});
          this.add(s+T,'fx',{emitter,name:'pressure'});
        }
        this.end=2.7+T+.65;
      } else if(this.id==='gate') {
        for(let n=0;n<3;n++) {
          const s=n*1.5,gapX=.5+((n+this.cycle)%2===0?-.14:.14);
          this.warnings.push({key:'g'+n,start:s,fire:s+T,kind:'gate',gapX,gap:q.gap});
          this.add(s+T,'curtain',{gapX,gap:q.gap,y:.16,speed:q.speed,radius:.012,life:3.5});
        }
        this.end=3+T+3.5;
      } else if(this.id==='sweep') {
        const right=this.cycle%2===0;
        this.warnings.push({key:'s',start:0,fire:T,kind:'sweep',x0:right?.14:.86,x1:right?.86:.14,width:.055});
        this.add(T,'beam',{kind:'sweep',x0:right?.14:.86,x1:right?.86:.14,y:.16,width:.055,duration:2.6});
        this.add(T,'fx',{emitter,name:'pressure'});
        this.end=T+2.6;
      } else if(this.id==='radial') {
        this.tell('r',0,T*.55,T,{kind:'radial',emitter,gapAngle:.62});
        this.add(T,'ring',{key:'r',emitter,speed:q.speed*.85,gapAngle:.62,count:24,radius:.011,life:4});
        this.add(T,'fx',{emitter,name:'pressure'});
        this.end=T+4;
      } else if(this.id==='pincer') {
        for(let n=0;n<2;n++) {
          const s=n*2.5,k='p'+n,e={x:(n+this.cycle)%2===0?.14:.86,y:.16};
          this.tell(k,s,s+T*.55,s+T,{kind:'fan',emitter:e,halfAngle:.16});
          for(let b=0;b<3;b++) this.add(s+T+b*.16,'fan',{key:k,emitter:e,speed:q.speed,count:3,spread:.15,radius:.012,life:3.5});
        }
        this.end=2.5+T+.32+3.5;
      } else {
        for(let n=0;n<3;n++) {
          const s=n*1.5,k='e'+n;
          this.tell(k,s,s,s+T,{kind:'circle',radius:.07});
          this.add(s+T,'hazard',{key:k,radius:.07,duration:.6});
        }
        this.end=3+T+.6;
      }
      this.duration=this.end+q.recovery;
      this.add(this.end,'recovery');
      this.add(this.duration,'complete');
    }
    advance(to,targetAt) {
      if(!Number.isFinite(to)||to<0||to<this.time) throw new RangeError('Monotonic finite seconds required');
      if(typeof targetAt!=='function') throw new TypeError('Supply targetAt(eventTime) for deterministic aim');
      const emitted=[];
      if(!this.cancelled) while(this.cursor<this.plan.length&&this.plan[this.cursor].at<=to) {
        const p=this.plan[this.cursor++];
        if(p.type==='lock') this.locks.set(p.key,point(targetAt(p.at)));
        const e={...p,target:p.key?this.locks.get(p.key):undefined};
        this.events.push(e); this.history.push(e); emitted.push(e);
      }
      this.time=to;
      return emitted;
    }
    cancel(reason='owner-destroyed') {
      this.cancelled=true; this.events=[]; this.warnings=[];
      this.history.push({at:Math.max(0,this.time),type:'cleanup',reason});
    }
    sample(t=this.time,target={x:.5,y:.8}) {
      if(t>this.time||t<0) throw new RangeError('Advance before sampling');
      const bullets=[],beams=[],hazards=[],fx=[],warnings=[];
      if(this.cancelled) return {bullets,beams,hazards,fx,warnings,phase:'cancelled'};
      const bullet=(e,a)=>{
        const age=t-e.at;
        if(age>=0&&age<e.life) bullets.push({id:e.order+':'+a,x:e.emitter.x+Math.cos(a)*e.speed*age,y:e.emitter.y+Math.sin(a)*e.speed*age,vx:Math.cos(a)*e.speed,vy:Math.sin(a)*e.speed,radius:e.radius,spawn:e.at});
      };
      for(const e of this.events) {
        const age=t-e.at;
        if(age<0) continue;
        if(e.type==='beam'&&age<e.duration) {
          if(e.kind==='lane') {
            const a=angle(e.emitter,e.target);
            beams.push({a:e.emitter,b:{x:e.emitter.x+Math.cos(a)*1.5,y:e.emitter.y+Math.sin(a)*1.5},width:e.width,kind:e.kind});
          } else {
            const x=e.x0+(e.x1-e.x0)*age/e.duration;
            beams.push({a:{x,y:e.y},b:{x,y:1.04},width:e.width,kind:e.kind});
          }
        } else if(e.type==='curtain'&&age<e.life) {
          for(let i=0;i<=40;i++) { const x=i/40;
            if(Math.abs(x-e.gapX)>=e.gap/2+e.radius) bullets.push({id:e.order+':'+i,x,y:e.y+age*e.speed,vx:0,vy:e.speed,radius:e.radius,spawn:e.at});
          }
        } else if(e.type==='ring') {
          const exit=angle(e.emitter,e.target);
          for(let i=0;i<e.count;i++){const a=i*TAU/e.count;if(Math.abs(delta(a,exit))>e.gapAngle)bullet(e,a);}
        } else if(e.type==='fan') {
          const a=angle(e.emitter,e.target);
          for(let i=0;i<e.count;i++)bullet(e,a+(i-(e.count-1)/2)*e.spread);
        } else if(e.type==='hazard'&&age<e.duration) hazards.push({center:e.target,radius:e.radius});
        else if(e.type==='fx'&&age<.6) fx.push({center:e.emitter,frame:Math.min(11,Math.floor(age*20))});
      }
      for(const w of this.warnings) if(t>=w.start&&t<w.fire) {
        warnings.push({...w,target:this.locks.get(w.key)||point(target),committed:t>=w.lock,progress:(t-w.start)/(w.fire-w.start)});
      }
      return {bullets,beams,hazards,fx,warnings,phase:t>=this.duration?'complete':t>=this.end?'recovery':warnings.length?'warning':'attack'};
    }
  }
  function hit(snapshot,position,radius=.012,previous=position,dt=0) {
    for(const b of snapshot.bullets) {
      // Relative swept motion catches crossings between ticks, including fast bullets.
      const travel=Math.max(0,dt),r=b.radius+radius;
      const old={x:b.x-b.vx*travel-previous.x,y:b.y-b.vy*travel-previous.y};
      const now={x:b.x-position.x,y:b.y-position.y};
      if(segmentDistance({x:0,y:0},old,now)<=r)return true;
    }
    for(const b of snapshot.beams) if(segmentDistance(position,b.a,b.b)<=b.width/2+radius || segmentDistance(previous,b.a,b.b)<=b.width/2+radius)return true;
    for(const h of snapshot.hazards) if(segmentDistance(h.center,previous,position)<=h.radius+radius)return true;
    return false;
  }
  return {Encounter,presets,recipes,hit,segmentDistance};
});
