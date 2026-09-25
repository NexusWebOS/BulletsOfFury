"""Align legacy encounter assertions with the authored Stage 7 Warden and Stage 5 HP budget."""
from pathlib import Path

p = Path('_BUILD_SOURCE/test_fl.js')
b = p.read_bytes()
assert b'\r\n' in b

old = ("  var _boss270=JSON.parse(vm.runInContext(\"(function(){run.stage=7;curStage=STAGES[6];player.x=250;player.y=500;var b={x:240,y:118,_drawY:118,w:220,h:216,maxhp:300,hp:300,dead:false,flash:0};shipBossInit(b,'sludgeemperor');var out=[];[.9,.65,.4,.15].forEach(function(f){eBullets.length=0;b.hp=b.maxhp*f;b._sbStep=0;shipBossAttack(b);var warned=!!b._s7Flood;if(warned)for(var i=0;i<150;i++)sludgeFloodTick(b,1/60);out.push({k:eBullets.map(function(q){return q.kind;}),warned:warned});b._s7Flood=null;});return JSON.stringify(out);})()\",ctxv));\r\n"
       "  ok(_boss270[0].k.indexOf('s7acid')>=0&&_boss270[1].warned&&_boss270[1].k.indexOf('s7sludge')>=0&&_boss270[2].k.indexOf('s7acid')>=0&&_boss270[3].k.indexOf('s7laser')>=0&&_boss270[3].k.indexOf('s7grenade')>=0,'Sludge Emperor advances through pressure, warned flood, crown and reactor-purge phases');\r\n"
       "  ok(vm.runInContext(\"SHIPBOSS.sludgeemperor.pats.length===4&&SHIPBOSS.sludgeemperor.hpMul>=1.6&&SUBBOSS[7].kind==='dualscoopdredger'\",ctxv),'Stage 7 has a reinforced four-phase boss and the supplied dedicated miniboss');")
new = ("  var _warden270=JSON.parse(vm.runInContext(\"(function(){run.stage=7;curStage=STAGES[6];var b={x:240,y:118,_drawY:118,w:220,h:216,maxhp:300,hp:300,dead:false,flash:0};shipBossInit(b,'sludgeemperor');return JSON.stringify({name:b.name,phase:b._s7warden&&b._s7warden.final.phase,coreHp:b._s7warden&&b._s7warden.final.cores.map(function(c){return c.hp;}),noHit:b._s7warden&&b._s7warden.noHit,barHidden:b._s7FinalNoBar});})()\",ctxv));\r\n"
       "  ok(_warden270.name==='TOXIC PORTAL WARDEN'&&_warden270.phase==='portalClose'&&_warden270.coreHp.length===2&&_warden270.coreHp.every(function(n){return n>0;})&&_warden270.noHit&&_warden270.barHidden,'Toxic Portal Warden starts in its protected portal entrance with two separate reactor cores');\r\n"
       "  ok(vm.runInContext(\"SHIPBOSS.sludgeemperor.pat==='s7warden'&&SHIPBOSS.sludgeemperor.hpMul>=1.6&&SUBBOSS[7].kind==='dualscoopdredger'\",ctxv),'Stage 7 fields its dedicated Warden director and Dual Scoop Dredger miniboss');")
old, new = old.encode(), new.encode()
assert b.count(old) == 1
b = b.replace(old, new)
old = b"SHIPBOSS.xenoregent.pats.length===4&&SHIPBOSS.xenoregent.hpMul>=1.6&&SUBBOSS[5].kind==='chaosharrier'"
new = b"SHIPBOSS.xenoregent.pats.length===4&&SHIPBOSS.xenoregent.hpMul===1&&SUBBOSS[5].kind==='chaosharrier'"
assert b.count(old) == 1
b = b.replace(old, new)
old = b"'Stage 5 keeps the approved Chaos Harrier and gains a reinforced four-phase boss'"
new = b"'Stage 5 keeps the Chaos Harrier and four-phase Regent on the single-scaled HP budget'"
assert b.count(old) == 1
b = b.replace(old, new)
p.write_bytes(b)
