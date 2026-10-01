"""patch_launch_scale_1001c - one ship size from the intro into PLAY, and no dead stop in any launch.

Mike, 1001: "keep it at gameplay scale at all times and not do that or any sudden stops on any levels?
always remain in motion but just slow down as we get to the intro's and stuff unless its the fast levels
like space and the sky levels."

Every edit is an anchored replace that must match exactly once, or the script refuses and writes nothing
(CLAUDE.md 0906v: a str.replace that silently no-ops is a patch that did not land).
"""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'assets', 'game.js')
src = open(P, 'rb').read().decode('utf8')
assert '\r\n' not in src, 'game.js is LF'

EDITS = []
def E(old, new):
    EDITS.append((old, new))

# 1. PLAY draws the hull at SHIP_DRAW_H (0819c); the pose said 76.1, so every launch that "settled onto the
#    play pose" settled 27% too big and popped down at GO.
E("""    y: player.y,
    h: ((player.h||34)*2.05)/cf
  };""",
"""    y: player.y,
    /* ⚠ THE HEIGHT PLAY ACTUALLY DRAWS (1001c). _drawPlayerCore blits the hull at SHIP_DRAW_H (0819c) - this
       still returned 0810a's content-height formula, 76.1 for Cole, so every launch settled the ship 27% TOO BIG
       for the countdown and PLAY cut it back to 60 at GO: Mike's "scaling in/out of our ship from the intro to
       the gameplay". Measured by probe_launchscale_1001c.py off the blits themselves. drawShipSprite takes the
       same canvas height _drawPlayerCore does, so this is the one number both sides draw. */
    h: SHIP_DRAW_H
  };""")

# 2. constants beside the countdown scroll
E("""const LAUNCH_COUNTDOWN_SCROLL=24;  // encounter clock; Stage 5 visual scroll stays at cruise""",
"""const LAUNCH_COUNTDOWN_SCROLL=24;  // encounter clock; Stage 5 visual scroll stays at cruise
/* ⚠ NO GROUND LAUNCH STOPS ANY MORE (1001c). Mike: "not do that or any sudden stops on any levels? always remain
   in motion but just slow down as we get to the intro's". The brake used to ease 1750 -> 0 on a 2 s clock while
   the level had already landed ~1160 px into it, so the world stood DEAD STILL (measured: 0 px/s for ~0.6 s)
   and then crawled at 24 for the countdown and jumped to 40 at GO. Now the brake is DISTANCE-driven: it starts
   LAUNCH_BRAKE_DIST short of the join and decelerates so it reaches PLAY's own 40 px/s at exactly the frame the
   level lands, and the countdown keeps that same 40 into PLAY. One speed from the landing on - no stop, no step. */
const LAUNCH_PLAY_SCROLL=40;       // drawLevelMaster's own rate (mapScroll + dt*40)
const LAUNCH_LAND=SEG_B3+1400;     // the dist at which the level joins the connector (launchConnDy)
const LAUNCH_BRAKE_DIST=2400;      // ~2.7 s of braking from 1750 to 40""")

E("""function launchConnDy(){
  const LAND=SEG_B3+1400;""",
"""function launchConnDy(){
  const LAND=LAUNCH_LAND;""")

# 3. launch init: reset the brake latch
E("""    drawLaunch._warpAudio=false; drawLaunch._spPose=null;
    /* ⚠ THE STAGE-5 BUILD""",
"""    drawLaunch._warpAudio=false; drawLaunch._spPose=null; drawLaunch._brkV0=null; drawLaunch._brkK=0;
    /* ⚠ THE STAGE-5 BUILD""")

# 4. ground runs hand over to the brake early enough to slow down rather than stop
E("""    const _launchEnd=_gravityStage?(SEG_B3+SEG_B1+240):(SEG_B3+240);""",
"""    const _launchEnd=_gravityStage?(SEG_B3+SEG_B1+240):(_space||_s6)?(SEG_B3+240):(LAUNCH_LAND-LAUNCH_BRAKE_DIST);""")

