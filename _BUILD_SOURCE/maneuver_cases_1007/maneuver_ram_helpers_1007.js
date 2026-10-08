
/* Sovereign's ram must warn for the same footprint that can hit the pilot.
   Its shield is wider than the hull; weapon loss can leave that shield intact. */
function maneuverRamRadius(b){
 const S=b._s4war,H=S?.shield;
 let radius=b.w*(H&&(H.active||H.rearming) ? .67 : .5);
 if(H?.active)for(const n of H.nodes||[])if(!n.dead)radius=Math.max(radius,Math.abs(n.x-b.x)+36);
 for(const t of S?.coreTurrets||[])if(!t.dead&&t.materialize>=1)radius=Math.max(radius,Math.abs(t.x-b.x)+Math.max(36,(t.w||0)/2));
 return radius;
}
function maneuverRamWarm(b,base,E){
 const P=MANEUVER_SAFETY_1007.profiles[diffKey]||MANEUVER_SAFETY_1007.profiles.normal;
 // Near an edge, escaping inward crosses the assembly's swept horizontal span.
 const sweep=E?Math.abs(E.tx-E.ox):0;
 return Math.max(base,P.reaction+(maneuverRamRadius(b)+P.pad+sweep)/(MANEUVER_SAFETY_1007.slowSpeed*1.35)+.12);
}
function maneuverRamWidth(b){return 2*maneuverRamRadius(b)+6;}
