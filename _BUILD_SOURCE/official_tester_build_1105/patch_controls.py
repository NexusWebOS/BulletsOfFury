from pathlib import Path
import re
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');src=(W/'game.before.js').read_bytes().decode('utf8');assert '\r\n'not in src
start=src.index('/* ⚠ THE MOUSE DEFAULTS ARE ADDED');end=src.index('/* ⚠ START IS THE PAUSE BUTTON',start)
src=src[:start]+'''/* November 5 tester layout: right-click Retina, Space missiles, physical mouse
   button 4 (browser button 3) Multi-Retina. Double-tap right-click and hold the
   second press also scans multiple targets. Keyboard and controller alternatives
   remain available and future custom rebindings remain authoritative. */
'''+src[end:]
start=src.index('/* ⚠ THE TWO SIDE MOUSE BUTTONS');end=src.index('const KEYBIND_DEFAULT=',start)
src=src[:start]+'''/* Physical mouse button 5 remains Charge (browser button 4 / mouse4).
   Existing profiles migrate these three physical controls once, below. */
'''+src[end:]
src=src.replace("bomb:['k','mouse2','pad_b1','pad_b6'],retina:['c',' ','mouse3','pad_b5'],multilock:['y','pad_b3']","bomb:['k',' ','pad_b1','pad_b6'],retina:['c','mouse2','pad_b5'],multilock:['y','mouse3','pad_b3']",1)
needle='function saveKeybind(){'
migration='''function upgradeMouseControls1105(){
  try{if(localStorage.getItem('bof_mouse_controls_1105')==='1')return;}catch(_){}
  const reserved=[' ','mouse2','mouse3'];
  for(const action of Object.keys(KEYBIND_DEFAULT)){
    const old=keybind[action]||[];keybind[action]=old.filter(k=>!reserved.includes(k));
    if(!keybind[action].length)keybind[action]=KEYBIND_DEFAULT[action].filter(k=>!reserved.includes(k));
  }
  for(const [action,key]of [['bomb',' '],['retina','mouse2'],['multilock','mouse3']])keybind[action].push(key);
  try{localStorage.setItem('bof_keys',JSON.stringify(keybind));localStorage.setItem('bof_mouse_controls_1105','1');}catch(_){}
}
upgradeMouseControls1105();
'''
assert needle in src;src=src.replace(needle,migration+needle,1)
needle='  const keys={}, pressed={};';src=src.replace(needle,needle+'''
  const mouseRetina={lastUp:-1e9,downAt:0,multi:false};
  function cancelMouseRetina(){
    mouseRetina.lastUp=-1e9;mouseRetina.downAt=0;mouseRetina.multi=false;
    for(const k of ['mouse2','mouse3']){keys[k]=false;pressed[k]=false;}
  }
''',1)
src=src.replace('clearTaps(); mouse.down=false;','clearTaps(); mouse.down=false; cancelMouseRetina();',1)
start=src.index('     Mike\'s tester: "Add mouse buttons');end=src.index('     ⚠ NO NEW INPUT PLUMBING',start)
src=src[:start]+'''     Current mouse profile: left-click fires, right-click Retina, button 4
     Multi-Retina and button 5 Charge. Space launches missiles.

'''+src[end:]
old='''    const mk=MOUSE_KEY[e.button|0]; if(mk) mkey(mk,true);
    mpos(e);'''
new='''    const button=e.button|0,mk=MOUSE_KEY[button],fresh=mk&&!keys[mk];
    if(mk)mkey(mk,true);
    if(button>=2&&button<=4)e.preventDefault();
    if(button===2&&fresh){
      const now=performance.now(),allowed=state===GS.PLAY&&(keybind.retina||[]).includes('mouse2');
      mouseRetina.multi=allowed&&now-mouseRetina.lastUp<=300;
      mouseRetina.downAt=now;mouseRetina.lastUp=-1e9;
      // The second press belongs to the native scan, not single-target cycleLock.
      if(mouseRetina.multi)pressed.mouse2=false;
    }
    mpos(e);'''
assert old in src;src=src.replace(old,new,1)
old='''    const mk=e?MOUSE_KEY[e.button|0]:null;
    if(mk) mkey(mk,false); else for(const k of MOUSE_KEY) mkey(k,false); });'''
