const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'test_fl.js'),s=fs.readFileSync(p,'utf8');
if(/(^|[^\r])\n/.test(s))throw new Error('suite must remain CRLF');
const backup=path.join(__dirname,'..','_shots','overlord_eight_beat_warning_0915','recovery','test_fl.js.pre-fixture');
fs.mkdirSync(path.dirname(backup),{recursive:true});fs.writeFileSync(backup,s,'utf8');
const old="    +\"for(var i=0;i<35;i++)updateOverlordX(b,1/60);var lane=b._chargeTell.lane,locked=b._chargeTell.locked,glow=b._ovChargeGlow,warn=b._combatWarnings&&b._combatWarnings['overlord-charge'];\"\r\n"+
"    +\"player.x=410;for(var j=0;j<16;j++)updateOverlordX(b,1/60);var held=b._chargeTell.lane;\"\r\n"+
"    +\"while(b._ovState==='chargeTell')updateOverlordX(b,1/60);player.x=80;for(var k=0;k<14;k++)updateOverlordX(b,1/60);\"\r\n"+
"    +\"return JSON.stringify({lane:lane,held:held,locked:locked,glow:glow,warn:warn?{t:warn.t,warm:warn.warm,arrow:warn._arrowN}:null,state:b._ovState,x:b.x});})()\",ctxv));\r\n"+
"  ok(_charge265.warn&&_charge265.warn.t>0.5&&_charge265.warn.warm===1.08&&_charge265.warn.arrow>=1,\r\n";
const neu="    +\"for(var i=0;i<50;i++)updateOverlordX(b,1/60);var lane=b._chargeTell.lane,locked=b._chargeTell.locked,glow=b._ovChargeGlow,warn=b._combatWarnings&&b._combatWarnings['overlord-charge'],beat=b._chargeTell.beat;\"\r\n"+
"    +\"player.x=410;for(var j=0;j<16;j++)updateOverlordX(b,1/60);var held=b._chargeTell.lane;\"\r\n"+
"    +\"while(b._ovState==='chargeTell')updateOverlordX(b,1/60);player.x=80;for(var k=0;k<14;k++)updateOverlordX(b,1/60);\"\r\n"+
"    +\"return JSON.stringify({lane:lane,held:held,locked:locked,glow:glow,beat:beat,warn:warn?{t:warn.t,warm:warn.warm}:null,state:b._ovState,x:b.x});})()\",ctxv));\r\n"+
"  ok(_charge265.warn&&_charge265.warn.t>0.8&&_charge265.warn.warm===1.60&&_charge265.beat>=4,\r\n";
const n=s.split(old).length-1;if(n!==1)throw new Error('fixture expected once, got '+n);
const out=s.replace(old,neu);if(/(^|[^\r])\n/.test(out))throw new Error('suite endings changed');fs.writeFileSync(p,out,'utf8');
console.log('updated Overlord warning fixture for eight-beat cadence');
