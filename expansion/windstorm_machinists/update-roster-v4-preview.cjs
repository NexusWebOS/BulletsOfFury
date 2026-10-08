const fs=require('fs'),path=require('path'),root=__dirname;
const p=path.join(root,'preview.html');let s=fs.readFileSync(p,'utf8');
for(const who of ['wren','rolf','chaz'])s=s.replaceAll('identity/'+who+'_portrait_v3.png','identity/'+who+'_portrait_v4.png').replaceAll('identity/'+who+'_front.png','identity/'+who+'_front_v4.png');
s=s.replaceAll('previews/machinists_v2.png','previews/machinists_v4.png').replace(/Practical haircuts, weathered faces, worn workwear, and distinct crew identities\.[^<]+/,'Wren wears black and white armor. Rolf has blue hair and a blue outfit. Chaz retains blond hair, now with a red forehead bandana and red outfit. Their grounded faces and current game portrait frames are preserved.');
fs.writeFileSync(p,s);
for(const file of ['README.md','COVERAGE.md']){const f=path.join(root,file);let d=fs.readFileSync(f,'utf8');d=d.replace('38 unmodified generation masters','39 unmodified generation masters').replaceAll('38 preserved masters','39 preserved masters');if(!d.includes('ROSTER_V4.md'))d+='\nThe selected [Machinist appearance revision](ROSTER_V4.md) gives Rolf blue hair/blue clothing, Wren black/white armor, and blond Chaz a red outfit and forehead bandana. Selected portraits, avatars and full-body poses use versioned v4 exports.\n';fs.writeFileSync(f,d);}
console.log('Preview and index select appearance revision 4');
