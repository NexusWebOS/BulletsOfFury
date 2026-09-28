// Runs the suite's own boot (everything before section 1) and then only the named test modules.
//   node _BUILD_SOURCE/run_section_0928.js test_encounter_upgrades_0928.cjs
// A development convenience for iterating on one section; the full test_fl.js remains the gate.
const fs=require('fs'),path=require('path'),vm=require('vm');
const src=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const cut=src.indexOf("console.log('\\n=== 1. manifest / asset keys ===');");
if(cut<0)throw new Error('boot marker not found');
const mods=process.argv.slice(2);
const tail=`\n${mods.map(m=>`require('./${m}')(vm,ctxv,ok);`).join('\n')}\n`+
  `console.log(errors.length?('FAILED — '+errors.length+'\\n'+errors.join('\\n')):'SECTION OK');process.exit(errors.length?1:0);\n`;
const code=src.slice(0,cut)+tail;
const file=path.join(__dirname,'_run_section_tmp.js');fs.writeFileSync(file,code);
try{require(file);}finally{try{fs.unlinkSync(file);}catch(_){}}
