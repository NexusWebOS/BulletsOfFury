const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p);
function once(old,replacement,label){const a=Buffer.from(old,'ascii'),b=Buffer.from(replacement,'ascii'),at=s.indexOf(a);if(at<0)throw new Error(label+' anchor missing');if(s.indexOf(a,at+a.length)>=0)throw new Error(label+' anchor repeated');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
once(
"    +\"var p0=beat(.90,2),p1=beat(.70,10),p2=beat(.45,24),p3=beat(.20,48),node=b._mega.nodes[0],pos=carrierMegaNodePos(b,node),hit=carrierMegaNodeAt(b,pos.x,pos.y)===node;\"\r\n",
"    +\"var p0=beat(.90,2),c0=!!b._mega.cycloneFan,p1=beat(.70,10),p2=beat(.45,24),p3=beat(.20,48),node=b._mega.nodes[0],pos=carrierMegaNodePos(b,node),hit=carrierMegaNodeAt(b,pos.x,pos.y)===node;\"\r\n",
'capture opening warning');
once(
"    +\"carrierMegaNodeDamage(b,node,99);var first=node.hp===1&&!node.dead;carrierMegaNodeDamage(b,node,99);return JSON.stringify({p:[p0,p1,p2,p3],phase:b._mega.phase,nodes:b._mega.nodes.length,hit:hit,first:first,dead:node.dead,fl:_navalFlashes.length});})()\",ctxv));\r\n",
"    +\"carrierMegaNodeDamage(b,node,99);var first=node.hp===1&&!node.dead;carrierMegaNodeDamage(b,node,99);return JSON.stringify({p:[p0,p1,p2,p3],c0:c0,phase:b._mega.phase,nodes:b._mega.nodes.length,hit:hit,first:first,dead:node.dead,fl:_navalFlashes.length});})()\",ctxv));\r\n",
'return opening warning');
once(
"  ok(_mega269.p[0].indexOf('s6cyclone')>=0,\r\n     'the carrier opens on shield-up cyclone rakes between warheads');\r\n",
"  ok(_mega269.c0&&_mega269.p[0].indexOf('s6cyclone')<0,\r\n     'the carrier opens its shield-up cyclone rake through a committed shared warning');\r\n",
'update carrier opening contract');
if(!s.includes(13))throw new Error('test_fl CRLF lost');fs.writeFileSync(p,s);console.log('PATCHED_STAGE6_CARRIER_CYCLONE_REGRESSION_0916');
