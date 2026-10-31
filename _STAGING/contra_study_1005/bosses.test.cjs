'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {Boss,definitions,collides}=require('./bosses.js');
const target=()=>({x:210,y:450});
test('every form at every preset reaches grounded vulnerability and remains finite',()=>{
  for(const id of Object.keys(definitions))for(const difficulty of ['Easy','Normal','Furious']){
    const b=new Boss(id,difficulty);
    for(let phase=0;phase<b.def.phases.length;phase++){
      b.advance(b.phaseStart+b.tell+.7,target);
      const p=b.pose();for(const x of p.parts)assert.ok(Number.isFinite(x.x)&&Number.isFinite(x.y));
      b.advance(b.phaseStart+b.tell+b.active+.5,target);
      const core=b.pose().parts.find(p=>p.id==='core');assert.ok(core.vulnerable);assert.ok(Math.abs(core.y-420)<.001);
      assert.ok(b.damage('core',100));
    }
    assert.ok(b.dead);assert.equal(b.pose().hazards.length,0);assert.equal(b.pose().bullets.length,0);
  }
});
test('lock is immutable and body crossing follows committed lane',()=>{
  const b=new Boss('regent');b.advance(1,target);const lock=b.lock;
  b.advance(1.8,()=>({x:850,y:210}));assert.equal(b.lock,lock);assert.deepEqual(b.lock,target());
  assert.equal(b.pose().parts.find(p=>p.id==='core').y,450);assert.ok(b.hit({x:b.pose().parts.at(-1).x,y:450}));
});
test('destroying one emitter removes its existing and queued shots, leaves the other functional',()=>{
  const b=new Boss('coupler');b.advance(1.6,target);assert.ok(b.projectiles.some(p=>p.owner==='left'));
  b.damage('left',30);assert.equal(b.projectiles.length,0);assert.ok(!b.pose().parts.some(p=>p.id==='left'));
  b.advance(b.period+1.6,target);assert.ok(b.projectiles.some(p=>p.owner==='right'));assert.ok(!b.projectiles.some(p=>p.owner==='left'));
});
test('phase boundary clears old owner projectiles, locks, parts and collision',()=>{
  const b=new Boss('payload');b.advance(1.6,target);assert.ok(b.projectiles.length);b.nextPhase();
  assert.equal(b.projectiles.length,0);assert.equal(b.lock,null);assert.equal(b.state,'transition');assert.equal(b.hit(target()),false);
  b.advance(b.transitionUntil+.1,target);assert.equal(b.kind,'column');assert.ok(b.alive('mouth'));assert.ok(!b.alive('left'));
  b.cancel('encounter-exit');b.advance(b.time+10,target);assert.equal(b.pose().hazards.length,0);assert.equal(b.projectiles.length,0);
});
test('articulated endpoints and collision share exact transforms; disarm clears the chain',()=>{
  const b=new Boss('spindle');b.advance(b.tell+.65,target);const p=b.pose();
  for(const tip of p.parts.filter(p=>p.id!=='core')){const segments=p.segments.filter(s=>s.owner===tip.id);assert.deepEqual(segments.at(-1).b,{x:tip.x,y:tip.y});assert.ok(b.hit(tip,0));}
  b.damage('spoke0',22);assert.ok(!b.pose().hazards.some(h=>h.owner==='spoke0'));
});
test('mask orbit has a genuinely hollow centre and independent mask collision',()=>{
  const b=new Boss('regent');b.nextPhase();b.nextPhase();b.advance(b.phaseStart+b.tell+.5,target);
  const p=b.pose(),core=p.parts.find(p=>p.id==='core'),mask=p.parts.find(p=>p.id==='mask0');
  assert.equal(b.hit(core,12),false);assert.ok(b.hit(mask,0));b.damage('mask0',12);assert.ok(!b.pose().hazards.some(h=>h.owner==='mask0'));
});
test('catch-up processing matches 30/60/144Hz without losing release slots',()=>{
  function run(hz){const b=new Boss('payload');for(let i=1;i<=hz*12;i++)b.advance(i/hz,target);return b.events;}
  assert.deepEqual(run(30),run(60));assert.deepEqual(run(60),run(144));
  const events=run(60);assert.equal(events.filter(e=>e.type==='recovery').length,2);
});
test('world-pixel capsules preserve gaps and reject invalid inputs',()=>{
  const s={kind:'segment',a:{x:10,y:10},b:{x:100,y:10},r:5};assert.ok(collides({x:50,y:15},0,s));assert.equal(collides({x:50,y:16},0,s),false);
  assert.throws(()=>new Boss('absent'));assert.throws(()=>new Boss('regent','Normal',NaN));const b=new Boss();assert.throws(()=>b.advance(NaN));assert.throws(()=>b.damage('core',-1));
});
test('default arena keeps articulated tips visible throughout their sweep',()=>{
  for(const id of ['spindle','payload']){
    const b=new Boss(id);if(id==='payload'){b.nextPhase();b.nextPhase();}
    for(let i=1;i<=600;i++){
      b.advance(b.phaseStart+i/120,target);
      for(const p of b.pose().parts)assert.ok(p.x-p.r>=0&&p.x+p.r<=b.W&&p.y-p.r>=0&&p.y+p.r<=b.H,`${id} ${p.id} ${b.time}`);
    }
  }
});
