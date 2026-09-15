const fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.resolve(__dirname,'..'),src=fs.readFileSync(path.join(root,'assets/game.js'),'utf8');
let passed=0,failed=0,checks=[];function ok(name,v){checks.push({name,ok:!!v});v?passed++:failed++;}
const files=['mouse_neutral.png','mouse_left_click.png','mouse_right_click.png','mouse_wheel.png','key_spacebar.png','key_r.png'];
for(const f of files)ok(f+' exists',fs.existsSync(path.join(root,'assets/game/ui/input_prompts_0915',f)));
for(const k of ['input_mouse_neutral_0915','input_mouse_left_0915','input_mouse_right_0915','input_mouse_wheel_0915','input_key_space_0915','input_key_r_0915'])ok(k+' registered',src.includes(k));
ok('help page renders all four mouse states',src.includes("['input_mouse_neutral_0915','POINTER']")&&src.includes("['input_mouse_wheel_0915','WHEEL']"));
ok('mouse buttons map to pressed art',src.includes("mouse0:'input_mouse_left_0915'")&&src.includes("mouse2:'input_mouse_right_0915'"));
ok('space and R keys map to authored art',src.includes("' ':'input_key_space_0915'")&&src.includes("r:'input_key_r_0915'"));
ok('options uses generated prompt mapper',src.includes('inputPromptArt(_shownBind)'));
console.log(JSON.stringify({passed,failed,checks},null,2));process.exitCode=failed?1:0;
