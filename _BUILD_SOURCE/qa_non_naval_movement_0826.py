#!/usr/bin/env python3
"""Real-browser audit for non-naval unit spacing and movement rules."""
import functools
import http.server
import json
import os
import sys
import threading

from playwright.sync_api import sync_playwright


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args, **_kwargs):
        pass


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, _request, _client_address):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=ROOT)
    server = QuietServer(('127.0.0.1', 0), handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


RUN = r"""
(stage) => {
  let seed=(20260826+stage*977)>>>0;
  Math.random=function(){ seed=(seed*1664525+1013904223)>>>0; return seed/4294967296; };
  ASSETS.ready=true; run.mode='arcade'; run.pilot='cole';
  beginStage(stage); setState(GS.PLAY); player.reset();
  player.invuln=1e9; player.hp=1e9; player.x=VW/2; player.y=VH*0.84;
  enemies.length=0; eBullets.length=0; pBullets.length=0;

  const seen=new Map(); let uid=0, worst=null, overlaps=0;
  const add=(e)=>{
    let r=seen.get(e); if(r) return r;
    const prop=!!(e.prop||e._prop||e.pattern==='prop'||(typeof PROP_BLAST!=='undefined'&&PROP_BLAST[e.type]));
    const tank=!!(e._vkind==='tank'||/tank|apc|truck/i.test(String(e.type||''))||/^tank/.test(String(e.pattern||''))||e.pattern==='s1tank');
    const jet=!tank&&!prop&&!e._naval&&typeof isJetEnemy==='function'&&isJetEnemy(e);
    r={id:++uid,type:String(e.type||'?'),pattern:String(e.pattern||'?'),prop,tank,jet,age:0,
       minX:e.x,maxX:e.x,minWY:Infinity,maxWY:-Infinity,lastX:e.x,lastSign:0,lastTurn:-999,
       fastTurns:0,turns:0,maxSpin:0,phases:{},dirs:{},turnSamples:[]};
    seen.set(e,r); return r;
  };
  const frames=66*60;
  for(let f=0;f<frames;f++){
    player.invuln=1e9; player.hp=1e9; player.dead=false;
    if(subBoss&&subBossActive&&stageTimer-(subBoss._qaBorn||stageTimer)>1.0){ subBoss.hp=0; subBoss.dead=true; subBossActive=false; subBossDone=true; }
    if(subBoss&&!subBoss._qaBorn) subBoss._qaBorn=stageTimer;
    updatePlay(1/60);
    const src=(typeof levelSrcY==='function')?levelSrcY():0;
    for(const e of enemies){
      if(e.dead||e._naval||e.pattern==='naval') continue;
      const r=add(e); r.age++;
      r.minX=Math.min(r.minX,e.x); r.maxX=Math.max(r.maxX,e.x);
      const wy=src+e.y; r.minWY=Math.min(r.minWY,wy); r.maxWY=Math.max(r.maxWY,wy);
      r.maxSpin=Math.max(r.maxSpin,Math.abs(e.spin||0));
      if(e._phase) r.phases[e._phase]=1;
      if(e._tankPathDir!=null) r.dirs[e._tankPathDir]=1;
      if(r.jet && r.age>8){
        const dx=e.x-r.lastX, sign=Math.abs(dx)>0.08?Math.sign(dx):0;
        if(sign&&r.lastSign&&sign!==r.lastSign){
          r.turns++; if(f-r.lastTurn<15){
            r.fastTurns++;
            if(r.turnSamples.length<6){
              const near=enemies.filter(o=>o!==e&&!o.dead).map(o=>({type:String(o.type||'?'),
                dx:+(o.x-e.x).toFixed(2),dy:+(o.y-e.y).toFixed(2)}))
                .filter(o=>Math.abs(o.dx)<100&&Math.abs(o.dy)<100).slice(0,5);
              r.turnSamples.push({f,age:r.age,x:+e.x.toFixed(2),y:+e.y.toFixed(2),dx:+dx.toFixed(3),
                ap:String(e._apPhase||''),e1:String(e.e1||''),vkind:String(e._vkind||''),near});
            }
          } r.lastTurn=f;
        }
        if(sign) r.lastSign=sign;
      }
      r.lastX=e.x;
    }
    const live=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e._naval&&e.pattern!=='naval'&&
      e.y+(e.h||0)/2>viewTopY()&&e.y-(e.h||0)/2<VH&&
      e.x+(e.w||0)/2>0&&e.x-(e.w||0)/2<worldWidth());
    for(let a=0;a<live.length;a++) for(let b=a+1;b<live.length;b++){
      const A=live[a],B=live[b],ra=add(A),rb=add(B);
      if(ra.age<30||rb.age<30) continue;
      const ox=(A.w+B.w)*0.5+SEP_GAP-Math.abs(B.x-A.x);
      const oy=(A.h+B.h)*0.5+SEP_GAP-Math.abs(B.y-A.y);
      // ox/oy include the four-pixel readability gap. Count actual unit-frame burial, not a
      // subpixel shortfall inside that extra safety gap.
      if(ox<=SEP_GAP+0.5||oy<=SEP_GAP+0.5) continue;
      overlaps++;
      const ratio=Math.min(ox/Math.max(1,Math.min(A.w,B.w)),oy/Math.max(1,Math.min(A.h,B.h)));
      if(!worst||ratio>worst.ratio) worst={ratio,types:[ra.type,rb.type],patterns:[ra.pattern,rb.pattern],ox,oy,
        eligible:[sepEligible(A),sepEligible(B)],movable:[sepMovable(A),sepMovable(B)],
        entering:[!!A.enter,!!B.enter],amini:[!!A._amini,!!B._amini],age:[ra.age,rb.age],
        pos:[[A.x,A.y],[B.x,B.y]],live:live.map(q=>[String(q.type||'?'),String(q.pattern||'?'),
          +q.x.toFixed(1),+q.y.toFixed(1),q.w,q.h])};
    }
  }
  const rows=[...seen.values()].map(r=>({type:r.type,pattern:r.pattern,prop:r.prop,tank:r.tank,jet:r.jet,
    xSpan:+(r.maxX-r.minX).toFixed(3),worldYSpan:+(r.maxWY-r.minWY).toFixed(3),
    fastTurns:r.fastTurns,turns:r.turns,maxSpin:+r.maxSpin.toFixed(4),
    phases:Object.keys(r.phases),dirs:Object.keys(r.dirs),age:r.age,turnSamples:r.turnSamples}));
  return {stage,spawned:rows.length,overlaps,worst,rows,timer:stageTimer};
}
"""


def main():
    server = serve()
    errors = []
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            page = browser.new_page(viewport={'width': 1100, 'height': 1000})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{server.server_address[1]}/index.html', wait_until='load', timeout=60000)
            page.wait_for_function("() => typeof updatePlay==='function' && (window.__bofFrames|0)>4", timeout=60000)
            stages = [int(x) for x in sys.argv[1:]] or list(range(1, 9))
            for stage in stages:
                results.append(page.evaluate(RUN, stage))
            browser.close()
    finally:
        server.shutdown()

    failed = False
    for result in results:
        props = [r for r in result['rows'] if r['prop'] and r['age'] >= 10]
        tanks = [r for r in result['rows'] if r['tank'] and r['age'] >= 10]
        jets = [r for r in result['rows'] if r['jet'] and r['age'] >= 10]
        # A map-anchored prop must move down on screen with terrain scroll; lateral travel is the
        # forbidden wobble. Jet reversals are judged only on the generic sine/weave paths that the
        # runtime converts to authored curves; loops, fly-bys and attack AIs turn by design.
        moving_props = [r for r in props if r['xSpan'] > 0.01]
        wobbling_jets = [r for r in jets if r['pattern'] in ('sine', 'weave', 's1jet') and r['fastTurns'] > 2]
        spinning_tanks = [r for r in tanks if r['maxSpin'] > 0.001]
        bad = bool(result['overlaps'] or moving_props or wobbling_jets or spinning_tanks)
        failed |= bad
        print(f"stage {result['stage']}: {result['spawned']} units, {len(jets)} jets, {len(tanks)} tanks, "
              f"{len(props)} fixed hazards, overlap-frames={result['overlaps']} {'FAIL' if bad else 'OK'}")
        if result['worst']:
            print('  worst overlap:', json.dumps(result['worst'], sort_keys=True))
        if moving_props:
            print('  moving hazards:', json.dumps(moving_props[:6], sort_keys=True))
        if wobbling_jets:
            print('  rapid jet reversals:', json.dumps(wobbling_jets[:6], sort_keys=True))
        if spinning_tanks:
            print('  tank spin:', json.dumps(spinning_tanks[:6], sort_keys=True))
    if errors:
        failed = True
        print('page errors:', errors[:8])
    if failed:
        raise SystemExit(1)
    print('NON-NAVAL MOVEMENT AUDIT OK')


if __name__ == '__main__':
    main()