# 5. the brake
E("""    drawLaunch._pt+=dt; const p=clamp(drawLaunch._pt/2.0,0,1);
    drawLaunch._spd=lerp(1750,((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:0),_ease(p));
    drawLaunch._dist+=drawLaunch._spd*dt;                          /* level keeps scrolling in smoothly while braking */
    if(drawLaunch._pt>=2.0){ drawLaunch._phase='settle'; drawLaunch._pt=0; }""",
"""    drawLaunch._pt+=dt;
    if(_space){
      /* from the speed it is ACTUALLY flying at: the space run tops out at 3200, and lerping from a literal 1750
         halved the speed in one frame (measured 3200 -> 1748 on stage 9's first brake frame, 1001c) */
      if(drawLaunch._brkV0==null) drawLaunch._brkV0=drawLaunch._spd||1750;
      const p=clamp(drawLaunch._pt/2.0,0,1);
      drawLaunch._spd=lerp(drawLaunch._brkV0,STAGE5_SPACE_CRUISE,_ease(p));
      drawLaunch._dist+=drawLaunch._spd*dt;                        /* level keeps scrolling in smoothly while braking */
      if(drawLaunch._pt>=2.0){ drawLaunch._phase='settle'; drawLaunch._pt=0; }
    }else{
      /* Constant deceleration over the distance LEFT, so the speed is LAUNCH_PLAY_SCROLL exactly when the level
         lands (v^2 = v1^2 + (v0^2-v1^2)*rem/S). It never falls below v1, so it cannot stall short of the join. */
      if(drawLaunch._brkV0==null){ drawLaunch._brkV0=drawLaunch._spd; drawLaunch._brkS=Math.max(1,LAUNCH_LAND-drawLaunch._dist); }
      const V0=drawLaunch._brkV0, V1=LAUNCH_PLAY_SCROLL, S=drawLaunch._brkS;
      const rem=Math.max(0,LAUNCH_LAND-drawLaunch._dist);
      drawLaunch._spd=Math.sqrt(V1*V1+Math.max(0,V0*V0-V1*V1)*rem/S);
      const step=drawLaunch._spd*dt;
      if(drawLaunch._dist+step>=LAUNCH_LAND){
        /* the travel past the join is level travel: spend it on mapScroll so not one frame stands still */
        const over=drawLaunch._dist+step-LAUNCH_LAND, _rng=(typeof levelScrollRange==='function')?levelScrollRange():0;
        drawLaunch._dist=LAUNCH_LAND; drawLaunch._spd=V1;
        mapScroll=_rng>0?Math.min(_rng,mapScroll+over):mapScroll+over;
        drawLaunch._phase='settle'; drawLaunch._pt=0;
      }else drawLaunch._dist+=step;
      drawLaunch._brkK=clamp(1-Math.max(0,LAUNCH_LAND-drawLaunch._dist)/S,0,1);
    }""")

# 6. settle / load / countdown: ground stages hold PLAY's speed
E("""    drawLaunch._pt+=dt; drawLaunch._spd=((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_COUNTDOWN_SCROLL);
    const _rng=(typeof levelScrollRange==='function')?levelScrollRange():0;
    mapScroll=_rng>0 ? Math.min(_rng,mapScroll+LAUNCH_COUNTDOWN_SCROLL*dt)
                     : mapScroll+LAUNCH_COUNTDOWN_SCROLL*dt;
    const skyLead=""",
"""    drawLaunch._pt+=dt; drawLaunch._spd=((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_PLAY_SCROLL);
    const _rng=(typeof levelScrollRange==='function')?levelScrollRange():0, _crawl=_space?LAUNCH_COUNTDOWN_SCROLL:LAUNCH_PLAY_SCROLL;
    mapScroll=_rng>0 ? Math.min(_rng,mapScroll+_crawl*dt)
                     : mapScroll+_crawl*dt;
    const skyLead=""")

E("""    drawLaunch._spd=_s6?STAGE6_SKY_CRUISE:((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_COUNTDOWN_SCROLL);
    const _rng=(typeof levelScrollRange==='function')?levelScrollRange():0;
    mapScroll=_rng>0?Math.min(_rng,mapScroll+drawLaunch._spd*dt):mapScroll+drawLaunch._spd*dt;""",
"""    drawLaunch._spd=_s6?STAGE6_SKY_CRUISE:((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_PLAY_SCROLL);
    const _rng=(typeof levelScrollRange==='function')?levelScrollRange():0;
    mapScroll=_rng>0?Math.min(_rng,mapScroll+drawLaunch._spd*dt):mapScroll+drawLaunch._spd*dt;""")

E("""    drawLaunch._spd=_s6?Math.max(STAGE6_SKY_CRUISE,(drawLaunch._spd||STAGE6_SKY_CRUISE)-700*dt):((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_COUNTDOWN_SCROLL);""",
"""    drawLaunch._spd=_s6?Math.max(STAGE6_SKY_CRUISE,(drawLaunch._spd||STAGE6_SKY_CRUISE)-700*dt):((run.stage===5||run.stage===9)?STAGE5_SPACE_CRUISE:LAUNCH_PLAY_SCROLL);""")

