const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];function check(ok,name){checks.push({name,ok:!!ok});if(!ok)throw Error(name);}
 const saved=keybind.bomb.slice(),startSaved=keybind.start.slice();
 function tap(key,fn){Input.clearTaps();Input.injectTap(key);return fn();}
 keybind.bomb=['u','mouse2'];
 check(tap('u',Input.menuBack),'remapped keyboard B backs out');
 check(tap('pad_b1',Input.menuBack),'physical controller B backs out');
 check(!tap('backspace',Input.menuBack),'Backspace is not navigation');
 check(!tap('mouse2',Input.menuBack),'mouse binding does not trigger unrelated menu navigation');
 keybind.start=['o','pad_b9'];check(tap('o',Input.menuStart),'remapped Start works');
 check(tap('pad_b9',Input.menuConfirm),'controller Start confirms');
 keybind.bomb=saved;keybind.start=startSaved;
 for(const name of ['HELP','CREDITS','DIFF','MODESEL','OPTIONS','PASSWORD']){
  Input.clearTaps();setState(GS[name]);if(name==='OPTIONS'){rebindAction=null;optSnap=null;}if(name==='PASSWORD')drawPassword.typing=false;
  Input.injectTap('backspace');check(!menuBackTick()&&state===GS[name],name+' ignores Backspace navigation');
  Input.clearTaps();Input.injectTap('pad_b1');check(menuBackTick()&&state===GS.TITLE,name+' B returns to title');
 }
 setState(GS.OPTIONS);rebindAction='fire';Input.clearTaps();Input.injectTap('pad_b1');
 check(!menuBackTick()&&Input.tap('pad_b1'),'rebinding owns B until capture finishes');rebindAction=null;
 setState(GS.PASSWORD);drawPassword.typing=true;pwInput='';pwKey('BACK');
 check(state===GS.PASSWORD&&pwInput==='','delete on empty password does not exit');
 pwInput='ABC';pwKey('BACK');check(pwInput==='AB','delete removes exactly one character');
 Input.clearTaps();Input.injectTap('k');check(!menuBackTick()&&Input.tap('k'),'typing owns the keyboard B letter');
 const glyph=helpGlyph,text=msgTextLeft,images=[],labels=[];
 helpGlyph=(k)=>images.push(k);msgTextLeft=(s)=>labels.push(s);
 for(const name of ['TITLE','DIFF','OPTIONS','PASSWORD']){state=GS[name];menuControlFooter();}
 controlHintRow([['pad_dpad','PILOT'],['pad_a','LAUNCH'],['pad_b','BACK']]);
 helpGlyph=glyph;msgTextLeft=text;
 check(['pad_dpad','pad_a','pad_b','pad_start'].every(k=>images.includes(k)),'shared menu rows use authored D-pad, A, B and Start assets');
 check(labels.includes('BACK')&&!labels.some(s=>/BKSP|BACKSPACE|K BACK|ENTER =/.test(s)),'captions describe actions without conflicting physical keys');
 check(['pad_dpad','pad_a','pad_b','pad_c','pad_y','pad_start'].every(k=>BOFX.cells[k]&&BOFX.cells[k][0]==='ui_help'),'all control icons resolve to the inspected generated Help atlas');
 Input.clearTaps();return {passed:checks.length,failed:0,checks};
})()\`,ctxv);
console.log(JSON.stringify(result,null,2));
`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