new='''    const button=e?e.button|0:-1,mk=e?MOUSE_KEY[button]:null;
    if(mk&&keys[mk]&&button>=2&&button<=4)e.preventDefault();
    if(button===2){
      const now=performance.now();
      mouseRetina.lastUp=keys.mouse2&&!mouseRetina.multi&&state===GS.PLAY&&now-mouseRetina.downAt<=250?now:-1e9;
      mouseRetina.multi=false;
    }
    if(mk)mkey(mk,false);else{for(const k of MOUSE_KEY)mkey(k,false);cancelMouseRetina();} });
  cv.addEventListener('auxclick',e=>{if(e.button===3||e.button===4)e.preventDefault();});'''
assert old in src;src=src.replace(old,new,1)
src=src.replace('Binding missiles to button 2 is useless','Binding Retina to button 2 is useless',1)
# Space is a fixed menu Confirm key even though it is now a combat missile key.
needle="k=>!/^mouse\\d/.test(k)&&k!=='backspace'&&ok(k)"
assert needle in src;src=src.replace(needle,"k=>!/^mouse\\d/.test(k)&&k!=='backspace'&&k!==' '&&ok(k)",1)
needle='  return {keys,mouse,down,tap,clearTaps,pollGamepad,'
replace='''  return {keys,mouse,down,tap,clearTaps,cancelMouseRetina,
    get mouseMultiRetina(){return mouseRetina.multi&&state===GS.PLAY&&!!keys.mouse2&&(keybind.retina||[]).includes('mouse2');},
    pollGamepad,'''
assert needle in src;src=src.replace(needle,replace,1)
old="function retinaScanHeld(){const K=keybindFor(_seat);return (K.multilock||[]).some(k=>Input.down(k));}"
new="function retinaScanHeld(){const K=keybindFor(_seat);return (K.multilock||[]).some(k=>Input.down(k))||(_seat===1&&Input.mouseMultiRetina);}"
assert old in src;src=src.replace(old,new,1)
needle='  const _prevState=state;';assert needle in src;src=src.replace(needle,needle+'\n  if(s!==state)Input.cancelMouseRetina();',1)
# Keep the actual in-game control sheet consistent with both this profile and
# later remapping; existing authored mouse/keycap art remains unchanged.
needle="  const mouse=[['input_mouse_left_0915','FIRE','#ff796d'],\n               ['input_mouse_right_0915','MISSILE','#ff796d'],"
replacement="  const boundName=k=>{const pair=[['fire','FIRE'],['bomb','MISSILE'],['retina','RETINA'],['multilock','MULTI-RETINA'],['charge','CHARGE']].find(([a])=>(keybind[a]||[]).includes(k));return pair?pair[1]:'-';};\n  const mouse=[['input_mouse_left_0915',boundName('mouse0'),'#ff796d'],\n               ['input_mouse_right_0915',boundName('mouse2'),'#ff796d'],"
assert needle in src;src=src.replace(needle,replacement,1)
src=src.replace("helpLabel('MOUSE 4: RETINA   MOUSE 5: CHARGE',VW/2,VH*.905,11,'#9fd6ff');","helpLabel('MOUSE 4: '+boundName('mouse3')+'   MOUSE 5: '+boundName('mouse4'),VW/2,VH*.905,11,'#9fd6ff');",1)
src=src.replace("helpLabel('HOLD '+helpBind('multilock',2)+' TO SCAN MULTIPLE TARGETS',VW/2,VH*.937,11,'#ffd36b');","helpLabel('SPACE: '+boundName(' ')+'   '+((keybind.retina||[]).includes('mouse2')?'DOUBLE RIGHT-CLICK + HOLD: MULTI':'HOLD '+helpBind('multilock',2)+' TO SCAN'),VW/2,VH*.937,11,'#ffd36b');",1)
(W/'game.js').write_text(src,encoding='utf8',newline='\n')
index=(R/'index.html').read_bytes();m=re.search(rb'(assets/game\.js\?v=)[^"\x27>]+',index);assert m;index=index[:m.start()]+m[1]+b'official-mouse-1105'+index[m.end():];(W/'index.html').write_bytes(index)
print('Prepared mouse controls, one-time migration, gesture lifecycle and cache refresh.')