# 7. the ship: one size, every phase
E("""  let shipX=VW/2, shipY, suf='', shipH=62; // plain hull; the thruster is drawn live (drop 0808g)""",
"""  /* ONE SIZE FROM THE FIRST LAUNCH FRAME TO PLAY (1001c): the hull PLAY draws, never a cinematic 62/90/128
     that has to be shrunk back at GO. Motion carries the arrival; scale does not. */
  let shipX=VW/2, shipY, suf='', shipH=POSE.h; // plain hull; the thruster is drawn live (drop 0808g)""")

E("""    if(run.stage===9){const pe=_ease(clamp(dist/Math.max(1,SEG_B1*0.78),0,1));shipH=lerp(14,SPACE_SHIP_SIZE,pe);shipY=lerp(VH*0.30,VH*0.44,pe);}
    else if(_space){ // lifting off: the ship scales up as it rockets toward space
      const lift=_ease(clamp(dist/(SEG_B3),0,1)); shipH=lerp(62, 128, lift); shipY=lerp(VH*0.66, VH*0.30, lift); }""",
"""    if(run.stage===9){const pe=_ease(clamp(dist/Math.max(1,SEG_B1*0.78),0,1));shipH=SPACE_SHIP_SIZE;shipY=lerp(VH*0.30,VH*0.44,pe);}
    else if(_space){ // lifting off toward space - at play size; the climb is the motion
      const lift=_ease(clamp(dist/(SEG_B3),0,1)); shipY=lerp(VH*0.66, VH*0.30, lift); }""")

E("""    const k=_ease(clamp(drawLaunch._pt/2.0,0,1));
    shipY=_space?lerp(VH*0.42,VH*0.60,k):lerp(POSE.y+54,POSE.y+30,k);
    if(_space) shipH=lerp(run.stage===9?SPACE_SHIP_SIZE:128,SHIP_DRAW_H,k);""",
"""    const k=_space?_ease(clamp(drawLaunch._pt/2.0,0,1)):_ease(drawLaunch._brkK||0);
    shipY=_space?lerp(VH*0.42,VH*0.60,k):lerp(POSE.y+54,POSE.y+30,k);
    if(run.stage===9) shipH=SPACE_SHIP_SIZE;""")

E("""    shipY=_space?lerp(VH*0.60,POSE.y-42,k):lerp(POSE.y+30,POSE.y+20,k);
    shipH=lerp(62, POSE.h, k);""",
"""    shipY=_space?lerp(VH*0.60,POSE.y-42,k):lerp(POSE.y+30,POSE.y+20,k);
    shipH=POSE.h;""")

E("""  let _gravityDrawSize=Math.max(SPACE_SHIP_SIZE,shipH);""",
"""  let _gravityDrawSize=SPACE_SHIP_SIZE;   // the spaceship's own play size, whatever the plane beside it draws at (1001c)""")

E("""      else { shipH=lerp(S.fh,gph==='brake'?SHIP_DRAW_H:POSE.h,k); _gravityDrawSize=Math.max(SPACE_SHIP_SIZE,shipH); }""",
"""      else { shipH=lerp(S.fh,gph==='brake'?SHIP_DRAW_H:POSE.h,k); _gravityDrawSize=SPACE_SHIP_SIZE; }""")

# 8. stage 5's fury intro: plane and fighter at their play sizes
E("""const x=lerp(VW/2,pose.x,k),y=lerp(S.build?VH*.59:pose.y,pose.y,k),size=lerp(S.build?118:SPACE_SHIP_SIZE,SPACE_SHIP_SIZE,k);""",
"""const x=lerp(VW/2,pose.x,k),y=lerp(S.build?VH*.59:pose.y,pose.y,k),size=SPACE_SHIP_SIZE;   // play size throughout (1001c): no 118 px fighter shrunk to 48 at the countdown""")
E(""" if(S.build&&S.phase==='sky'&&gravityMode.partStartAge==null){drawShipSprite(x,y,90,'');}
 else if(furyShipReady())furyShipDrawPhase(G,x,y,size,90,_pilotKey());
 else drawShipSprite(x,y,90,'');""",
""" if(S.build&&S.phase==='sky'&&gravityMode.partStartAge==null){drawShipSprite(x,y,SHIP_DRAW_H,'');}
 else if(furyShipReady())furyShipDrawPhase(G,x,y,size,SHIP_DRAW_H,_pilotKey());
 else drawShipSprite(x,y,SHIP_DRAW_H,'');""")

