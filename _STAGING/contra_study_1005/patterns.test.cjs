'use strict';
const assert=require('node:assert/strict');
const {Encounter,recipes,presets,hit,segmentDistance}=require('./patterns.js');
let checks=0;
function test(name,fn){fn();checks++;console.log('PASS '+name);}
const targetAt=t=>({x:.5+.25*Math.sin(t*2),y:.8});
test('All recipe event histories are independent of 30/60/144 Hz and skipped frames',()=>{
  for(const id of Object.keys(recipes))for(const mode of Object.keys(presets)){
    const expected=new Encounter(id,mode);expected.advance(expected.duration,targetAt);
    for(const hz of [30,60,144]){
      const e=new Encounter(id,mode);
      for(let t=0;t<e.duration;t+=1/hz)e.advance(t,targetAt);
      e.advance(e.duration,targetAt);
      assert.deepEqual(e.history,expected.history,id+' '+mode+' '+hz);
      assert.deepEqual(e.sample(e.duration),expected.sample(expected.duration));
    }
  }
});
test('Aim freezes at lock, even if target changes sides before release',()=>{
  const e=new Encounter('cannon');e.advance(.7,()=>({x:.2,y:.8}));
  e.advance(1.3,()=>({x:.9,y:.8}));
  assert.equal(e.events.find(x=>x.type==='beam').target.x,.2);
  assert(Object.isFrozen(e.locks.get('c0')));
});
test('Owner/phase cancellation clears live geometry and all pending attacks',()=>{
  for(const id of Object.keys(recipes)){
    const e=new Encounter(id);e.advance(1.3,targetAt);e.cancel('phase-change');
    const count=e.history.length;assert.equal(e.advance(100,targetAt).length,0);
    assert.equal(e.history.length,count);
    const s=e.sample();for(const k of ['bullets','beams','hazards','warnings','fx'])assert.equal(s[k].length,0);
  }
});
test('Walking gates preserve the requested gap and alternate it',()=>{
  for(const mode of Object.keys(presets)){
    const e=new Encounter('gate',mode);e.advance(e.cfg.tell+.01,targetAt);
    const s=e.sample(),g=e.events.find(x=>x.type==='curtain');
    assert(s.bullets.length>0);
    for(const b of s.bullets)assert(Math.abs(b.x-g.gapX)>=g.gap/2+b.radius-1e-9);
    const next=e.plan.filter(x=>x.type==='curtain')[1];assert.notEqual(g.gapX,next.gapX);
    assert(g.gap>.1);
  }
});
test('Radial exits remain empty for every preset',()=>{
  for(const mode of Object.keys(presets)){
    const e=new Encounter('radial',mode);e.advance(e.cfg.tell+.8,()=>({x:.5,y:.8}));
    const s=e.sample();assert(s.bullets.length>0);
    assert.equal(hit(s,{x:.5,y:.25+.8*e.cfg.speed*.85}),false);
  }
});
test('Swept projectile collision catches a crossing missed by endpoint checks',()=>{
  const s={bullets:[{x:.7,y:.5,vx:1,vy:0,radius:.01}],beams:[],hazards:[]};
  assert.equal(hit(s,{x:.5,y:.5},.01),false);
  assert.equal(hit(s,{x:.5,y:.5},.01,{x:.5,y:.5},.4),true);
});
test('Warnings precede damaging releases and have bounded recovery',()=>{
  for(const id of Object.keys(recipes))for(const mode of Object.keys(presets)){
    const e=new Encounter(id,mode);
    assert(e.duration-e.end>=1.1);
    for(const w of e.warnings)assert(w.fire-w.start>=.95-1e-9);
    for(const p of e.plan.filter(p=>p.key&&p.type!=='lock'))assert(e.plan.some(l=>l.type==='lock'&&l.key===p.key&&l.at<p.at));
  }
});
test('Invalid time, recipe and target inputs fail explicitly',()=>{
  assert.throws(()=>new Encounter('missing'));const e=new Encounter();
  assert.throws(()=>e.advance(NaN,targetAt));e.advance(1,targetAt);
  assert.throws(()=>e.advance(.5,targetAt));assert.throws(()=>e.advance(2));
  assert.throws(()=>new Encounter().advance(2,()=>({x:NaN,y:0})));
  assert.equal(segmentDistance({x:0,y:0},{x:0,y:0},{x:0,y:0}),0);
});
console.log(checks+' meaningful checks passed; 18 recipe/preset combinations exercised.');
