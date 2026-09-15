const fs=require('fs');
const file=require('path').resolve(__dirname,'test_fl.js');
let src=fs.readFileSync(file,'utf8');
const lines=["require('./test_retina_audit_0915.cjs')(vm,ctxv,ok);","require('./test_elemental_absorb_0915.cjs')(vm,ctxv,ok);"];
if(lines.every(line=>src.includes(line))){console.log('Retina and elemental suite hooks already present.');process.exit(0);}
const marker='// ===== 305. DIRECTIONAL RETINA SCAN, 0914 =====';
if(!src.includes(marker))throw new Error('section 305 marker not found');
const eol=src.includes('\r\n')?'\r\n':'\n';
for(const line of lines)if(!src.includes(line))src=src.replace(marker,line+eol+eol+marker);
fs.writeFileSync(file,src,'utf8');
if(eol==='\r\n'&&!fs.readFileSync(file,'utf8').includes('\r\n'))throw new Error('CRLF lost');
console.log('Added Retina audit tests to the complete suite.');