# 9. the kit's orbit keeps Mike's approved spread; only the craft it locks onto is play-sized
E(""" const angle=base+(age-start)*.65+spin,radius=(92+(i%2)*45)*scale;
 let px=x+Math.cos(angle)*radius,py=y+Math.sin(angle)*radius*.65;
 if(phase==='scatter'||phase==='snap'){
  const s=phase==='scatter'?clamp(G.t/GRAVITY_SCATTER_DUR,0,1):1;
  px+=Math.cos(angle)*28*scale*s;py+=Math.sin(angle)*25*scale*s+12*scale*s*s;
 }""",
""" /* The orbit keeps the 118 px cinematic hull's spread Mike approved (0914), so the kit still circles wide and
    clear of the plane; only the craft it LOCKS onto is the play-sized one (1001c), so nothing shrinks at GO. */
 const oscale=Math.max(scale,FURY_ORBIT_HULL/128);
 const angle=base+(age-start)*.65+spin,radius=(92+(i%2)*45)*oscale;
 let px=x+Math.cos(angle)*radius,py=y+Math.sin(angle)*radius*.65;
 if(phase==='scatter'||phase==='snap'){
  const s=phase==='scatter'?clamp(G.t/GRAVITY_SCATTER_DUR,0,1):1;
  px+=Math.cos(angle)*28*oscale*s;py+=Math.sin(angle)*25*oscale*s+12*oscale*s*s;
 }""")
E("""const FURY_PART_START=3.1,FURY_PART_GAP=.54,FURY_PART_RISE=1.1;""",
"""const FURY_PART_START=3.1,FURY_PART_GAP=.54,FURY_PART_RISE=1.1;
const FURY_ORBIT_HULL=118;   // the cinematic hull the kit's orbit was laid out around (0914)""")

# 10. the plane holds its size through the kit's arrival and charge; it tucks only under the closing snap
E("""  if(phase==='drift') return planeH;
  if(phase==='charge'){ const q=clamp((t||0)/GRAVITY_CHARGE_DUR,0,1); return lerp(planeH,tuck,q*q*(3-2*q)); }
  return tuck;""",
"""  /* 1001c: no visible shrink while the kit orbits - the plane holds its play size through drift, charge and
     scatter, and tucks only during the snap, when the converging hardware closes over it. */
  if(phase==='drift'||phase==='charge'||phase==='scatter') return planeH;
  if(phase==='snap'){ const q=clamp((t||0)/GRAVITY_SNAP_DUR,0,1); return lerp(planeH,tuck,q*q*(3-2*q)); }
  return tuck;""")

# 11. the outbound routes drew the climbing ship at 38 against PLAY's 60
E("""    drawShipSprite(outboundScreenX(o), o.py, 38, '');
  /* the vortex over everything.""",
"""    drawShipSprite(outboundScreenX(o), o.py, SHIP_DRAW_H, '');   // play size (1001c), was 38
  /* the vortex over everything.""")
E("""    drawShipSprite(outboundScreenX(o), o.py, 38, '');      // plain hull + live thruster (drop 0808g)""",
"""    drawShipSprite(outboundScreenX(o), o.py, SHIP_DRAW_H, ''); // play size (1001c), was 38""")

# 12. the stage-8 arrival grew the ship out of the rift from 6 px
E("""sy=lerp(py+3,pose.y,k),sh=lerp(6,pose.h,k);""",
"""sy=lerp(py+3,pose.y,k),sh=pose.h;   // out of the rift at play size (1001c), never grown from a 6 px speck""")

E(""" px=lerp(x+((i%3)-1)*52,px,entry);py=lerp(VH+size*1.8,py,entry);
 const e=snap*snap;px=lerp(px,x+q.x*scale,e);py=lerp(py,y+q.y*scale,e);
 return {key:q.key+'_top',x:px,y:py,rotation:(base+sign*elapsed*.9)*(1-e),size:size*(q.partScale||1)*lerp(1.65,1,snap),entry};""",
""" const osize=Math.max(size,FURY_ORBIT_HULL);   // the kit flies at its approved 0914 size and closes onto the play-sized craft in the snap
 px=lerp(x+((i%3)-1)*52,px,entry);py=lerp(VH+osize*1.8,py,entry);
 const e=snap*snap;px=lerp(px,x+q.x*scale,e);py=lerp(py,y+q.y*scale,e);
 return {key:q.key+'_top',x:px,y:py,rotation:(base+sign*elapsed*.9)*(1-e),size:(q.partScale||1)*lerp(osize*1.65,size,snap),entry};""")

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit('REFUSED: anchor matched %d times:\n%s' % (n, old[:200]))
for old, new in EDITS:
    src = src.replace(old, new)
open(P, 'wb').write(src.encode('utf8'))
print('applied', len(EDITS), 'edits')
